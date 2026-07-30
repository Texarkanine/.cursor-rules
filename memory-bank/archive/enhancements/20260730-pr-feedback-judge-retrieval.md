---
task_id: pr-feedback-judge-retrieval
complexity_level: 2
date: 2026-07-30
status: completed
---

# TASK ARCHIVE: PR Feedback Judge — Correct and Efficient Retrieval

## SUMMARY

Reworked `rules/pr-feedback-judge/SKILL.md` so verdicts rest on current code rather than stale review anchors: explicit anchor state (computed in `--jq`), a need-gated code-access ladder, and an evidence-gated `already addressed` disposition. Measured corpus (86 PRs / 293 inlines) showed only 17% of anchors safe to read at face value. Shipped as [PR #100](https://github.com/Texarkanine/.cursor-rules/pull/100) (merged).

## REQUIREMENTS

- Classify every inline comment's anchor state before judging; never index current code by `original_line`.
- Resolve outdated anchors by locating `diff_hunk` content, not by line number.
- Gate code access on need; four-rung ladder (at PR head → in-repo off-head → raw contents → size-gated clone).
- Add `already addressed` as a fifth disposition, requiring code evidence.
- Project fetches to rubric fields; retain every field staleness detection needs; declare the rung used and degrade loudly when code is unreachable.
- Out of TDD scope (skill wording / change-detector carve-out). Out of scope: standalone transport rule, PR-review skill. Generated trees not touched in-task.

## IMPLEMENTATION

**Design of record** (creative, later deleted from `active/` before archive): anchor-state model + need-gated ladder + `already addressed` as one coordinated decision; rejected standalone transport rule and PR-review skill at operator direction.

**Preflight amendment:** compute `anchor` in the T1 `--jq` projection (`file` / `outdated` / `current`) rather than asking the agent to derive it per item — converts the top adherence risk into a mechanical label.

**Files modified:**

- `rules/pr-feedback-judge/SKILL.md` — Anchor State; Reading the Code Under Review; `--jq` projections with computed `anchor`; URL-table Fetches notes; item-filter wording; five dispositions; intro/triage/tail; gate-and-escalate orchestration step; failure modes; header prose.
- `memory-bank/systemPatterns.md` — surgical note: generated-tree lag can flip mid-task agent decisions; prefer canonical `rules/` / `rulesets/` for load-bearing policy.
- `scripts/verify-skillify.py` — deleted post-review (migration-era change-detector; retired skills still listed after #89).

**Naming:** code-access rungs named by condition, not lettered — skill already uses `Tier`/`T1`/`T2` for fetch access.

## TESTING

No new automated tests — skill wording; content assertions would be change-detectors under `always-tdd`.

- `make test` green (symlink + README-link gates).
- Live acceptance on `#discussion_r3653815924` (PR #91): `anchor=outdated`, declines `original_line=47`, locates via `diff_hunk`, off-head fetch leaves status and worktree list clean.
- Preflight PASS (six blocking checks + adopted innovation); QA PASS.
- Whole-script `verify-skillify.py` was red at baseline for unrelated missing skills; build asserted this skill's structure directly, then the script was removed.

## LESSONS LEARNED

- Prefer moving a classification policy into an existing transform (`--jq`) over restating it as a per-item instruction.
- Generated-tree lag is a decision risk, not just a sync inconvenience: stale alwaysApply copies of `always-tdd` and `niko-preflight` would have produced the wrong TDD and preflight calls in this same task.
- When a purpose-built verifier is red at baseline for unrelated reasons, name the targeted substitute assertion in the plan's verify step — do not discover it only at build step 11.
- Live acceptance made the defect concrete: current L47 of the edited skill is unrelated Anchor State prose, exactly what a naive `original_line` read would have quoted.

## PROCESS IMPROVEMENTS

- For load-bearing policy decisions mid-task, read canonical `rules/` / `rulesets/` rather than generated `.cursor/` / `.claude/` copies.
- Promote a live acceptance run to the gating check when the deliverable is a different verdict, not merely better instrumentation.

## TECHNICAL IMPROVEMENTS

- Four-way duplication of the inline `--jq` expression left as deliberate recipe surface for agent copy-paste; not DRY debt to collapse.
- After merge: `chore(dev): ai-rizz sync` refreshes generated trees (already done on this line of history).

## NEXT STEPS

None for this task. Separate open work (mb-init AGENTS/CLAUDE awareness, issue #101) is unrelated and was excluded from PR #100.
