"""Bounded API connection reuse; no application/result/permission cache."""

from collections.abc import Callable
from contextlib import contextmanager
from threading import Lock
from typing import Any, cast
import atexit
import psycopg
from psycopg_pool import ConnectionPool
from psycopg.abc import Buffer
from psycopg.types.json import set_json_loads
from pydantic import TypeAdapter, ConfigDict
from custometry_api.config import Settings

_json_value = TypeAdapter[Any](Any, config=ConfigDict(cache_strings=False))


def load_json_value(data: str | Buffer) -> Any:
    # JSONB is already syntactically validated by PostgreSQL. Decode plain JSON
    # values with the existing Rust parser, without a cross-request string cache.
    return _json_value.validate_json(data if isinstance(data, (str, bytes)) else bytes(data))


def configure_connection(connection: psycopg.Connection[Any]) -> None:
    set_json_loads(load_json_value, context=connection)


_lock = Lock()
_pools: dict[tuple[object, ...], ConnectionPool[psycopg.Connection[Any]]] = {}


def connection_factory(settings: Settings, *, autocommit_reads: bool = False) -> Callable[[], psycopg.Connection[Any]]:
    # A bounded registry accommodates isolated test applications without permitting
    # one pool per request/user. A production worker uses one database identity.
    key = (
        settings.database_host,
        settings.database_port,
        settings.database_name,
        settings.database_user,
        str(settings.database_password_file),
    )

    def get_pool():
        with _lock:
            pool = _pools.get(key)
            if pool is None:
                if len(_pools) >= 8:
                    raise psycopg.OperationalError("DATABASE_POOL_LIMIT")
                pool = ConnectionPool[psycopg.Connection[Any]](
                    kwargs=dict(
                        host=settings.database_host,
                        port=settings.database_port,
                        dbname=settings.database_name,
                        user=settings.database_user,
                        password=settings.read_database_password(),
                        connect_timeout=settings.database_connect_timeout_seconds,
                        options="-c statement_timeout=10000 -c idle_in_transaction_session_timeout=15000",
                    ),
                    configure=configure_connection,
                    min_size=0,
                    max_size=8,
                    max_waiting=64,
                    timeout=5,
                    max_idle=60,
                    max_lifetime=900,
                    open=True,
                )
                _pools[key] = pool
        return pool

    @contextmanager
    def scoped_connection():
        with get_pool().connection() as connection:
            if not autocommit_reads:
                yield connection
                return
            # Read-committed SELECTs do not need an implicit BEGIN/COMMIT pair.
            # Explicit c.transaction() (including initial calendar provisioning)
            # still provides its normal atomic commit/rollback boundary.
            prior = connection.autocommit
            connection.autocommit = True
            try:
                yield connection
            finally:
                if not connection.closed:
                    if connection.info.transaction_status != psycopg.pq.TransactionStatus.IDLE:
                        connection.rollback()
                    connection.autocommit = prior

    # Existing repository factories are consumed exclusively as scoped `with`
    # contexts. The pool retains transaction commit/rollback and broken-connection
    # disposal; it never returns a live connection outside that context.
    return cast(Callable[[], psycopg.Connection[Any]], scoped_connection)


def close_pools() -> None:
    with _lock:
        for pool in _pools.values():
            pool.close()
        _pools.clear()


atexit.register(close_pools)
