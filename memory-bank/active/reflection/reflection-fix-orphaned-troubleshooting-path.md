---
task_id: fix-orphaned-troubleshooting-path
date: 2026-04-03
complexity_level: 2
---

# Reflection: Fix Orphaned Troubleshooting Path

## Summary

Moved `/nk-refresh` troubleshooting logs from `memory-bank/troubleshooting/` to `memory-bank/active/troubleshooting/` and registered the path in the ephemeral file contract. All 5 requirements delivered cleanly; QA passed with no fixes.

## Requirements vs Outcome

Exact match. All five requirements (path fix, registry entry, archive exception, L4 cleanup, rework cleanup) were implemented as specified. No scope changes, no additions, no gaps.

## Plan Accuracy

Plan was accurate — 4 files, 5 edits, all landed as planned. The one insight from preflight was that archive phases use a blanket "delete ephemeral" instruction, so no archive-level edits were needed. This was correctly identified during preflight and saved unnecessary work.

## Build & QA Observations

Build was mechanical — each change was a single-line insertion or path replacement. No iteration needed. QA passed clean. The verification greps (zero stale references, correct new references in 3+2 locations) provided high confidence.

## Insights

### Technical

The Niko memory bank has two distinct deletion contract patterns:
1. **Archive phases** (L2/L3/L4): blanket "delete all ephemeral files" — anything under `active/` is covered automatically.
2. **`/niko` entrypoint** (Step 2a, Step 3b): selective delete lists — new ephemeral subdirectories must be explicitly added.

This asymmetry means adding a new ephemeral directory type requires updating the `/niko` selective lists but NOT the archive phases. Future additions should check both patterns.

### Process

Nothing notable — clean execution once the proper workflow was followed.

### Million-Dollar Question

If troubleshooting had been under `active/` from the start, the only difference would be that the `/niko` selective delete lists would have included it. The current implementation IS the foundational solution. No more elegant alternative exists.
