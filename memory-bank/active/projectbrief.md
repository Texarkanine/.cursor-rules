# Project Brief: Migrate Manual Rules to Skill Resources

## User Story

Relocate all `alwaysApply: false` niko content out of the Cursor rules tree (`rulesets/niko/niko/**/*.mdc`) into the `niko` entry skill's resource directory (`rulesets/niko/skills/niko/resources/**/*.md`), so that cross-harness translation (a16n, rulesync, and any future AgentSkills.io-aware tool) becomes correct by construction rather than requiring a converter-specific flag.

See the architecture decision: [creative-manual-rules-as-skill-resources.md](creative/creative-manual-rules-as-skill-resources.md).

Background: [rulesync #1515](https://github.com/dyoshikawa/rulesync/issues/1515) demonstrates the portability bug when a converter mistranslates `alwaysApply: false` (manual) rules into always-on prompts.

## Requirements

1. **Move `alwaysApply: false` content** from `rulesets/niko/niko/{core,level1,level2,level3,level4,phases}/**/*.mdc` into `rulesets/niko/skills/niko/resources/` mirroring the current tree. Total: 24 files.
2. **Strip frontmatter** and rename `.mdc` → `.md` on every moved file.
3. **Keep as rules** (do not move):
   - `rulesets/niko/niko-core.mdc` (`alwaysApply: true`) — genuine global prompt.
   - `rulesets/niko/niko/core/memory-bank-paths.mdc` (`alwaysApply: true`) — deferred; revisit separately.
   - `rulesets/niko/niko/memory-bank/**/*.mdc` — these use `globs:` (File Rules), not `alwaysApply: false`; they auto-inject when editing matching memory-bank files and have clean cross-harness equivalents (Claude `paths:`). Not in scope.
4. **Rewrite every internal path reference** from `.cursor/rules/shared/niko/...` to the new skill-resource path across all niko tree files and SKILL.md files.
5. **Path rewrites must be scripted**, not manual, with:
   - A helper/audit script that enumerates the `alwaysApply: false` files (the "to be moved" set) and persists that index.
   - A main rewrite script with a dry-run default that prints an auditable index of `(filename, line number, old path, new path)` for every reference it would touch. Human approval precedes execution.
6. **Update documentation**: `memory-bank/systemPatterns.md` "File Organization" section must reflect the rule-vs-resource split.
7. **Verify**:
   - `grep` for `.cursor/rules/shared/niko` in `rulesets/` returns zero hits after rewrite.
   - `ai-rizz` dry-run shows `.cursor/skills/niko/resources/` populated and the old tree absent.
   - `a16n convert --from cursor --to claude --rewrite-path-refs --dry-run` emits zero `orphan-path-ref` warnings.

## Out of Scope

- `memory-bank-paths.mdc` resource/rule classification (follow-up).
- Removing `.cursor/rules/shared/niko/` backward-compat shims for external consumers (follow-up).
- Any rules not under `rulesets/niko/niko/` (e.g., `always-tdd.mdc`, `test-running-practices.mdc`, `visual-planning.mdc`).
