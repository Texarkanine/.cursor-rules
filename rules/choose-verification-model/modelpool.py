"""Shared selection and catalog-refresh helpers.

``select`` chooses one reviewer slug. ``build_catalog`` is added with
the refresh executable.
"""


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
