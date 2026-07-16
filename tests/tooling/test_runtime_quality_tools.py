from __future__ import annotations

import json
import socket
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import browser_smoke
from tools.custometry_quality import cleanup
from tools.custometry_quality import compose_lifecycle
from tools.custometry_quality import doctor
from tools.custometry_quality import gate_licenses
from tools.custometry_quality import gate_performance
from tools.custometry_quality import gate_recovery
from tools.custometry_quality import gate_sbom
from tools.custometry_quality import validate_migration_lifecycle


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def dump(path: Path, value: object) -> Path:
    return write(path, json.dumps(value, ensure_ascii=False, sort_keys=True))


def completed(
    command: list[str], returncode: int = 0, stdout: str = "", stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, returncode, stdout=stdout, stderr=stderr)


def simulated_network_failure(command: list[str]) -> bool:
    if "http://1.1.1.1" in command or "raise OSError" in command:
        return True
    if "exec" not in command:
        return False
    exec_index = command.index("exec")
    return (
        command[exec_index + 2 : exec_index + 3] == ["edge"]
        and "http://api:8000/health/live" in command
    )


def doctor_pins(root: Path) -> None:
    write(root / ".node-version", "24.18.0\n")
    write(root / ".uv-version", "0.9.26\n")
    dump(root / "package.json", {"packageManager": "pnpm@11.13.0"})


def version_output(command: list[str]) -> str:
    if command[:2] == ["node", "--version"]:
        return "v24.18.0\n"
    if command[:2] == ["uv", "--version"]:
        return "uv 0.9.26\n"
    if command == ["pnpm", "--version"] or command[:3] == ["corepack", "pnpm", "--version"]:
        return "11.13.0\n"
    return "1.0.0\n"


def test_doctor_runtime_observes_engine_and_rejects_unavailable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(doctor.sys, "version_info", (3, 12, 0))
    doctor_pins(tmp_path)

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        if command == ["pnpm", "--version"]:
            return completed(command, returncode=1, stderr="broken shim")
        if command[:3] == ["docker", "context", "ls"]:
            return completed(
                command,
                stdout=json.dumps(
                    {
                        "Current": True,
                        "Name": "desktop-linux",
                        "DockerEndpoint": "unix:///desktop.sock",
                    }
                )
                + "\n",
            )
        if command[:3] == ["docker", "--context", "desktop-linux"]:
            return completed(
                command,
                stdout=json.dumps(
                    {
                        "Name": "desktop",
                        "DockerRootDir": "/var/lib/docker",
                        "MemTotal": 8_000_000_000,
                    }
                ),
            )
        return completed(command, stdout=version_output(command))

    def which(_command: str) -> str:
        return "/bin/tool"

    def which_without_docker(command: str) -> str | None:
        return None if command == "docker" else "/bin/tool"

    result = doctor.check(
        tmp_path,
        mode="runtime",
        min_free_gib=0,
        which=which,
        runner=runner,
    )
    assert result.ok
    assert result.details["tools"]["pnpm"]["command"] == "corepack pnpm --version"
    failed = doctor.check(
        tmp_path,
        mode="runtime",
        min_free_gib=0,
        which=which_without_docker,
        runner=runner,
    )
    assert not failed.ok
    assert not failed.observed


def test_doctor_rejects_two_responsive_local_engines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(doctor.sys, "version_info", (3, 12, 0))
    doctor_pins(tmp_path)

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        if command[:3] == ["docker", "context", "ls"]:
            contexts = [
                {
                    "Current": True,
                    "Name": "desktop-linux",
                    "DockerEndpoint": "unix:///desktop.sock",
                },
                {
                    "Current": False,
                    "Name": "colima",
                    "DockerEndpoint": "unix:///colima.sock",
                },
            ]
            return completed(command, stdout="\n".join(json.dumps(item) for item in contexts))
        if command[:2] == ["docker", "--context"]:
            context = command[2]
            return completed(
                command,
                stdout=json.dumps(
                    {
                        "Name": context,
                        "DockerRootDir": f"/var/lib/{context}",
                        "MemTotal": 8_000_000_000,
                    }
                ),
            )
        return completed(command, stdout=version_output(command))

    def which(_command: str) -> str:
        return "/bin/tool"

    result = doctor.check(
        tmp_path,
        mode="runtime",
        min_free_gib=0,
        which=which,
        runner=runner,
    )
    assert not result.ok
    assert any(item.code == "container-engine-count-invalid" for item in result.findings)


