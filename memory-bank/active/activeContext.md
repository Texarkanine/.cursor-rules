# Active Context

## Current Task
Fix L4 Sub-Run Completion Flow (issue-54) — Rework: Option B

## Phase
BUILD - COMPLETE

## What Was Done
All 4 implementation steps complete:
1. `/niko` SKILL.md — full state routing with mermaid diagram (Step 2: State Routing with 2a/2b subgraphs)
2. `complexity-analysis.mdc` — stripped to pure classifier (Step 1: Classification Target — 3 lines replacing ~95 lines)
3. `milestones.mdc` — lifecycle table and prose updated to reference `/niko` instead of `complexity-analysis.mdc`
4. `level4-workflow.mdc` — diagram entry changed from "Complexity Analysis" to "/niko", subgraph renamed to "/niko State Routing"

## Key Decisions
- "Task complete?" check widened everywhere: REFLECT COMPLETE or L1 + QA PASS (not just L4 path)
- State routing fires regardless of user input
- Diagram carries branching; prose describes node bodies

## Files Modified
- `rulesets/niko/skills/niko/SKILL.md`
- `rulesets/niko/niko/core/complexity-analysis.mdc`
- `rulesets/niko/niko/memory-bank/active/milestones.mdc`
- `rulesets/niko/niko/level4/level4-workflow.mdc`

## Next Step
QA review
