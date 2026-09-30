# Active Context

- **Current Task:** XDG user assets for choose-verification-model
- **Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)
- **What Was Done:** Level 3 plan for a read-time merge of shipped assets with `$XDG_DATA_HOME/choose-verification-model`. Home `tiers.toml` is the local tier authority. Source-tree refresh still rewrites the skill assets. An install writes the home catalog and mapping. Tests and file-level steps are in `tasks.md`. The architecture record is `memory-bank/active/creative/creative-asset-overlay.md`. Preflight passed with advisories. The operator asked what decision was needed; none is. The marker-file idea was explained and left unused: ai-rizz copies `assets/`, so `assets/.publish` would ship into every install.
- **Next Step:** Operator runs `/niko-build`. Keep the parent-directory publish check. Give `user_assets_dir` empty defaults so production can call it with no arguments.
