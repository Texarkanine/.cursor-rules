# Progress

Skip an enabled reviewer slug the catalog does not know, print a slug that can be placed, and exit successfully. Write nothing about the skip.

**Complexity:** Level 1

## 2026-10-15 - COMPLEXITY ANALYSIS - COMPLETE

* Work completed
    - Restated the bug: an unknown reviewer slug aborts `pick.py` even when other enabled slugs can be placed
    - Confirmed the skip is silent, so the caller sees only the printed slug
    - Classified the change as Level 1
* Decisions made
    - Level 1: one behavior in the picker, no new selection rule
* Insights
    - The skill tells the caller to use the printed slug and to read stderr only on a non-zero exit, so a warning line in the same output can be mistaken for the answer

## 2026-10-15 - BUILD - COMPLETE

* Work completed
    - An unknown enabled reviewer slug is skipped, with nothing written about it
    - A placeable slug is still printed and the process exits 0
    - The reported command prints `gemini-4-argon-medium`
    - `make test`: 110 tests OK
* Decisions made
    - A list of only unknown slugs prints the author, the existing empty-pool result
    - The thinking-stem test still proves `claude-sonnet-5-high` is not the thinking row, without requiring exit 2
* Insights
    - Exit 2 was also how one test showed two stems did not match. After a silent skip, that proof is "the unknown slug is not chosen"
