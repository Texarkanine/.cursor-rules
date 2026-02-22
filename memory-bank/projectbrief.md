# Project Brief: niko2-level4-impl

## User Story

As a niko2 operator, I want Level 4 workflow support so that tasks too large to plan and execute in one pass can be broken down into tracked milestones and executed as a series of L1/L2/L3 sub-runs.

## Use-Cases

### Use-Case 1: Fresh L4 Task

Operator invokes `/niko` with a large, multi-milestone request. Complexity analysis classifies it as L4, generates a milestone list, writes it to `memory-bank/milestones.md`, and initiates the first sub-run by classifying that milestone as L1/L2/L3.

### Use-Case 2: L4 Re-entry

After a sub-run completes through reflect, operator invokes `/niko` again. Complexity analysis detects `memory-bank/milestones.md` presence, reads the milestone list, checks off the completed milestone, identifies the next unchecked one, and classifies it as L1/L2/L3 for the next sub-run.

### Use-Case 3: L4 Capstone Archive

Operator invokes `/niko` after all milestones are checked. Complexity analysis detects completion, routes to the L4 archive phase. Capstone archive inlines all sub-run reflections, documents how the milestone list evolved, and summarizes the final system state. Ephemeral files cleared.

## Requirements

1. `level4-workflow.mdc` — describes the milestone-based loop: how L4 operates at the complexity-analysis level, sub-run routing, no dedicated plan/build (those come from the sub-run's complexity level), capstone archive trigger
2. `level4-archive.mdc` — capstone archive format: original milestone list, how it evolved, each sub-run's key outcomes (inlined from their reflections), final system state
3. `complexity-analysis.mdc` updates — L4 detection via `milestones.md` presence, milestone generation for fresh L4 (produce bullet list of milestones), re-entry logic (read milestone list, check off completed, pull next), completion detection (all checked → capstone archive)
4. `memory-bank-paths.mdc` update — add `memory-bank/milestones.md` as a new ephemeral L4-specific file with lifecycle description
5. SKILL.md stubs updated — `.claude/skills/level4-workflow/SKILL.md`, `.cursor/skills/shared/level4-*/SKILL.md` currently stub; need to route correctly (level4-workflow loads level4-workflow.mdc; level4-archive loads level4-archive.mdc; level4-plan and level4-build remain not-applicable stubs per the design)
6. `memory-bank/systemPatterns.md` update — current L4 entry incorrectly shows sequential workflow; update to reflect milestone-based composition

## Key Design Decisions (from previous session, already resolved)

- **L4 = project composition**: not a sequential workflow — complexity analysis IS the L4 plan; sub-run builds ARE the L4 build. No dedicated `level4-plan.mdc` or `level4-build.mdc` needed.
- **Milestone list storage**: `memory-bank/milestones.md` — dedicated file, presence = L4 in-flight (resolved via standalone creative phase, 2026-02-21)
- **No capstone reflect**: sub-run reflections accumulate and cover it; the capstone archive IS the retrospective synthesis
- **No archive between sub-runs**: ephemeral files persist across sub-runs; milestone list mutates; reflections accumulate
- **Milestone mutation on re-entry**: happens in complexity analysis at `/niko` re-entry, not in reflect (reflect is backward-looking)

## Constraints

1. Do NOT add `level4-plan.mdc` or `level4-build.mdc` — L4 has no dedicated plan/build; those stubs stay empty with a clear comment
2. The complexity-analysis.mdc changes must not break L1/L2/L3 detection — the milestones.md check is a pre-pass before normal classification
3. All new content must match niko2 density calibration: dense actionable prose, no bloat
