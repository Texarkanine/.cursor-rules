# Architecture Decision: Manual Rules as Skill Resources

## Question

Cursor's `alwaysApply: false` "manual rules" are static resources bundled in the `.cursor/rules/` tree by convention. Other harnesses (rulesync, Claude Code directly) lack the concept and can mistranslate these into always-on prompts (see [rulesync #1515](https://github.com/dyoshikawa/rulesync/issues/1515)).

Today the workaround is `a16n convert --rewrite-path-refs`, which correctly rewrites path references and treats `alwaysApply: false` rules appropriately. But that binds us to a specific converter's semantics.

**Can we restructure the repo so that "manual rules" live where they semantically belong — as static resources under the skills that consume them — making the cross-harness translation a non-issue rather than a converter feature?**

## Requirements & Constraints

**Ranked quality attributes:**
1. Cross-harness portability (a16n, rulesync, Copilot, Continue, future tools)
2. Semantic correctness (never let a resource become a global prompt)
3. Maintainability (single editor; predictable layout)
4. ai-rizz sync compatibility
5. Cursor `@`-mention ergonomics (nice-to-have)

**Constraints:**
- `rulesets/` is source-of-truth; `ai-rizz` already syncs `rulesets/niko/skills/` and top-level rules into `.cursor/`.
- `rulesets/niko/skills/*/SKILL.md` follows AgentSkills.io shape.
- Of the `.mdc` files under `rulesets/niko/niko/`:
  - `memory-bank-paths.mdc` is `alwaysApply: true` (genuine always-on rule).
  - The `memory-bank/**/*.mdc` templates use `globs:` (Cursor File Rules; Claude `paths:` equivalent) — clean cross-harness translation, out of scope.
  - The remaining **24** files (under `core/`, `level{1..4}/`, `phases/creative/`) are `alwaysApply: false` — referenced exclusively by explicit path from skills and other `.mdc` files. They are functionally static resources.
- `niko-core.mdc` at `rulesets/niko/niko-core.mdc` is `alwaysApply: true` and is a genuine always-on rule.

**In scope:** the 24 `alwaysApply: false` files under `rulesets/niko/niko/{core,level1-4,phases}`.
**Out of scope:** `niko-core.mdc`, `always-tdd.mdc`, `test-running-practices.mdc`, `visual-planning.mdc`, `memory-bank-paths.mdc` (deferred), and `memory-bank/**/*.mdc` (File Rules, not manual rules).

## Components

```
Skills (portable)            Rules (Cursor-ambient)        Resources (skill-loaded)
-----------------            ----------------------        ------------------------
niko/SKILL.md                niko-core.mdc                 core/*, levelN/*,
niko-plan/SKILL.md           (alwaysApply: true)           phases/creative/*,
niko-creative/SKILL.md                                     memory-bank/*
...
    ^                             ^                              ^
    |                             |                              |
    +-- invoked by agent          +-- auto-injected               +-- loaded by path
                                                                    from skills
```

The Resources bucket has no semantic relationship with Cursor's rules system — it lives there only because Cursor's rules tree happens to be the distribution channel shared with skills in current tooling.

## Options Evaluated

- **A. Status quo + `a16n --rewrite-path-refs`.** Keep everything under `rulesets/niko/niko/**/*.mdc`; declare a16n the supported converter; accept that rulesync and any tool without equivalent handling will mistranslate.
- **B. Consolidate resources under the `niko` skill.** Move all ~28 files to `rulesets/niko/skills/niko/resources/` mirroring the current tree; strip frontmatter; rewrite ~35 path references once.
- **C. Per-skill colocation.** Each phase skill owns its phase content; cross-skill content (memory-bank-paths, complexity-analysis, reconcile-persistent, creative templates) goes to a shared skill.
- **D. Sibling `niko-resources` skill.** All content in a dedicated skill with `disable-model-invocation: true`, separate from the entry skill.

## Analysis