def test_doctor_writes_owned_runtime_env_atomically_and_refuses_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(doctor.sys, "version_info", (3, 12, 0))
    doctor_pins(tmp_path)

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        if command[:3] == ["docker", "context", "ls"]:
            return completed(
                command,
                stdout=json.dumps(
                    {
                        "Current": True,
                        "Name": "desktop-linux",
                        "DockerEndpoint": "unix:///desktop.sock",
                    }
                ),
            )
        if command[:2] == ["docker", "--context"]:
            return completed(
                command,
                stdout=json.dumps(
                    {
                        "Name": "desktop",
                        "DockerRootDir": "/var/lib/docker",
                        "MemTotal": 8_000_000_000,
                    }
                ),
            )
        return completed(command, stdout=version_output(command))

    def which(_command: str) -> str:
        return "/bin/tool"

    first = doctor.check(
        tmp_path,
        mode="runtime",
        min_free_gib=0,
        which=which,
        runner=runner,
        write_env=Path(".runtime/local.env"),
        http_port_range="49100-49199",
        project_name="custometry-local",
    )
    assert first.ok
    env_path = tmp_path / ".runtime/local.env"
    ownership = tmp_path / ".runtime/local.env.ownership.json"
    assert "CUSTOMETRY_BIND_HOST=127.0.0.1" in env_path.read_text()
    assert json.loads(ownership.read_text())["owned_paths"] == [
        ".runtime/local.env",
        ".runtime/local.env.ownership.json",
    ]
    assert env_path.stat().st_mode & 0o777 == 0o600
    second = doctor.check(
        tmp_path,
        mode="runtime",
        min_free_gib=0,
        which=which,
        runner=runner,
        write_env=Path(".runtime/local.env"),
        http_port_range="49100-49199",
        project_name="custometry-local",
    )
    assert not second.ok
    assert any(item.code == "runtime-env-write-failed" for item in second.findings)


def test_doctor_project_name_is_stable_per_checkout() -> None:
    first = doctor.default_project_name(Path("/workspace/one"))
    assert first == doctor.default_project_name(Path("/workspace/one"))
    assert first != doctor.default_project_name(Path("/workspace/two"))
    assert first.startswith("custometry-") and len(first) == len("custometry-") + 10


def test_doctor_rejects_tool_version_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(doctor.sys, "version_info", (3, 12, 0))
    doctor_pins(tmp_path)

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        if command[:2] == ["node", "--version"]:
            return completed(command, stdout="v22.0.0\n")
        return completed(command, stdout=version_output(command))

    def which(_command: str) -> str:
        return "/bin/tool"

    result = doctor.check(
        tmp_path,
        mode="static",
        min_free_gib=0,
        which=which,
        runner=runner,
    )
    assert not result.ok
    assert any(item.code == "tool-version-mismatch" for item in result.findings)


def test_cleanup_is_dry_run_and_requires_manifest_plus_confirmation(tmp_path: Path) -> None:
    target = write(tmp_path / ".cache/a", "data")
    manifest = dump(tmp_path / "owned.json", {"schema_version": 1, "owned_paths": [".cache"]})
    dry = cleanup.check(tmp_path, manifest)
    assert dry.ok and target.exists() and dry.details["mode"] == "dry-run"
    unconfirmed = cleanup.check(tmp_path, manifest, apply=True)
    assert not unconfirmed.ok and target.exists()
    applied = cleanup.check(tmp_path, manifest, apply=True, confirm=cleanup.CONFIRMATION)
    assert applied.ok and not target.exists()


