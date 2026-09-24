"""Shared selection and catalog-refresh helpers.

``select`` chooses one reviewer slug. ``build_catalog`` rebuilds scores
and output prices while keeping hand-set tiers.
"""

import re

_LINK = re.compile(r"\[(.*)\]\([^)]*\)\Z")
_SEPARATOR = re.compile(r":?-{3,}:?\Z")
_CATEGORIES = ("agentic", "coding", "reasoning")
_FAST_SUFFIX = "-fast"
_THINKING_SUFFIX = "-thinking"
_CURSOR_PREFIX = "cursor-"
_LISTING_ROW = re.compile(r"([a-z0-9][a-z0-9.\-]*) - (.+)")
_EFFORTS = ("extra-high", "minimal", "medium", "xhigh", "none", "high", "low", "max")
TIER_ORDER = ("C", "B", "A", "S")
NEVER_TIER = "never"


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


def _split_effort(slug: str):
    """Return ``(stem, effort)`` for a trailing effort word.

    The effort words are the ones ``agent --list-models`` uses:
    ``none``, ``minimal``, ``low``, ``medium``, ``high``, ``xhigh``,
    ``extra-high``, and ``max``. The longest match wins, so
    ``extra-high`` and ``xhigh`` are not read as ``high``. A slug with
    no effort word returns ``(slug, None)``.
    """
    for name in _EFFORTS:
        suffix = f"-{name}"
        if slug.endswith(suffix):
            return slug[: -len(suffix)], name
    return slug, None


def model_key(slug: str) -> str:
    """Return the catalog key for ``slug``.

    A trailing ``-fast`` is the same model. A trailing effort word is
    the same model too. BenchLM does not score effort, so the key is
    the model stem. ``thinking`` stays in the stem. An effort directly
    before ``-thinking`` is removed and ``-thinking`` is kept:
    ``claude-4.6-opus-high-thinking`` is ``claude-4.6-opus-thinking``.
    """
    bare = canonical_slug(slug)
    if bare.endswith(_THINKING_SUFFIX):
        stem, effort = _split_effort(bare[: -len(_THINKING_SUFFIX)])
        if effort is None:
            return bare
        return stem + _THINKING_SUFFIX
    stem, effort = _split_effort(bare)
    if effort is None:
        return bare
    return stem


def _stored_index(models):
    """Map each model stem to the catalog key that stores its row."""
    index = {}
    for stored in models:
        index.setdefault(model_key(stored), stored)
    return index


def select(catalog, mapping, author, enabled, rng):
    """Return one reviewer slug, or raise ``SelectionError``.

    ``catalog`` and ``mapping`` are the parsed JSON objects. ``author``
    is the slug of the model asking for a reviewer. ``enabled`` is the
    Task-tool slug list. ``rng`` is a ``random.Random`` instance; a
    fixed seed makes the choice repeatable.

    A trailing ``-fast`` is stripped before lookup. Fast and non-fast
    spellings of one model are one candidate. A trailing effort word
    is stripped the same way: BenchLM scored the model, not the effort.
    Every effort of a model is that one row. When the author's model
    is not in the catalog, or its tier is ``never``, return that
    spelling. An enabled spelling whose tier is ``never`` is skipped.
    An enabled spelling whose model is not in the catalog still raises
    ``SelectionError``.

    The printed reviewer keeps the effort from the enabled spelling.
    Two efforts of one model are one candidate, and the first spelling
    in ``enabled`` is the one printed. The author's effort is not
    copied onto the reviewer.

    Rank is dense rank by score inside the author's tier, best at
    rank 1. The window is a different family, from one rank below the
    author through the best in the tier. An empty window looks up one
    tier and takes the cheapest different family, then the cheapest
    slug in that tier. Those prices are the base output prices. When
    every encoded step has left the pool empty, return the author
    spelling instead of failing.

    After that choice, append ``-fast`` only when the author slug ended
    in ``-fast`` and the chosen model has a fast variant.
    """
    models = catalog["models"]
    tier_order = catalog["tier_order"]
    families = mapping["models"]
    stored_of = _stored_index(models)
    author_stored = stored_of.get(model_key(author))
    if author_stored is None:
        return author

    enabled_stored = []
    spellings = {}
    seen = set()
    for slug in enabled:
        stored = stored_of.get(model_key(slug))
        if stored is None:
            raise SelectionError(slug, f"unknown slug: {slug}")
        if stored not in seen:
            seen.add(stored)
            enabled_stored.append(stored)
            spellings[stored] = canonical_slug(slug)

    def usable(stored):
        entry = models[stored]
        tier = entry["tier"]
        score = entry["score"]
        return tier is not None and tier in tier_order and score is not None

    def family(stored):
        mapped = families.get(stored)
        if mapped is None or not mapped.get("family"):
            raise SelectionError(stored, f"unknown slug: {stored}")
        return mapped["family"]

    if models[author_stored]["tier"] == NEVER_TIER:
        return author
    if not usable(author_stored):
        raise SelectionError(author, f"unknown slug: {author}")

    author_family = family(author_stored)
    author_tier = models[author_stored]["tier"]
    pool = [stored for stored in enabled_stored if usable(stored)]
    rank_set = [stored for stored in pool if models[stored]["tier"] == author_tier]
    if author_stored not in rank_set:
        rank_set.append(author_stored)

    distinct_scores = sorted(
        {models[stored]["score"] for stored in rank_set}, reverse=True
    )
    rank_of_score = {score: index + 1 for index, score in enumerate(distinct_scores)}
    author_rank = rank_of_score[models[author_stored]["score"]]
    window_limit = author_rank + 1
    window = []
    for stored in rank_set:
        if stored not in pool:
            continue
        if family(stored) == author_family:
            continue
        if rank_of_score[models[stored]["score"]] <= window_limit:
            window.append(stored)
    if window:
        chosen = rng.choice(window)
        return _with_speed(spellings[chosen], author, models[chosen].get("has_fast"))

    tier_index = tier_order.index(author_tier)
    if tier_index + 1 >= len(tier_order):
        return author
    next_tier = tier_order[tier_index + 1]
    next_members = [stored for stored in pool if models[stored]["tier"] == next_tier]

    def cheapest(candidates):
        priced = [
            stored
            for stored in candidates
            if models[stored]["output_cost_per_million"] is not None
        ]
        if not priced:
            return None
        lowest = min(models[stored]["output_cost_per_million"] for stored in priced)
        tied = [
            stored
            for stored in priced
            if models[stored]["output_cost_per_million"] == lowest
        ]
        return rng.choice(tied)

    different = [stored for stored in next_members if family(stored) != author_family]
    chosen = cheapest(different)
    if chosen is None:
        chosen = cheapest(next_members)
    if chosen is None:
        return author
    return _with_speed(spellings[chosen], author, models[chosen].get("has_fast"))


