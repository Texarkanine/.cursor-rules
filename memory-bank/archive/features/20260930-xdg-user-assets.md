---
task_id: xdg-user-assets
complexity_level: 3
date: 2026-09-30
status: completed
---

# TASK ARCHIVE: XDG user assets for choose-verification-model

## SUMMARY

Consumers of `choose-verification-model` can keep a catalog, a mapping, and a tier list in an XDG data directory. `pick.py` merges that directory with the shipped assets on every run. A home `tiers.toml` is the only local tier authority. Refresh from `rules/choose-verification-model` still rewrites the skill assets and ignores the home directory. Refresh from an install writes `catalog.json` and `mapping.json` under the home directory and never writes `tiers.toml`. The agent-facing commands are unchanged.

After the feature was built, the operator had a source-tree refresh add Claude Sonnet 5.5 (`claude-sonnet-5-5`) at tier A, and then had catalog scores stored to two decimal places (`72.6333...` is `72.63`).

## REQUIREMENTS

The user story: a consumer wants the skill's assets in an XDG home directory, and wants to run refresh as soon as a new model drops, so they can set tiers locally while later skill updates still fill in models they never touched.

Use cases:

- Run refresh before the upstream skill lists a new model. The new model lands in the home directory.
- Put a tier list next to that catalog and change tiers.
- A later skill update supplies shipped defaults for models the consumer never set. The model they set keeps their setting.

Requirements:

1. Assets can live in an XDG home directory.
2. `scripts/refresh.py` writes that same directory.
3. A consumer can run refresh, not only the maintainer.
4. A refresh before the upstream skill has updated pulls in a newly dropped model.
5. The consumer can assign and adjust tiers in that home directory.
6. Local settings take precedence.
7. Models the consumer did not set take the defaults from a later skill update.
8. The Python scripts do the merge. Agents do not.
9. The tier list sits next to the catalog.

Constraints: the merge is invisible to agents, `SKILL.md` does not change, and tiers are what consumers adjust. A later score change is unlikely to matter.

Acceptance criteria: an install refresh writes the XDG directory; a model present only because the consumer refreshed early is in that directory; a local tier survives a later skill update while untouched models take shipped defaults; agents still invoke the skill the same way.

## IMPLEMENTATION

New module `rules/choose-verification-model/scripts/homeassets.py`. `pick.py` and `refresh.py` call it. It does not select a reviewer and it does not open the network.

Directory: `$XDG_DATA_HOME/choose-verification-model` when that variable is set and non-empty, on every OS. Otherwise `~/.local/share/choose-verification-model`. On Windows (`nt`) with the variable unset, `%LOCALAPPDATA%/choose-verification-model`. `user_assets_dir()` takes no required arguments. Omitted values use `os.environ`, `Path.home()`, and `sys.platform`.

Publish check: the skill directory is named `choose-verification-model` and its parent is named `rules`. That is the source tree. Any other parent, including the installed copy under `ai-rizz`, is a consumer.

Merge, in `merge_documents`:

- Mapping rows are the union. A home row replaces the shipped row for the same stem.
- Catalog rows are the union. For a stem on both sides, the home row supplies score, price, `has_fast`, and the rest of the fields, then the shipped `tier` is put back. A stem on only one side keeps that row, including its tier.
- `tier_order` comes from the shipped catalog.
- A home `tiers.toml` is applied with `previous_from_tiers` and `model_key`. The first listing wins. Stems it does not name keep the tier from the catalog step. Warnings from that parse are discarded.
- Missing home files contribute nothing. Invalid JSON raises. `tomllib` is imported only inside the tiers read, so `import pick` still works on Python older than 3.11 when that file is absent.

`pick.main` loads the merge unless both `catalog` and `mapping` are passed. If only one is passed, the other comes from the merge. Optional `assets_dir` and `user_dir` exist for tests.

`refresh.main`: a passed `dest` keeps the previous read and write. With `dest` omitted, a source tree reads and writes that tree's `assets/` and does not read the home directory. Any other install loads the shipped mapping and tiers, unions the home mapping, overlays the home tier lists onto the shipped lists, runs the existing fill and catalog build, creates the home directory, and writes `catalog.json` and `mapping.json` there. It does not write `tiers.toml` and it does not modify the skill assets.

`references/refresh.md` states the split. The `python3` and `py -3` commands are unchanged. `SKILL.md` was not edited.

