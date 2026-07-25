# Progress

Migrate agent-selected description rules and any remaining commands in `rules/` into Cursor agent skills via `npx a16n convert` (cursor → a16n IR → cursor) with `--delete-source`, after careful discover/dry-run enumeration against a16n and ai-rizz docs, with liberal git checkpoints.

**Complexity:** Level 3

## 2026-07-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed Fresh memory-bank state; persistent files already present
    - Clarified and approved intent with operator
    - Classified task as Level 3 and initialized ephemeral memory-bank files
* Decisions made
    - Level 3: multi-component migration with conversion/layout decisions; not L2 (not self-contained) and not L4 (not system-wide redesign)
* Insights
    - `.cursor/commands/shared` is currently empty; discover will confirm whether any commands remain in conversion scope
    - Several `rules/*.mdc` already have non-empty `description:` and `alwaysApply: false` (likely SimpleAgentSkill candidates); always-apply and glob file-rules should stay rules unless discover says otherwise
