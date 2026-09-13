---
task_id: speedup-giesen
complexity_level: 2
date: 2026-09-13
status: completed
---

# TASK ARCHIVE: speedup-giesen

## SUMMARY

Shipped `/speedup-giesen` as an a-la-carte skill at `rules/speedup-giesen/SKILL.md`. It opens on Fabian Giesen's 2× / 100× tweet (operator-confirmed: https://x.com/rygorous/status/1271296834439282690) and audits a finished, behavior-correct codebase for wasted work. The report turn does not edit; the operator picks which findings to cut, then When fixing runs. Draft PR: [#126](https://github.com/Texarkanine/.cursor-rules/pull/126).

## REQUIREMENTS

- Canonical `rules/speedup-giesen/SKILL.md`, invocably named `speedup-giesen`.
- Opening key is the entire Giesen tweet, attributed, with that URL. Do not paraphrase. Use 2× / 100×, not the 50% / 10× circulating variant.
- Shape the hunt from coachhouse-isp-status (`4ca55929-6140-4444-b3eb-d3183f57a455`) and client-side-mdc-render (`5dc46b7a-40af-48dd-8e69-fadf1e1caae9`).
- Canonical `rules/` only; no generated `.cursor/` / `.claude/` edits; no ruleset unless later requested.
- Prose/policy: no change-detector tests. `make test` still passes.
- Post-reflect operator recast: audit and wait, not apply-in-the-same-turn.

## IMPLEMENTATION

One file: `rules/speedup-giesen/SKILL.md`. Composite: the quote is the stance; a numbered pass is the workflow. A la carte like `xy-problem`. `REUSE.toml` already covers `rules/**/*.md`.

The pass reports stupid-class findings (surface, waste, why 100×, what you would stop doing) and stops. When fixing is a later turn, gated on the operator naming items. Tests: change them only if the speedup can be wrong in a way the old suite would still pass; then the smallest test that fails when that shortcut is wrong, not a test of the new internals. Reuse going stale is an example, not the predicate.

Preflight advisory (measure before/after) was folded into the verify step as "report the observed multiplier when timed," not a seventh required step.

## TESTING

No new automated tests. `make test` PASS (ruleset symlink + README-link checks; a-la-carte `rules/` skills are invisible to those scripts). `/niko-preflight` PASS WITH ADVISORY. `/niko-qa` PASS on the apply-cuts draft. The post-reflect audit-then-wait recast was operator-directed and was not re-run through QA.

## LESSONS LEARNED

- `make test` cannot see an a-la-carte skill under `rules/`. That is layout-script scope, not a reason to lock wording with a test.
- When the operator names a prior local pass by repo, search sibling `project_id` / `cwd` values. The remembered name was lan-isp-status; the matching hunt was coachhouse-isp-status.
- Do not write a fake absolute ("do not change tests") and then unsay it. State the real conditional rule.
- The suite tracks the product contract, not the new internals. A speedup can add a failure the old tests cannot see; that is when a test is owed.

## PROCESS IMPROVEMENTS

- Distill a named quote as a decompression key; spell out only what the quote does not already encode (here: finished product, audit-then-wait, untested shortcuts).
- Absolute-then-carve-out is the wrong shape for an agent reader.

## TECHNICAL IMPROVEMENTS

None. Optional later: a ruleset if consumers want this bundled rather than a la carte.

## NEXT STEPS

- Merge PR #126.
- After merge: `chore(dev): ai-rizz sync` so the generated `.cursor/` tree offers `/speedup-giesen`.
