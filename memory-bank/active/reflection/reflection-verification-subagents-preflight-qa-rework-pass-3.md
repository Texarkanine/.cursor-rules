---
task_id: verification-subagents-preflight-qa
date: 2026-08-10
complexity_level: 3
---

# Reflection: verification-subagents-preflight-qa (rework pass 3 — Mermaid layout)

## Summary

Pass 3 replaced nested Preflight/QA subgraphs with Mermaid subprocess nodes (`[["🐈 …"]]`) and thick `==Spawn==>` edges so Spawn/Verdict charts are human-readable on GitHub / mermaid.live. Build and QA both passed; ideology washes kept without the flatten fallback.

## Requirements vs Outcome

Delivered: readable live charts under `rulesets/niko/` (README short/long/per-level + L1–L4 workflows), Spawn semantics preserved, layout SoT documented in `techContext.md`. Deferred Done/stop shapes stayed deferred. No requirements dropped or silently reinterpreted.

## Plan Accuracy

Six-step build order (short → long → per-level → workflows → audit → verify) matched reality. Long-chart ideology fallback was prepared and unused — the right kind of unused contingency. `/niko` entry chart needed no edit (audit-only step paid for itself as a non-change).

## Creative Phase Review

Option A (subprocess) held up cleanly; operator polish (🐈 labels, no “subagent” word, thick Spawn, triple-cue legend) landed without re-litigating structure. On-chart Verdict → reading note was the right trade: ink stayed honest, doctrine stayed teachable. Creative’s mermaid.live evidence for the short chart predicted Build success; its caution on the long chart was appropriately conservative.

## Build & QA Observations

Build was mechanical once the encoding lock existed — replace clusters, retarget Pass/Fail edges, sync legends. Layout gate (mermaid.live + PNG) mattered more than `mmdc` compile alone. [QA](b563d8a0-864e-475b-8404-b9c24345a248) (gemini-3.1-pro) found no gaps; plan and creative lock matched the diff.

## Cross-Phase Analysis

Root cause was known before Build (Mermaid ignores subgraph `direction` when interior nodes link outside). Creative converted that into an encoding lock; Preflight then Build had little ambiguity left. Cursor-preview-as-SoT was the original failure mode — fixing the gate (techContext + verify step) is as important as fixing the ink.

## Insights

### Technical
- Nested filled subgraphs with cross-boundary edges are a Mermaid/dagre failure class on GitHub; subprocess `[[ ]]` leaves plus thick labeled Spawn edges encode “forked verifier” without that layout trap. Ideology-only clusters can remain if they do not wrap the cross-boundary nodes.

### Process
- For consumer-facing Mermaid, treat mermaid.live / GitHub as layout SoT and Cursor preview as non-authoritative — `mmdc` compile proves syntax, not readability.
