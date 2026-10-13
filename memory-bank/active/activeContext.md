# Active Context

## Current Task: mb-init-agents-only
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done
- Intent confirmed by operator: drop `CLAUDE.md` from Niko's root bootstrap; Claude Code reads repo-root `AGENTS.md`.
- Operator decision: skip `AGENTS.md` only when `AGENTS.md` exists; `CLAUDE.md` no longer matters to the gate at all.
- Complexity determined: Level 2.
- Plan written to `tasks.md`: two prose/policy units (`memory-bank-init.md` bootstrap section, Niko README line 36) plus a grep + `make test` verify step. No new executable behavior.

## Next Step
- Preflight (subagent).
