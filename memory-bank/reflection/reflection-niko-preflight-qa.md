# Reflection: Niko Preflight/QA Refactor

**Task ID:** niko-preflight-qa
**Date:** 2026-02-17
**Complexity:** Level 3 (Intermediate Feature)
**Branch:** niko-preflight-qa

## Summary

Restructured the Niko workflow system by creating a new `/preflight` command (pre-build plan validation for L3+ tasks) and completely rewriting `/qa` from a pre-build mechanical validation step to a post-build semantic review step. Updated all workflow routing, visual maps, core rules, and level-specific workflow files to reflect the new command positions:

- **L1:** `/niko` -> `/build` -> `/reflect` -> `/archive`
- **L2:** `/niko` -> `/plan` -> `/build` -> `/qa` -> `/reflect` -> `/archive`
- **L3+:** `/niko` -> `/plan` <-> `/creative` -> `/preflight` -> `/build` <-> `/qa` -> `/reflect` -> `/archive`

**Scope:** 34 files touched (25 committed + 9 QA fixes), net -1,221 lines (old mechanical validation code removed, replaced with leaner semantic review content).

## What Went Well

1. **Plan-driven execution was effective.** The user provided a detailed plan with draft content for both new commands and specific file-by-file modification instructions. This eliminated ambiguity and allowed systematic execution across 25+ files without rework.

2. **Gate mechanism is clean.** The `.preflight_status` and `.qa_validation_status` status files provide simple, file-based gates that are easy to check and clear. Each gate has a clear owner (command that creates it), a clear consumer (command that checks it), and a clear cleanup path (archive).

3. **QA review caught real issues.** Running the newly-defined `/qa` semantic review process against its own implementation found 4 blocking issues that the build phase missed:
   - Stale workflow in `systemPatterns.md`
   - Stale "NIKO QA MODE" diagram node in `van-mode-map.mdc`
   - Obsolete `rule-calling-guide.mdc` still referencing deleted mechanical checks
   - 471 lines of dead code in `van-qa-checks/` directory

4. **Net negative LOC.** Replacing the old mechanical validation (PowerShell/Bash scripts for dependency checks, config validation, environment checks, build tests) with semantic review constraints resulted in significantly less code overall.

## Challenges Encountered

1. **Large file rewrites.** The `van-mode-map.mdc` files (~900 lines each) contained extensive embedded PowerShell/Bash scripts. Incremental edits with the Edit tool couldn't cleanly remove hundreds of lines of old code block content, requiring full file rewrites with the Write tool.

2. **Near-identical file pairs.** The `van-mode-map.mdc` exists in two locations (top-level and `van_mode_split/`) with subtle differences. Similarly, `qa-mode-map.mdc` and `van-qa-main.mdc` overlap significantly. Each pair required separate, careful edits to maintain their individual characteristics while updating the shared content.

3. **Cross-file consistency.** With 25+ files sharing overlapping workflow descriptions, phase counts, routing rules, and mermaid diagrams, keeping everything consistent required systematic grep verification after all edits were complete.

4. **Context window pressure.** The task spanned two conversation sessions due to context window exhaustion. The continuation relied on a session summary to reconstruct state, which worked but added overhead.

## Lessons Learned

1. **The QA process validates itself.** Dogfooding the `/qa` command against its own implementation proved its value immediately — it caught stale references, dead code, and a regression that manual review during the build phase missed. The semantic constraints (especially Regression and Integrity) are effective at catching things that aren't compilation errors but are genuine quality issues.

2. **Mechanical validation was replaced, not lost.** The old QA did dependency checks, config validation, environment checks, and build tests. These are still valuable but are now assumed to be handled by the build toolchain itself (lint, build, test commands). The new `/qa` catches what those tools cannot: over-engineering, incomplete implementations, pattern violations, and implementation debris.

3. **File-based gates are simple and robust.** Using `.preflight_status` and `.qa_validation_status` as simple text files in the memory bank is a good pattern — it's debuggable (you can `cat` the file), it survives context resets, and it's trivially cleared during archive.

4. **Archive cleanup must be updated when adding new ephemeral files.** The `.preflight_status` file was initially missing from all archive cleanup references. This was caught during verification but highlights that any new ephemeral file added to the workflow must be traced through to the archive cleanup path.

## Process Improvements

1. **Run `/qa` earlier in multi-file refactors.** For large cross-cutting changes, consider running a partial QA review after completing each logical group of files rather than waiting until the entire build is complete.

2. **Grep-based verification is essential for cross-file consistency.** The verification step (grep for old patterns, grep for new patterns, confirm no stale references) should be a non-negotiable part of any workflow refactor.

## Technical Improvements

1. **Integration Insight (advisory, not actioned):** The `van_mode_split/` architecture creates maintenance burden through near-identical file pairs. A future refactor could consolidate `van-mode-map.mdc` into a single canonical version, and extract shared QA semantic constraints into a single reusable definition rather than repeating them across `qa.md`, `qa-mode-map.mdc`, and `van-qa-main.mdc`.

## Next Steps

- Proceed to `/archive` when ready to finalize
