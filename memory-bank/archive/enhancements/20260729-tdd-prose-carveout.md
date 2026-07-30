---
task_id: tdd-prose-carveout
complexity_level: 2
date: 2026-07-29
status: completed
---

# TASK ARCHIVE: TDD executable-versus-prose carve-out and preflight guard

## SUMMARY

Added a scope boundary to `always-tdd.mdc` so TDD governs executable behavior rather than all changes, and amended `niko-preflight` so its blocking TDD check rejects plans that schedule assertions on prose. Delivered against [issue #95](https://github.com/Texarkanine/.cursor-rules/issues/95); QA passed after one trivial fix. Shipped on draft PR [#98](https://github.com/Texarkanine/.cursor-rules/pull/98), with post-reflect review feedback partially addressed.

## REQUIREMENTS

- `always-tdd.mdc` states an executable-versus-prose carve-out: TDD governs executable behavior; it does not govern human-facing prose or policy artifacts.
- The carve-out forbids inventing string, heading, or checklist assertions to satisfy TDD, and names alternatives: review, a purpose-built gate, or nothing.
- `niko-preflight` fails plans that propose tests locking prose, policy, or markdown content, with a fix instruction to remove them.
- `niko-preflight` does not fail plans that correctly omit TDD ordering for non-executable units.
- Constraint: carve-out must resist the prior failure mode (relabeling prose assertions as "structural markers") and must not sweep legitimate packaging/install-contract tests out of scope.

## IMPLEMENTATION

**Boundary design:** Behavioral, not a file taxonomy. The decisive gate is the **change-detector** question: if the only way to make the test fail is for someone to deliberately edit the artifact it asserts on, it is a change-detector, not a test. Artifact-kind lists remain for fast recognition; the gate is what survives relabeling.

**Files modified:**

- `rules/always-tdd.mdc` — `## What TDD Governs`; change-detector gate; document-assert cue; opening paragraph rescoped from "all code changes" to executable behavior.
- `rulesets/niko/skills/niko-preflight/SKILL.md` — step 2 (prose-lock FAIL + non-executable non-FAIL), step 6 (qualified to executable behavior), step 9 (fix instruction both directions).
- `memory-bank/systemPatterns.md` — recorded the tracked-`.cursor/` lag convention (feature commits touch `rules/`/`rulesets/`; generated tree re-synced under separate `chore(dev): ai-rizz sync` commits).

**Beyond the issue:** Preflight step 6 had to be amended alongside step 2. Leaving it unqualified would have contradicted the new guard eleven lines above and invited agents to revive prose tests to satisfy completeness.

**Post-reflect on PR #98:** Tightened prose; restored block→cite→replan on TDD FAIL; packaging wording shifted to "not a change-detector"; applied review Items 4 and 5 (artifact-scoped exemption; document-assert gate cue). Rejected CodeRabbit Item 4 "solely" stance in favor of operator alternate.

## TESTING

No new automated tests — both deliverables are non-executable prose; inventing heading/phrase assertions would violate the carve-out. Existing `make test` (ruleset symlink + README link checkers) still run and passed.

- Preflight PASS (two plan amendments: heading rename to `## What TDD Governs`; generated-tree dependency note corrected with git evidence).
- Build matched plan; `make test` green.
- QA PASS after one trivial fix: opening sentence named "What TDD Governs" instead of pointing at "the next section" positionally.
- Requirement 4 exercised live by this task's own preflight run. Requirement 3 checked by reading the FAIL condition against the issue's `test_pr_template_and_title_ci.py` example — no live failing-plan exercise; first real test is the next task that tries to schedule a prose test.

## LESSONS LEARNED

- Boundaries drawn around categories get relabeled; boundaries drawn around consequences do not. When an agent keeps evading a rule, check whether the rule is drawn around categories instead of failure modes.
- Changing a rule that gates your own workflow can deadlock: had preflight failed this plan under the old wording, the only compliant repair would have been inventing the prose tests the task prohibits. Workable move: judge intent, record the override, let the change close the ambiguity for the next task.
- Preflight paid for itself on a two-file prose change — caught a heading collision and replaced a vague generated-tree assumption with evidence.
- In this repo, tracked `.cursor/` copies are expected to lag feature commits; do not hand-edit them inside the feature task.
- What shipped bolts the scope gate in front of a four-step process that still assumes scope. The more elegant foundational shape would fold "is this executable?" into step 1 before locating test infrastructure — recorded as design debt, right-sized out of this task.

## PROCESS IMPROVEMENTS

- When amending a blocking check, grep sibling checks in the same file for contradictions before shipping (step 6 vs step 2).
- For self-referential rule changes, treat "this task's own preflight" as a live exercise of the non-FAIL path and document the FAIL path as a known verification limit rather than claiming full coverage.

## TECHNICAL IMPROVEMENTS

- Optionally fold the change-detector question into `always-tdd` step 1 as the first substep, so scope is foundational rather than a bolt-on section.
- Level2/level3 plan and build docs still say every step maps to a TDD cycle; issue #95 left them out of scope. If prose tests still appear after this ship, those docs are the next place to look.
- After push: `chore(dev): ai-rizz sync` to refresh the generated `.cursor/` tree from remote.

## NEXT STEPS

- PR #98 review Item 3 still open: name "memory-bank narrative" explicitly in both out-of-scope lists (issue #95 wording).
- Merge PR #98 when review is satisfied; then sync generated `.cursor/` copies.
- Watch the next prose-only or prose-test-proposing plan for the first live exercise of the new FAIL path.
