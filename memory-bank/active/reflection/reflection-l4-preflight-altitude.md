---
task_id: l4-preflight-altitude
date: 2026-09-12
complexity_level: 3
---

# Reflection: l4-preflight-altitude

## Summary

`/niko-preflight` now dispatches on `progress.md` Complexity: L2/L3 load `references/default-preflight.md` (today's TDD/completeness bar, word `milestone` removed); L4 loads `references/l4-preflight.md` (W4 milestone design). Spawn line unchanged. QA passed after one close-sentence rework.

## Requirements vs Outcome

Delivered as asked. Issue #122's wrong bar is gone: L4 one-liners are not judged as implementation plans. L2/L3 TDD encoding is not relaxed. Tickets are referenced when they exist and never created. `milestones.mdc` still forbids checklist sub-bullets and file lists. Canonical edits stayed under `rulesets/`; `.cursor/` was not synced in this task.

Added at Build: the Preflight advisory wrong-reference guard on `default-preflight.md`. Added at QA rework: check 6's handoff FAIL is conditioned on a shared artifact; check 2 does not FAIL the real Execution Order checklist.

## Plan Accuracy

The five-unit file list was right. The surprise was not a missing file — it was check 6's last sentence collapsing "missing invariants section" and "missing handoff rule" into one unconditioned FAIL. The plan already said the handoff rule applies when two milestones share an artifact; implementation dropped the "when."

Check 2 had the same shape of underspecification: "sections must not contain checkboxes" while the canonical format puts the real checklist under `## Execution Order`. That was an advisory that would have become a live L4 false FAIL.

Challenges that materialized: generated-tree lag (planned, not a fail); mixed-bar risk (addressed by exclusive load + both files' wrong-reference guards). Challenges that did not: dual-skill drift (we did not pick A); spawn-line edits (we did not pick A or C).

## Creative Phase Review

D + W4 held. The important creative correction was the operator's: Preflight/QA are spawned skills with a one-line bootstrap, so they must not become plan/build workflow routers even though they *split* like level-specific plan files. That distinction is the whole design.

Dispatch on Complexity rather than `milestones.md` presence was the load-bearing finding and it survived build. L2 vs L3 did not need a second creative; sharing `default-preflight.md` was correct.

## Build & QA Observations

Build was prose/policy and `make test` was green on the first pass. QA (Grok 4.6 xhigh) caught the unconditioned handoff FAIL. Rework was one qualified sentence plus two cheap clarifications. Second QA (GPT 5.6) passed with no findings.

The gap between plan and first implementation was a compound-sentence bug, not a wrong design.

## Cross-Phase Analysis

Creative named "handoff as a rule when two milestones share an artifact." Plan unit 2.2.6 kept the "when." Build's check 6 close sentence forgot the "when." QA read the plan against the file and caught it. Preflight of *this* L3 plan could not have caught it: it judged `tasks.md`, not a sample L4 `milestones.md`.

The Preflight advisory (wrong-reference guard on default) was taken at Build. That is the useful direction: a one-line defense that makes a dispatcher mix-up fail loud.

## Insights

### Technical
- L4 dispatch must key off `progress.md` Complexity, not `milestones.md` presence: every sub-run still has that file and still needs the L2/L3 bar.
- Facts a later milestone worker needs must live in `milestones.md` or `projectbrief.md`. `/niko` Step 2a deletes `tasks.md` and `progress.md`.
- Niko workflow skills keep `references/` beside `SKILL.md` in the ruleset. Topic skills still live under `rules/` and symlink in. Putting Preflight's L4 checks under `rules/` as a symlink would have been the wrong home.

### Process
- A spawned skill's bootstrap must stay one line. Level-specific *files* inside that skill are the split; loading the level workflow from the subagent is a different pattern and would fatten the spawn prompt.
- When a plan uses "when X, FAIL for Y; also FAIL for Z," write two sentences in the check file. One close sentence will drop the "when."
- Mixing Preflight/QA model families paid rent: the first QA found the real FAIL; the second confirmed the rework.
