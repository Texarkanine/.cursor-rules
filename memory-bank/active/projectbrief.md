# Project Brief

## User Story

As a Niko operator, I want the persistent memory-bank reconciliation contract to catch new standing contracts (without inviting changelog noise) so that architectural conventions like shared error identity and test oracles land in `systemPatterns` / `techContext` instead of dying in ephemeral creative docs.

## Use-Case(s)

### Use-Case 1

An agent finishes a task that introduced a shared contract (typed errors, test oracles, path layers). On reconcile, the standing-contract probe forces a surgical update to the matching persistent file — not a silent skip rationalized as “implementation detail.”

### Use-Case 2

An agent finishes ordinary work that invalidated nothing lasting. It prints a one-line skip receipt per file citing the probe, and leaves the high-level overview untouched. Missing things remain acceptable; pollution does not.

## Requirements

1. Edit canonical sources only under `rulesets/niko/` (not `.cursor/` / `.claude/`).
2. In `reconcile-persistent.md`: replace blanket “under-updating is safe / skip confidently” with asymmetric risk (skip OK for narrative/history; not harmless for new standing contracts); add a standing-contract probe after compare; require visible skip receipts that cite the probe.
3. In `systemPatterns.mdc`: soften “never record what you just built” so task-shipped system-wide contracts can still get a briefing paragraph; keep damage-test gating — do not invent write-when-unsure.
4. In `techContext.mdc`: extend When to Update so process/oracle/assertion-contract changes count, with explicit contrast vs listing every helper.
5. Preserve anti-noise invariants: surgical edits only; no feature dumps; no cataloging every script/module.
6. Noise is worse than omission: the fix targets false “implementation detail” skips of standing contracts, not completeness. Hard rule remains that persistent files must never contain content that does not belong. Do not encode “omissions are expected by design” as a standing skip license for maintainers (operator flavor, not a rule).

## Out of Scope

- Regenerating `.cursor/` / `.claude/` via ai-rizz / a16n in this task.
- Broadening update policy toward write-when-unsure or comprehensive audits.
- Changes to productContext.mdc unless tripwire/skip-receipt consistency requires a minimal touch.
