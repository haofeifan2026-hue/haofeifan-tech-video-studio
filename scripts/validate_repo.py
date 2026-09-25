#!/usr/bin/env python3
from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/end-to-end-production.md",
    "references/content-driven-broll.md",
    "references/quality-gates.md",
    "references/style-presets.md",
    "references/integrations.md",
    "references/upgrading.md",
    "scripts/compose_vertical_still.py",
    "scripts/install.sh",
)
FORBIDDEN_PORTABLE_PATHS = ("/" + "Users/", "/var/" + "folders/")
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_frontmatter(errors: list[str]) -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", skill, flags=re.DOTALL)
    if not match:
        errors.append("SKILL.md must start with YAML frontmatter")
        return
    frontmatter = match.group(1)
    if not re.search(r"^name:\s+haofeifan-tech-video-studio\s*$", frontmatter, re.MULTILINE):
        errors.append("SKILL.md has an unexpected or missing name")
    description = re.search(r"^description:\s+(.+)$", frontmatter, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 40:
        errors.append("SKILL.md description is missing or too short")


def check_links(errors: list[str]) -> None:
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (markdown.parent / target).resolve()
            if not resolved.exists():
                relative = markdown.relative_to(ROOT)
                errors.append(f"broken local link in {relative}: {raw_target}")


def check_portability(errors: list[str]) -> None:
    extensions = {".md", ".py", ".sh", ".yaml", ".yml"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in extensions or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_PORTABLE_PATHS:
            if forbidden in text:
                errors.append(f"non-portable absolute path in {path.relative_to(ROOT)}: {forbidden}")


def check_python(errors: list[str]) -> None:
    for directory in (ROOT / "scripts", ROOT / "tests"):
        if not directory.exists():
            continue
        for source in directory.rglob("*.py"):
            try:
                py_compile.compile(str(source), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(f"python compile failed for {source.relative_to(ROOT)}: {exc.msg}")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_frontmatter(errors)
    check_links(errors)
    check_portability(errors)
    check_python(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    print(f"Checked {len(REQUIRED_FILES)} required files, local links, portability, and Python syntax.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
