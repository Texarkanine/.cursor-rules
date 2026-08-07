---
task_id: verification-subagents-preflight-qa
date: 2026-08-07
complexity_level: 2
---

# Reflection: verification-subagents-preflight-qa (rework pass 2)

## Summary

Pass 2 folded TDD plan-encoding failure into ordinary rearchitect/`FAIL` → `/niko-plan`, tightened Plan authorship via a `- Tests first:` template substep (stockroom-ratified), and finished the cheap fixups including README long-chart Option A and clear-before-QA-Spawn. QA PASS with two advisories; both resolved or owned in Reflect.

## Requirements vs Outcome

Delivered: no `FAIL (TDD)` species left under `rulesets/niko/`; Handle Results/STOP lists route TDD encoding as rearchitect; L2/L3 plan templates encode per-unit test-before-code with an always-tdd escape hatch; QA status cleared before Spawn; long-chart Fail edges honestly labeled (`L1 Fail / L2+ fixable` → Build, `L2+ rearchitect` → Plan). Out of scope held (no solid TDD auto-heal, no L4 FAIL(TDD) edge, no retry counters).

## Plan Accuracy

Preflight’s amendments (site enumeration, template-not-prose for step 3, operator-gated step 4) were the right build gospel. Stockroom archaeology confirmed the template fix rather than inventing new liturgy. Surprises were process-shaped: stale pass-1 `.preflight-status` correctly blocked `/niko-build`; `.cursor/` lag made both preflight and QA verifiers briefly follow obsolete Step 4 / “apply trivial fixes” instructions until they read canonical `rulesets/`.

## Build & QA Observations

Build was mostly label/prose surgery plus one template change; verify was cheap (`make test`, `mmdc`, ad-hoc `rg`). Operator loop on the long-chart Fail fork (scratch A vs B) was the only multi-turn design beat and landed Option A cleanly. QA was judge-only and clean; advisories were cosmetics (L1 legend, dangling SVG pointers).

## Insights

### Technical
- Plan quality fixes belong in the emitted `tasks.md` template shape, not louder preamble prose — agents fill the blanks they are handed.
- Overview charts want one shared destination edge with a stacked label; per-level charts keep short single-purpose Fail labels.

### Process
- A prior plan’s `PASS WITH ADVISORY` is not a build gate for a new plan — clear and re-Spawn preflight.
- `.cursor/` lag on verification skills is not theoretical: it changed verifier behavior live twice this task (preflight continue-vs-stop; QA fix-vs-judge). Canonical `rulesets/` wins when the question is load-bearing.
- Operator-owned legend trims (L1 drop of unused `🧑‍💻` bullet) are not unplanned drift — record them, don’t auto-revert.

### Million-Dollar Question

If TDD-as-rearchitect and template-encoded test-first had been foundational, pass 1 would never have grown a special `FAIL (TDD)` status/edge/self-heal species. The durable fix was always Plan authorship + ordinary rearchitect routing. What we built is that.

## QA Advisories Disposition

- **L1 legend `🧑‍💻` line:** Operator intentional — L1 has no operator nodes, so the bullet does not belong. Kept. (Dashed-edge legend symbols the L1 chart lacks remain the older deferred L1-legend item; not expanded this pass.)
- **Dangling SVG pointers:** Section rewritten to say scratch SVGs were deleted; mermaid blocks in the creative doc are the durable compare.
