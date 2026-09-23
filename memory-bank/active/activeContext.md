# Active Context

## Current Task: choose-verification-model
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- `rules/choose-verification-model/`: `SKILL.md`, `pick.py`, `refresh.py`, `modelpool.py`, `mapping.json`, `catalog.json`
- `tests/choose-verification-model/`: 27 tests. `make test` passes, including the link checks
- Symlink `rulesets/niko/skills/choose-verification-model`. Nine spawn lines and the README Subagent Selection section run `pick.py`
- PR workflow job `choose-verification-model` runs `make test-choose-verification-model` on Python 3.11

## Decisions
- A null-tier or null-score author exits 2
- Opus and Sonnet share family `claude`. Both Composer slugs share family `composer`. `composer-2.5-fast` uses the `Composer 2.5 (Fast)` price row, multiplier 1
- BenchLM fetch sends a User-Agent. The default urllib agent gets 403

## Deviations
- Added the null-tier author exit from the preflight advisory. It was not in the plan's behavior list
- Shebangs on `pick.py` and `refresh.py` so the executable bit can launch them

## Tests
- 27 new unittest cases, including 1 refresh-then-pick integration case. `make test` passed

## Next Step
- QA PASSED — proceed to `/niko-reflect`