def compose_files(root: Path, *, host_ip: str = "127.0.0.1") -> None:
    write(
        root / "deploy/edge/nginx.conf",
        """events {}
http {
  upstream custometry_web {
    server web:8080;
  }
  server {
    listen 8080;
    location / {
      proxy_pass http://custometry_web;
    }
  }
}
""",
    )
    write(
        root / "compose.yaml",
        f"""name: custometry
services:
  control-db:
    image: example/db:1
    mem_limit: 128m
    networks: [control]
    healthcheck: {{test: [CMD, true]}}
  migrate:
    image: example/migrate:1
    mem_limit: 64m
    profiles: [migration]
    networks: [control]
    restart: "no"
  api:
    image: example/api:1
    mem_limit: 128m
    networks: [web_to_api, control]
    healthcheck: {{test: [CMD, true]}}
  web:
    image: example/web:1
    mem_limit: 128m
    healthcheck: {{test: [CMD, true]}}
    networks: [edge_to_web, web_to_api]
  edge:
    image: example/web:1
    command: [nginx, -c, /etc/nginx/edge.conf, -g, "daemon off;"]
    mem_limit: 64m
    read_only: true
    healthcheck: {{test: [CMD, true]}}
    ports:
      - target: 8080
        published: 0
        host_ip: {host_ip}
    networks: [ingress_edge, edge_to_web]
networks:
  ingress_edge:
    internal: false
  edge_to_web:
    internal: true
  web_to_api:
    internal: true
  control:
    internal: true
""",
    )
    dump(
        root / "policy.json",
        {
            "schema_version": 2,
            "public_services": {"edge": 8080},
            "public_health_paths": {"edge": "/health/live"},
            "internal_networks": ["edge_to_web", "web_to_api", "control"],
            "edge_networks": ["ingress_edge"],
            "edge_allowlist": ["edge"],
            "ingress_path": {
                "edge_service": "edge",
                "web_service": "web",
                "api_service": "api",
                "edge_to_web_network": "edge_to_web",
                "web_to_api_network": "web_to_api",
                "web_target": "web:8080",
                "api_target": "api:8000",
            },
            "edge_proxy_contract": {
                "source": "deploy/edge/nginx.conf",
                "upstream_name": "custometry_web",
            },
            "ingress_isolation_probes": {
                "allowed": [
                    "wget",
                    "--quiet",
                    "--timeout=2",
                    "--spider",
                    "http://web:8080/health/live",
                ],
                "denied": [
                    "wget",
                    "--quiet",
                    "--timeout=2",
                    "--spider",
                    "http://api:8000/health/live",
                ],
            },
            "egress_networks": [],
            "egress_allowlist": [],
            "negative_egress_probes": {
                "api": {
                    "preflight": ["python", "-c", "print('ok')"],
                    "external": ["python", "-c", "raise OSError"],
                },
                "web": {
                    "preflight": ["wget", "http://api:8000/health/live"],
                    "external": ["wget", "http://1.1.1.1"],
                },
            },
            "max_runtime_memory_gib": 1,
            "lifecycle": {
                "database_services": ["control-db"],
                "migration_service": "migrate",
                "application_services": ["api", "web", "edge"],
                "profiles": ["migration"],
            },
        },
    )


def test_compose_static_and_runtime_fail_closed(tmp_path: Path) -> None:
    compose_files(tmp_path)
    assert compose_lifecycle.static_check(tmp_path, Path("compose.yaml"), Path("policy.json")).ok
    compose_files(tmp_path, host_ip="${CUSTOMETRY_BIND_HOST:-127.0.0.1}")
    assert compose_lifecycle.static_check(tmp_path, Path("compose.yaml"), Path("policy.json")).ok
    compose_files(tmp_path, host_ip="0.0.0.0")
    assert not compose_lifecycle.static_check(
        tmp_path, Path("compose.yaml"), Path("policy.json")
    ).ok
    compose_files(tmp_path)
    with (tmp_path / "compose.yaml").open("a", encoding="utf-8") as stream:
        stream.write("  rogue:\n    internal: false\n")
    unclassified = compose_lifecycle.static_check(
        tmp_path, Path("compose.yaml"), Path("policy.json")
    )
    assert any(item.code == "network-unclassified" for item in unclassified.findings)
    compose_files(tmp_path)

    calls: list[list[str]] = []
    selected_port = compose_lifecycle.select_runtime_port("custometry-ci-test123")

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if "ps" in command:
            return completed(
                command,
                stdout=json.dumps(
                    [
                        {"Service": name, "State": "running", "Health": "healthy"}
                        for name in ("control-db", "api", "web", "edge")
                    ]
                ),
            )
        if "port" in command:
            return completed(command, stdout=f"127.0.0.1:{selected_port}\n")
        if simulated_network_failure(command):
            return completed(command, returncode=1, stderr="network unreachable")
        return completed(command)

    runtime = compose_lifecycle.check(
        tmp_path,
        mode="runtime",
        compose=Path("compose.yaml"),
        policy=Path("policy.json"),
        runner=runner,
        project_name_factory=lambda: "custometry-ci-test123",
        http_port=selected_port,
        health_probe=lambda _url, _timeout: 200,
    )
    assert runtime.ok and runtime.details["runtime_observed"] is True
    assert calls
    assert all(
        command[0:4] == ["docker", "compose", "--project-name", "custometry-ci-test123"]
        for command in calls
    )
    assert calls[-1][-3:] == ["down", "--volumes", "--remove-orphans"]
    assert any(command[-4:] == ["up", "-d", "--wait", "control-db"] for command in calls)
    assert any(command[-3:] == ["run", "--rm", "migrate"] for command in calls)
    assert any(command[-6:] == ["up", "-d", "--wait", "api", "web", "edge"] for command in calls)
    assert any("build" in command for command in calls)
    assert runtime.details["mapped_ports"] == {"edge": selected_port}
    assert runtime.details["ingress_isolation_observed"] == {
        "edge_to_web": True,
        "edge_to_api_denied": True,
    }
    assert runtime.details["negative_egress_observed"] == ["api", "web"]
    assert runtime.details["public_health"]["edge"]["status"] == 200
    runtime_env_paths = [
        Path(command[command.index("--env-file") + 1])
        for command in calls
        if "--env-file" in command
    ]
    assert runtime_env_paths
    assert all(path.parent.parent == tmp_path / ".runtime" for path in runtime_env_paths)
    assert (tmp_path / ".runtime").is_dir()
    assert not any((tmp_path / ".runtime").iterdir())

    write(tmp_path / "release.env", "CUSTOMETRY_API_IMAGE=example/api@sha256:" + "a" * 64)
    write(tmp_path / "release.yaml", "services: {}\n")
    release_calls: list[list[str]] = []

    def release_runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        release_calls.append(command)
        if "ps" in command:
            return completed(
                command,
                stdout=json.dumps(
                    [
                        {"Service": name, "State": "running", "Health": "healthy"}
                        for name in ("control-db", "api", "web", "edge")
                    ]
                ),
            )
        if "port" in command:
            return completed(command, stdout=f"127.0.0.1:{selected_port}\n")
        if simulated_network_failure(command):
            return completed(command, returncode=1, stderr="network unreachable")
        return completed(command)

    release = compose_lifecycle.check(
        tmp_path,
        mode="runtime",
        compose=Path("compose.yaml"),
        policy=Path("policy.json"),
        runner=release_runner,
        project_name_factory=lambda: "custometry-ci-release1",
        release_env=Path("release.env"),
        release_overlay=Path("release.yaml"),
        http_port=selected_port,
        health_probe=lambda _url, _timeout: 200,
    )
    assert release.ok and release.details["artifact_mode"] == "pull"
    assert any("pull" in command for command in release_calls)
    assert not any("build" in command for command in release_calls)


