---
task_id: verification-subagents-preflight-qa
complexity_level: 3
date: 2026-08-10
status: completed
---

# TASK ARCHIVE: verification-subagents-preflight-qa

## SUMMARY

Shipped independent Preflight/QA verification subagents for Niko (Spawn/Verdict orchestration, nine-site Spawn tripwire, skill Step 4 stop, judge-only QA), then three rework passes culminating in Mermaid chart layout that is human-readable on GitHub / mermaid.live.

**Final visual encoding (pass 3):** nested `PreflightSubagent` / `QASubagent` subgraphs removed; Preflight/QA are Mermaid subprocess nodes (`[[ ]]`) with thick `==Spawn==>` edges; per-level and workflow charts use 🐱 (parent autonomous) / 🐈 (sub-agent); README **long** chart intentionally has **no** emoji (blends multiple levels — cannot faithfully mark manual vs autonomous). Ideology washes (Planning/Execution/Learning) kept. On-chart Verdict node removed; parent owns outbound edges via reading note. Layout SoT = mermaid.live / GitHub (not Cursor preview / casual `mmdc`).

Draft PR: [#109](https://github.com/Texarkanine/.cursor-rules/pull/109) on `flowcharts`. Earlier feature surface largely lived on `validation-subagents` / PR #108 (already reviewed/reworked in-session; this archive is the complete active-MB story on this branch).

## REQUIREMENTS

From the project brief (final form):

1. Live charts under `rulesets/niko/` are authority; creative docs are exploration.
2. Parent Spawns the verifier; outbound Pass/Fail(/rearchitect) edges are the parent’s; “terminal node” = no outbound solid edges (operator polish wording).
3. Verification skills stop after verification — do not advance phases.
4. Parent advances per chart edges after Spawn returns.
5. No `run-verification.md`; model heuristic lives in the Spawn phase-mapping one-liner.
6. Manual recovery is fully manual (PASS must not auto-continue).
7. README long keeps ideology washes when readable; nested subagent clusters forbidden.
8. Minimal Niko voice.

**Pass 2 extras:** fold TDD plan-encoding failure into ordinary rearchitect; Plan templates get `- Tests first:`; no special `FAIL (TDD)` species.

**Pass 3 extras:** charts readable on GitHub/mermaid.live; subprocess encoding; deferred Done/stop shapes.

## IMPLEMENTATION

### Arc (compressed)

1. **Original L3 feature:** Spawn/Verdict charts + nine verbatim Spawn call sites + skill Step 4 End of Verification + Handle Results report-only. Early overbuild (`run-verification.md`) amended out before build. Operator QA hygiene: minimal Spawn charge; QA judge-not-fix.
2. **Rework 1 (L2, PR #108 review):** PASS WITH ADVISORY as build gate; Spawn charge stem; full Mermaid node names; STOP lists aligned with solid edges; status vocabulary.
3. **Rework pass 2 (L2):** Remove `FAIL (TDD)`; TDD encoding → `FAIL (rearchitect)` → Plan; L2/L3 plan templates `- Tests first:` with `N/A for prose & policy artifacts` hatch; clear `.qa-validation-status` before QA Spawn; README long Fail Option A (shared Build-edge label).
4. **Pass 3 (L3, Mermaid layout):** Subprocess encoding across README + L1–L4 workflows; `techContext` Diagrams SoT line; `systemPatterns` standing contract against nested Preflight/QA subgraphs. Operator post-Reflect legend polish (🐈 = sub-agent; terminal = no solid outs); long chart emoji omission intentional.

### Key files touched (final surface)

- [rulesets/niko/README.md](https://github.com/Texarkanine/.cursor-rules/blob/flowcharts/rulesets/niko/README.md) — short/long/per-level charts + shared legend
- `rulesets/niko/skills/niko/references/level{1,2,3,4}/*-workflow.md` — routing maps + legends
- Nine Spawn call sites across level workflows / skills (stem: prefer smarter family; charge = run skill only)
- `rulesets/niko/skills/niko-preflight/`, `niko-qa/` — Step 4 stop + Phase write; judge-only QA
- `memory-bank/techContext.md` — consumer Mermaid layout SoT
- `memory-bank/systemPatterns.md` — no nested Preflight/QA subgraphs; thick Spawn + subprocess encoding

### Creative decisions (inlined)

**Pass 3 — Subagent visual encoding (gospel for charts):** Options A subprocess / B flat diamond+Verdict / C ideology+subprocess. Selected **A**: `[["🐈 …"]]` (or bare `[[ ]]` on long) replaces nested subgraphs; Verdict doctrine → reading note. Long: try ideology+subprocess first; flatten ideology if unreadable (fallback unused). Operator polish: no word “subagent” in labels; 🐈 vs 🐱; thick `==Spawn==>`; later operator clarification that **long chart skips all emoji** because it blends levels.

**Earlier creatives (historical / superseded for live charts):**

- *Verification wording / orchestration:* structure-first then prose; Q1 shared procedure abandoned for parent one-liner; Q2 unconditional Step 4 stop; Q3 model capability ladder. No `run-verification.md`.
- *Diagram grammar / C.2a review page:* Spawn ≠ terminal; solid Verdict edges = parent auto-continue. Live charts later diverged (node names, TDD edge experiments, then subprocess) — review page exploration only.
- *L1 verification diagram / README QA fail edges:* scratch comparisons; Option A long-chart Fail labeling shipped in pass 2; SVGs not durable.

### Operator legend polish (post-Reflect, archived as shipped)

```
🐱 = Phase executed autonomously
🐈 = Phase executed autonomously in a sub-agent
🧑‍💻 = Phase initiated by operator with explicit command
Solid / dashed = operator gating
Outbound edges from a 🐈 sub-agent are taken by the parent once the sub-agent completes.
A node with no outbound solid edges is a terminal node.
```

`==Spawn==>` remains in chart ink; legend no longer restates the “do not run in this conversation” tripwire (still on phase-mapping Spawn stems).

## TESTING

- `make test` green after chart edits
- 10/10 mermaid blocks compile with `mmdc` (syntax only — not layout SoT)
- Dry-read: no `subgraph PreflightSubagent` / `subgraph QASubagent` under `rulesets/niko/`
- Layout: mermaid.live eyeball (short + long); browser Mermaid JS is the acceptance gate
- `/niko-preflight` PASS (gemini-3.1-pro) for pass 3 plan
- `/niko-qa` PASS (gemini-3.1-pro) for pass 3 build
- Prior passes: Opus / GPT Terra QA PASSes; dry-read walkthroughs for nine Spawn sites and Step 4 stops

## LESSONS LEARNED

**Technical**

- Nested filled Mermaid subgraphs with cross-boundary edges fail on GitHub/mermaid.live (subgraph `direction` ignored when interior nodes link outside; edges under fills / cluster borders). Subprocess `[[ ]]` leaves avoid that class; ideology-only clusters can remain if they do not wrap the cross-boundary nodes.
- `mmdc` compile ≠ human layout. Cursor preview lied about the same charts.
- Spawn outputs are status/MB files — shared working tree is a silent assumption of the fork design.
- Solid chart edges are insufficient if STOP lists still name the old transition.
- Plan quality for TDD belongs in the `tasks.md` template shape (`- Tests first:`), not a special preflight self-heal species.

**Process**

- Over-briefing a verification subagent makes evaluation unfalsifiable — charge = load-and-run skill only.
- Reserve “terminal node” for nodes with no solid outs; Spawn is not a terminal vocabulary.
- Stale `.preflight-status` / `.qa-validation-status` and lagging `.cursor/` skill copies change verifier behavior live; clear status for *this* plan; read canonical `rulesets/` when load-bearing.
- Creative overbuild → amend lean → charts-as-SoT paid off once encoding locked.

## PROCESS IMPROVEMENTS

- Consumer-facing Mermaid: check mermaid.live / GitHub before calling Build done; document SoT in `techContext`.
- Preflight PASS WITH ADVISORY is a valid build gate for localized plan amendments; a prior plan’s status is not a gate for a new plan.
- When overview charts stack multiple levels, prefer honesty (no emoji) over forced 🐱/🐈 that would mis-teach.

## TECHNICAL IMPROVEMENTS

- Deferred: Done/MergePR → Mermaid stop (double-circle) / terminal (stadium) shapes — needs GitHub Mermaid version check.
- Optional: restore a one-line Spawn legend tripwire if agents miss phase-mapping stems.
- Issue #107 (mmdc compile CI) remains useful as a *syntax* gate, not a layout gate.

## NEXT STEPS

- Merge / squash [PR #109](https://github.com/Texarkanine/.cursor-rules/pull/109) (`flowcharts`).
- Optional `chore(dev): ai-rizz sync` after push so generated `.cursor/` / `.claude` catch chart/legend lag.
- Optional follow-ups: Done/stop shapes; L3 QA FAIL(fixable) solid into `/niko-build` operator node (older open question); if TDD encoding keeps failing after Plan tighten → postmortem, not a special edge.
