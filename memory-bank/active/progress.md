# Progress

Add an executable-versus-prose scope carve-out to `always-tdd.mdc` so TDD stops requiring invented assertions on human-facing prose, and amend `niko-preflight` so it fails plans that still propose such tests. Specified by [issue #95](https://github.com/Texarkanine/.cursor-rules/issues/95).

**Complexity:** Level 2

## 2026-07-29 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Read the persistent memory bank files and located the source of truth for both target artifacts: `rules/always-tdd.mdc` and `rulesets/niko/skills/niko-preflight/SKILL.md`.
    - Confirmed operator intent against issue #95 and wrote `projectbrief.md`.
    - Classified the task as Level 2.
* Decisions made
    - Level 2 rather than Level 3: the issue supplies the design, so a creative phase would be ceremony. The two edits are prose-only and independently valid, which makes the change self-contained.
    - Edit only `rules/` and `rulesets/`. The `.cursor/` and `.claude/` trees are generated copies.
    - Write no new tests for this change, which is the carve-out applied to itself. The repo's `make test` covers ruleset symlinks and README links only.
* Insights
    - `niko-preflight` step 6 "Completeness Precheck" is a second source of prose-test pressure that issue #95 does not mention. Amending only step 2 would leave the guard contradicting a sibling check in the same file.
    - This task is a live test of its own deliverable: it is a prose-only change that must pass the very preflight guard it installs. If the wording is too loose, preflight will not catch a bad plan; if too strict, preflight will fail this task's own correct plan.

## 2026-07-29 - PLAN - COMPLETE

* Work completed
    - Surveyed TDD pressure across the niko skills and confirmed the sibling TDD rules need no carve-out, being globbed to `*Test.java` and to shell scripts.
    - Read `rules/prompt-authoring/SKILL.md` to author the rule prose against the repo's own standard.
    - Wrote a 5-step plan across 2 files into `tasks.md`, with behaviors, challenges, and pre-mortem.
* Decisions made
    - The boundary is behavioral, not a file taxonomy: the decisive gate asks what makes a test go red, because a taxonomy is what the prior agent relabeled its way around.
    - Preflight step 6 must be amended alongside step 2, or the guard contradicts a sibling check in the same file.
    - No automated tests, which is the carve-out applied to itself; the existing structural suite still runs.
* Insights
    - The prior failure's rationalization, "structural markers not prose," is an argument against artifact-kind boundaries in general. Only a rule about the test's failure mode survives relabeling.

## 2026-07-29 - PREFLIGHT - PASS

* Work completed
    - Ran all seven preflight checks against the plan; wrote `PASS` to `.preflight-status`.
    - Amended the plan twice: renamed the new heading to `## What TDD Governs`, and corrected the generated-tree dependency note with evidence.
* Decisions made
    - Passed the blocking TDD Plan Encoding check while recording that its current wording cannot cleanly authorize the pass. The FAIL condition targets a pretext, and this plan instead argues its units are out of scope and says why. The ambiguity between those two is the defect under repair, and it was resolved toward the intent of the change.
    - Do not touch the tracked `.cursor/` copies. Feature commits here touch `rules/` alone; the generated tree is re-synced under separate `chore(dev): ai-rizz sync` commits, and `ai-rizz` reads the remote anyway.
    - Applied one advisory: name the gate **change-detector** in both files so it can be cited without restating it.
* Insights
    - Fixing a rule while governed by it produces a real deadlock, not just an awkward moment: had preflight failed this plan, the only compliant repair would have been to invent the very prose tests the task prohibits. That is the strongest available evidence that issue #95 describes a genuine defect.
    - The `.cursor/` copies of the target files are tracked, but staleness between a feature commit and the next sync commit is the repo's normal state, not a defect.

## 2026-07-29 - BUILD - COMPLETE

* Work completed
    - Added `## What TDD Governs` to `rules/always-tdd.mdc` and rescoped the opening paragraph from "all code changes" to changes in executable behavior.
    - Amended `rulesets/niko/skills/niko-preflight/SKILL.md` at step 2 (scope clause, executable-scoped ordering FAIL, new change-detector FAIL), step 6 (executable qualifier), and step 9 (fix instruction for both directions).
    - Ran `make test`: passes. Verified the suite is not vacuous by reading `check-ruleset-symlinks.sh`. No linter errors.
* Decisions made
    - Used a single `## What TDD Governs` section with no leaf sub-headings, keeping **change-detector** greppable through bold at its definition rather than through a heading. `markdown-style.mdc` warns against leaf headings where paragraphs suffice.
    - Kept the pre-existing `.cursor/rules/shared/always-tdd.mdc` pointer at preflight line 27 and made the new FAIL condition self-contained instead, so the guard holds even where that path does not resolve.
* Insights
    - The build closed the ambiguity preflight had to judge around. The amended step 2 now names "rule and skill wording" as carrying no test-before-code obligation, so a future task shaped like this one gets a clean pass instead of a reasoned override.
    - Rescoping the opening sentence mattered more than adding the new section. An agent that reads "All code changes" first will carry that framing into a section that contradicts it.