def test_compose_ps_decoder_accepts_array_object_and_ndjson() -> None:
    record = {"Service": "api", "State": "running", "Health": "healthy"}
    assert compose_lifecycle.decode_compose_ps_records(json.dumps(record)) == [record]
    assert compose_lifecycle.decode_compose_ps_records(json.dumps([record])) == [record]
    ndjson = "\n".join((json.dumps(record), json.dumps({**record, "Service": "web"})))
    assert [item["Service"] for item in compose_lifecycle.decode_compose_ps_records(ndjson)] == [
        "api",
        "web",
    ]
    with pytest.raises(ValueError, match="line 2"):
        compose_lifecycle.decode_compose_ps_records(f"{json.dumps(record)}\nnot-json")


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        (
            "networks: [web_to_api, control]",
            "networks: [web_to_api, control, ingress_edge]",
            "edge-network-not-allowlisted",
        ),
        ("read_only: true", "read_only: false", "edge-root-filesystem-writable"),
        (
            "read_only: true\n    healthcheck:",
            "read_only: true\n    volumes: [edge-cache:/cache]\n    healthcheck:",
            "edge-writable-volume-forbidden",
        ),
        (
            "read_only: true\n    healthcheck:",
            "read_only: true\n    secrets: [edge-secret]\n    healthcheck:",
            "edge-secret-mounted",
        ),
        (
            "read_only: true\n    healthcheck:",
            "read_only: true\n    dns: [1.1.1.1]\n    healthcheck:",
            "edge-custom-resolver-forbidden",
        ),
    ],
)
def test_compose_static_rejects_edge_boundary_mutations(
    tmp_path: Path, old: str, new: str, expected_code: str
) -> None:
    compose_files(tmp_path)
    compose = tmp_path / "compose.yaml"
    source = compose.read_text(encoding="utf-8")
    assert old in source
    compose.write_text(source.replace(old, new, 1), encoding="utf-8")
    result = compose_lifecycle.static_check(tmp_path, Path("compose.yaml"), Path("policy.json"))
    assert not result.ok
    assert any(item.code == expected_code for item in result.findings)


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        (
            "networks: [web_to_api, control]",
            "networks: [edge_to_web, web_to_api, control]",
            "edge-api-network-overlap",
        ),
        (
            "networks: [edge_to_web, web_to_api]",
            "networks: [edge_to_web]",
            "web-api-network-members-invalid",
        ),
        (
            "networks: [control]\n    healthcheck:",
            "networks: [control, edge_to_web]\n    healthcheck:",
            "edge-web-network-members-invalid",
        ),
    ],
)
def test_compose_static_rejects_ingress_path_segmentation_drift(
    tmp_path: Path, old: str, new: str, expected_code: str
) -> None:
    compose_files(tmp_path)
    compose = tmp_path / "compose.yaml"
    source = compose.read_text(encoding="utf-8")
    assert old in source
    compose.write_text(source.replace(old, new, 1), encoding="utf-8")
    result = compose_lifecycle.static_check(tmp_path, Path("compose.yaml"), Path("policy.json"))
    assert not result.ok
    assert any(item.code == expected_code for item in result.findings)


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        (
            "server web:8080;",
            "server api:8000;",
            "edge-upstream-target-drift",
        ),
        (
            "server web:8080;",
            "server example.com:443;",
            "edge-upstream-target-drift",
        ),
        (
            "http {",
            "http {\n  resolver 1.1.1.1;",
            "edge-nginx-resolver-forbidden",
        ),
        (
            "proxy_pass http://custometry_web;",
            "proxy_pass http://api:8000;",
            "edge-proxy-pass-drift",
        ),
    ],
)
def test_compose_static_rejects_edge_proxy_source_drift(
    tmp_path: Path, old: str, new: str, expected_code: str
) -> None:
    compose_files(tmp_path)
    source_path = tmp_path / "deploy/edge/nginx.conf"
    source = source_path.read_text(encoding="utf-8")
    assert old in source
    source_path.write_text(source.replace(old, new, 1), encoding="utf-8")
    result = compose_lifecycle.static_check(tmp_path, Path("compose.yaml"), Path("policy.json"))
    assert not result.ok
    assert any(item.code == expected_code for item in result.findings)


