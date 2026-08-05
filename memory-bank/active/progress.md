# Progress

Rename the `visual-planning` skill to `illustrate-complexity` and rewrite it so it triggers on any explanation that needs an illustration, not only on planning. Update every reference to the old name. Add agentskills.io pointers to the authoring ruleset, including a new `skill-frontmatter.md` reference under `prompt-authoring`.

**Complexity:** Level 2

## 2026-08-05 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Traced the skill's git history and identified its retired siblings, `planning-execution` and `task-list-management`.
    - Confirmed that the authoring README and `prompt-authoring` already describe the skill as general illustration guidance, while the frontmatter does not.
    - Verified all four external URLs return 200.
    - Wrote `projectbrief.md`, `activeContext.md`, and this file.
* Decisions made
    - Level 2. The work is content edits to two skills in one subsystem. Design decisions are settled. Risk is low, and `make test` verifies the symlink and link invariants a rename can break.
    - Name: `illustrate-complexity`.
    - The agentskills.io pointer work is in scope, at both the README and the `references/` level.
    - No always-applied tripwire rule.
* Insights
    - The root cause is a description that outlived its context. When a skill's siblings are retired, its own framing needs re-deriving; nothing in the repo prompts that today.
    - TDD does not apply here. This is rule and skill prose, which `always-tdd.mdc` carves out. `make test` is the purpose-built gate for the layout invariants the rename touches.

## 2026-08-05 - PLAN - COMPLETE

* Work completed
    - Wrote the 12-step implementation plan to `tasks.md`, with a test plan, challenges, and a pre-mortem.
* Decisions made
    - Only four body areas may change: the opening, the chart-type escape hatch, the `## Planning Workflow` replacement, and the frontmatter. Everything else stays byte-identical, and step 12 diffs it to prove that.
* Insights
    - The pre-mortem's leading risk is scope creep, because a 164-line file invites a full rewrite. Naming the four permitted areas is the control.

## 2026-08-05 - PREFLIGHT - COMPLETE

* Work completed
    - Ran all seven preflight checks. Result: PASS with three plan amendments and one advisory taken in scope.
    - Verified `REUSE.toml` licenses by glob and `ai-rizz.skbd` lists directories only, so the rename touches neither.
* Decisions made
    - Split the test plan into "Committed Gates" and "One-Time Build Checks". The greps are one-shot acceptance checks and must never be committed as tests, because as persisted tests they would be change-detectors.
    - Constrained step 6: no use-block may prescribe a diagram type or a fixed order. `rules/architecture-docs/SKILL.md` line 46 rejects mandating one type. Type selection stays with the table.
    - Took the advisory in scope: `skill-frontmatter.md` gains two sentences on re-deriving a survivor's description after a skill is split or its siblings retired.
* Insights
    - The retired `## Planning Workflow` ritual ("start with a flowchart, then add...") directly contradicted `architecture-docs`. Deleting it resolves a live conflict rather than only removing stale framing.
