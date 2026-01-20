# Tech Context: Cursor Rules Repository

## Technologies
- **Format**: Markdown with YAML frontmatter (.mdc files)
- **Diagrams**: Mermaid for flowcharts and process maps
- **Platform**: Cross-platform (Windows PowerShell, Mac/Linux Bash)

## File Conventions
- Rule files use `.mdc` extension
- Command files use `.md` extension
- All paths should be workspace-relative

## Synchronization
Syncing between source (`rulesets/`) and active (`.cursor/rules/`) is handled by **ai-rizz** tool.
See `ai-rizz.skbd` for configuration. Do not manually sync files.

## Git Conventions
- Commits: Use conventional commit prefixes (feat, fix, chore, docs)
- No GPG signing required
