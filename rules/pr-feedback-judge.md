# PR Feedback Judge

Evaluate one or more pieces of GitHub PR review feedback against the standard "valid? worth fixing? in scope for this PR?" rubric and emit a per-item verdict with an explicit disposition.

## When to use

- You've been handed one or more GitHub PR-feedback URLs (whole PR, a specific PR review, or individual inline / conversation comments — any mix) and need to decide what to do with each piece of feedback.
- Typical usage point: at the `reflect → pr open → [here]` seam of a Niko flow, when reviewers (human or bot) have weighed in and you're triaging their feedback before responding or fixing.

**Access requirements.** Prefers the `gh` CLI for direct, batched fetches. Falls back to a registered GitHub MCP server. Requires one or the other — anonymous public access is not supported.

## ⚠️ Load-bearing instruction: fetch first, never judge from the URL alone

**Always fetch the actual comment text before forming any opinion.** Do not improvise a verdict from the URL slug, the file path, or your prior knowledge of the PR. The reviewer's actual words — and the diff hunk they were anchored to — are the *only* evidence you may judge from. Fetch first, then evaluate. Every time.

## URL shape → GitHub endpoint

Classify each input URL by its fragment, then dispatch:

| URL fragment | Shape | API path (under `https://api.github.com`) | Yields |
|---|---|---|---|
| (none) — `…/pull/N` | Whole PR | `/repos/{o}/{r}/pulls/{N}/comments` + `/repos/{o}/{r}/issues/{N}/comments` + `/repos/{o}/{r}/pulls/{N}/reviews` (all paginated) | Every inline review comment, every conversation comment, every review body |
| `#pullrequestreview-<rid>` | PR review | `/repos/{o}/{r}/pulls/{N}/reviews/<rid>` + `/repos/{o}/{r}/pulls/{N}/reviews/<rid>/comments` | Review body + every inline comment in that review |
| `#discussion_r<cid>` | Inline review comment | `/repos/{o}/{r}/pulls/comments/<cid>` | Single inline comment (incl. `diff_hunk`, `path`, `in_reply_to_id`) |
| `#issuecomment-<cid>` | Conversation comment | `/repos/{o}/{r}/issues/comments/<cid>` | Single conversation comment |

If a URL doesn't match any of these shapes: emit "could not classify URL: `<url>`" for that item and continue with the rest. Do not crash, do not guess.

## Tier detection (in priority order)

Evaluate tiers in this exact order. Use the first one available; do not fall through to a lower tier if a higher one is present.

### T1 — `gh` CLI (preferred)

Detection:

```bash
command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1
```

If both succeed, use `gh api` for all fetches. T1 wins on efficiency: it has direct O(1) endpoints for both single-comment URL shapes and composes naturally with batched shell pipelines.

Per-shape invocation recipes:

```bash
# Whole PR (paginated)
gh api --paginate "repos/{o}/{r}/pulls/{N}/comments"
gh api --paginate "repos/{o}/{r}/issues/{N}/comments"
gh api --paginate "repos/{o}/{r}/pulls/{N}/reviews"

# Specific PR review
gh api "repos/{o}/{r}/pulls/{N}/reviews/{rid}"
gh api --paginate "repos/{o}/{r}/pulls/{N}/reviews/{rid}/comments"

# Single inline review comment (direct, O(1))
gh api "repos/{o}/{r}/pulls/comments/{cid}"

# Single conversation comment (direct, O(1))
gh api "repos/{o}/{r}/issues/comments/{cid}"
```

### T2 — GitHub MCP server (fallback)

Detection: scan the harness's **registered-MCP-servers list** (the same block of MCP metadata exposed to you at invocation time) for any server whose **name, identifier, or description** contains `github` (case-insensitive substring). If one matches, use its read-only PR/issue tools.

**Anti-pattern — do NOT do this:** filesystem-scan for MCPs (e.g., walking `~/.cursor/projects/*/mcps/`, reading descriptor JSON files off disk, or any other out-of-band discovery). The detection signal is the registered-MCP list already in your runtime context. If you're searching the filesystem for an MCP, you're doing it wrong.

Once a GitHub MCP is detected, read its tool schemas at runtime and pick the tool that matches each URL shape. The popular GitHub MCPs (e.g., `user-github`) expose method-dispatched, PR/issue-scoped tools — there is **no single-comment-by-ID getter**, so single-comment URLs require a list-and-filter against the parent PR/issue:

| URL shape | T2 access pattern |
|---|---|
| Whole PR `…/pull/N` | All review-thread comments + all PR conversation comments + all reviews of PR `{o}/{r}#{N}` |
| `#pullrequestreview-{rid}` | All review-thread comments on PR `{o}/{r}#{N}`, filtered to `pull_request_review_id == {rid}` + the review body for `{rid}` |
| `#discussion_r{cid}` | All review-thread comments on PR `{o}/{r}#{N}`, filtered to `id == {cid}` |
| `#issuecomment-{cid}` | All conversation comments on PR `{o}/{r}#{N}`, filtered to `id == {cid}` |

Derive `{N}` from the URL path (`…/pull/N#…`) when filtering for single-comment URLs.

### No tier available — fail loudly

If neither T1 nor T2 is available, emit verbatim:

