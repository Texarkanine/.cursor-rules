# Progress

## niko-preflight-qa

### First pass (complete)
- [x] Create /preflight command file
- [x] Rewrite /qa command file
- [x] Update command files (build, plan, creative, reflect, archive)
- [x] Update core rules (main, complexity-decision-tree, mode-transition-optimization, memory-bank-paths)
- [x] Update workflow level rules (Level 2, 3, 4)
- [x] Update visual maps (van-mode-map x2, qa-mode-map, van-qa-main, mode-transitions, reports)
- [x] Update archive files (archive-mode-map, archive-basic, archive-intermediate, archive-comprehensive)
- [x] Update README.md workflow diagrams
- [x] QA semantic review — PASS (4 findings fixed)
- [x] Reflection complete

### Rework (PR #38 review feedback) — COMPLETE
- [x] P0: Revert + surgical re-edit van_mode_split/van-mode-map.mdc
- [x] P0: Revert + surgical re-edit van-mode-map.mdc (top-level)
- [x] P0: Revert + surgical re-edit qa-mode-map.mdc
- [x] P0: Revert + surgical re-edit van-qa-main.mdc
- [x] P1: Apply workflow suggestion to systemPatterns.md (always archive)
- [x] P1: Apply workflow suggestion to complexity-decision-tree.mdc
- [x] P2: Remove/shrink "Next Steps" duplication in command files
- [x] P2: Consolidate duplicate dotfile-deletion refs in archive.md
- [x] P2: Trim QA/Preflight duplication in workflow-level3.mdc and workflow-level4.mdc
- [x] P2: Nest prerequisites by level in build.md
- [x] P3: Add "Output to Operator" section to each command
- [x] P3: Delete rule-calling-help.mdc
- [x] P3: Delete rule-calling-guide.mdc
- [x] P3: Update common-fixes.mdc for semantic QA

### QA Semantic Review (rework) — PASS
- [x] Fixed path convention in preflight.md and qa.md (rulesets/ → .cursor/rules/shared/)
- Advisory: van-mode-map files retain inherited stale content from main (intentional per P0 strategy)
- Advisory: .cursor/rules/shared/ copies need sync from rulesets/ source
