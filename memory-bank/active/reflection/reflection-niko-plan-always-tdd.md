---
task_id: niko-plan-always-tdd
date: 2026-08-18
complexity_level: 3
---

# Reflection: niko-plan-always-tdd

## Summary

L2 and L3 Plan now emit typed units whose executable substeps are always-tdd stages in order. L3 Build names the same sequence as L2 Build. QA passed. The preflight TDD gate is unchanged.

## Requirements vs Outcome

Delivered the brief: Plan owns the schedule, always-tdd owns doctrine, preflight stays a blocking gate, prose/policy stays exempt. Did not add an explicit load (B) or point Plan at preflight FAIL clauses — both were recorded non-adds so the next executable Plan can measure structure-alone.

## Plan Accuracy

File list and unit order were right. Preflight amended three things before build (installed-path pointers, Behaviors exemption slot, L3 Build clash). Build did not reorder or split steps. The original Unit 3 "dry-read Build" clause was a conditional; preflight made it a confirmed one-line fix. Without that amendment, build would likely have skipped the clash.

## Creative Phase Review

D (template-as-schedule) held: stage names plus a closed-stack pointer were enough to write the docs without copying always-tdd. Friction is still ahead — whether Plan agents fill the new template is untested. B remains the right second instrument.

## Build & QA Observations

Build was prose/policy; no test-first cycle for this deliverable. Two mid-build progress saves, then QA. QA passed with no rework. Its advisory matches the creative: treat the next executable Plan as the live test of D.

## Cross-Phase Analysis

The task exists because agents copy the template harder than the instruction. Preflight found that same failure one section up: Behaviors to Verify had no exemption slot even after the Implementation Plan grew one. Preflight also found that L3 Plan and L3 Build named two rituals, while L2 Build was already correct — Plan had treated "Build" as one file. Causal chain: a gloss copied into Plan and L3 Build drifted together; aligning Plan without grepping Build would have left the drift in the execute path.

## Insights

### Technical

- Sibling fields encode membership. Numbered substeps encode order. Injecting always-tdd does not write `tasks.md`.
- The pretrained gloss "fail → pass → refactor" is not always-tdd: it skips stubbing and invents a refactor stage.

### Process

- When two phases must name one ritual, search the phrase in both. The L2 copy being right does not mean the L3 copy is.
- Completeness checks should read the template the agent fills, not only the instruction that describes it.
- Do not add a second salience instrument in the same diff as D. B is the follow-on if the next executable Plan still fails encoding.
