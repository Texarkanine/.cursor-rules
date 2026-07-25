---
task_id: rulesets-link-ci
date: 2026-07-25
complexity_level: 2
---

# Reflection: rulesets-link-ci

## Summary

Shipped POSIX check scripts, `make test`, and a two-job PR workflow that verify `rulesets/` symlink targets and README internal links. Delivered to plan; no framework introduced.

## Requirements vs Outcome

All brief requirements met: two separable checks, shared Make entrypoint, GHA invokes Make only, scripts follow shell-posix-style. Added optional rulesets-root CLI args (preflight amendment) for fixture negatives without mutating the real tree.

## Plan Accuracy

Sequence and file list held. Main surprise was TDD encoding for “layout assertions, not unit tests” — resolved by RED Make targets then GREEN scripts, not shunit2.

## Build & QA Observations

Build was straightforward once the no-framework decision landed. QA caught real cleanup: duplicated path helpers and an opaque FAIL-marker pipeline (replaced with a temp failure file).

## Insights

### Technical
- Without `pipefail`, communicating failure out of `find | while` subshells needs an out-of-band channel (temp file works; pipeline-tail status alone is easy to get wrong).

### Process
- “No test framework” still needs an explicit RED→GREEN story in the plan or preflight will (correctly) block on TDD encoding.

### Million-Dollar Question

Nothing notable — Make + two small scripts + two CI jobs is the natural shape if this had been assumed from day one.
