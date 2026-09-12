# Current Task: l4-preflight-altitude

**Complexity:** Level 3

## Component Analysis

Draft only — implementation plan waits on the operator's mechanism choice.

### Affected Components
- **niko-preflight skill**: currently one workflow that loads `tasks.md` and applies TDD Plan Encoding (including the word "milestone") plus file-level Completeness. Does not load `milestones.md`.
- **L4 plan + workflow**: spawn the same `/niko-preflight` skill after writing the milestone list; say preflight "validates the milestone list" without stating altitude.
- **milestones.mdc + level4-plan.md**: quality criteria and a format contradiction (plan Step 5 wants L-estimates on `milestones.md`; mdc forbids notes/sub-bullets on checklist lines). Cross-milestone invariants already belong in `milestones.md` as a section, not as checklist notes.
- **`/niko` Step 2a**: deletes `tasks.md`, `activeContext.md`, `progress.md`, creative, troubleshooting, and status files; preserves `milestones.md`, `projectbrief.md`, `reflection/`. Anything a later milestone worker needs must survive that cut.
- **L2/L3 preflight spawn sites**: identical "only instruction you add is `Run the /niko-preflight` skill`" line. Sub-runs keep `milestones.md` while `progress.md` Complexity is L1/L2/L3.

### Cross-Module Dependencies
- L4 Plan → writes `milestones.md` → spawns Preflight → operator review → `/niko` classifies first unchecked milestone → sub-run Plan/Preflight/Build. Sub-run Preflight must keep the L2/L3 bar.
- Preflight status contract (`preflight-status.mdc`, `.preflight-status`, judge-and-report, four strings) is shared. Any new skill must not grow a second glossary.

### Boundary Changes
- Public operator surface may stay `/niko-preflight` or add a second slash skill, depending on the chosen mechanism.
- Spawn-line identity across L2/L3/L4 is a grep-verifiable contract; a new L4 skill would change the two L4 spawn sites on purpose.

## Open Questions

- [ ] **How should L4 preflight be structured?** → Unresolved: awaiting operator choice among A (new skill), B (branch in SKILL.md), C (L4 routing), D (same skill + extracted L4 reference), and placement W1–W4. See `memory-bank/active/creative/creative-l4-preflight-mechanism.md`.
