# Task: /niko-save Command

* Task ID: niko-save
* Complexity: Level 2
* Type: Simple Enhancement

Implement `/niko-save` — an operator-invokable skill that flushes in-context memory bank state to disk and commits all changes atomically. Not a workflow phase; does not advance workflow state. Canonical source: `rulesets/niko/skills/niko-save/SKILL.md`.

## Test Plan (TDD)

### Behaviors to Verify

This repository has no automated test infrastructure. The deliverables are markdown instruction files (SKILL.md, README updates). Verification will be performed by structural review during QA.

- **Frontmatter compliance**: SKILL.md has `name` and `description` fields in YAML frontmatter matching the pattern of existing skills
- **Guard rail**: Skill detects when no active state exists and stops without making changes
- **State flush — tasks.md**: Instructions direct the agent to update completed/in-progress step markers
- **State flush — activeContext.md**: Instructions direct the agent to update phase, recent actions, next steps
- **State flush — progress.md**: Instructions direct the agent to record any unrecorded phase completions
- **State flush — creative/reflection**: Instructions address in-progress creative/reflection docs
- **Atomic commit**: Instructions produce a single commit with format `chore: /niko-save [task-id] at [phase]`
- **Non-advancement**: Skill explicitly does NOT trigger phase transitions, advance the workflow, or produce deliverables
- **Task-id and phase extraction**: Instructions identify where to derive task-id and phase from existing memory bank files

### Test Infrastructure

- Framework: None (rules/skills repository — no application code, no test runner)
- Test location: N/A
- Conventions: N/A
- New test files: None

## Implementation Plan

1. **Create `rulesets/niko/skills/niko-save/SKILL.md`**
   - Files: `rulesets/niko/skills/niko-save/SKILL.md` (new)
   - Changes: New skill file with:
     - YAML frontmatter (`name: niko-save`, `description: ...`)
     - Step 1: Guard — verify active memory bank state exists
     - Step 2: Read current disk state of all ephemeral files
     - Step 3: Flush — update each ephemeral file with in-context state not yet on disk
     - Step 4: Commit atomically with `chore: /niko-save [task-id] at [phase]`
     - Explicit non-advancement disclaimer

2. **Update `rulesets/niko/README.md`**
   - Files: `rulesets/niko/README.md`
   - Changes: Add `/niko-save` documentation in the Usage section, explaining its purpose (mid-phase save for cross-harness portability and graceful exit) and that resume is handled by `/niko` re-entry

## Technology Validation

No new technology — validation not required.

## Dependencies

- Existing memory bank file conventions (paths, formats)
- Existing skill frontmatter pattern (`name`, `description`)
- Existing commit message conventions (`chore:` prefix)

## Challenges & Mitigations

- **Judgment call for flush**: The agent must assess what in-context state hasn't been written to disk — this is inherently fuzzy. Mitigation: SKILL.md instructions should be specific about what to check in each file, giving the agent a concrete checklist rather than a vague "flush everything."
- **Task-id extraction**: Task-id might be in `tasks.md` header, `progress.md`, or `projectbrief.md` with varying formats. Mitigation: Specify a clear precedence order for finding task-id.
- **Phase extraction**: Phase comes from `activeContext.md` which has no rigid schema. Mitigation: Instruct the agent to read the `**Phase:**` field, matching the convention used by all existing phases.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight (PASS)
- [x] Build
- [ ] QA
