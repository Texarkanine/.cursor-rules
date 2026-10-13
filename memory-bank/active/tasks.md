# Task: Memory-bank init writes AGENTS.md only

* Task ID: mb-init-agents-only
* Complexity: Level 2
* Type: simple enhancement

On first (uninitialized) memory-bank init, Niko currently writes a root `AGENTS.md` + `CLAUDE.md` pair, and only when both are absent. Claude Code now reads repo-root `AGENTS.md` directly, so the `CLAUDE.md` shim (`@AGENTS.md`) is dead weight. Change init to write only the thin `AGENTS.md`, gated on root `AGENTS.md` alone (absent → create; present → leave alone and print the advisory). `CLAUDE.md` takes no part in the gate and is never created. Update the Niko README sentence that describes this.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior. Both edits are Niko skill/reference wording and README prose about repository bootstrap, which `always-tdd` places out of scope ("rule and skill wording"; "Repository bootstrap (AGENTS.md, CLAUDE.md, copied init text, etc.)"). A content assertion on these files would be a change-detector.

### Test Infrastructure

- Framework: `make test` — shell layout checks (`scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`) plus stdlib `unittest` under `tests/`
- Test location: `scripts/`, `tests/`
- Conventions: README internal links and ruleset symlinks are gated by the scripts; the unittest suite covers `choose-verification-model` only
- New test files: none

## Implementation Plan

### 1. Memory-bank init bootstrap section — prose/policy

- Files: `rulesets/niko/skills/niko/references/core/memory-bank-init.md`
- No tests: prose/policy artifact

1. Retitle `### Root bootstrap files` to `### Root bootstrap file`.
2. Replace the both-absent gate sentence with: install a thin root `AGENTS.md` only when root `AGENTS.md` is absent; keep the presence definition (regular file or symlink) and the no-edit-through-symlink rule; add one sentence that init never creates `CLAUDE.md` and an existing one does not affect this step.
3. Delete the four-row `AGENTS.md` × `CLAUDE.md` decision table (one condition left; prose carries it).
4. Rewrite the "When either file is already present" paragraph for `AGENTS.md` alone: create nothing; do not append to, rewrite, or symlink-replace it; same advisory content (found and left alone, `memory-bank/` is the preferred GlobalPrompt, cleaning house is the operator's choice, no migration skill).
5. Rewrite the next paragraph: drop "Do not create one file when the other already exists"; singularize "bootstrap files"/"templates" to `AGENTS.md`/"the template".
6. Leave the `AGENTS.md` template text unchanged.
7. Delete the `#### \`CLAUDE.md\` template` heading and its fenced `@AGENTS.md` block.
8. Change "(and, when applicable, the root bootstrap pair)" to "(and, when applicable, the root `AGENTS.md`)".
9. Leave line 28's read-only anti-duplication scan (which lists `CLAUDE.md`) unchanged.

### 2. Niko README note — prose/policy

- Files: `rulesets/niko/README.md`
- No tests: prose/policy artifact

1. Replace line 36 with: on first (uninitialized) memory-bank init, when there is no root `AGENTS.md`, Niko also writes a thin one that points harnesses at `memory-bank/`; if `AGENTS.md` already exists, init leaves it alone.

### 3. Verify

1. `grep -rn "CLAUDE" rulesets/` shows only the line-28 anti-duplication scan and the new step-2 "never creates `CLAUDE.md`" sentence.
2. Run `make test`; read the full output; all green.

## Technology Validation

No new technology - validation not required

## Dependencies

- None. Generated `.cursor/` and `.claude/` copies are re-synced later by the operator's `chore(dev): ai-rizz sync` after push (per `systemPatterns.md`); not part of this task.

## Challenges & Mitigations

- Agents know the `CLAUDE.md` → `@AGENTS.md` shim convention and may add it from habit: the explicit "init never creates `CLAUDE.md`" sentence closes that gap at the cost of one line.
- The injected `.claude/` copy in this repo will still describe the pair until the ai-rizz sync: read the canonical `rulesets/` file when reviewing, not the injected copy.

## Pre-Mortem

- Premise wrong (Claude Code does not read root `AGENTS.md`): this session loaded root `AGENTS.md` with no `CLAUDE.md` present, and the operator states it; accepted.
- A missed reference still describes the pair: the step-3 grep over `rulesets/` catches it; archives are historical records and stay as written.
- Repos with only a `CLAUDE.md` now get a new `AGENTS.md` that Claude Code also loads: intended by operator decision (gate on `AGENTS.md` alone); recorded in `activeContext.md`.

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

PASS. Reviewed `main...HEAD` against this plan, using the canonical `rulesets/` files.

- Completeness: Unit 1 steps 1–9 and Unit 2 step 1 are done as written. The `AGENTS.md` template text and the line-28 scan are unchanged. AC 1–5 are met; `make test` is green (symlinks, README links, 100 unittest).
- KISS/DRY/YAGNI: the change only removes text. Nothing new was added except the planned "never creates `CLAUDE.md`" sentence.
- Regression: no links point to the renamed `Root bootstrap file(s)` heading. Only `rulesets/` and `memory-bank/active/` changed; the generated `.cursor/` and `.claude/` trees wait for the ai-rizz sync.
- Integrity: no leftover scaffolding, placeholders, or stray pair wording in `rulesets/niko`.
- Documentation: the README line 36 is updated. No other Niko doc describes the pair.
- Advisory (non-blocking): "Do not follow symlinks to edit through them" now repeats the "do not … symlink-replace it" rule, because init never edits an existing `AGENTS.md`. Requirement 3 keeps it on purpose.
- Advisory (non-blocking): AC 6 (non-draft PR and `/handoff` note) is still open. No L2 phase step does it, so the orchestrating session must.
