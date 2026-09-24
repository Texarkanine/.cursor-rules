# Active Context

## Current Task: effort-variant-slug
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done
- Abandoned the outside-author placement plan after its build step 1; reverted the uncommitted `benchlm_scores` / `scores.json` edits (`1ca0157`). Decision: `memory-bank/active/creative/creative-outside-author-placement.md`.
- Replanned for a superset catalog: widen `model_key` to the CLI effort vocabulary (`none`, `minimal`, `extra-high`, `max`, effort before `-thinking`), have refresh warn about `agent --list-models` stems with no mapping row, onboard the 36 missing stems, and document tiers-as-trust onboarding.

## Decisions
- Operator (2026-09-24): tiers are trust calibration, never derived from score. Kimi K3 at A above Opus at S is intended.
- Operator (2026-09-24): outside authors are brand-new models, onboarded with a hand tier the hour they ship. The author echo covers the gap.
- Operator (2026-09-24): the catalog is a superset of every available, recognized model `agent --list-models` reports, because each worker passes in its own enabled set.
- The listing command is `agent --list-models`; `--models` does not exist.
- Build stops at an operator gate for tiers on the new rows. The agent does not propose tiers.

## Next Step
- Preflight this plan.

## Files
- `rules/choose-verification-model/scripts/modelpool.py`
- `rules/choose-verification-model/scripts/refresh.py`
- `rules/choose-verification-model/assets/mapping.json`
- `rules/choose-verification-model/assets/catalog.json`
- `rules/choose-verification-model/references/refresh.md`
- `tests/choose-verification-model/test_pick.py`
- `tests/choose-verification-model/test_refresh.py`
