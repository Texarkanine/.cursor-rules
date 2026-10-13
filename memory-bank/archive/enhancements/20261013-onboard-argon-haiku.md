---
task_id: onboard-argon-haiku
complexity_level: 2
date: 2026-10-13
status: completed
---

# TASK ARCHIVE: Onboard Gemini 4 Argon and Claude Haiku 5.5

## SUMMARY

Added Gemini 4 Argon at tier A and both Claude Haiku 5.5 stems at tier C to the choose-verification-model catalog. Shipped `select` tests pin the tiers. `make test`: 110 tests OK. QA passed with no rework.

## REQUIREMENTS

- Gemini 4 Argon at tier A, through the catalog refresh.
- Claude Haiku 5.5 at tier C. Cursor lists a thinking stem as its own key, so that stem is tier C too.
- Existing mapping rows unchanged.

## IMPLEMENTATION

Tiers were set in `tiers.toml`, then `scripts/refresh.py` wrote the catalog. Mapping gained `gemini-4-argon`, `claude-haiku-5-5`, and `claude-haiku-5-5-thinking`. Argon stores score 78.43, output price $10, and `has_fast` false. Both Haiku stems store score 82.7, output price $0.50, and `has_fast` false, and both use BenchLM slug `claude-haiku-5-5`. Other catalog scores moved with current BenchLM numbers. Fable 5, GPT-5.1, and GPT-5 Mini were not added.

Files: `rules/choose-verification-model/assets/tiers.toml`, `rules/choose-verification-model/assets/mapping.json`, `rules/choose-verification-model/assets/catalog.json`, `tests/choose-verification-model/test_shipped.py`.

## TESTING

New shipped tests went red on unknown slugs, then green. A Sol author prints Argon, and Opus stays Opus, so Argon is tier A and not tier S. Gemini 3.8 Flash does not select Argon. A fast Sol author prints Argon without `-fast`. Composer prints each Haiku stem, and Terra stays Terra, so both stems are tier C and not tier B or A. A fast Composer author prints them without `-fast`. `make test`: 110 tests OK. QA passed with no rework.

## LESSONS LEARNED

Cursor lists Claude Haiku 5.5 as `claude-haiku-5-5` and `claude-haiku-5-5-thinking`. BenchLM scores only the first. Refresh maps the thinking stem to that slug and to the pricing name Claude Haiku 5.5. The thinking stem needs its own tier, or the shipped ladder check fails.

A live refresh rewrites stored scores for models already in the catalog. The mapping rows are what stay put.

## PROCESS IMPROVEMENTS

Simulate `fill_mapping` against the live listing before editing `tiers.toml`. The listing names models the task did not ask for, and some of them match.

## TECHNICAL IMPROVEMENTS

A table of `(slug, tier, has_fast)` plus one pin helper would replace the four `select` tests per stem. Preflight recorded that and it was not built here. This task was three rows.

## NEXT STEPS

The installed skill copy changes after this lands on the remote `ai-rizz` reads, in a later `chore(dev): ai-rizz sync`.
