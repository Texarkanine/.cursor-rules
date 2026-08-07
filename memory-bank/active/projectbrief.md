# Project Brief: Verification Subagents for Preflight & QA

## User Story

As an operator running Niko across harnesses, I want preflight and QA to run as independent verification subagents (separate context, preferably a different/smarter model family) so validation is not rubber-stamped by the same agent that planned or built — while keeping Niko portable and dual-context safe (parent orchestration vs operator-manual recovery).

## Requirements

1. **Subagent verification** — Preflight and QA execute as forked verification agents; parent waits, reads status/report, then continues existing PASS/FAIL edges.
2. **Child stop via spawn, not skill identity** — The forked agent must stop after one verification pass. That stop is enforced by how the parent invokes the subagent, not by baking “I am a child” into `niko-preflight` / `niko-qa`. Skills remain valid when the operator invokes them directly.
3. **Manual recovery is fully manual** — If a verification subagent never launches, the operator may open a new conversation and run `/niko-preflight` or `/niko-qa` to accomplish verification. On PASS, that recovery path must **not** auto-continue into the next phase. Resume of the normal workflow is a separate new conversation with the normal model selection.
4. **Parent owns phase transitions** — Solid edges (e.g. L2 preflight PASS → build) remain the parent’s job after reading verification results. Mermaid flowcharts stay as-is; subagent is an implementation detail, not a new visual subgraph.
5. **Portable model selection** — Prefer a model at least as capable as the parent, smarter if available, different family if possible. No Composer/vendor SKU hardcoding; must work across Cursor, Claude Code, and unknown harnesses/model menus.
6. **Minimal prose** — Placement of orchestration text must be precise, concise, and maximally efficient. Prefer tiny edits in the right spots (level phase mappings / spawn instructions; skills only if unavoidable) under `rulesets/niko/`.

## Out of Scope

- Redrawing workflow mermaid to depict subagents
- Changing what preflight/QA *check* (semantic content of validation), except as needed for orchestration/stop behavior
- Loading OptMem in verification subagents (explicitly not loaded; treated as desirable independence)