> Cannot fetch GitHub data. Install [GitHub CLI](https://cli.github.com/) and run `gh auth login`, or register a GitHub MCP server with your harness.

Do not attempt anonymous `curl`. Do not scrape HTML. Do not pre-fetch the URL via any other path. Stop and surface the message.

## The intro (always emit, before any items)

Emit the following block verbatim before evaluating any items:

> Evaluating each piece of PR feedback. I'll fetch the actual comment text first — never judging from the URL alone — then for each item answer three questions and state the disposition.
>
> 1. **Valid?** Is the reviewer technically right about the code? Why or why not?
> 2. **Worth fixing?** Is the issue real and severe enough to act on at all? Why or why not?
> 3. **In scope for this PR?** Should it be fixed on this branch, deferred to a follow-up, or dismissed? Why or why not?
>
> The three answers compose into a disposition. Feedback can be valid but not worth fixing, or valid and worth fixing but out of scope for *this* PR — I'll spell each one out.

## The per-item block (emit for every item, in order)

```markdown
### Item N — [link to comment](url) by @author

**Where**: `path/to/file.ts:L42` (or "(conversation comment)" for issue-level / "(review body)" for review-level)

**Reviewer's point** *(quoted or paraphrased)*:
> …

**1. Valid?** ✅ / ❌ — …

**2. Worth fixing?** ✅ / ❌ — …

**3. In scope for this PR?** ✅ / ❌ / 🕒 follow-up — …

**Disposition**: fix in this PR | defer to follow-up | dismiss with acknowledgment | dismiss
```

Disposition vocabulary is fixed (4 values). Pick exactly one per item. Use the emoji set ✅ / ❌ / 🕒 only.

## Triage table (conditional — only when item count > 5)

If — and only if — the total number of items to evaluate is greater than 5 (e.g., a whole-PR URL on a busy PR), emit a compact triage table **before** the per-item blocks:

```markdown
| # | Item | Author | Disposition |
|---|---|---|---|
| 1 | [discussion_r123](url) | @reviewer | fix in this PR |
| 2 | [issuecomment-456](url) | @reviewer | dismiss |
```

For 5 or fewer items, skip the table — the per-item blocks alone are clearer at that scale.

## Tail (always emit, after all per-item blocks)

> N items evaluated · X to fix in this PR · Y deferred · Z dismissed.

Then add this one-line tip with a minimal body template:

> To turn all "defer to follow-up" items into a GitHub issue, run: `gh issue create --title "Follow-ups from PR #N" --body-file <path>`. Suggested minimal body:
>
> ```markdown
> Follow-ups deferred from PR #N. Each item links back to the original review comment.
>
> - [ ] [discussion_r123](https://github.com/{o}/{r}/pull/N#discussion_r123) — @reviewer — <one-line "in scope?" answer / why it's deferred>
> - [ ] [discussion_r456](https://github.com/{o}/{r}/pull/N#discussion_r456) — @reviewer — <…>
> ```

## Orchestration walkthrough

For each invocation:

1. **Classify each URL** against the shape table. Emit "could not classify" for any that don't match and continue.
2. **Detect tier** (T1 → T2 → fail). Pick the first available. If none, emit the failure message and stop.
3. **Fetch.** Issue the per-shape calls for each classified URL.
   - **Batch-fetch discipline (specific to this step):** if you end up with **3 or more structurally-identical `gh api` calls** in one invocation (e.g., the user gave you multiple `#discussion_r…` URLs all hitting `pulls/comments/<cid>`), issue them as **one batched shell pipeline**, not a sequential loop of tool calls. Example:

     ```bash
     for cid in 123 456 789; do
       gh api "repos/Texarkanine/a16n/pulls/comments/${cid}"
     done | jq -s '.'
     ```

     For T2 (MCP), batching is per-tool — make the minimum number of distinct MCP calls (e.g., one `get_review_comments` for the whole PR, then filter locally to all the requested `cid`s).
4. **Resolve reply context.** If a fetched inline comment has a non-null `in_reply_to_id`, make one extra call to fetch the parent thread (cheap — single comment). The parent provides the context the reviewer was responding to.
5. **Skip empty review entries.** A PR review with an empty body and no associated inline comments contributes nothing — drop it silently.
6. **Render.** Emit the intro, then (if items > 5) the triage table, then per-item blocks in input order, then the tail.

## Failure modes

- **Malformed / unclassifiable URL** → "could not classify URL: `<url>`" for that item; continue with the rest.
- **T1 hits a 404** → "Got 404 fetching `<url>`. Either the PR is private and your `gh` auth doesn't cover it, the comment was deleted, or the URL is malformed. Cannot evaluate this item." Continue with the rest.
- **No tier available** → see the failure message in the tier-detection section above. Stop.
- **`gh` rate-limit error** → surface `gh`'s message verbatim. Do not retry blindly. Stop.

## Example invocation

User input:

```
/pr-feedback-judge https://github.com/Texarkanine/a16n/pull/97 https://github.com/Texarkanine/a16n/pull/97#discussion_r1234567890
```

Expected sequence:

1. Classify → URL 1 is whole-PR, URL 2 is single inline comment.
2. Detect T1 (`gh` available, authenticated).
3. Fetch (batched where possible):

   ```bash
   gh api --paginate "repos/Texarkanine/a16n/pulls/97/comments"
   gh api --paginate "repos/Texarkanine/a16n/issues/97/comments"
   gh api --paginate "repos/Texarkanine/a16n/pulls/97/reviews"
   gh api "repos/Texarkanine/a16n/pulls/comments/1234567890"
   ```

4. Render the intro, then per-item blocks for each inline comment, each conversation comment, each non-empty review body, and the explicitly-named single inline comment (deduplicated if it's already covered by the whole-PR fetch — render it once, in the position the user listed it).
5. Render the tail and the follow-up-issue tip.
