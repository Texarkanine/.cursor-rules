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

## 2026-09-12 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 plan: two prose/policy units (`rules/always-tdd.mdc`, `rulesets/niko/skills/niko-preflight/SKILL.md`); no new tests.
    - Locked in-scope to the product-user consequence test; out-of-scope illustrations with `, etc.`; contract-test sentence names this product and skips when semver already signals.
    - Preflight: classify / expanded strike / FAIL-on-actual-executability; no third plan-mutation type.
* Decisions made
    - Did not lock the issue-body proposed wording.
    - Did not edit L2/L3 plan docs: planner already loads always-tdd; the failed path was preflight treating the label as decisive.
    - No in-scope category list (including no “product CLIs”) so vendored CLIs cannot be relabeled in.
* Insights
    - Inventing tests was the PASS path because FAIL still keyed off the plan’s “executable” label after a strike. The preflight FAIL bullet is the load-bearing echo, not a second copy of What TDD Governs.
