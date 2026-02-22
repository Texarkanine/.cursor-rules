---
task_id: archive-completion-gate
date: 2026-01-25
complexity: level-1
status: completed
---

# TASK ARCHIVE: Archive Command Completion Gate

## SUMMARY

Added a "completion gate" pattern to the `/archive` command to prevent agents from reporting completion before finishing all required steps (particularly the mandatory git commit).

## REQUIREMENTS

- Prevent incomplete workflow execution in `/archive` command
- Add explicit stop condition that agents cannot miss
- Provide verifiable completion criteria

## IMPLEMENTATION

Added two sections to `rulesets/niko/commands/niko/archive.md`:

1. **Completion Gate (at top, line 3):**
   ```markdown
   **⛔ COMPLETION GATE:** This command ends with a git commit. Do not report completion until `git log -1` shows `chore: archive <task-id>`.
   ```

2. **Verification Section (before Next Steps):**
   ```markdown
   ## Verification (REQUIRED before responding)
   Before reporting completion, run:
   git log -1 --oneline && git status --short memory-bank/
   ```

## TESTING

- Verified file changes with `head` and `tail` commands
- Commit successful: `97c1b5c fix(niko): add completion gate to archive command`

## LESSONS LEARNED

1. Critical requirements buried mid-workflow get skipped - put them at TOP
2. Verifiable stop conditions ("run this command") work better than prose instructions
3. Commands with mandatory git commits need explicit gates

## REFERENCES

- Reflection: `memory-bank/reflection/reflection-archive-completion-gate.md`
- Related: Previous archive failure in this session where agent skipped git commit step
