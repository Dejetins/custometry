from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/dev"


def run(*command: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        list(command),
        cwd=ROOT,
        env=merged,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )


def test_development_compose_config_is_loopback_only_and_data_is_separated() -> None:
    completed = run(
        "docker",
        "compose",
        "-f",
        "compose.yaml",
        "-f",
        "compose.dev.yaml",
        "--profile",
        "demo",
        "config",
        "--format",
        "json",
        env={
            "COMPOSE_PROJECT_NAME": "custometry-hybrid-test",
            "CUSTOMETRY_HYBRID_PROJECT_NAME": "custometry-hybrid-test",
        },
    )

    assert completed.returncode == 0, completed.stderr
    config = json.loads(completed.stdout)
    assert config["name"] == "custometry-hybrid-test"
    services = config["services"]
    for name in ("control-db", "demo-source-db"):
        assert services[name]["ports"][0]["host_ip"] == "127.0.0.1"
        assert int(services[name]["ports"][0]["target"]) == 5432
    volumes = config["volumes"]
    assert volumes["control_db_data"]["name"] != volumes["demo_source_data"]["name"]
    assert volumes["control_db_data"]["labels"]["com.custometry.data-role"] == "control"
    assert volumes["demo_source_data"]["labels"]["com.custometry.data-role"] == "demo"
    assert config["networks"]["control"].get("internal", False) is False
    assert config["networks"]["demo_source"].get("internal", False) is False


def test_cli_static_validation_and_reset_fail_closed_before_docker_mutation() -> None:
    validation = run(
        str(SCRIPT),
        "validate",
        env={"NVM_DIR": str(ROOT / ".runtime" / "test-missing-nvm")},
    )
    assert validation.returncode == 0, validation.stderr
    assert "development-runtime-validation=passed" in validation.stdout

    missing = run(str(SCRIPT), "reset-demo")
    assert missing.returncode == 2
    assert "requires --confirm RESET-DEMO" in missing.stderr

    incorrect = run(str(SCRIPT), "reset-demo", "--confirm", "RESET-CONTROL")
    assert incorrect.returncode == 2
    assert "requires --confirm RESET-DEMO" in incorrect.stderr


def test_release_entrypoints_do_not_load_development_override() -> None:
    for relative in (
        "deploy/compose/bootstrap.sh",
        "deploy/compose/compose.release.yaml",
        "deploy/compose/ci-smoke.sh",
    ):
        assert "compose.dev.yaml" not in (ROOT / relative).read_text(encoding="utf-8")
