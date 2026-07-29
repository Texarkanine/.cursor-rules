# Progress

Add an executable-versus-prose scope carve-out to `always-tdd.mdc` so TDD stops requiring invented assertions on human-facing prose, and amend `niko-preflight` so it fails plans that still propose such tests. Specified by [issue #95](https://github.com/Texarkanine/.cursor-rules/issues/95).

**Complexity:** Level 2

## 2026-07-29 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Read the persistent memory bank files and located the source of truth for both target artifacts: `rules/always-tdd.mdc` and `rulesets/niko/skills/niko-preflight/SKILL.md`.
    - Confirmed operator intent against issue #95 and wrote `projectbrief.md`.
    - Classified the task as Level 2.
* Decisions made
    - Level 2 rather than Level 3: the issue supplies the design, so a creative phase would be ceremony. The two edits are prose-only and independently valid, which makes the change self-contained.
    - Edit only `rules/` and `rulesets/`. The `.cursor/` and `.claude/` trees are generated copies.
    - Write no new tests for this change, which is the carve-out applied to itself. The repo's `make test` covers ruleset symlinks and README links only.
* Insights
    - `niko-preflight` step 6 "Completeness Precheck" is a second source of prose-test pressure that issue #95 does not mention. Amending only step 2 would leave the guard contradicting a sibling check in the same file.
    - This task is a live test of its own deliverable: it is a prose-only change that must pass the very preflight guard it installs. If the wording is too loose, preflight will not catch a bad plan; if too strict, preflight will fail this task's own correct plan.
