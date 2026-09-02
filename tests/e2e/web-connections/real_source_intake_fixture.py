"""Disposable real W14 boundary for W33 browser evidence.

Production FastAPI, ConnectionService, PostgreSQL persistence, authorization,
redaction, connector test, and discovery execute unchanged. The token identity,
safe persistence probe, and container lifecycle are fixture-only.
"""

from __future__ import annotations

import argparse
import os
import secrets
import tempfile
from pathlib import Path
from uuid import UUID

import psycopg
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Header, HTTPException
from testcontainers.postgres import PostgresContainer

from custometry_api.config import Settings
from custometry_api.connections.router import create_connection_app
from packages.identity_access.domain.policy import Actor


POSTGRES_IMAGE = (
    "postgres:17.5-alpine3.21@"
    "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4"
)
WORKSPACE_ID = UUID("11111111-1111-4111-8111-111111111111")
OWNER_ID = UUID("22222222-2222-4222-8222-222222222222")
OUTSIDER_ID = UUID("33333333-3333-4333-8333-333333333333")


class TokenIdentity:
    def __init__(self) -> None:
        self.actors = {
            "owner": Actor(
                OWNER_ID,
                WORKSPACE_ID,
                "owner@example.invalid",
                frozenset(
                    {
                        "connection.read_metadata",
                        "connection.manage",
                        "connection.secret.rotate",
                    }
                ),
            ),
            "no-permission": Actor(
                OUTSIDER_ID,
                WORKSPACE_ID,
                "outsider@example.invalid",
                frozenset(),
            ),
        }

    def authenticate(self, token: str) -> Actor:
        try:
            return self.actors[token]
        except KeyError as error:
            raise RuntimeError("unknown fixture token") from error


def migrate(host: str, port: int, password_file: Path) -> None:
    names = {
        "CUSTOMETRY_DATABASE_HOST": host,
        "CUSTOMETRY_DATABASE_PORT": str(port),
        "CUSTOMETRY_DATABASE_NAME": "custometry",
        "CUSTOMETRY_DATABASE_USER": "custometry",
        "CUSTOMETRY_DATABASE_PASSWORD_FILE": str(password_file),
    }
    previous = {name: os.environ.get(name) for name in names}
    os.environ.update(names)
    try:
        command.upgrade(Config("migrations/alembic.ini"), "head")
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def fixture_app(settings: Settings) -> FastAPI:
    identity = TokenIdentity()
    application = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    application.mount(
        "/connections",
        create_connection_app(settings, identity_service=identity),  # type: ignore[arg-type]
    )

    def actor(authorization: str | None) -> Actor:
        if authorization is None:
            raise HTTPException(status_code=401)
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer":
            raise HTTPException(status_code=401)
        try:
            return identity.authenticate(token)
        except RuntimeError as error:
            raise HTTPException(status_code=401) from error

    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=3,
        )

    @application.get("/health/ready")
    def ready() -> dict[str, str]:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return {"status": "ready", "version": "w33-real-w14-fixture"}

    @application.get("/identity/me")
    def me(authorization: str | None = Header(default=None)) -> dict[str, object]:
        current = actor(authorization)
        return {
            "principal_id": str(current.principal_id),
            "workspace_id": str(current.workspace_id),
            "email": current.email,
            "permissions": sorted(current.permissions),
            "installation_admin": False,
            "token_kind": "fixture",
        }

    @application.get("/__fixture__/proof/{connection_id}")
    def proof(connection_id: UUID) -> dict[str, object]:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, workspace_id, connector_id, display_name, status,
                       profile_ref IS NOT NULL, secret_ref IS NOT NULL
                FROM source_connections WHERE id = %s
                """,
                (connection_id,),
            )
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(status_code=404)
            cursor.execute(
                "SELECT count(*) FROM source_intake_audit_events WHERE resource_id = %s",
                (str(connection_id),),
            )
            audit_count = int(cursor.fetchone()[0])
        return {
            "connection_id": str(row[0]),
            "workspace_id": str(row[1]),
            "connector_id": str(row[2]),
            "display_name": str(row[3]),
            "status": str(row[4]),
            "profile_reference_persisted": bool(row[5]),
            "secret_reference_persisted": bool(row[6]),
            "audit_count": audit_count,
            "raw_references_exposed": False,
        }

    _ = (ready, me, proof)
    return application


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    control_secret = secrets.token_urlsafe(24)
    source_secret = secrets.token_urlsafe(24)
    with tempfile.TemporaryDirectory(prefix="custometry-w33-") as temporary:
        temporary_path = Path(temporary)
        control_file = temporary_path / "control-password"
        source_file = temporary_path / "source-password"
        control_file.write_text(control_secret, encoding="utf-8")
        source_file.write_text(source_secret, encoding="utf-8")
        with (
            PostgresContainer(
                image=POSTGRES_IMAGE,
                username="custometry",
                password=control_secret,
                dbname="custometry",
            ) as control,
            PostgresContainer(
                image=POSTGRES_IMAGE,
                username="custometry",
                password=source_secret,
                dbname="northwind_retail",
            ) as source,
        ):
            control_host = control.get_container_host_ip()
            control_port = int(control.get_exposed_port(5432))
            source_host = source.get_container_host_ip()
            source_port = int(source.get_exposed_port(5432))
            migrate(control_host, control_port, control_file)
            with (
                psycopg.connect(
                    host=control_host,
                    port=control_port,
                    dbname="custometry",
                    user="custometry",
                    password=control_secret,
                ) as connection,
                connection.transaction(),
                connection.cursor() as cursor,
            ):
                cursor.execute(
                    "INSERT INTO identity_workspaces (id, key, name, active) VALUES (%s, 'northwind-retail', 'Northwind Retail', true)",
                    (WORKSPACE_ID,),
                )
                for principal_id, label in ((OWNER_ID, "owner"), (OUTSIDER_ID, "outsider")):
                    cursor.execute(
                        "INSERT INTO identity_principals (id, email, password_hash, installation_admin, active) VALUES (%s, %s, 'fixture-only', false, true)",
                        (principal_id, f"{label}@example.invalid"),
                    )
            with (
                psycopg.connect(
                    host=source_host,
                    port=source_port,
                    dbname="northwind_retail",
                    user="custometry",
                    password=source_secret,
                ) as connection,
                connection.transaction(),
                connection.cursor() as cursor,
            ):
                cursor.execute("CREATE SCHEMA retail")
                cursor.execute(
                    "CREATE TABLE retail.receipts (receipt_id bigint PRIMARY KEY, net_amount numeric(12,2), status text)"
                )
                cursor.execute(
                    "INSERT INTO retail.receipts VALUES (1, 125.50, 'completed'), (2, 89.00, 'returned')"
                )
                cursor.execute(
                    "CREATE TABLE retail.customers (customer_id bigint PRIMARY KEY, email text, loyalty_card text)"
                )
                cursor.execute(
                    "INSERT INTO retail.customers VALUES (1, 'redacted@example.invalid', 'card-redacted')"
                )
            settings = Settings(
                environment="test",
                version="w33-real-w14-fixture",
                database_host=control_host,
                database_port=control_port,
                database_name="custometry",
                database_user="custometry",
                database_password_file=control_file,
                source_postgresql_host=source_host,
                source_postgresql_port=source_port,
                source_postgresql_database="northwind_retail",
                source_postgresql_user="custometry",
                source_postgresql_password_file=source_file,
                identity_cookie_secure=False,
            )
            uvicorn.run(
                fixture_app(settings), host="127.0.0.1", port=args.port, log_level="warning"
            )


if __name__ == "__main__":
    main()
