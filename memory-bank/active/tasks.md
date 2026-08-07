# Task: verification-subagents-preflight-qa (rework pass 2)

* Task ID: verification-subagents-preflight-qa
* Complexity: Level 2
* Type: remediation (TDD routing + Plan tightening)

**Authority:** This file is the gospel for what to build next. Creative docs are exploration only. Live charts = `rulesets/niko/`.

## Decisions (operator 2026-08-07)

- TDD plan-encoding failure **is** `FAIL (rearchitect)` → Plan (operator path). No special `FAIL (TDD)` species.
- Durable fix is **Plan authorship**, not a special preflight auto-heal edge.
- Stockroom history of past TDD-preflight catches informs Plan tightening; repeated fails after that → postmortem.

## Test Plan (TDD)

Prose/policy — always-tdd carve-out. No change-detector tests.

### Behaviors to Verify

- [Dry-read]: no `FAIL (TDD)` in `rulesets/niko/` charts, skills, or `preflight-status.mdc`
- [Dry-read]: TDD plan-encoding Handle Results routes as rearchitect (kick back to Plan / operator)
- [Dry-read]: L2/L3 STOP lists no longer carve out TDD
- [Dry-read]: level plan docs (or shared plan guidance) require per-unit test-before-code ordering explicit enough that preflight’s TDD check is redundant for well-formed plans
- [make test] + [mmdc] on touched charts

## Implementation Plan

1. **Stockroom archaeology (before chart edits)** ← next
   - `/sr-search` (semantic + query as needed): sessions where preflight found TDD plan-encoding problems and how the fix was executed (what it read, what it changed in `tasks.md`)
   - Distill: checklist of Plan requirements that would have prevented those fails
   - Files: notes in this `tasks.md` or a short `memory-bank/active/creative/` exploration doc if helpful — **not** gospel until folded into step 3
   - **Seed hits** (stockroom semantic 2026-08-07; fetch full text next session):
     - `471d0da3-6139-440c-88af-0531efeb2796#19` / `#` session same — preview about TDD encoding amend
     - `5c63e90b-6214-42ca-af9a-93c12d65f27a#23`
     - `dd70d758-8bb8-4047-b16c-b942bcad584d#33`
     - High-signal preview class: “TDD plan encoding (blocking, fixed) — Implementation steps lacked per-unit …”

2. **Remove `FAIL (TDD)` species (with operator on any mermaid >1 line)**
   - Charts L2/L3/README: delete solid `FAIL (TDD)` → Plan edges; ordinary FAIL / rearchitect path remains
   - `niko-preflight` Handle Results + FAIL Next Steps: TDD encoding → same as rearchitect (operator `/niko-plan`); drop `FAIL (TDD)` status write
   - `preflight-status.mdc`: remove `FAIL (TDD)` value
   - L2/L3 STOP lists / auto-continue prose: remove TDD carve-outs
   - Build guards: no `FAIL (TDD)` branch (item 8 from CodeRabbit superseded / simplified)

3. **Tighten Plan phase TDD authorship**
   - Level 2/3/4 plan references (and/or always-tdd cross-links): require the same per-unit test-before-code explicitness preflight checks for
   - Prefer lifting patterns found in step 1 over inventing new liturgy

4. **Cheap non-TDD fixups** (one-liners OK without operator; mermaid with operator)
   - L2 `/archive` → `/niko-archive`; clear deferred bullet in old reflection
   - Progress summary: drop “mermaid unchanged”
   - Double-backtick Spawn charge spans in progress (brief already being rewritten)
   - Optional: clear `.qa-validation-status` before QA spawn; README long QA fixable/rearchitect split — **with operator** if multi-line/mermaid

5. **Verify** — `make test`, `mmdc`, `rg FAIL \(TDD\)` clean under `rulesets/niko/`

## Out of scope this pass

- Restoring solid auto Plan re-entry for TDD
- CodeRabbit L4 “add FAIL (TDD) edge”
- Retry counters on rearchitect loops

## Status

- [x] Pass-1 rework shipped (most of nine review items)
- [x] Pass-2 decisions recorded (brief + this plan)
- [ ] Stockroom archaeology
- [ ] Remove `FAIL (TDD)` species
- [ ] Tighten Plan TDD authorship
- [ ] Cheap fixups
- [ ] Verify
