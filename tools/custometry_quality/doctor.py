from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Callable, Sequence, cast

from .core import (
    CheckResult,
    add_common_arguments,
    add_command_failure,
    canonical_json,
    load_json,
    main_guard,
    render_result,
    run_command,
    string_list,
)


Which = Callable[[str], str | None]
PORT_RANGE = re.compile(r"^(\d{1,5})-(\d{1,5})$")
PROJECT_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]{2,62}$")


def default_project_name(root: Path) -> str:
    digest = hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:10]
    return f"custometry-{digest}"


def parse_port_range(value: str) -> tuple[int, int]:
    match = PORT_RANGE.fullmatch(value)
    if not match:
        raise ValueError("port range must use START-END")
    start, end = int(match.group(1)), int(match.group(2))
    if not (1024 <= start <= end <= 65535):
        raise ValueError("port range must be within 1024..65535")
    return start, end


def select_free_loopback_port(port_range: tuple[int, int]) -> int:
    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise ValueError(f"no free loopback port in {port_range[0]}-{port_range[1]}")


def _owned_size(root: Path, manifest: Path) -> int:
    data = load_json(manifest)
    if data.get("schema_version") != 1:
        raise ValueError("ownership manifest requires schema_version=1")
    paths = string_list(data.get("owned_paths"), "owned_paths", non_empty=True)
    total = 0
    for raw in paths:
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"unsafe owned path: {raw}")
        target = root / relative
        resolved = target.resolve(strict=False)
        if resolved == root.resolve() or root.resolve() not in resolved.parents:
            raise ValueError(f"owned path escapes repository: {raw}")
        if target.is_file() or target.is_symlink():
            total += target.lstat().st_size
        elif target.is_dir():
            total += sum(
                item.lstat().st_size
                for item in target.rglob("*")
                if item.is_file() or item.is_symlink()
            )
    return total


def write_runtime_env(
    root: Path,
    path: Path,
    *,
    port: int,
    project_name: str,
    force: bool,
) -> tuple[Path, Path]:
    if not PROJECT_NAME.fullmatch(project_name):
        raise ValueError("project name must be a safe lowercase Compose project name")
    target = path if path.is_absolute() else root / path
    resolved = target.resolve(strict=False)
    if root.resolve() not in resolved.parents:
        raise ValueError("runtime env must be inside the repository")
    ownership = target.with_suffix(target.suffix + ".ownership.json")
    if not force and (target.exists() or ownership.exists()):
        raise ValueError("runtime env or ownership manifest exists; use --force to replace")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        f"COMPOSE_PROJECT_NAME={project_name}\n"
        "CUSTOMETRY_BIND_HOST=127.0.0.1\n"
        f"CUSTOMETRY_HTTP_PORT={port}\n"
    ).encode("utf-8")
    temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_bytes(payload)
    temporary.chmod(0o600)
    os.replace(temporary, target)
    relative_target = target.relative_to(root).as_posix()
    relative_ownership = ownership.relative_to(root).as_posix()
    ownership_payload = canonical_json(
        {
            "schema_version": 1,
            "owned_paths": [relative_target, relative_ownership],
            "purpose": "doctor-selected local runtime environment",
        }
    )
    ownership_tmp = ownership.with_name(f".{ownership.name}.{uuid.uuid4().hex}.tmp")
    ownership_tmp.write_bytes(ownership_payload)
    ownership_tmp.chmod(0o600)
    os.replace(ownership_tmp, ownership)
    return target, ownership


def _probe(
    command: list[str],
    *,
    root: Path,
    runner: Callable[..., subprocess.CompletedProcess[str]],
) -> subprocess.CompletedProcess[str]:
    return run_command(command, cwd=root, runner=runner, timeout=30)


def _entrypoints(
    root: Path,
    result: CheckResult,
    *,
    which: Which,
    runner: Callable[..., subprocess.CompletedProcess[str]],
) -> dict[str, dict[str, str | bool]]:
    probes: dict[str, list[str]] = {
        "git": ["git", "--version"],
        "uv": ["uv", "--version"],
        "node": ["node", "--version"],
        "docker-compose": ["docker", "compose", "version"],
    }
    details: dict[str, dict[str, str | bool]] = {}
    for name, command in probes.items():
        executable = command[0]
        if not which(executable):
            result.add("tool-missing", f"required executable is unavailable: {executable}")
            details[name] = {"ok": False, "command": " ".join(command)}
            continue
        completed = _probe(command, root=root, runner=runner)
        ok = completed.returncode == 0
        details[name] = {
            "ok": ok,
            "command": " ".join(command),
            "version": (completed.stdout or completed.stderr).strip()[:200],
        }
        if not ok:
            add_command_failure(result, command, completed, code="tool-entrypoint-broken")

    pnpm_candidates: list[list[str]] = []
    if which("pnpm"):
        pnpm_candidates.append(["pnpm", "--version"])
    if which("corepack"):
        pnpm_candidates.append(["corepack", "pnpm", "--version"])
    selected: subprocess.CompletedProcess[str] | None = None
    selected_command: list[str] | None = None
    attempts: list[str] = []
    for command in pnpm_candidates:
        completed = _probe(command, root=root, runner=runner)
        attempts.append(f"{' '.join(command)}={completed.returncode}")
        if completed.returncode == 0:
            selected, selected_command = completed, command
            break
    if selected is None or selected_command is None:
        result.add("tool-entrypoint-broken", "pnpm and corepack pnpm entrypoints are unavailable/broken")
        details["pnpm"] = {"ok": False, "attempts": ", ".join(attempts) or "none"}
    else:
        details["pnpm"] = {
            "ok": True,
            "command": " ".join(selected_command),
            "version": selected.stdout.strip()[:200],
            "attempts": ", ".join(attempts),
        }
    return details


