from __future__ import annotations

import copy
import json
import shutil
import subprocess
from pathlib import Path
from typing import Mapping, Sequence, cast

import pytest

from tools.custometry_quality import development_runtime
from tools.custometry_quality.core import JsonObject, json_object


ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "deploy/compose/development-runtime-policy.json"


def policy_document() -> JsonObject:
    value = cast(object, json.loads(POLICY_PATH.read_text(encoding="utf-8")))
    assert isinstance(value, dict)
    return cast(JsonObject, value)


def test_repository_development_runtime_contract_is_valid() -> None:
    result = development_runtime.static_check(ROOT)

    assert result.ok, result.to_dict()


def test_release_entrypoint_rejects_development_override_reference(tmp_path: Path) -> None:
    policy = development_runtime.load_policy(ROOT)
    required = (
        development_runtime.POLICY_PATH,
        Path("compose.dev.yaml"),
        Path("scripts/dev"),
        *policy.release_entrypoints,
    )
    for relative in required:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    bootstrap = tmp_path / "deploy/compose/bootstrap.sh"
    bootstrap.write_text(
        bootstrap.read_text(encoding="utf-8") + "\n# compose.dev.yaml must not enter release\n",
        encoding="utf-8",
    )

    result = development_runtime.static_check(tmp_path)

    assert not result.ok
    assert {finding.code for finding in result.findings} == {
        "development-override-in-release-path"
    }


def test_policy_requires_loopback_only_unique_ports() -> None:
    document = copy.deepcopy(policy_document())
    databases = json_object(document["database_services"], "database_services")
    control = json_object(databases["control-db"], "control-db")
    control["host"] = "0.0.0.0"

    with pytest.raises(ValueError, match="exactly 127.0.0.1"):
        development_runtime.parse_policy(document)

    document = copy.deepcopy(policy_document())
    databases = json_object(document["database_services"], "database_services")
    processes = json_object(document["host_processes"], "host_processes")
    control = json_object(databases["control-db"], "control-db")
    api = json_object(processes["api"], "api")
    api["port"] = control["port"]
    api["url"] = f"http://127.0.0.1:{control['port']}"

    with pytest.raises(ValueError, match="ports must be distinct"):
        development_runtime.parse_policy(document)


def test_policy_separates_control_and_demo_volumes_and_reset_target() -> None:
    document = copy.deepcopy(policy_document())
    databases = json_object(document["database_services"], "database_services")
    control = json_object(databases["control-db"], "control-db")
    demo = json_object(databases["demo-source-db"], "demo-source-db")
    demo["volume"] = control["volume"]
    document["reset_volume"] = control["volume"]

    with pytest.raises(ValueError, match="distinct volumes"):
        development_runtime.parse_policy(document)

    document = copy.deepcopy(policy_document())
    document["reset_volume"] = "control_db_data"
    with pytest.raises(ValueError, match="demo-source volume"):
        development_runtime.parse_policy(document)


def test_runtime_identity_is_stable_and_repository_specific(tmp_path: Path) -> None:
    policy = development_runtime.load_policy(ROOT)

    first = development_runtime.runtime_paths(tmp_path / "one", policy)
    repeated = development_runtime.runtime_paths(tmp_path / "one", policy)
    other = development_runtime.runtime_paths(tmp_path / "two", policy)

    assert first.project_name == repeated.project_name
    assert first.project_name.startswith("custometry-hybrid-")
    assert first.project_name != other.project_name
    assert first.runtime_dir.is_relative_to(tmp_path / "one" / ".runtime/development")


def test_runtime_directory_symlink_escape_is_rejected(tmp_path: Path) -> None:
    policy = development_runtime.load_policy(ROOT)
    root = tmp_path / "repository"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / ".runtime").symlink_to(outside, target_is_directory=True)
    paths = development_runtime.runtime_paths(root, policy)

    with pytest.raises(development_runtime.RuntimeErrorSafe, match="symbolic link"):
        development_runtime.prepare_runtime(paths, policy)

    assert not (outside / "development").exists()


def test_log_redaction_is_bounded() -> None:
    payload = (
        "password=hunter2\n"
        "TOKEN: abcdef\n"
        "postgresql://custometry:very-secret@127.0.0.1:55432/custometry\n"
        + "x" * 2048
    )

    rendered = development_runtime.redact(payload, max_bytes=512)

    assert "hunter2" not in rendered
    assert "abcdef" not in rendered
    assert "very-secret" not in rendered
    assert "[REDACTED]" in rendered
    assert len(rendered.encode("utf-8")) <= 512


