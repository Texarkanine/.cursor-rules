# TASK ARCHIVE: niko2 — L3 / Reflect / Archive / Creative

## METADATA
- **Task ID**: niko2-l3-reflect-archive-creative
- **Complexity**: Level 3 (meta — niko2 ruleset authoring)
- **Date Completed**: 2026-02-21

## SUMMARY

Implemented the majority of the niko2 rewrite: all L1–L3 phase documents (plan, build, reflect, archive), the complete creative phase system (orchestration skill + 4 phase types + authoring template), and the L3 workflow. L4 was intentionally stubbed as future work. The entire build was committed as one batch (`f18c9c1 chore: add niko2 ruleset`) because niko2's own scaffolding wasn't yet in place to enforce incremental commits.

This was a bootstrapping task: authoring a workflow tool without that tool guiding its own construction.

## REQUIREMENTS

The task was to fill in stubs from the niko2 rewrite (PR #39 / `67b4ae7`), delivering:

1. Reflect phase: thin-router SKILL.md + level-specific `level2-reflect.mdc` and `level3-reflect.mdc`
2. Archive phase: thin-router SKILL.md + level-specific `level2-archive.mdc` and `level3-archive.mdc`
3. L3 workflow: `level3-workflow.mdc` with mermaid graph, legend, operator-stop list, change tracking, phase mappings
4. Creative phase orchestration: `niko-creative/SKILL.md` — dual-mode, routes to 4 phase types, confidence evaluation
5. Creative phase types: algorithm, architecture, uiux, generic — each a standalone document
6. Creative phase authoring template: meta-template for future phase type authors
7. L3 plan phase: `level3-plan.mdc` — component analysis, open question identification, creative loop, TDD at component boundaries
8. L3 build phase: `level3-build.mdc` — creative doc review, module-by-module TDD, integration testing
9. L4 stubs: `level4-workflow.mdc`, `level4-plan.mdc`, `level4-build.mdc` — placeholder files, not implemented

Additionally delivered but not in original plan:
- `always-tdd.mdc`, `test-running-practices.mdc`, `visual-planning.mdc` — companion rules
- Complete `memory-bank/*.mdc` template files
- `.cursor/skills/shared/niko*/SKILL.md` wrapper files for Cursor IDE deployment

## IMPLEMENTATION

### Architecture

niko2 has a two-layer structure:
- **Content layer**: `.cursor/rules/shared/niko/**/*.mdc` — the actual ruleset content, loaded by agents in Cursor IDE context
- **Skill layer**: `.cursor/skills/shared/niko*/SKILL.md` (Cursor IDE) and `.claude/skills/` (Claude Code / ai-rizz) — thin wrappers that load and execute the content

The SKILL.md files for phases (plan, build, reflect, archive) are pure routers: they read the task's complexity level from `memory-bank/activeContext.md` and load the appropriate level-specific .mdc file. No phase logic lives in the SKILL.md itself.

### Key Design Decisions

**Thin-router pattern for reflect/archive**: SKILL.md files mirror the niko-plan pattern — pure routing, zero phase content. Level-specific .mdc files own ALL content. Rationale: >20% of inline instructions were irrelevant to non-target levels, creating confusion surface.

**L4 as project composition**: L4 tasks are too large to plan and execute in one pass. They are composed of multiple L1/L2/L3 sub-runs. Complexity analysis produces a milestone list; each sub-run completes through reflect, then `/niko` is re-invoked for the next milestone. The milestone list's presence IS the L4 signal. No capstone reflect — the capstone archive synthesizes sub-run reflections. (Milestone storage location: `memory-bank/milestones.md` — resolved in a standalone creative phase in the subsequent session.)

**Creative phase dual-mode**: `niko-creative` operates either within a niko workflow (invoked by the plan phase for flagged open questions) or standalone (operator invokes directly with a question). In workflow mode, context comes from the memory bank; in standalone mode, the operator provides the question. One invocation per open question; the workflow handles iteration.

**Open question terminology**: "mega-unknown" → "open question". Tested with a blind subagent — "mega-unknown" is not standard terminology and caused confusion.

**style-guide.md dropped**: visual style authorities folded into techContext.md Design System section. Reduces file count; techContext is already loaded by most phases.

**L3 workflow authored by operator** (File 2b): TD layout (not LR), explicit creative loop branch, operator gates at preflight/reflect/archive transitions. This was the structural spine that all other L3 phase files reference.

### Files Delivered (content layer)

```
.cursor/rules/shared/
  always-tdd.mdc                              (companion rule)
  test-running-practices.mdc                  (companion rule)
  visual-planning.mdc                         (companion rule)
  niko-core.mdc                               (core persona/principles)
  niko/core/
    complexity-analysis.mdc                   (L1–L4 detection, ephemeral file init)
    memory-bank-init.mdc                      (persistent file initialization)
    memory-bank-paths.mdc                     (canonical file locations)
  niko/level1/
    level1-workflow.mdc                       (LR graph, build→qa→done)
    level1-build.mdc                          (single-file TDD build)
  niko/level2/
    level2-workflow.mdc                       (TD graph, plan→preflight→build→qa→reflect→archive)
    level2-plan.mdc                           (~170 lines, dense actionable prose)
    level2-build.mdc                          (TDD build with preflight gate)
    level2-reflect.mdc                        (post-build reflection)
    level2-archive.mdc                        (self-contained archive doc)
  niko/level3/
    level3-workflow.mdc                       (TD graph with creative loop branch)
    level3-plan.mdc                           (component analysis, open question id, creative loop)
    level3-build.mdc                          (creative doc review, module TDD, integration testing)
    level3-reflect.mdc                        (full lifecycle review, cross-phase analysis)
    level3-archive.mdc                        (inline all ephemeral content)
  niko/level4/
    level4-workflow.mdc                       (STUB: "not implemented yet, stop")
    level4-plan.mdc                           (STUB: empty)
    level4-build.mdc                          (STUB: empty)
  niko/phases/creative/
    creative-phase-algorithm.mdc              (problem def, option comparison, KISS/DRY/YAGNI)
    creative-phase-architecture.mdc           (quality attribute ranking, risk/reversibility)
    creative-phase-uiux.mdc                   (design system check, accessibility first-class)
    creative-phase-generic.mdc                (derived criteria, bikeshedding guard)
    creative-phase-template.mdc               (meta-template for future phase authors)
  niko/memory-bank/
    activeContext.mdc, archives.mdc, creative.mdc, preflight-status.mdc,
    productContext.mdc, progress.mdc, projectbrief.mdc, qa-validation-status.mdc,
    reflections.mdc, systemPatterns.mdc, tasks.mdc, techContext.mdc
```

### Files Delivered (skill layer — Cursor IDE)

```
.cursor/skills/shared/
  niko/SKILL.md             (entry point: load memory bank, complexity analysis)
  niko-plan/SKILL.md        (router: reads level → loads level-specific plan .mdc)
  niko-preflight/SKILL.md   (preflight validation, writes .preflight-status)
  niko-build/SKILL.md       (router: reads level → loads level-specific build .mdc)
  niko-qa/SKILL.md          (semantic QA, writes .qa-validation-status)
  niko-reflect/SKILL.md     (router: reads level → loads level-specific reflect .mdc)
  niko-archive/SKILL.md     (router: reads level → loads level-specific archive .mdc)
  niko-creative/SKILL.md    (dual-mode creative phase orchestration)
  refresh/SKILL.md          (unstuck guidance for repeated failures)
```

### What Was Removed

Commit `8a5c12d chore: remove old Niko` deleted the original niko implementation:
- `.cursor/rules/shared/niko/Core/*.mdc` (8 files, ~1800 lines) — complex optimization/mode-transition system
- `.cursor/rules/shared/niko/Level1-3/*.mdc` (9 files) — original level workflows
The original niko was ~3500+ lines of tightly coupled rules; niko2 replaces it with ~3500 lines of modular, level-scoped content where each file is independently meaningful.

## TESTING

- No automated tests exist (markdown/ruleset project)
- Operator reviewed each file as delivered, applying edits before approving
- Creative phase algorithm.mdc tested with haiku subagents: high-confidence and low-confidence paths both verified to produce correct output format
- L3 workflow mermaid diagram reviewed for correctness by operator
- The `.claude/skills/` equivalents (Claude Code deployment) were exercised during the session itself — the niko2 system was used to run the session while being authored

## LESSONS LEARNED

- **Bootstrapping paradox**: A workflow tool cannot guide its own construction. The structured niko2 phases (preflight, change-tracking, incremental commits) were absent during niko2's own build. This is expected and unavoidable — acknowledge it explicitly at the start of any meta-build task.
- **Design decisions in tasks.md substitute for creative phase docs**: When the creative phase machinery isn't available, capturing design decisions explicitly in `tasks.md` (with options considered, rationale, and implementation notes) provides equivalent value. The `## Design Decisions` section in this task's tasks.md was the de-facto creative archive.
- **Operator review as QA gate**: For ruleset authoring, the operator reading and editing each file is a valid QA substitute. The `.qa-validation-status` artifact is less meaningful here than in code tasks.

## PROCESS IMPROVEMENTS

- **Incremental commits should be explicit in meta-build tasks**: Even without niko2 guiding the process, a convention like "commit each file immediately after operator approval" should be stated upfront. The single-batch commit makes it harder to reconstruct the order of decisions.
- **Uncommitted cleanups accumulate**: `.cursor/commands/niko*` deletions (old command system) were left unstaged at task close. Cleanup work should be committed immediately. At time of archive, these deletions remain uncommitted on the `niko2-level4` branch.

## TECHNICAL IMPROVEMENTS

- **Dual-target architecture needs documentation**: niko2 deploys to two targets — `.cursor/skills/shared/` for Cursor IDE and `.claude/skills/` for Claude Code (ai-rizz). The `.claude/skills/` files are the "live" system in the current session; the `.cursor/` files serve Cursor IDE. This parallel structure isn't documented and would confuse a new contributor. A README or `systemPatterns.md` entry should explain it.
- **L4 is fully stubbed and ready for implementation**: The stubs are correct (they fail gracefully with "not implemented" rather than silently misbehaving). Next session should implement `level4-workflow.mdc` and `level4-archive.mdc`, update `complexity-analysis.mdc` for L4 detection, and create the `milestones.md` lifecycle documentation.

## NEXT STEPS

1. **Commit the uncommitted `.cursor/commands/niko*` deletions** (old command system cleanup)
2. **Implement L4 workflow** — `level4-workflow.mdc`, `level4-archive.mdc`, `complexity-analysis.mdc` updates, `memory-bank/milestones.md` lifecycle. Milestone storage location resolved: `memory-bank/milestones.md`.
3. **Document dual-target architecture** in `memory-bank/systemPatterns.md` or a README
