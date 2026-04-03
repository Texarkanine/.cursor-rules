# Project Brief: /niko-save Command

## Task
Implement `/niko-save` as described in [issue #52](https://github.com/Texarkanine/.cursor-rules/issues/52).

## Requirements
`/niko-save` is an operator-invokable command that:

1. **Flushes in-context state to the memory bank** — any relevant state that exists in the context window but hasn't been written to disk:
   - `tasks.md`: mark completed steps, note which step is in progress
   - `activeContext.md`: current phase, what was just done, what the next action is
   - `progress.md`: any phase completions or significant work not yet recorded
   - Creative/reflection docs in progress

2. **Commits everything atomically** — memory bank flush first, then all changes (code, memory bank, everything) in a single commit: `chore: /niko-save [task-id] at [phase]`

## Key Constraints
- NOT a workflow phase — does not advance the workflow, trigger transitions, or produce deliverables
- Operator-initiated only (no auto-save)
- Save and resume happen in the same repo (memory bank is repo-local)
- No `/niko-resume` needed — `/niko` already handles re-entry via existing state detection

## Deliverable
- Canonical skill: `rulesets/niko/skills/niko-save/SKILL.md`
- Mirroring to `.cursor/` and `.claude/` handled out-of-band by ai-rizz/a16n tooling