def test_compose_policy_requires_denied_ingress_probe(tmp_path: Path) -> None:
    compose_files(tmp_path)
    policy_path = tmp_path / "policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    del policy["ingress_isolation_probes"]["denied"]
    dump(policy_path, policy)
    result = compose_lifecycle.static_check(tmp_path, Path("compose.yaml"), Path("policy.json"))
    assert not result.ok
    assert any(item.code == "compose-contract-invalid" for item in result.findings)


def test_compose_runtime_requires_public_health_and_negative_egress(
    tmp_path: Path,
) -> None:
    compose_files(tmp_path)
    selected_port = compose_lifecycle.select_runtime_port("custometry-ci-proof123")

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        if "ps" in command:
            return completed(
                command,
                stdout=json.dumps(
                    [
                        {"Service": name, "State": "running", "Health": "healthy"}
                        for name in ("control-db", "api", "web", "edge")
                    ]
                ),
            )
        if "port" in command:
            return completed(command, stdout=f"127.0.0.1:{selected_port}\n")
        return completed(command)

    unhealthy = compose_lifecycle.check(
        tmp_path,
        mode="runtime",
        compose=Path("compose.yaml"),
        policy=Path("policy.json"),
        runner=runner,
        project_name_factory=lambda: "custometry-ci-proof123",
        http_port=selected_port,
        health_probe=lambda _url, _timeout: 503,
    )
    assert any(item.code == "compose-public-health-invalid" for item in unhealthy.findings)

    def isolated_runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        if "ps" in command:
            return completed(
                command,
                stdout=json.dumps(
                    [
                        {"Service": name, "State": "running", "Health": "healthy"}
                        for name in ("control-db", "api", "web", "edge")
                    ]
                ),
            )
        if "port" in command:
            return completed(command, stdout=f"127.0.0.1:{selected_port}\n")
        if (
            "exec" in command
            and "http://api:8000/health/live" in command
            and command[command.index("exec") + 2] == "edge"
        ):
            return completed(command, returncode=1, stderr="network unreachable")
        return completed(command)

    unexpected_egress = compose_lifecycle.check(
        tmp_path,
        mode="runtime",
        compose=Path("compose.yaml"),
        policy=Path("policy.json"),
        runner=isolated_runner,
        project_name_factory=lambda: "custometry-ci-proof456",
        http_port=selected_port,
        health_probe=lambda _url, _timeout: 200,
    )
    assert any(item.code == "unexpected-runtime-egress" for item in unexpected_egress.findings)

    direct_api = compose_lifecycle.check(
        tmp_path,
        mode="runtime",
        compose=Path("compose.yaml"),
        policy=Path("policy.json"),
        runner=runner,
        project_name_factory=lambda: "custometry-ci-proof789",
        http_port=selected_port,
        health_probe=lambda _url, _timeout: 200,
    )
    assert any(item.code == "edge-api-isolation-breached" for item in direct_api.findings)


