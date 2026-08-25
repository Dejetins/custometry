"""Governed connection use cases over explicit repository and connector ports."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
import re
from typing import Protocol
from uuid import UUID, uuid4

from packages.connection_catalog.domain.model import (
    CatalogObject,
    ConnectionDefinition,
    ExtractionSession,
    SourceConnector,
)
from packages.contracts.source_intake import (
    PermissionAuthorizer,
    SourceIntakeActor,
    SourceIntakeFailure,
)


class ConnectionRepository(Protocol):
    def create(self, definition: ConnectionDefinition, *, actor_id: UUID) -> None: ...

    def get(self, *, workspace_id: UUID, connection_id: UUID) -> ConnectionDefinition | None: ...

    def save_catalog(
        self,
        *,
        workspace_id: UUID,
        connection_id: UUID,
        objects: tuple[CatalogObject, ...],
        actor_id: UUID,
        at: datetime,
    ) -> UUID: ...


ConnectorFactory = Callable[[ConnectionDefinition], SourceConnector]
_REFERENCE = re.compile(r"^[a-z][a-z0-9_.-]{2,79}$")
_MASKED_FIELDS = frozenset({"email", "phone", "loyalty_card", "external_person_id"})


class ConnectionService:
    """Keeps workspace authorization and secret-safe connector orchestration explicit."""

    def __init__(
        self,
        repository: ConnectionRepository,
        connector_factory: ConnectorFactory,
        authorize: PermissionAuthorizer,
    ) -> None:
        self._repository = repository
        self._connector_factory = connector_factory
        self._authorize = authorize

    def _permission(self, actor: SourceIntakeActor, permission: str) -> None:
        self._authorize(actor, permission)

    @staticmethod
    def _reference(value: str) -> str:
        normalized = value.strip().casefold()
        if _REFERENCE.fullmatch(normalized) is None:
            raise SourceIntakeFailure("INVALID_INPUT")
        return normalized

    def create(
        self,
        actor: SourceIntakeActor,
        *,
        connector_id: str,
        profile_ref: str,
        secret_ref: str,
        display_name: str,
    ) -> ConnectionDefinition:
        self._permission(actor, "connection.manage")
        if connector_id != "postgresql" or not display_name.strip():
            raise SourceIntakeFailure("INVALID_INPUT")
        definition = ConnectionDefinition(
            connection_id=uuid4(),
            workspace_id=actor.workspace_id,
            source_system_id=uuid4(),
            connector_id="postgresql",
            profile_ref=self._reference(profile_ref),
            secret_ref=self._reference(secret_ref),
            display_name=display_name.strip(),
            status="active",
            created_at=datetime.now(UTC),
        )
        self._repository.create(definition, actor_id=actor.principal_id)
        return definition

    def _load(
        self, actor: SourceIntakeActor, connection_id: UUID, permission: str
    ) -> ConnectionDefinition:
        self._permission(actor, permission)
        definition = self._repository.get(
            workspace_id=actor.workspace_id, connection_id=connection_id
        )
        if definition is None:
            raise SourceIntakeFailure("NOT_FOUND")
        if definition.status != "active":
            raise SourceIntakeFailure("CONNECTION_DISABLED")
        return definition

    def test(self, actor: SourceIntakeActor, connection_id: UUID) -> ConnectionDefinition:
        definition = self._load(actor, connection_id, "connection.manage")
        self._connector_factory(definition).test()
        return definition

    def discover(self, actor: SourceIntakeActor, connection_id: UUID) -> tuple[CatalogObject, ...]:
        definition = self._load(actor, connection_id, "connection.read_metadata")
        objects = self._connector_factory(definition).discover()
        self._repository.save_catalog(
            workspace_id=actor.workspace_id,
            connection_id=connection_id,
            objects=objects,
            actor_id=actor.principal_id,
            at=datetime.now(UTC),
        )
        return objects

    def preview(
        self,
        actor: SourceIntakeActor,
        connection_id: UUID,
        *,
        schema_name: str,
        object_name: str,
        columns: tuple[str, ...],
        limit: int,
    ) -> tuple[dict[str, object], ...]:
        definition = self._load(actor, connection_id, "connection.read_metadata")
        if not 1 <= limit <= 100 or not columns:
            raise SourceIntakeFailure("INVALID_INPUT")
        rows = self._connector_factory(definition).preview(
            schema_name=schema_name,
            object_name=object_name,
            columns=columns,
            limit=limit,
        )
        return tuple(
            {
                key: "***" if key.casefold() in _MASKED_FIELDS and value is not None else value
                for key, value in row.items()
            }
            for row in rows
        )

    def begin_session(self, actor: SourceIntakeActor, connection_id: UUID) -> ExtractionSession:
        definition = self._load(actor, connection_id, "connection.manage")
        return self._connector_factory(definition).begin_extraction_session(
            workspace_id=actor.workspace_id,
            source_system_id=definition.source_system_id,
        )

    def extract(
        self,
        actor: SourceIntakeActor,
        connection_id: UUID,
        *,
        session: ExtractionSession,
        schema_name: str,
        object_name: str,
        columns: tuple[str, ...],
        limit: int,
    ) -> tuple[dict[str, object], ...]:
        definition = self._load(actor, connection_id, "connection.manage")
        if (
            session.workspace_id != actor.workspace_id
            or session.source_system_id != definition.source_system_id
        ):
            raise SourceIntakeFailure("FORBIDDEN")
        if not 1 <= limit <= 10_000 or not columns:
            raise SourceIntakeFailure("INVALID_INPUT")
        return self._connector_factory(definition).extract(
            session=session,
            schema_name=schema_name,
            object_name=object_name,
            columns=columns,
            limit=limit,
        )

    def close_session(
        self,
        actor: SourceIntakeActor,
        connection_id: UUID,
        *,
        session: ExtractionSession,
        outcome: str,
    ) -> ExtractionSession:
        definition = self._load(actor, connection_id, "connection.manage")
        if outcome not in {"committed", "aborted"}:
            raise SourceIntakeFailure("INVALID_INPUT")
        if (
            session.workspace_id != actor.workspace_id
            or session.source_system_id != definition.source_system_id
        ):
            raise SourceIntakeFailure("FORBIDDEN")
        return self._connector_factory(definition).close_extraction_session(
            session,
            outcome,  # type: ignore[arg-type]
        )
