# Current Task: issue-82-shell-posix-style-errexit-examples

**Complexity:** Level 1

## Bug

Guide examples contradict its own `set -eu` mandate (`cmd; if [ $? …]`) and teach unsafe positional-arg restore (`"$*"` / unquoted `set --`).

## Why

Under `errexit`, a failing bare command exits before a following `$?` check. `"$*"` collapses args; unquoted restore word-splits and globs.

## Fix

- Inline `if` / `if !` for `sort`, `cp`/`mv`, and `find` assignment examples
- Function-scoped `set --` for the positional-parameter list example
- Validated under dash + bash; no automated tests (repo practice: skill/rule prose is correct-by-inspection)

## Files

- `rules/shell-posix-style.mdc` (canonical; `rulesets/shell/shell-posix-style.mdc` is a symlink)

## QA

- PASS — all acceptance criteria met; no YAGNI/KISS/completeness issues; `expr` left untouched
