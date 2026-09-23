"""Shared selection and catalog-refresh helpers.

``select`` chooses one reviewer slug. ``build_catalog`` rebuilds scores
and output prices while keeping hand-set tiers.
"""

import re

_LINK = re.compile(r"\[(.*)\]\([^)]*\)\Z")
_SEPARATOR = re.compile(r":?-{3,}:?\Z")
_CATEGORIES = ("agentic", "coding", "reasoning")
_FAST_SUFFIX = "-fast"


class SelectionError(Exception):
    """A reviewer could not be chosen.

    ``slug`` names the author or reviewer the operator has to fix, when
    one slug is the cause. The message always includes that slug.
    """

    def __init__(self, slug: str, message: str) -> None:
        self.slug = slug
        super().__init__(message)


def canonical_slug(slug: str) -> str:
    """Return the catalog slug for ``slug``.

    A trailing ``-fast`` is the same model. Speed does not change the
    bench score, the tier, the family, or the price used to rank.
    """
    if slug.endswith(_FAST_SUFFIX):
        return slug[: -len(_FAST_SUFFIX)]
    return slug


_EFFORTS = ("low", "medium", "high", "xhigh")
_EFFORT_INDEX = {name: index for index, name in enumerate(_EFFORTS)}


def _split_effort(slug: str):
    """Return ``(stem, effort)`` for a trailing effort word.

    ``xhigh`` is matched before ``high``. A slug with no effort word
    returns ``(slug, None)``.
    """
    for name in ("xhigh", "high", "medium", "low"):
        suffix = f"-{name}"
        if slug.endswith(suffix):
            return slug[: -len(suffix)], name
    return slug, None


def _far_score(models, anchor_score, stem, *, above: bool):
    """Return the nearest other-stem stored score on the requested side."""
    found = None
    for stored, entry in models.items():
        if entry.get("score_source") == "effort":
            continue
        if _split_effort(stored)[0] == stem:
            continue
        score = entry.get("score")
        if score is None:
            continue
        if above and score <= anchor_score:
            continue
        if not above and score >= anchor_score:
            continue
        if found is None:
            found = score
        elif above and score < found:
            found = score
        elif not above and score > found:
            found = score
    return found


def _nudge_off_stored_score(score, models, anchor_score):
    """Move ``score`` by 1e-6 toward ``anchor_score`` when it ties a stored row."""
    for entry in models.values():
        stored = entry.get("score")
        if stored is None or stored != score:
            continue
        if anchor_score < score:
            return score - 1e-6
        if anchor_score > score:
            return score + 1e-6
        return score + 1e-6
    return score


def _tier_between(score, models, tier_order):
    """Return the tier of the score-neighbors, preferring the higher tier."""
    lower = None
    upper = None
    for entry in models.values():
        if entry.get("score_source") == "effort":
            continue
        stored = entry.get("score")
        tier = entry.get("tier")
        if stored is None or tier not in tier_order:
            continue
        if stored < score and (lower is None or stored > lower[0]):
            lower = (stored, tier)
        elif stored > score and (upper is None or stored < upper[0]):
            upper = (stored, tier)
    if lower and upper:
        lower_tier = lower[1]
        upper_tier = upper[1]
        if tier_order.index(lower_tier) >= tier_order.index(upper_tier):
            return lower_tier
        return upper_tier
    if lower:
        return lower[1]
    if upper:
        return upper[1]
    return None


