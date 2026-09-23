# Active Context

## Current Task: choose-verification-model
**Phase:** REFLECT - COMPLETE

## What Was Done
- Reflect finished. Archive has not been run.
- After reflect, the operator reassigned tiers and changed the skill shape.
- Tiers are `C`, `B`, `A`, `S` from lowest to highest, assigned by hand. The letters stand where they disagree with BenchLM: Kimi stays A while Opus is S; Sonnet stays B while Grok is A.
- Sometimes-enabled slugs: `claude-fable-5-1-thinking-high` (S), `gpt-5.6-sol-medium` (A), `gpt-5.6-luna-medium` (C).
- A trailing `-fast` is the same catalog row. Rank uses the base output price. After the choice, append `-fast` only when the author slug ended in `-fast` and the chosen model has `has_fast`.
- Skill layout: `SKILL.md` only at the skill root; `scripts/pick.py`, `scripts/refresh.py`, `scripts/modelpool.py`; `assets/catalog.json`, `assets/mapping.json`; `references/refresh.md`. The description is not Niko-specific.
- Shipped mapping rows omit `output_multiplier`. It was 1 because each slug already had its own pricing row.
- Spawn lines were left as the build wrote them. The operator said not to edit anything outside the skill during the follow-up.
- `tests/choose-verification-model/` still imports from the skill root. `test_shipped.py` still requires `composer-2.5-fast` and JSON beside `SKILL.md`.

## Decisions
- A null-tier or null-score author exits 2
- Opus, Sonnet, and Fable share family `claude`. Sol, Terra, and Luna share `gpt`. Composer is one row, family `composer`.
- BenchLM fetch sends a User-Agent. The default urllib agent gets 403
- Fast price is not part of ranking. `has_fast` is true when the pricing page has a `{Name} (Fast)` row or the model's notes mention a fast mode

## Deviations
- Added the null-tier author exit from the preflight advisory. It was not in the plan's behavior list
- Shebangs on `pick.py` and `refresh.py` so the executable bit can launch them
- Post-reflect follow-up moved the skill into `scripts/`, `assets/`, and `references/`, and collapsed fast into the base slug. Spawn lines still say `pick.py` beside `SKILL.md`

## Tests
- 27 unittest cases were green at reflect. After the follow-up they still target the old paths and `composer-2.5-fast`

## Next Step
- Open the draft pull request on `model-reviewer-selection-tiers`, then `/niko-archive`.
