# Task: niko2-l3-reflect-archive-creative

* Task ID: niko2-l3-reflect-archive-creative
* Complexity: Level 3 (meta — this is a niko2 ruleset authoring task)
* Type: Feature implementation (filling in niko2 stubs)

Implement the Reflect skill, Archive skill, Creative skill + phase content, and full Level 3 workflow/plan/build for the niko2 rewrite. Each file is delivered one at a time for operator review.

## Design Decisions

### Creative Phase Orchestration
- During planning, the agent identifies **open questions** — aspects where the implementation approach is genuinely ambiguous and requires exploring multiple approaches before committing
- The flagging criteria: "If you cannot confidently describe HOW to implement this without exploring alternatives, it's an open question"
- `/creative` is invoked once per open question, routing to the best-fit creative impl (architecture, algorithm, uiux, or generic)
- Creative either resolves it autonomously (high confidence → proceeds) or surfaces findings to operator and waits (low confidence → deus ex humana)
- The determination of WHEN to enter creative is the critical L3 plan responsibility

### Reflect & Archive: Thin Router Skills + Level-Specific .mdc Files
- Skills (niko-reflect, niko-archive) are pure routers matching the niko-plan pattern
- Level-specific .mdc files own ALL content — zero irrelevant instructions per level
- Workflow files point to .mdc files directly for reflect/archive (not through the skill)
- Rationale: >20% of instructions were irrelevant to non-target levels when inline; split eliminates confusion surface

### L4 is Project Composition, Not a Workflow Level
- **L4 tasks are too big to plan and execute in one pass.** They are composed of multiple L1/L2/L3 sub-runs.
- Complexity analysis recognizes L4 and produces a **milestone list** (high-level bullets, not detailed plans) stored in a known location
- **The milestone list's presence IS the L4 signal.** No milestone list → fresh task, classify normally. Milestone list with unchecked items → pull next milestone. Milestone list with all items checked → capstone archive. This is unambiguous: standalone L1-L3 tasks never have a milestone list; L4 tasks always do.
- For each milestone: `/niko` pulls the next unchecked milestone, complexity-analyzes IT (as L1, L2, or L3), enters the appropriate workflow
- Each sub-run completes through reflect, then loops back to `/niko` for the next milestone
- **No archive between sub-runs** — reflections accumulate, progress accretes, milestone list mutates. Ephemeral files persist across sub-runs.
- **Milestone mutation happens in `/niko` on re-entry**, not in reflect. Reflect is backward-looking; milestone review is forward-looking. On re-entry, complexity analysis reads the latest reflection + remaining milestones and revises if needed.
- **No capstone reflect.** Sub-run reflections already capture everything. The capstone archive consolidates and synthesizes across sub-runs — that IS the retrospective work. A separate reflect step would duplicate it.
- **Dedicated L4 archive** (`level4-archive.mdc`): consolidates the whole project — original milestone list, how it evolved, each sub-run's key outcomes (inlined from their reflections), and the final state of the system. This is the only L4-specific phase file needed.
- No separate L4 plan/build files. L4 plan = milestone list (produced by complexity analysis). L4 build = the sub-run builds.

### Tightening Calibration
- niko2 L2 plan is ~170 lines (vs original L2 planning at ~190 lines of mostly mermaid diagrams)
- niko2 skills (preflight, QA) are ~100 lines of dense, actionable prose
- niko2 workflows (L1, L2) are ~55 lines: mermaid graph + legend + operator-stop list + change tracking + phase mappings table
- Target: same density for L3 equivalents. More content than L2 (creative phases add real complexity), but NO bloat

## Implementation Plan — One File at a Time

Each file below is a discrete deliverable. Operator reviews and approves before proceeding to the next.

### File 1: `skills/niko-reflect/SKILL.md` — Reflect Skill (DONE)
- Thin router matching niko-plan pattern

### File 2: `skills/niko-archive/SKILL.md` — Archive Skill (DONE)
- Thin router matching niko-plan pattern

### File 2a: Level-specific reflect/archive .mdc files (DONE)
- `level2/level2-reflect.mdc`, `level3/level3-reflect.mdc`
- `level2/level2-archive.mdc`, `level3/level3-archive.mdc`
- Updated `level2/level2-workflow.mdc` phase mappings

### File 2b: `niko/level3/level3-workflow.mdc` — Level 3 Workflow (DONE by operator)

### File 3: `skills/niko-creative/creative.md` — Creative Skill (Orchestration)
- Framework first — defines the contract that all creative phase types must fulfill
- Receives a flagged open question from the plan
- Analyzes the nature of the question → selects best-fit creative phase impl (architecture, algorithm, uiux, or generic)
- On RESOLVED (high confidence): documents decision, returns to workflow
- On UNRESOLVED (low confidence): presents findings to operator, waits
- Does NOT loop — one invocation per open question. The workflow handles iteration.

