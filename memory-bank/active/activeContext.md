# Active Context

## Current Task: issue-82-shell-posix-style-errexit-examples
**Phase:** BUILD - COMPLETE

## What Was Done
- Operator confirmed: no automated tests for skill/rule prose; correct-by-inspection + operator eye (and occasional out-of-band evals)
- Validated #82 claims under dash and bash (unreachable `$?` paths; `"$*"` restore splits/globs; proposed fixes work)
- Updated `rules/shell-posix-style.mdc`: inline error handling + function-scoped positional list; left `expr` alone
- Canonical path is `rules/`; `rulesets/shell/*.mdc` are symlinks

## Next Step
- QA phase (`niko-qa`)
