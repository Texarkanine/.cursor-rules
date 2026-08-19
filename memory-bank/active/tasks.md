# Task: preflight-analyze-and-report

* Task ID: preflight-analyze-and-report
* Complexity: Level 2
* Type: simple enhancement (rework, plan 3)

Restore the historic TDD-order amendment as one short exception on the shipped judge-only skill. Swap existing numbered steps. Do not invent a sequencing machine.

Reference: pre-judge-only `niko-preflight` invited “plan amendments”; stockroom heals that worked were test-before-code swaps of steps already in the unit. The old TDD check’s FAIL-rearchitect line stays for “no test steps.”

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: `make test`
- Test location: `scripts/`
- Conventions: layout/link gates
- New test files: none

## Implementation Plan

### 1. Brief is swap-only — prose/policy

- Files: `memory-bank/active/projectbrief.md`
- No tests: prose/policy artifact

1. Already applied this plan-pass. Live contract is Use-Case 1 (swap). Stage-label emission is out.

### 2. Short TDD-order exception in the skill — prose/policy

- Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
- No tests: prose/policy artifact

Write the smallest wording that does all of this. Do not add eligibility algorithms, one-to-one mappings, or before/after schemas.

1. **TDD Plan Encoding:** Keep the current checks. Add: if a unit already has test steps and production steps and they are in the wrong order, put the test steps first (same steps). Then continue. If there are no test steps, FAIL (rearchitect) as now. Change-detectors unchanged.
2. **Judge, Do Not Fix:** Keep the exclusive allowlist. Add that one swap to allowed writes. Still: no new steps, cases, files, stubs, behaviors; no other plan edits; status file stays the enum.
3. **Handle Results:** After that swap, `PASS WITH ADVISORY` and a finding. Do not `FAIL` for the swap itself.

Target length: a few sentences across those three sites, not a new subsection of policy.

## Technology Validation

No new technology - validation not required

## Dependencies

- Current judge-only skill text
- Pre-judge-only amendment behavior (historic), not its open-ended “make the change” / “plan amendments” license
- `niko-qa` unchanged

## Challenges & Mitigations

- **Prose bloat:** if a sentence is only there to prevent a clever misread, cut it; the allowlist already forbids synthesis.
- **“Prescribed always-tdd order” creep:** that phrase is how plan 2 added stages. This plan says “test steps first.”

## Pre-Mortem

- **Plan 2 again:** if step 2 mentions writing stub/red/green labels, it has failed.
- **Skill stays mute on the swap:** then historic TDD heals stay unofficial. The add in TDD Plan Encoding is the load-bearing sentence.

## Prior Preflights

Plan 1 FAIL: brief still forbade all self-heal. Plan 2 FAIL: stage labels vs “must not add steps.” This plan takes the swap-only cut.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight - PASS
- [x] Build
- [ ] QA
