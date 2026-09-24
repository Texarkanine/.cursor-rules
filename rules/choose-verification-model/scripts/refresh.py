#!/usr/bin/env python3
"""Catalog refresh: BenchLM category means and Cursor output prices."""

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from modelpool import build_catalog, fill_mapping

BENCHLM_URL = "https://benchlm.ai/data/models.json"
PRICING_URL = "https://cursor.com/docs/models-and-pricing.md"
_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def main(
    argv,
    *,
    benchlm=None,
    pricing_markdown=None,
    mapping=None,
    previous=None,
    dest=None,
    agent_models=None,
) -> int:
    """Fetch upstream catalogs and write ``assets/catalog.json``.

    ``argv`` has no required arguments. The keyword arguments inject
    already-loaded inputs for tests. When they are omitted, this
    function reads ``assets/mapping.json`` and ``assets/catalog.json``,
    fetches the BenchLM and pricing URLs, and writes the catalog back
    to ``assets/``. Warnings go to stderr.

    ``agent_models`` is the ``agent --list-models`` output. A string is
    that listing. ``False`` means no listing is available. ``None``
    runs ``agent --list-models``; a missing or failing command is
    treated as ``False``. With a listing, rows for listed models that
    mapping lacks are filled in. Without one, refresh warns once and
    skips the fill-in. The mapping is written as ``mapping.json`` next
    to the catalog.

    BenchLM rejects the default urllib user agent, so the request
    names this tool.
    """
    argparse.ArgumentParser(prog="refresh.py").parse_args(argv)
    if mapping is None:
        mapping = json.loads((_ASSETS / "mapping.json").read_text(encoding="utf-8"))
    if previous is None:
        previous_path = _ASSETS / "catalog.json"
        if previous_path.exists():
            previous = json.loads(previous_path.read_text(encoding="utf-8"))
        else:
            previous = {"tier_order": [], "models": {}}
    if benchlm is None:
        benchlm = json.loads(_fetch(BENCHLM_URL))
    if pricing_markdown is None:
        pricing_markdown = _fetch(PRICING_URL)
    if agent_models is None:
        agent_models = _list_models()
    if agent_models is False:
        fill_warnings = ["WARNING: agent --list-models unavailable; skipped model fill-in"]
    else:
        mapping, fill_warnings = fill_mapping(agent_models, mapping, pricing_markdown, benchlm)
    catalog, warnings = build_catalog(benchlm, pricing_markdown, mapping, previous)
    target = Path(dest) if dest is not None else _ASSETS / "catalog.json"
    target.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    target.with_name("mapping.json").write_text(
        json.dumps(mapping, indent=2) + "\n", encoding="utf-8"
    )
    for warning in fill_warnings + warnings:
        print(warning, file=sys.stderr)
    return 0


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
