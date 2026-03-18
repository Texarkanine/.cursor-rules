# Project Brief: Fix L4 Sub-Run Completion Flow

## User Story

As an operator using the Niko L4 workflow, when a sub-run (L1/L2/L3) completes within an L4 project, the "next step" guidance should direct me to re-enter with `/niko` (to continue to the next milestone), not to run `/niko-archive` (which would clean up `milestones.md` and break the L4 flow).

## Problem

1. **L2/L3 reflect phases** always output "Run `/niko-archive` to finalize" — even when the sub-run is part of an L4 project, where the correct next step is `/niko` re-entry.
2. **L1 workflow** has no reflect/archive phase and no re-entry guidance at all — it just ends with "Done" after QA passes. There's no mechanism for the L4 re-entry code to detect that an L1 sub-run completed.
3. **Ephemeral file cleanup** between sub-runs is not defined. Some cleanup must happen (tasks.md, activeContext.md, gate files) but milestones.md, progress.md, projectbrief.md, and reflection/ must be preserved.

## Requirements

1. L2/L3 reflect "Next Steps" must be context-aware: if `milestones.md` exists, direct to `/niko`; otherwise direct to `/niko-archive`.
2. L1 completion within L4 must be detectable by the `/niko` re-entry logic.
3. The complexity-analysis re-entry (Step 1a) must handle ephemeral cleanup between sub-runs — clean sub-run-scoped state while preserving L4-scoped state.
4. L4 workflow diagram and documentation must accurately reflect the corrected flow.

## Source

GitHub Issue: https://github.com/Texarkanine/.cursor-rules/issues/54
