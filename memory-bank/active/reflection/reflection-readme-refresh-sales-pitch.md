---
task_id: readme-refresh-sales-pitch
date: 2026-07-25
complexity_level: 2
---

# Reflection: README Refresh — Sell the High-Value Contents

## Summary

Rewrote the root `README.md` as a value-forward pitch with four ruleset "doors" (niko, authoring, script-it, shell) and created the missing `rulesets/script-it/README.md` in sibling style. Shipped to plan; QA passed clean with no fixes.

## Requirements vs Outcome

Every brief requirement delivered: pitch-first root README (not a catalog), four linked value props, install guidance retained, Structure section refreshed to name both rules and skills tiers, script-it README with Purpose/Scope entries. Nothing dropped, nothing added beyond the preflight's explicit RED step. This also closed the follow-up flagged in the `20260725-description-rules-and-commands-to-skills` archive (stale rules-only wording at the root).

## Plan Accuracy

The plan's sequence, file list, and challenges were correct. The only amendment came from preflight: making the RED demonstration an explicit first step rather than an implied convention. The anticipated challenge that mattered was exactly the one identified — root README sits outside CI's `rulesets/` link-check scope — and the scoped one-off check covered it.

## Build & QA Observations

Build was linear with no iteration: RED confirmed, README created, `make test` GREEN, root rewritten, all links verified. QA found nothing to fix. The pre-commitment to "every value prop must trace to a line in the linked source" turned QA's subjective-sounding accuracy review into a mechanical lookup.

## Insights

### Technical

- Root `README.md` is permanently outside `check-ruleset-readme-links.sh`'s scope; until the checker is extended (preflight advisory), any future root-README edit needs a manual link check. This is a standing gap, not a one-time issue.

### Process

- For docs/pitch tasks, grounding each claim in a quotable line from the linked source at *plan* time makes both writing and QA cheap — the accuracy check becomes lookup, not judgment.

### Million-Dollar Question

If "the root README is a pitch whose doors are ruleset READMEs" had been foundational, the link checker would have covered all tracked READMEs from the start (no `rulesets/`-only scoping), and CI would already guard the root. That is exactly the preflight advisory — a small follow-up, not a redesign.
