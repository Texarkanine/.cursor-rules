# Progress: Fix L4 Sub-Run Completion Flow (issue-54)

Fix the L4 sub-run completion flow so that sub-runs within L4 direct to `/niko` re-entry instead of `/niko-archive`, with proper ephemeral cleanup between sub-runs and L1 completion detection.

**Complexity:** Level 2

## History

- **Complexity Analysis**: Complete. Level 2 determined — bug fix affecting L2 reflect, L3 reflect, L1 workflow, and complexity-analysis re-entry logic.
- **Plan Phase**: Complete. 6-step implementation plan across 5 canonical files in `rulesets/niko/`. 10 verifiable behaviors defined. No new technology.
