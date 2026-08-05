---
task_id: illustrate-complexity
date: 2026-08-05
complexity_level: 2
---

# Reflection: illustrate-complexity

## Summary

Renamed `visual-planning` to `illustrate-complexity` and rewrote its frontmatter and four body areas so it triggers on any explanation that needs an illustration, not only on planning. Added agentskills.io pointers to the authoring ruleset, including a new `skill-frontmatter.md` reference. Delivered to plan; QA found one duplication and nothing substantive.

## Requirements vs Outcome

All eleven requirements delivered. Two changes beyond the original plan, both deliberate:

- Preflight added two sentences to `skill-frontmatter.md` on re-deriving a survivor's description after a skill is split or its siblings retired. That is the root cause of this task, and nothing in the repo prompted the check.
- Build dropped a planned sentence about separating the map from the driving instructions, because `prompt-authoring/references/workflow-prompts.md` already states it and `prompt-authoring` forbids restating a sibling.

Nothing was descoped. The operator rejected the always-applied tripwire rule before planning, so it was never in scope.

## Plan Accuracy

The file list and step sequence were exactly right; no step needed reordering or splitting. The one predicted challenge that materialized was the symlink rename, and the mitigation worked: `git mv` will not rename a symlink, so both were deleted and recreated with an immediate `make test-symlinks`.

Two surprises came from outside the challenge list. First, preflight found that `rules/architecture-docs/SKILL.md` explicitly rejects mandating one diagram type, which the `## Planning Workflow` section did — so the deletion resolved a live contradiction between two skills in one ruleset, not merely stale framing. Second, removing that trailing section stripped the file's EOF newline in `rulesets/authoring/README.md`, which no challenge anticipated and no committed gate checks.

## Build & QA Observations

Build was clean and fast; every step landed first try. The step 12 byte-identical diff was the most valuable part of the plan: it *proved* the emoji block, the five syntax rules, and all five diagram examples were untouched, rather than asserting it. That is the control that kept a 164-line file from turning into a full rewrite.

QA caught one real issue — the artifact list appeared three times, in the description, the body opening, and the destinations section — and fixed it in place. Only the description has to carry that list, because it is the one an agent reads before deciding to load the skill.

## Insights

### Technical

- Any future diagram guidance in this repo must not prescribe a diagram type or a fixed order. `rules/architecture-docs/SKILL.md` line 46 rejects that directly, and the retired `## Planning Workflow` had been contradicting it.
- Removing a trailing section from a Markdown file eats its EOF newline. Commit `a3a5437` once fixed EOF newlines across the repo, so this is a recurring hazard and neither `make test` target catches it.

### Process

- Naming the areas that must *not* change, then diffing them at the end, is a cheap and durable control against scope creep. Cheaper than reviewing what did change.
- When a skill's siblings are retired, the survivor keeps its old framing silently. This description outlived `planning-execution` by a year while the READMEs around it had already moved on. Human-facing docs drifting *ahead* of a machine-facing field is a detectable signal worth looking for elsewhere.

### Million-Dollar Question

If "a skill's `description` is a triggering surface that must be re-derived whenever the skill's arrangement changes" had been foundational, `visual-planning` would never have survived the #89 retirement with a planning-only description — that commit would have re-derived it. Half of that now exists: `skill-frontmatter.md` states the rule. The other half does not, because the repo has no formal retirement path where such a step could live; retirement is just a PR. That gap stays open, and it is not worth building a process to close it until a second instance appears.
