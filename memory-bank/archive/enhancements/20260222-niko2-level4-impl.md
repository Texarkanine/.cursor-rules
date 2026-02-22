# TASK ARCHIVE: niko2-level4-impl

## METADATA
- **Task ID**: niko2-level4-impl
- **Complexity**: Level 3
- **Date Completed**: 2026-02-22

## SUMMARY

Completed the Level 4 workflow for niko2. L4 is "project composition" — a task too large to plan and execute in one pass is decomposed into milestones, each executed as an independent L1/L2/L3 sub-run. This session added the two missing pieces: a dedicated `level4-plan.mdc` that generates the milestone list and routes to preflight, and a `milestones.mdc` governance doc that defines the format and lifecycle of `memory-bank/milestones.md`. It also updated `complexity-analysis.mdc` to route fresh L4 tasks through the Plan phase instead of attempting inline milestone generation. The previous session (`niko2-level4`) had already delivered `level4-workflow.mdc`, `level4-archive.mdc`, `memory-bank-paths.mdc`, and `systemPatterns.md` updates.

## REQUIREMENTS

From `projectbrief.md` (with design-evolution notes):

1. **`level4-workflow.mdc`** — milestone-based loop diagram, sub-run routing, operator handoff points, capstone archive trigger. ✅ Done in previous session; user-finalized with Plan + Preflight + Archive phase mappings.
2. **`level4-archive.mdc`** — capstone archive: original milestone list and evolution, inlined sub-run summaries, final system state, cross-run insights. ✅ Done in previous session.
3. **`complexity-analysis.mdc` updates** — L4 detection via `milestones.md` presence, re-entry logic (read/check-off/classify), completion detection (all `- [x]` → capstone). ✅ Done (user handled the subtractive edit in this session).
4. **`memory-bank-paths.mdc`** — add `memory-bank/milestones.md` as ephemeral L4-specific file with lifecycle description. ✅ Done in previous session.
5. **SKILL.md routing** — `level4-workflow` and `level4-archive` skills route to their respective `.mdc` files. ✅ Done in previous session.
6. **`memory-bank/systemPatterns.md`** — correct L4 row from sequential workflow to milestone-based composition. ✅ Done in previous session.

**Design evolution (not in original brief):** The original brief's constraint #1 stated "Do NOT add `level4-plan.mdc`" based on the initial design where complexity analysis was the L4 plan. This was revised before this session: the finalized design adds a dedicated L4 Plan phase (generating milestones + routing through preflight) and the corresponding `level4-plan.mdc` and `milestones.mdc`. `tasks.md` captured the evolved design; `projectbrief.md` was not updated.

**This session's deliverables:**
- `level4-plan.mdc` (NEW) — L4 plan phase: load context, verify no milestones.md exists, decompose into 3–7 milestones, write milestones.md, update tasks.md + activeContext.md, log progress, transition to preflight
- `milestones.mdc` (NEW) — governance doc: milestones.md format, quality criteria (independently deliverable, L1/L2/L3-scoped, concrete, non-overlapping), lifecycle table
- `complexity-analysis.mdc` (UPDATE) — removed "Fresh L4 Kickoff" inline section; fresh L4 now routes to level4-workflow.mdc Plan phase

## IMPLEMENTATION

### Architecture: L4 = Project Composition

L4 has no monolithic plan or build phase. Complexity analysis IS the L4 orchestrator:
- **Fresh L4**: `milestones.md` absent → route to Plan phase → Plan generates milestones → Preflight validates → operator re-invokes `/niko` → re-entry begins
- **Re-entry**: `milestones.md` present → check off prior milestone if REFLECT COMPLETE → classify next unchecked as L1/L2/L3 → run sub-workflow
- **Completion**: all `- [x]` → operator invokes `/niko-archive` → capstone archive

The milestone list (`memory-bank/milestones.md`) serves as both the in-flight signal (presence = L4 active) and the state tracker (checkbox state = progress). It is created only by `level4-plan.mdc` and deleted only by `level4-archive.mdc`.

### Key Files

| File | Location (rulesets) | Action |
|------|---------------------|--------|
| `level4-plan.mdc` | `rulesets/niko2/niko/level4/` | NEW — milestone generation phase |
| `milestones.mdc` | `rulesets/niko2/niko/memory-bank/` | NEW — milestones.md governance |
| `complexity-analysis.mdc` | `rulesets/niko2/niko/core/` | UPDATE — removed inline Fresh L4 Kickoff |
| `level4-workflow.mdc` | `rulesets/niko2/niko/level4/` | PREV SESSION — phase diagram + mappings |
| `level4-archive.mdc` | `rulesets/niko2/niko/level4/` | PREV SESSION — capstone archive |
| `memory-bank-paths.mdc` | `rulesets/niko2/niko/core/` | PREV SESSION — milestones.md ephemeral entry |

> All edits target `rulesets/niko2/niko/`; ai-rizz syncs to `.cursor/rules/shared/niko/`.

### level4-plan.mdc structure (7 steps)

1. Load context (memory bank files + milestones.mdc)
2. Verify prerequisites (no milestones.md yet; stop if present)
3. Generate 3–7 milestones using quality criteria from milestones.mdc; add parallelization flowchart if applicable
4. Write `memory-bank/milestones.md`
5. Update `memory-bank/tasks.md` (milestone list + scope estimates) and `memory-bank/activeContext.md` (PLAN COMPLETE + Milestone Plan section)
6. Log progress + print L4 Plan Result summary
7. Phase transition → invoke `niko-preflight` skill

