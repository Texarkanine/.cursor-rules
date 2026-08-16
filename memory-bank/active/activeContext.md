# Active Context

## Current Task: writing-styles-ruleset
**Phase:** BUILD - COMPLETE

## What Was Done
- Renamed `rules/asd-ste100.mdc` and `rules/iso-24495.mdc` to `always-respond-*`; retitled; qualifier now "Clarity and accuracy trump style."
- Added always-respond keys for `turner-truth` and `orwell-6`; four `always-write-*` keys; four `*-style` ManualPrompt skills.
- Assembled `rulesets/writing-styles/` (four skill symlinks + README with style-selection pointers and placeholder sample table). Added root README door.
- `make test` PASS. Old names gone. No always-on `.mdc` in the ruleset.

## Files
- `/home/mobaxterm/git/.cursor-rules/rules/always-respond-asd-ste100.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/always-respond-iso-24495.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/always-respond-turner-truth.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/always-respond-orwell-6.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/always-write-asd-ste100.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/always-write-iso-24495.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/always-write-turner-truth.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/always-write-orwell-6.mdc`
- `/home/mobaxterm/git/.cursor-rules/rules/asd-ste100-style/SKILL.md`
- `/home/mobaxterm/git/.cursor-rules/rules/iso-24495-style/SKILL.md`
- `/home/mobaxterm/git/.cursor-rules/rules/turner-truth-style/SKILL.md`
- `/home/mobaxterm/git/.cursor-rules/rules/orwell-6-style/SKILL.md`
- `/home/mobaxterm/git/.cursor-rules/rulesets/writing-styles/README.md`
- `/home/mobaxterm/git/.cursor-rules/rulesets/writing-styles/skills/{asd-ste100-style,iso-24495-style,turner-truth-style,orwell-6-style}`
- `/home/mobaxterm/git/.cursor-rules/README.md`

## Decisions
- Turner/Orwell keys stay one-liners; Princeton URL labeled `Book:` to match `Official standard:` / `Public summary:`.
- README "Which Style" is pointers only (preflight advisory).

## Deviations
- None — built to the amended plan.

## Next Step
- QA review (spawn `/niko-qa`).
