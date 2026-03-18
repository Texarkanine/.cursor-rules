# Active Context

## Current Task
Fix L4 Sub-Run Completion Flow (issue-54) — Rework: Option B, continued

## Phase
PLAN - IN-PROGRESS

## What Was Done
Operator feedback: L4 workflow still redundantly describes /niko state routing (checkoff, cleanup, resume, classify). Now that /niko owns all state routing, level4-workflow.mdc should only describe what's unique to L4: the initial kickoff (plan → preflight → review) and phase mappings.

## Next Step
Plan and implement the simplification of level4-workflow.mdc
