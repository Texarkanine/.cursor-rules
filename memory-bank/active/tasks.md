# Task: preflight-analyze-and-report

* Task ID: preflight-analyze-and-report
* Complexity: Level 2
* Type: simple enhancement (rework)

Rework the shipped judge-only preflight skill: TDD **re-order** of already-enumerated test steps is a fixable fail the subagent applies in-phase. Missing tests stay FAIL (rearchitect). Other plan amendments stay forbidden.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: `make test` (ruleset symlink + README link checks in `scripts/`)
- Test location: `scripts/`
- Conventions: layout/link gates, not skill-prose assertions
- New test files: none

## Implementation Plan

### 1. TDD re-order carve-out — prose/policy

- Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
- No tests: prose/policy artifact

1. In **TDD Plan Encoding**, split the order FAIL. If an executable unit already names test steps (cases, stubs, suite, or test files) but sequences them after or mixed with production steps — including TDD only in a preamble while those names live in Files/Changes — **re-sequence** so tests come first. Use only names already in the unit. Record the finding. Continue; the TDD check then passes. If an executable unit has **no** test steps, or the only TDD claim is a disclaimer with nothing to re-sequence, **FAIL (rearchitect)**. Change-detectors stay FAIL with the existing remove instruction (not a reorder).
2. In **Judge, Do Not Fix**, keep the exclusive allowlist and add one exception: the TDD re-sequence in step 1. That write may change Implementation Plan numbered steps **only** to put already-enumerated test work before already-enumerated production work. It must not add steps, cases, files, stubs, or behaviors. All other plan text stays read-only.
3. In **Handle Results**, state that a TDD order miss is fixed in-phase by the subagent; after a successful re-sequence the status is PASS or PASS WITH ADVISORY (finding recorded). Do not leave FAIL solely because an order fix was applied. Missing-test and change-detector FAILs still do not patch.

## Technology Validation

No new technology - validation not required

## Dependencies

- Shipped judge-only block in the same skill (steps 8–10)
- Operator rework brief: reorder already-enumerated tests; do not synthesize

## Challenges & Mitigations

- **"Encode stub → red → green" vs inventing tests:** allowed only when the unit already names the tests. Writing the four always-tdd stage labels around those names is a re-sequence. Inventing a `Behaviors to Verify` list or a new test file is not.
- **Ambiguous which lines are tests:** if the subagent cannot point at existing test steps, FAIL (rearchitect). Do not guess.
- **Allowlist hole:** the exception must be named and bounded. "Update tasks.md" remains findings-only plus this one rewrite.

## Pre-Mortem

- **Subagents treat any TDD miss as a license to write a suite:** already covered — no-test units FAIL rearchitect; exception forbids added steps/cases/files.
- **Status stays FAIL after a successful reorder, so build stays blocked:** Handle Results must say PASS / PASS WITH ADVISORY after an in-phase fix.
- **Wrong layer (Plan templates, not preflight):** Plan already emits the schedule; this carve-out is the verification pass the operator re-derived. Stay in the skill.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
