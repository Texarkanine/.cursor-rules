---
task_id: standing-contract-reconcile-guard
date: 2026-08-04
complexity_level: 2
---

# Reflection: standing-contract-reconcile-guard

## Summary

Tightened the persistent MB reconcile contract so standing contracts are not false-skipped, while keeping deliberate incompleteness and anti-noise bias. Delivered as planned with one QA clarity fix on per-file probe scoping.

## Requirements vs Outcome

All brief requirements met: asymmetric skip, standing-contract probe, skip receipts, systemPatterns contract carve-out, techContext process/oracle contrast, productContext untouched, skip-biased doubt (no write-when-unsure). Design color (incomplete by design; never pollute) encoded in reconcile guardrails and systemPatterns When to Update.

## Plan Accuracy

File list and sequence were correct. Numbering the probe as step 4 (not 3b) was a minor build-time clarity choice. Generic “typed-error helper” examples replaced a repo-specific ScriptError path so the shipped ruleset stays portable. The real surprise was QA: the per-file loop + task-global probe needed an explicit “belongs in this file” gate to avoid forcing productContext updates.

## Build & QA Observations

Build was a clean prose edit; verification checklist and `make test` passed first try. QA caught the probe-scoping ambiguity before reflect — cheap fix, high leverage against the pollution failure mode we were trying to prevent.

## Insights

### Technical
- A task-global probe inside a per-file loop needs an explicit membership gate (“belongs in *this* file per its guidance”), or every standing contract looks like it belongs everywhere.

### Process
- When fixing an instruction that overshot toward skip, keep the stronger invariant (never pollute) in the same paragraph as the new inclusion path — otherwise agents read the carve-out as a completeness invitation.

### Million-Dollar Question

If standing-contract capture had been a foundational assumption of the 2026-07-09 update contract, reconcile would have shipped with the probe and asymmetric risk from day one, and “under-updating is safe” would never have been stated as a blanket. What we built is that retroactive correction; no broader redesign needed.
