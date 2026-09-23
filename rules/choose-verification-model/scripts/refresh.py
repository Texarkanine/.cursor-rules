#!/usr/bin/env python3
"""Catalog refresh: BenchLM category means and Cursor output prices."""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

from modelpool import build_catalog

BENCHLM_URL = "https://benchlm.ai/data/models.json"
PRICING_URL = "https://cursor.com/docs/models-and-pricing.md"
_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def main(argv, *, benchlm=None, pricing_markdown=None, mapping=None, previous=None, dest=None) -> int:
    """Fetch upstream catalogs and write ``assets/catalog.json``.

    ``argv`` has no required arguments. The keyword arguments inject
    already-loaded inputs for tests. When they are omitted, this
    function reads ``assets/mapping.json`` and ``assets/catalog.json``,
    fetches the BenchLM and pricing URLs, and writes the catalog back
    to ``assets/``. Warnings go to stderr.

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
    catalog, warnings = build_catalog(benchlm, pricing_markdown, mapping, previous)
    target = Path(dest) if dest is not None else _ASSETS / "catalog.json"
    target.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    for warning in warnings:
        print(warning, file=sys.stderr)
    return 0


def _fetch(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "choose-verification-model"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
