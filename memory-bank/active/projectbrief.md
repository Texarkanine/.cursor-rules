# Project Brief

## User Story

As an operator running Niko, I want the Plan phase to emit per-unit red/green (always-tdd) ordering for executable work so that preflight stops being the place that invents TDD structure, and build can follow the plan without coding first.

## Use-Case(s)

### Use-Case 1

An L2 or L3 Plan runs for a task that changes executable behavior. The written `tasks.md` implementation steps are ordered stub → red → green per unit, explicit enough that a reasonable implementer cannot follow the plan by coding first. Preflight's TDD Plan Encoding check passes without in-phase rewrite.

### Use-Case 2

An L2 or L3 Plan runs for prose/policy-only work (rule/skill wording, docs). Those units are marked as owing no tests. No change-detector tests are scheduled.

### Use-Case 3

Preflight still FAILs (rearchitect) if a future plan somehow omits per-unit test-before-code order. It does not self-heal TDD encoding.

## Requirements

1. Niko Plan (the L2/L3 plan docs that `niko-plan` routes to) always plans executable units in the test-first order defined by `always-tdd.mdc`.
2. Activation must leverage how agents actually follow instructions: named frameworks and closed-stack pointers to `always-tdd` content, not a restatement of that rule. Whether an explicit *load* of `always-tdd.mdc` during Plan is required is an open design question — decide it with evidence, including stockroom incidents where preflight later patched TDD order.
3. The plan's *output contract* (the `tasks.md` template) must make order unmistakable. A TDD disclaimer, a "maps to one TDD cycle" label, or a sibling `Tests first:` field next to `Changes:` is not enough; those shapes are what preflight already FAILs.
4. Keep the existing prose/policy carve-out (`N/A` / no tests for those artifacts; no change-detectors).
5. Leave preflight as the hard gate. Do not restore TDD self-heal.

## Constraints

1. Edit canonical sources under `rulesets/` (and `rules/` if a rule must change). Never edit generated `.cursor/` or `.claude/` copies.
2. Do not duplicate `always-tdd.mdc` doctrine into Plan. Plan owns the schedule; `always-tdd` owns the process.
3. `always-tdd.mdc` is local policy bundled always-on with Niko. It is not a pretrained decompression key the way "Orwell's 6 rules" is. Generic "TDD" / "red-green-refactor" is pretrained — and is the gloss Plan already used, which failed. Daz notes reservations about that particular key; always-tdd's stubbing ritual is the novel part pretrained TDD does not contain.
4. This task's own deliverable is plan-doc / skill wording (prose/policy). Do not invent markdown change-detector tests to satisfy TDD.
5. L4 Plan stays a milestone list; TDD encoding belongs on L2/L3 sub-run plans. L1 has no Plan phase.
6. Prompt-authoring: numbered lists mean order; bullets mean a set. Closed-stack references to `always-tdd` are allowed; restating its body is not.

## Acceptance Criteria

1. L2 and L3 plan instructions cause each executable unit's numbered substeps to follow `always-tdd`'s test-first process (stub tests, stub interface, write tests and watch fail, write code to pass).
2. A plan filled from the template cannot be read as implementation-only steps under a TDD preamble.
3. Prose/policy units remain explicitly exempt.
4. Preflight's TDD Plan Encoding check is unchanged in role: blocking, rearchitect on FAIL, no autonomous TDD rewrite.
5. Design record states how Plan activates `always-tdd` (name/pointer, load, template-as-schedule, or mix) and why, citing stockroom failure modes.