def place_effort(catalog, mapping, slug: str):
    """Return the catalog entry and family for ``slug``.

    An exact catalog key returns the stored entry and its mapping
    family. An unmatched effort spelling of a stored effort-suffixed
    key returns a new entry and the sibling family. The new entry is
    not written into ``catalog``.

    ``slug`` may end in ``-fast``. That suffix is stripped before
    lookup and does not change the score, the tier, or the price.

    Raises ``SelectionError`` naming ``slug`` when the spelling cannot
    be placed. Rows whose ``score_source`` is ``effort`` are not
    anchors and are not score-neighbors. Siblings and far rows are
    stored rows.
    """
    key = canonical_slug(slug)
    models = catalog["models"]
    families = mapping["models"]
    tier_order = list(catalog["tier_order"])

    def family_of(stored):
        mapped = families.get(stored) or {}
        family = mapped.get("family")
        if isinstance(family, str) and family:
            return family
        return None

    def stored_row(stored):
        return models[stored].get("score_source") != "effort"

    if key in models:
        family = family_of(key)
        if family is None:
            raise SelectionError(slug, f"unknown slug: {slug}")
        return models[key], family

    stem, effort = _split_effort(key)
    if effort is None:
        raise SelectionError(slug, f"unknown slug: {slug}")
    requested = _EFFORT_INDEX[effort]
    siblings = []
    for stored in models:
        if not stored_row(stored):
            continue
        stored_stem, stored_effort = _split_effort(stored)
        if stored_stem != stem or stored_effort is None:
            continue
        entry = models[stored]
        tier = entry.get("tier")
        score = entry.get("score")
        if tier not in tier_order or score is None or family_of(stored) is None:
            continue
        siblings.append((_EFFORT_INDEX[stored_effort], stored))
    if not siblings:
        raise SelectionError(slug, f"unknown slug: {slug}")

    lower = [pair for pair in siblings if pair[0] < requested]
    upper = [pair for pair in siblings if pair[0] > requested]
    if lower and upper:
        lower_index, lower_slug = max(lower)
        upper_index, upper_slug = min(upper)
        lower_score = models[lower_slug]["score"]
        upper_score = models[upper_slug]["score"]
        fraction = (requested - lower_index) / (upper_index - lower_index)
        score = lower_score + (upper_score - lower_score) * fraction
        anchor = min(
            siblings, key=lambda pair: (abs(pair[0] - requested), -pair[0])
        )[1]
    elif lower:
        anchor_index, anchor = max(lower)
        anchor_score = models[anchor]["score"]
        far = _far_score(models, anchor_score, stem, above=True)
        steps = requested - anchor_index
        room = 3 - anchor_index
        if far is None:
            score = anchor_score + steps * 1e-3
        else:
            score = anchor_score + (far - anchor_score) * (steps / (room + 1))
    elif upper:
        anchor_index, anchor = min(upper)
        anchor_score = models[anchor]["score"]
        far = _far_score(models, anchor_score, stem, above=False)
        steps = anchor_index - requested
        room = anchor_index
        if far is None:
            score = anchor_score - steps * 1e-3
        else:
            score = anchor_score - (anchor_score - far) * (steps / (room + 1))
    else:
        raise SelectionError(slug, f"unknown slug: {slug}")

    anchor_score = models[anchor]["score"]
    score = _nudge_off_stored_score(score, models, anchor_score)
    tier = _tier_between(score, models, tier_order)
    if tier is None:
        raise SelectionError(slug, f"unknown slug: {slug}")
    anchor_entry = models[anchor]
    return (
        {
            "tier": tier,
            "score": score,
            "score_source": "effort",
            "output_cost_per_million": anchor_entry.get("output_cost_per_million"),
            "has_fast": bool(anchor_entry.get("has_fast")),
        },
        family_of(anchor),
    )


def _expand_effort(catalog, mapping, slugs):
    """Return copies of ``catalog`` and ``mapping`` with effort rows added.

    ``place_effort`` sees the original objects, so one synthetic row is
    never the anchor for the next slug. The caller's dicts are unchanged.
    """
    models = dict(catalog["models"])
    families = dict(mapping["models"])
    for slug in slugs:
        key = canonical_slug(slug)
        if key in models:
            continue
        entry, family = place_effort(catalog, mapping, slug)
        models[key] = entry
        families[key] = {"family": family}
    return {**catalog, "models": models}, {**mapping, "models": families}


