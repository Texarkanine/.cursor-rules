# Task: txrk9-pr-review

* Task ID: txrk9-pr-review
* Complexity: Level 2
* Type: simple enhancement

Land the TXRK9 PR Review prompt as `rules/pr-review/SKILL.md` and retarget it so Other findings actually get published. Critical, posting shape, cap, neighborhood filters, and silence-after-a-real-cull stay. No CodeRabbit nit stream. No merge with `pr-feedback-judge`.


## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior. Skill wording is prose/policy under always-tdd. Do not invent change-detector tests that lock prompt text.

### Test Infrastructure

- Framework: `make test` (`scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`)
- Test location: `scripts/`
- Conventions: layout/link checks on ruleset trees only
- New test files: none

This change does not add a ruleset or a README link, so `make test` is a no-op regression check, not coverage of the prompt. Not blocking: infrastructure exists; it does not apply to this artifact.

## Implementation Plan

### 1. Author `rules/pr-review/SKILL.md` — prose/policy

- Files: `rules/pr-review/SKILL.md`
- No tests: prose/policy artifact

**Packaging (locked):**

1. Canonical path `rules/pr-review/SKILL.md`. No ruleset wrapper (same as `pr-feedback-judge`). Do not edit `.cursor/` or `.claude/`.
2. Frontmatter: `name: pr-review`, `disable-model-invocation: true`, a description that names PR review / TXRK9 / the automation paste-source, and names `pr-feedback-judge` plus ponytail-review as neighbors it does not cover.
3. Body after the closing `---` is the paste payload. Do not put "this is a skill" or paste instructions in the body — the operator copies from the H1 down.
4. REUSE already covers `rules/**/*.md` as PPL-S. No `REUSE.toml` edit.
5. Apply `prompt-authoring`: composite is fine if personality / workflow / reference stay legible; number ordered steps; no sibling-prompt cross-references; spend `never` only where literal; self-check before done.
6. Apply `illustrate-complexity` / workflow-prompt diagram rule: add one compact mermaid flowchart as the *map* of hunt → cull → sort → post (including the Other pass and early abort). Numbered prose remains the *driving instructions*. Do not cram the bar into the chart.

**Start from the operator's current prompt (the `/niko` message), then apply these Other-sensitivity edits — not a rewrite:**

1. **Personality (opening).** Keep advisory reviewer, Critical vs Other, no invented nits. Retarget silence: a clean all-clear is success only after Other has been hunted and culled. Inventing nits to look thorough is a failed review. Dropping a surviving Other so the review looks quiet is also a failed review. Do not keep the current "Silence is a successful review" as an unqualified default — that line is why live runs approve with zero inlines.
2. **Other hunt (workflow), only when Q2 and Q3 are yes.** After the cascade, before approve, a numbered Other pass. Closed hunt list (bullets = set, not sequence):
    - An edge the new code does not handle, with a named input, while the happy path still works
    - A test that would still pass if that edge were wrong
    - A lockstep this repo already keeps (prompt / help / completion / docs vs code, or two files that must say the same thing) that this diff broke or failed to update
    - A silent fallback or swallowed error this diff introduces
    - A caller or callee contract the neighbors honor that this hunk does not
3. **Duty before approve.** If Q2 and Q3 are yes, hunt Other before approving. Approving because nothing is Critical, without that hunt, is a miss. Keep "If nothing survives and you did review the diff: approve."
4. **Split the confidence filter (reference).** Critical: omit if you cannot prove the intent-failing scenario. Other: omit if you cannot name a concrete input, caller, or invariant; do **not** omit merely because a stronger author might have done it on purpose. Delete or narrow the current blanket "If a stronger author might have done this on purpose and you cannot prove the claim, omit it" so it no longer kills Other.
5. **Keep unchanged:** Q1–Q4 cascade and stop-at-first-no; Q2/Q3 early abort; Critical definition; neighborhood-checked and not-already-owned filters; Valid and In scope; cap of 6; inline-when-possible; 🦮 What's In This PR shape; comment templates; `post_review_comment_on_pr` once; never open a PR; request review by `Texarkanine` when Critical and the author is not that user; no nit/thought/suggestion labels; no "no issues" banner.
6. **Do not add:** a quota ("post at least N Other"); few-shot examples (they become the whole taxonomy); CodeRabbit severity theater; a merge with `pr-feedback-judge`.

**Calibration (for the author of the skill, not to paste as few-shots):** Other that should survive looks like SumMem#5 recall-past-`WAKE_LINES`, SumMem#10 nap instruction naming `summem` instead of `.summem/summem`, SumMem#18 dropped "keep notes tracked" lockstep. Nits that must still die: formatting, naming, import order, "consider extracting", house patterns, CI-owned issues.

### 2. Layout regression — prose/policy

- Files: none new
- No tests: prose/policy artifact

1. Run `make test` to confirm ruleset symlink and README-link checks still pass.

## Technology Validation

No new technology - validation not required

## Dependencies

- Operator will paste the skill body into the Cursor automation system prompt after merge (out of repo; not a build step)
- `make test` for layout regression only

## Challenges & Mitigations

- **Overshoot into nits:** Other hunt is a closed list; keep the do-not-publish / already-owned / neighborhood filters; no nit labels.
- **Opening line still wins because agents read the whole prompt at once:** retarget silence in the opening *and* restated at the approve gate (prompt-authoring: repeat a constraint where the agent might act).
- **Critical bar accidentally lowered:** do not edit the Critical definition or Q3 hunt; only split the confidence omit.
- **Paste includes frontmatter:** body after `---` is the payload; no paste-meta in the body.
- **Wrong packaging (ruleset / generated trees):** follow `pr-feedback-judge`; canonical `rules/` only.

## Pre-Mortem

- **The next automation run still approves with zero inlines because "silence is success" and "approve if nothing survives" remain the loudest lines:** already covered by Challenge "Opening line still wins" — retarget plus approve-gate restatement is the plan change, not an extra step.
- **We designed a new review philosophy instead of a surgical Other pass, and Critical quality regresses:** already covered by "Critical bar accidentally lowered"; Build copies the current prompt and applies the numbered edits; no greenfield rewrite.
- **The skill is treated as in-IDE-only and the automation keeps the old prompt:** out of scope (operator paste). Acceptance criterion 4 is "pasteable", not "already pasted".
- **L2 was too thin and Build invents the Other design:** this plan *is* the design. If Build wants a different hunt list or a quota, that is a rework, not improvisation.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
