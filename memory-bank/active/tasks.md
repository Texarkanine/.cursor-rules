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
- **B5 (L1 completion, L4 context)**: milestones.md exists → operator directed to "Run `/niko` to continue to the next milestone"
- **B6 (L1 completion, standalone)**: milestones.md absent → current behavior (commit and done)
- **B7 (Re-entry, L2/L3 sub-run)**: milestones.md exists + activeContext shows REFLECT COMPLETE → check off milestone, clean sub-run state, classify next
- **B8 (Re-entry, L1 sub-run)**: milestones.md exists + .qa-validation-status PASS + progress.md shows Level 1 → check off milestone, clean sub-run state, classify next
- **B9 (Cleanup preserves L4 state)**: Between sub-runs, milestones.md, projectbrief.md, progress.md, and reflection/ are preserved
- **B10 (Cleanup removes sub-run state)**: Between sub-runs, tasks.md, activeContext.md, creative/, .qa-validation-status, .preflight-status are deleted

### Test Infrastructure

- Framework: **None** — this project consists entirely of `.mdc` rule files with no executable code or automated test framework.
- Verification approach: Operator reviews each modified rule file against the behavior specifications above.


## Implementation Plan

### Step 1: L2 Reflect — Context-aware "Next Steps"

- File: `rulesets/niko/niko/level2/level2-reflect.mdc`
- Changes: In Step 8 "Log Progress", replace the hardcoded "Next Steps" block with a conditional:
  - Check whether `memory-bank/active/milestones.md` exists
  - If milestones.md exists: `Run /niko to continue to the next milestone.`
  - If milestones.md absent: `Run /niko-archive to create the archive document and finalize the current project.`
- Behaviors: B1, B2

### Step 2: L3 Reflect — Context-aware "Next Steps"

- File: `rulesets/niko/niko/level3/level3-reflect.mdc`
- Changes: Same pattern as Step 1, applied to Step 7 "Log Progress"
- Behaviors: B3, B4

### Step 3: L1 Workflow — L4-aware completion guidance

- File: `rulesets/niko/niko/level1/level1-workflow.mdc`
- Changes: In the "Commit When Done" section, after the commit instruction:
  - If `milestones.md` exists, this is an L4 sub-run: inform the operator to run `/niko` to continue. STOP and wait.
  - If no milestones.md: current behavior (done, no further guidance)
- No new state markers — detection relies on naturally existing artifacts.
- Behaviors: B5, B6

### Step 4: Complexity Analysis — Generalized re-entry detection

- File: `rulesets/niko/niko/core/complexity-analysis.mdc`
- Changes to Step 1a:
  - Widen the "sub-run complete?" check from just REFLECT COMPLETE to also recognize L1 completion: `.qa-validation-status` shows PASS and `progress.md` shows Level 1 complexity.
  - Update mermaid diagram to reflect the widened check.
- No artificial markers — inferred from naturally existing state.
- Behaviors: B7, B8

### Step 5: Complexity Analysis — Ephemeral cleanup between sub-runs

- File: `rulesets/niko/niko/core/complexity-analysis.mdc`
- Changes to Step 1a, after checking off the completed milestone:
  - **Delete** (sub-run scoped): `tasks.md`, `activeContext.md`, `creative/`, `.qa-validation-status`, `.preflight-status`
  - **Preserve** (L4 scoped): `milestones.md`, `projectbrief.md`, `progress.md`, `reflection/`
- Update mermaid diagram to include cleanup node.
- Behaviors: B9, B10

### Step 6: L4 Workflow — Diagram label update

- File: `rulesets/niko/niko/level4/level4-workflow.mdc`
- Changes: Update the SubRun edge label from "Sub-run reflect complete" to "Sub-run complete" to cover L1 sub-runs (which have no reflect phase)


## Technology Validation

No new technology — validation not required.


## Dependencies

- Each step is independent and can be implemented in any order
- All changes are to canonical sources in `rulesets/niko/` per the `agent-customization-locations.mdc` rule


## Challenges & Mitigations

- **No test infrastructure**: Verification is operator review of rule file content. Precise behaviors (B1-B10) defined for traceability.
- **L1 completion detection without markers**: Relies on naturally existing state (`.qa-validation-status` + Level 1 in `progress.md`). These artifacts are guaranteed to exist after a successful L1 sub-run per existing workflow rules.
- **Ephemeral cleanup correctness**: Explicitly listing both "delete" and "preserve" sets, cross-referenced against the L4 capstone archive's prerequisites (which reads `reflection/`).


## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
