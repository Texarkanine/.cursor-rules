# Current Task: tdd-product-user-scope

**Complexity:** Level 1 (rework)

## Fix

**What broke:** The out-of-scope illustration `agent-facing prompts` named the audience, not the role. A later eval harness for product rules/skills would look like an “agent-facing prompt” and get skipped.

**Why:** #123 needed bootstrap (`AGENTS.md`, `CLAUDE.md`, copied init) out of TDD. That is not “all prompts.”

**What changed:** In `rules/always-tdd.mdc`, replaced that phrase with bootstrap illustrations. Left “rule and skill wording” in the prose/policy list. Did not edit niko-preflight.

**Files:** `rules/always-tdd.mdc`

**Tests:** None. Prose/policy; a wording assertion would be a change-detector. `make test` passed (symlink + README-link checks).

## QA Result

**Status:** PASS

**Findings:**
- No blocking findings. The sole canonical product edit removes the overly broad phrase and names repository bootstrap by role and examples.
- No KISS, DRY, YAGNI, completeness, regression, integrity, or documentation issue found. The existing rule-and-skill wording carve-out remains intact, and `niko-preflight` does not repeat the removed phrase.
- `make test` passed; its ruleset-symlink and README-link checks cover the applicable repository integrity gates. No document-content test was added because it would be a change-detector.
