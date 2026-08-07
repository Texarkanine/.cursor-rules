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
| Subagent → `Verdict` | Subagent ends here; does not advance the workflow |
| Edges out of `Verdict` | Taken by the **parent** (solid = auto, dashed = operator) |
| **Terminal node** | Only dashed outs (e.g. Reflect → Archive). Spawn/Verdict phases are **not** terminal nodes |
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

1. **Apply charts** from review page to `level1`–`level4` `*-workflow.md` (mermaid + shared legend language)
2. **Apply README** short / long / per-level / L4 slices from review page (ideology `classDef`; subagents default)
3. **Phase mappings** — Spawn one-liner per verification phase
4. **Secondary sites** — `level2-build.md`, `level3-build.md`, `level4-plan.md` Step 7
5. **Skills** — Step 4 End of Verification + Handle Results micro-edits
6. **Dry-read** walkthroughs 1–6

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

### Phase mapping (preflight; QA swaps skill name)

~~~markdown
- **Level N Preflight Phase**: Spawn a subagent at least as capable as you (smarter / different family if possible) to run the `niko-preflight` skill — do not run the skill in this conversation.
~~~

### Secondary (build missing-preflight)

~~~markdown
🚨 If preflight has not passed: STOP — Spawn a subagent at least as capable as you (smarter / different family if possible) to run the `niko-preflight` skill; do not run it in this conversation. Re-check `memory-bank/active/.preflight-status` before continuing.
~~~

### Skill Step 4

~~~markdown
## Step 4: End of Verification

Update `memory-bank/active/activeContext.md` so `**Phase:**` records this phase complete with PASS or FAIL. Do not load a level workflow or begin another phase. Stop.
~~~

### Handle Results

- preflight “Allow transition to `/niko-build`” → result/advisory only, not a transition grant  
- preflight “re-run `/niko-plan`” → tell the operator in the report  
- qa “Return to the Build/Plan phase” → record that Build/Plan must rerun  

## Status

- [x] Component analysis complete
- [x] Open questions resolved (diagram locked)
- [x] Test planning complete
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Creative (diagram) complete
- [ ] Preflight (re-run after this lock)
- [ ] Build
- [ ] QA
- [ ] Reflect
- [ ] Archive
