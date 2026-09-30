---
task_id: xdg-user-assets
date: 2026-09-30
complexity_level: 3
---

# Reflection: XDG user assets for choose-verification-model

## Summary

Pick merges the shipped catalog and mapping with `$XDG_DATA_HOME/choose-verification-model`. A home `tiers.toml` is the only local tier authority. Source-tree refresh still rewrites the skill assets. An install writes the home catalog and mapping and does not write `tiers.toml`. QA passed.

## Requirements vs Outcome

The four acceptance criteria in the brief are met: an install refresh writes the XDG directory, a model the consumer refreshed in early is kept, a local tier survives a later skill update while untouched models keep the shipped tier, and the agent-facing commands are unchanged. `SKILL.md` was not edited.

After the build, the operator asked for a source-tree refresh that places Claude Sonnet 5.5 at tier A. That is in the shipped catalog as `claude-sonnet-5-5`. It is not part of the XDG plan. The same refresh rewrote BenchLM scores. The unittest suite still passed.

## Plan Accuracy

The four units, the file list, and the test list matched the build. No step was reordered. The named challenges all showed up as written: the issue 129 test had to isolate `XDG_DATA_HOME`, refresh tests had to pass a temp `assets_dir`, `tomllib` stayed inside the tiers read, and the both-sides catalog test is what keeps a home catalog's `tier` from winning.

The only plan fix was the preflight advisory: `user_assets_dir` needed defaults so `pick` could call it with no arguments. That was a signature default, not a redesign. The surprise was outside the plan. The Task model list included `claude-sonnet-5-5-high`, the shipped catalog did not, and `pick.py` exited 2, so QA could not start until the catalog had that stem.

## Creative Phase Review

Read-time overlay held. A home catalog row wins on score, price, and `has_fast`, and the shipped tier is put back before the home tier list is applied. Source-tree refresh ignored the home directory, which is what made the later Sonnet refresh safe to run from this repo.

The parent-directory publish check held. The marker-file alternative did not. `ai-rizz` copies `assets/`, so a marker inside that directory would have made every install look like the source tree.

## Build & QA Observations

Each executable unit went red, then green. The pick test had to expect a slug the real catalog would not echo. An author the real catalog does not know is printed back unchanged, so an expected author slug would have passed before the merge existed.

QA passed and did not ask for a code change. It noted two advisories: `refresh.py` has small private readers that duplicate `homeassets.py`, and the consumer mapping union calls `merge_documents` with an empty catalog. Importing the private readers would be worse. A second mapping-only function would be a second merge.

## Cross-Phase Analysis

Preflight's signature advisory is the bug the build would have hit on the first no-argument call. The marker-file note was the right kind of alternative and the wrong place for the file. The operator had already explained the copy behavior, so build did not reopen it.

The picker failure was not a hole in the merge plan. The catalog had not been refreshed for a model that dropped the same day. The overlay is how a consumer adds that model without a skill update. The operator chose the maintainer path instead: refresh this tree and set tier A.

## Insights

### Technical

- A `tier` field written into `catalog.json` is a generated copy. The user's setting is `tiers.toml`. Letting the copy win would freeze tiers the user never edited.
- Anything placed under `assets/` is copied into installs. A publish marker cannot live there.

### Process

- When `pick.py` exits 2 on a slug that just appeared, the stem follows the sibling already in the catalog. `claude-opus-5-5` is the pattern for `claude-sonnet-5-5`. The maintainer fix is a `tiers.toml` line and a source-tree refresh, not dropping the slug to force a reviewer.
