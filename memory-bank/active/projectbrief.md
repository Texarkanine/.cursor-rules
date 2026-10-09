# Project Brief: archive-whole-task

Implement [issue #133](https://github.com/Texarkanine/.cursor-rules/issues/133) as written: a plain `/niko-archive` archives the whole task at its highest level, even after a rework was classified lower.

## Requirements

Leave classification and the rework flow as they are. Change only:

1. `rulesets/niko/skills/niko-archive/SKILL.md`: the task to archive is every cycle `progress.md` records. Route on the highest complexity level `progress.md` records, not the `**Complexity:**` header alone. A highest level of Level 1 still means no archive.
2. `rulesets/niko/skills/niko/SKILL.md` Step 3b: the rework entry appended to `progress.md` also records the task's current complexity level.
3. `rulesets/niko/skills/niko/references/level1/level1-workflow.md` Wrap-Up: after the `milestones.md` check, if `memory-bank/active/reflection/` has files, print "Run `/niko-archive`" instead of the delete instructions.

## Acceptance

- A plain `/niko-archive` on termeleon `ea8b52c` and inquirerjs-checkbox-search `1d65046` (both headers say Level 1; both are Level 2 tasks with reworks) routes to the Level 2 archive, covers every cycle, and writes `complexity_level: 2`.
- A Level 1 rework of a Level 2 task ends by pointing to `/niko-archive`. A plain Level 1 task still ends with the delete instructions.

## Out of Scope

- The Level 4 capstone gap in the issue's "Noticed, not verified" section.
- Operator steer: a precision strike. Very few, targeted edits.
