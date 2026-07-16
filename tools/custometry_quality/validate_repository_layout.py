from __future__ import annotations

import argparse
import fnmatch
import subprocess
from pathlib import Path
from typing import Sequence

from .core import (
    CheckResult,
    JsonObject,
    add_common_arguments,
    load_json,
    main_guard,
    render_result,
    require_file,
    string_list,
)


DEFAULT_MANIFEST = Path(__file__).parent / "contracts/repository-layout.json"


def _validate_manifest(data: JsonObject) -> tuple[list[str], list[str], list[str]]:
    if data.get("schema_version") != 1:
        raise ValueError("layout manifest must be an object with schema_version=1")
    return (
        string_list(data.get("required_files"), "required_files"),
        string_list(data.get("required_directories"), "required_directories"),
        string_list(data.get("forbidden_tracked_globs"), "forbidden_tracked_globs"),
    )


def _tracked_files(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files"], cwd=root, text=True, capture_output=True, check=False
    )
    if completed.returncode != 0:
        raise ValueError(f"git ls-files failed: {completed.stderr.strip()}")
    return [line for line in completed.stdout.splitlines() if line]


def check(root: Path, manifest: Path = DEFAULT_MANIFEST) -> CheckResult:
    result = CheckResult("validate_repository_layout")
    manifest_path = manifest if manifest.is_absolute() else root / manifest
    if not require_file(manifest_path, result):
        return result
    try:
        required_files, required_directories, forbidden_globs = _validate_manifest(
            load_json(manifest_path)
        )
    except ValueError as exc:
        result.add("layout-manifest-invalid", str(exc), manifest_path)
        return result
    for item in required_files:
        if not (root / item).is_file():
            result.add("required-file-missing", "required repository file is absent", item)
    for item in required_directories:
        if not (root / item).is_dir():
            result.add("required-directory-missing", "required repository directory is absent", item)
    try:
        tracked = _tracked_files(root)
    except ValueError as exc:
        result.observed = False
        result.add("git-state-unobserved", str(exc), root)
        return result
    for item in tracked:
        for pattern in forbidden_globs:
            if fnmatch.fnmatch(item, pattern):
                result.add("forbidden-tracked-file", f"tracked path matches {pattern}", item)
    result.details.update(
        required_files=len(required_files),
        required_directories=len(required_directories),
        tracked_files=len(tracked),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate blueprint-aligned repository layout")
    add_common_arguments(parser)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.manifest), args.json)


if __name__ == "__main__":
    main_guard(cli)
