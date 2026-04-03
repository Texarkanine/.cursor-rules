# Architecture Decision: Interaction with Complexity Analysis Clarification

## Requirements & Constraints
- **Quality attributes (ranked)**: (1) No duplicate clarification loops, (2) Clear ownership boundaries, (3) Simplicity
- **Technical constraint**: Complexity analysis currently writes projectbrief.md AND prompts for clarification (Step 4 of complexity-analysis skill)
- **Dependency**: Q2 decided that the intent loop is dialogue-only; complexity analysis still writes projectbrief.md

## Context

Given Q2's resolution (intent loop is dialogue-only, no artifact), complexity analysis retains its projectbrief.md-writing responsibility. The only change is that the input it works from has already been validated by the intent clarification loop. Its "prompting for clarification" clause becomes redundant.

## Options Evaluated
- **Option A (Remove clarification from complexity analysis)**: Delete the "prompting for clarification" clause. Complexity analysis trusts the validated input.
- **Option B (Keep as safety net)**: Complexity analysis still checks for completeness but only prompts if something is critically missing for level classification.

## Analysis

Option A is the clear winner. The user just approved the restatement. Having complexity analysis re-prompt ("but are you sure about...?") undermines the intent loop and creates confusion. If the restatement was insufficient, the intent loop should have caught it.

Option B introduces the exact redundancy the feature eliminates.

## Decision

**Selected**: Option A — Remove clarification clause from complexity analysis
**Rationale**: The intent loop upstream is now the single owner of "do we understand what the user wants?" Complexity analysis focuses purely on classifying the validated input.
**Tradeoff**: None significant — complexity analysis's classification logic (decision tree, indicators, assessment questions) remains fully intact.

## Implementation Notes
- Complexity analysis Step 4: change "Populate it from the user's input, prompting for clarification if the requirements are incomplete or ambiguous" to "Populate it from the user's input (validated by the intent clarification step)"
- All other complexity analysis steps unchanged
