# Current Task: sync-pr-feedback-judgier-with-main

**Complexity:** Level 1

## Fix

- What broke: `pr-feedback-judgier` was behind `main`; merge conflict in `rules/pr-feedback-judge/SKILL.md` after main reformatted headings
- Why: this branch added feedback-gating sections; main renamed section headings and trimmed parentheticals
- What changed: kept gating (author resolution, what becomes an Item, fetch/filter orchestration); adopted main's `## Tier Detection Order` and other auto-merged heading reformatting
- Files affected: `rules/pr-feedback-judge/SKILL.md` (plus clean merges of `always-tdd`, `niko-core`, `test-running-practices` from main)

## QA

- Result: PASS
- Findings: none blocking; gating semantics retained; main heading style adopted; `main` is ancestor of HEAD; no conflict markers
