# Active Context

- **Current Task:** XDG user assets for choose-verification-model
- **Phase:** BUILD - COMPLETE
- **What Was Done:** Shipped assets merge with `$XDG_DATA_HOME/choose-verification-model` at read time. Home `tiers.toml` is the local tier authority. Source-tree refresh still rewrites the skill assets and ignores the home directory. An install writes the home catalog and mapping and does not write `tiers.toml`. `SKILL.md` is unchanged. `make test` passed: 99 choose-verification-model tests, symlink check, and README link check. After build, the operator had refresh add `claude-sonnet-5-5` (Claude Sonnet 5.5, the same spelling step as `claude-opus-5-5`) at tier A. BenchLM scores refreshed with it. The suite still passes.
- **Files:** `rules/choose-verification-model/scripts/homeassets.py`, `scripts/pick.py`, `scripts/refresh.py`, `references/refresh.md`, `tests/choose-verification-model/test_homeassets.py`, `tests/choose-verification-model/test_shipped.py`
- **Decisions:** `user_assets_dir` with no arguments uses `os.environ`, `Path.home()`, and `sys.platform`. When only one of `catalog` or `mapping` is passed to `pick.main`, the other document comes from the merge.
- **Deviations:** None beyond those two preflight advisories. The parent-directory publish check stayed.
- **Next Step:** QA. Reviewer slug from `pick.py` is `kimi-k3-high`.
