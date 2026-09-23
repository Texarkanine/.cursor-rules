"""Invariants of the catalog and mapping that ship with the skill.

Numeric scores are not locked. A refresh may change them.
"""

import json
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
sys.path.insert(0, str(SKILL_DIR))

SPAWNABLE = (
    "claude-opus-5-5-medium",
    "claude-sonnet-5-thinking-high",
    "composer-2.5",
    "composer-2.5-fast",
    "gemini-3.8-flash-high",
    "gpt-5.6-terra-medium",
    "grok-4.7-high",
    "kimi-k3-high",
    "muse-spark-1.3-high",
)

REQUIRED_CATALOG_KEYS = ("tier", "score", "score_source", "output_cost_per_million")


def _load(name):
    return json.loads((SKILL_DIR / name).read_text(encoding="utf-8"))


class ShippedTests(unittest.TestCase):
    def test_catalog_and_mapping_share_slugs(self):
        """Every mapping slug is a catalog slug, including the nine spawnable slugs."""
        mapping = _load("mapping.json")
        catalog = _load("catalog.json")
        self.assertLessEqual(set(mapping["models"]), set(catalog["models"]))
        for slug in SPAWNABLE:
            self.assertIn(slug, mapping["models"])
            self.assertIn(slug, catalog["models"])

    def test_catalog_entries_have_required_keys(self):
        """Catalog entries have the schema keys. Families are non-empty.

        Each spawnable slug has a score and tier ``general``.
        """
        mapping = _load("mapping.json")
        catalog = _load("catalog.json")
        for entry in catalog["models"].values():
            for key in REQUIRED_CATALOG_KEYS:
                self.assertIn(key, entry)
        for entry in mapping["models"].values():
            family = entry.get("family")
            self.assertIsInstance(family, str)
            self.assertTrue(family)
        for slug in SPAWNABLE:
            entry = catalog["models"][slug]
            self.assertEqual(entry["tier"], "general")
            self.assertIsNotNone(entry["score"])
