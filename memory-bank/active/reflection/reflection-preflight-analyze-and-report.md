---
task_id: preflight-analyze-and-report
date: 2026-08-19
complexity_level: 2
---

# Reflection: preflight-analyze-and-report

## Summary

Preflight is judge-only plus one swap: existing test steps before existing production steps. Missing tests still FAIL. QA passed on the swap-only wording.

## Requirements vs Outcome

First pass shipped judge-only. Rework added the TDD-order exception the operator asked for. Plan 2 overbuilt (emit always-tdd stage labels) and FAILed preflight. Plan 3 (swap-only, short prose) shipped.

## Plan Accuracy

Plan 2’s “prescribed stages” phrase was the defect. Historic heals were step swaps, not a new template. The brief had to retract first-pass “no self-heal” lines so QA would not fail AC-2.

## Build & QA Observations

Build was three short edits in one skill. `make test` green. QA PASS, no advisories.

## Insights

### Technical
- “Put the test steps first. Same steps.” is the whole carve-out. Naming the four always-tdd stages in the skill is how you accidentally authorize adding steps.

### Process
- Rework that appends a new paragraph without retracting the old acceptance criteria will FAIL the next preflight. Update the live contract.

### Million-Dollar Question

What we built. The old open “plan amendments” license produced the useful TDD swaps *and* the SumMem overfit. The exclusive allowlist plus one swap sentence is the split.
