# Current Task: issue-72-progress-mdc-load

**Task ID:** issue-72-progress-mdc-load
**Complexity:** Level 1
**Branch:** `issue-72`
**Issue:** [#72](https://github.com/Texarkanine/.cursor-rules/issues/72) (mechanical-alignment portion only)

## Scope Recap

Mechanical alignment from issue #72: require explicit `Load:` of `progress.mdc` before any write to `progress.md` that happens at **creation** or **phase-transition** time. Deeper-fix options (IN-PROGRESS grain; `nk-save` scoping) intentionally deferred.

## Work Checklist

- [x] Locate: the two write sites in scope — `complexity-analysis.md` Step 4 (creation) and each `levelN-workflow.md` Phase Mappings step 1 (phase-transition update).
- [x] "Test" (ruleset change, no automated harness): the rule-file `Load:` pattern should match prior art in `memory-bank-init.md`; each rewritten step must keep the load and the write as separate imperatives so a skimming agent cannot miss the load.
- [x] Fix: edit canonical files under `rulesets/niko/**`.
    - [x] `rulesets/niko/skills/niko/references/core/complexity-analysis.md` — add `Load:` line + globs-insufficiency rationale to Step 4; defer Format details to the rule (do not restate).
    - [x] `rulesets/niko/skills/niko/references/level1/level1-workflow.md` — split phase-transition step into `1. Load:` + `2. Update`; renumber downstream steps.
    - [x] `rulesets/niko/skills/niko/references/level2/level2-workflow.md` — same split + renumber.
    - [x] `rulesets/niko/skills/niko/references/level3/level3-workflow.md` — same split + renumber.
    - [x] `rulesets/niko/skills/niko/references/level4/level4-workflow.md` — same split + renumber.
- [x] Verify: diff review — only in-scope files touched; no `SKILL.md` Step 3b edits; no `.cursor/**` / `.claude/**` hand-edits.
- [x] Commit on branch `issue-72` with accurate, scoped message (`b0c0eb9`).
- [ ] QA: operator review of the five-file diff for pattern fidelity (no grain drift, numbered steps clean, rationale intact).
- [ ] Push branch `issue-72` and open PR (operator-driven).

## Session Mis-steps (preserved for record)

- First pass by the prior agent combined Load + Update into one sentence per workflow step, and additionally modified `SKILL.md` Step 3b (out of scope). Shipped as commit `0fbb324`.
- Reviewed, `git reset --hard HEAD~1` on unpushed commit `0fbb324`, redone cleanly as `b0c0eb9`.
- `/niko` Step 7 (Classify Complexity) and all memory-bank ephemeral writes were skipped by the prior agent; this file and its siblings are a retroactive reconstruction based on session context.
