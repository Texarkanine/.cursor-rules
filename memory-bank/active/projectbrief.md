# Project Brief

## User Story

As a Niko user (or someone installing Niko into a fresh repo), I want memory-bank initialization to install a thin root `AGENTS.md` + `CLAUDE.md` bootstrap pair when neither file exists, so that non-Niko harnesses can discover `memory-bank/` without requiring Niko workflows to be running.

## Use-Case(s)

### Use-Case 1: Fresh repo, no root bootstrap

Operator runs memory-bank init on a repo with neither `AGENTS.md` nor `CLAUDE.md`. After persistent files are created, both bootstrap files are written (thin map + `@AGENTS.md` shim).

### Use-Case 2: Existing bootstrap present

Operator runs memory-bank init where either or both of `AGENTS.md` / `CLAUDE.md` already exist. Init creates neither bootstrap file, does not modify existing ones, and may print a short advisory.

## Requirements

1. On the **uninitialized** memory-bank init path, after persistent files are created: if both root `AGENTS.md` and `CLAUDE.md` are absent, create both as specified in [issue #101](https://github.com/Texarkanine/.cursor-rules/issues/101).
2. If either file is present (regular file or symlink at repo root): create neither; do not follow links to edit through them.
3. Optional: when skipped, print a brief advisory (no migration-skill handoff).
4. Persistent-file authoring continues to scan existing AI-facing docs for anti-duplication (existing rule); that read-only behavior is unchanged.
5. Bootstrap content must stay as generic as practical so it survives rare memory-bank layout updates.

## Constraints

1. No append/edit/sidecar/migration/sync of existing bootstrap files in init (v1 non-goals in the issue).
2. Do not inline or `@`-import persistent file bodies into the GlobalPrompt.
3. Gate stays on the uninitialized branch — not re-litigated on every later `/niko` run.
4. Canonical edits under `rulesets/` (not generated `.cursor/` / untracked `.claude/` trees).
5. Prior broader coexistence creatives (agents-awareness / conflicts / sidecars) are superseded by this narrower write path.

## Acceptance Criteria

1. Fresh repo (no `AGENTS.md`, no `CLAUDE.md`): after memory-bank init, both files exist with the thin map + `@AGENTS.md` shim as specified in the issue.
2. If either file already exists at the repo root: init creates neither bootstrap file and does not modify the existing one(s).
3. Init does not append to, rewrite, or symlink-replace existing bootstrap files.
4. Persistent-file authoring still respects the existing anti-duplication scan against AI-facing docs.
5. Optional: when bootstrap is skipped, init reports a brief advisory (no skill handoff required for v1).
