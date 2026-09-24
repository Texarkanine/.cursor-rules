---
task_id: effort-variant-slug
complexity_level: 2
date: 2026-09-24
status: completed
---

# TASK ARCHIVE: Resolve every Cursor model slug, with hand-set tiers

## SUMMARY

Issue [#129](https://github.com/Texarkanine/.cursor-rules/issues/129) asked that an effort spelling not make `pick.py` exit 2. What shipped is a stem-keyed superset catalog covering every model `agent --list-models` reports, filled in by refresh, with tiers in a hand-edited `assets/tiers.toml` (including `never`). Pull request: https://github.com/Texarkanine/.cursor-rules/pull/130

## REQUIREMENTS

- Effort is a parameter of a model, not a model. Catalog keys are stems; no per-effort score.
- CLI effort words: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, `max`, including effort before `-thinking`. Trailing `-fast` is stripped first.
- The catalog is a superset of listed, recognizable models. `--reviewer-models` is the enabled subset.
- Refresh fills in mapping and catalog rows. Tiers are hand-set trust, never derived from score.
- `never` keeps a model out of review without deleting it. Missing author (or `never` author) prints back, exit 0. Unknown enabled slug still exits 2.
- `SKILL.md` stays a thin caller. Refresh runs from this repository and writes the skill's `assets/`.

## IMPLEMENTATION

Three plans. First: interpolate a per-effort score in memory (shipped, then removed as invented precision). Second: place an outside author by BenchLM score among catalog neighbors (abandoned mid-build). Creative decision E: onboard, don't place — tiers encode trust, and outside authors are brand-new models onboarded the hour they ship.

Final: `model_key` stems slugs; `fill_mapping` matches listing names to pricing rows and scored BenchLM slugs by word sets; `has_fast` follows listed `-fast` spellings; `tiers.toml` is the only hand-edited tier file (read with `tomllib`, never written). Pick still reads JSON.

Files: `rules/choose-verification-model/scripts/modelpool.py`, `refresh.py`, `assets/{tiers.toml,mapping.json,catalog.json}`, `references/refresh.md`, `tests/choose-verification-model/test_{pick,refresh,shipped}.py`.

Unrecognized on the 2026-09-24 listing (no rows): `claude-fable-5`, `claude-fable-5-thinking`, `gpt-5-mini` (no BenchLM score); `gpt-5.1` (no pricing row). Operator placed 15 models on the ladder and 29 under `never`.

## TESTING

Each new behavior was red on the stub, then green. Live refresh added 32 rows and reproduced all 12 prior mapping matches. Acceptance: issue command prints `claude-opus-5-5-high-fast`; without author `-fast`, `claude-opus-5-5-high`; `missing-author` echoes; max/minimal reviewers resolve. Preflight and QA both PASS WITH ADVISORY. `make test`: 79 tests OK. PR review: a scalar `S = "…"` in `tiers.toml` now warns naming the key and is skipped.

## LESSONS LEARNED

Cursor, the pricing page, and BenchLM order a model's words differently (`Claude Opus 4.6` / `Claude 4.6 Opus` / `claude-opus-4-6`). Word-set matching reproduced every hand-written mapping row; string transforms did not.

Keep hand-set judgment out of generated files. The operator's friction was editing tiers among generated fields, not JSON syntax.

An interpolated effort score was order-identical to "just beside its sibling." That check was stronger than a design debate.

## PROCESS IMPROVEMENTS

Preflight and QA check plan shape and fidelity to the brief, not whether the brief's premise matches the operator. Two plans passed Preflight and were abandoned. On a picker or policy task, ask what the judgment fields mean (here, tiers) before planning.

## TECHNICAL IMPROVEMENTS

With the stem as the model and tiers as hand-set trust from the start, pick would only rank, and refresh would own the catalog. `mapping.json` is still the place for hand overrides (interim scores, unmatched models). A cleaner split would put those in a neighbor of `tiers.toml` and let refresh own `mapping.json` entirely.

## NEXT STEPS

- After merge: `chore(dev): ai-rizz sync` so the installed skill copy matches. The live copy still has effort-suffixed catalog keys.
- LlamaPReview on PR #130 (not done): warn when a listing yields zero stems; optional checked-in listing fixture so fill-in is re-derived in CI.
- Older Claude `-thinking` stems map to BenchLM's Non-Reasoning base when the Reasoning entry is unscored. Moot for rows tiered `never`.
