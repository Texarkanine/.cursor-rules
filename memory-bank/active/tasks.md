# Task: writing-styles-ruleset

* Task ID: writing-styles-ruleset
* Complexity: Level 2
* Type: simple enhancement

Expand the two existing always-on writing-style keys into a four-slug family (always-respond, always-write, ManualPrompt skill) and a skills-only `writing-styles` ruleset whose README leaves sample-output cells as placeholders.

## Test Plan (TDD)

### Behaviors to Verify

- [Ruleset assembly]: add `rulesets/writing-styles/skills/<slug>-style` → `../../../rules/<slug>-style` → `make test` / `test-symlinks` passes (targets exist)
- [README canonical links]: `rulesets/writing-styles/README.md` links to `../../rules/<slug>-style/SKILL.md` (not the ruleset symlink stub) → `make test` / `test-readme-links` passes
- [Always-on stay a la carte]: `rulesets/writing-styles/` contains no `always-respond-*.mdc` or `always-write-*.mdc` → find under that tree returns none
- [Old names gone]: `rules/asd-ste100.mdc` and `rules/iso-24495.mdc` do not exist; renamed `always-respond-*` files do
- [Edge: symlink relative path]: a `../../rules/...` link from `rulesets/writing-styles/skills/` would miss (too short) → use `../../../rules/<slug>-style` like `authoring` / `shell`
- [Edge: README stub link]: linking `./skills/asd-ste100-style` → `test-readme-links` fails with "symlink link … point at rules/ canonical path"
- [Regression]: existing rulesets still pass `make test`
- [Review, not automated]: each of the 12 files has the flavor heading, the shared qualifier sentence, and the correct frontmatter (`alwaysApply: true` vs `disable-model-invocation: true`); skill `name` matches folder; keys are not restated into full style manuals

### Test Infrastructure

- Framework: repo `make test` (POSIX shell checkers)
- Test location: `scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh` (wired in `Makefile`)
- Conventions: checkers walk every `rulesets/` tree; a new ruleset is picked up automatically. No wording assertions (change-detectors).
- New test files: none

## Implementation Plan

1. [x] Rename and retitle the two existing always-respond keys
   - Files: `rules/asd-ste100.mdc` → `rules/always-respond-asd-ste100.mdc`; `rules/iso-24495.mdc` → `rules/always-respond-iso-24495.mdc`
   - Tests first: N/A for prose & policy artifacts
   - Changes: `git mv` both. Heading becomes `Always Respond in ASD-STE100` / `Always Respond in ISO 24495`. Keep the existing key sentence (standard name + public URL + ISO part map). Replace the last sentence with: `If doing so would remove a required technical term or a precise meaning, keep the term. Clarity and accuracy trump style.` Keep `alwaysApply: true`.

