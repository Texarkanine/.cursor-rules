# Project Brief

## User Story

As the Niko maintainer, I want memory-bank init to stop bootstrapping a root `CLAUDE.md`, so that Niko only writes the one root file every harness now reads: `AGENTS.md`. Claude Code reads repo-root `AGENTS.md` directly, so the `@AGENTS.md` shim is no longer needed.

## Use-Case(s)

### Use-Case 1

Fresh repo with no root `AGENTS.md`: first memory-bank init writes the thin `AGENTS.md` index and nothing else at the root. This holds whether or not a root `CLAUDE.md` exists.

### Use-Case 2

Repo that already has a root `AGENTS.md` (file or symlink): init creates nothing, does not touch it, and prints the short advisory.

## Requirements

1. In `rulesets/niko/skills/niko/references/core/memory-bank-init.md`, remove the `CLAUDE.md` template and all "pair" wording; init installs only `AGENTS.md`.
2. The bootstrap gate keys on root `AGENTS.md` alone: create it when absent, skip when present. `CLAUDE.md` plays no part in the gate (operator decision, 2026-10-12).
3. Keep the existing presence semantics (regular file or symlink), the no-edit-through-symlink rule, the no-append/rewrite rule, and the advisory when skipped.
4. Update the matching sentence in `rulesets/niko/README.md`.

## Constraints

1. Canonical edits under `rulesets/` only; never edit generated `.cursor/` or `.claude/` trees.
2. Leave the read-only anti-duplication scan (which lists `CLAUDE.md` among existing AI-facing docs) unchanged.
3. Keep the `AGENTS.md` template text unchanged.

## Acceptance Criteria

1. `memory-bank-init.md` no longer instructs creating `CLAUDE.md` and has no `CLAUDE.md` template.
2. Init creates `AGENTS.md` when, and only when, root `AGENTS.md` is absent.
3. When `AGENTS.md` is present, init creates nothing, modifies nothing, and prints the advisory.
4. README describes the AGENTS.md-only behavior.
5. `make test` passes.
6. A non-draft PR is open; a `/handoff` note is left.
