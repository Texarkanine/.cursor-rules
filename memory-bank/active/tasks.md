# Task: preflight-analyze-and-report

* Task ID: preflight-analyze-and-report
* Complexity: Level 2
* Type: simple enhancement (rework)

Rework the shipped judge-only preflight skill: TDD **re-order** of already-enumerated test steps is a fixable fail the subagent applies in-phase. Missing tests stay FAIL (rearchitect). Other plan amendments stay forbidden.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: `make test` (ruleset symlink + README link checks in `scripts/`)
- Test location: `scripts/`
- Conventions: layout/link gates, not skill-prose assertions
- New test files: none

## Implementation Plan

### 1. TDD re-order carve-out — prose/policy

- Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
- No tests: prose/policy artifact

1. In **TDD Plan Encoding**, split the order FAIL. If an executable unit already names test steps (cases, stubs, suite, or test files) but sequences them after or mixed with production steps — including TDD only in a preamble while those names live in Files/Changes — **re-sequence** so tests come first. Use only names already in the unit. Record the finding. Continue; the TDD check then passes. If an executable unit has **no** test steps, or the only TDD claim is a disclaimer with nothing to re-sequence, **FAIL (rearchitect)**. Change-detectors stay FAIL with the existing remove instruction (not a reorder).
2. In **Judge, Do Not Fix**, keep the exclusive allowlist and add one exception: the TDD re-sequence in step 1. That write may change Implementation Plan numbered steps **only** to put already-enumerated test work before already-enumerated production work. It must not add steps, cases, files, stubs, or behaviors. All other plan text stays read-only.
3. In **Handle Results**, state that a TDD order miss is fixed in-phase by the subagent; after a successful re-sequence the status is PASS or PASS WITH ADVISORY (finding recorded). Do not leave FAIL solely because an order fix was applied. Missing-test and change-detector FAILs still do not patch.

## Technology Validation

No new technology - validation not required

## Dependencies

- Shipped judge-only block in the same skill (steps 8–10)
- Operator rework brief: reorder already-enumerated tests; do not synthesize

## Challenges & Mitigations

- **"Encode stub → red → green" vs inventing tests:** allowed only when the unit already names the tests. Writing the four always-tdd stage labels around those names is a re-sequence. Inventing a `Behaviors to Verify` list or a new test file is not.
- **Ambiguous which lines are tests:** if the subagent cannot point at existing test steps, FAIL (rearchitect). Do not guess.
- **Allowlist hole:** the exception must be named and bounded. "Update tasks.md" remains findings-only plus this one rewrite.

## Pre-Mortem

- **Subagents treat any TDD miss as a license to write a suite:** already covered — no-test units FAIL rearchitect; exception forbids added steps/cases/files.
- **Status stays FAIL after a successful reorder, so build stays blocked:** Handle Results must say PASS / PASS WITH ADVISORY after an in-phase fix.
- **Wrong layer (Plan templates, not preflight):** Plan already emits the schedule; this carve-out is the verification pass the operator re-derived. Stay in the skill.

## Preflight Findings

Run 2026-08-19. Status: **FAIL** (fixable — no rearchitect). Findings recorded; no implementation-plan unit was modified.

### F1 — BLOCKING (conflict): the Project Brief contradicts the plan it authorizes

The plan implements the brief's `## Rework` paragraph, which reverses earlier statements in the same brief that were never retracted:

- Requirement 2 — "Preflight must not amend the implementation plan in `tasks.md` (**no TDD self-heal**, no in-place unit rewrites, ...)"
- Constraint 2 — "TDD Plan Encoding stays a blocking rearchitect gate. **This task does not reopen self-heal.**"
- Acceptance Criterion 2 — "Allowed writes are enumerated and **do not include rewriting implementation-plan units**."
- Use-Case 1 — "It **does not rewrite implementation units** in `tasks.md`."

