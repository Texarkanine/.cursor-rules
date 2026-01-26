# Tasks

## Current Task: Fix Niko Command Paths

**Status:** Reflection Complete
**Complexity:** Level 1 (Bulk Find/Replace)
**Task ID:** niko-command-paths

### Description
Update `/niko/X` command invocations to `/X` after ai-rizz removed the niko namespace from command paths.

### Files to Update
- [x] `rulesets/niko/niko/visual-maps/van-mode-map.mdc`
- [x] `rulesets/niko/niko/visual-maps/qa-mode-map.mdc`
- [x] `rulesets/niko/niko/visual-maps/van_mode_split/van-mode-map.mdc`
- [x] `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-main.mdc`
- [x] `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/mode-transitions.mdc`
- [x] `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/reports.mdc`
- [x] `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/rule-calling-guide.mdc`
- [x] `rulesets/niko/niko/Core/memory-bank-paths.mdc`
- [x] `rules/wiggum-niko-coderabbit-pr.md`

### Status
- [x] Planning complete
- [x] Implementation complete
- [x] Verification complete

### Results
- 9 files updated via single `sed` command
- 0 remaining `/niko/X` command references in target scope

### Reflection
See `memory-bank/reflection/reflection-niko-command-paths.md`

---

## Previous Task: Wiggum-Niko CodeRabbit PR Integration

**Status:** Reflection Complete
**Complexity:** Level 1 (Quick Task)
**Task ID:** wiggum-niko-coderabbit

### Description
Create a Niko-integrated version of the wiggum-coderabbit-pr command that uses Niko's memory bank for tracking fixes and /reflect command before commit/push cycles.

### Status
- [x] Planning complete
- [x] Implementation complete
- [x] Verification complete
- [x] Reflection complete

### Deliverable
`rules/wiggum-niko-coderabbit-pr.md` (138 lines)

### Reflection
See `memory-bank/reflection/reflection-wiggum-niko-coderabbit.md`

---

## Previous Task: TDD Integration into Niko

**Status:** Reflection Complete
**Complexity:** Level 2 (Enhancement)
**Task ID:** tdd-integration

### Status
- [x] Planning complete
- [x] Implementation complete  
- [x] Reflection complete
- [ ] Archive complete

### Commits
- `5fe9de8` - fix(niko): Reinforce TDD in core
- `040a703` - fix(niko): reinforce TDD requirement in memory bank files
- `545074c` - feat(niko): Updated flowcharts and recipes to enforce TDD
- `3e72244` - chore: ready for pr review
