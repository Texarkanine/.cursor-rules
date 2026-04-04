# Progress: fix-orphaned-troubleshooting-path

Move `/nk-refresh` troubleshooting logs from `memory-bank/troubleshooting/` to `memory-bank/active/troubleshooting/` and register the path in the ephemeral file contract so archive and rework cleanup covers it.

**Complexity:** Level 2

## Phase History

- **Complexity Analysis**: Complete — Level 2 determined.
- **Plan**: Complete — 4 canonical files, 5 behaviors, no new tech.
- **Preflight**: PASS — all checks green; archive phases use blanket ephemeral wipe so no archive edits needed.
- **Build**: Complete — 4 canonical files edited, all 5 behaviors verified, zero stale refs.
- **QA**: PASS — all constraints satisfied, no fixes needed.
