# Task: effort-variant-slug

* Task ID: effort-variant-slug
* Complexity: Level 2
* Type: bug fix

Make every slug `agent --list-models` reports resolve to a hand-tiered catalog model. The effort collapse already shipped in `5f4b940` (stem keys, printed effort from the candidate spelling, author echo). This plan widens the effort vocabulary to the CLI's and makes refresh fill in mapping and catalog rows for listed models that lack them. The operator then tiers the new rows. No tier or score is derived. Refresh is run from this repository and writes the skill's `assets/`. Decision record: `memory-bank/active/creative/creative-outside-author-placement.md`.

## Test Plan (TDD)

### Behaviors to Verify

Effort vocabulary (`model_key`):

- [New efforts]: `claude-opus-5-5-max`, `gpt-5.6-sol-none`, `muse-spark-1.3-minimal`, `gpt-5.5-extra-high` → `claude-opus-5-5`, `gpt-5.6-sol`, `muse-spark-1.3`, `gpt-5.5`
- [Effort before thinking]: `claude-4.6-opus-high-thinking`, `claude-4.6-sonnet-medium-thinking`, `claude-4.6-opus-max-thinking` → `claude-4.6-opus-thinking`, `claude-4.6-sonnet-thinking`, `claude-4.6-opus-thinking`
- [Fast is stripped first]: `claude-opus-5-5-max-fast` → `claude-opus-5-5`; `gpt-5.5-extra-high-fast` → `gpt-5.5`
- [Longest effort wins]: `gpt-5.5-extra-high` is not effort `high` on stem `gpt-5.5-extra`; `grok-4.7-xhigh` is not `high` on `grok-4.7-x`
- [No effort is unchanged]: `gpt-5.2`, `gemini-3.1-pro`, `kimi-k2.7-code`, `gpt-5-mini`, `claude-sonnet-5-thinking` → themselves
- [Idempotent]: `model_key(model_key(s)) == model_key(s)` for each case above
- [Existing cases hold]: the current `test_model_key_strips_effort_and_keeps_thinking` assertions still pass
- [Max reviewer resolves]: `select` with enabled `claude-opus-5-5-max` and a stored `claude-opus-5-5` row → that spelling can be printed; no exit 2

Listing and fill-in (`parse_listing`, `fill_mapping`):

