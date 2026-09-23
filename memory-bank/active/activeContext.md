# Active Context

## Current Task: effort-variant-slug
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- `place_effort` places an unmatched effort spelling between the stored effort and the next stored score. A tier boundary keeps the higher tier. Rows with `score_source` `effort` are not anchors.
- `select` ranks those in-memory rows and does not write `catalog.json`. An author spelling that cannot be placed is returned as given. An unplaceable reviewer still raises `SelectionError`.
- `refresh.md` describes that behavior. `SKILL.md` is unchanged.
- `make test`: 55 tests OK.

## Next Step
- QA the build.

## Files
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/scripts/modelpool.py`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/scripts/pick.py`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/references/refresh.md`
- `/home/mobaxterm/git/.cursor-rules/tests/choose-verification-model/test_pick.py`
- `/home/mobaxterm/git/.cursor-rules/tests/choose-verification-model/test_shipped.py`

## Deviations
- The nudge fixture uses an effort-source row at the landing score. A real stored row in that gap would have been the far neighbor, so the interpolated score would not have landed on it.
- Preflight advisory A is in the code: siblings and far rows skip `score_source == effort`. Advisory B is the `select` and `main` docstring updates. Advisory C, the both-siblings branch, stayed and has a test.
