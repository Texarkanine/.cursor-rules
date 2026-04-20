# Active Context

**Current Task:** Migrate manual rules to skill resources
**Phase:** PREFLIGHT - COMPLETE (PASS)

## What Was Done

- Ran Level 3 preflight against the plan.
- Inspected ai-rizz source to verify how it handles skill subdirectories. Found `cp -rL` at line 4826 — full subtree preserved. Target dir is `.cursor/skills/shared/<name>/` for commit mode.
- Plan blocking fix: updated Cursor-form path from `.cursor/skills/niko/resources/...` → `.cursor/skills/shared/niko/resources/...` (the `shared/` infix is ai-rizz's commit-mode convention).
- Consolidated script count 3 → 2 matching user's mental model: `audit_manual_rules.py` (helper) + `migrate_manual_rules.py` (main, with subcommands `preview`, `rewrite-refs`, `move-files`, `verify`).
- `migration-audit.json` earmarked for gitignore.
- Advisory: `a16n` behavior for the `shared/` infix will be verified during QA dry-run.

## Next Step

Proceed to Build phase: author `scripts/audit_manual_rules.py` and `scripts/migrate_manual_rules.py`, then run `audit → preview → (operator approves) → rewrite-refs → move-files → verify → docs → ai-rizz sync → a16n dry-run → commits`.

Operator input required at the approval gate between `preview` and `rewrite-refs`.
