"""S01 disposable PostgreSQL proof. No shared DB, volume, source checkout or secrets output."""

from __future__ import annotations
import argparse
import os
from pathlib import Path
import secrets
import subprocess
import tempfile
import time
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image", required=True, help="An already available PostgreSQL image identity"
    )
    args = parser.parse_args()
    name = "custometry-ms004-s01-" + uuid4().hex[:12]
    with tempfile.TemporaryDirectory(prefix="ms004-s01-") as directory:
        secret = Path(directory) / "password"
        secret.write_text(secrets.token_urlsafe(32))
        secret.chmod(0o600)
        subprocess.run(
            [
                "docker",
                "run",
                "--detach",
                "--name",
                name,
                "--label",
                "custometry.owner=MS-004-S01",
                "--publish",
                "127.0.0.1::5432",
                "--mount",
                f"type=bind,src={secret},dst=/run/secrets/password,readonly",
                "--env",
                "POSTGRES_PASSWORD_FILE=/run/secrets/password",
                args.image,
            ],
            check=True,
            capture_output=True,
        )
        try:
            for _ in range(60):
                ready = subprocess.run(
                    ["docker", "exec", name, "pg_isready", "-U", "postgres"], capture_output=True
                )
                if ready.returncode == 0:
                    break
                time.sleep(0.5)
            else:
                raise RuntimeError("task-owned PostgreSQL did not become ready")
            port = (
                subprocess.check_output(["docker", "port", name, "5432/tcp"], text=True)
                .strip()
                .rsplit(":", 1)[1]
            )
            env = {**os.environ, "MS004_DATABASE_PORT": port, "MS004_PASSWORD_FILE": str(secret)}
            return subprocess.run(
                [
                    "uv",
                    "run",
                    "--locked",
                    "--package",
                    "custometry-api",
                    "--all-groups",
                    "pytest",
                    "-q",
                    "tests/integration/semantic/test_s01.py",
                ],
                cwd=ROOT,
                env=env,
            ).returncode
        finally:
            subprocess.run(
                ["docker", "rm", "--force", "--volumes", name], check=True, capture_output=True
            )


if __name__ == "__main__":
    raise SystemExit(main())
