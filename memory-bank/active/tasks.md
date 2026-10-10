# Task: archive-whole-task (rework: gate the Level 1 handoff on the router's rule)

* Task ID: archive-whole-task
* Complexity: Level 1
* Type: bug fix

## Fix

- **What broke:** Level 1 Wrap-Up pointed to `/niko-archive` whenever `memory-bank/active/reflection/` had files. A reflection left over from an earlier task met that test, so a plain Level 1 task could be sent to an archive that routes at Level 1 and cannot run. The operator then never saw the delete instructions.
- **Why:** the handoff and the `/niko-archive` router tested different things. They agree only when `active/` is in a normal state.
- **What changed:** the handoff now uses the router's rule. It fires when `progress.md` records an earlier cycle classified above Level 1. The `milestones.md` check still runs first.
- **Files:** `rulesets/niko/skills/niko/references/level1/level1-workflow.md` (Wrap-Up item 3 and its branch label)

## Verification

No tests: rule wording is out of `always-tdd` scope.

- `make test` green: symlink and README link checks, 100 unittest cases
- termeleon `ea8b52c` (cycles classified Level 2, Level 2, Level 1; header Level 1): handoff fires
- inquirerjs-checkbox-search `1d65046` (Level 2, Level 1; header Level 1): handoff fires
- This task (Level 2, then this Level 1 rework): handoff fires; the router then picks the Level 2 archive
- Plain Level 1 task, with or without a stale reflection file: one Level 1 cycle, so the delete instructions print
- Level 1 L4 sub-run: the `milestones.md` check runs first, so the sub-run message prints

## QA Results

PASS (2026-10-09). Semantic review of the rework edit (+2/-2 in `level1-workflow.md`) against the rework requirement and CodeRabbit r4235005318. `make test` is green: symlink and README link checks pass, and 100 unittest cases pass. Wrap-Up now gives the same answer as the `/niko-archive` router in every state. Re-traced: both acceptance states get the handoff; a plain Level 1 task with a stale reflection file gets the delete instructions; an L4 sub-run gets the sub-run message. When the handoff fires, the earlier cycle reached REFLECT COMPLETE, so the Level 2 and Level 3 archive reflection gate still passes. No KISS, DRY, YAGNI, completeness, regression, integrity, or documentation violations.

Two non-blocking advisories are in `memory-bank/active/.qa-validation-status`:

1. Wrap-Up restates the router's rule instead of pointing to it. If the router's rule changes, this condition must change with it.
2. Carried, out of scope: level1-workflow.md line 26 still says Level 1 has no `/niko-archive`.
