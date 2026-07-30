---
task_id: mb-init-agents-bootstrap
complexity_level: 2
date: 2026-07-30
status: completed
---

# TASK ARCHIVE: mb-init-agents-bootstrap

## SUMMARY

Extended uninitialized memory-bank init so that, after persistent files are created, a thin root `AGENTS.md` + `CLAUDE.md` pair is installed only when both are absent; otherwise skip with an optional advisory. Delivered per [issue #101](https://github.com/Texarkanine/.cursor-rules/issues/101). Shipped on branch `niko-init` (PR #102 draft).

## REQUIREMENTS

- Uninitialized init path only: after persistents exist, if both root bootstrap files are absent → create thin `AGENTS.md` map + `CLAUDE.md` with `@AGENTS.md`.
- If either path is present (file or symlink): create neither; do not follow links to edit through them.
- Optional brief advisory when skipped; no migration-skill handoff.
- Anti-duplication scan before persistent-file authoring unchanged.
- Templates stay generic (paths/roles); no `@`-import of persistent bodies; no append/sidecar/migration/sync of existing bootstrap files.
- Canonical edits under `rulesets/` only.

## IMPLEMENTATION

**Design of record:** issue #101 decision table (prior agents-awareness / conflicts creatives superseded; no creative phase).

**Files modified:**

- `rulesets/niko/skills/niko/references/core/memory-bank-init.md` — bootstrap gate after persistent creation; fenced copy-exact templates for thin `AGENTS.md` and one-line `CLAUDE.md`.
- `rulesets/niko/README.md` — short Persistent Files note that fresh init installs the pair when both are absent.
- `rulesets/niko/skills/niko/SKILL.md` — related wording tweak on the init path (same branch).

Did not dogfood-create root bootstrap files in this repo (gate is uninitialized-only; this repo is already partially initialized). Generated `.cursor/` / `.claude/` trees not touched.

## TESTING

No new automated tests — skill/procedure prose under the `always-tdd` carve-out; content assertions would be change-detectors.

- `make test` green (symlink + README-link gates).
- Preflight PASS (advisory: this repo still lacks root bootstrap files; install left as operator choice).
- QA PASS: ACs covered; non-goals absent; uninitialized-only placement correct; no generated-tree or dogfood-install drift.

## LESSONS LEARNED

- When an issue already encodes the decision table and non-goals, skipping creative and treating the issue as design of record keeps L2 lean without losing fidelity.
- A both-absent write on the uninitialized path is the right foundational shape; coexistence/migration belongs in a separate product if ever.

## PROCESS IMPROVEMENTS

- Prefer issue-as-design-of-record for narrow write-path briefs that already supersede broader exploratory creatives — load the issue, not the superseded creative docs.

## TECHNICAL IMPROVEMENTS

- Open follow-up (out of this brief): whether AGENTS/CLAUDE templates should live under `assets/` rather than inline in `memory-bank-init.md`, since `/niko` Step 0 may load init when persistents are missing and templates inflate that rare path's context. Not required for #101 ACs.
- CodeRabbit on PR #102 asked for lstat/O_EXCL/atomic pair create — wrong layer for agent prose; both-absent gate is intentional; dismiss.

## NEXT STEPS

None for this task. Operator may one-time dogfood the thin pair on this repo after merge, or leave it for a future migration path.
