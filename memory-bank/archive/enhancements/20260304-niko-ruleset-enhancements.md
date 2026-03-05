---
task_id: niko-ruleset-enhancements
complexity_level: 2
date: 2026-03-04
status: completed
---

# TASK ARCHIVE: Niko Ruleset Enhancements

## SUMMARY

Three targeted improvements to the Niko ruleset in `rulesets/niko/`: (1) QA and Plan phases now enforce documentation updates alongside code changes; (2) Level 1 workflow includes a numbered Wrap-Up with explicit output-to-operator cleanup guidance for `memory-bank/active/`; (3) eight lazy internal rule path references were expanded to full `.cursor/rules/shared/niko/...` installed paths. Each item was committed separately for clean PR review.

## REQUIREMENTS

- **QA & Plan documentation**: QA must verify that project documentation affected by code changes was updated; Plan (L2/L3/L4) must include documentation update steps in implementation plans; L4 milestones that change documented behavior must include doc updates in scope.
- **L1 wrap-up**: Provide guidance for cleaning up `memory-bank/active/` after L1 tasks (no archive phase). Recommendation: lightweight numbered Wrap-Up with operator output, not a new phase.
- **Lazy path references**: All bare-filename `.mdc` references in Niko rule files must use full installed paths (e.g. `.cursor/rules/shared/niko/memory-bank/active/milestones.mdc`).
- **Delivery**: Separate commit per item; all edits in `rulesets/niko/` (canonical source only).

## IMPLEMENTATION

- **Item 1**: Added a **Documentation** constraint to `rulesets/niko/skills/niko-qa/SKILL.md` (same severity as missing requirement). Added documentation-planning bullets to `level2-plan.mdc`, `level3-plan.mdc`; added milestone-scope note to `level4-plan.mdc`. Commit: `feat: enforce documentation updates in QA and Plan phases`.
- **Item 2**: Replaced floating "Commit When Done" / "Cleanup" prose in `level1-workflow.mdc` with a **Wrap-Up** section: step 1 commit, step 2 print cleanup instructions to the operator (formatted block). Follow-up commit restructured this as numbered steps with explicit operator output. Commits: `docs: add memory-bank cleanup guidance to L1 workflow`, `docs: restructure L1 cleanup as numbered wrap-up steps with operator output`.
- **Item 3**: In `rulesets/niko/niko/memory-bank/active/milestones.mdc` lifecycle table, expanded five references (`level4-plan.mdc`, `complexity-analysis.mdc` x3, `level4-archive.mdc`) to full paths. In `level4-plan.mdc`, expanded three references (`milestones.mdc` x2, `complexity-analysis.mdc` x1). Left `common-fixes.mdc` in `activeContext.mdc` example block as-is (example prose, not a rule reference). Commit: `fix: expand lazy rule path references to full installed paths`.

Key files: `rulesets/niko/skills/niko-qa/SKILL.md`, `rulesets/niko/niko/level1/level1-workflow.mdc`, `rulesets/niko/niko/level2/level2-plan.mdc`, `rulesets/niko/niko/level3/level3-plan.mdc`, `rulesets/niko/niko/level4/level4-plan.mdc`, `rulesets/niko/niko/memory-bank/active/milestones.mdc`.

## TESTING

- No automated tests (rule-text only). Verification: manual review; ripgrep confirmed no remaining lazy `.mdc` references in rule instruction text. Preflight validated plan; QA passed all seven semantic constraints (KISS, DRY, YAGNI, Completeness, Regression, Integrity, Documentation).

## LESSONS LEARNED

- **Reference audits**: Distinguish rule references (instructions for agents to load/follow) from example or template prose (e.g. `activeContext.mdc` example block). Only the former need full-path expansion.
- **L2 scoping**: Three related enhancements with one commit each kept the PR reviewable and the history clear.
- **L1 structure**: Aligning L1 wrap-up with other levels’ “output to operator” pattern (numbered steps, explicit print block) avoids floating prose and matches phase conventions.

## PROCESS IMPROVEMENTS

- None beyond what was implemented (doc enforcement in Plan/QA; L1 wrap-up structure).

## TECHNICAL IMPROVEMENTS

- None. Additive rule changes only.

## NEXT STEPS

None. Sync canonical `rulesets/niko/` to `.cursor/` and `.claude/` per project tooling (e.g. ai-rizz / a16n) as usual.
