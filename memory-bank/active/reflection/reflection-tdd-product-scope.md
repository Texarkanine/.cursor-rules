---
task_id: tdd-product-scope
date: 2026-08-20
complexity_level: 2
---

# Reflection: tdd-product-scope

## Summary

Replaced the in-scope paragraph in `rules/always-tdd.mdc` so TDD names the product's executable behavior and no longer says "If something executes it." Preflight and QA passed. The residual risk is that the em-dash list still uses the tokens both incidents quoted.

## Requirements vs Outcome

The brief asked for a principle, not an exclusion list, and for preflight not to classify lint/CI wiring as product behavior. We shipped the principle in one file and did not echo it into niko-preflight. Whether that is enough for the next GPT 5.6 preflight is unproven; we did not add the issue's guardrail paragraph.

## Plan Accuracy

The plan's file list and one-unit scope were right. The surprise was not a missed file: Preflight and QA both noted that phrase 1 is still almost verbatim after the prefix. That was the one-file bet, not a planning error.

## Build & QA Observations

Build was the planned one-line replacement. `make test` passed. QA PASSed and repeated the phrase-1 advisory; it did not ask for rework.

## Insights

### Technical

- A category list will be relabeled (lint is a CLI; `release-please.yaml` is a workflow). Putting "the product's" in front of the same list may not change the read that produced the FAILs. The change-detector paragraph already steers by failure mode; scope still steers by artifact kind.

### Process

- L2 locks wording in the plan. For a high-challenge sentence, that means Preflight/QA can only advise on a bet already taken. That is correct for the workflow and is why the residual stayed advisory.

### Million-Dollar Question

If TDD scope had always used the same test as change-detectors — would a user of the product observe the break? — lint-script wiring and invoke-only CI would never have looked in-scope, and the em-dash list would not need to exist.
