# Active Context

## Current Task: verification-subagents-preflight-qa

**Phase:** BUILD - IN PROGRESS (rework pass 2) — waiting on operator for step-4 gated items

## What Was Done

- Stockroom archaeology: three seed sessions confirm preflight always fixed the same shape (Files/Changes-only steps / helpers-before-tests / verify-last) by adding per-unit test-first substeps
- Removed all `FAIL (TDD)` from `rulesets/niko/` (5 chart edges, skill Handle Results/Next Steps, status vocab, L2/L3 STOP prose); TDD encoding now routes as rearchitect → `/niko-plan`
- Plan templates: `- Tests first:` before `- Changes:` on L2/L3 with always-tdd escape hatch
- Cheap one-liners: L2 `/niko-archive`, progress summary, deferred bullets, Spawn-charge double-backticks
- Verify: `make test` green; mmdc OK; `rg` clean under `rulesets/niko/`

## Files Modified

- `rulesets/niko/skills/niko/references/level2/level2-workflow.md`
- `rulesets/niko/skills/niko/references/level3/level3-workflow.md`
- `rulesets/niko/README.md`
- `rulesets/niko/skills/niko-preflight/SKILL.md`
- `rulesets/niko/niko/memory-bank/active/preflight-status.mdc`
- `rulesets/niko/skills/niko/references/level2/level2-plan.md`
- `rulesets/niko/skills/niko/references/level3/level3-plan.md`
- `memory-bank/active/{tasks,activeContext,progress}.md`
- `memory-bank/active/reflection/reflection-verification-subagents-preflight-qa.md`

## Waiting On Operator

1. Clear `.qa-validation-status` before QA spawn — no such instruction in `rulesets/` today. Add a one-liner somewhere (where?), skip this pass, or other?
2. README long-chart QA split (`README.md` ~L126 combined `Level 2+ Fail` edge) — split fixable vs rearchitect (adds mermaid lines)? Do / skip / later?

## Next Step

Operator answers above → finish step 4 → BUILD COMPLETE → Spawn QA
