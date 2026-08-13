---
task_id: iso-24495-decompression-key
complexity_level: 2
date: 2026-08-13
status: completed
---

# TASK ARCHIVE: ISO 24495 decompression key

## SUMMARY

Filled `rules/iso-24495.mdc` as a short always-on decompression key for ISO 24495 (Plain language), matching `rules/asd-ste100.mdc`. It names the four Part 1 principles (relevant, findable, understandable, usable), maps Parts 2 and 3 by role, and points at the IPL Federation public summary. QA passed with no rework. No ruleset.

## REQUIREMENTS

- Fill the stub `rules/iso-24495.mdc` as an always-on key in the asd-ste100 shape (`alwaysApply: true`, name the standard, public URL, precision exception).
- Treat it as a decompression key: name the framework; do not rewrite the standard.
- Ground it in the series, not only Part 3. Name the four Part 1 principles. Note Part 2 (legal communication) and Part 3 (science writing) as applications.
- Link only to https://www.iplfederation.org/iso-standard/. Do not link a sample PDF. Do not copy paid ISO text.
- No ruleset unless later requested. Do not edit generated `.cursor/` copies.
- `make test` still passes.

## IMPLEMENTATION

Two-paragraph body, same layout as `asd-ste100.mdc`. Principles are inline (preflight advisory: no bullets). Canonical file: `rules/iso-24495.mdc`. `REUSE.toml` already covers `rules/**/*.mdc`.

After reflect, the operator asked whether to paraphrase the IPL summary into the rule. Decision: no. The four names plus the part map plus the URL are the payload. Restating the page would duplicate a free source into always-on context and would drift.

**Key files:**

- `rules/iso-24495.mdc` — always-on decompression key
- `memory-bank/archive/features/20260813-iso-24495-decompression-key.md` — this archive

## TESTING

No new automated tests (prose/policy; wording assertions would be change-detectors). `make test` (ruleset symlink + README-link checks) PASS.

- Preflight PASS WITH ADVISORY (inline principle names)
- Build matched the amended plan
- QA PASS with no findings

## LESSONS LEARNED

- For a paid standard, point the key at a free series-level public summary. A sample PDF of one part is the wrong target.
- Do not paraphrase that summary into the rule. Naming is the decompression; copying the explainer fights the key.
- ASD-STE100 and ISO 24495 should stay sibling a la carte keys. They cover different layers. Merging them would block installing one without the other.
- Preflight's inline-vs-bullets advisory is the always-on token budget acting as a real constraint.

## PROCESS IMPROVEMENTS

- When the operator hands a paid-standard PDF of one part, look for a free series summary before treating the PDF as the key. That check happened in intent clarification here; keep doing it.

## TECHNICAL IMPROVEMENTS

None. Optional later: a ruleset that bundles this rule, if consumers want it as a set rather than a la carte.

## NEXT STEPS

- Draft PR from `iso-plain`
- After merge: `chore(dev): ai-rizz sync` so the generated `.cursor/` tree picks up the new always-on rule
