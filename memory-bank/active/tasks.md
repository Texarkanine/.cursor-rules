# Task: PR Feedback Judge — Correct and Efficient Retrieval

* Task ID: pr-feedback-judge-retrieval
* Complexity: Level 2
* Type: Simple enhancement, correctness-driven

Rework `rules/pr-feedback-judge/SKILL.md` so its verdicts rest on the current state of the code rather than on a review anchor that has probably moved. Adds an anchor-state model, a need-gated code-access ladder, an evidence-gated `already addressed` disposition, and field projection on the fetch recipes. Design of record: `memory-bank/active/creative/creative-pr-feedback-judge-retrieval.md`.

## Test Plan (TDD)

`always-tdd` does not govern this change. Its carve-out names "rule and skill wording" as out of scope, and any test asserting on `SKILL.md` prose would be a change-detector — red only when someone deliberately edits the file, silent when the skill actually misbehaves. Per that rule, none are written. Verification is the existing purpose-built gates, a structural self-check, and a live acceptance run against a PR with a known-outdated anchor.

### Behaviors to Verify

- Outdated anchor, live run → given `#discussion_r3653815924` on PR #91 (`line == null`, `original_line == 47`, `commit_id` differs), the skill classifies it outdated, declines to read current code at line 47, and locates the referenced text by `diff_hunk` content instead.
- Current anchor, live run → given a comment with `line == original_line` and `commit_id == original_commit_id`, the skill reads at `line` and says the anchor is current.
- Need gate → given feedback answerable from `diff_hunk` alone, the skill escalates to no code source at all and does not fetch files.
- Rung selection in-repo, off-head → from a checkout whose `HEAD` is not the PR head, the skill uses `git fetch origin pull/N/head` plus ref reads, and leaves `git status` clean and `git worktree list` unchanged.
- Rung selection outside a repo → from `mktemp -d`, the skill uses raw `contents` fetches and does not clone.
- Clone gate → given a repository whose `.size` is large, the skill stays on raw fetches and states why rather than cloning.
- Loud degradation → when no code source is reachable, the output says the verdict rests on `diff_hunk` alone.
- `already addressed` requires evidence → an outdated anchor with no code inspection must not yield `already addressed`.
- Edge: `subject_type == "file"` → a null `line` is reported as file-scoped, not outdated.
- Edge: outdated but still actionable → an outdated anchor whose finding still stands is still an Item; outdated is not a filter.
- Edge: foreign repository → author-stance dispositions are flagged as inapplicable when the operator cannot push.
- Regression: projection retains anchor fields → the `--jq` filters still emit `subject_type`, `line`, `original_line`, `commit_id`, `original_commit_id`, `side`, `in_reply_to_id`, `body`, `diff_hunk`.
- Regression: existing behavior intact → URL classification, T1/T2 fetch-tier detection, author resolution for `#issuecomment-…`, and the summary/walkthrough filtering all still work as before.

### Test Infrastructure

- Framework: none for content. `make test` (`scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`) is the repository's gate; CI is `.github/workflows/rulesets-links.yml` running the same targets. Baseline confirmed green before any edit.
- Test location: no test directory exists; this repository has no content-assertion suite by design.
- Conventions: correctness of rule and skill prose is enforced by review plus purpose-built gates, per the `always-tdd` carve-out.
- New test files: none. Adding one would be the change-detector the rule forbids.
- Additional checks: `python3 scripts/verify-skillify.py` (asserts `pr-feedback-judge` remains a structurally valid command-skill), and the live acceptance run against PR #91 described above.

## Implementation Plan

Concepts are defined before the sections that reference them, so no step requires backtracking.

