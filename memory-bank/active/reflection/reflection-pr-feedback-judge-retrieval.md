---
task_id: pr-feedback-judge-retrieval
date: 2026-07-30
complexity_level: 2
---

# Reflection: PR Feedback Judge — Correct and Efficient Retrieval

## Summary

Reworked `rules/pr-feedback-judge/SKILL.md` so verdicts rest on current code: explicit anchor state (computed in `--jq`), a need-gated code-access ladder, and an evidence-gated `already addressed` disposition. Build and QA both passed; live acceptance confirmed the outdated-anchor path on PR #91.

## Requirements vs Outcome

All eight brief requirements and six acceptance criteria landed in the skill body. Nothing was descoped. The only verification softening was treating whole-script `verify-skillify.py` red as pre-existing noise and asserting this skill's structure directly — the plan's intent was preserved.

## Plan Accuracy

The eleven-step sequence and single-file scope held. Preflight's Radical Innovation (compute `anchor` in the projection) was the right call and became the main adherence mitigation. Challenges that materialized were naming (`Tier` collision) and length; both were handled as planned. The surprise was how vividly the live acceptance illustrated the defect: current L47 of the edited skill is unrelated Anchor State prose, exactly what a naive `original_line` read would have quoted.

## Build & QA Observations

Build was clean — one coordinated rewrite, no iteration loops. QA found no substantive gaps; the repeated `--jq` expression was judged deliberate recipe surface rather than accidental DRY debt.

## Insights

### Technical
- Prefer moving a classification policy into an existing transform (`--jq`) over restating it as a per-item instruction; it converts an adherence risk into a mechanical one.
- Generated-tree lag is not merely cosmetic: stale alwaysApply copies of `always-tdd` and `niko-preflight` would have produced the wrong TDD and preflight calls in this same task. Recorded surgically in `systemPatterns.md`.

### Process
- When the repository's purpose-built verifier is red at baseline for unrelated reasons, say so in the plan's verify step and name the targeted substitute assertion — do not discover it only at build step 11.

### Million-Dollar Question

If anchor staleness and code access had been foundational when the skill was first written, the fetch recipes would have shipped with field projection and a computed `anchor` from day one, and the "working tree is the PR head" assumption would never have been implicit. What we built is that foundational shape applied after the fact; a cleaner origin would mainly have been shorter history, not a different design.
