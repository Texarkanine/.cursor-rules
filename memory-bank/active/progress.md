# Progress

Ship the `choose-verification-model` skill: a stdlib Python picker and a catalog refresh, then point Niko QA and Preflight at the picker so verification-model choice is a script run instead of an inference turn.

**Complexity:** Level 3

## 2026-09-23 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated the picker, the refresh, the three boards, and the scored-effort rule
    - Recorded the skill name `choose-verification-model`
    - Classified the task as Level 3
* Decisions made
    - Level 3, because the feature spans the skill, two executables, the catalog, the mapping, and the existing QA and Preflight selection text, and the selection rule is already specified
* Insights
    - Published SWE-bench rows name an effort only on Verified, and only as `(high)` or `(medium)`