def test_compose_runtime_bounds_checkout_bind_visibility_retry(tmp_path: Path) -> None:
    compose_files(tmp_path)
    selected_port = compose_lifecycle.select_runtime_port("custometry-ci-bind123")
    database_attempts = 0
    observed_delays: list[float] = []

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        nonlocal database_attempts
        if command[-4:] == ["up", "-d", "--wait", "control-db"]:
            database_attempts += 1
            if database_attempts == 1:
                return completed(
                    command,
                    returncode=1,
                    stderr=(
                        'invalid mount config for type "bind": bind source path does not exist'
                    ),
                )
        if "ps" in command:
            return completed(
                command,
                stdout=json.dumps(
                    [
                        {"Service": name, "State": "running", "Health": "healthy"}
                        for name in ("control-db", "api", "web", "edge")
                    ]
                ),
            )
        if "port" in command:
            return completed(command, stdout=f"127.0.0.1:{selected_port}\n")
        if simulated_network_failure(command):
            return completed(command, returncode=1, stderr="network unreachable")
        return completed(command)

    result = compose_lifecycle.check(
        tmp_path,
        mode="runtime",
        compose=Path("compose.yaml"),
        policy=Path("policy.json"),
        runner=runner,
        project_name_factory=lambda: "custometry-ci-bind123",
        http_port=selected_port,
        health_probe=lambda _url, _timeout: 200,
        sleep=observed_delays.append,
    )
    assert result.ok
    assert database_attempts == 2
    assert observed_delays == [compose_lifecycle.BIND_VISIBILITY_RETRY_DELAYS[0]]
    assert result.details["bind_visibility_retries"] == 1
    assert (tmp_path / ".runtime").is_dir()
    assert not any((tmp_path / ".runtime").iterdir())


def test_compose_runtime_fails_after_bounded_bind_visibility_retries(
    tmp_path: Path,
) -> None:
    compose_files(tmp_path)
    selected_port = compose_lifecycle.select_runtime_port("custometry-ci-bind456")
    database_attempts = 0
    observed_delays: list[float] = []

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        nonlocal database_attempts
        if command[-4:] == ["up", "-d", "--wait", "control-db"]:
            database_attempts += 1
            return completed(
                command,
                returncode=1,
                stderr=('invalid mount config for type "bind": bind source path does not exist'),
            )
        return completed(command)

    result = compose_lifecycle.check(
        tmp_path,
        mode="runtime",
        compose=Path("compose.yaml"),
        policy=Path("policy.json"),
        runner=runner,
        project_name_factory=lambda: "custometry-ci-bind456",
        http_port=selected_port,
        health_probe=lambda _url, _timeout: 200,
        sleep=observed_delays.append,
    )
    assert not result.ok
    assert database_attempts == 1 + len(compose_lifecycle.BIND_VISIBILITY_RETRY_DELAYS)
    assert observed_delays == list(compose_lifecycle.BIND_VISIBILITY_RETRY_DELAYS)
    assert any(item.code == "compose-bind-visibility-failed" for item in result.findings)
    assert (tmp_path / ".runtime").is_dir()
    assert not any((tmp_path / ".runtime").iterdir())


def test_compose_runtime_rejects_occupied_explicit_port(tmp_path: Path) -> None:
    compose_files(tmp_path)

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        return completed(command)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as occupied:
        occupied.bind(("127.0.0.1", 0))
        port = int(occupied.getsockname()[1])
        result = compose_lifecycle.check(
            tmp_path,
            mode="runtime",
            compose=Path("compose.yaml"),
            policy=Path("policy.json"),
            http_port=port,
            runner=runner,
        )
    assert not result.ok
    assert result.findings[0].code == "runtime-http-port-unavailable"


def test_browser_manifest_static_and_runtime(tmp_path: Path) -> None:
    write(tmp_path / "deploy/compose/ci-smoke.sh", "#!/usr/bin/env bash\nexit 0\n")
    manifest = dump(
        tmp_path / "browser.json",
        {
            "schema_version": 1,
            "runtime": {
                "lifecycle": browser_smoke.LIFECYCLE,
                "command": ["bash", "deploy/compose/ci-smoke.sh"],
                "environment": {"CUSTOMETRY_RUN_BROWSER": "1"},
            },
            "journeys": [{"name": "help", "path": "/help", "assert_text": "Help"}],
        },
    )
    assert browser_smoke.check(tmp_path, mode="static", manifest=manifest.relative_to(tmp_path)).ok
    observed_env: dict[str, str] = {}

    def browser_runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        observed_env.update(kwargs["env"])
        return completed(command)

    runtime = browser_smoke.check(
        tmp_path,
        mode="runtime",
        manifest=manifest.relative_to(tmp_path),
        runner=browser_runner,
    )
    assert runtime.ok and runtime.details["runtime_observed"]
    assert observed_env["CUSTOMETRY_RUN_BROWSER"] == "1"

    def failed_browser_runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        return completed(command, 1, stderr="boom")

    failed = browser_smoke.check(
        tmp_path,
        mode="runtime",
        manifest=manifest.relative_to(tmp_path),
        runner=failed_browser_runner,
    )
    assert failed.findings[0].code == "browser-smoke-failed"


def test_browser_manifest_rejects_network_downloading_command(tmp_path: Path) -> None:
    write(tmp_path / "deploy/compose/ci-smoke.sh", "#!/usr/bin/env bash\nexit 0\n")
    manifest = dump(
        tmp_path / "browser.json",
        {
            "schema_version": 1,
            "runtime": {
                "lifecycle": browser_smoke.LIFECYCLE,
                "command": ["npx", "--yes", "pnpm@11.13.0"],
                "environment": {"CUSTOMETRY_RUN_BROWSER": "1"},
            },
            "journeys": [{"name": "help", "path": "/help", "assert_text": "Help"}],
        },
    )
    result = browser_smoke.check(tmp_path, mode="static", manifest=manifest.relative_to(tmp_path))
    assert not result.ok
    assert result.findings[0].code == "browser-manifest-invalid"


def migration_files(root: Path) -> None:
    write(
        root / "migrations/versions/001_init.py",
        'revision = "001"\ndown_revision = None\n'
        "def upgrade():\n    return 1\n"
        "def downgrade():\n    return 1\n",
    )


def test_migration_static_and_runtime_steps(tmp_path: Path) -> None:
    migration_files(tmp_path)
    assert validate_migration_lifecycle.check(tmp_path).ok
    manifest = dump(
        tmp_path / "runtime.json",
        {
            "schema_version": 1,
            "commands": {step: ["migration", step] for step in validate_migration_lifecycle.STEPS},
        },
    )
    calls: list[str] = []

    def runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        calls.append(command[-1])
        return completed(command)

    result = validate_migration_lifecycle.check(
        tmp_path,
        mode="runtime",
        runtime_manifest=manifest.relative_to(tmp_path),
        runner=runner,
    )
    assert result.ok and calls == list(validate_migration_lifecycle.STEPS)
    write(
        tmp_path / "migrations/versions/001_init.py",
        'revision="001"\ndown_revision=None\ndef upgrade():\n    pass\ndef downgrade():\n    pass\n',
    )
    assert not validate_migration_lifecycle.check(tmp_path).ok


def test_migration_graph_rejects_unknown_parent_and_multiple_roots(tmp_path: Path) -> None:
    migration_files(tmp_path)
    write(
        tmp_path / "migrations/versions/002_bad.py",
        'revision = "002"\ndown_revision = "missing"\n'
        "def upgrade():\n    return 1\n"
        "def downgrade():\n    return 1\n",
    )
    failed = validate_migration_lifecycle.check(tmp_path)
    assert any(item.code == "migration-parent-unknown" for item in failed.findings)

    write(
        tmp_path / "migrations/versions/002_bad.py",
        'revision = "002"\ndown_revision = None\n'
        "def upgrade():\n    return 1\n"
        "def downgrade():\n    return 1\n",
    )
    failed = validate_migration_lifecycle.check(tmp_path)
    assert any(item.code == "migration-root-count-invalid" for item in failed.findings)


def cyclone(license_id: str = "Apache-2.0") -> dict[str, Any]:
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "components": [
            {
                "type": "library",
                "name": "package",
                "version": "1",
                "licenses": [{"license": {"id": license_id}}],
            }
        ],
    }


def test_sbom_and_license_gates_reject_unknown(tmp_path: Path) -> None:
    sbom = dump(tmp_path / "sbom.json", cyclone())
    policy = dump(
        tmp_path / "policy.json",
        {"schema_version": 1, "allowed": ["Apache-2.0"], "denied": ["GPL-3.0-only"]},
    )
    assert gate_sbom.check(tmp_path, sbom.relative_to(tmp_path)).ok
    assert gate_licenses.check(
        tmp_path, sbom.relative_to(tmp_path), policy.relative_to(tmp_path)
    ).ok
    dump(sbom, cyclone("NOASSERTION"))
    failed = gate_licenses.check(tmp_path, sbom.relative_to(tmp_path), policy.relative_to(tmp_path))
    assert failed.findings[0].code == "license-unknown"


