# System Patterns: Cursor Rules Repository

## File Organization
- Source rules in `rulesets/` are the source of truth
- `.cursor/rules/shared/` contains active copies for Cursor to load
- Both locations must stay synchronized

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
- **Mode Transitions**: NIKO (init) → PLAN → CREATIVE → BUILD → REFLECT → ARCHIVE
- **Memory Bank Files**: Ephemeral (tasks.md, progress.md, creative/, reflection/) vs Persistent (archives, project context)

## Archive Pattern
- Archives live in `memory-bank/archive/<kind>/YYYYMMDD-<task-id>.md`
- Archives should be self-contained (no broken links after `/archive clear`)
- Ephemeral content must be inlined, not linked
