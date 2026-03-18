---
task_id: issue-54
date: 2026-03-17
complexity_level: 2
---

# Reflection: Fix L4 Sub-Run Completion Flow

## Summary

Fixed the L4 sub-run completion flow so sub-runs direct to `/niko` re-entry instead of `/niko-archive`, with proper cleanup and L1 detection. Then refactored to separate concerns: `/niko` owns state routing, `complexity-analysis` owns classification only.

## Requirements vs Outcome

All four original requirements delivered. The rework (Option B) was operator-initiated after the first build passed QA — it improved architecture without changing behavior. Preflight caught missing `milestones.mdc` cross-references; QA caught a pre-existing edge case (first entry after L4 plan) and fixed it in-line.

## Plan Accuracy

Original plan was accurate but prompted an architectural revision. Rework plan was tight — 4 steps, no deviations. Preflight proved its value by catching the `milestones.mdc` dependency that the plan missed. The "first-entry-after-L4-plan" edge case was pre-existing, not introduced by the refactor, but worth fixing during the rewrite.

## Build & QA Observations

Both builds were clean. The diagram-carries-branching pattern paid off: `/niko` SKILL.md absorbed 100+ lines of routing logic but stayed readable because the mermaid diagram handles all branching and prose only describes node bodies. `complexity-analysis.mdc` shrank from ~209 lines to ~116 lines — the re-entry check (95 lines of subgraphs and prose) replaced by a 3-line classification target step.

## Insights

### Technical
- Separating state routing from classification clarified both files' responsibilities. The original L4 implementation put re-entry logic in complexity-analysis because that's where classification happened — but routing and classification are different concerns. The refactor made both files simpler.
- "Infer from what's already there" > "write new markers." The widened "task complete?" check (REFLECT COMPLETE or L1+QA PASS) works for both L4 and standalone contexts without introducing new state.

### Process
- Operator-driven iteration (build → QA → reflect → rework → build) works well for design refinement. First pass establishes correctness; rework improves architecture. The ability to redirect after reflect but before archive was the right workflow seam.

### Million-Dollar Question
If the separation of concerns had been foundational from the start, `/niko` would always have been the state router and `complexity-analysis` would always have been a pure classifier. The original L4 implementation conflated them because classification was the only entry point that ran on every invocation. The current design — where `/niko` routes and complexity-analysis classifies — is the design that would have emerged from a clean-sheet approach.
