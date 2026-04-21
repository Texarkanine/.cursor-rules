# Tech Context: Cursor Rules Repository

## Technologies
- **Rule format**: Markdown with YAML frontmatter (`.mdc` files) — `alwaysApply: true` or `globs:` to trigger auto-injection.
- **Skill format**: AgentSkills-idiomatic `SKILL.md` (Markdown with `name:` / `description:` frontmatter).
- **Reference format**: Plain Markdown (`.md`) with no frontmatter — loaded by explicit path from skills or other references. Folder name (`references/`) matches the AgentSkills.io convention.
- **Diagrams**: Mermaid for flowcharts and process maps.
- **Platform**: Cross-platform (Windows PowerShell, Mac/Linux Bash).
- **Cross-harness translation**: `a16n` converts Cursor customizations to other harnesses (e.g., Claude Code). Accepts `--from-dir <src>` / `--to-dir <dst>` to operate on arbitrary source/target trees rather than the in-repo `.cursor/` / `.claude/`.

## File Conventions
- Rule files: `.mdc` extension, live under `rulesets/**/*.mdc` (sources) and sync into `.cursor/rules/**`.
- Skill files: `SKILL.md` inside a named skill directory, live under `rulesets/niko/skills/<name>/SKILL.md` (sources) and sync into `.cursor/skills/shared/<name>/SKILL.md`.
- Reference files: `.md` extension with no frontmatter, live under `rulesets/niko/skills/niko/references/**/*.md` (sources) and sync into `.cursor/skills/shared/niko/references/**/*.md`. Loaded by explicit path from skills and other references.
- All paths should be workspace-relative.

## Synchronization
Syncing between source (`rulesets/`) and active trees (`.cursor/rules/`, `.cursor/skills/`) is handled by **ai-rizz**. See `ai-rizz.skbd` for configuration. Do not manually edit the active trees. Note: `ai-rizz` reads from the configured git remote, not the local working tree, so uncommitted changes to `rulesets/` are invisible to it until pushed.

## Git Conventions
- Commits: Use conventional commit prefixes (feat, fix, chore, docs)
- No GPG signing required for agents
