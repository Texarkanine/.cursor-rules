# Project Brief

## User Story

As the operator, I want Preflight to return one of four results so build, autonomous re-plan, and operator re-plan are distinct, and I want scheduled change-detector tests struck in-phase the same way reversed TDD steps already are.

## Use-Case(s)

### Use-Case 1

Numbered steps say “write X, then write tests for X.” Preflight swaps them to “write tests for X, then write X,” records the finding, writes `PASS WITH ADVISORY`.

### Use-Case 2

A numbered step is a scheduled change-detector. Preflight deletes that step. Keep the other steps. Records the finding, writes `PASS WITH ADVISORY`.

### Use-Case 3

Plan has issues with known fixes. Preflight writes `FAIL (fixable)`. Planner re-plans. Parent → Plan, no operator. May loop.

### Use-Case 4

The plan has issues that require materially changing it. Preflight writes `FAIL (blocking)`. Operator provides guidance, then invokes `/niko-plan`.

### Use-Case 5

Bookkeeping: `.preflight-status` first line is one of the four result strings; the rest of that file is this run's findings. `progress.md` logs that Preflight completed. `tasks.md` changes only via in-phase swap/strike.

## Requirements

1. Judge and report. The only in-phase plan writes are the TDD step-swap and striking scheduled change-detector steps.
2. Four outs, exact strings: `PASS`, `PASS WITH ADVISORY`, `FAIL (fixable)`, `FAIL (blocking)`.
3. `PASS` and `PASS WITH ADVISORY` unblock build. Proceed if that level allows autonomy (L2 solid → build; L3 still dashed `/niko-build`).
4. `FAIL (fixable)`: plan has issues with known fixes; planner re-plans; parent → Plan; no operator; may loop.
5. `FAIL (blocking)`: plan has issues that require materially changing the plan; operator provides guidance, then `/niko-plan`. Meanings live in `preflight-status.mdc`; do not grow a second glossary in the skill.
6. Missing tests on an executable unit, a convention/conflict that needs a different approach, and brief-level scope change are not in-phase.
7. Bookkeeping writes stay. `.preflight-status` first line is the four-value enum (no bare `FAIL`). Findings for this run follow in the same file.
8. `FAIL (fixable)` name reuse with QA is intentional. Do not rename. Different checks, different semaphore files.
9. Nine-site Spawn stem unchanged (still “run the skill only”).
10. L2 and L3 workflow charts and STOP lists match the four outs. README charts that still show a single Preflight FAIL match them too. L4 splits FAIL only because blocking vs fixable now exists. L1 has no Preflight.

## Constraints

1. Canonical edits under `rulesets/` only.
2. `niko-qa` unchanged. No QA edge rewrite.
3. No general plan amendment. No emitting missing always-tdd stages.
4. Status file: first line is the semaphore; the body is this run's findings. Not a structured schema.
5. No nested Preflight/QA subgraphs in Mermaid.

## Acceptance Criteria

1. The skill forbids design amendments, synthesized tests, and applying Radical Innovation. In-phase writes are only the TDD swap and change-detector strike.
2. After a TDD swap or a change-detector strike: `PASS WITH ADVISORY` and a finding, unless another check fails.
3. Handle Results and the status file use the four strings. `FAIL (fixable)` → Plan. `FAIL (blocking)` → operator provides guidance, then `/niko-plan`. Not “re-run `/niko-preflight`” as the fixable next step.
4. L2/L3 STOP lists treat only `FAIL (blocking)` (and L3 PASS / PASS WITH ADVISORY → build) as operator gates. `FAIL (fixable)` is not a STOP.
5. The brief does not require writing missing always-tdd stages.

## Prior rework

Judge-only shipped, then TDD swap-only. This pass is https://github.com/Texarkanine/.cursor-rules/issues/114: four-way outs plus change-detector strike. Supersedes the earlier “change-detectors stay FAIL and do not patch.”

## Rework

Cut Handle Results (step 10) from `niko-preflight`. Preflight reports and stops.

### User Story

As the operator, I want Preflight to write the result it already judged and stop, so parent routing is not restated inside the skill.

### Use-Case(s)

#### Use-Case 1

Checks finish. Write Status copies the already-chosen first line from the mdc allowed values, then this run’s findings. No Handle Results step.

#### Use-Case 2

TDD missing-tests fails. The TDD bullet writes `FAIL (blocking)`. It does not point at Handle Results.

#### Use-Case 3

A swap or strike records a finding and continues. That does not pick an out. If Judge still PASSes, the first line is `PASS WITH ADVISORY` because advisories exist, not because a Write Status override said so.

### Requirements

1. Delete step 10 Handle Results.
2. TDD missing-tests: write `FAIL (blocking)`; do not say “Route as … (Handle Results)”.
3. Write Status stays: one allowed value from `preflight-status.mdc`, then this run’s findings. Do not add “PASS WITH ADVISORY unless another check fails”.
4. Drop the FAIL print Next Steps menu (parent routing). Keep the PASS / FAIL print blocks otherwise.
5. Step 4 still copies the first line into `**Phase:**` and stops.

### Constraints

1. Canonical edits under `rulesets/` only.
2. `niko-qa` unchanged.
3. Do not revert README/L3 chart aesthetics.
4. Do not grow a second glossary in the skill.
5. Status is determined upstream; Write Status serializes it.

### Acceptance Criteria

1. `niko-preflight` has no Handle Results step.
2. The skill does not tell the Preflight agent to invoke Plan or `/niko-plan`.
3. The skill does not contain “PASS WITH ADVISORY unless another check fails”.
4. FAIL print has no Next Steps subsection.
