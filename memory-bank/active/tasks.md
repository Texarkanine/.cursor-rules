# Task: effort-variant-slug

* Task ID: effort-variant-slug
* Complexity: Level 2
* Type: bug fix

Make every slug `agent --list-models` reports resolve to a hand-tiered catalog model. The effort collapse already shipped in `5f4b940` (stem keys, printed effort from the candidate spelling, author echo). This plan widens the effort vocabulary to the CLI's, has refresh name listed models that lack a mapping row, and onboards the missing models as mapping and catalog rows that the operator tiers. No tier or score is derived. Decision record: `memory-bank/active/creative/creative-outside-author-placement.md`.

## Test Plan (TDD)

### Behaviors to Verify

- [New efforts]: `model_key` on `claude-opus-5-5-max`, `gpt-5.6-sol-none`, `muse-spark-1.3-minimal`, `gpt-5.5-extra-high` → `claude-opus-5-5`, `gpt-5.6-sol`, `muse-spark-1.3`, `gpt-5.5`
- [Effort before thinking]: `claude-4.6-opus-high-thinking`, `claude-4.6-sonnet-medium-thinking`, `claude-4.6-opus-max-thinking` → `claude-4.6-opus-thinking`, `claude-4.6-sonnet-thinking`, `claude-4.6-opus-thinking`
- [Fast is stripped first]: `claude-opus-5-5-max-fast` → `claude-opus-5-5`; `gpt-5.5-extra-high-fast` → `gpt-5.5`
- [Longest effort wins]: `gpt-5.5-extra-high` is not read as effort `high` on stem `gpt-5.5-extra`; `grok-4.7-xhigh` is not `high` on `grok-4.7-x`
- [No effort is unchanged]: `gpt-5.2`, `gemini-3.1-pro`, `kimi-k2.7-code`, `gpt-5-mini`, `claude-sonnet-5-thinking` → themselves
- [Idempotent]: `model_key(model_key(s)) == model_key(s)` for each case above
- [Existing cases hold]: the current `test_model_key_strips_effort_and_keeps_thinking` assertions still pass
- [Max reviewer resolves]: `select` with enabled `claude-opus-5-5-max` and a stored `claude-opus-5-5` row → that spelling can be printed; no exit 2
- [Listing parse]: listing text with a header line, `auto - Auto (default)`, blank lines, a trailing tip line, and `slug - Name` rows → the set of `model_key` stems of the rows, without `auto`
- [Unmapped stems]: listing stems `{a, b}` with mapping `{a}` → `["b"]`; all mapped → `[]`; efforts and `-fast` of a mapped stem are not reported
- [Refresh warns unmapped]: `refresh.main(..., agent_models=listing)` → stderr has `WARNING: unmapped model b` and no line for `a`; the catalog is still written
- [No agent CLI]: `refresh.main` with the listing unavailable → one `WARNING:` line saying the model listing was skipped; catalog still written; exit 0
- [Regression]: issue command with seed 0 still prints `claude-opus-5-5-high-fast`; missing author still echoes; null-tier or null-score author still exits 2; unknown reviewer still exits 2

### Test Infrastructure

- Framework: stdlib `unittest`, run by `make test`
- Test location: `tests/choose-verification-model/`
- Conventions: `model_key` cases in `test_pick.py`; `_entry`, `_catalog`, `_mapping`, `_run` helpers in `test_pick.py`; refresh inputs injected through `refresh.main` keyword arguments in `test_refresh.py`; shipped-asset invariants in `test_shipped.py`
- New test files: none

## Implementation Plan

### 1. CLI effort vocabulary in `model_key` — executable

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `tests/choose-verification-model/test_pick.py`

1. Stub tests: in `test_pick.py`, add empty `test_model_key_reads_cli_efforts`, `test_model_key_reads_effort_before_thinking`, `test_model_key_leaves_non_effort_suffixes`, and `test_max_effort_reviewer_resolves`.
2. Stub interface: no new public names. Update the `_split_effort` and `model_key` docstrings: efforts are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, `max`, longest match first; an effort directly before `-thinking` is removed and `-thinking` is kept.
3. Write tests and run red: the New efforts, Effort before thinking, Fast is stripped first, Longest effort wins, No effort is unchanged, Idempotent, and Max reviewer resolves behaviors. Run `make test`; the new cases fail on the four-word vocabulary.
4. Write code and run green: extend the effort tuple, match longest first, and in `model_key` handle `<stem>-<effort>-thinking` → `<stem>-thinking` after stripping `-fast`. Run `make test`.

