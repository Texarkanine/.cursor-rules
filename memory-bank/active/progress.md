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
