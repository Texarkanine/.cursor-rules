# Task: effort-variant-slug

* Task ID: effort-variant-slug
* Complexity: Level 2
* Type: bug fix

An unmatched effort spelling (`low`, `medium`, `high`, `xhigh`) of a model whose stored catalog key already ends in an effort word gets an in-memory row: its own score, a tier taken from the score-neighbors, and the sibling's family and base price. `select` then runs the existing window and one-tier lookup. When the author spelling still cannot be placed, `select` returns that spelling and the process exits 0. The on-disk catalog stays the hand-chosen set. `SKILL.md` stays a thin caller.


## Test Plan (TDD)

### Behaviors to Verify

- [Higher and extra-high stay apart]: catalog has `m-medium` only → `place_effort` on `m-high` and `m-xhigh` returns two scores, both above `m-medium`, and `m-high` < `m-xhigh`
- [Lower effort sits below the stored row]: `place_effort` on `m-low` returns a score below `m-medium`
- [Boundary takes the higher tier]: stored `m-medium` is tier B and the next higher score is tier A → `m-high` is tier A
- [Shared neighbor tier stays]: both score-neighbors are tier A → the synthetic tier is A
- [Exact key stays the stored row]: `place_effort` on `m-medium` returns that row's score and tier
- [Bare key is not an effort anchor]: catalog has `composer-2.5` and no effort-suffixed sibling → `composer-2.5-high` raises `SelectionError` naming that slug
- [Thinking stays in the stem]: catalog has `claude-sonnet-5-thinking-high` → `claude-sonnet-5-high` raises `SelectionError`
- [Null sibling score]: the only sibling has `score: null` → `SelectionError` naming the unmatched slug
- [Caller catalog is unchanged]: `select` returns and `catalog["models"]` is still the dict the caller passed, with the same tiers
- [Synthetic reviewer can be printed]: author is an exact low-tier row; the only eligible reviewer is `m-xhigh` → `select` returns `m-xhigh`
- [Higher effort is a different row]: author `m-high` with a tier-B peer and a tier-A model enabled prints the tier-A model; the same pool with author `m-medium` prints the tier-B peer
- [Empty pool prints the requested spelling]: author `m-low` alone → `m-low`, not `m-medium`
- [Fast suffix]: author ends in `-fast` and the sibling has `has_fast` → a chosen synthetic reviewer is printed with `-fast`; placement used the base price
- [Shipped command]: `pick.py --model cursor-grok-4.6-xhigh-fast --reviewer-models claude-opus-5-5-high,gpt-5.6-terra-medium,grok-4.7-xhigh` exits 0, stdout is one of those spellings or the author, with `-fast` only as `_with_speed` already appends it, and `assets/catalog.json` bytes are unchanged
- [Unplaceable author is printed]: `--model missing-author --reviewer-models other` → exit 0, stdout `missing-author`. The same for an author whose stem has no effort-suffixed sibling, such as `composer-2.5-high` when the catalog has only `composer-2.5`. A known author row with null tier or null score still exits 2
- [Still unknown]: `missing-reviewer` exits 2 and names that slug (existing test)

### Test Infrastructure

- Framework: stdlib `unittest`, `python3 -m unittest discover -s tests/choose-verification-model -p 'test_*.py'`
- Test location: `tests/choose-verification-model/`
- Conventions: in-memory catalogs via `_entry`, `_catalog`, `_mapping`, `_run`; shipped invariants in `test_shipped.py`. Fixture tiers in the new cases are `B`/`A`, so they do not collide with the suite's default tier names `low`/`mid`/`high`.
- New test files: none

## Implementation Plan

### 1. place_effort — executable

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `tests/choose-verification-model/test_pick.py`

1. Stub tests: in `test_pick.py`, add empty cases for the `place_effort` behaviors (scores apart, lower effort below, boundary tier, shared tier, exact key, bare key, thinking stem, null score).
2. Stub interface: `place_effort(catalog, mapping, slug) -> tuple[dict, str]` in `modelpool.py`. Returns `(entry, family)`. Docstring: exact key returns the stored entry and its family; an unmatched effort spelling returns a new entry and the sibling family. Raises `SelectionError` naming `slug`.
3. Write tests and run red: assert the formula below. Run those cases and confirm they fail.
4. Write code and run green:
    - Effort order is `low`, `medium`, `high`, `xhigh` (indexes 0–3). Strip a trailing `-fast` with `canonical_slug` first. Split a trailing effort word, matching `xhigh` before `high`.
    - Exact catalog key: return that entry and its mapping family.
    - Otherwise the slug must end in an effort word. Siblings are catalog keys with the same stem that themselves end in an effort word. A sibling counts only when its tier is in `tier_order`, its score is not null, and its mapping family is a non-empty string. No such sibling → `SelectionError`.
    - Both a lower and an upper sibling: score interpolates by effort index between those two stored scores.
    - Only a lower sibling: anchor is that sibling. Far is the other-stem stored row with the smallest score strictly above the anchor. `room` is `3 - anchor_index`. Fraction is `(requested - anchor_index) / (room + 1)`. Score sits that fraction of the way from the anchor to the far score. No far row: `anchor_score + (requested - anchor_index) * 1e-3`.
    - Only an upper sibling: mirror. `room` is `anchor_index`. Fraction is `(anchor_index - requested) / (room + 1)`. No far row: `anchor_score - (anchor_index - requested) * 1e-3`.
    - If that score equals a stored score, nudge `1e-6` toward the anchor.
    - Tier comes from stored score-neighbors of that score (other synthetics are not neighbors). Different tiers → the higher `tier_order` index. Same tier → that tier. One neighbor → that tier.
    - Family, `output_cost_per_million`, and `has_fast` come from the nearest usable sibling by absolute effort-index distance. A tie takes the higher effort. `score_source` is `effort`.
    - Return a new dict. Do not mutate `catalog` or `mapping`.

