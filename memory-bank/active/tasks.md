# Task: verification-subagents-preflight-qa

* Task ID: verification-subagents-preflight-qa
* Complexity: Level 3
* Type: orchestration / prompt authorship

Preflight and QA run in forked subagents. **Charts are source of truth** (C.2a Spawn / Verdict grammar). Prose percolates from charts. No `run-verification.md`.

## Locked design

**Authoritative chart + legend:** `memory-bank/active/creative/creative-verification-diagrams-review.md` (operator-approved).

| Concept | Meaning |
| --- | --- |
| `--Spawn-->` | Parent forks a subagent to run that phase; do not run the skill in this conversation |
| Subagent → `Verdict` | Subagent ends here; outbound edges taken by the **parent** |
| **Terminal node** | Only dashed outs (e.g. Reflect → Archive) |
| QA contract | Judge only: status/findings/Phase writes; never edit implementation |
| Spawn prompt | Minimal — load and run the skill; no task briefing (parent habit, not legend) |
| README long | Ideology bands (Planning / Execution / Learning) get light wash; subagent boxes unstyled; Preflight⊂Planning, QA⊂Execution |

**Historical only (do not follow for build):** `creative-verification-orchestration.md` (`run-verification.md`), Fable wording blocks as drop-in prose, `creative-l1-verification-diagram.md` options A–G / C.2b. Prefer review-page charts + tight Step 4 / Spawn phase-mapping lines below.

**Pins (out of this task):** creative-exploration as subagent → no; Spawn edge emoji → later.

## Component Analysis

### Affected Components

- Level 1–4 `*-workflow.md`: mermaid + legend (+ STOP lists: do not call Spawn phases “terminal”)
- `rulesets/niko/README.md`: short / long / per-level / L4 abridgments per review page
- Phase mappings + secondary call sites: Spawn one-liner (not “Invoke the skill”)
- `niko-preflight` / `niko-qa`: Step 4 stop + `activeContext` Phase; Handle Results report-only

### Boundary Changes

- Manual skill invoke: PASS does not continue the workflow in that conversation
- Status-file gates unchanged
- Mermaid **does** change (charts first)

## Open Questions

- [x] Diagram grammar → **LOCKED** C.2a Spawn/Verdict (`creative-verification-diagrams-review.md`)
- [x] No `run-verification.md`; Spawn edge + skill stop
- [x] “Terminal node” reserved; Spawn phases use Spawn vocabulary
- [x] README long: ideology wash; QA in Execution; Preflight in Planning

## Breadth gaps

| Gap | Plan response |
| --- | --- |
| Skill Step 4 still continues | Rewrite to stop; write `activeContext` Phase |
| Parent runs skill inline | “Do not run the skill in this conversation” on Spawn call sites |
| Secondary sites “proceed as instructed” | Same Spawn one-liner; re-check status |
| Handle Results transition verbs | Report-only |
| Calling QA/preflight “terminal” in STOP lists | Don’t — Reflect-style only-dashed nodes only |
| Reintroducing `run-verification.md` / wait liturgy | Reject |

## Test Plan

Prose only (`always-tdd` carve-out). Dry-read after charts+prose:

1. L2: Spawn preflight → solid Verdict→build; Spawn QA → solid Verdict→reflect  
2. L3: Spawn preflight → dashed Verdict→`/niko-build`; Spawn QA → reflect  
3. Manual `/niko-preflight` PASS → stop; `/niko` resumes from recorded phase  
4. Skills never load a level workflow after verification  
5. No invoke-and-proceed-in-process call sites  
6. README long: ideology wash; nested subagents; no orphan Spawn nodes  

## Implementation Plan

1. [x] **Apply charts** from review page to `level1`–`level4` `*-workflow.md` (mermaid + shared legend language)
2. [x] **Apply README** short / long / per-level / L4 slices from review page (ideology `classDef`; subagents default)
3. [x] **Phase mappings** — Spawn one-liner per verification phase
4. [x] **Secondary sites** — `level2-build.md`, `level3-build.md`, `level4-plan.md` Step 7
5. [x] **Skills** — Step 4 End of Verification + Handle Results micro-edits
6. [x] **Dry-read** walkthroughs 1–6

## Technology Validation

No new technology - validation not required.

## Challenges & Mitigations

- Drift back to “QA is a terminal node” → breaks solid Verdict edges; use Spawn vocabulary only
- Dark-mode ideology wash → tune fill later; don’t style subagent boxes
- Step 4 soft wording → child continues; must be unconditional stop

## Pre-Mortem

- Build from orchestration creative → wrong design; review page is SoT  
- Charts ship without phase-mapping/skill percolation → agents ignore mermaid  
- C.2b (all-dashed Verdict) creeps back → parent STOPs after Spawn  

## Build-source wording

Paste **verbatim** at every call site of that kind (grep-verifiable tripwire — same technique as the consent header). Do not paraphrase across levels.

### Phase mapping (preflight; QA swaps skill name)

Nine sites total: L1 QA, L2 PF, L2 QA, L3 PF, L3 QA, L4 PF (phase mappings); L2/L3 build missing-preflight; L4 plan Step 7 (use phase-mapping shape below, not the build-guard shape).

~~~markdown
- **Level N Preflight Phase**: Spawn a subagent at least as capable as you (smarter / different family if possible) to run the `niko-preflight` skill — do not run the skill in this conversation.
~~~

