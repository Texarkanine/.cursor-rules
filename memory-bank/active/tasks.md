# Task: tdd-product-scope

* Task ID: tdd-product-scope
* Complexity: Level 2
* Type: bug fix

Rewrite the in-scope sentence in `always-tdd` so TDD attaches to the product's executable behavior, not to whatever a package manager or Actions runner happens to execute. Spec: [Texarkanine/.cursor-rules#116](https://github.com/Texarkanine/.cursor-rules/issues/116).

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: Make (`make test`) — rulesets symlink targets and README internal links
- Test location: `scripts/`
- Conventions: layout and link checks; no content assertions on rule prose
- New test files: none

## Implementation Plan

### 1. What TDD Governs in-scope sentence — prose/policy

- Files: `rules/always-tdd.mdc`
- No tests: prose/policy artifact

1. In `## What TDD Governs`, replace only the in-scope paragraph. Current text: `In scope: executable behavior — code, schemas, parsers, CLIs, and any configuration or workflow the product runs, etc. If something executes it, it is in scope, whatever its file extension.` Replacement: `In scope: the product's executable behavior — code, schemas, parsers, CLIs, and any configuration or workflow it runs, etc. File extension does not decide.`
2. Leave the out-of-scope sentence and the change-detector paragraph unchanged.
3. Do not add named exclusions (lint, format, typecheck, CI, release-please, or any other tool class). Do not edit `rulesets/niko/skills/niko-preflight/SKILL.md` or generated `.cursor/` / `.claude/` copies. `rulesets/niko/always-tdd.mdc` is a symlink to `rules/always-tdd.mdc`; do not replace the symlink.

## Technology Validation

No new technology - validation not required

## Dependencies

- None

## Challenges & Mitigations

- A later reader still treats "it runs" as the CI or package-manager runner: "it" is the product in the same sentence; the paragraph now opens with "the product's executable behavior." Do not "clarify" by listing tools.
- A product that *is* a GitHub Action could look excluded if scope meant "what the process executes": the lead phrase is the product's behavior (what it delivers), not "if the product's process executes the file."
- Preflight's local prose/policy parenthetical still looks exhaustive: TDD Plan Encoding already defers to `always-tdd` for what counts as executable. A second definition is a guardrail. Accept the one-file bet.
- Build expands this into the issue's two-paragraph exclusion list: the replacement sentence above is the whole change.

## Pre-Mortem

- Preflight still FAILs invoke-only CI because its own "executable work" wording never sees the new definition: already covered by the one-file bet in Challenges. If that happens after ship, it is a new incident, not a reason to pre-encode exclusions here.
- The replacement is so close to the old sentence that "something executes it" remains the remembered rule: the poison sentence is deleted, not rephrased with a synonym of "something."
- This needed a Level 3 creative phase: rejected. The operator already chose the design (steer, smallest tweak). One sentence in one file is Level 2.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
