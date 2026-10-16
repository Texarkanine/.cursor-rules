# Current Task: skip-unknown-reviewer-slugs

**Complexity:** Level 1

## Fix

An enabled reviewer slug missing from the catalog raised `SelectionError`. `pick.py` then exited 2 and printed nothing, so one unknown slug aborted the pick.

`select` now skips that slug and keeps going. Nothing is written about the skip. A placeable slug is still printed, and the process exits 0. A list of only unknown slugs prints the author, which is the existing empty-pool result.

Files: `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/scripts/pick.py`, `tests/choose-verification-model/test_pick.py`, `tests/choose-verification-model/test_shipped.py`.
