# Task: verification-subagents-preflight-qa (rework pass 2)

* Task ID: verification-subagents-preflight-qa
* Complexity: Level 2
* Type: remediation (TDD routing + Plan tightening)

**Authority:** This file is the gospel for what to build next. Creative docs are exploration only. Live charts = `rulesets/niko/`.

## Decisions (operator 2026-08-07)

- TDD plan-encoding failure **is** `FAIL (rearchitect)` → Plan (operator path). No special `FAIL (TDD)` species.
- Durable fix is **Plan authorship**, not a special preflight auto-heal edge.
- Stockroom history of past TDD-preflight catches informs Plan tightening; repeated fails after that → postmortem.

## Test Plan (TDD)

Prose/policy — always-tdd carve-out. No change-detector tests.

### Behaviors to Verify

- [Dry-read]: no `FAIL (TDD)` in `rulesets/niko/` charts, skills, or `preflight-status.mdc`
- [Dry-read]: TDD plan-encoding Handle Results routes as rearchitect (kick back to Plan / operator)
- [Dry-read]: L2/L3 STOP lists no longer carve out TDD
- [Dry-read]: level plan docs (or shared plan guidance) require per-unit test-before-code ordering explicit enough that preflight’s TDD check is redundant for well-formed plans
- [make test] + [mmdc] on touched charts

## Implementation Plan

1. **Stockroom archaeology (before chart edits)**
   - `/sr-search` (semantic + query as needed): sessions where preflight found TDD plan-encoding problems and how the fix was executed (what it read, what it changed in `tasks.md`)
   - Distill: checklist of Plan requirements that would have prevented those fails
   - Files: notes in this `tasks.md` or a short `memory-bank/active/creative/` exploration doc if helpful — **not** gospel until folded into step 3
   - **Advisory input, not a gate:** step 3's design (below) stands on its own. If stockroom is unavailable or the seed hits yield nothing actionable, record that in one line and proceed to steps 2–4 rather than stalling.
   - **Seed hits** (stockroom semantic 2026-08-07; fetch full text next session):
     - `471d0da3-6139-440c-88af-0531efeb2796#19` / `#` session same — preview about TDD encoding amend
     - `5c63e90b-6214-42ca-af9a-93c12d65f27a#23`
     - `dd70d758-8bb8-4047-b16c-b942bcad584d#33`
     - High-signal preview class: “TDD plan encoding (blocking, fixed) — Implementation steps lacked per-unit …”
   - **Distill (2026-08-07 build):** Confirmed across three seed sessions + semantic neighbors. Preflight always failed the same shape: preamble/disclaimer said “TDD cycle” while numbered steps were `Files:`/`Changes:` only (or put helpers/constants before tests, or parked verification last). The in-phase fix was always the same: rewrite each unit with explicit test-before-code substeps (failing baseline first, then implement). That is exactly what step 3’s template `- Tests first:` encodes — no additional Plan liturgy needed beyond the template + escape hatch.

2. **Remove `FAIL (TDD)` species (with operator on any mermaid >1 line)**
   - **Mermaid edges — five single-line deletions** (each chart keeps its sibling dashed `FAIL` edge, so the rearchitect path survives; all five are 1-line deletes, so no operator gate is triggered):
     - `rulesets/niko/skills/niko/references/level2/level2-workflow.md:18`
     - `rulesets/niko/skills/niko/references/level3/level3-workflow.md:18`
     - `rulesets/niko/README.md:109` (long chart), `:197` (per-level L2), `:241` (per-level L3)
   - `rulesets/niko/skills/niko-preflight/SKILL.md`: drop `FAIL (TDD)` from the status-value list (`:61`), fold Handle Results `On FAIL (TDD plan encoding)` into the rearchitect bullet (`:69`), delete the `On FAIL (TDD)` Next Steps line (`:107`)
   - `rulesets/niko/niko/memory-bank/active/preflight-status.mdc:16`: remove the `FAIL (TDD)` value
   - L2/L3 STOP lists / auto-continue prose: `level2-workflow.md:43` (drop the `FAIL (TDD)`→plan clause) and `:48`, `level3-workflow.md:51` (drop the parenthetical carve-out)
   - **Build guards — verify only, no edit expected:** `level2-build.md:16` and `level3-build.md:18` already gate on `PASS` / `PASS WITH ADVISORY` alone; there is no `FAIL (TDD)` branch to remove (CodeRabbit item 8 is already satisfied). Confirm, don't invent a change.
   - **Generated trees:** `.cursor/` and `.claude/` never received the pass-1 `FAIL (TDD)` vocabulary, so this removal converges the trees. Do not edit them.

