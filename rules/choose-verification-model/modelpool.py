"""Shared selection and catalog-refresh helpers.

``select`` chooses one reviewer slug. ``build_catalog`` rebuilds scores
and output prices while keeping hand-set tiers.
"""

import re

_LINK = re.compile(r"\[(.*)\]\([^)]*\)\Z")
_SEPARATOR = re.compile(r":?-{3,}:?\Z")
_CATEGORIES = ("agentic", "coding", "reasoning")


class SelectionError(Exception):
    """A reviewer could not be chosen.

    ``slug`` names the author or reviewer the operator has to fix, when
    one slug is the cause. The message always includes that slug.
    """

    def __init__(self, slug: str, message: str) -> None:
        self.slug = slug
        super().__init__(message)


def select(catalog, mapping, author, enabled, rng):
    """Return one reviewer slug, or raise ``SelectionError``.

    ``catalog`` and ``mapping`` are the parsed JSON objects. ``author``
    is the slug of the model asking for a reviewer. ``enabled`` is the
    Task-tool slug list. ``rng`` is a ``random.Random`` instance; a
    fixed seed makes the choice repeatable.

    Rank is dense rank by score inside the author's tier, best at
    rank 1. The window is a different family, from one rank below the
    author through the best in the tier. An empty window looks up one
    tier and takes the cheapest different family, then the cheapest
    slug in that tier.
    """
    models = catalog["models"]
    tier_order = catalog["tier_order"]
    families = mapping["models"]
    if author not in models:
        raise SelectionError(author, f"unknown slug: {author}")
    for slug in enabled:
        if slug not in models:
            raise SelectionError(slug, f"unknown slug: {slug}")

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

    if not usable(author):
        raise SelectionError(author, f"unknown slug: {author}")

    author_family = family(author)
    author_tier = models[author]["tier"]
    pool = [slug for slug in enabled if usable(slug)]
    rank_set = [slug for slug in pool if models[slug]["tier"] == author_tier]
    if author not in rank_set:
        rank_set.append(author)

    distinct_scores = sorted({models[slug]["score"] for slug in rank_set}, reverse=True)
    rank_of_score = {score: index + 1 for index, score in enumerate(distinct_scores)}
    author_rank = rank_of_score[models[author]["score"]]
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
        return rng.choice(window)

    tier_index = tier_order.index(author_tier)
    if tier_index + 1 >= len(tier_order):
        raise SelectionError(author, f"no reviewer for {author}")
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
        raise SelectionError(author, f"no reviewer for {author}")
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
    ``previous``.     A slug that was not in ``previous`` gets ``tier`` null.
    """
    prices = _output_prices(pricing_markdown)
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
        }
    return {"tier_order": tier_order, "models": models}, warnings


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


def _output_prices(markdown):
    prices = {}
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
    return prices


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
