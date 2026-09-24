#!/usr/bin/env python3
"""Print one verification-model slug."""

import argparse
import json
import random
import sys
from pathlib import Path

from modelpool import SelectionError, select

_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def _read_json(name: str):
    path = _ASSETS / name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main(argv, *, catalog=None, mapping=None) -> int:
    """Parse arguments and print the chosen slug.

    ``argv`` is the argument list after the program name. ``catalog``
    and ``mapping`` are parsed JSON objects; when either is omitted it
    is loaded from ``assets/`` in this skill.

    Returns 0 when a slug was printed. That includes an author whose
    model is not in the catalog: stdout is that spelling. An effort
    word on a known model is that model. Returns 2 when an enabled
    slug's model is not in the catalog, or the author row has a null
    tier or null score. On failure, stdout is empty and stderr names
    the slug. When the encoded search leaves an empty pool, the author
    spelling is printed instead of rejected.
    """
    parser = argparse.ArgumentParser(prog="pick.py")
    parser.add_argument("--model", required=True)
    parser.add_argument("--reviewer-models", required=True)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args(argv)
    if catalog is None:
        catalog = _read_json("catalog.json")
    if mapping is None:
        mapping = _read_json("mapping.json")
    enabled = [part.strip() for part in args.reviewer_models.split(",") if part.strip()]
    rng = random.Random(args.seed) if args.seed is not None else random.Random()
    try:
        slug = select(catalog, mapping, args.model, enabled, rng)
    except SelectionError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(slug)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