def _with_speed(display, author, has_fast):
    """Return ``display``, or ``display`` plus ``-fast``.

    Cost ranking has already finished on the base price. The suffix is
    applied only when the author was the fast half of its pair and this
    model has a fast variant. ``display`` already carries the effort
    from the review candidate.
    """
    if author.endswith(_FAST_SUFFIX) and has_fast:
        return display + _FAST_SUFFIX
    return display


def parse_listing(listing: str) -> dict:
    """Return ``{stem: display name}`` from ``agent --list-models`` output.

    A row is ``slug - Name``. Other lines are not rows. ``auto`` is not
    a model. Keys are ``model_key`` stems in first-seen order; the
    value is the display name of that stem's first row.
    """
    stems = {}
    for slug, name in _listing_rows(listing):
        stems.setdefault(model_key(slug), name)
    return stems


def _listing_rows(listing):
    for line in listing.splitlines():
        match = _LISTING_ROW.fullmatch(line.strip())
        if match and match.group(1) != "auto":
            yield match.group(1), match.group(2).strip()


def fill_mapping(listing: str, mapping, pricing_markdown: str, benchlm):
    """Return ``(mapping, warnings)`` with rows added for listed models.

    ``listing`` is ``agent --list-models`` output. For each listed stem
    that ``mapping`` lacks, a row ``{family, pricing_name,
    benchlm_slug, interim_score}`` is appended to a copy of the
    mapping. Existing rows are never changed.

    Words are lowercased text split on spaces and hyphens. A pricing
    row matches when its name has no ``(`` and all its words are among
    the display name's words plus the stem's family. The match with
    the most words wins; a longer name breaks a tie. The BenchLM match
    is the single scored item whose slug, split on non-alphanumerics,
    has the same sorted words as the pricing name with dots read as
    separators. The family is the stem's first hyphen word after a
    leading ``cursor-``.

    A stem with no pricing match, no scored BenchLM match, or more than
    one is not added, and a warning names it and the missing source.
    """
    models = dict(mapping["models"])
    prices, _notes = _pricing_rows(pricing_markdown)
    names = [name for name in prices if "(" not in name]
    scored = {}
    items = benchlm.get("items") if isinstance(benchlm, dict) else None
    for item in items or []:
        slug = item.get("slug")
        if isinstance(slug, str) and _category_values(benchlm, slug):
            scored.setdefault(_slug_words(slug), []).append(slug)
    warnings = []
    for stem, display in parse_listing(listing).items():
        if stem in models:
            continue
        family = _family(stem)
        have = set(_words(display)) | {family}
        candidates = [name for name in names if set(_words(name)) <= have]
        if not candidates:
            warnings.append(f"WARNING: unrecognized model {stem}: no pricing row")
            continue
        pricing_name = max(candidates, key=lambda name: (len(_words(name)), len(name)))
        matches = scored.get(_slug_words(pricing_name), [])
        if not matches:
            warnings.append(f"WARNING: unrecognized model {stem}: no BenchLM score")
            continue
        if len(matches) > 1:
            warnings.append(f"WARNING: unrecognized model {stem}: ambiguous BenchLM match")
            continue
        models[stem] = {
            "family": family,
            "pricing_name": pricing_name,
            "benchlm_slug": matches[0],
            "interim_score": None,
        }
    return {**mapping, "models": models}, warnings


