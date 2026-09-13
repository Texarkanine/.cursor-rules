# Task: speedup-giesen

* Task ID: speedup-giesen
* Complexity: Level 2
* Type: simple enhancement

A slash-invocable topic skill whose opening payload is Fabian Giesen's 2× / 100× tweet, used as a decompression key, then a short numbered passover of a finished, behavior-correct codebase looking for work we can stop doing.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior. This task is entirely prose/policy (skill wording). Do not invent tests.

Existing `make test` (ruleset symlink + README-link checks) must still pass. It will not see this skill unless a ruleset grows a symlink or README link; this plan does not add either.

### Test Infrastructure

- Framework: POSIX shell scripts invoked by Make
- Test location: `scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`
- Conventions: no wording assertions; layout/link integrity only
- New test files: none

## Implementation Plan

### 1. Author `/speedup-giesen` — prose/policy — done

- Files: `rules/speedup-giesen/SKILL.md`
- No tests: prose/policy artifact

1. Create `rules/speedup-giesen/SKILL.md` as canonical source (this repo never authors into generated `.cursor/` / `.claude/` trees). `REUSE.toml` already covers `rules/**/*.md` as PPL-S.
2. Frontmatter: `name: speedup-giesen`. Do not set `disable-model-invocation`. Write `description` as a trigger: finished/correct codebase + speed without behavior change + "are we doing something stupid" / 10×–100× class. Name the near neighbor it is not: a YAGNI/simplification pass, a new-feature build, or Knuth's noncritical 97%. Keep it under the agentskills.io description limit.
3. Open the body on the entire Giesen tweet as the decompression key, attributed, with the operator-confirmed URL. Do not paraphrase. Use this text:
    look, I'm sorry, but the rule is simple:
    if you made something 2x faster, you might have done something smart
    if you made something 100x faster, you definitely just stopped doing something stupid
    — Fabian Giesen (@rygorous), 11 June 2020
    https://x.com/rygorous/status/1271296834439282690
4. Treat the skill as a composite: the quote is personality (stance); a numbered pass is workflow (order). Do not rewrite a performance-engineering textbook — the named quote unpacks that. Add only what the quote does not encode, taken from the two local templates (coachhouse-isp-status `4ca55929-6140-4444-b3eb-d3183f57a455`, client-side-mdc-render `5dc46b7a-40af-48dd-8e69-fadf1e1caae9`):
    1. Confirm the product already behaves correctly. If the ask is a new feature or a behavior change, stop — this skill does not apply.
    2. Name the surfaces that must get cheaper (operator-named, else the boot/request path the user actually waits on). Do not hunt the rest of the tree.
    3. Walk those surfaces for wasted work of the class those sessions found: the same job every tick/render, parsing more than the answer requires, a new connection per request, rebuilding what is already in hand, destroying work before the replacement exists. Examples of the class, not a checklist to exhaust.
    4. Classify each candidate: stopping it is "something stupid" (100× class) vs "something smart" (2× class — new cache layer, clever algorithm, architecture rewrite). Keep the first. Leave the second unless the operator asked for clever.
    5. Apply only the stupid-class cuts. Observable behavior stays. Do not add machinery to go faster. Do not edit tests unless a new hold would make a broken optimization invisible — then add the smallest behavior lock, not a wording assertion.
    6. Verify behavior still holds. Report what you stopped doing and which class of speedup it is. If you only find 2×-smart candidates, report them and stop.
5. Headings name content, no parentheticals, no hard-wrapped prose. No cross-references to sibling skills (ponytail, niko, xy-problem). No new ruleset, symlink, or README line — a la carte under `rules/`, same as `xy-problem`.
6. Run `make test` after the file exists. Expect PASS with no new coverage of this skill.

## Technology Validation

No new technology - validation not required

## Dependencies

- Prompt-authoring kinds (personality + workflow composite) and skill-frontmatter trigger rules — apply at author time; do not cite those files from inside the skill.
- Giesen tweet URL, operator-confirmed.
- Existing Make layout tests, run but not extended.

## Challenges & Mitigations

- Skill becomes a performance textbook and fights the decompression key: keep the quote as the payload; workflow is only the novel constraints (behavior preservation, finished product, stupid vs smart, do not add machinery).
- Skill is so thin the agent still hunts clever 2× micro-opts: step 4–6 make "smart" the reject class unless asked, and require stop-and-report when that is all there is.
- Trigger fires on "make it faster" during feature work: description bounds to already-correct products and names new features as a non-use.
- A la carte skill is easy to miss in a niko-only install: out of scope; no ruleset unless later requested (same call as the ISO 24495 key).

## Pre-Mortem

- Failed because we paraphrased Giesen or led with a lecture: plan step 3 forbids paraphrase and requires the tweet as the opening key — already covered by Challenge 1's shape; the fix is the ordered body, not a new step.
- Failed because we added it to the niko ruleset and it loaded on every coding task: the plan explicitly does not add a ruleset or niko symlink.
- Failed because Build wrote change-detector tests against the quote: Test Plan already forbids them; Preflight should FAIL the plan if a later edit adds wording assertions.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA

## QA Results

- ✅ PASS — The canonical skill meets the plan and brief: correct path and name, complete attributed quote and confirmed URL, and the six-step behavior-preserving passover.
- ✅ PASS — The preflight measurement advisory was addressed narrowly in step 6; no unnecessary machinery was introduced.
- ✅ PASS — `make test` passed; no generated-tree, ruleset, symlink, README, or change-detector-test changes were made.
