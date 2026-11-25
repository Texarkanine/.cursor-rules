---
task_id: google-gas-tiers
date: 2026-11-25
complexity_level: 2
---

# Reflection: Place the Gemini 4 gas models and refresh BenchLM scores

## Summary

The shipped catalog ranks on BenchLM's published overall, and the gas models are placed Carbon in S, Neon in A, Hydrogen in B, with Argon left in A. That is what the brief asked for, and QA passed.

## Requirements vs Outcome

All four requirements are on the committed branch. The score is the top-level `displayScore`, and the category mean remains only when that overall is missing. No tier moved because of a score. Three flags stayed review notes: Neon +19.6 above the A median, Hydrogen +12.5 above the B median, and Sonnet 5 thinking −11.0 below A. The working-tree `tiers.toml` edits are not part of the outcome. QA also noted that `references/refresh.md` line 19 still says "BenchLM category scores" while line 45 states the real rule. That sentence was left as an advisory.

## Plan Accuracy

The first plan stopped itself: it refreshed from category means, and Neon and Hydrogen have none, so they could not be listed. The published-overall rule was already in the brief and in `build_catalog` before `tasks.md` said so. The replan described that branch. The surprise was the working tree, which grew from the two thinking stems to also move `cursor-grok-4.6` and add `cursor-grok-4.7`.

## Build & QA Observations

Build confirmed 131 tests and did not refresh, because a refresh would have written the unstaged tier edits into the catalog. QA passed with those two advisories and no rework.

## Insights

### Technical

A null `displayCategoryScores` block is not "BenchLM has no score." The published overall is a separate field, and `fill_mapping` has to treat it as a match or the model never gets a row.

### Process

A `FAIL (blocking)` line stays the build gate until a new preflight overwrites the file. The brief and the code moving on does not clear it. The plan text has to change with them, or build stops on the old sentence.

### Million-Dollar Question

The rule we shipped is the one we would have wanted at the start: overall, else the category mean, else an interim score. The hold on Neon and Hydrogen was the cost of the older mean. A drift sidecar was considered and left out. The session report is enough for one placement.
