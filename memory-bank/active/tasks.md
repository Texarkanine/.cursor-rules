# Task: archive-whole-task

* Task ID: archive-whole-task
* Complexity: Level 2
* Type: bug fix

After a rework is classified lower than the task, a plain `/niko-archive` archives only the last cycle at the lowered level ([#133](https://github.com/Texarkanine/.cursor-rules/issues/133)). Fix: the archive router covers every cycle `progress.md` records and routes on the highest level any cycle was classified at; `/niko` Step 3b records the task's level in the rework entry; a Level 1 rework of a larger task points to `/niko-archive` instead of the delete instructions. Classification and the rework flow do not change.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior. All three edits are skill wording (out of scope under `always-tdd`, "What TDD Governs").

Verification without tests:

- `make test` stays green (symlinks, README links, unittest).
- Trace: the edited router read against termeleon `ea8b52c` `progress.md` (header Level 1; entries classify Level 2, Level 2, Level 1) → Level 2 archive, `complexity_level: 2`, covers all three cycles.
- Trace: same for inquirerjs-checkbox-search `1d65046` `progress.md` (header Level 1; entries classify Level 2, Level 1) → Level 2 archive, `complexity_level: 2`.
- Trace: Level 3 task, Level 2 rework, Level 1 rework → the Step 3b lines record Level 3 and Level 2, header Level 1 → Level 3 archive (reads `creative/`).
- Trace: Level 1 Wrap-Up with `reflection/` files and no `milestones.md` → prints "Run `/niko-archive`"; with neither → delete instructions as before; with `milestones.md` (L4 sub-run, which keeps `reflection/`) → L4 sub-run message as before.

### Test Infrastructure

- Framework: `make test` (shell layout checks + stdlib `unittest`)
- Test location: `scripts/`, `tests/`
- Conventions: n/a for this task
- New test files: none

## Implementation Plan

### 1. Archive covers the whole task and routes on its highest level — prose/policy

- Files: `rulesets/niko/skills/niko-archive/SKILL.md`
- No tests: prose/policy artifact

1. Step 1: after the read list, add one sentence: the task is every cycle `progress.md` records, reworks included; `tasks.md` and `activeContext.md` hold only the latest cycle.
2. Step 2: add one sentence: the task's complexity level is the highest level any cycle was classified at; a rework can lower the `**Complexity:**` header, so the header alone is not enough. Keep the existing STOP paragraph. Step 3 stays as is (it loads the workflow for that level; Level 1 has no Archive mapping, as today).

### 2. Rework entry records the task's level — prose/policy

- Files: `rulesets/niko/skills/niko/SKILL.md` (Step 3b, item 1)
- No tests: prose/policy artifact

1. Item 1 becomes: append rework initiation, the operator's feedback, and the task's current `**Complexity:**` level to `progress.md`.

### 3. Level 1 rework of a larger task points to the archive — prose/policy

- Files: `rulesets/niko/skills/niko/references/level1/level1-workflow.md` (Wrap-Up, item 3)
- No tests: prose/policy artifact

1. Lead line: check whether `milestones.md` exists, then whether `memory-bank/active/reflection/` has files.
2. Insert a branch after the L4 sub-run branch: `reflection/` has files (Level 1 rework of a larger task) → print "✅ **Level 1 rework complete.**" and "Run `/niko-archive` to archive the whole task.", then STOP.
3. Relabel the last branch from "milestones.md does not exist" to "Neither"; its content stays.

## Technology Validation

No new technology - validation not required

## Dependencies

- None. The generated `.cursor/` and `.claude/` trees lag until a later `chore(dev): ai-rizz sync`; edit only `rulesets/`.

## Challenges & Mitigations

- "Highest level recorded" could match a level that is only mentioned (e.g. "Level 1 skips plan" in termeleon/inquirer entries, or "considered Level 3"): word it as the level a cycle was *classified at*, not any level the text mentions.
- An L4 sub-run that is Level 1 keeps `reflection/` from earlier milestones: the `milestones.md` check stays first, so that run still gets the L4 sub-run message.
- `complexity-analysis.md` still calls the header "the system of record" for the task's level, so it seems to contradict the router. The archive agent reads only the router, so the two never meet at runtime. The issue keeps classification unchanged, so this task leaves that text as is.

## Pre-Mortem

- The edit grows past the issue (README, archives format, classification text, level archives): the plan names exactly three files and one or two sentences each; anything else is out of scope unless a trace fails.
- The acceptance states predate the Step 3b line, so routing on that line alone would still say Level 1: the router reads every cycle's classification, and the traces use the real pre-change files.
- The Level 2 archive writes `complexity_level` from the header (1) even though it was routed at Level 2: the router calls the routed value "the task's complexity level", the same name as the archive field; the trace checks that.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
