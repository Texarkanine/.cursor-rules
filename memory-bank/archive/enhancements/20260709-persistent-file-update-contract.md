---
task_id: persistent-file-update-contract
complexity_level: 2
date: 2026-07-09
status: completed
---

# TASK ARCHIVE: Persistent-File Rule Update Contract

## SUMMARY

Amended the three persistent memory-bank guidance rules at their canonical sources (`rulesets/niko/niko/memory-bank/`) so any agent that picks up the glob-attached rule understands both what belongs in each file (briefing altitude, sharpened Avoid lists) and when it may be updated (invalidation-only, surgical fixes, skip confidently). Design was pre-resolved in a standalone creative exploration; build and QA passed on the first pass with no fixes required.

## REQUIREMENTS

- **systemPatterns.mdc**: Add altitude-test Avoid item (subsystem deep-dives); defuse the append invitation in "How to Create"; add a compact generic "When to Update" section between "How to Create" and "Format."
- **productContext.mdc** and **techContext.mdc**: Add proportionate "When to Update" sections with file-appropriate invalidation examples; productContext also gains a small "Avoid" subsection.
- **Authority direction**: No cross-reference to `reconcile-persistent.md` — the rules carry the judgment; reconcile-persistent already loads them for content definition.
- **Tripwire phrases**: "factually wrong" and "materially incomplete" appear verbatim in all three rules (deliberate, grep-verifiable duplication matching `reconcile-persistent.md`).
- **Style & scope**: Prose per `markdown-style.mdc` and prompt-authoring conventions; canonical sources only (`rulesets/`), never `.cursor/` or `.claude/` copies.
- **Out of scope**: Changes to `reconcile-persistent.md`; template guard line (option D) for rule-less harnesses; ai-rizz / a16n regeneration.

## IMPLEMENTATION

**Failure mode addressed:** Session residue at the wrong altitude — agents append task narratives and subsystem deep-dives because rules define creation but not stewardship, and the Avoid list filters triviality rather than altitude.

**Approach (Option B from creative doc):** Inline a compact "When to Update" contract in all three persistent rules plus an altitude test in `systemPatterns.mdc`. Restores symmetry with ephemeral rules (`activeContext.mdc`, `tasks.mdc`) which already had "When to Update" sections.

**Files modified (canonical only):**

- `rulesets/niko/niko/memory-bank/systemPatterns.mdc` — Avoid item 4 (subsystem deep-dives + altitude test); brevity sentence defers to update contract; new "When to Update" section; joined one pre-existing hard-wrapped paragraph for markdown-style compliance.
- `rulesets/niko/niko/memory-bank/productContext.mdc` — new "Avoid" subsection (implementation vocabulary; feature-by-feature accretion); new "When to Update" section.
- `rulesets/niko/niko/memory-bank/techContext.mdc` — new "When to Update" section (existing Avoid list already covered what-belongs adequately).

**Persistent reconciliation:** `memory-bank/systemPatterns.md` gained a surgical note generalizing grep-verifiable duplication (consent header + tripwire phrases) as established repo practice. `productContext.md` and `techContext.md` untouched — nothing invalidated.

## TESTING

No automated test runner for prose artifacts (flagged honestly at plan time). Verification:

- **Preflight PASS** (2 info, 1 advisory): rule consumers (`memory-bank-init.md`, `reconcile-persistent.md`) confirmed additive; canonical ↔ `.cursor` copies in sync pre-edit (drift expected until regeneration).
- **QA PASS**: All 10 acceptance behaviors verified — section ordering, tripwire phrases exactly once per rule, zero cross-references to reconcile-persistent or skill paths, style compliance, no edits outside `rulesets/`. KISS/DRY/YAGNI/completeness/regression/integrity/documentation clean; zero fixes.
- **Self-checks**: `rg` for tripwire phrases and cross-reference absence; linter clean.

## LESSONS LEARNED

- **Glob-attached rules need stewardship, not just creation guidance.** Where a rule has "How to Create" but no "When to Update," out-of-workflow agents invent an append-biased update policy.
- **Verbatim tripwire phrases make deliberate duplication grep-verifiable** — same technique as the consent header. This repo now has two established instances of the pattern.
- **Standalone `/creative` before `/niko` worked well** for a design-heavy-but-small L2 task: the run inherited a settled design and executed without open questions.
- **Scope `rg` searches explicitly** — unscoped `rg` from the workspace root can hang indefinitely in WSL.
- **Four-section skeleton now uniform** across memory-bank rules (File / How to Create / When to Update / Format). A formal statement that this skeleton is the template for future rules is the remaining step toward the foundational-assumption design.

## PROCESS IMPROVEMENTS

- Continue using standalone creative exploration for design-heavy L2 tasks before invoking `/niko`.
- Always scope `rg` to explicit directories in this environment.

## TECHNICAL IMPROVEMENTS

- **Follow-on (option D):** Add a one-line maintenance notice to generated persistent `.md` templates so rule-less harnesses (e.g. `AGENTS.md` pseudo-memory-bank) see the update contract.
- **Deployment:** Regenerate `.cursor/` / `.claude/` copies via ai-rizz / a16n after canonical rule edits.

## NEXT STEPS

- Regenerate `.cursor/` / `.claude/` rule copies when ready (deployment follow-up).
- Consider option D (template guard line) as a separate decision for rule-less harnesses.
