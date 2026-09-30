#!/usr/bin/env python3
"""Catalog refresh: BenchLM category means and Cursor output prices."""

import argparse
import json
import shutil
import subprocess
import sys
import tomllib
import urllib.request
from pathlib import Path

from homeassets import is_source_tree, merge_documents, overlay_tiers, user_assets_dir
from modelpool import build_catalog, fill_mapping, previous_from_tiers

BENCHLM_URL = "https://benchlm.ai/data/models.json"
PRICING_URL = "https://cursor.com/docs/models-and-pricing.md"
_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def main(
    argv,
    *,
    benchlm=None,
    pricing_markdown=None,
    mapping=None,
    tiers=None,
    dest=None,
    agent_models=None,
    assets_dir=None,
    user_dir=None,
) -> int:
    """Fetch upstream catalogs and write the catalog and the mapping.

    ``argv`` has no required arguments. The keyword arguments inject
    already-loaded inputs for tests. Warnings go to stderr.

    ``dest``, when passed, is the catalog path. Inputs then come from
    the keyword arguments or from this skill's ``assets/``, and the
    mapping is written beside ``dest``.

    When ``dest`` is omitted and this file's skill directory is
    ``rules/choose-verification-model``, that tree's ``assets/`` is
    read and written. The home directory is not read. From any other
    install, the shipped mapping and tiers are merged with the home
    directory, and ``catalog.json`` and ``mapping.json`` are written
    there. ``assets_dir`` and ``user_dir`` override those directories
    in tests. ``tiers.toml`` is never written.

    ``tiers`` is the parsed ``tiers.toml``: the operator's hand-set
    tiers, and the only source of catalog tiers. Refresh never writes
    that file. Reading it needs Python 3.11 or later (``tomllib``).

    ``agent_models`` is the ``agent --list-models`` output. A string is
    that listing. ``False`` means no listing is available. ``None``
    runs ``agent --list-models``; a missing or failing command is
    treated as ``False``. With a listing, rows for listed models that
    mapping lacks are filled in, and a listed model's ``has_fast``
    follows its listed ``-fast`` spellings. Without one, refresh warns
    once, skips the fill-in, and takes ``has_fast`` from the pricing
    page. The mapping is written as ``mapping.json`` next to the
    catalog.

    BenchLM rejects the default urllib user agent, so the request
    names this tool.
    """
    argparse.ArgumentParser(prog="refresh.py").parse_args(argv)
    if dest is not None:
        if mapping is None:
            mapping = json.loads((_ASSETS / "mapping.json").read_text(encoding="utf-8"))
        if tiers is None:
            tiers = tomllib.loads((_ASSETS / "tiers.toml").read_text(encoding="utf-8"))
        return _publish(
            Path(dest), mapping, tiers, benchlm, pricing_markdown, agent_models
        )

    assets = Path(assets_dir) if assets_dir is not None else _ASSETS
    if is_source_tree(assets.parent):
        if mapping is None:
            mapping = json.loads((assets / "mapping.json").read_text(encoding="utf-8"))
        if tiers is None:
            tiers = tomllib.loads((assets / "tiers.toml").read_text(encoding="utf-8"))
        return _publish(
            assets / "catalog.json",
            mapping,
            tiers,
            benchlm,
            pricing_markdown,
            agent_models,
        )

    home = Path(user_dir) if user_dir is not None else user_assets_dir()
    if mapping is None:
        shipped_mapping = json.loads((assets / "mapping.json").read_text(encoding="utf-8"))
        user_mapping = _read_json_if_present(home / "mapping.json")
        _ignored, mapping = merge_documents(
            {"tier_order": [], "models": {}},
            shipped_mapping,
            None,
            user_mapping,
            None,
        )
    if tiers is None:
        shipped_tiers = tomllib.loads((assets / "tiers.toml").read_text(encoding="utf-8"))
        user_tiers = _read_tiers_if_present(home / "tiers.toml")
        if user_tiers is None:
            tiers = shipped_tiers
        else:
            tiers = overlay_tiers(shipped_tiers, user_tiers)
    home.mkdir(parents=True, exist_ok=True)
    return _publish(home / "catalog.json", mapping, tiers, benchlm, pricing_markdown, agent_models)


def _publish(target, mapping, tiers, benchlm, pricing_markdown, agent_models):
    """Build the catalog and write it and the mapping. Never writes tiers."""
    if benchlm is None:
        benchlm = json.loads(_fetch(BENCHLM_URL))
    if pricing_markdown is None:
        pricing_markdown = _fetch(PRICING_URL)
    if agent_models is None:
        agent_models = _list_models()
    if agent_models is False:
        listing = None
        fill_warnings = ["WARNING: agent --list-models unavailable; skipped model fill-in"]
    else:
        listing = agent_models
        mapping, fill_warnings = fill_mapping(listing, mapping, pricing_markdown, benchlm)
    previous, tier_warnings = previous_from_tiers(tiers, mapping)
    catalog, warnings = build_catalog(
        benchlm, pricing_markdown, mapping, previous, listing=listing
    )
    target = Path(target)
    target.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    target.with_name("mapping.json").write_text(
        json.dumps(mapping, indent=2) + "\n", encoding="utf-8"
    )
    for warning in fill_warnings + tier_warnings + warnings:
        print(warning, file=sys.stderr)
    return 0


def _read_json_if_present(path):
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_tiers_if_present(path):
    if not path.is_file():
        return None
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _list_models():
    """Return ``agent --list-models`` output, or ``False`` when it is unavailable."""
    command = shutil.which("agent")
    if command is None:
        return False
    try:
        result = subprocess.run(
            [command, "--list-models"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    if result.returncode != 0:
        return False
    return result.stdout


def _fetch(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "choose-verification-model"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
