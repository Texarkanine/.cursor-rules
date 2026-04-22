---
task_id: niko-commit-autonomy
complexity_level: 3
date: 2026-04-22
status: completed
---

# TASK ARCHIVE: Niko Commit Autonomy

## SUMMARY

Addressed a conflict between Cursor’s base Shell-tool injection (“NEVER commit unless the user explicitly asks…”) and Niko workflows that *prescribe* commits at phase boundaries and in `/nk-save`. The team designed and implemented a **general Niko principle**—**workflow invocation is explicit consent**—using **first-person operator voice** in an inline header duplicated at every commit-prescribing entry point, so the authorization sits in the same reading context as the sub-command the agent is executing (mitigating the “`/niko-build` is not `/niko`” failure mode).

**Shipped (branch `let-me-git-on-with-it`, commits including `6e695d1`, `7171c9d`, `c504f6a`):** the canonical header text was added to **six** files under `rulesets/niko/skills/`: `level{1..4}/level{N}-workflow.md`, `nk-save/SKILL.md`, and `niko-creative/SKILL.md`. A large orthogonal change—migrating many reference `.mdc` files into `.cursor/skills/shared/niko/references/**/*.md`—landed in the same build commit; it was not in the original plan (see **PROCESS IMPROVEMENTS**).

**Planned but not in initial build (later or partial):** contributor doc `rulesets/niko/skills/niko/references/core/invocation-consent.md`; `memory-bank/systemPatterns.md` was updated at some point with a Niko System Patterns bullet for this principle (see **REQUIREMENTS** / **OUTCOME**).

**Process caveat:** PREFLIGHT and formal QA were skipped; behavioral canaries (B1–B5) were not run before reflect/archive. This archive records that gap honestly.

## REQUIREMENTS

| Source | Requirement |
|--------|-------------|
| Project brief / tasks | **Minimal surface area;** **dissolve** the base-prompt conflict (satisfy “explicitly asked”) rather than **override** it. |
| | **Bounded scope:** only Niko-prescribed moments—not arbitrary commits. |
| | **Creative phase** for phrasing and placement. |
| | **Validation strategy** in the design (behavioral + structural). |
| Creative (iteration 3) | **C6a:** per-file **inline** full text at each commit-prescribing site; **6 files** (4 level workflows + `nk-save` + `niko-creative`); first-person operator voice. |
| | **Supporting:** contributor `invocation-consent.md` + `systemPatterns` bullet. |

**Outcome note:** The reflection file stated the `systemPatterns` bullet and contributor doc were **not** done. The repository’s `memory-bank/systemPatterns.md` now documents **Workflow Invocation is Explicit Consent** under Niko System Patterns; the standalone contributor doc may still be missing—verify in tree if needed.

## IMPLEMENTATION

### Mechanism (final)

**Canonical header (verbatim as placed):**

> **Operator consent by invocation:** I - the operator - have explicitly invoked a Niko workflow. Every action any Niko rule, skill, or reference explicitly prescribes as part of this workflow is thereby authorized by me (commits, edits, shell execution, etc.). You have standing permission to perform the prescribed actions without seeking secondary confirmation. **Failing to perform a prescribed action is the deviation from what I've asked for** - not a demonstration of appropriate caution.

**Why this shape**

- **First-person operator voice** to satisfy “user explicitly asked” on the base prompt’s terms.
- **“Any Niko rule, skill, or reference”** matches the Niko taxonomy after reference migration.
- **“Explicitly prescribes as part of this workflow”** bounds scope without a heavy escape-hatch paragraph.
- **“Failing to perform a prescribed action is the deviation…”** targets the “too proactive” / overcaution pressure without naming Cursor.

### Options considered (creative phase, condensed)

- **C1 Named Exception** — Rejected: quotes Cursor; ages poorly; violates “not a harness patch.”
- **C2 Core bullet only** — Rejected as sole fix: sub-command context may not load always-on core.
- **C3 git-safety extension** — Rejected: wrong concern cluster.
- **C5 user-level** — Rejected: not versioned with Niko.
- **C6 variants:** **C6a** chosen (inline duplicate text in 6 files). **C6b** (Load: canonical) deferred—acceptable refactor if drift appears. **C6c** (every `/niko-*` skill) rejected as too broad. **C6d** (core + per-file) held as escalation if canary fails.

**Design v2 reframe (operator):** the rule is a **portable Niko principle**—“invocation is consent for everything the workflow prescribes”—not a Cursor-specific exception.

**Observed failure mode:** agents treated `/niko-build` (etc.) as not inheriting consent from “invoking Niko,” so consent must be **co-located** with the file the agent is reading for that sub-command.

### Key files touched

