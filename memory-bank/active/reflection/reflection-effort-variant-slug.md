---
task_id: effort-variant-slug
date: 2026-09-24
complexity_level: 2
---

# Reflection: effort-variant-slug

## Summary

Issue #129 asked that an effort spelling not make `pick.py` exit 2. What shipped is a stem-keyed superset catalog covering every model `agent --list-models` reports, filled in by refresh, with tiers in a hand-edited `tiers.toml` (including `never`). QA passed with advisory; 78 tests.

## Requirements vs Outcome

The final brief's requirements shipped: CLI effort vocabulary, stem keys with no per-effort score, refresh fill-in, author echo, and operator-set tiers. The brief itself moved three times. First build: an interpolated per-effort score (shipped, then removed as invented precision). Second plan: place outside authors by score-neighbor tier (abandoned mid-build; tiers are trust, not score). Final plan: superset catalog plus onboarding. Three units were added during build at the operator's direction: `has_fast` from the listing, a tier reminder on every refresh, and `tiers.toml` with `never`. Advisory B (a scalar value in `tiers.toml` is read character by character) is open.

## Plan Accuracy

The final plan's sequence held, and its live-data validation paid off: the matching rule's 44/48 and 32-row predictions were exact. The surprises were premises, not steps. Each replan came from a fact only the operator had: tiers encode trust, outside authors are brand-new models, the catalog must be a superset, and speed is a model parameter. None were in the code or the issue.

## Build & QA Observations

Test-first worked cleanly for every unit, including the three added mid-build. The tier gate (a shipped test red until tiers are set) did its job: build stopped for the operator without anyone proposing tiers. QA found only documentation and input-validation advisories. Two earlier Preflights passed plans whose premises were later abandoned.

## Insights

### Technical

- Cursor, the pricing page, and BenchLM order a model's words differently (`Claude Opus 4.6`, `Claude 4.6 Opus`, `claude-opus-4-6`). Word-set matching reproduced every hand-written mapping row; string transforms did not.
- Keep hand-set judgment out of generated files. The friction the operator hit was editing tiers among generated fields, not JSON syntax; a read-only `tiers.toml` also sidestepped `tomllib` having no writer.

### Process

- Preflight and QA check a plan's shape and its fidelity to the brief, not whether the brief's premise matches what the operator means. Two plans passed Preflight and were then abandoned. On a picker or policy task, asking the operator what the judgment fields mean (here, tiers) before planning would have saved two cycles.
- When the operator says "this is getting heinous," a quick read-only check (the interpolated score was order-identical to "just beside its sibling") was a stronger argument than a design debate.

### Million-Dollar Question

With the stem as the model and tiers as hand-set trust from the start, the catalog would always have been generated from the CLI listing plus `tiers.toml`, and `pick` would only rank. That is roughly what shipped. The remaining difference is `mapping.json`: now that refresh fills it in, it is mostly machine-written, but hand overrides (interim scores, unmatched models) still live in it. A cleaner split would put overrides in `tiers.toml`'s neighbor and let refresh own `mapping.json` entirely.
