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
