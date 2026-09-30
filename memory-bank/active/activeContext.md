# Active Context

- **Current Task:** XDG user assets for choose-verification-model
- **Phase:** BUILD - IN-PROGRESS
- **What Was Done:** Level 3 plan for a read-time merge of shipped assets with `$XDG_DATA_HOME/choose-verification-model`. Home `tiers.toml` is the local tier authority. Source-tree refresh still rewrites the skill assets. An install writes the home catalog and mapping. Tests and file-level steps are in `tasks.md`. The architecture record is `memory-bank/active/creative/creative-asset-overlay.md`. Preflight passed with advisories. The operator asked what decision was needed; none is. The marker-file idea was explained and left unused: ai-rizz copies `assets/`, so `assets/.publish` would ship into every install. Build keeps the parent-directory publish check.
- **Next Step:** Units 1 and 2 are green. Next is unit 3: consumer refresh writes the home catalog and mapping; source-tree refresh still writes the skill assets and ignores the home directory.
