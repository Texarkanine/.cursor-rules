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
    - `rulesets/shell/shell-posix-style.mdc` is a symlink to `rules/shell-posix-style.mdc` (edit `rules/`)

## 2026-07-14 - BUILD - COMPLETE

* Work completed
    - Shell demos confirmed both #82 defects and both proposed fixes (dash + bash)
    - Replaced unreachable `$?` examples with inline `if` / `if !` in variable-scope, return-value, and find sections
    - Replaced `"$*"` / unquoted restore with function-scoped `set --` positional list example
* Decisions made
    - No committed test harness for rule prose (operator: correct-by-inspection)
    - Keep intentional `expr` examples (out of scope per #82)
* Insights
    - Unsafe restore also glob-expanded in the working tree (`a*` matched real files) — strong teaching moment captured in the comment
