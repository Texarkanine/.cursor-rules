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
7. **README long** — Ideology subgraphs (Planning / Execution / Learning) lightly washed; subagent subgraphs default; Preflight�README long** — Ideology subgraphs (Planning / Execution / Learning) lightly washed; subagent subgraphs default; Preflight⊂Planning; QA⊂Execution.
8. **Minimal direct prose** — Match existing Niko voice.

## Out of Scope

- Changing what preflight/QA *check* semantically (review criteria), except stop/transition wording
- Loading OptMem in verification subagents
- Creative phase as a verification-style subagent (pinned: no)
- Programming Niko as a real AST/state machine (intentional prompt-portable tradeoff)
