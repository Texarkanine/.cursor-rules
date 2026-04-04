# Task: Fix Orphaned Troubleshooting Path

* Task ID: fix-orphaned-troubleshooting-path
* Complexity: Level 2
* Type: Bug fix

`/nk-refresh` writes diagnostic scratch logs to `memory-bank/troubleshooting/`, which sits outside `memory-bank/active/` and is never cleaned up by archive, rework, or milestone-advance flows. Move the path under `active/` and register it in the ephemeral file contract.

## Test Plan (TDD)

### Behaviors to Verify

- **B1 (path correctness)**: `nk-refresh/SKILL.md` Step 2 references `memory-bank/active/troubleshooting/` → troubleshooting logs land inside the active-folder cleanup scope
- **B2 (path registry)**: `memory-bank-paths.mdc` lists `active/troubleshooting/` as ephemeral with "deleted, not inlined" annotation → agents know the lifecycle
- **B3 (archive exception)**: `archives.mdc` explicitly states troubleshooting logs are deleted without inlining → prevents agents from wasting tokens summarizing verbose diagnostic notes
- **B4 (L4 cleanup)**: `niko/SKILL.md` Step 2a delete list includes `troubleshooting/` → milestone advance cleans it up
- **B5 (rework cleanup)**: `niko/SKILL.md` Step 3b delete list includes `troubleshooting/` → rework re-entry cleans it up
- **Edge: no regression on existing cleanup items**: All pre-existing items in the Step 2a and Step 3b delete lists remain unchanged

### Test Infrastructure

- Framework: None (documentation-only repository; .mdc/.md rule files consumed by AI agents)
- Test location: N/A
- Conventions: Semantic review via grep/read verification against the changed files
- New test files: None

## Implementation Plan

1. **Edit `rulesets/niko/skills/nk-refresh/SKILL.md`** (B1)
   - File: `rulesets/niko/skills/nk-refresh/SKILL.md`
   - Change: Line 52 — replace `memory-bank/troubleshooting/troubleshooting-<timestamp>.md` with `memory-bank/active/troubleshooting/troubleshooting-<timestamp>.md`

2. **Edit `rulesets/niko/niko/core/memory-bank-paths.mdc`** (B2)
   - File: `rulesets/niko/niko/core/memory-bank-paths.mdc`
   - Change: After the L4 Milestone List bullet, add a new bullet for Troubleshooting Docs with the `active/troubleshooting/` path and "deleted, not inlined" lifecycle note

3. **Edit `rulesets/niko/niko/memory-bank/archives.mdc`** (B3)
   - File: `rulesets/niko/niko/memory-bank/archives.mdc`
   - Change: After the paragraph about inlining ephemeral content, add an exception paragraph for troubleshooting logs

4. **Edit `rulesets/niko/skills/niko/SKILL.md`** (B4, B5)
   - File: `rulesets/niko/skills/niko/SKILL.md`
   - Change (Step 2a): Add `troubleshooting/ (if present)` to the delete list
   - Change (Step 3b): Add `troubleshooting/ (if present)` to the delete list

5. **Verification**: Grep for any remaining `memory-bank/troubleshooting` (without `active/`) references in `rulesets/` to confirm no stale paths survive

## Technology Validation

No new technology — validation not required.

## Dependencies

- None. All changes are internal to canonical rule/skill files under `rulesets/niko/`.

## Challenges & Mitigations

- **Non-canonical copies diverge**: `.cursor/` and `.claude/` copies of `refresh/SKILL.md` still reference the old path. Mitigation: These are synced out-of-band by `ai-rizz`/`a16n` — document in commit message that sync is needed.
- **Existing orphaned `memory-bank/troubleshooting/` directories in consumer repos**: Mitigation: Out of scope; consumers can delete manually. This fix prevents future accumulation.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight
- [x] Build
- [x] QA
