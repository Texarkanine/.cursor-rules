# Project Brief: Verification Subagents for Preflight & QA

## User Story

As an operator running Niko across harnesses, I want preflight and QA to run as independent verification subagents (separate context, preferably a different/smarter model family) so validation is not rubber-stamped by the same agent that planned or built — while keeping Niko portable and dual-context safe (parent orchestration vs operator-manual recovery).

## Requirements

1. **Charts are source of truth** — Level-N workflow mermaid diagrams define process semantics. Prose (phase mappings, skills, secondary call sites, README) percolates from chart+legend changes; not the other way around.
2. **Verification is terminal** — QA and preflight are terminal in the sense chosen in creative (subagent-terminal T1 and/or phase-terminal T2 like Reflect / L3 preflight). The agent that runs verification does not advance the workflow.
3. **Parent (or operator) advances** — Outbound progress after verification is not performed inside the verifier.
4. **Subagent invoke** — Parent forks a subagent (model ≥ self, smarter / different family if possible) to run `niko-preflight` / `niko-qa`; do not run the skill in the parent conversation. No separate `run-verification.md` orchestration file.
5. **Manual recovery is fully manual** — Operator may run the skill in a new conversation; PASS must not auto-continue; resume is a separate conversation (`/niko` or next slash command per chart).
6. **Portable model selection** — Capability heuristic, no vendor SKU hardcoding.
7. **Minimal direct prose** — Match existing Niko voice; no throat-clearing.

## Out of Scope

- Changing what preflight/QA *check* semantically (review criteria), except stop/transition wording
- Loading OptMem in verification subagents
- Programming Niko as a real AST/state machine (intentional prompt-portable tradeoff)
