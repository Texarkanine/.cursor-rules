# Acceptance Checklist: architecture-docs skill

TDD stand-in for prose skill content. Updated after post-reflect portability fix: shipped skill must not require Niko/memory-bank vocabulary.

## Structure (creative pedagogy)

- [x] Frontmatter has `name: architecture-docs` and a `description` that triggers on writing/improving project architecture docs
- [x] Short **genre frame**: project architecture docs vs how-to guides vs maintainer orientation notes vs agent compact models — **without** naming memory-bank / Niko / `systemPatterns` / `techContext`
- [x] Prefer-local-why / FOSS-does-not-redefine-good judgment note (no Niko evidence-tag ladder required in the shipped skill)
- [x] Skill is **reference-shaped**: flat principle sections; no workflow-led spine; no narrative case-study body
- [x] Each principle has: stated principle → why it matters → **Not this** anti-pattern

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

## Anti-recipe / anti-absorption / portability

- [x] Does **not** instruct “always open with a control-flow diagram” without enclosing principle that chooses diagram for the load-bearing story — phrase may appear only under **Not this**
- [x] Does **not** mention memory-bank, Niko, `systemPatterns.md`, or `techContext.md`
- [x] Does **not** instruct agents to edit maintainer orientation notes / agent system models when the ask is for project architecture docs
- [x] Does **not** present FOSS outlines as the definition of good relative to this project's recoverable why
- [x] Does **not** duplicate prompt-authoring / markdown-style / visual-planning guidance (assumes or stays silent)

## Packaging

- [x] `rulesets/authoring/skills/architecture-docs` is a directory symlink to `../../../rules/architecture-docs`
- [x] `rulesets/authoring/README.md` documents the skill (purpose + scope) without Niko/memory-bank jargon
- [x] REUSE: `rules/**/*.md` covers `SKILL.md`
- [x] Changeset does not modify stockroom / ai-rizz / a16n architecture markdown or Niko mdc templates
