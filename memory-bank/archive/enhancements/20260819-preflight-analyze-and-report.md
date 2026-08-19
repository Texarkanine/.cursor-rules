---
task_id: preflight-analyze-and-report
complexity_level: 3
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: preflight-analyze-and-report

## SUMMARY

Finished the Preflight contract for https://github.com/Texarkanine/.cursor-rules/issues/114: four result strings (`PASS`, `PASS WITH ADVISORY`, `FAIL (fixable)`, `FAIL (blocking)`), in-phase TDD step-swap and change-detector strike, and isolation so Preflight reports and stops. Parent routing lives on the charts, Build gates, and `preflight-status.mdc`. Meanings of the four strings live only in that `.mdc`. Findings for a run live in `.preflight-status` (first line is the semaphore; the rest is this run’s findings).

Four passes on the same task: judge-only, TDD swap-only, the rest of #114 (L3), then a Level 1 rework that deleted Handle Results (step 10). Draft PR: https://github.com/Texarkanine/.cursor-rules/pull/115 (`tamp-down-preflight`). Operator README/L3 chart aesthetics (`504d4f3`) were left intact. `niko-qa` was not edited.

The final rework classified as Level 1 (no archive on that workflow). The operator invoked `/niko-archive` anyway so this document could hold the L3 story plus the Handle Results cut. Complexity in this frontmatter is 3.

## REQUIREMENTS

From the project brief (final form, including the Handle Results rework):

1. Judge and report. In-phase plan writes are only the TDD step-swap and striking scheduled change-detector steps.
2. Four outs, exact strings: `PASS`, `PASS WITH ADVISORY`, `FAIL (fixable)`, `FAIL (blocking)`. No bare `FAIL`.
3. `PASS` and `PASS WITH ADVISORY` unblock build (L2 solid → build; L3 still dashed `/niko-build`).
4. `FAIL (fixable)`: plan has issues with known fixes; planner re-plans; parent → Plan; no operator; may loop.
5. `FAIL (blocking)`: plan has issues that require materially changing the plan; operator provides guidance, then `/niko-plan`.
6. Meanings live in `preflight-status.mdc`. Do not grow a second glossary in the skill.
7. Status is determined upstream during checks. Write Status serializes the first line. Do not keep “PASS WITH ADVISORY unless another check fails” in the skill.
8. No Handle Results step. The skill does not tell the Preflight agent to invoke Plan or `/niko-plan`.
9. FAIL print has no Next Steps subsection.
10. `.preflight-status`: first line is the enum; the rest is this run’s findings. `tasks.md` changes only via swap/strike.
11. `FAIL (fixable)` name reuse with QA is intentional. Nine-site Spawn stem unchanged. `niko-qa` unchanged. Canonical edits under `rulesets/` only. No nested Preflight/QA subgraphs. No emitting missing always-tdd stages.

Supersedes the earlier “change-detectors stay FAIL and do not patch.”

## IMPLEMENTATION

### Arc

1. **Judge-only** — Preflight reports; no general plan amendment.
2. **TDD swap-only** — reversed test/code steps are reordered in-phase (`Same steps`).
3. **#114 L3** — four-way status vocabulary; change-detector strike (`Keep the other steps`); L2/L3/L4 and README chart splices; combined `PASS / PASS WITH ADVISORY` edge (operator: two pass lines clutter); findings in `.preflight-status`; Build reads the first line exactly; L2/L3 Build remediations: missing file still spawns Preflight, `FAIL (fixable)` → Plan, `FAIL (blocking)` → operator.
4. **L1 rework** — deleted Handle Results. TDD missing-tests writes `FAIL (blocking)` on that bullet. FAIL print dropped the Next Steps menu.

No creative phase. The issue specified the outs, the chart, the name-reuse, and the in-phase vs FAIL line.

### Key files

