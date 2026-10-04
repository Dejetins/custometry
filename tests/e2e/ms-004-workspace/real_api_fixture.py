"""Task-owned disposable source/control databases; never target an existing database."""

from __future__ import annotations
import argparse
import signal
from types import FrameType
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
        "--image",
        default=os.environ.get(
            "MS004_POSTGRES_IMAGE",
            "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4",
        ),
    )
    args = parser.parse_args()

    def terminate(signum: int, frame: FrameType | None) -> None:
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, terminate)
    name = "custometry-ms004-s04-" + uuid4().hex[:12]
    with tempfile.TemporaryDirectory(prefix="ms004-s04-") as directory:
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
                "custometry.owner=MS-004-S04",
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
                raise RuntimeError("isolated PostgreSQL unavailable")
            port = (
                subprocess.check_output(["docker", "port", name, "5432/tcp"], text=True)
                .strip()
                .rsplit(":", 1)[1]
            )
            for db in ("control", "source"):
                subprocess.run(
                    ["docker", "exec", name, "createdb", "-U", "postgres", db],
                    check=True,
                    capture_output=True,
                )
            for script in ("015_profile.sh", "020_schema.sql", "030_seed.sql"):
                source = ROOT / "deploy/demo-source/init" / script
                command = ["docker", "exec", "-i", name]
                command += (
                    ["bash"]
                    if script.endswith(".sh")
                    else ["psql", "-U", "postgres", "-d", "source", "-v", "ON_ERROR_STOP=1"]
                )
                subprocess.run(command, input=source.read_bytes(), check=True, capture_output=True)
            env = dict(os.environ)
            for prefix, db in (
                ("CUSTOMETRY_DATABASE", "control"),
                ("CUSTOMETRY_TEST_DATABASE", "control"),
                ("CUSTOMETRY_TEST_SOURCE", "source"),
            ):
                env.update(
                    {
                        prefix + "_HOST": "127.0.0.1",
                        prefix + "_PORT": port,
                        prefix + "_USER": "postgres",
                        prefix + "_PASSWORD_FILE": str(secret),
                    }
                )
                env[prefix + ("_DATABASE" if prefix.endswith("SOURCE") else "_NAME")] = db
            env["MS004_S04_OWNED_DATABASE"] = "1"
            subprocess.run(
                [
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
                ],
                cwd=ROOT,
                env=env,
                check=True,
            )
            env["CUSTOMETRY_CORS_ALLOWED_ORIGINS"] = '["http://127.0.0.1:41744"]'
            env["CUSTOMETRY_IDENTITY_COOKIE_SECURE"] = "false"
            os.environ.update(env)
            from scenario import create_scenario
            import uvicorn

            app = create_scenario(Path(directory) / "artifacts")
            uvicorn.run(app, host="127.0.0.1", port=58144, log_level="error", access_log=False)
            return 0
        finally:
            subprocess.run(
                ["docker", "rm", "--force", "--volumes", name], check=True, capture_output=True
            )


if __name__ == "__main__":
    raise SystemExit(main())
