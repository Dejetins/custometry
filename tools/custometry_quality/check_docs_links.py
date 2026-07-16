from __future__ import annotations

import argparse
import re
import urllib.parse
from pathlib import Path
from typing import Iterable, Sequence

from .core import CheckResult, add_common_arguments, main_guard, render_result


LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


def slug(text: str) -> str:
    value = re.sub(r"[`*_~]", "", text.strip().lower())
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def anchors(path: Path) -> set[str]:
    return {slug(match.group(1)) for match in HEADING.finditer(path.read_text(encoding="utf-8"))}


def markdown_files(root: Path, inputs: Iterable[Path] | None = None) -> list[Path]:
    if inputs:
        files: list[Path] = []
        for item in inputs:
            resolved = root / item
            if resolved.is_dir():
                files.extend(resolved.rglob("*.md"))
            elif resolved.is_file():
                files.append(resolved)
        return sorted(set(files))
    return sorted(
        [
            *root.glob("*.md"),
            *(root / "docs").rglob("*.md"),
            *(root / "docs-site/docs").rglob("*.md"),
        ]
    )


def check(root: Path, inputs: Iterable[Path] | None = None) -> CheckResult:
    result = CheckResult("check_docs_links")
    files = markdown_files(root, inputs)
    if not files:
        result.observed = False
        result.add("no-documents", "no Markdown files were selected", root)
        return result
    checked = 0
    for source in files:
        text = source.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            raw = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
            if not raw or raw.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            checked += 1
            target_part, _, fragment = raw.partition("#")
            target_part = urllib.parse.unquote(target_part)
            target = source if not target_part else (source.parent / target_part).resolve()
            line = text.count("\n", 0, match.start()) + 1
            if not target.exists():
                result.add("broken-link", f"target does not exist: {raw}", source, line)
                continue
            if fragment and target.is_file() and target.suffix.lower() == ".md":
                expected = urllib.parse.unquote(fragment).lower()
                if expected not in anchors(target):
                    result.add("broken-anchor", f"anchor does not exist: #{fragment}", source, line)
    result.details.update(documents=len(files), local_links=checked)
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate local Markdown links and anchors")
    add_common_arguments(parser)
    parser.add_argument("paths", type=Path, nargs="*")
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.paths or None), args.json)


if __name__ == "__main__":
    main_guard(cli)
