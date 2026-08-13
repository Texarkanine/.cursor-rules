# Task: iso-24495-decompression-key

* Task ID: iso-24495-decompression-key
* Complexity: Level 2
* Type: simple enhancement

Fill the stub `rules/iso-24495.mdc` as a short always-on decompression key for ISO 24495 (Plain language), matching the shape of `rules/asd-ste100.mdc`. Name the four Part 1 principles and the roles of Parts 2 and 3. Point at the IPL Federation public summary. Do not copy paid standard text. Do not add a ruleset.

## Test Plan (TDD)

### Behaviors to Verify

- Always-on key: agent loads `rules/iso-24495.mdc` with `alwaysApply: true` → prose to the operator follows ISO 24495 in spirit
- Decompression: agent reads the four named principles (relevant, findable, understandable, usable) → pretrained knowledge of ISO 24495-1 can fire without a rewrite of the standard
- Series, not Part 3 only: agent reads Parts 2 and 3 named by role → legal communication and science writing are applications of Part 1, not the whole key
- Canonical URL: agent follows the only standard link → https://www.iplfederation.org/iso-standard/ (no sample PDF)
- Precision exception: a required technical term would be lost by style → keep the term; clarity wins
- Regression: `make test` → still PASS (this file is a la carte under `rules/`; symlink and README-link checks must not break)

### Test Infrastructure

- Framework: `make test` (`scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`)
- Test location: `scripts/`
- Conventions: layout/link checks for rulesets; no suite that asserts on rule wording
- New test files: none — this is a prose/policy rule. A test that asserted on headings or phrases in `iso-24495.mdc` would be a change-detector. Verify by review in QA, plus the existing `make test` regression.

## Implementation Plan

1. [x] Write the ISO 24495 decompression key
   - Files: `rules/iso-24495.mdc`
   - Tests first: N/A for prose & policy artifacts
   - Changes: keep `alwaysApply: true`. Add a short title and body in the shape of `rules/asd-ste100.mdc`:
     - Instruct the agent to write agent-to-operator prose in the spirit of ISO 24495 (Plain language)
     - Name the four Part 1 principles: relevant, findable, understandable, usable
     - Note that Part 2 applies those principles to legal communication and Part 3 to science writing
     - Link only to https://www.iplfederation.org/iso-standard/
     - Keep the same precision exception as ASD-STE100 (required technical terms and precise meaning win)
     - Stay short. Do not copy ISO clause text. Do not add a ruleset, README listing, or generated `.cursor/` copy (sync is a later `chore(dev): ai-rizz sync` after push)
     - Preflight amendment: prefer inline comma-separated principle names over a bulleted list to minimize always-on context cost (matches asd-ste100 brevity)

2. [x] Regression check
   - Files: none new
   - Tests first: N/A for prose & policy artifacts
   - Changes: run `make test` and confirm PASS

## Technology Validation

No new technology - validation not required

## Dependencies

- Shape template: `rules/asd-ste100.mdc`
- Public summary: https://www.iplfederation.org/iso-standard/
- Licensing: `REUSE.toml` already covers `rules/**/*.mdc` as PPL-S; no annotation change

## Challenges & Mitigations

- Over-copying the standard: keep the file at asd-ste100 length plus the four principle names and the Part 2/3 one-liner. If a sentence restates a clause instead of naming it, cut it.
- Two always-on voice rules (ASD-STE100 and ISO 24495): they target different layers (simplified English vs relevance/findability/understandability/usability). Both say "in the spirit of" and share the precision exception. Do not try to merge them in this task.
- Wrong canonical URL: use only the IPL Federation page from the approved intent. Do not link iso.org purchase pages or the iteh sample PDF.

## Pre-Mortem

- The key names only Part 3 science writing, so agents skip Part 1: already covered by Challenge "Over-copying" plus Implementation step 1 (name Part 1 principles; Parts 2 and 3 by role).
- The key grows into a mini-style-guide and burns always-on context: already covered by the length cap in Challenge "Over-copying".
- A later agent adds heading/phrase tests to "satisfy TDD": the Test Plan already forbids that; preflight should FAIL any such addition.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
