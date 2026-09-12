# Active Context

## Current Task: l4-preflight-altitude
**Phase:** BUILD - COMPLETE

## What Was Done
- Split `/niko-preflight`: SKILL.md dispatches on `progress.md` Complexity; `references/default-preflight.md` holds L2/L3 checks (word `milestone` removed from TDD units); `references/l4-preflight.md` holds W4 altitude checks.
- Folded the Preflight advisory: `default-preflight.md` FAILs blocking if Complexity is Level 4.
- W4 format in `milestones.mdc` and `level4-plan.md` (L-estimates off checkbox lines). Classification reads the W4 row. README + `level4-workflow.md` state L4 altitude. Spawn lines unchanged. `.cursor/` not edited.
- `make test` passed (symlink + README link checks).

## Next Step
- QA review.
