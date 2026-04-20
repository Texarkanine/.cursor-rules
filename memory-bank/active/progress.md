# Progress: Migrate Manual Rules to Skill Resources

## Summary

Relocate all `alwaysApply: false` niko content from `rulesets/niko/niko/**/*.mdc` into `rulesets/niko/skills/niko/resources/**/*.md`, strip frontmatter, rewrite internal path references via scripted audit/rewrite tools with dry-run + human approval, and update `systemPatterns.md` to reflect the new rule-vs-resource split. Motivated by cross-harness portability (see [rulesync #1515](https://github.com/dyoshikawa/rulesync/issues/1515)) and decided in `creative/creative-manual-rules-as-skill-resources.md`.

**Complexity:** Level 3

## History

- Creative phase complete (ran standalone before task classification). Architecture decision: Option B — consolidate resources under the `niko` skill.
- Complexity analysis complete: Level 3.
- Leaving complexity analysis → entering plan phase.
