# Refresh the Catalog

Run `scripts/refresh.py` with Python 3 from this skill's directory. It rewrites `assets/catalog.json` from BenchLM category scores and Cursor output prices. It keeps `tier_order` and any tier already set. A new slug gets a null tier and a stderr warning.

```bash
python3 scripts/refresh.py
```

```powershell
py -3 scripts/refresh.py
```

Tiers run `C`, `B`, `A`, `S` from lowest to highest. Assign them by hand.

A trailing `-fast` is the same model. It shares the base slug's bench score, tier, family, and output price. `composer-2.5-fast` is `composer-2.5`. `grok-4.7-medium-fast` is `grok-4.7-medium`. Refresh sets `has_fast` when the pricing page has a `{Name} (Fast)` row, or the model's notes mention a fast mode. The fast price is not stored. Pick ranks on the base price, then appends `-fast` only when the author slug ended in `-fast` and the chosen model has a fast variant.

An interim score in `assets/mapping.json` is a guess. Refresh replaces it once BenchLM has any of agentic, coding, or reasoning for that model. `output_multiplier` is optional. When a row omits it, the base price is used as printed.
