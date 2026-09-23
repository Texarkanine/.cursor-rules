# Project Brief

## User Story

As an operator running Niko QA and Preflight, I want a script to choose the verification model so that the choice follows a fixed rank, family, tier, and cost rule without spending an inference turn on it.

## Use-Case(s)

### Pick a reviewer

The author model is known (`grok-4.7-high`). The enabled models are the slugs already listed for this session's Task tool. The script returns one reviewer slug.

### Refresh the catalog

Someone reruns the refresh executable. It pulls BenchLM category scores and Cursor output prices, keeps hand-set tiers and interim scores, and warns when a new model has no tier.

## Requirements

1. The skill is named `choose-verification-model`.
2. It ships two executables under `scripts/`, a catalog JSON and a mapping JSON under `assets/`, and refresh instructions under `references/`. Python 3.11, standard library only.
3. The pick command takes `--model <author-slug>` and `--reviewer-models <comma-separated enabled slugs>`. The enabled list is the Task-tool slug list, not the output of `agent models`. Unknown slugs are an error. `tier: null` and `score: null` are out of the pool.
4. Rank is position by score inside the tier, best at the top. The pool is same tier, different family, from one rank below the author through the best in the tier. Pick one at random. Family comes from the mapping, so `grok-*` and `cursor-grok-*` can share one.
5. If that window is empty, or the tier has no different family, look up exactly one tier and take the cheapest different-family model there. If that tier has no different family either, take the cheapest model there.
6. The score is the equal-weight mean of the BenchLM category scores that exist among agentic, coding, and reasoning, from `https://benchlm.ai/data/models.json`. A missing category is left out of the mean. BenchLM does not score Cursor effort slugs, so every slug mapped to the same BenchLM model shares that mean. A trailing `-fast` is that same model. Ranking uses the base output price. After a slug is chosen, append `-fast` only when the author slug ended in `-fast` and the chosen model has a fast variant.
7. When all three categories are missing, refresh keeps an operator interim score and marks it as a guess. When any of the three is present, refresh replaces that interim score. A model with neither a category score nor an interim score stays `score: null`.
8. Cost is the base output price in USD per million tokens, from https://cursor.com/docs/models-and-pricing. The mapping points each slug at a pricing row and at a BenchLM model slug. `has_fast` is set when that page has a `{Name} (Fast)` row or the model's notes mention a fast mode. The fast price is not stored.
9. Tiers are `C`, `B`, `A`, `S` from lowest to highest, assigned by hand. Refresh keeps the existing tier. A new slug gets `tier: null` and prints `WARNING: must set tier for …`.
10. Point the in-repo QA and Preflight selection text, including the spawn lines, at this script.

## Constraints

1. No third-party packages. The mapping is JSON.
2. Cursor Router is not the means. The spawn path needs a concrete slug, and the router does not know the author model.
3. The slugs this session can spawn each get a BenchLM category mean and a hand-assigned tier, so they are in the pool. Fable, Sol, and Luna stay in the catalog and are passed only when enabled.
4. Canonical edits go under `rules/` and `rulesets/`. Do not edit generated `.cursor/` or `.claude/` copies.

## Acceptance Criteria

1. Given an author slug and an enabled-slug list, the pick command prints one slug that satisfies the rank, family, tier, and fallback rules, and never prints a null-tier or null-score slug. The nine spawnable slugs are selectable once that rule is applied.
2. Refresh rewrites scores and output costs from the two upstream sources, preserves tiers, and warns on a new null tier.
3. The QA and Preflight selection text in this repo tells the agent to run the pick command instead of choosing a model by deliberation.
