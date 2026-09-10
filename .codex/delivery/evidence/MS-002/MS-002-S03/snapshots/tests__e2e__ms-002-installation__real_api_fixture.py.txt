"""Owned loopback test lifecycle: production API, migrated PostgreSQL, real faults."""
from __future__ import annotations

import os
import secrets
import tempfile
import threading
from pathlib import Path

import psycopg
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from testcontainers.postgres import PostgresContainer  # pyright: ignore[reportMissingTypeStubs]

from custometry_api.config import Settings
from custometry_api.main import create_app

IMAGE = "postgres:17.5-alpine3.21@sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4"


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="custometry-s03-") as temporary:
        root = Path(temporary).resolve()
        password = secrets.token_hex(32)
        password_file = root / "password"
        password_file.write_text(password)
        password_file.chmod(0o600)
        storage = root / "artifacts"
        storage.mkdir()
        with PostgresContainer(IMAGE, username="custometry", password=password, dbname="custometry") as database:
            os.environ.update({
                "CUSTOMETRY_DATABASE_HOST": database.get_container_host_ip(),
                "CUSTOMETRY_DATABASE_PORT": str(database.get_exposed_port(5432)),
                "CUSTOMETRY_DATABASE_PASSWORD_FILE": str(password_file),
                "CUSTOMETRY_ANALYTICS_ARTIFACT_ROOT": str(storage),
            })
            command.upgrade(Config("migrations/alembic.ini"), "head")
            settings = Settings()
            app = create_app(settings=settings)
            server: uvicorn.Server | None = None
            thread: threading.Thread | None = None

            def start_api() -> None:
                nonlocal server, thread
                server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="critical", access_log=False))
                thread = threading.Thread(target=server.run)
                thread.start()

            def stop_api() -> None:
                if server:
                    server.should_exit = True
                if thread:
                    thread.join(timeout=10)

            control = FastAPI()

            def health() -> dict[str, str]:
                return {"status": "ok"}

            def fault(mode: str) -> dict[str, str]:
                if mode == "api-stop":
                    stop_api()
                elif mode == "api-start":
                    start_api()
                elif mode == "database-stop":
                    database.get_wrapped_container().stop(timeout=2)
                elif mode == "database-start":
                    database.get_wrapped_container().start()
                    # Docker reallocates an ephemeral host port after restart.
                    settings.database_port = int(database.get_exposed_port(5432))
                elif mode == "storage-stop":
                    storage.rename(root / "retained-artifacts")
                elif mode == "storage-start":
                    (root / "retained-artifacts").rename(storage)
                elif mode in ("schema-stop", "schema-start"):
                    with psycopg.connect(host=settings.database_host, port=settings.database_port, dbname=settings.database_name, user=settings.database_user, password=password) as conn:
                        conn.execute("UPDATE alembic_version SET version_num = %s", ("unsupported-test-head" if mode == "schema-stop" else "0009_notifications",))
                else:
                    return {"status": "unsupported"}
                return {"status": "ok"}

            control.add_api_route("/health", health, methods=["GET"])
            control.add_api_route("/fault/{mode}", fault, methods=["POST"])
            start_api()
            try:
                uvicorn.run(control, host="127.0.0.1", port=8001, log_level="critical", access_log=False)
            finally:
                stop_api()


if __name__ == "__main__":
    main()
