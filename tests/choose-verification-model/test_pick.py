"""Selection rule for the verification-model picker.

The tests build catalogs in memory. ``main`` is given those objects so
the exit-code cases do not read the shipped JSON.
"""

import io
import random
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "rules" / "choose-verification-model"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from modelpool import select  # noqa: E402
from pick import main  # noqa: E402


def _entry(tier, score, cost, source="benchlm", has_fast=False):
    return {
        "tier": tier,
        "score": score,
        "score_source": source if score is not None else None,
        "output_cost_per_million": cost,
        "has_fast": has_fast,
    }


def _catalog(models, tier_order=("low", "mid", "high")):
    return {"tier_order": list(tier_order), "models": models}


def _mapping(families):
    return {
        "models": {
            slug: {
                "family": family,
                "pricing_name": slug,
                "output_multiplier": 1,
                "benchlm_slug": None,
                "interim_score": None,
            }
            for slug, family in families.items()
        }
    }


def _run(catalog, mapping, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = main(argv, catalog=catalog, mapping=mapping)
    return code, stdout.getvalue(), stderr.getvalue()


class PickTests(unittest.TestCase):
    def test_window_pick_is_different_family_and_seed_repeats(self):
        """Author rank 2. A cheaper same-family model is excluded.

        The printed slug is one of the two different-family models, and
        the same ``--seed`` prints it again.
        """
        models = {
            "author": _entry("mid", 80, 10),
            "same-cheaper": _entry("mid", 90, 1),
            "diff-best": _entry("mid", 90, 20),
            "diff-tied": _entry("mid", 80, 20),
        }
        families = {
            "author": "grok",
            "same-cheaper": "grok",
            "diff-best": "claude",
            "diff-tied": "gemini",
        }
        catalog = _catalog(models)
        mapping = _mapping(families)
        argv = [
            "--model",
            "author",
            "--reviewer-models",
            "author,same-cheaper,diff-best,diff-tied",
            "--seed",
            "3",
        ]
        code_a, out_a, _err_a = _run(catalog, mapping, argv)
        code_b, out_b, _err_b = _run(catalog, mapping, argv)
        self.assertEqual(code_a, 0)
        self.assertEqual(out_a.strip(), out_b.strip())
        self.assertIn(out_a.strip(), {"diff-best", "diff-tied"})

    def test_one_rank_below_is_eligible(self):
        """A different-family model at the next-worse distinct score is printed."""
        models = {
            "author": _entry("mid", 90, 10),
            "one-below": _entry("mid", 80, 10),
            "two-below": _entry("mid", 70, 1),
        }
        families = {"author": "grok", "one-below": "claude", "two-below": "gemini"}
        slug = select(
            _catalog(models),
            _mapping(families),
            "author",
            ["author", "one-below", "two-below"],
            random.Random(1),
        )
        self.assertEqual(slug, "one-below")

    def test_two_ranks_below_is_excluded_when_window_is_nonempty(self):
        """The model two dense ranks worse is not printed."""
        models = {
            "author": _entry("mid", 90, 10),
            "in-window": _entry("mid", 90, 10),
            "one-below-same": _entry("mid", 80, 10),
            "two-below": _entry("mid", 70, 1),
        }
        families = {
            "author": "grok",
            "in-window": "claude",
            "one-below-same": "grok",
            "two-below": "gemini",
        }
        enabled = ["author", "in-window", "one-below-same", "two-below"]
        catalog = _catalog(models)
        mapping = _mapping(families)
        for seed in range(15):
            slug = select(catalog, mapping, "author", enabled, random.Random(seed))
            self.assertEqual(slug, "in-window")

    def test_same_family_and_author_are_excluded_from_the_window(self):
        """Same-family models, including the author, are not printed."""
        models = {
            "author": _entry("mid", 80, 1),
            "same": _entry("mid", 95, 1),
            "other": _entry("mid", 80, 50),
        }
        families = {"author": "grok", "same": "grok", "other": "claude"}
        enabled = ["author", "same", "other"]
        catalog = _catalog(models)
        mapping = _mapping(families)
        for seed in range(15):
            slug = select(catalog, mapping, "author", enabled, random.Random(seed))
            self.assertEqual(slug, "other")

    def test_tied_score_shares_dense_rank_with_the_author(self):
        """A different-family model with the author's score is eligible."""
        models = {
            "author": _entry("mid", 80, 10),
            "tied": _entry("mid", 80, 99),
            "one-below-same": _entry("mid", 50, 1),
            "two-below": _entry("mid", 10, 1),
        }
        families = {
            "author": "grok",
            "tied": "claude",
            "one-below-same": "grok",
            "two-below": "gemini",
        }
        slug = select(
            _catalog(models),
            _mapping(families),
            "author",
            ["author", "tied", "one-below-same", "two-below"],
            random.Random(1),
        )
        self.assertEqual(slug, "tied")

    def test_empty_window_takes_cheapest_different_family_one_tier_up(self):
        """The next tier's cheapest different family wins over a cheaper same family."""
        models = {
            "author": _entry("low", 50, 1),
            "same-cheap": _entry("mid", 90, 1),
            "diff-costly": _entry("mid", 90, 9),
            "diff-cheap": _entry("mid", 40, 3),
        }
        families = {
            "author": "grok",
            "same-cheap": "grok",
            "diff-costly": "claude",
            "diff-cheap": "gemini",
        }
        slug = select(
            _catalog(models),
            _mapping(families),
            "author",
            ["author", "same-cheap", "diff-costly", "diff-cheap"],
            random.Random(1),
        )
        self.assertEqual(slug, "diff-cheap")

    def test_empty_window_all_same_family_takes_cheapest(self):
        """When the next tier has no other family, print its cheapest slug."""
        models = {
            "author": _entry("low", 50, 1),
            "pricey": _entry("mid", 90, 8),
            "cheap": _entry("mid", 10, 2),
        }
        families = {"author": "grok", "pricey": "grok", "cheap": "grok"}
        slug = select(
            _catalog(models),
            _mapping(families),
            "author",
            ["author", "pricey", "cheap"],
            random.Random(1),
        )
        self.assertEqual(slug, "cheap")

    def test_tied_cheapest_cost_is_chosen_by_seed(self):
        """Two models at the cheapest cost are both reachable, and a seed repeats."""
        models = {
            "author": _entry("low", 50, 1),
            "cheap-a": _entry("mid", 10, 2),
            "cheap-b": _entry("mid", 90, 2),
            "pricey": _entry("mid", 80, 7),
        }
        families = {
            "author": "grok",
            "cheap-a": "grok",
            "cheap-b": "grok",
            "pricey": "grok",
        }
        enabled = ["author", "cheap-a", "cheap-b", "pricey"]
        catalog = _catalog(models)
        mapping = _mapping(families)
        self.assertEqual(
            select(catalog, mapping, "author", enabled, random.Random(4)),
            select(catalog, mapping, "author", enabled, random.Random(4)),
        )
        seen = {
            select(catalog, mapping, "author", enabled, random.Random(seed))
            for seed in range(40)
        }
        self.assertEqual(seen, {"cheap-a", "cheap-b"})

    def test_abandoned_family_stays_inside_the_intelligence_window(self):
        """No different family: drop that constraint and stay within one rank.

        The author is in the window, so the pick does not fail closed.
        A same-family model two ranks below stays out. A seed repeats.
        """
        models = {
            "better-same": _entry("high", 90, 1),
            "author": _entry("high", 80, 1),
            "one-below": _entry("high", 60, 1),
            "two-below": _entry("high", 40, 1),
        }
        families = {slug: "grok" for slug in models}
        catalog = _catalog(models)
        mapping = _mapping(families)
        enabled = list(models)
        self.assertEqual(
            select(catalog, mapping, "author", enabled, random.Random(1)),
            select(catalog, mapping, "author", enabled, random.Random(1)),
        )
        seen = {
            select(catalog, mapping, "author", enabled, random.Random(seed))
            for seed in range(40)
        }
        self.assertEqual(seen, {"better-same", "author", "one-below"})

    def test_fast_author_alone_returns_the_fast_spelling(self):
        """The window holds only this model, so the fast spelling of it is the review."""
        models = {
            "claude-opus-5-5-medium": _entry("S", 77, 20, has_fast=True),
        }
        slug = select(
            _catalog(models, tier_order=("C", "B", "A", "S")),
            _mapping({"claude-opus-5-5-medium": "claude"}),
            "claude-opus-5-5-medium-fast",
            ["claude-opus-5-5-medium"],
            random.Random(1),
        )
        self.assertEqual(slug, "claude-opus-5-5-medium-fast")

    def test_fast_author_appends_fast_only_when_the_chosen_model_has_it(self):
        """Speed is applied after the base choice, and only if that row has fast."""
        models = {
            "grok-4.7-high": _entry("A", 70, 6, has_fast=True),
            "gpt-5.6-sol-medium": _entry("A", 72, 20, has_fast=True),
            "kimi-k3-high": _entry("A", 78, 15, has_fast=False),
        }
        families = {
            "grok-4.7-high": "grok",
            "gpt-5.6-sol-medium": "gpt",
            "kimi-k3-high": "kimi",
        }
        catalog = _catalog(models, tier_order=("C", "B", "A", "S"))
        mapping = _mapping(families)
        sol_enabled = ["grok-4.7-high", "gpt-5.6-sol-medium"]
        self.assertEqual(
            select(catalog, mapping, "grok-4.7-high-fast", sol_enabled, random.Random(0)),
            "gpt-5.6-sol-medium-fast",
        )
        self.assertEqual(
            select(catalog, mapping, "grok-4.7-high", sol_enabled, random.Random(0)),
            "gpt-5.6-sol-medium",
        )
        self.assertEqual(
            select(
                catalog,
                mapping,
                "grok-4.7-high-fast",
                ["grok-4.7-high", "kimi-k3-high"],
                random.Random(0),
            ),
            "kimi-k3-high",
        )

    def test_composer_fast_author_prints_a_fast_reviewer(self):
        """``composer-2.5-fast`` prints ``-fast`` when the chosen row has a fast variant."""
        models = {
            "composer-2.5": _entry("C", 60, 2.5, has_fast=True),
            "gpt-5.6-luna-medium": _entry("C", 58, 1.2, has_fast=True),
        }
        families = {"composer-2.5": "composer", "gpt-5.6-luna-medium": "gpt"}
        slug = select(
            _catalog(models, tier_order=("C", "B", "A", "S")),
            _mapping(families),
            "composer-2.5-fast",
            list(families),
            random.Random(0),
        )
        self.assertEqual(slug, "gpt-5.6-luna-medium-fast")

    def test_null_tier_unknown_tier_and_null_score_are_never_printed(self):
        """A slug with no usable tier or score stays out of the pool."""
        models = {
            "author": _entry("mid", 50, 10),
            "null-tier": _entry(None, 99, 1),
            "missing-tier": _entry("nope", 99, 1),
            "null-score": _entry("mid", None, 1),
            "valid": _entry("mid", 40, 50),
        }
        families = {
            "author": "grok",
            "null-tier": "claude",
            "missing-tier": "gemini",
            "null-score": "gpt",
            "valid": "kimi",
        }
        enabled = ["author", "null-tier", "missing-tier", "null-score", "valid"]
        catalog = _catalog(models)
        mapping = _mapping(families)
        for seed in range(10):
            slug = select(catalog, mapping, "author", enabled, random.Random(seed))
            self.assertEqual(slug, "valid")

    def test_null_cost_is_skipped_by_cheapest_and_allowed_in_the_window(self):
        """A null price drops out of the cost fallback and stays in the rank window."""
        window_models = {
            "author": _entry("mid", 50, 10),
            "null-cost": _entry("mid", 90, None),
        }
        window_families = {"author": "grok", "null-cost": "claude"}
        self.assertEqual(
            select(
                _catalog(window_models),
                _mapping(window_families),
                "author",
                ["author", "null-cost"],
                random.Random(1),
            ),
            "null-cost",
        )

        fallback_models = {
            "author": _entry("low", 50, 1),
            "null-cost": _entry("mid", 99, None),
            "priced": _entry("mid", 10, 4),
            "same-cheaper": _entry("mid", 10, 1),
        }
        fallback_families = {
            "author": "grok",
            "null-cost": "claude",
            "priced": "gemini",
            "same-cheaper": "grok",
        }
        self.assertEqual(
            select(
                _catalog(fallback_models),
                _mapping(fallback_families),
                "author",
                ["author", "null-cost", "priced", "same-cheaper"],
                random.Random(1),
            ),
            "priced",
        )

    def test_unknown_reviewer_slug_exits_2_and_names_the_slug(self):
        """A ``--reviewer-models`` slug missing from the catalog is an error."""
        models = {"author": _entry("mid", 80, 1)}
        code, stdout, stderr = _run(
            _catalog(models),
            _mapping({"author": "grok"}),
            ["--model", "author", "--reviewer-models", "author,missing-reviewer"],
        )
        self.assertEqual(code, 2)
        self.assertEqual(stdout.strip(), "")
        self.assertIn("missing-reviewer", stderr)

    def test_unknown_author_slug_exits_2(self):
        """An author slug missing from the catalog is an error."""
        code, stdout, stderr = _run(
            _catalog({"other": _entry("mid", 80, 1)}),
            _mapping({"other": "claude"}),
            ["--model", "missing-author", "--reviewer-models", "other"],
        )
        self.assertEqual(code, 2)
        self.assertEqual(stdout.strip(), "")
        self.assertIn("missing-author", stderr)

    def test_null_tier_or_null_score_author_exits_2(self):
        """An author with no usable tier or score is an error, same as an unknown slug."""
        enabled = ["author", "other"]
        families = {"author": "grok", "other": "claude"}
        other = _entry("mid", 80, 1)
        for author_entry in (_entry(None, 90, 1), _entry("mid", None, 1)):
            code, stdout, stderr = _run(
                _catalog({"author": author_entry, "other": other}),
                _mapping(families),
                ["--model", "author", "--reviewer-models", ",".join(enabled), "--seed", "1"],
            )
            self.assertEqual(code, 2)
            self.assertEqual(stdout.strip(), "")
            self.assertIn("author", stderr)
