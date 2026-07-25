# Project Brief

## User Story

As a ruleset author, I want CI and a local `make test` entrypoint that verify symlink targets and README internal links under `rulesets/` so that broken references are caught before (and during) pull request review.

## Use-Case(s)

### Use-Case 1

A developer breaks a symlink under `rulesets/` (or points it at a missing path). Running `make test` locally reports the failure; opening a PR causes GitHub Actions to fail the same check.

### Use-Case 2

A developer updates a README under `rulesets/` with an internal link to a path that does not exist. `make test` and the PR CI job both fail that check.

## Requirements

1. Validate that every symlink under `rulesets/` resolves to a target that exists.
2. Validate that every internal link in README documents under `rulesets/` points at a target that exists.
3. Expose the checks as two separate checks (distinct jobs and/or distinct script entrypoints).
4. Provide a local entrypoint via Makefile (`make test`) that runs the same checks developers and CI use.
5. Add a GitHub Actions workflow that runs on pull requests and invokes that same entrypoint (no duplicated check logic in YAML).
6. If implemented with shell scripts, follow `rules/shell-posix-style.mdc`.

## Constraints

1. Prefer Makefile + scripts under a scripts directory over embedding check logic only in GitHub Actions.
2. Shell scripts must adhere to `rules/shell-posix-style.mdc`.
3. Scope is the `rulesets/` directory tree (not the whole repo), unless planning finds a stronger existing convention.

## Acceptance Criteria

1. `make test` runs both checks and exits non-zero if either fails.
2. A PR CI workflow runs on pull requests and fails when either check fails.
3. The two checks are separable (can be run/reported independently).
4. Broken symlink targets and broken README internal links under `rulesets/` are detected.
5. Shell script implementations comply with `rules/shell-posix-style.mdc`.
