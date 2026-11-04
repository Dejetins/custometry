"""Bounded reuse of Identity projection reads within one authorized read request.

Only the resource-access read adapter opts in. A new instance and effective time
are created for every GET; write/checkpoint paths never use this projection.
"""
from collections.abc import Callable
from contextlib import contextmanager
from copy import deepcopy
from datetime import date
from decimal import Decimal
from uuid import UUID
import json
from typing import Any, cast


_IMMUTABLE = (str, int, float, bool, bytes, type(None), UUID, date, Decimal)


def copy_row(value: Any) -> Any:
    # PostgreSQL/JSON projection containers are acyclic. UUID/date/Decimal scalar
    # values are immutable and need no pickle reconstruction on every read.
    if isinstance(value, _IMMUTABLE):
        return value
    if isinstance(value, dict):
        return {key: copy_row(item) for key, item in cast(dict[Any, Any], value).items()}
    if isinstance(value, list):
        return [copy_row(item) for item in cast(list[Any], value)]
    if isinstance(value, tuple):
        return tuple(copy_row(item) for item in cast(tuple[Any, ...], value))
    return deepcopy(value)


class RequestProjection:
    def __init__(self, connect: Callable[[], Any]):
        self.source = connect
        self.rows: dict[tuple[Any, ...], list[Any]] = {}
        self.bytes = 0

    @contextmanager
    def connect(self):
        with self.source() as connection:
            yield ProjectionConnection(connection, self)


class ProjectionConnection:
    def __init__(self, connection: Any, projection: RequestProjection):
        self.connection, self.projection = connection, projection

    @contextmanager
    def cursor(self, **kwargs: Any):
        with self.connection.cursor(**kwargs) as cursor:
            yield ProjectionCursor(cursor, self.projection)


class ProjectionCursor:
    def __init__(self, cursor: Any, projection: RequestProjection):
        self.cursor, self.projection = cursor, projection
        self.result: list[Any] = []
        self.position = 0

    def execute(self, query: str, parameters: Any = None):
        # These statements are internal Identity projection SQL, never user SQL.
        normalized = query.strip().upper()
        if not normalized.startswith(('SELECT', 'WITH RECURSIVE')) or 'FOR UPDATE' in normalized or 'PG_ADVISORY' in normalized:
            raise RuntimeError('READ_PROJECTION_STATEMENT_REQUIRED')
        key = (query, tuple(parameters or ()))
        self.position = 0
        cached = self.projection.rows.get(key)
        if cached is not None:
            self.result = cached
            return self
        self.cursor.execute(query, parameters)
        self.result = self.cursor.fetchall()
        if len(self.projection.rows) < 128 and len(self.result) <= 2048:
            size = len(json.dumps(self.result, default=str).encode())
            if self.projection.bytes + size <= 1024 * 1024:
                self.projection.rows[key] = self.result
                self.projection.bytes += size
        return self

    def fetchone(self):
        if self.position >= len(self.result):
            return None
        value = copy_row(self.result[self.position])
        self.position += 1
        return value

    def fetchall(self):
        values = copy_row(self.result[self.position:])
        self.position = len(self.result)
        return values