def test_license_gate_ignores_file_inventory_and_classifies_review_required(
    tmp_path: Path,
) -> None:
    document = cyclone("MPL-2.0")
    document["components"].append({"type": "file", "name": "/app/record", "version": "1"})
    sbom = dump(tmp_path / "sbom.json", document)
    policy = dump(
        tmp_path / "policy.json",
        {
            "schema_version": 1,
            "allowed": ["Apache-2.0"],
            "denied": ["AGPL-3.0-only"],
            "review_required": ["MPL-2.0"],
        },
    )
    result = gate_licenses.check(tmp_path, sbom.relative_to(tmp_path), policy.relative_to(tmp_path))
    assert [finding.code for finding in result.findings] == ["license-review-required"]
    assert result.details["components_evaluated"] == 1
    assert result.details["components_ignored"] == 1


def test_license_gate_rejects_overlapping_policy_categories(tmp_path: Path) -> None:
    sbom = dump(tmp_path / "sbom.json", cyclone())
    policy = dump(
        tmp_path / "policy.json",
        {
            "schema_version": 1,
            "allowed": ["Apache-2.0"],
            "denied": ["Apache-2.0"],
            "review_required": [],
        },
    )
    result = gate_licenses.check(tmp_path, sbom.relative_to(tmp_path), policy.relative_to(tmp_path))
    assert result.findings[0].code == "license-input-invalid"


def test_release_sbom_is_bound_to_expected_candidate_digests(tmp_path: Path) -> None:
    subject = "sha256:" + "a" * 64
    document = cyclone()
    document["metadata"] = {"properties": [{"name": gate_sbom.SUBJECT_PROPERTY, "value": subject}]}
    sbom = dump(tmp_path / "sbom.json", document)
    assert gate_sbom.check(
        tmp_path,
        sbom.relative_to(tmp_path),
        expected_subjects=[subject],
        require_subjects=True,
    ).ok
    drift = gate_sbom.check(
        tmp_path,
        sbom.relative_to(tmp_path),
        expected_subjects=["sha256:" + "b" * 64],
        require_subjects=True,
    )
    assert any(item.code == "sbom-subject-drift" for item in drift.findings)
    missing_expectation = gate_sbom.check(
        tmp_path, sbom.relative_to(tmp_path), require_subjects=True
    )
    assert not missing_expectation.ok and not missing_expectation.observed


def test_recovery_and_performance_evidence_gates(tmp_path: Path) -> None:
    now = datetime.now(UTC).isoformat()
    recovery = dump(
        tmp_path / "recovery.json",
        {
            "schema_version": 1,
            "started_at": now,
            "finished_at": now,
            "environment": "ci",
            "restore_target_disposable": True,
            "backup_created": True,
            "restore_succeeded": True,
            "data_hash_match": True,
            "application_restart_succeeded": True,
            "backup_manifest": {"sha256": "a" * 64},
        },
    )
    assert gate_recovery.check(tmp_path, recovery.relative_to(tmp_path)).ok
    data = json.loads(recovery.read_text())
    data["data_hash_match"] = False
    dump(recovery, data)
    assert any(
        item.code == "recovery-proof-failed"
        for item in gate_recovery.check(tmp_path, recovery.relative_to(tmp_path)).findings
    )

    performance = dump(
        tmp_path / "performance.json",
        {
            "schema_version": 1,
            "measured_at": now,
            "environment": "ci-arm64",
            "workload": "smoke",
            "command": "benchmark",
            "baseline_identity": "base",
            "candidate_identity": "candidate",
            "metrics": [
                {
                    "name": "latency_ms",
                    "direction": "lower",
                    "baseline": 100,
                    "candidate": 104,
                    "max_regression_percent": 5,
                    "samples": 5,
                }
            ],
        },
    )
    assert gate_performance.check(tmp_path, performance.relative_to(tmp_path)).ok
    data = json.loads(performance.read_text())
    data["metrics"][0]["candidate"] = 110
    dump(performance, data)
    assert (
        gate_performance.check(tmp_path, performance.relative_to(tmp_path)).findings[0].code
        == "performance-regression"
    )


def test_missing_runtime_evidence_is_failure(tmp_path: Path) -> None:
    result = gate_recovery.check(tmp_path, Path("missing.json"))
    assert not result.ok and not result.observed
    assert result.findings[0].code == "recovery-evidence-missing"
