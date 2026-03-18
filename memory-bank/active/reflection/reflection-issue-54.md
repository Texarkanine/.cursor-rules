---
task_id: issue-54
date: 2026-03-17
complexity_level: 2
---

# Reflection: Fix L4 Sub-Run Completion Flow

## Summary

Fixed the L4 sub-run completion flow across 5 rule files so that sub-runs correctly direct to `/niko` re-entry instead of `/niko-archive`, with L1 completion detection from natural state and ephemeral cleanup between sub-runs.

## Requirements vs Outcome

All 4 requirements delivered. One design refinement: the original plan proposed an artificial `L1 COMPLETE` state marker, but operator feedback guided the design toward inferring completion from naturally existing artifacts (`.qa-validation-status` PASS + Level 1 in `progress.md`). This was a better outcome — no coupling between L1's workflow and L4's re-entry logic.

## Plan Accuracy

Plan was accurate — correct files, correct sequence, correct scope. The L1 marker revision happened during planning (before build), not as a mid-build surprise. No steps were added, reordered, or removed during implementation.

## Build & QA Observations

Build was clean — each step was a focused text edit to a specific section of a rule file. QA found no substantive issues. Pre-existing note: L2 workflow diagram says `/archive` instead of `/niko-archive`.

## Insights

### Technical
- The L4 sub-run system implicitly requires a uniform "sub-run terminal state" interface, but L1/L2/L3 have fundamentally different lifecycles (L1 has no reflect/archive). When composing sub-workflows, the parent needs to handle each sub-workflow's terminal state indicators, or the sub-workflows need a uniform completion signal. We chose inference from existing artifacts, which is more resilient than requiring sub-workflows to adopt L4-specific markers.

### Process
- Operator pushback on the artificial marker was correct and improved the design. "Infer from what's already there" is a better principle than "write new state to signal completion." This reduces coupling and avoids requiring downstream workflows to know about upstream contexts they don't otherwise participate in.

### Million-Dollar Question

If sub-run re-entry had been foundational from the start, the reflect phases would never mention archiving directly. Archiving would be a concern of the parent context only — standalone tasks get archived, L4 sub-runs get managed by L4 workflow. The current design is close to this: reflect phases now delegate the next-step decision to a milestones.md presence check rather than hardcoding `/niko-archive`.
