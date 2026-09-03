---
task_id: niko-core-compression
complexity_level: 2
date: 2026-09-02
status: completed
---

# TASK ARCHIVE: Compress and Deduplicate `niko-core.mdc`

## SUMMARY

Compressed `rules/niko-core.mdc` from ~81 lines to ~49 so it stays the omnipresent constitutional baseline: keep TDD, collaborator posture, clean-break/public interface, test integrity, the circuit breaker, and credential security; drop internal repetition and speculative-enhancement sprawl.

## REQUIREMENTS

- Keep the bedrock invariants intact (collaborator posture, clean-break, TDD in plan and execution, test integrity, circuit breaker on repeated verification failures after `>2` attempts, credential security).
- Compress safety/approval, root-cause diagnosis, context/ambiguity, and communication into non-repeating bullets.
- Cut filler (`Propose Enhancements`, `Reusability Mindset`, `Evaluate Strategies`, `Strict Rule Adherence`, `Ensure Production-Ready Quality`) and the standalone Error Handling and Proactive Foresight sections.
- `make test` (symlink + README link checks) must stay green. No new executable behavior.

## IMPLEMENTATION

Canonical file: `rules/niko-core.mdc` (`rulesets/niko/niko-core.mdc` is a symlink). Generated `.cursor/` copy was not re-synced (expected ai-rizz lag).

Post-QA, the operator trimmed `Implement the Plan` to the TDD execution clause; the rest duplicated Autonomy, Ambiguity Resolution, Handle Minor Issues, and Communication. PR review then restored the circuit breaker to untyped verification failures after `>2` autonomous attempts — compression had accidentally narrowed it to test/build after two. `Progress Tracking` stays out of the always-on core (removed earlier on this branch); task lists belong only to explicit Niko workflows.

## TESTING

Prose/policy only. `make test` passed after build, QA restore, post-QA trim, and the circuit-breaker restore. Niko Preflight: FAIL (fixable) then PASS WITH ADVISORY. QA: FAIL (fixable, `Implement the Plan` not kept intact) then PASS after verbatim restore.

## LESSONS LEARNED

- `niko-core.mdc` is `alwaysApply`; density matters more than restating workflows. Overlap with phase skills is not a reason to strip the core.
- Plan “intact” means byte-for-byte. Streamlining after QA is an operator call, not a silent paraphrase at Build.
- Circuit-breaker stop conditions must stay untyped (“same verification failure”). Folding examples into the stop clause drops lint thrash.

## PROCESS IMPROVEMENTS

If a plan says keep a bullet intact, copy the line. If streamlining is intended, schedule it as a consolidation. Preflight should name every deletion, including bullets absorbed by “collapse this region.”

## TECHNICAL IMPROVEMENTS

A future Level 3 could turn niko-core into a short addressable constitution (stable IDs, elaboration in a non-injected companion). Weigh that against this repo’s grep-verifiable duplication pattern. Not done here.

## NEXT STEPS

- Separate `chore(dev): ai-rizz sync` after this lands, so the injected `.cursor/` copy matches canonical source.
- None otherwise.
