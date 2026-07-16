from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path
from typing import Iterable, Sequence

from .core import CheckResult, add_common_arguments, main_guard, render_result, require_dir


SHARED = {"contracts", "localization", "plugin_sdk"}
BANNED_DOMAIN_IMPORTS = {"fastapi", "celery", "sqlalchemy", "psycopg", "redis", "valkey"}
BANNED_TS_CORE_IMPORTS = {
    "react",
    "next",
    "express",
    "fastify",
    "@nestjs",
    "typeorm",
    "prisma",
}
TS_IMPORT = re.compile(
    r"(?:\bfrom\s+|\bimport\s*\(|\brequire\s*\()\s*['\"]([^'\"]+)['\"]"
    r"|\bimport\s*['\"]([^'\"]+)['\"]"
)


def _imports(path: Path) -> Iterable[tuple[str, int]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name, node.lineno
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module, node.lineno


def _ts_imports(path: Path) -> Iterable[tuple[str, int]]:
    text = path.read_text(encoding="utf-8")
    for match in TS_IMPORT.finditer(text):
        module = match.group(1) or match.group(2)
        yield module, text.count("\n", 0, match.start()) + 1


def _ts_target(module: str, path: Path, package_root: Path) -> str | None:
    if module.startswith("@custometry/"):
        return module.removeprefix("@custometry/").replace("-", "_")
    if not module.startswith("."):
        return None
    resolved = (path.parent / module).resolve(strict=False)
    try:
        relative = resolved.relative_to(package_root.resolve())
    except ValueError:
        return None
    return relative.parts[0] if relative.parts else None


def check(root: Path, packages: Path = Path("packages")) -> CheckResult:
    result = CheckResult("check_ddd_boundaries")
    package_root = root / packages
    if not require_dir(package_root, result):
        return result
    contexts = {item.name for item in package_root.iterdir() if item.is_dir()}
    python_files = sorted(package_root.rglob("*.py"))
    for path in python_files:
        relative = path.relative_to(package_root)
        owner = relative.parts[0]
        domain_layer = any(part in {"domain", "application"} for part in relative.parts[1:-1])
        try:
            imports = list(_imports(path))
        except SyntaxError as exc:
            result.add("python-syntax-invalid", str(exc), path, exc.lineno)
            continue
        for module, line in imports:
            parts = module.split(".")
            if parts[0] == "packages" and len(parts) > 1:
                target = parts[1]
                if target in contexts and target not in {owner, *SHARED}:
                    result.add(
                        "cross-context-import",
                        f"{owner} imports private context {target}; use an explicit port/contract",
                        path,
                        line,
                    )
            if domain_layer and parts[0] in BANNED_DOMAIN_IMPORTS:
                result.add(
                    "framework-import-in-core",
                    f"{parts[0]} is forbidden in domain/application code",
                    path,
                    line,
                )
    ts_files = sorted(
        path
        for suffix in ("*.ts", "*.tsx", "*.js", "*.jsx")
        for path in package_root.rglob(suffix)
        if not {"node_modules", "dist", "coverage"}.intersection(path.parts)
    )
    for path in ts_files:
        relative = path.relative_to(package_root)
        owner = relative.parts[0]
        core_layer = any(part in {"domain", "application"} for part in relative.parts[1:-1])
        for module, line in _ts_imports(path):
            target = _ts_target(module, path, package_root)
            if target in contexts and target not in {owner, *SHARED}:
                result.add(
                    "cross-context-import",
                    f"{owner} imports private context {target}; use an explicit port/contract",
                    path,
                    line,
                )
            top_level = module.split("/", 1)[0]
            scoped = "/".join(module.split("/", 2)[:2]) if module.startswith("@") else top_level
            if core_layer and (top_level in BANNED_TS_CORE_IMPORTS or scoped in BANNED_TS_CORE_IMPORTS):
                result.add(
                    "framework-import-in-core",
                    f"{scoped} is forbidden in domain/application code",
                    path,
                    line,
                )
    result.details.update(
        contexts=len(contexts), python_files=len(python_files), typescript_files=len(ts_files)
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enforce modular-monolith import boundaries")
    add_common_arguments(parser)
    parser.add_argument("--packages", type=Path, default=Path("packages"))
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.packages), args.json)


if __name__ == "__main__":
    main_guard(cli)
