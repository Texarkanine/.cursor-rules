---
task_id: manual-rules-to-skill-resources
date: 2026-04-20
complexity_level: 3
---

# Reflection: Migrate Manual Rules to Skill Resources

## Summary

Relocated 24 `alwaysApply: false` niko workflow/phase content files from `rulesets/niko/niko/{core,level1..4,phases}/**/*.mdc` to `rulesets/niko/skills/niko/resources/` as plain Markdown, rewrote 36 internal path references across 12 files, and updated `systemPatterns.md`. The primary goal — making cross-harness portability correct by construction, so the `alwaysApply: false` rulesync #1515 mistranslation cannot occur — was fully achieved. A secondary a16n limitation (17 orphan-path-ref warnings on resource-path refs) was anticipated by preflight Finding 4 and accepted per its documented fallback.

## Requirements vs Outcome

Every requirement from `projectbrief.md` was met:

- **Move 24 files, strip frontmatter, rename `.mdc` → `.md`** — done; verified 24 destination files exist, zero remaining `alwaysApply: false` references in migrated content.
- **Keep `niko-core.mdc`, `memory-bank-paths.mdc`, `memory-bank/**/*.mdc` as rules** — untouched; 17 preserved-ref checks pass.
- **Rewrite internal path refs** — 36 refs across 12 files rewritten; `verify` subcommand confirms all 36 resolve to files on disk.
- **Scripted with dry-run + operator gate** — `preview` subcommand gated the destructive `rewrite-refs` and `move-files`.
- **Update `systemPatterns.md`** — three-tier (rules / skills / resources) layout documented.
- **Verification: grep / ai-rizz / a16n** — grep and local invariants clean; a16n verified via sandbox (operator-suggested use of `--from-dir`/`--to-dir`); ai-rizz remains deferred post-merge because it reads from the git remote.

One addition not in the original plan: the creative-phase-template's "Example: Skeleton" showed the old `alwaysApply: false` frontmatter format — stale documentation that became visible only after the migration changed the convention. QA caught it and applied a trivial fix.

## Plan Accuracy

The 11-step implementation plan ran in order with no rework. Two planned deviations, both authorized in advance:

1. **Scripts consolidated 3 → 2** per preflight Finding 6 (merge `preview_ref_rewrite.py` + `execute_migration.py` into subcommands). Consolidation matched operator preference and produced a cleaner CLI.
2. **a16n verification moved from build to QA.** The plan expected a post-sync check; the `ai-rizz` remote-sourcing discovered during build (it reads from github.com/texarkanine/.cursor-rules.git rather than local working tree) made this impossible pre-merge. The operator's mid-QA hint about `a16n --from-dir`/`--to-dir` enabled in-phase verification via sandbox instead of waiting for the remote merge.

Challenges predicted in the plan all materialized and their mitigations held:
- **Frontmatter strip could eat body content** → anchored regex (`\A---\n.*?\n---\n\n?`) matched only the leading frontmatter; fenced-block frontmatter examples in `creative-phase-template.md` body were preserved correctly.
- **Broken path refs leak into memory-bank docs** → the `verify` subcommand's "every new-form ref resolves to a file on disk" invariant catches this class of error.
- **Hidden refs in unusual files** → the full-tree scan with per-file grep is exhaustive within the niko tree.

## Creative Phase Review

One creative decision: Option B — consolidate all 24 resources under the `niko` skill. It held up with zero friction during build. No boundary questions, no "which skill owns this?" judgment calls. The decision's KEY rationale — "semantic correctness is enforced at repo layout, not converter configuration" — was validated at QA: even when a16n partially fell short on secondary ref-rewriting, the primary structural property (no `alwaysApply: false` anywhere near a Claude converter) was unshakeable because it lives in the file layout.

One asserted claim in the creative doc was disproven: "a16n --rewrite-path-refs handles the Cursor↔Claude swap because it rewrites any source-format path, not only rules paths." Preflight Finding 4 (advisory) caught this as unverified and routed it to QA for empirical check. QA disproved it — a16n doesn't enumerate skill-nested resource paths for rewrite. This is the system working correctly: creative made a claim, preflight flagged uncertainty, QA verified, operator had a pre-authorized fallback path ready.

## Build & QA Observations

Build was unusually smooth:
- `audit_manual_rules.py` produced exactly 24 entries on the first run.
- `preview` produced the expected 36 refs / 12 files with zero false positives.
- `rewrite-refs` + `move-files` executed without retries.
- Every one of `verify`'s 4 invariants passed on first try.
- Four semantic commits split cleanly via stage-by-path.

