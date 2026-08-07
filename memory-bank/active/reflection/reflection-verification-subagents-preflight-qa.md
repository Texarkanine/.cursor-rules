---
task_id: verification-subagents-preflight-qa
date: 2026-08-07
complexity_level: 3
---

# Reflection: verification-subagents-preflight-qa

## Summary

Shipped Spawn/Verdict orchestration for Niko preflight and QA: charts are SoT, nine verbatim Spawn call sites, skill Step 4 stops without advancing, QA is judge-only. Two QA passes (Opus then GPT Terra after operator rework) both PASS; design held.

## Requirements vs Outcome

All eight brief requirements landed. Charts drive prose; Spawn ≠ terminal node; skills stop; parent follows Verdict edges; no `run-verification.md`; manual recovery does not auto-continue; README ideology wash; prose stayed minimal after operator cuts. Out of scope held (no OptMem in verifiers, no creative-as-verifier, no AST state machine).

## Plan Accuracy

Early plan overbuilt (`run-verification.md`, fork/wait liturgy). Operator amendment before build was the real plan: parent one-liner + skill stop + charts. Breadth walk (nine sites, Step 4, Phase write, Handle Results, L4, L1 QA) prevented the enthusiasm miss. File list and SoT path (`rulesets/niko/` only) were right.

## Creative Phase Review

Three creative layers: wording (Fable), orchestration (Opus), then diagram grammar (C.2a). Structure-first then prose was correct; the diagram creative was the load-bearing one — locking Spawn/Verdict vocabulary stopped the “QA is terminal” pattern-match that would have broken L2 solid edges. Superseded creatives correctly bannered as historical.

## Build & QA Observations

Build was mechanical once charts locked. First QA (Opus) PASS but over-briefed spawn + QA editing product files — operator rework fixed process hygiene, not the design. Re-Spawn on GPT Terra with minimal charge PASS; `mmdc` compile of all 10 blocks was the hard check. Trivial fixes only (L3 throat-clear, `**Phase:**` field).

## Cross-Phase Analysis

Creative overbuild → preflight invalidated → leaner plan → clean build. Operator QA after first PASS caught process smell the skill criteria did not (spawn briefing, judge-vs-fix). Charts-as-SoT made second QA cheap: compile + verbatim grep, not re-litigation. Shared-worktree presumption stayed advisory by design.

## Insights

### Technical
- Mermaid compile (`mmdc`) plus a verbatim-legend/Spawn grep turns diagram grammar into a check, not a reading — keep that for #107 CI.
- Spawn outputs are status/MB files; harnesses that fork a separate worktree break the gate silently. Deliberate tradeoff; do not grow the one-liner to encode it.

### Process
- Over-briefing a verifier makes the evaluation unfalsifiable; charge = load-and-run skill. Parent habits stay out of the legend.
- Reserve “terminal node” for only-dashed-out nodes; Spawn phases use Spawn vocabulary or L2 parents stop after fork.
- First-pass QA PASS is not end of story when the operator is the real judge of process smell — clear status and re-Spawn.

### Deferred (not fixed this task)
- L1 shared legend documents symbols the L1 chart lacks (verbatim-shared was the plan).
- L3 `QA FAIL (fixable)` is solid into an operator-command node.
