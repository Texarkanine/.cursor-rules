# Refresh the Catalog

Run `scripts/refresh.py` from this skill's directory. It needs Python 3.11 or later. Pick does not.

```bash
python3 scripts/refresh.py
```

```powershell
py -3 scripts/refresh.py
```

## Where Refresh Writes

A run from `rules/choose-verification-model` reads and writes that tree's `assets/`. A run from an install writes `catalog.json` and `mapping.json` under `$XDG_DATA_HOME/choose-verification-model`. When `XDG_DATA_HOME` is unset or empty, the directory is `~/.local/share/choose-verification-model`. On Windows, when that variable is unset, the directory is `%LOCALAPPDATA%/choose-verification-model`. Refresh does not write `tiers.toml`.

Pick merges the home directory on its own. A home `tiers.toml` overrides the tier of each model it lists. A model the file does not list keeps the shipped tier.

Refresh reads `agent --list-models`, BenchLM category scores, the Cursor pricing page, and `tiers.toml`. Warnings go to stderr. Without the `agent` CLI, refresh warns once, skips the fill-in, and still writes the catalog.

## Tiers

Tiers are your trust in a model for the work you ask of it. They are set by hand in `tiers.toml` and are never derived from a score. The source tree keeps that file at `assets/tiers.toml`. A home directory may keep its own. List slugs under `C`, `B`, `A`, and `S`, lowest to highest, or under `never`. Any Cursor spelling names its model: effort and `-fast` are ignored. A `never` model is not chosen as a reviewer. As the author, pick prints it back. Refresh does not warn about it.

Refresh warns about every model with no tier, on every run, and about a model listed twice or not in the mapping. After editing `tiers.toml`, run refresh so the catalog picks up the change.

## New Models

Run refresh. For each listed model with no mapping row, refresh finds its pricing row and its BenchLM entry, adds the mapping row, and writes a catalog row with no tier. A model it cannot match is not added, and the warning names the missing source. Existing mapping rows are never changed. Add the new model to `tiers.toml`, then run refresh again.

The catalog covers every model you can use, not only the ones you enable. A row is a reviewer candidate only when one of its spellings is in `--reviewer-models`.

## Slugs

A model's effort, speed, and context window are parameters. Cursor spells effort and speed into the slug, but the model is the stem: `grok-4.7-medium-fast` is `grok-4.7`. The effort words are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `extra-high`, and `max`. An effort may come before `-thinking`: `claude-4.6-opus-high-thinking` is `claude-4.6-opus-thinking`. `thinking` stays in the stem. BenchLM has one number per model, so `effort_encoded` is false on every row.

The printed reviewer keeps the effort written on its `--reviewer-models` spelling. The author's effort is not copied across. When the author's model is not in the catalog, pick prints that spelling and exits 0. An enabled spelling whose model is not in the catalog exits 2 and names it.

## Fast

If a model has fast, it has it at every effort. For a model in the `agent --list-models` output, `has_fast` is whether any listed spelling of it ends in `-fast`. For any other model, refresh uses the pricing page: a `{Name} (Fast)` row, or notes that mention a fast mode. The fast price is not stored. Pick ranks on the base price, then appends `-fast` when the author slug ended in `-fast` and the chosen model has fast.

## Mapping Overrides

An interim score in `assets/mapping.json` is a guess. Refresh replaces it once BenchLM has any of agentic, coding, or reasoning for that model. To onboard a model refresh cannot match, add its mapping row by hand, with an interim score when BenchLM has none. `output_multiplier` is optional. When a row omits it, the base price is used as printed.
