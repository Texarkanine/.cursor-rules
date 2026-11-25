# Task: Place the Gemini 4 gas models and refresh BenchLM scores

* Task ID: google-gas-tiers
* Complexity: Level 2
* Type: simple enhancement

Refresh the shipped catalog from BenchLM. The catalog score is the published overall, the top-level `displayScore`. The equal-weight mean of the agentic, coding, and reasoning cells remains only when that overall is missing. The nested `scores.displayScore` is unread. Move `gemini-4-carbon` from A to S. List `gemini-4-neon` in A and `gemini-4-hydrogen` in B. Leave `gemini-4-argon` in A. Report score outliers for review, and do not move a model because of a score.

This replaces the category-mean plan that preflight blocked. `build_catalog`, `fill_mapping`, the gas rows, and the tests below are already on `google-gasses`. Build confirms them. It does not add a second scorer.


## Test Plan (TDD)

### Behaviors to Verify

- Published overall wins: a BenchLM item whose categories average 20 and whose top-level `displayScore` is 91.8 stores score 91.8 and `score_source` `benchlm`.
- Null overall keeps the mean: the same item with `displayScore` null stores 20.
- Legacy field: a nested `scores.displayScore` of 77, with no top-level overall, does not become the score. The category mean stands.
- Overall with null categories: an item whose agentic, coding, and reasoning cells are null and whose `displayScore` is 78.8 stores 78.8, replacing an interim score.
- Onboarding: `fill_mapping` adds `gemini-4-neon` when the BenchLM item has `displayScore` 91.8 and null category cells.
- Opus with Carbon: `select` author `claude-opus-5-5-medium`, enabled `[claude-opus-5-5-medium, gemini-4-carbon-low]` → `gemini-4-carbon-low`. Carbon is S. While Carbon is A, Opus stays Opus, because nothing sits above S.
- Sol with Neon: author `gpt-5.6-sol-medium`, enabled `[gpt-5.6-sol-medium, gemini-4-neon-high]` → `gemini-4-neon-high`. Neon is A.
- Opus with Neon: author `claude-opus-5-5-medium`, enabled `[claude-opus-5-5-medium, gemini-4-neon-high]` → `claude-opus-5-5-medium`. Neon is not S. Together with the Sol case, Neon is A.
- Terra with Hydrogen: author `gpt-5.6-terra-medium`, enabled `[gpt-5.6-terra-medium, gemini-4-hydrogen-high]` → `gemini-4-hydrogen-high`.
- Sol with Hydrogen: author `gpt-5.6-sol-medium`, enabled `[gpt-5.6-sol-medium, gemini-4-hydrogen-high]` → `gpt-5.6-sol-medium`. Hydrogen is not A or S. Together with the Terra case, Hydrogen is B.
- Flash with Neon: author `gemini-3.8-flash-high`, enabled `[gemini-3.8-flash-high, gemini-4-neon-high]` only → `gemini-3.8-flash-high`. Same family. The enabled list must not include Carbon, or the S fallback can print Carbon.
- Flash with Hydrogen: author `gemini-3.8-flash-high`, enabled `[gemini-3.8-flash-high, gemini-4-hydrogen-high]` only → `gemini-3.8-flash-high`.
- Placeable rows: catalog tiers are Carbon S, Neon A, Hydrogen B, Argon A. Each of the four has a non-null score and `score_source` `benchlm`. The numeric score is not locked.
- Fast Sol with Neon: author `gpt-5.6-sol-medium-fast`, enabled `[gpt-5.6-sol-medium, gemini-4-neon-high]` → `gemini-4-neon-high`. Neon has no `-fast` spelling, so no suffix is appended.
- Regression: Argon's existing Sol / Opus / Flash / fast-Sol tests stay as they are. Fable 5.2 stays `never`.

### Test Infrastructure

- Framework: stdlib `unittest`, invoked by `make test`
- Test location: `tests/choose-verification-model/test_refresh.py` and `tests/choose-verification-model/test_shipped.py`
- Conventions: refresh tests call `build_catalog` or `fill_mapping` with a fixture. Shipped tests call `select` on the shipped catalog and mapping, two-candidate enabled lists, and the docstring states what the printed slug proves about the tier. Numeric catalog scores are not locked. `ShippedTests`, method names `test_<author>_...`.
- New test files: none

## Implementation Plan

### 1. Published overall and gas tiers — executable

- Files: `tests/choose-verification-model/test_refresh.py`, `tests/choose-verification-model/test_shipped.py`, `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/assets/tiers.toml`, `rules/choose-verification-model/assets/catalog.json`, `rules/choose-verification-model/assets/mapping.json`
- `rules/choose-verification-model/references/refresh.md` already states this score rule. No edit.

