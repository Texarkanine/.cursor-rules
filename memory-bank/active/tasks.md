# Task: Fix L4 Sub-Run Completion Flow — Rework: Option B

* Task ID: issue-54
* Complexity: Level 2
* Type: Refactor (separation of concerns)

Move L4 re-entry state management and existing-work-check from `complexity-analysis.mdc` to `/niko` SKILL.md. `/niko` becomes the state router; `complexity-analysis.mdc` becomes a pure classifier.


## Test Plan (TDD)

### Behaviors to Verify

Behaviors B1-B6 (reflect/L1 "Next Steps" guidance) are already implemented and unaffected.

- **B7 (L4 re-entry, L2/L3 sub-run)**: milestones.md exists + REFLECT COMPLETE → /niko checks off milestone, cleans sub-run state, routes to classification
- **B8 (L4 re-entry, L1 sub-run)**: milestones.md exists + Level 1 + QA PASS → same as B7
- **B9 (Cleanup preserves L4 state)**: milestones.md, projectbrief.md, progress.md, reflection/ preserved
- **B10 (Cleanup removes sub-run state)**: tasks.md, activeContext.md, creative/, .qa-validation-status, .preflight-status deleted
- **B11 (L4 all done)**: milestones.md exists + all milestones checked → /niko directs to /niko-archive (capstone)
- **B12 (L4 sub-run in-progress)**: milestones.md exists + sub-run NOT complete → /niko resumes sub-run
- **B13 (Standalone complete)**: no milestones + all ephemeral files + task complete (REFLECT COMPLETE or L1 + QA PASS) → rework or archive
- **B14 (Standalone in-progress, new input)**: no milestones + all ephemeral files + NOT complete + user input → warn
- **B15 (Standalone in-progress, no input)**: no milestones + all ephemeral files + NOT complete + no user input → resume workflow
- **B16 (Fresh task)**: no milestones + missing ephemeral files + user input → straight to classification
- **B17 (No input, no work)**: no milestones + missing ephemeral files + no user input → done
- **B18 (Classification target — L4)**: milestones.md exists when classification loads → classify first unchecked milestone, not user input
- **B19 (Classification target — standalone)**: no milestones.md → classify user input
- **B20 (Normal one-off fast path)**: no milestones, no ephemeral files, user input → /niko → classification → decision tree (no L4 branching touched)

### Test Infrastructure

- Framework: **None** — operator verification against behavior specifications.


## Implementation Plan

### Step 1: /niko SKILL.md — Full state routing [DONE]

- File: `rulesets/niko/skills/niko/SKILL.md`
- Replace the current Step 2 "Resume Check (No User Input)" with a comprehensive Step 2 "State Routing" that always runs (regardless of user input). Move the following logic here from complexity-analysis:
  - L4 milestone transition (check off, cleanup, capstone-or-classify)
  - L4 sub-run resume
  - Existing work check (with widened "task complete?" — REFLECT COMPLETE or L1 + QA PASS)
  - Rework flow
  - Fresh task / no-input routing
- New mermaid diagram showing the full state machine with subgraphs
- Prose describes each node's body (no conditionals — diagram handles branching)
- Step 3 becomes: load complexity-analysis.mdc
- Behaviors: B7-B17, B20

### Step 2: complexity-analysis.mdc — Pure classifier [DONE]

- File: `rulesets/niko/niko/core/complexity-analysis.mdc`
- Remove the entire Step 1 "Re-entry Check" (both subgraphs, all 1a/1b prose)
- Replace with a lightweight Step 1 "Classification Target":
  - If milestones.md exists, read it — the classification target is the first unchecked milestone description
  - Otherwise, the classification target is the user's task input
- Renumber remaining steps (Decision Tree becomes Step 2, etc.)
- Everything from the Decision Tree onward is unchanged
- Behaviors: B18, B19

### Step 3: milestones.mdc — Update cross-references (preflight finding) [DONE]

- File: `rulesets/niko/niko/memory-bank/active/milestones.mdc`
- Update lifecycle table: 3 rows reference `complexity-analysis.mdc Step 1` → update to reference `/niko` state routing
- Update prose: lines 9 and 52 reference "complexity analysis" as the consumer of the milestones.md signal → update to "/niko"

### Step 4: level4-workflow.mdc — Diagram attribution update [DONE]

- File: `rulesets/niko/niko/level4/level4-workflow.mdc`
- The diagram currently labels `Start(("Complexity Analysis"))` and shows milestone management (checkoff, cleanup, classify) flowing from that entry point. With Option B, milestone management happens in `/niko` before complexity-analysis is invoked.
- Update the diagram's entry label and subgraph boundaries to reflect the new split: `/niko` handles state routing and milestone management, complexity-analysis handles classification only.
- Update any corresponding prose below the diagram if needed.


## Technology Validation

No new technology — validation not required.


## Dependencies

- Step 1 and Step 2 should be implemented together (the logic moves from one file to the other)
- L2/L3 reflect and L1 workflow changes from the original build are already in place and unaffected


## Challenges & Mitigations

- **/niko SKILL.md grows significantly**: Mitigated by the diagram-carries-branching pattern — the diagram IS the state machine, prose describes node bodies. Structure matches what /niko already does as an entry point.
- **Existing-work-check widened criteria**: The "task complete?" check now uses REFLECT COMPLETE or L1 + QA PASS everywhere (not just L4 path). This correctly detects standalone L1 completion, which was previously a gap.
- **Step 2 fires with user input**: The existing work check must catch work-in-flight even when the user provides new task input. The current "skip Step 2 if user input" behavior is removed.


## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight
- [x] Build
- [x] QA
