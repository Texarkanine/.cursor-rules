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

## 2026-07-25 - PLAN - COMPLETE

* Work completed
    - Staged `rules/*.mdc` and ran `a16n discover` / IR round-trip dry-runs
    - Wrote full L3 plan in `tasks.md` (components, TDD behaviors, ordered steps, pre-mortem)
    - Dropped `@`-neutralize approach after operator pushback
* Decisions made
    - Description rules (10): a16n cursor → IR → cursor via selective staging + harvest into `rules/<name>/SKILL.md`
    - Commands (2): hand-wrap ManualPrompt skills with `disable-model-invocation: true` (operator: go 1)
    - FileRules/GlobalPrompts: out of scope
* Insights
    - Full-tree convert renames FileRules to `cursor-rules-*` — selective staging is load-bearing
    - a16n `--delete-source` cleans stage/IR only; canonical `git rm` of `rules/` sources is still required
