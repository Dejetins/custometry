# pyright: reportMissingTypeStubs=false
from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import Connection
from testcontainers.postgres import PostgresContainer


POSTGRES_IMAGE = (
    "postgres:17.5-alpine3.21@"
    "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4"
)


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
class NotificationBoundaries:
    connect: Callable[[], Connection[Any]]
    database_host: str
    database_port: int
    database_password_file: Path


@dataclass(frozen=True, slots=True)
class NotificationRuntime:
    connect: Callable[[], Connection[Any]]
    workspace_id: UUID
    second_workspace_id: UUID
    reader_id: UUID
    acknowledger_id: UUID
    outsider_id: UUID


@pytest.fixture(scope="session")
def notification_boundaries(
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[NotificationBoundaries]:
    secret = "w37-disposable-postgres-only"
    secret_file = tmp_path_factory.mktemp("w37-secrets") / "postgres-password"
    secret_file.write_text(secret, encoding="utf-8")
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

        migrate(
            host=host,
            port=port,
            database="custometry",
            user="custometry",
            password_file=secret_file,
            revision="head",
        )
        yield NotificationBoundaries(connect, host, port, secret_file)


@pytest.fixture
def notification_runtime(
    notification_boundaries: NotificationBoundaries,
) -> NotificationRuntime:
    values = [uuid4() for _ in range(5)]
    workspace_id, second_workspace_id, reader_id, acknowledger_id, outsider_id = values
    with (
        notification_boundaries.connect() as connection,
        connection.transaction(),
        connection.cursor() as cursor,
    ):
        cursor.executemany(
            "INSERT INTO identity_workspaces (id, key, name) VALUES (%s, %s, %s)",
            (
                (workspace_id, f"w37-{str(workspace_id)[:8]}", "W37 Primary"),
                (
                    second_workspace_id,
                    f"w37-{str(second_workspace_id)[:8]}",
                    "W37 Secondary",
                ),
            ),
        )
        cursor.executemany(
            """
            INSERT INTO identity_principals (id, email, password_hash)
            VALUES (%s, %s, 'not-a-login-secret')
            """,
            (
                (reader_id, f"{reader_id}@example.invalid"),
                (acknowledger_id, f"{acknowledger_id}@example.invalid"),
                (outsider_id, f"{outsider_id}@example.invalid"),
            ),
        )
    return NotificationRuntime(
        notification_boundaries.connect,
        workspace_id,
        second_workspace_id,
        reader_id,
        acknowledger_id,
        outsider_id,
    )
