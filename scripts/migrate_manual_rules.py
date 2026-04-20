#!/usr/bin/env python3
"""Migrate manual niko rules → skill resources.

Driven by `scripts/migration-audit.json` (produced by
`scripts/audit_manual_rules.py`). Subcommands:

  preview       Dry-run. Scan the target tree for references to moved files
                and print `<file>:<line> | <old_ref> → <new_ref>`.
  rewrite-refs  Execute. Rewrite every matched reference in place.
  move-files    Execute. `git mv` each source file, rename `.mdc` → `.md`,
                and strip the leading YAML frontmatter block. Supports
                `--dry-run` to preview without mutating.
  verify        Dry-run. Run invariant checks:
                  - zero refs to moved `.cursor/rules/shared/niko/...` paths
                  - still-at-rules refs preserved
                  - every new-form ref resolves to a file on disk
                  - destination tree contains the expected 24 resources

Run `preview` first; gate the operator on its output before running the
destructive subcommands.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT_JSON = REPO_ROOT / "scripts" / "migration-audit.json"
DEFAULT_TARGET_DIR = REPO_ROOT / "rulesets" / "niko"
DEST_RESOURCE_ROOT = REPO_ROOT / "rulesets" / "niko" / "skills" / "niko" / "resources"

# Subset of paths whose `.cursor/rules/shared/niko/...` refs stay unchanged.
STILL_AT_RULES_PREFIXES = (
    ".cursor/rules/shared/niko/core/memory-bank-paths.mdc",
    ".cursor/rules/shared/niko/memory-bank/",
)

# Frontmatter block anchored at line 1, non-greedy. Matches `---\n...\n---\n`
# (and an optional trailing blank line). Does NOT match in-body fenced examples.
FRONTMATTER_LEAD_RE = re.compile(r"\A---\n.*?\n---\n\n?", re.DOTALL)

# File extensions to scan for reference rewrites. Skip binary/lockfile-y types.
SCAN_EXTS = {".md", ".mdc", ".txt", ".json", ".yaml", ".yml", ".py", ".sh"}


@dataclass(frozen=True)
class AuditEntry:
    old_path: str
    new_path: str
    old_ref: str
    new_ref: str
    had_frontmatter: bool


def load_audit(path: Path = AUDIT_JSON) -> list[AuditEntry]:
    if not path.is_file():
        raise SystemExit(
            f"ERROR: audit index missing: {path}\n"
            "Run `scripts/audit_manual_rules.py` first."
        )
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [AuditEntry(**r) for r in raw]


def iter_scan_files(root: Path) -> Iterable[Path]:
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        # Skip the audit JSON itself to avoid self-rewrite noise.
        if p.resolve() == AUDIT_JSON.resolve():
            continue
        yield p


def build_ref_map(entries: list[AuditEntry]) -> dict[str, str]:
    return {e.old_ref: e.new_ref for e in entries}


# ---------- preview / rewrite-refs shared scanner ----------

@dataclass
class Match:
    file: Path
    line_no: int
    old_ref: str
    new_ref: str
    line_text: str


def scan_matches(root: Path, ref_map: dict[str, str]) -> list[Match]:
    """Return all matches in files under `root`."""
    sorted_refs = sorted(ref_map.keys(), key=len, reverse=True)
    matches: list[Match] = []
    for fp in iter_scan_files(root):
        try:
            text = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if not any(r in text for r in sorted_refs):
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for ref in sorted_refs:
                if ref in line:
                    matches.append(Match(fp, i, ref, ref_map[ref], line.rstrip()))
    return matches


def format_match(m: Match, base: Path) -> str:
    rel = m.file.relative_to(base) if m.file.is_relative_to(base) else m.file
    return f"{rel.as_posix()}:{m.line_no} | {m.old_ref} → {m.new_ref}"


def cmd_preview(args: argparse.Namespace) -> int:
    entries = load_audit()
    ref_map = build_ref_map(entries)
    target = Path(args.target_dir).resolve()
    matches = scan_matches(target, ref_map)

    if args.json:
        out = [
            {
                "file": (m.file.relative_to(REPO_ROOT).as_posix()
                         if m.file.is_relative_to(REPO_ROOT) else m.file.as_posix()),
                "line": m.line_no,
                "old_ref": m.old_ref,
                "new_ref": m.new_ref,
                "line_text": m.line_text,
            }
            for m in matches
        ]
        print(json.dumps(out, indent=2))
    else:
        for m in matches:
            print(format_match(m, REPO_ROOT))

    files_touched = len({m.file for m in matches})
    print(f"\n[preview] {len(matches)} ref(s) across {files_touched} file(s). "
          f"No files modified.", file=sys.stderr)
    return 0


def cmd_rewrite_refs(args: argparse.Namespace) -> int:
    entries = load_audit()
    ref_map = build_ref_map(entries)
    target = Path(args.target_dir).resolve()
    matches = scan_matches(target, ref_map)

    # Report first (same shape as preview).
    for m in matches:
        print(format_match(m, REPO_ROOT))

    # Group matches by file and rewrite once per file.
    files_by_path: dict[Path, list[Match]] = {}
    for m in matches:
        files_by_path.setdefault(m.file, []).append(m)

    sorted_refs = sorted(ref_map.keys(), key=len, reverse=True)
    rewritten = 0
    for fp, _file_matches in files_by_path.items():
        text = fp.read_text(encoding="utf-8")
        new_text = text
        for ref in sorted_refs:
            if ref in new_text:
                new_text = new_text.replace(ref, ref_map[ref])
        if new_text != text:
            fp.write_text(new_text, encoding="utf-8")
            rewritten += 1

    print(f"\n[rewrite-refs] WROTE: {rewritten} file(s), "
          f"{len(matches)} ref replacement(s).", file=sys.stderr)
    return 0


# ---------- move-files ----------

def strip_frontmatter(text: str) -> tuple[str, bool]:
    m = FRONTMATTER_LEAD_RE.match(text)
    if not m:
        return text, False
    return text[m.end():], True


def git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "mv", str(src), str(dst)],
        cwd=REPO_ROOT,
        check=True,
    )


def cmd_move_files(args: argparse.Namespace) -> int:
    entries = load_audit()
    dry = args.dry_run

    moved = 0
    stripped = 0
    for e in entries:
        src = REPO_ROOT / e.old_path
        dst = REPO_ROOT / e.new_path
        if not src.is_file():
            print(f"SKIP (source missing): {e.old_path}", file=sys.stderr)
            continue
        if dst.exists():
            print(f"SKIP (dest exists): {e.new_path}", file=sys.stderr)
            continue
        action = "DRY" if dry else "MOVE"
        print(f"[{action}] git mv {e.old_path} → {e.new_path}")
        if dry:
            continue
        git_mv(src, dst)
        moved += 1
        text = dst.read_text(encoding="utf-8")
        new_text, did_strip = strip_frontmatter(text)
        if did_strip:
            dst.write_text(new_text, encoding="utf-8")
            stripped += 1
            print(f"        └─ stripped frontmatter")
        else:
            print(f"        └─ no frontmatter to strip", file=sys.stderr)

    summary = f"[move-files] {'would move' if dry else 'moved'} {moved if not dry else len(entries)} file(s); "
    summary += f"stripped frontmatter in {stripped} file(s)." if not dry else "dry-run."
    print(f"\n{summary}", file=sys.stderr)
    return 0


# ---------- verify ----------

MOVED_OLD_REF_RE = re.compile(
    r"\.cursor/rules/shared/niko/(?:"
    r"core/(?:complexity-analysis|intent-clarification|memory-bank-init|reconcile-persistent)"
    r"|level[1-4]/"
    r"|phases/creative/"
    r")"
)
PRESERVED_OLD_REF_RE = re.compile(
    r"\.cursor/rules/shared/niko/(?:core/memory-bank-paths\.mdc|memory-bank/)"
)
NEW_REF_RE = re.compile(r"\.cursor/skills/shared/niko/resources/[A-Za-z0-9/_\-\.]+\.md")


def _scan_all(root: Path, pattern: re.Pattern[str]) -> list[tuple[Path, int, str]]:
    hits: list[tuple[Path, int, str]] = []
    for fp in iter_scan_files(root):
        try:
            for i, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), start=1):
                for m in pattern.finditer(line):
                    hits.append((fp, i, m.group(0)))
        except UnicodeDecodeError:
            continue
    return hits


def cmd_verify(args: argparse.Namespace) -> int:
    target = Path(args.target_dir).resolve()
    passed = []
    failed = []

    # Check 1: no refs to moved rules remain in target tree.
    moved_hits = _scan_all(target, MOVED_OLD_REF_RE)
    if moved_hits:
        failed.append(
            f"[FAIL] {len(moved_hits)} lingering ref(s) to moved files under "
            f".cursor/rules/shared/niko/..."
        )
        for fp, ln, s in moved_hits[:10]:
            failed.append(f"         {fp.relative_to(REPO_ROOT)}:{ln} {s}")
    else:
        passed.append("[PASS] No refs to moved rules remain.")

    # Check 2: preserved refs still exist (we expect at least one).
    preserved_hits = _scan_all(target, PRESERVED_OLD_REF_RE)
    if preserved_hits:
        passed.append(
            f"[PASS] {len(preserved_hits)} preserved ref(s) to still-at-rules files present."
        )
    else:
        failed.append(
            "[FAIL] No preserved refs found — either nothing referenced them "
            "(unexpected) or they got over-rewritten."
        )

    # Check 3: every new-form ref resolves to a file on disk.
    new_hits = _scan_all(target, NEW_REF_RE)
    resolved = 0
    unresolved: list[tuple[Path, int, str]] = []
    for fp, ln, s in new_hits:
        # s is a `.cursor/skills/shared/niko/resources/...` source-form ref.
        # It maps to `rulesets/niko/skills/niko/resources/...` on disk.
        mapped = s.replace(
            ".cursor/skills/shared/niko/resources/",
            "rulesets/niko/skills/niko/resources/",
            1,
        )
        if (REPO_ROOT / mapped).is_file():
            resolved += 1
        else:
            unresolved.append((fp, ln, s))
    if unresolved:
        failed.append(f"[FAIL] {len(unresolved)} new-form ref(s) do NOT resolve to files on disk.")
        for fp, ln, s in unresolved[:10]:
            failed.append(f"         {fp.relative_to(REPO_ROOT)}:{ln} {s}")
    else:
        passed.append(f"[PASS] All {resolved} new-form ref(s) resolve to files on disk.")

    # Check 4: destination tree has exactly 24 .md files.
    if DEST_RESOURCE_ROOT.is_dir():
        count = sum(1 for _ in DEST_RESOURCE_ROOT.rglob("*.md"))
        if count == 24:
            passed.append(f"[PASS] Destination tree has 24 .md resource files.")
        else:
            failed.append(f"[FAIL] Destination tree has {count} .md files; expected 24.")
    else:
        failed.append(f"[FAIL] Destination tree does not exist: {DEST_RESOURCE_ROOT}")

    for line in passed + failed:
        print(line)
    print()
    if failed:
        print(f"VERIFY: {len(failed)} failure(s).", file=sys.stderr)
        return 1
    print("VERIFY: all checks passed.", file=sys.stderr)
    return 0


# ---------- entrypoint ----------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_prev = sub.add_parser("preview", help="Dry-run: print refs that would be rewritten.")
    p_prev.add_argument("--target-dir", default=str(DEFAULT_TARGET_DIR))
    p_prev.add_argument("--json", action="store_true")
    p_prev.set_defaults(func=cmd_preview)

    p_rw = sub.add_parser("rewrite-refs", help="Execute: rewrite refs in place.")
    p_rw.add_argument("--target-dir", default=str(DEFAULT_TARGET_DIR))
    p_rw.set_defaults(func=cmd_rewrite_refs)

    p_mv = sub.add_parser("move-files", help="Execute: git mv + frontmatter strip for each audit entry.")
    p_mv.add_argument("--dry-run", action="store_true", help="Print intended moves; do not mutate.")
    p_mv.set_defaults(func=cmd_move_files)

    p_ver = sub.add_parser("verify", help="Dry-run: run invariant checks.")
    p_ver.add_argument("--target-dir", default=str(DEFAULT_TARGET_DIR))
    p_ver.set_defaults(func=cmd_verify)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
