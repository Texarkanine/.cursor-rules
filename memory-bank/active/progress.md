# Progress

Let consumers of `choose-verification-model` store the skill's assets in an XDG home directory, run refresh into that directory themselves, and keep local tier edits while later skill updates fill in models they never set. The Python scripts merge this mechanically. The agent-facing skill stays as it is.

**Complexity:** Level 3

## 2026-09-30 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed the restated intent with the operator
    - Classified the task as Level 3
    - Wrote the project brief, active context, and task stub
* Decisions made
    - Level 3: a complete feature across the refresh write path and the existing read path, with a merge contract to design first
    - Not Level 4: the change stays inside `choose-verification-model`
    - Not Level 2: the XDG layout and the shipped-versus-local merge are design work, not a change that can be coded immediately
* Insights
    - Catalog score conflicts are unlikely, because a score rarely changes after a model first lands
    - Tiers are the file consumers adjust
    - Agents must not see or perform the merge

## 2026-09-30 - CREATIVE - COMPLETE

* Work completed
    - Explored how shipped assets and a home directory combine
    - Recorded the decision in `memory-bank/active/creative/creative-asset-overlay.md`
* Decisions made
    - Pick merges on every run
    - A home `tiers.toml` is the local tier setting; the `tier` field in a home catalog does not freeze shipped tiers
    - Refresh from `rules/choose-verification-model` still rewrites the skill assets and ignores the home directory
    - Refresh from an install writes `catalog.json` and `mapping.json` under the XDG data directory and never writes `tiers.toml`
    - Home directory is `$XDG_DATA_HOME/choose-verification-model`, with the XDG default `~/.local/share`, and `%LOCALAPPDATA%` on Windows when the variable is unset
* Insights
    - The installed skill is a real copy at `~/.cursor/skills/ai-rizz/choose-verification-model`, so a parent named `rules` distinguishes the source tree
    - The five-new-models case only works if pick unions the files; a refresh snapshot alone hides a later skill update

## 2026-09-30 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 3 plan to `memory-bank/active/tasks.md`
    - Mapped tests onto `tests/choose-verification-model/` and the new `homeassets.py`
* Decisions made
    - Four implementation units: merge module, pick load, refresh write target, refresh.md
    - `SKILL.md` is not edited
    - `pick.main` and `refresh.main` grow optional `assets_dir` and `user_dir` keyword arguments for tests; a passed `dest` keeps today's refresh write
* Insights
    - `test_issue_129_command_exits_0_and_leaves_the_catalog` calls `pick.main` without an injected catalog, so it has to point `XDG_DATA_HOME` at an empty directory

## 2026-09-30 - PREFLIGHT - COMPLETE

* Work completed
    - Ran all seven Level 2/3 preflight checks against the codebase; none failed
    - Wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`
* Decisions made
    - Plan is build-ready as-is; both findings are advisory and do not gate the build
* Insights
    - `user_assets_dir` is stubbed with all-required parameters but called with none in unit 2; the build should give it None-sentinel defaults
    - A committed marker file beside `assets/` would be a more robust publish-mode signal than the parent-directory-name heuristic; recorded as a radical-innovation candidate for the operator to weigh

## 2026-09-30 - HANDOFF

* Work completed
    - Told the operator the build needs no design decision
    - Explained the marker-file advisory
* Decisions made
    - Keep the directory-name publish check. The operator did not ask to switch
* Insights
    - ai-rizz copies the `assets/` directory, so a marker inside it would make every install look like the source tree

## 2026-09-30 - BUILD - COMPLETE

* Work completed
    - Added `homeassets.py` and merged shipped assets with the XDG home directory on read
    - `pick.py` loads that merge unless both documents are injected
    - Install refresh writes the home catalog and mapping; source-tree refresh still rewrites the skill assets and ignores the home directory
    - Updated `references/refresh.md`. `SKILL.md` is unchanged
    - `make test` passed: 99 choose-verification-model tests, plus the symlink and README link checks
* Decisions made
    - `user_assets_dir` can be called with no arguments. Omitted values use `os.environ`, `Path.home()`, and `sys.platform`
    - When `pick.main` receives only one of `catalog` or `mapping`, the other document comes from the merge
    - The publish check stays the parent directory name `rules`
* Insights
    - QA was not started. `pick.py` exited 2 with `unknown slug: claude-sonnet-5-5-high`. That spelling is on the Task model list. The catalog has no `claude-sonnet-5-5` stem. The picker skill says not to guess a reviewer
