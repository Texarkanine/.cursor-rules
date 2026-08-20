# Progress

Tighten TDD / preflight scope so developer-tooling wiring and invoke-only CI are not treated as executable product behavior, using the smallest steering wording rather than an exclusion list. Spec: [Texarkanine/.cursor-rules#116](https://github.com/Texarkanine/.cursor-rules/issues/116).

**Complexity:** Level 2

## 2026-08-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Validated intent against #116 and the SumMem#20 comment
    - Recorded operator authorship constraint: steer, do not enumerate incidents
    - Classified as Level 2
* Decisions made
    - Level 2: bug/error correction that is not a single-component typo; the work needs a design pass on wording, not an immediate one-line edit
* Insights
    - The two incidents share one misread ("if something executes it" = any runner), not two rules to add

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan: one prose/policy unit, no tests
    - Locked the replacement in-scope sentence; out-of-scope and change-detector text stay
* Decisions made
    - Smallest tweak is to make the product the owner of "executable behavior" and delete the poison sentence, not to list lint/CI exclusions
    - Do not edit niko-preflight; it already defers to always-tdd for the test-first process
    - Edit `rules/always-tdd.mdc` only (`rulesets/niko/always-tdd.mdc` is a symlink)
* Insights
    - The issue's proposed second paragraph is the N-guardrails move the operator asked us not to take
