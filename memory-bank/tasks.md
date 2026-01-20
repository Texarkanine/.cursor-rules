# Tasks

## Active Task: Archive Inlining Fix

**Task ID**: archive-inlining-fix
**Complexity**: Level 2
**Status**: IN PROGRESS

### Problem
Archive templates instruct users to "link to" ephemeral files (reflection, creative phase docs), but `/archive clear` deletes these files, creating broken links in archives.

### Solution
Update archive templates to **inline** relevant content from ephemeral files instead of linking to them.

### Files to Update

#### Primary (rulesets/niko/)
- [x] `niko/visual-maps/archive-mode-map.mdc`
  - Updated References section to warn against linking ephemeral files
  - Added guidance to inline content in appropriate sections
- [x] `niko/Level3/archive-intermediate.mdc`
  - Section 3: Changed "Direct links to" creative docs → **inline** key decisions
  - Section 6: Changed "Direct link to" reflection → **inline** key lessons

#### Sync (.cursor/rules/shared/niko/)
- [x] `visual-maps/archive-mode-map.mdc`
- [x] `Level3/archive-intermediate.mdc`

#### Verified No Changes Needed
- [x] `niko/Level2/archive-basic.mdc` - No link instructions, only describes what gets cleared
- [x] `niko/Level4/archive-comprehensive.mdc` - Describes review process, no link instructions

### Acceptance Criteria
1. Archive templates instruct to inline (not link) ephemeral content
2. Archives remain useful after `/archive clear` is run
3. Both ruleset locations are synchronized
