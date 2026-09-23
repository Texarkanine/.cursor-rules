# Active Context

- **Current Task:** Add `cursor-grok-4.6-xhigh` to the verification catalog
- **Phase:** `QA - COMPLETE (PASS)`
- **What Was Done:** Shipped tests went red on the missing slug, then green after the mapping row, `refresh.py`, and tier A. Score 76.5 from BenchLM, base output cost 6, `has_fast` true. A second refresh kept tier A. `make test`: 36 tests OK.
- **Files:** `rules/choose-verification-model/assets/mapping.json`, `rules/choose-verification-model/assets/catalog.json`, `tests/choose-verification-model/test_shipped.py`
- **Decisions:** Family `grok`. No selector change. Assertions were written in the red run rather than as a separate empty-stub commit.
- **Next Step:** QA.
