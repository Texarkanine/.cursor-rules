# Active Context

## Current Task: Onboard Gemini 4 Argon and Claude Haiku 5.5
**Phase:** BUILD - COMPLETE

## What Was Done
- Shipped `select` tests went red on unknown slugs, then green after `tiers.toml` and `refresh.py`.
- `gemini-4-argon` is tier A. `claude-haiku-5-5` and `claude-haiku-5-5-thinking` are tier C. None has a fast variant.
- Mapping gained only those three stems. Existing mapping rows are unchanged. `make test`: 110 tests OK.

## Next Step
- QA review.

## Files
- `/home/mobaxterm/worktrees/Texarkanine/.cursor-rules/.cursor-rules-gemini-4-argon/tests/choose-verification-model/test_shipped.py`
- `/home/mobaxterm/worktrees/Texarkanine/.cursor-rules/.cursor-rules-gemini-4-argon/rules/choose-verification-model/assets/tiers.toml`
- `/home/mobaxterm/worktrees/Texarkanine/.cursor-rules/.cursor-rules-gemini-4-argon/rules/choose-verification-model/assets/mapping.json`
- `/home/mobaxterm/worktrees/Texarkanine/.cursor-rules/.cursor-rules-gemini-4-argon/rules/choose-verification-model/assets/catalog.json`