QA caught exactly what it should:
- One documentation drift (template skeleton) — trivial fix.
- One predicted external-tool limitation (a16n orphan refs) — operator-accepted per preflight fallback.
- No rework. No plan revisions.

## Cross-Phase Analysis

- **Preflight → Build (single-character save):** Preflight Finding 1 caught that `.cursor/skills/niko/resources/...` in the original plan should be `.cursor/skills/shared/niko/resources/...` — the `shared/` infix that ai-rizz inserts. Without this fix, all 36 rewritten refs would have been wrong. Preflight's source-inspection style (reading ai-rizz.src:4826) produced a much higher-confidence finding than any guess could have.
- **Preflight → QA (authorization pre-positioned):** Preflight Finding 4's advisory + explicit fallback menu ("accept orphan-path-ref warnings or adjust a16n mapping") meant the exact QA finding that materialized had a pre-decided resolution path. Without this, QA would have routed back to Plan to re-architect ref handling, spending days replanning instead of accepting a known upstream-tool limitation.
- **Operator → QA (scope unlock):** A two-line operator hint ("you can pick your dirs") turned a "deferred to post-merge" risk into an in-phase verification. The delta between "assume it'll work" and "empirically verified with receipts" is the difference between a healthy Reflect phase and a post-merge surprise.
- **Plan → Build (cost reduction):** 2 scripts (per Finding 6) instead of 3 meant fewer CLI surfaces, one shared audit-loading path, one consistent error model — nothing to stitch together. Consolidation costs less cognitive overhead both at build time and when re-reading the scripts later.

## Insights

### Technical

- **Separate rewrite from move.** Rewriting path refs and physically moving files must be factored as two sequential, reversible steps. If combined into one script run, rollback means un-moving 24 files — way harder than `git restore` on 12 edited files. The `preview → rewrite-refs → move-files` ordering in our script made the failure mode at each stage trivially recoverable. Generalizable rule: **in bulk migrations, factor destructive transformations so each stage's rollback is a single `git` operation.**
- **a16n's rewrite-path-refs surface is top-level-only.** It discovers rules and SKILL.md files but does not index paths under a skill's `resources/` subtree as convertible entities for path-ref rewriting, even though it copies those files to the output tree. Any Cursor→Claude migration that uses skill-nested resources needs either an upstream a16n fix or a post-processing step on the converted output. Worth filing an issue; documented in follow-up #1.
- **A JSON audit index plus operator-gated dry-run is dramatically safer than one-pass migration for 20+ files.** The operator approves against an auditable artifact (`scripts/migration-audit.json`, plus `preview` output) rather than trusting a single monolithic run. For the operator, this turned a scary destructive operation into a 30-second skim of a concrete artifact.

### Process

- **Preflight findings derived from reading tool source should be flagged as higher-confidence** than findings derived from interface-level reasoning or guessing. Finding 1 (the `shared/` infix) came from `ai-rizz.src:4826` — a ground-truth source inspection — and prevented a wholesale misrouting of the migration. Worth normalizing as a preflight hygiene rule: "when verifying tool behavior, prefer reading the tool's source to guessing from its docs or its name."
- **Advisory preflight findings should carry an explicit fallback menu.** Finding 4 worked exactly as designed: "a16n behavior for .cursor/skills/shared/... paths is unverified; **Fallbacks: accept orphan-path-ref warnings or adjust a16n mapping.**" When the predicted failure materialized in QA, the operator had pre-authorized resolution paths instead of fresh decision-making under uncertainty. Compare to the alternate timeline where Finding 4 had said only "this is unverified — check in QA": QA would have reported 17 warnings as a blocking FAIL, routed back to Plan, spent a day redesigning, and ended up at the same decision anyway. Worth templatizing: **advisory findings should always name 2-3 concrete fallbacks that the operator is pre-authorized to choose from.**
- **Mid-phase operator hints can unlock scope.** The operator's two-line "you can pick your dirs" suggestion converted a "structural-only, runtime deferred" QA into a "runtime-verified" QA, closing the feedback loop an entire merge cycle earlier. When the agent says "I can't verify X because of constraint Y," responding with a constraint workaround (rather than agreeing to defer) can be the highest-leverage contribution an operator makes. Worth noting as a collaboration pattern.
