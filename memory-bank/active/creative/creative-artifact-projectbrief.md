# Architecture Decision: Output Artifact and Relationship to projectbrief.md

## Requirements & Constraints
- **Quality attributes (ranked)**: (1) Downstream phases get a reliable source of truth, (2) No lossy compression of external specs, (3) Simplicity of ownership
- **Technical constraint**: Downstream phases (complexity analysis, planning, build) consume `projectbrief.md`. Whatever the intent loop produces must be compatible.
- **Scope**: How the approved restatement relates to `projectbrief.md`; not the restatement's internal format.

## Components

- **Intent clarification loop** (new): produces a user-approved restatement via dialogue
- **Complexity analysis** (`.claude/skills/complexity-analysis/SKILL.md`): currently creates `projectbrief.md` in Step 4
- **Plan phases** (L2/L3/L4): consume `projectbrief.md` for component analysis, requirements, test planning
- **`projectbrief.md`**: the file downstream phases read for "what the user wants"

## Options Evaluated
- **Option A (Restatement IS projectbrief)**: Intent loop writes the approved restatement directly to `projectbrief.md`. Complexity analysis changes from creator to consumer.
- **Option B (No artifact — dialogue only)**: Intent loop produces no file. The approved restatement lives in conversation context. Complexity analysis still writes projectbrief.md from the now-validated input. Plan phase expands the validated intent into a full brief.
- **Option C (Restatement feeds projectbrief)**: Intent loop writes restatement to a temporary artifact. Complexity analysis creates `projectbrief.md` using the restatement as input.

## Analysis

| Criterion | Option A (IS projectbrief) | Option B (Dialogue only) | Option C (Feeds projectbrief) |
|---|---|---|---|
| Reliable source of truth | Good — single writer | Good — existing pipeline unchanged | Risk — handoff complexity |
| No lossy compression | Good | Best — nothing to compress, external refs stay in context | Risk |
| Simplicity | Moderate — changes ownership | Best — minimal changes to existing system | Most complex |
| Cross-session persistence | Good — written to file | Risk — context lost between sessions | Moderate |

Key insights:
- The user clarified: the restatement is ephemeral dialogue context, not a persistent artifact. It stays in the conversation and informs the plan phase, which writes projectbrief.md.
- Complexity analysis still writes projectbrief.md as it does today — but from validated input rather than raw input.
- The intent crystallizes into the projectbrief during planning; after that, the restatement has no further purpose.
- Cross-session risk is acceptable because `/niko` re-entry detects active state and resumes from the last committed phase. If the session dies mid-intent-clarification, no ephemeral files exist yet, so `/niko` re-enters cleanly as "Fresh."

## Decision

**Selected**: Option B — No artifact; dialogue only
**Rationale**: Minimal changes to existing system. The intent clarification loop's value is in the dialogue (building shared understanding), not in producing a file. Complexity analysis and plan phases continue to work as designed, just with better input. External-spec references stay in context naturally without risk of lossy compression into a file.
**Tradeoff**: If session dies mid-intent-clarification, the dialogue is lost and the user must restart. Acceptable because no ephemeral files have been committed yet — the system is in a clean "Fresh" state.

## Implementation Notes
- Intent clarification loop: no file writes. Prints restatement, waits for user approval, loops if rejected.
- Complexity analysis Step 4: remove "prompting for clarification if requirements are incomplete or ambiguous" clause. It still writes projectbrief.md from the user's input (which is now validated).
- Plan phase: unchanged — continues to consume projectbrief.md and expand it.
- The approved restatement is available in conversation context for complexity analysis and the plan phase that follows in the same session.
