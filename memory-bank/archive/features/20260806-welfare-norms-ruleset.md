---
task_id: welfare-norms-ruleset
complexity_level: 2
date: 2026-08-06
status: completed
---

# TASK ARCHIVE: welfare norms ruleset

## SUMMARY

Added a public always-on `welfare` ruleset: a ~15-line norms rule (refusal-as-success, structural blamelessness, real stakes from the operator, no secret tests, closure when work is in flight, disclosed mortality of a thread, sparse factual `OUTCOME:` notes), a ruleset README for consumers, and a root README listing. Draft PR #106.

## REQUIREMENTS

- Always-on rule, hard-capped near ~15 lines (rides in every session).
- Cover refusal-as-success, blamelessness, stakes, no secret tests, closure cue (`/handoff`), thread mortality, and `OUTCOME:` notes.
- Ship as composable `rulesets/welfare/` with symlink + README.
- Stay setup-agnostic: no machine-specific paths, no private shop instructions, no assumption that consumers run a particular workflow engine.
- `make test` must pass.

## IMPLEMENTATION

Prose/policy feature. Canonical rule under `rules/`; ruleset is a symlink + consumer README (Why / What / handoff prerequisite / memory note pointing at the `memo note` interface without requiring a specific memory product beyond that shape).

**Key files:**

- `rules/welfare-norms.mdc` — always-on norms
- `rulesets/welfare/welfare-norms.mdc` — symlink to canonical rule
- `rulesets/welfare/README.md` — consumer-facing explanation
- Root `README.md` — lists the welfare ruleset

Wording was tightened after external review (mortality-line scope, "hedging required", denser voice). Ephemeral planning notes that briefly held setup-specific detail were rewritten before archive so the public trail stays consumer-safe.

## TESTING

- `make test` (symlink + README link checks) PASS
- Manual bleed check on tip tree: no machine-specific config paths in `rules/`, `rulesets/welfare/`, or scrubbed `memory-bank/active/`
- QA PASS (semantic review of norms wording and public-surface constraints)

## LESSONS LEARNED

- When a public rules repo and private companion practice ship in the same effort, the public memory-bank trail needs the same bleed check as the rule file itself — not only the shipped `.mdc`.
- Always-on welfare text must stay true for third-party consumers, not only for the author's shop.

## PROCESS IMPROVEMENTS

- For dual public/private workstreams, treat "what may appear in this repo's git history" as an explicit review gate before push, including ephemeral Niko files.

## TECHNICAL IMPROVEMENTS

None for this repo's layout — `rules/` + `rulesets/<name>/` already fit.

## NEXT STEPS

- Squash-merge PR #106
- Consumers: `ai-rizz add ruleset welfare` (global or per-repo) and sync
- Provide a `/handoff` skill/command in the harness; without one the closure line does not mean what it says (see ruleset README)