1. Stub tests: the methods already exist. Do not add duplicates. Refresh: `test_published_overall_replaces_the_category_mean`, `test_null_overall_keeps_the_category_mean`, `test_legacy_nested_display_score_is_not_the_overall`, `test_published_overall_beats_interim_when_categories_are_null`, `test_published_overall_without_categories_is_a_match`. Shipped: `test_opus_author_prints_gemini_4_carbon`, `test_sol_author_prints_gemini_4_neon`, `test_opus_author_does_not_select_gemini_4_neon`, `test_terra_author_prints_gemini_4_hydrogen`, `test_sol_author_does_not_select_gemini_4_hydrogen`, `test_gemini_3_8_flash_does_not_select_gemini_4_neon`, `test_gemini_3_8_flash_does_not_select_gemini_4_hydrogen`, `test_gas_rows_are_placeable`, `test_fast_sol_author_prints_gemini_4_neon_without_fast`.
2. Stub interface: no new functions. The score rule is `build_catalog` reading `_published_overall` before `_category_values`. Onboarding uses `_is_scored`. Placement is `select`.
3. Write tests and run red: the assertions are the behaviors above. They go red if the catalog score is the category mean while a top-level `displayScore` is present, if a published overall with null categories is ignored, if Carbon is still A, or if Neon or Hydrogen is absent. On this branch they are expected green. Run the named tests. A red result is a regression against this plan.
4. Write code and run green: if step 3 was green, leave `modelpool.py`, `tiers.toml`, `catalog.json`, and `mapping.json` as they are. If step 3 was red, the production rule is: score is the top-level `displayScore` to two decimal places; else the mean of the present agentic, coding, and reasoning cells; else an interim score. `fill_mapping` treats a published overall as a scored item. In `tiers.toml`, `gemini-4-carbon` is under S, `gemini-4-neon` under A, `gemini-4-hydrogen` under B, and `gemini-4-argon` stays under A. The tiers comment states the published-overall rule. Refresh, when a row is missing, is `python3 scripts/refresh.py` from `rules/choose-verification-model`. Do not invent an interim score. Do not hand-edit catalog scores. Re-run the named tests, then `make test`.

### 2. Tier score review — prose/policy

- Files: none
- No tests: prose/policy artifact

1. After the green run, group ladder tiers (not `never`) by catalog score. Flag a model whose score is 8 or more points from its tier's median.
2. For a flagged row whose score is the category-mean fallback, name which of agentic, coding, and reasoning were present. A published overall needs no category unpack.
3. Report the flags in the session. Do not edit `tiers.toml` from a flag. Argon staying in A is already decided. The known flags on the 2026-11-25 catalog are Neon 19.6 above the A median, Hydrogen 12.5 above the B median, and Sonnet 5 thinking 11.0 below the A median.

### 3. Draft PR 141 — prose/policy

- Files: the GitHub pull request body
- No tests: prose/policy artifact

1. The body already states the four placements, the 2026-11-25 overalls, and that the three flags are review notes. Confirm that, and keep it if a later commit changes the story.
2. Push `google-gasses`. Leave the PR draft.

## Technology Validation

No new technology - validation not required

## Dependencies

- BenchLM `https://benchlm.ai/data/models.json` (User-Agent `choose-verification-model`)
- Cursor pricing page `https://cursor.com/docs/models-and-pricing.md`
- `agent --list-models` on PATH
- `rules/choose-verification-model/scripts/modelpool.py` (`build_catalog`, `_published_overall`, `_is_scored`) and `modelpool.select`
- `rules/choose-verification-model/scripts/refresh.py`

## Challenges & Mitigations

- Neon or Hydrogen has a null published overall and no agentic, coding, or reasoning cell: refresh will not list the row. Stop and report. Do not write an interim score. Null category cells alone are not that stop. A non-null top-level `displayScore` is enough, which is what `test_published_overall_without_categories_is_a_match` locks.
- `agent` is missing, or refresh cannot word-match the BenchLM slug: fill-in is skipped or the row is omitted. Hand-write only the missing mapping row when BenchLM has a published overall or a category score, then refresh again. Leave every existing mapping row unchanged. Fable and DeepSeek V4.1 Flash stay hand-written.
- Carbon in S lets an A Gemini author draw Carbon when the same-tier window is empty and no other family is in S. That is `modelpool.select`'s next-tier fallback. Do not change it. The Flash/Neon test omits Carbon from its enabled list so it does not lock that fallback.
- Refresh rewrites every score, price, and `has_fast`. Two-candidate tier tests do not lock scores. If an older shipped test goes red, read it. Update it only when the fact it locks (printed reviewer, price, fast) actually changed.
- The working tree may move `claude-opus-5-thinking` and `claude-sonnet-5-thinking` from A to `never`. That edit is outside this task. Do not stage it.
- Refresh from an install writes `$XDG_DATA_HOME`, not this tree. Run it from `rules/choose-verification-model`.

## Pre-Mortem

- The plan is read as the old category-mean plan, and a null category cell stops the listing again: step 1 names `_published_overall` and the onboarding test. A null category cell is not a stop.
- Carbon's move is reversed because 88.2 sits far from the other S scores: the placement is the operator's trust call. The report may flag the gap. It must not edit the tier.
- A flagged non-gas model gets a tier edit in the same change: step 2 forbids it. The unstaged thinking-stem edit is the same hazard and stays unstaged.
- `catalog.json` is hand-edited and drifts from `tiers.toml`: refresh is the only writer of the catalog and the mapping, except a mapping row refresh cannot match.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