Implementation step 2 adds exactly such a write. The Rework paragraph is later and unambiguous, so intent is clear — but nothing marks the four items above as superseded. QA validates the build against these acceptance criteria, so a correct build of this plan is measurable as an AC-2 violation at the next gate.

**Fix (operator, in `memory-bank/active/projectbrief.md`):** carve the TDD re-sequence out of Requirement 2, Constraint 2, AC 2, and Use-Case 1 so each states the boundary as "no plan amendments **except** re-sequencing already-enumerated test steps ahead of already-enumerated production steps." Then re-run `/niko-preflight`. AC 4 needs no change: after a successful re-sequence there is no FAIL, so "preflight itself does not patch" still holds for every FAIL path.

### F2 — MEDIUM (completeness): the modal-heal generalization is not in an implementation step

The brief's Rework designates "encode stub → red → green around **already-named** tests" as the allowed generalization of a bare swap. In the plan this appears only under `## Challenges & Mitigations`, which is reasoning, not artifact text. Implementation step 1 says "Use only names already in the unit" but never authorizes writing the always-tdd stage labels. A build that follows the numbered steps literally can ship a carve-out that permits only a literal reordering, under-delivering the stated requirement.

**Fix:** extend step 1's text so the skill states that a re-sequence may express the result as the always-tdd stages in order (stub tests, stub interface, write tests and run red, write code and run green) — matching the substep shape `level2-plan.md` already requires — provided every test named comes from the unit as written.

### F3 — ADVISORY: `PASS` vs `PASS WITH ADVISORY` after a re-sequence

Step 3 permits either. `rulesets/niko/niko/memory-bank/active/preflight-status.mdc` defines `PASS` as "checks passed with no advisories", so a bare `PASS` after preflight rewrote part of the plan hides the one write preflight is now allowed to make. Recommend the skill mandate `PASS WITH ADVISORY` whenever a re-sequence was applied.

### F4 — ADVISORY: state that `niko-qa` is out of scope

`rulesets/niko/skills/niko-qa/SKILL.md` carries a parallel `Judge, Do Not Fix` block. It is parallel in shape, not verbatim, so amending preflight's copy breaks no duplication tripwire — but a build agent may "helpfully" mirror the carve-out into QA, where post-build self-heal is not wanted. Recommend the plan's Dependencies note QA as deliberately unchanged.

### Checks that passed

- **TDD Plan Encoding** — the sole unit edits skill wording, which `always-tdd.mdc` classifies as prose/policy; `No tests: prose/policy artifact` is correct, and no change-detector test is scheduled.
- **Convention Compliance** — `rulesets/niko/skills/niko-preflight/SKILL.md` is a real file, not a symlink into `rules/`, so it is the canonical edit target; generated `.cursor/` and `.claude/` trees are untouched.
- **Dependency Impact** — no documentation step is owed: `rulesets/niko/README.md` and `level2-workflow.md` reference preflight only through workflow-chart `FAIL -> Plan` edges and a status-file table row, all of which stay accurate (an order miss now resolves to PASS; the FAIL edge survives for missing tests and change-detectors). `level2-build.md`'s "trust the sequence" reinforces the carve-out rather than conflicting with it.
- **Conflict Detection** — no duplication-in-waiting. `level2-plan.md` step 5 already emits per-unit always-tdd substeps; this carve-out is the verification backstop for plans that did not, which the Pre-Mortem already reasons through.

### Radical Innovation (advisory — not applied)

Make the one permitted plan write auditable. The carve-out's weak point is that "I only re-sequenced" is self-reported: an operator reading a PASS cannot tell whether preflight moved two lines or synthesized a schedule. Have step 3 require that an applied re-sequence (a) always writes `PASS WITH ADVISORY`, never bare `PASS`, and (b) records the affected unit's step ordering before and after — old numbers, new numbers — in the findings section. Cost is roughly one sentence in the skill; it converts an unverifiable claim into a diffable receipt, and it subsumes F3.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
