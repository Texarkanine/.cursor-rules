# Project Brief: Verification Subagents for Preflight & QA

## User Story

As an operator running Niko across harnesses, I want preflight and QA to run as independent verification subagents (separate context, preferably a different/smarter model family) so validation is not rubber-stamped by the same agent that planned or built — while keeping Niko portable and dual-context safe (parent orchestration vs operator-manual recovery).

## Authority

- **Gospel for this task:** `memory-bank/active/tasks.md` (the current plan) and this brief. When they conflict with creative docs, the plan/brief win.
- **Creative docs** under `memory-bank/active/creative/` are **exploration** — useful history and grammar notes, not live authority. Do not treat LOCKED creative pages as charts-to-ship.
- **Live shipped charts:** `rulesets/niko/` (level workflows + README). Edit those when changing behavior.

## Requirements

1. **Live charts live under `rulesets/niko/`** — C.2a Spawn/Verdict grammar was explored in creative docs; what ships is the mermaid in level workflows and README. Prose percolates from those live charts.
2. **Spawn, not “terminal node”** — Parent `--Spawn-->` forks the verifier. Subagent ends at `Verdict`. Outbound edges from `Verdict` are the parent’s (solid = auto, dashed = operator). Reserve **terminal node** for only-dashed-out nodes (e.g. Reflect → Archive).
3. **Subagent does not advance** — The agent running `niko-preflight` / `niko-qa` stops after verification; it does not load a level workflow or begin another phase.
4. **Parent advances** — After Spawn returns, parent follows the chart edges (including L2 solid preflight→build / QA→reflect).
5. **No orchestration file** — No `run-verification.md`. Model heuristic lives in the Spawn phase-mapping line.
6. **Manual recovery is fully manual** — Operator may run the skill in a new conversation; PASS must not auto-continue; resume via `/niko` or the next slash command per chart.
7. **README long** — Ideology subgraphs (Planning / Execution / Learning) lightly washed; subagent subgraphs default; Preflight⊂Planning; QA⊂Execution.
8. **Minimal direct prose** — Match existing Niko voice.

## Out of Scope

- Loading OptMem in verification subagents
- Creative phase as a verification-style subagent (pinned: no)
- Programming Niko as a real AST/state machine (intentional prompt-portable tradeoff)
- Bounding `FAIL (rearchitect)` retry loops with a counter (explicitly declined)

## Rework (pass 1 — largely shipped on PR #108)

Operator review of nine inlines — most applied (PASS WITH ADVISORY gate, Spawn charge stem, full node names, QA forbid/Findings, L3 narrative delete, etc.). See git history on `validation-subagents`.

## Rework (pass 2 — current gospel)

Operator decisions 2026-08-07 after breakfast:

1. **Fold TDD plan-encoding failure into `FAIL (rearchitect)`** that kicks back to Plan (existing dashed/operator path on L2/L3). Remove the special `FAIL (TDD)` status value, chart edges, STOP-list carve-outs, and Handle Results / Next Steps / `preflight-status.mdc` vocabulary for it. Rationale: not planning TDD is an architectural failure; same destination as rearchitect.
2. **Do not invent a third preflight failure species on charts.** Fixable vs rearchitect remains the taxonomy; TDD was a misclassified instance of rearchitect, not a forever-special edge.
3. **Tighten Plan so it authors correct TDD structure up front** — preflight was catching factory-bad plans for months; the durable fix is planning guidance, not a perpetual auto-heal carve-out. Use stockroom (`/sr-search`) to find prior sessions where preflight found TDD problems and what information/edits it used to fix them; lift that into level plan docs / always-tdd pointers as needed.
4. **If TDD keeps failing after Plan is tightened** — postmortem: why does Plan keep emitting bad TDD structure? Treat repeated preflight→rearchitect loops as signal, not as a reason to restore a special auto edge.
5. **Remaining cheap CodeRabbit fixups** (one-liners / non-TDD): `/archive`→`/niko-archive` on L2 chart; progress “mermaid unchanged”; Spawn-charge double-backticks in brief/progress; clear `.qa-validation-status` before QA spawn (wording with operator if >1 line); README long QA split fixable/rearchitect (mermaid — with operator). **Do not** implement CodeRabbit’s L4 “split FAIL (TDD)” recommendation — superseded by (1).
6. **Authority reminder** — creative = exploration; `tasks.md` = what we build next.
