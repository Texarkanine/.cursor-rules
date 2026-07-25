# Active Context

## Current Task: rulesets-link-ci
**Phase:** BUILD - COMPLETE

## What Was Done
- Added `scripts/check-ruleset-symlinks.sh` and `scripts/check-ruleset-readme-links.sh` (POSIX, optional rulesets-root arg)
- Added `Makefile` with `test`, `test-symlinks`, `test-readme-links`
- Added `.github/workflows/rulesets-links.yml` with two PR jobs calling Make targets
- Documented `make test` in root `README.md`; noted Testing Process in `memory-bank/techContext.md`
- Verified: `make test` exits 0 on current tree; temp fixtures fail for dangling symlink and broken README link

## Files created/modified
- `/home/mobaxterm/git/.cursor-rules/scripts/check-ruleset-symlinks.sh`
- `/home/mobaxterm/git/.cursor-rules/scripts/check-ruleset-readme-links.sh`
- `/home/mobaxterm/git/.cursor-rules/Makefile`
- `/home/mobaxterm/git/.cursor-rules/.github/workflows/rulesets-links.yml`
- `/home/mobaxterm/git/.cursor-rules/README.md`
- `/home/mobaxterm/git/.cursor-rules/memory-bank/techContext.md`

## Next Step
- QA review
