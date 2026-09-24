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

from modelpool import SelectionError, model_key, select  # noqa: E402
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

    def test_never_author_is_printed(self):
        """An author whose tier is never is printed back and main exits 0."""
        catalog = _catalog(
            {"old-high": _entry("never", 50, 15), "peer": _entry("A", 70, 5)},
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"old-high": "claude", "peer": "gpt"})
        code, stdout, stderr = _run(
            catalog, mapping, ["--model", "old-high-fast", "--reviewer-models", "peer"]
        )
        self.assertEqual((code, stdout.strip(), stderr), (0, "old-high-fast", ""))

    def test_never_reviewer_is_skipped(self):
        """An enabled slug whose tier is never is not chosen and is not an error."""
        catalog = _catalog(
            {
                "author": _entry("A", 70, 5),
                "old": _entry("never", 71, 1),
                "peer": _entry("A", 69, 5),
            },
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"author": "a", "old": "b", "peer": "c"})
        for seed in range(5):
            self.assertEqual(
                select(catalog, mapping, "author", ["old", "peer"], random.Random(seed)),
                "peer",
            )

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


class EffortIdentityTests(unittest.TestCase):
    def test_model_key_strips_effort_and_keeps_thinking(self):
        """Effort is not part of the model. A non-effort token stays."""
        self.assertEqual(model_key("gemini-3.8-flash-low"), "gemini-3.8-flash")
        self.assertEqual(model_key("gemini-3.8-flash-medium"), "gemini-3.8-flash")
        self.assertEqual(model_key("gemini-3.8-flash-high"), "gemini-3.8-flash")
        self.assertEqual(model_key("gemini-3.8-flash-xhigh-fast"), "gemini-3.8-flash")
        self.assertEqual(model_key("claude-sonnet-5-thinking-high"), "claude-sonnet-5-thinking")
        self.assertEqual(model_key("claude-sonnet-5-high"), "claude-sonnet-5")
        self.assertEqual(model_key("composer-2.5"), "composer-2.5")
        self.assertEqual(model_key("composer-2.5-fast"), "composer-2.5")

    def test_model_key_reads_cli_efforts(self):
        """Every effort word agent --list-models uses is stripped, longest first."""
        cases = {
            "claude-opus-5-5-max": "claude-opus-5-5",
            "gpt-5.6-sol-none": "gpt-5.6-sol",
            "muse-spark-1.3-minimal": "muse-spark-1.3",
            "gpt-5.5-extra-high": "gpt-5.5",
            "grok-4.7-xhigh": "grok-4.7",
            "claude-opus-5-5-max-fast": "claude-opus-5-5",
            "gpt-5.5-extra-high-fast": "gpt-5.5",
        }
        for slug, key in cases.items():
            with self.subTest(slug=slug):
                self.assertEqual(model_key(slug), key)
                self.assertEqual(model_key(key), key)

    def test_model_key_reads_effort_before_thinking(self):
        """An effort directly before -thinking is removed; -thinking stays."""
        cases = {
            "claude-4.6-opus-high-thinking": "claude-4.6-opus-thinking",
            "claude-4.6-sonnet-medium-thinking": "claude-4.6-sonnet-thinking",
            "claude-4.6-opus-max-thinking": "claude-4.6-opus-thinking",
        }
        for slug, key in cases.items():
            with self.subTest(slug=slug):
                self.assertEqual(model_key(slug), key)
                self.assertEqual(model_key(key), key)

    def test_model_key_leaves_non_effort_suffixes(self):
        """Slugs with no effort word are their own key, and keys are idempotent."""
        for slug in (
            "gpt-5.2",
            "gemini-3.1-pro",
            "kimi-k2.7-code",
            "gpt-5-mini",
            "claude-sonnet-5-thinking",
        ):
            with self.subTest(slug=slug):
                self.assertEqual(model_key(slug), slug)

    def test_max_effort_reviewer_resolves(self):
        """An enabled max-effort spelling is the stored model and can be printed."""
        catalog = _catalog(
            {
                "gemini-3.8-flash": _entry("S", 70, 3.5),
                "claude-opus-5-5": _entry("S", 77, 20),
            },
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"gemini-3.8-flash": "gemini", "claude-opus-5-5": "claude"})
        self.assertEqual(
            select(
                catalog,
                mapping,
                "gemini-3.8-flash-low",
                ["claude-opus-5-5-max"],
                random.Random(0),
            ),
            "claude-opus-5-5-max",
        )

    def test_effort_on_a_bare_key_is_that_model(self):
        """composer-2.5-high ranks as composer-2.5 and can select a reviewer."""
        catalog = _catalog(
            {
                "composer-2.5": _entry("C", 60, 2.5),
                "luna": _entry("C", 80, 1),
            },
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"composer-2.5": "composer", "luna": "gpt"})
        self.assertEqual(
            select(catalog, mapping, "composer-2.5-high", ["luna"], random.Random(0)),
            "luna",
        )
        self.assertEqual(
            select(catalog, mapping, "composer-2.5", ["luna"], random.Random(0)),
            "luna",
        )

    def test_author_effort_does_not_change_the_reviewer(self):
        """low and xhigh of one author select the same reviewer spelling."""
        catalog = _catalog(
            {
                "grok": _entry("A", 70, 6),
                "gemini-3.8-flash": _entry("A", 75, 3.5, has_fast=False),
            },
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"grok": "grok", "gemini-3.8-flash": "gemini"})
        enabled = ["gemini-3.8-flash-high"]
        low = select(catalog, mapping, "grok-low", enabled, random.Random(0))
        extra = select(catalog, mapping, "grok-xhigh", enabled, random.Random(0))
        self.assertEqual(low, "gemini-3.8-flash-high")
        self.assertEqual(extra, low)

    def test_printed_effort_is_the_candidate_not_the_author(self):
        """The reviewer effort is the spelling on the candidate list."""
        catalog = _catalog(
            {
                "gemini-3.8-flash": _entry("A", 75, 3.5),
                "claude-opus-5-5": _entry("S", 77, 20, has_fast=True),
            },
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"gemini-3.8-flash": "gemini", "claude-opus-5-5": "claude"})
        self.assertEqual(
            select(
                catalog,
                mapping,
                "gemini-3.8-flash-low",
                ["claude-opus-5-5-high"],
                random.Random(0),
            ),
            "claude-opus-5-5-high",
        )

    def test_fast_appends_to_the_candidate_effort(self):
        """-fast follows the author. The candidate's effort stays put."""
        catalog = _catalog(
            {
                "grok": _entry("A", 70, 6, has_fast=True),
                "gemini-3.8-flash": _entry("A", 75, 3.5, has_fast=True),
            },
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"grok": "grok", "gemini-3.8-flash": "gemini"})
        enabled = ["gemini-3.8-flash-high"]
        self.assertEqual(
            select(catalog, mapping, "grok-low-fast", enabled, random.Random(0)),
            "gemini-3.8-flash-high-fast",
        )
        self.assertEqual(
            select(catalog, mapping, "grok-low", enabled, random.Random(0)),
            "gemini-3.8-flash-high",
        )

    def test_first_listed_effort_is_the_one_candidate(self):
        """Two efforts of one model are one row. The first spelling is printed."""
        catalog = _catalog(
            {
                "grok": _entry("A", 70, 6),
                "gemini-3.8-flash": _entry("A", 75, 3.5),
            },
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"grok": "grok", "gemini-3.8-flash": "gemini"})
        self.assertEqual(
            select(
                catalog,
                mapping,
                "grok-high",
                ["gemini-3.8-flash-low", "gemini-3.8-flash-high"],
                random.Random(0),
            ),
            "gemini-3.8-flash-low",
        )

    def test_empty_pool_keeps_the_author_effort(self):
        """Returning the author prints the spelling they were invoked as."""
        catalog = _catalog(
            {"gemini-3.8-flash": _entry("S", 75, 3.5)},
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"gemini-3.8-flash": "gemini"})
        self.assertEqual(
            select(
                catalog,
                mapping,
                "gemini-3.8-flash-low",
                ["gemini-3.8-flash-low"],
                random.Random(0),
            ),
            "gemini-3.8-flash-low",
        )

    def test_thinking_stem_does_not_match_the_bare_model(self):
        """claude-sonnet-5-high is not claude-sonnet-5-thinking."""
        catalog = _catalog(
            {"claude-sonnet-5-thinking": _entry("A", 71, 10)},
            tier_order=("C", "B", "A", "S"),
        )
        mapping = _mapping({"claude-sonnet-5-thinking": "claude"})
        code, stdout, stderr = _run(
            catalog,
            mapping,
            [
                "--model",
                "claude-sonnet-5-thinking-high",
                "--reviewer-models",
                "claude-sonnet-5-high",
            ],
        )
        self.assertEqual(code, 2)
        self.assertEqual(stdout.strip(), "")
        self.assertIn("claude-sonnet-5-high", stderr)

    def test_select_does_not_mutate_the_catalog(self):
        """Ranking an effort spelling does not add a row."""
        models = {
            "grok": _entry("A", 70, 6),
            "gemini-3.8-flash": _entry("A", 75, 3.5),
        }
        catalog = _catalog(models, tier_order=("C", "B", "A", "S"))
        mapping = _mapping({"grok": "grok", "gemini-3.8-flash": "gemini"})
        before = {key: dict(value) for key, value in catalog["models"].items()}
        select(
            catalog,
            mapping,
            "grok-xhigh",
            ["gemini-3.8-flash-high"],
            random.Random(0),
        )
        self.assertIs(catalog["models"], models)
        self.assertEqual(
            {key: dict(value) for key, value in catalog["models"].items()},
            before,
        )