3. **Tighten Plan phase TDD authorship — put the requirement in the emitted artifact, not another instruction**
   - Root cause: `level2-plan.md` Step 5 and `level3-plan.md` Step 7 already *say* "each step maps to one TDD cycle", but the `tasks.md` output template they hand the planner has only `- Files:` / `- Changes:` substeps. The template is where implementation-only plans come from, so that is what changes.
   - `rulesets/niko/skills/niko/references/level2/level2-plan.md` (`## Implementation Plan` template, ~`:97`) and `level3-plan.md` (~`:169`): add a per-step `- Tests first:` substep naming the test file and the case(s) to write and watch fail, ordered **before** `- Changes:`.
   - The `- Tests first:` substep must carry an explicit carve-out escape hatch (e.g. `N/A — prose/policy artifact per always-tdd`) so the template cannot push change-detector tests onto documentation units. Without it this fix creates the exact failure mode this task's own plan avoids.
   - Do **not** add a parallel prose instruction alongside the existing "maps to one TDD cycle" line — that is the duplication the plan warns about. Tighten the wording of the existing line only if the template change leaves it ambiguous.
   - `rulesets/niko/always-tdd.mdc` is a **symlink** to `rules/always-tdd.mdc` (shared rule; currently `rulesets/niko/` is its only consumer). Prefer the Niko plan docs; only touch the shared rule if the carve-out wording itself is wrong.

4. **Cheap non-TDD fixups** (one-liners OK without operator; mermaid with operator)
   - `level2-workflow.md:27` `/archive` → `/niko-archive`; then update the now-satisfied bullet under `### Deferred (not fixed this task)` in `memory-bank/active/reflection/reflection-verification-subagents-preflight-qa.md:44` (and the matching `progress.md:197` line)
   - Progress summary: drop “mermaid unchanged” (`memory-bank/active/progress.md:3`)
   - Double-backtick Spawn charge spans in progress (`progress.md:210`, `:230` — nested single backticks render broken); brief already rewritten
   - **Operator-gated — done:** clear `.qa-validation-status` before QA spawn (L1/L2/L3 QA Phase Mapping lines). README long-chart Fail fork: **Option A** — expand Build-edge label to `L1 Fail / L2+ fixable`, rename Plan edge to `L2+ rearchitect` (no new edge geometry).

5. **Verify** — `make test`, `mmdc` on the touched charts, `rg 'FAIL \(TDD\)'` clean under `rulesets/niko/`
   - The `rg` sweep is an **ad-hoc verification command**, not a test to commit. Do not add a script or CI check asserting the absence of a phrase — that would be the change-detector the always-tdd carve-out forbids.
   - `rg` will still hit `memory-bank/` (brief, progress, reflections, this file): that is the intended historical record. Scope the sweep to `rulesets/niko/`.

## Preflight Findings (2026-08-07)

✅ **PASS WITH ADVISORY.** Plan amended in place (steps 1–5 above); no rearchitect needed.

- **TDD encoding — pass.** Every unit delivers rule/skill/README wording and mermaid, which `always-tdd` carves out explicitly. The plan names the carve-out, schedules no change-detector tests, and step 5's `rg` sweep is now marked ad-hoc.
- **Convention — pass.** All edits land in `rulesets/`; `.cursor/` and `.claude/` untouched, and neither ever received the pass-1 vocabulary.
- **Dependency impact — amended.** All 12 `FAIL (TDD)` lines in `rulesets/` (5 mermaid edges, 3 in the preflight skill, 3 in L2/L3 prose, 1 status value) are now enumerated by file and line. Verified each of the five chart edges has a sibling dashed `FAIL` edge, so no deletion orphans the rearchitect route.
- **Conflict — amended.** Step 3's real target is the `tasks.md` output template, not a new instruction; the existing "maps to one TDD cycle" line already occupies that slot. `always-tdd.mdc` flagged as a symlinked shared rule.
- **Completeness — amended.** Two underspecified step-4 targets resolved to exact paths; the "optional" items reclassified as operator-gated; step 1 marked advisory so unavailable stockroom cannot block step 3.
- **Advisory (no action needed):** brief item 4 (postmortem if TDD keeps failing) is a conditional future policy with no build action this pass. Belongs in reflection, not the plan.