- [Listing parse]: text with the `Available models` header, blank lines, `auto - Auto (default)`, `slug - Name` rows, and a trailing `Tip:` line → `{stem: display name}` with one entry per `model_key` stem (first row's name), no `auto`
- [Price by words, any order]: stem `claude-4.6-opus`, display `Claude Opus 4.6 1M`, pricing row `Claude 4.6 Opus` → `pricing_name` `Claude 4.6 Opus`
- [Family word counts]: stem `gpt-5.3-codex`, display `Codex 5.3 Low`, pricing row `GPT-5.3 Codex` → matched
- [Most words wins]: display `GPT-5 Mini` with rows `GPT-5` and `GPT-5 Mini` → `GPT-5 Mini`; display `Claude Opus 5.5 1M` with rows `Claude Opus 5` and `Claude Opus 5.5` → `Claude Opus 5.5`
- [Parenthesized rows ignored]: `Grok 4.6 (Fast)` and `Claude Opus 4.7 (fast mode)` are never a `pricing_name`
- [BenchLM by same words]: `Claude 4.6 Opus` → scored slug `claude-opus-4-6`; `Claude Opus 5` does not match `claude-opus-5-5` (word counts differ)
- [Only scored BenchLM items]: a BenchLM item with no agentic, coding, or reasoning score is not a match
- [Ambiguous BenchLM]: two scored slugs with the same words → not added; warning names the stem
- [Family]: `cursor-grok-4.5` → `grok`; `muse-spark-1.3` → `muse`; `kimi-k2.7-code` → `kimi`
- [Thinking shares the model]: `claude-opus-5` and `claude-opus-5-thinking` get the same `pricing_name` and `benchlm_slug`
- [New row shape]: an added row is `{family, pricing_name, benchlm_slug, interim_score: null}`, appended after existing rows
- [Unrecognized]: no pricing row → not added, `WARNING: unrecognized model {stem}: no pricing row`; price but no scored BenchLM match → not added, `WARNING: unrecognized model {stem}: no BenchLM score`
- [Existing rows untouched]: a mapped stem whose row the rule would match differently is left exactly as it was; mapped stems absent from the listing stay
- [Refresh fills in]: `refresh.main(..., agent_models=listing, dest=tmp/catalog.json)` → `tmp/mapping.json` has the new row, `tmp/catalog.json` has it with `tier: null`, stderr has `must set tier` for it and the unrecognized warnings
- [No agent CLI]: `refresh.main(..., agent_models=False)` → one `WARNING:` line that the model listing was skipped; mapping written unchanged; catalog written; exit 0
- [Regression]: issue command with seed 0 still prints `claude-opus-5-5-high-fast`; missing author still echoes; null-tier or null-score author still exits 2; unknown reviewer still exits 2

### Test Infrastructure

- Framework: stdlib `unittest`, run by `make test`
- Test location: `tests/choose-verification-model/`
- Conventions: `model_key` cases in `test_pick.py`; `_entry`, `_catalog`, `_mapping`, `_run` helpers in `test_pick.py`; `_benchlm`, `_mapping`, `_previous` helpers and injected `refresh.main` keyword arguments in `test_refresh.py`; shipped-asset invariants in `test_shipped.py`
- New test files: none

## Implementation Plan

### 1. CLI effort vocabulary in `model_key` — executable [x]

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `tests/choose-verification-model/test_pick.py`

1. Stub tests: in `test_pick.py`, add empty `test_model_key_reads_cli_efforts`, `test_model_key_reads_effort_before_thinking`, `test_model_key_leaves_non_effort_suffixes`, and `test_max_effort_reviewer_resolves`.
2. Stub interface: no new public names. Update the `_split_effort` and `model_key` docstrings: efforts are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, `max`, longest match first; an effort directly before `-thinking` is removed and `-thinking` is kept.
3. Write tests and run red: the effort-vocabulary behaviors above. Run `make test`; the new cases fail on the four-word vocabulary.
4. Write code and run green: extend the effort tuple, match longest first, and in `model_key` turn `<stem>-<effort>-thinking` into `<stem>-thinking` after stripping `-fast`. Run `make test`.

### 2. Refresh fills in listed models — executable [x]

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `rules/choose-verification-model/scripts/refresh.py`, `tests/choose-verification-model/test_refresh.py`

1. Stub tests: in `test_refresh.py`, add empty cases for each listing and fill-in behavior above.
2. Stub interface in `modelpool.py`, with docstrings:
    - `parse_listing(listing: str) -> dict`: rows are `slug - Name`; `auto` is not a model; keys are `model_key` stems in first-seen order; the value is the first row's display name.
    - `fill_mapping(listing: str, mapping, pricing_markdown: str, benchlm) -> tuple[dict, list]`: returns a new mapping with rows appended for matchable unmapped stems, and the warnings. Matching rule, stated once here: words are the lowercased text split on spaces and hyphens. A pricing row matches when it has no `(` and all its words are among the display name's words plus the stem's family. The match with the most words wins; a longer name breaks a tie. The BenchLM match is the single scored item whose slug, split on non-alphanumerics, has the same sorted words as the pricing name with dots read as separators. Family is the stem's first hyphen word after a leading `cursor-`. Existing rows are never changed.
    - `refresh.main` gains keyword `agent_models=None`: a string is the listing; `False` means no listing; `None` runs `agent --list-models`, and a missing or failing command is treated as `False`. The mapping is written as `mapping.json` next to the catalog target.
3. Write tests and run red: the listing and fill-in behaviors. Inject the listing as a string and the unavailable case as `agent_models=False`, so no test spawns a process. Every `refresh.main` test passes `agent_models` and a temp `dest`. Run `make test`; the new cases fail.
4. Write code and run green: implement `parse_listing`, `fill_mapping` (reusing `_pricing_rows` and `_category_values`), and in `refresh.main`: get the listing (injected, else `shutil.which("agent")` then `subprocess.run(["agent", "--list-models"], capture_output=True, text=True, timeout=60)`), call `fill_mapping` or add one skip warning, write `mapping.json` next to the target, then call `build_catalog` with the filled mapping. Run `make test`.

### 3. Onboard the listed models — data, with an operator gate

- Files: `rules/choose-verification-model/assets/mapping.json`, `rules/choose-verification-model/assets/catalog.json`
- No new tests: the existing `test_shipped.py` invariants (`model_key(slug) == slug`, every tier on the ladder, mapping keys in the catalog, non-empty families) cover the rows

1. Run `python3 scripts/refresh.py` from the skill directory. Expected on the operator's account (2026-09-24): 32 rows added, 4 unrecognized (`claude-fable-5`, `claude-fable-5-thinking`, `gpt-5-mini`: no BenchLM score; `gpt-5.1`: no pricing row).
2. Read the added rows against the refresh output. Do not hand-edit a match to make it fit; if a row is wrong, the rule is wrong, so go back to unit 2 with a failing test.
3. Record the unrecognized stems under an `## Unrecognized` heading in this file.
4. **Operator gate.** Stop and give the operator the list of rows with `tier: null`. `make test` stays red on `test_catalog_entries_have_required_keys` until every tier is set. Do not propose or fill tiers. Build continues when the operator has set them.
5. Run `make test` green.

### 4. Onboarding and tier policy — prose/policy

- Files: `rules/choose-verification-model/references/refresh.md`
- No tests: prose/policy artifact

1. Replace the effort paragraph: an effort word, from the CLI's vocabulary, is the same model as its stem, and the printed reviewer keeps the enabled spelling's effort.
2. State that tiers are the operator's trust calibration, set by hand, and never derived from score.
3. State onboarding: run refresh from this repository; it reads `agent --list-models`, fills in mapping and catalog rows for new models, and warns about models it cannot match; then set each new tier by hand. Without the CLI it skips the fill-in.
4. State that the catalog is a superset: a row is a reviewer only when its slug is enabled.

## Technology Validation

No new technology - validation not required. Verified 2026-09-24 against live sources:

- `agent --list-models` exists in the installed Cursor CLI (`2026.08.25-3e8eec8`); `--models` is not a valid flag. 240 slugs collapse to 48 stems.
- The unit 2 matching rule resolves 44 of 48 stems and reproduces the `pricing_name` and `benchlm_slug` of all 12 existing mapping rows. The 4 misses are real gaps in the sources, not rule failures.

## Dependencies

- `model_key`, `canonical_slug`, `select`, `build_catalog`, `_pricing_rows`, and `_category_values` in `modelpool.py` as shipped in `5f4b940`
- Cursor CLI `agent --list-models` (refresh only; optional)
- BenchLM `models.json` and the Cursor pricing page, already fetched by refresh
- Operator tier assignments for the new rows

## Challenges & Mitigations

- Word-subset matching could pick a wrong but plausible pricing row as sources change: most-words-wins, parenthesized rows excluded, and an exact sorted-word BenchLM match; unit 3 step 2 reads every added row before the operator tiers it.
- A future model whose real name ends in an effort word would be split wrongly: `test_shipped.py` asserts `model_key(slug) == slug` for every catalog key, and a split stem would show up as an odd added row in unit 3.
- The listing is per account: fill-in only runs when the operator refreshes, and coverage is not a shipped test, so another account cannot turn the suite red.
- `agent` is a `.cmd` shim on some Windows installs: `shutil.which` resolves it; a failure is a warning, not an error.
- Refresh now writes `mapping.json`: existing rows keep their bytes because new rows are appended to the parsed dict in order and the file is written with the current indentation.

## Pre-Mortem

- The plan fails because build fills tiers to get `make test` green: unit 3 forbids proposing tiers, and the operator gate is a hard stop.
- The plan fails because build hand-fixes a bad auto-match: unit 3 step 2 sends a bad match back to unit 2 as a failing test.
- The plan fails because the fill-in rewrites the operator's hand-edited mapping rows: the Existing rows untouched behavior locks that.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
