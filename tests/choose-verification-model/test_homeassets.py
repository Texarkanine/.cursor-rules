"""Home-directory overlay for choose-verification-model assets.

Directory resolution, the source-tree check, and the per-model merge.
Nothing in this module opens a network connection.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from homeassets import (  # noqa: E402
    is_source_tree,
    load_effective,
    merge_documents,
    user_assets_dir,
)


def _row(tier, score=1, has_fast=False, cost=1):
    return {
        "tier": tier,
        "score": score,
        "score_source": "benchlm",
        "effort_encoded": False,
        "output_cost_per_million": cost,
        "has_fast": has_fast,
    }


def _catalog(models, tier_order=("C", "B", "A", "S")):
    return {"tier_order": list(tier_order), "models": models}


def _mapping(families):
    return {"models": {stem: {"family": family} for stem, family in families.items()}}


class UserAssetsDirTests(unittest.TestCase):
    def test_xdg_data_home_wins(self):
        """A set, non-empty XDG_DATA_HOME is the directory's parent."""
        got = user_assets_dir(
            {"XDG_DATA_HOME": "/data"}, home=Path("/home/u"), platform="linux"
        )
        self.assertEqual(got, Path("/data/choose-verification-model"))

    def test_unset_or_empty_xdg_uses_home_share(self):
        """No XDG_DATA_HOME uses ~/.local/share under the given home."""
        for environ in ({}, {"XDG_DATA_HOME": ""}):
            with self.subTest(environ=environ):
                got = user_assets_dir(environ, home=Path("/home/u"), platform="linux")
                self.assertEqual(
                    got, Path("/home/u/.local/share/choose-verification-model")
                )

    def test_windows_without_xdg_uses_localappdata(self):
        """Platform nt with no XDG_DATA_HOME uses LOCALAPPDATA."""
        got = user_assets_dir(
            {"LOCALAPPDATA": "/local"}, home=Path("/home/u"), platform="nt"
        )
        self.assertEqual(got, Path("/local/choose-verification-model"))


class SourceTreeTests(unittest.TestCase):
    def test_rules_parent_is_the_source_tree(self):
        """rules/choose-verification-model is the publish tree."""
        self.assertTrue(is_source_tree(Path("rules/choose-verification-model")))

    def test_other_parent_is_not_the_source_tree(self):
        """An install whose parent is ai-rizz is a consumer tree."""
        self.assertFalse(is_source_tree(Path("ai-rizz/choose-verification-model")))


