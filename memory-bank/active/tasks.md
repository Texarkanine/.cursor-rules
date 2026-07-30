# Task: mb-init-agents-bootstrap

* Task ID: mb-init-agents-bootstrap
* Complexity: Level 2
* Type: simple enhancement

On the uninitialized memory-bank init path, after persistent files are created, install a thin root `AGENTS.md` + `CLAUDE.md` pair only when both are absent; otherwise skip (optional advisory). Authoritative spec: [issue #101](https://github.com/Texarkanine/.cursor-rules/issues/101).

## Test Plan (TDD)

### Behaviors to Verify

Deliverable is skill/procedure prose under the `always-tdd` carve-out (user-facing policy). No automated content assertions — those would be change-detectors. Verify by build/QA checklist against the issue ACs:

- Both absent → init creates thin `AGENTS.md` map + `CLAUDE.md` with `@AGENTS.md`
- Either present (file or symlink) → creates neither; no modify/append/rewrite/symlink-replace
- Skipped case → optional brief advisory; no migration-skill handoff
- Anti-duplication scan before persistent-file authoring remains
- Gate stays on uninitialized branch only (not every `/niko`)
- Template stays generic (paths/roles, not project-specific facts)

### Test Infrastructure

- Framework: none for prose; layout gates via `make test` (`scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`)
- Test location: N/A for new behavior tests
- Conventions: prior L2 prose tasks (e.g. tdd-prose-carveout) — QA semantic review + `make test` regression
- New test files: none

## Implementation Plan

1. Extend uninitialized section of canonical init procedure
   - Files: `rulesets/niko/skills/niko/references/core/memory-bank-init.md`
   - Changes: After persistent files are created (before "partially initialized / ready for new work"), add bootstrap gate: if both root `AGENTS.md` and `CLAUDE.md` are absent → write the pair from the in-doc template; else create neither, do not follow symlinks to edit, optionally print advisory. Keep anti-duplication scan unchanged. Do not touch Partially Initialized ephemeral-file guidance.
2. Embed install templates in that same file
   - Files: `rulesets/niko/skills/niko/references/core/memory-bank-init.md`
   - Changes: Fenced copy-targets for (a) generic thin `AGENTS.md` (memory-bank pointer, one-line purpose each for the three persistent files, archive layout, brief `active/` awareness, conditional load; paths in backticks) and (b) one-line `CLAUDE.md` = `@AGENTS.md`. No `@`-import of persistent bodies.
3. Document the behavior for operators
   - Files: `rulesets/niko/README.md`
   - Changes: Short note under Persistent Files that fresh (uninitialized) init also installs the thin root pair when both are absent; point at the better-than-AGENTS.md framing already in the README — do not restate the full decision table.
4. Regression gate
   - Files: none
   - Changes: Run `make test`; fix any link/symlink breakage introduced by README edits.
5. Do not edit generated trees; do not create root bootstrap files in this repo as part of build (gate is uninitialized-only; this repo is already partially initialized)

## Technology Validation

No new technology - validation not required

## Dependencies

- Issue #101 decision table and non-goals (authoritative)
- `always-tdd` prose carve-out
- Canonical edit rule: `rulesets/` only (generated `.cursor/` / `.claude/` lag; sync is a separate push-then-ai-rizz chore)

## Challenges & Mitigations

- Template too specific → drifts on layout changes: Keep AGENTS.md generic (roles + backtick paths); issue already flags this as a non-goal for sync.
- Agent edits through a symlink: Presence = path exists; instruct "do not follow links to edit through them."
- Temptation to also install on this repo / every `/niko`: Explicit non-step; gate remains uninitialized-only.
- README over-documents coexistence cases: One short paragraph; full matrix stays in init procedure / issue.

## Pre-Mortem

- Plan failed because build treated this as a coexistence/migration product (append/sidecar): Scope is write-path both-absent only; Challenge already covers temptation — QA checks non-goals absent from the diff.
- Plan failed because AGENTS.md template encoded this repo's specifics or `@`-imported persistent bodies: Step 2 lists required thin content; QA checklist rejects inlining.
- Plan failed because someone added change-detector tests on template wording: Test plan explicitly forbids; verify via AC checklist + `make test` only.
- Plan failed because edits landed in `.cursor/` / `.claude/` and drifted from canonical: Step 5 + systemPatterns; touch `rulesets/` only.

## Preflight Findings

- PASS with advisory: this repo has neither root bootstrap file today, but the uninitialized-only gate means shipping the procedure will not install them here. One-time dogfood after merge (manual create of the thin pair, or a future migration path) is operator choice — out of this brief.
- No plan amendments.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA
