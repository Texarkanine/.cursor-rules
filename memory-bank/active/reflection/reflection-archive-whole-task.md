---
task_id: archive-whole-task
date: 2026-10-09
complexity_level: 2
---

# Reflection: archive-whole-task

## Summary

A plain `/niko-archive` now archives every cycle `progress.md` records and routes on the highest level any cycle was classified at. `/niko` Step 3b records the current complexity level in the rework entry, and a Level 1 rework of a larger task ends by pointing to `/niko-archive`. Three files changed: 15 lines added, 3 removed. Both acceptance states route to the Level 2 archive.

## Requirements vs Outcome

All three changes in issue #133 shipped. Classification and the rework flow did not change. One wording change differs from the issue: Step 3b records "the current complexity level", not "the task's current level". On a second rework, the header holds the outgoing cycle's level, which is not always the task's. Routing does not depend on that line, so the change is safe.

## Plan Accuracy

The plan held: three files, one or two sentences each, in the planned order. The challenges it named (a level that is only mentioned, L4 sub-runs keeping `reflection/`) were real, and its wording handled them. The surprise came from formatting, not from the logic (see Build & QA).

## Build & QA Observations

The build was clean, and `make test` was green before and after. The first preflight subagent died with HTTP 429 when Fable 5.1 usage credits ran out. It wrote nothing, so I respawned it on Opus 5.5. QA passed and raised one real risk: Step 3b wrote the field name as `**Complexity:**` in code format, which invites an agent to copy it as a second field line. The resume step, the Level 1 completion check, and complexity analysis all look that field up by name. I removed the formatting after QA passed. The edit only removes formatting, so I did not re-run QA; this note records that.

## Insights

### Technical
- Write a field name in code format inside an instruction only when the instruction means "write this field". An agent copies literal `**Field:**` text into whatever it appends. If other steps look that field up by name, the copy creates a second match.
- The router works on files written before this change. Complexity analysis already appends a "Classified ... as Level N" entry for each cycle, so routing on "every cycle's classification" needs no new record. The Step 3b line is backup for files where those entries are thin.

### Process
- Nothing notable

### Million-Dollar Question

If the system had been designed this way from the start, it would split the field, as the issue suggests. The `progress.md` header would hold the task's level, as a running maximum. The `tasks.md` header would hold the current cycle's level, and the roughly ten per-cycle readers would read that instead. The archive would then route on one field with no history to scan. This change does not block that design.
