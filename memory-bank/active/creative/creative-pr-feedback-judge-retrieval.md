# Decision: PR Feedback Judge — Correct and Efficient Retrieval

## Context

**What needs to be decided.** How `/pr-feedback-judge` obtains the two things its rubric depends on: the reviewer's words, and the code those words describe. The comment side is settled (see `creative-pr-feedback-judge-fetch-tiers.md`: `gh` CLI → GitHub MCP → fail loudly). What was never decided is the code side. The skill silently assumes the operator's working tree is the PR head, and it has no notion that a review anchor can go stale.

**Why it matters.** The skill's load-bearing instruction is that the reviewer's words *and the diff hunk they were anchored to* must be retrieved before judging. It enforces the first half and ignores the second. Measured against this repository's own corpus — 86 pull requests, 293 inline review comments, all of them line-anchored — the anchors are far less stable than the skill assumes:

- 119 (41%) are outdated: `line` is `null` while `original_line` is set, so GitHub can no longer place them in the current diff.
- 125 (43%) are still anchored but have drifted — 123 have `commit_id != original_commit_id`, 12 have `line != original_line`, and those two groups overlap. The branch moved underneath these comments, so any line number that still matches may match by coincidence.
- Only 49 (17%) are unambiguously current: anchored, same line, same commit.

Reading current code at a comment's `original_line` therefore reads the wrong text most of the time, and nothing about the failure is visible. That is precisely the error the skill was written to prevent, reached through an unguarded door.

**Constraints.**

1. Correctness before economy. A cheaper retrieval that risks judging the wrong text is not cheaper.
2. Escalation must be gated on need. Most items are judgeable from `diff_hunk` plus the reviewer's text; code access is the exception, not the default.
3. Never disturb the operator's working state. If a local copy at the PR head is required and the current checkout is elsewhere, obtain it additively.
4. Cloning is a last resort. Typical clones are fast — a blobless `cli/cli` took 1.27s for 12 MB — but the operator maintains repositories in the tens of gigabytes where a clone is far slower than any API path. GitHub reports `repos/{o}/{r}.size` in KB, so size is knowable before committing to a clone.
5. Degradation must be loud. When the skill judges from the hunk alone because no code was reachable, it says so.
6. Field projection must not strip the fields that staleness detection needs. The economy decision and the correctness decision touch the same fetch.

## Options Evaluated

### Anchor trust

- **A1 — Status quo:** read `path` and whatever line number is present. Rejected: wrong text in 83% of corpus comments.
- **A2 — Trust `line`, treat `null` as outdated, never index current code by `original_line`.** Anchor state becomes an explicit input to the verdict.
- **A3 — Ignore line numbers entirely; always locate by content from `diff_hunk`.** Correct but wasteful, and it discards a reliable signal for the 17% that are genuinely current.

### Code access

- **C1 — Assume the working tree is the PR head.** The current implicit behavior. Rejected: unverified, and false whenever the operator has switched branches, pulled, or is not in the repository.
- **C2 — Always fetch files through the API.** Correct anywhere, but wasteful when the operator is already standing in the right checkout, and unable to support repository-wide search or test execution.
- **C3 — Need-gated escalation ladder.** Verify the cheap case, escalate only as the rubric demands, clone only when nothing else can answer the question.

### Disposition vocabulary

- **D1 — Keep four values.** Rejected: an outdated anchor whose finding the current head already satisfies has no honest home. `dismiss` misreports a valid finding as rejected; `fix in this PR` invents work that does not exist.
- **D2 — Add `already addressed` as a fifth value, evidence-gated.**

## Analysis

The three questions are not independent. Staleness detection is what makes code access *necessary* — an outdated anchor is the main reason to look past `diff_hunk` at all, because deciding between "already fixed" and "merely displaced" requires the current code. And field projection is where a careless economy would delete the staleness signal. So the design is one decision with three faces, not three decisions.

