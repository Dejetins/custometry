from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, cast
from uuid import UUID, uuid4

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import Connection
from redis import Redis
from testcontainers.core.container import DockerContainer  # pyright: ignore[reportMissingTypeStubs]
from testcontainers.core.wait_strategies import (  # pyright: ignore[reportMissingTypeStubs]
    LogMessageWaitStrategy,
)
from testcontainers.postgres import PostgresContainer  # pyright: ignore[reportMissingTypeStubs]

from packages.identity_access.domain.policy import Actor


POSTGRES_IMAGE = (
    "postgres:17.5-alpine3.21@"
    "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4"
)
VALKEY_IMAGE = "valkey/valkey:8.0.1-alpine"


def migrate(
    *, host: str, port: int, database: str, user: str, password_file: Path, revision: str
) -> None:
    names = {
        "CUSTOMETRY_DATABASE_HOST": host,
        "CUSTOMETRY_DATABASE_PORT": str(port),
        "CUSTOMETRY_DATABASE_NAME": database,
        "CUSTOMETRY_DATABASE_USER": user,
        "CUSTOMETRY_DATABASE_PASSWORD_FILE": str(password_file),
    }
    previous = {name: os.environ.get(name) for name in names}
    os.environ.update(names)
    try:
        configuration = Config("migrations/alembic.ini")
        if revision.startswith("-"):
            command.downgrade(configuration, revision.removeprefix("-"))
        else:
            command.upgrade(configuration, revision)
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


@dataclass(frozen=True, slots=True)
class ExecutionRuntime:
    connect: Callable[[], Connection[Any]]
    valkey: Redis
    workspace_id: UUID
    owner: Actor
    operator: Actor
    outsider: Actor


@dataclass(frozen=True, slots=True)
class ExecutionBoundaries:
    connect: Callable[[], Connection[Any]]
    valkey: Redis
    database_host: str
    database_port: int
    database_password_file: Path


class RedisMaintenance(Protocol):
    def ping(self) -> bool: ...

    def flushdb(self) -> bool: ...


@pytest.fixture(scope="session")
def execution_boundaries(
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[ExecutionBoundaries]:
    secret = "w36-disposable-postgres-only"
    secret_file = tmp_path_factory.mktemp("w36-secrets") / "postgres-password"
    secret_file.write_text(secret, encoding="utf-8")
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

        migrate(
            host=host,
            port=port,
            database="custometry",
            user="custometry",
            password_file=secret_file,
            revision="head",
        )
        valkey_ready = LogMessageWaitStrategy("Ready to accept connections").with_startup_timeout(30)
        with (
            DockerContainer(VALKEY_IMAGE)
            .with_exposed_ports(6379)
            .waiting_for(valkey_ready) as valkey_container
        ):
            valkey = Redis(
                host=valkey_container.get_container_host_ip(),
                port=int(valkey_container.get_exposed_port(6379)),
                decode_responses=False,
                socket_timeout=3,
            )
            assert cast(RedisMaintenance, valkey).ping()
            yield ExecutionBoundaries(connect, valkey, host, port, secret_file)


@pytest.fixture
def execution_runtime(
    execution_boundaries: ExecutionBoundaries,
) -> Iterator[ExecutionRuntime]:
    connect, valkey = execution_boundaries.connect, execution_boundaries.valkey
    cast(RedisMaintenance, valkey).flushdb()
    workspace_id = uuid4()
    owner_id = uuid4()
    operator_id = uuid4()
    outsider_id = uuid4()
    with connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO identity_workspaces (id, key, name, active)
            VALUES (%s, %s, 'W36 Integration', true)
            """,
            (workspace_id, f"w36-{workspace_id.hex[:20]}"),
        )
        for principal_id, label in (
            (owner_id, "owner"),
            (operator_id, "operator"),
            (outsider_id, "outsider"),
        ):
            cursor.execute(
                """
                INSERT INTO identity_principals
                  (id, email, password_hash, installation_admin, active)
                VALUES (%s, %s, 'integration-only-not-a-secret', false, true)
                """,
                (principal_id, f"w36-{label}-{principal_id}@example.test"),
            )
    owner = Actor(
        owner_id,
        workspace_id,
        "owner@example.test",
        frozenset({"run.read"}),
    )
    operator = Actor(
        operator_id,
        workspace_id,
        "operator@example.test",
        frozenset({"run.read", "run.cancel", "run.retry", "run.create"}),
    )
    outsider = Actor(outsider_id, workspace_id, "outsider@example.test", frozenset())
    yield ExecutionRuntime(connect, valkey, workspace_id, owner, operator, outsider)
    with connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            """
            TRUNCATE TABLE execution_reconciliation_findings, execution_idempotency,
              execution_outbox, execution_transition_history, execution_attempts,
              execution_runs CASCADE
            """
        )
        cursor.execute("DELETE FROM identity_principals WHERE id = ANY(%s)", ([owner_id, operator_id, outsider_id],))
        cursor.execute("DELETE FROM identity_workspaces WHERE id = %s", (workspace_id,))
