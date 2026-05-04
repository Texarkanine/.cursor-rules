# Project Brief

Implements the **mechanical alignment** portion of [issue #72](https://github.com/Texarkanine/.cursor-rules/issues/72): the canonical `progress.mdc` rule must be explicitly loaded before `progress.md` is created or updated during phase transitions, because `globs:` auto-attachment cannot match a file that does not yet exist on disk (and can also be bypassed by non-editor write paths).

## User Story

As a Niko operator, I want every Niko skill/reference that writes to `progress.md` to explicitly `Load:` the `progress.mdc` rule first, so that the template is reliably followed on creation and phase-transition updates — not just when the editor happens to auto-attach the rule via `globs:`.

## Use-Case(s)

### Use-Case 1: Fresh task creation

During `/niko` → complexity analysis, `progress.md` does not yet exist. The `globs:` pattern has nothing to match, so the template rule is never attached. The agent invents a shape based on sibling files (`tasks.md`'s `# Current Task: […]` header leaks through) and subsequent writes reinforce that drift.

### Use-Case 2: Phase-transition updates in levels 1-4

Each `levelN-workflow.md` "Phase Mappings" section directs the agent to update `progress.md` when leaving a phase. Without an explicit `Load:`, the agent pattern-matches on the file's current shape rather than the canonical template.

## Requirements

1. `complexity-analysis.md` Step 4 (progress.md creation) must direct the agent to explicitly `Load:` `progress.mdc` before writing the file.
2. Each `levelN-workflow.md` (L1–L4) phase-transition step must direct the agent to explicitly `Load:` `progress.mdc` before updating the file, as a separate numbered step preceding the update.
3. The canonical `Load:` pattern must match prior art in `memory-bank-init.md` (inline `Load: \`path\` and <do X> by following the instructions in the rule.`).
4. Each load directive must briefly document **why** explicit load is required (globs cannot match a not-yet-existing file; non-editor write paths can bypass attachment).

## Constraints

1. **Scope:** mechanical alignment only. The "deeper fix" options (a) extend the template with an IN-PROGRESS grain, or (b) restrict `nk-save` from touching `progress.md` — are explicitly out of scope for this task.
2. **No out-of-scope touches:** `SKILL.md` Step 3b (rework append) must remain untouched — the rework case happens *after* `progress.md` exists, so `globs:` auto-attachment does apply there.
3. **Canonical edits only:** changes must go in `rulesets/niko/**`. Do not hand-edit `.cursor/**` or `.claude/**` (those are synced by ai-rizz / a16n).
4. **Format reference, not restatement:** the edits should point at the rule's Format, not re-author a second copy of it inline (that would create a drift surface).

## Acceptance Criteria

1. Running `/niko` on a fresh memory bank produces a `progress.md` whose title is `# Progress` (not `# Progress: <Task Name>`) and whose sections follow the `[Date] - [Phase] - [Status]` / Work completed / Decisions made / Insights structure.
2. Every phase-transition step in every `levelN-workflow.md` has an explicit `Load:` directive for `progress.mdc` **before** the update directive.
3. `complexity-analysis.md` Step 4 has an explicit `Load:` directive for `progress.mdc` before the `progress.md` creation/replacement instructions.
4. No changes to `SKILL.md` Step 3b or other out-of-scope locations.
5. A single commit on branch `issue-72` captures the change with an accurate, appropriately-scoped commit message.
