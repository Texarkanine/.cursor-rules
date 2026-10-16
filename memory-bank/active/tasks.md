# Current Task: skip-unknown-reviewer-slugs

**Complexity:** Level 1

## Fix

An enabled reviewer slug missing from the catalog raised `SelectionError`. `pick.py` then exited 2 and printed nothing, so one unknown slug aborted the pick.

`select` now skips that slug and keeps going. Nothing is written about the skip. A placeable slug is still printed, and the process exits 0. A list of only unknown slugs prints the author, which is the existing empty-pool result.

Files: `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/scripts/pick.py`, `tests/choose-verification-model/test_pick.py`, `tests/choose-verification-model/test_shipped.py`.

## QA Review

- Status: PASS
- KISS / DRY / YAGNI: The implementation uses a simple `continue` within the enabled slug loop in `modelpool.py`; no extra abstractions or unused parameters.
- Completeness: Meets all requirements in `projectbrief.md` — missing catalog slugs are skipped silently, available models are placed with exit 0, empty-pool fallback returns author, and no output is sent to stderr.
- Regression & Integrity: All 110 tests pass without errors; docstrings in `modelpool.py` and `pick.py` match updated behavior; no leftover scaffolding.

