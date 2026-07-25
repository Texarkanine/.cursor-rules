# Project Brief

## User Story

As a maintainer of this ai-rizz source repository, I want agent-selected description rules and commands converted into Cursor agent skills (via a16n IR round-trip) so that we no longer ship description-based rules or commands.

## Use-Case(s)

### Use-Case 1

An operator discovers in-scope Cursor customizations under `rules/`, converts description-bearing rules (and any remaining commands) through a16n IR back to Cursor skills with `--delete-source`, and commits incrementally so mistakes are recoverable.

### Use-Case 2

Consumers of this repo via ai-rizz continue to get equivalent guidance, now as skills rather than agent-selected rules/commands, with rulesets/symlinks and docs still correct.

## Requirements

1. Read [a16n docs](https://texarkanine.github.io/a16n/) and [ai-rizz docs](https://texarkanine.github.io/ai-rizz/) carefully before converting.
2. Enumerate conversion targets first with `npx a16n discover` (and dry-runs as needed).
3. Convert commands and rules with descriptions into agent skills by converting cursor → a16n IR → cursor.
4. Use `--delete-source` so source description rules/commands are removed after conversion.
5. Work in the `rules/` directory (canonical source for this repo).
6. End state: no agent-selected description rules and no commands remain in scope.
7. Use git commits liberally for easy recovery.

## Constraints

1. Preserve always-apply global prompts and glob-based file rules unless discover shows they are in scope for this migration.
2. Respect ai-rizz source-repo layout (rules vs rulesets/skills/commands).
3. Prefer a16n conversion over hand-rewriting content.
4. Commits must use `--no-gpg-sign` and git must be invoked with `--no-pager`.

## Acceptance Criteria

1. `npx a16n discover` (and related checks) show no remaining in-scope description rules or commands that should have become skills.
2. Converted content exists as Cursor skills under the appropriate `rules/` (and ruleset) layout.
3. Source description rules/commands that were converted are deleted (via `--delete-source` or equivalent verified outcome).
4. Ruleset symlinks/docs updated as needed so ai-rizz install paths remain coherent.
5. Migration progress is checkpointed with recoverable git commits.
