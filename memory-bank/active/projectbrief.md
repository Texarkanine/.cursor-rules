# Project Brief

## User Story

As the operator, I want `/niko-preflight` to judge the plan and report, and to put already-enumerated TDD steps into the prescribed always-tdd order when they are out of order, so a verifier cannot become the planner except for that one sequencing fix.

## Use-Case(s)

### Use-Case 1

An executable unit names tests but lists them after (or mixed with) production work. Preflight re-sequences those names into always-tdd order (stub tests → stub interface → write tests and run red → write code and run green), records the finding, and writes `PASS WITH ADVISORY`.

### Use-Case 2

Preflight keeps its own bookkeeping: `.preflight-status` (exactly one allowed value), a progress note, the `**Phase:**` field, and a `## Preflight Findings` section in `tasks.md`. It does not grow the status file into a findings store.

### Use-Case 3

An executable unit has no test steps, or a change-detector is scheduled, or Radical Innovation suggests a design change. Preflight reports. It does not invent tests, remove change-detectors itself, or apply the innovation.

## Requirements

1. Preflight analyzes the plan and reports judgments.
2. The only allowed plan write is TDD re-order: already-enumerated test work moved ahead of already-enumerated production work, expressed as the prescribed always-tdd stages. No new cases, files, stubs, or behaviors.
3. Bookkeeping writes stay: `.preflight-status`, `progress.md`, `**Phase:**` in `activeContext.md`, findings appended in `tasks.md`.
4. `.preflight-status` remains the one-line enum in `preflight-status.mdc`. Findings stay in `tasks.md` / `progress.md` — do not invent a findings schema in the status file.
5. Missing tests on an executable unit, and change-detectors, stay FAIL. Those paths do not patch.

## Constraints

1. Canonical edits under `rulesets/` only. Do not edit generated `.cursor/` or `.claude/` trees.
2. `niko-qa` stays judge-only with no TDD-reorder carve-out.
3. Do not reopen general plan amendment or Radical Innovation apply.

## Acceptance Criteria

1. The live skill forbids in-scope design amendments, synthesized tests, and applying Radical Innovation.
2. The live skill tells the subagent to re-sequence already-enumerated TDD steps into the prescribed always-tdd order and to treat that as in-phase work.
3. After a successful re-sequence the status is `PASS WITH ADVISORY`, with the finding recorded. Status is not left `FAIL` solely because an order fix was applied.
4. Allowed writes are enumerated: bookkeeping plus that one TDD re-sequence. Implementation Plan units are otherwise read-only.
5. This brief no longer contains a live requirement that forbids TDD re-order.

## Rework

First pass shipped judge-only (no plan writes except bookkeeping). Operator 2026-08-19: layer TDD re-order on top of that. Preflight FAIL: the first-pass requirements still forbade self-heal. This plan-pass retracts those lines so the contract matches the layering.

Operator on this `/niko-plan`: the whole purpose is authorizing TDD reorder into the prescribed order. Everything else stays judge-and-report plus bookkeeping. Status-file-as-findings-store is out of scope.
