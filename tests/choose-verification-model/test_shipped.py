"""Invariants of the catalog and mapping that ship with the skill.

Numeric scores are not locked. A refresh may change them.
"""

import io
import json
import os
import random
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
ASSETS = SKILL_DIR / "assets"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from modelpool import model_key, select  # noqa: E402
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
    "gemini-4-argon-medium",
)

# Enabled only some of the time. They still have to be in the catalog
# so a reviewer list that includes them can place them.
SOMETIMES = (
    "claude-fable-5-1-thinking-high",
    "gpt-5.6-sol-medium",
    "gpt-5.6-luna-medium",
    "claude-haiku-5-5-low",
    "claude-haiku-5-5-thinking-low",
)

REQUIRED_CATALOG_KEYS = (
    "tier",
    "score",
    "score_source",
    "effort_encoded",
    "output_cost_per_million",
)


def _load(name):
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))


class ShippedTests(unittest.TestCase):
    def test_catalog_and_mapping_share_slugs(self):
        """Every mapping slug is a catalog slug, including the sometimes-enabled ones."""
        mapping = _load("mapping.json")
        catalog = _load("catalog.json")
        self.assertLessEqual(set(mapping["models"]), set(catalog["models"]))
        for slug in SPAWNABLE + SOMETIMES:
            key = model_key(slug)
            self.assertEqual(model_key(key), key)
            self.assertIn(key, mapping["models"])
            self.assertIn(key, catalog["models"])

    def test_catalog_entries_have_required_keys(self):
        """Catalog entries have the schema keys. Families are non-empty.

        The ladder is C, B, A, S from lowest to highest. Each shipped
        slug has a score and a tier on that ladder, or the tier never.
        The letters themselves are hand-assigned and are not locked.
        """
        mapping = _load("mapping.json")
        catalog = _load("catalog.json")
        self.assertEqual(catalog["tier_order"], ["C", "B", "A", "S"])
        ladder = set(catalog["tier_order"]) | {"never"}
        for slug, entry in catalog["models"].items():
            self.assertEqual(model_key(slug), slug)
            for key in REQUIRED_CATALOG_KEYS:
                self.assertIn(key, entry)
            self.assertIn(entry["tier"], ladder)
            self.assertFalse(entry["effort_encoded"])
        for entry in mapping["models"].values():
            family = entry.get("family")
            self.assertIsInstance(family, str)
            self.assertTrue(family)
        for slug in SPAWNABLE + SOMETIMES:
            entry = catalog["models"][model_key(slug)]
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

        The author is the fast half of cursor-grok-4.6. The reviewer
        effort is the one on the Opus candidate. Numeric scores are
        not locked.
        """
        path = ASSETS / "catalog.json"
        before = path.read_bytes()
        stdout = io.StringIO()
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as empty_home:
            previous = os.environ.get("XDG_DATA_HOME")
            os.environ["XDG_DATA_HOME"] = empty_home
            try:
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
            finally:
                if previous is None:
                    os.environ.pop("XDG_DATA_HOME", None)
                else:
                    os.environ["XDG_DATA_HOME"] = previous
        self.assertEqual(code, 0)
        self.assertEqual(stderr.getvalue().strip(), "")
        self.assertEqual(stdout.getvalue().strip(), "claude-opus-5-5-high-fast")
        self.assertEqual(path.read_bytes(), before)

    def test_sol_author_prints_gemini_4_argon(self):
        """A Sol author prints Argon, so this row is tier A."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "gpt-5.6-sol-medium",
            ["gpt-5.6-sol-medium", "gemini-4-argon-medium"],
            random.Random(0),
        )
        self.assertEqual(slug, "gemini-4-argon-medium")

    def test_opus_author_does_not_select_gemini_4_argon(self):
        """Opus stays Opus, so Argon is not tier S."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "claude-opus-5-5-medium",
            ["claude-opus-5-5-medium", "gemini-4-argon-medium"],
            random.Random(0),
        )
        self.assertEqual(slug, "claude-opus-5-5-medium")

    def test_gemini_3_8_flash_does_not_select_gemini_4_argon(self):
        """Two Gemini rows do not review each other."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "gemini-3.8-flash-high",
            ["gemini-3.8-flash-high", "gemini-4-argon-medium"],
            random.Random(0),
        )
        self.assertEqual(slug, "gemini-3.8-flash-high")

    def test_fast_sol_author_prints_gemini_4_argon_without_fast(self):
        """A fast Sol author prints Argon without -fast."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "gpt-5.6-sol-medium-fast",
            ["gpt-5.6-sol-medium", "gemini-4-argon-medium"],
            random.Random(0),
        )
        self.assertEqual(slug, "gemini-4-argon-medium")

    def test_composer_author_prints_claude_haiku_5_5(self):
        """A Composer author prints Haiku 5.5, so this row is tier C."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "composer-2.5",
            ["composer-2.5", "claude-haiku-5-5-low"],
            random.Random(0),
        )
        self.assertEqual(slug, "claude-haiku-5-5-low")

    def test_terra_author_does_not_select_claude_haiku_5_5(self):
        """Terra stays Terra, so Haiku 5.5 is not tier B or A."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "gpt-5.6-terra-medium",
            ["gpt-5.6-terra-medium", "claude-haiku-5-5-low"],
            random.Random(0),
        )
        self.assertEqual(slug, "gpt-5.6-terra-medium")

    def test_fast_composer_author_prints_claude_haiku_5_5_without_fast(self):
        """A fast Composer author prints Haiku 5.5 without -fast."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "composer-2.5-fast",
            ["composer-2.5", "claude-haiku-5-5-low"],
            random.Random(0),
        )
        self.assertEqual(slug, "claude-haiku-5-5-low")

    def test_composer_author_prints_claude_haiku_5_5_thinking(self):
        """A Composer author prints thinking Haiku 5.5, so this row is tier C."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "composer-2.5",
            ["composer-2.5", "claude-haiku-5-5-thinking-low"],
            random.Random(0),
        )
        self.assertEqual(slug, "claude-haiku-5-5-thinking-low")

    def test_terra_author_does_not_select_claude_haiku_5_5_thinking(self):
        """Terra stays Terra, so thinking Haiku 5.5 is not tier B or A."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "gpt-5.6-terra-medium",
            ["gpt-5.6-terra-medium", "claude-haiku-5-5-thinking-low"],
            random.Random(0),
        )
        self.assertEqual(slug, "gpt-5.6-terra-medium")

    def test_fast_composer_author_prints_claude_haiku_5_5_thinking_without_fast(self):
        """A fast Composer author prints thinking Haiku 5.5 without -fast."""
        slug = select(
            _load("catalog.json"),
            _load("mapping.json"),
            "composer-2.5-fast",
            ["composer-2.5", "claude-haiku-5-5-thinking-low"],
            random.Random(0),
        )
        self.assertEqual(slug, "claude-haiku-5-5-thinking-low")
