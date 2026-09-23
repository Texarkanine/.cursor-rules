# Active Context

## Current Task: choose-verification-model
**Phase:** BUILD - IN-PROGRESS

## What Was Done
- Preflight gate was `PASS WITH ADVISORY`; no creative-phase documents
- Unit 1: `select` and `pick.py` pass 14 tests. `make test` runs the new target plus the link checks
- A null-tier or null-score author exits 2, covering the preflight advisory
- Unit 2: `build_catalog` and `refresh.py` pass 11 tests, including refresh-then-pick
- Unit 3: shipped mapping and catalog for the nine spawnable slugs, tier `general`, scores from a live refresh
- Unit 4: `SKILL.md`, the niko ruleset symlink, and executable bits on both scripts
- Unit 5: nine spawn lines and the README now run `pick.py`

## Next Step
- Unit 6: PR CI job for the picker tests
