# Progress

Fix `shell-posix-style.mdc` examples called out in issue #82: replace `set -eu`-incompatible post-command `$?` checks with inline `if`/`if !` handling, and replace the unsafe positional-arg save/restore round-trip with a function-scoped approach — after validating both changes are correct.

**Complexity:** Level 1

## 2026-07-14 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed intent against issue #82 and existing guide anchors
    - Classified as Level 1 (single-component documentation bug fix)
* Decisions made
    - Level 1: skip plan/creative/preflight/reflect/archive; go straight to build then QA
* Insights
    - `rulesets/shell/shell-posix-style.mdc` and `rules/shell-posix-style.mdc` are identical mirrors; edit canonical ruleset and sync
