# Project Brief

## User Story

As a rules author, I want the Mermaid-diagram skill to trigger whenever an explanation needs an illustration, so that diagrams appear in documentation, READMEs, and design notes — not only in planning artifacts.

## Use-Case(s)

### Use-Case 1: Authoring documentation

An agent writes a README or an architecture note. The subject has branching structure. The skill triggers, and the agent adds a diagram.

### Use-Case 2: Planning work

An agent plans a non-trivial task. The skill triggers as it does today. This must not regress.

### Use-Case 3: Authoring a skill

An agent edits a `SKILL.md`. It must know that `description` drives triggering, and what the format limits are. The repo's own guidance does not cover this today. That gap is what let the `visual-planning` description stay wrong for a year.

## Requirements

1. Rename `rules/visual-planning/` to `rules/illustrate-complexity/`.
2. Replace the frontmatter description. Target ~300 characters. Imperative. It covers docs, READMEs, design notes, prompts, plans, and chat answers. It excludes numeric charting.
3. Open the body on the general case, not on planning.
4. Move the "more than a paragraph of *and then*" test near the top of the body.
5. Keep the emoji library unchanged. It is a shared design language across chart types.
6. Add one sentence and a link to <https://mermaid.js.org/intro/syntax-reference.html> for chart types the table omits.
7. Replace `## Planning Workflow` with a section covering three uses: planning, documenting, and answering a question. Each use gets short, specific guidance. It states that chat diagrams stay small, because most chat UIs render them badly, and that a large diagram is correct on a web page, because Mermaid gives the reader a lightbox.
8. Update every reference to the old name: the `rulesets/authoring/skills/` symlink, the `rulesets/niko/skills/` symlink, `rulesets/authoring/README.md`, `rulesets/niko/README.md`, and `memory-bank/techContext.md`.
9. Add a link to <https://agentskills.io/skill-creation/best-practices> in `rulesets/authoring/README.md`.
10. Create `rules/prompt-authoring/references/skill-frontmatter.md`. It covers what the repo omits: `description` drives triggering, the 1024-character limit, and when to split content into `references/`. It links the agentskills best-practices and optimizing-descriptions pages.
11. Add a one-line conditional pointer to that reference from `rules/prompt-authoring/SKILL.md`. The pointer states when to read the file.

## Constraints

1. Edit canonical sources only: `rules/` and `rulesets/`. Never edit `.cursor/` or `.claude/`.
2. Make no change wider than a requirement needs.
3. Every edited file must obey the repo's own rules, including `markdown-style.mdc`, `asd-ste100.mdc`, and `prompt-authoring`.
4. Archive files keep the old name. Do not rewrite them.
5. Do not add an always-applied tripwire rule. The operator rejected it.

## Acceptance Criteria

1. `make test` passes.
2. No file under `rules/` or `rulesets/` refers to `visual-planning`, and `memory-bank/techContext.md` names the new skill. The generated `.cursor/` and `.claude/` trees are excluded; they lag by design.
3. The new description is under 1024 characters and names no planning-only trigger.
4. No section of the skill body frames the skill as a step inside a planning workflow.
5. `rules/prompt-authoring/SKILL.md` grows by no more than a few lines.
