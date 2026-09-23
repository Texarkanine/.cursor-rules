# Task: Add cursor-grok-4.6-xhigh to the verification catalog

* Task ID: cursor-grok-4-6
* Complexity: Level 2
* Type: simple enhancement

Add one catalog row, `cursor-grok-4.6-xhigh`, family `grok`, tier A, BenchLM slug `grok-4-6`, pricing name `Grok 4.6`. Refresh sets the score and the $6 base output price, and sets `has_fast` from the `Grok 4.6 (Fast)` row. The fast spelling stays a suffix.


## Test Plan (TDD)

### Behaviors to Verify

- [Fast suffix on this row]: author `gpt-5.6-sol-medium-fast`, enabled `gpt-5.6-sol-medium` and `cursor-grok-4.6-xhigh` → `cursor-grok-4.6-xhigh-fast`.
- [No suffix when the author is not fast]: same enabled set, author `gpt-5.6-sol-medium` → `cursor-grok-4.6-xhigh`.
- [Not tier S]: author `claude-opus-5-5-medium`, enabled `claude-opus-5-5-medium` and `cursor-grok-4.6-xhigh` → `claude-opus-5-5-medium`. Opus is tier S. A second usable tier-S row is always inside Opus's window. Staying on Opus means this row is not tier S.
- [Same family]: author `grok-4.7-high`, enabled `grok-4.7-high` and `cursor-grok-4.6-xhigh` → `grok-4.7-high`. Two grok rows do not review each other.
- [Shipped membership]: `cursor-grok-4.6-xhigh` is in mapping and catalog, score is not null, tier is on the C-B-A-S ladder. Existing `SPAWNABLE` loop. Do not assert the letter A, the numeric score, or the $6 price.

Sol is tier A. With only Sol enabled beside this row, Sol's window includes the row when it is tier A, and Sol's one-tier lookup (S) includes it when it is tier S. The Opus case excludes S. Tier B or C is outside both Sol's window and that lookup, so Sol would print itself. Together, Sol printing this row and Opus printing itself require tier A, without a letter equality.

### Test Infrastructure

- Framework: stdlib `unittest`, `make test` / `python3 -m unittest discover -s tests/choose-verification-model -p 'test_*.py'`
- Test location: `tests/choose-verification-model/`
- Conventions: `test_shipped.py` loads `rules/choose-verification-model/assets/` and does not lock scores or tier letters. `test_pick.py` builds catalogs in memory and stays fixture-only.
- New test files: none

## Implementation Plan

### 1. Shipped acceptance of cursor-grok-4.6-xhigh — executable

- Files: `tests/choose-verification-model/test_shipped.py`, `rules/choose-verification-model/assets/mapping.json`, `rules/choose-verification-model/assets/catalog.json`

1. Stub tests: In `test_shipped.py`, add empty test methods for the fast suffix, the non-fast author, the Opus tier-S exclusion, and the same-family grok case. Leave `SPAWNABLE` unchanged in the stub so that loop is not red yet.
2. Stub interface: No new functions. `select` and `build_catalog` already implement the rule.
3. Write tests and run red: Fill the four methods. Add `cursor-grok-4.6-xhigh` to `SPAWNABLE`. Import `select` the same way `test_pick.py` does. Run `python3 -m unittest discover -s tests/choose-verification-model -p 'test_shipped.py'`. Expect failure: unknown slug, or the new slug missing from mapping.
4. Write code and run green: Add the mapping row (`family` grok, `pricing_name` `Grok 4.6`, `benchlm_slug` `grok-4-6`, `interim_score` null). Run `python3 scripts/refresh.py` from `rules/choose-verification-model/`. Set `tier` to `A` on the new catalog entry only. Re-run the shipped tests, then `make test`.

## Technology Validation

No new technology - validation not required

## Dependencies

- BenchLM `https://benchlm.ai/data/models.json` and `https://cursor.com/docs/models-and-pricing.md`, fetched by `refresh.py` during build.
- Existing `select` / `build_catalog` in `rules/choose-verification-model/scripts/modelpool.py`.

## Challenges & Mitigations

- Refresh warns `must set tier` and writes `tier: null` for a new slug. Set A immediately after that run. A second refresh keeps A once it is in `catalog.json`.
- If BenchLM or the pricing page fails to fetch, do not invent a score or a price. Stop and report the warning.
- `claude-opus-5-5-high` and `grok-4.7-xhigh` stay unknown. Do not add them while making the new tests pass.
- Family `cursor` would let this row review `grok-4.7-high`. The same-family test fails closed on that.

## Pre-Mortem

- The sample command is treated as the definition of done, so the build also renames Opus and Grok 4.7. The brief already excludes that. Tests call `select` with catalog slugs only.
- A hand-edited score drifts off BenchLM. The only hand edit after refresh is `tier`.
- Asserting `tier == "A"` or `output_cost_per_million == 6` in `test_shipped.py` fights the existing "letters and scores are not locked" contract and goes red on the next honest refresh. Sol printing this row, and Opus printing itself, require tier A without a letter equality. No price assertion.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
