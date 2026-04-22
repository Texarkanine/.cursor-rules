# Progress: Niko Commit Autonomy

## Summary

Design a minimal, bounded rule/guidance insertion that pre-authorizes Niko-prescribed commits on the operator's behalf, satisfying Cursor's base prompt's "user explicitly asked" condition rather than attempting to override it. Diagnostic work is already complete (captured in `cursor_request_for_system_prompt_detail.md`); this task is the design+build follow-up.

**Complexity:** Level 3

## Rationale

- Requires **design exploration** (phrasing, placement, scope boundaries) — user explicitly asked for a creative phase. Rules this out of L1/L2 which skip creative.
- **Scope** is small-to-moderate (≈1 new file, possibly a minimal pointer in another), but design decisions dominate.
- **Risk** is non-trivial: a badly-worded pre-authorization could either fail silently (agents still hesitate) or overshoot (agents commit outside Niko boundaries).

## Phase log

- `COMPLEXITY-ANALYSIS` — complete, Level 3 determined.
- `PLAN` — in progress. Plan drafted with one open question (OQ-1: phrasing & placement of the pre-authorization rule). Invoked creative phase for OQ-1.
- `CREATIVE (OQ-1)` — iteration 1, unresolved. Produced five candidate packages (C1–C5) and recommended combined C2+C4. Operator responded with (a) a sixth option they were already considering — per-workflow/per-skill headers — and (b) a major reframe: the rule should be a **general Niko principle** ("invocation is explicit consent"), not a Cursor-specific patch. Also surfaced an empirical failure mode: agents reasoning that `/niko-X` sub-commands don't inherit consent from `/niko`.
- `CREATIVE (OQ-1)` — iteration 2, **unresolved (by design)**. Rewrote creative doc with (1) prose names on every option, (2) C6 with sub-variants (a/b/c/d), (3) generic-principle framing as v2, (4) sub-command failure mode explicitly addressed. New recommendation: **C6d Hybrid** (niko-core bullet + canonical reference file + 5 per-file headers). Seven numbered questions posed. Awaiting operator input.
- `CREATIVE (OQ-1)` — iteration 3, **RESOLVED** (collaboratively with operator). Landed on **C6a** (per-file inline headers) scoped to 6 files: `level{1..4}-workflow.md`, `nk-save/SKILL.md`, `niko-creative/SKILL.md`. First-person operator voice. `tasks.md` Open Questions checklist was not updated at the time; flagged in reflect.
- `PREFLIGHT` — **skipped**.
- `BUILD` — informal. Commit `6e695d1` added the 6 headers and also bundled an orthogonal `.cursor/rules/shared/niko/` → `.cursor/skills/shared/niko/references/` migration (~50 files). Two fix-up commits followed: `7171c9d` (typo) and `c504f6a` (reference fix). Two supporting artifacts from the creative decision did NOT land: contributor doc at `rulesets/niko/skills/niko/references/core/invocation-consent.md` and `memory-bank/systemPatterns.md` bullet.
- `QA` — **skipped**. No canary (B1–B5) run. No `.qa-validation-status` file.
- `REFLECT` — complete with caveat. Reflection at `memory-bank/active/reflection/reflection-niko-commit-autonomy.md` covers plan/creative/informal-build and explicitly notes the skipped preflight/QA as process observations. Awaiting operator input on whether to run the skipped canary + create the missing artifacts before archiving, or to archive as-is with follow-ups tracked separately.