- `rulesets/niko/niko/memory-bank/active/preflight-status.mdc` — four-string glossary; glob on `.preflight-status`
- `rulesets/niko/skills/niko-preflight/SKILL.md` — strike + swap; Write Status; no Handle Results; Step 4 copies first line into `**Phase:**` and stops
- `rulesets/niko/skills/niko/references/level{2,3,4}/level{2,3,4}-workflow.md` — four-way fork; combined PASS edge; STOP lists (L2/L3)
- `rulesets/niko/README.md` — matching Preflight charts (L1 unchanged)
- `rulesets/niko/skills/niko/references/level{2,3}/level{2,3}-build.md` — first-line gate; fail remediations
- `rulesets/niko/niko/core/memory-bank-paths.mdc` — status file: first line gates Build; rest is findings; deleted at archive

### Creative phase decisions

None. No `memory-bank/active/creative/` files. The outs and routing were specified in the issue and brief.

### Reflection (inlined)

Preflight is a four-way semaphore with two in-phase plan writes. Three L3-era passes, then the Handle Results cut. QA PASS on the #114 pass (two advisories, neither blocking) and PASS with no advisories on the L1 cut.

Plan accuracy: the four-unit split (status, skill, workflows, README) was the right file list. Challenges named STOP lists still saying “Preflight FAIL,” GitHub layout if Preflight were nested, and “re-run `/niko-preflight`” as a fixable next step. Two parallel PASS edges were later folded into one label at operator request.

Surprise: `level{2,3}-build.md` still told a parent that hit a failing status to re-spawn Preflight. The plan checked the Build *gate* and cleared it; the remediation sentence was a different site. That wording was fixed in PR follow-up (missing → Preflight; fixable → Plan; blocking → operator).

No creative phase. Build was prose/policy; `make test` green. Charts rendered under `mmdc`.

Plan 2 on an earlier rework failed because it tried to emit always-tdd stage labels. This plan said do not invent tests and do not emit always-tdd stages.

Retracting the brief before planning (strike is in-phase) meant Preflight measured the intended contract.

## TESTING

- `make test` (symlink + README link checks) after the #114 build and after the Handle Results cut
- Nine Mermaid charts in the four changed files compiled with `mmdc` on the L3 pass
- `/niko-qa` PASS (Claude Opus) on the L3 pass — two non-blocking advisories: strike bullet dropped the old purpose-built-CI-gate parenthetical; Build still re-spawned Preflight (later fixed)
- `/niko-qa` PASS (GPT 5.6) on the L1 Handle Results cut — no findings or advisories

No new automated tests: skill, chart, and vocabulary wording is prose/policy. Change-detector tests on those artifacts were out of scope.

## LESSONS LEARNED

- Edge *style* is the chart contract. A new result label must inherit the style of the edge it rides, or the STOP list and the diagram disagree.
- Splitting a result enum exposes every branch on the coarse value. The gate check and the remediation text attached to a failed gate are different sites.
- Two copies of the four-string glossary drift. Define them once in `preflight-status.mdc`; the skill is the recipe.
- Status is judged during checks. Write Status copies it. “PASS WITH ADVISORY unless another check fails” re-judges at the end and is redundant with FAIL-wins.
- Handle Results was leftover dispatch. After Step 4 already stops, report is the action. Parent → Plan lives on the chart.
- `FAIL (fixable)` name reuse with QA works when the chart pairs the label with the destination. Do not rename to dodge the collision.
- Rework that changes an AC must retract the old AC in the brief before the next Preflight.

## PROCESS IMPROVEMENTS

- When splitting an enum, list every *reader* of the old value, not only the write site and the gate check — include remediation sentences on the failed gate.
- Isolation: if nothing else should dump Preflight findings into `tasks.md`, do not add defensive “do not write findings there” lines; remove the invites instead.
- Operator chart aesthetics are a follow-up commit, not something later review should revert.

## TECHNICAL IMPROVEMENTS

None beyond what shipped. `niko-qa` still has a Handle Results step; that was an explicit constraint, not a missed edit. The generated `.cursor/` tree lags `rulesets/` until an `ai-rizz` sync.

## NEXT STEPS

None required for this task. PR #115 is the remaining merge vehicle.