class MergeTests(unittest.TestCase):
    def test_mapping_union_home_replaces_and_adds(self):
        """Home mapping replaces a shared stem and contributes a new one."""
        _catalog_doc, mapping = merge_documents(
            _catalog({"a": _row("C"), "b": _row("C")}),
            _mapping({"a": "ship", "b": "ship"}),
            None,
            _mapping({"b": "home", "c": "home"}),
            None,
        )
        self.assertEqual(mapping["models"]["a"]["family"], "ship")
        self.assertEqual(mapping["models"]["b"]["family"], "home")
        self.assertEqual(mapping["models"]["c"]["family"], "home")

    def test_shared_catalog_stem_keeps_shipped_tier(self):
        """Home score and has_fast win. The shipped tier is restored."""
        catalog, _mapping_doc = merge_documents(
            _catalog({"b": _row("C", score=1, has_fast=False, cost=9)}),
            _mapping({"b": "b"}),
            _catalog({"b": _row("S", score=8, has_fast=True, cost=2)}),
            None,
            None,
        )
        row = catalog["models"]["b"]
        self.assertEqual(row["tier"], "C")
        self.assertEqual(row["score"], 8)
        self.assertTrue(row["has_fast"])
        self.assertEqual(row["output_cost_per_million"], 2)

    def test_home_only_catalog_row_keeps_its_tier(self):
        """A stem that exists only in the home catalog is kept, tier included."""
        catalog, _mapping_doc = merge_documents(
            _catalog({"a": _row("C")}),
            _mapping({"a": "a"}),
            _catalog({"c": _row("S", score=4, has_fast=True)}),
            None,
            None,
        )
        self.assertEqual(catalog["models"]["c"], _row("S", score=4, has_fast=True))

    def test_shipped_only_catalog_row_is_kept(self):
        """A stem that exists only in the shipped catalog is kept."""
        shipped_row = _row("B", score=3, has_fast=False, cost=6)
        catalog, _mapping_doc = merge_documents(
            _catalog({"a": shipped_row}),
            _mapping({"a": "a"}),
            _catalog({"c": _row("S")}),
            None,
            None,
        )
        self.assertEqual(catalog["models"]["a"], shipped_row)

    def test_home_tier_list_overrides_one_stem(self):
        """One listed stem changes tier. Every unlisted stem keeps the catalog tier."""
        catalog, _mapping_doc = merge_documents(
            _catalog({"a": _row("C"), "b": _row("B")}),
            _mapping({"a": "a", "b": "b"}),
            None,
            None,
            {"S": ["a"]},
        )
        self.assertEqual(catalog["models"]["a"]["tier"], "S")
        self.assertEqual(catalog["models"]["b"]["tier"], "B")

    def test_home_tier_effort_spelling_names_the_stem(self):
        """An effort spelling overrides the stem model_key returns."""
        catalog, _mapping_doc = merge_documents(
            _catalog({"b": _row("C")}),
            _mapping({"b": "b"}),
            None,
            None,
            {"A": ["b-high-fast"]},
        )
        self.assertEqual(catalog["models"]["b"]["tier"], "A")
        self.assertNotIn("b-high-fast", catalog["models"])

    def test_first_home_tier_listing_wins(self):
        """The same stem under two home tiers keeps the first listing."""
        catalog, _mapping_doc = merge_documents(
            _catalog({"a": _row("C")}),
            _mapping({"a": "a"}),
            None,
            None,
            {"S": ["a"], "A": ["a-low"]},
        )
        self.assertEqual(catalog["models"]["a"]["tier"], "S")

    def test_tier_order_comes_from_the_shipped_catalog(self):
        """A home catalog's tier_order is ignored."""
        catalog, _mapping_doc = merge_documents(
            _catalog({"a": _row("C")}, tier_order=("C", "B", "A", "S")),
            _mapping({"a": "a"}),
            _catalog({}, tier_order=("S",)),
            None,
            None,
        )
        self.assertEqual(catalog["tier_order"], ["C", "B", "A", "S"])


class LoadEffectiveTests(unittest.TestCase):
    def test_missing_home_directory_returns_the_shipped_documents(self):
        """No home directory: the merged documents are the shipped ones."""
        catalog = _catalog({"a": _row("B", score=5, cost=4)})
        mapping = _mapping({"a": "alpha"})
        with tempfile.TemporaryDirectory() as tmp:
            shipped = Path(tmp) / "assets"
            shipped.mkdir()
            (shipped / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            (shipped / "mapping.json").write_text(json.dumps(mapping), encoding="utf-8")
            loaded_catalog, loaded_mapping = load_effective(
                shipped, Path(tmp) / "missing"
            )
        self.assertEqual(loaded_catalog, catalog)
        self.assertEqual(loaded_mapping, mapping)

    def test_invalid_home_catalog_raises(self):
        """Invalid home catalog JSON propagates JSONDecodeError."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shipped = root / "assets"
            home = root / "home"
            shipped.mkdir()
            home.mkdir()
            (shipped / "catalog.json").write_text(
                json.dumps(_catalog({"a": _row("C")})), encoding="utf-8"
            )
            (shipped / "mapping.json").write_text(
                json.dumps(_mapping({"a": "a"})), encoding="utf-8"
            )
            (home / "catalog.json").write_text("{", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                load_effective(shipped, home)
