# Project Brief

## User Story

As a Niko operator, I want plans stress-tested with a pre-mortem before build so that likely failure modes surface while the plan can still change — without bolting on a negative "what must never" checklist that fights prompt-authoring practice or duplicates existing constraints/invariants.

## Use-Case(s)

### Use-Case 1

During `/niko-plan` (or an adjacent phase), the agent runs a pre-mortem: "If this plan were to fail, what would be the likely cause?" Findings feed back into the plan (mitigations, scope cuts, open questions) before preflight/build.

### Use-Case 2

When evaluating the issue's secondary "Hard No's / what must never" idea, the agent investigates whether that need is already covered by plan-phase constraints/invariants (especially L3/L4). If so, strengthen or clarify those hooks rather than inventing a parallel negative checklist. If a residue remains, reframe it positively or drop it.

## Requirements

1. Add a **pre-mortem** lens to Niko's planning path as the primary deliverable ([issue #78](https://github.com/Texarkanine/.cursor-rules/issues/78)).
2. Decide placement (plan, creative, preflight, or new step) through design — not a bare paste of the issue prompts.
3. Investigate "what must never" / hard-no: treat as secondary; prefer existing constraints/invariants or drop/reframe rather than co-equal negative checklist.
4. Follow good prompt-authoring practice: prefer positive "do this / how" over "don't do that / how not."
5. Edit canonical sources under `rulesets/` (never `.cursor/` / `.claude/` generated copies).
6. Full Niko path including creative/design for open questions.

## Constraints

1. Canonical edits only in `rulesets/` (and `rules/` if applicable); installed trees are generated.
2. Do not invent a "hard no" ritual if constraints/invariants already cover the need.
3. Pre-mortem must inject a new angle on plan deficiencies before execution commitment — not duplicate preflight's codebase-reality checks.
4. Changes must compose with existing L2–L4 plan/preflight/creative workflows.

## Acceptance Criteria

1. Pre-mortem is a named, operable part of the Niko planning path at the levels where it belongs.
2. Design rationale documents where it lives and why (vs creative/preflight).
3. "What must never" is either folded into constraints/invariants, reframed positively, or explicitly declined — with rationale.
4. Prompt wording follows prompt-authoring guidance (positive framing where possible).
5. QA/preflight of the change itself passes; issue #78 intent is satisfied without over-building.
