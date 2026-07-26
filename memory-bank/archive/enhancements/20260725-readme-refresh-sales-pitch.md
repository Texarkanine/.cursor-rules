---
task_id: readme-refresh-sales-pitch
complexity_level: 2
date: 2026-07-25
status: completed
---

# TASK ARCHIVE: README Refresh — Sell the High-Value Contents

## SUMMARY

Rewrote the root `README.md` as a value-forward pitch with four ruleset "doors" (niko, authoring, script-it, shell) and created the missing `rulesets/script-it/README.md` in sibling style. Shipped to plan; QA passed clean with no fixes. Also closed the follow-up from `20260725-description-rules-and-commands-to-skills` (stale rules-only wording at the root).

## REQUIREMENTS

- Root README leads with value: reader understands what/why within the first screen; pitch, not catalog.
- All four rulesets linked with accurate 1–2-sentence value props grounded in their source docs.
- `rulesets/script-it/README.md` exists, matches sibling README conventions, links resolve.
- Install guidance retained; Structure section names both rules (`.mdc`) and skills (`SKILL.md`) tiers.
- Canonical sources only; `make test` green; prose follows `markdown-style.mdc`.

## IMPLEMENTATION

**Approach:** RED→GREEN against the existing link/symlink checkers, then rewrite the pitch.

1. Scoped one-off link check asserted missing `rulesets/script-it/README.md` (RED) — preflight amendment made this explicit.
2. Created `rulesets/script-it/README.md` (Purpose/Scope for `script-it-instead` + `how-to-script-it-instead`).
3. Rewrote root `README.md`: opening value prop, four ruleset doors, install guidance in the opener, refreshed Structure, preserved Checks and Big Thanks.

**Key files:** `README.md`, `rulesets/script-it/README.md`. No persistent memory-bank updates (nothing invalidated).

## TESTING

- Preflight PASS (one plan amendment: explicit RED step; advisory to extend link checker left unapplied).
- Build: RED confirmed → GREEN after script-it README; `make test` green; root README link check 5/5.
- QA PASS (clean): KISS/DRY/YAGNI/Completeness/Regression/Integrity/Documentation; pitch accuracy spot-checks all traceable to source lines. No fixes required.

## LESSONS LEARNED

- Root `README.md` is permanently outside `check-ruleset-readme-links.sh`'s `rulesets/`-only scope; until the checker is extended, every root-README edit needs a manual link check.
- For docs/pitch tasks, grounding each claim in a quotable source line at plan time makes writing and QA mechanical lookups rather than judgment calls.

## PROCESS IMPROVEMENTS

- Keep the "every value prop traces to a source line" commitment in the plan for future pitch/docs work — it paid for itself at QA.

## TECHNICAL IMPROVEMENTS

- Extend `scripts/check-ruleset-readme-links.sh` (or equivalent) to cover the root `README.md`, closing the standing CI gap flagged as a preflight advisory.

## NEXT STEPS

- Optionally extend the README link checker to include root `README.md` (preflight advisory / standing gap).
