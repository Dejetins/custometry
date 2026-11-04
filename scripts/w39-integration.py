"""Run focused W39 checks in an isolated, resource-bounded real PostgreSQL."""

from pathlib import Path
import os
import subprocess
import tempfile
import time
import secrets
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
name = "custometry-w39-check-" + uuid4().hex[:10]
with tempfile.TemporaryDirectory(prefix="w39-check-") as temp:
    secret = Path(temp) / "password"
    secret.write_text(secrets.token_urlsafe(32))
    secret.chmod(0o600)
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--name",
            name,
            "--label",
            "custometry.owner=W39",
            "--memory",
            "1g",
            "--cpus",
            "2",
            "--log-opt",
            "max-size=5m",
            "--log-opt",
            "max-file=2",
            "-p",
            "127.0.0.1::5432",
            "--mount",
            f"type=bind,src={secret},dst=/run/secrets/password,readonly",
            "-e",
            "POSTGRES_PASSWORD_FILE=/run/secrets/password",
            "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4",
        ],
        check=True,
        capture_output=True,
    )
    try:
        for _ in range(60):
            if (
                subprocess.run(
                    ["docker", "exec", name, "pg_isready", "-h", "127.0.0.1", "-U", "postgres"],
                    capture_output=True,
                ).returncode
                == 0
            ):
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("OWNED_POSTGRES_UNAVAILABLE")
        port = (
            subprocess.check_output(["docker", "port", name, "5432/tcp"], text=True)
            .strip()
            .rsplit(":", 1)[1]
        )
        env = dict(os.environ)
        for prefix in ("CUSTOMETRY_DATABASE", "CUSTOMETRY_TEST_DATABASE"):
            for k, v in dict(
                HOST="127.0.0.1",
                PORT=port,
                NAME="postgres",
                USER="postgres",
                PASSWORD_FILE=str(secret),
            ).items():
                env[prefix + "_" + k] = v
        if any("presentation" in arg for arg in sys.argv[1:]):
            subprocess.run(
                ["docker", "exec", name, "createdb", "-U", "postgres", "source"], check=True
            )
            for script in ("015_profile.sh", "020_schema.sql", "030_seed.sql"):
                source = ROOT / "deploy/demo-source/init" / script
                command = ["docker", "exec", "-i", name] + (
                    ["bash"]
                    if script.endswith(".sh")
                    else ["psql", "-U", "postgres", "-d", "source", "-v", "ON_ERROR_STOP=1"]
                )
                subprocess.run(command, input=source.read_bytes(), check=True, capture_output=True)
            for k, v in dict(
                HOST="127.0.0.1",
                PORT=port,
                DATABASE="source",
                USER="postgres",
                PASSWORD_FILE=str(secret),
            ).items():
                env["CUSTOMETRY_TEST_SOURCE_" + k] = v
            env["MS004_S03_OWNED_DATABASE"] = "1"
        subprocess.run(
            ["uv", "run", "--locked", "alembic", "-c", "migrations/alembic.ini", "upgrade", "head"],
            cwd=ROOT,
            env=env,
            check=True,
        )
        result = subprocess.run(
            [
                "uv",
                "run",
                "--locked",
                "pytest",
                "-q",
                *(sys.argv[1:] or ["tests/integration/identity_access"]),
            ],
            cwd=ROOT,
            env=env,
        )
        raise SystemExit(result.returncode)
    finally:
        subprocess.run(
            ["docker", "rm", "--force", "--volumes", name], check=True, capture_output=True
        )