def _words(text):
    return [word for word in re.split(r"[\s\-]+", text.lower()) if word]


def _slug_words(text):
    return tuple(sorted(word for word in re.split(r"[^a-z0-9]+", text.lower()) if word))


def _family(stem):
    if stem.startswith(_CURSOR_PREFIX):
        stem = stem[len(_CURSOR_PREFIX) :]
    return stem.split("-")[0]


def previous_from_tiers(doc, mapping):
    """Return ``(previous, warnings)`` for ``build_catalog`` from ``tiers.toml``.

    ``doc`` is the parsed TOML: keys ``S``, ``A``, ``B``, ``C``, and
    ``never``, each a list of slugs. A listed slug goes through
    ``model_key``, so any Cursor spelling of a model names that model.
    ``previous`` is ``{"tier_order": TIER_ORDER, "models": {stem:
    {"tier": tier}}}``. ``never`` is a tier value but not on the ladder.

    Warnings: a key that is not a tier; a stem listed under two tiers
    (the first listing is kept); a listed stem that ``mapping`` lacks.
    """
    tiers = {}
    warnings = []
    for tier, slugs in doc.items():
        if tier not in TIER_ORDER and tier != NEVER_TIER:
            warnings.append(f"WARNING: unknown tier {tier} in tiers.toml")
            continue
        for slug in slugs:
            stem = model_key(slug)
            if stem in tiers:
                kept = tiers[stem]
                warnings.append(
                    f"WARNING: {stem} is listed under {kept} and {tier} in tiers.toml; using {kept}"
                )
                continue
            tiers[stem] = tier
            if stem not in mapping["models"]:
                warnings.append(f"WARNING: tiers.toml lists {stem}, which is not in mapping")
    models = {stem: {"tier": tier} for stem, tier in tiers.items()}
    return {"tier_order": list(TIER_ORDER), "models": models}, warnings


def build_catalog(benchlm, pricing_markdown, mapping, previous, listing=None):
    """Return a catalog and the warnings produced while building it.

    ``benchlm`` is the parsed BenchLM models document. ``pricing_markdown``
    is the Cursor pricing page. ``mapping`` and ``previous`` are the
    parsed mapping and the catalog from the last refresh.

    The score is the equal-weight mean of the BenchLM agentic, coding,
    and reasoning category scores that are present. That mean is the
    model. BenchLM does not encode effort, so ``effort_encoded`` is
    false. An interim score is kept only when all three are missing,
    and replaced once any of them appears. It does not encode effort
    either. ``tier_order`` and each existing tier are copied from
    ``previous``. A slug that was not in ``previous`` gets ``tier``
    null. Every row whose tier is null gets a ``must set tier``
    warning, on every run.

    ``listing`` is ``agent --list-models`` output, or ``None``. For a
    stem the listing names, ``has_fast`` is whether any listed slug for
    that stem ends in ``-fast``: that is the spelling ``pick`` appends.
    For an unlisted stem, or with no listing, ``has_fast`` is true when
    the pricing page has a ``(Fast)`` row for that model, or the
    model's notes mention a fast mode. The fast price is not stored. Ranking uses the base output price. ``output_multiplier``
    scales that base price when a mapping row sets it; otherwise it is 1.
    """
    prices, notes = _pricing_rows(pricing_markdown)
    listed = set()
    listed_fast = set()
    for listed_slug, _name in _listing_rows(listing or ""):
        stem = model_key(listed_slug)
        listed.add(stem)
        if listed_slug.endswith(_FAST_SUFFIX):
            listed_fast.add(stem)
    previous_models = (previous or {}).get("models") or {}
    tier_order = list((previous or {}).get("tier_order") or [])
    models = {}
    warnings = []
    for slug, row in mapping["models"].items():
        tier = (previous_models.get(slug) or {}).get("tier")
        if tier is None:
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
        if slug in listed:
            has_fast = slug in listed_fast
        else:
            has_fast = _has_fast(pricing_name, prices, notes)
        models[slug] = {
            "tier": tier,
            "score": score,
            "score_source": source,
            "effort_encoded": False,
            "output_cost_per_million": cost,
            "has_fast": has_fast,
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
