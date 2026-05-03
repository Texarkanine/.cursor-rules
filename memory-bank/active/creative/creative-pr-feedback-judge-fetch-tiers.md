# Decision: PR Feedback Judge — GitHub Fetch Tier Strategy

## Context

**What needs to be decided.** The command's GitHub-access strategy. The original plan assumed `gh` CLI is universally available and authenticated. That's false for the actual audience: anyone with Cursor (and via `a16n`, anyone with Claude Code) on any machine, including a "drive-by review" use case where the user is curious about a public PR but has no GitHub tooling installed and no auth.

**Why it matters.** The command must work, with graceful degradation, on:
1. Local dev box with `gh` installed and authenticated to a personal account.
2. CI / sandbox / fresh machine with `curl` only — no `gh`, no auth.
3. An agent harness that has its own URL-fetch tool (Cursor's web fetch, Claude Code's `WebFetch`, etc.) but no shell tooling installed at all.

If the command demands `gh`, it fails outright in cases 2 and 3 — which is exactly the most interesting "drop-in" use case.

**Constraints.**
1. Public PRs MUST be reviewable on a vanilla machine with no GitHub auth (this is the "drive-by" requirement).
2. Private PRs MUST work when `gh` is installed and authenticated, and MUST fail with a clear, actionable error otherwise.
3. The strategy must be detectable at runtime — the command body tells the agent how to probe & pick, not "you have gh, use it."
4. Whatever tier is chosen, output to the LLM must be JSON or otherwise structured-ish — feeding the agent raw 200KB of GitHub HTML to extract one comment is the failure mode we're trying to avoid (per `script-it-instead`).
5. The tier strategy must compose with the batch-fetch discipline — one script per invocation, regardless of which tier it picks.

## Options Evaluated

The space is a chain, not a set. Each tier is strictly better than the next on output quality and strictly worse on availability. The real decision is which tiers to include and the detection/fallback wiring.