def _reported_version(details: dict[str, dict[str, str | bool]], tool: str) -> str | None:
    raw = details.get(tool, {}).get("version")
    if not isinstance(raw, str):
        return None
    match = re.search(r"\d+(?:\.\d+){1,3}", raw)
    return match.group(0) if match else None


def _validate_version_pins(
    root: Path,
    result: CheckResult,
    details: dict[str, dict[str, str | bool]],
) -> None:
    pin_files = {
        "node": root / ".node-version",
        "uv": root / ".uv-version",
        "pnpm": root / "package.json",
    }
    expected: dict[str, str] = {}
    for tool in ("node", "uv"):
        path = pin_files[tool]
        if not path.is_file():
            result.observed = False
            result.add("tool-version-pin-missing", f"{tool} version pin is required", path)
            continue
        value = path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"\d+(?:\.\d+){1,3}", value):
            result.add("tool-version-pin-invalid", f"invalid {tool} version pin: {value!r}", path)
            continue
        expected[tool] = value
    package_path = pin_files["pnpm"]
    if not package_path.is_file():
        result.observed = False
        result.add("tool-version-pin-missing", "pnpm packageManager pin is required", package_path)
    else:
        try:
            package_manager = load_json(package_path).get("packageManager")
        except ValueError as exc:
            result.add("tool-version-pin-invalid", str(exc), package_path)
        else:
            match = re.fullmatch(r"pnpm@(\d+(?:\.\d+){1,3})", str(package_manager))
            if not match:
                result.add(
                    "tool-version-pin-invalid",
                    "packageManager must pin exact pnpm@X.Y.Z",
                    package_path,
                )
            else:
                expected["pnpm"] = match.group(1)
    for tool, pin in expected.items():
        actual = _reported_version(details, tool)
        if actual is None:
            continue
        if actual != pin:
            result.add(
                "tool-version-mismatch",
                f"{tool} reports {actual}; repository requires {pin}",
                pin_files[tool],
            )
    result.details["version_pins"] = expected


def _runtime_engines(
    root: Path,
    result: CheckResult,
    *,
    runner: Callable[..., subprocess.CompletedProcess[str]],
) -> tuple[list[dict[str, object]], dict[str, object] | None]:
    context_command = ["docker", "context", "ls", "--format", "{{json .}}"]
    contexts = _probe(context_command, root=root, runner=runner)
    if contexts.returncode != 0:
        result.observed = False
        add_command_failure(result, context_command, contexts, code="container-context-unobserved")
        return [], None
    responsive: list[dict[str, object]] = []
    identities: set[tuple[str, str]] = set()
    current_markers = 0
    current_context: str | None = None
    current_info: dict[str, object] | None = None
    for line in contexts.stdout.splitlines():
        try:
            item = cast(dict[str, object], json.loads(line))
        except json.JSONDecodeError:
            result.add("container-context-invalid", "docker context output is not JSON")
            continue
        is_current = item.get("Current") in (True, "true", "*")
        if is_current:
            current_markers += 1
        name = item.get("Name")
        endpoint = item.get("DockerEndpoint")
        if not isinstance(name, str) or not isinstance(endpoint, str):
            continue
        if not endpoint.startswith(("unix://", "npipe://")):
            if is_current:
                current_context = name
            continue
        command = ["docker", "--context", name, "info", "--format", "{{json .}}"]
        completed = _probe(command, root=root, runner=runner)
        if completed.returncode != 0:
            continue
        try:
            info = cast(dict[str, object], json.loads(completed.stdout))
        except json.JSONDecodeError:
            result.add("container-context-info-invalid", f"context {name} returned invalid JSON")
            continue
        if is_current:
            current_context = name
            current_info = info
        identity = (str(info.get("Name", name)), str(info.get("DockerRootDir", endpoint)))
        if identity in identities:
            continue
        identities.add(identity)
        responsive.append({"context": name, "endpoint": endpoint, "engine": identity[0]})
    if current_markers != 1:
        result.add("container-current-context-invalid", f"expected one current context, got {current_markers}")
    elif current_info is None:
        result.add(
            "container-current-engine-unavailable",
            f"current Docker context {current_context or '<unknown>'} is not a responsive local engine",
        )
    return responsive, current_info


