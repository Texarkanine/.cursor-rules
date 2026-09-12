---
task_id: tdd-product-user-scope
date: 2026-09-12
complexity_level: 2
---

# Reflection: tdd-product-user-scope

## Summary

Shipped the #116 follow-up: `always-tdd` now classifies by whether a user of this product can observe a break, and niko-preflight FAILs on that test rather than the plan’s “executable” label. QA passed verbatim against the locked sentences.

## Requirements vs Outcome

Delivered as specified in the brief and plan. Did not lock the issue-body proposed wording; did not touch #122 or generated trees. Live proof of the misclassified-executable path is still the next vendor-bootstrap plan — this task’s own plan was correctly prose/policy, so it could not exercise that FAIL path.

## Plan Accuracy

Sequence, files, and locked sentences were right. Build did not reorder or add steps. The FAIL-after-strike challenge was the one that mattered; it was designed in Plan rather than discovered in Build.

## Build & QA Observations

Build was a two-file wording apply. QA caught nothing substantive: character-for-character match, `make test` green, no generated-tree edits. Advisory only: L2/L3 plan docs still say executable vs prose/policy without restating the consequence test — they already defer to `always-tdd`, so they were left alone on purpose.

## Insights

### Technical

- Prefixing “the product's” does not survive a vendored CLI. An in-scope category list is the bug; the change-detector consequence test is the classifier.
- “Do not invent tests” loses when FAIL keys off the plan’s “executable” label. After a strike, the judge has to ask What TDD Governs, not what the planner wrote on the heading.

### Process

- A one-file bet that preflight will inherit always-tdd fails when preflight has its own FAIL path. Echo the classifier as judge actions (classify / strike / FAIL), not as a second copy of the definition.
- Lock sentences in the L2 plan; treat issue-body “proposed wording” as a draft. QA then has something to diff.

### Million-Dollar Question

If “would a user of this product observe the break?” had been the definition from the start, #95’s change-detector paragraph, #116’s prefix, and this FAIL rewrite would have been the same sentence. Foundational still means asking that question in always-tdd Determine Scope before locating tests — #95 already recorded that and this task still did not reshape the four steps. The split we shipped is the right one for a follow-up: reference holds the test, workflow holds the judge actions.