def select(catalog, mapping, author, enabled, rng):
    """Return one reviewer slug, or raise ``SelectionError``.

    ``catalog`` and ``mapping`` are the parsed JSON objects. ``author``
    is the slug of the model asking for a reviewer. ``enabled`` is the
    Task-tool slug list. ``rng`` is a ``random.Random`` instance; a
    fixed seed makes the choice repeatable.

    A trailing ``-fast`` is stripped before lookup. Fast and non-fast
    spellings of one model are one candidate. An unmatched effort
    spelling of a stored effort-suffixed key is placed in memory for
    this call and is not written back. When the author spelling cannot
    be placed, return that spelling. An enabled spelling that cannot
    be placed still raises ``SelectionError``.

    Rank is dense rank by score inside the author's tier, best at
    rank 1. The window is a different family, from one rank below the
    author through the best in the tier. An empty window looks up one
    tier and takes the cheapest different family, then the cheapest
    slug in that tier. Those prices are the base output prices. When
    every encoded step has left the pool empty, return the author
    instead of failing.

    After that choice, append ``-fast`` only when the author slug ended
    in ``-fast`` and the chosen model has a fast variant.
    """
    try:
        catalog, mapping = _expand_effort(catalog, mapping, [author, *enabled])
    except SelectionError as exc:
        if exc.slug == author:
            return author
        raise
    models = catalog["models"]
    tier_order = catalog["tier_order"]
    families = mapping["models"]
    author_key = canonical_slug(author)
    if author_key not in models:
        return author

    enabled_keys = []
    seen = set()
    for slug in enabled:
        key = canonical_slug(slug)
        if key not in models:
            raise SelectionError(slug, f"unknown slug: {slug}")
        if key not in seen:
            seen.add(key)
            enabled_keys.append(key)

    def usable(slug):
        entry = models[slug]
        tier = entry["tier"]
        score = entry["score"]
        return tier is not None and tier in tier_order and score is not None

    def family(slug):
        mapped = families.get(slug)
        if mapped is None or not mapped.get("family"):
            raise SelectionError(slug, f"unknown slug: {slug}")
        return mapped["family"]

    if not usable(author_key):
        raise SelectionError(author, f"unknown slug: {author}")

    author_family = family(author_key)
    author_tier = models[author_key]["tier"]
    pool = [slug for slug in enabled_keys if usable(slug)]
    rank_set = [slug for slug in pool if models[slug]["tier"] == author_tier]
    if author_key not in rank_set:
        rank_set.append(author_key)

    distinct_scores = sorted({models[slug]["score"] for slug in rank_set}, reverse=True)
    rank_of_score = {score: index + 1 for index, score in enumerate(distinct_scores)}
    author_rank = rank_of_score[models[author_key]["score"]]
    window_limit = author_rank + 1
    window = []
    for slug in rank_set:
        if slug not in pool:
            continue
        if family(slug) == author_family:
            continue
        if rank_of_score[models[slug]["score"]] <= window_limit:
            window.append(slug)
    if window:
        return _with_speed(rng.choice(window), author, models)

    tier_index = tier_order.index(author_tier)
    if tier_index + 1 >= len(tier_order):
        return _with_speed(author_key, author, models)
    next_tier = tier_order[tier_index + 1]
    next_members = [slug for slug in pool if models[slug]["tier"] == next_tier]

    def cheapest(candidates):
        priced = [
            slug
            for slug in candidates
            if models[slug]["output_cost_per_million"] is not None
        ]
        if not priced:
            return None
        lowest = min(models[slug]["output_cost_per_million"] for slug in priced)
        tied = [
            slug
            for slug in priced
            if models[slug]["output_cost_per_million"] == lowest
        ]
        return rng.choice(tied)

    different = [slug for slug in next_members if family(slug) != author_family]
    chosen = cheapest(different)
    if chosen is None:
        chosen = cheapest(next_members)
    if chosen is None:
        return _with_speed(author_key, author, models)
    return _with_speed(chosen, author, models)


def _with_speed(chosen, author, models):
    """Return ``chosen``, or ``chosen`` plus ``-fast``.

    Cost ranking has already finished on the base price. The suffix is
    applied only when the author was the fast half of its pair and this
    model has a fast variant.
    """
    if author.endswith(_FAST_SUFFIX) and models[chosen].get("has_fast"):
        return chosen + _FAST_SUFFIX
    return chosen


