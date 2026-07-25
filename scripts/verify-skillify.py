#!/usr/bin/env python3
"""Verify description-rules→skills migration end state (B1–B8, I2)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"
RULESETS = ROOT / "rulesets"

DESCRIPTION_SKILLS = [
    "bash-style",
    "cursor-conversation-transcript",
    "cursor-create-rule",
    "github-open-a-pull-request-gh",
    "how-to-script-it-instead",
    "planning-execution",
    "shell-posix-style",
    "shell-tdd",
    "task-list-management",
    "visual-planning",
]

COMMAND_SKILLS = [
    "pr-feedback-judge",
    "wiggum-niko-coderabbit-pr",
]

KEEP_AS_RULES = [
    "always-tdd",
    "git-safety",
    "niko-core",
    "script-it-instead",
    "test-running-practices",
    "markdown-style",
    "java-gradle-tdd",
]

EXISTING_SKILLS = [
    "architecture-docs",
    "prompt-authoring",
    "xy-problem",
]

# ruleset-local name → canonical rules/<name> directory
RULESET_SKILL_LINKS = [
    ("shell", "bash-style", "bash-style"),
    ("shell", "shell-posix-style", "shell-posix-style"),
    ("shell", "shell-tdd", "shell-tdd"),
    ("script-it", "how-to-script-it-instead", "how-to-script-it-instead"),
    ("meta", "conversation-transcript", "cursor-conversation-transcript"),
    ("meta", "create-cursor-rule", "cursor-create-rule"),
    ("authoring", "visual-planning", "visual-planning"),
    ("niko", "visual-planning", "visual-planning"),
]

FM_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    if not m:
        return {}
    data: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        data[key.strip()] = val.strip().strip('"').strip("'")
    return data


def classify_mdc(path: Path) -> str:
    """Mirror a16n priority: alwaysApply → GlobalPrompt; globs → FileRule; else description → SimpleAgentSkill."""
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    always = fm.get("alwaysApply", "").lower()
    if always == "true":
        return "GlobalPrompt"
    globs = fm.get("globs")
    if globs is not None and globs != "":
        return "FileRule"
    desc = fm.get("description", "")
    if desc:
        return "SimpleAgentSkill"
    return "Unknown"


def check(cond: bool, label: str, errors: list[str]) -> None:
    if not cond:
        errors.append(label)


def main() -> int:
    errors: list[str] = []

    # B1: among remaining rules/*.mdc, SimpleAgentSkill set must be empty (end state).
    # Mid-migration baseline is recorded separately; end-state B1 ≡ B7.
    mdc_files = sorted(RULES.glob("*.mdc"))
    simple = [p.stem for p in mdc_files if classify_mdc(p) == "SimpleAgentSkill"]
    check(
        simple == [],
        f"B1/B7: residual SimpleAgentSkill .mdc: {simple}",
        errors,
    )

    # B2: each description rule landed as skill, source .mdc gone
    for name in DESCRIPTION_SKILLS:
        skill = RULES / name / "SKILL.md"
        mdc = RULES / f"{name}.mdc"
        check(skill.is_file(), f"B2: missing {skill.relative_to(ROOT)}", errors)
        if skill.is_file():
            fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
            check(
                bool(fm.get("description")),
                f"B2: empty description in {skill.relative_to(ROOT)}",
                errors,
            )
        check(not mdc.exists(), f"B2: source still present {mdc.relative_to(ROOT)}", errors)

    # B3: commands hand-wrapped as ManualPrompt skills
    for name in COMMAND_SKILLS:
        skill = RULES / name / "SKILL.md"
        src = RULES / f"{name}.md"
        check(skill.is_file(), f"B3: missing {skill.relative_to(ROOT)}", errors)
        if skill.is_file():
            text = skill.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            check(
                fm.get("disable-model-invocation", "").lower() == "true",
                f"B3: {skill.relative_to(ROOT)} missing disable-model-invocation: true",
                errors,
            )
            check(
                fm.get("description") == f"Invoke with /{name}",
                f"B3: {skill.relative_to(ROOT)} description must be Invoke with /{name}",
                errors,
            )
        check(not src.exists(), f"B3: source still present {src.relative_to(ROOT)}", errors)

    # B4: keep-as-rules intact
    for name in KEEP_AS_RULES:
        mdc = RULES / f"{name}.mdc"
        check(mdc.is_file(), f"B4: missing keep-as-rule {mdc.relative_to(ROOT)}", errors)
        if mdc.is_file():
            kind = classify_mdc(mdc)
            check(
                kind in ("GlobalPrompt", "FileRule"),
                f"B4: {name}.mdc classified as {kind}, expected GlobalPrompt|FileRule",
                errors,
            )

    # B5: existing skills intact
    for name in EXISTING_SKILLS:
        skill = RULES / name / "SKILL.md"
        check(skill.is_file(), f"B5: missing existing skill {skill.relative_to(ROOT)}", errors)

    # B6 / I2: ruleset skill symlinks resolve; no dangling .mdc symlinks to converted sources
    for ruleset, local, target in RULESET_SKILL_LINKS:
        link = RULESETS / ruleset / "skills" / local
        expected = (RULES / target).resolve()
        check(link.is_symlink(), f"B6: missing symlink {link.relative_to(ROOT)}", errors)
        if link.is_symlink() or link.exists():
            check(
                link.exists(),
                f"B6/I2: dangling symlink {link.relative_to(ROOT)}",
                errors,
            )
            if link.exists():
                check(
                    link.resolve() == expected,
                    f"B6: {link.relative_to(ROOT)} → {link.resolve()} != {expected}",
                    errors,
                )
        # meta used short names; shell/script-it/authoring/niko used same stem as target
        if ruleset == "meta":
            stale_candidates = [
                RULESETS / "meta" / "conversation-transcript.mdc"
                if local == "conversation-transcript"
                else RULESETS / "meta" / "create-cursor-rule.mdc"
            ]
        else:
            stale_candidates = [RULESETS / ruleset / f"{local}.mdc"]
        for stale_path in stale_candidates:
            # Path.exists() is False for dangling symlinks; use lexists via is_symlink|exists.
            stale_present = stale_path.is_symlink() or stale_path.exists()
            check(
                not stale_present,
                f"B6: stale ruleset .mdc symlink still present {stale_path.relative_to(ROOT)}",
                errors,
            )

    # B8: no residual frontmatter-less command .md at rules/ top level
    for path in sorted(RULES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        check(
            text.lstrip().startswith("---"),
            f"B8: residual command-like file without skill wrap: {path.relative_to(ROOT)}",
            errors,
        )

    # script-it GlobalPrompt must remain as ruleset rule symlink
    gp = RULESETS / "script-it" / "script-it-instead.mdc"
    check(
        gp.is_symlink() and gp.exists(),
        "B4/B6: rulesets/script-it/script-it-instead.mdc GlobalPrompt symlink missing",
        errors,
    )

    if errors:
        print("FAIL — verify-skillify")
        for e in errors:
            print(f"  - {e}")
        print(f"\n{len(errors)} assertion(s) failed")
        return 1

    print("PASS — verify-skillify (B1–B8, I2)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
