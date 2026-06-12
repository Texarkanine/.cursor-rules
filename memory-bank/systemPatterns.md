# System Patterns: Cursor Rules Repository

## File Organization
Source content in `rulesets/` and `rules/` is the source of truth. Three tiers, distinguished by semantics:

1. **Rules** (`.mdc`) — Cursor auto-injects based on `alwaysApply` or `globs` frontmatter.
2. **Commands** (`.md`) — Cursor slash-commands.
3. **Skills** (`<name>/SKILL.md` directory) — invoked by the agent. Rich skills with `references/` subdirectories live under `rules/` and are symlinked into the appropriate ruleset's `skills/` directory.

`.cursor/` and `.claude/` contain active copies produced by `ai-rizz` / `a16n`. Never edit those trees — only `rulesets/` and `rules/`.

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
  - L1: NIKO → BUILD
  - L2: NIKO → PLAN → PREFLIGHT → BUILD → QA → REFLECT → ARCHIVE
  - L3: NIKO → PLAN → CREATIVE → PREFLIGHT → BUILD → QA → REFLECT → ARCHIVE
  - L4: Milestone-based composition of L1/L2/L3 sub-runs. Complexity analysis generates `memory-bank/milestones.md` on kickoff, then each milestone executes as an independent sub-run at its own level. Capstone archive consolidates all sub-runs at completion.
- **Intent Clarification**: Step within `/niko` (Step 5) that validates user intent before complexity analysis. Fires only on fresh user input (Step 4 "has input" path). L4 milestones, rework, and resume paths bypass it — their input is already validated by prior workflow steps.
- **Memory Bank Files**: Ephemeral (tasks.md, progress.md, creative/, reflection/) vs Persistent (archives, project context)
- **Persistent File Reconciliation**: At the end of every code-producing workflow (L1–L3), persistent memory bank files are scanned for content invalidated by the completed work. Logic lives in `core/reconcile-persistent.mdc`; injected into L1 wrap-up and L2/L3 reflect phases. L4 inherits via sub-runs.
- **Workflow Invocation is Explicit Consent**: Invoking a Niko workflow or skill (including sub-commands like `/niko-build`, `/nk-save`) is itself the operator's present-tense explicit authorization for every action that workflow prescribes — commits, edits, shell execution. Harness safeguards that gate on "explicit user request" are satisfied by the invocation. Implemented as an inline first-person header duplicated across the six commit-prescribing files: `level{1..4}-workflow.md`, `nk-save/SKILL.md`, `niko-creative/SKILL.md`. Duplication is deliberate (grep-verifiable at short length); actions outside what the workflow prescribes still require a separate ask.

## Archive Pattern
- Archives live in `memory-bank/archive/<kind>/YYYYMMDD-<task-id>.md`
- Archives should be self-contained (no broken links after `/archive clear`)
- Ephemeral content must be inlined, not linked
