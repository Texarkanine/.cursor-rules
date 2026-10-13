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
