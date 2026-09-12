---
name: nk-operator-dod-prready
description: Definition of Done - Pull Request Ready for Operator Review
---

# Definition of Done: PR Ready (Default)

This skill defines the default Definition of Done (DoD) for `/nk-operator`. Each task is driven through implementation, non-draft pull request creation, automated review and CI stabilization, and cleanly archived on its PR branch before being left open for Operator review.

## Success Criteria

A task is considered complete under `prready` when all of the following conditions are met:

1. **Test-Driven Implementation:** All requirements are implemented following TDD with 100% of new and existing test suites passing locally.
2. **QA Validation:** The task has achieved a `PASS` (or `PASS WITH ADVISORY`) from `/niko-qa`.
3. **Reflect Completed:** Reflection is recorded in `memory-bank/active/reflection/`.
4. **Non-Draft Pull Request Open:** A non-draft pull request against the target base branch is open, linking to the ticket (`Fixes #<id>`). If the repository defines a pull request template (e.g. `.github/pull_request_template.md`), follow it; otherwise, use the fallback template in `rulesets/niko/skills/nk-operator/references/default-pr-template.md`. Rely on ambient skills or CLI tooling rather than named external tools.
5. **Continuous Integration Green:** All automated status checks and CI workflows pass.
   - If CI fails, the worker attempts up to 2 automated test-driven fixes.
   - If CI remains red after 2 attempts, the worker halts and escalates to the Wave Operator / Operator as `BLOCKED`.
6. **Review Feedback Stabilized:** Automated reviewer bots (such as CodeRabbit, Cursor bot, or Copilot review) and reviewer comments are evaluated:
   - The worker runs `/pr-feedback-judge` against the pull request comments and review bodies.
   - Comments critiquing in-flight `memory-bank/active/` files (such as incomplete checkboxes) are dismissed by policy: `memory-bank/active/ is the in-flight execution state; it will be archived and deleted prior to merge.`
   - Critical or blocking findings (contract breaks, deleted endpoints, broken tests, security flaws, architecture/dataflow divergence) must be resolved via TDD.
   - The review loop is: `1 mandatory initial round + up to 2 follow-up rounds if critical blocking issues exist` (total rounds: between 1 and 3).
   - If critical blocking issues remain after 3 rounds, halt and escalate to the Wave Operator / Operator as `BLOCKED`.
7. **Clean Archive on the PR Branch:**
   - Once CI and review feedback are satisfied, the worker runs `/niko-archive` directly on the pull request branch.
   - The archive operation compiles all reflections, creative decisions, and rework learnings into a single, permanent archive document under `memory-bank/archive/<category>/YYYYMMDD-<task-id>.md`.
   - The `memory-bank/active/` directory is completely removed from the branch.
   - The worker commits the archive with `chore: archive <task-id> and clear memory bank` and pushes to origin.
8. **Pull Request Left Open:** The pull request remains open for final Operator inspection and merge. Workers never merge to the base branch.
