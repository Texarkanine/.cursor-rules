# Project Brief

## User Story

As the operator, I want preflight to judge and report, and to put existing TDD steps in test-before-code order when they are reversed, so it cannot become the planner except for that swap.

## Use-Case(s)

### Use-Case 1

Numbered steps say “write X, then write tests for X.” Preflight swaps them to “write tests for X, then write X,” records the finding, writes `PASS WITH ADVISORY`.

### Use-Case 2

Bookkeeping: one-line `.preflight-status`, progress, Phase, findings in `tasks.md`. No findings schema in the status file.

### Use-Case 3

No test steps, or a change-detector, or a design idea. Report only. Do not invent tests. Do not apply Radical Innovation.

## Requirements

1. Judge and report.
2. The only plan write is reordering **existing numbered steps** so test work comes before production work. Same steps. No new steps, cases, files, or stubs.
3. Bookkeeping writes stay (status enum, progress, Phase, findings section).
4. `.preflight-status` stays the one-line enum.
5. Missing test steps, and change-detectors, stay FAIL and do not patch.

## Constraints

1. Canonical edits under `rulesets/` only.
2. `niko-qa` unchanged.
3. No general plan amendment. No “emit the four always-tdd labels” rule — that adds steps.

## Acceptance Criteria

1. The skill forbids design amendments, synthesized tests, and applying Radical Innovation.
2. The skill tells the subagent: if test steps and production steps exist and are in the wrong order, put the test steps first.
3. After that swap: `PASS WITH ADVISORY` and a finding. Not `FAIL` for the swap itself.
4. Allowed writes: bookkeeping plus that swap.
5. The brief does not require writing missing always-tdd stages.

## Rework

Judge-only shipped. Operator: allow TDD reorder of existing steps — what preflight already did in the wild when it “amended for TDD ordering.” Plan 2 failed by also authorizing stage-label emission. This pass is swap-only. Concise skill prose is the build.
