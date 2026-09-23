---
task_id: effort-variant-slug
date: 2026-09-23
complexity_level: 2
---

# Reflection: effort-variant-slug

## Summary

`pick.py` places an unmatched effort spelling in memory and ranks it with the existing window. When the author spelling still cannot be placed, the script prints that spelling and exits 0. QA passed with one advisory.

## Requirements vs Outcome

The brief's five requirements shipped. Different efforts stay different rows, the printed reviewer is an enabled spelling or the author, and `catalog.json` is not given a row per effort. The author echo was added after planning, at the operator's request, and it lives in `select` rather than in `SKILL.md`.

## Plan Accuracy

The three-step sequence held. BenchLM having no per-effort scores was confirmed before the plan, so the derived score was not a surprise during build. The surprise was the nudge fixture: a real stored row inside the gap is the far neighbor, so the interpolated score does not land on it. The test had to use an effort-source row, which placement ignores.

## Build & QA Observations

The new tests failed on the stub, then passed. `make test` ended at 55 tests. QA found one unreachable guard after a successful expand and did not block. Preflight's "stored rows only" and docstring advisories were taken during build. The both-siblings branch stayed, with a test.

## Insights

### Technical

- A stored score strictly between the anchor and the model you thought was next is the far neighbor. A formula test that wants to land on an existing score has to use a row the search is not allowed to treat as a neighbor.

### Process

- Picking policy belongs in the script. A skill sentence that tells the agent what to do on exit 2 is a second picker.

### Million-Dollar Question

If effort had been a column from the start, the catalog key would be the model stem and the stored effort would be a field. Placement would compare effort indexes without parsing suffixes, and `xhigh` would not have to be matched before `high`. The keys we already ship encode effort in the slug, so the suffix parser is the fit for this catalog. A stem migration was not this task.
