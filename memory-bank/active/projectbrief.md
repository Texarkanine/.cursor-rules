# Project Brief

## User Story

As a maintainer of the POSIX shell style guide, I want incorrect `$?`-after-command and unsafe positional-arg restore examples fixed (and validated as correct) so the guide is consistent with its own `set -eu` mandate and does not teach unsafe patterns.

## Use-Case(s)

### Use-Case 1

An agent or human following `shell-posix-style.mdc` copies an error-handling example; under `set -eu` the post-command `$?` branch is unreachable, so they need inline `if` / `if !` examples instead.

### Use-Case 2

Someone uses the "positional parameters as a list" pattern and needs a safe approach that does not round-trip via `"$*"` / unquoted `set --`.

## Requirements

1. Fix post-command `$?` checks in the guide that are unreachable under `set -eu` (cp, sort/`pd_status`, find/`file_list` examples) per [issue #82](https://github.com/Texarkanine/.cursor-rules/issues/82).
2. Fix the positional-parameter list example to avoid unsafe `"$*"` / unquoted restore; prefer wrapping temporary `set --` work in a function.
3. Validate that the requested changes are correct and worth applying before/as part of the edit.
4. Edit the canonical source (`rulesets/shell/shell-posix-style.mdc`) and keep the mirrored `rules/shell-posix-style.mdc` in sync if that is how this repo mirrors shell rules.

## Constraints

1. Do not rewrite intentional `expr` examples to `$((…))` (explicitly out of scope in #82).
2. Prefer clean-break documentation fixes; no backwards-compatibility obligation for incorrect examples.

## Acceptance Criteria

1. No remaining examples in the targeted sections use unreachable post-command `$?` checks under `set -eu`.
2. The positional-parameter list example no longer uses `"$*"` / unquoted `set --` restore.
3. Changes are validated as shell-correct (errexit-compatible error handling; safe arg handling).
4. Canonical and mirrored copies stay consistent.
