# Tech Context

A repository of Cursor customizations authored here as canonical source and distributed to live agent trees by external tooling. The entity taxonomy and source-of-truth rules live in `memory-bank/systemPatterns.md`; this file covers the tooling around them.

## Distribution Tooling

- **ai-rizz** installs rules and rulesets from this repo into a consumer's `.cursor/` tree (configured in `ai-rizz.skbd`). It reads from the configured git *remote*, not the local working tree, so changes are invisible to it until pushed.
- **a16n** converts Cursor customizations to other harnesses (e.g. Claude Code). It accepts `--from-dir` / `--to-dir` to operate on arbitrary trees rather than the in-repo `.cursor/` / `.claude/`.
- Rules can also be viewed rendered as Markdown on GitHub via `client-side-mdc-render` (linked from the README).

## Skill Format

Skills follow the [Agent Skills specification](https://agentskills.io/specification). `rules/prompt-authoring/references/skill-frontmatter.md` orients on the container; the spec holds the limits.

## Testing Process

`make test` runs rulesets layout checks (symlink targets and README internal links) via scripts in `scripts/`. Pull request CI is `.github/workflows/rulesets-links.yml` and invokes the same Make targets.

## Platform

Cross-platform: any rule content or script must hold up under both Windows PowerShell and Mac/Linux Bash.

## Diagrams

Mermaid, per the `illustrate-complexity` skill. Consumer-facing charts (README, published docs) must be checked on mermaid.live / GitHub — Cursor preview is not layout SoT.

## Licensing

Licensing follows the REUSE specification (`REUSE.toml`, `LICENSES/`). New files may need copyright and license information recorded there.

## Git Conventions

Conventional-commit prefixes (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`). Agents commit without GPG signing.
