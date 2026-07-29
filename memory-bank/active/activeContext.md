# Active Context

## Current Task: tdd-prose-carveout
**Phase:** PLAN - COMPLETE

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

## Next Step
- Invoke the `niko-preflight` skill.
