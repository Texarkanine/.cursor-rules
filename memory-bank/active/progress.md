# Progress

Add local `make test` and PR GitHub Actions CI that verify (1) all symlinks under `rulesets/` have existing targets and (2) all internal links in `rulesets/**/README*` documents have existing targets — as two separate checks sharing the same scripts entrypoint, with shell scripts following `rules/shell-posix-style.mdc`.

**Complexity:** Level 2

## 2026-07-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Clarified intent with operator (symlink + README link checks; local Makefile/`make test`; GHA invokes same entrypoint; POSIX shell style)
    - Classified as Level 2 Simple Enhancement
    - Created ephemeral memory-bank files
* Decisions made
    - Level 2: self-contained enhancement (new scripts/Makefile/workflow; no architectural change to rulesets packaging)
* Insights
    - Repo currently has no `.github/workflows/`; CI and local test tooling are greenfield for this task

## 2026-07-25 - PLAN - COMPLETE

* Work completed
    - Surveyed repo: no existing Makefile/scripts/test/.github; 16 rulesets symlinks + 3 READMEs with simple inline links
    - Operator clarified: no test framework; layout property checks via scripts + Makefile
    - Wrote Level 2 implementation plan in `tasks.md`
* Decisions made
    - Two scripts + Makefile targets; GHA two jobs each calling a Make target
    - Ignore external/`mailto:`/`#fragment-only` links; strip fragments before path checks
    - Brief root README documentation of `make test`
* Insights
    - Shell ruleset’s shunit2 guidance does not apply when the “tests” are disk-layout assertions

## 2026-07-25 - PREFLIGHT - COMPLETE

* Work completed
    - Validated plan against empty greenfield tooling surface and rulesets layout
    - Amended plan for explicit RED→GREEN per check and optional rulesets-root CLI arg
    - Wrote `.preflight-status` = PASS
* Decisions made
    - Treat check scripts themselves as the layout assertions (no shunit2)
* Insights
    - Optional root arg keeps negative confirmation off the real `rulesets/` tree