Creative decision, selected: read-time overlay, write target by tree. It is the only option that shows shipped defaults on the next pick, keeps personal tiers out of the committed catalog, and leaves both command lines unchanged. The tradeoff: a home catalog row wins on score, price, and `has_fast`, so a later shipped score stays hidden behind that row. The brief accepts that. Tiers are exempt.

Options rejected:

- Home is the only write, and publish is a flag. No-arg refresh could no longer update the committed catalog.
- Snapshot, then prefer the home catalog when it exists. A skill update's new models stay invisible until the user runs refresh again. A home `tiers.toml` that replaced the shipped tier list entirely was also rejected: models absent from the home file would lose their shipped tiers.

The publish check keys off the parent directory name `rules`, not a marker file. A marker inside `assets/` would ship with every install, because `ai-rizz` copies that directory. The live install is a real copy at `~/.cursor/skills/ai-rizz/choose-verification-model`.

Operator requests after the planned build, on the same branch:

- Source-tree refresh, with `claude-sonnet-5-5` listed under tier A in `assets/tiers.toml`. The stem matches `claude-opus-5-5`. The listing slug `claude-sonnet-5-5-high` is that model. Refresh matched BenchLM and the pricing page and also rewrote the other scores. Sonnet 5 without thinking stays `never`.
- Catalog scores are stored to two decimal places. `build_catalog` rounds the BenchLM mean and an interim score with `round(score, 2)`. `72.63333333333333` is `72.63`.

QA advisories, left as they are: `refresh.py` has small private readers that duplicate the ones in `homeassets.py`, and the consumer mapping union calls `merge_documents` with an empty catalog. Importing the private readers would be worse. A second mapping-only function would be a second merge.

## TESTING

Executable units were written test-first. Each went red on an empty implementation, then green.

`tests/choose-verification-model/test_homeassets.py` covers the XDG path, the source-tree check, the mapping union, both-sides and one-side catalog rows, the home tier list (including an effort spelling and first-listing wins), `tier_order`, a missing home directory, invalid JSON, a `pick.main` run whose home tier changes the printed slug, a consumer refresh (home files written, skill catalog untouched, mapping union, home tier on the written catalog), and a source-tree refresh that ignores a disagreeing home tier.

`tests/choose-verification-model/test_shipped.py` points `XDG_DATA_HOME` at an empty directory for the issue 129 command, so a developer's home tier list cannot change that slug. The pick test expects a slug the real catalog would not echo: an unknown author is printed back unchanged, so expecting the author slug would have passed before the merge existed.

`tests/choose-verification-model/test_refresh.py` asserts that the mean of 70, 74, and 73.9 is stored as 72.63.

Preflight result was `PASS WITH ADVISORY`. QA result was `PASS`. QA re-ran the choose-verification-model suite: 99 tests, OK, and did not ask for a code change. After the two-decimal change the same suite was 100 tests, OK. `make test` (that suite plus the symlink and README link checks) passed on the overlay before the Sonnet refresh.

## LESSONS LEARNED

- A `tier` field written into `catalog.json` is a generated copy. The user's setting is `tiers.toml`. Letting the copy win would freeze tiers the user never edited.
- Anything placed under `assets/` is copied into installs. A publish marker cannot live there.
- When `pick.py` exits 2 on a slug that just appeared, the stem follows the sibling already in the catalog. `claude-opus-5-5` is the pattern for `claude-sonnet-5-5`. The maintainer fix is a `tiers.toml` line and a source-tree refresh, not dropping the slug to force a reviewer.
- The overlay is how a consumer adds that model without waiting for a skill update. The operator chose the maintainer path for Sonnet 5.5 and put it in the shipped catalog.

## PROCESS IMPROVEMENTS

Preflight's signature advisory was the bug the build would have hit on the first no-argument call to `user_assets_dir`. The marker-file note was the right kind of alternative and the wrong place for the file. The operator had already explained that `ai-rizz` copies `assets/`, so build did not reopen it.

The picker failure was not a hole in the merge plan. The shipped catalog had not been refreshed for a model that dropped the same day.

## TECHNICAL IMPROVEMENTS

None left open. The two QA notes are deliberate: duplicated three-line readers, and one merge function used for a mapping-only union.

## NEXT STEPS

Draft pull request 131 is open for this branch and was not merged by this archive. The in-repo `.cursor/` tree still lags the canonical `rules/` change until a later `chore(dev): ai-rizz sync`, which cannot run in the same task because `ai-rizz` reads the git remote.
