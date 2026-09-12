# Task: tdd-product-user-scope

* Task ID: tdd-product-user-scope
* Complexity: Level 2
* Type: bug fix

The #116 one-file bet failed: prefixing “the product's” and deleting “If something executes it” still left the in-scope category list and an ambiguous “user” in the contract-test sentence, so an L2 plan that vendored a third-party script and wrote `AGENTS.md` / `CLAUDE.md` invented file-presence / heading-order tests and preflight PASSed them. Replace the category list with the same consequence test change-detectors already use; make preflight classify and FAIL using that test, not the plan’s “executable” label. Issue-body proposed wording is not the locked text ([comment](https://github.com/Texarkanine/.cursor-rules/issues/123#issuecomment-5647217454)). Not #122.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: Make targets `test-symlinks` and `test-readme-links` (`Makefile`)
- Test location: `scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`
- Conventions: layout/link checks only; no wording assertions (those would be change-detectors)
- New test files: none

Live proof is the next L2 plan that vendors a third-party tool and writes agent bootstrap — not a suite that greps these sentences.

## Implementation Plan

### 1. always-tdd What TDD Governs — prose/policy

- Files: `rules/always-tdd.mdc` (`rulesets/niko/always-tdd.mdc` is a symlink; do not edit `.cursor/rules/shared/always-tdd.mdc` in this task)
- No tests: prose/policy artifact

1. Replace the in-scope sentence. **Do not** restore a category list (`code, schemas, parsers, CLIs, and any configuration or workflow it runs`). Those tokens are how vendored CLIs and agent workflows get relabeled in-scope. Locked replacement for the in-scope paragraph:

    `In scope: behavior a user of this product can observe breaking. File extension does not decide.`

2. Keep the existing out-of-scope prose/policy list. Append a second out-of-scope sentence whose illustrations end in `, etc.` Locked addition:

    `Repository bootstrap, vendored third-party tools, agent-facing prompts, gitignore lines, etc. are out of scope even when an agent or a developer tool invokes them.`

3. Rewrite the contract-test sentence so “user” cannot mean the next agent, and so lockstep is allowed only for **this** product’s published contract. Locked replacement for the paragraph that today begins “Delete change-detectors”:

    `Delete change-detectors; write none. The failure mode decides, not the format. A test that locks a contract across files (manifest/version lockstep, dual plugin manifests, etc.) is a contract test only when that lockstep is the published contract of this product: it goes red when the contract breaks for a user of this product, not when content is merely edited. If semantic versioning already signals the expectation, do not add the test. Enforce out-of-scope artifacts with review, a purpose-built gate (commit-title lint, link checker, schema validator), or nothing at all.`

4. Leave sections 1–4 (Determine Scope through Write Code) unchanged. Do not copy the issue body’s three-sentence “Proposed wording” block.

### 2. niko-preflight TDD Plan Encoding — prose/policy

- Files: `rulesets/niko/skills/niko-preflight/SKILL.md` (do not edit `.cursor/skills/shared/niko-preflight/SKILL.md` in this task)
- No tests: prose/policy artifact

`always-tdd` owns the definition. This unit states judge actions. Do not paste What TDD Governs into the skill.

1. In **TDD Plan Encoding**, after the bullet that says prose/policy owes no tests, insert this classification bullet:

    `Classify a unit as executable only when a user of this product can observe the behavior breaking. An agent or a developer tool invoking it is not enough. The plan's "executable" label is not decisive when it contradicts that test.`

2. Expand the existing change-detector strike bullet so it also deletes scheduled contract tests that are not this product’s published contract. Still one strike: delete that step, keep the other steps, record and continue. Locked replacement:

    `When a numbered step is a scheduled change-detector (a test that can only go red when someone deliberately edits the artifact it asserts on — heading, phrase, link, or checklist assertions on a document), or a scheduled contract test that is not the published contract of this product, delete that step. Keep the other steps. Record the finding and continue.`

3. Replace the FAIL bullet so inventing tests is not the PASS path after a strike. Locked replacement:

    `FAIL when the numbered steps for a unit that is executable under What TDD Governs have no test steps (implementation-only under a "we follow TDD" disclaimer, or TDD only in the preamble). This still applies after a strike that left such a unit with no tests. After a strike, a unit that is not executable under that rule owes no tests; omitting them passes.`

4. Keep `Do not invent tests. Do not emit always-tdd stages.` where it is.

5. Grep the rest of this skill for a sibling contradiction (lesson from #95): **Completeness Precheck** and **Judge, Do Not Fix**. Completeness already defers the TDD boundary to this check; add that it must not demand tests because the plan labeled a unit executable. Judge, Do Not Fix still allows only swap plus this strike (not a third mutation); retitle “change-detector strike” to “strike” so the expanded strike is in scope of the same allowed write. Do not add a unit-reclassify edit.

## Technology Validation

No new technology - validation not required

## Dependencies

- Unit 2 after unit 1: preflight judges using What TDD Governs; the definition must exist in `always-tdd` first.
- Generated `.cursor/` / `.claude/` copies lag until a later `chore(dev): ai-rizz sync`. Preflight’s new bullets must carry the classifier so a stale injected `always-tdd` cannot undo the echo.

## Challenges & Mitigations

- **Category-list relabeling:** Naming product CLIs or workflows in the in-scope sentence pulls vendored CLIs back in (the #116 failure). Mitigation: in-scope is only the consequence test; illustrations live in out-of-scope and end with `, etc.`
- **#95 packaging sweep:** “semver skip” must not ban this product’s real published contract (install/CLI lockstep). Mitigation: contract tests remain when they are this product’s published contract; they are forbidden when they only protect the next agent or a vendored tool.
- **FAIL-after-strike loop:** Striking eight invented tests and then FAILing “executable unit has no test steps” recreates the incident. Mitigation: FAIL uses What TDD Governs, not the plan label.
- **Definition drift:** A second full copy of What TDD Governs in preflight will diverge. Mitigation: always-tdd holds the sentences; preflight states classify / strike / FAIL actions only.
- **Generated-tree lag:** Mid-task agents may still see old injected always-tdd. Mitigation: expected; preflight bullets are self-sufficient; no in-task `.cursor/` edits.

## Pre-Mortem

- **Copied the issue’s proposed wording as the rule:** Closed three-item exclusion list, no `, etc.`, still premature. Plan response: locked sentences above; definition is the consequence test; illustrations have `, etc.`
- **Strike without changing FAIL:** Preflight deletes heading-order tests then FAILs missing TDD steps. Already covered by Challenge “FAIL-after-strike loop.”
- **Left “CLIs, and any configuration or workflow it runs” in always-tdd:** Same #116 misread. Already covered by Challenge “Category-list relabeling.”
- **“User of this product” still read as the agent:** Out-of-scope invocation sentence plus preflight “an agent or a developer tool invoking it is not enough” are the disambiguation; do not drop them at build.
- **This task’s own plan used as live TDD-encoding proof:** This plan is correctly prose/policy, so it cannot exercise the misclassified-executable FAIL path. Live proof remains the next vendor-bootstrap plan, recorded as a verification limit, not a reason to invent tests here.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
