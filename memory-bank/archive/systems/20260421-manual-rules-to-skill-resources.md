---
task_id: manual-rules-to-skill-resources
complexity_level: 3
date: 2026-04-21
status: completed
---

# TASK ARCHIVE: Migrate Manual Rules to Skill Resources

## SUMMARY

Relocated twenty-four `alwaysApply: false` niko workflow and phase documents from `rulesets/niko/niko/{core,level1..4,phases/creative}/**/*.mdc` into `rulesets/niko/skills/niko/references/**/*.md` (mirrored tree), stripped YAML frontmatter, renamed `.mdc` → `.md`, and rewrote thirty-six internal path references across twelve files using audited Python tooling with operator-gated preview. Documentation updates landed in `memory-bank/systemPatterns.md` (three-tier rules / skills / resources model) and related persistent memory-bank files (`productContext.md`, `techContext.md`). Primary goal: cross-harness correctness **by construction** so converters cannot mistranslate “manual” rules as always-on prompts ([rulesync #1515](https://github.com/dyoshikawa/rulesync/issues/1515)). A secondary finding: `a16n --rewrite-path-refs` does not rewrite path strings under `.cursor/skills/<skill>/references/` to Claude form—seventeen `orphan-path-ref` warnings in sandbox conversion were operator-accepted per preflight Finding 4 fallback; filed as upstream follow-up.

## REQUIREMENTS

1. Move all in-scope `alwaysApply: false` content (twenty-four files) from `rulesets/niko/niko/` subtrees into `rulesets/niko/skills/niko/references/`, strip frontmatter, use `.md` extension.
2. Leave as Cursor rules: `niko-core.mdc`, `memory-bank-paths.mdc`, and `memory-bank/**/*.mdc` (globs-based file rules)—unchanged by this migration.
3. Rewrite every reference from old `.cursor/rules/shared/niko/...` manual-rule paths to `.cursor/skills/shared/niko/references/...` everywhere under `rulesets/niko/` that pointed at moved files; preserve references that intentionally still target rules (`memory-bank-paths.mdc`, `memory-bank/**` templates).
4. Implement migration with machine-generated audit index, dry-run preview, explicit execute subcommands—no hand-edited bulk path churn.
5. Update `memory-bank/systemPatterns.md` “File Organization” for the rule-vs-resource split.
6. Verify with scripted checks: no stale refs to moved paths under `.cursor/rules/shared/niko/` except allowed still-at-rules targets; all new resource refs resolve on disk; exactly twenty-four resource files in destination tree; external tool checks as feasible (`a16n` via `--from-dir`/`--to-dir` sandbox; `ai-rizz` full sync deferred until post-merge because it reads from remote).

## IMPLEMENTATION

### Architecture (creative phase)

**Problem:** Cursor “manual rules” (`alwaysApply: false`) live under the rules tree by convention; other harnesses can treat them as always-on prompts.

**Options considered:**

| Option | Idea |
|--------|------|
| A | Status quo + rely on `a16n --rewrite-path-refs` |
| B | Consolidate all movable content under the `niko` skill as plain resources |
| C | Per-skill colocation (each phase skill owns its files) |
| D | Dedicated `niko-resources` sibling skill |

**Decision:** **Option B** — mirror the existing subtree under `rulesets/niko/skills/niko/references/`. Rationale: portability and semantic correctness come from **layout**, not converter flags; `ai-rizz` already syncs the skills tree; one-time migration cost with no ongoing taxonomy ceremony (C/D add sharing or redundant skills). Tradeoff accepted: one-time migration effort and slightly longer `@`-mention paths.

**Correction after QA:** The creative doc assumed `a16n --rewrite-path-refs` rewrote any Cursor-format path including skill resources. Empirical QA showed resource paths under `.cursor/skills/shared/niko/references/` are **not** rewritten to `.claude/skills/...`; rule↔rule refs rewrite correctly. Primary migration goal still holds; a16n gap is tooling-level follow-up.

### Tooling

- **`scripts/audit_manual_rules.py`** — walks `rulesets/niko/niko/`, emits `scripts/migration-audit.json` (gitignored): twenty-four records with `old_path`, `new_path`, `old_ref`, `new_ref`; excludes `memory-bank-paths.mdc` and `memory-bank/**`.
- **`scripts/migrate_manual_rules.py`** — subcommands: `preview` (dry-run table), `rewrite-refs`, `move-files` (`git mv`, strip **leading** frontmatter only via anchored pattern so in-body fenced examples stay intact), `verify` (grep + resolution checks).
- **`.gitignore`** — ignores regenerable `scripts/migration-audit.json`.

Preflight tightened the Cursor-form target path to **`.cursor/skills/shared/niko/references/...`** (includes `shared/` infix from ai-rizz commit-mode layout)—avoiding systematic broken refs.

### Execution summary

1. Operator approved `preview` output (thirty-six refs, twelve files).
2. `rewrite-refs` updated references in core rules, level workflows/reflect/plan files, milestones template, and `niko` / `niko-creative` SKILL files.
3. `move-files` relocated twenty-four files and stripped leading frontmatter.
4. `memory-bank/systemPatterns.md` updated for three-tier documentation; `productContext.md` / `techContext.md` reconciled for terminology and sync notes.

### Key files touched (representative)

- New: `scripts/audit_manual_rules.py`, `scripts/migrate_manual_rules.py`.
- Modified (path rewrites): twelve files under `rulesets/niko/niko/` and `rulesets/niko/skills/` as listed in active context before archive.
- Moved: twenty-four resources from `rulesets/niko/niko/...` → `rulesets/niko/skills/niko/references/...`.
- Docs: `memory-bank/systemPatterns.md`, `memory-bank/productContext.md`, `memory-bank/techContext.md`.
- QA fix: `creative-phase-template.md` authoring example updated—post-migration resources have no frontmatter; removed stale `alwaysApply: false` skeleton from the template section.

## TESTING

- **`python3 scripts/migrate_manual_rules.py verify`** — PASS: no prohibited `.cursor/rules/shared/niko/` refs to moved subtrees; seventeen preserved refs to `memory-bank-paths.mdc` and `memory-bank/**` match baseline; all thirty-six `.cursor/skills/shared/niko/references/...` refs resolve; exactly twenty-four `.md` files under `resources/`.
- **a16n:** Sandbox `a16n convert --from cursor --to claude --rewrite-path-refs` with `--from-dir`/`--to-dir` against a mirrored tree: seventeen `orphan-path-ref` warnings (resource paths not rewritten in output); copies of resource files present under `.claude/skills/niko/references/`. Accepted per preflight Finding 4.
- **ai-rizz:** Full sync not run against uncommitted local-only state (remote-sourced tool). Structural expectation based on `cp -rL` skills sync and local verify.

## LESSONS LEARNED

- **Separate path rewrites from file moves** into reversible stages; each rollback should map to a small `git` operation (restore edited files vs. revert renames).
- **JSON audit index + operator-approved preview** scales better than one-shot scripts for twenty-plus files.
- **Creative claims about tool behavior need empirical verification** (preflight/QA); an incorrect a16n assumption was caught before it derailed the main outcome because layout-based correctness does not depend on that rewrite.
- **Anchored frontmatter stripping** (`\A---\n...\n---`) avoids damaging in-body fenced examples (e.g. creative phase template).

## PROCESS IMPROVEMENTS

- Treat **source-inspected** preflight findings (e.g. reading ai-rizz implementation for the `shared/` path infix) as higher confidence than doc-guessing.
- For **advisory** preflight items, always attach an explicit **fallback menu** so QA can resolve predictable tool limitations without reopening full replan.

## TECHNICAL IMPROVEMENTS

- Upstream **a16n**: extend `--rewrite-path-refs` to treat paths under `.cursor/skills/<name>/references/` as first-class conversion targets (`.cursor/` → `.claude/`). Until then, Claude-only consumers may need post-processing or a different pipeline.
- After merge: run **`ai-rizz sync`** smoke test to confirm generated `.cursor/skills/shared/niko/references/` matches expectations.
- Optional follow-ups: **`memory-bank-paths.mdc`** rule-vs-resource classification; whether to delete or shim old `.cursor/rules/shared/niko/<moved>` paths for external consumers.

## NEXT STEPS

1. File or track upstream work for **a16n resource path rewriting** under skill `resources/` trees.
2. **Post-push `ai-rizz sync`** verification** on the merged branch.
3. (Existing backlog) Revisit **`memory-bank-paths.mdc`** classification and **backward-compat shims** for old rule paths if needed.
