---
task_id: rulesets-link-ci
complexity_level: 2
date: 2026-07-25
status: completed
---

# TASK ARCHIVE: rulesets-link-ci

## SUMMARY

Added POSIX check scripts, a Makefile (`make test`), and a two-job GitHub Actions PR workflow that verify (1) every symlink under `rulesets/` has an existing target and (2) every internal link in `rulesets/**/README*` resolves on disk. No unit-test framework — the checks assert on-disk layout properties and are the shared local/CI entrypoint.

## REQUIREMENTS

- Validate every symlink under `rulesets/` resolves to an existing target.
- Validate every internal link in README documents under `rulesets/` points at an existing path.
- Expose the two checks as separable entrypoints (distinct scripts / Make targets / CI jobs).
- Provide `make test` as the shared local aggregate entrypoint.
- Add a PR GitHub Actions workflow that invokes Make targets only (no duplicated check logic in YAML).
- Shell scripts follow `rules/shell-posix-style.mdc`.
- Ignore `http(s)://`, `mailto:`, and bare `#anchor` links; strip `#fragments` before path checks.

## IMPLEMENTATION

Greenfield tooling (no prior Makefile/scripts/test/`.github/workflows/` in this repo). Approach: two check scripts plus shared path helpers, Makefile targets for each check and for `make test`, and a two-job workflow calling those targets.

**Key files:**

- `scripts/check-ruleset-symlinks.sh` — walks `rulesets/` symlinks; fails on dangling targets
- `scripts/check-ruleset-readme-links.sh` — extracts inline Markdown links from `rulesets/**/README*`; fails on missing relative targets
- `scripts/rulesets-check-common.sh` — shared path-resolution helpers (extracted during QA)
- `Makefile` — per-check targets + aggregate `test`
- `.github/workflows/rulesets-links.yml` — two PR jobs, each invoking a Make target
- Root `README.md` — Checks section documenting `make test`
- `memory-bank/techContext.md` — Testing Process pointer to Make/scripts/workflow

**Notable details:** Scripts accept an optional rulesets-root argument (default `rulesets/`) so negative confirms use temp fixtures without mutating the live tree. README link extraction is POSIX `awk` over inline `[text](url)` only. Failure signaling from `find | while` subshells uses a temp failure file (not `pipefail`). REUSE defaults (`**/*` → AGPL) covered new files with no override.

## TESTING

No unit-test framework (operator decision). Verification:

- **RED→GREEN per check:** Make targets failed before scripts existed; passed after implementation.
- **Live tree:** `make test` exits 0 against current `rulesets/`.
- **Negative fixtures:** temp trees with a dangling symlink and a broken README link cause the respective scripts/`make test` to exit non-zero and report paths.
- **Preflight PASS** with amendments (explicit RED→GREEN ordering; optional root arg).
- **QA PASS** after trivial cleanup (shared helpers; clearer failure-file exit status).

## LESSONS LEARNED

- Without `pipefail`, communicating failure out of `find | while` subshells needs an out-of-band channel (temp file works; pipeline-tail status alone is easy to get wrong).
- “No test framework” still needs an explicit RED→GREEN story in the plan or preflight will (correctly) block on TDD encoding — layout-property scripts *are* the assertions.
- Make + two small scripts + two CI jobs is the natural shape; the main planning surprise was encoding TDD without shunit2.

## PROCESS IMPROVEMENTS

- When checks are disk-layout assertions rather than code unit tests, document the RED Make-target → GREEN script sequence up front so preflight does not stall.

## TECHNICAL IMPROVEMENTS

None beyond what shipped — shared helpers and temp-file failure signaling already landed in QA.

## NEXT STEPS

None.