1. [x] Add the anchor-state model
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: new `## Anchor State` section after `## URL shape → GitHub endpoint`. Defines three states — current, outdated, file-scoped — and their consequences for judgment. States that `original_line` and `original_commit_id` address the historical blob only and are retained for reporting. States that a current `line` is trustworthy only when the code source is verified at the PR head. Per the preflight amendment, the state arrives pre-computed in the `anchor` field from step 3's projection, so this section defines what each value *means* rather than asking the agent to derive it; it also gives the derivation once, for T2, where no `--jq` runs.
2. [x] Add the code-access ladder
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: new `## Reading the Code Under Review` section. Opens with the need gate (`diff_hunk` plus reviewer text is the default). Four rungs named by condition, not lettered — see Challenge 1: at the PR head; in the repository off-head (`git fetch origin pull/{N}/head`, then `git show FETCH_HEAD:{path}` / `git ls-tree` / `git grep … FETCH_HEAD`, all read-only, worktree only to run something and then removed); not in the repository (raw `contents` fetches); clone as last resort behind `gh api repos/{o}/{r} --jq .size`. Requires declaring the rung used.
3. [x] Add field projection to the fetch recipes
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: `--jq` projections on the T1 `gh api` recipes under `### T1 — gh CLI`, retaining every field the anchor model needs and **computing the `anchor` field mechanically** (`if .subject_type == "file" then "file" elif .line == null then "outdated" else "current" end`), per the preflight amendment. Note the measured savings and the explicit prohibition on stripping anchor fields. Add the diff-transport note: `gh pr diff {N} -R {o}/{r}` or `Accept: application/vnd.github.diff`; never bare `pulls/{N}` JSON for diff purposes; never the `.patch` media type. Mirror the projection instruction for T2 as filter-locally guidance.
4. [x] Extend the URL-shape table
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: `Fetches` column notes the anchor fields now retrieved for inline shapes.
5. [x] Wire anchor state into item filtering
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: in `## What becomes an Item`, state explicitly that anchor state is not a filter — an outdated anchor whose finding still stands is still an Item. Anchor state informs the verdict, never item-ness.
6. [x] Extend the disposition vocabulary and per-item block
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: `## Per-Item Block` gains anchor state and code source on the `**Where**` line; disposition list becomes five values; `already addressed` defined as valid-when-written and satisfied on the current head, requiring code evidence. Question 1 is judged as of when the comment was written; `already addressed` resolves question 3. Emoji set stays ✅/❌/🕒 — see Challenge 2.
7. [x] Update the emitted blocks
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: `## Intro Block` gains a clause covering already-satisfied feedback; `## Conditional Triage Table` example shows the new disposition; `## Tail Block` gains the already-addressed count.
8. [x] Add the gate-and-escalate step to orchestration
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: new step in `## Orchestration walkthrough` between fetching and filtering — classify anchors, decide whether code is needed, select and declare a rung.
9. [x] Extend failure modes
   - Files: `rules/pr-feedback-judge/SKILL.md`
   - Changes: entries for unreachable code source (degrade loudly to hunk-only), oversized repository (stay on raw fetches, say why), and foreign repository (author-stance dispositions inapplicable).
10. [x] Update the header prose
    - Files: `rules/pr-feedback-judge/SKILL.md`
    - Changes: `**Access requirements.**` gains the code-access dependency; the load-bearing instruction extends to require checking whether the anchor still describes current code.
11. [x] Verify
    - Files: none
    - Changes: run `make test` and `python3 scripts/verify-skillify.py`; read the whole file for internal consistency and dead cross-references; confirm markdown-style compliance (headings not bold, no heading parentheticals, no hard wrapping); execute the live acceptance run against PR #91's outdated comment.
    - Results: `make test` green. `verify-skillify.py` fails baseline on 4 unrelated missing skills (same before and after this edit); targeted check confirms `pr-feedback-judge` remains a valid command-skill. Live acceptance on `#discussion_r3653815924`: `anchor=outdated`, declines `original_line=47`, locates via `diff_hunk`, off-head rung leaves status and worktree list clean. Emphasis density ~2.6 bold/1k.

## Technology Validation

No new dependencies. Every mechanic the plan relies on was validated during the creative phase or at plan time, in this environment:

- `git fetch origin pull/99/head` then `git show FETCH_HEAD:{path}` read a file at the PR head with the working tree confirmed clean and the branch unchanged.
- `git grep {pattern} FETCH_HEAD` and `git ls-tree FETCH_HEAD` both operate against the bare ref with no checkout.
- `gh api "repos/{o}/{r}/contents/{path}?ref={sha}" -H "Accept: application/vnd.github.raw"` returned raw bytes, 2,070 versus 3,782 for base64 JSON.
- `gh api repos/{o}/{r} --jq .size` distinguished 769 KB from 62.5 GB before any transfer.
- `gh pr diff {N} -R {o}/{r}` works from outside any checkout.
- `make test` green at baseline.
- The anchor-computing `--jq` projection ran against PR #91 and correctly labelled `3653815924` as `outdated` and the two live comments as `current`. Cost is 15,059 bytes versus 14,805 for a projection that omits the computed field, against 20,543 unprojected.

