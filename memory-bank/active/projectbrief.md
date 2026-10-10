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

## Rework: Gate the Level 1 Handoff on the Router's Rule

Source: CodeRabbit review comment [r4235005318](https://github.com/Texarkanine/.cursor-rules/pull/134#discussion_r4235005318) on PR #134.

Level 1 Wrap-Up points to `/niko-archive` whenever `memory-bank/active/reflection/` has files. A reflection left over from an earlier task does not mean the task was reworked. In that state, a plain Level 1 task is sent to `/niko-archive`. The router then finds only Level 1, which has no archive, and the operator never sees the delete instructions.

### Requirement

In `rulesets/niko/skills/niko/references/level1/level1-workflow.md` Wrap-Up, replace the `reflection/` check with the router's own rule: `progress.md` records a cycle classified above Level 1. Keep the `milestones.md` check first.

### Acceptance

- A Level 1 rework of a Level 2 task (both acceptance states above) still ends by pointing to `/niko-archive`.
- A plain Level 1 task ends with the delete instructions, even when a stale reflection file is present.
- A Level 1 L4 sub-run still gets the sub-run message.

### Out of Scope

- The other two CodeRabbit claims on PR #134, judged invalid.
- QA advisory 3 (`level1-workflow.md` line 26 still says Level 1 has no `/niko-archive`).
