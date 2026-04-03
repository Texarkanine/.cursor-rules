# Architecture Decision: Structural Form Within /niko

## Requirements & Constraints
- **Quality attributes (ranked)**: (1) Maintainability of state machine, (2) Consistency with existing patterns, (3) Readability
- **Technical constraint**: Must integrate with existing `/niko` state machine flowchart and step-definition pattern
- **Dependencies**: Q1 (only fires on Step 4 "has input" path), Q2 (writes projectbrief.md), Q3 (subsumes complexity analysis's clarification)

## Components

Current `/niko` state machine pattern:
- **Flowchart** = authoritative routing map showing nodes and edges
- **Step definitions** = prose below the flowchart explaining how to evaluate/execute each node
- **Substantial processing** is delegated to separate skill files via `Load:` directives (e.g., Step 6 loads `complexity-analysis/SKILL.md`)
- **Simple routing** is inline in step definitions (e.g., Step 5 reads two fields and loads a workflow)

## Options Evaluated
- **Option A (New step + skill file)**: New numbered step in flowchart, with `Load: .claude/skills/intent-clarification/SKILL.md`. Mirrors complexity-analysis pattern.
- **Option B (Sub-step 4a)**: Intent loop as Step 4a under Step 4. Keeps numbering stable.
- **Option C (Inline in /niko)**: Full loop logic in the step definition text.
- **Option D (Absorbed into complexity analysis)**: Complexity analysis gains an intent-clarification preamble.

## Analysis

| Criterion | A (New step + skill) | B (Sub-step 4a) | C (Inline) | D (Absorbed into CA) |
|---|---|---|---|---|
| Maintainability | Best — isolated changes | Moderate — Step 4 grows | Worst — bloats state machine | Poor — conflates concerns |
| Pattern consistency | Best — matches CA pattern | Poor — sub-steps are for subgraphs | Moderate — some steps are inline | Poor — violates Q2/Q3 ownership |
| Readability | Good — flowchart shows the step exists, skill has the details | Moderate — 4a implies sub-case of 4 | Poor — long step definition | Moderate |
| Requires renumbering | Yes (Steps 5→6, 6→7) | No | No | No |

Key insights:
- The state machine separates routing logic (flowchart) from processing logic (skill files). Intent clarification is processing logic — it has research, restatement construction, user interaction, and a convergence loop. It belongs in a skill file.
- Sub-steps in the existing pattern belong to subgraphs (L4 Re-entry, Standalone Re-entry). There's no "Fresh Input" subgraph for Step 4. Making 4a here breaks the pattern.
- Renumbering is a one-time cost. The flowchart is the authority, not the numbers — the numbers are just labels.
- Option D was already ruled out by Q2 (intent loop owns projectbrief) and Q3 (complexity analysis loses clarification responsibility).

## Decision

**Selected**: Option A — New numbered step + separate skill file
**Rationale**: Follows the established pattern (complexity-analysis is the precedent). Keeps the state machine readable by delegating processing to a skill file. Clean separation between routing and logic.
**Tradeoff**: Requires renumbering existing Steps 5→6 and 6→7. One-time cost, no ongoing impact.

## Implementation Notes
- New file: `.claude/skills/intent-clarification/SKILL.md` containing the full loop specification
- `/niko` state machine: insert new step between Step 4 "has input" and current Step 6 (Classify Complexity)
- Renumber: current Step 5 (Resume) → Step 6, current Step 6 (Classify) → Step 7
- New Step 5 definition: `Load: .claude/skills/intent-clarification/SKILL.md`
- Flowchart edge: Step 4 "has input" → Step 5 (Clarify Intent) → Step 7 (Classify Complexity)
- Step 5 is an action node (not a decision node) — it always proceeds to Step 7 upon completion
