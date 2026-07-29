# Active Context

## Current Task: tdd-prose-carveout
**Phase:** REFLECT COMPLETE

## What Was Done
- Read the three persistent memory bank files at the operator's instruction; confirmed `rules/` and `rulesets/` are the source of truth and the `.cursor/` and `.claude/` trees are generated copies that must not be edited.
- Confirmed the operator's intent: implement [issue #95](https://github.com/Texarkanine/.cursor-rules/issues/95) as written. Determined **Level 2**: the issue already specifies the design, so no creative phase is earned, and the two edits are prose-only and independently valid.
- Surveyed TDD pressure across the niko skills. Confirmed the sibling TDD rules need no carve-out, since `java-gradle-tdd.mdc` is globbed to `*Test.java` and `shell-tdd` is scoped to shell scripts, both inherently executable.
- Planned a 5-step implementation across 2 files, recorded in `tasks.md`.

## Key Decisions
- **The boundary is behavioral, not a file taxonomy.** The prior failure was an agent recasting template assertions as "structural markers, not prose," which any list of artifact kinds invites. The decisive gate is instead: if the only way to make the test fail is to deliberately edit the artifact it asserts on, it is a change-detector, not a test. The artifact list stays for fast recognition, but the gate is what an agent lands on after arguing past the list.
- **Step 6 of preflight must be amended too.** Its "Verify test coverage is planned for all new behavior" is a second prose-test pressure point eleven lines below the guard, in the same file. Issue #95 does not mention it; leaving it would make the guard contradict a sibling check.
- **No automated tests for this change**, which is the carve-out applied to itself. The existing `make test` structural suite still runs, because it covers the ruleset symlink and README-link contract that both edited files are reachable from.
- **No change to `rulesets/niko/README.md`** line 24. The carve-out sharpens what counts as code rather than contradicting that one-line summary.
- **Known verification limit:** the only live preflight evidence available is this task's own run, which exercises requirement 4 (do not fail correct prose-only plans) and leaves requirement 3 (fail plans proposing prose tests) unexercised. QA reads the FAIL condition against the issue's `test_pr_template_and_title_ci.py` example instead.
- **Preflight passed the blocking TDD check under a recorded ambiguity.** The current FAIL condition targets implementation-only steps "under a 'we follow TDD' disclaimer"; this plan is implementation-only but argues its units are out of TDD scope and states the gate. Those differ, and whether the present wording distinguishes them is the defect being repaired. Resolved toward the intent of the change. Had it failed, the only compliant repair would have been to invent the prose tests the task prohibits.
- **Do not touch the tracked `.cursor/` copies.** They are tracked, but feature commits here touch `rules/` alone and the generated tree is re-synced under separate `chore(dev): ai-rizz sync` commits.
- **Heading renamed** to `## What TDD Governs`, avoiding collision with the existing `## 1. Determine Scope`.
- **Gate named `change-detector`** in both files, so review and future rules can cite it without restating the definition.

## Files Modified
- `/home/mobaxterm/git/.cursor-rules/rules/always-tdd.mdc` - added `## What TDD Governs`; opening paragraph rescoped to executable behavior.
- `/home/mobaxterm/git/.cursor-rules/rulesets/niko/skills/niko-preflight/SKILL.md` - steps 2, 6, and 9 amended.

## Build Outcome
- 21 insertions, 5 deletions across 2 files. No deviations from plan beyond the two amendments preflight recorded.
- `make test` passes. Confirmed the suite is not vacuous: `check-ruleset-symlinks.sh` fails on unresolvable symlink targets and is silent on success.
- Self-consistency confirmed. The amended preflight step 2 explicitly names "rule and skill wording" as carrying no test-before-code obligation, which is exactly this task's own deliverable, so the guard now passes this plan unambiguously rather than by the judgment call preflight had to make.
- Requirement 3 confirmed against the issue's example: `test_pr_template_and_title_ci.py` asserted markdown headings, a CONTRIBUTING link, and absence of checklists. The new FAIL condition names heading, link-presence, and checklist assertions on a document, and closes the "structural markers" relabeling.

## QA Outcome
- PASS across all seven constraints. One trivial fix applied: the opening sentence now names "What TDD Governs" instead of pointing at "the next section".
- Deliberate holds: duplicated change-detector definition, preflight step 6's redundant guard clause, no `rulesets/niko/README.md` change, no persistent memory-bank updates.

## Reflection Outcome
- Written to `memory-bank/active/reflection/reflection-tdd-prose-carveout.md`.
- Headline insight: a boundary written as a taxonomy of artifact kinds invites relabeling; a boundary written as a question about failure modes does not. When an agent keeps evading a rule, check whether the rule is drawn around categories instead of consequences.
- Persistent reconciliation: `systemPatterns.md` updated surgically to record that the tracked `.cursor/` tree is expected to lag behind feature commits and is re-synced separately, a fact this task had to reconstruct from git history. `productContext.md` and `techContext.md` needed nothing.

## Next Step
- Run `/niko-archive` to create the archive document and finalize the current project.
