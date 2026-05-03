# Decision: PR Feedback Judge — GitHub Fetch Tier Strategy

## Context

**What needs to be decided.** The command's GitHub-access strategy. The audience is anyone with Cursor (or Claude Code via `a16n`) on any machine, with the realistic assumption that **anyone doing this for real is logged in to GitHub somehow** — either via a GitHub MCP server or via the `gh` CLI. Anonymous public-only access is a "drive-by curiosity" use case worth supporting on a best-effort basis but not worth over-engineering for.

**Why it matters.** The command must work, with sensible degradation, on:
1. A machine with a GitHub MCP server registered with the harness — the cleanest, harness-native option.
2. A machine with `gh` CLI installed and authenticated — the dominant case for serious contributors.
3. A machine with neither — best-effort access to public PRs only; no acrobatics for private repos or rate-limit headroom.

If the command demands a single tool, it fails on the other configurations. Order matters: prefer the tool that the user has *intentionally* set up for GitHub access over the one that happens to be on `PATH`.

**Constraints.**
1. MCP, when present, MUST be preferred — it's harness-native, requires no shell, and reflects the user's deliberate authentication choice.
2. `gh` CLI is the strong default when no MCP is registered.
3. Public PRs SHOULD be reviewable on a vanilla machine with neither MCP nor `gh` installed (best-effort, not a hard requirement). Failure here is acceptable; failure here without a clear "install gh" message is not.
4. **No env-var token harvesting.** If the user hasn't installed `gh` or registered an MCP, we don't grovel through `GITHUB_TOKEN` / `GH_TOKEN` / `~/.config/...` to authenticate `curl` requests. That's the user's choice to make.
5. Whatever tier is chosen, output to the LLM must be JSON or otherwise structured-ish — feeding the agent raw HTML to extract one comment is the failure mode we're trying to avoid.
6. The strategy must be detectable at runtime — the command body tells the agent how to probe & pick.
7. The strategy must compose with the batch-fetch discipline from `script-it-instead` — one logical batch per invocation.

## Options Evaluated

The space is a chain. Each tier is strictly better than the next on output quality and data completeness, and each requires more explicit user setup.

- **T0 — GitHub MCP server**: harness-native, surfaces tools like `get_pull_request_review_comments`, `get_pull_request_comments`, `get_pull_request_reviews`, `get_issue_comment` (exact names vary by MCP implementation). Authentication flows through the MCP's own setup. Best-quality data, no shell required, not affected by rate limits unless the MCP exposes them.
- **T1 — `gh` CLI**: `gh api repos/.../pulls/comments/123 --jq '...'`. Authenticated with the user's GitHub account. Clean JSON. Handles pagination via `--paginate`. Standard for serious contributors.
- **T2 — Anonymous REST (`curl` + `jq` or stdlib)**: `curl -fsS https://api.github.com/repos/.../pulls/comments/123`. Public PRs only, 60 req/hr anonymous limit, no env-token grovel. Best-effort fallback.
- ~~**T3 — Web-fetch on the API URL**~~: feasible but only marginally different from T2 (different invocation, same data). Collapsed into T2's "and if neither curl nor jq exists, the harness web-fetch can hit the same `api.github.com` URL" footnote.
- ~~**T4 — Web-fetch on the HTML page**~~: dropped; strictly dominated by T2 (same access path, dramatically noisier output).

## Analysis

