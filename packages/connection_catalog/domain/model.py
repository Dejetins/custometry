"""Locale-neutral connection and connector contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ConnectionDefinition:
    connection_id: UUID
    workspace_id: UUID
    source_system_id: UUID
    connector_id: Literal["postgresql"]
    profile_ref: str
    secret_ref: str
    display_name: str
    status: Literal["active", "disabled", "archived"]
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ConnectorCapabilities:
    connector_id: str
    driver: str
    driver_version: str
    supported_source_versions: tuple[str, ...]
    consistency_modes: tuple[str, ...]
    pushdown: tuple[str, ...]
    read_only_enforced: bool
    identifier_quoting: str
    timezone_semantics: str
    decimal_semantics: str


@dataclass(frozen=True, slots=True)
class CatalogObject:
    schema_name: str
    object_name: str
    object_type: Literal["table", "view"]
    columns: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExtractionSession:
    session_id: UUID
    workspace_id: UUID
    source_system_id: UUID
    consistency_mode: Literal["repeatable_read", "best_effort_validated"]
    state: Literal["active", "committed", "aborted", "expired"]
    opened_at: datetime
    expires_at: datetime


class SourceConnector(Protocol):
    """Port owned by Connection Catalog/Ingestion; adapters stay private."""

    def capabilities(self) -> ConnectorCapabilities: ...

    def test(self) -> None: ...

    def discover(self) -> tuple[CatalogObject, ...]: ...

    def preview(
        self, *, schema_name: str, object_name: str, columns: tuple[str, ...], limit: int
    ) -> tuple[dict[str, object], ...]: ...

    def begin_extraction_session(
        self, *, workspace_id: UUID, source_system_id: UUID
    ) -> ExtractionSession: ...

    def extract(
        self,
        *,
        session: ExtractionSession,
        schema_name: str,
        object_name: str,
        columns: tuple[str, ...],
        limit: int,
    ) -> tuple[dict[str, object], ...]: ...

    def close_extraction_session(
        self, session: ExtractionSession, outcome: Literal["committed", "aborted"]
    ) -> ExtractionSession: ...
