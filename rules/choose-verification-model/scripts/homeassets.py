"""Merge shipped skill assets with the XDG home directory.

Pick and refresh call this module. It does not choose a reviewer and
it does not open a network connection.
"""

import copy
import json
import os
import sys
from pathlib import Path

from modelpool import model_key, previous_from_tiers


def user_assets_dir(environ=None, *, home=None, platform=None):
    """Return the home directory that holds this skill's assets.

    ``environ`` is a mapping of environment variables. When it is
    omitted, ``os.environ`` is used. ``home`` is the user's home
    directory. When it is omitted, ``Path.home()`` is used.
    ``platform`` is a ``sys.platform`` value. When it is omitted,
    ``sys.platform`` is used.

    ``XDG_DATA_HOME``, when set and non-empty, is the base on every
    platform. Otherwise platform ``nt`` uses ``LOCALAPPDATA``. Every
    other platform uses ``home / ".local" / "share"``. The directory
    name ``choose-verification-model`` is appended to that base.
    """
    if environ is None:
        environ = os.environ
    if home is None:
        home = Path.home()
    if platform is None:
        platform = sys.platform
    xdg = environ.get("XDG_DATA_HOME")
    if xdg:
        base = Path(xdg)
    elif platform == "nt":
        base = Path(environ["LOCALAPPDATA"])
    else:
        base = Path(home) / ".local" / "share"
    return base / "choose-verification-model"


def is_source_tree(skill_dir):
    """Return whether ``skill_dir`` is the canonical source tree.

    True only when the directory is named ``choose-verification-model``
    and its parent is named ``rules``. An installed copy, whose parent
    is the ruleset name, is false.
    """
    path = Path(skill_dir)
    return path.name == "choose-verification-model" and path.parent.name == "rules"


def overlay_tiers(shipped, user):
    """Return tier lists with each home stem moved onto its home tier.

    ``shipped`` and ``user`` are parsed ``tiers.toml`` documents: tier
    names mapped to lists of slugs. The result is a copy of ``shipped``.
    Each stem named in ``user`` is removed from every shipped list and
    placed on the home tier. ``model_key`` names the stem, so an effort
    spelling matches the shipped slug. The first home listing of a stem
    wins. Inputs are not modified.
    """
    result = {}
    for tier, slugs in shipped.items():
        if isinstance(slugs, list):
            result[tier] = list(slugs)
        else:
            result[tier] = copy.deepcopy(slugs)
    claimed = {}
    for tier, slugs in (user or {}).items():
        if not isinstance(slugs, list):
            continue
        for slug in slugs:
            stem = model_key(slug)
            if stem not in claimed:
                claimed[stem] = tier
    if claimed:
        for tier, slugs in list(result.items()):
            if isinstance(slugs, list):
                result[tier] = [slug for slug in slugs if model_key(slug) not in claimed]
        for stem, tier in claimed.items():
            bucket = result.get(tier)
            if not isinstance(bucket, list):
                bucket = []
                result[tier] = bucket
            bucket.append(stem)
    return result


def merge_documents(
    shipped_catalog, shipped_mapping, user_catalog, user_mapping, user_tiers
):
    """Return ``(catalog, mapping)`` for one pick.

    ``user_catalog``, ``user_mapping``, and ``user_tiers`` are parsed
    documents, or ``None`` when that home file is missing. Mapping rows
    are the union, and a home row replaces the shipped row for the same
    stem. Catalog rows are the union. For a stem in both catalogs, the
    home row supplies score, price, ``has_fast``, and the rest of the
    fields, and the shipped ``tier`` is put back. A stem on only one
    side keeps that row, including its tier. ``tier_order`` is the
    shipped list.

    ``user_tiers`` is then applied with ``previous_from_tiers`` and
    ``model_key``. A stem it names takes that tier. The first listing
    wins. Stems it does not name keep the tier from the catalog step.
    Warnings from that parse are discarded. Inputs are not modified.
    """
    catalog = copy.deepcopy(shipped_catalog)
    mapping = copy.deepcopy(shipped_mapping)
    if user_mapping and user_mapping.get("models"):
        models = mapping.setdefault("models", {})
        for stem, row in user_mapping["models"].items():
            models[stem] = copy.deepcopy(row)
    if user_catalog and user_catalog.get("models"):
        models = catalog.setdefault("models", {})
        shipped_models = shipped_catalog.get("models") or {}
        for stem, row in user_catalog["models"].items():
            if stem in shipped_models:
                merged = copy.deepcopy(row)
                merged["tier"] = copy.deepcopy(shipped_models[stem].get("tier"))
                models[stem] = merged
            else:
                models[stem] = copy.deepcopy(row)
    catalog["tier_order"] = list(shipped_catalog.get("tier_order") or [])
    if user_tiers:
        previous, _warnings = previous_from_tiers(user_tiers, mapping)
        for stem, row in previous["models"].items():
            entry = (catalog.get("models") or {}).get(stem)
            if entry is not None:
                entry["tier"] = row["tier"]
    return catalog, mapping


def load_effective(shipped_dir, user_dir):
    """Read both directories and return the merged catalog and mapping.

    A missing home file is omitted. Invalid JSON raises
    ``json.JSONDecodeError``. ``tiers.toml`` is parsed with ``tomllib``
    only when that file exists.
    """
    shipped_dir = Path(shipped_dir)
    user_dir = Path(user_dir)
    return merge_documents(
        _read_json(shipped_dir / "catalog.json"),
        _read_json(shipped_dir / "mapping.json"),
        _read_optional_json(user_dir / "catalog.json"),
        _read_optional_json(user_dir / "mapping.json"),
        _read_optional_tiers(user_dir / "tiers.toml"),
    )


def _read_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _read_optional_json(path):
    if not path.is_file():
        return None
    return _read_json(path)


def _read_optional_tiers(path):
    if not path.is_file():
        return None
    import tomllib

    return tomllib.loads(path.read_text(encoding="utf-8"))
