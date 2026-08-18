# Task: niko-plan-always-tdd

* Task ID: niko-plan-always-tdd
* Complexity: Level 3
* Type: process enhancement (Plan-phase TDD encoding)

Make Niko Plan emit per-unit always-tdd ordering for executable work so preflight stops rewriting plans.

## Pinned Info

### Plan vs doctrine vs gate

Plan owns the *schedule* (what `tasks.md` looks like). `always-tdd.mdc` owns the *doctrine* (how executable work is done). Preflight only checks that the schedule is unambiguous. Naming "TDD" without numbering the work is the failure mode.

```mermaid
flowchart LR
  doctrine["always-tdd.mdc always-on doctrine"]
  plan["L2/L3 Plan docs"]
  tasks["tasks.md per unit"]
  pref["Preflight TDD Plan Encoding"]
  build["Build executes the schedule"]
  doctrine -->|"closed-stack pointer"| plan
  plan --> tasks
  tasks --> pref
  pref -->|"PASS"| build
  doctrine -.->|"already injected"| build
```

## Component Analysis

### Affected Components
- **L2 Plan** (`rulesets/niko/skills/niko/references/level2/level2-plan.md`): current "maps to one TDD cycle" gloss + `Tests first` / `Changes` sibling fields. This is the output contract L2 agents copy.
- **L3 Plan** (`rulesets/niko/skills/niko/references/level3/level3-plan.md`): same template family; same defect at component granularity.
- **niko-plan router** (`rulesets/niko/skills/niko-plan/SKILL.md`): routes only; no TDD content. Leave thin unless a one-line closed-stack pointer earns its keep.
- **L2/L3 Build**: already numbers stub → red → green. Out of scope unless Plan's new vocabulary would contradict them (it should match, not rewrite Build).
- **Preflight TDD Plan Encoding**: blocking gate; stays. Not the place to invent TDD structure.
- **always-tdd.mdc**: doctrine; do not duplicate into Plan.

### Cross-Module Dependencies
- Plan → `tasks.md` → Preflight check → Build. If Plan's template is the FAIL shape, Preflight must rewrite or hard-FAIL. Stockroom: usually rewrite (band-aid).
- always-tdd is alwaysApply; Plan and Build both assume it is present. Plan must not treat "bundled" as "the schedule is implied."

### Boundary Changes
- Public contract of Niko Plan's `tasks.md` Implementation Plan section changes: per-unit typed steps with numbered test-first substeps, not sibling fields. Consumers are future Plan agents and Preflight.

### Invariants & Constraints
- Must preserve always-tdd as the sole doctrine (no forked four-step essay in Plan).
- Must preserve prose/policy carve-out and change-detector ban.
- Must preserve Preflight as blocking rearchitect on TDD FAIL (no self-heal).
- Must preserve prompt-authoring: numbered list = order; bullets = a set; closed-stack refs OK; restating sibling prompts is not.
- Canonical edits under `rulesets/` only.
- This task's deliverable is skill wording: no markdown change-detector tests.

## Open Questions

- [x] How should Plan activate always-tdd? → Resolved: template-as-schedule (numbered per-unit substeps are the work; closed-stack pointer to always-tdd; no doctrine copy; explicit load held in reserve). See `memory-bank/active/creative/creative-plan-tdd-activation.md`.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior. Both plan docs are skill wording (prose/policy). Inventing heading/phrase assertions on them would be change-detectors banned by always-tdd.

Live exercise of the new schedule is the next Niko task that changes executable behavior — not this one.

### Test Infrastructure

- Framework: `make test` (ruleset symlink targets + README internal links via `scripts/`)
- Test location: `scripts/` plus `.github/workflows/rulesets-links.yml`
- Conventions: no prompt-content snapshot tests
- New test files: none

### Integration Tests

- None. After the edits, `make test` must still pass (layout/links only).

## Implementation Plan

### 1. L2 Plan instructions — prose/policy

- Files: `rulesets/niko/skills/niko/references/level2/level2-plan.md`
- No tests: prose/policy artifact

1. In Step 3 (Test Planning), state that behaviors to verify are executable only; prose/policy units do not get invented tests (carve-out in `always-tdd.mdc`).
2. In Step 5, replace the "maps to roughly one TDD cycle: write failing test → implement to pass → refactor" gloss and the `Tests first` carve-out line with: each step is one unit typed **executable** or **prose/policy**; executable numbered substeps are the stages of `always-tdd.mdc` in order; a step whose substeps could be reordered and still read correctly is not planned yet; prose/policy units use ordered work steps plus `No tests: prose/policy artifact` and never schedule a change-detector.
3. In the `tasks.md` template's Implementation Plan, replace the `Files` / `Tests first` / `Changes` sibling fields with typed unit headings and numbered substeps matching the creative sketch (stub tests, stub interface, write tests and run red, write code and run green — names only, no doctrine copy).

### 2. L3 Plan instructions — prose/policy

- Files: `rulesets/niko/skills/niko/references/level3/level3-plan.md`
- No tests: prose/policy artifact

1. Same Test Planning qualifier as L2, on Step 6 (include component-boundary executable behaviors; still no invented prose tests).
2. Same Step 7 replacement as L2 Step 5, keeping L3 extras (group by component, creative refs, diagrams).
3. Same Implementation Plan template replacement as L2, keeping L3 fields (`Creative ref` where applicable).

### 3. Confirm non-goals — prose/policy

- Files: `rulesets/niko/skills/niko-plan/SKILL.md`, `rulesets/niko/skills/niko-preflight/SKILL.md`, `rules/always-tdd.mdc`, `rulesets/niko/skills/niko/references/level2/level2-build.md`, `rulesets/niko/skills/niko/references/level3/level3-build.md`, `rulesets/niko/skills/niko/references/level4/level4-plan.md`
- No tests: prose/policy artifact

1. Dry-read: router stays a router; preflight TDD gate unchanged in role; always-tdd unchanged; Build already numbers the same sequence (no edit unless a clash appears); L4 stays a milestone list.
2. If a clash appears (Plan's new stage names contradict Build's one-liner), make the smallest closed-stack pointer on Build — do not expand this step speculatively.

## Technology Validation

No new technology - validation not required

## Dependencies

- Creative decision: `memory-bank/active/creative/creative-plan-tdd-activation.md`
- Doctrine: `rules/always-tdd.mdc` (always-on; do not copy)
- Gate: `rulesets/niko/skills/niko-preflight/SKILL.md` TDD Plan Encoding (do not change)

## Challenges & Mitigations

- Agents copy the example harder than the instruction: change Step 5/7 *and* the template; leave no `Tests first` / `Changes` sibling example behind.
- Four stage names look like restating always-tdd: names plus "in order, per `always-tdd.mdc`" only — no stubbing commentary, no change-detector paragraph.
- Next executable Plan still fails encoding: do not add a load step in this change; B is the recorded follow-on, not a preflight self-heal.

## Pre-Mortem

- This plan failed because we rewrote the template but left "maps to one TDD cycle" in the instruction, so agents still emitted a disclaimer plus implementation list: already covered by Challenge 1 (edit both).
- This plan failed because we pasted always-tdd's how-to into Plan and it drifted at the next always-tdd edit: already covered by Challenge 2 (names only).
- This plan failed because structure-alone was not enough salience and we had no recorded next instrument: already covered by Challenge 3 (B in reserve, not this diff).
- This plan failed because we added markdown tests that lock heading strings, violating the carve-out this repo just shipped: Test Plan above forbids it; QA should reject any such tests.

## Status

- [x] Initialization complete
- [x] Component analysis complete
- [x] Open questions resolved
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
