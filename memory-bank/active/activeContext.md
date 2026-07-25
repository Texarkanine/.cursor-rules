# Active Context

## Current Task: description-rules-and-commands-to-skills
**Phase:** PLAN - COMPLETE

## What Was Done
- Planned Level 3 migration: stage-only a16n IR round-trip for 10 description rules → `rules/<name>/SKILL.md`; keep GlobalPrompts + FileRules.
- Operator decision: hand-wrap `pr-feedback-judge` and `wiggum-niko-coderabbit-pr` as ManualPrompt skills (`disable-model-invocation: true`); **reject** `@`-neutralize workaround.
- Empirical discover: staged `rules/*.mdc` → 10 simple-agent-skill, 5 global-prompt, 2 file-rule; commands skipped by a16n on `@`.

## Next Step
- Preflight phase to validate the plan before build.
