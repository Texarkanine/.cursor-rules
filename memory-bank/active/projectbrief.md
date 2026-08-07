# Project Brief: Verification Subagents for Preflight & QA

## User Story

As an operator running Niko across harnesses, I want preflight and QA to run as independent verification subagents (separate context, preferably a different/smarter model family) so validation is not rubber-stamped by the same agent that planned or built — while keeping Niko portable and dual-context safe (parent orchestration vs operator-manual recovery).

## Requirements

1. **Charts are source of truth** — Locked grammar in `memory-bank/active/creative/creative-verification-diagrams-review.md` (C.2a Spawn / Verdict). Level-N workflow mermaid and README charts apply that page; prose percolates from them.
2. **Spawn, not “terminal node”** — Parent `--Spawn-->` forks the verifier. Subagent ends at `Verdict`. Outbound edges from `Verdict` are the parent’s (solid = auto, dashed = operator). Reserve **terminal node** for only-dashed-out nodes (e.g. Reflect → Archive).
3. **Subagent does not advance** — The agent running `niko-preflight` / `niko-qa` stops after verification; it does not load a level workflow or begin another phase.
4. **Parent advances** — After Spawn returns, parent follows the chart edges (including L2 solid preflight→build / QA→reflect).
5. **No orchestration file** — No `run-verification.md`. Model heuristic lives in the Spawn phase-mapping line.
6. **Manual recovery is fully manual** — Operator may run the skill in a new conversation; PASS must not auto-continue; resume via `/niko` or the next slash command per chart.
7. **README long** — Ideology subgraphs (Planning / Execution / Learning) lightly washed; subagent subgraphs default; Preflight⊂Planning; QA⊂Execution.
8. **Minimal direct prose** — Match existing Niko voice.

## Out of Scope

- Changing what preflight/QA *check* semantically (review criteria), except stop/transition wording
- Loading OptMem in verification subagents
- Creative phase as a verification-style subagent (pinned: no)
- Programming Niko as a real AST/state machine (intentional prompt-portable tradeoff)

## Rework

PR [#108](https://github.com/Texarkanine/.cursor-rules/pull/108) operator review — apply all nine agreed fixes:

1. **PASS with ADVISORY** — Restore pass-class semantics (document advisories; still a valid transition/build gate). Drop “not a transition grant.” Align with L2/L3 build prerequisites and creative wording (“record PASS; document advisory…”).
2. **TDD plan-encoding FAIL** — Restore automatic self-heal loop that was removed. Spawn-compatible: verification skill still stops at Verdict; parent (or report routing the parent follows) re-enters plan — do not leave only “tell the operator.” Prefer restoring actionable auto re-plan behavior consistent with charts.
3. **QA forbid line** — Drop `/ruleset/` (and avoid over-specifying product/implementation taxonomy); forbid editing the work under review.
4. **QA allowlist** — Closed exhaustive list of allowed writes (status file, tasks.md findings, progress.md notes, `**Phase:**` in activeContext at Step 4 only). Not a generic `active/` umbrella. Nothing else.
5. **QA FAIL Findings template** — “each semantic finding and why it blocks.”
6. **QA PASS Findings template** — “each semantic finding and why it does or does not block.”
7. **Spawn charge (all sites)** — Split parent duty from child charge. Parent: spawn (prefer smarter/different family if available); do not run skill in this conversation. Parent-authored charge only: `Run the `/niko-qa` skill` or `Run the `/niko-preflight` skill`. Do not say the entire prompt must be exactly that one line (harness/OptMem injection is expected). No task briefing.
8. **Flowchart node names** — Revert abbreviations (`PF`/`PFV`/`QA`/`QAV`) to full indicative names (e.g. prior `NikoPreflight` / `NikoQA`, or `SubNikoQA` style). Apply everywhere relevant (L1–L4 workflows + README charts).
9. **L4 throat-clear** — Delete “Milestone bodies inherit Spawn/QA…”; subgraph + phase-mappings already say it.
