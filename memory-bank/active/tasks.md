# Task: standing-contract-reconcile-guard

* Task ID: standing-contract-reconcile-guard
* Complexity: Level 2
* Type: simple enhancement

Tighten the persistent memory-bank update contract so agents catch new standing contracts on reconcile, without inviting changelog noise or a completeness hunt. Persistent MB files remain a deliberately incomplete high-level subset: omission is expected; pollution is forbidden.

## Test Plan (TDD)

### Behaviors to Verify

- [B1 standing-contract probe]: Agent completes a task that introduced a shared contract (typed errors, oracles, path layers) → compare path treats matching persistent file as materially incomplete and updates surgically
- [B2 asymmetric skip]: Agent completes narrative-only / no-contract work → skip remains correct; guardrails no longer claim under-updating is universally “safe”
- [B3 skip receipt]: Agent updates nothing → operator output includes one line per file `[productContext|systemPatterns|techContext]: skip — <reason>` citing the standing-contract probe
- [B4 systemPatterns contract carve-out]: Task ships a system-wide contract → guidance allows a briefing paragraph; task history / feature dump still forbidden
- [B5 techContext process change]: New required assert/signal convention → When to Update examples cover process/oracle changes; listing every helper still out of scope
- [B6 anti-noise invariant]: Doubt / incompleteness language still prefers skip over inventing content when the probe is “no”; no write-when-unsure default
- [B7 tripwire retention]: Phrases `factually wrong` and `materially incomplete` remain verbatim in all three guidance rules and `reconcile-persistent.md`
- [Edge: catalog escape hatch]: Agent rationalizes “don’t list every library/script” → techContext / systemPatterns contrast makes clear the *contract* is in scope, the catalog is not
- [Edge: productContext]: Ordinary task with no product-picture change → productContext skip receipt; no forced productContext edit from this enhancement

### Test Infrastructure

- Framework: none for prose/policy (repo `make test` covers ruleset symlinks + README links only)
- Test location: N/A — `always-tdd` out-of-scope for rule/instruction wording; prior similar task (`persistent-file-update-contract`) used review gates
- Conventions: QA acceptance checklist + `rg` self-checks (tripwire phrases, forbidden blanket phrases removed, no edits outside `rulesets/`)
- New test files: none (do not add change-detector content tests)

### Verification Steps (manual / review)

1. `rg` tripwire phrases in `rulesets/niko/niko/memory-bank/*.mdc` and `rulesets/niko/skills/niko/references/core/reconcile-persistent.md`
2. Confirm removed/replaced: `Skip confidently`, blanket `Under-updating is safe`, TL;DR `Skip silently`
3. Confirm presence: standing-contract probe, skip-receipt format, deliberate-incompleteness / anti-pollution posture
4. Style pass: `markdown-style.mdc` + `prompt-authoring` (workflow ordering explicit; no hollow “be careful”)
5. `make test` for unrelated regression on ruleset layout

## Implementation Plan

1. Rewrite `reconcile-persistent.md` procedure and guardrails
   - Files: `rulesets/niko/skills/niko/references/core/reconcile-persistent.md`
   - Changes:
     - TL;DR: drop “Skip silently”; state update-what-was-invalidated **or** what the standing-contract probe marks incomplete; skip with receipt otherwise
     - After step 3 Compare, add step **3b Standing-contract probe** (yes/no: shared contract across scripts/tests; would a future contributor invent a conflicting approach?). If yes → materially incomplete → surgical update. Catalog of helpers still out of scope; documenting the *contract* is in scope
     - Renumber / adjust steps 4–5 so skip path requires receipts; update path notes what changed
     - Guardrails: replace “Skip confidently / Under-updating is safe” with asymmetric risk — skip only when absence is harmless; under-updating safe for narrative/history; **not** safe for new standing contracts; when unsure which case, print skip reason (do not skip silently). Preserve: selective, surgical, system-level scope
     - Encode design color briefly: these files are a high-level incomplete subset by design; they must never contain content that does not belong
     - Clarify probe vs guidance Avoid lists: Avoid items govern *altitude/shape of content when writing*; a **yes** on the standing-contract probe still requires a surgical update — creation-time “if unsure, don’t document” must not short-circuit the probe