2. [x] Add the two new always-respond keys
   - Files: `rules/always-respond-turner-truth.mdc`, `rules/always-respond-orwell-6.mdc`
   - Tests first: N/A for prose & policy artifacts
   - Changes: Same frontmatter and qualifier. Headings: `Always Respond in Turner Truth` / `Always Respond in Orwell 6`. Bodies stay decompression keys — do not expand Pinker, Thomas and Turner, or Orwell's six rules.
     - turner-truth: use classical style as mentioned by Steven Pinker and according to [Thomas and Turner's *Clear and Simple as the Truth*](https://press.princeton.edu/books/hardcover/9780691654744/clear-and-simple-as-the-truth), using plain English.
     - orwell-6: Use Orwell's 6 rules for writing.

3. [x] Add the four always-write keys
   - Files: `rules/always-write-asd-ste100.mdc`, `rules/always-write-iso-24495.mdc`, `rules/always-write-turner-truth.mdc`, `rules/always-write-orwell-6.mdc`
   - Tests first: N/A for prose & policy artifacts
   - Changes: `alwaysApply: true`. Headings: `Always Write Prose in <Style>`. Same keys and qualifier as the matching always-respond file; the lead clause is writing prose, not agent-to-operator replies.

4. [x] Add the four ManualPrompt skills
   - Files: `rules/asd-ste100-style/SKILL.md`, `rules/iso-24495-style/SKILL.md`, `rules/turner-truth-style/SKILL.md`, `rules/orwell-6-style/SKILL.md`
   - Tests first: N/A for prose & policy artifacts
   - Changes: Frontmatter `name: <slug>-style` (must match folder), `description: Invoke with /<slug>-style`, `disable-model-invocation: true`. Heading: `<Style> Style`. Body is the key plus qualifier only — no respond/write domain, no "when to use" section.

5. [x] Assemble the `writing-styles` ruleset
   - Files: `rulesets/writing-styles/skills/{asd-ste100-style,iso-24495-style,turner-truth-style,orwell-6-style}` (symlinks), `rulesets/writing-styles/README.md`
   - Verification: existing `make test` is the gate (no new test files). Create skill dirs in step 4 first so symlink targets exist; run `make test` after symlinks + README land (full regression again in step 7).
   - Changes: `ln -s ../../../rules/<slug>-style` for each skill (same relative depth as `rulesets/authoring/skills/`). README: short intro; optional one-paragraph "when to use which style" guide (decompression pointers only — no expanded manuals); state that always-on `always-respond-*` / `always-write-*` files live a la carte under `rules/` and are **not** in this ruleset; four skill entries with Purpose/Scope linking `../../rules/<slug>-style/SKILL.md`; one shared prompt (`explain what nodejs is`) and a four-row sample table whose cells are explicit placeholders for an operator-filled stripped Opus 5 `claude -p` run. Do not invent sample outputs. Do not add always-on `.mdc` files to this tree.

6. [x] Add the root README door
   - Files: `README.md`
   - Tests first: N/A for prose & policy artifacts (root README is outside `check-ruleset-readme-links.sh`)
   - Changes: New What's Inside entry for [writing-styles](./rulesets/writing-styles/README.md), sibling tone to authoring/shell/welfare. One or two sentences: four decompression-key styles, ManualPrompt call-ins in the ruleset, always-on respond/write variants a la carte.

7. [x] Verify layout
   - Files: none new
   - Tests first: run `make test` (whole suite)
   - Changes: fix any broken symlink or README-link failure. Confirm old `rules/asd-ste100.mdc` / `rules/iso-24495.mdc` paths are gone and `rulesets/writing-styles/` has no always-on `.mdc`.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `make test` checkers (`scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`)
- Public URLs already used or confirmed: https://www.asd-ste100.org/, https://www.iplfederation.org/iso-standard/, https://press.princeton.edu/books/hardcover/9780691654744/clear-and-simple-as-the-truth
- Cursor skill frontmatter: `disable-model-invocation` per https://cursor.com/docs/skills#frontmatter-fields

## Challenges & Mitigations

- [Copy-paste drift across 12 files]: copy the qualifier sentence verbatim; vary only heading, lead clause (respond vs write vs none), and the key sentence
- [README points at ruleset symlink stubs]: link `../../rules/<slug>-style/SKILL.md` only; `test-readme-links` will catch a stub
- [Wrong symlink depth]: use `../../../rules/<slug>-style` from `rulesets/writing-styles/skills/`, matching authoring/shell
- [Always-on files accidentally added to the ruleset]: step 5 forbids `.mdc` in that tree; step 7 find-checks it
- [Keys expand into restated manuals]: steps 2–4 say do not expand; Turner/Orwell stay the approved one-liners
- [Invented README samples]: placeholders only; do not run or fake `claude -p`

## Pre-Mortem

- [Old filenames left as copies, so consumers keep installing `asd-ste100`]: already covered by Challenge on assembly — step 1 is `git mv`, step 7 asserts the old paths are gone
- [Ruleset ships always-on rules and the skills become redundant]: already covered by Challenge "Always-on files accidentally added"
- [README sample table filled with guessed prose, presented as Opus 5 output]: already covered by Challenge "Invented README samples"
- [Root door omitted because `make test` does not see `README.md`]: plan response — step 6 is a required implementation step, not optional docs polish
- [Skill `name` ≠ folder, so `/asd-ste100-style` does not resolve]: plan response — step 4 requires `name` match folder (`<slug>-style`)

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS WITH ADVISORY)
- [x] Build
- [x] QA (PASS)
