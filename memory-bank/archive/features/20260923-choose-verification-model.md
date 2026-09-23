---
task_id: choose-verification-model
complexity_level: 3
date: 2026-09-23
status: completed
---

# TASK ARCHIVE: choose-verification-model

## SUMMARY

Shipped an a-la-carte skill, `choose-verification-model`, that prints one verification-model slug from a hand-tiered catalog. `scripts/pick.py` ranks by BenchLM category mean, family, tier, and base output price. `scripts/refresh.py` rewrites scores and prices and keeps the hand-set tiers. Draft pull request: https://github.com/Texarkanine/.cursor-rules/pull/127

Nothing calls the picker yet. Niko QA and Preflight still say to prefer a smarter model from a different family. The spawn-line and README edits from the original build were restored to main after reflect, and the niko skill symlink was removed.

## REQUIREMENTS

The brief, after the post-reflect redesign:

1. Skill name `choose-verification-model`.
2. Executables under `scripts/`, catalog and mapping under `assets/`, refresh instructions under `references/`. Python 3.11, standard library only.
3. `pick.py` takes `--model` and `--reviewer-models`. Unknown slugs, and an author with a null tier or null score, exit 2 and name the slug. `tier: null` and `score: null` stay out of the pool.
4. Dense rank by score inside the tier, best at rank 1. The window is the same tier, a different family, from one rank below the author through the best. Pick one at random.
5. An empty window looks up exactly one tier: cheapest different family, then cheapest slug in that tier. When that search still leaves the pool empty, print the author. Do not look down a tier. Do not pull same-family peers in the current tier back into the window.
6. Score is the equal-weight mean of BenchLM agentic, coding, and reasoning that are present, from `https://benchlm.ai/data/models.json`. A trailing `-fast` is the same catalog row. Ranking uses the base output price. After the choice, append `-fast` only when the author slug ended in `-fast` and the chosen model has `has_fast`.
7. When all three categories are missing, refresh keeps an operator interim score. When any category is present, refresh replaces that interim. Neither stays `score: null`.
8. Cost is the base output price in USD per million tokens, from https://cursor.com/docs/models-and-pricing. `has_fast` is true when that page has a `{Name} (Fast)` row with a parsed price, or the model's notes mention a fast mode. The fast price is not stored.
9. Tiers are `C`, `B`, `A`, `S` from lowest to highest, assigned by hand. Refresh keeps an existing tier. A new slug gets `tier: null` and `WARNING: must set tier for …`.
10. Do not point Niko workflows or the Niko README at this script.

Acceptance: a printed slug satisfies the rank rule; refresh rewrites scores and costs and preserves tiers; Niko text stays as on main.

The original plan also required pointing nine QA and Preflight spawn lines and the README at `pick.py`, and shipping every slug in one tier named `general`, including `composer-2.5-fast` as its own row. The operator pulled the Niko wiring out of this branch and replaced the tier and fast rules above.

## IMPLEMENTATION

Layout, agentskills.io subdirs only. `SKILL.md` is the only file at the skill root. It is a short happy path, not Niko-specific: run `scripts/pick.py`, pass your slug and the enabled slugs, use the printed slug, and stop on a non-zero exit. Refresh lives in `references/refresh.md`.

| Path | Role |
| --- | --- |
| `rules/choose-verification-model/scripts/modelpool.py` | `select`, `build_catalog`, `canonical_slug`, `_with_speed`, `_has_fast` |
| `rules/choose-verification-model/scripts/pick.py` | CLI. Loads `assets/`. Exit 2, empty stdout, stderr names the slug |
| `rules/choose-verification-model/scripts/refresh.py` | Fetches BenchLM and the pricing page, writes `assets/catalog.json` |
| `rules/choose-verification-model/assets/catalog.json` | `tier_order` `["C","B","A","S"]` and per-slug score, tier, cost, `has_fast` |
| `rules/choose-verification-model/assets/mapping.json` | Family, pricing name, BenchLM slug. No shipped `output_multiplier` |
| `tests/choose-verification-model/test_*.py` | unittest. Imports `scripts/` and loads `assets/` |
| `Makefile` | `test` depends on `test-choose-verification-model` |
| `.github/workflows/rulesets-links.yml` | Job checks out, sets up Python 3.11, runs that Make target |
| `.gitignore` | `__pycache__/` |
| `memory-bank/techContext.md` | Testing Process names the unittest suite and points the CI Python version at the workflow |

`select` walks the window, then one tier up. Two sites return the author: there is no tier above, or the next tier is empty or every member there has a null price. `_with_speed` then appends `-fast` only for a fast author whose chosen model has `has_fast`. A printed fast spelling does not have to appear in `--reviewer-models`. Enabled roots make the fast spelling valid. Cost accounting never sees the fast price.

`build_catalog` still multiplies by `output_multiplier` when a mapping row sets one (default 1). Shipped rows omit the field because each slug already had its own pricing-page row. `Composer 2.5 (Fast)` is $15 against a $2.5 base; that price is not stored and is not a 2× multiplier.

Hand-assigned letters, including where they disagree with BenchLM. Sometimes-enabled slugs stay in the catalog and are passed in `--reviewer-models` only when enabled.