### milestones.mdc placement

Placed in `memory-bank/` subdir rather than `level4/` as originally planned. Rationale: it's a governance doc for a memory-bank file (`globs: memory-bank/milestones.md`), semantically belonging with the other memory-bank governance docs. Install path `.cursor/rules/shared/niko/memory-bank/milestones.mdc` is used consistently throughout the codebase.

### complexity-analysis.mdc change

The "Fresh L4 Kickoff" section (which had attempted inline milestone generation) was removed entirely. The re-entry pre-check was renamed from `## Step 1:` to `## Step 0:` (QA fix — see below) to avoid collision with the Decision Tree `## Step 1:`. Fresh L4 routing is now: classify as L4 → load level4-workflow.mdc → Plan phase handles milestone generation. Clean separation of concerns.

## TESTING

- **Manual inspection**: All 7 steps of `level4-plan.mdc` cross-checked against the implementation plan in `tasks.md`
- **Cross-reference validation**: Install paths for all `.mdc` cross-references verified against file locations post-ai-rizz-sync
- **Lifecycle tracing**: milestones.md creation → re-entry check-off → deletion path traced end-to-end across `level4-plan.mdc` → `complexity-analysis.mdc` → `level4-archive.mdc`
- **Regression check**: L1/L2/L3 decision tree paths in `complexity-analysis.mdc` unaffected by the Step 0 pre-check addition
- **`/niko-qa` semantic review**: PASS — 4 trivial issues found and fixed (see below)

### QA Findings (all fixed)

1. `complexity-analysis.mdc` — duplicate `## Step 1:` heading: re-entry check and decision tree both labeled Step 1. Renamed re-entry check to `## Step 0:`.
2. `level4-plan.mdc` Step 3 — wrong path `memory-bank/milestones.mdc` (memory-bank dir, not rules dir). Fixed to "from milestones.mdc (loaded in Step 1)".
3. `level4-plan.mdc` Step 3 — missing "3–7" milestone count bound. Added to guidance.
4. `level4-plan.mdc` Step 5 — missing `tasks.md` update (plan required both tasks.md + activeContext.md; only activeContext.md was present). Added tasks.md update bullet.
5. `milestones.mdc` — format spec didn't show the optional parallelization flowchart that `level4-plan.mdc` creates. Updated format spec and added clarifying note that complexity analysis identifies milestones by `- [ ]`/`- [x]` markers only.

## LESSONS LEARNED

- **Cross-referencing rule files: use install paths.** In niko2 `.mdc` files, references to other rule files must use the `.cursor/rules/shared/niko/...` install path (post-ai-rizz-sync), not the `rulesets/niko2/niko/...` edit path. The wrong path looks like a valid memory-bank path (`memory-bank/milestones.mdc`) and won't be caught by static analysis — only semantic review catches it. Alternatively, phrase references contextually ("from milestones.mdc loaded in Step 1") to be path-agnostic.
- **Mixed-content milestone files are safe but need documentation.** The optional parallelization flowchart creates a mixed format (diagram + checklist). Complexity analysis's marker-based parsing (`- [ ]`/`- [x]`) is naturally robust to this. The key is documenting the invariant — milestones.mdc now explicitly states this. If the format evolves further (per-milestone metadata), YAML front matter would be cleaner.
- **User-handled subtractive changes are a valid division of labor.** For high-confidence, surgical subtractive edits to core files, having the user make the change themselves is often the right call. Less risk of collateral damage; user can apply the change with full context of their intent.

## PROCESS IMPROVEMENTS

- **Update projectbrief.md when the design changes materially.** This session's projectbrief.md had a stale constraint ("Do NOT add `level4-plan.mdc`") that directly contradicted the actual implementation plan in tasks.md. When the plan phase revises a constraint or key design decision from the brief, amend the brief before finalizing tasks.md. The brief is the north star document — it should never contradict the active plan.
- **Read-back check during build.** For each implementation step, before marking it complete, re-read the plan item verbatim to confirm all sub-bullets were addressed. Issue #4 (missing tasks.md update) would have been caught by "Step 5: Update tasks.md _and_ activeContext.md — did I update both?" This habit takes seconds and prevents QA catching omissions.
- **Flag path-reference risk in plan.** When a task involves writing `.mdc` files that cross-reference other `.mdc` files, add a plan note: "Use install paths (`.cursor/rules/shared/niko/...`), not edit paths (`rulesets/niko2/niko/...`)." Preflight should check for this proactively.

## TECHNICAL IMPROVEMENTS

- **Future: consider YAML front matter for milestone metadata.** As the L4 workflow matures, per-milestone metadata (estimated scope, actual scope, status notes) may become useful for preflight validation or capstone archive generation. Embedding this in the checklist as inline notes works but is harder to parse. YAML front matter in `milestones.md` would provide structured metadata while keeping the checklist clean. Not needed now — surface for future L4 hardening.
- **Future: preflight validation for milestone quality.** Currently `/niko-preflight` receives the milestone list as plain text in the plan output. A dedicated preflight checklist item that validates each milestone against the milestones.mdc quality criteria (independently deliverable, L1/L2/L3-scoped, concrete, non-overlapping) would catch decomposition issues before sub-runs begin.

## NEXT STEPS

None. The L4 workflow is complete end-to-end: complexity analysis routes fresh L4 to the Plan phase, the Plan phase generates and validates milestones, re-entry manages the sub-run loop, and the capstone archive closes the project. The system is ready for a live L4 task to exercise the full workflow.
