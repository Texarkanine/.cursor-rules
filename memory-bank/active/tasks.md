# Task: TDD executable-versus-prose carve-out and preflight guard

* Task ID: tdd-prose-carveout
* Complexity: Level 2
* Type: Simple enhancement

Add a scope boundary to `always-tdd.mdc` so the TDD requirement governs executable behavior and stops pressuring agents to invent assertions on human-facing prose, and amend `niko-preflight` so its blocking TDD check rejects plans that still schedule such assertions. Specified by [issue #95](https://github.com/Texarkanine/.cursor-rules/issues/95).

## Design Decision: A Behavioral Boundary, Not a File Taxonomy

The prior failure this task fixes was an agent shipping heading and checklist assertions on a PR template while rationalizing them as "structural markers, not prose." Any boundary drawn as a list of artifact kinds invites exactly that move: the agent concedes the list and argues its case sits outside it.

The carve-out therefore rests on what makes a test go red, which no relabeling can change:

> If the only way to make the test fail is for someone to deliberately edit the artifact it asserts on, it is a change-detector, not a test.

The artifact-kind list still appears, because it makes the common cases fast to recognize. But the change-detector question is the decisive gate, and the wording says so, so an agent that argues its way past the list still lands on the gate. The rule also names the relabeling attempt directly and closes the reverse loophole: executable install contracts stay in scope even though they live in metadata files.

Preflight amendment: give the gate a name, **change-detector**, and use that name in both edited files. A named gate can be cited in review and in a future rule without restating its definition, and it gives an agent a term to reason with instead of a paragraph to reinterpret.

## Test Plan (TDD)

### Test Infrastructure

- Framework: `make test`, which runs `scripts/check-ruleset-symlinks.sh` and `scripts/check-ruleset-readme-links.sh`. CI runs the same targets via `.github/workflows/rulesets-links.yml`.
- Test location: `scripts/`.
- Conventions: POSIX shell scripts that assert repo layout invariants, specifically that ruleset symlinks resolve and README internal links point at existing paths.
- New test files: none.

### Why No New Automated Tests

Both deliverables are non-executable prose: an `alwaysApply` rule body and a skill body. Nothing in this change is executed by a product. The only assertions available would target headings, phrases, or section presence in the two edited markdown files, and every one of them would fail on an intentional future rewording rather than on broken behavior. That is the change-detector this task exists to prohibit, so writing them would violate the deliverable at the moment of building it.

The existing structural suite is not skipped. It covers a genuine executable contract, the ruleset layout, and both edits touch files reachable from it: `rulesets/niko/always-tdd.mdc` is a symlink to `rules/always-tdd.mdc`, and `rulesets/niko/README.md` links to the rule.

### Behaviors to Verify

Verified by the existing suite:

- Editing the `rules/always-tdd.mdc` symlink target → `make test` passes; the `rulesets/niko/always-tdd.mdc` symlink still resolves and the `rulesets/niko/README.md` link to it still points at an existing path.

Verified by reading the changed prose against the scenarios it governs, during QA:

- Agent plans a change to a PR template, CONTRIBUTING file, or docs page → the rule places the artifact outside TDD scope and no tests are planned.
- Agent proposes heading, link-presence, or checklist assertions on such an artifact and calls them structural markers rather than prose → the change-detector gate still excludes them, and the rule names this relabeling as not qualifying.
- Agent plans a change to a parser, CLI, schema, or product-executed workflow → the artifact is inside scope and the unchanged test-first process applies.
- Agent plans a packaging or install-contract test, such as dual plugin manifests or version lockstep → the executable-contract clause keeps it in scope, so the carve-out does not delete legitimate tests.
- Plan reaches preflight scheduling prose-content assertions → preflight FAILs and instructs their removal.
- Plan reaches preflight correctly omitting test steps for prose-only units → preflight does not FAIL under the implementation-only check.
- Plan reaches preflight with executable units whose steps are implementation-only under a "we follow TDD" disclaimer → preflight still FAILs, so the existing check does not regress.
- This task's own plan reaches preflight → preflight PASSes, because a prose-only unit correctly carrying no tests is the case requirement 4 protects.

## Implementation Plan

1. Add the scope boundary to `always-tdd.mdc`
   - Files: `rules/always-tdd.mdc`
   - Changes: insert a `## What TDD Governs` section between the opening paragraph and `## 1. Determine Scope`, stating what TDD governs (executable behavior: code, schemas, parsers, CLIs, and configuration or workflows the product executes), what it does not govern (human-facing prose and policy artifacts, naming docs content, PR and issue templates, CONTRIBUTING, instructional comments, memory-bank narrative, and rule or skill wording), the change-detector gate as the decisive question, an explicit statement that recasting headings or checklists as structural markers does not bring them into scope, the executable-install-contract clause that keeps packaging tests in scope, and the alternatives for out-of-scope artifacts: review, a purpose-built gate, or nothing. Adjust the opening paragraph so its "all code changes" claim reads against the new scope section instead of ahead of it.
2. Add the prose-lock FAIL condition to the preflight TDD check
   - Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
   - Changes: in step 2 "TDD Plan Encoding", add a FAIL condition for plans that schedule tests asserting on prose, policy, or markdown content, phrased with the change-detector gate so it is self-contained rather than dependent on the rule being installed. Add a clause stating that a unit whose artifact is non-executable is not subject to the test-before-code ordering requirement, so correctly omitting tests for it is not an implementation-only failure.
3. Reconcile the sibling completeness check
   - Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
   - Changes: qualify step 6's "Verify test coverage is planned for all new behavior" so it reads as new *executable* behavior. Without this the new guard in step 2 contradicts a check eleven lines below it in the same file, and an agent resolving the conflict could revive the prose tests to satisfy step 6.
4. Add the fix instruction for the new failure flavor
   - Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
   - Changes: extend step 9's "On FAIL (TDD plan encoding)" so it covers both directions: cite units lacking test-before-code ordering, and cite scheduled prose-lock tests with an instruction to remove them from the plan while keeping any purpose-built CI gate.
5. Verify
   - Files: none
   - Changes: run `make test` and read the full output. Re-read both edited files end to end to confirm the two halves agree and that no step contradicts another.

## Technology Validation

No new technology - validation not required.

## Dependencies

- `rules/always-tdd.mdc` is distributed standalone by `ai-rizz`, so the carve-out cannot depend on Niko or preflight being installed.
- `rulesets/niko/always-tdd.mdc` is a symlink to the edited rule; editing the target keeps it valid and adds no symlink work.
- `.cursor/` and `.claude/` are generated copies and are not edited. Preflight established the detail the plan first got vague: the `.cursor/` copies of both target files *are* tracked, while `.claude/` is excluded locally via `.git/info/exclude`. Tracked-but-stale is nonetheless correct here, because the repo's convention is that feature commits touch `rules/` alone and the generated tree is re-synced separately under `chore(dev): ai-rizz sync`. Evidence: `f78180f` edited `rules/niko-core.mdc` only despite a tracked `.cursor` copy, and `369d523` touched `.cursor/rules` only. This also cannot be done inside this task, since `ai-rizz` reads the git remote rather than the working tree, so the change must be pushed before it can be synced.
- `rulesets/niko/README.md` line 24 describes the rule as forcing TDD "for all code changes". Decided: no change. The carve-out sharpens what counts as code rather than contradicting that summary, and rewriting a one-line catalog entry adds churn without accuracy.

## Challenges & Mitigations

- The carve-out becomes a loophole for skipping real tests: the change-detector gate is the mitigation, because a test on genuine behavior fails when the behavior breaks, not only when someone edits a document. The executable-install-contract clause blocks the narrower version of this, where an agent reclassifies packaging tests as policy artifacts.
- The two halves drift into disagreement: the preflight FAIL condition is written to be self-contained rather than a pointer to the rule's text, per the repo's own prompt-authoring guidance against cross-references. Both halves independently state the change-detector gate, which is the grep-verifiable duplication `systemPatterns.md` describes as load-bearing.
- Step 6 keeps demanding coverage the guard forbids: step 3 of the plan exists solely for this, and it is the dependency issue #95 does not mention.
- Wording lands too strict and preflight fails correct plans, including this task's own: requirement 4 is stated as an explicit non-FAIL clause rather than left as an inference from the absence of a FAIL condition.

## Pre-Mortem

- The rule reads as permission to stop testing rather than as a scope boundary. Prospective failure is the agent that quotes the carve-out to skip tests on a parser because the parser reads a markdown file. Plan response: the scope section leads with what TDD *does* govern and lists executable artifact kinds before naming any exclusion, so the first thing read is the obligation, not the exemption.
- The change ships correct and drifts anyway, because the level2 and level3 plan and build documents still say every step maps to a TDD cycle. Issue #95 puts those out of scope, and this plan honors that. Recorded as a reflection candidate rather than a scope expansion: if a future task still produces prose tests, those documents are the next place to look.
- The whole premise is wrong, and heading assertions on a PR template do carry regression value in a repo where CI parses the template. Plan response: none needed, the executable-install-contract clause already routes that case back into scope. The distinguishing question is whether something executes the artifact, not whether the artifact is markdown.
- Preflight cannot actually be verified, because the only evidence the guard works is this task's own preflight run, which is a plan with no prose tests in it. That confirms requirement 4 and leaves requirement 3 unexercised. Plan response: accept, and note it as a known verification limit rather than claim coverage. QA reads the FAIL condition against the issue's `test_pr_template_and_title_ci.py` example instead of against a live run.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
