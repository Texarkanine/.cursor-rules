# Project Brief

## User Story

As a Niko operator, I want TDD and preflight to treat only product-delivered or product-runtime behavior as executable, so that a plan that only rewires developer tooling or invokes a third-party CI action is not FAILed for missing tests.

## Use-Case(s)

### Lint-script wiring

A plan binds a root `lint` / `format` / `typecheck` script to a developer tool and adds that tool's config, with no product tests. Preflight TDD Plan Encoding must PASS. Incident: [a16n#74](https://github.com/Texarkanine/a16n/issues/74) / [PR #155](https://github.com/Texarkanine/a16n/pull/155).

### Invoke-only CI workflow

A plan adds a GitHub Actions workflow that only invokes a third-party action (the product is not itself an Action). Preflight TDD Plan Encoding must PASS. Incident: [SumMem#20](https://github.com/Texarkanine/SumMem/issues/20).

## Requirements

1. Fix the misread specified in [Texarkanine/.cursor-rules#116](https://github.com/Texarkanine/.cursor-rules/issues/116), including the comment that widens the same class to invoke-only CI/release workflows.
2. TDD remains in force for product CLIs, runtime configuration, and shipped workflows.
3. Preflight must not classify a unit as executable product behavior merely because a package manager or Actions runner executes a developer tool or someone else's action.

## Constraints

1. Precision and brevity are paramount. Find the smallest and best tweak that produces the outcome.
2. Steer the reader toward the intended scope. Do not erect N named guardrails for N past incidents; those incidents are examples of a class, not a checklist to encode. There are far more failure modes than we can list.
3. Edit canonical sources under `rulesets/` only. Do not edit generated `.cursor/` or `.claude/` copies.

## Acceptance Criteria

1. An L2 plan that only rewires lint/format/typecheck scripts and their config, with no new product tests, can PASS TDD Plan Encoding.
2. An L2 plan that only adds a CI/release workflow that invokes a third-party action, with no new product tests, can PASS TDD Plan Encoding.
3. A plan that adds or changes a product CLI, product-runtime config, or shipped workflow still owes tests for that behavior.
4. The shipped wording states a principle. It does not grow an exclusion list of tools, scripts, or workflow filenames.