Parent post-Spawn behavior is **not** in this line — it lives in the chart + legend (outbound edges from `Verdict` are the parent’s). Ship legends in the same edit as the Spawn call sites.

### Secondary (build missing-preflight)

~~~markdown
🚨 If preflight has not passed: STOP — Spawn a subagent at least as capable as you (smarter / different family if possible) to run the `niko-preflight` skill; do not run it in this conversation. Re-check `memory-bank/active/.preflight-status` before continuing.
~~~

### Skill Step 4

~~~markdown
## Step 4: End of Verification

Update `memory-bank/active/activeContext.md` so `**Phase:**` records this phase complete with PASS or FAIL (e.g. `**Phase:** PREFLIGHT - COMPLETE (PASS)` / `**Phase:** QA - COMPLETE (FAIL)`). Do not load a level workflow or begin another phase. Stop.
~~~

### Handle Results

- preflight “Allow transition to `/niko-build`” → result/advisory only, not a transition grant  
- preflight “re-run `/niko-plan`” → tell the operator in the report  
- qa “Return to the Build/Plan phase” → record that Build/Plan must rerun  

## Preflight Findings (2026-08-07 re-run)

- **PASS** — plan maps all nine call sites + charts/README/skills; TDD carve-out (prose); review page is SoT; superseded creatives bannered
- **Amended** — verbatim Spawn tripwire; L4 plan Step 7 uses phase-mapping shape; Step 4 Phase example; parent continuation = chart/legend
- **Advisory** — at build, treat `creative-verification-orchestration.md` / wording / L1 options as historical only (banners already present); do not edit generated `.cursor/`

## QA Findings (2026-08-07)

- **PASS** — all six plan steps implemented; nine verbatim Spawn sites (7 phase-mapping shape + 2 build-guard shape) and zero residual `Invoke the niko-preflight/qa skill`; both skills' Step 4 = End of Verification with the `**Phase:**` write; Handle Results report-only
- **Charts verified against SoT** — all 10 changed mermaid blocks (README ×6, L1–L4 ×1) compile under `mmdc` 11.14.0; README long renders ideology wash on Planning/Execution/Learning with default-fill subagent boxes nested inside, `Build` inside Execution, no orphan Spawn nodes; L4 README preflight subagent nests correctly inside `First L4 Run`
- **Shared legend is verbatim** across README + all four workflows (5/5 on every new legend line) — a grep-verifiable tripwire like the consent header
- **Dry-reads 1–6 re-run independently** — L2 solid Verdict→build / Verdict→reflect; L3 dashed preflight Verdict, solid QA→reflect, STOP list retains `Preflight PASS -> Build`; skills stop and never load a workflow; `/niko` Step 6 resumes from the recorded `**Phase:**`
- **Fixed (trivial)** — `level3-workflow.md` shipped review-page voice ("terminal-shaped in the old sense… vocabulary stays consistent with L2… The STOP list still includes…"), duplicating both the legend above it and the STOP list below it. Rewritten as one operational line in L2/L4's voice.
- **Fixed (trivial)** — `activeContext.md` used a `## Phase:` heading instead of the `**Phase:**` field that `/niko` Step 6 and `activeContext.mdc` require; normalized while writing the QA verdict. Pre-existing drift in this repo's own memory bank, not a build defect.

### Advisory (non-blocking, for Reflect)

- L1's shared legend documents 🧑‍💻, dashed edges, and `Reflect → Archive` in a chart that has none of them and a file that says L1 has no reflect/archive. Verbatim-shared legend was the plan's choice; tailoring it per level is a design call, not a QA fix.
- Verification subagents write `tasks.md` / `progress.md` / `activeContext.md` / status files, so Spawn presumes a **shared working tree**. Harnesses that fork into a separate worktree would silently break the status-file gate. The amended plan deliberately dropped this precondition from the one-liner.
- Pre-existing, untouched by this build: `level2-workflow.md` labels the archive node `/archive` rather than `/niko-archive`; L3's `QA FAIL (fixable)` edge is solid into the operator-command node `🧑‍💻 /niko-build`.
- `systemPatterns.md` line 21 lists the verbatim-tripwire technique's instances; the nine-site Spawn line is now a third instance. Registering it belongs to Reflect's `reconcile-persistent` pass, not QA.

## QA Findings (2026-08-07 re-Spawn)

- **PASS** — the operator QA rework preserves the locked C.2a Spawn/Verdict design and all six implementation-plan steps.
- **Verified** — all 10 changed Mermaid blocks compile with `mmdc` 11.14.0; nine Spawn call sites are present and no residual `Invoke the niko-preflight/qa skill` wording remains.
- **Verified** — both verification skills stop after recording their result; QA is explicitly judge-only and its permitted writes are constrained to the memory-bank verdict artifacts.
- **Advisory (non-blocking)** — Spawn presumes a shared working tree because verifier outputs are status and memory-bank files; this remains a deliberate portability tradeoff recorded for Reflect.

## Status

- [x] Component analysis complete
- [x] Open questions resolved (diagram locked)
- [x] Test planning complete
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Creative (diagram) complete
- [x] Preflight (PASS with advisory)
- [x] Build (operator QA rework: legend trim, Spawn charge, QA judge-only)
- [x] QA (PASS — re-Spawn after operator rework)
- [ ] Reflect
- [ ] Archive