def test_demo_reset_requires_exact_owned_volume_labels(tmp_path: Path) -> None:
    policy = development_runtime.load_policy(ROOT)
    paths = development_runtime.runtime_paths(tmp_path, policy)
    demo_volume = development_runtime.expected_volume_name(paths, "demo")
    labels = {
        **development_runtime.OWNERSHIP_LABELS,
        "com.custometry.data-role": "demo",
        "com.docker.compose.project": paths.project_name,
        "com.docker.compose.volume": "demo_source_data",
    }

    development_runtime.validate_demo_volume_labels(paths, policy, demo_volume, labels)

    with pytest.raises(development_runtime.RuntimeErrorSafe, match="not the exact"):
        development_runtime.validate_demo_volume_labels(
            paths,
            policy,
            development_runtime.expected_volume_name(paths, "control"),
            labels,
        )
    with pytest.raises(development_runtime.RuntimeErrorSafe, match="ownership labels"):
        development_runtime.validate_demo_volume_labels(paths, policy, demo_volume, {})


def test_owned_process_requires_pid_group_and_exact_start_fingerprint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    record = {
        "pid": 123,
        "pgid": 123,
        "started": "Mon Jul 21 01:00:00 2026",
        "observed_command": "uv run uvicorn",
    }
    def fingerprint(pid: int) -> tuple[str, str] | None:
        return ("Mon Jul 21 01:00:00 2026", "uv run uvicorn") if pid == 123 else None

    def process_group(pid: int) -> int:
        return pid

    monkeypatch.setattr(development_runtime, "_process_fingerprint", fingerprint)
    monkeypatch.setattr(development_runtime.os, "getpgid", process_group)

    assert development_runtime.owned_process_identity(record) == (123, 123)

    record["started"] = "Mon Jul 21 02:00:00 2026"
    assert development_runtime.owned_process_identity(record) is None


def test_status_distinguishes_healthy_degraded_and_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    policy = development_runtime.load_policy(ROOT)
    paths = development_runtime.runtime_paths(tmp_path, policy)
    def engine(root: Path) -> str:
        return "desktop-linux"

    def healthy_compose(
        runtime_paths: development_runtime.RuntimePaths,
        runtime_policy: development_runtime.RuntimePolicy,
    ) -> dict[str, str]:
        return {
            "control-db": "healthy",
            "demo-source-db": "healthy",
        }

    def empty_state(runtime_paths: development_runtime.RuntimePaths) -> dict[str, object]:
        return {"processes": {}}

    monkeypatch.setattr(development_runtime, "_ensure_engine", engine)
    monkeypatch.setattr(development_runtime, "compose_health", healthy_compose)
    monkeypatch.setattr(development_runtime, "_load_state", empty_state)

    assert development_runtime.status_runtime(paths, policy).overall == "degraded"

    def unavailable_compose(
        runtime_paths: development_runtime.RuntimePaths,
        runtime_policy: development_runtime.RuntimePolicy,
    ) -> dict[str, str]:
        return {
            "control-db": "unavailable",
            "demo-source-db": "unavailable",
        }

    monkeypatch.setattr(development_runtime, "compose_health", unavailable_compose)
    assert development_runtime.status_runtime(paths, policy).overall == "unavailable"


def test_compose_health_requires_loopback_tcp_visibility(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    policy = development_runtime.load_policy(ROOT)
    paths = development_runtime.runtime_paths(tmp_path, policy)
    records = [
        {"Service": "control-db", "State": "running", "Health": "healthy"},
        {"Service": "demo-source-db", "State": "running", "Health": "healthy"},
    ]

    def compose_ps(
        command: Sequence[str],
        *,
        cwd: Path,
        env: Mapping[str, str] | None = None,
        timeout: int = 120,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0, json.dumps(records), "")

    def tcp_hidden(host: str, port: int, timeout: float = 0.5) -> bool:
        return False

    monkeypatch.setattr(development_runtime, "_run", compose_ps)
    monkeypatch.setattr(development_runtime, "_tcp_ready", tcp_hidden)

    assert development_runtime.compose_health(paths, policy) == {
        "control-db": "degraded",
        "demo-source-db": "degraded",
    }