The corpus also warns against the obvious shortcut. It is tempting to read a null `line` as proof the operator already fixed the finding, but a further 125 comments drifted without going outdated at all: churn in these files is routine and is frequently unrelated to any given finding. Anchor movement is evidence that the code *may* have changed, never evidence that a *specific* finding was resolved. `already addressed` therefore has to be earned by looking at code, which is exactly why the ladder exists.

One more subtlety the corpus did not exercise but the design must not trip over: a comment with `subject_type == "file"` has a null `line` legitimately, because it is attached to the whole file rather than a line. All 293 comments here are `subject_type == "line"`, so the measurement is uncontaminated, but a null-line test that ignores `subject_type` would misclassify file-level comments as outdated.

On economy, the operator's starting premise — that the API pads everything with JSON — is only selectively true, and acting on the general version of it would make things worse:

- `pulls/{N}/files` versus the raw unified diff measured at 1.07x, 1.14x, and 1.25x across three PRs. There is no diff bloat worth avoiding, and cloning to avoid it is a net loss.
- `pulls/{N}` bare is 21,999 bytes for a PR whose diff is 891 bytes — 24x — because GitHub embeds two complete repository objects under `head` and `base`. Never fetch it for diff purposes.
- The `application/vnd.github.patch` media type is 18,378 bytes where `.diff` is 891, because patch format carries per-commit metadata. Prefer `.diff`.
- The comment endpoints the skill actually lives on do have removable padding: reviews project from 7,818 to 3,329 bytes (57%), inline comments from 20,543 to 14,805 (28%). Inlines save less because `body` and `diff_hunk` are the payload, and both must be kept.
- A single file can be fetched raw rather than as base64 JSON: 2,070 bytes versus 3,782 for the same file. This is what makes the no-clone tier viable.

## Decision

Three coordinated changes to `rules/pr-feedback-judge/SKILL.md`.

### Anchor trust model

Adopt **A2**. Every inline comment carries an explicit anchor state derived from `subject_type`, `line`, and `commit_id`:

- **Current** — `line` is non-null. Read current code at `line`, and only when the code source is verified to be at the PR head SHA.
- **Outdated** — `subject_type == "line"` and `line` is null. The anchor no longer exists. Do not read current code at any line number. Locate the referenced text by searching the current file for the content of `diff_hunk`.
- **File-scoped** — `subject_type == "file"`. A null `line` is expected and carries no staleness meaning.

`original_line` and `original_commit_id` index the historical blob only. They are never used to address current code. They are retained for reporting, so a verdict can say what the reviewer was looking at.

### Code access ladder

Adopt **C3**. Before any tier, ask whether the item needs code beyond `diff_hunk`; the default answer is no. Escalate only when the reviewer's claim reaches outside the hunk — a caller, a test, a type, a config — or when an outdated anchor must be resolved.

- **Tier A — already at the PR head.** `git rev-parse HEAD` equals the PR's `head.sha`. Read files directly. Free, and the only tier where a non-null `line` can be trusted verbatim.
- **Tier B — in the repository, different commit.** `git fetch origin pull/{N}/head`, which is purely additive: it adds objects and sets `FETCH_HEAD` without touching the index, the working tree, or any branch. Then read directly against the ref, with no checkout at all — `git show FETCH_HEAD:{path}` for a file, `git ls-tree FETCH_HEAD` to enumerate, `git grep {pattern} FETCH_HEAD` to search the whole tree. All three are read-only and need no cleanup, so no destructive git operation is ever orchestrated. Materialize a worktree only to *run* something, since a test runner needs real files on disk: `git worktree add --detach` into `mktemp -d`, then `git worktree remove`. Deleting the directory without removing the worktree is not an adequate substitute — it strands an administrative entry under `.git/worktrees/` that keeps appearing in `git worktree list` until someone prunes, leaving the repository dirty while the filesystem looks clean.
- **Tier C — not in the repository.** Fetch only the files needed, raw: `gh api "repos/{o}/{r}/contents/{path}?ref={sha}" -H "Accept: application/vnd.github.raw"`. Preferred over cloning at every repository size.
- **Tier D — clone, last resort.** Only when Tier C cannot answer the question because the objects are not local at all: searching a whole tree the operator does not have, or running tests. Note that tree-wide search is *not* a reason to clone when Tier B applies, since `git grep` works against a fetched ref. Check `gh api repos/{o}/{r} --jq .size` first — it answers in KB, and it separates a 769 KB repository from a 62 GB one before any transfer begins. Above the operator's tolerance, stay on Tier C and say why. When cloning is genuinely warranted, use `--filter=blob:none --depth 1 --single-branch` into a `mktemp -d`.

