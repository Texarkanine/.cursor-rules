# TASK ARCHIVE: Fix Niko Command Paths

## METADATA
- **Task ID:** niko-command-paths
- **Date:** 2026-01-25
- **Complexity:** Level 1 (Bulk Find/Replace)
- **Status:** COMPLETE

## SUMMARY

Updated `/niko/X` command invocations to `/X` across rule files after ai-rizz removed the niko namespace from command installation paths. This was a follow-up fix to commit `809bb88` which updated the command files but missed the rule files.

## REQUIREMENTS

- Update all `/niko/build`, `/niko/qa`, `/niko/plan`, `/niko/creative`, `/niko/archive`, `/niko/reflect`, `/niko/refresh` references to `/build`, `/qa`, `/plan`, `/creative`, `/archive`, `/reflect`, `/refresh`
- Scope: `rulesets/niko/niko/` and `rules/` directories only
- Do NOT modify memory-bank archives or installed `.cursor/rules/` files

## IMPLEMENTATION

Single `sed -i` command with 7 replacement patterns applied to 9 files:

```bash
sed -i \
  -e 's|/niko/build|/build|g' \
  -e 's|/niko/qa|/qa|g' \
  -e 's|/niko/plan|/plan|g' \
  -e 's|/niko/creative|/creative|g' \
  -e 's|/niko/archive|/archive|g' \
  -e 's|/niko/reflect|/reflect|g' \
  -e 's|/niko/refresh|/refresh|g' \
  <files...>
```

### Files Changed
| File | Changes |
|------|---------|
| `rulesets/niko/niko/visual-maps/van-mode-map.mdc` | 16 |
| `rulesets/niko/niko/visual-maps/van_mode_split/van-mode-map.mdc` | 18 |
| `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-main.mdc` | 10 |
| `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/mode-transitions.mdc` | 8 |
| `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/reports.mdc` | 4 |
| `rulesets/niko/niko/visual-maps/van_mode_split/van-qa-utils/rule-calling-guide.mdc` | 6 |
| `rulesets/niko/niko/visual-maps/qa-mode-map.mdc` | 2 |
| `rulesets/niko/niko/Core/memory-bank-paths.mdc` | 2 |
| `rules/wiggum-niko-coderabbit-pr.md` | 16 |

## TESTING

- Verified 0 remaining `/niko/X` command references in target scope via `grep`
- Confirmed git diff shows expected 9 files changed

## LESSONS LEARNED

1. Shell tools like `sed` are more efficient than individual Edit tool calls for bulk mechanical changes
2. When updating command paths, check both command files AND rule files that reference those commands

## REFERENCES

- Reflection: `memory-bank/reflection/reflection-niko-command-paths.md`
- Prior commit: `809bb88` (fix: attempt to fix niko command paths /niko/X -> plain /X)
