"""Opt-in real Docker S02 boundary; keeps the isolated owned root/volumes stopped."""

import copy
import json
import os
from pathlib import Path
import secrets
import shutil
import ssl
import urllib.error
import urllib.request
from typing import Any

import pytest

from tools.custometry_quality import installation as installer


def test_installed_https_and_real_readiness(monkeypatch: pytest.MonkeyPatch) -> None:
    base_path = os.environ.get("CUSTOMETRY_S02_BASE_STATE")
    image = os.environ.get("CUSTOMETRY_S02_API_IMAGE")
    tls_dir = os.environ.get("CUSTOMETRY_S02_TLS_DIRECTORY")
    if not base_path or not image or not tls_dir:
        pytest.skip("Explicit isolated S02 runtime inputs required")
    base = json.loads(Path(base_path).read_bytes())
    root = Path(base["root"]).parent / ("ms002-s02-" + secrets.token_hex(6))
    root.mkdir(mode=0o700)
    state = copy.deepcopy(base)
    state.update(
        id="custometry-" + secrets.token_hex(12),
        root=str(root),
        state="prepared",
        last_completed_step="prepared",
        demo=False,
        port=0,
        origin=None,
        failure_code=None,
        volumes={},
        networks={},
    )
    state.pop("config_sha256", None)
    for item in state["images"]:
        if item["role"] == "api":
            item["docker_id"] = image
    installer.atomic(root / "installation.json", state)
    installer.prepare(root, state)
    shutil.copytree(
        Path(base["root"]) / "acquisition/current/bundle", root / "acquisition/current/bundle"
    )
    runtime = installer.Runtime(root, state)
    files = {
        "certificate": str(Path(tls_dir) / "local-cert.pem"),
        "private_key": str(Path(tls_dir) / "local-key.pem"),
        "trust_root": str(Path(tls_dir) / "ca/rootCA.pem"),
    }
    outcomes = {}
    try:
        runtime.configure()
        runtime.migrate()
        installer.checkpoint(root, state, "migrated")
        runtime.activate_tls(files)
        installer.checkpoint(root, state, "ready")
        outcomes["ready"] = runtime.installed_status()["state"]
        context = ssl.create_default_context(cafile=files["trust_root"])
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=context)
        )

        def request(
            path: str, method: str = "GET", headers: dict[str, str] | None = None
        ) -> tuple[int, dict[str, str], bytes]:
            req = urllib.request.Request(
                state["origin"] + path, method=method, headers=headers or {}
            )
            try:
                response = opener.open(req, timeout=10)
            except urllib.error.HTTPError as error:
                response = error
            with response:
                response_status = response.status
                assert isinstance(response_status, int)
                return (
                    response_status,
                    {k.lower(): v for k, v in response.headers.items()},
                    bytes(response.read()),
                )

        for path in (
            "/",
            "/docs/",
            "/api/health/live",
            "/api/health/ready",
            "/api/version",
            "/api/installation/status",
        ):
            assert request(path)[0] == 200, path
        for path in (
            "/identity",
            "/api/identity/bootstrap",
            "/api/openapi.json",
            "/api/connections",
            "/workspace",
            "/api/installation/status/extra",
        ):
            assert request(path)[0] == 403, path
        for method in ("POST", "PUT", "DELETE", "OPTIONS", "HEAD"):
            assert request("/api/installation/status", method)[0] == 405
        assert request("/", headers={"Origin": "https://unapproved.invalid"})[0] == 403
        assert request("/", headers={"Host": "127.0.0.1:1"})[0] == 403
        assert request("/", headers={"Origin": state["origin"]})[0] == 200
        outcomes["restricted_ingress"] = "pass"
        edge_id = runtime.cp(["ps", "-q", "edge"])
        api_id = runtime.cp(["ps", "-q", "api"])
        db_id = runtime.cp(["ps", "-q", "control-db"])
        for target, network, port in ((api_id, "web_to_api", "8000"), (db_id, "control", "5432")):
            item = json.loads(runtime.run(["inspect", target]))[0]
            address = item["NetworkSettings"]["Networks"][state["id"] + "_" + network]["IPAddress"]
            with pytest.raises(installer.consumer.ConsumerError):
                runtime.run(["exec", edge_id, "nc", "-z", "-w", "2", address, port])
        runtime.cp(["exec", "-T", "edge", "wget", "-qO-", "http://web:8080/health/live"])
        runtime.cp(["exec", "-T", "web", "wget", "-qO-", "http://api:8000/health/live"])
        outcomes["adjacency"] = "pass"
        with pytest.raises((urllib.error.HTTPError, urllib.error.URLError, ConnectionError)):
            urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
                state["origin"].replace("https:", "http:") + "/", timeout=5
            )
        outcomes["no_http_fallback"] = "pass"
        active_hash = installer.sha(root / "config/compose.json")
        active_revision = state["tls"]["revision"]
        negative_dir = Path(tls_dir) / "s02-negative-tls"
        for candidate in (
            {
                **files,
                "certificate": str(negative_dir / "wrong-cert.pem"),
                "private_key": str(negative_dir / "wrong-key.pem"),
            },
            {**files, "private_key": str(negative_dir / "wrong-key.pem")},
            {**files, "certificate": str(negative_dir / "expired-cert.pem")},
        ):
            with pytest.raises(installer.consumer.ConsumerError, match="TLS_INVALID"):
                runtime.activate_tls(candidate)
            assert installer.sha(root / "config/compose.json") == active_hash
            assert state["tls"]["revision"] == active_revision
            assert runtime.installed_status()["state"] == "ready_for_bootstrap"
        outcomes["invalid_tls_retains_active"] = "pass"
        original_config = runtime.installed_config

        def invalid_config(tls: dict[str, Any]) -> dict[str, Any]:
            config = original_config(tls)
            path = next(Path(p) for p in tls["configs"] if p.endswith("edge.conf"))
            path.chmod(0o600)
            path.write_text(path.read_text() + "invalid_directive;\n")
            path.chmod(0o444)
            return config

        with monkeypatch.context() as patch:
            patch.setattr(runtime, "installed_config", invalid_config)
            with pytest.raises(installer.consumer.ConsumerError, match="COMMAND_FAILED"):
                runtime.activate_tls(files)
        assert installer.sha(root / "config/compose.json") == active_hash
        assert runtime.installed_status()["state"] == "ready_for_bootstrap"
        outcomes["invalid_nginx_retains_active"] = "pass"

        # Real schema mutation is confined to this newly created operational test DB.
        def sql(query: str) -> str:
            return runtime.cp(
                [
                    "exec",
                    "-T",
                    "control-db",
                    "psql",
                    "-U",
                    "custometry",
                    "-d",
                    "custometry",
                    "-At",
                    "-c",
                    query,
                ]
            )

        try:
            sql("UPDATE alembic_version SET version_num='unsupported'")
            code, headers, body = request("/api/installation/status")
            assert code == 503 and json.loads(body)["code"] == "SCHEMA_INCOMPATIBLE"
            assert headers["cache-control"] == "no-store"
            assert request("/api/health/ready")[0] == 503
        finally:
            sql("UPDATE alembic_version SET version_num='0009_notifications'")
        config_path = root / "config/compose.json"
        writable_config = json.loads(config_path.read_bytes())
        readonly_config = copy.deepcopy(writable_config)
        readonly_config["services"]["api"]["volumes"] = [
            str(root / "artifacts") + ":/var/lib/custometry/artifacts:ro"
        ]
        installer.atomic(config_path, readonly_config)
        state["config_sha256"] = installer.sha(config_path)
        runtime.cp(["up", "-d", "--no-deps", "api"])
        try:
            # Wait for liveness, not readiness, on the deliberately unwritable mount.
            import time

            deadline = time.monotonic() + 20
            while request("/api/health/live")[0] != 200:
                assert time.monotonic() < deadline
                time.sleep(1)
            code, _, body = request("/api/installation/status")
            assert code == 503 and json.loads(body)["code"] == "STORAGE_UNAVAILABLE"
        finally:
            installer.atomic(config_path, writable_config)
            state["config_sha256"] = installer.sha(config_path)
            runtime.cp(["up", "-d", "--no-deps", "--wait", "api"])
        runtime.cp(["stop", "control-db"])
        try:
            code, _, body = request("/api/installation/status")
            assert code == 503 and json.loads(body)["code"] == "DATABASE_UNAVAILABLE"
            assert b"/var/" not in body and b"SELECT" not in body
        finally:
            runtime.cp(["up", "-d", "--no-deps", "--wait", "control-db"])
        assert runtime.installed_status()["state"] == "ready_for_bootstrap"
        outcomes["database_schema_storage_negatives"] = "pass"
        # Rotation with the same valid external pair still creates a new immutable revision.
        previous = state["tls"]["revision"]
        runtime.activate_tls(files)
        assert state["tls"]["revision"] != previous
        assert runtime.installed_status()["state"] == "ready_for_bootstrap"
        outcomes["rotation"] = "pass"
        before_secret = installer.sha(root / "secrets/control_db_password")
        before_tls = copy.deepcopy(state["tls"])
        runtime.cp(["stop"])
        runtime.cp(["up", "-d", "--no-deps", "--wait", "control-db", "api", "web", "edge"])
        assert runtime.installed_status()["state"] == "ready_for_bootstrap"
        assert installer.sha(root / "secrets/control_db_password") == before_secret
        assert state["tls"] == before_tls
        assert sql("SELECT version_num FROM alembic_version") == "0009_notifications"
        outcomes["stop_restart_persistence"] = "pass"
    finally:
        runtime.cp(["stop"])
        state["state"] = "stopped"
        installer.atomic(root / "installation.json", state)
        # Private runtime receipt for reruns; durable report copies safe observations only.
        installer.atomic(root / "logs/test-result.json", outcomes)
        print("S02 runtime root:", root)
