# Active Context

**Current Task:** Migrate manual rules to skill resources
**Phase:** BUILD - COMPLETE (PASS)

## What Was Done

### Files created

- `scripts/audit_manual_rules.py` — walks `rulesets/niko/niko/`, emits `scripts/migration-audit.json` with 24 records mapping each `alwaysApply: false` `.mdc` to its target `.md` under `rulesets/niko/skills/niko/resources/`. Validated: 24 entries; `memory-bank-paths.mdc` and `memory-bank/**` excluded.
- `scripts/migrate_manual_rules.py` — subcommands `preview`, `rewrite-refs`, `move-files`, `verify`. Driven by the audit JSON.
- `.gitignore` — excludes `scripts/migration-audit.json` (regenerable).

### Files modified by path-rewrite (12 files, 36 refs)

- `rulesets/niko/niko/core/{complexity-analysis,memory-bank-paths}.mdc` — refs to level{1..4}-workflow.
- `rulesets/niko/niko/level{1..4}/*-workflow.mdc` — intra-level refs (these files themselves were then moved).
- `rulesets/niko/niko/level{1,2,3}/*-reflect.mdc`, `level4-plan.mdc` — refs to core & workflow files.
- `rulesets/niko/niko/memory-bank/active/milestones.mdc` — refs to level4 workflow/archive.
- `rulesets/niko/skills/niko/SKILL.md` (6 refs), `rulesets/niko/skills/niko-creative/SKILL.md` (4 refs).

### Files moved (24 files, renamed `.mdc` → `.md`, frontmatter stripped)

All under `rulesets/niko/niko/{core,level1..4,phases/creative}/` → `rulesets/niko/skills/niko/resources/<same-subtree>/`.

### Docs

- `memory-bank/systemPatterns.md` "File Organization" rewritten to document the three-tier split (rules / skills / resources) and the migration tooling in `scripts/`.

## Verification

`python3 scripts/migrate_manual_rules.py verify` — all checks PASS:

- No refs to moved rules remain under `.cursor/rules/shared/niko/{core/complexity-analysis|core/intent-clarification|core/memory-bank-init|core/reconcile-persistent|level[1-4]/|phases/creative/}`.
- 17 preserved refs to still-at-rules files (`memory-bank-paths.mdc`, `memory-bank/**`) intact — matches pre-rewrite baseline.
- All 36 new-form refs (`.cursor/skills/shared/niko/resources/...`) resolve to real files on disk.
- Destination tree has exactly 24 `.md` resource files.

Body fenced-block example frontmatter in `creative-phase-template.md` (inner `---`/`---` around lines 78/80) preserved — leading-frontmatter strip did not touch in-body examples.

## Deferred Checks (→ QA)

- **`ai-rizz sync` dry-run:** `ai-rizz` reads from the git remote (`github.com/texarkanine/.cursor-rules.git` per `ai-rizz.skbd`), so it cannot verify uncommitted local state. `.cursor/rules/shared/niko/` is currently stale (last synced 2026-02-22). QA should push to remote, run `ai-rizz sync`, and confirm `.cursor/skills/shared/niko/resources/` populates with 24 `.md` files and `.cursor/rules/shared/niko/` no longer contains the 24 moved files (memory-bank-paths + memory-bank/** should remain).
- **`a16n convert --from cursor --to claude --rewrite-path-refs --dry-run`:** explicitly deferred by preflight Finding 4. Depends on the synced `.cursor/` tree; QA should run after the ai-rizz sync above.

## Deviations from Plan

None. Executed to the letter, with two exceptions explicitly authorized by the preflight:

1. Scripts consolidated 3 → 2 (preflight Finding 6).
2. Runtime verification via ai-rizz/a16n deferred to QA (preflight Finding 4 plus the ai-rizz remote-sourced constraint observed during build).

## Next Step

QA phase: invoke `niko-qa` skill. QA should run the two deferred runtime checks against a pushed branch and perform semantic review.
