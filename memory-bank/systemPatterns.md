# System Patterns: Cursor Rules Repository

## File Organization
- Source rules in `rulesets/` are the source of truth
- `.cursor/**/shared/**/*` contains active copies for Cursor to load
- Edits are only EVER made to `rules/` and `rulesets/` - NEVER to `.cursor/` or `.claude/`

## Rule File Structure (.mdc)
```yaml
---
description: Brief description of the rule
globs: "pattern-for-auto-loading"
alwaysApply: false
---
# Rule Title
> **TL;DR:** One-sentence summary

## Content sections...
```

## Niko System Patterns
- **Complexity Levels**: 1 (simple) to 4 (complex system)
- **Mode Transitions** (level-dependent):
  - L1: NIKO → INTENT CLARIFICATION → BUILD
  - L2: NIKO → INTENT CLARIFICATION → PLAN → PREFLIGHT → BUILD → QA → REFLECT → ARCHIVE
  - L3: NIKO → INTENT CLARIFICATION → PLAN → CREATIVE → PREFLIGHT → BUILD → QA → REFLECT → ARCHIVE
  - L4: Milestone-based composition of L1/L2/L3 sub-runs. Complexity analysis generates `memory-bank/milestones.md` on kickoff, then each milestone executes as an independent sub-run at its own level. Capstone archive consolidates all sub-runs at completion.
- **Intent Clarification**: Fires only on fresh user input (Step 4 "has input" path in `/niko`). L4 milestones, rework, and resume paths bypass it — their input is already validated by prior workflow steps.
- **Memory Bank Files**: Ephemeral (tasks.md, progress.md, creative/, reflection/) vs Persistent (archives, project context)

## Archive Pattern
- Archives live in `memory-bank/archive/<kind>/YYYYMMDD-<task-id>.md`
- Archives should be self-contained (no broken links after `/archive clear`)
- Ephemeral content must be inlined, not linked
