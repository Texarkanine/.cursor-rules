# Progress: Migrate Manual Rules to Skill Resources

## Summary

Relocate all `alwaysApply: false` niko content from `rulesets/niko/niko/**/*.mdc` into `rulesets/niko/skills/niko/resources/**/*.md`, strip frontmatter, rewrite internal path references via scripted audit/rewrite tools with dry-run + human approval, and update `systemPatterns.md` to reflect the new rule-vs-resource split. Motivated by cross-harness portability (see [rulesync #1515](https://github.com/dyoshikawa/rulesync/issues/1515)) and decided in `creative/creative-manual-rules-as-skill-resources.md`.

**Complexity:** Level 3

## History

- Creative phase complete (ran standalone before task classification). Architecture decision: Option B — consolidate resources under the `niko` skill.
- Complexity analysis complete: Level 3.
- Leaving complexity analysis → entering plan phase.
- Plan phase complete. Scope refined from ~28 files to 24 files (memory-bank templates are `globs:` File Rules, out of scope). Implementation plan in `tasks.md`: three Python scripts (audit, rewrite with dry-run, migrate+strip-frontmatter) plus verify script, 10 ordered steps with operator approval gate between preview and execute.
- Leaving plan phase → entering preflight phase.
- Preflight complete (PASS). Fixed blocking Cursor-form path (`.cursor/skills/shared/niko/resources/...`, with the ai-rizz `shared/` infix). Consolidated scripts 3→2 via radical-innovation finding. Advisory: verify a16n's handling of the `shared/` infix during QA.
- Leaving preflight phase → entering build phase.
- Build phase complete (PASS). Authored `scripts/audit_manual_rules.py` (24-entry audit) and `scripts/migrate_manual_rules.py` (preview / rewrite-refs / move-files / verify). Operator approved preview. Executed rewrite-refs (36 refs across 12 files), move-files (24 files moved + frontmatter stripped), `systemPatterns.md` documentation update, and verify (all 4 invariants PASS). `ai-rizz` and `a16n` runtime verification deferred to QA — both require a synced `.cursor/` tree and `ai-rizz` is remote-sourced so cannot verify uncommitted state.
- Leaving build phase → entering QA phase.
- QA phase complete (PASS). Static semantic review applied KISS/DRY/YAGNI/Completeness/Regression/Integrity/Documentation. One trivial-fix finding: `creative-phase-template.md` skeleton showed old `alwaysApply: false` frontmatter → updated to reflect new resource-file convention. a16n runtime check executed via sandbox (`a16n --from-dir` / `--to-dir` against a manually-synced mirror of `rulesets/`): 17 orphan-path-ref warnings for resource-path refs, operator-accepted per preflight Finding 4 fallback. Follow-up filed to upstream a16n's rewrite-path-refs for skill-resources. `ai-rizz` runtime check remains deferred post-merge (remote-sourced; structural correctness already established).
- Leaving QA phase → entering Reflect phase (L3 workflow: QA PASS → Reflect is a solid edge).
- Reflect phase complete. Wrote `memory-bank/active/reflection/reflection-manual-rules-to-skill-resources.md`. Reconciled persistent files: surgical updates to `productContext.md` (Quality Standards) and `techContext.md` (Technologies / File Conventions / Synchronization) to reflect the new three-tier content model; `systemPatterns.md` already updated in build. Key insights: (tech) separate rewrite from move for reversibility, a16n's rewrite-path-refs is top-level-only, JSON audit + gated dry-run scales safely; (process) source-derived preflight findings outrank guesses, advisory findings should carry explicit fallback menus, mid-phase operator hints can unlock scope.
- Leaving Reflect phase → awaiting operator decision on Archive transition (L3 workflow: Reflect → Archive is a dashed edge).
