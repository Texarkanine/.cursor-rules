# Tasks

## niko-preflight-qa: Add /preflight command and reposition /qa

**Complexity:** Level 3
**Status:** BUILD COMPLETE (rework from PR review feedback)

### Original Plan
- Create `/preflight` command (pre-build plan validation, L3+, gates `/build`)
- Rewrite `/qa` from pre-build mechanical validation to post-build semantic review (L2+, gates `/reflect`)
- Update all routing: commands, core rules, workflow levels, visual maps, archive cleanup

### Implementation (first pass)
- 34 files modified across commands, core rules, workflow levels, visual maps, archive files, and README
- Net -1,221 lines (removed old PowerShell/Bash mechanical validation, replaced with semantic review)

### PR Review Feedback — Rework Plan

PR #38 received 23 inline review comments from the repo owner. The core concern: **diffs are too large and too noisy for human review**, especially in the visual-maps files. Several files were rewritten when they should have been surgically edited. Secondary concerns: duplication across commands, missing ARCHIVE in workflows, obsolete files not cleaned up, and commands lacking operator-facing output instructions.

#### P0 — Revert and apply surgical edits

These files had sweeping rewrites that make the diff unreadable. Revert each to `main`, then re-apply only the semantic changes needed for preflight/qa repositioning.

1. **Revert `rulesets/niko/niko/visual-maps/van_mode_split/van-mode-map.mdc`**
   - `git checkout main -- <file>`
   - Re-apply: (a) remove old NIKO QA validation section from flowchart, (b) add preflight to workflow overview for L3+ only, (c) update workflow paths to show correct level-dependent routing
   - Fix: preflight must NOT appear for L2 (was inconsistent)

2. **Revert `rulesets/niko/niko/visual-maps/van-mode-map.mdc`**
   - Same approach as above — identical issues (whitespace noise + L2 preflight inconsistency)

3. **Revert `rulesets/niko/niko/visual-maps/qa-mode-map.mdc`**
   - `git checkout main -- <file>`
   - Re-apply targeted edits: (a) update TL;DR to mention post-build semantic review, (b) add new semantic constraints section (KISS/DRY/YAGNI/Completeness/Regression/Integrity/Integration Insight), (c) update main flowchart to show post-build flow and `.qa_validation_status` output, (d) KEEP existing universal checks / memory bank verification sections — they still apply

4. **Revert `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-main.mdc`**
   - `git checkout main -- <file>`
   - Re-apply only: (a) update timing references from pre-build to post-build, (b) update focus from mechanical checks to semantic review, (c) do NOT duplicate content from `/qa` command

#### P1 — Workflow completeness (always archive)

5. **`memory-bank/systemPatterns.md`** — Apply reviewer's suggestion:
   - L1: NIKO → BUILD
   - L2: NIKO → PLAN → BUILD → QA → REFLECT → ARCHIVE
   - L3: NIKO → PLAN → CREATIVE → PREFLIGHT → BUILD → QA → REFLECT → ARCHIVE
   - L4: NIKO → PLAN → CREATIVE → PREFLIGHT → BUILD → QA → REFLECT → ARCHIVE

6. **`rulesets/niko/niko/Core/complexity-decision-tree.mdc`** — Apply reviewer's suggestion: update workflow table to show ARCHIVE for L2+, confirm L1 skips it

7. **Fix L2 vs L3+ preflight inconsistency** — Addressed as part of P0 items 1-2; ensure all workflow diagrams only show preflight for L3+

#### P2 — Reduce duplication

8. **Remove/shrink "Next Steps" in commands** — In `build.md`, `plan.md`, `preflight.md`, `qa.md`, `reflect.md`: replace verbose workflow-navigation sections with a single line deferring to loaded level workflow rules. Gate conditions ("X blocks Y until PASS") stay; procedural "how to run the next command" goes.

9. **Consolidate duplicate dotfile-deletion refs in `archive.md`** — Find the two references to deleting `.qa_validation_status` / `.preflight_status` and merge into one list

10. **Trim QA/Preflight duplication in level workflows** — In `workflow-level3.mdc` and `workflow-level4.mdc`: keep gate logic ("run `/preflight` — blocks `/build` until PASS or ADVISORY"), remove detailed procedural steps that duplicate command content

11. **Nest prerequisites by level in `build.md`** — Convert flat list with inline "For Level 3-4:" to properly nested list grouped by level

#### P3 — Operator output and cleanup

12. **Add "Output to Operator" section to each command** — Each command (`build`, `plan`, `preflight`, `qa`, `reflect`, `archive`) gets a short section specifying what to print for the human when the command completes (summary, result, next step)

13. **Delete `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/rule-calling-help.mdc`** — Nothing references it except its own frontmatter glob

14. **Delete `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/rule-calling-guide.mdc`** — Flagged as obsolete in reflection doc; no active consumers

15. **Update `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/common-fixes.mdc`** — Its main consumers (the deleted van-qa-checks files) are gone. Update to align with semantic QA process since `/qa` command and `van-qa-main` still reference it

### Design Decisions

- **Commands stay as procedural text, NOT flowcharts.** Flowcharts belong in visual-maps. Commands are agent instructions.
- **Gate conditions are duplicated intentionally** in both the command and the workflow level file — this is load-bearing enforcement that needs to be present in both contexts.
- **Detailed "how to run" procedures live ONLY in the command file** — workflow files reference the command, not reproduce it.
- **L1 skips ARCHIVE** — the commit speaks for itself on trivial bug fixes.
- **`.qa_validation_status` still exists** — it was NOT removed by this PR. It's written by post-build `/qa` and gates `/reflect`. The reviewer's question was about whether it was orphaned; it is not.

### Reflection (first pass)
- Complete — see `memory-bank/reflection/reflection-niko-preflight-qa.md`
