---
task_id: persistent-file-update-contract
date: 2026-07-09
complexity_level: 2
---

# Reflection: Persistent-File Rule Update Contract

## Summary

Amended the three persistent memory-bank guidance rules to define both what belongs in each file (altitude test, sharpened Avoid lists) and when it may be updated (invalidation-only, surgical, skip confidently). Delivered exactly to plan; QA clean on the first pass.

## Requirements vs Outcome

All five brief requirements delivered. One micro-addition beyond the letter of the plan: joining a pre-existing hard-wrapped paragraph in `systemPatterns.mdc` while editing it (covered by the brief's style-compliance requirement, documented as a deviation at build).

## Plan Accuracy

The plan was accurate — 5 steps, no reordering, no surprises. The design being fully pre-resolved in a standalone creative exploration (operator-refined before `/niko` was invoked) made plan and build nearly mechanical. Preflight's consumer check (`memory-bank-init.md`, `reconcile-persistent.md`) confirmed the additive edits were safe exactly as predicted.

## Build & QA Observations

Build was clean; the only friction was environmental — an unscoped `rg` over the workspace hung indefinitely (killed and re-run with explicit paths). QA found nothing to fix.

## Insights

### Technical

- The failure mode this task addresses ("rules define creation but not stewardship") is worth checking wherever a glob-attached rule describes a long-lived artifact: if the rule has "How to Create" but no "When to Update," out-of-workflow agents will invent their own update policy, and it will be append-biased.
- Verbatim tripwire phrases ("factually wrong or materially incomplete") shared between the rules and `reconcile-persistent.md` make the deliberate duplication grep-verifiable — the same technique as the consent header. This repo now has two instances of the pattern; it is established practice, not an experiment.

### Process

- Standalone `/creative` before `/niko` worked well for a design-heavy-but-small task: the L2 run inherited a settled design and executed without a single open question. The creative doc slotting into `memory-bank/active/creative/` for the subsequent task was seamless (after the prior task's archive cleared the directory around it).
- Unscoped `rg` from the workspace root can hang in this environment (WSL); always scope searches to explicit directories.

### Million-Dollar Question

If update contracts had been a foundational assumption, every memory-bank guidance rule would have been born with the File / How to Create / When to Update / Format skeleton as a fixed template, and `reconcile-persistent.md` would have been a trivial loop over "apply each rule's When to Update section." What we built converges on that shape retroactively — the persistent rules now match the ephemeral rules' skeleton — so the elegant end-state is what now exists, minus a formal statement that the four-section skeleton is the template for future memory-bank rules.
