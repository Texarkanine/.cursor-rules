---
task_id: writing-styles-ruleset
complexity_level: 2
date: 2026-08-17
status: completed
---

# TASK ARCHIVE: writing-styles ruleset

## SUMMARY

Shipped four writing-style decompression keys (ASD-STE100, ISO 24495, Thomas and Turner classical style, Orwell's six rules) in always-respond, always-write, and skill flavors, plus a skills-only `writing-styles` ruleset. Always-on files stay a la carte. The ruleset ships only the four skills so installing the set does not turn on `alwaysApply`. QA passed. Post-reflect polish renamed every file to a `style-` prefix, made H1s generic obligation/scope, let the agent pick the skills, and filled the README sample table. Draft PR: https://github.com/Texarkanine/.cursor-rules/pull/112

## REQUIREMENTS

Original brief (paths later superseded by Rework):

- Four slugs: `asd-ste100`, `iso-24495`, `thomas-turner-truth` (TTT on lists; credit both authors), `orwell-6`.
- Three files per slug: always-respond, always-write, skill. Rename existing `rules/asd-ste100.mdc` and `rules/iso-24495.mdc` into the always-respond slots.
- Always-on: `alwaysApply: true`, not members of the ruleset.
- Skills: key + shared qualifier only. Keys name the framework; do not rewrite it.
- Shared qualifier on every file: if applying the style would remove a required technical term or a precise meaning, keep the term. Clarity and accuracy trump style.
- Ruleset `rulesets/writing-styles/` ships only the four skills plus a README with a sample table. Root README door.
- Canonical sources only — do not edit generated `.cursor/` or `.claude/` copies. Do not harvest samples by moving `~/.claude` trees. Do not register the ruleset in this clone's `ai-rizz.skbd` unless asked.
- `make test` still passes. No wording/change-detector tests.

Post-reflect Rework (approved in-session; this is what shipped):

- Filenames: `rules/style-always-respond-<slug>.mdc`, `rules/style-always-write-<slug>.mdc`, `rules/style-<slug>/SKILL.md`. Invoke `/style-asd-ste100`.
- Always-on H1s: `# 🚨 Required Writing Style for Responses` / `for Prose`. Skill H1: `# Required Writing Style`. Body holds the decompression key.
- Always-respond lead: `Always respond to the operator`. Orwell: `in keeping with` (not `with`/`using`, which reads as “print the list”).
- Skills have real “Use when…” trigger descriptions with near-neighbor exclusions. `disable-model-invocation` removed — the agent may pick them.
- Operator filled the README sample table (Opus 5, prompt “Explain what NodeJS is.”).

## IMPLEMENTATION

Level 2, seven-step plan, existing `make test` as the executable gate. No new test files. Build was a mechanical copy of key + qualifier with heading/lead changes, then a rename chain:

1. `rules/asd-ste100.mdc` / `rules/iso-24495.mdc` → `always-respond-<slug>.mdc`
2. `turner-truth` → `thomas-turner-truth` (list label TTT)
3. All twelve files → `style-` prefix; skill folders `style-<slug>`; ruleset symlinks `../../../rules/style-<slug>`

`alwaysApply` is injection only. The model-facing must is 🚨 + “Required” on the H1 + “Always” as the first body verb. Not CRITICAL (fights the qualifier). Heading is obligation/scope; body is the key. Slugs (`thomas-turner-truth`, `orwell-6`) are not keys and must not appear in titles.

**Key files:**

- `rules/style-always-respond-{asd-ste100,iso-24495,thomas-turner-truth,orwell-6}.mdc`
- `rules/style-always-write-{asd-ste100,iso-24495,thomas-turner-truth,orwell-6}.mdc`
- `rules/style-{asd-ste100,iso-24495,thomas-turner-truth,orwell-6}/SKILL.md`
- `rulesets/writing-styles/skills/style-*` → `../../../rules/style-<slug>`
- `rulesets/writing-styles/README.md` — styles + filled sample table
- Root `README.md` — 📝 door
- `memory-bank/archive/features/20260817-writing-styles-ruleset.md` — this archive

Old names gone: `rules/asd-ste100.mdc`, `rules/iso-24495.mdc`, unprefixed `always-respond-*` / `always-write-*`, `*-style/` folders.

## TESTING

No new automated tests (prose/policy; wording assertions would be change-detectors). `make test` (ruleset symlink + README-link checks) PASS on first build run and after polish.

- Preflight PASS WITH ADVISORY (Composer 2.5) — existing checkers suffice; optional README “Which Style” pointer added
- Build matched the amended plan
- QA PASS (Gemini 3.1 Pro) — no findings
- Reflect: persistent files (`productContext.md`, `systemPatterns.md`, `techContext.md`) skip-reconciled — the 3-flavor split stays a writing-styles convention, not a standing contract

## LESSONS LEARNED

- When a family has both always-on and call-in flavors, put only the call-ins in the ruleset. Installing the set must not turn on `alwaysApply`.
- Had the flavor prefix existed when ASD-STE100 and ISO 24495 shipped, this task would have been four new files and a ruleset, not a rename plus ten.
- `alwaysApply` does not tell the model the rule is required. The H1 and the first body verb do.
- Skill trigger descriptions that say “leans X; also Y” contradict themselves. Name when to use and a near neighbor they do not cover, in ordinary words.

## PROCESS IMPROVEMENTS

- Ship the filename convention (`style-always-respond-`, `style-always-write-`, `style-<slug>/`) before the first always-on key in a family, so later siblings are adds not renames.
- Do not harvest `claude -p` samples by moving `~/.claude` trees. Operator fills the table, or the cells stay placeholders.

## TECHNICAL IMPROVEMENTS

None as architecture. The 3-flavor split is a writing-styles convention only — do not promote it into `systemPatterns.md` unless a second family needs the same split.

## NEXT STEPS

- Merge draft PR https://github.com/Texarkanine/.cursor-rules/pull/112
- After merge: `chore(dev): ai-rizz sync` so the generated `.cursor/` / `.claude/` trees pick up the new files (ai-rizz reads remote; do not edit those trees in-task)
- Do not register `writing-styles` in this clone's `ai-rizz.skbd` unless asked
