#!/usr/bin/env python3
"""Audit helper: enumerate `alwaysApply: false` niko content files.

Walks `rulesets/niko/niko/` recursively. For each `*.mdc` file it reads the
leading YAML frontmatter and includes the file iff `alwaysApply: false` is
present. Emits a JSON index at `scripts/migration-audit.json` mapping each
included file to:

    {
        "old_path": "rulesets/niko/niko/<subtree>/<name>.mdc",
        "new_path": "rulesets/niko/skills/niko/resources/<subtree>/<name>.md",
        "old_ref":  ".cursor/rules/shared/niko/<subtree>/<name>.mdc",
        "new_ref":  ".cursor/skills/shared/niko/resources/<subtree>/<name>.md",
        "had_frontmatter": true
    }

Explicit skip list (stay as rules): `memory-bank-paths.mdc`.

The `memory-bank/**` subtree uses File Rules (`globs:`) and will never match
`alwaysApply: false`, but is also pre-filtered defensively.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_ROOT = REPO_ROOT / "rulesets" / "niko" / "niko"
DEST_ROOT_REL = Path("rulesets/niko/skills/niko/resources")
OUTPUT = REPO_ROOT / "scripts" / "migration-audit.json"

OLD_REF_ROOT = ".cursor/rules/shared/niko"
NEW_REF_ROOT = ".cursor/skills/shared/niko/resources"

SKIP_NAMES = {"memory-bank-paths.mdc"}
SKIP_SUBTREE_PREFIX = ("memory-bank",)

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
ALWAYS_APPLY_FALSE_RE = re.compile(r"^\s*alwaysApply\s*:\s*false\s*$", re.MULTILINE)


def read_frontmatter(path: Path) -> tuple[str | None, bool]:
    """Return (frontmatter_body, had_frontmatter). Body excludes the --- fences."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, False
    return m.group(1), True


def is_in_scope(path: Path) -> bool:
    if path.name in SKIP_NAMES:
        return False
    rel = path.relative_to(SCAN_ROOT)
    # Skip memory-bank subtree defensively.
    if rel.parts and rel.parts[0] in SKIP_SUBTREE_PREFIX:
        return False
    fm, had = read_frontmatter(path)
    if not had or fm is None:
        return False
    return bool(ALWAYS_APPLY_FALSE_RE.search(fm))


def build_record(path: Path) -> dict[str, object]:
    rel = path.relative_to(SCAN_ROOT)
    subtree = rel.parent
    stem = rel.stem
    new_name = f"{stem}.md"
    new_path = DEST_ROOT_REL / subtree / new_name
    old_ref = f"{OLD_REF_ROOT}/{rel.as_posix()}"
    new_subtree = subtree.as_posix()
    new_ref = f"{NEW_REF_ROOT}/{new_subtree + '/' if new_subtree and new_subtree != '.' else ''}{new_name}"
    old_path_rel = path.relative_to(REPO_ROOT).as_posix()
    return {
        "old_path": old_path_rel,
        "new_path": new_path.as_posix(),
        "old_ref": old_ref,
        "new_ref": new_ref,
        "had_frontmatter": True,
    }


def collect_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(SCAN_ROOT.rglob("*.mdc")):
        if is_in_scope(path):
            records.append(build_record(path))
    return records


def print_table(records: list[dict[str, object]]) -> None:
    widths = {
        "old_path": max((len(str(r["old_path"])) for r in records), default=0),
        "new_path": max((len(str(r["new_path"])) for r in records), default=0),
    }
    header = f"{'OLD PATH':<{widths['old_path']}}  →  {'NEW PATH':<{widths['new_path']}}"
    print(header)
    print("-" * len(header))
    for r in records:
        print(f"{r['old_path']:<{widths['old_path']}}  →  {r['new_path']:<{widths['new_path']}}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print-table", action="store_true", help="Print human-readable path mapping table")
    ap.add_argument("-o", "--output", default=str(OUTPUT), help=f"Output JSON path (default: {OUTPUT})")
    args = ap.parse_args()

    if not SCAN_ROOT.is_dir():
        print(f"ERROR: scan root does not exist: {SCAN_ROOT}", file=sys.stderr)
        return 2

    records = collect_records()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    print(f"Audited {len(records)} file(s). Index written to: {out_path}")
    if args.print_table:
        print()
        print_table(records)
    return 0


if __name__ == "__main__":
    sys.exit(main())
