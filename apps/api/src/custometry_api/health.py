"""Health contracts and the PostgreSQL readiness adapter."""

from dataclasses import dataclass
from typing import Protocol

import psycopg

from custometry_api.config import Settings


class ReadinessProbe(Protocol):
    """Port used by the API health boundary."""

    def is_ready(self) -> bool:
        """Return whether the API can safely accept requests."""

        ...


@dataclass(frozen=True, slots=True)
class PostgreSQLReadinessProbe:
    """Check database connectivity and that the Foundation migration exists."""

    settings: Settings

    def is_ready(self) -> bool:
        try:
            with psycopg.connect(
                host=self.settings.database_host,
                port=self.settings.database_port,
                dbname=self.settings.database_name,
                user=self.settings.database_user,
                password=self.settings.read_database_password(),
                connect_timeout=self.settings.database_connect_timeout_seconds,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT EXISTS ("
                        "SELECT 1 FROM pg_catalog.pg_class "
                        "WHERE relnamespace = 'public'::regnamespace "
                        "AND relname = 'platform_metadata'"
                        ")"
                    )
                    row = cursor.fetchone()
                    return bool(row and row[0])
        except (OSError, ValueError, psycopg.Error):
            return False
