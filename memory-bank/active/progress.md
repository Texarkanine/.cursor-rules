# Progress: Fix L4 Sub-Run Completion Flow (issue-54)

Fix the L4 sub-run completion flow so that sub-runs within L4 direct to `/niko` re-entry instead of `/niko-archive`, with proper ephemeral cleanup between sub-runs and L1 completion detection.

**Complexity:** Level 2

## History

- **Complexity Analysis**: Complete. Level 2 determined — bug fix affecting L2 reflect, L3 reflect, L1 workflow, and complexity-analysis re-entry logic.
- **Plan Phase**: Complete. 6-step implementation plan across 5 canonical files in `rulesets/niko/`. 10 verifiable behaviors defined. Revised per operator feedback: no artificial markers, L1 completion inferred from natural state.
- **Preflight Phase**: PASS WITH ADVISORY. All checks passed. Advisory: defensive archive guard for L2/L3 archive phases (out of scope).
- **Build Phase**: Complete. All 6 steps implemented. No deviations from plan.
- **QA Phase**: PASS. All requirements verified, no blocking findings.
- **Reflect Phase**: Complete. Key insight: infer completion from existing artifacts rather than introducing artificial markers. Reduces coupling between workflow levels.
