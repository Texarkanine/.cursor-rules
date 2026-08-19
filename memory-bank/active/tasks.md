# Task: preflight-analyze-and-report

* Task ID: preflight-analyze-and-report
* Complexity: Level 2
* Type: simple enhancement

Tighten `/niko-preflight` so it judges the plan and reports. It must not rewrite implementation units. Bookkeeping writes stay. Match QA's judge-only shape; do not invent a second dialect.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: `make test` (ruleset symlink + README link checks in `scripts/`)
- Test location: `scripts/`
- Conventions: layout/link gates, not skill-prose assertions
- New test files: none

## Implementation Plan

### 1. Judge-only preflight skill — prose/policy

- Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
- No tests: prose/policy artifact

1. Add a **Judge, Do Not Fix** block modeled on `rulesets/niko/skills/niko-qa/SKILL.md` (surface and judge; never modify the plan under review). Allowed writes only: `memory-bank/active/.preflight-status`, Preflight findings in `tasks.md` / `progress.md`, and (at Step 4) the `**Phase:**` field in `activeContext.md`. Spell the findings boundary: append a findings section; do not rewrite Implementation Plan units, behavior lists, or other scheduled work.
2. Radical Innovation: keep the request to describe one concrete change. Delete the line that says to make an in-scope change to the plan. The only write path for that idea is a finding (advisory if in-scope, advisory-and-do-not-apply if it would change level or brief).
3. Generate Preflight Report: write status; update `tasks.md` with findings only — drop "plan amendments".
4. Handle Results: FAIL still routes to the operator (`/niko-plan` on rearchitect; operator addresses findings then re-runs on fixable). No wording that preflight already patched the plan.

## Technology Validation

No new technology - validation not required

## Dependencies

- QA skill's judge-only / allowed-writes wording (`rulesets/niko/skills/niko-qa/SKILL.md`)
- Existing status vocab in `rulesets/niko/niko/memory-bank/active/preflight-status.mdc`

## Challenges & Mitigations

- **Agents still amend from niko-core autonomy or from reading persistent MB files:** the allowlist must be exclusive (`Allowed writes only`), same as QA. Preflight Step 1 still reads `systemPatterns.md` / `techContext.md`; the skill must not leave a hole that those "When to Update" rules can fill.
- **Findings section vs plan rewrite:** "update `tasks.md`" alone is how the SumMem run rewrote units. The skill must say append-findings, not rewrite units.
- **TDD gate:** do not soften FAIL (rearchitect) for TDD encoding. This task removes self-heal; it does not reopen it.

## Pre-Mortem

- **Skill still invites DO in a later step, so models amend anyway:** already covered by Challenges 1–2 (exclusive allowlist + findings-only step 8 + delete "make the change").
- **We forbid every `tasks.md` write and then findings have nowhere to go:** allowed list keeps a findings append; do not omit `tasks.md` entirely.
- **Wrong layer (parent Spawn charge vs skill):** Spawn is still "run the skill only". The leak is in the skill. No workflow/chart change.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