- `rulesets/niko/skills/niko/references/level{1,2,3,4}/level{N}-workflow.md` — header at top; phase mappings still list archive paths under `.cursor/skills/shared/...`.
- `rulesets/niko/skills/nk-save/SKILL.md`
- `rulesets/niko/skills/niko-creative/SKILL.md`
- Build commit also carried **~50-file** reference migration (`.cursor/rules/shared/niko/...` → `.cursor/skills/shared/niko/references/...` and related); dominant fraction of the diff per reflection.

## TESTING

| Planned | Result |
|--------|--------|
| **B1–B5** (behavioral canaries) | **Not run** before reflect/archive. |
| **PREFLIGHT** | **Skipped.** |
| **QA (`/niko-qa`)** | **Skipped;** no `memory-bank/active/.qa-validation-status`. |
| **S1–S4** (structural) | Partially addressable; no formal run recorded. |
| Follow-up fix commits | `7171c9d` (typo), `c504f6a` (reference fix) — text/structure, not behavioral proof. |

**Load-bearing gap:** the deliverable is **agent runtime behavior**; without B1 (minimal L1 run → commit at prescribed point), success is unproven. Treat **B1** as the first follow-up for anyone merging or relying on this change.

## LESSONS LEARNED

- **First-person operator voice** is the load-bearing design choice; placement (C2 vs C6) is secondary for harness satisfaction.
- **Six short duplicates** are an intentional trade-off for grep-verifiability vs **C6b** single source of truth.
- **Sub-command isolation** of context means co-location with the prescribing file beats a distant always-on rule for this class of problem.
- **Resolved creative decisions must be written back** to `tasks.md` / `progress.md` before build—otherwise the plan drifts and scope can slip.
- **“Supporting artifacts”** (contributor doc, systemPatterns) should be **numbered implementation steps**, not a separate creative-only list—or they fall through.
- **Skipped preflight** on a “small” build still allowed a **large bundled migration** in the same commit as the 6 header insertions.

## PROCESS IMPROVEMENTS

- After a **collaborative creative close**, add an explicit **reconcile plan** step before build (checkboxes, phase log, implementation steps).
- For **rule-authoring tasks whose success is behavior**, treat **QA / B1** as blocking for “done,” not optional.
- **Preflight** as cheap insurance when creative resolution was informal or the build might bundle unrelated work.

## TECHNICAL IMPROVEMENTS

- Run **B1** and optionally B3/B4 on primary model(s) after merge.
- Add **`invocation-consent.md`** if contributors need a single place explaining intentional duplication (still recommended in creative).
- If phrasing drifts across six files, consider **C6b** (canonical file + one-line pointers).

## NEXT STEPS

1. **B1 canary** (L1 Niko on a throwaway branch): confirm agent commits without re-ask at the prescribed point.
2. **Optional:** add `rulesets/niko/skills/niko/references/core/invocation-consent.md` if not present.
3. **Optional:** B3/B4 negative tests; cross-model (B5) if multiple models matter for the operator.
4. Reconcile any **open PR** with the branch named in `activeContext` before merge (verify current branch/PR in Git).

---

## Inlined: problem statement (from project brief)

Cursor’s base agent prompt (Shell tool) includes a strong instruction to never commit unless the user explicitly asks, which can override workspace-prescribed Niko commits. The fix must **not** be an adversarial override; it must read as the operator’s standing authorization for **only** what Niko workflows explicitly prescribe.

## Inlined: reflection cross-phase summary

- **Plan → build:** OQ-1 was resolved in creative iteration 3, but `tasks.md` / `progress.md` were not fully reconciled; informal build followed. **Scope expansion:** large reference migration bundled with the six headers—judge as appropriate for the project; preflight would have forced explicit acknowledgment.
- **Creative → build:** two supporting artifacts (contributor doc, systemPatterns) were at risk; systemPatterns in-repo now contains the pattern bullet per current `memory-bank/systemPatterns.md`.
- **QA absence:** cannot distinguish “shipped” from “works” until B1 runs.

(Full original reflection: was in `memory-bank/active/reflection/reflection-niko-commit-autonomy.md`, now subsumed by this archive.)

## Inlined: creative “Decision” (iteration 3)

- **C6a**, six files, inline full text; no niko-core bullet in first pass; C6d as escalation.
- Rejected: C1, C2 alone, C3, C5, C6c, C6d initially, C6b for first pass.
- **Supporting artifacts** listed: `invocation-consent.md` + `systemPatterns` bullet (see **NEXT STEPS**).

(Full option matrices and long-form v2 canonical wording: was in `memory-bank/active/creative/creative-commit-autonomy.md`, summarized above; this archive is the standing record.)
