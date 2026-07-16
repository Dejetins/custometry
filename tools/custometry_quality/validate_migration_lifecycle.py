from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path
from typing import Callable, Sequence, cast

from .core import (
    CheckResult,
    JsonObject,
    add_common_arguments,
    add_command_failure,
    json_object,
    load_json,
    main_guard,
    render_result,
    require_dir,
    require_file,
    run_command,
    string_list,
)


STEPS = ("upgrade_empty", "upgrade_repeat", "downgrade", "reupgrade")


def _revision(path: Path, result: CheckResult) -> tuple[str, tuple[str, ...]] | None:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        result.add("migration-syntax-invalid", str(exc), path, exc.lineno)
        return None
    assigned: dict[str, object] = {}
    functions: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    try:
                        assigned[target.id] = ast.literal_eval(node.value) if node.value else None
                    except (ValueError, TypeError):
                        assigned[target.id] = "dynamic"
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions[node.name] = node
    raw_revision = assigned.get("revision")
    if not isinstance(raw_revision, str) or not raw_revision:
        result.add("migration-revision-missing", "revision string is required", path)
        revision = None
    else:
        revision = raw_revision
    if "down_revision" not in assigned:
        result.add("migration-parent-missing", "down_revision declaration is required", path)
        parents: tuple[str, ...] | None = None
    else:
        raw_parent = assigned["down_revision"]
        if raw_parent is None:
            parents = ()
        elif isinstance(raw_parent, str) and raw_parent:
            parents = (raw_parent,)
        elif isinstance(raw_parent, (tuple, list)):
            parent_values = cast(tuple[object, ...] | list[object], raw_parent)
            if parent_values and all(
                isinstance(item, str) and bool(item) for item in parent_values
            ):
                parents = tuple(cast(tuple[str, ...] | list[str], raw_parent))
            else:
                result.add(
                    "migration-parent-invalid",
                    "down_revision merge tuple must contain revision strings",
                    path,
                )
                parents = None
        else:
            result.add(
                "migration-parent-invalid",
                "down_revision must be null, a revision string, or a non-empty revision tuple",
                path,
            )
            parents = None
    for name in ("upgrade", "downgrade"):
        function = functions.get(name)
        if function is None:
            result.add("migration-function-missing", f"{name}() is required", path)
        elif len(function.body) == 1 and isinstance(function.body[0], ast.Pass):
            result.add("migration-function-empty", f"{name}() cannot be pass", path)
    if revision is None or parents is None:
        return None
    return revision, parents


def _validate_graph(
    revisions: list[tuple[Path, str, tuple[str, ...]]], result: CheckResult
) -> None:
    by_id: dict[str, tuple[Path, tuple[str, ...]]] = {}
    for path, revision, parents in revisions:
        if revision in by_id:
            result.add(
                "migration-revision-duplicate",
                f"revision {revision} is also declared by {by_id[revision][0]}",
                path,
            )
            continue
        by_id[revision] = (path, parents)
    for revision, (path, parents) in by_id.items():
        for parent in parents:
            if parent not in by_id:
                result.add(
                    "migration-parent-unknown",
                    f"revision {revision} references unknown parent {parent}",
                    path,
                )
    roots = [revision for revision, (_, parents) in by_id.items() if not parents]
    if len(roots) != 1:
        result.add("migration-root-count-invalid", f"expected one migration root, got {len(roots)}")
    referenced = {parent for _, parents in by_id.values() for parent in parents}
    heads = set(by_id) - referenced
    if len(heads) != 1:
        result.add("migration-head-count-invalid", f"expected one migration head, got {len(heads)}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(revision: str) -> None:
        if revision in visited or revision not in by_id:
            return
        if revision in visiting:
            result.add("migration-cycle", f"cycle includes revision {revision}", by_id[revision][0])
            return
        visiting.add(revision)
        for parent in by_id[revision][1]:
            visit(parent)
        visiting.remove(revision)
        visited.add(revision)

    for revision in by_id:
        visit(revision)


def _runtime_contract(data: JsonObject) -> dict[str, list[str]]:
    if data.get("schema_version") != 1:
        raise ValueError("runtime manifest requires schema_version=1")
    commands = json_object(data.get("commands"), "commands")
    result: dict[str, list[str]] = {}
    for step in STEPS:
        result[step] = string_list(commands.get(step), f"commands.{step}", non_empty=True)
    return result


def check(
    root: Path,
    *,
    mode: str = "static",
    migrations: Path = Path("migrations/versions"),
    runtime_manifest: Path = Path("tests/contracts/migration-lifecycle.json"),
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> CheckResult:
    result = CheckResult("validate_migration_lifecycle")
    migration_root = root / migrations
    if not require_dir(migration_root, result):
        return result
    files = sorted(path for path in migration_root.glob("*.py") if path.name != "__init__.py")
    if not files:
        result.observed = False
        result.add("migrations-missing", "no migration revisions found", migration_root)
        return result
    revisions: list[tuple[Path, str, tuple[str, ...]]] = []
    for path in files:
        parsed = _revision(path, result)
        if parsed is not None:
            revisions.append((path, *parsed))
    _validate_graph(revisions, result)
    result.details.update(mode=mode, revisions=len(files))
    if mode == "static":
        return result
    if mode != "runtime":
        result.add("migration-mode-invalid", f"unsupported mode {mode}")
        return result
    manifest_path = root / runtime_manifest
    if not require_file(manifest_path, result, "migration-runtime-manifest-missing"):
        return result
    try:
        commands = _runtime_contract(load_json(manifest_path))
    except ValueError as exc:
        result.add("migration-runtime-manifest-invalid", str(exc), manifest_path)
        return result
    for step in STEPS:
        completed = run_command(commands[step], cwd=root, runner=runner, timeout=300)
        if completed.returncode != 0:
            add_command_failure(result, commands[step], completed, code=f"migration-{step}-failed")
            break
    result.details["runtime_steps_observed"] = len(STEPS) if result.ok else 0
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate migration source and lifecycle")
    add_common_arguments(parser)
    parser.add_argument("--mode", choices=("static", "runtime"), default="static")
    parser.add_argument("--migrations", type=Path, default=Path("migrations/versions"))
    parser.add_argument(
        "--runtime-manifest", type=Path, default=Path("tests/contracts/migration-lifecycle.json")
    )
    args = parser.parse_args(argv)
    return render_result(
        check(
            args.root.resolve(),
            mode=args.mode,
            migrations=args.migrations,
            runtime_manifest=args.runtime_manifest,
        ),
        args.json,
    )


if __name__ == "__main__":
    main_guard(cli)
