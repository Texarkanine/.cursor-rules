# Active Context

## Current Task: effort-variant-slug
**Phase:** BUILD - IN-PROGRESS (waiting at the unit 3 operator tier gate)

## What Was Done
- Abandoned the outside-author placement plan after its build step 1; reverted the uncommitted `benchlm_scores` / `scores.json` edits (`1ca0157`). Decision: `memory-bank/active/creative/creative-outside-author-placement.md`.
- Replanned for a superset catalog: widen `model_key` to the CLI effort vocabulary (`none`, `minimal`, `extra-high`, `max`, effort before `-thinking`), make refresh fill in mapping and catalog rows for `agent --list-models` stems with no mapping row (null tier), onboard by running it, and document tiers-as-trust onboarding.
- Validated the fill-in matching rule on live data: 44 of 48 stems resolve; all 12 existing rows are reproduced exactly.

## Decisions
- Operator (2026-09-24): tiers are trust calibration, never derived from score. Kimi K3 at A above Opus at S is intended.
- Operator (2026-09-24): outside authors are brand-new models, onboarded with a hand tier the hour they ship. The author echo covers the gap.
- Operator (2026-09-24): the catalog is a superset of every available, recognized model `agent --list-models` reports, because each worker passes in its own enabled set.
- The listing command is `agent --list-models`; `--models` does not exist.
- Build stops at an operator gate for tiers on the new rows. The agent does not propose tiers.
- Operator (2026-09-24): refresh fills in catalog rows, not just warns. Refresh runs from this repository and writes the skill's `assets/`. A catalog outside the skill, refreshed per user, is a later maybe and out of scope.

## Build So Far
- Unit 1 (`1e6472c`): `model_key` reads `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, `max`, and an effort before `-thinking`.
- Unit 2 (`1e6472c`): `parse_listing`, `fill_mapping`, and `refresh.main(agent_models=...)`; refresh writes `mapping.json` next to the catalog. 65 tests green at that commit.
- Unit 3: real refresh added 32 rows with `tier: null`; 4 stems unrecognized (listed in `tasks.md`). Existing mapping and catalog rows unchanged. `make test` is red only on `test_catalog_entries_have_required_keys` until tiers are set.
- Unit 2b (operator-directed): with a listing, a listed stem's `has_fast` is whether the listing has a `-fast` spelling for it; unlisted stems and no-listing refreshes keep the pricing rule. Re-ran refresh: exactly `gpt-5.3-codex`, `gpt-5.2`, `claude-opus-4-7`, `claude-opus-4-7-thinking` flipped to true. 69 tests; only the tier gate is red.
- Known gap, not fixed: `has_fast` is per stem, but `gpt-5.4-low` has no `-fast` spelling while other `gpt-5.4` efforts do, so a fast author choosing `gpt-5.4-low` would print a slug that does not exist.
- Known gap, not fixed (pre-existing): `build_catalog` warns `must set tier` only for a slug new to the previous catalog, so a second refresh before tiering prints no tier reminders.

## Next Step
- Operator sets `tier` on the 32 null-tier rows in `rules/choose-verification-model/assets/catalog.json`. Then: `make test` green, unit 4 prose, finish Build.

## Files
- `rules/choose-verification-model/scripts/modelpool.py`
- `rules/choose-verification-model/scripts/refresh.py`
- `rules/choose-verification-model/assets/mapping.json`
- `rules/choose-verification-model/assets/catalog.json`
- `rules/choose-verification-model/references/refresh.md`
- `tests/choose-verification-model/test_pick.py`
- `tests/choose-verification-model/test_refresh.py`
