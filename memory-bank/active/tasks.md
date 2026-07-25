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

### Verification during Build

1. Implement scripts; run against current `rulesets/` (expect PASS — currently 16 symlinks, 3 READMEs, no dangling links observed).
2. Spot-check negative paths in a temp copy or with a deliberate local break+restore if needed (not committed).
3. Run `make test` end-to-end.
4. Confirm workflow YAML calls `make` targets only.

## Implementation Plan

TDD note: there is no unit-test framework. Each check script *is* the assertion over on-disk layout. Per unit: establish a failing Make entrypoint (RED), then implement the script until the current `rulesets/` tree passes (GREEN), then confirm a deliberate local breakage fails (not committed).

1. **Symlink check (RED → GREEN)**
   - Files: `Makefile` (target `test-symlinks`), `scripts/check-ruleset-symlinks.sh`
   - RED: Add `test-symlinks` Make target invoking the script path; run it and observe failure (missing/stub script).
   - GREEN: Implement POSIX `sh` script — resolve repo root; scan a rulesets root (default `rulesets/`, overridable by optional CLI arg for fixture/negative checks); find symlinks; fail and list any whose target does not exist (`test -e`); entry-point/`main` per shell-posix-style; executable bit. Re-run until exit 0 on current tree.
   - Negative confirm (uncommitted): run against a temp fixture tree with a dangling symlink; observe non-zero exit.

2. **README internal-link check (RED → GREEN)**
   - Files: `Makefile` (target `test-readme-links`), `scripts/check-ruleset-readme-links.sh`
   - RED: Add `test-readme-links` Make target; run and observe failure (missing/stub script).
   - GREEN: Implement — scan rulesets root (same default/optional-arg convention); find `README*`; extract Markdown inline links `[text](url)`; skip external/`mailto:`/`#…`; strip `#fragment`; resolve relative to the README’s directory; fail and report missing targets. Re-run until exit 0 on current tree.
   - Negative confirm (uncommitted): run against a temp fixture tree with a broken relative link; observe non-zero exit.

3. **Aggregate `make test`**
   - Files: `Makefile`
   - Changes: phony `test` depending on `test-symlinks` and `test-readme-links`; run `make test` and confirm exit 0 on current tree.

4. **GitHub Actions PR workflow (two separate checks)**
   - Files: `.github/workflows/rulesets-links.yml`
   - Changes: `on: pull_request`; two jobs (`ruleset-symlinks`, `ruleset-readme-links`) each checkout + matching Make target only (no duplicated check logic).

5. **Document local entrypoint**
   - Files: `README.md` (root)
   - Changes: short note that `make test` validates `rulesets/` symlinks and README internal links (same checks as PR CI).

6. **REUSE / licensing**
   - Files: `REUSE.toml` only if needed; else default `**/*` AGPL for Makefile/scripts/workflow
   - Changes: confirm scripts are not swept into LicenseRef-PPL-S overrides; leave AGPL.
## Technology Validation

No new technology - validation not required. Uses stock POSIX `sh`, `make`, and GitHub Actions `ubuntu-latest` (or equivalent) with checkout + `make`.

## Dependencies

- POSIX shell utilities (`find`, `test`, `sed`/`awk` as needed for link extraction)
- GNU or BSD `make` (simple phony targets; avoid GNU-only features)
- GitHub Actions (hosted runners)

## Challenges & Mitigations

- **Markdown link extraction edge cases** (images, nested parens, reference-style links): Scope to inline `[text](url)` as used in current READMEs; skip `http(s)://` and `mailto:`; document limitation if reference-style appears later
- **Directory symlinks** (e.g. skills dirs): `test -e` accepts directories; treat as valid targets
- **techContext “cross-platform PowerShell” note**: Operator chose POSIX scripts + Make; CI and intended local use are Unix/WSL. Mitigate by documenting `make test` for Unix-like environments; do not add PowerShell ports in this task
- **False positives on intentional external-only READMEs**: External links are ignored by design

## Pre-Mortem

- **Plan treated this as a unit-test suite and overbuilt shunit2/fixtures**: Already rejected by operator — stick to layout checks + Makefile only
- **CI duplicates script logic in YAML and drifts from local `make test`**: Plan requires jobs to call Make targets only (Challenge covered by Implementation step 4)
- **Link checker is too naive and breaks CI on common Markdown forms we already use**: Pre-scan shows only simple relative + external inline links; keep extractor minimal and ignore externals (Challenge 1)
- **`make test` name implies a broader suite later contributors overload**: Accept the name (operator requested); keep targets narrowly about rulesets link integrity for now

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA

## Preflight Amendments

- Encoded explicit RED→GREEN ordering per check unit (no unit framework; scripts are the layout assertions).
- Scripts accept optional rulesets-root argument (default `rulesets/`) so negative confirms use temp fixtures without mutating the real tree.
