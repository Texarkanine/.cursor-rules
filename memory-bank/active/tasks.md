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

1. **Add symlink check script**
   - Files: `scripts/check-ruleset-symlinks.sh`
   - Changes: POSIX `sh`; resolve repo root; find symlinks under `rulesets/`; fail and list any whose target does not exist (`test -e`); entry-point protection / `main` pattern per shell-posix-style + shell-tdd sourcing hygiene where applicable; executable bit

2. **Add README internal-link check script**
   - Files: `scripts/check-ruleset-readme-links.sh`
   - Changes: find `README*` under `rulesets/`; extract Markdown inline links `[text](url)`; skip external/`mailto:`/`#…`; strip `#fragment`; resolve relative to the README’s directory; fail and report missing targets

3. **Wire Makefile**
   - Files: `Makefile`
   - Changes: phony targets `test`, `test-symlinks`, `test-readme-links`; `test` depends on both check targets; each check target invokes the corresponding script

4. **Add GitHub Actions PR workflow (two separate checks)**
   - Files: `.github/workflows/rulesets-links.yml` (name flexible; keep clear)
   - Changes: `on: pull_request`; two jobs (e.g. `ruleset-symlinks`, `ruleset-readme-links`) each checking out the repo and running the matching `make` target — separate status checks on the PR

5. **Document local entrypoint**
   - Files: `README.md` (root)
   - Changes: short note that `make test` validates `rulesets/` symlinks and README internal links (same checks as PR CI)

6. **REUSE / licensing**
   - Files: `REUSE.toml` only if new paths need overrides; otherwise default `**/*` AGPL applies to Makefile/scripts/workflow
   - Changes: confirm no prompt-license override incorrectly covers scripts; leave as AGPL unless planning finds a conflict

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
- [ ] Preflight
- [ ] Build
- [ ] QA
