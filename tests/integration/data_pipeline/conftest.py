from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import psycopg
import pytest
from psycopg import Connection

from plugins.connector_postgresql.adapter import PostgreSQLConnector, PostgreSQLTarget


@dataclass(frozen=True, slots=True)
class DataPipelineRuntime:
    connect: Callable[[], Connection[Any]]
    connector: PostgreSQLConnector
    workspace_id: UUID
    actor_id: UUID

    def create_connection(self, source_system_id: UUID) -> UUID:
        connection_id = uuid4()
        with self.connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO source_connections
                  (id, workspace_id, source_system_id, connector_id, profile_ref,
                   secret_ref, display_name, status, created_by)
                VALUES (%s, %s, %s, 'postgresql', 'retail_demo',
                        'retail_demo_reader', %s, 'active', %s)
                """,
                (
                    connection_id,
                    self.workspace_id,
                    source_system_id,
                    f"Retail {connection_id}",
                    self.actor_id,
                ),
            )
        return connection_id


def _secret(variable: str) -> str:
    value = os.environ.get(variable)
    if value is None:
        pytest.skip(f"{variable} is required for the real PostgreSQL boundary")
    return Path(value).read_text(encoding="utf-8").strip()


@pytest.fixture
def data_pipeline_runtime() -> Iterator[DataPipelineRuntime]:
    control_password = _secret("CUSTOMETRY_TEST_DATABASE_PASSWORD_FILE")
    source_password = _secret("CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE")

    def connect() -> Connection[Any]:
        return psycopg.connect(
            host=os.environ.get("CUSTOMETRY_TEST_DATABASE_HOST", "127.0.0.1"),
            port=int(os.environ.get("CUSTOMETRY_TEST_DATABASE_PORT", "55432")),
            dbname=os.environ.get("CUSTOMETRY_TEST_DATABASE_NAME", "custometry"),
            user=os.environ.get("CUSTOMETRY_TEST_DATABASE_USER", "custometry"),
            password=control_password,
            connect_timeout=3,
        )

    connector = PostgreSQLConnector(
        PostgreSQLTarget(
            host=os.environ.get("CUSTOMETRY_TEST_SOURCE_HOST", "127.0.0.1"),
            port=int(os.environ.get("CUSTOMETRY_TEST_SOURCE_PORT", "55433")),
            dbname=os.environ.get("CUSTOMETRY_TEST_SOURCE_DATABASE", "northwind_retail"),
            user=os.environ.get("CUSTOMETRY_TEST_SOURCE_USER", "demo_reader"),
            password=source_password,
        )
    )
    workspace_id = uuid4()
    actor_id = uuid4()
    with connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            """
            TRUNCATE TABLE
              data_pipeline_outbox, semantic_dataset_versions, data_quality_reports,
              data_quality_waivers, artifact_dependencies, artifact_manifests,
              execution_claims, ingestion_watermarks, ingestion_batches,
              source_catalog_snapshots, source_connections
            CASCADE
            """
        )
        cursor.execute(
            """
            INSERT INTO identity_principals
              (id, email, password_hash, installation_admin, active)
            VALUES (%s, %s, 'integration-only-not-a-secret', false, true)
            """,
            (actor_id, f"w15-{actor_id}@example.test"),
        )
        cursor.execute(
            """
            INSERT INTO identity_workspaces (id, key, name, active)
            VALUES (%s, %s, 'W15 Integration', true)
            """,
            (workspace_id, f"w15-{workspace_id.hex[:20]}"),
        )
    yield DataPipelineRuntime(connect, connector, workspace_id, actor_id)
    with connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            """
            TRUNCATE TABLE
              data_pipeline_outbox, semantic_dataset_versions, data_quality_reports,
              data_quality_waivers, artifact_dependencies, artifact_manifests,
              execution_claims, ingestion_watermarks, ingestion_batches,
              source_catalog_snapshots, source_connections
            CASCADE
            """
        )
        cursor.execute("DELETE FROM identity_principals WHERE id = %s", (actor_id,))
        cursor.execute("DELETE FROM identity_workspaces WHERE id = %s", (workspace_id,))