### File 4: `niko/phases/creative/creative-phase-algorithm.mdc` — Algorithm Creative Phase
- Port from original niko, tightened to niko2 style
- Focus: problem definition, option comparison, complexity analysis, KISS/DRY/YAGNI evaluation
- Output: decision documented in `memory-bank/creative/creative-[feature_name].md`

### File 5: `niko/phases/creative/creative-phase-architecture.mdc` — Architecture Creative Phase
- Port from original niko, tightened to niko2 style (currently a stub in niko2)
- Focus: requirements analysis, component identification, architecture options, evaluation, decision
- Evaluation criteria: scalability, maintainability, performance, security, cost, time to market

### File 6: `niko/phases/creative/creative-phase-uiux.mdc` — UI/UX Creative Phase
- Port from original niko, tightened to niko2 style (currently a stub in niko2)
- Focus: style guide integration, user needs, IA, interaction design, visual design, accessibility
- Critical: must check for `memory-bank/style-guide.md` first

### File 7: `niko/phases/creative/creative-phase-generic.mdc` — Generic Creative Phase
- Fallback for open questions that don't fit architecture, algorithm, or uiux
- Uses the universal Problem → Options → Analysis → Decision structure without domain-specific evaluation criteria
- Thinner than specialized phases but covers the long tail

### File 8: `niko/phases/creative/creative-phase-template.mdc` — Creative Phase Authoring Template
- Meta-template for ruleset authors creating NEW creative phase types
- NOT invoked during tasks — this is documentation for extending niko2
- Extracted from the patterns across files 4-7: the contract, the structure, the expected inputs/outputs

### File 9: `niko/level3/level3-plan.mdc` — Level 3 Plan Phase
- Follows L2 plan structure but adds open question identification and creative phase flagging
- Includes component analysis, cross-module dependency mapping, risk assessment
- TDD test planning at feature/module granularity

### File 10: `niko/level3/level3-build.mdc` — Level 3 Build Phase
- Follows L2 build structure but adds creative doc review
- Review plan AND all creative phase decisions before building
- Module-by-module TDD iteration
- Integration testing across modules after individual module tests pass

## Status

- [x] File 1: Reflect skill (thin router)
- [x] File 2: Archive skill (thin router)
- [x] File 2a: Level-specific reflect/archive .mdc files (4 files + workflow update)
- [x] File 2b: L3 workflow (operator-authored)
- [x] File 3: Creative skill (orchestration) — framework first
- [x] File 4: Creative phase — algorithm
- [ ] File 5: Creative phase — architecture
- [ ] File 6: Creative phase — uiux
- [ ] File 7: Creative phase — generic
- [ ] File 8: Creative phase — authoring template (meta)
- [ ] File 9: L3 plan
- [ ] File 10: L3 build

## Future Work (Outside Current Task)

### L4 Implementation
- `level4/level4-workflow.mdc` — milestone-based loop through `/niko`, no dedicated plan/build
- `level4/level4-archive.mdc` — capstone archive consolidating all sub-runs (no separate capstone reflect)
- Updates to `core/complexity-analysis.mdc` — detect L4 (milestone list presence), produce milestones, handle re-entry/mutation, detect completion (all milestones checked)
- Milestone storage location TBD (dedicated section in a known file; its presence/absence is the L4 signal)

### Mermaid Chart Enforcement in Planning/Design Docs
- Enforce appropriate use of mermaid diagrams in L2+ plan and creative phases
- "Appropriate" = enhances intelligibility beyond prose alone. The RIGHT chart at the RIGHT time:
  - **Flowchart**: control flow, decision trees, workflow routing
  - **Class diagram / UML**: code structure — captures INTENT, leaves implementation to implementor
  - **Sequence diagram**: component interactions, API call flows, event sequences
  - **ERD**: data models, relationships, schema design
- Valuable at project brief level and top of tasks.md
- Existing `rules/visual-planning.mdc` has guidelines but isn't rigidly adhered to; want rigid adherence with precise, sparing use
- Consider "pinned info" section in projectbrief.md for north-star charts/requirements
  - Rule: every edit must re-assess pinned info accuracy and relevance
  - Prevents stale diagrams from misleading later phases

### Batch Operation Rule (Non-Niko)
- When multiple independent operations of the same type are needed, batch into a single command
- `rm file1 file2 file3` not three separate deletes
- For tools that don't accept multiple targets, write a shell loop rather than N tool calls
- Reduces token waste, latency, and context pollution
