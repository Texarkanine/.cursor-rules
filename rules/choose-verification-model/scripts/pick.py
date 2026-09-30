#!/usr/bin/env python3
"""Print one verification-model slug."""

import argparse
import random
import sys
from pathlib import Path

from homeassets import load_effective, user_assets_dir
from modelpool import SelectionError, select

_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def main(argv, *, catalog=None, mapping=None, assets_dir=None, user_dir=None) -> int:
    """Parse arguments and print the chosen slug.

    ``argv`` is the argument list after the program name. ``catalog``
    and ``mapping`` are parsed JSON objects. When both are passed, no
    asset file is read. When either is omitted, that document is the
    merge of ``assets_dir`` with ``user_dir``. ``assets_dir`` defaults
    to ``assets/`` in this skill. ``user_dir`` defaults to
    ``user_assets_dir()``.

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
    if catalog is None or mapping is None:
        loaded_catalog, loaded_mapping = load_effective(
            assets_dir if assets_dir is not None else _ASSETS,
            user_dir if user_dir is not None else user_assets_dir(),
        )
        if catalog is None:
            catalog = loaded_catalog
        if mapping is None:
            mapping = loaded_mapping
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
