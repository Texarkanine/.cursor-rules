# Progress: Fix L4 Sub-Run Completion Flow (issue-54)

Fix the L4 sub-run completion flow so that sub-runs within L4 direct to `/niko` re-entry instead of `/niko-archive`, with proper ephemeral cleanup between sub-runs and L1 completion detection.

**Complexity:** Level 2

## History

- **Complexity Analysis**: Complete. Level 2 determined.
- **Plan Phase**: Complete. 6-step plan across 5 files. Revised per operator feedback (no artificial markers).
- **Preflight Phase**: PASS WITH ADVISORY.
- **Build Phase**: Complete. All 6 steps implemented.
- **QA Phase**: PASS.
- **Reflect Phase**: Complete. Key insight: infer from existing state.
- **Rework initiated**: Operator feedback — move L4 re-entry state management from complexity-analysis to /niko (Option B). Separation of concerns: /niko owns lifecycle/state routing, complexity-analysis owns classification only.
