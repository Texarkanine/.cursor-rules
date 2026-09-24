# Project Brief

## User Story

As an operator running `choose-verification-model`, I want an effort spelling of a known model to rank as that model, so that `pick.py` does not invent an intelligence for an effort BenchLM did not score.

## Use-Case(s)

### Author effort differs from the stored row

The live author slug differs from the catalog key by an effort word (`low`, `medium`, `high`, `xhigh`), with or without a trailing `-fast`. That author is the catalog model. The effort does not move their tier or their score.

### Reviewer list contains an unmatched effort spelling

A slug in `--reviewer-models` names the model and the effort to spawn if that model is chosen. The effort is not a second score. The printed reviewer keeps that spelling's effort.

## Requirements

As described in [issue #129](https://github.com/Texarkanine/.cursor-rules/issues/129):

1. An effort word must not make `pick.py` give up, and it must not create a score. BenchLM has one number per model. `effort_encoded` is false. The catalog key is the model stem.
2. `gemini-3.8-flash-low` is `gemini-3.8-flash`. The same is true for `medium`, `high`, and `xhigh`, and for a trailing `-fast`. `thinking` stays in the stem.
3. The printed reviewer keeps the effort written on the `--reviewer-models` spelling. The author's effort is not copied onto the reviewer. Two efforts of one model are one candidate; the first spelling is the one printed.
4. `-fast` is still appended only when the author slug ended in `-fast` and the chosen model has a fast variant.
5. When the author's model is not in the catalog, the script prints that spelling and exits 0. The choice stays inside the script. The skill does not grow a branch that tells the agent to pick a reviewer from a non-zero exit.

## Constraints

1. The hand-chosen catalog stays the set of reviewers we decided to keep. Writing every effort spelling into `catalog.json` is not the goal.
2. Different efforts of one model are the same row. There is no per-effort score to store.
3. Do not store or rank on the fast price. Trailing `-fast` means the same model, same score, same tier.
4. Do not retier the rows already chosen. Effort is not a reason to.
5. `SKILL.md` stays a thin caller: run the script and use the slug it prints.

## Acceptance Criteria

1. `python3 scripts/pick.py --model cursor-grok-4.6-xhigh-fast --reviewer-models claude-opus-5-5-high,gpt-5.6-terra-medium,grok-4.7-xhigh --seed 0` prints `claude-opus-5-5-high-fast` and exits 0. The `high` is the Opus candidate's effort. The `-fast` is the author's.
2. The same reviewer list with `--model cursor-grok-4.6-xhigh` prints `claude-opus-5-5-high`.
3. `gemini-3.8-flash-low` and `gemini-3.8-flash-xhigh` rank as `gemini-3.8-flash`.
4. `catalog.json` keys have no effort suffix, and every row has `effort_encoded` false.
5. `--model missing-author --reviewer-models other` prints `missing-author` and exits 0. A known row with a null tier or null score still exits 2. An enabled spelling whose model is absent still exits 2 and names that slug.

## Rework

The operator's placement rule, after the effort correction:

1. Refresh ingests a wide BenchLM score table. One mean per BenchLM model. Effort is not in it.
2. The catalog stays the hand-tiered subset enabled as reviewers. It does not gain a row per BenchLM model.
3. An author who is not a catalog row is placed by their BenchLM score among the catalog's score-neighbors. A tier boundary keeps the higher tier. Then the existing window runs.
4. An author with no BenchLM score is still printed, exit 0. An enabled slug whose model is not in the catalog still exits 2.
5. One score per model. The operator does not enable both the bottom and the top effort of the same model. The printed effort stays the first `--reviewer-models` spelling.
