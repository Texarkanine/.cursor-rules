# Tasks

## XDG user assets for choose-verification-model

## Open Questions

- [x] How do shipped skill assets and the user's XDG directory combine on read and on write? → Resolved: pick merges on every run; a home `tiers.toml` overrides per model and a home catalog row does not freeze tiers; refresh in `rules/choose-verification-model` still rewrites the skill assets from those files alone; refresh from an install writes `catalog.json` and `mapping.json` under `$XDG_DATA_HOME/choose-verification-model` (see `memory-bank/active/creative/creative-asset-overlay.md`)
