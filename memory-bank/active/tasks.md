# Task: niko-plan-premortem

* Task ID: niko-plan-premortem
* Complexity: Level 3
* Type: feature

Add a pre-mortem lens to Niko's planning path ([issue #78](https://github.com/Texarkanine/.cursor-rules/issues/78)). Investigate whether "what must never" / hard-no is redundant with existing constraints/invariants.

## Component Analysis

### Affected Components
- **L2 Plan** (`rulesets/niko/skills/niko/references/level2/level2-plan.md`): Has Challenges & Mitigations (step-scoped prospective risk); no invariants section; no creative. Candidate for pre-mortem if L2+ is in scope.
- **L3 Plan** (`rulesets/niko/skills/niko/references/level3/level3-plan.md`): Has Invariants & Constraints (static) + Challenges & Mitigations (step-scoped) + mid-plan creative loop. Primary insertion surface.
- **L4 Plan** (`rulesets/niko/skills/niko/references/level4/level4-plan.md`): Has cross-milestone invariants (static); defers detailed risk to L1–L3 sub-runs. May need only a light touch or none.
- **Preflight** (`rulesets/niko/skills/niko-preflight/SKILL.md`): Codebase-reality validation + Radical Innovation advisory. Wrong home for prospective failure brainstorming (would duplicate/confuse).
- **Creative** (`rulesets/niko/skills/niko-creative/SKILL.md`): Open-question design only. Wrong home for routine plan stress-test.
- **Prompt authoring** (`prompt-authoring` skill): Guides positive framing; informs how pre-mortem and any hard-no residue are worded.

### Cross-Module Dependencies
- Plan → Creative (L3 only, mid-plan) → Plan resume → Preflight → Build
- Pre-mortem findings must be able to feed back into plan content (mitigations, open questions, scope cuts) before preflight
- Reflect already asks whether identified challenges materialized (L3) — pre-mortem output should remain compatible with that retrospective

### Boundary Changes
- Plan-phase procedure and `tasks.md` template sections change (agent-facing contract for plan artifacts)
- Possibly level workflows if a new named step needs explicit phase mapping (unlikely if kept inside plan)
- No change to memory-bank file taxonomy expected

### Invariants & Constraints
- Canonical edits only under `rulesets/`
- Pre-mortem must not duplicate preflight's codebase-reality checks
- Prefer positive prompt framing; avoid inventing a parallel "hard no" ritual if invariants/constraints already cover it
- Must compose with existing L2–L4 workflows without forcing creative on L2

## Open Questions

- [x] **Q1: Pre-mortem placement & relationship to Challenges & Mitigations** → Resolved: Dedicated Pre-Mortem step in plan after Implementation Plan, before Challenges; complementary to step-scoped Challenges; not creative/preflight (see `memory-bank/active/creative/creative-premortem-placement.md`)

- [ ] **Q2: Which complexity levels receive pre-mortem**
  - Problem: L2 only, L3 only, L2+L3, or also L4 top-level?
  - Why ambiguous: L2 has Challenges but no creative; L4 has invariants but defers detail to sub-runs; over-applying adds ceremony to small plans.
  - Constraints: Proportional to level; L1 stays lean; L4 sub-runs inherit whatever their level gets.

- [ ] **Q3: Disposition of "what must never" / hard-no**
  - Problem: Keep as separate ritual, fold into Invariants & Constraints, reframe positively, or decline?
  - Why ambiguous: Issue floated it; operator suspects it's spurious and conflicts with prompt-authoring; existing invariants may already cover the need.
  - Constraints: Prefer positive framing; do not invent parallel negative checklist if existing hooks suffice; document rationale either way.
