# Decision: Hard-No / What-Must-Never Disposition

## Context

**What:** What to do with issue #78's secondary "Hard No's / What must this plan never allow?" idea.

**Why it matters:** Shipping a parallel negative checklist would fight prompt-authoring practice and may duplicate L3/L4 Invariants & Constraints. Declining without checking those hooks could leave a real gap.

**Constraints:**
- Operator bias: pre-mortem primary; hard-no suspect/possibly spurious
- Prompt-authoring: prefer positive "do this / how" over "don't do that / how not"; reserve "never" for literally true cases
- L3 plan already has **Invariants & Constraints** ("properties the correct solution must preserve")
- L4 plan already has **cross-milestone invariants** ("no milestone is permitted to violate")
- L2 plan has **no** invariants section — only Challenges
- Pre-mortem (Q1) already covers prospective failure imagination; this question is about *hard constraints*, not failure modes

## Options Evaluated

- **A — Decline entirely**: Document that hard-no is out of scope; ship pre-mortem only; leave Invariants as-is.
- **B — Fold into existing Invariants**: No new ritual; optionally clarify L3/L4 Invariants guidance so "plan must preserve X" covers the useful residue of "must never allow ¬X" — positive framing.
- **C — New Hard-No section** (L2+L3 or L3): Parallel checklist next to Pre-Mortem.
- **D — Add Invariants to L2 + clarify L3/L4**: Expand invariants coverage downward so L2 also names preservation rules.

## Analysis

| Criterion | A Decline | B Fold/clarify | C New Hard-No | D Invariants on L2 |
|-----------|-----------|----------------|---------------|---------------------|
| Prompt-authoring fit | Good | Best — positive preservation language | Poor — negative checklist | Good |
| Overlap with existing | Ignores useful residue | Uses existing hooks | Duplicates L3/L4 | Expands L2 ceremony |
| Simplicity | Highest | Small clarification | New section forever | Extra L2 section |
| Fitness for #78 secondary | Partial — may leave L3 wording weak | Strong — addresses residue without new ritual | Overbuilds | Scope creep vs issue |

Key insights:
- "What must the plan never allow?" and "What invariants must the solution preserve?" are the same constraint set with opposite polarity. Prompt-authoring says keep the positive form.
- L2's lack of invariants is intentional lean planning — Challenges + new Pre-Mortem are enough. Adding L2 invariants (D) is a different feature than #78.
- Option C recreates the problem the operator flagged.
- Option B is a light touch: ensure L3 (and if needed L4) Invariants guidance explicitly invites *plan-level* preservation rules (behavioral/safety properties), not only technical constraints — without renaming to "hard no."

## Decision

**Selected**: Option B — Fold into existing Invariants; decline a separate hard-no ritual

**Rationale:** The useful residue of "what must never" is already named Invariants & Constraints. Clarify that guidance (positive framing) rather than inventing a negative twin. Decline Option C explicitly in the plan/reflection trail so #78's secondary ask is answered.

**Tradeoff:** L2 still has no invariants section. Accepted: L2 pre-mortem + Challenges cover failure modes; hard preservation lists are L3+ weight. Not expanding L2 for this issue (YAGNI / D declined).

## Implementation Notes

- **Do not** add a Hard-No / What-Must-Never section to any plan template.
- In `level3-plan.md`, lightly strengthen the Invariants & Constraints bullet so it clearly covers plan-level properties that must hold (safety, compatibility, non-goals-as-preserved-boundaries) — still positive "must preserve / must hold."
- Touch `level4-plan.md` only if the existing cross-milestone invariants wording is already clear enough (likely: leave alone or one clarifying phrase). Prefer minimal change.
- In creative/plan docs and eventual issue closeout: state explicitly that hard-no was investigated and declined as a separate ritual.
- Pre-mortem and choice-pre-mortem prompts should only ask for likely causes and plan/choice responses — do not name or invite a parallel negative checklist in agent-facing copy.
