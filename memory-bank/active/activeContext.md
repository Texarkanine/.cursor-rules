# Active Context

## Current Task: architecture-docs-authoring-skill
**Phase:** BUILD - COMPLETE

## What Was Done
- Deep research: stockroom Architecture (pages + archive + sessions), ai-rizz Architecture, Niko templates + update-contract archive, a16n understanding-conversions, rust-analyzer + Flutter engine FOSS docs
- Synthesized principles in `architecture-docs-research.md`; TDD checklist in `architecture-docs-acceptance.md`
- Authored `rules/architecture-docs/SKILL.md` (framed principle + anti-pattern reference)
- Packaged: symlink `rulesets/authoring/skills/architecture-docs` → `../../../rules/architecture-docs`; README entry; REUSE already covers `rules/**/*.md`

## Files Created or Modified
- `rules/architecture-docs/SKILL.md` (new)
- `rulesets/authoring/skills/architecture-docs` (symlink)
- `rulesets/authoring/README.md`
- `memory-bank/active/architecture-docs-research.md`
- `memory-bank/active/architecture-docs-acceptance.md`
- `memory-bank/active/tasks.md`, `activeContext.md`

## Key Implementation Decisions
- Ten portable principles + short domain-mapping sibling note (a16n); no case-study novels in skill body
- Orientation-diagram principle explicitly anti-mimics "always control-flow Mermaid"
- Genre frame separates Architecture from memory-bank / how-to / agent system-model

## Deviations from Plan
- None material — FOSS used as tertiary corroboration only; research notes stay in memory bank

## Integration / Verification
- Acceptance checklist all green; packaging `readlink` OK; sibling repos and Niko mdc templates untouched

## Next Step
- QA phase (automatic after build PASS per L3 workflow)
