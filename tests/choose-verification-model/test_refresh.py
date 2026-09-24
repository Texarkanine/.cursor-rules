"""Catalog refresh behavior, including a refresh-then-pick case.

Fixtures stand in for the BenchLM document and the pricing page.
Nothing in this module opens a network connection.
"""

import io
import json
import random
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from modelpool import (  # noqa: E402
    build_catalog,
    fill_mapping,
    parse_listing,
    previous_from_tiers,
    select,
)
from refresh import main as refresh_main  # noqa: E402


def _benchlm(items):
    return {
        "items": [
            {
                "slug": slug,
                "scores": {"displayCategoryScores": categories},
            }
            for slug, categories in items.items()
        ]
    }


def _mapping(rows):
    models = {}
    for slug, row in rows.items():
        models[slug] = {
            "family": row["family"],
            "pricing_name": row["pricing_name"],
            "output_multiplier": row.get("output_multiplier", 1),
            "benchlm_slug": row.get("benchlm_slug"),
            "interim_score": row.get("interim_score"),
        }
    return {"models": models}


def _previous(models, tier_order=("low", "high")):
    return {"tier_order": list(tier_order), "models": models}


class RefreshTests(unittest.TestCase):
    def test_mean_of_three_categories_sets_benchlm_source(self):
        """Agentic, coding, and reasoning present: score is their mean."""
        catalog, warnings = build_catalog(
            _benchlm({"m": {"agentic": 10, "coding": 20, "reasoning": 30}}),
            "| Model | Output |\n| --- | --- |\n| Row | $5 |\n",
            _mapping({"slug": {"family": "a", "pricing_name": "Row", "benchlm_slug": "m"}}),
            _previous({"slug": {"tier": "low"}}),
        )
        self.assertEqual(catalog["models"]["slug"]["score"], 20)
        self.assertEqual(catalog["models"]["slug"]["score_source"], "benchlm")
        self.assertFalse(catalog["models"]["slug"]["effort_encoded"])
        self.assertEqual(warnings, [])

    def test_null_reasoning_is_left_out_of_the_mean(self):
        """A null category is skipped. The other two are averaged."""
        catalog, _warnings = build_catalog(
            _benchlm({"m": {"agentic": 10, "coding": 30, "reasoning": None}}),
            "| Model | Output |\n| --- | --- |\n| Row | $5 |\n",
            _mapping({"slug": {"family": "a", "pricing_name": "Row", "benchlm_slug": "m"}}),
            _previous({"slug": {"tier": "low"}}),
        )
        self.assertEqual(catalog["models"]["slug"]["score"], 20)
        self.assertEqual(catalog["models"]["slug"]["score_source"], "benchlm")

    def test_interim_score_kept_when_every_category_is_null(self):
        """No category scores: the mapping's interim score is the score."""
        catalog, warnings = build_catalog(
            _benchlm({"m": {"agentic": None, "coding": None, "reasoning": None}}),
            "| Model | Output |\n| --- | --- |\n| Row | $5 |\n",
            _mapping(
                {
                    "slug": {
                        "family": "a",
                        "pricing_name": "Row",
                        "benchlm_slug": "m",
                        "interim_score": 7,
                    }
                }
            ),
            _previous({"slug": {"tier": "low"}}),
        )
        self.assertEqual(catalog["models"]["slug"]["score"], 7)
        self.assertEqual(catalog["models"]["slug"]["score_source"], "interim")
        self.assertNotIn("interim", " ".join(warnings))

    def test_interim_score_replaced_when_a_category_appears(self):
        """A later refresh with any category drops the interim score."""
        mapping = _mapping(
            {
                "slug": {
                    "family": "a",
                    "pricing_name": "Row",
                    "benchlm_slug": "m",
                    "interim_score": 7,
                }
            }
        )
        previous = _previous({"slug": {"tier": "low"}})
        pricing = "| Model | Output |\n| --- | --- |\n| Row | $5 |\n"
        first, _warnings = build_catalog(
            _benchlm({"m": {"agentic": None, "coding": None, "reasoning": None}}),
            pricing,
            mapping,
            previous,
        )
        self.assertEqual(first["models"]["slug"]["score_source"], "interim")
        second, warnings = build_catalog(
            _benchlm({"m": {"agentic": 12, "coding": None, "reasoning": None}}),
            pricing,
            mapping,
            previous,
        )
        self.assertEqual(second["models"]["slug"]["score"], 12)
        self.assertEqual(second["models"]["slug"]["score_source"], "benchlm")
        self.assertNotIn("interim", " ".join(warnings))

    def test_missing_category_and_interim_warns(self):
        """Neither a category nor an interim score: score stays null."""
        catalog, warnings = build_catalog(
            _benchlm({}),
            "| Model | Output |\n| --- | --- |\n| Row | $5 |\n",
            _mapping(
                {
                    "slug": {
                        "family": "a",
                        "pricing_name": "Row",
                        "benchlm_slug": "missing",
                        "interim_score": None,
                    }
                }
            ),
            _previous({"slug": {"tier": "low"}}),
        )
        self.assertIsNone(catalog["models"]["slug"]["score"])
        self.assertIsNone(catalog["models"]["slug"]["score_source"])
        self.assertIn("WARNING: must set interim score for slug", warnings)

    def test_shared_benchlm_slug_shares_score_not_price(self):
        """Two Cursor slugs mapped to one BenchLM item share its score."""
        pricing = "\n".join(
            [
                "| Model | Output |",
                "| --- | --- |",
                "| Fast | $15 |",
                "| Slow | $2.5 |",
            ]
        )
        catalog, _warnings = build_catalog(
            _benchlm({"shared": {"agentic": 10, "coding": 20, "reasoning": 30}}),
            pricing,
            _mapping(
                {
                    "fast": {
                        "family": "composer",
                        "pricing_name": "Fast",
                        "benchlm_slug": "shared",
                    },
                    "slow": {
                        "family": "composer",
                        "pricing_name": "Slow",
                        "benchlm_slug": "shared",
                    },
                }
            ),
            _previous({"fast": {"tier": "low"}, "slow": {"tier": "low"}}),
        )
        self.assertEqual(catalog["models"]["fast"]["score"], catalog["models"]["slow"]["score"])
        self.assertEqual(catalog["models"]["fast"]["score"], 20)
        self.assertEqual(catalog["models"]["fast"]["output_cost_per_million"], 15)
        self.assertEqual(catalog["models"]["slow"]["output_cost_per_million"], 2.5)

    def test_linked_model_cell_and_output_column_follow_the_header(self):
        """``[Name](url)`` yields Name. Output is found by its header."""
        pricing = "\n".join(
            [
                "| Output | Model |",
                "| --- | --- |",
                "| $2 | [Linked](https://example.com/linked) |",
                "",
                "| Notes | Model | Output |",
                "| --- | --- | --- |",
                "| ignore | Plain | $4 |",
            ]
        )
        catalog, warnings = build_catalog(
            _benchlm(
                {
                    "a": {"agentic": 1, "coding": 1, "reasoning": 1},
                    "b": {"agentic": 1, "coding": 1, "reasoning": 1},
                }
            ),
            pricing,
            _mapping(
                {
                    "linked": {"family": "a", "pricing_name": "Linked", "benchlm_slug": "a"},
                    "plain": {"family": "b", "pricing_name": "Plain", "benchlm_slug": "b"},
                }
            ),
            _previous({"linked": {"tier": "low"}, "plain": {"tier": "low"}}),
        )
        self.assertEqual(catalog["models"]["linked"]["output_cost_per_million"], 2)
        self.assertEqual(catalog["models"]["plain"]["output_cost_per_million"], 4)
        self.assertEqual(warnings, [])

    def test_output_multiplier_scales_the_price(self):
        """The pricing-row dollars are multiplied by ``output_multiplier``."""
        catalog, _warnings = build_catalog(
            _benchlm({"m": {"agentic": 1, "coding": 1, "reasoning": 1}}),
            "| Model | Output |\n| --- | --- |\n| Row | $10 |\n",
            _mapping(
                {
                    "slug": {
                        "family": "a",
                        "pricing_name": "Row",
                        "benchlm_slug": "m",
                        "output_multiplier": 2,
                    }
                }
            ),
            _previous({"slug": {"tier": "low"}}),
        )
        self.assertEqual(catalog["models"]["slug"]["output_cost_per_million"], 20)

    def test_fast_pricing_row_marks_has_fast_and_keeps_the_base_price(self):
        """A ``(Fast)`` row or a fast-mode note sets ``has_fast``. Cost stays base."""
        pricing = "\n".join(
            [
                "| Model | Output | Notes |",
                "| --- | --- | --- |",
                "| Widget | $10 | - |",
                "| Widget (Fast) | $40 | - |",
                "| Noted | $5 | Fast mode is available at 2x pricing |",
                "| Plain | $3 | - |",
            ]
        )
        catalog, warnings = build_catalog(
            _benchlm(
                {
                    "w": {"agentic": 1, "coding": 1, "reasoning": 1},
                    "n": {"agentic": 1, "coding": 1, "reasoning": 1},
                    "p": {"agentic": 1, "coding": 1, "reasoning": 1},
                }
            ),
            pricing,
            _mapping(
                {
                    "widget": {"family": "a", "pricing_name": "Widget", "benchlm_slug": "w"},
                    "noted": {"family": "b", "pricing_name": "Noted", "benchlm_slug": "n"},
                    "plain": {"family": "c", "pricing_name": "Plain", "benchlm_slug": "p"},
                }
            ),
            _previous(
                {
                    "widget": {"tier": "low"},
                    "noted": {"tier": "low"},
                    "plain": {"tier": "low"},
                }
            ),
        )
        self.assertEqual(catalog["models"]["widget"]["output_cost_per_million"], 10)
        self.assertTrue(catalog["models"]["widget"]["has_fast"])
        self.assertEqual(catalog["models"]["noted"]["output_cost_per_million"], 5)
        self.assertTrue(catalog["models"]["noted"]["has_fast"])
        self.assertFalse(catalog["models"]["plain"]["has_fast"])
        self.assertEqual(warnings, [])

    def test_missing_price_row_warns_and_stores_null(self):
        """A pricing name with no row leaves the cost null."""
        catalog, warnings = build_catalog(
            _benchlm({"m": {"agentic": 1, "coding": 1, "reasoning": 1}}),
            "| Model | Output |\n| --- | --- |\n| Other | $5 |\n",
            _mapping({"slug": {"family": "a", "pricing_name": "Missing", "benchlm_slug": "m"}}),
            _previous({"slug": {"tier": "low"}}),
        )
        self.assertIsNone(catalog["models"]["slug"]["output_cost_per_million"])
        self.assertIn("WARNING: must set cost for slug", warnings)

    def test_existing_tier_and_tier_order_survive_refresh(self):
        """An existing tier stays. A new slug is null and named on the warning."""
        catalog, warnings = build_catalog(
            _benchlm(
                {
                    "a": {"agentic": 1, "coding": 1, "reasoning": 1},
                    "b": {"agentic": 1, "coding": 1, "reasoning": 1},
                }
            ),
            "| Model | Output |\n| --- | --- |\n| A | $1 |\n| B | $2 |\n",
            _mapping(
                {
                    "kept": {"family": "a", "pricing_name": "A", "benchlm_slug": "a"},
                    "newcomer": {"family": "b", "pricing_name": "B", "benchlm_slug": "b"},
                }
            ),
            _previous({"kept": {"tier": "general"}}, tier_order=["general"]),
        )
        self.assertEqual(catalog["tier_order"], ["general"])
        self.assertEqual(catalog["models"]["kept"]["tier"], "general")
        self.assertIsNone(catalog["models"]["newcomer"]["tier"])
        self.assertIn("WARNING: must set tier for newcomer", warnings)
        self.assertNotIn("WARNING: must set tier for kept", warnings)

    def test_refresh_then_pick_follows_the_rank_rule(self):
        """A catalog built from fixtures selects the one eligible reviewer."""
        pricing = "\n".join(
            [
                "| Model | Output |",
                "| --- | --- |",
                "| Author | $5 |",
                "| Same | $1 |",
                "| Trap | $0.25 |",
                "| Gap | $1 |",
                "| Want | $3 |",
                "| Costly | $9 |",
            ]
        )
        mapping = _mapping(
            {
                "author": {"family": "grok", "pricing_name": "Author", "benchlm_slug": "author-m"},
                "same-best": {"family": "grok", "pricing_name": "Same", "benchlm_slug": "same-m"},
                "two-below": {"family": "gemini", "pricing_name": "Trap", "benchlm_slug": "trap-m"},
                "gap": {"family": "grok", "pricing_name": "Gap", "benchlm_slug": "gap-m"},
                "want": {"family": "claude", "pricing_name": "Want", "benchlm_slug": "want-m"},
                "costly": {"family": "kimi", "pricing_name": "Costly", "benchlm_slug": "costly-m"},
            }
        )

        def cats(score):
            return {"agentic": score, "coding": score, "reasoning": score}

        catalog, warnings = build_catalog(
            _benchlm(
                {
                    "author-m": cats(80),
                    "same-m": cats(90),
                    "trap-m": cats(10),
                    "gap-m": cats(50),
                    "want-m": cats(40),
                    "costly-m": cats(70),
                }
            ),
            pricing,
            mapping,
            {
                "tier_order": ["low", "high"],
                "models": {
                    "author": {"tier": "low"},
                    "same-best": {"tier": "low"},
                    "two-below": {"tier": "low"},
                    "gap": {"tier": "low"},
                    "want": {"tier": "high"},
                    "costly": {"tier": "high"},
                },
            },
        )
        self.assertEqual(warnings, [])
        slug = select(
            catalog,
            mapping,
            "author",
            ["author", "same-best", "two-below", "gap", "want", "costly"],
            random.Random(1),
        )
        self.assertEqual(slug, "want")


