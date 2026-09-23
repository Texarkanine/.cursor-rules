# Progress

Ship the `choose-verification-model` skill: a stdlib Python picker and a catalog refresh, then point Niko QA and Preflight at the picker so verification-model choice is a script run instead of an inference turn.

**Complexity:** Level 3

## 2026-09-23 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated the picker, the refresh, the three boards, and the scored-effort rule
    - Recorded the skill name `choose-verification-model`
    - Classified the task as Level 3
* Decisions made
    - Level 3, because the feature spans the skill, two executables, the catalog, the mapping, and the existing QA and Preflight selection text, and the selection rule is already specified
* Insights
    - Published SWE-bench rows name an effort only on Verified, and only as `(high)` or `(medium)`

## 2026-09-23 - PLAN - COMPLETE

* Work completed
    - Mapped the skill, the symlink into the niko ruleset, the nine spawn lines, and the README tip
    - Wrote the pick and refresh behaviors, the catalog schema, and the TDD steps
* Decisions made
    - No creative phase. The selection rule, the three boards, and the scored-effort rule were already specified
    - Tests are stdlib unittest beside the skill, run from Make
    - A reviewer slug missing from the catalog is a hard error, so the shipped mapping covers the captured Cursor slug list
* Insights
    - The spawn clause has to name `pick.py` beside `SKILL.md`. A `rules/` path would be wrong in a project that only installed the niko ruleset

## 2026-09-23 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Ran the Level 2/3 preflight checks against `tasks.md`: TDD ordering, convention compliance, dependency impact, conflict detection, and completeness
    - Cross-checked all nine spawn sites via grep, the `illustrate-complexity` symlink precedent, `REUSE.toml`, `.gitignore`, and `.github/workflows/rulesets-links.yml`
* Decisions made
    - `FAIL (fixable)`: PR CI (`rulesets-links.yml`) never runs the new Make target the plan adds, so the new Python tests would not gate PRs; the plan hardcodes `python3` into shipped rule text without covering `techContext.md`'s Windows/PowerShell requirement
    - Recorded two smaller fixable/advisory findings (`.gitignore` `__pycache__`, README supplementary-rules bullet) and one advisory Radical Innovation idea (auto-seed tiers from score quantiles on first refresh)
* Insights
    - The repo's "CI mirrors Make targets 1:1" convention (`techContext.md`) is easy to violate silently: adding a Make target without a matching CI job leaves it unenforced in PRs

## 2026-09-23 - PLAN - COMPLETE

* Work completed
    - Added a CI job, a `__pycache__/` gitignore entry, Bash and PowerShell invocations, and a README supplementary bullet to the plan
* Decisions made
    - Spawn lines name Python 3 and leave the interpreter binary to `SKILL.md`
    - Declined auto-seeding tiers from score quantiles
* Insights
    - A `python3` literal in a shipped rule fails the repo's PowerShell-and-Bash rule even when this machine has `python3`
