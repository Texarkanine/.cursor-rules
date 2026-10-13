---
task_id: mb-init-agents-only
date: 2026-10-12
complexity_level: 2
---

# Reflection: Memory-bank init writes AGENTS.md only

## Summary

Niko's first-init root bootstrap now writes only a thin `AGENTS.md`, created when root `AGENTS.md` is absent; `CLAUDE.md` is never created and no longer affects the gate. Preflight and QA both passed; `make test` is green.

## Requirements vs Outcome

All four requirements and acceptance criteria 1–5 were delivered as planned. The operator changed one requirement during intent clarification: the gate keys on `AGENTS.md` alone, rather than the recommended "skip if either exists". Nothing was dropped or added. AC 6 (non-draft PR and `/handoff`) runs after this phase, at the operator's request.

## Plan Accuracy

The file list, sequence, and scope were right; the build was a straight run. The one miss was in the plan's own check: the grep expectation listed only the pre-existing line 28 and forgot the "never creates `CLAUDE.md`" sentence the plan itself added. The build corrected the expectation, not the content.

## Build & QA Observations

The build was clean. QA found no defects. One non-blocking redundancy remains on purpose: "do not follow symlinks to edit through them" overlaps "do not … symlink-replace it" now that init never edits an existing file. Fable 5.1 was out of credits for Preflight, so both subagents ran on Opus, which is the same model family as the author.

## Insights

### Technical
- Issue #101's "both absent" gate rested on a harness fact that the rule itself never stated: Claude Code ignoring `AGENTS.md`. When that fact changed, only the issue's rationale showed which half of the design depended on it. If a rule exists only for compatibility, it can say which harness behavior it covers. That shows when the rule can be retired.

### Process
- Base verify expectations (grep hits, counts) on the planned end state, not on the file as it was before the edit.

### Million-Dollar Question

If harnesses had always read `AGENTS.md`, init would have had one gate on one file, which is what exists now. The remaining question is the one Preflight raised: most consumer repos already have an `AGENTS.md`, so the skip path is the common one. A read-only check could show the operator a pointer to paste when the existing file never mentions `memory-bank/`. That is a separate product decision and is not part of this task.
