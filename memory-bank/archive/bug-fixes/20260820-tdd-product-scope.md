---
task_id: tdd-product-scope
complexity_level: 2
date: 2026-08-20
status: completed
---

# TASK ARCHIVE: tdd-product-scope

## SUMMARY

Fixed the always-tdd scope misread in [issue #116](https://github.com/Texarkanine/.cursor-rules/issues/116): TDD was attaching to whatever a package manager or Actions runner executes (lint-script wiring on [a16n#74](https://github.com/Texarkanine/a16n/issues/74); invoke-only Release Please on [SumMem#20](https://github.com/Texarkanine/SumMem/issues/20)). Replaced the in-scope paragraph in `rules/always-tdd.mdc` so it names the product's executable behavior and deletes "If something executes it." Did not add an exclusion list and did not edit niko-preflight. Draft PR: [#117](https://github.com/Texarkanine/.cursor-rules/pull/117).

## REQUIREMENTS

- TDD governs executable behavior the product delivers or uses at runtime; product CLIs, runtime config, and shipped workflows stay in scope.
- A plan that only rewires lint/format/typecheck (or only invokes a third-party CI action) must be able to PASS TDD Plan Encoding without product tests.
- Smallest steering tweak. No named guardrails for the two incidents. Canonical edit only (`rules/always-tdd.mdc`; `rulesets/niko/always-tdd.mdc` is a symlink). No generated `.cursor/` / `.claude/` edits.

## IMPLEMENTATION

One sentence. Before: `In scope: executable behavior — code, schemas, parsers, CLIs, and any configuration or workflow the product runs, etc. If something executes it, it is in scope, whatever its file extension.` After: `In scope: the product's executable behavior — code, schemas, parsers, CLIs, and any configuration or workflow it runs, etc. File extension does not decide.`

Out-of-scope and change-detector paragraphs unchanged. niko-preflight unchanged: it already points at always-tdd for the test-first process, and once a unit is not executable it already passes without tests. A second definition would have been the exclusion-list move.

## TESTING

No new automated tests (prose/policy). `make test` passed (ruleset symlink + README link checks). `/niko-preflight` PASS WITH ADVISORY. `/niko-qa` PASS. Both advisories: the em-dash list still contains the tokens the incidents quoted (`CLIs, and any configuration or workflow it runs`); generated `.cursor/rules/shared/always-tdd.mdc` still has the old sentence until `chore(dev): ai-rizz sync`. Live proof is the next lint-only or invoke-only-CI preflight, not this task's own plan.

## LESSONS LEARNED

- The two incidents were one misread ("if something executes it" = any runner), not two rules to add.
- Category lists get relabeled (lint is a CLI; `release-please.yaml` is a workflow). Prefixing "the product's" may not change that read.
- The change-detector paragraph already steers by failure mode. If TDD scope had used the same test — would a user of the product observe the break? — lint wiring and invoke-only CI would never have looked in-scope.
- Preflight names always-tdd as the home of the process, not explicitly as the classifier of "executable." The one-file bet depends on the next judge inheriting What TDD Governs.

## PROCESS IMPROVEMENTS

L2 locks the sentence in the plan, so Preflight/QA can only advise on a bet already taken. That is correct for the workflow. Do not promote a one-file wording bug to L3 just to get a creative phase.

## TECHNICAL IMPROVEMENTS

Optionally replace the in-scope category list with the same consequence test the change-detector paragraph already uses. Do not add that in a follow-up unless the one-file bet fails.

## NEXT STEPS

- Merge [PR #117](https://github.com/Texarkanine/.cursor-rules/pull/117), then `chore(dev): ai-rizz sync`.
- Watch the next lint-only or invoke-only-CI `/niko-preflight`. If it still FAILs TDD encoding, the useful second sentence is a pointer (classify executable using What TDD Governs), not an exclusion list.
