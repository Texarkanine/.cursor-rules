# Project Brief: Fix Orphaned Troubleshooting Path

## User Story

The `/nk-refresh` skill writes diagnostic scratch logs to `memory-bank/troubleshooting/`, which sits outside `memory-bank/active/` and is therefore never cleaned up by the archive phase or any other cleanup step. This causes leftover files to accumulate across tasks.

## Requirements

1. Move the troubleshooting log path from `memory-bank/troubleshooting/` to `memory-bank/active/troubleshooting/`
2. Register the new path in `memory-bank-paths.mdc` as an ephemeral entry, noting it is **deleted (not inlined)** during archive
3. Add an exception note to `archives.mdc` that troubleshooting logs are deleted without inlining
4. Add `troubleshooting/` to the cleanup lists in `/niko` entrypoint (Step 2a L4 milestone advance, Step 3b standalone rework clear)
5. Only edit canonical `rulesets/` files — `.cursor/` and `.claude/` copies are synced out-of-band
