from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
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


CONFIRMATION = "DELETE-CUSTOMETRY-OWNED-PATHS"


@dataclass(frozen=True, slots=True)
class Candidate:
    path: Path
    size: int


def _size(path: Path) -> int:
    if path.is_symlink() or path.is_file():
        return path.lstat().st_size
    return sum(item.lstat().st_size for item in path.rglob("*") if item.is_file() or item.is_symlink())


def _manifest(data: JsonObject) -> list[str]:
    if data.get("schema_version") != 1:
        raise ValueError("ownership manifest requires schema_version=1")
    return string_list(data.get("owned_paths"), "owned_paths", non_empty=True)


def collect(root: Path, manifest: Path, result: CheckResult) -> list[Candidate]:
    if not require_file(manifest, result, "ownership-manifest-missing"):
        return []
    try:
        paths = _manifest(load_json(manifest))
    except ValueError as exc:
        result.add("ownership-manifest-invalid", str(exc), manifest)
        return []
    candidates: list[Candidate] = []
    resolved_root = root.resolve()
    for raw in paths:
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            result.add("unsafe-owned-path", "owned path must be relative and cannot contain `..`", raw)
            continue
        target = root / relative
        resolved = target.resolve(strict=False)
        if resolved == resolved_root or resolved_root not in resolved.parents:
            result.add("unsafe-owned-path", "owned path escapes repository or selects its root", raw)
            continue
        if target.exists() or target.is_symlink():
            candidates.append(Candidate(target, _size(target)))
    return sorted(candidates, key=lambda item: item.path.as_posix())


def check(
    root: Path,
    manifest: Path,
    *,
    apply: bool = False,
    confirm: str | None = None,
) -> CheckResult:
    result = CheckResult("cleanup")
    manifest_path = manifest if manifest.is_absolute() else root / manifest
    candidates = collect(root, manifest_path, result)
    if result.findings:
        return result
    result.details.update(
        mode="apply" if apply else "dry-run",
        candidates=[str(item.path.relative_to(root)) for item in candidates],
        bytes=sum(item.size for item in candidates),
    )
    if not apply:
        return result
    if confirm != CONFIRMATION:
        result.add("cleanup-confirmation-required", f"--confirm must equal {CONFIRMATION}")
        return result
    for candidate in candidates:
        if candidate.path.is_symlink() or candidate.path.is_file():
            candidate.path.unlink()
        elif candidate.path.is_dir():
            shutil.rmtree(candidate.path)
    remaining = [item.path for item in candidates if item.path.exists() or item.path.is_symlink()]
    if remaining:
        result.add("cleanup-postcondition-failed", f"paths remain: {remaining}")
    result.details["deleted"] = len(candidates) - len(remaining)
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safely clean only manifest-owned paths")
    add_common_arguments(parser)
    parser.add_argument("--ownership-manifest", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="delete candidates; default is dry-run")
    parser.add_argument("--confirm", help=f"required with --apply: {CONFIRMATION}")
    args = parser.parse_args(argv)
    return render_result(
        check(
            args.root.resolve(),
            args.ownership_manifest,
            apply=args.apply,
            confirm=args.confirm,
        ),
        args.json,
    )


if __name__ == "__main__":
    main_guard(cli)
