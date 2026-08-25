"""Read-only, bounded PostgreSQL implementation of the SourceConnector port."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from importlib.metadata import version
from typing import Any
from uuid import UUID, uuid4

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

from packages.connection_catalog.domain.model import (
    CatalogObject,
    ConnectorCapabilities,
    ExtractionSession,
)
from packages.contracts.source_intake import SourceIntakeFailure


@dataclass(frozen=True, slots=True)
class PostgreSQLTarget:
    host: str
    port: int
    dbname: str
    user: str
    password: str
    connect_timeout_seconds: int = 3
    statement_timeout_ms: int = 5_000


class PostgreSQLConnector:
    """Uses quoted identifiers and server-enforced read-only transactions."""

    def __init__(self, target: PostgreSQLTarget) -> None:
        self._target = target
        self._sessions: dict[UUID, tuple[ExtractionSession, psycopg.Connection[Any]]] = {}

    def _connect(self) -> psycopg.Connection[Any]:
        try:
            connection = psycopg.connect(
                host=self._target.host,
                port=self._target.port,
                dbname=self._target.dbname,
                user=self._target.user,
                password=self._target.password,
                connect_timeout=self._target.connect_timeout_seconds,
                options=(
                    "-c default_transaction_read_only=on "
                    f"-c statement_timeout={self._target.statement_timeout_ms}"
                ),
            )
        except psycopg.Error as exc:
            raise SourceIntakeFailure("SOURCE_UNAVAILABLE") from exc
        return connection

    def capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(
            connector_id="postgresql",
            driver="psycopg",
            driver_version=version("psycopg"),
            supported_source_versions=("15", "16", "17"),
            consistency_modes=("repeatable_read", "best_effort_validated"),
            pushdown=("projection", "limit"),
            read_only_enforced=True,
            identifier_quoting="double_quote",
            timezone_semantics="server_typed_to_utc_contract",
            decimal_semantics="native_numeric_to_decimal",
        )

    def test(self) -> None:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute("SHOW transaction_read_only")
            row = cursor.fetchone()
            if row is None or str(row[0]).casefold() != "on":
                raise SourceIntakeFailure("READ_ONLY_REQUIRED")
            cursor.execute("SELECT current_setting('server_version_num')::integer")
            version_row = cursor.fetchone()
            if version_row is None or int(version_row[0]) < 150000:
                raise SourceIntakeFailure("SOURCE_VERSION_UNSUPPORTED")

    def discover(self) -> tuple[CatalogObject, ...]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT c.table_schema, c.table_name, t.table_type,
                       array_agg(c.column_name ORDER BY c.ordinal_position) AS columns
                FROM information_schema.columns AS c
                JOIN information_schema.tables AS t
                  ON t.table_schema = c.table_schema AND t.table_name = c.table_name
                WHERE c.table_schema NOT IN ('pg_catalog', 'information_schema')
                GROUP BY c.table_schema, c.table_name, t.table_type
                ORDER BY c.table_schema, c.table_name
                """
            )
            rows = cursor.fetchall()
        return tuple(
            CatalogObject(
                schema_name=str(row["table_schema"]),
                object_name=str(row["table_name"]),
                object_type="view" if str(row["table_type"]).casefold() == "view" else "table",
                columns=tuple(str(item) for item in row["columns"]),
            )
            for row in rows
        )

    @staticmethod
    def _query(
        cursor: Any,
        *,
        schema_name: str,
        object_name: str,
        columns: tuple[str, ...],
        limit: int,
    ) -> tuple[dict[str, object], ...]:
        statement = sql.SQL("SELECT {columns} FROM {table} LIMIT %s").format(
            columns=sql.SQL(", ").join(sql.Identifier(column) for column in columns),
            table=sql.Identifier(schema_name, object_name),
        )
        try:
            cursor.execute(statement, (limit,))
            rows = cursor.fetchall()
        except psycopg.Error as exc:
            raise SourceIntakeFailure("SOURCE_QUERY_REJECTED") from exc
        return tuple(dict(row) for row in rows)

    def preview(
        self, *, schema_name: str, object_name: str, columns: tuple[str, ...], limit: int
    ) -> tuple[dict[str, object], ...]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            return self._query(
                cursor,
                schema_name=schema_name,
                object_name=object_name,
                columns=columns,
                limit=limit,
            )

    def begin_extraction_session(
        self, *, workspace_id: UUID, source_system_id: UUID
    ) -> ExtractionSession:
        connection = self._connect()
        try:
            connection.execute("BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY")
        except psycopg.Error as exc:
            connection.close()
            raise SourceIntakeFailure("SOURCE_SESSION_REJECTED") from exc
        opened = datetime.now(UTC)
        session = ExtractionSession(
            session_id=uuid4(),
            workspace_id=workspace_id,
            source_system_id=source_system_id,
            consistency_mode="repeatable_read",
            state="active",
            opened_at=opened,
            expires_at=opened + timedelta(minutes=5),
        )
        self._sessions[session.session_id] = (session, connection)
        return session

    def _active(self, session: ExtractionSession) -> psycopg.Connection[Any]:
        stored = self._sessions.get(session.session_id)
        if stored is None or stored[0] != session or session.state != "active":
            raise SourceIntakeFailure("EXTRACTION_SESSION_INVALID")
        if session.expires_at <= datetime.now(UTC):
            stored[1].rollback()
            stored[1].close()
            del self._sessions[session.session_id]
            raise SourceIntakeFailure("EXTRACTION_SESSION_EXPIRED")
        return stored[1]

    def extract(
        self,
        *,
        session: ExtractionSession,
        schema_name: str,
        object_name: str,
        columns: tuple[str, ...],
        limit: int,
    ) -> tuple[dict[str, object], ...]:
        connection = self._active(session)
        with connection.cursor(row_factory=dict_row) as cursor:
            return self._query(
                cursor,
                schema_name=schema_name,
                object_name=object_name,
                columns=columns,
                limit=limit,
            )

    def close_extraction_session(
        self, session: ExtractionSession, outcome: str
    ) -> ExtractionSession:
        connection = self._active(session)
        try:
            if outcome == "committed":
                connection.commit()
            elif outcome == "aborted":
                connection.rollback()
            else:
                raise SourceIntakeFailure("INVALID_INPUT")
        finally:
            connection.close()
            self._sessions.pop(session.session_id, None)
        return replace(session, state=outcome)  # type: ignore[arg-type]


def json_safe_value(value: object) -> object:
    """Retained for explicit scalar normalization by API adapters."""

    if isinstance(value, (datetime, Decimal)):
        return str(value)
    return value
