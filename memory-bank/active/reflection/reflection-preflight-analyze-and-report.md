---
task_id: preflight-analyze-and-report
date: 2026-08-19
complexity_level: 3
---

# Reflection: preflight-analyze-and-report

## Summary

Preflight is now a four-way semaphore (PASS / PASS WITH ADVISORY / FAIL (fixable) / FAIL (blocking)) with two in-phase plan writes (TDD step-swap and change-detector strike). Three passes on the same task: judge-only, swap-only, then the rest of https://github.com/Texarkanine/.cursor-rules/issues/114. QA PASS on this pass.

## Requirements vs Outcome

Delivered. Status vocabulary dropped bare `FAIL`. The skill strikes scheduled change-detectors in-phase, keeps the TDD swap, and routes the four strings. L2/L3/L4 charts and STOP lists, plus README short/long/L2/L3/L4 Init charts, match the pinned four-way fork. L1 and QA edges untouched. Nine-site Spawn stem unchanged. No missing always-tdd stages.

Earlier passes on this task: judge-only shipped, then swap-only. This pass supersedes “change-detectors stay FAIL and do not patch.”

## Plan Accuracy

The four-unit split (status, skill, workflows, README) was the right file list. Challenges named the real traps: STOP lists still saying “Preflight FAIL,” GitHub layout if Preflight were nested, and “re-run `/niko-preflight`” as a fixable next step. Those are what we edited. Two parallel PASS / PASS WITH ADVISORY edges (same destination and style) matched the pinned chart; L4 `ManualPlan -.-> NikoPlan` matched L2/L3 rather than leaving a dangling operator node.

Surprise was outside the plan’s touch list: `level{2,3}-build.md` still tell a parent that hit a failing status to re-spawn Preflight. The plan checked the Build *gate* (both FAILs block Build) and cleared it. The remediation sentence on that gate is a different site. QA logged it as a non-blocking advisory.

## Creative Phase Review

No creative phase. The issue specified the outs, the chart, the name-reuse, and the in-phase vs FAIL line. Nothing was a mega-unknown.

## Build & QA Observations

Build was prose/policy: no tests, `make test` green (symlink + README links). QA PASS with two advisories. Charts rendered under `mmdc`. No rework from QA.

## Cross-Phase Analysis

Plan 2 on the earlier rework failed because it tried to emit always-tdd stage labels. That lesson held: this plan said “do not invent tests; do not emit always-tdd stages,” and Build did not.

Retracting the brief before planning (change-detector strike is now in-phase) meant Preflight measured the intended contract, not the superseded “report only” AC. That was the process fix from the last reflection, applied.

The remaining causal chain: splitting an enum finer exposes every reader of the coarse value. Preflight updated the status file, skill, charts, and STOP lists. The Build-phase “if not PASS, spawn Preflight” sentence was a reader the plan did not list, so it survived.

## Insights

### Technical
- Edge *style* is the chart contract. A new result label must inherit the style of the edge it rides (`PASS WITH ADVISORY` on the existing PASS→build/review edge), or the STOP list and the diagram disagree.
- Splitting a result enum exposes every branch on the coarse value. The gate check and the remediation text attached to a failed gate are different sites.

### Process
- Rework that changes an AC must retract the old AC in the brief before the next Preflight, or Preflight fails the live contract. Done on this pass.
- `FAIL (fixable)` name reuse with QA is workable when the chart pairs the label with the destination (Preflight → Plan, QA → Build). Do not rename to dodge the collision.
