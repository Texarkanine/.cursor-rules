# Active Context

## Current Task: tdd-product-user-scope
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- Dropped **agent-facing prompts** from always-tdd. Out-of-scope second sentence is now repository bootstrap (`AGENTS.md`, `CLAUDE.md`, copied init text, etc.), vendored third-party tools, gitignore lines, etc.
- No niko-preflight edit. No generated-tree edits. `make test` passed.
- QA found no semantic, scope, or documentation issues in the Level 1 rework.

## Next Step
- Run `/niko-archive` for the L2 task (this L1 rework is not a reason to delete `memory-bank/active/`).