The skill declares which tier it used. When no tier above the gate was reachable, it states that the judgment rests on `diff_hunk` alone, so the weaker verdict is visible rather than silent. On a repository the operator cannot push to, it notes that author-stance dispositions do not apply.

### Disposition vocabulary

Adopt **D2**. The fixed vocabulary becomes five values: `fix in this PR`, `already addressed`, `defer to follow-up`, `dismiss with acknowledgment`, `dismiss`.

`already addressed` means the finding was valid when written and the current PR head already satisfies it. It requires code evidence from the ladder; an outdated anchor on its own never justifies it. Within the rubric, validity is judged as of the time the comment was written, and `already addressed` resolves the third question rather than the first, so a correct reviewer stays correct in the record. The triage table and the tail counts gain the new bucket.

**Rationale.** Correctness drives the whole design: the measured 41% outdated rate makes anchor state a required input, resolving anchor state is what makes code access necessary, and `already addressed` is the verdict that state produces. Efficiency then falls out of it rather than fighting it — the ladder's cheap tiers handle the common cases, and projection trims the metadata the rubric never reads while explicitly preserving the fields staleness detection depends on.

**Tradeoff.** The skill body grows, and each inline gains a classification step before judgment. That cost is accepted: the alternative is a skill whose central promise — never judge without looking at what the reviewer saw — holds for one comment in six.

## Implementation Notes

Projection must retain `id`, `user.login`, `path`, `subject_type`, `line`, `original_line`, `commit_id`, `original_commit_id`, `side`, `in_reply_to_id`, `body`, and `diff_hunk`. Everything else on the comment object — `_links`, `reactions`, `html_url`, `pull_request_url`, the full user object, `node_id` — is droppable. Reviews keep `id`, `user.login`, `state`, and `body`.

For the current diff, use `gh pr diff {N} -R {o}/{r}`, which works outside any checkout, or `gh api repos/{o}/{r}/pulls/{N} -H "Accept: application/vnd.github.diff"`. Both return the same bytes. Do not fetch `pulls/{N}` as JSON for this purpose, and do not use the `.patch` media type.

Existing sections needing edits: the access-requirements paragraph gains the code-access dependency; the URL-shape table's `Fetches` column gains the anchor fields; `What becomes an Item` gains anchor-state handling; the per-item block gains an anchor/source line and the fifth disposition; the triage table and tail gain the new bucket; `Orchestration walkthrough` gains the gate-and-escalate step between fetching and filtering; `Failure modes` gains an unreachable-code-source entry.

## Corpus Measurements

Source: all 86 pull requests on `Texarkanine/.cursor-rules`, 293 inline review comments, `subject_type` uniformly `line`.

The three anchor states partition the corpus:

- Unambiguously current — anchored, same line, same commit: 49 (17%)
- Anchored but drifted: 125 (43%)
- Outdated, `line == null`: 119 (41%)

Within the 125 drifted, the two drift signals overlap and are reported separately: 123 have `commit_id != original_commit_id`, and 12 have `line != original_line`.

Also measured: 23 PRs have inline comments spanning more than one head commit.
