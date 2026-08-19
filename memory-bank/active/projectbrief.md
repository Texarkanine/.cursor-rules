# Project Brief

## User Story

As the operator, I want `/niko-preflight` to analyze the plan and report findings without rewriting it, so a verifier cannot silently become the planner.

## Use-Case(s)

### Use-Case 1

A preflight subagent finds a TDD-encoding hole, a change-detector, or an in-scope Radical Innovation. It records findings and a PASS/FAIL status. It does not rewrite implementation units in `tasks.md`.

### Use-Case 2

A preflight subagent still writes the bookkeeping it owns: `.preflight-status`, phase in `activeContext.md`, a progress note, and (if needed) a findings section that does not change the plan.

## Requirements

1. Preflight analyzes the plan and reports judgments only.
2. Preflight must not amend the implementation plan in `tasks.md` (no TDD self-heal, no in-place unit rewrites, no applying Radical Innovation).
3. Status, progress, and phase bookkeeping remain allowed writes.
4. Findings may be recorded without changing planned units.

## Constraints

1. Canonical edits under `rulesets/` only. Do not edit generated `.cursor/` or `.claude/` trees.
2. TDD Plan Encoding stays a blocking rearchitect gate. This task does not reopen self-heal.
3. QA's judge-only shape is the existing pattern to match, not a second feature.

## Acceptance Criteria

1. The live `/niko-preflight` skill no longer instructs the agent to make in-scope plan changes or to update `tasks.md` with plan amendments.
2. Allowed writes are enumerated and do not include rewriting implementation-plan units.
3. Radical Innovation may still describe a change; it must not apply one.
4. A FAIL still tells the operator to fix via `/niko-plan` or a re-run after they change the plan — preflight itself does not patch.

## Rework

Operator 2026-08-19: keep judge-only for design amendments. Carve out **TDD ordering only**.

A preflight subagent that finds test steps already enumerated but sequenced after (or mixed with) production steps must treat that as a **fixable** fail and **re-sequence those steps itself** — tests before code — then continue. That is inside preflight's purview.

It must **not** invent tests. If a unit has no test steps (no named cases, stubs, or suite), that stays **FAIL (rearchitect)**. Preflight cannot turn "write X, write Y, write Z" into a TDD schedule.

Historic modal heal (encode stub → red → green around **already-named** tests) is the allowed generalization of a swap. New behaviors, new test files, or missing coverage stay report-only / rearchitect.