| Slug | Tier | Family | Sometimes |
| --- | --- | --- | --- |
| `claude-opus-5-5-medium` | S | claude | |
| `claude-fable-5-1-thinking-high` | S | claude | yes |
| `kimi-k3-high` | A | kimi | |
| `muse-spark-1.3-high` | A | muse | |
| `gemini-3.8-flash-high` | A | gemini | |
| `gpt-5.6-sol-medium` | A | gpt | yes |
| `grok-4.7-high` | A | grok | |
| `claude-sonnet-5-thinking-high` | B | claude | |
| `gpt-5.6-terra-medium` | B | gpt | |
| `composer-2.5` | C | composer | |
| `gpt-5.6-luna-medium` | C | gpt | yes |

Opus and Fable are both family `claude` in S, so their different-family window is empty and there is no tier above. They print themselves. That is the empty-pool case. Kimi stays A while Opus is S. Sonnet stays B while Grok is A.

No creative phase. The selection rule was specified before build. Preflight changed the score source from SWE-bench to the BenchLM category mean after live leaderboards had no rows for these models. An optional `--json` decision trace was advisory and was not built. A null-tier or null-score author exits 2; that came from a preflight advisory and was not in the original behavior list. `refresh.py` sends `User-Agent: choose-verification-model` because BenchLM returns 403 to urllib's default agent.

## TESTING

Tests live under `tests/choose-verification-model/` so an install of the skill does not copy them. `make test` runs the two ruleset layout checks and `python3 -m unittest discover -s tests/choose-verification-model -p 'test_*.py'`. At archive, that suite is 32 cases, green.

Covered pick behaviors include the rank window, one rank below, two ranks below excluded, same family excluded, tied dense rank, seed ties, null tier or score never printed, null cost skipped by the cheapest fallback and still eligible in the window, unknown author and reviewer exit 2, and a null-tier or null-score author exit 2. An empty window takes the cheapest different family one tier up, or the cheapest slug there when that tier is one family. A top-tier author with an empty window prints themselves across seeds. A non-top author prints themselves when the next tier is empty (Terra in B with only Composer in C enabled) or when the only model in the next tier has no price. A cheaper model in a lower tier is not chosen. Fast-author cases append `-fast` only when the chosen model has `has_fast`.

Refresh fixtures cover the three-category mean, a missing category, interim kept and then replaced, a shared BenchLM slug with independent prices, a Markdown-link model cell, Output found by header, tier preservation, a missing price warning, `output_multiplier` scaling a fixture price, and `has_fast` from a `(Fast)` row or from notes that mention fast mode, without storing the fast price. `test_shipped.py` checks that mapping slugs are catalog slugs, required keys exist, `tier_order` is `C B A S`, and families are non-empty. It does not lock numeric scores or per-slug letters, and it does not require `composer-2.5-fast` as its own row.

`/niko-preflight` ended `PASS WITH ADVISORY` after earlier failures: SWE-bench had no rows for these models (blocking; score source moved to BenchLM), PR CI did not run the new Make target, spawn lines hardcoded an interpreter, and a null-tier author was unspecified. Advisories left unused: the `--json` trace, and auto-seeding tiers from score quantiles.

`/niko-qa` on `claude-sonnet-5-thinking-high` was `FAIL (fixable)` because `techContext.md` still said `make test` was only layout checks. The Testing Process sentence was updated. The rerun on `gemini-3.8-flash-high` was `PASS`. That pass described the tree at reflect time: tier `general`, nine spawn lines rewritten, the niko symlink present, and an empty next tier raising `SelectionError`. All four of those were superseded after reflect. The empty next tier now returns the author and is tested.

`reuse lint` was compliant. No `REUSE.toml` edit. Default AGPL covers the new Python and JSON. `rules/**/*.md` covers `SKILL.md` as PPL-S.

## LESSONS LEARNED

- `https://benchlm.ai/data/models.json` returns 403 unless the request sets a User-Agent.
- Fast variants on the pricing page are their own rows, or a note that a fast mode exists. `Composer 2.5 (Fast)` is $15, not a multiplier on the $2.5 row. Ranking never uses that price.
- A trailing `-fast` is a parameter on the model root, like effort. Strip it before lookup. Append it after the base slug is chosen, and only when the author was the fast half and `has_fast` is set.
- An empty pool is a degenerate end of the existing search, not a new step that drops the family constraint inside the current tier. Returning the author is allowed only after the window and the one-tier-up cheapest passes have both found nothing.
- Letters are hand-assigned. A higher BenchLM score does not move a model into a higher tier.
- A plan that adds a Make target has to update `memory-bank/techContext.md` when that file states what `make test` runs. Preflight's "CI matches Make" check does not read that sentence.
- Tests must import the skill from `scripts/` and load JSON from `assets/`. Opening the pull request while `make test` still targeted the old paths left a red suite on the branch.
- Preflight's live fetch is what killed the SWE-bench score. The leaderboards had no rows for these models. The category mean on BenchLM did.

## PROCESS IMPROVEMENTS

- When a follow-up changes the contract after reflect, the memory-bank files from the build go stale while the code moves. The archive has to record the shipped rule, and say which QA sentences describe an earlier tree.
- "Return the author" and "drop the family constraint and keep searching the current tier" were treated as the same fix once. They are not. The second was reverted. A successor should not restore same-family peer selection inside the rank window.

## TECHNICAL IMPROVEMENTS

No standing architecture change beyond the skill. `productContext.md` and `systemPatterns.md` took no contract from this task. The optional `--json` decision trace was not built.

## NEXT STEPS

Draft pull request 127 is the delivery. Merge it when review is acceptable. Do not point Niko workflows, the Niko README, or a niko skill symlink at the picker unless a later task asks for that.
