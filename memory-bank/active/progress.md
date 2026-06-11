# Progress

Two deliverables: (1) sharpen `rules/markdown-style.mdc` (tilde code-fence nesting,
no-hard-wrap rule, heading sub-rules, broadened globs); (2) author a new self-contained
prompt-authoring skill under `rulesets/` (classify-what-you-write lens, agent-ordering
guidance, cross-reference rules, Rossmann-derived prose style).

**Complexity:** Level 3

## 2026-06-11 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Cleared stale already-merged task state (#76) and committed the cleanup.
    - Confirmed intent with the operator (two-deliverable scope).
    - Classified the task as Level 3.
* Decisions made
    - Level 3 chosen: spans an existing-rule enhancement plus a new multi-file skill
      (multiple components / new reusable artifact), despite a largely pre-settled design.
* Insights
    - Canonical skill location for a non-niko general-purpose skill is unresolved; all
      current skills live under `rulesets/niko/skills/`. Resolve in Plan.
