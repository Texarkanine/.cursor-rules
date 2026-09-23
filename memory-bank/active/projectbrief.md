# Project Brief

## User Story

As an operator running `/choose-verification-model`, I want `cursor-grok-4.6-xhigh` in the catalog, including its fast spelling, so that `pick.py` accepts that author slug instead of exiting 2.

## Use-Case(s)

### Use-Case 1

`pick.py --model cursor-grok-4.6-xhigh-fast` with reviewer slugs that are already in the catalog exits 0 and prints a reviewer. Today it exits 2: `unknown slug: cursor-grok-4.6-xhigh-fast`.

## Requirements

1. Catalog slug is `cursor-grok-4.6-xhigh`. The fast spelling is `cursor-grok-4.6-xhigh-fast` and is not its own row.
2. `has_fast` is true. Cursor's pricing page has `Grok 4.6` at $6 output and `Grok 4.6 (Fast)` at $12. Rank on the base price.
3. BenchLM slug `grok-4-6` supplies the category mean. Family is `grok`.
4. Hand-set tier is A, with Grok 4.7.

## Constraints

1. Do not retarget existing slugs. `claude-opus-5-5-high` and `grok-4.7-xhigh` are still unknown. The sample command that lists those reviewers will still exit 2 after this change. That follow-up is out of scope.
2. Edit `rules/choose-verification-model/` only. Do not edit the installed copy under the user skills tree or the generated `.cursor/` tree.

## Acceptance Criteria

1. `cursor-grok-4.6-xhigh` is in `mapping.json` and `catalog.json`, with a non-null score, tier A, base output cost, and `has_fast` true.
2. A fast author whose only in-window reviewer is this row prints `cursor-grok-4.6-xhigh-fast`. A non-fast author prints `cursor-grok-4.6-xhigh`.
3. `pick.py` does not report `unknown slug` for `cursor-grok-4.6-xhigh` or `cursor-grok-4.6-xhigh-fast`.
