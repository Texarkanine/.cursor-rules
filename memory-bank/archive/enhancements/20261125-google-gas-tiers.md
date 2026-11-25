---
task_id: google-gas-tiers
complexity_level: 2
date: 2026-11-25
status: completed
---

# TASK ARCHIVE: Place the Gemini 4 gas models and refresh BenchLM scores

## SUMMARY

The shipped catalog ranks on BenchLM's published overall. Carbon is S at 88.2, Neon is A at 91.8, Hydrogen is B at 78.8, and Argon stays A at 79.1. QA passed. After reflection, further hand-set tier moves on this branch were copied into the catalog.

## REQUIREMENTS

- The catalog score is the top-level BenchLM `displayScore`. When that overall is missing, the score is the equal-weight mean of whichever of the agentic, coding, and reasoning cells are present. The nested `scores.displayScore` stays unread.
- `gemini-4-carbon` is S, `gemini-4-neon` is A, `gemini-4-hydrogen` is B, and `gemini-4-argon` stays A.
- A score that sits well apart from its tier is reported. The tier stays where it was set.
- Finish the held work on PR 141.

## IMPLEMENTATION

`build_catalog` reads `_published_overall` before the category mean. `fill_mapping` treats a published overall as a scored item, which is how Neon and Hydrogen get rows while their category cells are null. Tiers were set in `assets/tiers.toml`, and refresh wrote `catalog.json` and `mapping.json`. The Mapping Overrides section of `references/refresh.md` already stated this score rule. The shipped rule is published overall, then the category mean, then an interim score on a hand-written mapping row.

Files: `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/assets/tiers.toml`, `rules/choose-verification-model/assets/catalog.json`, `rules/choose-verification-model/assets/mapping.json`, `tests/choose-verification-model/test_refresh.py`, `tests/choose-verification-model/test_shipped.py`.

After the reflection, `tiers.toml` moved `claude-opus-5-thinking`, `claude-sonnet-5-thinking`, `cursor-grok-4.6`, `cursor-grok-4.5`, and `gemini-3.7-flash` to `never`, and listed `cursor-grok-4.7` under A. The catalog picked up those five `never` rows. `cursor-grok-4.7` is absent from `catalog.json` and `mapping.json`, because `agent --list-models` does not list that spelling and refresh skips it. The score-rule sentences were removed from the `tiers.toml` header. The rule remains in `modelpool.py` and in Mapping Overrides.

## TESTING

Shipped `select` tests pin the gas tiers. An Opus author prints `gemini-4-carbon-low`. A Sol author prints Neon, and an Opus author stays Opus. A Terra author prints Hydrogen, and a Sol author stays Sol. Gemini 3.8 Flash stays Flash against Neon and against Hydrogen when the enabled list has no Carbon. A fast Sol author prints Neon with no `-fast` suffix. Refresh tests cover a published overall replacing the category mean, a null overall keeping the mean, the legacy nested field staying unread, and a published overall with null categories onboarding the row. At QA, `make test` reported 131 tests OK. QA passed with two advisories and no rework. The later catalog update added a lock that each catalog tier equals `tiers.toml`, and a Sol author is printed back when `cursor-grok-4.6` is the other candidate. PR 141's Choose Verification Model check succeeded.

## LESSONS LEARNED

A null `displayCategoryScores` block can sit beside a published overall. `fill_mapping` has to treat that overall as a match, or the model never gets a row.

The first plan refreshed from category means. Neon and Hydrogen have none, so preflight wrote `FAIL (blocking)` and build stopped on that line. The brief and `build_catalog` already used the published overall. The plan was rewritten and preflight was run again.

On the 2026-11-25 catalog, QA flagged Neon 19.6 above the A median, Hydrogen 12.5 above the B median, and Sonnet 5 thinking 11.0 below the A median. Each `score_source` was `benchlm`. The flags stayed review notes. Sonnet 5 thinking later moved to `never` by hand.

A refresh copies every `tiers.toml` edit into `catalog.json`. The gas build left the extra tier edits unstaged so a refresh would not publish them. They were committed afterward, then published into the catalog.

## PROCESS IMPROVEMENTS

Build keeps the first line of `memory-bank/active/.preflight-status` until a new preflight overwrites the file. Rewriting the plan leaves a `FAIL (blocking)` in force.

## TECHNICAL IMPROVEMENTS

Line 19 of `references/refresh.md` still summarizes the inputs as "BenchLM category scores". Mapping Overrides, from line 45, states the published-overall rule.

`cursor-grok-4.7` is tier A in `tiers.toml` and has no catalog row. Pick skips that spelling until `agent --list-models` lists it, or until a mapping row is written by hand.

A drift sidecar for score-versus-tier gaps was considered and left out. The session report covered this placement.

## NEXT STEPS

PR 141 is open and mergeable. The ruleset checks that ran succeeded, and CodeRabbit was skipped. Merge, then `chore(dev): ai-rizz sync`, when this should land on the remote the installed skill reads.
