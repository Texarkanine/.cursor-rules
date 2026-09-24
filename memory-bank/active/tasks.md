# Task: effort-variant-slug

* Task ID: effort-variant-slug
* Complexity: Level 2
* Type: bug fix

Place an author who is not a catalog row by their real BenchLM score, then run the existing reviewer window. The catalog stays the hand-tiered enabled set. Effort stays one row per model. No invented effort score.


## Test Plan (TDD)

### Behaviors to Verify

- [Wide mean]: a BenchLM item with agentic, coding, and reasoning → `benchlm_scores` stores their mean under that item's slug. An item with no category scores is absent. A mapped catalog row's `score` equals that mean for its `benchlm_slug`.
- [Wide table stays out of the catalog]: an item that mapping does not name → it is in `benchlm_scores` and not in `catalog["models"]`. Existing mapped tiers are copied. `effort_encoded` stays false.
- [Catalog author is unchanged]: author `grok-4.7-high` with that stem in the catalog → the printed reviewer is the one the existing window already prints. The wide table is not consulted for their tier.
- [Outside author is placed]: catalog has tier B score 10 and tier A score 40. Wide score for `outsider` is 20. Author `outsider`, enabled the A-tier model → `select` prints that model. The same author with wide score 5 (below B) stays in B's neighbor tier and does not jump to A.
- [Boundary keeps the higher tier]: wide score sits on the gap between a B row and an A row → the author's tier for the window is A.
- [No BenchLM score echoes]: author `missing-author` with no wide score → `select` returns `missing-author`. `--model missing-author` exits 0 and prints it.
- [Unknown reviewer still exits 2]: enabled `missing-reviewer` → exit 2, stderr names it. A wide score for that slug does not make it a reviewer.
- [Effort spelling of an outside model]: author `outsider-high-fast` uses the wide score of `outsider`. A fast author appends `-fast` only when the chosen catalog row has `has_fast`. The printed effort is the enabled spelling's effort.
- [Unknown family does not empty the window]: an outside author with a score and no mapping family can still print a different-family catalog reviewer.
- [Caller data unchanged]: `select` does not insert the outside author into the caller's catalog or scores.
- [Regression]: null tier or null score on a catalog author still exits 2. `thinking` stays in the stem. `composer-2.5-high` ranks as `composer-2.5`. Issue command with seed 0 still prints `claude-opus-5-5-high-fast`.

### Test Infrastructure

- Framework: stdlib `unittest`
- Test location: `tests/choose-verification-model/`
- Conventions: `_entry`, `_catalog`, `_mapping`, `_run` in `test_pick.py`. Refresh fixtures build a BenchLM document and pricing markdown in `test_refresh.py`. Shipped invariants in `test_shipped.py`.
- New test files: none

## Implementation Plan

### 1. benchlm_scores — executable

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/scripts/refresh.py`, `tests/choose-verification-model/test_refresh.py`

1. Stub tests: `test_wide_mean_is_stored_under_the_benchlm_slug`, `test_unmapped_model_stays_out_of_the_catalog`, empty bodies, in `test_refresh.py`.
2. Stub interface: `benchlm_scores(benchlm) -> dict` in `modelpool.py`. Docstring: equal-weight mean of present agentic, coding, and reasoning scores, keyed by BenchLM slug. Missing categories are skipped. No category scores → omit the slug. `build_catalog` keeps its signature and reads this dict for a mapped `benchlm_slug`. `refresh.main` writes the dict to `assets/scores.json`.
3. Write tests and run red: assert the mean, the omission, catalog equality with the wide mean, and that an unmapped slug is absent from `catalog["models"]`.
4. Write code and run green: implement `benchlm_scores`, call it from `build_catalog`, write `assets/scores.json` from `refresh.main`.

### 2. place the author, then the existing window — executable

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/scripts/pick.py`, `tests/choose-verification-model/test_pick.py`, `tests/choose-verification-model/test_shipped.py`

1. Stub tests: the outside-author, boundary, echo, unknown-reviewer, effort-spelling, unknown-family, and caller-unchanged cases in `test_pick.py`, empty bodies.
2. Stub interface: `select(catalog, mapping, author, enabled, rng, scores=None)`. Docstring: a catalog author uses that row. An author absent from the catalog uses `scores[model_key(author)]` when present. Tier comes from the catalog score-neighbors; a boundary keeps the higher tier. No score → return the author spelling. An enabled model absent from the catalog raises `SelectionError` even if `scores` has it. A missing mapping family does not exclude candidates. The window, the one-tier lookup, the effort spelling, and `-fast` stay as they are.
3. Write tests and run red: the assertions in Behaviors to Verify for `select` and `main`.
4. Write code and run green: place the author in memory for the call, then the existing window. `pick.main` loads `assets/scores.json` when `scores` is omitted. Shipped issue command stays `claude-opus-5-5-high-fast`.

### 3. refresh.md — prose/policy

- Files: `rules/choose-verification-model/references/refresh.md`
- No tests: prose/policy artifact

1. State that `assets/scores.json` is the wide BenchLM mean, one number per model, and that `catalog.json` is only the tiered enabled subset.
2. State that an author missing from the catalog is placed from `scores.json` among the catalog neighbors, and that no wide score still prints the author and exits 0.
3. State that the operator keeps one effort of a model in the candidate list. The bottom and the top effort of one model are not both enabled.

## Technology Validation

No new technology - validation not required. Refresh already fetches BenchLM.

## Dependencies

- BenchLM `models.json`, already fetched by `refresh.py`
- Existing `select` window, one-tier lookup, `model_key`, and `_with_speed`
- `assets/catalog.json` tiers and `assets/mapping.json` families for the enabled subset

## Challenges & Mitigations

- A Cursor slug that is not a BenchLM slug has no wide score: `model_key` is the lookup. `cursor-grok-4.6` is in the catalog, so it does not need the wide table. An unmapped author whose stem is not a BenchLM slug is printed, exit 0.
- An outside author has no family: a missing family does not drop candidates for being the same family.
- A wide score must not become a reviewer: enabled slugs still have to be catalog keys. Exit 2 names the slug.
- `build_catalog`'s return value stays `(catalog, warnings)` so the existing refresh tests keep their call shape. The wide dict is a separate function.

## Pre-Mortem

- The outside author's tier is invented the way effort scores were: the score is the BenchLM mean only. The tier is the catalog neighbor's tier. No new number is written into `catalog.json`.
- The window returns the author because the placed tier has no other family, and the run looks dead in the water: that is the existing empty-pool rule. The plan does not add a second search.
- `scores.json` and the catalog row disagree for one BenchLM slug: `build_catalog` reads `benchlm_scores` for the mapped row, and the wide-mean test locks that equality.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
