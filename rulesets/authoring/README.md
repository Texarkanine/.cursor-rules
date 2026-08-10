# Authoring Ruleset

This ruleset collects guidance for authoring things in their various forms including agentic harness rules, system prompts, skills, etc.

The rules here cover what to write. For the Agent Skills format itself - the `SKILL.md` container, its frontmatter, and its limits - the upstream authority is [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) and [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).

## 🗺️ [architecture-docs](./skills/architecture-docs/SKILL.md)

- **Purpose**: How to write project architecture documentation, based on [Diátaxis](https://diataxis.fr/) principles.
- **Scope**: Project architecture / systems-atlas docs. Not product how-to guides, and not a substitute for short maintainer orientation notes or agent-only compact system models.

## 📈 [illustrate-complexity](./skills/illustrate-complexity/SKILL.md)

- **Purpose**: How to use [Mermaid](https://mermaid.js.org/) diagrams to illustrate concepts. Given a topic, helps select the right diagram type and structure it clearly.
- **Scope**: Any explanation of a system's structure, flow, or relationships - a document, a prompt, a plan, or an answer in chat.

## ✍️ [markdown-style](./markdown-style.mdc)

- **Purpose**: How to structure Markdown documents that work for humans, agents, *and* rendering engines. Focuses on syntax; the formatting of the document.
- **Scope**: `*.md`, `*.mdc` files.

## ✍️ [prompt-authoring](./skills/prompt-authoring/SKILL.md)

- **Purpose**: How to author a prompt to maximize the chances of an agent adhering to its instructions. Focuses on semantics; the meaning and narrative structure.
- **Scope**: Any prompt-like artifact (workflow, reference, personality, or a mix).