### 2. Refresh names unmapped listed models — executable

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/scripts/refresh.py`, `tests/choose-verification-model/test_refresh.py`

1. Stub tests: in `test_refresh.py`, add empty `test_listing_parses_to_stems`, `test_unmapped_listed_stems_are_reported`, `test_refresh_warns_for_unmapped_listed_models`, and `test_refresh_without_agent_listing_warns_once`.
2. Stub interface: `listed_stems(listing: str) -> set[str]` and `unmapped_stems(listing: str, mapping) -> list[str]` in `modelpool.py`, each with a docstring: a listing row is `slug - Name`; `auto` is not a model; the result is `model_key` stems; `unmapped_stems` is sorted. `refresh.main` gains keyword `agent_models=None`; docstring: a string is the listing; `False` means no listing is available; `None` runs `agent --list-models`, and a missing or failing command is treated as `False`. No listing → one skip warning, coverage skipped.
3. Write tests and run red: the Listing parse, Unmapped stems, Refresh warns unmapped, and No agent CLI behaviors. Inject the listing as a string, and the unavailable case as `agent_models=False`, so no test spawns a process. Tests pass `dest` to a temp path so the working tree is not written. Run `make test`; the new cases fail.
4. Write code and run green: implement both helpers. In `refresh.main`, obtain the listing (injected, else `subprocess.run(["agent", "--list-models"], capture_output=True, text=True, timeout=60)` after `shutil.which("agent")`), append `WARNING: unmapped model {stem}` for each unmapped stem to the existing warnings, or one skip warning when there is no listing. Run `make test`.

### 3. Onboard the listed models — data, with an operator gate

- Files: `rules/choose-verification-model/assets/mapping.json`, `rules/choose-verification-model/assets/catalog.json`
- No new tests: the existing `test_shipped.py` invariants (`model_key(slug) == slug`, every tier on the ladder, mapping keys in the catalog, non-empty families) cover the rows

1. Run `python3 scripts/refresh.py` from the skill directory. The unmapped warnings are the onboarding list (36 stems on the operator's account on 2026-09-24).
2. For each unmapped stem, add a `mapping.json` row: `family`, `pricing_name` (a Model cell on the Cursor pricing page), `benchlm_slug` (a BenchLM `models.json` slug), `interim_score: null`. Thinking and non-thinking stems of one model may share `benchlm_slug` and `pricing_name`. Do not guess a BenchLM or pricing match; a stem with neither is unrecognized.
3. Re-run refresh. New rows get `tier: null` and `must set tier` warnings. Rows with no score or no price are unrecognized: remove them from `mapping.json` and `catalog.json`, and list them under an `## Unrecognized` heading in this file.
4. **Operator gate.** Stop and give the operator the list of rows with `tier: null`. `make test` stays red on `test_catalog_entries_have_required_keys` until every tier is set. Do not propose or fill tiers. Build continues when the operator has set them.
5. Run `make test` green. Re-run refresh once more; no `unmapped model` warnings remain except the unrecognized stems.

### 4. Onboarding and tier policy — prose/policy

- Files: `rules/choose-verification-model/references/refresh.md`
- No tests: prose/policy artifact

1. Replace the effort paragraph: an effort word, from the CLI's vocabulary, is the same model as its stem, and the printed reviewer keeps the enabled spelling's effort.
2. State that tiers are the operator's trust calibration, set by hand, and never derived from score.
3. State onboarding: refresh names listed models without a mapping row; add the row, refresh, set the tier. Refresh reads `agent --list-models`; without the CLI it skips that check.
4. State that the catalog is a superset: a row is a reviewer only when its slug is enabled.

## Technology Validation

No new technology - validation not required. `agent --list-models` exists in the installed Cursor CLI (verified 2026-09-24, `2026.08.25-3e8eec8`); `--models` is not a valid flag.

## Dependencies

- `model_key`, `canonical_slug`, `select`, and `build_catalog` in `modelpool.py` as shipped in `5f4b940`
- Cursor CLI `agent --list-models` (refresh only; optional)
- BenchLM `models.json` and the Cursor pricing page, already fetched by refresh
- Operator tier assignments for the new rows

## Challenges & Mitigations

- Stems that differ from BenchLM or pricing names (`claude-4.6-opus` vs `claude-opus-4-6`, dots vs dashes): step 3 matches each stem by hand against the fetched sources, never by transform. Unmatched stems go to the Unrecognized list.
- A future model whose real name ends in an effort word would be split wrongly: the idempotence test catches this for shipped keys; `test_shipped.py` already asserts `model_key(slug) == slug` for every catalog key.
- The listing is per account: the coverage check is a refresh warning, not a shipped test, so another operator's account cannot turn the suite red.
- `agent` is a `.cmd` shim on some Windows installs: `shutil.which` resolves it; a failure is a warning, not an error.

## Pre-Mortem

- The plan fails because build fills tiers to get `make test` green: step 3 forbids proposing tiers, and the operator gate is a hard stop.
- The plan fails because rows are onboarded with a fabricated BenchLM match: step 3 requires the match to exist in the fetched sources; otherwise the stem is unrecognized.
- The plan fails because the catalog is only complete for this account: accepted. The listing is the operator's; other operators' extra models echo their author or exit 2 on an unknown reviewer, and refresh's warnings show the operator what to onboard.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
