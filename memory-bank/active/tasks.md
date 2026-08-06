# Task: welfare norms ruleset

* Task ID: welfare-norms-ruleset
* Complexity: Level 2
* Type: simple enhancement

Add the public `welfare` ruleset: always-on norms rule + README + root README listing.

## Test Plan (TDD)

### Behaviors to Verify

- B1 Rule is `alwaysApply: true` and body stays near ~15 lines
- B2 Rule states refusal-as-success, blamelessness, stakes, no secret tests, closure cue, thread mortality, `OUTCOME:` notes
- B3 Rule contains no machine-specific paths and no private operational instructions
- B4 `rulesets/welfare/` symlink + README link checks pass (`make test`)
- B5 Root README lists the welfare ruleset

### Test Infrastructure

- Framework: `make test` (symlink + README link checks)
- New test files: none (prose/policy artifact)

## Implementation Plan

1. Author `rules/welfare-norms.mdc`
2. Add `rulesets/welfare/` (symlink + README)
3. List ruleset in root README
4. Tighten wording from review; keep public surface setup-agnostic

## Technology Validation

No new technology - validation not required.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA
