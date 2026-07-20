from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence, cast
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, build_opener

from .core import (
    CheckResult,
    JsonObject,
    JsonValue,
    json_integer,
    json_list,
    json_object,
    json_string,
    load_json,
    load_yaml,
    main_guard,
    repo_root,
)


POLICY_PATH = Path("deploy/compose/development-runtime-policy.json")
OWNERSHIP_LABELS = {
    "com.custometry.owner": "W11-HYBRID-DEVELOPMENT-RUNTIME",
    "com.custometry.runtime": "hybrid",
}
STATUS_CODES = {"healthy": 0, "degraded": 1, "unavailable": 2}
REDACTION_PATTERNS = (
    re.compile(r"(?i)\b(password|secret|token|dsn)(\s*[:=]\s*)(\S+)"),
    re.compile(r"(?i)([a-z][a-z0-9+.-]*://[^\s:/@]+:)([^\s@]+)(@)"),
)


class RuntimeErrorSafe(RuntimeError):
    """An operator-safe failure that never includes secret material."""


@dataclass(frozen=True, slots=True)
class DatabaseService:
    name: str
    host: str
    port: int
    database: str
    user: str
    volume: str
    data_role: str


@dataclass(frozen=True, slots=True)
class HostProcess:
    name: str
    host: str
    port: int
    url: str
    readiness_path: str
    command: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RuntimePolicy:
    runtime_id: str
    compose_files: tuple[Path, ...]
    project_prefix: str
    state_root: Path
    databases: dict[str, DatabaseService]
    host_processes: dict[str, HostProcess]
    secret_files: tuple[str, ...]
    reset_confirmation: str
    reset_volume: str
    release_entrypoints: tuple[Path, ...]
    log_tail_lines: int
    log_max_bytes: int


@dataclass(frozen=True, slots=True)
class RuntimePaths:
    root: Path
    runtime_dir: Path
    secrets_dir: Path
    logs_dir: Path
    state_file: Path
    project_name: str


@dataclass(frozen=True, slots=True)
class RuntimeStatus:
    overall: str
    lines: tuple[str, ...]


def _relative_path(value: JsonValue, label: str) -> Path:
    raw = json_string(value, label)
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != raw:
        raise ValueError(f"{label} must be a normalized repository-relative path")
    return path


def _loopback_host(value: JsonValue, label: str) -> str:
    host = json_string(value, label)
    if host != "127.0.0.1":
        raise ValueError(f"{label} must be exactly 127.0.0.1")
    return host


def _port(value: JsonValue, label: str) -> int:
    port = json_integer(value, label)
    if not 1024 <= port <= 65535:
        raise ValueError(f"{label} must be an unprivileged TCP port")
    return port


def _string_tuple(value: JsonValue, label: str) -> tuple[str, ...]:
    items = json_list(value, label)
    if not items or not all(isinstance(item, str) and item for item in items):
        raise ValueError(f"{label} must be a non-empty list of non-empty strings")
    return tuple(cast(list[str], items))


def parse_policy(document: JsonObject) -> RuntimePolicy:
    if document.get("schema_version") != 1:
        raise ValueError("development runtime policy requires schema_version=1")
    runtime_id = json_string(document.get("runtime_id"), "runtime_id")
    if runtime_id != "custometry-hybrid":
        raise ValueError("runtime_id must be custometry-hybrid")
    compose_files = tuple(
        _relative_path(item, f"compose_files[{index}]")
        for index, item in enumerate(json_list(document.get("compose_files"), "compose_files"))
    )
    if compose_files != (Path("compose.yaml"), Path("compose.dev.yaml")):
        raise ValueError("compose_files must be exactly compose.yaml and compose.dev.yaml")
    project_prefix = json_string(document.get("compose_project_prefix"), "compose_project_prefix")
    if re.fullmatch(r"custometry-hybrid-[a-z0-9-]*", project_prefix) is None:
        raise ValueError("compose_project_prefix must be repository-specific hybrid identity")
    state_root = _relative_path(document.get("state_root"), "state_root")
    if state_root.parts[:2] != (".runtime", "development"):
        raise ValueError("state_root must be under .runtime/development")

    database_raw = json_object(document.get("database_services"), "database_services")
    if set(database_raw) != {"control-db", "demo-source-db"}:
        raise ValueError("database_services must contain exactly control-db and demo-source-db")
    databases: dict[str, DatabaseService] = {}
    for name, raw in database_raw.items():
        item = json_object(raw, f"database_services.{name}")
        databases[name] = DatabaseService(
            name=name,
            host=_loopback_host(item.get("host"), f"database_services.{name}.host"),
            port=_port(item.get("port"), f"database_services.{name}.port"),
            database=json_string(item.get("database"), f"database_services.{name}.database"),
            user=json_string(item.get("user"), f"database_services.{name}.user"),
            volume=json_string(item.get("volume"), f"database_services.{name}.volume"),
            data_role=json_string(item.get("data_role"), f"database_services.{name}.data_role"),
        )
    if databases["control-db"].data_role != "control":
        raise ValueError("control-db must have data_role=control")
    if databases["demo-source-db"].data_role != "demo":
        raise ValueError("demo-source-db must have data_role=demo")
    if databases["control-db"].volume == databases["demo-source-db"].volume:
        raise ValueError("control and demo databases must use distinct volumes")

    process_raw = json_object(document.get("host_processes"), "host_processes")
    if set(process_raw) != {"api", "web"}:
        raise ValueError("host_processes must contain exactly api and web")
    host_processes: dict[str, HostProcess] = {}
    for name, raw in process_raw.items():
        item = json_object(raw, f"host_processes.{name}")
        host = _loopback_host(item.get("host"), f"host_processes.{name}.host")
        port = _port(item.get("port"), f"host_processes.{name}.port")
        url = json_string(item.get("url"), f"host_processes.{name}.url")
        if url != f"http://{host}:{port}":
            raise ValueError(f"host_processes.{name}.url must match its loopback host and port")
        readiness_path = json_string(
            item.get("readiness_path"), f"host_processes.{name}.readiness_path"
        )
        if not readiness_path.startswith("/") or readiness_path.startswith("//"):
            raise ValueError(f"host_processes.{name}.readiness_path must be an absolute path")
        host_processes[name] = HostProcess(
            name=name,
            host=host,
            port=port,
            url=url,
            readiness_path=readiness_path,
            command=_string_tuple(item.get("command"), f"host_processes.{name}.command"),
        )

    all_ports = [item.port for item in databases.values()] + [
        item.port for item in host_processes.values()
    ]
    if len(all_ports) != len(set(all_ports)):
        raise ValueError("database and host-process ports must be distinct")
    secret_files = _string_tuple(document.get("secret_files"), "secret_files")
    if set(secret_files) != {
        "control_db_password",
        "demo_source_admin_password",
        "demo_source_reader_password",
    }:
        raise ValueError("secret_files must be exactly the three Foundation Compose secrets")
    reset_confirmation = json_string(document.get("reset_confirmation"), "reset_confirmation")
    if reset_confirmation != "RESET-DEMO":
        raise ValueError("reset_confirmation must be RESET-DEMO")
    reset_volume = json_string(document.get("reset_volume"), "reset_volume")
    if reset_volume != databases["demo-source-db"].volume:
        raise ValueError("reset_volume must select only the demo-source volume")
    if reset_volume == databases["control-db"].volume:
        raise ValueError("reset_volume must never select the control volume")
    release_entrypoints = tuple(
        _relative_path(item, f"release_entrypoints[{index}]")
        for index, item in enumerate(
            json_list(document.get("release_entrypoints"), "release_entrypoints")
        )
    )
    logs = json_object(document.get("logs"), "logs")
    log_tail_lines = json_integer(logs.get("tail_lines"), "logs.tail_lines")
    log_max_bytes = json_integer(logs.get("max_bytes"), "logs.max_bytes")
    if not 1 <= log_tail_lines <= 500 or not 1024 <= log_max_bytes <= 1024 * 1024:
        raise ValueError("log bounds exceed the accepted development policy")
    return RuntimePolicy(
        runtime_id=runtime_id,
        compose_files=compose_files,
        project_prefix=project_prefix,
        state_root=state_root,
        databases=databases,
        host_processes=host_processes,
        secret_files=secret_files,
        reset_confirmation=reset_confirmation,
        reset_volume=reset_volume,
        release_entrypoints=release_entrypoints,
        log_tail_lines=log_tail_lines,
        log_max_bytes=log_max_bytes,
    )


def load_policy(root: Path) -> RuntimePolicy:
    return parse_policy(load_json(root / POLICY_PATH))


def runtime_paths(root: Path, policy: RuntimePolicy) -> RuntimePaths:
    digest = hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:10]
    project_name = f"{policy.project_prefix}{digest}"
    runtime_dir = root / policy.state_root / digest
    return RuntimePaths(
        root=root,
        runtime_dir=runtime_dir,
        secrets_dir=runtime_dir / "secrets",
        logs_dir=runtime_dir / "logs",
        state_file=runtime_dir / "state.json",
        project_name=project_name,
    )


def _service_mapping(document: JsonObject, label: str) -> JsonObject:
    return json_object(document.get("services"), f"{label}.services")


