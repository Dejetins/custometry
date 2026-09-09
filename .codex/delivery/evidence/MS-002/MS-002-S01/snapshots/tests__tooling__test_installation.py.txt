"""Persistent ownership, retry and fail-closed installer contracts."""

import argparse
import json
from pathlib import Path
import socket
import subprocess
import sys
from typing import Any

import pytest

from tools.custometry_quality import installation as subject


def args(root: Path, source: Path, trust: Path) -> argparse.Namespace:
    return argparse.Namespace(
        root=root,
        action="install",
        source=source,
        trust=trust,
        demo=False,
        bind="127.0.0.1",
        lan=False,
        port=0,
        certificate=None,
        private_key=None,
        trust_root=None,
    )


def initialized(tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    source = tmp_path / "source"
    source.mkdir()
    trust = tmp_path / "trust.json"
    trust.write_text(
        json.dumps({"files": [{"path": "delivery.zip", "size_bytes": 1, "sha256": "a" * 64}]})
    )
    root = tmp_path / "owned"
    with subject.locked(root, True):
        data = subject.initial(root, args(root, source, trust), {"context": "test", "cpu_cap": 4})
        subject.prepare(root, data)
    return root, data


def test_identity_and_secret_survive_repeat_and_competing_process(tmp_path: Path) -> None:
    root, data = initialized(tmp_path)
    before = (root / "installation.json").read_bytes()
    password = (root / "secrets/control_db_password").read_bytes()
    with subject.locked(root):
        process = subprocess.run(
            [
                sys.executable,
                "-c",
                "from pathlib import Path; "
                "from tools.custometry_quality.installation import locked; "
                f"\nwith locked(Path({str(root)!r})): pass",
            ],
            capture_output=True,
            text=True,
        )
        assert process.returncode != 0
        assert "INSTALLATION_LOCKED" in process.stderr
        subject.prepare(root, data)
    assert (root / "installation.json").read_bytes() == before
    assert (root / "secrets/control_db_password").read_bytes() == password
    assert subject.read_state(root)["id"] == data["id"]


def test_foreign_root_and_symlink_never_adopted(tmp_path: Path) -> None:
    foreign = tmp_path / "foreign"
    foreign.mkdir(mode=0o700)
    sentinel = foreign / "sentinel"
    sentinel.write_text("foreign")
    with pytest.raises(subject.consumer.ConsumerError, match="FOREIGN_ROOT"):
        with subject.locked(foreign, True):
            pass
    link = tmp_path / "link"
    link.symlink_to(foreign, target_is_directory=True)
    with pytest.raises(subject.consumer.ConsumerError, match="UNSAFE_PATH"):
        with subject.locked(link, True):
            pass
    assert sentinel.read_text() == "foreign"
    assert list(foreign.iterdir()) == [sentinel]


def test_unknown_state_and_secret_symlink(tmp_path: Path) -> None:
    root, data = initialized(tmp_path)
    data["schema_version"] = "future/v2"
    subject.atomic(root / "installation.json", data)
    with pytest.raises(subject.consumer.ConsumerError, match="STATE_SCHEMA"):
        subject.read_state(root)
    secret = root / "secrets/control_db_password"
    secret.unlink()
    secret.symlink_to(tmp_path / "absent")
    with pytest.raises(OSError):
        subject.prepare(root, data)
    assert not (tmp_path / "absent").exists()


def test_engine_mismatch() -> None:
    saved = {"context": "a", "id": "one", "endpoint": "unix:///a", "architecture": "arm64"}
    for key in saved:
        changed = {**saved, key: "other"}
        with pytest.raises(subject.consumer.ConsumerError, match="ENGINE_IDENTITY"):
            subject.same_engine(saved, changed)


@pytest.mark.parametrize("name", ["../escape", "/absolute", "a//b", "a\\b", "./file"])
def test_inventory_traversal_before_copy(tmp_path: Path, name: str) -> None:
    with pytest.raises(subject.consumer.ConsumerError, match="TRUST_PATH"):
        subject.consumer.checked_copy(
            tmp_path,
            tmp_path / "copy",
            {"files": [{"path": name, "size_bytes": 0, "sha256": "a" * 64}]},
        )
    assert not (tmp_path / "copy").exists()


def test_corrupt_copy_cannot_execute_reader(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "payload").write_text("altered")
    with pytest.raises(subject.consumer.ConsumerError, match="TRUSTED_HASH"):
        subject.consumer.checked_copy(
            source,
            tmp_path / "copy",
            {"files": [{"path": "payload", "size_bytes": 7, "sha256": "a" * 64}]},
        )


def test_failure_records_resumable_state_without_regenerating_secret(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, data = initialized(tmp_path)
    monkeypatch.setattr(subject, "engine", lambda *_: data["engine"])
    monkeypatch.setattr(subject, "same_engine", lambda *_: None)

    def failed(*_: Any) -> None:
        raise subject.consumer.ConsumerError("COMMAND_TIMEOUT")

    monkeypatch.setattr(subject, "acquire", failed)
    secret = (root / "secrets/control_db_password").read_bytes()
    request = args(root, tmp_path, tmp_path)
    request.action = "resume"
    with pytest.raises(subject.consumer.ConsumerError, match="COMMAND_TIMEOUT"):
        subject.execute(request)
    after = subject.read_state(root)
    assert (after["state"], after["last_completed_step"], after["failure_code"]) == (
        "failed",
        "prepared",
        "COMMAND_TIMEOUT",
    )
    assert after["id"] == data["id"]
    assert (root / "secrets/control_db_password").read_bytes() == secret


def test_unknown_head_never_runs_migration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, data = initialized(tmp_path)
    runtime = subject.Runtime(root, data)
    commands: list[list[str]] = []
    monkeypatch.setattr(runtime, "ownership", lambda: None)
    monkeypatch.setattr(runtime, "run", lambda *_: "")
    monkeypatch.setattr(runtime, "cp", lambda command, *rest: commands.append(command) or "")
    monkeypatch.setattr(runtime, "database_head", lambda: "future_head")
    with pytest.raises(subject.consumer.ConsumerError, match="SCHEMA_FORWARD_REPAIR"):
        runtime.migrate()
    assert not any("migrate" in command for command in commands)


def test_foreign_volume_labels_fail_before_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, data = initialized(tmp_path)
    data["volumes"] = {"control_db_data": {}}
    runtime = subject.Runtime(root, data)

    def response(command: list[str], *_: Any) -> str:
        if "ls" in command:
            return data["id"] + "_control_db_data"
        return '[{"Labels": {"com.docker.compose.project": "foreign"}}]'

    monkeypatch.setattr(runtime, "run", response)
    with pytest.raises(subject.consumer.ConsumerError, match="FOREIGN_RESOURCE"):
        runtime.ownership()


def test_occupied_explicit_port(tmp_path: Path) -> None:
    root, _ = initialized(tmp_path)
    request = args(root, tmp_path / "source", tmp_path / "trust.json")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        request.port = sock.getsockname()[1]
        with pytest.raises(subject.consumer.ConsumerError, match="PORT_UNAVAILABLE"):
            subject.initial(root, request, {})


def test_command_does_not_inherit_compose_or_engine_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("COMPOSE_FILE", "/foreign")
    monkeypatch.setenv("DOCKER_HOST", "tcp://foreign")
    result = subject.command(
        [
            sys.executable,
            "-c",
            "import os; print('COMPOSE_FILE' in os.environ or 'DOCKER_HOST' in os.environ)",
        ]
    )
    assert result == "False"


@pytest.mark.parametrize(
    "field,value,code",
    [
        ("DriverStatus", [], "CONTAINERD_STORE_REQUIRED"),
        ("OSType", "windows", "ENGINE_OS_UNSUPPORTED"),
        ("Architecture", "riscv64", "ENGINE_PLATFORM_UNSUPPORTED"),
        ("MemTotal", 1024, "ENGINE_RESOURCES"),
    ],
)
def test_engine_preflight_rejects_unsupported_inputs(
    monkeypatch: pytest.MonkeyPatch, field: str, value: Any, code: str
) -> None:
    info = {
        "ID": "engine",
        "OSType": "linux",
        "Architecture": "arm64",
        "DriverStatus": [["driver-type", "io.containerd.snapshotter.v1"]],
        "MemTotal": 8 * subject.GIB,
        "NCPU": 4,
        "ServerVersion": "29.6.2",
    }
    info[field] = value

    def command(arguments: list[str]) -> str:
        if arguments[-1] == "show":
            return "local"
        if "context" in arguments and "inspect" in arguments:
            return '[{"Endpoints":{"docker":{"Host":"unix:///local.sock"}}}]'
        if "info" in arguments:
            return json.dumps(info)
        return "2.39.0"

    monkeypatch.setattr(subject, "command", command)
    with pytest.raises(subject.consumer.ConsumerError, match=code):
        subject.engine()


def test_config_edit_is_rejected_before_compose(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, data = initialized(tmp_path)
    config = root / "config/compose.json"
    subject.atomic(config, {"services": {}})
    data["config_sha256"] = subject.sha(config)
    subject.atomic(config, {"services": {"foreign": {}}})

    def unexpected(*_: Any, **__: Any) -> str:
        pytest.fail("A modified Compose file must not be executed")

    monkeypatch.setattr(subject, "command", unexpected)
    with pytest.raises(subject.consumer.ConsumerError, match="CONFIG_CHANGED"):
        subject.Runtime(root, data).cp(["stop"])


def test_failed_preflight_does_not_leave_unadoptable_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "new"
    request = args(root, tmp_path / "absent", tmp_path / "absent-trust")
    monkeypatch.setattr(subject, "engine", lambda: {})
    with pytest.raises(subject.consumer.ConsumerError, match="SUPPLY_MISSING"):
        subject.execute(request)
    assert not root.exists()