| Criterion | T0 MCP | T1 gh | T2 anon | (notes) |
|---|---|---|---|---|
| Detection signal | MCP tool list contains a github-related tool | `command -v gh && gh auth status` succeeds | `command -v curl` succeeds | |
| Public PRs | ✅ | ✅ | ✅ | |
| Private PRs | ✅ if MCP is authenticated | ✅ | ❌ → message: "install gh and run `gh auth login`" | |
| Output quality | Clean structured tool result | Clean JSON | Clean JSON | |
| Auth model | MCP-specific | `gh auth login` (one-time) | None (don't grovel for env tokens) | per constraint 4 |
| Rate limit headroom | MCP-dependent (typically authenticated) | 5000/hr | 60/hr — fine for one PR review, not engineered around | |
| Composes with batch-fetch | ✅ MCP tools take ID lists or paginated args | ✅ `--paginate` | ✅ `?per_page=100&page=N` cursor | |
| Setup the user already chose | They installed an MCP for this | They authed `gh` for this | None | this is the explicit ordering criterion |

**Key insights:**
- Tier ordering tracks *user setup intent*, not just availability. Someone who registered a GitHub MCP did it deliberately; we should respect that over a `gh` that happens to be on the box for some other reason.
- T1 and T2 hit identical REST endpoints, so the URL→API path table in the command body remains tier-agnostic between them. T0 uses MCP-tool names instead of API paths, but the *shape* of the data the agent reasons over (author / body / path / diff_hunk / verdict) is the same.
- "Long lists silently truncating during pagination" is not a real risk worth engineering around — if a whole-PR fetch returns more items than will fit in one realistic chat turn, the user can just point at the specific review or comment URL instead. **No sanity-check / count-verification step needed.** (Operator confirmed.)
- T0 detection is harness-shaped, not POSIX-shaped: in Cursor the agent sees enabled MCPs in its context block; in Claude Code, the same. The command body should describe the *capability* it needs ("a GitHub MCP tool capable of fetching PR comments by ID") and let the agent map that to whatever specific tool name its harness exposes.

## Decision

**Selected**: a three-tier ordered fallback chain — **T0 (GitHub MCP) → T1 (`gh` CLI) → T2 (anonymous `curl`, best-effort)** — with explicit detection probes at each tier and a single "install gh and authenticate" failure message when a private repo is encountered without T0 or T1.

**Rationale**: Satisfies all seven constraints. Reflects the realistic audience: most users will have either MCP or `gh` deliberately set up; serving them well is the job. Anonymous works for drive-by curiosity but is not the design center.

**Tradeoff**: The command body has a tier-detection block plus three invocation recipes per logical operation. Boilerplate cost in exchange for working across the full audience.

## Implementation Notes

### Detection (described, not scripted — T0 is not detectable from shell)

The command body instructs the agent to evaluate tiers in order:

1. **T0**: scan the harness's available-MCP-tools block (the same block that exposes any other MCP). If there's a tool whose schema indicates it fetches GitHub PR comments / reviews / issue comments by ID (typical names: `get_pull_request_*`, `mcp_github_*`), use that tool family for all fetches in this invocation.
2. **T1**: if no T0 tool is available, run `command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1`. If both succeed, use `gh api`.
3. **T2**: otherwise, use `curl -fsS https://api.github.com/...` (with `jq` for parsing if present, else `python3 -c 'import json, sys; ...'`). If even `curl` is unavailable, the agent may fall back to its harness web-fetch tool on the same `api.github.com` URL. Do **not** read or pass `GITHUB_TOKEN` / `GH_TOKEN` / any auth env var.

### URL→API mapping (shared by T1 and T2; T0 uses MCP tool names instead)

| URL fragment | API path (under `https://api.github.com`) |
|---|---|
| (none) — `…/pull/N` | `/repos/{o}/{r}/pulls/{N}/comments` + `/repos/{o}/{r}/issues/{N}/comments` + `/repos/{o}/{r}/pulls/{N}/reviews` (all paginated) |
| `#pullrequestreview-{rid}` | `/repos/{o}/{r}/pulls/{N}/reviews/{rid}` + `/repos/{o}/{r}/pulls/{N}/reviews/{rid}/comments` |
| `#discussion_r{cid}` | `/repos/{o}/{r}/pulls/comments/{cid}` |
| `#issuecomment-{cid}` | `/repos/{o}/{r}/issues/comments/{cid}` |

### Failure-mode block additions

- **T2 hits a 404** → message: "Got 404 fetching `<url>`. Most likely: this PR is private and you're not authenticated. Install [GitHub CLI](https://cli.github.com/) and run `gh auth login`, or register a GitHub MCP server with your harness. Cannot evaluate this item."
- **T2 hits a rate limit (`X-RateLimit-Remaining: 0`)** → message: "Anonymous GitHub rate limit exhausted (60/hr). Authenticate via `gh auth login` or a GitHub MCP server for a higher limit, or wait for the limit to reset (`X-RateLimit-Reset` header in the response)."
- **No tier available** (no MCP, no `gh`, no `curl`, no harness web-fetch) → message: "Cannot fetch GitHub data. Install [GitHub CLI](https://cli.github.com/) and run `gh auth login`."

### README implications

The ruleset README lists the supported access paths in priority order, with one line each: "Prefers a registered GitHub MCP server. Falls back to `gh` CLI if available and authenticated. Public PRs work best-effort with `curl` only."
