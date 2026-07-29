---
task_id: tdd-prose-carveout
date: 2026-07-29
complexity_level: 2
---

# Reflection: TDD executable-versus-prose carve-out and preflight guard

## Summary

Added a scope boundary to `always-tdd.mdc` so the TDD requirement governs executable behavior rather than all changes, and amended `niko-preflight` so its blocking TDD check rejects plans that schedule assertions on prose. Delivered as specified in issue #95, in 21 insertions across 2 files, with QA passing on the first pass.

## Requirements vs Outcome

All four requirements delivered, none dropped or reinterpreted.

One thing was added beyond the issue: preflight's step 6 completeness check, which said "verify test coverage is planned for all new behavior", was qualified to executable behavior. The issue named only step 2. Had step 6 been left alone, the new guard eleven lines above it would have contradicted a sibling check in the same file, and the obvious way for an agent to resolve that conflict is to revive the prose tests. This was not scope creep so much as the issue's own goal being unreachable without it.

## Plan Accuracy

The plan's sequence, file list, and scope were correct, and no step needed reordering or splitting. Preflight produced two amendments, neither of them a sequencing error: a planned `## Scope` heading would have sat directly above the existing `## 1. Determine Scope`, and the plan's dependency note about the generated trees was vague where the truth was specific.

The most interesting miss is inverted. The plan anticipated that the *new* wording might land too strict and fail this task's own correct plan. What actually happened is that the *old* wording nearly did. Preflight's existing FAIL condition targets "implementation-only steps under a 'we follow TDD' disclaimer", and a prose-only plan is exactly that shape. Passing it required judging the check's intent against its letter.

## Build & QA Observations

Build was clean and matched the plan step for step. QA found one trivial issue — the opening sentence pointed at "the next section" positionally, which breaks if anything is later inserted between — and nothing substantive.

The verification story is honestly incomplete, and it is worth naming rather than glossing. Requirement 4, that preflight not fail correct prose-only plans, was exercised live by this task's own preflight run. Requirement 3, that it fail plans proposing prose tests, has no live exercise at all; it was checked by reading the new FAIL condition against the `test_pr_template_and_title_ci.py` example the issue describes. The first real test of requirement 3 will be the next task that tries to schedule a prose test.

## Insights

### Technical

- A boundary written as a taxonomy of artifact kinds invites relabeling; a boundary written as a question about failure modes does not. The prior failure this task fixes was an agent conceding that prose is out of scope and then arguing its heading assertions were "structural markers". No lengthening of the artifact list would have stopped that. What stops it is asking what turns the test red, because the answer does not change when you rename the thing you are asserting on. This generalizes well beyond TDD: when an agent keeps evading a rule, check whether the rule is drawn around categories instead of consequences.
- In this repo, the `.cursor/` copies of source files are tracked but deliberately allowed to go stale. Feature commits touch `rules/` and `rulesets/` alone, and the generated tree is re-synced in separate `chore(dev): ai-rizz sync` commits. It also cannot be done inside a feature task, because `ai-rizz` reads the git remote rather than the working tree, so the change must be pushed before it can be synced. Evidence: `f78180f` edited `rules/niko-core.mdc` only despite a tracked copy existing, and `369d523` touched `.cursor/rules` alone.

### Process

- Changing a rule that gates your own workflow can deadlock, and it is worth recognizing the shape early. Here, had preflight failed this plan, the only compliant repair would have been to invent the prose tests the task exists to prohibit. There was no legal exit. The workable move is to judge the gate's intent, record the override and its reasoning where the operator will see it, and let the resulting change close the ambiguity for the next task — which this one does, since preflight step 2 now names rule and skill wording explicitly.
- Preflight paid for itself on a two-file prose change, which is not where I would have expected it to. It caught a heading collision that would have shipped as a readability wart and replaced an assumption about the generated trees with evidence. Neither would have been caught by the test suite, and both were cheaper to fix before the build than after.

### Million-Dollar Question

If "TDD governs executable behavior" had been foundational, the rule would not carry a scope section at all — scope would live inside step 1. The current four-step process opens by assuming the change is in scope and then asks where the tests go, which is why step 1.3 has to catch the fallout with "if you cannot locate existing test infrastructure, stop and ask". That instruction is a symptom of the missing question. Foundationally, step 1 would begin by asking whether the change is executable at all, with the change-detector question as its first substep, and only then proceed to locating test infrastructure. What shipped bolts the scope gate on top of a process that presumes scope. It works, and it is the right size for this task, but the more elegant shape would have folded the gate into the process rather than in front of it.
