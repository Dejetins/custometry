"""Disposable production W16 boundary for W32 browser evidence.

The fixture migrates PostgreSQL, publishes a governed Receipt artifact, and
mounts the production analytics FastAPI adapter, service, repository, and local
immutable artifact store. Only token identity and fixture data are test-only.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import psycopg
import pyarrow as pa
import pyarrow.parquet as pq
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Header, HTTPException
from psycopg import Connection
from psycopg.types.json import Jsonb
from testcontainers.postgres import PostgresContainer

from custometry_api.analytics.router import create_analytics_app
from custometry_api.config import Settings
from packages.analytics_core.application.service import AnalyticsService
from packages.analytics_core.domain.model import AnalyticsRequest, Period, TimeComparison
from packages.analytics_core.infrastructure.local import LocalAnalyticsArtifactStore
from packages.analytics_core.infrastructure.postgres import PostgresAnalyticsRepository
from packages.identity_access.domain.policy import Actor


POSTGRES_IMAGE = (
    "postgres:17.5-alpine3.21@"
    "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4"
)
WORKSPACE_ID = UUID("11111111-1111-4111-8111-111111111111")
OWNER_ID = UUID("22222222-2222-4222-8222-222222222222")
OUTSIDER_ID = UUID("33333333-3333-4333-8333-333333333333")
CONNECTION_ID = UUID("44444444-4444-4444-8444-444444444444")
SOURCE_SYSTEM_ID = UUID("55555555-5555-4555-8555-555555555555")
BATCH_ID = UUID("66666666-6666-4666-8666-666666666666")
ARTIFACT_ID = UUID("77777777-7777-4777-8777-777777777777")
QUALITY_ID = UUID("88888888-8888-4888-8888-888888888888")
SEMANTIC_DATASET_ID = UUID("99999999-9999-4999-8999-999999999999")
SEMANTIC_VERSION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
CALENDAR_VERSION_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")


class TokenIdentity:
    def __init__(self) -> None:
        self.actors = {
            "owner": Actor(
                OWNER_ID,
                WORKSPACE_ID,
                "owner@example.invalid",
                frozenset({"analysis.read", "analysis.run", "analysis.manage", "export.create"}),
            ),
            "viewer": Actor(
                OWNER_ID,
                WORKSPACE_ID,
                "viewer@example.invalid",
                frozenset({"analysis.read"}),
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


def publish_fixture(connect: Callable[[], Connection[Any]], artifact_root: Path) -> None:
    receipt_path = artifact_root / "semantic" / "receipt.parquet"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {"receipt_id": "r-2024-1", "receipt_datetime": datetime(2024, 3, 1, 10, tzinfo=UTC), "customer_id": "c-1", "gross_amount": "100", "net_amount": "90", "discount_amount": "10", "store_id": "store-1", "channel_id": "web", "currency": "RUB", "status": "completed"},
        {"receipt_id": "r-2024-2", "receipt_datetime": datetime(2024, 8, 1, 11, tzinfo=UTC), "customer_id": "c-2", "gross_amount": "200", "net_amount": "180", "discount_amount": "20", "store_id": "store-2", "channel_id": "retail", "currency": "RUB", "status": "completed"},
        {"receipt_id": "r-2025-1", "receipt_datetime": datetime(2025, 3, 1, 10, tzinfo=UTC), "customer_id": "c-1", "gross_amount": "160", "net_amount": "145", "discount_amount": "15", "store_id": "store-1", "channel_id": "web", "currency": "RUB", "status": "completed"},
        {"receipt_id": "r-2025-2", "receipt_datetime": datetime(2025, 8, 1, 11, tzinfo=UTC), "customer_id": "c-3", "gross_amount": "320", "net_amount": "280", "discount_amount": "40", "store_id": "store-2", "channel_id": "retail", "currency": "RUB", "status": "completed"},
    ]
    pq.write_table(pa.Table.from_pylist(rows), receipt_path)
    content_hash = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    with connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO identity_workspaces (id, key, name) VALUES (%s, %s, %s)",
            (WORKSPACE_ID, "northwind-retail", "Northwind Retail"),
        )
        cursor.execute(
            "INSERT INTO identity_principals (id, email, password_hash) VALUES (%s, %s, %s), (%s, %s, %s)",
            (OWNER_ID, "owner@example.invalid", "fixture", OUTSIDER_ID, "outsider@example.invalid", "fixture"),
        )
        cursor.execute(
            """INSERT INTO source_connections
               (id, workspace_id, source_system_id, connector_id, profile_ref, secret_ref,
                display_name, status, created_by)
               VALUES (%s, %s, %s, 'postgresql', 'fixture-profile', 'fixture-secret',
                       'W32 governed sales', 'active', %s)""",
            (CONNECTION_ID, WORKSPACE_ID, SOURCE_SYSTEM_ID, OWNER_ID),
        )
        cursor.execute(
            """INSERT INTO ingestion_batches
               (id, workspace_id, connection_id, source_system_id, semantic_dataset_id,
                idempotency_key, state, consistency_mode)
               VALUES (%s, %s, %s, %s, %s, 'w32-real-boundary', 'committed', 'repeatable_read')""",
            (BATCH_ID, WORKSPACE_ID, CONNECTION_ID, SOURCE_SYSTEM_ID, SEMANTIC_DATASET_ID),
        )
        cursor.execute(
            """INSERT INTO artifact_manifests
               (id, workspace_id, producer_batch_id, artifact_type, entity, relative_uri,
                content_hash, row_count, byte_size, schema_json, pii_class, state)
               VALUES (%s, %s, %s, 'semantic_entity', 'Receipt', 'semantic/receipt.parquet',
                       %s, %s, %s, %s, 'internal', 'committed')""",
            (ARTIFACT_ID, WORKSPACE_ID, BATCH_ID, content_hash, len(rows), receipt_path.stat().st_size, Jsonb({"fields": list(rows[0])})),
        )
        cursor.execute(
            """INSERT INTO data_quality_reports
               (id, workspace_id, batch_id, decision, rule_versions, violations,
                applied_waiver_ids, evaluated_at)
               VALUES (%s, %s, %s, 'passed', %s, %s, %s, %s)""",
            (QUALITY_ID, WORKSPACE_ID, BATCH_ID, Jsonb({"receipt": "v1"}), Jsonb([]), Jsonb([]), datetime.now(UTC)),
        )
        cursor.execute(
            """INSERT INTO semantic_dataset_versions
               (id, semantic_dataset_id, workspace_id, version, status, quality_report_id,
                bindings, capability_matrix, impact_summary, request_hash)
               VALUES (%s, %s, %s, 1, 'published', %s, %s, %s, %s, %s)""",
            (
                SEMANTIC_VERSION_ID,
                SEMANTIC_DATASET_ID,
                WORKSPACE_ID,
                QUALITY_ID,
                Jsonb([{"entity": "Receipt", "artifact_id": str(ARTIFACT_ID)}]),
                Jsonb({"sales": "available", "discount_analytics": "total_only", "pvm": "unavailable"}),
                Jsonb({"fixture": "W32 governed projection"}),
                "c" * 64,
            ),
        )


def fixture_app(connect: Callable[[], Connection[Any]], artifact_root: Path) -> FastAPI:
    identity = TokenIdentity()
    repository = PostgresAnalyticsRepository(connect)
    store = LocalAnalyticsArtifactStore(artifact_root)
    analytics = AnalyticsService(
        projections=repository,
        artifacts=store,
        results=repository,
        result_store=store,
    )
    def seed_result() -> None:
        analytics.run(
            workspace_id=WORKSPACE_ID,
            principal_id=OWNER_ID,
            permissions=frozenset({"analysis.read", "analysis.run"}),
            request=AnalyticsRequest(
                result_type="sales",
                semantic_dataset_version_id=SEMANTIC_VERSION_ID,
                comparison=TimeComparison(
                    mode="previous_year_calendar_aligned",
                    current_period=Period(date(2025, 1, 1), date(2025, 12, 31)),
                    comparison_period=Period(date(2024, 1, 1), date(2024, 12, 31)),
                    timezone="UTC",
                    calendar_version_id=CALENDAR_VERSION_ID,
                    incomplete_period_policy="explicit_partial",
                    leap_day_policy="calendar_map",
                    iso_week_53_policy="explicit_partial",
                    definition_compatibility_policy="require_same_versions",
                ),
            ),
        )

    seed_result()
    application = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    application.mount(
        "/analytics",
        create_analytics_app(
            Settings(database_password_file=Path("/not-read"), analytics_artifact_root=artifact_root),
            identity_service=identity,  # type: ignore[arg-type]
            analytics_service=analytics,
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

    @application.get("/health/ready")
    def ready() -> dict[str, str]:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return {"status": "ready", "version": "w32-real-w16-fixture"}

    @application.get("/identity/me")
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

    @application.post("/__fixture__/reset")
    def reset() -> dict[str, str]:
        with connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute("DELETE FROM analytics_results")
        seed_result()
        return {"status": "reset"}

    return application


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    secret = "w32-disposable-postgres-only"
    with tempfile.TemporaryDirectory(prefix="custometry-w32-") as temporary:
        temporary_path = Path(temporary)
        password_file = temporary_path / "postgres-password"
        password_file.write_text(secret, encoding="utf-8")
        with PostgresContainer(
            image=POSTGRES_IMAGE,
            username="custometry",
            password=secret,
            dbname="custometry",
        ) as postgres_container:
            host = postgres_container.get_container_host_ip()
            port = int(postgres_container.get_exposed_port(5432))

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
            artifact_root = (temporary_path / "artifacts").resolve()
            publish_fixture(connect, artifact_root)
            uvicorn.run(fixture_app(connect, artifact_root), host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
