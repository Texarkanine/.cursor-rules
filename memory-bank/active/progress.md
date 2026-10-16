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
