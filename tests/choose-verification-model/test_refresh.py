"""Catalog refresh behavior, including a refresh-then-pick case.

Fixtures stand in for the BenchLM document and the pricing page.
Nothing in this module opens a network connection.
"""

import random
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from modelpool import build_catalog, select  # noqa: E402


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
