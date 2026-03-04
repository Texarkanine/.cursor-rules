# Task: Niko Ruleset Enhancements

* Task ID: niko-ruleset-enhancements
* Complexity: Level 2
* Type: Simple Enhancement (3 targeted rule-text changes)

Three targeted improvements to the Niko ruleset in `rulesets/niko/`. Each item is committed separately for clean PR review.

## Test Plan (TDD)

### Behaviors to Verify

This task modifies `.mdc` rule files (AI instruction text). There is no executable code and no test infrastructure for rule files. Verification is manual:

- [Item 1 - QA doc check]: QA rule includes a documentation-completeness constraint → agent will check docs during QA
- [Item 1 - Plan doc step]: L2/L3/L4 plan rules include documentation updates as a planning step → agent will plan doc changes
- [Item 2 - L1 wrap-up]: L1 workflow includes cleanup guidance → user knows to clean `memory-bank/active/` post-PR
- [Item 3 - Lazy refs]: All bare-filename `.mdc` references in rule files are replaced with full installed paths → grep confirms zero lazy refs remain

### Test Infrastructure

- Framework: N/A (pure documentation/rule-text changes)
- Test location: N/A
- Conventions: N/A
- New test files: none
- Verification method: `rg` (ripgrep) to confirm no lazy references remain; manual review of changed files

## Implementation Plan

### Step 1: QA & Plan Documentation Enforcement (Item 1)

**1a. Add documentation check to QA** (`rulesets/niko/skills/niko-qa/SKILL.md`)
- In Step 2, item 2 (the review constraints list), add a new **Documentation** constraint after **Integrity**:
  - Verify that any project documentation (README files, doc comments, memory bank persistent files, configuration docs) affected by the code changes was updated alongside those changes. Treat missing documentation updates as an incomplete implementation — same severity as a missing feature.

**1b. Add documentation planning to L2 Plan** (`rulesets/niko/niko/level2/level2-plan.mdc`)
- In Step 5 (Create Implementation Plan), add a bullet requiring the plan to include documentation update steps for any docs affected by the implementation.

**1c. Add documentation planning to L3 Plan** (`rulesets/niko/niko/level3/level3-plan.mdc`)
- In Step 7 (Create Implementation Plan), add the same documentation bullet.

**1d. Add documentation planning to L4 Plan** (`rulesets/niko/niko/level4/level4-plan.mdc`)
- In Step 3 (Generate Milestone List), add a note that milestones which change documented behavior should include documentation updates in scope.

**Commit**: `feat: enforce documentation updates in QA and Plan phases`

### Step 2: Level 1 Wrap-Up Guidance (Item 2)

**Opinion & Rationale**: Add a brief "Cleanup" note to L1's existing "Commit When Done" section in the L1 workflow. This reminds the user to delete `memory-bank/active/` after the PR is merged (or before opening, at their discretion). Reasoning:
- L1 is deliberately lightweight; adding an archive phase contradicts its design
- Auto-deleting then committing again adds noise to the PR and loses the "work shown"
- A simple reminder is proportional to L1's scope — users who know the system will already do this, and newcomers get the nudge they need

**File**: `rulesets/niko/niko/level1/level1-workflow.mdc`
- Expand the "Commit When Done" section to include a cleanup note telling the user to delete `memory-bank/active/` and commit when they're satisfied with the work (e.g., after PR merge).

**Commit**: `docs: add memory-bank cleanup guidance to L1 workflow`

### Step 3: Fix Lazy Internal Rule References (Item 3)

**3a. Fix `rulesets/niko/niko/memory-bank/active/milestones.mdc`** (lifecycle table, lines 46-50):
- `level4-plan.mdc` → `.cursor/rules/shared/niko/level4/level4-plan.mdc`
- `complexity-analysis.mdc` (3 occurrences) → `.cursor/rules/shared/niko/core/complexity-analysis.mdc`
- `level4-archive.mdc` → `.cursor/rules/shared/niko/level4/level4-archive.mdc`

**3b. Fix `rulesets/niko/niko/level4/level4-plan.mdc`** (lines 26, 36, 46):
- Line 26: `milestones.mdc` → `.cursor/rules/shared/niko/memory-bank/active/milestones.mdc`
- Line 36: `` `complexity-analysis.mdc` `` → `` `.cursor/rules/shared/niko/core/complexity-analysis.mdc` ``
- Line 46: `milestones.mdc` → `.cursor/rules/shared/niko/memory-bank/active/milestones.mdc`

**Note**: `rulesets/niko/niko/memory-bank/active/activeContext.mdc` line 54 references `common-fixes.mdc` but this is inside an *example block* showing past context text, not an actual rule reference. Leave as-is.

**Commit**: `fix: expand lazy rule path references to full installed paths`

## Technology Validation

No new technology - validation not required.

## Dependencies

- None. All changes are independent text edits.

## Challenges & Mitigations

- **Table formatting in milestones.mdc**: The lifecycle table uses backtick-wrapped filenames in table cells. Must preserve table alignment and markdown rendering after expanding to longer paths. Mitigation: verify table renders correctly after edit.
- **Wording consistency**: New plan/QA text must match the tone and style of surrounding constraints. Mitigation: model phrasing after existing constraints in the same lists.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
