# TASK ARCHIVE: Archive Inlining Fix

## METADATA
- **Task ID**: archive-inlining-fix
- **Complexity**: Level 2 (Simple Enhancement)
- **Date Completed**: 2026-01-20
- **Status**: COMPLETED & ARCHIVED

## SUMMARY

Fixed inconsistency in Niko archive templates where instructions said to "link to" ephemeral files (reflection, creative phase docs) that get deleted by `/archive clear`, resulting in broken links. Updated templates to instruct users to **inline** relevant content instead.

Also cleaned up an empty placeholder file (`van-qa-checks/file-verification.mdc`) that was never implemented.

## REQUIREMENTS

1. Archive templates must instruct users to inline (not link) ephemeral content
2. Archives must remain useful after `/archive clear` is run
3. Empty placeholder files should be removed

## IMPLEMENTATION

### Changes to `archive-mode-map.mdc`
Updated the References section template from:
```
- [Link to reflection document]
- [Link to creative phase documents]
```
To (now marked optional):
```
## References (Optional - omit if none)
- [Link to external issue/ticket that prompted this work]
- [Link to external specs or documentation]
- [Link to related PR in another repository]

> **NOTE:** This section is OPTIONAL. Omit it entirely if there are no useful external references.
```

### Changes to `archive-intermediate.mdc` (Level 3)
- **Section 3 (Design Decisions)**: Changed "Direct links to creative docs" → "**Inline** key decisions, rationale, alternatives considered"
- **Section 6 (Reflection)**: Changed "Direct link to reflection" → "**Inline** key lessons, challenges, outcomes"

### Cleanup
- Deleted empty `van-qa-checks/file-verification.mdc` placeholder (both rulesets/ and .cursor/rules/shared/ copies)

## TESTING

- Verified grep shows no remaining "link to reflection/creative" instructions in archive templates
- Confirmed Level 2 and Level 4 archive templates don't have the same issue (they describe review process, not linking)

## LESSONS LEARNED

1. **Check for sync tools first** - This repo uses ai-rizz for syncing `rulesets/` to `.cursor/rules/shared/`. Edit source files only.
2. **Distinguish internal vs. user-facing** - Internal file names like `van-*.mdc` shouldn't appear in user documentation
3. **Archive = Self-Contained** - Archives must be standalone documents that work after ephemeral files are cleaned up
4. **Optional sections should be omitted, not filled with placeholders** - If a template section has no useful content, omit it entirely rather than adding placeholder or vague text

