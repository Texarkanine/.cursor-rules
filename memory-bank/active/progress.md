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

## 2026-09-23 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Re-ran the Level 2/3 checks on the revised plan. Confirmed the previous run's four fixes are in the plan
    - Fetched live `leaderboards.json` and the pricing page to test the parsing assumptions
* Decisions made
    - `FAIL (fixable)`: effort must come from the rows' `reasoning_effort` field, with the name parenthetical as fallback. Live Verified has `Gemini 3 Pro` tagged `high` only in that field. Also, the skipped-null stderr warning has no test, and the leaderboards URL is unpinned
    - Advisories: fill tiers before the spawn lines reach `main`, and have the skill say to omit `inherit`. Radical Innovation: an operator-owned tier overlay file that refresh never writes
* Insights
    - SWE-bench rows record effort in a structured `reasoning_effort` field, and the row name does not always repeat it

## 2026-09-23 - PLAN - COMPLETE

* Work completed
    - Pointed effort matching at `reasoning_effort`, with the name parenthetical as fallback
    - Pinned the leaderboards URL and added the Gemini 3 Pro test case
    - Removed the skipped-null warning that had no test
* Decisions made
    - Declined a separate tier file and declined holding the spawn-line edit for a later PR
    - The skill tells the agent to omit `inherit`
* Insights
    - On Verified, `Gemini 3 Pro` is effort `high` only in `reasoning_effort`

## 2026-09-23 - PLAN - COMPLETE

* Work completed
    - Replaced the SWE-bench score with the mean of BenchLM agentic, coding, and reasoning
    - Added interim scores for models that have none of those three categories
    - Pinned the nine spawnable slugs and put them in tier `general`
* Decisions made
    - A missing category is left out of the mean. Composer 2.5 has no reasoning score. Grok 4.7's catalog item includes one
    - Tests live under `tests/choose-verification-model/` so they are not copied with the skill
* Insights
    - BenchLM's public model pages withhold an overall rank for Muse Spark 1.3, Composer 2.5, and Grok 4.7, and still publish the category rows the mean uses

## 2026-09-23 - PREFLIGHT - COMPLETE (FAIL (blocking))

* Work completed
    - Ran the Level 2/3 checks on the third plan revision and confirmed the previous run's fixes are in it
    - Checked the live leaderboards against the Task-tool slug list, checked pricing rows, and read the `ai-rizz` embedded-skill copy path
* Decisions made
    - `FAIL (blocking)`: none of the enabled Cursor models has a row on `Test`, `Verified`, or `Multimodal`. The newest row is from 2026-02-26. Every shipped slug would have a null score, and every pick would exit 2. The fix changes brief requirement 6 or 10, so the operator must choose it
    - Fixable: pin the captured slug list in `tasks.md`. Advisories: pricing cells that are Markdown links, test files shipping to consumers, the parenthetical in the spawn lines. Radical Innovation: rank by a hand-ordered list in each tier instead of external scores
* Insights
    - A benchmark-fed picker needs a staleness check against the models it has to rank. For current frontier models, frontier rows appear only on `Verified`

## 2026-09-23 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Re-ran the Level 2/3 checks on the BenchLM-category revision of the plan
    - Re-fetched the live, pinned `benchlm.ai/data/models.json` and the live pricing page; confirmed all nine spawnable slugs now score and price correctly, resolving the prior `FAIL (blocking)`
    - Confirmed all four prior fixable findings (pinned slug list, pricing-link test behavior, tests moved out of the skill directory, parenthetical spawn-line fix) are present in this revision
    - Independently re-verified Makefile, `.gitignore`, `REUSE.toml`, the CI workflow, all nine spawn sites, and the `illustrate-complexity` symlink/README precedent
* Decisions made
    - `PASS WITH ADVISORY`: two advisories recorded (an untested null-tier-author edge case; a pricing-name exactness note for multi-variant rows), plus one advisory Radical Innovation idea (an optional `--json` decision-trace flag on `pick.py`)
* Insights
    - BenchLM withholds `displayScore`/`overallRank`/`evidenceStatus` for some models while still publishing usable `displayCategoryScores`, which is exactly the gap the revised score formula was designed to use

## 2026-09-23 - BUILD - COMPLETE

* Work completed
    - Shipped `select` and `pick.py`, `build_catalog` and `refresh.py`, and the nine-slug mapping and catalog in tier `general`
    - Pointed the nine QA and Preflight spawn lines and the README at `pick.py`
    - Added a PR job that runs `make test-choose-verification-model`
* Decisions made
    - A null-tier or null-score author exits 2
    - Opus and Sonnet share family `claude`. Both Composer slugs share `composer`. Fast Composer uses its own pricing row
    - The BenchLM fetch sends a User-Agent
* Insights
    - BenchLM returns 403 to urllib's default User-Agent
    - `Composer 2.5 (Fast)` is its own pricing row, so the fast slug does not need an output multiplier

## 2026-09-23 - QA - COMPLETE (FAIL (fixable))

* Work completed
    - Reviewed `select`, `build_catalog`, the shipped catalog/mapping, all nine spawn sites, the README, the CI job, `.gitignore`, and executable bits against the plan and the Test Plan's full behavior list
    - Ran `make test` (27 unit tests plus both shell-script checks, all green) and `reuse lint` (compliant, no `REUSE.toml` edit needed)
* Decisions made
    - `FAIL (fixable)`: `memory-bank/techContext.md`'s Testing Process section was not updated and now misdescribes `make test` as only rulesets layout checks, omitting the new Python 3.11 `unittest` suite
    - One advisory recorded: the one-tier-up fallback's empty-next-tier case is sound but untested and unspecified by the plan
* Insights
    - This task is the first to give the repo an executable-behavior test suite (Python/`unittest`) rather than shell-script layout checks, so the doc gap was easy to miss without explicitly diffing `techContext.md`'s Testing Process claim against the new Makefile/CI content

## 2026-09-23 - BUILD - COMPLETE (QA fix)

* Work completed
    - Updated the Testing Process section of `memory-bank/techContext.md` so `make test` includes the stdlib unittest suite under `tests/`, and the CI job's Python version stays a pointer at the workflow
* Decisions made
    - Left the empty-next-tier advisory untested. QA marked it non-blocking
* Insights
    - The Testing Process sentence is a claim about `make test`, so a new Make target makes it wrong until that sentence moves


