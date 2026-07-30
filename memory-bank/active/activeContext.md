# Active Context

## Current Task: tdd-prose-carveout
**Phase:** REFLECT COMPLETE (PR #98 open; review feedback partially addressed)

## What Was Done
- Implemented [issue #95](https://github.com/Texarkanine/.cursor-rules/issues/95) as L2: `## What TDD Governs` in `always-tdd.mdc`, preflight steps 2/6/9 guard. QA PASS, reflect complete.
- Opened draft PR [#98](https://github.com/Texarkanine/.cursor-rules/pull/98).
- Post-reflect tightening: shorter carve-out/preflight prose; restored block→cite→replan order on TDD FAIL handling.
- Operator reworked packaging wording: install-contract tests are "not a change-detector," not "in scope for TDD."
- Judged PR #98 feedback. Applied: Item 4 (operator alternate — "owes no tests for those artifacts"); Item 5 (gate cue is "Before writing a test that asserts on a document's contents," not "When unsure").

## Key Decisions
- Boundary is behavioral (change-detector), not a file taxonomy.
- Preflight step 6 must stay qualified to executable behavior.
- No new automated tests for this prose-only change; `make test` still runs.
- Item 4 CodeRabbit "solely" stance rejected as must-fix; operator's artifact-scoped wording preferred.
- Item 5 kept: conditional "when unsure" undercut the decisive gate for standalone always-tdd; cue fires when about to assert on document contents.

## Files Modified
- `rules/always-tdd.mdc` — `## What TDD Governs`; change-detector gate; document-assert cue.
- `rulesets/niko/skills/niko-preflight/SKILL.md` — steps 2, 6, 9; artifact-scoped prose exemption.
- `memory-bank/systemPatterns.md` — tracked `.cursor/` lag convention.

## Remaining from PR #98 review
- Item 1: absolute paths in this file (being fixed in this save).
- Item 2: reflection Summary still says "QA passing on the first pass" — should be "after one trivial fix."
- Item 3: name "memory-bank narrative" explicitly in both out-of-scope lists (issue #95 wording).

## Next Step
- Address remaining review Items 1–3 if desired, then `/niko-archive` to finalize. Or archive now and leave 1–3 for a follow-up.
