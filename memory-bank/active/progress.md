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
