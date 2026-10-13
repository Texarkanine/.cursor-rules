---
task_id: onboard-argon-haiku
date: 2026-10-13
complexity_level: 2
---

# Reflection: Onboard Gemini 4 Argon and Claude Haiku 5.5

## Summary

Gemini 4 Argon is in the catalog at tier A, and both Claude Haiku 5.5 stems are at tier C. The shipped `select` tests pin those tiers. The build matched the plan.

## Requirements vs Outcome

The operator asked for Argon at A and Claude Haiku 5.5 at C. Both shipped. The thinking stem was not named separately. Refresh adds it as its own key, and a null tier cannot ship, so it is C as well. That was decided in the plan, before build. Existing mapping rows were not rewritten. Other catalog scores moved with BenchLM. Fable 5, GPT-5.1, and GPT-5 Mini were left out.

## Plan Accuracy

The sequence held: tests red on unknown slugs, then `tiers.toml`, then one refresh, then green. The simulated fill matched the live run, including the four warnings. The score churn the preflight advisory predicted showed up and was left in the diff.

## Build & QA Observations

The red run and the green run each happened once. QA passed with no findings. The work was in seeing that one product name is two catalog keys, and that a refresh rewrites every stored score.

## Insights

### Technical

- Cursor lists Claude Haiku 5.5 as `claude-haiku-5-5` and `claude-haiku-5-5-thinking`. BenchLM scores only the first. Refresh maps both stems to that slug and to the pricing name Claude Haiku 5.5. The thinking stem needs its own tier or the shipped ladder check fails.
- A live refresh rewrites stored scores for models already in the catalog. The mapping rows are what stay put.

### Process

- Simulate `fill_mapping` against the live listing before editing `tiers.toml`. The listing names models the task did not ask for, and some of them match.

### Million-Dollar Question

A table of `(slug, tier, has_fast)` plus one pin helper would replace the four `select` tests per stem. Preflight recorded that and did not apply it. This task was three rows, and the hand-written tests match the Grok 4.6 onboarding. The helper is the next onboarding's change, not this one's.
