# Task: Onboard Gemini 4 Argon and Claude Haiku 5.5

* Task ID: onboard-argon-haiku
* Complexity: Level 2
* Type: simple enhancement

Refresh the choose-verification-model catalog so Gemini 4 Argon is tier A and Claude Haiku 5.5 is tier C. A live refresh also adds the thinking stem of Haiku 5.5, which is a separate catalog key for the same product, so that stem is tier C too.


## Test Plan (TDD)

### Behaviors to Verify

- Argon is selectable: a reviewer list containing `gemini-4-argon-medium` → the slug is in the shipped catalog and mapping
- Argon is tier A: author `gpt-5.6-sol-medium`, enabled Sol and `gemini-4-argon-medium` → `gemini-4-argon-medium`
- Argon is not tier S: author `claude-opus-5-5-medium`, enabled Opus and `gemini-4-argon-medium` → `claude-opus-5-5-medium`
- Argon does not review another Gemini: author `gemini-3.8-flash-high`, enabled Flash and `gemini-4-argon-medium` → `gemini-3.8-flash-high`
- Argon has no fast variant: author `gpt-5.6-sol-medium-fast`, enabled Sol and `gemini-4-argon-medium` → `gemini-4-argon-medium`
- Haiku is selectable: a reviewer list containing `claude-haiku-5-5-low` → the slug is in the shipped catalog and mapping
- Haiku is tier C: author `composer-2.5`, enabled Composer and `claude-haiku-5-5-low` → `claude-haiku-5-5-low`
- Haiku is not tier B or A: author `gpt-5.6-terra-medium`, enabled Terra and `claude-haiku-5-5-low` → `gpt-5.6-terra-medium`
- Haiku has no fast variant: author `composer-2.5-fast`, enabled Composer and `claude-haiku-5-5-low` → `claude-haiku-5-5-low`
- Thinking Haiku is selectable: a reviewer list containing `claude-haiku-5-5-thinking-low` → the slug is in the shipped catalog and mapping
- Thinking Haiku is tier C: author `composer-2.5`, enabled Composer and `claude-haiku-5-5-thinking-low` → `claude-haiku-5-5-thinking-low`
- Thinking Haiku is not tier B or A: author `gpt-5.6-terra-medium`, enabled Terra and `claude-haiku-5-5-thinking-low` → `gpt-5.6-terra-medium`
- Thinking Haiku has no fast variant: author `composer-2.5-fast`, enabled Composer and `claude-haiku-5-5-thinking-low` → `claude-haiku-5-5-thinking-low`

### Test Infrastructure

- Framework: stdlib `unittest`, run with `make test`
- Test location: `tests/choose-verification-model/`
- Conventions: `ShippedTests` in `test_shipped.py` calls `select` on the shipped JSON. Tiers are pinned by who gets chosen, not by reading the tier letter. Numeric scores stay unlocked. `SPAWNABLE` holds slugs this session can spawn. `SOMETIMES` holds slugs that still have to resolve.
- New test files: none

## Implementation Plan

### 1. Ship Argon and both Haiku 5.5 stems — executable

- Files: `tests/choose-verification-model/test_shipped.py`, `rules/choose-verification-model/assets/tiers.toml`, `rules/choose-verification-model/assets/mapping.json`, `rules/choose-verification-model/assets/catalog.json`

1. Stub tests: add empty methods on `ShippedTests` for the Argon, Haiku, and thinking-Haiku cases, and add the three spellings to `SPAWNABLE` or `SOMETIMES` only as comments until the assertions exist.
2. Stub interface: no new functions. `select` and `refresh.py` already implement this.
3. Write tests and run red: fill in the assertions above. Put `gemini-4-argon-medium` in `SPAWNABLE`. Put `claude-haiku-5-5-low` and `claude-haiku-5-5-thinking-low` in `SOMETIMES`. Run `python3 -m unittest tests.choose-verification-model.test_shipped`. Expect `unknown slug` failures.
4. Write code and run green: add `gemini-4-argon` under A in `tiers.toml`, and add `claude-haiku-5-5` and `claude-haiku-5-5-thinking` under C. From `rules/choose-verification-model`, run `python3 scripts/refresh.py`. Confirm the mapping gained only those three stems and that every pre-existing mapping row is unchanged. Then re-run the shipped tests, then `make test`.

## Technology Validation

No new technology - validation not required

## Dependencies

- `agent --list-models` on this machine
- BenchLM `https://benchlm.ai/data/models.json`
- Cursor pricing `https://cursor.com/docs/models-and-pricing.md`
- Python 3.11 or later (`tomllib`)

## Challenges & Mitigations

- Refresh adds `claude-haiku-5-5-thinking` as well as `claude-haiku-5-5`. BenchLM scores only `claude-haiku-5-5`, and both stems match the pricing name Claude Haiku 5.5. The operator named that product at tier C, so both stems are C. A null tier would fail the shipped ladder check.
- A live listing also names Fable 5, GPT-5.1, and GPT-5 Mini. A simulated fill leaves them out: Fable 5 and GPT-5 Mini have no BenchLM category score, and GPT-5.1 has no pricing row. Do not add rows for them. Keep the warnings.
- Refresh can rewrite other catalog scores. Do not hand-edit scores. Existing mapping rows must stay equal to their pre-refresh bytes.
- Argon and Haiku have no `-fast` spelling in the listing, and the pricing notes do not mention a fast mode. The fast-author tests pin `has_fast` false.

## Pre-Mortem

- One Haiku slug was assumed, so the thinking stem shipped with a null tier or was deleted and came back on the next refresh: the plan names both keys and tiers both before the green run.
- Catalog JSON was hand-written, so the next refresh disagreed: the plan runs `refresh.py` after `tiers.toml`.
- A test locked BenchLM's 80.88 overall, which is not the stored score: tests assert `select` results. The stored score is the mean of the agentic, coding, and reasoning categories that are present. Haiku currently has one of those.
- Refresh onboarded Fable 5 or GPT-5.1 and the suite gained null tiers: already covered by the listing simulation in Challenges. If the live run adds any other stem, remove that row and stop.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
