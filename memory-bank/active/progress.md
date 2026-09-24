# Progress

Place an unmatched effort spelling of a catalog model on the scale so `pick.py` can rank the author and choose a reviewer, as laid out in `memory-bank/active/projectbrief.md` and [issue #129](https://github.com/Texarkanine/.cursor-rules/issues/129).

**Complexity:** Level 2

## 2026-09-23 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated issue #129 and received operator approval
    - Wrote the project brief, active context, task stub, and this progress file
* Decisions made
    - Level 2: one subsystem, but the placement rule is still an open design choice, so the plan phase has to choose it before code
* Insights
    - A single-component bug whose correct behavior is unspecified is not a Level 1 minimum fix

## 2026-09-23 - PLAN - COMPLETE

* Work completed
    - Read `modelpool.py`, the shipped catalog, and the pick tests
    - Checked BenchLM `models.json`: model slugs such as `claude-opus-5-5` and `grok-4-7`, no effort spellings
    - Wrote the Level 2 plan in `tasks.md`
* Decisions made
    - Unmatched effort spellings get an in-memory row derived from the stored effort and its score-neighbors
    - A tier boundary keeps the higher tier
    - Enabled synthetics may be printed; the author spelling is printed only by the empty-pool rule
    - `catalog.json` is not given a row per effort
* Insights
    - The issue's "known score" is not on BenchLM. Exit-2-until-a-score-appears would leave the reported command failing

## 2026-09-23 - PLAN - AMENDED

* Work completed
    - Recorded the operator's author-echo rule in the brief and the plan
* Decisions made
    - When the author spelling cannot be placed, `select` returns that spelling and the process exits 0
    - The skill stays a thin caller. It does not tell the agent to pick a reviewer after a non-zero exit
    - An unplaceable reviewer slug still exits 2. A stored author row with a null tier or null score still exits 2
* Insights
    - The script is the whole picking policy. An agent should not finish a decision the script refused to make

## 2026-09-23 - PREFLIGHT - COMPLETE

* Work completed
    - Ran the seven Level 2 default-preflight checks against `modelpool.py`, `pick.py`, the shipped catalog and mapping, and all three test files
    - Verified the shipped-command fixture resolves against the shipped catalog (one exact key, two one-sibling placements)
    - Traced every `modelpool` consumer; confirmed only `test_unknown_author_slug_exits_2` changes behavior and its rewrite is scheduled
    - Wrote `.preflight-status`: PASS WITH ADVISORY
* Decisions made
    - No in-phase plan edits: TDD ordering was already correct and no change-detectors were scheduled, so neither the swap nor the strike applied
    - Three advisories recorded, none blocking: sibling anchors should say "stored rows only"; `select`/`main` docstrings go stale; the both-siblings interpolation branch is unreachable with any refreshable catalog
* Insights
    - The plan's mitigation notes can disambiguate a spec sentence that is incomplete when read alone - but the sentence an implementer codes from is still the right place for the qualifier

## 2026-09-23 - BUILD - COMPLETE

* Work completed
    - Added `place_effort` and `_expand_effort` and taught `select` to rank in-memory effort rows
    - An author spelling that cannot be placed is printed and the process exits 0
    - Wrote the slug-identity paragraph in `references/refresh.md`
    - `make test`: 55 tests OK
* Decisions made
    - Effort-source rows are not siblings or score-neighbors
    - Kept the both-siblings interpolation and tested it
    - `SKILL.md` gained no exit-2 branch
* Insights
    - A stored row inside the gap to the next model is the far neighbor, so a nudge test has to land on a row placement is not allowed to treat as a neighbor

## 2026-09-23 - QA - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Reviewed `place_effort`, `_expand_effort`, `select`, `main`, `refresh.md`, and both test files against the plan and brief
    - Confirmed 55 tests OK, `SKILL.md` untouched, `catalog.json` gains no rows
    - Wrote `.qa-validation-status`: PASS WITH ADVISORY
* Decisions made
    - PASS: all seven semantic checks hold; the one advisory (unreachable `author_key` guard in `select`) does not block acceptance
    - Preflight advisories A and B verified closed in code; C kept with a test as allowed
* Insights
    - The unreachable guard is the only dead branch the build added; everything else is exercised by a named test behavior

## 2026-09-23 - REFLECT - COMPLETE

* Work completed
    - Compared the brief and the plan with the build and the QA pass
    - Wrote `memory-bank/active/reflection/reflection-effort-variant-slug.md`
    - Left `productContext.md`, `systemPatterns.md`, and `techContext.md` unchanged
* Decisions made
    - The suffix parser stays. A stem-plus-effort catalog would be a different task
* Insights
    - A skill branch on exit 2 is a second picker. The script is the policy

## 2026-09-23 - OPERATOR CORRECTION

* Work completed
    - Removed `place_effort`. `model_key` strips effort. Catalog keys are stems. Rows set `effort_encoded` false
    - Printed reviewer effort comes from the first enabled spelling of that model
    - `make test`: 46 tests OK
* Decisions made
    - Effort is not comparable across families and is not a BenchLM score, so it is not a rank input
    - The candidate list is where the review effort is chosen
* Insights
    - A universal low/medium/high/xhigh ladder invents notches some models do not have, and it invents gaps BenchLM never measured

## 2026-09-23 - OPERATOR CORRECTION - CHECKPOINT

* Work completed
    - Operator asked for a replan: wide BenchLM scores, a tiered catalog of enabled reviewers, place the author on that catalog, then the existing window
    - Checkpointed the effort-is-not-a-score correction before that plan
* Decisions made
    - This correction stays. The replan does not bring back invented effort scores

## 2026-09-23 - PLAN - COMPLETE

* Work completed
    - Wrote the rework plan in `tasks.md` and the Rework section of `projectbrief.md`
* Decisions made
    - `assets/scores.json` holds one BenchLM mean per model. `catalog.json` stays the tiered enabled subset
    - An outside author is placed by that mean among catalog score-neighbors. A boundary keeps the higher tier. The existing window then runs
    - No wide score prints the author and exits 0. A wide score does not make a non-catalog slug a reviewer
* Insights
    - The dead-in-the-water case that remains is an author whose stem is not a BenchLM slug and not a catalog key

## 2026-09-23 - PREFLIGHT - COMPLETE

* Work completed
    - Ran the seven Level 2 default-preflight checks against `modelpool.py`, `pick.py`, `refresh.py`, the shipped catalog and mapping, and all three test files
    - Verified both executable units already order stub-tests before code and no change-detectors were scheduled, so neither the swap nor the strike applied
    - Wrote `.preflight-status`: PASS WITH ADVISORY
* Decisions made
    - No in-phase plan edits: TDD ordering was already correct and no change-detectors were scheduled
    - Three advisories recorded, none blocking: main/refresh test hermeticity for the new scores input; placement distance pinned by example rather than a one-sentence rule; stem-versus-BenchLM-slug punctuation misses echo safely
* Insights
    - The radical sketch (precompute placement.json at refresh so pick is a dict lookup) is a judgment call against the smaller scores.json diff; recorded as advisory only

## 2026-09-24 - BUILD - ABANDONED

* Work completed
    - Creative exploration `memory-bank/active/creative/creative-outside-author-placement.md` resolved to "onboard, don't place"
    - Stopped the build of the placement plan after step 1. Reverted its uncommitted `benchlm_scores` / `scores.json` edits; the patch is kept outside the repo
* Decisions made
    - Tiers are the operator's trust calibration, not a function of score. No tier is ever derived from score neighbors
    - Outside authors are brand-new models, onboarded with a hand tier the hour they ship. The existing author echo covers the gap
* Insights
    - Preflight checks plan shape, not premise: it passed a plan whose tier rule contradicted what tiers mean

## 2026-09-24 - PLAN - COMPLETE

* Work completed
    - Ran `agent --list-models`: 240 slugs collapse to 48 stems, 12 already mapped
    - Rewrote `projectbrief.md` for a superset catalog and `tasks.md` as four units: CLI effort vocabulary, refresh coverage warnings, onboarding data with an operator tier gate, refresh.md policy
* Decisions made
    - Effort vocabulary is the CLI's: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, `max`; an effort may precede `-thinking`
    - Coverage is a refresh warning, not a shipped test, because the listing is per account
    - `pick.py` never calls the `agent` CLI
* Insights
    - The shipped `model_key` already misses live slugs such as `claude-opus-5-5-max` and `gpt-5.6-sol-none`, so an enabled max-effort reviewer exits 2 today

## 2026-09-24 - PLAN - AMENDED

* Work completed
    - Operator directed that refresh fill in catalog rows. Rewrote unit 2 as `parse_listing` + `fill_mapping` and unit 3 as run-refresh-then-review with the tier gate
    - Validated the matching rule against live BenchLM, the pricing page, and the CLI listing: 44 of 48 stems resolve, 12 of 12 existing rows reproduced, 4 real gaps
* Decisions made
    - Price match: pricing-row words (no parentheses) are a subset of display-name words plus family; most words wins. BenchLM match: the one scored slug with the same sorted words
    - Existing mapping rows are never rewritten; unmatched stems are warned, not added
    - A catalog outside the skill is out of scope
* Insights
    - Cursor, the pricing page, and BenchLM order the same model's words differently (`Claude Opus 4.6`, `Claude 4.6 Opus`, `claude-opus-4-6`); word sets match where string transforms do not



## 2026-09-24 - PREFLIGHT - COMPLETE

* Result: `PASS WITH ADVISORY`
    - TDD ordering correct for units 1-2; unit 3 data covered by shipped invariants; unit 4 prose. No plan edits
    - Advisories: refresh.main test hermeticity, interim-score wording, effort-suffix mis-split risk for future stems; radical sketch: refresh prints suggested BenchLM/pricing matches for unmapped stems

## 2026-09-24 - PREFLIGHT - COMPLETE (RERUN)

* Result: `PASS WITH ADVISORY`
    - Units 1-2 test-first; unit 3 covered by shipped invariants; unit 4 prose. No plan edits
    - Confirmed `refresh.py` JSON format matches shipped `mapping.json`, so appended rows keep existing bytes; no existing test calls `refresh.main`
    - Advisories: always pass `dest` when injecting `mapping`; red suite during the tier gate; effort-suffix mis-split risk; interim-score wording. Radical sketch: check in the listing as an asset instead of spawning `agent`

## 2026-09-24 - BUILD - COMPLETE

* Work completed
    - Units 1-4 built test-first; units 2b (`has_fast` from the listing), 2c (tier reminder every run), and 2d (`tiers.toml` with a `never` tier) added at the operator's direction during build
    - Real refresh added 32 rows; 4 stems unrecognized. Operator tiered every listed model in `tiers.toml` (15 on the ladder, 29 `never`)
    - `make test`: 78 tests OK; acceptance commands re-run on the tiered catalog
* Decisions made
    - Tiers are hand-edited TOML read by refresh; machine data stays JSON, so pick needs no TOML
    - `-fast` stays appended from the author's speed and the chosen model's `has_fast`, even off the caller's list
* Insights
    - The pain the operator hit was hand data mixed into generated data, not JSON syntax; separating the two files fixed it
    - A per-effort `-fast` gap was not real: speed is a model parameter, valid at every effort

## 2026-09-24 - QA - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Reviewed the build diff (`modelpool.py`, `refresh.py`, `refresh.md`, the three assets, and the three test files) against the amended plan and brief
    - Confirmed 78 tests OK; acceptance commands 1, 2, and 6 re-run; shipped tiers match `tiers.toml`; mapping and catalog diffs are pure additions
    - Wrote `.qa-validation-status`: PASS WITH ADVISORY
* Decisions made
    - PASS: all seven semantic checks hold. Four advisories (stale `select` docstring on `never`, scalar TOML values, brief criterion 5 wording, one unwrapped docstring line) do not block
* Insights
    - Operator-directed mid-build units (2b, 2c, 2d) were each built test-first, so QA could check them against recorded behaviors like planned units

## 2026-09-24 - REFLECT - COMPLETE

* Work completed
    - Rewrote the reflection for the whole arc: interpolated effort scores, abandoned score placement, superset catalog with `tiers.toml`
    - Reconciled persistent files: `techContext.md` now says the suite needs Python 3.11+; product and system patterns unchanged
* Decisions made
    - QA advisory B (scalar values in `tiers.toml`) left open for the operator
* Insights
    - Plans passed Preflight twice with premises the operator later rejected; for policy tasks, ask what the judgment fields mean before planning

## 2026-09-24 - ARCHIVE - IN-PROGRESS

* Work completed
    - PR #130 review: non-list `tiers.toml` values now warn and skip (`a20f4cd`); 79 tests
    - Leaving Reflect for Archive
