---
task_id: archive-whole-task
complexity_level: 2
date: 2026-10-10
status: completed
---

# TASK ARCHIVE: Archive the whole task after a lower-level rework

## SUMMARY

Issue [#133](https://github.com/Texarkanine/.cursor-rules/issues/133): when a rework was classified at a lower level than the original task, a plain `/niko-archive` read only the `**Complexity:**` header. It saw Level 1, which has no archive, so a Level 2 task with a Level 1 rework could not be archived. Now `/niko-archive` archives every cycle `progress.md` records and routes on the highest level any cycle was classified at. A Level 1 rework of a larger task ends by pointing to `/niko-archive`. Pull request: https://github.com/Texarkanine/.cursor-rules/pull/134

The task ran two cycles: the Level 2 fix, then a Level 1 rework from PR review. This archive was itself routed by the new rule: the header said Level 1, and the router picked the Level 2 archive.

## REQUIREMENTS

- Leave classification and the rework flow as they are. Operator steer: a precision strike, very few targeted edits.
- `/niko-archive`: the task is every cycle `progress.md` records. Route on the highest classified level, not the header alone. A highest level of Level 1 still means no archive.
- `/niko` Step 3b: the rework entry in `progress.md` also records the current complexity level.
- Level 1 Wrap-Up: after the `milestones.md` check, point a rework of a larger task to `/niko-archive` instead of printing the delete instructions.
- Acceptance: termeleon `ea8b52c` and inquirerjs-checkbox-search `1d65046` (Level 2 tasks with reworks; both headers say Level 1) route to the Level 2 archive and write `complexity_level: 2`. A plain Level 1 task still ends with the delete instructions.
- Rework (CodeRabbit [r4235005318](https://github.com/Texarkanine/.cursor-rules/pull/134#discussion_r4235005318)): gate the Level 1 handoff on the router's own rule, not on files in `reflection/`. A reflection left over from an earlier task must not send a plain Level 1 task to an archive that cannot run.
- Out of scope: the Level 4 capstone gap in the issue's "Noticed, not verified" section.

## IMPLEMENTATION

Three files, 15 lines added and 3 removed:

- `rulesets/niko/skills/niko-archive/SKILL.md`: Step 1 says the task is every cycle `progress.md` records, and that `tasks.md` and `activeContext.md` hold only the latest cycle. Step 2 defines the task's complexity level as the highest level any cycle was classified at, because a rework can lower the header.
- `rulesets/niko/skills/niko/SKILL.md` Step 3b: the rework entry also records "the current complexity level". This is the header's value at rework time, not "the task's level": on a second rework, the header holds the outgoing cycle's level. Routing does not depend on this line.
- `rulesets/niko/skills/niko/references/level1/level1-workflow.md` Wrap-Up: checks `milestones.md` first, then whether `progress.md` records an earlier cycle classified above Level 1. If so, it prints "Run `/niko-archive` to archive the whole task".

The first cycle gated the Level 1 handoff on files in `reflection/`. CodeRabbit showed that a stale reflection from an earlier task met that test. The rework replaced it with the router's own rule, so the two steps agree in every state.

The router works on `progress.md` files written before this change. Complexity analysis already appends a "Classified ... as Level N" entry for each cycle, so no new record is needed. The Step 3b line is a backup for files where those entries are thin.

Preflight advisories taken: (1) the Step 3b wording above, and (2) the router names the routed value "the task's complexity level". Advisory 3 (a running-peak `**Task complexity:**` line) was declined, per the precision-strike steer.

## TESTING

Rule and skill wording is out of `always-tdd` scope, so no tests were owed. Verification:

- `make test` green in every phase: symlink check, README link check, 100 unittest cases.
- Traced both acceptance states from their real files. termeleon `ea8b52c` (classified Level 2, Level 2, Level 1) and inquirerjs-checkbox-search `1d65046` (Level 2, Level 1) both get the Wrap-Up handoff and route to the Level 2 archive.
- Rework traces: a plain Level 1 task with a stale reflection file gets the delete instructions. A Level 1 L4 sub-run gets the sub-run message. A Level 1 rework of a Level 1 task gets the delete instructions.
- Preflight: PASS WITH ADVISORY. QA: PASS on both cycles, run on Opus 5.5. The first preflight subagent, on Fable 5.1, failed with HTTP 429 (usage credits ran out) and wrote nothing; it was respawned on Opus 5.5.
- Archive gate: a rework starts only from a Complete task, and Level 2 and above are Complete only after Reflect. So when the handoff fires, `reflection-<task-id>.md` exists and the Level 2 and Level 3 archive prerequisite passes.
- After the first QA passed, Step 3b's code-formatted `**Complexity:**` was changed to plain words. The edit only removed formatting, so QA was not re-run.
- PR #134 has an approving review from `cursor`. CodeRabbit's other two claims were dismissed: the task level is recorded, and the `.summem/naps` deletions are SumMem nap merges, not lost notes.

## LESSONS LEARNED

- Write a field name in code format inside an instruction only when the agent should write that field. Agents copy literal `**Field:**` text into what they append, and steps that look the field up by name then find two matches.
- A handoff that sends the operator to another step should use that step's own test. When the two test different things, they agree only in normal states.
- In a cycle-by-cycle log, the record that matters may already exist. Here, each cycle's classification entry made routing on history possible with no new field.

## PROCESS IMPROVEMENTS

None. The plan held: three files, in the planned order. The one formatting risk was caught by QA, and the one logic gap by PR review. Both were fixed within the normal flow.

## TECHNICAL IMPROVEMENTS

- Split the field, as the issue suggests. The `progress.md` header would hold the task's level as a running maximum. The `tasks.md` header would hold the current cycle's level, and the roughly ten per-cycle readers would read that. The archive would route on one field, with no history to scan. This change does not block that design.
- Level 1 Wrap-Up restates the router's rule instead of pointing to it. If the router's rule changes, Wrap-Up must change with it, or the original bug comes back.

## NEXT STEPS

- Merge PR #134, then `chore(dev): ai-rizz sync` so the installed `.cursor/` and `.claude/` copies match.
- `level1-workflow.md` line 26 still says Level 1 tasks have no `/niko-archive`, while Wrap-Up can now point to it. Out of scope here.
- "The task's complexity level" means different things in the router, `complexity-analysis.md`, and `/niko` Step 3.
- The Level 4 capstone gap noted in issue #133 is still unverified.