2. Soften `systemPatterns.mdc` When to Update
   - Files: `rulesets/niko/niko/memory-bank/systemPatterns.mdc`
   - Changes:
     - Replace “never the place to record what you just built” with: do not dump task history/changelog; **do** record a durable pattern when work established a system-wide contract a developer outside that task would need — even if it shipped in this task’s diff
     - Replace “When in doubt, don't: a missing pattern is cheap to add later…” with damage-test gating: if damage is not plausible, skip; if plausible, short briefing paragraph. Keep noise-is-worse framing (accumulated noise makes the file useless). Do **not** say write-when-unsure. Optionally note deliberate incompleteness (missing truths expected; wrong content forbidden)
     - Retain verbatim `factually wrong or materially incomplete` tripwire

3. Extend `techContext.mdc` When to Update examples
   - Files: `rulesets/niko/niko/memory-bank/techContext.mdc`
   - Changes:
     - After tool-swap style examples, add: update when the *process* changed — including a new required way to assert or signal failures — not only when a tool binary was replaced. Pointers to a shared contract module belong; a catalog of every script does not
     - Keep `When in doubt, don't` and tripwire phrase
     - Do not broaden into completeness pressure

4. Leave `productContext.mdc` untouched unless preflight finds tripwire/procedure inconsistency (skip receipts live in reconcile procedure, not in product When to Update)

5. Verification pass (no code implementation beyond prose)
   - Run review checklist from Test Plan; run `make test`

## Technology Validation

No new technology - validation not required

## Dependencies

- Canonical edit rule: `rulesets/` only (`agent-customization-locations`)
- Prior contract: tripwire duplication with guidance rules (`memory-bank/systemPatterns.md` documents the technique)
- Authority direction from 2026-07-09 archive: guidance rules must not cross-reference `reconcile-persistent.md` paths
- Style: `markdown-style.mdc`, `prompt-authoring`

## Challenges & Mitigations

- **Probe becomes a completeness hunt**: Phrase as two yes/no questions about *standing contracts* and *conflicting future approaches*; explicitly keep “listing every helper out of scope”; restate deliberate incompleteness in reconcile guardrails
- **Softened systemPatterns invites task dumps**: Pair contract carve-out with explicit ban on history/changelog; require damage-test pass for additions
- **Overshooting into write-when-unsure**: Never flip the default; only remove rationalizations that preferred false skip for contracts; keep “noise worse than omission” visible
- **Tripwire / wording drift across three rules + reconcile**: Edit surgically; `rg` verify tripwires unchanged in count/placement intent; no cross-refs from rules to reconcile

## Pre-Mortem

- **Plan failed because prose still let agents call contracts “implementation detail”**: Ensure techContext contrast and probe’s “documenting the *contract* is in scope” appear in the same mental path as the old escape hatch; already partly Challenge 1
- **Plan failed because agents treated skip receipts as license to invent skip reasons without running the probe**: Receipt instruction must require citing the standing-contract probe outcome, not only “not invalidated”
- **Plan failed because “deliberately incomplete” was read as “never update”**: Pair incompleteness with the probe as the exception path for standing contracts — incompleteness is about altitude/subset, not a ban on contract capture
- **Plan failed by editing generated `.cursor/` copies**: Implementation steps name `rulesets/` paths only; verification confirms no `.cursor/` / `.claude/` edits

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS WITH ADVISORY)
- [x] Build
- [x] QA (PASS)

## Build Checklist

- [x] Step 1: rewrite reconcile-persistent.md
- [x] Step 2: soften systemPatterns.mdc When to Update
- [x] Step 3: extend techContext.mdc When to Update
- [x] Step 4: productContext.mdc untouched
- [x] Step 5: verification (26/26 checks + make test)

## Preflight Amendments

- Added: probe outcome overrides creation-time Avoid “if unsure, don’t document” for the update decision (Avoid still governs altitude when writing)
