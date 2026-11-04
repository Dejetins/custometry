"""Create an isolated candidate DB from the exact task baseline, then serve it."""

from pathlib import Path
import json
import os
import subprocess
import time
import secrets
import shutil

ROOT = Path(__file__).resolve().parents[1]
runtime = ROOT / ".runtime/w39"
candidate = runtime / "candidate"
candidate.mkdir(exist_ok=True)
# Avoid snapshot IO during measured baseline opens. The clone preserves fixture IDs.
while not (runtime / "baseline-soak-start").exists():
    time.sleep(2)
source = json.loads((runtime / "connection.json").read_text())
name = "custometry-w39-candidate-c67c"
secret = candidate / "password"
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
        "2g",
        "--cpus",
        "4",
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
    raise RuntimeError("CANDIDATE_POSTGRES_UNAVAILABLE")
port = (
    subprocess.check_output(["docker", "port", name, "5432/tcp"], text=True)
    .strip()
    .rsplit(":", 1)[1]
)
original = (runtime / "container").read_text()
with (candidate / "baseline.dump").open("wb") as out:
    subprocess.run(
        ["docker", "exec", original, "pg_dump", "-U", "postgres", "-Fc", "control"],
        stdout=out,
        check=True,
    )
subprocess.run(["docker", "exec", name, "createdb", "-U", "postgres", "control"], check=True)
with (candidate / "baseline.dump").open("rb") as src:
    subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            name,
            "pg_restore",
            "-U",
            "postgres",
            "-d",
            "control",
            "--no-owner",
        ],
        stdin=src,
        check=True,
    )
shutil.copytree(
    Path(source["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).parent / "artifacts",
    candidate / "artifacts",
    dirs_exist_ok=True,
)
env = dict(os.environ)
for prefix in ("CUSTOMETRY_DATABASE", "CUSTOMETRY_TEST_DATABASE"):
    for k, v in dict(
        HOST="127.0.0.1", PORT=port, NAME="control", USER="postgres", PASSWORD_FILE=str(secret)
    ).items():
        env[prefix + "_" + k] = v
extra = {
    "CUSTOMETRY_ANALYTICS_ARTIFACT_ROOT": str(candidate / "artifacts"),
    "CUSTOMETRY_CORS_ALLOWED_ORIGINS": '["http://127.0.0.1:41740","http://localhost:41740"]',
    "CUSTOMETRY_IDENTITY_COOKIE_SECURE": "false",
}
env.update(extra)
connection = {
    k: v
    for k, v in env.items()
    if k.startswith(("CUSTOMETRY_DATABASE", "CUSTOMETRY_TEST_DATABASE"))
} | extra
(candidate / "connection.json").write_text(json.dumps(connection))
(candidate / "connection.json").chmod(0o600)
(candidate / "container").write_text(name)
subprocess.run(
    ["uv", "run", "--locked", "alembic", "-c", "migrations/alembic.ini", "upgrade", "head"],
    cwd=ROOT,
    env=env,
    check=True,
)
(candidate / "ready").write_text("cloned baseline fixture and migrated candidate")
print("Candidate database ready; starting API58140", flush=True)
os.environ.update(env)
os.execvp(
    "uv",
    [
        "uv",
        "run",
        "--locked",
        "uvicorn",
        "custometry_api.main:create_app",
        "--factory",
        "--host",
        "127.0.0.1",
        "--port",
        "58140",
        "--log-level",
        "warning",
        "--no-access-log",
    ],
)
