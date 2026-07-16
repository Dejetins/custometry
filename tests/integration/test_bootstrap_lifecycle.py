from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = ROOT / "deploy/compose/bootstrap.sh"


def run_bootstrap(tmp_path: Path, *arguments: str, path: str | None = None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("COMPOSE_PROJECT_NAME", None)
    environment.pop("CUSTOMETRY_DATA_PROFILE", None)
    environment["CUSTOMETRY_RUNTIME_ENV_FILE"] = str(tmp_path / "runtime.env")
    environment["CUSTOMETRY_SECRETS_DIR"] = str(tmp_path / "secrets")
    if path is not None:
        environment["PATH"] = path
    return subprocess.run(
        ["bash", str(BOOTSTRAP), *arguments],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def test_down_without_installation_is_truthful_and_creates_no_state(tmp_path: Path) -> None:
    completed = run_bootstrap(tmp_path, "--down")

    assert completed.returncode == 0
    assert "nothing to stop" in completed.stdout
    assert not (tmp_path / "runtime.env").exists()
    assert not (tmp_path / "secrets").exists()


@pytest.mark.parametrize(
    "arguments",
    [
        ("--build", "--data-profile", "smoke"),
        ("--build", "--data-profile", "demo", "--allow-large-data"),
    ],
)
def test_seeded_profile_or_allow_change_fails_before_state_mutation(
    tmp_path: Path, arguments: tuple[str, ...]
) -> None:
    secrets = tmp_path / "persisted-secrets"
    (tmp_path / "runtime.env").write_text(
        "\n".join(
            (
                "COMPOSE_PROJECT_NAME=custometry-test-owned",
                "CUSTOMETRY_BIND_HOST=127.0.0.1",
                "CUSTOMETRY_HTTP_PORT=42319",
                "CUSTOMETRY_VERSION=0.1.0-dev.0",
                "CUSTOMETRY_ENVIRONMENT=development",
                f"CUSTOMETRY_SECRETS_DIR={secrets}",
                "CUSTOMETRY_DATA_PROFILE=demo",
                "CUSTOMETRY_ALLOW_BENCHMARK=0",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_docker = fake_bin / "docker"
    fake_docker.write_text(
        "#!/usr/bin/env bash\n"
        "if [[ \"$1 $2\" == \"compose version\" ]]; then exit 0; fi\n"
        "if [[ \"$1\" == \"info\" ]]; then exit 0; fi\n"
        "if [[ \"$1 $2\" == \"volume inspect\" ]]; then exit 0; fi\n"
        "exit 1\n",
        encoding="utf-8",
    )
    fake_docker.chmod(0o755)

    completed = run_bootstrap(
        tmp_path,
        *arguments,
        path=f"{fake_bin}:{os.environ['PATH']}",
    )

    assert completed.returncode == 2
    assert "differs from persisted data" in completed.stderr
    assert "--reset-demo-data" in completed.stderr
    assert not secrets.exists()
