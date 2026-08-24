# Project Brief

## User Story

As the operator of the TXRK9 PR Review Cursor automation, I want the review prompt (canonicalized here as a skill) to call out Other findings — things that are probably wrong but not show-stoppers — so that I still get Critical hits at the current quality, without a CodeRabbit-style nit flood, and I can paste the same text into the automation system prompt.

## Use-Case(s)

### Use-Case 1

A Cursor automation runs on an opened or updated pull request, with this prompt as its system prompt. It posts one review via the Comment on pull request tool: indicative 🦮 What's In This PR, inline findings, approve when the cull is empty after a real Other pass.

### Use-Case 2

An agent in a checkout that has this skill invoked reviews a PR to the same bar (same cascade, same posting shape). The automation does not load skills; this copy is the paste source.

## Requirements

1. Land the current TXRK9 PR Review prompt in this repository as a skill under `rules/` (canonical source; no requirement to wrap it in a ruleset).
2. Keep the product: advisory reviewer; 1–4 cascade with stop-at-first-no; Critical vs Other; inline when a line exists; 🦮 What's In This PR body; cap of 6 with Critical uncapped; early abort as Critical body-only; request review by `Texarkanine` when Critical and the PR was not opened by that user.
3. Raise sensitivity on Other: findings that are probably wrong, in scope, and not nits, even when the happy path still works.
4. Do not weaken the Critical bar. Do not add nit / thought / suggestion labels. Do not invent work to look thorough. Silence remains a valid all-clear after Other has been hunted and culled.
5. The skill body must be pasteable into a Cursor automation system prompt: self-contained, no sibling-prompt cross-references.

## Constraints

1. Automations do not load skills; in-repo skill is the source of truth the operator copies.
2. Neighbors of this artifact: `rules/pr-feedback-judge/` is second-order (comments in, dispositions out). Do not merge the two.
3. `rules/` and `rulesets/` are the canonical trees. Do not edit `.cursor/` or `.claude/`.
4. Skill wording is prose/policy under always-tdd: no change-detector tests that lock prompt text.

## Acceptance Criteria

1. A skill directory exists under `rules/` whose `SKILL.md` is the TXRK9 PR Review prompt, including the posting contract and the cascade.
2. Other is a duty after Q2 and Q3 succeed, not only a leftover class that the cull deletes by default.
3. Critical findings, body shape, cap, and the no-nits / neighborhood / already-owned filters still match the current prompt's intent.
4. An agent can paste `SKILL.md` body (or the whole file, if frontmatter is harmless) into the Cursor automation system prompt without needing other files from this repo.
