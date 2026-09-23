#!/usr/bin/env python3
"""Print one QA or Preflight reviewer slug."""

import argparse
import json
import random
import sys
from pathlib import Path

from modelpool import SelectionError, select


def _read_json(name: str):
    path = Path(__file__).resolve().parent / name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main(argv, *, catalog=None, mapping=None) -> int:
    """Parse arguments and print the chosen slug.

    ``argv`` is the argument list after the program name. ``catalog``
    and ``mapping`` are parsed JSON objects; when either is omitted it
    is loaded from the file beside this script.

    Returns 0 when a slug was printed. Returns 2 when no reviewer can
    be chosen. On failure, stdout is empty and stderr names the slug.
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