_SCORED = {"agentic": 70, "coding": 70, "reasoning": 70}
_UNSCORED = {"agentic": None, "coding": None, "reasoning": None}


def _listing(rows):
    body = "\n".join(f"{slug} - {name}" for slug, name in rows)
    return (
        "Available models\n\nauto - Auto (default)\n"
        f"{body}\n\n"
        "Tip: use --model <id> (or /model <id> in interactive mode) to switch.\n"
    )


def _pricing(names):
    lines = ["| Model | Output |", "| --- | --- |"]
    lines += [f"| {name} | $5 |" for name in names]
    return "\n".join(lines) + "\n"


def _fill(rows, pricing_names, bench, mapping=None):
    return fill_mapping(
        _listing(rows),
        mapping if mapping is not None else {"models": {}},
        _pricing(pricing_names),
        _benchlm(bench),
    )


class FillTests(unittest.TestCase):
    """Refresh fills in mapping rows for listed models that lack one."""

    def test_listing_parses_to_stems(self):
        """Header, blanks, auto, and the tip line are not rows; efforts collapse to one stem."""
        listed = parse_listing(
            _listing(
                [
                    ("grok-4.7-low", "Grok 4.7  Low"),
                    ("grok-4.7-low-fast", "Grok 4.7  Low Fast"),
                    ("grok-4.7-xhigh", "Grok 4.7  Extra High"),
                    ("claude-4.6-opus-high-thinking", "Claude Opus 4.6 1M Thinking"),
                    ("gpt-5.2", "GPT-5.2"),
                ]
            )
        )
        self.assertEqual(
            list(listed.items()),
            [
                ("grok-4.7", "Grok 4.7  Low"),
                ("claude-4.6-opus-thinking", "Claude Opus 4.6 1M Thinking"),
                ("gpt-5.2", "GPT-5.2"),
            ],
        )

    def test_price_matches_words_in_any_order(self):
        """Claude Opus 4.6 1M matches the pricing row Claude 4.6 Opus."""
        mapping, warnings = _fill(
            [("claude-4.6-opus-high", "Claude Opus 4.6 1M")],
            ["Claude 4.6 Opus"],
            {"claude-opus-4-6": _SCORED},
        )
        self.assertEqual(warnings, [])
        self.assertEqual(mapping["models"]["claude-4.6-opus"]["pricing_name"], "Claude 4.6 Opus")

    def test_family_word_counts_toward_the_price_match(self):
        """Codex 5.3 Low on stem gpt-5.3-codex matches GPT-5.3 Codex."""
        mapping, warnings = _fill(
            [("gpt-5.3-codex-low", "Codex 5.3 Low")],
            ["GPT-5.3 Codex"],
            {"gpt-5-3-codex": _SCORED},
        )
        self.assertEqual(warnings, [])
        self.assertEqual(mapping["models"]["gpt-5.3-codex"]["pricing_name"], "GPT-5.3 Codex")

    def test_most_words_wins(self):
        """GPT-5 Mini beats GPT-5; Claude Opus 5 does not match Claude Opus 5.5."""
        mapping, warnings = _fill(
            [
                ("gpt-5-mini", "GPT-5 Mini"),
                ("claude-opus-5-5-low", "Claude Opus 5.5 1M Low"),
            ],
            ["GPT-5", "GPT-5 Mini", "Claude Opus 5", "Claude Opus 5.5"],
            {"gpt-5-mini": _SCORED, "claude-opus-5-5": _SCORED},
        )
        self.assertEqual(warnings, [])
        self.assertEqual(mapping["models"]["gpt-5-mini"]["pricing_name"], "GPT-5 Mini")
        self.assertEqual(mapping["models"]["claude-opus-5-5"]["pricing_name"], "Claude Opus 5.5")

    def test_parenthesized_pricing_rows_are_ignored(self):
        """Fast and fast-mode pricing rows are never a pricing_name."""
        mapping, warnings = _fill(
            [
                ("cursor-grok-4.6-high-fast", "Grok 4.6 Fast"),
                ("claude-opus-4-7-high-fast", "Claude Opus 4.7 1M High Fast"),
            ],
            ["Grok 4.6 (Fast)", "Grok 4.6", "Claude Opus 4.7 (fast mode)", "Claude 4.7 Opus"],
            {"grok-4-6": _SCORED, "claude-opus-4-7": _SCORED},
        )
        self.assertEqual(warnings, [])
        self.assertEqual(mapping["models"]["cursor-grok-4.6"]["pricing_name"], "Grok 4.6")
        self.assertEqual(mapping["models"]["claude-opus-4-7"]["pricing_name"], "Claude 4.7 Opus")

    def test_benchlm_match_uses_the_same_words(self):
        """Claude 4.6 Opus matches claude-opus-4-6; word counts must agree."""
        mapping, warnings = _fill(
            [
                ("claude-4.6-opus-high", "Claude Opus 4.6 1M"),
                ("claude-opus-5-low", "Claude Opus 5 1M Low"),
            ],
            ["Claude 4.6 Opus", "Claude Opus 5"],
            {"claude-opus-4-6": _SCORED, "claude-opus-5-5": _SCORED},
        )
        self.assertEqual(mapping["models"]["claude-4.6-opus"]["benchlm_slug"], "claude-opus-4-6")
        self.assertNotIn("claude-opus-5", mapping["models"])
        self.assertEqual(
            warnings, ["WARNING: unrecognized model claude-opus-5: no BenchLM score"]
        )

    def test_unscored_benchlm_item_is_not_a_match(self):
        """A BenchLM item with no category scores is ignored."""
        mapping, warnings = _fill(
            [("claude-fable-5-low", "Claude Fable 5 1M Low (NO ZDR)")],
            ["Claude Fable 5"],
            {"claude-fable-5": _UNSCORED},
        )
        self.assertNotIn("claude-fable-5", mapping["models"])
        self.assertEqual(
            warnings, ["WARNING: unrecognized model claude-fable-5: no BenchLM score"]
        )

    def test_ambiguous_benchlm_match_is_not_added(self):
        """Two scored slugs with the same words: no row, a warning naming the stem."""
        mapping, warnings = _fill(
            [("glm-5.2-high", "GLM 5.2")],
            ["GLM 5.2"],
            {"glm-5-2": _SCORED, "glm-5.2": _SCORED},
        )
        self.assertNotIn("glm-5.2", mapping["models"])
        self.assertEqual(
            warnings, ["WARNING: unrecognized model glm-5.2: ambiguous BenchLM match"]
        )

    def test_family_is_the_first_word_after_cursor_prefix(self):
        """cursor-grok-4.5 is grok; muse-spark-1.3 is muse; kimi-k2.7-code is kimi."""
        mapping, warnings = _fill(
            [
                ("cursor-grok-4.5-high", "Grok 4.5"),
                ("muse-spark-1.3-high", "Muse Spark 1.3 1M"),
                ("kimi-k2.7-code", "Kimi K2.7 Code"),
            ],
            ["Grok 4.5", "Muse Spark 1.3", "Kimi K2.7 Code"],
            {"grok-4-5": _SCORED, "muse-spark-1-3": _SCORED, "kimi-k2-7-code": _SCORED},
        )
        self.assertEqual(warnings, [])
        families = {stem: row["family"] for stem, row in mapping["models"].items()}
        self.assertEqual(
            families,
            {"cursor-grok-4.5": "grok", "muse-spark-1.3": "muse", "kimi-k2.7-code": "kimi"},
        )

    def test_thinking_stem_shares_the_model(self):
        """A thinking stem and its bare stem get the same pricing row and BenchLM slug."""
        mapping, warnings = _fill(
            [
                ("claude-opus-5-low", "Claude Opus 5 1M Low"),
                ("claude-opus-5-thinking-high", "Claude Opus 5 1M Thinking"),
            ],
            ["Claude Opus 5"],
            {"claude-opus-5": _SCORED},
        )
        self.assertEqual(warnings, [])
        bare = mapping["models"]["claude-opus-5"]
        thinking = mapping["models"]["claude-opus-5-thinking"]
        self.assertEqual(bare, thinking)
        self.assertEqual(bare["benchlm_slug"], "claude-opus-5")

    def test_new_row_shape_and_order(self):
        """An added row has four keys and comes after the existing rows."""
        existing = _mapping(
            {"grok-4.7": {"family": "grok", "pricing_name": "Grok 4.7", "benchlm_slug": "grok-4-7"}}
        )
        mapping, warnings = _fill(
            [("grok-4.7-low", "Grok 4.7  Low"), ("gpt-5.2", "GPT-5.2")],
            ["Grok 4.7", "GPT-5.2"],
            {"grok-4-7": _SCORED, "gpt-5-2": _SCORED},
            mapping=existing,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(list(mapping["models"]), ["grok-4.7", "gpt-5.2"])
        self.assertEqual(
            mapping["models"]["gpt-5.2"],
            {
                "family": "gpt",
                "pricing_name": "GPT-5.2",
                "benchlm_slug": "gpt-5-2",
                "interim_score": None,
            },
        )

    def test_unrecognized_stems_are_warned_not_added(self):
        """No pricing row, or no scored BenchLM match: no row and a warning."""
        mapping, warnings = _fill(
            [("gpt-5.1-low", "GPT-5.1 Low"), ("gpt-5-mini", "GPT-5 Mini")],
            ["GPT-5.1 Codex", "GPT-5 Mini"],
            {"gpt-5-1-codex": _SCORED},
        )
        self.assertEqual(mapping["models"], {})
        self.assertEqual(
            warnings,
            [
                "WARNING: unrecognized model gpt-5.1: no pricing row",
                "WARNING: unrecognized model gpt-5-mini: no BenchLM score",
            ],
        )

    def test_existing_rows_are_untouched(self):
        """A mapped stem keeps its row; a mapped stem absent from the listing stays."""
        existing = _mapping(
            {
                "grok-4.7": {"family": "hand", "pricing_name": "Hand Name", "benchlm_slug": "hand"},
                "unlisted": {"family": "x", "pricing_name": "X", "benchlm_slug": "x"},
            }
        )
        before = json.loads(json.dumps(existing))
        mapping, warnings = _fill(
            [("grok-4.7-low", "Grok 4.7  Low")],
            ["Grok 4.7"],
            {"grok-4-7": _SCORED},
            mapping=existing,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(mapping, before)
        self.assertEqual(existing, before)

    def test_refresh_fills_in_rows(self):
        """refresh.main writes the filled mapping and a null-tier catalog row next to dest."""
        existing = _mapping(
            {"grok-4.7": {"family": "grok", "pricing_name": "Grok 4.7", "benchlm_slug": "grok-4-7"}}
        )
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "catalog.json"
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = refresh_main(
                    [],
                    benchlm=_benchlm({"grok-4-7": _SCORED, "gpt-5-2": _SCORED}),
                    pricing_markdown=_pricing(["Grok 4.7", "GPT-5.2"]),
                    mapping=existing,
                    tiers={"A": ["grok-4.7"]},
                    dest=dest,
                    agent_models=_listing(
                        [("grok-4.7-low", "Grok 4.7  Low"), ("gpt-5.2", "GPT-5.2"), ("gpt-5.1", "GPT-5.1")]
                    ),
                )
            written_mapping = json.loads((Path(tmp) / "mapping.json").read_text(encoding="utf-8"))
            written_catalog = json.loads(dest.read_text(encoding="utf-8"))
        self.assertEqual(code, 0)
        self.assertEqual(list(written_mapping["models"]), ["grok-4.7", "gpt-5.2"])
        self.assertIsNone(written_catalog["models"]["gpt-5.2"]["tier"])
        self.assertEqual(written_catalog["models"]["grok-4.7"]["tier"], "A")
        lines = stderr.getvalue().splitlines()
        self.assertIn("WARNING: must set tier for gpt-5.2", lines)
        self.assertIn("WARNING: unrecognized model gpt-5.1: no pricing row", lines)

    def test_null_tier_in_previous_still_warns(self):
        """A row whose previous tier is null gets the tier warning again, once."""
        _catalog, warnings = build_catalog(
            _benchlm({"m": _SCORED}),
            _pricing(["Row"]),
            _mapping({"m": {"family": "a", "pricing_name": "Row", "benchlm_slug": "m"}}),
            _previous({"m": {"tier": None}}),
        )
        self.assertEqual(warnings, ["WARNING: must set tier for m"])

    def test_listing_fast_spelling_sets_has_fast(self):
        """No (Fast) pricing row, but the listing has a -fast spelling: has_fast is true."""
        catalog, _warnings = build_catalog(
            _benchlm({"m": _SCORED}),
            _pricing(["Row"]),
            _mapping({"m": {"family": "a", "pricing_name": "Row", "benchlm_slug": "m"}}),
            _previous({"m": {"tier": "low"}}),
            listing=_listing([("m-high", "Row High"), ("m-high-fast", "Row High Fast")]),
        )
        self.assertTrue(catalog["models"]["m"]["has_fast"])

    def test_listing_without_fast_spelling_clears_has_fast(self):
        """A (Fast) pricing row, but the listing has no -fast spelling: has_fast is false."""
        catalog, _warnings = build_catalog(
            _benchlm({"m": _SCORED}),
            _pricing(["Row", "Row (Fast)"]),
            _mapping({"m": {"family": "a", "pricing_name": "Row", "benchlm_slug": "m"}}),
            _previous({"m": {"tier": "low"}}),
            listing=_listing([("m-high", "Row High")]),
        )
        self.assertFalse(catalog["models"]["m"]["has_fast"])

    def test_unlisted_stem_keeps_pricing_has_fast(self):
        """A stem absent from the listing is decided by the pricing page."""
        catalog, _warnings = build_catalog(
            _benchlm({"m": _SCORED, "n": _SCORED}),
            _pricing(["Row", "Row (Fast)", "Other"]),
            _mapping(
                {
                    "m": {"family": "a", "pricing_name": "Row", "benchlm_slug": "m"},
                    "n": {"family": "b", "pricing_name": "Other", "benchlm_slug": "n"},
                }
            ),
            _previous({"m": {"tier": "low"}, "n": {"tier": "low"}}),
            listing=_listing([("x-high-fast", "X Fast")]),
        )
        self.assertTrue(catalog["models"]["m"]["has_fast"])
        self.assertFalse(catalog["models"]["n"]["has_fast"])

    def test_refresh_uses_the_listing_for_has_fast(self):
        """refresh.main passes its listing to the catalog build; False falls back to pricing."""
        written = {}
        for label, agent_models in (
            ("listing", _listing([("m-high", "Row High"), ("m-high-fast", "Row High Fast")])),
            ("none", False),
        ):
            with tempfile.TemporaryDirectory() as tmp:
                dest = Path(tmp) / "catalog.json"
                with redirect_stderr(io.StringIO()):
                    refresh_main(
                        [],
                        benchlm=_benchlm({"m": _SCORED}),
                        pricing_markdown=_pricing(["Row"]),
                        mapping=_mapping(
                            {"m": {"family": "a", "pricing_name": "Row", "benchlm_slug": "m"}}
                        ),
                        tiers={"C": ["m"]},
                        dest=dest,
                        agent_models=agent_models,
                    )
                written[label] = json.loads(dest.read_text(encoding="utf-8"))
        self.assertTrue(written["listing"]["models"]["m"]["has_fast"])
        self.assertFalse(written["none"]["models"]["m"]["has_fast"])

    def test_refresh_without_agent_listing_warns_once(self):
        """agent_models=False: one skip warning, mapping unchanged, catalog written."""
        existing = _mapping(
            {"grok-4.7": {"family": "grok", "pricing_name": "Grok 4.7", "benchlm_slug": "grok-4-7"}}
        )
        before = json.loads(json.dumps(existing))
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "catalog.json"
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = refresh_main(
                    [],
                    benchlm=_benchlm({"grok-4-7": _SCORED}),
                    pricing_markdown=_pricing(["Grok 4.7"]),
                    mapping=existing,
                    tiers={"A": ["grok-4.7"]},
                    dest=dest,
                    agent_models=False,
                )
            written_mapping = json.loads((Path(tmp) / "mapping.json").read_text(encoding="utf-8"))
            catalog_written = dest.exists()
        self.assertEqual(code, 0)
        self.assertTrue(catalog_written)
        self.assertEqual(written_mapping, before)
        self.assertEqual(
            stderr.getvalue().splitlines(),
            ["WARNING: agent --list-models unavailable; skipped model fill-in"],
        )


class TiersTests(unittest.TestCase):
    """Tiers come from the hand-edited tiers.toml, parsed by refresh."""

    _MAPPING = _mapping(
        {
            stem: {"family": "f", "pricing_name": "Row", "benchlm_slug": "m"}
            for stem in ("a", "b", "c")
        }
    )

    def test_tiers_from_toml_use_model_key_and_the_fixed_order(self):
        """Listed spellings collapse to stems; tier_order is C, B, A, S."""
        previous, warnings = previous_from_tiers(
            {"S": ["a"], "A": ["b-high-fast"]}, self._MAPPING
        )
        self.assertEqual(warnings, [])
        self.assertEqual(previous["tier_order"], ["C", "B", "A", "S"])
        self.assertEqual(previous["models"], {"a": {"tier": "S"}, "b": {"tier": "A"}})

    def test_never_is_a_tier_value_outside_the_order(self):
        """A stem under never gets tier never, which is not on the ladder."""
        previous, warnings = previous_from_tiers({"never": ["c"]}, self._MAPPING)
        self.assertEqual(warnings, [])
        self.assertEqual(previous["models"], {"c": {"tier": "never"}})
        self.assertNotIn("never", previous["tier_order"])

    def test_unknown_tier_key_warns(self):
        """A key that is not S, A, B, C, or never warns and tiers nothing."""
        previous, warnings = previous_from_tiers({"Z": ["a"]}, self._MAPPING)
        self.assertEqual(previous["models"], {})
        self.assertEqual(warnings, ["WARNING: unknown tier Z in tiers.toml"])

    def test_non_list_tier_value_warns_and_is_skipped(self):
        """A scalar under a tier key is not read character by character; it warns and tiers nothing."""
        previous, warnings = previous_from_tiers(
            {"S": "a", "A": ["b"]}, self._MAPPING
        )
        self.assertEqual(previous["models"], {"b": {"tier": "A"}})
        self.assertEqual(
            warnings, ["WARNING: tier S in tiers.toml must be a list of slugs; skipped"]
        )

    def test_stem_listed_twice_warns_and_keeps_the_first(self):
        """The same stem under two tiers warns and keeps the first listing."""
        previous, warnings = previous_from_tiers(
            {"S": ["a"], "A": ["a-low"]}, self._MAPPING
        )
        self.assertEqual(previous["models"], {"a": {"tier": "S"}})
        self.assertEqual(
            warnings, ["WARNING: a is listed under S and A in tiers.toml; using S"]
        )

    def test_listed_stem_missing_from_mapping_warns(self):
        """A listed stem that mapping lacks warns."""
        _previous_doc, warnings = previous_from_tiers({"B": ["x"]}, self._MAPPING)
        self.assertEqual(
            warnings, ["WARNING: tiers.toml lists x, which is not in mapping"]
        )

    def test_refresh_reads_tiers_and_never_writes_them(self):
        """refresh.main tiers the catalog from tiers; never rows do not warn; no tiers.toml is written."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "catalog.json"
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = refresh_main(
                    [],
                    benchlm=_benchlm({"m": _SCORED}),
                    pricing_markdown=_pricing(["Row"]),
                    mapping=self._MAPPING,
                    tiers={"S": ["a"], "never": ["c"]},
                    dest=dest,
                    agent_models=_listing([]),
                )
            catalog = json.loads(dest.read_text(encoding="utf-8"))
            wrote_tiers = (Path(tmp) / "tiers.toml").exists()
        self.assertEqual(code, 0)
        self.assertFalse(wrote_tiers)
        self.assertEqual(catalog["tier_order"], ["C", "B", "A", "S"])
        tiers = {stem: entry["tier"] for stem, entry in catalog["models"].items()}
        self.assertEqual(tiers, {"a": "S", "b": None, "c": "never"})
        self.assertEqual(stderr.getvalue().splitlines(), ["WARNING: must set tier for b"])
