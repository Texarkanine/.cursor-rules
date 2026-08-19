# Task: preflight-analyze-and-report

* Task ID: preflight-analyze-and-report
* Complexity: Level 2
* Type: simple enhancement (rework, plan 2)

Layer one plan write onto shipped judge-only preflight: re-sequence already-enumerated TDD steps into the prescribed always-tdd order. Bookkeeping stays. No other plan edits. Status file stays the one-line enum.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: `make test` (ruleset symlink + README link checks in `scripts/`)
- Test location: `scripts/`
- Conventions: layout/link gates, not skill-prose assertions
- New test files: none

## Implementation Plan

### 1. Brief contract matches the layering — prose/policy

- Files: `memory-bank/active/projectbrief.md`
- No tests: prose/policy artifact

1. Already applied in this plan-pass: first-pass lines that forbade all TDD self-heal are retracted. Live requirements, use-cases, and acceptance criteria state the TDD re-order exception and keep every other plan write forbidden. Status-file findings schema is explicitly out of scope.

### 2. TDD re-order in the preflight skill — prose/policy

- Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
- No tests: prose/policy artifact

1. **TDD Plan Encoding:** If an executable unit already names test work (cases, stubs, suite, or test files) but sequences it after or mixed with production work — including TDD only in a preamble while those names live in Files/Changes — re-sequence into the prescribed always-tdd stages: stub tests, stub interface, write tests and run red, write code and run green. Use only names already in the unit. Writing those four stage labels around those names is the allowed form. If an executable unit has no test steps to re-sequence, FAIL (rearchitect). Change-detectors stay FAIL with the existing remove instruction.
2. **Judge, Do Not Fix:** Exclusive allowlist: `.preflight-status`, findings in `tasks.md` / `progress.md`, `**Phase:**` in `activeContext.md`, and the TDD re-sequence in step 1. The re-sequence may change Implementation Plan numbered steps only to put already-enumerated test work before already-enumerated production work in always-tdd order. It must not add steps, cases, files, stubs, or behaviors. All other plan text stays read-only. Do not write findings into `.preflight-status` beyond the one allowed enum value.
3. **Handle Results:** After a successful TDD re-sequence, write `PASS WITH ADVISORY` and record the finding. Do not leave `FAIL` solely because an order fix was applied. Missing-test and change-detector FAILs still do not patch.

## Technology Validation

No new technology - validation not required

## Dependencies

- Shipped judge-only block in the same skill
- `preflight-status.mdc` allowed values unchanged
- `niko-qa` deliberately unchanged — do not copy the TDD carve-out there

## Challenges & Mitigations

- **Ambiguous which lines are tests:** if the subagent cannot point at existing test steps, FAIL (rearchitect). Do not guess.
- **Four stage labels look like synthesis:** they are allowed only as the expression of already-named tests. A new `Behaviors to Verify` entry or a new test file is still synthesis and forbidden.
- **Findings durability:** `tasks.md` + `progress.md` already outlive the subagent session. Expanding `.preflight-status` would change a standing one-line contract; leave it.

## Pre-Mortem

- **Brief and skill drift again:** unit 1 is the retracted contract; unit 2 must not reintroduce "no TDD self-heal" without the exception.
- **Subagents invent a suite and call it re-order:** already covered — no names → rearchitect; no added cases/files.
- **Status-file findings creep:** Requirement 4 and skill step 2 say the enum only.

## Prior Preflight (plan 1)

FAIL 2026-08-19: brief contradiction (F1), encode-stages not in a numbered step (F2). Addressed in this plan. Advisories F3 (PASS WITH ADVISORY after re-sequence) and F4 (QA out of scope) folded in. Radical Innovation (before/after step receipt) not taken — a recorded finding is enough; a formal before/after schema is extra.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
