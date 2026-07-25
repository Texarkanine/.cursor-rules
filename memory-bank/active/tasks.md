# Task: rulesets-link-ci

* Task ID: rulesets-link-ci
* Complexity: Level 2
* Type: Simple enhancement

Add POSIX check scripts + Makefile + GitHub Actions PR CI that verify (1) every symlink under `rulesets/` has an existing target and (2) every internal link in `rulesets/**/README*` has an existing target. No unit-test framework — the checks assert on-disk layout properties. `make test` is the shared local/CI entrypoint.

## Test Plan (TDD)

### Behaviors to Verify

- **Symlinks OK**: all current `rulesets/` symlinks resolve → `scripts/check-ruleset-symlinks.sh` exits 0
- **Broken symlink**: a dangling symlink under `rulesets/` → that script exits non-zero and reports the path
- **README links OK**: all current internal links in `rulesets/**/README*` resolve → `scripts/check-ruleset-readme-links.sh` exits 0
- **Broken internal link**: a README relative link to a missing path → that script exits non-zero and reports file + link
- **External links ignored**: `http(s)://`, `mailto:`, and bare `#anchor` links are not treated as filesystem targets
- **Fragments stripped**: `[x](./file.md#section)` checks `./file.md` existence only
- **`make test` aggregates**: runs both checks; fails if either fails
- **CI uses same entrypoint**: PR workflow jobs invoke Make targets (not duplicated inline logic)

### Test Infrastructure

- Framework: none (operator decision — layout property checks, not code unit tests)
- Test location: N/A — verification is running the check scripts / `make test` against the repo tree
- Conventions: POSIX `sh` per `rules/shell-posix-style.mdc`; Makefile as developer entrypoint
- New test files: none

## Implementation Plan

1. [x] **Symlink check (RED → GREEN)** — `Makefile` + `scripts/check-ruleset-symlinks.sh`
2. [x] **README internal-link check (RED → GREEN)** — `Makefile` + `scripts/check-ruleset-readme-links.sh`
3. [x] **Aggregate `make test`**
4. [x] **GitHub Actions PR workflow** — `.github/workflows/rulesets-links.yml` (two jobs)
5. [x] **Document local entrypoint** — root `README.md` Checks section
6. [x] **REUSE / licensing** — default AGPL via `**/*`; no override needed

## Technology Validation

No new technology - validation not required.

## Dependencies

- POSIX shell utilities (`find`, `test`, `awk`, `readlink`)
- `make`
- GitHub Actions

## Challenges & Mitigations

- **Markdown link extraction edge cases**: Scoped to inline `[text](url)`; skips externals
- **Directory symlinks**: `test -e` accepts directories
- **PowerShell note in techContext**: Documented Unix/`make test`; no PowerShell port

## Pre-Mortem

- Overbuilt unit suite: rejected by operator
- CI/Make drift: jobs call Make targets only
- Naive link checker: sufficient for current README forms

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA

## Preflight Amendments

- Encoded explicit RED→GREEN ordering per check unit (no unit framework; scripts are the layout assertions).
- Scripts accept optional rulesets-root argument (default `rulesets/`) so negative confirms use temp fixtures without mutating the real tree.
