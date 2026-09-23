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

from modelpool import SelectionError, place_effort, select  # noqa: E402
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

    def test_unresolvable_empty_pool_returns_the_author(self):
        """Every encoded step left an empty pool: print the author.

        Same-family peers in this tier are not a substitute. There is
        no higher tier to search.
        """
        models = {
            "author": _entry("high", 90, 1),
            "same": _entry("high", 80, 1),
        }
        families = {"author": "grok", "same": "grok"}
        catalog = _catalog(models)
        mapping = _mapping(families)
        enabled = ["author", "same"]
        seen = {
            select(catalog, mapping, "author", enabled, random.Random(seed))
            for seed in range(20)
        }
        self.assertEqual(seen, {"author"})

    def test_empty_or_unpriced_next_tier_returns_the_author(self):
        """A non-top author prints themselves when the next tier cannot.

        Terra is B and Composer is C, with nothing enabled in A.
        A next tier whose only model has no price is the same outcome.
        """
        models = {
            "gpt-5.6-terra-medium": _entry("B", 67, 12),
            "composer-2.5": _entry("C", 60, 2.5),
        }
        self.assertEqual(
            select(
                _catalog(models, tier_order=("C", "B", "A", "S")),
                _mapping(
                    {
                        "gpt-5.6-terra-medium": "gpt",
                        "composer-2.5": "composer",
                    }
                ),
                "gpt-5.6-terra-medium",
                ["gpt-5.6-terra-medium", "composer-2.5"],
                random.Random(1),
            ),
            "gpt-5.6-terra-medium",
        )
        unpriced = {
            "author": _entry("mid", 50, 1),
            "below": _entry("low", 10, 1),
            "above": _entry("high", 90, None),
        }
        self.assertEqual(
            select(
                _catalog(unpriced),
                _mapping({"author": "grok", "below": "composer", "above": "claude"}),
                "author",
                ["author", "below", "above"],
                random.Random(1),
            ),
            "author",
        )

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

    def test_unknown_author_slug_is_printed(self):
        """An author the script cannot place is printed, and the process exits 0."""
        code, stdout, stderr = _run(
            _catalog({"other": _entry("mid", 80, 1)}),
            _mapping({"other": "claude"}),
            ["--model", "missing-author", "--reviewer-models", "other"],
        )
        self.assertEqual(code, 0)
        self.assertEqual(stdout.strip(), "missing-author")
        self.assertEqual(stderr.strip(), "")

        fast_code, fast_stdout, fast_stderr = _run(
            _catalog({"other": _entry("mid", 80, 1)}),
            _mapping({"other": "claude"}),
            ["--model", "missing-author-fast", "--reviewer-models", "other"],
        )
        self.assertEqual(fast_code, 0)
        self.assertEqual(fast_stdout.strip(), "missing-author-fast")
        self.assertEqual(fast_stderr.strip(), "")

        bare_code, bare_stdout, bare_stderr = _run(
            _catalog({"composer-2.5": _entry("mid", 60, 1)}, tier_order=("C", "B", "A", "S")),
            _mapping({"composer-2.5": "composer"}),
            ["--model", "composer-2.5-high", "--reviewer-models", "composer-2.5"],
        )
        self.assertEqual(bare_code, 0)
        self.assertEqual(bare_stdout.strip(), "composer-2.5-high")
        self.assertEqual(bare_stderr.strip(), "")

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


class SelectEffortTests(unittest.TestCase):
    def test_synthetic_reviewer_can_be_printed(self):
        """An enabled effort spelling is a reviewer when it is the tier above."""
        catalog = _catalog(
            {
                "author": _entry("B", 10, 1),
                "m-medium": _entry("A", 50, 5, has_fast=False),
            },
            tier_order=("B", "A", "S"),
        )
        mapping = _mapping({"author": "grok", "m-medium": "claude"})
        self.assertEqual(
            select(catalog, mapping, "author", ["m-xhigh"], random.Random(0)),
            "m-xhigh",
        )

    def test_higher_effort_is_a_different_row(self):
        """A higher effort ranks in the tier above; the stored effort stays below."""
        models = {
            "m-medium": _entry("B", 20, 9),
            "other-b": _entry("B", 12, 1),
            "above-high": _entry("A", 50, 100),
        }
        families = {"m-medium": "claude", "other-b": "gemini", "above-high": "gpt"}
        catalog = _catalog(models, tier_order=("B", "A", "S"))
        mapping = _mapping(families)
        enabled = ["other-b", "above-high"]
        self.assertEqual(
            select(catalog, mapping, "m-high", enabled, random.Random(0)),
            "above-high",
        )
        self.assertEqual(
            select(catalog, mapping, "m-medium", enabled, random.Random(0)),
            "other-b",
        )

    def test_empty_pool_prints_the_requested_effort(self):
        """The empty-pool author is the requested spelling, not the stored sibling."""
        catalog = _catalog(
            {"m-medium": _entry("S", 50, 1)},
            tier_order=("B", "A", "S"),
        )
        mapping = _mapping({"m-medium": "claude"})
        self.assertEqual(
            select(catalog, mapping, "m-low", ["m-low"], random.Random(0)),
            "m-low",
        )

    def test_fast_author_appends_fast_on_a_synthetic_reviewer(self):
        """A fast author prints -fast when the sibling row has a fast variant."""
        catalog = _catalog(
            {
                "author": _entry("B", 10, 1),
                "m-medium": _entry("A", 50, 5, has_fast=True),
            },
            tier_order=("B", "A", "S"),
        )
        mapping = _mapping({"author": "grok", "m-medium": "claude"})
        self.assertEqual(
            select(catalog, mapping, "author-fast", ["m-xhigh"], random.Random(0)),
            "m-xhigh-fast",
        )

    def test_caller_catalog_is_unchanged(self):
        """select does not insert effort rows into the caller's catalog."""
        models = {
            "m-medium": _entry("B", 20, 9),
            "other-b": _entry("B", 12, 1),
            "above-high": _entry("A", 50, 100),
        }
        catalog = _catalog(models, tier_order=("B", "A", "S"))
        mapping = _mapping(
            {"m-medium": "claude", "other-b": "gemini", "above-high": "gpt"}
        )
        before = {key: dict(value) for key, value in catalog["models"].items()}
        select(
            catalog,
            mapping,
            "m-high",
            ["other-b", "above-high"],
            random.Random(0),
        )
        self.assertIs(catalog["models"], models)
        self.assertEqual(
            {key: dict(value) for key, value in catalog["models"].items()},
            before,
        )


