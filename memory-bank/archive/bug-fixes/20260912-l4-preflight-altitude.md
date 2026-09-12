---
task_id: l4-preflight-altitude
complexity_level: 3
date: 2026-09-12
status: completed
---

# TASK ARCHIVE: l4-preflight-altitude

## SUMMARY

Closed [issue #122](https://github.com/Texarkanine/.cursor-rules/issues/122): `/niko-preflight` on Level 4 no longer treats `milestones.md` one-liners as L2/L3 implementation plans. The skill dispatches on `progress.md` `**Complexity:**`: Levels 2 and 3 load `references/default-preflight.md` (today's TDD and completeness bar); Level 4 loads `references/level4-preflight.md` (milestone-design altitude). Spawn line unchanged. Canonical edits under `rulesets/` only. Draft PR: [#125](https://github.com/Texarkanine/.cursor-rules/pull/125).

## REQUIREMENTS

From the project brief (operator-locked after Creative):

1. Fix #122: L4 preflight must not treat each checkbox as a full L2/L3 implementation plan.
2. Present mechanism options; operator chooses before implementation. Chosen: **D + W4**.
3. When Complexity is Level 4, judge L4 design (coverage, order, done, risks, invariants). Sub-run plans are written later, when `/niko` classifies the next unchecked milestone.
4. Reuse an existing ticket when one exists. Do not create tickets.
5. Do not allow implementation plans (sub-bullets, TDD steps, file lists) on L4 checklist lines.
6. Do not relax L2/L3 TDD encoding or completeness-of-steps.
7. Canonical edits under `rulesets/` only. Generated `.cursor/` is a later `chore(dev): ai-rizz sync`.
8. Preflight stays judge-and-report: four status strings, meanings only in `preflight-status.mdc`. Spawn line stays `Run the /niko-preflight skill`.

## IMPLEMENTATION

### Mechanism (Creative, inlined)

Operator-named options A–C, plus discovered D–F.

- **A. New skill** — isolate L4 in `/niko-preflight-l4`. Strong isolation; second glossary; spawn-line identity breaks at L4 sites. Not chosen.
- **B. Branch inside SKILL.md** — smallest diff; mixed-bar (TDD and "do not require TDD" in one file the agent reads whole). Not chosen as the whole solution.
- **C. Skip / self-gate / extra spawn prompt** — C2/C3 abandon the L4 judge; C4 violates the one-line spawn contract. Rejected.
- **D. Same skill, extracted L4 reference** — one slash name, one spawn line; SKILL.md dispatches; L4 checks live in a sibling file that does not mention TDD. **Chosen.**
- **E. Drop the word `milestone` only** — Completeness still FAILs one-liners. Inadequate alone (the word still left the TDD sentence).
- **F. Dual-write a fake L4 `tasks.md`** — two plans drift. Rejected.

Fact placement (orthogonal to the skill vote):

- **W1** sections below the checklist; **W2** brief only; **W3** ticket in the one-liner only; **W4** ticket on the checkbox when one exists, done/risks/invariants as sections. **W4 chosen.**

Operator constraints on D: Preflight remains a spawned skill (not a plan/build workflow router). L2 and L3 share one file. L4 gets its own sibling. Dispatch on Complexity Level 4 only — never `milestones.md` presence (every sub-run still has that file).

Load-bearing research that survived build:

- `/niko` Step 2a deletes `tasks.md` and `progress.md`. Done, risks, and ticket refs that live only there are gone before later milestones run. They belong in `milestones.md` / `projectbrief.md`.
- Handoff is a *rule* (who may touch a shared artifact, and when), not a file inventory.
- Serial-safe checklist plus a DAG when the work is not a line. The list is a valid serial walk of the DAG.
- Do not judge numbered test-first substeps, file paths, or L-estimates on checkbox lines.

### Arc

1. **Extract L2/L3 checks** into `default-preflight.md`. Word `milestone` removed from TDD units. Later: wrong-reference guard if Complexity is Level 4. Rebase onto [#124](https://github.com/Texarkanine/.cursor-rules/pull/124) landed product-user TDD wording here (`What TDD Governs`, strike non-product contract tests).
2. **Write L4 checks** in `level4-preflight.md` (renamed from the planned `l4-preflight.md`). Judges decomposition, not implementation steps. Seven checks. Check 9 (convention/conflict at L4 / generated-tree edits) was struck as this-repo leak. Required `Ref:` / `projectbrief.md` pointer was dropped: L4 briefs are whole-program north stars, not per-milestone cite targets; tickets go on the checkbox when they exist.
3. **Dispatcher SKILL.md** — Load, Determine Complexity (FAIL blocking unless 2/3/4; skip to Write Status), Route to exactly one check file, Radical Innovation, Judge, Write Status, Log, End of Verification stop. Does not load a level workflow. CodeRabbit: an `Otherwise` fallthrough to the L2/L3 bar was the #122 hole for missing Complexity on an in-flight L4; exclusive FAIL replaced it.
4. **W4 format** — `milestones.mdc` heading blocks (not tables): Cross-milestone invariants, Execution Order (checkbox list + optional DAG), Per-milestone done and risks. `level4-plan.md` writes that format; L-estimates stay in the plan result / `progress.md`.
5. **Classify + docs** — complexity analysis classifies the first unchecked checkbox plus that milestone's done/risks heading block. README: "L4 Preflight validates the milestone list. Sub-run Preflight uses the L2/L3 bar."
6. **QA rework** — check 6 handoff-rule FAIL only when two milestones share an artifact. Check 2 does not FAIL the real Execution Order checklist as "extra checkboxes." Judge: TDD swap/strike only when the loaded checks performed those edits.
7. **Reflect** — surgical `systemPatterns.md`: Niko workflow `references/` live beside `SKILL.md` in the ruleset; topic skills still symlink from `rules/`.
8. **Post-reflect skill prose** — SKILL.md numbered like plan/build/archive. Step 4 (Radical Innovation) is a question plus one advisory write, not a bullet list. Step 5 (Judge) leads with the verdict; allowed writes are the one real set. Radical Innovation stays after Route, not inside it.

### Key files

- `rulesets/niko/skills/niko-preflight/SKILL.md` — dispatcher + shared close
- `rulesets/niko/skills/niko-preflight/references/default-preflight.md` — L2/L3 checks
- `rulesets/niko/skills/niko-preflight/references/level4-preflight.md` — L4 milestone-design checks
- `rulesets/niko/niko/memory-bank/active/milestones.mdc` — W4 format
- `rulesets/niko/skills/niko/references/level4/level4-plan.md` — writes W4; spawn line unchanged
- `rulesets/niko/skills/niko/references/core/complexity-analysis.md` — classify target includes the heading block
- `rulesets/niko/README.md` — L4 key-differences bullet
- `memory-bank/systemPatterns.md` — File Organization sentence for Niko workflow `references/`

Runtime load paths remain `.cursor/skills/shared/niko-preflight/references/…`. Those files do not exist until sync.

### L4 preflight checks (as shipped)

1. Prerequisites (Complexity 4, file exists, header match)
2. Checklist shape (one GFM checkbox; extra checkboxes in other sections FAIL blocking; do not FAIL the real list for living under Execution Order)
3. Coverage / no overlap
4. Scope and concreteness (independent, L1–L3, concrete)
5. Order: serial-safe walk; DAG required when not a line and must agree with the checklist
6. Cross-milestone invariants (section required; handoff *rule* only when two milestones share an artifact)
7. Done and risks (heading block; no required `Ref:` field; do not FAIL for a missing ticket; packet must be enough to classify)

### Reflection (inlined)

Delivered as asked. The five-unit file list was right. The surprise was check 6's last sentence collapsing "missing invariants section" and "missing handoff rule" into one unconditioned FAIL — the plan already had the "when"; implementation dropped it. Check 2 had the same shape: "sections must not contain checkboxes" while the canonical format puts the real checklist under Execution Order.

D + W4 held. The important creative correction was the operator's: Preflight/QA are spawned skills with a one-line bootstrap, so they must not become plan/build workflow routers even though they *split* like level-specific plan files.

Build was prose/policy; `make test` green on the first pass. First QA (Grok 4.6 xhigh) caught the unconditioned handoff FAIL. Rework was one qualified sentence plus two cheap clarifications. Second QA (GPT 5.6) passed.

This L3 Preflight could not have caught the L4 check-6 bug: it judged `tasks.md`, not a sample L4 `milestones.md`.

## TESTING

No new automated tests (prose/policy; wording assertions would be change-detectors). `make test` (ruleset symlink + README link checks) passed after Build.

This task's own `/niko-preflight`: `PASS WITH ADVISORY` (L3 plan, lagging `.cursor/` copy of the pre-split skill — correct bar). Advisories taken: wrong-reference guard on `default-preflight.md`; `systemPatterns.md` sentence at Reflect.

`/niko-qa`: FAIL (unconditioned handoff rule), then PASS after rework.

Live proof is the next real L4 Preflight after `chore(dev): ai-rizz sync`. Until then, live L4 dispatch 404s on the new reference files.

## LESSONS LEARNED

- L4 dispatch must key off `progress.md` Complexity, not `milestones.md` presence: every sub-run still has that file and still needs the L2/L3 bar. An `Otherwise` fallthrough to default is the same hole when Complexity is missing on an in-flight L4.
- Facts a later milestone worker needs must live in `milestones.md` or `projectbrief.md`. Step 2a deletes `tasks.md` and `progress.md`.
- A spawned skill's bootstrap must stay one line. Level-specific *files* inside that skill are the split; loading the level workflow from the subagent is a different pattern.
- When a plan uses "when X, FAIL for Y; also FAIL for Z," write two sentences in the check file. One close sentence will drop the "when."
- Workflow list signals: a heading that names the work, then a verb, then either sentences (one action) or a bullet set (order does not matter). Do not bullet a question as if it were a task. Radical Innovation is after Route, not inside it.
- Do not require a `projectbrief.md` pointer as a per-milestone `Ref`. L4 briefs are whole-program north stars. Tickets on the checkbox when they exist; do not FAIL for a missing ticket.

## PROCESS IMPROVEMENTS

Mixing Preflight/QA model families paid rent: the first QA found the real FAIL; the second confirmed the rework.

Lock the spawn-skill vs workflow-router distinction in creative, not in build: converting Preflight to "load the level workflow" would fatten the subagent bootstrap.

## TECHNICAL IMPROVEMENTS

Niko workflow skills keep `references/` next to `SKILL.md` under `rulesets/niko/skills/<name>/`. Topic skills still live under `rules/` and symlink in. Putting Preflight's L4 checks under `rules/` as a symlink would have been the wrong home. That sentence is now in `systemPatterns.md`.

## NEXT STEPS

- Merge [PR #125](https://github.com/Texarkanine/.cursor-rules/pull/125), then `chore(dev): ai-rizz sync` so `.cursor/skills/shared/niko-preflight/references/` exists at the paths SKILL.md loads.
- Watch the next real L4 `/niko-preflight`. That is live proof, not this task's suite.
- Leftover (not blocking this archive): `level4-plan.md` Step 5/6 still says "validate the milestone list" without restating L4 altitude. The README bullet carries that distinction. Operator did not require a further plan-file edit.