- **T1 — `gh` CLI**: `gh api repos/.../pulls/comments/123 --jq '...'`. Authenticated. Clean JSON. Handles pagination via `--paginate`. Best when present; absent on most fresh machines.
- **T2 — Anonymous REST (`curl` + `jq`)**: `curl -fsS https://api.github.com/repos/.../pulls/comments/123 | jq '...'`. Identical JSON shape to T1 (because gh wraps this API). Public PRs only. 60 requests/hour anonymous rate limit, which is plenty for one PR review. `jq` is much more commonly installed than `gh`.
- **T3 — Anonymous REST without `jq`**: same `curl`, but pipe to a runtime stdlib (Python's `json` module via `python3 -c …`). Trades one tool dependency (`jq`) for another (`python3` or `node`), both more universal than `gh`.
- **T4 — Harness web-fetch + LLM extraction**: invoke the harness's URL fetch tool (e.g. `WebFetch`) on the comment URL, get markdown-converted HTML, let the LLM pluck out the body. Always available (the harness *is* the runtime), but produces noisy output and burns context. The user's note explicitly identified this as the "very noisy" floor.
- **T5 — Harness web-fetch on the API URL**: invoke the harness's URL fetch tool on the *API* URL (`https://api.github.com/repos/.../pulls/comments/123`) instead of the human page. The fetch tool returns the JSON body verbatim. This is the elegant fallback when no shell tooling exists at all — same data quality as T1/T2/T3, no auth, no shell.

## Analysis

| Criterion | T1 gh | T2 curl+jq | T3 curl+stdlib | T4 web-fetch HTML | T5 web-fetch API |
|---|---|---|---|---|---|
| Public PRs | ✅ | ✅ | ✅ | ✅ | ✅ |
| Private PRs | ✅ | ❌ | ❌ | ❌ | ❌ |
| Output quality | Clean JSON | Clean JSON | Clean JSON | Noisy markdown | Clean JSON |
| Availability on fresh machine | Rare | Common | Very common | Universal | Universal |
| Rate limit headroom | 5000/hr | 60/hr | 60/hr | Harness-dependent | 60/hr (anon) |
| Composes with batch-fetch | ✅ paginate | ✅ link header | ✅ link header | ⚠️ one URL per call | ⚠️ one URL per call |
| Auth required | Yes | No | No | No | No |

**Key insights:**
- T1, T2, T3, and T5 all return the **same JSON shape** because they all hit the same REST API. That means the *parsing & template-rendering* logic in the command body is tier-agnostic — only the fetch invocation changes.
- T2 and T3 are essentially the same tier with different tool prefs. Including both as alternatives within one tier (`jq` if present, else stdlib) gives ~universal coverage of fetch-once parsing without bloating the chain.
- T4 (HTML scrape) is dominated by T5 (API JSON via the same web-fetch tool). The user's example URL `https://github.com/Texarkanine/a16n/pull/97#discussion_r3177417607` and its API equivalent `https://api.github.com/repos/Texarkanine/a16n/pulls/comments/3177417607` are both reachable by any fetch tool; T5 is strictly better. **T4 should not appear in the chain.**
- T5 has one practical wrinkle: pagination. Whole-PR runs need 3 list endpoints, and listing comments on a busy PR can paginate. `Link:` headers may not survive harness web-fetch (some tools strip them). Mitigation: in T5 mode, the command instructs the agent to use the explicit `?per_page=100&page=N` cursor and stop when a page returns `[]` — works without needing the Link header.
- Private repos in T2/T3/T5 fail with a 404 (not 401, deliberately, to avoid leaking existence). The command body must catch this and translate to "this looks like a private PR — install `gh` and run `gh auth login`, or paste the comment text directly."

**What dominates:**
- T1 is best when present. Detect with `command -v gh >/dev/null && gh auth status >/dev/null 2>&1`.
- T2/T3 collapse into a single "shell + fetch + structured-parse" tier. Detect with `command -v curl`, then `command -v jq` decides which parser.
- T5 is the universal floor. Detect by: shell unavailable OR no `curl`.
- T4 is dropped.

## Decision

**Selected**: a three-tier ordered fallback chain — **T1 → T2/T3 → T5** — with explicit detection probes and a unified failure message for private PRs in unauthenticated tiers.

**Rationale**: Satisfies all five constraints. Public PRs work everywhere (T1, T2, T3, or T5 — at least one is always available because the harness itself qualifies as T5). Private PRs work in T1 and fail loudly with actionable guidance otherwise. The command body's parsing logic stays simple because all three remaining tiers return the same JSON shape — only the *invocation* differs.

**Tradeoff**: Slightly more boilerplate in the command body (the detection block + three `gh` / `curl` / web-fetch invocation recipes for the same logical operation). Acceptable because the tradeoff is "one extra paragraph in a rule file" against "command silently breaks for the majority of the audience."

## Implementation Notes

### Detection block (command body emits as one shell line plus a fallback note)

```bash
# Tier detection — run once at command start
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  TIER=gh
elif command -v curl >/dev/null 2>&1; then
  if command -v jq >/dev/null 2>&1; then TIER=curl_jq; else TIER=curl_stdlib; fi
else
  TIER=webfetch
fi
```

If shell itself is unavailable to the agent (rare but possible in some restricted harness modes), `TIER=webfetch` is the agent's only choice and it must use the harness web-fetch tool directly on `api.github.com` URLs.

### URL→API mapping (now tier-agnostic, since the JSON path is identical)

| URL fragment | API path (relative to `https://api.github.com`) |
|---|---|
| (none) — `…/pull/N` | `/repos/{o}/{r}/pulls/{N}/comments?per_page=100` + `/repos/{o}/{r}/issues/{N}/comments?per_page=100` + `/repos/{o}/{r}/pulls/{N}/reviews?per_page=100` |
| `#pullrequestreview-{rid}` | `/repos/{o}/{r}/pulls/{N}/reviews/{rid}` + `/repos/{o}/{r}/pulls/{N}/reviews/{rid}/comments?per_page=100` |
| `#discussion_r{cid}` | `/repos/{o}/{r}/pulls/comments/{cid}` |
| `#issuecomment-{cid}` | `/repos/{o}/{r}/issues/comments/{cid}` |

Per-tier invocation recipes (the command body shows one example for each operation in each tier; the rest is mechanical):

- T1 (gh): `gh api 'repos/{o}/{r}/pulls/comments/{cid}'` (and `--paginate` for list endpoints)
- T2 (curl+jq): `curl -fsS "https://api.github.com/repos/{o}/{r}/pulls/comments/{cid}" | jq '.'`
- T3 (curl+stdlib): `curl -fsS … | python3 -c 'import json, sys; …'`
- T5 (webfetch): use the harness web-fetch tool on `https://api.github.com/repos/{o}/{r}/pulls/comments/{cid}` — returns raw JSON

### Failure-mode block additions

- **404 on a comment fetch in T2/T3/T5** → message: "Got 404 fetching `<url>`. Most likely causes: (a) the PR is private and you're not authenticated — install `gh` and run `gh auth login` to access private content; (b) the comment was deleted; (c) the URL is malformed. Cannot evaluate this item."
- **Rate-limit (429 / 403 with `X-RateLimit-Remaining: 0`) in T2/T3/T5** → message: "GitHub anonymous rate limit exhausted (60 req/hr). Either authenticate with `gh auth login` for 5000/hr, or wait for the limit to reset (`X-RateLimit-Reset` header in the response)."
- **`gh auth status` fails in T1 detection** → falls through to T2/T3/T5 as if `gh` weren't installed. Don't try to use `gh` unauthenticated; it's strictly worse than `curl` in that mode.

### Documentation in the README

The ruleset README must state the access tier in plain English: "Works on public PRs without any setup. For private PRs, install [GitHub CLI](https://cli.github.com/) and run `gh auth login`."
