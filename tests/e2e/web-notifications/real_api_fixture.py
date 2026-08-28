"""Disposable W37 PostgreSQL/API boundary for W35 browser evidence.

This fixture is test-only. It mounts the production Notifications FastAPI adapter
and store unchanged, while providing deterministic Identity/access ports and
explicit reset/revoke controls outside the product API namespace.
"""

from __future__ import annotations

import argparse
import os
import tempfile
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import psycopg
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Header, HTTPException
from psycopg import Connection
from testcontainers.postgres import PostgresContainer

from custometry_api.config import Settings
from custometry_api.notifications.router import create_notifications_app
from packages.contracts.notifications import (
    DeepLinkDescriptor,
    NotificationActor,
    NotificationEvent,
    NotificationFailure,
    RecipientCandidate,
)
from packages.identity_access.domain.policy import Actor
from packages.notifications.application.service import NotificationInboxService
from packages.notifications.infrastructure.postgres import PostgresNotificationStore


POSTGRES_IMAGE = (
    "postgres:17.5-alpine3.21@"
    "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4"
)
WORKSPACE_ID = UUID("11111111-1111-4111-8111-111111111111")
ACKNOWLEDGER_ID = UUID("22222222-2222-4222-8222-222222222222")
READER_ID = UUID("33333333-3333-4333-8333-333333333333")
OUTSIDER_ID = UUID("44444444-4444-4444-8444-444444444444")


class TokenIdentity:
    def __init__(self) -> None:
        self.actors = {
            "acknowledger": Actor(
                ACKNOWLEDGER_ID,
                WORKSPACE_ID,
                "acknowledger@example.invalid",
                frozenset({"notification.read", "notification.acknowledge", "run.read"}),
            ),
            "reader": Actor(
                READER_ID,
                WORKSPACE_ID,
                "reader@example.invalid",
                frozenset({"notification.read", "run.read"}),
            ),
            "no-permission": Actor(
                OUTSIDER_ID,
                WORKSPACE_ID,
                "outsider@example.invalid",
                frozenset({"run.read"}),
            ),
        }

    def authenticate(self, raw_token: str) -> Actor:
        actor = self.actors.get(raw_token)
        if actor is None:
            raise RuntimeError("unknown fixture token")
        return actor


class DynamicAccess:
    def __init__(self) -> None:
        self.resource_grants: set[tuple[UUID, UUID, str, str]] = set()

    def require(self, actor: NotificationActor, action: str) -> None:
        if action not in actor.permissions:
            raise NotificationFailure("FORBIDDEN")

    def can_access(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
    ) -> bool:
        return (
            actor.principal_id,
            workspace_id,
            resource_type,
            resource_id,
        ) in self.resource_grants

    def can_disclose_deep_link(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
        deep_link: DeepLinkDescriptor,
    ) -> bool:
        del deep_link
        return self.can_access(
            actor,
            workspace_id=workspace_id,
            resource_type=resource_type,
            resource_id=resource_id,
        )


class Recipients:
    def eligible_recipients(self, event: NotificationEvent) -> tuple[RecipientCandidate, ...]:
        del event
        return (
            RecipientCandidate(ACKNOWLEDGER_ID, "w35-policy-v1", "preferences:run:v1"),
            RecipientCandidate(READER_ID, "w35-policy-v1", "preferences:run:v1"),
        )


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


def fixture_app(connect: Callable[[], Connection[Any]]) -> FastAPI:
    identity = TokenIdentity()
    access = DynamicAccess()
    service = NotificationInboxService(
        PostgresNotificationStore(connect),
        access,
        recipients=Recipients(),
    )
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.mount(
        "/notifications",
        create_notifications_app(
            Settings(version="w35-real-w37-fixture"),
            identity_service=identity,  # type: ignore[arg-type]
            notification_service=service,
        ),
    )

    def actor_from_header(authorization: str | None) -> Actor:
        if authorization is None:
            raise HTTPException(status_code=401)
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer":
            raise HTTPException(status_code=401)
        try:
            return identity.authenticate(token)
        except RuntimeError as error:
            raise HTTPException(status_code=401) from error

    def reset_data() -> dict[str, int]:
        with connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute("DELETE FROM notification_audit_outbox")
            cursor.execute("DELETE FROM notification_idempotency")
            cursor.execute("DELETE FROM notification_item_events")
            cursor.execute("DELETE FROM notification_inbox_items")
            cursor.execute("DELETE FROM notification_source_events")
        access.resource_grants.clear()
        now = datetime.now(UTC)
        definitions = (
            ("run-critical", "critical", "RUN_FAILED", now - timedelta(minutes=6), False),
            ("run-critical", "critical", "RUN_STUCK", now - timedelta(minutes=5), False),
            ("run-warning", "warning", "RUN_STUCK", now - timedelta(minutes=4), False),
            ("run-recovered", "info", "RUN_RECOVERED", now - timedelta(minutes=3), True),
        )
        projected = 0
        for resource_id, severity, code, occurred_at, resolved in definitions:
            event = NotificationEvent(
                event_id=uuid4(),
                source_owner="execution",
                source_type="execution.run.terminal.v1",
                source_version=1,
                workspace_id=WORKSPACE_ID,
                resource_type="run",
                resource_id=resource_id,
                severity=severity,  # type: ignore[arg-type]
                category="run",
                occurred_at=occurred_at,
                message_code=code,
                message_parameters=(("state_code", code),),
                group_key=f"run:{resource_id}",
                deep_link=DeepLinkDescriptor("UI-OPS-002", (("run_id", resource_id),)),
                trace_id=f"trace-{resource_id}",
                resolved=resolved,
            )
            outcome = service.project_event(event)
            projected += outcome.projected_recipients
            for principal_id in (ACKNOWLEDGER_ID, READER_ID):
                access.resource_grants.add(
                    (principal_id, WORKSPACE_ID, "run", resource_id)
                )
        with connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                "UPDATE notification_inbox_items SET freshness = 'stale' WHERE resource_id = %s",
                ("run-warning",),
            )
        return {"projected": projected}

    @app.get("/health/ready")
    def ready() -> dict[str, str]:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return {"status": "ready", "version": "w35-real-w37-fixture"}

    @app.get("/identity/me")
    def me(authorization: str | None = Header(default=None)) -> dict[str, object]:
        actor = actor_from_header(authorization)
        return {
            "principal_id": str(actor.principal_id),
            "workspace_id": str(actor.workspace_id),
            "email": actor.email,
            "permissions": sorted(actor.permissions),
            "installation_admin": False,
            "token_kind": "fixture",
        }

    @app.post("/__fixture__/reset")
    def reset() -> dict[str, int]:
        return reset_data()

    @app.post("/__fixture__/revoke")
    def revoke() -> dict[str, bool]:
        access.resource_grants.clear()
        return {"revoked": True}

    reset_data()
    return app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    secret = "w35-disposable-postgres-only"
    with tempfile.TemporaryDirectory(prefix="custometry-w35-") as temporary:
        password_file = Path(temporary) / "postgres-password"
        password_file.write_text(secret, encoding="utf-8")
        with PostgresContainer(
            image=POSTGRES_IMAGE,
            username="custometry",
            password=secret,
            dbname="custometry",
        ) as container:
            host = container.get_container_host_ip()
            port = int(container.get_exposed_port(5432))

            def connect() -> Connection[Any]:
                return psycopg.connect(
                    host=host,
                    port=port,
                    dbname="custometry",
                    user="custometry",
                    password=secret,
                    connect_timeout=3,
                )

            migrate(host, port, password_file)
            uvicorn.run(fixture_app(connect), host="127.0.0.1", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
