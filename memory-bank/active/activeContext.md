# Active Context

## Current Task: effort-variant-slug
**Phase:** BUILD - COMPLETE

## What Was Done
- Unit 1: `model_key` reads the CLI effort vocabulary (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, `max`) and an effort before `-thinking`.
- Unit 2: `parse_listing` and `fill_mapping`; refresh reads `agent --list-models` and fills in mapping and catalog rows for matchable unmapped stems (word-set match against pricing and scored BenchLM), warning on the rest. Refresh writes `mapping.json` next to the catalog.
- Unit 2b (operator-directed): a listed model's `has_fast` follows its listed `-fast` spellings; unlisted models keep the pricing rule.
- Unit 2c (operator-directed): `must set tier` on every refresh for every null tier.
- Unit 2d (operator-directed): tiers live in hand-edited `assets/tiers.toml` (slug lists under `S`, `A`, `B`, `C`, `never`), read by refresh with `tomllib`, never written. `never` rows are skipped as reviewers; a `never` author is printed back.
- Unit 3: refresh added 32 rows; 4 stems unrecognized (listed in `tasks.md`). The operator tiered every listed model: 15 on the ladder, 29 `never`.
- Unit 4: `references/refresh.md` rewritten for tiers, onboarding, slugs, fast, and overrides.
- `make test`: 78 tests OK. Acceptance commands 1, 2, and 6 re-run on the tiered catalog: `claude-opus-5-5-high-fast`, `claude-opus-5-5-high`, `missing-author`.

## Decisions
- Operator (2026-09-24): tiers are trust calibration, never derived from score.
- Operator (2026-09-24): outside authors are brand-new models, onboarded with a hand tier the hour they ship; the author echo covers the gap.
- Operator (2026-09-24): the catalog is a superset of every available, recognized model `agent --list-models` reports.
- Operator (2026-09-24): refresh fills in catalog rows; it runs from this repository and writes the skill's `assets/`. A catalog outside the skill is out of scope.
- Operator (2026-09-24): models are parameterized by effort, speed, and context window; fast is per model, never per effort.
- Operator (2026-09-24): `-fast` is appended when the author was fast and the chosen model has fast, even if that spelling is not in `--reviewer-models`.
- Operator (2026-09-24): tiers in one hand-edited TOML file with slug lists per tier; machine data stays JSON.

## Deviations
- Units 2b, 2c, and 2d were added during build at the operator's direction; each was built test-first and recorded in `tasks.md`.
- `refresh.main(previous=...)` was replaced by `refresh.main(tiers=...)`; the three refresh-main tests from unit 2 were updated to pass `tiers`.
- Refresh (and the test suite, which imports it) now needs Python 3.11+ for `tomllib`. Pick does not.

## Known Gaps
- For older Claude models, BenchLM has a Non-Reasoning base and a `-thinking` Reasoning entry; refresh maps Cursor `-thinking` stems to the base entry. Moot for rows tiered `never`.

## Next Step
- QA.

## Files
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/scripts/modelpool.py`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/scripts/refresh.py`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/assets/tiers.toml`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/assets/mapping.json`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/assets/catalog.json`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/references/refresh.md`
- `/home/mobaxterm/git/.cursor-rules/tests/choose-verification-model/test_pick.py`
- `/home/mobaxterm/git/.cursor-rules/tests/choose-verification-model/test_refresh.py`
- `/home/mobaxterm/git/.cursor-rules/tests/choose-verification-model/test_shipped.py`
