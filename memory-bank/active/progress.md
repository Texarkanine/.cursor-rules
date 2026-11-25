# Progress

Refresh choose-verification-model from current BenchLM scores, place Carbon in S, Neon in A, and Hydrogen in B, leave Argon in A, and flag tier-mates whose scores sit well apart. Finish the hold on draft PR 141.

**Complexity:** Level 2

## 2026-11-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed no active memory bank; the hold lives on draft PR 141 (`google-gasses`)
    - Restated the gas placements and the review-only score flags; the operator approved, and added that Argon stays in A because it is being sunset
    - Classified the work as Level 2: one subsystem, tiers already chosen
* Decisions made
    - Level 2. The change is an update of choose-verification-model, not a new feature across components
    - Continue PR 141 rather than open a second branch
* Insights
    - On 2026-11-19 Hydrogen and Neon were recorded as A in a comment and left unlisted, because a null BenchLM score makes that author exit 2. The operator now places Hydrogen in B, not A

## 2026-11-25 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan for `google-gas-tiers` in `memory-bank/active/tasks.md`
    - Mapped nine shipped-catalog behaviors onto `tests/choose-verification-model/test_shipped.py`
    - Sequenced tiers.toml, then one refresh from `rules/choose-verification-model`, then the score report and the PR 141 body
* Decisions made
    - Carbon is proved S because an Opus author prints it. Neon is proved A by Sol printing it and Opus refusing it. Hydrogen is proved B by Terra printing it and Sol refusing it
    - A null category score stops the listing. No interim score
    - Outliers are 8 or more points from the tier median, or a mean of a single BenchLM category. Flags do not move tiers
    - Push the branch and replace the Hold section. Leave the PR draft
* Insights
    - A two-candidate pool selects the other model whenever it shares the tier, at any score gap. Tier is what those tests lock
    - Carbon in S can review an A Gemini author when the same-tier window is empty. That is the existing next-tier fallback. The plan does not change it

## 2026-11-25 - PREFLIGHT - COMPLETE

* Work completed
    - Ran the Level 2 preflight against `tasks.md`, the shipped catalog, `modelpool.select`, `refresh.py`, live BenchLM data, and `agent --list-models`
    - `.preflight-status` first line: `FAIL (blocking)`
* Decisions made
    - The plan is blocked, not edited: Neon and Hydrogen have no BenchLM agentic, coding, or reasoning score, so refresh adds neither row and the plan's own stop condition fires. Operator guidance on interim scores (or holding them out) is needed, then `/niko-plan`
* Insights
    - The documented onboarding path in `references/refresh.md` (hand-written mapping row with an interim score) is the one the plan forbids
    - Four of the nine new tests pass vacuously before the change, so "all new tests fail" is inaccurate
