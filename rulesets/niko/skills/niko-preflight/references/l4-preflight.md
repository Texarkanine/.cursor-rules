# L4 Preflight Checks

L4 milestone-design checks. Load this file only when `memory-bank/active/progress.md` `**Complexity:**` is Level 4. Follow every numbered step below, then return to the skill for Radical Innovation, Judge, Write Status, and stop.

The design surface is `memory-bank/active/milestones.md` plus `memory-bank/active/projectbrief.md`. Do not treat the L4 `tasks.md` stub as the plan. Do not read `references/default-preflight.md`. Do not require numbered test-first substeps, concrete file paths, validation sequences, or L-estimates on checkbox lines.

## Additional loads

Read:

- `memory-bank/active/milestones.md` (required)
- `memory-bank/active/projectbrief.md` (L4 design surface; already in the skill's shared load)

## Checks

1. **Prerequisites**
   - `memory-bank/active/progress.md` `**Complexity:**` must be Level 4. If it is not, this is the wrong reference. Write `FAIL (blocking)`. Do not run the remaining checks.
   - `memory-bank/active/milestones.md` must exist. If it does not, write `FAIL (blocking)`.
   - Header must be `# Milestones: <task-id>` matching the active task ID in `memory-bank/active/tasks.md`. Header mismatch: write `FAIL (fixable)`.
2. **Checklist shape**
   - Each milestone is one GFM checkbox line (`- [ ]` or `- [x]`). No sub-bullets on those lines.
   - Sections (invariants, DAG, done/risks table or headings) must not contain `- [ ]` or `- [x]`. Extra checkboxes poison `/niko` classify. Any extra checkbox: write `FAIL (blocking)`.
3. **Coverage**
   - Every requirement in `projectbrief.md` maps to at least one milestone.
   - No two milestones cover the same purpose. Gap or overlap: write `FAIL (blocking)`.
4. **Scope and concreteness**
   - Each milestone is independently deliverable, L1–L3 scoped (not itself L4), and names a concrete deliverable.
   - Nested L4, future-dependent work, or a vague activity line: write `FAIL (blocking)`.
5. **Order**
   - The checklist order must be safe for serial execution (`/niko` always takes the first unchecked box). Milestone N must not require work from milestone N+1. Unsafe order or future-dependency: write `FAIL (blocking)`.
   - A dependency DAG belongs in the Execution Order section only when the work is not a straight line, and it must match the checklist. Parallel claimed in prose but no DAG: write `FAIL (fixable)`.
6. **Cross-milestone invariants**
   - A Cross-milestone invariants section must exist. It states properties no milestone may violate — not goals or requirements.
   - When two milestones share an artifact, the section states a handoff *rule* (who may touch it, and when). Not a file inventory. Missing section or missing handoff rule: write `FAIL (fixable)`.
7. **Done, risks, and refs**
   - Each checkbox has a joinable row or heading block (not a checkbox sub-bullet) with:
     - **Done** — a judgeable definition of done
     - **Risks / invariants** — critical risks for that milestone, or an explicit pointer that a cross-milestone invariant covers it
     - **Ref** — an existing ticket if the brief or issue already has one; otherwise a pointer into `projectbrief.md`. Do not create tickets. Do not FAIL for a missing ticket when none exists.
   - Missing Done, Risks/invariants, or Ref: write `FAIL (fixable)`.
8. **Persistent-file sufficiency**
   - The checkbox plus its done/risks/ref row plus `projectbrief.md` (plus the ticket if linked) must be enough for a later agent to classify and plan the milestone after `/niko` Step 2a deletes `tasks.md` and `progress.md`.
   - Too vague to classify: write `FAIL (blocking)`. Missing pointer only: write `FAIL (fixable)`.
9. **Convention and conflict at L4 altitude**
   - Flag a decomposition that would edit generated `.cursor/` / `.claude/` trees, or that would break a published contract implied by the brief or invariants.
   - Do not require a per-milestone file list. Do not require numbered test-first substeps or concrete file paths on one-liners.
