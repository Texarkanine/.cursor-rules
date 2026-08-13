---
task_id: iso-24495-decompression-key
date: 2026-08-13
complexity_level: 2
---

# Reflection: ISO 24495 decompression key

## Summary

Filled `rules/iso-24495.mdc` as a two-paragraph always-on decompression key. It names ISO 24495, the four Part 1 principles, Parts 2 and 3 by role, and the IPL Federation URL. QA passed with no rework.

## Requirements vs Outcome

All seven requirements and five acceptance criteria landed. Nothing was dropped or added after intent. The preflight advisory (inline principle names, not bullets) tightened wording; it did not change scope.

## Plan Accuracy

The plan was right: one prose file, then `make test`. No extra files. The only surprise was in intent, before the plan: the first PDF was Part 3 only. The operator redirected to the series summary. Challenges about over-copying and the wrong URL did not fire in build.

## Build & QA Observations

Build was one write. `make test` passed. QA ([ISO 24495 QA review](8f51f3d5-bc57-4b10-8d21-1a8afd1f6eaa)) found no issues.

## Insights

### Technical
- For a paid standard, the decompression key should point at a free, series-level public summary. A sample PDF of one part is the wrong target: it is incomplete and not freely reusable.

### Process
- Preflight's inline-vs-bullets advisory is the always-on token budget acting as a real constraint. Treat it as a plan amendment, not as optional style.

### Million-Dollar Question
- Two sibling a la carte keys (ASD-STE100 for simplified English; ISO 24495 for relevance, findability, understandability, usability) is the elegant form. Merging them would block installing one without the other. What we built is what you would author if both keys had been assumed from the start.
