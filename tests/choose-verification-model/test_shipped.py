"""Invariants of the catalog and mapping that ship with the skill.

Numeric scores are not locked. A refresh may change them.
"""

import io
import json
import random
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
ASSETS = SKILL_DIR / "assets"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from modelpool import select  # noqa: E402
from pick import main  # noqa: E402

SPAWNABLE = (
    "claude-opus-5-5-medium",
    "claude-sonnet-5-thinking-high",
    "composer-2.5",
    "gemini-3.8-flash-high",
    "gpt-5.6-terra-medium",
    "cursor-grok-4.6-xhigh",
    "grok-4.7-high",
    "kimi-k3-high",
    "muse-spark-1.3-high",
)

# Enabled only some of the time. They still have to be in the catalog
# so a reviewer list that includes them does not exit 2.
SOMETIMES = (
    "claude-fable-5-1-thinking-high",
    "gpt-5.6-sol-medium",
    "gpt-5.6-luna-medium",
)

REQUIRED_CATALOG_KEYS = ("tier", "score", "score_source", "output_cost_per_million")


def _load(name):
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))


class ShippedTests(unittest.TestCase):
    def test_catalog_and_mapping_share_slugs(self):
        """Every mapping slug is a catalog slug, including the sometimes-enabled ones."""
        mapping = _load("mapping.json")
        catalog = _load("catalog.json")
        self.assertLessEqual(set(mapping["models"]), set(catalog["models"]))
        for slug in SPAWNABLE + SOMETIMES:
            self.assertIn(slug, mapping["models"])
            self.assertIn(slug, catalog["models"])

    def test_catalog_entries_have_required_keys(self):
        """Catalog entries have the schema keys. Families are non-empty.

        The ladder is C, B, A, S from lowest to highest. Each shipped
        slug has a score and a tier on that ladder. The letters
        themselves are hand-assigned and are not locked.
        """
        mapping = _load("mapping.json")
        catalog = _load("catalog.json")
        self.assertEqual(catalog["tier_order"], ["C", "B", "A", "S"])
        ladder = set(catalog["tier_order"])
        for entry in catalog["models"].values():
            for key in REQUIRED_CATALOG_KEYS:
                self.assertIn(key, entry)
            self.assertIn(entry["tier"], ladder)
        for entry in mapping["models"].values():
            family = entry.get("family")
            self.assertIsInstance(family, str)
            self.assertTrue(family)
        for slug in SPAWNABLE + SOMETIMES:
            entry = catalog["models"][slug]
            self.assertIsNotNone(entry["score"])

    def test_fast_sol_author_prints_cursor_grok_4_6_fast(self):
        """A fast Sol author prints this row with -fast."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "gpt-5.6-sol-medium-fast",
            ["gpt-5.6-sol-medium", "cursor-grok-4.6-xhigh"],
            random.Random(0),
        )
        self.assertEqual(slug, "cursor-grok-4.6-xhigh-fast")

    def test_sol_author_prints_cursor_grok_4_6_without_fast(self):
        """A non-fast Sol author prints this row without -fast."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "gpt-5.6-sol-medium",
            ["gpt-5.6-sol-medium", "cursor-grok-4.6-xhigh"],
            random.Random(0),
        )
        self.assertEqual(slug, "cursor-grok-4.6-xhigh")

    def test_opus_author_does_not_select_cursor_grok_4_6(self):
        """Opus stays Opus, so this row is not tier S."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "claude-opus-5-5-medium",
            ["claude-opus-5-5-medium", "cursor-grok-4.6-xhigh"],
            random.Random(0),
        )
        self.assertEqual(slug, "claude-opus-5-5-medium")

    def test_grok_4_7_does_not_select_cursor_grok_4_6(self):
        """Two grok rows do not review each other."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "grok-4.7-high",
            ["grok-4.7-high", "cursor-grok-4.6-xhigh"],
            random.Random(0),
        )
        self.assertEqual(slug, "grok-4.7-high")

    def test_issue_129_command_exits_0_and_leaves_the_catalog(self):
        """An effort-variant argv exits 0 and does not rewrite the catalog.

        The printed slug is one of the spellings the caller passed, plus
        the fast suffix the picker already appends. Numeric scores are
        not locked.
        """
        path = ASSETS / "catalog.json"
        before = path.read_bytes()
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(
                [
                    "--model",
                    "cursor-grok-4.6-xhigh-fast",
                    "--reviewer-models",
                    "claude-opus-5-5-high,gpt-5.6-terra-medium,grok-4.7-xhigh",
                    "--seed",
                    "0",
                ]
            )
        self.assertEqual(code, 0)
        self.assertEqual(stderr.getvalue().strip(), "")
        self.assertIn(
            stdout.getvalue().strip(),
            {
                "claude-opus-5-5-high",
                "claude-opus-5-5-high-fast",
                "gpt-5.6-terra-medium",
                "gpt-5.6-terra-medium-fast",
                "grok-4.7-xhigh",
                "grok-4.7-xhigh-fast",
                "cursor-grok-4.6-xhigh",
                "cursor-grok-4.6-xhigh-fast",
            },
        )
        self.assertEqual(path.read_bytes(), before)