def check(
    root: Path,
    *,
    mode: str = "static",
    min_free_gib: float = 25.0,
    max_container_engines: int = 1,
    runtime_memory_budget_gib: float = 6.0,
    ownership_manifest: Path | None = None,
    max_owned_disk_gib: float = 25.0,
    write_env: Path | None = None,
    force: bool = False,
    http_port_range: str = "48100-48199",
    project_name: str | None = None,
    which: Which = shutil.which,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> CheckResult:
    result = CheckResult("doctor")
    result.details.update(
        mode=mode,
        python=platform.python_version(),
        platform=platform.platform(),
        cpu_count=os.cpu_count(),
    )
    tools = _entrypoints(root, result, which=which, runner=runner)
    result.details["tools"] = tools
    _validate_version_pins(root, result, tools)
    resolved_project_name = project_name or default_project_name(root)
    result.details["project_name"] = resolved_project_name
    if sys.version_info[:2] != (3, 12):
        result.add("python-version-invalid", "Custometry tooling must run on Python 3.12")
    disk = shutil.disk_usage(root)
    free_gib = disk.free / (1024**3)
    result.details["free_disk_gib"] = round(free_gib, 2)
    if free_gib < min_free_gib:
        result.add("disk-capacity-low", f"free disk {free_gib:.2f} GiB is below {min_free_gib:.2f} GiB")
    if ownership_manifest is not None:
        manifest_path = ownership_manifest if ownership_manifest.is_absolute() else root / ownership_manifest
        if not manifest_path.is_file():
            result.observed = False
            result.add("ownership-manifest-missing", "owned disk cannot be measured", manifest_path)
        else:
            try:
                owned_bytes = _owned_size(root, manifest_path)
            except ValueError as exc:
                result.add("ownership-manifest-invalid", str(exc), manifest_path)
            else:
                owned_gib = owned_bytes / (1024**3)
                result.details["owned_disk_gib"] = round(owned_gib, 3)
                if owned_gib > max_owned_disk_gib:
                    result.add(
                        "owned-disk-budget-exceeded",
                        f"owned disk {owned_gib:.3f} GiB exceeds {max_owned_disk_gib:.3f} GiB",
                        manifest_path,
                    )
    if mode == "static":
        if write_env is not None:
            result.add("runtime-env-mode-invalid", "--write-runtime-env requires --mode runtime")
        return result
    if mode != "runtime":
        result.add("doctor-mode-invalid", f"unsupported mode: {mode}")
        return result
    if not which("docker"):
        result.observed = False
        result.add("container-engine-unobserved", "Docker runtime cannot be inspected")
        return result
    responsive, current_info = _runtime_engines(root, result, runner=runner)
    if len(responsive) != max_container_engines:
        result.add(
            "container-engine-count-invalid",
            f"expected {max_container_engines} responsive local engine, observed {len(responsive)}",
        )
    memory_bytes = current_info.get("MemTotal") if current_info else None
    if isinstance(memory_bytes, int):
        memory_gib = memory_bytes / (1024**3)
        result.details["runtime_memory_capacity_gib"] = round(memory_gib, 2)
        if memory_gib < runtime_memory_budget_gib:
            result.add(
                "runtime-memory-capacity-low",
                f"engine capacity {memory_gib:.2f} GiB is below {runtime_memory_budget_gib:.2f} GiB",
            )
    else:
        result.add("runtime-memory-unobserved", "Docker MemTotal is unavailable")
    result.details["responsive_local_engines"] = responsive
    if write_env is not None and result.ok:
        try:
            port = select_free_loopback_port(parse_port_range(http_port_range))
            env_path, owner_path = write_runtime_env(
                root,
                write_env,
                port=port,
                project_name=resolved_project_name,
                force=force,
            )
        except ValueError as exc:
            result.add("runtime-env-write-failed", str(exc), write_env)
        else:
            result.details["runtime_env"] = {
                "path": str(env_path),
                "ownership_manifest": str(owner_path),
                "http_port": port,
                "project_name": resolved_project_name,
            }
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate local development prerequisites")
    add_common_arguments(parser)
    parser.add_argument("--mode", choices=("static", "runtime"), default="static")
    parser.add_argument("--min-free-gib", type=float, default=25.0)
    parser.add_argument("--max-container-engines", type=int, default=1)
    parser.add_argument("--runtime-memory-budget-gib", type=float, default=6.0)
    parser.add_argument("--ownership-manifest", type=Path)
    parser.add_argument("--max-owned-disk-gib", type=float, default=25.0)
    parser.add_argument("--write-runtime-env", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--http-port-range", default="48100-48199")
    parser.add_argument("--project-name")
    args = parser.parse_args(argv)
    return render_result(
        check(
            args.root.resolve(),
            mode=args.mode,
            min_free_gib=args.min_free_gib,
            max_container_engines=args.max_container_engines,
            runtime_memory_budget_gib=args.runtime_memory_budget_gib,
            ownership_manifest=args.ownership_manifest,
            max_owned_disk_gib=args.max_owned_disk_gib,
            write_env=args.write_runtime_env,
            force=args.force,
            http_port_range=args.http_port_range,
            project_name=args.project_name,
        ),
        args.json,
    )


if __name__ == "__main__":
    main_guard(cli)
