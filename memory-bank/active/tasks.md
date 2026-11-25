# Task: Place the Gemini 4 gas models and refresh BenchLM scores

* Task ID: google-gas-tiers
* Complexity: Level 2
* Type: simple enhancement

Refresh the shipped catalog from current BenchLM category means. Move `gemini-4-carbon` from A to S. List `gemini-4-neon` in A and `gemini-4-hydrogen` in B. Leave `gemini-4-argon` in A. Report score outliers for review, and do not move a model because of a score.


## Test Plan (TDD)

### Behaviors to Verify

- Opus with Carbon: `select` author `claude-opus-5-5-medium`, enabled `[claude-opus-5-5-medium, gemini-4-carbon-low]` → `gemini-4-carbon-low`. Carbon is S. While Carbon is A, Opus stays Opus, because nothing sits above S.
- Sol with Neon: author `gpt-5.6-sol-medium`, enabled `[gpt-5.6-sol-medium, gemini-4-neon-high]` → `gemini-4-neon-high`. Neon is A.
- Opus with Neon: author `claude-opus-5-5-medium`, enabled `[claude-opus-5-5-medium, gemini-4-neon-high]` → `claude-opus-5-5-medium`. Neon is not S. Together with the Sol case, Neon is A.
- Terra with Hydrogen: author `gpt-5.6-terra-medium`, enabled `[gpt-5.6-terra-medium, gemini-4-hydrogen-high]` → `gemini-4-hydrogen-high`.
- Sol with Hydrogen: author `gpt-5.6-sol-medium`, enabled `[gpt-5.6-sol-medium, gemini-4-hydrogen-high]` → `gpt-5.6-sol-medium`. Hydrogen is not A or S. Together with the Terra case, Hydrogen is B.
- Flash with Neon: author `gemini-3.8-flash-high`, enabled `[gemini-3.8-flash-high, gemini-4-neon-high]` only → `gemini-3.8-flash-high`. Same family. The enabled list must not include Carbon, or the S fallback can print Carbon.
- Flash with Hydrogen: author `gemini-3.8-flash-high`, enabled `[gemini-3.8-flash-high, gemini-4-hydrogen-high]` only → `gemini-3.8-flash-high`.
- Placeable rows: catalog tiers are Carbon S, Neon A, Hydrogen B, Argon A. Each of the four has a non-null score and `score_source` `benchlm`. The numeric score is not locked.
- Fast Sol with Neon: author `gpt-5.6-sol-medium-fast`, enabled `[gpt-5.6-sol-medium, gemini-4-neon-high]` → `gemini-4-neon-high`, plus `-fast` only when that row's `has_fast` is true. The expected suffix is taken from `agent --list-models` or the pricing page, then hardcoded. Same assertion for Hydrogen with a Terra author that already ends in `-fast` is unnecessary if the Neon case locks the suffix rule for a new Gemini 4 row; add the Hydrogen twin only when its `has_fast` differs from Neon's.
- Missing row: before refresh, a Neon or Hydrogen author spelling is returned unchanged. That is the red state, not a behavior to keep.
- Regression: Argon's existing Sol / Opus / Flash / fast-Sol tests stay as they are. Fable 5.2 stays `never`.

### Test Infrastructure

- Framework: stdlib `unittest`, invoked by `make test`
- Test location: `tests/choose-verification-model/test_shipped.py`
- Conventions: `select` on the shipped catalog and mapping, two-candidate enabled lists, docstring states what the printed slug proves about the tier. Numeric scores are not locked. `ShippedTests`, method names `test_<author>_...`.
- New test files: none

## Implementation Plan

### 1. Gas tiers in the shipped catalog — executable

- Files: `tests/choose-verification-model/test_shipped.py`, `rules/choose-verification-model/assets/tiers.toml`, `rules/choose-verification-model/assets/catalog.json`, `rules/choose-verification-model/assets/mapping.json`

