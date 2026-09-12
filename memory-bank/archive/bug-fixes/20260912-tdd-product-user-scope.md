---
task_id: tdd-product-user-scope
complexity_level: 2
date: 2026-09-12
status: completed
---

# TASK ARCHIVE: tdd-product-user-scope

## SUMMARY

Closed [issue #123](https://github.com/Texarkanine/.cursor-rules/issues/123): the #116 one-file bet failed. `always-tdd` now classifies by whether a user of this product can observe a break, and niko-preflight FAILs on that test rather than the plan’s “executable” label. A Level 1 rework dropped the too-broad illustration **agent-facing prompts**. Draft PR: [#124](https://github.com/Texarkanine/.cursor-rules/pull/124).

## REQUIREMENTS

- TDD and preflight judge only behavior a user of **this** product can observe breaking. Not #122.
- Repository bootstrap (`AGENTS.md`, `CLAUDE.md`, copied init text), vendored third-party tools, gitignore lines, etc. are out of scope even when an agent invokes them.
- Contract tests only for this product’s published contract; skip if semver already signals. “User” means a user of the product.
- Preflight must not classify executable because an agent or developer tool invokes a unit; inventing tests must not be the PASS path.
- Rework: do not name “prompts” as a species; keep “rule and skill wording” as the change-detector carve-out. If evals existed for product rules, those would be eval-first TDD; `AGENTS.md` still would not.

## IMPLEMENTATION

Canonical only: `rules/always-tdd.mdc` (symlink `rulesets/niko/always-tdd.mdc`); `rulesets/niko/skills/niko-preflight/SKILL.md`. No generated `.cursor/` / `.claude/` edits.

always-tdd in-scope is the consequence test only (no CLI/workflow list). Out-of-scope keeps the #95 prose/policy list and adds bootstrap by role and files. Contract-test sentence requires this product’s published contract and a user of this product; semver skip.

Preflight states judge actions, not a second definition: classify by product-user observability; strike non-product contract tests; FAIL uses What TDD Governs, not the plan label. Completeness must not demand tests because the plan labeled a unit executable. Judge Do Not Fix still allows only swap plus that strike.

Rework replaced `agent-facing prompts` with `Repository bootstrap (AGENTS.md, CLAUDE.md, copied init text, etc.)`.

## TESTING

No new automated tests (prose/policy; wording assertions would be change-detectors). `make test` passed. Original `/niko-preflight` PASS WITH ADVISORY; `/niko-qa` PASS. Rework QA PASS. Live proof is the next L2 plan that vendors a third-party tool and writes `AGENTS.md` — this task’s own plan was correctly prose/policy.

## LESSONS LEARNED

- Prefixing “the product's” does not survive a vendored CLI. An in-scope category list is the bug; the change-detector consequence test is the classifier.
- “Do not invent tests” loses when FAIL keys off the plan’s “executable” label. After a strike, the judge has to ask What TDD Governs.
- A one-file bet that preflight will inherit always-tdd fails when preflight has its own FAIL path. Echo classify / strike / FAIL, not a second copy of the definition.
- “Agent-facing prompts” names the audience, not the role. Product rules with evals would look like that phrase and get skipped. Name bootstrap files instead.

## PROCESS IMPROVEMENTS

Lock sentences in the L2 plan; treat issue-body “proposed wording” as a draft. QA then has something to diff. Operator marking proposed wording premature was correct.

## TECHNICAL IMPROVEMENTS

Foundational still means asking the consequence question in always-tdd Determine Scope before locating tests (#95 design debt). This task did not reshape the four steps. The split shipped is reference holds the test, workflow holds the judge actions.

## NEXT STEPS

- Merge [PR #124](https://github.com/Texarkanine/.cursor-rules/pull/124), then `chore(dev): ai-rizz sync`.
- Watch the next vendor-bootstrap `/niko-preflight`. That is live proof, not this task’s suite.
- [#122](https://github.com/Texarkanine/.cursor-rules/issues/122) remains a different bug (L4 vs L2/L3 altitude).