class PlaceEffortTests(unittest.TestCase):
    def _pair(self, models, families, tier_order=("B", "A", "S")):
        return _catalog(models, tier_order), _mapping(families)

    def test_higher_and_extra_high_scores_stay_apart(self):
        """Two efforts above one stored row get different scores, both above it."""
        catalog, mapping = self._pair(
            {
                "m-medium": _entry("A", 10, 5, has_fast=True),
                "ceiling-high": _entry("A", 40, 1),
            },
            {"m-medium": "claude", "ceiling-high": "gpt"},
        )
        high, high_family = place_effort(catalog, mapping, "m-high")
        extra, extra_family = place_effort(catalog, mapping, "m-xhigh")
        self.assertAlmostEqual(high["score"], 20)
        self.assertAlmostEqual(extra["score"], 30)
        self.assertLess(high["score"], extra["score"])
        self.assertGreater(high["score"], 10)
        self.assertEqual(high["tier"], "A")
        self.assertEqual(extra["tier"], "A")
        self.assertEqual(high["score_source"], "effort")
        self.assertEqual(high["output_cost_per_million"], 5)
        self.assertTrue(high["has_fast"])
        self.assertEqual(high_family, "claude")
        self.assertEqual(extra_family, "claude")

    def test_lower_effort_sits_below_the_stored_row(self):
        """A lower effort is placed below the stored sibling."""
        catalog, mapping = self._pair(
            {
                "m-medium": _entry("A", 10, 1),
                "floor-low": _entry("A", 4, 1),
            },
            {"m-medium": "claude", "floor-low": "gpt"},
        )
        low, _family = place_effort(catalog, mapping, "m-low")
        self.assertAlmostEqual(low["score"], 7)
        self.assertLess(low["score"], 10)

    def test_boundary_takes_the_higher_tier(self):
        """Score-neighbors in B and A assign the higher tier."""
        catalog, mapping = self._pair(
            {
                "m-medium": _entry("B", 10, 1),
                "above-high": _entry("A", 40, 1),
            },
            {"m-medium": "claude", "above-high": "gpt"},
        )
        high, _family = place_effort(catalog, mapping, "m-high")
        self.assertAlmostEqual(high["score"], 20)
        self.assertEqual(high["tier"], "A")

    def test_shared_neighbor_tier_stays(self):
        """Score-neighbors in the same tier keep that tier."""
        catalog, mapping = self._pair(
            {
                "m-medium": _entry("A", 10, 1),
                "ceiling-high": _entry("A", 40, 1),
            },
            {"m-medium": "claude", "ceiling-high": "gpt"},
        )
        high, _family = place_effort(catalog, mapping, "m-high")
        self.assertEqual(high["tier"], "A")

    def test_exact_key_returns_the_stored_row(self):
        """An exact catalog key is that row, including after a fast strip."""
        catalog, mapping = self._pair(
            {"m-medium": _entry("B", 10, 5, has_fast=True)},
            {"m-medium": "claude"},
        )
        entry, family = place_effort(catalog, mapping, "m-medium")
        fast_entry, fast_family = place_effort(catalog, mapping, "m-medium-fast")
        self.assertIs(entry, catalog["models"]["m-medium"])
        self.assertIs(fast_entry, entry)
        self.assertEqual(entry["score"], 10)
        self.assertEqual(entry["tier"], "B")
        self.assertEqual(entry["score_source"], "benchlm")
        self.assertEqual(family, "claude")
        self.assertEqual(fast_family, "claude")

    def test_bare_key_is_not_an_effort_anchor(self):
        """A stored key with no effort suffix does not anchor an effort spelling."""
        catalog, mapping = self._pair(
            {"composer-2.5": _entry("C", 60, 1)},
            {"composer-2.5": "composer"},
            tier_order=("C", "B", "A", "S"),
        )
        with self.assertRaises(SelectionError) as caught:
            place_effort(catalog, mapping, "composer-2.5-high")
        self.assertIn("composer-2.5-high", str(caught.exception))

    def test_thinking_stays_in_the_stem(self):
        """Stripping an effort word does not drop a non-effort token."""
        catalog, mapping = self._pair(
            {"claude-sonnet-5-thinking-high": _entry("A", 71, 1)},
            {"claude-sonnet-5-thinking-high": "claude"},
        )
        with self.assertRaises(SelectionError) as caught:
            place_effort(catalog, mapping, "claude-sonnet-5-high")
        self.assertIn("claude-sonnet-5-high", str(caught.exception))

    def test_null_sibling_score_is_unknown(self):
        """A sibling with no score cannot place an effort spelling."""
        catalog, mapping = self._pair(
            {"m-medium": _entry("A", None, 1)},
            {"m-medium": "claude"},
        )
        with self.assertRaises(SelectionError) as caught:
            place_effort(catalog, mapping, "m-high")
        self.assertIn("m-high", str(caught.exception))

    def test_between_two_siblings_interpolates_by_effort_index(self):
        """A spelling between two stored efforts sits on the index fraction.

        Equal distance to both siblings takes the higher effort's family and price.
        """
        catalog, mapping = self._pair(
            {
                "m-low": _entry("A", 10, 1, has_fast=False),
                "m-high": _entry("A", 40, 9, has_fast=True),
            },
            {"m-low": "claude", "m-high": "gpt"},
        )
        medium, family = place_effort(catalog, mapping, "m-medium")
        self.assertAlmostEqual(medium["score"], 25)
        self.assertEqual(family, "gpt")
        self.assertEqual(medium["output_cost_per_million"], 9)
        self.assertTrue(medium["has_fast"])

    def test_end_of_scale_uses_a_small_step(self):
        """With no row beyond the anchor, efforts step by 1e-3 and stay ordered."""
        catalog, mapping = self._pair(
            {"m-medium": _entry("A", 10, 1)},
            {"m-medium": "claude"},
        )
        high, _high_family = place_effort(catalog, mapping, "m-high")
        extra, _extra_family = place_effort(catalog, mapping, "m-xhigh")
        low, _low_family = place_effort(catalog, mapping, "m-low")
        self.assertAlmostEqual(high["score"], 10.001)
        self.assertAlmostEqual(extra["score"], 10.002)
        self.assertAlmostEqual(low["score"], 9.999)
        self.assertEqual(high["tier"], "A")

    def test_exact_collision_nudges_toward_the_anchor(self):
        """A score that lands on a stored row moves 1e-6 toward the anchor.

        The row at 20 is an effort row, so it is not the far neighbor.
        The far neighbor stays at 40, and the one-third step lands on 20.
        """
        catalog, mapping = self._pair(
            {
                "m-medium": _entry("A", 10, 1),
                "ceiling-high": _entry("A", 40, 1),
                "ghost-high": _entry("A", 20, 1, source="effort"),
            },
            {
                "m-medium": "claude",
                "ceiling-high": "gpt",
                "ghost-high": "gemini",
            },
        )
        high, _family = place_effort(catalog, mapping, "m-high")
        self.assertAlmostEqual(high["score"], 20 - 1e-6)

    def test_catalog_is_not_mutated(self):
        """place_effort leaves the caller's catalog and mapping alone."""
        catalog, mapping = self._pair(
            {
                "m-medium": _entry("A", 10, 5, has_fast=True),
                "ceiling-high": _entry("A", 40, 1),
            },
            {"m-medium": "claude", "ceiling-high": "gpt"},
        )
        before_models = {key: dict(value) for key, value in catalog["models"].items()}
        before_families = {
            key: dict(value) for key, value in mapping["models"].items()
        }
        place_effort(catalog, mapping, "m-high")
        self.assertEqual(
            {key: dict(value) for key, value in catalog["models"].items()},
            before_models,
        )
        self.assertEqual(set(catalog["models"]), set(before_models))
        self.assertEqual(
            {key: dict(value) for key, value in mapping["models"].items()},
            before_families,
        )

    def test_effort_rows_are_not_siblings(self):
        """A row marked effort is not an anchor, so placement ignores it."""
        catalog, mapping = self._pair(
            {
                "m-medium": _entry("A", 10, 5),
                "m-high": _entry("A", 12, 1, source="effort"),
                "ceiling-high": _entry("A", 40, 1),
            },
            {"m-medium": "claude", "m-high": "claude", "ceiling-high": "gpt"},
        )
        extra, _family = place_effort(catalog, mapping, "m-xhigh")
        self.assertAlmostEqual(extra["score"], 30)
