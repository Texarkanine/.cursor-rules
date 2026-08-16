---
task_id: writing-styles-ruleset
date: 2026-08-16
complexity_level: 2
---

# Reflection: writing-styles-ruleset

## Summary

Shipped four writing-style decompression keys in always-respond, always-write, and ManualPrompt flavors, plus a skills-only `writing-styles` ruleset. QA passed with no rework.

## Requirements vs Outcome

All thirteen brief requirements landed: 12 files, old names gone, always-on pair a la carte, skills-only ruleset, shared qualifier, placeholder sample table, root door. Nothing dropped or added beyond the preflight README "Which Style" pointer paragraph.

## Plan Accuracy

The seven-step sequence and file list were right. Challenges that mattered were the ones we named (symlink depth, README stub links, not expanding keys). No reordering.

## Build & QA Observations

Build was mechanical copy of the key + qualifier with a heading/lead change. `make test` passed on the first run. QA found no issues.

## Insights

### Technical
- When a family has both always-on and call-in flavors, put only the call-ins in the ruleset. Installing the set must not turn on `alwaysApply`.

### Process
- Nothing notable

### Million-Dollar Question

What we built. The only debt was the rename: had the flavor prefix existed when ASD-STE100 and ISO 24495 shipped, this task would have been four new files and a ruleset, not a rename plus ten.
