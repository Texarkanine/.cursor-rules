# Active Context

## Current Task: effort-variant-slug
**Phase:** BUILD - operator reversed the placement rule after reflect

## What Was Done
- Effort is not a score. `model_key` strips `-fast` and one trailing effort word. `thinking` stays. Every effort of a model is that one BenchLM row.
- Catalog and mapping keys are model stems. Each catalog row has `effort_encoded: false`.
- The printed reviewer keeps the effort on the first `--reviewer-models` spelling of that model. The author's effort is not copied. `-fast` still follows the author when `has_fast` is true.
- An author whose model is absent is printed, exit 0. An enabled spelling whose model is absent exits 2.
- `make test`: 46 tests OK. `SKILL.md` is unchanged.
- Draft PR 130 still describes the rejected in-memory interpolation. This correction is local and uncommitted.

## Next Step
- Commit and push when the operator asks, then correct the PR body. Archive stays after that.

## Files
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/scripts/modelpool.py`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/scripts/pick.py`
- `/home/mobaxterm/git/.cursor-rules/rules/choose-verification-model/references/refresh.md`
- `/home/mobaxterm/git/.cursor-rules/tests/choose-verification-model/test_pick.py`
- `/home/mobaxterm/git/.cursor-rules/tests/choose-verification-model/test_shipped.py`

## Deviations
- The operator rejected score interpolation. Effort changes intelligence differently per family, and BenchLM does not encode it. The catalog key is the model. Effort is chosen only on the review candidate.