def static_check(root: Path) -> CheckResult:
    result = CheckResult("development_runtime")
    policy_path = root / POLICY_PATH
    compose_path = root / "compose.dev.yaml"
    script_path = root / "scripts/dev"
    for path in (policy_path, compose_path, script_path):
        if not path.is_file():
            result.observed = False
            result.add("development-runtime-file-missing", "required file does not exist", path)
    if not result.observed:
        return result
    try:
        policy = load_policy(root)
        override = load_yaml(compose_path)
        services = _service_mapping(override, "compose.dev.yaml")
        volumes = json_object(override.get("volumes"), "compose.dev.yaml.volumes")
        networks = json_object(override.get("networks"), "compose.dev.yaml.networks")
    except ValueError as exc:
        result.add("development-runtime-contract-invalid", str(exc))
        return result
    if set(services) != set(policy.databases):
        result.add(
            "development-compose-service-scope",
            "compose.dev.yaml may override only control-db and demo-source-db",
            compose_path,
        )
    for name, database in policy.databases.items():
        try:
            service = json_object(services.get(name), f"services.{name}")
            ports = json_list(service.get("ports"), f"services.{name}.ports")
        except ValueError as exc:
            result.add("development-port-invalid", str(exc), compose_path)
            continue
        if len(ports) != 1:
            result.add(
                "development-port-count",
                f"{name} must publish exactly one development port",
                compose_path,
            )
            continue
        try:
            published = json_object(ports[0], f"services.{name}.ports[0]")
        except ValueError as exc:
            result.add("development-port-invalid", str(exc), compose_path)
            continue
        if published.get("host_ip") != "127.0.0.1" or published.get("target") != 5432:
            result.add(
                "development-port-not-loopback",
                f"{name} must publish PostgreSQL only on 127.0.0.1",
                compose_path,
            )
        if database.volume not in volumes:
            result.add(
                "development-volume-missing",
                f"{name} volume {database.volume} is not declared",
                compose_path,
            )
    if set(networks) != {"control", "demo_source"}:
        result.add(
            "development-network-scope",
            "compose.dev.yaml must override exactly the control and demo_source networks",
            compose_path,
        )
    for name in ("control", "demo_source"):
        try:
            network = json_object(networks.get(name), f"networks.{name}")
        except ValueError as exc:
            result.add("development-network-invalid", str(exc), compose_path)
            continue
        if network.get("internal") is not False:
            result.add(
                "development-network-host-binding-incompatible",
                f"{name} must set internal: false for Docker Desktop loopback publication",
                compose_path,
            )
    extension = override.get("x-custometry-development-runtime")
    try:
        marker = json_object(extension, "x-custometry-development-runtime")
    except ValueError as exc:
        result.add("development-release-marker-missing", str(exc), compose_path)
    else:
        if marker.get("release_eligible") is not False or marker.get("mode") != "hybrid":
            result.add(
                "development-release-marker-invalid",
                "development override must be explicitly hybrid and release-ineligible",
                compose_path,
            )
    for entrypoint in policy.release_entrypoints:
        path = root / entrypoint
        if not path.is_file():
            result.observed = False
            result.add("release-entrypoint-missing", "release entrypoint is absent", path)
            continue
        if "compose.dev.yaml" in path.read_text(encoding="utf-8"):
            result.add(
                "development-override-in-release-path",
                "release entrypoint must not reference compose.dev.yaml",
                path,
            )
    script_text = script_path.read_text(encoding="utf-8")
    if "development_runtime" not in script_text or "--locked" not in script_text:
        result.add(
            "development-cli-wrapper-invalid",
            "scripts/dev must use the locked Python development runtime",
            script_path,
        )
    result.details.update(
        {
            "project_prefix": policy.project_prefix,
            "database_services": sorted(policy.databases),
            "host_processes": sorted(policy.host_processes),
            "release_entrypoints_checked": len(policy.release_entrypoints),
        }
    )
    return result


def redact(text: str, *, max_bytes: int) -> str:
    value = text
    for pattern in REDACTION_PATTERNS:
        if pattern.groups == 3 and pattern.pattern.startswith("(?i)\\b"):
            value = pattern.sub(r"\1\2[REDACTED]", value)
        else:
            value = pattern.sub(r"\1[REDACTED]\3", value)
    fields_redacted = value != text
    encoded = value.encode("utf-8", errors="replace")
    if len(encoded) > max_bytes:
        marker = "[output truncated to policy bound"
        if fields_redacted:
            marker += "; [REDACTED] fields removed"
        marker += "]\n"
        marker_bytes = marker.encode("utf-8")
        tail_size = max(0, max_bytes - len(marker_bytes))
        value = marker + encoded[-tail_size:].decode("utf-8", errors="ignore")
    return value


def _compose_environment(paths: RuntimePaths, policy: RuntimePolicy) -> dict[str, str]:
    control = policy.databases["control-db"]
    demo = policy.databases["demo-source-db"]
    return {
        "COMPOSE_PROJECT_NAME": paths.project_name,
        "CUSTOMETRY_HYBRID_PROJECT_NAME": paths.project_name,
        "CUSTOMETRY_CONTROL_DB_PORT": str(control.port),
        "CUSTOMETRY_DEMO_DB_PORT": str(demo.port),
        "CUSTOMETRY_SECRETS_DIR": str(paths.secrets_dir),
        "CUSTOMETRY_DATA_PROFILE": "demo",
        "CUSTOMETRY_ALLOW_BENCHMARK": "0",
    }


