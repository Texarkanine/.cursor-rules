# Task: Fix L4 Sub-Run Completion Flow

* Task ID: issue-54
* Complexity: Level 2
* Type: Bug fix (multi-component)

When an L2/L3 sub-run completes as part of an L4 project, the reflect phase's "Next Steps" incorrectly directs the operator to `/niko-archive`. This breaks the L4 flow because `/niko-archive` deletes `milestones.md`. The correct next step is `/niko` re-entry, which checks off the completed milestone and routes to the next one.

Additionally, L1 sub-runs within L4 have no terminal "next step" guidance and no mechanism for re-entry detection. Between sub-runs, no ephemeral cleanup is defined.


## Test Plan (TDD)

### Behaviors to Verify

- **B1 (L2 reflect, L4 context)**: milestones.md exists → "Next Steps" says "Run `/niko` to continue to the next milestone"
- **B2 (L2 reflect, standalone)**: milestones.md absent → "Next Steps" says "Run `/niko-archive`" (unchanged behavior)
- **B3 (L3 reflect, L4 context)**: Same as B1
- **B4 (L3 reflect, standalone)**: Same as B2
- **B5 (L1 completion, L4 context)**: milestones.md exists → activeContext set to `L1 COMPLETE`, operator directed to "Run `/niko`"
- **B6 (L1 completion, standalone)**: milestones.md absent → current behavior (commit and done, no further guidance)
- **B7 (Re-entry, L2/L3 sub-run)**: milestones.md exists + activeContext shows `REFLECT COMPLETE` → check off milestone, clean sub-run state, classify next
- **B8 (Re-entry, L1 sub-run)**: milestones.md exists + activeContext shows `L1 COMPLETE` → check off milestone, clean sub-run state, classify next
- **B9 (Cleanup preserves L4 state)**: Between sub-runs, milestones.md, projectbrief.md, progress.md, and reflection/ are preserved
- **B10 (Cleanup removes sub-run state)**: Between sub-runs, tasks.md, activeContext.md, creative/, .qa-validation-status, .preflight-status are deleted

### Test Infrastructure

- Framework: **None** — this project consists entirely of `.mdc` rule files with no executable code or automated test framework.
- Verification approach: Structural review of each modified rule file against the behavior specifications above. Each behavior maps to a specific conditional block or instruction in the rule files that can be verified by reading the file.
- **⚠️ Flagged**: No automated test infrastructure exists. Verification is manual/structural. Operator should confirm this approach is acceptable.

### New test files: none


## Implementation Plan

### Step 1: L2 Reflect — Context-aware "Next Steps" (B1, B2)

- File: `rulesets/niko/niko/level2/level2-reflect.mdc`
- Changes: In Step 8 "Log Progress", replace the hardcoded "Next Steps" block with a conditional:
  - Add instruction before the output template: "Check whether `memory-bank/active/milestones.md` exists"
  - If milestones.md exists: `Run /niko to continue to the next milestone.`
  - If milestones.md absent: `Run /niko-archive to create the archive document and finalize the current project.`

### Step 2: L3 Reflect — Context-aware "Next Steps" (B3, B4)

- File: `rulesets/niko/niko/level3/level3-reflect.mdc`
- Changes: Same pattern as Step 1, applied to Step 7 "Log Progress"

### Step 3: L1 Workflow — L4-aware completion (B5, B6)

- File: `rulesets/niko/niko/level1/level1-workflow.mdc`
- Changes: Expand "Commit When Done" section to be L4-aware:
  - After the commit step, add: "Check whether `memory-bank/active/milestones.md` exists"
  - If milestones.md exists: update `activeContext.md` phase to `L1 COMPLETE`, then tell operator "Run `/niko` to continue to the next milestone." STOP and wait.
  - If milestones.md absent: "You're done!" (current behavior)

### Step 4: Complexity Analysis — Generalized re-entry detection (B7, B8)

- File: `rulesets/niko/niko/core/complexity-analysis.mdc`
- Changes to Step 1a text:
  - Replace "If REFLECT COMPLETE" with "If sub-run complete (activeContext phase is `REFLECT COMPLETE` or `L1 COMPLETE`)"
  - Update mermaid diagram: rename `RC2{"Reflect-complete?"}` to `RC2{"Sub-run<br>complete?"}`

### Step 5: Complexity Analysis — Ephemeral cleanup between sub-runs (B9, B10)

- File: `rulesets/niko/niko/core/complexity-analysis.mdc`
- Changes to Step 1a:
  - After "Check off that sub-run's milestone in `milestones.md`", add a new cleanup step:
    > **Clean sub-run state:** Delete `tasks.md`, `activeContext.md`, `creative/`, `.qa-validation-status`, `.preflight-status` from `memory-bank/active/`. **Preserve** `milestones.md`, `projectbrief.md`, `progress.md`, and `reflection/` — these are L4-scoped.
  - Update mermaid diagram to include cleanup node between CheckOff and AllDone/NextSub

### Step 6: L4 Workflow — Diagram label update

- File: `rulesets/niko/niko/level4/level4-workflow.mdc`
- Changes: Update the `SubRun` edge label from `"Sub-run reflect complete"` to `"Sub-run complete"` to accurately cover L1 sub-runs (which have no reflect phase)


## Technology Validation

No new technology — validation not required.


## Dependencies

- Each step is independent and can be implemented in any order
- All changes are to canonical sources in `rulesets/niko/` per the `agent-customization-locations.mdc` rule
- After implementation, `ai-rizz` sync will propagate changes to `.cursor/rules/`


## Challenges & Mitigations

- **No test infrastructure**: Verification is manual/structural review of rule file content. Mitigated by defining precise behaviors (B1-B10) that map 1:1 to conditional blocks in the rule files.
- **L1 COMPLETE as new convention**: Introducing a new terminal state for L1 within L4 context. Mitigated by keeping it isolated to the L1 workflow's completion section — standalone L1 behavior is unchanged.
- **Ephemeral cleanup correctness**: Deleting the wrong files would break L4 flow (too aggressive) or leave stale state (too conservative). Mitigated by explicitly listing both "delete" and "preserve" sets, cross-referenced against the L4 archive's prerequisites.
- **Defensive measure (out of scope)**: L2/L3 archive phases could detect milestones.md and refuse to run during L4 sub-runs. Not implementing now — the primary fix prevents operators from being directed to `/niko-archive` in the first place. Could be a future enhancement.


## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
