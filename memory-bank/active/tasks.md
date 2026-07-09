# Task: Persistent-File Rule Update Contract

* Task ID: persistent-file-update-contract
* Complexity: Level 2
* Type: rule enhancement (prose-only)

Amend the three persistent memory-bank guidance rules at their canonical sources under `rulesets/niko/niko/memory-bank/` so any agent that picks up the glob-attached rule understands both what belongs in the file (altitude: durable, system-wide, briefing-level) and when it may be updated (only when completed work invalidated content; surgical fixes; when in doubt, don't). Design pre-resolved in `memory-bank/active/creative/creative-persistent-file-update-contract.md`.

## Test Plan (TDD)

### Applicability

All deliverables are prose (`.mdc` rules). No executable code and no Markdown test runner exists in this repo (same situation as the md-style-and-prompt-authoring task). Verification is acceptance checks in QA plus `rg` self-checks for the grep-able invariants. Flagged honestly rather than fabricating tests.

### Behaviors to Verify

- `systemPatterns.mdc` "Avoid" list → gains a fourth item covering subsystem deep-dives, containing the altitude test (would a developer working on an *unrelated* part of the system do damage without knowing this?).
- `systemPatterns.mdc` "How to Create" → the bare append invitation ("can be appended to later as actual work reveals patterns") is gone; the brevity sentence defers to the update contract.
- `systemPatterns.mdc` → gains a "When to Update" section between "How to Create" and "Format" stating: default is no action; this file never records what you just built/fixed/learned; update only on invalidation; surgical fix only; when in doubt, don't.
- `productContext.mdc` → gains a small "Avoid" subsection (implementation vocabulary in use cases; feature-by-feature accretion) and a proportionate "When to Update" section.
- `techContext.mdc` → gains a proportionate "When to Update" section (existing Avoid list already covers what-belongs adequately).
- Grep tripwire → the exact phrases "factually wrong" and "materially incomplete" appear in all three rules and already exist in `reconcile-persistent.md` (deliberate, grep-verifiable duplication).
- Cross-reference check → `rg` finds no mention of `reconcile-persistent`, `.cursor/skills`, or any skill path inside the three rules.
- Section ordering → "When to Update" sits between "How to Create" and "Format", matching the ephemeral rules (`activeContext.mdc`, `tasks.mdc`) convention.
- Style compliance → no hard-wrapped prose in added content; headings short, portable, no parentheticals; absolutes reserved.
- No edits under `.cursor/` or `.claude/` (canonical sources only).

### Test Infrastructure

- Framework: none (prose artifacts). Verification is manual QA against the behaviors above plus `rg` self-checks.
- New test files: none.

## Implementation Plan

1. Amend `systemPatterns.mdc` what-belongs definition.
   - Files: `rulesets/niko/niko/memory-bank/systemPatterns.mdc`
   - Changes: rephrase the "Err on the side of brevity..." sentence to defer to the update contract; add Avoid item 4 (subsystem deep-dives + altitude test).
2. Add "When to Update" to `systemPatterns.mdc`.
   - Files: `rulesets/niko/niko/memory-bank/systemPatterns.mdc`
   - Changes: new H2 section between "How to Create" (after its "Avoid" H3) and "Format", per the creative doc draft: read-often/write-rarely framing, no-task-history rule, invalidation-only trigger with tripwire phrases, surgical scope, skip-confidently close.
3. Amend `productContext.mdc`.
   - Files: `rulesets/niko/niko/memory-bank/productContext.mdc`
   - Changes: add "Avoid" H3 under "How to Create" (implementation vocabulary; feature accretion); add "When to Update" H2 (product-not-work framing, invalidation examples: new constituency, retired use case, changed constraint).
4. Amend `techContext.mdc`.
   - Files: `rulesets/niko/niko/memory-bank/techContext.mdc`
   - Changes: add "When to Update" H2 after the existing "Avoid" H3, before "Format" (invalidation examples: build tool replaced, test process changed, environment step added; new content must be durable pointers).
5. Self-check pass.
   - Files: all three rules
   - Changes: none expected — run `rg` checks (tripwire phrases present in all three + reconcile-persistent; no skill-path references; no edits outside `rulesets/`), read lints, verify markdown-style compliance.

## Technology Validation

No new technology - validation not required.

## Dependencies

- None. All design decisions pre-resolved in the creative document; no external state required.

## Challenges & Mitigations

- Tripwire phrases must match `reconcile-persistent.md` exactly ("factually wrong", "materially incomplete"): copy the phrases verbatim from that file, verify with `rg` in step 5.
- The rules must stay reference-kind (prompt-authoring): no workflow steps, no personality; the "When to Update" section states a condition and a scope, not a procedure. Review in step 5.
- Risk of over-writing (this task is itself prose about not over-writing): keep each addition to one short section; the creative doc drafts are the ceiling, not the floor.

## Preflight Findings

- [INFO] Rule consumers verified: only `memory-bank-init.md` (creation flow) and `reconcile-persistent.md` (reconciliation flow) load these rules; both edits are additive and break neither. Tripwire phrases currently exist only in `reconcile-persistent.md` — copying them verbatim creates the intended grep tripwire.
- [INFO] Canonical rules and `.cursor/rules/shared/niko/memory-bank/` copies are in sync today; edits will make them drift until the ai-rizz / a16n regeneration flow runs (deployment follow-up, out of scope per brief).
- [ADVISORY] Option D from the creative doc (a one-line maintenance notice in the generated `.md` templates) is the only lever that reaches rule-less harnesses (the `AGENTS.md` pseudo-memory-bank case). Out of brief scope; operator follow-on.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight — PASS (2 info, 1 advisory)
- [ ] Build
- [ ] QA