| Criterion | A: Status quo | B: Under `niko` skill | C: Per-skill | D: Sibling skill |
|---|---|---|---|---|
| Cross-harness portability | ⚠️ converter-dependent | ✅ by construction | ✅ by construction | ✅ by construction |
| Semantic correctness | ⚠️ depends on converter | ✅ structure = meaning | ✅ | ✅ |
| Maintainability | ✅ no change | ⚠️ one-time migration | ❌ sharing model needed | ⚠️ one-time + extra skill |
| Simplicity | ⚠️ conflates rule and resource | ✅ clean split | ⚠️ forces shared skill anyway | ⚠️ ceremonial skill |
| ai-rizz compatibility | ✅ | ✅ already syncs skills tree | ✅ | ✅ |
| Cursor `@`-mention | ✅ | ✅ slightly longer path | ✅ | ✅ |
| Future-proofing | ❌ every new harness re-opens issue | ✅ | ✅ | ✅ |
| Migration risk | ✅ none | ⚠️ contained, grep-verifiable | ❌ ownership decisions per file | ⚠️ same as B |

**Key insights:**

- A vs. B is the real choice. C and D don't add value; they add ceremony.
- A keeps leaning on a Cursor quirk that a16n happens to paper over. Any harness without the flag (rulesync today; unknown tools tomorrow) re-opens the issue.
- B is a one-time cost with no ongoing tax. `ai-rizz` already syncs `rulesets/niko/skills/`; `a16n --rewrite-path-refs` still works because it rewrites any source-format path, not just rules paths.
- C has a genuine sharing problem. `memory-bank-paths`, `complexity-analysis`, `reconcile-persistent`, memory-bank templates, and creative-phase templates are cross-skill. Colocating forces duplication or a sibling shared skill — which is essentially D.
- The strategic win of B: it removes an artificial category. The repo says what it means — `niko-core.mdc` is a rule because it's always-on; everything else is a resource because skills load it. That clarity *is* the portability: any target harness that understands AgentSkills.io works, no translation table required.

## Decision

**Selected:** Option B — consolidate all `alwaysApply: false` content under `rulesets/niko/skills/niko/resources/` as plain `.md`. Keep `niko-core.mdc` as a rule. Defer `memory-bank-paths.mdc` as a separate follow-up.

**Rationale:** The top-ranked quality attribute (cross-harness portability) is solved **by construction** rather than by converter configuration. Semantic correctness is enforced at repo layout. Maintainability is preserved (one-time migration, no tooling changes) and actually improves because organization finally matches semantics.

**Tradeoff accepted:** one-time migration of ~28 files plus ~35 path-reference rewrites, and slightly longer `@`-mention paths in Cursor.

## Implementation Notes

- **Layout:** mirror the current tree under the entry skill.
  ```
  rulesets/niko/skills/niko/
    SKILL.md
    resources/
      core/                    # complexity-analysis, intent-clarification, memory-bank-init, reconcile-persistent
      level1/ level2/ level3/ level4/
      memory-bank/
      phases/creative/
  ```
- **Strip frontmatter entirely** (these are resources, not rules). Rename `.mdc` → `.md`.
- **Path rewrites:** every `.cursor/rules/shared/niko/...` reference becomes a skill-relative path. In Cursor that renders as `.cursor/skills/niko/resources/...`; in Claude Code as `.claude/skills/niko/resources/...`. `a16n --rewrite-path-refs` handles the Cursor↔Claude swap because it rewrites any source-format path, not only rules paths.
- **Keep `niko-core.mdc`** as a rule at `rulesets/niko/niko-core.mdc` (genuine `alwaysApply: true`).
- **Defer `memory-bank-paths.mdc`**: marked `alwaysApply: true` today but reads like reference material. Keep as a rule in this migration; consider downgrading to a resource in a follow-up.
- **Verification:**
  - `grep -r '.cursor/rules/shared/niko' rulesets/` returns zero hits.
  - `ai-rizz` dry-run produces `.cursor/skills/niko/resources/` populated correctly, and `.cursor/rules/shared/niko/` no longer exists (or is empty).
  - `a16n convert --from cursor --to claude --rewrite-path-refs --dry-run` produces zero `orphan-path-ref` warnings.
- **Docs:** update `memory-bank/systemPatterns.md` "File Organization" to reflect the new rule-vs-resource split.

## Follow-ups

1. `memory-bank-paths.mdc` rule-vs-resource classification (separate creative question if genuinely ambiguous; otherwise a simple edit).
2. Consider whether `.cursor/rules/shared/niko/` should be deleted entirely from `ai-rizz`'s sync output once migration lands, or retained with backward-compat shims for external consumers of specific `.mdc` paths.
