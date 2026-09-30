"""Home-directory overlay for choose-verification-model assets.

Directory resolution, the source-tree check, and the per-model merge.
Nothing in this module opens a network connection.
"""

import importlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from homeassets import (  # noqa: E402
    is_source_tree,
    load_effective,
    merge_documents,
    user_assets_dir,
)
from pick import main as pick_main  # noqa: E402

_fixtures = importlib.import_module("tests.choose-verification-model.test_refresh")  # noqa: E402
_benchlm = _fixtures._benchlm
_asset_mapping = _fixtures._mapping
_pricing = _fixtures._pricing
_SCORED = _fixtures._SCORED
refresh_main = _fixtures.refresh_main


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


class PickOverlayTests(unittest.TestCase):
    def test_home_tier_changes_the_printed_slug(self):
        """A home tiers.toml moves one stem onto the tier that changes the winner."""
        catalog = _catalog(
            {
                "gamma": _row("C", score=10, cost=10),
                "beta": _row("B", score=50, cost=1),
                "delta": _row("B", score=50, cost=9),
            }
        )
        mapping = _mapping({"gamma": "gamma", "beta": "beta", "delta": "delta"})
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / "assets"
            home = root / "home"
            assets.mkdir()
            home.mkdir()
            (assets / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            (assets / "mapping.json").write_text(json.dumps(mapping), encoding="utf-8")
            (home / "tiers.toml").write_text('S = ["beta"]\n', encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = pick_main(
                    [
                        "--model",
                        "gamma",
                        "--reviewer-models",
                        "gamma,beta,delta",
                        "--seed",
                        "0",
                    ],
                    assets_dir=assets,
                    user_dir=home,
                )
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue().strip(), "delta")


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


def _skill_assets(root, parent_name):
    assets = root / parent_name / "choose-verification-model" / "assets"
    assets.mkdir(parents=True)
    return assets


def _write_json(path, document):
    path.write_text(json.dumps(document), encoding="utf-8")


def _snapshot(directory):
    files = {}
    if directory.exists():
        for path in directory.rglob("*"):
            if path.is_file():
                files[path.relative_to(directory).as_posix()] = path.read_bytes()
    return files


def _run_refresh(assets, home, bench_slugs, pricing_names):
    stderr = io.StringIO()
    with redirect_stderr(stderr):
        code = refresh_main(
            [],
            benchlm=_benchlm({slug: _SCORED for slug in bench_slugs}),
            pricing_markdown=_pricing(pricing_names),
            assets_dir=assets,
            user_dir=home,
            agent_models=False,
        )
    return code


class RefreshWriteTests(unittest.TestCase):
    def test_consumer_refresh_writes_home_catalog_and_mapping(self):
        """An install writes the home catalog and mapping, and leaves the skill catalog alone."""
        mapping = _asset_mapping(
            {"kept": {"family": "k", "pricing_name": "Kept", "benchlm_slug": "kept"}}
        )
        shipped_catalog = b'{"untouched": true}\n'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = _skill_assets(root, "ai-rizz")
            home = root / "home"
            _write_json(assets / "mapping.json", mapping)
            (assets / "tiers.toml").write_text('A = ["kept"]\n', encoding="utf-8")
            (assets / "catalog.json").write_bytes(shipped_catalog)
            code = _run_refresh(assets, home, ["kept"], ["Kept"])
            self.assertEqual(code, 0)
            self.assertTrue((home / "catalog.json").is_file())
            self.assertTrue((home / "mapping.json").is_file())
            self.assertFalse((home / "tiers.toml").exists())
            self.assertEqual((assets / "catalog.json").read_bytes(), shipped_catalog)

    def test_consumer_refresh_unions_mapping_stems(self):
        """Home-only and shipped-only mapping stems are both written."""
        shipped = _asset_mapping(
            {
                "shipped": {
                    "family": "s",
                    "pricing_name": "Shipped",
                    "benchlm_slug": "shipped",
                }
            }
        )
        home_mapping = _asset_mapping(
            {"added": {"family": "a", "pricing_name": "Added", "benchlm_slug": "added"}}
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = _skill_assets(root, "ai-rizz")
            home = root / "home"
            home.mkdir()
            _write_json(assets / "mapping.json", shipped)
            (assets / "tiers.toml").write_text('A = ["shipped"]\n', encoding="utf-8")
            _write_json(home / "mapping.json", home_mapping)
            code = _run_refresh(assets, home, ["shipped", "added"], ["Shipped", "Added"])
            written = json.loads((home / "mapping.json").read_text(encoding="utf-8"))
        self.assertEqual(code, 0)
        self.assertEqual(set(written["models"]), {"shipped", "added"})

    def test_consumer_refresh_applies_the_home_tier_list(self):
        """The written catalog uses the home tier for a listed stem and the shipped tier otherwise."""
        shipped = _asset_mapping(
            {
                "moved": {
                    "family": "m",
                    "pricing_name": "Moved",
                    "benchlm_slug": "moved",
                },
                "stays": {
                    "family": "s",
                    "pricing_name": "Stays",
                    "benchlm_slug": "stays",
                },
            }
        )
        home_tiers = 'S = ["moved"]\n'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = _skill_assets(root, "ai-rizz")
            home = root / "home"
            home.mkdir()
            _write_json(assets / "mapping.json", shipped)
            (assets / "tiers.toml").write_text(
                'A = ["moved"]\nB = ["stays"]\n', encoding="utf-8"
            )
            (home / "tiers.toml").write_text(home_tiers, encoding="utf-8")
            code = _run_refresh(assets, home, ["moved", "stays"], ["Moved", "Stays"])
            catalog = json.loads((home / "catalog.json").read_text(encoding="utf-8"))
            kept_tiers = (home / "tiers.toml").read_text(encoding="utf-8")
        self.assertEqual(code, 0)
        self.assertEqual(catalog["models"]["moved"]["tier"], "S")
        self.assertEqual(catalog["models"]["stays"]["tier"], "B")
        self.assertEqual(kept_tiers, home_tiers)

    def test_source_tree_refresh_ignores_the_home_tier(self):
        """A rules/ tree writes the shipped tier and does not change the home directory."""
        shipped = _asset_mapping(
            {"stem": {"family": "s", "pricing_name": "Stem", "benchlm_slug": "stem"}}
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = _skill_assets(root, "rules")
            home = root / "home"
            home.mkdir()
            _write_json(assets / "mapping.json", shipped)
            (assets / "tiers.toml").write_text('A = ["stem"]\n', encoding="utf-8")
            (home / "tiers.toml").write_text('S = ["stem"]\n', encoding="utf-8")
            (home / "catalog.json").write_text('{"local": true}\n', encoding="utf-8")
            before = _snapshot(home)
            code = _run_refresh(assets, home, ["stem"], ["Stem"])
            catalog = json.loads((assets / "catalog.json").read_text(encoding="utf-8"))
            after = _snapshot(home)
        self.assertEqual(code, 0)
        self.assertEqual(catalog["models"]["stem"]["tier"], "A")
        self.assertEqual(after, before)
