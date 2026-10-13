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

## 2026-10-12 - BUILD - COMPLETE

* Work completed
    - Rewrote the `memory-bank-init.md` bootstrap section for `AGENTS.md` only; removed the four-row table and the `CLAUDE.md` template.
    - Updated `rulesets/niko/README.md` line 36.
    - `make test` green; grep over `rulesets/` shows only the scan line and the new "never creates `CLAUDE.md`" sentence.
* Decisions made
    - Preflight advisory 3 (paste-in pointer on skip) left for the operator; not in the brief.
* Insights
    - The plan's own grep expectation forgot the sentence the plan added; verify expectations should be derived from the planned text, not the pre-edit state.

## 2026-10-12 - QA - COMPLETE

* Work completed
    - Semantic review of `main...HEAD` against the plan: all planned steps done; AC 1–5 met; `make test` green. Result `PASS` in `.qa-validation-status`; findings in `tasks.md`.
* Decisions made
    - Two non-blocking advisories: the kept symlink sentence is now redundant (Requirement 3 keeps it); AC 6 (PR and `/handoff`) is still for the orchestrating session.
* Insights
    - No other canonical Niko file describes the pair, so the two-file edit is complete.

## 2026-10-12 - REFLECT - COMPLETE

* Work completed
    - Reflection written; persistent-file reconciliation skipped all three (receipts in session output).
* Decisions made
    - Preflight advisory 3 recorded as a separate product question for the operator.
* Insights
    - A compatibility rule can state the harness behavior it depends on; issue #101's "both absent" gate did not.

## 2026-10-12 - POST-REFLECT - PR OPENED

* Work completed
    - Non-draft PR #135 opened on `niko-no-CLAUDE.md` (AC 6); `/handoff` baton written.
* Decisions made
    - None.
* Insights
    - None.
