# Tasks

## niko-preflight-qa: Add /preflight command and reposition /qa

**Complexity:** Level 3
**Status:** REFLECT complete

### Plan
- Create `/preflight` command (pre-build plan validation, L3+, gates `/build`)
- Rewrite `/qa` from pre-build mechanical validation to post-build semantic review (L2+, gates `/reflect`)
- Update all routing: commands, core rules, workflow levels, visual maps, archive cleanup

### Implementation
- 34 files modified across commands, core rules, workflow levels, visual maps, archive files, and README
- Net -1,221 lines (removed old PowerShell/Bash mechanical validation, replaced with semantic review)

### QA Review
- **PASS** — 4 findings fixed during review (stale systemPatterns.md, stale van-mode-map diagram, obsolete rule-calling-guide references, deleted van-qa-checks directory)

### Reflection
- Complete — see `memory-bank/reflection/reflection-niko-preflight-qa.md`
