---
task_id: standing-contract-reconcile-guard
complexity_level: 2
date: 2026-08-04
status: completed
---

# TASK ARCHIVE: Standing-Contract Reconcile Guard

## SUMMARY

Tightened the persistent memory-bank reconcile contract so agents catch new standing contracts (shared error identity, test oracles, path layers) instead of false-skipping them as “implementation detail,” while keeping skip-biased doubt for noise. Follows the 2026-07-09 `persistent-file-update-contract` work, which overshot toward silent under-updating. Draft PR: [#104](https://github.com/Texarkanine/.cursor-rules/pull/104).

## REQUIREMENTS

- Edit canonical `rulesets/niko/` only (no `.cursor/` / `.claude/` sync in-task).
- `reconcile-persistent.md`: kill blanket “under-updating is safe / skip confidently”; add standing-contract probe; require per-file skip receipts citing the probe.
- `systemPatterns.mdc`: allow briefing a task-shipped system-wide contract; damage-test gating; no write-when-unsure.
- `techContext.mdc`: process/oracle/assertion changes count; catalog of helpers still out of scope.
- Preserve surgical/anti-noise invariants. Do not encode “omissions are expected by design” as a skip license.
- Out of scope: productContext.mdc (unless forced), ai-rizz regeneration, completeness audits.

## IMPLEMENTATION

**Failure mode:** Instructions preferred silent skip; “materially incomplete” was read as patching wrong paragraphs, not adding missing standing contracts. Escape hatch: “don’t list every library.”

**Canonical files:**

- `rulesets/niko/skills/niko/references/core/reconcile-persistent.md` — probe (per-file, absent/stale), skip receipts, asymmetric skip.
- `rulesets/niko/niko/memory-bank/systemPatterns.mdc` — contract carve-out + damage test; removed “never record what you just built” / “cheap to add later.”
- `rulesets/niko/niko/memory-bank/techContext.mdc` — test-process examples include assert/signal contracts vs catalog.

**Dogfood:** `memory-bank/systemPatterns.md` gained a one-line pointer to the probe + skip receipts.

**Post-reflect:** Ponytail tune cut ScriptError-specific parentheticals and “omissions expected by design” flavor. CodeRabbit review fixes: TL;DR per-file receipts; probe gated on absent/stale in *this* file (`f4dfc88`).

## TESTING

Prose/policy — no executable tests. Verification: tripwire/`rg` checklist + `make test` (ruleset symlinks + README links). Preflight PASS WITH ADVISORY (`.cursor/` lag expected). QA PASS with one clarity fix (probe membership gate).

## LESSONS LEARNED

- A task-global probe inside a per-file loop needs an explicit “belongs in *this* file” gate, or every standing contract looks like it belongs everywhere.
- Task-scoped “if you update nothing, print receipts” breaks the mixed-update path; receipts must be per skipped file.
- “Omissions are expected by design” was operator flavor; written as a rule it reads as a skip license — keep only the hard rule (never contain what doesn’t belong) and the asymmetry (skip fine for narrative, not for a probe-caught contract).
- Corpus check: past reconciliations already use terse per-file verdicts; “under-updating is safe per the rule” appears verbatim as a skip rationalization.
- If standing-contract capture had been foundational in the 2026-07-09 update contract, the probe and asymmetric risk would have shipped then; this task is that retroactive correction.

## PROCESS IMPROVEMENTS

- When fixing an instruction that overshot toward skip, keep the stronger anti-pollution invariant next to the new inclusion path so agents don’t read the carve-out as a completeness invitation.
- Stockroom history of prior reconciliations is useful for tuning agent-facing prose length and vocabulary.

## TECHNICAL IMPROVEMENTS

- Injected `.cursor/` copies still lag until a separate ai-rizz sync after merge/push.
- Follow-on (optional): align any generated copies of reconcile-persistent / guidance rules when syncing.

## NEXT STEPS

- Merge PR #104 when ready; regenerate `.cursor/` in a follow-up chore commit after push.
- None otherwise.
