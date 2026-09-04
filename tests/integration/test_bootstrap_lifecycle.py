from __future__ import annotations

import os
import stat
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


def test_bootstrap_protects_host_secret_directory_and_allows_non_root_mount_reads(
    tmp_path: Path,
) -> None:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_docker = fake_bin / "docker"
    fake_docker.write_text(
        "#!/usr/bin/env bash\n"
        "if [[ \"$1 $2\" == \"compose version\" ]]; then exit 0; fi\n"
        "if [[ \"$1\" == \"info\" ]]; then exit 0; fi\n"
        "exit 1\n",
        encoding="utf-8",
    )
    fake_docker.chmod(0o755)

    completed = run_bootstrap(
        tmp_path,
        "--build",
        path=f"{fake_bin}:{os.environ['PATH']}",
    )

    assert completed.returncode != 0
    secrets_dir = tmp_path / "secrets"
    assert stat.S_IMODE(secrets_dir.stat().st_mode) == 0o700
    assert {
        path.name: stat.S_IMODE(path.stat().st_mode)
        for path in secrets_dir.iterdir()
    } == {
        "control_db_password": 0o444,
        "demo_source_admin_password": 0o444,
        "demo_source_reader_password": 0o444,
    }
    assert stat.S_IMODE((tmp_path / "runtime.env").stat().st_mode) == 0o600


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


def test_bootstrap_waits_for_tcp_after_temporary_socket_server(tmp_path: Path) -> None:
    """A transient init server must not admit migrations before final startup."""
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_docker = fake_bin / "docker"
    fake_docker.write_text(
        """#!/usr/bin/env python3
import os
import sys
from pathlib import Path

args = sys.argv[1:]
state = Path(os.environ["CUSTOMETRY_RUNTIME_ENV_FILE"]).parent
if "pg_isready" in args:
    count_file = state / "probes"
    count = int(count_file.read_text()) + 1 if count_file.exists() else 1
    count_file.write_text(str(count))
    tcp = "-h" in args and args[args.index("-h") + 1] == "127.0.0.1"
    # During initialization only the socket is ready; it disappears on restart.
    ready = (tcp and count >= 3) or (not tcp and count == 1)
    if ready and tcp:
        (state / "tcp-ready").touch()
    sys.exit(0 if ready else 1)
if "migrate" in args:
    if not (state / "tcp-ready").exists():
        sys.exit(42)
    (state / "migrated").touch()
if "port" in args:
    print("127.0.0.1:42319")
sys.exit(0)
""",
        encoding="utf-8",
    )
    fake_docker.chmod(0o755)
    for command in ("sleep", "curl"):
        stub = fake_bin / command
        stub.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        stub.chmod(0o755)

    completed = run_bootstrap(
        tmp_path, "--build", path=f"{fake_bin}:{os.environ['PATH']}"
    )

    assert completed.returncode == 0, completed.stderr
    assert (tmp_path / "migrated").exists()
    assert int((tmp_path / "probes").read_text()) >= 3
