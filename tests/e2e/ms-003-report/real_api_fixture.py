"""Production API and S01 data, with a separate real analyst for browser proof."""

from __future__ import annotations
import json
import os
import secrets
import subprocess
import sys
import socket
import signal
from types import FrameType
from urllib.request import urlopen
from pathlib import Path
from uuid import UUID, uuid4
import psycopg
import uvicorn
from fastapi import FastAPI, HTTPException
from apps.worker_data.prepare_retail_report import prepare
from custometry_api.config import Settings
from custometry_api.identity.router import create_identity_service
from tools.custometry_quality import development_runtime as runtime

ROOT = Path(__file__).resolve().parents[3]
PORT = 58104
CONTROL = 58105


def main() -> None:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", PORT))
    policy = runtime.load_policy(ROOT)
    paths = runtime.runtime_paths(ROOT, policy)
    prepared = prepare(ROOT)
    env = {
        **os.environ,
        **runtime.host_environment(paths, policy, "api"),
        "CUSTOMETRY_CORS_ALLOWED_ORIGINS": '["http://127.0.0.1:41734"]',
    }
    settings = Settings.model_validate(
        {
            k.removeprefix("CUSTOMETRY_").lower(): v
            for k, v in env.items()
            if k.startswith("CUSTOMETRY_") and k != "CUSTOMETRY_CORS_ALLOWED_ORIGINS"
        }
    )
    identity = create_identity_service(settings)
    secret = json.loads((paths.secrets_dir / "retail-report.json").read_text())
    tokens = identity.login(
        email=secret["admin_email"],
        password=secret["admin_password"],
        workspace_id=UUID(prepared["workspace_id"]),
        device_label="S04-fixture-admin",
    )
    admin = identity.authenticate(tokens.access_token)
    label = uuid4().hex[:12]
    email = f"s04-{label}@example.invalid"
    password = secrets.token_urlsafe(32)
    invitation = identity.invite(
        admin, workspace_id=admin.workspace_id, email=email, roles=["analyst"], expires_in_hours=24
    )
    principal = identity.accept_invitation(token=invitation.token, password=password)
    identity.logout(tokens.refresh_token, tokens.csrf_token)
    private = paths.runtime_dir / "ms003-s04-browser.json"
    private.write_text(
        json.dumps({"workspace": prepared["workspace_id"], "email": email, "password": password})
    )
    private.chmod(0o600)
    process: subprocess.Popen[bytes] | None = None
    held: dict[Path, bytes] = {}

    def start() -> None:
        nonlocal process
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "custometry_api.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(PORT),
                "--log-level",
                "error",
                "--no-access-log",
            ],
            cwd=ROOT,
            env=env,
        )

    def stop() -> None:
        if process is not None:
            process.terminate()
            process.wait(timeout=15)

    control = FastAPI()

    @control.get("/health")
    def health() -> dict[str, str]:
        if process is None or process.poll() is not None:
            raise HTTPException(503)
        try:
            with urlopen(f"http://127.0.0.1:{PORT}/health/ready", timeout=1) as response:
                if response.status != 200:
                    raise HTTPException(503)
        except OSError as exc:
            raise HTTPException(503) from exc
        return {"status": "ready"}

    @control.post("/restart")
    def restart() -> dict[str, str]:
        stop()
        start()
        return {"status": "restarting"}

    @control.post("/artifact/{snapshot}/{mode}")
    def artifact(snapshot: UUID, mode: str) -> dict[str, str]:
        # Faults can touch only this run's newly created analyst snapshots.
        with psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
        ) as conn:
            found = conn.execute(
                "SELECT 1 FROM presentation_versions v JOIN presentation_documents d ON d.id=v.document_id WHERE d.owner_principal_id=%s AND v.payload->>'snapshot_id'=%s",
                (principal, str(snapshot)),
            ).fetchone()
        if not found:
            raise HTTPException(403)
        path = paths.runtime_dir / "artifacts" / "objects" / f"{snapshot}.json"
        if mode in ("missing", "storage"):
            held[path] = path.read_bytes()
            path.unlink()
            if mode == "storage":
                path.mkdir()
        elif mode == "restore" and path in held:
            if path.is_dir():
                path.rmdir()
            path.write_bytes(held.pop(path))
        else:
            raise HTTPException(400)
        return {"status": "ok"}

    @control.post("/expire")
    def expire() -> dict[str, str]:
        # Only sessions of this run's newly created analyst may be expired.
        with psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
        ) as conn:
            conn.execute(
                "UPDATE identity_sessions SET access_expires_at=now()-interval '1 second' WHERE principal_id=%s AND revoked_at IS NULL",
                (principal,),
            )
        return {"status": "ok"}

    _ = health, restart, artifact, expire
    def terminate(_signum: int, _frame: FrameType | None) -> None:
        # Uvicorn re-raises SIGTERM after graceful shutdown. Unwind this fixture's
        # finally block instead of letting the OS skip artifact/secret cleanup.
        raise SystemExit(0)

    previous_term = signal.signal(signal.SIGTERM, terminate)
    start()
    try:
        uvicorn.run(control, host="127.0.0.1", port=CONTROL, log_level="error", access_log=False)
    finally:
        stop()
        for path, raw in held.items():
            if path.is_dir():
                path.rmdir()
            path.write_bytes(raw)
        private.unlink(missing_ok=True)
        signal.signal(signal.SIGTERM, previous_term)


if __name__ == "__main__":
    main()
