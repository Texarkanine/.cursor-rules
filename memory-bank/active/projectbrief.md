# Project Brief

## User Story

As an operator running `choose-verification-model`, I want every slug `agent --list-models` reports to resolve to a hand-tiered catalog model, so that whatever subset a worker passes as `--reviewer-models`, and whichever model is the author, `pick.py` makes a correct selection instead of exiting 2 or inventing an intelligence.

## Use-Case(s)

### Author effort differs from the stored row

The live author slug differs from the catalog key by an effort word, with or without a trailing `-fast`. That author is the catalog model. The effort does not move their tier or their score.

### Reviewer list is someone else's subset

Other operators enable a different set of models. The catalog is a superset: every model the Cursor CLI lists that refresh can recognize. A catalog row is a candidate only when a slug for it is in `--reviewer-models`.

### A new model ships

The operator onboards it in the release hour: run refresh from this repository, which fills in the mapping and catalog rows for it, then set its tier by hand. Until then, an author on that model is printed back with exit 0.

## Requirements

As described in [issue #129](https://github.com/Texarkanine/.cursor-rules/issues/129), extended by operator direction on 2026-09-24:

1. An effort word must not make `pick.py` give up, and it must not create a score. BenchLM has one number per model. The catalog key is the model stem. `effort_encoded` is false.
2. The effort vocabulary is the one `agent --list-models` uses: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, `max`. The effort may come before `-thinking` (`claude-4.6-opus-high-thinking`). `thinking` stays in the stem. A trailing `-fast` is stripped first.
3. The printed reviewer keeps the effort written on the `--reviewer-models` spelling. Two efforts of one model are one candidate; the first spelling is the one printed.
4. `-fast` is appended only when the author slug ended in `-fast` and the chosen model has a fast variant.
5. The catalog covers every model stem in the operator's `agent --list-models` listing that refresh can recognize: a BenchLM score or an interim score, and a price.
6. Tiers are the operator's trust calibration, set by hand. No tier is derived from a score.
7. Refresh fills in rows. For each stem in the `agent --list-models` listing that has no mapping row, refresh matches it to a Cursor pricing row and a scored BenchLM model, appends a mapping row, and writes its catalog row with a null tier. A stem it cannot match is not added and gets a warning that names the missing source. Existing mapping rows are never rewritten. When the `agent` CLI is not available, refresh warns once and still writes the catalog.
8. When the author's model is not in the catalog, the script prints that spelling and exits 0. The skill does not grow a branch that tells the agent to pick a reviewer from a non-zero exit.

## Constraints

1. Different efforts of one model are the same row. There is no per-effort score to store.
2. Do not store or rank on the fast price.
3. Do not derive, infer, or retier from scores. The operator sets every tier.
4. `SKILL.md` stays a thin caller: run the script and use the slug it prints.
5. `pick.py` does not call the `agent` CLI. Only refresh, which the operator runs, reads the listing.
6. Refresh is run from this repository and writes the skill's own `assets/`. A catalog stored outside the skill, refreshed by each user on their own schedule, is a possible later change and is out of scope.

## Acceptance Criteria

1. `python3 scripts/pick.py --model cursor-grok-4.6-xhigh-fast --reviewer-models claude-opus-5-5-high,gpt-5.6-terra-medium,grok-4.7-xhigh --seed 0` prints `claude-opus-5-5-high-fast` and exits 0.
2. The same reviewer list with `--model cursor-grok-4.6-xhigh` prints `claude-opus-5-5-high`.
3. `model_key` maps `claude-opus-5-5-max-fast` to `claude-opus-5-5`, `claude-4.6-opus-high-thinking` to `claude-4.6-opus-thinking`, `gpt-5.5-extra-high` to `gpt-5.5`, `gpt-5.6-sol-none` to `gpt-5.6-sol`, and `muse-spark-1.3-minimal` to `muse-spark-1.3`.
4. Refresh against an injected listing appends a mapping row and a null-tier catalog row for each matchable unmapped stem, warns `must set tier` for it, and warns `unrecognized model {stem}` with the missing source for each stem it cannot match. Existing mapping rows are byte-for-byte unchanged.
5. After refresh and the operator's tiers, every stem in the operator's listing is a catalog key with a tier on the ladder, or is recorded in `tasks.md` as unrecognized.
6. `--model missing-author --reviewer-models other` prints `missing-author` and exits 0. A known row with a null tier or null score still exits 2. An enabled spelling whose model is absent still exits 2 and names that slug.
