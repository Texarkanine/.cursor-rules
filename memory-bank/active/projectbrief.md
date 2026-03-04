# Project Brief: Niko Ruleset Enhancements

## User Story

As a Niko user, I want three targeted improvements to the Niko ruleset:

1. **QA & Plan documentation enforcement**: QA should always verify that relevant documentation was updated alongside code changes. Plan should proactively include documentation updates in its output.
2. **Level 1 wrap-up guidance**: Evaluate and opine on how Level 1 tasks should handle `memory-bank/active/` cleanup, since L1 has no archive phase.
3. **Fix lazy internal rule references**: All internal references to Niko rule files that use shorthand (e.g., `milestones.mdc`) must be expanded to their full expected path form (e.g., `.cursor/rules/shared/niko/memory-bank/active/milestones.mdc`).

## Requirements

- Each of the three items should be committed separately so the PR shows distinct changes per item.
- Edits must target the canonical source in `rulesets/niko/` — never `.cursor/` or `.claude/`.
- Item 2 requires evaluation and an opinionated recommendation, not necessarily a code change.
