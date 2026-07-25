---
task_id: description-rules-and-commands-to-skills
date: 2026-07-25
complexity_level: 3
---

# Reflection: description-rules-and-commands-to-skills

## Summary

Migrated ten agent-selected description rules through a16n IR into `rules/<name>/SKILL.md`, hand-wrapped the two remaining commands as ManualPrompt skills, and rewired ruleset symlinks/docs. Verify harness and staged discover both green; QA passed with one trivial cleanup.

## Requirements vs Outcome

Delivered the full acceptance set: no residual SimpleAgentSkill `.mdc` or top-level command `.md` under `rules/`; skills landed in ai-rizz authoring layout; GlobalPrompts/FileRules preserved; rulesets resolve; liberal git checkpoints. Did not refresh generated `.cursor/`/`.claude/` trees (explicitly out of scope). No requirements dropped or silently reinterpreted.

## Plan Accuracy

Selective staging + IR round-trip worked exactly as planned; the FileRule rename hazard and `@`-skip on commands were real and correctly mitigated. The eight ruleset symlink rewrites matched the preflight inventory. Main plan deviation: one batched commit for all ten description conversions instead of per-name commits — acceptable because the a16n step itself was atomic. Verify harness earned its keep by catching the dangling-symlink false negative early.

## Creative Phase Review

No creative phase documents. Open questions were resolved in plan/preflight (hand-wrap commands; selective staging). That was the right call — the remaining ambiguity was operational, not design.

## Build & QA Observations

Build was mechanical and fast once staging was scripted. QA found only an unused local in the verifier. The interesting failure mode was `Path.exists()` treating dangling ruleset symlinks as already gone — fixed before ruleset rewrite completed.

## Cross-Phase Analysis

Preflight’s explicit meta skill-link naming amendment prevented a build-time naming guess. Operator rejection of `@`-neutralize during plan avoided a wrong creative/build path. Fail-first verify made the mid-migration B6 gap visible instead of discovering broken rulesets after “done.”

## Insights

### Technical
- After deleting symlink targets, Python `Path.exists()` is false for dangling links; migration verifiers that assert “stale symlink removed” must use `is_symlink() or exists()` (lexists semantics).
- a16n discover JSON uses `type` (kebab-case) and ManualPrompt items expose `promptName`, not `name`.

### Process
- For content migrations where the converter only understands a foreign layout, a temp stage + harvest plan plus an end-state verifier is enough — creative phase is optional when the only unknowns are tool classification quirks already settled by dry-run.
