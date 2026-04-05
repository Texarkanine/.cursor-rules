---
task_id: issue-57-persistent-file-reconciliation
complexity_level: 3
date: 2026-04-05
status: completed
---

# TASK ARCHIVE: Persistent File Reconciliation at Workflow End

## SUMMARY

Added a shared reconciliation rule (`reconcile-persistent.mdc`) and injected it into L1 wrap-up and L2/L3 reflect phases so that, after every code-producing Niko workflow (L1–L3), agents scan `productContext.md`, `systemPatterns.md`, and `techContext.md` for content that is factually wrong or materially incomplete relative to the work just completed, and update only what that task invalidated. L4 needs no change: sub-runs use L1–L3 workflows. QA added a bullet to `systemPatterns.md` documenting the new pattern (closing a plan gap that had deferred that update as “self-referential”).

Source: [Issue #57](https://github.com/Texarkanine/.cursor-rules/issues/57).

## REQUIREMENTS

From the project brief:

1. At the end of every code-producing workflow (L1–L3), persistent memory bank files must be checked against completed work and updated when invalidated.
2. **Single source of truth** for reconciliation logic (non-duplicated logic may appear only as “load and follow” at injection sites).
3. **Selective, not routine** — quick scan and skip when nothing applies; not a full rewrite ritual.
4. **Surgical, not comprehensive** — only what this task invalidated; no unrelated staleness audits.
5. **Respect existing guidance** — each persistent file’s `.mdc` rule defines content; reconciliation defers to those rules.
6. **No scope creep** — project knowledge only; e.g. a one-off component does not force `techContext.md` edits unless the task changed stack/conventions.
7. **L4 inherits** via sub-run workflows.

All requirements were met.

## IMPLEMENTATION

### Shared rule

- **New:** `rulesets/niko/niko/core/reconcile-persistent.mdc` — defines the three persistent files, points to their guidance rules, prescribes compare → skip or surgical update, and guardrails (selective, surgical, system scope, skip when in doubt). Preflight refinement: trigger updates when content is **factually wrong** or **materially incomplete**.

### Workflow injections

Each injection is a single “load canonical rule and follow” instruction (no duplicated procedure text):

- **`rulesets/niko/niko/level1/level1-workflow.mdc`** — Wrap-Up: reconcile before final commit.
- **`rulesets/niko/niko/level2/level2-reflect.mdc`** — After reflection document written, before memory-bank commit steps.
- **`rulesets/niko/niko/level3/level3-reflect.mdc`** — Same pattern as L2 (step numbering adjusted per level).

**L4:** Verified unchanged — capstone archive does not need reconciliation; sub-runs already reconcile.

### Documentation fix during QA

- **`memory-bank/systemPatterns.md`** — Added a bullet describing the persistent-file reconciliation pattern so the memory bank matches the new workflow behavior.

### Operational note (repository conventions)

Canonical Niko rules live under `rulesets/`; this repo uses automation (e.g. `ai-rizz`) to install copies under `.cursor/rules/`. Editors should change `rulesets/` (and equivalents), not hand-edit generated `.cursor/` copies for this content.

### Design decision (creative phase, inlined)

**Options considered:**

| Criterion | A: Reflect / Wrap-Up | B: Archive / Wrap-Up | C: New phase |
|-----------|----------------------|----------------------|--------------|
| Maintainability | Strong — 3 small injections + 1 rule | Same structure | Weaker — new workflow nodes |
| Simplicity | Strong | Archive semantics muddy (“preserve persistent” vs reconcile) | Over-built for a usually-no-op step |
| Context | Strong — same session as build + reflect | Weaker — archive may be a later session | Depends on placement |

**Decision:** **Option A** — inject into L1 **Wrap-Up** and L2/L3 **Reflect** (after reflection doc, before commits that finalize the phase). **Rationale:** The reconciling agent has full context; archive phases stay clearly “preserve persistent / archive-only” without mixing in edits; no new workflow graph nodes for a step that should usually no-op.

## TESTING

No automated test framework for this rules-only change. Validation was:

- **Preflight:** Conventions, dependencies, and completeness checks passed; “materially incomplete” trigger folded into the reconciliation procedure.
- **Manual / review:** New `.mdc` structure, injection points before commits, L4 untouched.
- **`/niko-qa`:** PASS; one finding — missing `systemPatterns.md` mention of reconciliation — fixed in place.

## LESSONS LEARNED

- Centralizing cross-cutting workflow behavior in one `.mdc` and injecting “load X and follow” at a few edges scales well for rule-based systems and avoids copy/paste drift.
- Reconciliation belongs in the last **autonomous** step where the agent still holds full task context (wrap-up / reflect), not in a separate archive session where context may be thinner.
- Treating “document the new pattern in `systemPatterns.md`” as part of the deliverable — not something to defer as “self-referential” — avoids pushing obvious doc gaps to QA and keeps the memory bank honest from the first merge.

## PROCESS IMPROVEMENTS

- In planning, avoid deferring updates to persistent docs when the task **introduces** a durable pattern those files are meant to capture; include explicit checklist items for `systemPatterns.md` (or equivalent) when the feature changes how the system works at a glance.

## TECHNICAL IMPROVEMENTS

- **None required** beyond the delivered reconciliation hook. For future cross-cutting Niko workflow behavior, prefer the same pattern: one canonical rule file + minimal load instructions at injection sites.

## NEXT STEPS

None. If maintaining forked installs of rules, run the usual `rulesets/` → `.cursor/rules/` sync (e.g. via `ai-rizz`) so deployed copies match canonical sources.