def compose_command(paths: RuntimePaths, policy: RuntimePolicy, *arguments: str) -> list[str]:
    command = ["docker", "compose"]
    for path in policy.compose_files:
        command.extend(("-f", str(paths.root / path)))
    command.extend(("--project-name", paths.project_name, *arguments))
    return command


def _run(
    command: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    timeout: int = 120,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        env=merged,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if check and completed.returncode != 0:
        output = redact(completed.stderr or completed.stdout, max_bytes=4000).strip()
        raise RuntimeErrorSafe(f"command failed ({command[0]}): {output}")
    return completed


def _ensure_engine(root: Path) -> str:
    context = _run(["docker", "context", "show"], cwd=root).stdout.strip()
    if not context:
        raise RuntimeErrorSafe("Docker context is unavailable")
    _run(["docker", "compose", "version"], cwd=root)
    _run(["docker", "info", "--format", "{{.ID}}"], cwd=root, timeout=30)
    return context


def _write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def _load_state(paths: RuntimePaths) -> dict[str, object]:
    if not paths.state_file.is_file():
        return {"schema_version": 1, "project_name": paths.project_name, "processes": {}}
    if paths.state_file.is_symlink():
        raise RuntimeErrorSafe("development runtime state must not be a symbolic link")
    try:
        value = cast(object, json.loads(paths.state_file.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeErrorSafe("development runtime state is unreadable; refusing ownership action") from exc
    if not isinstance(value, dict):
        raise RuntimeErrorSafe("development runtime state has a foreign project identity")
    state = cast(dict[str, object], value)
    if state.get("project_name") != paths.project_name:
        raise RuntimeErrorSafe("development runtime state has a foreign project identity")
    processes = state.get("processes")
    if not isinstance(processes, dict):
        raise RuntimeErrorSafe("development runtime process state is invalid")
    return state


def _process_fingerprint(pid: int) -> tuple[str, str] | None:
    completed = subprocess.run(
        ["ps", "-p", str(pid), "-o", "lstart=", "-o", "command="],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        return None
    line = completed.stdout.strip()
    match = re.match(r"^(.{24})\s+(.*)$", line)
    if match is None:
        return None
    return match.group(1).strip(), match.group(2).strip()


def owned_process_identity(record: object) -> tuple[int, int] | None:
    if not isinstance(record, dict):
        return None
    typed_record = cast(dict[str, object], record)
    pid, pgid = typed_record.get("pid"), typed_record.get("pgid")
    started = typed_record.get("started")
    command = typed_record.get("observed_command")
    if (
        not isinstance(pid, int)
        or not isinstance(pgid, int)
        or not isinstance(started, str)
        or not isinstance(command, str)
    ):
        return None
    current = _process_fingerprint(pid)
    if current != (started, command):
        return None
    try:
        current_pgid = os.getpgid(pid)
    except ProcessLookupError:
        return None
    return (pid, pgid) if current_pgid == pgid == pid else None


def _port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((host, port))
        except OSError:
            return False
    return True


def _tcp_ready(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _wait_database_ports(policy: RuntimePolicy, timeout: int = 30) -> None:
    deadline = time.monotonic() + timeout
    pending = set(policy.databases)
    while pending and time.monotonic() < deadline:
        pending = {
            name
            for name in pending
            if not _tcp_ready(policy.databases[name].host, policy.databases[name].port)
        }
        if pending:
            time.sleep(0.25)
    if pending:
        raise RuntimeErrorSafe(
            f"loopback database ports did not become ready: {', '.join(sorted(pending))}"
        )


def prepare_runtime(paths: RuntimePaths, policy: RuntimePolicy) -> None:
    directories = (
        paths.root / ".runtime",
        paths.root / policy.state_root,
        paths.runtime_dir,
        paths.logs_dir,
        paths.secrets_dir,
    )
    for directory in directories:
        if directory.is_symlink():
            raise RuntimeErrorSafe(f"runtime directory must not be a symbolic link: {directory}")
        if directory.exists() and not directory.is_dir():
            raise RuntimeErrorSafe(f"runtime path is not a directory: {directory}")
        directory.mkdir(exist_ok=True)
        try:
            directory.resolve().relative_to(paths.root.resolve())
        except ValueError as exc:
            raise RuntimeErrorSafe("runtime directory escapes repository ownership") from exc
    os.chmod(paths.runtime_dir, 0o700)
    os.chmod(paths.secrets_dir, 0o700)
    for name in policy.secret_files:
        path = paths.secrets_dir / name
        if path.is_symlink():
            raise RuntimeErrorSafe(f"runtime secret must not be a symbolic link: {name}")
        if not path.is_file() or path.stat().st_size == 0:
            path.write_text(secrets.token_hex(32) + "\n", encoding="ascii")
        os.chmod(path, 0o444)


def _host_environment(paths: RuntimePaths, policy: RuntimePolicy, name: str) -> dict[str, str]:
    environment = os.environ.copy()
    environment["CUSTOMETRY_DEV_RUNTIME_ID"] = paths.project_name
    if name == "api":
        control = policy.databases["control-db"]
        environment.update(
            {
                "CUSTOMETRY_ENVIRONMENT": "development",
                "CUSTOMETRY_DATABASE_HOST": control.host,
                "CUSTOMETRY_DATABASE_PORT": str(control.port),
                "CUSTOMETRY_DATABASE_NAME": control.database,
                "CUSTOMETRY_DATABASE_USER": control.user,
                "CUSTOMETRY_DATABASE_PASSWORD_FILE": str(
                    paths.secrets_dir / "control_db_password"
                ),
            }
        )
    return environment


def _start_host_process(
    paths: RuntimePaths,
    policy: RuntimePolicy,
    process: HostProcess,
    state: dict[str, object],
) -> tuple[int, bool]:
    raw_processes = state.setdefault("processes", {})
    if not isinstance(raw_processes, dict):
        raise RuntimeErrorSafe("development runtime process state is invalid")
    processes = cast(dict[str, object], raw_processes)
    owned = owned_process_identity(processes.get(process.name))
    if owned is not None:
        return owned[0], True
    processes.pop(process.name, None)
    if not _port_available(process.host, process.port):
        raise RuntimeErrorSafe(
            f"{process.name} port {process.host}:{process.port} is owned by another process"
        )
    log_path = paths.logs_dir / f"{process.name}.log"
    with log_path.open("ab") as stream:
        child = subprocess.Popen(
            list(process.command),
            cwd=paths.root,
            env=_host_environment(paths, policy, process.name),
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    fingerprint: tuple[str, str] | None = None
    for _ in range(20):
        fingerprint = _process_fingerprint(child.pid)
        if fingerprint is not None:
            break
        if child.poll() is not None:
            break
        time.sleep(0.05)
    if fingerprint is None:
        raise RuntimeErrorSafe(f"{process.name} exited before ownership could be recorded")
    processes[process.name] = {
        "pid": child.pid,
        "pgid": child.pid,
        "started": fingerprint[0],
        "observed_command": fingerprint[1],
        "log": str(log_path.relative_to(paths.root)),
    }
    _write_json_atomic(paths.state_file, state)
    return child.pid, False


def _http_ready(url: str, timeout: float = 1.0) -> bool:
    opener = build_opener(ProxyHandler({}))
    try:
        with opener.open(url, timeout=timeout) as response:
            return 200 <= response.status < 400
    except (HTTPError, URLError, TimeoutError, OSError):
        return False


def _wait_http(process: HostProcess, timeout: int = 60) -> None:
    deadline = time.monotonic() + timeout
    url = process.url + process.readiness_path
    while time.monotonic() < deadline:
        if _http_ready(url):
            return
        time.sleep(0.5)
    raise RuntimeErrorSafe(f"{process.name} readiness did not become healthy at {url}")


def _run_migrations(paths: RuntimePaths, policy: RuntimePolicy) -> None:
    control = policy.databases["control-db"]
    environment = _host_environment(paths, policy, "api")
    command = [
        "uv",
        "run",
        "--locked",
        "--package",
        "custometry-api",
        "alembic",
        "-c",
        "migrations/alembic.ini",
        "upgrade",
        "head",
    ]
    completed = _run(command, cwd=paths.root, env=environment, timeout=120)
    migration_log = redact(completed.stdout + completed.stderr, max_bytes=16384)
    (paths.logs_dir / "migration.log").write_text(migration_log, encoding="utf-8")
    if control.data_role != "control":
        raise RuntimeErrorSafe("migration target is not the control database")


def _synchronize_persistent_credentials(paths: RuntimePaths, policy: RuntimePolicy) -> None:
    commands = {
        "control-db": """
set -eu
secret="$(tr -d '\\r\\n' </run/secrets/control_db_password)"
case "$secret" in ''|*[!a-f0-9]*) exit 2 ;; esac
printf "ALTER ROLE custometry PASSWORD '%s';\\n" "$secret" \
  | psql -v ON_ERROR_STOP=1 -U custometry -d custometry >/dev/null
unset secret
""".strip(),
        "demo-source-db": """
set -eu
admin_secret="$(tr -d '\\r\\n' </run/secrets/demo_source_admin_password)"
reader_secret="$(tr -d '\\r\\n' </run/secrets/demo_source_reader_password)"
case "$admin_secret" in ''|*[!a-f0-9]*) exit 2 ;; esac
case "$reader_secret" in ''|*[!a-f0-9]*) exit 2 ;; esac
printf "ALTER ROLE demo_source_admin PASSWORD '%s';\\nALTER ROLE demo_reader PASSWORD '%s';\\n" \
  "$admin_secret" "$reader_secret" \
  | psql -v ON_ERROR_STOP=1 -U demo_source_admin -d northwind_retail >/dev/null
unset admin_secret reader_secret
""".strip(),
    }
    environment = _compose_environment(paths, policy)
    for service, script in commands.items():
        _run(
            compose_command(
                paths,
                policy,
                "--profile",
                "demo",
                "exec",
                "-T",
                service,
                "sh",
                "-ceu",
                script,
            ),
            cwd=paths.root,
            env=environment,
            timeout=30,
        )


def _decode_compose_ps(payload: str) -> list[JsonObject]:
    stripped = payload.strip()
    if not stripped:
        return []
    try:
        decoded = cast(object, json.loads(stripped))
    except json.JSONDecodeError:
        records: list[JsonObject] = []
        for line in stripped.splitlines():
            value = cast(object, json.loads(line))
            if not isinstance(value, dict):
                raise ValueError("Compose ps records must be objects")
            records.append(cast(JsonObject, value))
        return records
    if isinstance(decoded, dict):
        return [cast(JsonObject, decoded)]
    if isinstance(decoded, list):
        items = cast(list[object], decoded)
        if all(isinstance(item, dict) for item in items):
            return cast(list[JsonObject], items)
    raise ValueError("Compose ps output must be an object, array, or NDJSON objects")


def compose_health(paths: RuntimePaths, policy: RuntimePolicy) -> dict[str, str]:
    completed = _run(
        compose_command(paths, policy, "--profile", "demo", "ps", "--format", "json"),
        cwd=paths.root,
        env=_compose_environment(paths, policy),
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        return {name: "unavailable" for name in policy.databases}
    try:
        records = _decode_compose_ps(completed.stdout)
    except (json.JSONDecodeError, ValueError):
        return {name: "unavailable" for name in policy.databases}
    by_service = {str(item.get("Service")): item for item in records}
    health: dict[str, str] = {}
    for name in policy.databases:
        record = by_service.get(name)
        raw_state = str(record.get("State", "")) if record else ""
        raw_health = str(record.get("Health", "")) if record else ""
        database = policy.databases[name]
        if (
            raw_state == "running"
            and raw_health == "healthy"
            and _tcp_ready(database.host, database.port)
        ):
            health[name] = "healthy"
        elif record is not None:
            health[name] = "degraded"
        else:
            health[name] = "unavailable"
    return health


def status_runtime(paths: RuntimePaths, policy: RuntimePolicy) -> RuntimeStatus:
    lines = ["mode=hybrid", f"project={paths.project_name}"]
    try:
        context = _ensure_engine(paths.root)
    except RuntimeErrorSafe:
        lines.append("docker=unavailable")
        for name in policy.databases:
            lines.append(f"{name}=unavailable")
        for name in policy.host_processes:
            lines.append(f"{name}=unavailable ownership=not-observed")
        lines.append("overall=unavailable")
        return RuntimeStatus("unavailable", tuple(lines))
    lines.append(f"docker=healthy context={context}")
    database_health = compose_health(paths, policy)
    for name, database in policy.databases.items():
        lines.append(
            f"{name}={database_health[name]} endpoint={database.host}:{database.port} "
            f"data-role={database.data_role}"
        )
    try:
        state = _load_state(paths)
    except RuntimeErrorSafe:
        state = cast(dict[str, object], {"processes": {}})
    raw_processes = state.get("processes", {})
    processes = cast(dict[str, object], raw_processes) if isinstance(raw_processes, dict) else {}
    host_health: dict[str, str] = {}
    for name, process in policy.host_processes.items():
        owned = owned_process_identity(processes.get(name))
        ready = owned is not None and _http_ready(process.url + process.readiness_path)
        host_health[name] = "healthy" if ready else "degraded"
        ownership = "owned" if owned is not None else "not-owned"
        pid = f" pid={owned[0]}" if owned is not None else ""
        lines.append(
            f"{name}={host_health[name]} ownership={ownership}{pid} url={process.url}"
        )
    database_states = set(database_health.values())
    if "unavailable" in database_states:
        overall = "unavailable"
    elif database_states == {"healthy"} and set(host_health.values()) == {"healthy"}:
        overall = "healthy"
    else:
        overall = "degraded"
    lines.append(f"overall={overall}")
    return RuntimeStatus(overall, tuple(lines))


def up_runtime(paths: RuntimePaths, policy: RuntimePolicy) -> RuntimeStatus:
    validation = static_check(paths.root)
    if not validation.ok:
        messages = "; ".join(item.message for item in validation.findings)
        raise RuntimeErrorSafe(f"development runtime contract is invalid: {messages}")
    context = _ensure_engine(paths.root)
    prepare_runtime(paths, policy)
    environment = _compose_environment(paths, policy)
    _run(
        compose_command(
            paths,
            policy,
            "--profile",
            "demo",
            "up",
            "-d",
            "--wait",
            "control-db",
            "demo-source-db",
        ),
        cwd=paths.root,
        env=environment,
        timeout=180,
    )
    _wait_database_ports(policy)
    _synchronize_persistent_credentials(paths, policy)
    _run_migrations(paths, policy)
    state = _load_state(paths)
    state.update(
        {
            "schema_version": 1,
            "mode": "hybrid",
            "project_name": paths.project_name,
            "docker_context": context,
        }
    )
    for name in ("api", "web"):
        process = policy.host_processes[name]
        pid, reused = _start_host_process(paths, policy, process, state)
        print(f"{name}-process={'reused' if reused else 'started'} pid={pid}")
        _wait_http(process)
    status = status_runtime(paths, policy)
    if status.overall != "healthy":
        raise RuntimeErrorSafe(f"Hybrid runtime started with overall={status.overall}")
    return status


def _stop_owned_process(record: object, name: str) -> None:
    owned = owned_process_identity(record)
    if owned is None:
        return
    pid, pgid = owned
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if _process_fingerprint(pid) is None:
            return
        time.sleep(0.1)
    if owned_process_identity(record) is not None:
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            return
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        if _process_fingerprint(pid) is None:
            return
        time.sleep(0.1)
    raise RuntimeErrorSafe(f"owned {name} process group did not stop")


def down_runtime(paths: RuntimePaths, policy: RuntimePolicy) -> None:
    state = _load_state(paths)
    raw_processes = state.get("processes", {})
    processes = cast(dict[str, object], raw_processes) if isinstance(raw_processes, dict) else {}
    for name in ("web", "api"):
        _stop_owned_process(processes.get(name), name)
    try:
        _ensure_engine(paths.root)
    except RuntimeErrorSafe:
        if processes or paths.runtime_dir.exists():
            raise
        return
    else:
        _run(
            compose_command(
                paths,
                policy,
                "--profile",
                "demo",
                "down",
                "--remove-orphans",
            ),
            cwd=paths.root,
            env=_compose_environment(paths, policy),
            timeout=120,
        )
    if paths.runtime_dir.is_symlink():
        raise RuntimeErrorSafe("runtime cleanup root must not be a symbolic link")
    if paths.runtime_dir.exists():
        try:
            paths.runtime_dir.resolve().relative_to(paths.root.resolve())
        except ValueError as exc:
            raise RuntimeErrorSafe("runtime cleanup root escapes repository ownership") from exc
        shutil.rmtree(paths.runtime_dir)


def expected_volume_name(paths: RuntimePaths, data_role: str) -> str:
    if data_role == "control":
        return f"{paths.project_name}-control-data"
    if data_role == "demo":
        return f"{paths.project_name}-demo-data"
    raise ValueError(f"unknown data role {data_role}")


def validate_demo_volume_labels(
    paths: RuntimePaths,
    policy: RuntimePolicy,
    volume_name: str,
    labels: Mapping[str, str],
) -> None:
    expected = expected_volume_name(paths, "demo")
    control = expected_volume_name(paths, "control")
    if volume_name != expected or volume_name == control:
        raise RuntimeErrorSafe("reset target is not the exact Hybrid demo volume")
    expected_labels = {
        **OWNERSHIP_LABELS,
        "com.custometry.data-role": "demo",
        "com.docker.compose.project": paths.project_name,
        "com.docker.compose.volume": policy.reset_volume,
    }
    if any(labels.get(key) != value for key, value in expected_labels.items()):
        raise RuntimeErrorSafe("demo volume lacks exact repository ownership labels")


def reset_demo(paths: RuntimePaths, policy: RuntimePolicy, confirmation: str | None) -> None:
    if confirmation != policy.reset_confirmation:
        raise RuntimeErrorSafe(
            f"reset-demo requires --confirm {policy.reset_confirmation}; no data was changed"
        )
    _ensure_engine(paths.root)
    if not paths.secrets_dir.is_dir():
        raise RuntimeErrorSafe("Hybrid runtime is not active; no reset was performed")
    volume_name = expected_volume_name(paths, "demo")
    inspected = _run(
        ["docker", "volume", "inspect", volume_name],
        cwd=paths.root,
        check=False,
        timeout=30,
    )
    if inspected.returncode != 0:
        raise RuntimeErrorSafe("the exact Hybrid demo volume does not exist")
    try:
        payload = cast(object, json.loads(inspected.stdout))
        if not isinstance(payload, list) or not payload:
            raise TypeError
        records = cast(list[object], payload)
        record = records[0]
        if not isinstance(record, dict):
            raise TypeError
        labels = cast(dict[str, object], record).get("Labels")
    except (json.JSONDecodeError, IndexError, KeyError, TypeError) as exc:
        raise RuntimeErrorSafe("demo volume metadata is invalid") from exc
    if not isinstance(labels, dict):
        raise RuntimeErrorSafe("demo volume labels are invalid")
    raw_labels = cast(dict[object, object], labels)
    if not all(
        isinstance(key, str) and isinstance(value, str) for key, value in raw_labels.items()
    ):
        raise RuntimeErrorSafe("demo volume labels are invalid")
    validate_demo_volume_labels(
        paths,
        policy,
        volume_name,
        cast(dict[str, str], raw_labels),
    )
    environment = _compose_environment(paths, policy)
    _run(
        compose_command(
            paths,
            policy,
            "--profile",
            "demo",
            "rm",
            "--stop",
            "--force",
            "demo-source-db",
        ),
        cwd=paths.root,
        env=environment,
    )
    _run(["docker", "volume", "rm", volume_name], cwd=paths.root, timeout=30)
    _run(
        compose_command(
            paths,
            policy,
            "--profile",
            "demo",
            "up",
            "-d",
            "--wait",
            "demo-source-db",
        ),
        cwd=paths.root,
        env=environment,
        timeout=180,
    )
    print(f"demo-reset=completed volume={volume_name}")


def logs_runtime(paths: RuntimePaths, policy: RuntimePolicy, service: str | None) -> None:
    selected = service or "all"
    allowed = {*policy.host_processes, *policy.databases, "migration", "all"}
    if selected not in allowed:
        raise RuntimeErrorSafe(f"unknown log service {selected}; allowed: {', '.join(sorted(allowed))}")
    outputs: list[str] = []
    if selected in {"all", "api", "web", "migration"}:
        names = ("api", "web", "migration") if selected == "all" else (selected,)
        for name in names:
            path = paths.logs_dir / f"{name}.log"
            if not path.is_file():
                continue
            with path.open("rb") as stream:
                size = path.stat().st_size
                stream.seek(max(0, size - policy.log_max_bytes))
                text = stream.read(policy.log_max_bytes).decode("utf-8", errors="replace")
            lines = text.splitlines()[-policy.log_tail_lines :]
            outputs.append(f"== {name} ==\n" + "\n".join(lines))
    compose_services = (
        tuple(policy.databases)
        if selected == "all"
        else ((selected,) if selected in policy.databases else ())
    )
    if compose_services:
        completed = _run(
            compose_command(
                paths,
                policy,
                "--profile",
                "demo",
                "logs",
                "--no-color",
                "--tail",
                str(policy.log_tail_lines),
                *compose_services,
            ),
            cwd=paths.root,
            env=_compose_environment(paths, policy),
            check=False,
            timeout=30,
        )
        outputs.append(completed.stdout + completed.stderr)
    rendered = redact("\n".join(outputs), max_bytes=policy.log_max_bytes)
    print(rendered.rstrip())


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Custometry owned development runtime")
    subparsers = parser.add_subparsers(dest="action", required=True)
    up = subparsers.add_parser("up", help="start the owned development runtime")
    up.add_argument("--mode", choices=("hybrid",), default="hybrid")
    subparsers.add_parser("down", help="stop owned processes and containers; preserve data")
    subparsers.add_parser("status", help="report healthy, degraded, or unavailable state")
    logs = subparsers.add_parser("logs", help="show bounded redacted logs")
    logs.add_argument("service", nargs="?")
    reset = subparsers.add_parser("reset-demo", help="reset only the owned demo volume")
    reset.add_argument("--confirm")
    subparsers.add_parser("validate", help="validate static development and release isolation")
    return parser


def cli(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    root = repo_root()
    try:
        policy = load_policy(root)
        paths = runtime_paths(root, policy)
        if arguments.action == "validate":
            result = static_check(root)
            if result.ok:
                print("development-runtime-validation=passed")
                return 0
            for finding in result.findings:
                print(f"[{finding.code}] {finding.message}", file=sys.stderr)
            return 1
        if arguments.action == "up":
            status = up_runtime(paths, policy)
            print("\n".join(status.lines))
            return STATUS_CODES[status.overall]
        if arguments.action == "down":
            down_runtime(paths, policy)
            print(f"runtime-stopped={paths.project_name} persistent-data=preserved")
            return 0
        if arguments.action == "status":
            status = status_runtime(paths, policy)
            print("\n".join(status.lines))
            return STATUS_CODES[status.overall]
        if arguments.action == "logs":
            logs_runtime(paths, policy, arguments.service)
            return 0
        if arguments.action == "reset-demo":
            reset_demo(paths, policy, arguments.confirm)
            return 0
    except (RuntimeErrorSafe, ValueError) as exc:
        print(f"development-runtime-error: {exc}", file=sys.stderr)
        return 2
    raise AssertionError(f"unhandled action {arguments.action}")


if __name__ == "__main__":
    main_guard(cli)
