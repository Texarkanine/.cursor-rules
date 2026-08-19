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

## Rework (issue #114)

As described in https://github.com/Texarkanine/.cursor-rules/issues/114. Judge-only plus TDD step-swap already shipped; this pass is the rest of the Preflight contract.

Supersedes Requirement 5 and Use-Case 3 on change-detectors (those stay in-phase, not FAIL). Missing tests on an executable unit, a convention/conflict that needs a different approach, and brief-level scope change are not in-phase — FAIL (fixable or blocking) by the “materially change the plan” line. Do not over-define that line. Do not emit missing always-tdd stages.

Four outs: **PASS** and **PASS WITH ADVISORY** unblock build (proceed if that level allows autonomy). **FAIL (fixable)** — known fix, planner must rewrite; parent → Plan, no operator, may loop. **FAIL (blocking)** — would materially change the plan; operator reviews and invokes `/niko-plan`.

In-phase (not a re-plan), both `PASS WITH ADVISORY`: TDD step-swap (already in the skill); strike scheduled change-detector tests (same steps, one deleted).

`FAIL (fixable)` name reuse with QA is intentional. Different checks, different semaphore files. Do not rename. Nine-site Spawn stem unchanged. QA edge rewrite, status-as-findings-store, and always-tdd stage emission are out of scope unless they fall out.

Likely touch: L2/L3 workflow charts and STOP lists; README charts if they still show a single Preflight FAIL; `niko-preflight` Handle Results plus change-detector strike; `preflight-status.mdc` allowed values. L4 already has solid FAIL → plan; split only if blocking vs fixable is needed. L1 has no Preflight.
