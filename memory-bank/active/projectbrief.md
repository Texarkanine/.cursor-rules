# Project Brief

## User Story

As an operator running a Level 4 Niko task, I want `/niko-preflight` to judge the L4 design (milestone coverage, order, handoff, and judgeable done) rather than each one-line milestone as an L2/L3 implementation plan, so that a valid L4 plan is not a guaranteed blocking FAIL and so that sub-run TDD and file ownership stay in the sub-run where those plans are actually written.

## Use-Case(s)

### Use-Case 1

An L4 plan writes `memory-bank/active/milestones.md` as a one-line checklist (as `milestones.mdc` requires). Preflight loads that list, judges L4-altitude design, and does not FAIL blocking for missing numbered test-first steps or file-level paths on those one-liners.

### Use-Case 2

An L2 or L3 implementation plan in `tasks.md` is still judged with the existing TDD Plan Encoding and completeness-of-steps checks. This work does not relax that bar.

### Use-Case 3

A later worker picks up an unchecked milestone. The L4 surface has enough reference to the intended work (existing ticket if one exists), a judgeable definition of done, and the critical invariants or risks that must not be lost. Persistent memory-bank files hold most of the requirements; `milestones.md` is sequencing plus enough to understand the document.

### Use-Case 4

Before implementation, the operator reviews every viable mechanism (the three they named, plus any others discovered) with arguments for and against, risks and rewards, and chooses. Implementation follows that choice.

## Requirements

1. Fix https://github.com/Texarkanine/.cursor-rules/issues/122: L4 preflight must not treat each `milestones.md` checkbox as a full L2/L3 implementation plan.
2. Investigate and present mechanism options (separate skill, branched instructions inside preflight, different L4 routing, and any others discovered) with for/against, risks, and rewards. Operator chooses before implementation, regardless of complexity level.
3. When `memory-bank/active/milestones.md` exists and complexity is Level 4, preflight judges L4 design, not sub-run implementation plans. Those plans do not exist yet; they are written when `/niko` classifies the next unchecked milestone.
4. L4 checks include: all required milestones present (the set covers the brief); ordered correctly against interdependencies (execution-order DAG; skippable when the DAG is a straight line); each milestone has sufficient link or reference to the task description; each has a judgeable definition of done; each has critical invariants or risks spelled out.
5. Reuse an existing ticket (GitHub Issues, JIRA, etc.) when one exists as the task-description reference. Do not create tickets.
6. Discover what else an L4 milestone must have for an L4 run to succeed from the L4 workflow; do not invent extra fields up front.
7. Canonical edits under `rulesets/` only. The generated `.cursor/` copy of the skill is synced later, not in this task.

## Constraints

1. Do not change `milestones.mdc` to allow implementation plans (sub-bullets, notes, TDD steps, file lists) in the L4 checklist.
2. Do not relax TDD encoding or completeness-of-steps for actual L2/L3 `tasks.md` plans.
3. `milestones.md` stays sequencing plus enough detail to understand the document. Persistent files carry most of the requirements and definition of done.
4. Preflight remains judge-and-report: four status strings, no Handle Results, meanings only in `preflight-status.mdc`.
5. Do not create tickets in the operator's tracker.

## Acceptance Criteria

1. An L4 plan whose milestones are independently deliverable one-liners in the required checklist format is not a blocking FAIL solely for lacking numbered test-first substeps or concrete file paths on those lines.
2. L2/L3 preflight still FAILs blocking when an implementable unit has no numbered test-before-code steps.
3. The operator has reviewed a written options analysis (their three mechanisms plus any others found) and chosen one before implementation proceeds.
4. The chosen mechanism loads `milestones.md` for L4 (not the L4 `tasks.md` stub as the design surface) and judges coverage, dependency order, task-description references, judgeable done, and critical invariants or risks.
5. Existing tickets are referenced when present; no ticket is created by this workflow.
6. L4 workflow text that says preflight "validates the milestone list" states the L4 altitude of that validation.
