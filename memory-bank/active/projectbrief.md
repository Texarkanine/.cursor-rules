# Project Brief: Persistent File Reconciliation at Workflow End

## Source

[Issue #57](https://github.com/Texarkanine/.cursor-rules/issues/57) — Ensure persistent files get proper "update if necessary" treatment at end of workflows.

## Problem

Persistent memory-bank files (`productContext.md`, `systemPatterns.md`, `techContext.md`) are created at init and never systematically revisited. Tasks can invalidate their content — removing a workaround documented as a pattern, adding a component that changes how the system works, changing the tech stack. Future sessions start with a stale briefing and make silently wrong decisions.

## Requirements

1. At the end of every code-producing workflow (L1–L3), persistent files must be checked against the work just completed and updated if the work invalidated any of their content.
2. This must happen at every complexity level, including L1.

## Constraints

- **Single source of truth.** The reconciliation logic must live in one place. Non-duplicated logic may live in multiple places.
- **Selective, not routine.** Most tasks won't change persistent files. The step must be a quick scan and skip, not a ritual rewrite.
- **Surgical, not comprehensive.** Update what this task invalidated. Don't audit for unrelated staleness.
- **Respect existing guidance.** Each persistent file has a `.mdc` rule describing what belongs in it and how to write it. The reconciliation step should leverage that, not redefine it.
- **No scope creep into persistent files' purpose.** They capture project knowledge, not task-specific details. A new React component doesn't warrant a `techContext.md` update. A migration from Jest to Vitest does.
- **L4 inherits for free.** L4 sub-runs execute L1/L2/L3 workflows. If those workflows reconcile, L4 gets it automatically.

## User Preferences

- Creative exploration of design options requested before committing to an approach.
