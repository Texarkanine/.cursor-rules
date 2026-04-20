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

## QA Results

**Phase: QA - COMPLETE (PASS)**

### Findings resolved during QA

- **Fixed:** `creative-phase-template.md` skeleton updated to reflect the new resource-file convention (was still showing `alwaysApply: false` frontmatter in the authoring example).

### a16n runtime check (was preflight Finding 4 advisory)

Verified by running `a16n convert --from cursor --to claude --rewrite-path-refs` against a sandbox `.cursor/`-mirror built from current `rulesets/` via `a16n --from-dir/--to-dir`. Result: **17 orphan-path-ref warnings**, one per resource-path ref across:

- `.cursor/rules/shared/niko/core/memory-bank-paths.mdc` (4 refs)
- `.cursor/rules/shared/niko/memory-bank/active/milestones.mdc` (2 refs)
- `.cursor/skills/shared/niko/SKILL.md` (7 refs)
- `.cursor/skills/shared/niko-creative/SKILL.md` (4 refs)

a16n correctly copies the 24 resource files to `.claude/skills/niko/resources/` and correctly rewrites rule↔rule refs, but doesn't treat `.cursor/skills/<name>/resources/...` paths as convertible for `--rewrite-path-refs`. The converted `.claude/` output therefore contains path refs still written as `.cursor/skills/shared/niko/resources/...` — broken for Claude-only consumers.

**Operator-accepted** per preflight Finding 4 fallback. The migration's primary goal (avoiding `alwaysApply: false` mistranslation per rulesync#1515) is fully met. The a16n ref-rewrite limitation is a tooling issue requiring an upstream fix, queued as follow-up #1 in `tasks.md`.

### ai-rizz runtime check (deferred to post-merge)

Remains deferred. `ai-rizz` reads from the git remote per `ai-rizz.skbd`, so it cannot observe the uncommitted branch. Structural correctness is already established via preflight Finding 2 (`cp -rL`) and local `verify` invariants. Post-merge sync should confirm the tree shape matches the sandbox used for the a16n verification.

## Deviations from Plan

None substantive. Executed to the letter, with two planned exceptions:

1. Scripts consolidated 3 → 2 (preflight Finding 6).
2. `ai-rizz` runtime sync deferred (remote-sourced constraint); `a16n` runtime verified in QA via sandbox (per operator cue — the `--from-dir`/`--to-dir` flags make `.cursor/` sync unnecessary).

One QA-time trivial fix: `creative-phase-template.md` skeleton.

## Next Step

L3 workflow: QA PASS → Reflect is a dashed edge (requires operator input). Awaiting operator decision on Reflect transition.