### 2. select uses the in-memory rows — executable

- Files: `rules/choose-verification-model/scripts/modelpool.py`, `tests/choose-verification-model/test_pick.py`, `tests/choose-verification-model/test_shipped.py`

1. Stub tests: empty cases for synthetic reviewer printed, higher-effort author versus the stored effort, empty-pool spelling, fast suffix, caller catalog unchanged, the shipped command in `test_shipped.py`, and the rewrite of `test_unknown_author_slug_exits_2` so an unplaceable author is printed.
2. Stub interface: `_with_effort(catalog, mapping, slugs) -> tuple` in `modelpool.py`. `select` keeps its signature.
3. Write tests and run red: the higher-effort fixture prints the tier-A model; the stored-effort author prints the tier-B peer. Shipped argv exits 0. Confirm the new cases fail.
4. Write code and run green:
    - `_with_effort` copies `models` and mapping `models`. For each slug, if `canonical_slug` is already a key, leave it. Otherwise `place_effort` and insert the entry under the canonical key and `{family}` under the mapping copy.
    - `select` calls `_with_effort` with the author and every enabled slug before the existing lookup. The pool is still the enabled keys only. The author row is ranked even when it is synthetic, and it is printed by the existing empty-pool returns.
    - When `place_effort` fails for the author, `select` returns the original `--model` string. `main` prints it and returns 0. No second `-fast` is appended. A null tier or null score on a stored author row still raises. When `place_effort` fails for an enabled slug, `select` still raises `SelectionError` naming that slug.
    - `_with_speed` still appends `-fast` from the author's original spelling and the chosen entry's `has_fast`.
    - Run `python3 -m unittest discover -s tests/choose-verification-model -p 'test_*.py'`.

### 3. Slug identity note — prose/policy

- Files: `rules/choose-verification-model/references/refresh.md`
- No tests: prose/policy artifact

1. After the `-fast` paragraph, state that an unmatched effort spelling of a stored effort-suffixed key is placed in memory for that pick, that different efforts are different rows, and that the placement is not written to `assets/catalog.json`.
2. State that an author spelling the script cannot place is printed as given and the process exits 0.
3. Leave the `grok-4.7-medium-fast` is `grok-4.7-medium` sentence in place: it is the `-fast` rule.
4. Leave `SKILL.md` as the short happy path. Do not add a branch that tells the agent to choose a reviewer when the script exits non-zero.

## Technology Validation

No new technology - validation not required

## Dependencies

- `rules/choose-verification-model/scripts/modelpool.py` (`canonical_slug`, `select`, `SelectionError`, `_with_speed`)
- `rules/choose-verification-model/assets/catalog.json` and `mapping.json` (read-only during a pick)
- stdlib `unittest`

## Challenges & Mitigations

- BenchLM `models.json` has one row per model (`claude-opus-5-5`, `grok-4-7`) and no effort spellings. There is no published score to fetch. Placement derives the score from the stored sibling and its neighbors. When the author still cannot be placed, the script prints that author. An unplaceable reviewer still exits 2.
- A lower effort rarely drops a tier, because a tier change on the boundary keeps the higher letter. That is the issue's boundary rule. Fixture tests lock it.
- `composer-2.5` has no effort suffix, so `composer-2.5-high` is not placed. As an author, that spelling is printed back. As a reviewer, it exits 2.
- Shipped scores move on refresh. The shipped test asserts exit 0, an allowed spelling, and unchanged file bytes. Rank and tier assertions use fixture catalogs.
- Two synthetics in one pick are placed against stored rows only, so they do not depend on each other's insertion order.
- End-of-scale `1e-3` steps can sit past the last stored score. Nothing is beyond them to leap over. The `1e-6` nudge only breaks an exact tie with a stored score.

## Pre-Mortem

- The derived score is treated as if BenchLM had measured that effort, and a later reader retieres the catalog from it. The plan answers this by keeping `score_source` as `effort`, leaving disk rows alone, and saying so in `refresh.md`.
- Placement is implemented only in `pick.py`, so `select` callers still exit 2. Step 2 puts `_with_effort` inside `select`.
- A synthetic spelling that was never enabled gets printed. `_with_effort` inserts only the author and the enabled slugs, and the pool stays the enabled keys.
- High and extra-high collapse into one slot above the stored row. The fraction uses the effort index and `room`, so those two scores differ.
- The copy is skipped and a pick retieres a stored row in the caller's dict. Step 2 tests that the caller's `models` dict is unchanged.
- The author echo is written into `SKILL.md` as an agent policy, so the agent infers a reviewer the script refused to choose. Operator rejected that. The echo is a return value inside `select`. `SKILL.md` stays "use the slug it prints."

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
