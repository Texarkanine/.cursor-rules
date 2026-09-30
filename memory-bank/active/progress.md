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
