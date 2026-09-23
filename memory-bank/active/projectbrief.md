# Project Brief

## User Story

As an operator running `choose-verification-model`, I want an effort spelling that is not a catalog key to still receive a place on the scale, so that `pick.py` can rank the author and choose a reviewer instead of exiting before any ranking.

## Use-Case(s)

### Author effort differs from the stored row

The live author slug differs from the catalog key only by effort (`low`, `medium`, `high`, `xhigh`), with or without a trailing `-fast`. The selector places that author and runs the existing window and one-tier lookup.

### Reviewer list contains an unmatched effort spelling

A slug in `--reviewer-models` differs from a catalog key only by effort. That miss does not abort the pick before ranking.

## Requirements

As described in [issue #129](https://github.com/Texarkanine/.cursor-rules/issues/129):

1. A minor slug difference, such as effort level, must not make `pick.py` give up. Today `canonical_slug` strips a trailing `-fast` and then requires an exact catalog key. `low`, `medium`, `high`, and `xhigh` stay part of the key. A miss exits 2 before any ranking, for the author and for every slug in `--reviewer-models`.
2. An unmatched effort spelling gets a place on the scale: a tier, a rank among neighbors, a family, enough that the existing window and one-tier lookup can run.
3. The printed reviewer still comes from a decision about who is allowed to review, not from whatever slug happened to show up.
4. Opus at one effort is not Opus at another effort. Collapsing every effort of a model onto the one stored row would rank the author in the wrong place. The selector still has to know where that effort lands, relative to the rows we did choose.

## Constraints

1. The hand-chosen catalog stays the set of reviewers we decided to keep. Writing every effort spelling into `catalog.json` is not the goal.
2. Do not treat different efforts of one model as the same row.
3. Do not store or rank on the fast price. Trailing `-fast` already means the same model, same score, same tier. Effort does not.
4. Do not retier the rows already chosen, except as a side effect inside an in-memory catalog during one pick.
5. Several chosen keys already end in an effort word. A blind strip of that word cannot tell the chosen row from some other effort of that model.
6. The synthetic in-memory placement sketched in the issue is one approach to explore, not a decision.

## Acceptance Criteria

1. `python3 scripts/pick.py --model cursor-grok-4.6-xhigh-fast --reviewer-models claude-opus-5-5-high,gpt-5.6-terra-medium,grok-4.7-xhigh` does not exit 2 with `unknown slug`.
2. The author is placed relative to the stored rows for that effort, not collapsed onto a different effort of the same model.
3. The printed reviewer is a model the selector is allowed to choose, not an unmatched spelling that merely appeared in the input.
4. `catalog.json` on disk does not gain a row for every effort spelling.
