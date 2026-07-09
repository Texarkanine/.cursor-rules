---
task_id: niko-plan-premortem
date: 2026-07-09
complexity_level: 3
---

# Reflection: niko-plan-premortem

## Summary

Shipped Klein pre-mortem lenses on Niko's planning path: plan-end Pre-Mortem after Challenges on L2/L3, plus architecture choice-level pre-mortem after Decide. Hard-no declined; L3 Invariants clarified. Build and QA clean.

## Requirements vs Outcome

Delivered against the brief and #78: named operable pre-mortem at L2/L3; creative complement specified and implemented (architecture-only); hard-no investigated and declined with positive invariants residue; canonical `rulesets/` only. No requirements dropped. Scope grew once (Q4 creative complement) by design after operator ask — not scope creep during build.

## Plan Accuracy

Plan held. Sequence (red → L3 → L2 → architecture → template → green) matched reality. Challenges predicted (PM/Challenges conflation, choice vs plan blur, hard-no sneak-back) were mitigated in wording rather than discovered as build blockers. No step reordering needed.

## Creative Phase Review

- **Q1 placement (B2 after Challenges):** Held. Explicit "After Challenges…" transition + numbered step made order unambiguous; Challenges body left intact.
- **Q2 levels (L2+L3):** Held. L1/L4 correctly untouched.
- **Q3 hard-no (decline + clarify invariants):** Held. No hard-no section appeared; invariants bullet is positively framed and plan-level.
- **Q4 creative complement (architecture choice PM):** Held. Distinct object from plan-end; Risk criterion preserved; confidence gate present. Architecture special-casing vs other creative types is intentional and documented in the template.

## Build & QA Observations

Build was prose/workflow edits — structural B1–B11 red→green was the right TDD substitute. One verifier false-positive (prose mentioning ``## Pre-Mortem`` before the template heading) was a check bug, not a product bug. QA found nothing substantive.

## Cross-Phase Analysis

Operator pushback mid-plan (Challenges are valuable; order must be explicit) correctly overturned the first creative pick (B1 before Challenges) before build — that revision prevented shipping the wrong complementarity. Expanding Q4 into the same build after a second preflight kept creative and plan-end coherent rather than leaving a half-specified follow-up. Preflight advisories (no shared extract) stayed valid through QA.

## Insights

### Technical
- Plan-end Pre-Mortem and Challenges are complementary only if Challenges stay an identify+mitigate register and Pre-Mortem owns visualize-failure; collapsing them either no-ops or overwrites the register.
- Choice pre-mortem (creative) and plan pre-mortem need different objects in the prompt ("this decision" vs "this plan") or agents blur them into one vague risk pass.

### Process
- For prose/workflow Niko changes, encoding red→green structural assertions in the plan (and dogfooding Pre-Mortem on the plan itself) is enough TDD without inventing a test harness.
- When an operator challenges a creative decision after the fact, revise the creative doc and re-preflight before build — cheaper than shipping B1 and undoing it.
