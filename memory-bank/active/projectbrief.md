# Project Brief: welfare norms ruleset

## User Story

Agents and operators share standing welfare norms: refusal is success, blamelessness, real stakes, no secret tests, closure when work is in flight, disclosed mortality of a thread, and sparse factual outcome notes.

## Requirements

1. Add an always-on rule (~15 lines hard cap) covering those norms
2. Ship it as a composable `welfare` ruleset with a short README
3. List the ruleset in the repository README
4. Keep the rule harness-agnostic: no machine-specific paths, no private shop instructions, no assumptions about which workflow system a consumer uses

## Constraints

- One concern per commit, unsigned commits
- Feature branch off `main`
- `make test` must pass
