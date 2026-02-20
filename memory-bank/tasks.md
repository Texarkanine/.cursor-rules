# Task: niko2-l3-reflect-archive-creative

* Task ID: niko2-l3-reflect-archive-creative
* Complexity: Level 3 (meta — this is a niko2 ruleset authoring task)
* Type: Feature implementation (filling in niko2 stubs)

Implement the Reflect skill, Archive skill, Creative skill + phase content, and full Level 3 workflow/plan/build for the niko2 rewrite. Each file is delivered one at a time for operator review.

## Design Decisions

### Creative Phase Orchestration
- Plan identifies "mega-unknowns" — aspects where the implementation approach is genuinely ambiguous or requires design exploration
- `/creative` is invoked once per mega-unknown, routing to the best-fit creative impl (architecture, algorithm, uiux, or generic template)
- Creative either resolves it autonomously (proceeds) or surfaces findings to operator and waits (deus ex humana)
- The determination of WHEN to go creative is the critical L3/L4 plan responsibility

### Reflect & Archive are Level-Dependent
- L1: skips both
- L2+: reflect runs, archive runs
- The skills themselves route to the level-specific workflow for depth/format guidance
- But the niko2 archive template (`archives.mdc`) and reflection template (`reflections.mdc`) already define a universal format with "complexity-level specific sections" — so the skill just needs to scale depth, not switch templates

### Tightening Calibration
- niko2 L2 plan is ~170 lines (vs original L2 planning at ~190 lines of mostly mermaid diagrams)
- niko2 skills (preflight, QA) are ~100 lines of dense, actionable prose — no mermaid, no emoji headers, no checklists-as-verification
- niko2 workflows (L1, L2) are ~55 lines: mermaid graph + legend + operator-stop list + change tracking + phase mappings table
- Target: same density for L3 equivalents. More content than L2 (creative phases add real complexity), but NO bloat

## Implementation Plan — One File at a Time

Each file below is a discrete deliverable. Operator reviews and approves before proceeding to the next.

### File 1: `skills/niko-reflect/SKILL.md` — Reflect Skill
- Pattern: follows QA/preflight skill structure
- Load memory bank → verify prerequisites (QA must have passed) → review implementation against plan → document findings → write reflection file → update memory bank → route to workflow
- Level-scaling: L2 gets a focused reflection (what worked, what didn't, one actionable improvement). L3 adds creative phase effectiveness review and cross-phase analysis. L4 adds strategic insights and enterprise-wide process improvements.
- Output: structured operator-facing summary

### File 2: `skills/niko-archive/SKILL.md` — Archive Skill
- Pattern: follows QA/preflight skill structure
- Load memory bank → verify prerequisites (reflection must exist) → create archive document (INLINE all ephemeral content) → clear ephemeral files → git commit → route done
- Level-scaling: L2 archive is concise. L3 inlines creative phase decisions and reflection. L4 adds architectural documentation and deployment notes.
- Critical: archive format already defined in `niko/memory-bank/archives.mdc` — skill references that, doesn't duplicate it
- Critical: ephemeral cleanup list already defined in `niko/core/memory-bank-paths.mdc`

### File 3: `niko/phases/creative/creative-phase-algorithm.mdc` — Algorithm Creative Phase
- Port from original niko's algorithm creative phase, tightened to niko2 style
- Focus: problem definition, option comparison, complexity analysis, KISS/DRY/YAGNI evaluation
- Output: decision documented in `memory-bank/creative/creative-[feature_name].md`

### File 4: `niko/phases/creative/creative-phase-template.mdc` — Generic Creative Phase Template
- The catch-all for creative explorations that don't fit architecture, algorithm, or uiux
- Provides the universal structure: Problem → Options → Analysis → Decision → Implementation Notes
- Designed to be extensible — new creative phase types can be added by following this template's pattern

### File 5: `skills/niko-creative/creative.md` — Creative Skill (Orchestration)
- The routing skill: receives a flagged mega-unknown from the plan
- Analyzes the nature of the unknown → selects best-fit creative phase impl (architecture, algorithm, uiux, or generic template)
- Executes the creative phase → evaluates outcome
- On RESOLVED: documents decision, returns to workflow
- On UNRESOLVED: presents findings to operator, waits for input (deus ex humana)
- Does NOT loop — one invocation per mega-unknown. The workflow (or plan) handles iteration across multiple unknowns.

### File 6: `niko/level3/level3-workflow.mdc` — Level 3 Workflow
- Pattern: follows L1/L2 workflow structure (mermaid + legend + stop-list + change tracking + phase mappings)
- Phase sequence: Plan → Creative (per mega-unknown, may loop) → Preflight → Build → QA → Reflect → Archive
- Key additions vs L2: creative phase loop, preflight gate before build
- Operator-initiated transitions: Plan (on preflight/QA fail), Archive (after reflect)

### File 7: `niko/level3/level3-plan.mdc` — Level 3 Plan Phase
- Pattern: follows L2 plan structure but adds creative phase flagging
- Critical addition: "Mega-Unknown Identification" step — for each aspect of the plan where the implementation approach is genuinely ambiguous, flag it for creative exploration with a brief problem statement
- The flagging criteria: "If you cannot confidently describe HOW to implement this without exploring multiple approaches, it's a mega-unknown"
- Includes component analysis, cross-module dependency mapping, risk assessment
- TDD test planning still present but at feature/module granularity

### File 8: `niko/level3/level3-build.mdc` — Level 3 Build Phase
- Pattern: follows L2 build structure but adds creative doc review
- Step 1: Review plan AND all creative phase decisions before building
- Module-by-module TDD iteration (vs L2's step-by-step)
- Integration testing across modules after individual module tests pass
- Progress tracking at module granularity in tasks.md

## Status

- [x] File 1: Reflect skill
- [x] File 2: Archive skill (refactored: skills are thin routers, level-specific .mdc files own content)
- [ ] File 3: Creative phase — algorithm
- [ ] File 4: Creative phase — generic template
- [ ] File 5: Creative skill (orchestration)
- [ ] File 6: L3 workflow
- [ ] File 7: L3 plan
- [ ] File 8: L3 build
