# Architecture Decision: Which Paths Need Intent Clarification

## Requirements & Constraints
- **Quality attributes (ranked)**: (1) Zero friction on pre-validated input, (2) Maintainability, (3) Simplicity
- **Technical constraint**: Must integrate with existing `/niko` state machine without breaking L4/rework flows
- **Scope**: This decides WHERE the loop fires; HOW it works is addressed by other open questions

## Components

Four paths currently reach Step 6 (Classify Complexity):

1. **Step 4 "has input"** — Fresh start, raw user input, never validated
2. **Step 2 "not started"** — L4 milestone description as classification target. Written during L4 planning, already user-approved.
3. **Step 2a "milestones remain"** — Next milestone after completing a sub-run. Same source as #2.
4. **Step 3b (rework)** — User just provided rework context in Step 3a dialogue. Original intent was approved; rework feedback is scoped.

## Options Evaluated
- **Option A (Fresh input only)**: Intent clarification fires only on Step 4 "has input" path. All other paths skip it.
- **Option B (All paths)**: Every path to Step 6 gets intent clarification. Consistent but redundant.
- **Option C (Fresh + rework)**: Skip L4 milestones only; rework gets clarification.

## Analysis

| Criterion | Option A (Fresh only) | Option B (All paths) | Option C (Fresh + rework) |
|---|---|---|---|
| Zero friction | Best — skips pre-validated | Worst — restates validated intent | Middle — rework was just discussed |
| Maintainability | Simple — one integration point | Moderate — multiple integration points | Moderate — conditional logic |
| Simplicity | Simplest | Most consistent but over-applied | Middle complexity |
| Risk | Low — only skips already-validated paths | Low — but adds friction | Low |

Key insights:
- The unifying principle: intent clarification bridges raw, unvalidated input to a validated understanding. On every path except Step 4, that bridging has ALREADY happened at a prior point in the workflow.
- L4 milestones were approved during L4 planning. Rework context was gathered in Step 3a/3b dialogue.
- Step 4 "has input" is the ONLY entry point where truly unvalidated user input enters the pipeline.

## Decision

**Selected**: Option A — Fresh input only (Step 4 "has input" path)
**Rationale**: This is the only path where unvalidated input enters the system. All other paths have already been through a validation loop (L4 planning approval, rework dialogue). Applying intent clarification to them is redundant friction.
**Tradeoff**: If L4 milestone descriptions are somehow insufficiently specified, the gap won't be caught here. Accepted because L4 planning already validates milestones.

## Implementation Notes
- Single integration point: between Step 4's "has input" outcome and Step 6 (Classify Complexity)
- No conditional logic needed — it's a simple insertion into one path
- Other paths to Step 6 remain untouched
