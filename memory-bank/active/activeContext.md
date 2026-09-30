# Active Context

- **Current Task:** XDG user assets for choose-verification-model
- **Phase:** BUILD - IN-PROGRESS
- **What Was Done:** Level 3 plan for a read-time merge of shipped assets with `$XDG_DATA_HOME/choose-verification-model`. Home `tiers.toml` is the local tier authority. Source-tree refresh still rewrites the skill assets. An install writes the home catalog and mapping. Tests and file-level steps are in `tasks.md`. The architecture record is `memory-bank/active/creative/creative-asset-overlay.md`. Preflight passed with advisories. The operator asked what decision was needed; none is. The marker-file idea was explained and left unused: ai-rizz copies `assets/`, so `assets/.publish` would ship into every install. Build keeps the parent-directory publish check.
- **Next Step:** Unit 1 is green (`test_homeassets`, 15 tests). Next is unit 2: `pick.main` loads the merge, and the issue 129 test isolates `XDG_DATA_HOME`.