def build_catalog(benchlm, pricing_markdown, mapping, previous):
    """Return a catalog and the warnings produced while building it.

    ``benchlm`` is the parsed BenchLM models document. ``pricing_markdown``
    is the Cursor pricing page. ``mapping`` and ``previous`` are the
    parsed mapping and the catalog from the last refresh.

    The score is the equal-weight mean of the BenchLM agentic, coding,
    and reasoning category scores that are present. An interim score is
    kept only when all three are missing, and replaced once any of them
    appears. ``tier_order`` and each existing tier are copied from
    ``previous``. A slug that was not in ``previous`` gets ``tier`` null.

    ``has_fast`` is true when the pricing page has a ``(Fast)`` row for
    that model, or the model's notes mention a fast mode. The fast price
    is not stored. Ranking uses the base output price. ``output_multiplier``
    scales that base price when a mapping row sets it; otherwise it is 1.
    """
    prices, notes = _pricing_rows(pricing_markdown)
    previous_models = (previous or {}).get("models") or {}
    tier_order = list((previous or {}).get("tier_order") or [])
    models = {}
    warnings = []
    for slug, row in mapping["models"].items():
        if slug in previous_models:
            tier = previous_models[slug].get("tier")
        else:
            tier = None
            warnings.append(f"WARNING: must set tier for {slug}")
        present = _category_values(benchlm, row.get("benchlm_slug"))
        if present:
            score = sum(present) / len(present)
            source = "benchlm"
        elif row.get("interim_score") is not None:
            score = row["interim_score"]
            source = "interim"
        else:
            score = None
            source = None
            warnings.append(f"WARNING: must set interim score for {slug}")
        pricing_name = row.get("pricing_name")
        raw_price = prices.get(pricing_name) if pricing_name in prices else None
        if raw_price is None:
            cost = None
            warnings.append(f"WARNING: must set cost for {slug}")
        else:
            multiplier = row.get("output_multiplier")
            if multiplier is None:
                multiplier = 1
            cost = raw_price * multiplier
        models[slug] = {
            "tier": tier,
            "score": score,
            "score_source": source,
            "output_cost_per_million": cost,
            "has_fast": _has_fast(pricing_name, prices, notes),
        }
    return {"tier_order": tier_order, "models": models}, warnings


def _has_fast(pricing_name, prices, notes):
    if not pricing_name:
        return False
    fast_name = f"{pricing_name} (Fast)"
    if prices.get(fast_name) is not None:
        return True
    text = notes.get(pricing_name) or ""
    return "fast mode" in text.lower()


def _split_row(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _tables(markdown):
    tables = []
    current = []
    for line in markdown.splitlines():
        if line.strip().startswith("|"):
            current.append(line)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def _model_name(cell):
    match = _LINK.fullmatch(cell.strip())
    if match:
        return match.group(1).strip()
    return cell.strip()


def _parse_price(cell):
    text = cell.strip().lstrip("$").replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _pricing_rows(markdown):
    prices = {}
    notes = {}
    for table in _tables(markdown):
        header = _split_row(table[0])
        try:
            model_at = header.index("Model")
            output_at = header.index("Output")
        except ValueError:
            continue
        for line in table[1:]:
            cells = _split_row(line)
            if cells and all(_SEPARATOR.fullmatch(cell) for cell in cells if cell):
                continue
            if model_at >= len(cells) or output_at >= len(cells):
                continue
            name = _model_name(cells[model_at])
            if not name or name in prices:
                continue
            prices[name] = _parse_price(cells[output_at])
            notes[name] = cells[-1] if cells else ""
    return prices, notes


def _category_values(benchlm, benchlm_slug):
    if not benchlm_slug or not isinstance(benchlm, dict):
        return []
    for item in benchlm.get("items") or []:
        if item.get("slug") != benchlm_slug:
            continue
        categories = (item.get("scores") or {}).get("displayCategoryScores") or {}
        return [
            categories[key]
            for key in _CATEGORIES
            if categories.get(key) is not None
        ]
    return []
