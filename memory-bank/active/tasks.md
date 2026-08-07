# Task: verification-subagents-preflight-qa

* Task ID: verification-subagents-preflight-qa
* Complexity: Level 3
* Status: PLAN IN PROGRESS — open questions pending creative (prefer Opus/Fable for authorship)

## Component Analysis

### Affected components

| Component | Role today | Change needed |
| --- | --- | --- |
| `rulesets/niko/skills/niko-preflight/SKILL.md` | Full preflight procedure; Step 4 loads level workflow and may continue to next phase | End verification without auto-GO (recovery must not continue). Must not encode “I am a child.” |
| `rulesets/niko/skills/niko-qa/SKILL.md` | Full QA procedure; same Step 4 continue pattern | Same as preflight |
| `level1-workflow.md` … `level4-workflow.md` Phase Mappings | `Invoke the niko-preflight/qa skill` (inline, one line each) | Parent: fork verifier → wait → read status → continue existing PASS/FAIL edges. Mermaid unchanged. |
| Phase Transition call sites that invoke verification | e.g. `level2-build.md` / `level3-build.md` “if preflight missing, invoke skill”; `level4-plan.md` Step 7 “Invoke preflight”; plan docs’ “execute next phase” | Must not reintroduce single-context “invoke skill and proceed as instructed” that lets a verifier continue into build |
| Optional shared reference under `skills/niko/references/` | None today for verification orchestration | Creative decides: one shared “how to run verification” fragment vs verbatim duplication in each call site |
| `rulesets/niko/README.md` | Documents phases; mermaid is logical flow | Touch only if prose claims single-context continuity that becomes false; no subagent subgraph |

### Cross-module dependencies

- Level workflows → skills (invoke)
- Plan/Build phase docs → skills (recovery / missing-preflight paths)
- Skills Step 4 → level workflows (today’s continue path — the failure mode for a forked verifier)
- Status files (`.preflight-status`, `.qa-validation-status`) already gate Build/Reflect — parent resume should key off these

### Boundary changes

- Behavioral contract of `/niko-preflight` and `/niko-qa` when invoked directly: **PASS no longer means “continue the workflow in this context.”** Verification completes; resume is parent orchestration or a new operator-started conversation.
- Public skill names and status-file contracts stay the same.

### Invariants & constraints

- Must preserve: PASS/FAIL edge semantics on level mermaid (logical flow unchanged)
- Must preserve: dual-context — parent fork path and operator-manual skill invoke both valid
- Must preserve: skills installable alone (no Cursor-only APIs or OptMem assumptions in skill body)
- Must hold: child stop comes from spawn/parent instructions, not skill self-identity as “child”
- Must hold: manual recovery on PASS does not auto-continue
- Must hold: portable model heuristic (as capable / smarter if available / different family if possible)
- Must hold: minimal prose — placement over volume
- Non-goal: OptMem in validators; redrawing mermaid for subagents; changing what preflight/QA check semantically

### Alignment with systemPatterns

- Canonical edits under `rulesets/niko/` only (not `.cursor/`)
- Prefer pointing at skills over reproducing procedures — but orchestration (fork/wait/resume) is new and may need a single shared fragment; check whether duplication is load-bearing before DRYing
- Workflow invocation = consent still applies to parent commits after subagent returns

## Open Questions (for creative)

### Q1: Placement factoring

**Problem:** Where does the fork/wait/read/resume + spawn-stop + model-heuristic text live so it is correct at every call site without bloating skills or baking child identity into them?

**Why ambiguous:** Options include (a) one shared reference loaded by every phase-mapping line and build/plan recovery path, (b) verbatim short block duplicated at each call site (grep-verifiable), (c) skill Step 4 always-stop only + thin phase-mapping changes. Wrong factoring either breaks recovery, lets children continue, or over-edits.

**Constraints:** Minimal text; dual-context; no child-identity in skills; mermaid untouched; portable across harnesses.

### Q2: Exact skill Step 4 contract

**Problem:** What is the precise end-state of `niko-preflight` / `niko-qa` after writing status — always stop? stop except when…? What does the report tell the operator vs the parent?

**Why ambiguous:** Today Step 4 continues when operator input is not required. Recovery ideology says never GO from the skill. Parent solid edges still need someone to continue. Need exact wording that covers both without “you are a subagent.”

**Constraints:** Manual recovery fully manual; parent owns GO; skill remains correct when operator-invoked in a fresh window.

### Q3: Portable spawn / model selection wording

**Problem:** How to instruct “fork a verification agent with model ≥ self, prefer smarter / different family” without Cursor Composer steering or harness-specific tool names that break Claude Code / others?

**Why ambiguous:** Harnesses differ (Task tool + model enum vs other agent spawn). Over-specific = non-portable; over-vague = parent stays in-process or picks Composer.

**Constraints:** No vendor SKU hardcoding; works when model menu is unknown; prefer different family when possible.

## Test Planning

Out of scope for TDD executable suite: this task changes rule/skill/workflow prose only (`always-tdd` carve-out). Verification is review + dry-read of dual-context paths (parent fork vs manual invoke) against the brief — not change-detector tests on document contents.

## Implementation Plan

Deferred until open questions Q1–Q3 are resolved in creative. Skeleton expected after creative:

1. Apply agreed skill Step 4 contract to `niko-preflight` and `niko-qa`
2. Apply agreed orchestration fragment to level workflow Phase Mappings (and any shared reference)
3. Fix secondary call sites (build missing-preflight, L4 plan → preflight) to the same contract
4. README touch only if a false single-context claim remains
5. Dry-read walkthrough: L2 parent PASS→build; L3 PASS→wait `/niko-build`; manual recovery PASS→stop; subagent never continues
