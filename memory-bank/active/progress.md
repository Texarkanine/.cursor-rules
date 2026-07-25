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
