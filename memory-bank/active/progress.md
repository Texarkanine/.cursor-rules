# Progress

Remove `CLAUDE.md` from Niko's first-init root bootstrap so init writes only a thin `AGENTS.md`, gated on `AGENTS.md` alone; update the Niko README to match.

**Complexity:** Level 2

## 2026-10-12 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent clarified and approved; project brief written.
* Decisions made
    - Gate on root `AGENTS.md` only (operator); `CLAUDE.md` ignored by bootstrap.
    - Level 2: one subsystem, two canonical files.
* Insights
    - Issue #101 set the both-absent pair; its "CLAUDE.md only" rationale assumed Claude Code ignored `AGENTS.md`, which no longer holds.

## 2026-10-12 - PLAN - COMPLETE

* Work completed
    - Plan in `tasks.md`: rewrite `memory-bank-init.md` bootstrap section for `AGENTS.md` only (drop decision table and `CLAUDE.md` template), update README line 36, verify by grep and `make test`.
* Decisions made
    - Keep the line-28 read-only anti-duplication scan listing `CLAUDE.md` (consumer repos still have them).
    - Add one explicit "init never creates `CLAUDE.md`" sentence against habit-driven shims.
* Insights
    - No executable behavior changes; `always-tdd` names repository bootstrap and skill wording as out of scope.

## 2026-10-12 - PREFLIGHT - COMPLETE

* Work completed
    - Preflight ran the L2/L3 checks against the canonical `rulesets/` files. First line of `.preflight-status`: `PASS WITH ADVISORY`.
* Decisions made
    - No in-phase plan edits (no TDD step swap, no change-detector strike).
* Insights
    - AC 6 (non-draft PR, `/handoff` note) has no tasks.md step; the orchestrating session must do it after QA.
    - `grep -R`/`git grep` also show `always-tdd.mdc:14` (symlinked into `rulesets/niko/`); that hit is expected, not a missed reference.
