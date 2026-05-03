# Decision: PR Feedback Judge — GitHub Fetch Tier Strategy

## Context

**What needs to be decided.** The command's GitHub-access strategy. The audience is anyone with Cursor (or Claude Code via `a16n`) on any machine. The realistic assumption — operator-affirmed twice — is that **anyone doing this for real is logged in to GitHub somehow**, either via `gh` CLI or via a registered GitHub MCP server. Anonymous public-only access is not a use case worth supporting.

**Why it matters.** The command must work, with sensible degradation, on:
1. A machine with `gh` installed and authenticated (the dominant case for serious contributors).
2. A machine with a GitHub MCP server registered with the harness.
3. A machine with neither — fail loudly with one actionable message, no acrobatics.

If the command demands one specific tool, it fails when only the other is present. Order matters and is **efficiency-driven**: the tool whose API shape best matches our access pattern wins.

**Constraints.**
1. `gh` CLI, when authenticated, MUST be preferred — it has O(1) endpoints for both single-comment URL shapes (`#discussion_r{cid}` → `pulls/comments/{cid}`, `#issuecomment-{cid}` → `issues/comments/{cid}`) and composes naturally with `script-it-instead` for batched per-URL fetches.
2. A GitHub MCP server, when registered with the harness, is the secondary option — harness-native, requires no shell — but is dispreferred because the popular GitHub MCPs (verified against the official-style `user-github` server in this environment, 41 tools) expose only **method-dispatch tools that operate on a whole PR/issue** (`pull_request_read` with `method=get_review_comments|get_comments|get_reviews`; `issue_read` with `method=get_comments`). There is no single-comment-by-ID getter. For a `#discussion_r…` URL on a busy PR, MCP must list-and-filter where `gh` would do one direct call.
3. **Anonymous access is not a tier.** Cut entirely. No `curl` fallback, no env-var token grovel, no rate-limit engineering.
4. Whatever tier is chosen, output to the LLM must be JSON or otherwise structured-ish — feeding the agent raw HTML is the failure mode we're trying to avoid.
5. The tier strategy must compose with the batch-fetch discipline from `script-it-instead` — one logical batch per invocation.
6. MCP detection must be **loose**: any MCP server whose name, identifier, or description mentions "github" is presumed to be a GitHub MCP. Specific tool names vary by implementation (verified: `user-github`'s actual identifier is implementation-specific; the agent should match permissively and read the available tool schemas at runtime to decide which one applies to which URL shape).

## Options Evaluated

- **T1 — `gh` CLI**: `gh api repos/.../pulls/comments/123 --jq '...'`. Authenticated. Direct single-comment lookups. `--paginate` for list endpoints. Best fit for the four URL shapes the command handles, especially when invocations mix single-comment URLs with whole-PR URLs.
- **T2 — GitHub MCP server**: harness-native; the agent calls the MCP's read-only PR/issue tools and gets structured tool results. Authentication flows through the MCP's own setup. Works without a shell. Downside: read-tool surface is method-dispatched and PR-scoped, requiring list-and-filter for single-comment URLs.
- ~~**T3 — Anonymous REST**~~: dropped per operator. Realistic users are authenticated; if neither tier above is present, fail with a clear message.
- ~~**T4 — Web-fetch on HTML**~~: dropped (still); strictly dominated by anything that returns JSON.

## Analysis

| Criterion | T1 gh | T2 MCP |
|---|---|---|
| Detection signal | `command -v gh && gh auth status` | An MCP server is registered whose name / identifier / description matches `github` (case-insensitive substring) |
| Single-comment URL (`#discussion_r…`, `#issuecomment-…`) | ✅ Direct `pulls/comments/{cid}` / `issues/comments/{cid}` — one call each | ⚠️ List-and-filter via `pull_request_read get_review_comments` / `issue_read get_comments`, paginated, requires the parent PR/issue number to be derivable from the URL |
| Whole-PR URL | ✅ 3 paginated list calls | ✅ 3 method-dispatch calls (review_comments / reviews / comments), paginated |
| `#pullrequestreview-{rid}` URL | ✅ Direct `reviews/{rid}` + `reviews/{rid}/comments` | ⚠️ `get_reviews` (lists then filter) + `get_review_comments` (returns all PR review threads, then filter to ones in this review) |
| Composes with `script-it-instead` | ✅ Native — one shell pipeline batches across all URLs in the invocation | ⚠️ Batch is per-MCP-call; the agent makes N MCP calls but cannot inline them in a single shell script |
| Auth model | `gh auth login` (one-time, well-understood) | MCP-specific (varies by implementation) |
| Private repos | ✅ | ✅ if MCP is authenticated |
| Tool-name stability | Highly stable (`gh api`, REST URLs) | Implementation-dependent — but the agent reads schemas at runtime, so this is a non-issue once the *server* is detected |

**Key insights:**
- The dominant URL shape in the user's actual corpus is the single-comment anchor: 15 `#discussion_r…` + 2 `#issuecomment-…` + 8 `#pullrequestreview-…` = 25 of 76 extracted URL rows are anchored to a specific comment or review. `gh`'s direct lookups are O(1) for these; MCP's list-and-filter is O(N comments on the PR). With `script-it-instead` batching, T1 wins clearly on efficiency.
- T2's "no shell required" advantage matters only in environments where the agent has no shell access at all. That's a real-but-narrow case (some restricted harness modes). When it applies, T2 still works fine — just less efficiently.
- Detection of "is *a* GitHub MCP available" is best done as a permissive substring match on `github` against the MCP server's metadata, not by hardcoding tool names. This was operator-confirmed: "github mcp should be enough to cue an agent in." The actual server identifier in this environment is `user-github`, but other deployments use `mcp-github`, `github-mcp`, the official `github`, etc. Loose match avoids brittleness.
- Once a GitHub MCP is detected, the agent does not need our command body to enumerate its tools — MCP tool schemas are self-describing. The command body says "use the GitHub MCP's read-only PR/issue tools to fetch what these URLs reference"; the agent figures out which tool maps to which shape.

## Decision

**Selected**: a two-tier ordered chain — **T1 (`gh` CLI authenticated) → T2 (GitHub MCP, loose-detected) → fail loudly**.

**Rationale**: Satisfies all six constraints. T1 is preferred on efficiency for the dominant single-comment URL shape and on naturally batching with `script-it-instead`. T2 is the harness-native fallback that still works correctly without a shell, just with O(N) overhead for single-comment URLs. Anonymous and HTML scrape are explicitly out — any user invoking this command on a real PR will have at least one of these two access paths set up.

**Tradeoff**: A small population of users with neither `gh` installed nor a GitHub MCP registered will get a clear failure message instead of partial functionality. That's the right tradeoff: ship a tool that works correctly when used, not a tool that pretends to work when it can't.

## Implementation Notes

### Detection (described, evaluated in priority order)

The command body instructs the agent to evaluate tiers in order:

1. **T1**: run `command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1`. If both succeed, use `gh api`.
2. **T2**: if T1 fails, scan the harness's available-MCP-servers block for any server whose name, identifier, or description contains `github` (case-insensitive substring). If one is found, use its read-only PR/issue tools — the agent reads each tool's schema at invocation and maps URL shapes to tool calls.
3. **No tier**: emit "Cannot fetch GitHub data. Install [GitHub CLI](https://cli.github.com/) and run `gh auth login`, or register a GitHub MCP server with your harness."

### URL→API mapping (T1 — direct REST endpoints; T2 enumerated only as the access pattern, no specific tool names)

| URL fragment | T1 — `gh api` path | T2 — access pattern (agent picks matching MCP tool from schema) |
|---|---|---|
| (none) — `…/pull/N` | `repos/{o}/{r}/pulls/{N}/comments` + `repos/{o}/{r}/issues/{N}/comments` + `repos/{o}/{r}/pulls/{N}/reviews` (paginated) | All review-thread comments + all PR conversation comments + all reviews of PR `{o}/{r}#{N}` |
| `#pullrequestreview-{rid}` | `repos/{o}/{r}/pulls/{N}/reviews/{rid}` + `repos/{o}/{r}/pulls/{N}/reviews/{rid}/comments` | All review-thread comments on PR `{o}/{r}#{N}`, filtered to `pull_request_review_id == {rid}` + the review body for `{rid}` |
| `#discussion_r{cid}` | `repos/{o}/{r}/pulls/comments/{cid}` (direct, O(1)) | All review-thread comments on PR `{o}/{r}#{N}`, filtered to `id == {cid}` |
| `#issuecomment-{cid}` | `repos/{o}/{r}/issues/comments/{cid}` (direct, O(1)) | All conversation comments on PR `{o}/{r}#{N}`, filtered to `id == {cid}` |

For T2 single-comment URLs, the agent must derive `{N}` from the URL (`/pull/N#…`) — already trivially available since URL classification has already extracted it.

### Failure-mode block

- **T1 hits a 404** → message: "Got 404 fetching `<url>`. Either the PR is private and your gh auth doesn't cover it, the comment was deleted, or the URL is malformed. Cannot evaluate this item."
- **No tier available** → message above.

### README implications

Ruleset README explains in one paragraph: "Prefers `gh` CLI for direct, batched fetches. Falls back to a registered GitHub MCP server. Requires one or the other — anonymous public access is not supported."