1. Stub tests: add empty `ShippedTests` methods for the Opus/Carbon, Sol/Neon, Opus/Neon, Terra/Hydrogen, Sol/Hydrogen, Flash/Neon, Flash/Hydrogen, placeable-row, and fast-Sol/Neon cases. Docstrings state the behaviors above.
2. Stub interface: no new functions. `select` in `modelpool.py` and `refresh.py` already implement placement. Do not change them.
3. Write tests and run red: fill the assertions. Run `python3 -m unittest tests.choose-verification-model.test_shipped.ShippedTests.test_opus_author_prints_gemini_4_carbon tests.choose-verification-model.test_shipped.ShippedTests.test_sol_author_prints_gemini_4_neon tests.choose-verification-model.test_shipped.ShippedTests.test_opus_author_does_not_select_gemini_4_neon tests.choose-verification-model.test_shipped.ShippedTests.test_terra_author_prints_gemini_4_hydrogen tests.choose-verification-model.test_shipped.ShippedTests.test_sol_author_does_not_select_gemini_4_hydrogen tests.choose-verification-model.test_shipped.ShippedTests.test_gemini_3_8_flash_does_not_select_gemini_4_neon tests.choose-verification-model.test_shipped.ShippedTests.test_gemini_3_8_flash_does_not_select_gemini_4_hydrogen tests.choose-verification-model.test_shipped.ShippedTests.test_gas_rows_are_placeable tests.choose-verification-model.test_shipped.ShippedTests.test_fast_sol_author_prints_gemini_4_neon_without_fast`. Expect failure: Carbon is still A, and Neon and Hydrogen are absent.
4. Write code and run green: in `tiers.toml`, move `gemini-4-carbon` to S, add `gemini-4-neon` under A and `gemini-4-hydrogen` under B, leave `gemini-4-argon` under A. Replace the comment that says Neon and Hydrogen are A and unlisted. Run `python3 scripts/refresh.py` from `rules/choose-verification-model` so this tree's `assets/` is written. If a new stem is missing or its score is null, stop and report; do not invent an interim score. If stderr names a word-match miss and BenchLM has an agentic, coding, or reasoning score, add only that mapping row, then refresh again. Set the fast-Sol assertion's suffix from the listing or the pricing page before treating a suffix mismatch as a product bug. Re-run the new tests, then `make test`.

### 2. Tier score review — prose/policy

- Files: none
- No tests: prose/policy artifact

1. After the green refresh, group ladder tiers (not `never`) by catalog score. Flag a model whose score is 8 or more points from its tier's median.
2. Read the BenchLM category values behind each mean. Flag a mean built from only one of agentic, coding, and reasoning, and show the three categories beside the mean.
3. Report the flags in the session. Do not edit `tiers.toml` from a flag. Argon staying in A is already decided.

### 3. Draft PR 141 — prose/policy

- Files: the GitHub pull request body
- No tests: prose/policy artifact

1. Replace the Hold section with the four placements and the refresh date. Say the score flags are review notes, not tier changes.
2. Push `google-gasses`. Leave the PR draft.

## Technology Validation

No new technology - validation not required

## Dependencies

- BenchLM `https://benchlm.ai/data/models.json` (User-Agent `choose-verification-model`)
- Cursor pricing page `https://cursor.com/docs/models-and-pricing.md`
- `agent --list-models` on PATH
- `rules/choose-verification-model/scripts/refresh.py` and `modelpool.select`

## Challenges & Mitigations

- Neon or Hydrogen still has no agentic, coding, or reasoning score: a listed null score makes that author exit 2. Stop and report. Do not list the row and do not write an interim score.
- `agent` is missing, or refresh cannot word-match the BenchLM slug: fill-in is skipped or the row is omitted. Hand-write only the missing mapping row when BenchLM has a category score, then refresh again. Leave every existing mapping row unchanged.
- Carbon in S lets an A Gemini author draw Carbon when the same-tier window is empty and no other family is in S. That is `modelpool.select`'s next-tier fallback. Do not change `modelpool.py`. The Flash/Neon test omits Carbon from its enabled list so it does not lock that fallback.
- Refresh rewrites every score, price, and `has_fast`. Two-candidate tier tests do not lock scores. If an older shipped test goes red, read it. Update it only when the fact it locks (printed reviewer, price, fast) actually changed.
- The tiers comment still says Neon and Hydrogen are unlisted A. Replace it in the same edit.
- Refresh from an install writes `$XDG_DATA_HOME`, not this tree. Run it from `rules/choose-verification-model`.

## Pre-Mortem

- The catalog mean is treated as a full intelligence index, and a reasoning-only row is placed or flagged on that basis: the review step shows the three BenchLM categories and names a one-category mean. No catalog schema change.
- Carbon's move is "corrected" back to A because 88.0 sits far from the other S scores: the placement is the operator's trust call. The report may flag the gap. It must not edit the tier.
- A flagged non-gas model gets a tier edit in the same change: step 2 forbids it. Already the brief's out-of-scope line.
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