## QA Findings (2026-08-07, rework pass 2)

✅ **PASS.** Two non-blocking advisories; no Build or Plan rerun required.

### Verified

- **Step 2 — complete.** All 12 `FAIL (TDD)` sites gone; `rg` clean under `rulesets/niko/` and repo-wide outside `memory-bank/`. Each of the five deleted mermaid edges retains its sibling dashed `FAIL` edge, so the rearchitect route survives on L2, L3, and all three README charts. Build guards confirmed verify-only: L2 and L3 gate on `PASS` / `PASS WITH ADVISORY` alone.
- **Step 3 — complete.** `- Tests first:` sits between `- Files:` and `- Changes:` in both plan templates, carries the always-tdd `N/A` hatch, matches each file's indentation, and adds no parallel prose instruction — the existing "maps to one TDD cycle" lines are untouched. L4 needs no equivalent: its plan doc has no per-step implementation template. This satisfies preflight's "TDD ordering lives only in the preamble" FAIL condition per-unit.
- **Step 4 — complete.** `/niko-archive`, progress summary, satisfied `/archive` deferral bullet, double-backtick Spawn spans, README Option A, and `.qa-validation-status` clear at all three QA phase-mapping sites. L4 correctly has none — it has no QA phase.
- **Convention.** Only `rulesets/` and `memory-bank/` touched; `.cursor/` and `.claude/` untouched.
- **Nine-site Spawn tripwire intact.** The shared span still appears exactly nine times; the QA-status clear is prefixed *before* it rather than rewriting it, so `systemPatterns.md` stays accurate and needs no update.
- **Mechanical.** `make test` green; all 10 mermaid blocks compile (`mmdc` 11.14.0); README long-chart render inspected — `L1 Fail / L2+ fixable` solid to Build, dashed `L2+ rearchitect` to Plan, no orphan edges.

### Advisories (non-blocking, for Reflect)

- **Unplanned legend edit.** `level1-workflow.md` lost the legend line `🧑‍💻 = Phase initiated by operator with explicit command`. The plan does not authorize it and `activeContext.md` records "Deviations: None material". Non-behavioral, and arguably correct since the L1 chart has no `🧑‍💻` node — but it half-applies a design call pass 1 explicitly deferred: the legend still documents dashed edges, which the L1 chart also lacks. Reflect should either finish the tailoring (drop the dashed-edge line too) or restore the line, then reconcile the `### Deferred` bullet in `reflection-verification-subagents-preflight-qa.md` accordingly.
- **Dangling scratch pointers.** `creative/creative-readme-qa-fail-edges.md` has a "Rendered SVGs" section naming three SVGs that were never committed and do not exist. Cosmetic now, but `systemPatterns.md` requires archives be self-contained, so drop the section before archive.

## Out of scope this pass

- Restoring solid auto Plan re-entry for TDD
- CodeRabbit L4 “add FAIL (TDD) edge”
- Retry counters on rearchitect loops

## Status

- [x] Pass-1 rework shipped (most of nine review items)
- [x] Pass-2 decisions recorded (brief + this plan)
- [x] Preflight (PASS WITH ADVISORY — plan amended)
- [x] Stockroom archaeology
- [x] Remove `FAIL (TDD)` species
- [x] Tighten Plan TDD authorship
- [x] Cheap fixups (incl. QA-status clear + README Option A)
- [x] Verify (`make test` green; mmdc OK; `rg 'FAIL \(TDD\)'` clean under `rulesets/niko/`; build guards verify-only confirmed)
- [x] Build phase complete
- [x] QA (PASS — two advisories for Reflect; no Build/Plan rerun)