## Preflight Amendment

Preflight's Radical Innovation step produced one change, adopted into steps 1 and 3: **compute the anchor state in the `--jq` projection rather than asking the agent to derive it per item.** The projection already exists, so the marginal cost is 254 bytes, and the state arrives in the data as an `anchor` field.

This matters because it converts the single largest risk in the plan — Pre-Mortem finding 1, that a longer skill gets followed less — from an adherence problem into a mechanical one. An agent cannot forget to classify an anchor that is already labelled. The skill body still defines what each value means and gives the derivation once for T2, where no `--jq` runs.

## Dependencies

- `gh` authenticated, or a GitHub MCP server — unchanged from the existing T1/T2 contract.
- `git` for the two in-repository rungs only.
- Network access for the fetch tiers.
- The design of record in `memory-bank/active/creative/creative-pr-feedback-judge-retrieval.md`.

## Challenges & Mitigations

- Challenge 1 — "tier" name collision. The document already uses `Tier`, `T1`, and `T2` for *fetch access*, and `Failure modes` references both by name. A second lettered "Tier A–D" ladder for *code access* would be ambiguous exactly where precision matters. Mitigation: name the code rungs by condition rather than by letter, and reserve `Tier`/`T1`/`T2` for fetch access. This is a deliberate wording deviation from the creative doc's "Tier A–D" labels; it satisfies the acceptance criterion in substance.
- Challenge 2 — fixed emoji set. `already addressed` has no natural mark in the existing ✅/❌/🕒 set, and the document constrains output to those three. Mitigation: do not add a fourth emoji; question 3 keeps ✅ and the prose carries "already satisfied on the current head." The disposition line is where the value appears.
- Challenge 3 — skill length. The file is 181 lines and this adds two sections plus edits to nine more. An over-long skill degrades adherence. Mitigation: keep the new sections tight, put recipes in the existing code blocks rather than new prose, and cut nothing that is load-bearing. If it bloats past readability, the anchor model is the part to compress, not the ladder.
- Challenge 4 — the need gate could be read as permission to skip code entirely. Mitigation: pair the gate with the loud-degradation requirement so choosing no code source is a stated, visible choice rather than a silent default.
- Challenge 5 — outdated could be misread as dismissible. Mitigation: step 5 states explicitly that anchor state never filters items, and the `already addressed` definition requires code evidence rather than anchor movement.
- Challenge 6 — the generated `.cursor/` and `.claude/` copies of this skill will lag after the change. Mitigation: correct per `systemPatterns.md` — those trees re-sync in a separate `chore(dev): ai-rizz sync` commit after this is pushed. Do not edit them here.

## Pre-Mortem

- The plan failed because the skill got longer and the agent followed it less. This is the most likely failure, and it is not fully covered by Challenge 3: length is a symptom, adherence is the outcome. Plan response — at step 11, judge the result behaviorally rather than by line count, asking whether an agent reading it cold would classify an anchor before judging. If not, cut the explanatory prose and keep the imperatives.
- The plan failed because it optimized retrieval and never changed a verdict. The whole point is different, better dispositions; a beautifully instrumented ladder that still emits the old four values would be a null result. Plan response — the live acceptance run in step 11 is promoted to the gating check, and it must show the outdated comment reaching a different verdict than the current skill would give it.
- The plan failed on a wrong premise: that `already addressed` is common enough to matter. The 41% outdated rate measures anchor movement, not resolved findings, and the two are not the same. Plan response — no scope change, but the acceptance run must confirm the disposition is reachable on a real comment. If it turns out unreachable in practice, that is a reflection-phase finding, not a build-phase fix.
- The plan failed because the rung ladder assumes the operator is judging their own PR while the code-access design serves the foreign-repo case. Two audiences, one document. Plan response — already covered by Challenge 1's naming discipline and step 9's foreign-repository failure mode; no further change.
- The plan failed because nothing verified the anchor fields survived projection, and a later editor tightened the `--jq` filter. Plan response — step 3 carries the prohibition inline in the skill body next to the filter itself, so the constraint travels with the code it constrains rather than living only in this plan.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
