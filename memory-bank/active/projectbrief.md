# Project Brief

## User Story

As an operator running Niko on a consumer repository, I want TDD and preflight to judge only behavior a user of **this** product can observe breaking, so that vendoring a third-party tool and writing agent bootstrap files does not invent “contract tests” or FAIL for missing TDD steps.

## Use-Case(s)

### Use-Case 1

An L2 plan copies a third-party script (for example `.summem/summem`), pastes its init prompt into `AGENTS.md`, adds the Niko `# Agent context` template, writes `CLAUDE.md` as `@AGENTS.md`, and gitignores a cache path. Nothing the product ships to consumers changes. The plan is prose/policy plus file copy. No new tests. Preflight does not FAIL TDD Plan Encoding and does not leave file-presence / heading-order / gitignore-line tests scheduled.

### Use-Case 2

A plan that changes shipped CSS/JS, a product CLI, or runtime config the product’s users observe still follows TDD. Those units remain executable.

### Use-Case 3

A lockstep assertion is scheduled only when it is the published contract of **this** product. If semantic versioning already signals that expectation, the test is not added. “User” in the contract-test sentence means a user of the product, not the next agent or future contributor.

## Requirements

1. Close [issue #123](https://github.com/Texarkanine/.cursor-rules/issues/123): the #116 one-file bet failed; this is not #122.
2. `rules/always-tdd.mdc` What TDD Governs must classify by whether a user of the product can observe the break, not by the in-scope category list (`code, schemas, parsers, CLIs, and any configuration or workflow it runs`) or by “something an agent or developer tool invokes.”
3. Repository bootstrap, vendored third-party tools, agent-facing prompts, gitignore lines, etc. are out of TDD scope.
4. The contract-test exemption applies only to **this** product’s published contract. Semver already signaling the change means do not add the test.
5. Echo the same classifier in `niko-preflight` TDD Plan Encoding: do not classify a unit as executable because an agent or a developer tool invokes it; strike scheduled “contract tests” that do not protect a product user. Inventing tests must not be the PASS path.
6. Keep TDD for shipped product behavior (CSS/JS, product CLIs, runtime config).

## Constraints

1. The issue body’s “Proposed wording” is premature solutioning ([comment](https://github.com/Texarkanine/.cursor-rules/issues/123#issuecomment-5647217454)). Plan chooses wording; do not lock that paragraph.
2. Any counterexample list must include `, etc.`
3. Out of scope: [#122](https://github.com/Texarkanine/.cursor-rules/issues/122) (L4 vs L2/L3 altitude).
4. Canonical sources only (`rules/always-tdd.mdc`; `rulesets/niko/always-tdd.mdc` is a symlink; `rulesets/niko/skills/niko-preflight/SKILL.md`). No in-task edits to generated `.cursor/` or `.claude/` trees.
5. This work is rule/skill wording (prose/policy). Do not invent change-detector tests for the new sentences.

## Acceptance Criteria

1. An L2 plan that vendors a third-party script and adds `AGENTS.md` / `CLAUDE.md` with no new product tests is the same PASS path as “no new executable behavior”: not FAIL for missing TDD steps, and not PASS after inventing file-presence / heading-order / gitignore “contract tests.”
2. Preflight TDD Plan Encoding does not treat agent- or developer-tool invocation as sufficient to classify a unit executable.
3. Preflight strikes scheduled “contract tests” that do not protect a user of this product.
4. Product-observable executable behavior remains in TDD scope.
5. Canonical files carry the change; generated trees wait for a later `chore(dev): ai-rizz sync`.

## Rework

Operator (2026-09-12): **agent-facing prompts** is too broad. `AGENTS.md` / `CLAUDE.md` / copied init text are repository bootstrap and correctly owe no tests. Rules and skills in this repo are the product: today there is no eval framework, so they still owe no tests (change-detectors remain banned). If evals existed that go red when rule text makes agents misbehave, changing rules would be eval-first TDD; changing `AGENTS.md` still would not.

Drop **agent-facing prompts**. Keep the bootstrap role explicit (`AGENTS.md`, `CLAUDE.md`, copied init text, etc.). Do not remove “rule and skill wording” from the prose/policy list. Leave niko-preflight’s invocation classifier as-is unless it repeats the bad phrase.
