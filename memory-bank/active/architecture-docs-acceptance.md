# Acceptance Checklist: architecture-docs skill

TDD stand-in for prose skill content (step 4a). Each item must be observably true of `rules/architecture-docs/SKILL.md` before build marks content complete.

## Structure (creative pedagogy)

- [x] Frontmatter has `name: architecture-docs` and a `description` that triggers on writing/improving project architecture docs
- [x] Short **genre frame**: project architecture docs vs memory-bank `systemPatterns` / `techContext` vs user/contributor how-to guides
- [x] Explicit **evidence-weight** note: primary local docs ≥ Niko-adjacent templates > secondary a16n > tertiary FOSS; local wins on conflict
- [x] Skill is **reference-shaped**: flat principle sections; no workflow-led spine; no narrative case-study body
- [x] Each principle has: stated principle → why it matters → **Not this** anti-pattern → optional one-line evidence tag (`local` / `niko-adj` / `a16n` / `foss`)

## Principles present (from inventory)

- [x] Frame the genre before the outline
- [x] Apply an inclusion bar
- [x] WHAT-first; WHY for Chesterton’s fences
- [x] Orient with a diagram that loads the whole model
- [x] Name invariants and load-bearing boundaries
- [x] Route change surfaces
- [x] Keep procedures outbound
- [x] Allow audience-split overlap; forbid silent forks
- [x] Cluster at atlas grain
- [x] Prefer durable, brief stewardship

## Anti-recipe / anti-absorption

- [x] Does **not** instruct “always open with a control-flow diagram” (or any single diagram type) without enclosing principle that chooses diagram for the load-bearing story — phrase may appear only under **Not this**
- [x] Does **not** paste Niko Avoid / When-to-Update blocks verbatim
- [x] Does **not** instruct agents to edit `systemPatterns.md` / `techContext.md` when the ask is for project architecture docs
- [x] Does **not** present FOSS outlines as the definition of good relative to local goldens
- [x] Does **not** duplicate prompt-authoring / markdown-style / visual-planning guidance (assumes or stays silent)

## Packaging (step 5a — separate cycle)

- [x] `rulesets/authoring/skills/architecture-docs` is a directory symlink to `../../../rules/architecture-docs`
- [x] `rulesets/authoring/README.md` documents the skill (purpose + scope)
- [x] REUSE: `rules/**/*.md` already covers new `SKILL.md` (confirm; no REUSE.toml edit unless gap)
- [x] Changeset does not modify stockroom / ai-rizz / a16n architecture markdown or Niko `systemPatterns.mdc` / `techContext.mdc`
