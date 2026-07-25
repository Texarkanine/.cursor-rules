# Task: README Refresh — Sell the High-Value Contents

* Task ID: readme-refresh-sales-pitch
* Complexity: Level 2
* Type: Simple enhancement (documentation)

Rewrite the root `README.md` as a tight, value-forward pitch that positions the four rulesets (niko, authoring, script-it, shell) front-and-center, and create the missing `rulesets/script-it/README.md` in the style of the sibling ruleset READMEs. Canonical sources only; the root stays a pitch, not a catalog.

## Test Plan (TDD)

### Behaviors to Verify

- Script-it README exists: `rulesets/script-it/README.md` created → `make test` (readme-links job) picks it up and passes; today the file's absence means acceptance criterion 3 is unmet (RED state).
- Script-it README links resolve: each internal link (to `script-it-instead.mdc` symlink and `skills/how-to-script-it-instead`) → target exists on disk, asserted by `scripts/check-ruleset-readme-links.sh` via `make test`.
- Ruleset symlinks unaffected: `make test` (symlinks job) → still passes; no symlinks are touched.
- Root README links resolve: every relative link in root `README.md` (four ruleset READMEs, `rules/`, external URLs untouched) → target exists on disk. Root README is *outside* the CI checker's `rulesets/` scope, so this is asserted by a one-off inline link-extraction check during Build/QA (same awk logic as the checker, scoped to `README.md`).
- Value-prop accuracy: each ruleset's pitch line → consistent with that ruleset's own README/rule content (manual cross-read against `rulesets/{niko,authoring,shell}/README.md`, `rules/script-it-instead.mdc`, `rules/how-to-script-it-instead/SKILL.md`).
- Markdown style: both files → conform to `rules/markdown-style.mdc` (globs match `**/*.md`): no hard wrapping, short stand-alone headings, no clarifying parentheticals in headings.

### Test Infrastructure

- Framework: none (operator-established precedent from `rulesets-link-ci`): on-disk layout assertions via POSIX scripts
- Test location: `scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`, aggregated by `make test`; CI runs the same targets
- Conventions: layout-property scripts are the assertions; RED→GREEN is encoded as "acceptance property unmet before change, `make test` green after"
- New test files: none (new README simply enters the existing checker's scope)

## Implementation Plan

1. ✅ RED demonstration (preflight amendment)
    - Files: none
    - Changes: run the scoped one-off link check asserting the existence of `rulesets/script-it/README.md` and the intended root-README link targets — expect FAIL on the missing script-it README (RED)
2. ✅ Create `rulesets/script-it/README.md`
    - Files: `rulesets/script-it/README.md` (new)
    - Changes: sibling-style README (per `authoring`/`shell` pattern): H1 + one-paragraph intro on the ruleset's purpose (stop paying inference cost for mechanical tool-call loops), then Purpose/Scope entries for:
        - `script-it-instead` (link `./script-it-instead.mdc`) — always-apply tripwire; third structurally-similar tool call stops the loop
        - `how-to-script-it-instead` (link `./skills/how-to-script-it-instead/SKILL.md`) — the batch-scripting how-to: discover runtimes/CLIs, choose approach, collect→compress→one tool call
    - Verify: re-run the RED check → GREEN; `make test` passes (links + symlinks)
3. ✅ Rewrite root `README.md`
    - Files: `README.md`
    - Changes:
        - New opening: what this repo is (canonical, composable agent customizations — rules, skills, rulesets) and why to care
        - New "What's Inside" section: four doors with 1–2-sentence value props + links: `rulesets/niko/README.md`, `rulesets/authoring/README.md`, `rulesets/script-it/README.md`, `rulesets/shell/README.md`
        - Keep/refresh install guidance (ai-rizz, a16n, client-side-mdc-render links)
        - Refresh Structure section: mention both rules (`.mdc`) and skills (`<name>/SKILL.md`) tiers post-migration; rulesets = symlink groupings
        - Keep Checks section (`make test`) and Big Thanks list as-is
    - Verify: one-off link-extraction check over `README.md` confirms all relative targets exist
4. ✅ Full verification
    - Files: none
    - Changes: run `make test`; run the one-off root-README link check; cross-read pitch lines against source docs

## Technology Validation

No new technology - validation not required.

## Dependencies

- Existing check scripts and Makefile (present, verified)
- REUSE coverage: `rulesets/**/README.md` annotation already exists in `REUSE.toml` — no license file changes needed
- Ruleset READMEs and rule/skill sources as ground truth for pitch accuracy

## Challenges & Mitigations

- Root README is outside CI link-check scope (`rulesets/` only): a broken root link would ship silently. Mitigation: explicit one-off link check in Build step 2 / QA.
- Subjective pitch tone may miss the operator's taste: Mitigation: keep prose tight, ground every claim in an existing doc, no invented superlatives; operator reviews at PR.
- Stale "rules-only" terminology creeping back in: Mitigation: Structure section explicitly names both tiers per `systemPatterns.md` File Organization.
- Accidentally editing generated trees: Mitigation: touch only root `README.md` and `rulesets/script-it/README.md`; never `.cursor/`/`.claude/`.

## Pre-Mortem

- Wrong premise — operator actually wanted a full index: already resolved; brief explicitly says "NOT a full index"; ruleset READMEs own catalogs.
- Pitch overpromises (e.g., claims about Niko outcomes not supported by its README): plan response — every value prop must be traceable to a sentence in the linked README/rule; QA includes a cross-read step.
- Link rot at the wrong layer — links written relative to the wrong base (root vs ruleset dir): plan response — Build verifies with the actual checker (`make test`) for the ruleset README and the scoped one-off check for root; already covered by Challenge 1 for root.
- Markdown-style violation (hard-wrapped prose) slips in: plan response — final pass against `markdown-style.mdc` before QA.

## Preflight Findings

- PASS with one plan amendment: explicit RED step (run scoped link check before creating the script-it README) inserted as Implementation Plan step 1.
- Advisory (not applied — scope deviation): extend `scripts/check-ruleset-readme-links.sh` to also cover the root `README.md`, making the one-off root link check a permanent CI guarantee.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight - PASS (with advisory)
- [x] Build - COMPLETE
- [ ] QA
