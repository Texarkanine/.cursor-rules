# Project Brief

## User Story

As an operator running Niko QA and Preflight, I want a script to choose the verification model so that the choice follows a fixed rank, family, tier, and cost rule without spending an inference turn on it.

## Use-Case(s)

### Pick a reviewer

The author model is known (`grok-4.7-high`). The enabled models are the slugs already listed for this session's Task tool. The script returns one reviewer slug.

### Refresh the catalog

Someone reruns the refresh executable. It pulls SWE-bench scores and Cursor output prices, keeps hand-set tiers, and warns when a new model has no tier.

## Requirements

1. The skill is named `choose-verification-model`.
2. It ships two executables, a catalog JSON, and a mapping JSON. Python 3.11, standard library only.
3. The pick command takes `--model <author-slug>` and `--reviewer-models <comma-separated enabled slugs>`. The enabled list is the Task-tool slug list, not the output of `agent models`. Unknown slugs are an error. `tier: null` and `score: null` are out of the pool.
4. Rank is position by score inside the tier, best at the top. The pool is same tier, different family, from one rank below the author through the best in the tier. Pick one at random. Family comes from the mapping, so `grok-*` and `cursor-grok-*` can share one.
5. If that window is empty, or the tier has no different family, look up exactly one tier and take the cheapest different-family model there. If that tier has no different family either, take the cheapest model there.
6. Scores come from three boards, equal weight, renormalized over the boards that model-plus-effort actually has: SWE-bench (leaderboard name `Test`), SWE-bench Verified, and SWE-bench Multimodal. When several rows match one model and effort, use the latest dated row.
7. A score is not copied onto an effort the bench did not name. `low`, `xhigh`, `max`, and `none` stay out of the pool until a row names them. A model with no effort axis can be scored from an untagged row when the mapping points that row at that model. Fast is a price variant of a scored effort: `high-fast` keeps the `high` score and its own output price. Thinking slugs need their own scored row.
8. Cost is the output price in USD per million tokens, from https://cursor.com/docs/models-and-pricing. The mapping points each slug at a pricing row and at a SWE-bench row.
9. Tiers are an ordered list assigned by hand. Refresh keeps the existing tier. A new slug gets `tier: null` and prints `WARNING: must set tier for …`.
10. Point the in-repo QA and Preflight selection text, including the spawn lines, at this script.

## Constraints

1. No third-party packages. The mapping is JSON.
2. Cursor Router is not the means. The spawn path needs a concrete slug, and the router does not know the author model.
3. Verified repeats a filtered subset of full SWE-bench. A model on both is counted on those tasks twice. That double-count is accepted.
4. Canonical edits go under `rules/` and `rulesets/`. Do not edit generated `.cursor/` or `.claude/` copies.

## Acceptance Criteria

1. Given an author slug and an enabled-slug list, the pick command prints one slug that satisfies the rank, family, tier, and fallback rules, and never prints a null-tier, null-score, or unscored-effort slug.
2. Refresh rewrites scores and output costs from the two upstream sources, preserves tiers, and warns on a new null tier.
3. The QA and Preflight selection text in this repo tells the agent to run the pick command instead of choosing a model by deliberation.
