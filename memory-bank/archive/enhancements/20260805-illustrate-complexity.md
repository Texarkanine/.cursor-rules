---
task_id: illustrate-complexity
complexity_level: 2
date: 2026-08-05
status: completed
---

# TASK ARCHIVE: illustrate-complexity

## SUMMARY

Renamed the `visual-planning` skill to `illustrate-complexity` and rewrote its frontmatter plus four body areas, so it triggers whenever an explanation needs an illustration rather than only on planning. Repointed every reference to the old name. Added agentskills.io pointers to the authoring ruleset, including a new `rules/prompt-authoring/references/skill-frontmatter.md`.

The skill was the surviving Phase 1 of `planning-execution`, which superseded `task-list-management` in `9fc8675` (#15). Both siblings were deleted in `f6fc916` (#89), and nothing re-derived the survivor's description, so it still said "Apply when planning non-trivial work" a year later. The human-facing READMEs and `prompt-authoring/references/workflow-prompts.md` had already moved on and described the skill as general illustration guidance. Only the machine-facing `description` still said planning.

PR: [#105](https://github.com/Texarkanine/.cursor-rules/pull/105) - `feat(authoring)!: rename visual-planning to illustrate-complexity and broaden its trigger`.

## REQUIREMENTS

All eleven requirements were delivered.

1. Rename `rules/visual-planning/` to `rules/illustrate-complexity/`.
2. Replace the frontmatter description: ~300 characters, imperative, covering docs, READMEs, design notes, prompts, plans, and chat answers, and excluding numeric charting.
3. Open the body on the general case, not on planning.
4. Move the "more than a paragraph of *and then*" test near the top of the body.
5. Keep the emoji library unchanged. Operator rationale: an agent reaches for a given emoji only when that concept is present, so the library gives one design language across every chart type.
6. Add one sentence and a link to <https://mermaid.js.org/intro/syntax-reference.html> for the chart types the table omits.
7. Replace `## Planning Workflow` with a section covering three uses - planning, documenting, and answering a question - stating that chat diagrams stay small because most chat UIs render them badly, and that a large diagram is correct on a web page because Mermaid gives the reader a lightbox.
8. Update every reference to the old name: both ruleset symlinks, both ruleset READMEs, and `memory-bank/techContext.md`.
9. Link <https://agentskills.io/skill-creation/best-practices> from `rulesets/authoring/README.md`.
10. Create `rules/prompt-authoring/references/skill-frontmatter.md` covering what the repo omits: `description` drives triggering, the character limit, and when to split content into `references/`.
11. Add a one-line conditional pointer to that reference from `rules/prompt-authoring/SKILL.md`.

Constraints held: canonical sources only, no change wider than a requirement needed, archive files keep the old name, and no always-applied tripwire rule - the operator rejected that permanently.

## IMPLEMENTATION

Twelve steps, eight files, no new dependencies. Every step landed on the first try.

Files created or modified:

- `rules/illustrate-complexity/SKILL.md` - renamed from `rules/visual-planning/SKILL.md`, four hunks.
- `rulesets/authoring/skills/illustrate-complexity` and `rulesets/niko/skills/illustrate-complexity` - symlinks replacing the `visual-planning` links.
- `rulesets/authoring/README.md` and `rulesets/niko/README.md`.
- `memory-bank/techContext.md`.
- `rules/prompt-authoring/references/skill-frontmatter.md` - new.
- `rules/prompt-authoring/SKILL.md`.

Key decisions:

- The new description is 306 characters and keeps both narrowing devices: the "structure, flow, or relationships" subject qualifier and the numeric-charting exclusion. Broadening to "any explanation" was rejected as an over-triggering risk.
- The replacement section is titled `## Where the Diagram Will Be Read`. Preflight found that `rules/architecture-docs/SKILL.md` line 46 explicitly rejects mandating one diagram type and warns that doing so teaches mimicry, which the old `## Planning Workflow` ritual did. So the new section prescribes no type and no ordering; type selection stays with the table.
- Planning appears as one peer among three uses, never first, and the section is not titled as a workflow.
- `skill-frontmatter.md` states the durable facts and defers every number to the upstream specification, following the `techContext.mdc` convention of pointing at values rather than copying them. Preflight took an advisory in scope and added two sentences on re-deriving a survivor's description when a skill is split or its siblings are retired - the root cause of this task.

Deviations from plan, all deliberate:

- Moved the `illustrate-complexity` entry in `rulesets/authoring/README.md` to keep the section list alphabetical, where the plan said only to rename it in place.
- Dropped a planned sentence about separating the map from the driving instructions. `prompt-authoring/references/workflow-prompts.md` already states it, and `prompt-authoring` forbids restating a sibling.
- Restored a trailing newline in `rulesets/authoring/README.md` that removing the old trailing section had stripped.

Post-reflect operator tweaks (`57e4cad`, `78a4780`): `skill-frontmatter.md` lost a redundant opening clause and gained "refactored, reworked" to the list of shape changes; in the skill, syntax rule 5 became advisory rather than mandatory ("consider if it should be split... sometimes you really do need a big diagram"), and the plans-and-design-notes block gained "High detail and completeness are paramount." The rule 5 edit means the syntax block is no longer byte-identical to the pre-rename file, by operator choice after the build gate had proved it untouched.

## TESTING

Rule and skill prose, which `always-tdd.mdc` carves out of TDD as user-facing wording. No test files were added, and none should have been: a test asserting on this content could only go red when someone deliberately edits the artifact, which makes it a change-detector rather than a test.

Committed gates, which already exist and run in CI, go red when a link or symlink actually breaks for a consumer:

- `make test-symlinks` (`scripts/check-ruleset-symlinks.sh`) - both ruleset symlinks resolve to `rules/illustrate-complexity`. Run immediately after step 2 rather than at the end, because the symlink swap was the one predicted challenge.
- `make test-readme-links` (`scripts/check-ruleset-readme-links.sh`) - every internal link in both ruleset READMEs resolves.

One-time build checks, deliberately not committed: no `visual-planning` reference remains under `rules/` or `rulesets/`; `techContext.md` names the new skill; the description measures 306 characters; no `Planning Workflow` heading survives; and a diff against the pre-rename file shows exactly four hunks, proving the emoji block, the five syntax rules, and all five diagram examples were untouched.

Preflight: PASS, with three plan amendments and one advisory taken in scope. QA: PASS, with one DRY fix applied in place - the artifact list appeared in the description, the body opening, and the destinations section, and only the description has to carry it, because that is what an agent reads before deciding to load the skill.

## LESSONS LEARNED

- Any future diagram guidance in this repo must not prescribe a diagram type or a fixed order. `rules/architecture-docs/SKILL.md` line 46 rejects that directly, and the retired `## Planning Workflow` had been contradicting it. Deleting that section resolved a live conflict between two skills in one ruleset, not merely stale framing.
- Removing a trailing section from a Markdown file eats its EOF newline, and neither `make test` target catches it. Commit `a3a5437` once fixed EOF newlines repo-wide, so this is a recurring hazard.
- `git mv` will not rename a symlink; it keeps the old link name. Delete and recreate instead, then verify immediately.
- When a skill's siblings are retired, the survivor keeps its old framing silently. Human-facing docs drifting *ahead* of a machine-facing field is a detectable signal worth looking for elsewhere in the repo.

## PROCESS IMPROVEMENTS

- Naming the areas that must *not* change, then diffing them at the end, is a cheap and durable control against scope creep - cheaper than reviewing everything that did change. It is what kept a 164-line file from becoming a full rewrite, and it earned its place: it proved the untouched blocks rather than asserting them.
- Splitting a test plan into "committed gates" and "one-time build checks" is worth doing explicitly whenever the work is prose. It keeps acceptance greps from being mistaken for tests and committed as change-detectors.

## TECHNICAL IMPROVEMENTS

- Persistent reconciliation: `productContext` skipped and `systemPatterns` skipped, because it describes the skill-plus-symlink pattern generically and never named this skill. `techContext` gained a `## Skill Format` section pointing at the Agent Skills specification, which this task made an acknowledged upstream authority for artifacts this repo produces. The `Diagrams` line in `techContext` was fixed during build.
- Open gap, deliberately not closed: nothing enforces re-deriving a survivor's description after a retirement. `skill-frontmatter.md` states the rule, but the repo has no formal skill-retirement path where such a step could live - retirement is just a PR. Not worth building process for until a second instance appears.
- The generated `.cursor/` and `.claude/` trees still name the old skill. They lag by design and are re-synced in a separate `chore(dev): ai-rizz sync` commit after push, because `ai-rizz` reads the git remote.

## NEXT STEPS

- Merge PR [#105](https://github.com/Texarkanine/.cursor-rules/pull/105), then regenerate `.cursor/` and `.claude/` in a follow-up sync commit.
- The rename is a clean break for anyone who installed `visual-planning` through `ai-rizz`. The PR title carries the `!` marker; no compatibility shim was added, per the repo's clean-break default.
