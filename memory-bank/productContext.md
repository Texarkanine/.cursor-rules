# Product Context: Cursor Rules Repository

## Purpose
Provide high-quality, reusable Cursor IDE rules that enhance AI-assisted development workflows.

## Target Users
- Developers using Cursor IDE
- Teams wanting consistent AI behavior across projects
- Projects needing structured task management (Niko system)

## Key Features
1. **Niko Memory Bank System**: Complexity-based task routing, context preservation, archival
2. **TDD Rules**: Test-driven development enforcement
3. **Style Rules**: Language-specific coding conventions
4. **Planning Rules**: Visual planning and task decomposition

## Quality Standards
- Rules must be well-documented with clear descriptions
- Rules use the `.mdc` format with proper YAML frontmatter (either `alwaysApply: true` or `globs:` to trigger inclusion)
- Skills use the AgentSkills-idiomatic `SKILL.md` shape
- References (plain Markdown content loaded by path from skills or other references) use `.md` with no frontmatter; folder name matches the AgentSkills.io `references/` convention
- Examples should be practical and actionable
