# Progress

Tighten always-tdd and niko-preflight TDD Plan Encoding so TDD and “contract tests” apply only to behavior a user of this product can observe breaking — not vendored tools, agent bootstrap, or gitignore lines ([issue #123](https://github.com/Texarkanine/.cursor-rules/issues/123)).

**Complexity:** Level 2

## 2026-09-12 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed intent: fix #123 as the failed #116 one-file bet; issue-body proposed wording is not locked; counterexample lists need `, etc.`; exclude #122.
    - Classified Level 2: bug spanning always-tdd and niko-preflight TDD Plan Encoding.
* Decisions made
    - Level 2, not L1 (two components) and not L3 (wording/steering, no architectural redesign).
* Insights
    - #116 archived the category-list replacement as a follow-up only if the one-file bet failed. This task is that follow-up, plus the preflight echo #116 deliberately skipped.
