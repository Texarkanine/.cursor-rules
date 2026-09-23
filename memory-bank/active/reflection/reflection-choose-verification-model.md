---
task_id: choose-verification-model
date: 2026-09-23
complexity_level: 3
---

# Reflection: choose-verification-model

## Summary

The skill, the picker, the catalog refresh, and the Niko spawn lines shipped. QA failed once on a stale testing sentence in `techContext.md`, that sentence was corrected, and the rerun passed.

## Requirements vs Outcome

The brief's ten requirements are in the tree. `pick.py` applies the rank, family, tier, and cost rule. `refresh.py` rewrites scores and output prices and keeps hand-set tiers. The nine spawn lines and the README tell the agent to run the picker.

Two additions were not in the plan's behavior list. A null-tier or null-score author exits 2, from a preflight advisory. `refresh.py` sends a User-Agent because BenchLM returns 403 without one. `composer-2.5-fast` uses the `Composer 2.5 (Fast)` price row with multiplier 1, which the plan allowed when the row exists. The optional `--json` trace was left out. The empty-next-tier fallback stayed untested; QA marked it non-blocking.

## Plan Accuracy

The six units ran in order, and the red-then-green cycle held for the three executable units. The file list was right for the skill, the tests, the spawn lines, the README, and the CI job.

Two surprises were outside the challenge list. BenchLM rejects urllib's default User-Agent. `memory-bank/techContext.md` still described `make test` as only the layout checks, and the plan never named that file. The pricing-page and BenchLM-shape risks in the pre-mortem showed up as fixture tests, not as live parse failures. The earlier SWE-bench dead end was settled before this build and did not return.

## Creative Phase Review

No creative phase. The selection rule was already specified, and the build followed it. The live fetches belonged in preflight, which is where the score source changed from SWE-bench to BenchLM. A creative pass would not have found the User-Agent rejection.

## Build & QA Observations

The picker and refresh tests failed on stubs, then passed. `make test` was 27 unittest cases plus the two link checks.

The first QA pass, on `claude-sonnet-5-thinking-high`, was `FAIL (fixable)` for the Testing Process sentence. The fix pointed at `tests/` and left the Python version in the workflow. The rerun, on `gemini-3.8-flash-high`, was `PASS`. QA also noted the empty-next-tier path. That path errors, which is the same outcome as an empty pool, and none of the nine shipped slugs can hit it.

## Cross-Phase Analysis

Preflight's blocking finding, that SWE-bench had no rows for these models, stopped a picker that would have exited 2 on every call. That was the expensive discovery, and it happened before code.

The doc failure has a shorter chain. The plan added a Make target and a CI job, and preflight checked that CI mirrors Make. Neither step asked whether `techContext.md` still described `make test`. The file's own update rule says a test-process change is a surgical fix. QA was the first pass that compared the sentence to the Makefile.

## Insights

### Technical

- `https://benchlm.ai/data/models.json` returns 403 unless the request sets a User-Agent. `refresh.py` sends `choose-verification-model`.
- Fast variants on the Cursor pricing page are their own rows. `Composer 2.5 (Fast)` is not a multiplier on `Composer 2.5`.

### Process

- A plan that adds a Make target has to include `memory-bank/techContext.md` when that file states what `make test` runs. Preflight's "CI matches Make" check does not read that sentence.
