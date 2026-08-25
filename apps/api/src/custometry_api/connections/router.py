"""Secret-safe API contracts for PostgreSQL source discovery and extraction preview."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from typing import Annotated, Literal, cast
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Header, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from packages.connection_catalog.application.service import ConnectionService
from packages.connection_catalog.domain.model import (
    ConnectionDefinition,
    ExtractionSession,
)
from packages.connection_catalog.infrastructure.postgres import PostgresConnectionRepository
from packages.contracts.source_intake import (
    SOURCE_INTAKE_API_VERSION,
    SourceIntakeActor,
    SourceIntakeFailure,
)
from packages.identity_access.application.service import IdentityService
from packages.identity_access.domain.policy import (
    Actor,
    PolicyViolation,
    require_permission,
)
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from plugins.connector_postgresql import PostgreSQLConnector, PostgreSQLTarget


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ConnectionCreateRequest(StrictModel):
    connector_id: Literal["postgresql"]
    profile_ref: str = Field(min_length=3, max_length=80)
    secret_ref: str = Field(min_length=3, max_length=80)
    display_name: str = Field(min_length=1, max_length=160)


class ConnectionResponse(StrictModel):
    connection_id: UUID
    source_system_id: UUID
    connector_id: Literal["postgresql"]
    display_name: str
    status: Literal["active", "disabled", "archived"]


class ConnectorCapabilitiesResponse(StrictModel):
    driver: str
    driver_version: str
    supported_source_versions: list[str]
    consistency_modes: list[str]
    pushdown: list[str]
    read_only_enforced: bool


class ConnectionTestResponse(StrictModel):
    status: Literal["ready"]
    connection: ConnectionResponse
    capabilities: ConnectorCapabilitiesResponse


class CatalogObjectResponse(StrictModel):
    schema_name: str
    object_name: str
    object_type: Literal["table", "view"]
    columns: list[str]


class CatalogResponse(StrictModel):
    objects: list[CatalogObjectResponse]


class PreviewRequest(StrictModel):
    schema_name: str = Field(min_length=1, max_length=63)
    object_name: str = Field(min_length=1, max_length=63)
    columns: list[str] = Field(min_length=1, max_length=100)
    limit: int = Field(default=20, ge=1, le=100)


class PreviewResponse(StrictModel):
    rows: list[dict[str, object]]


class SessionResponse(StrictModel):
    session_id: UUID
    source_system_id: UUID
    consistency_mode: Literal["repeatable_read", "best_effort_validated"]
    state: Literal["active", "committed", "aborted", "expired"]
    opened_at: datetime
    expires_at: datetime


class ExtractRequest(PreviewRequest):
    session_id: UUID
    limit: int = Field(default=1_000, ge=1, le=10_000)


class ExtractResponse(StrictModel):
    row_count: int = Field(ge=0)
    content_hash: str = Field(min_length=64, max_length=64)


class CloseSessionRequest(StrictModel):
    session_id: UUID
    outcome: Literal["committed", "aborted"]


def _status_for(code: str) -> int:
    if code == "AUTHENTICATION_FAILED":
        return status.HTTP_401_UNAUTHORIZED
    if code == "FORBIDDEN":
        return status.HTTP_403_FORBIDDEN
    if code == "NOT_FOUND":
        return status.HTTP_404_NOT_FOUND
    if code == "CONFLICT":
        return status.HTTP_409_CONFLICT
    if code in {"SOURCE_UNAVAILABLE", "SOURCE_SESSION_REJECTED"}:
        return status.HTTP_503_SERVICE_UNAVAILABLE
    return status.HTTP_400_BAD_REQUEST


def _services(
    settings: Settings,
) -> tuple[IdentityService, ConnectionService, dict[UUID, PostgreSQLConnector]]:
    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    adapters: dict[UUID, PostgreSQLConnector] = {}

    def connector(definition: ConnectionDefinition) -> PostgreSQLConnector:
        if (
            definition.profile_ref != settings.source_postgresql_profile_ref
            or definition.secret_ref != settings.source_postgresql_secret_ref
        ):
            raise SourceIntakeFailure("SOURCE_PROFILE_UNAVAILABLE")
        adapter = adapters.get(definition.connection_id)
        if adapter is None:
            try:
                password = settings.read_source_postgresql_password()
            except (OSError, ValueError) as exc:
                raise SourceIntakeFailure("SOURCE_UNAVAILABLE") from exc
            adapter = PostgreSQLConnector(
                PostgreSQLTarget(
                    host=settings.source_postgresql_host,
                    port=settings.source_postgresql_port,
                    dbname=settings.source_postgresql_database,
                    user=settings.source_postgresql_user,
                    password=password,
                    connect_timeout_seconds=settings.source_postgresql_connect_timeout_seconds,
                    statement_timeout_ms=settings.source_postgresql_statement_timeout_ms,
                )
            )
            adapters[definition.connection_id] = adapter
        return adapter

    identity = IdentityService(PostgresIdentityRepository(connect), bootstrap_secret=None)

    def authorize(actor: SourceIntakeActor, permission: str) -> None:
        try:
            require_permission(cast(Actor, actor), permission)
        except PolicyViolation as exc:
            raise SourceIntakeFailure("FORBIDDEN") from exc

    service = ConnectionService(PostgresConnectionRepository(connect), connector, authorize)
    return identity, service, adapters


def _connection(definition: ConnectionDefinition) -> ConnectionResponse:
    return ConnectionResponse(
        connection_id=definition.connection_id,
        source_system_id=definition.source_system_id,
        connector_id=definition.connector_id,
        display_name=definition.display_name,
        status=definition.status,
    )


def _session(session: ExtractionSession) -> SessionResponse:
    return SessionResponse(
        session_id=session.session_id,
        source_system_id=session.source_system_id,
        consistency_mode=session.consistency_mode,
        state=session.state,
        opened_at=session.opened_at,
        expires_at=session.expires_at,
    )


def create_connection_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    connection_service: ConnectionService | None = None,
) -> FastAPI:
    default_identity, default_connections, adapters = _services(settings)
    identity = identity_service or default_identity
    connections = connection_service or default_connections
    sessions: dict[UUID, tuple[UUID, ExtractionSession]] = {}
    app = FastAPI(
        title="Custometry Source Connection API",
        version=SOURCE_INTAKE_API_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(SourceIntakeFailure)
    async def failure_handler(_: Request, exc: SourceIntakeFailure) -> JSONResponse:
        return JSONResponse(status_code=_status_for(exc.code), content={"code": exc.code})

    def authenticated(authorization: Annotated[str | None, Header()] = None) -> Actor:
        if authorization is None:
            raise SourceIntakeFailure("AUTHENTICATION_FAILED")
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer" or not token:
            raise SourceIntakeFailure("AUTHENTICATION_FAILED")
        try:
            return identity.authenticate(token)
        except Exception as exc:
            raise SourceIntakeFailure("AUTHENTICATION_FAILED") from exc

    @app.post("/", response_model=ConnectionResponse, operation_id="create_source_connection")
    def create(
        payload: ConnectionCreateRequest, actor: Actor = Depends(authenticated)
    ) -> ConnectionResponse:
        return _connection(connections.create(actor, **payload.model_dump()))

    @app.post(
        "/{connection_id}/test",
        response_model=ConnectionTestResponse,
        operation_id="test_source_connection",
    )
    def test(connection_id: UUID, actor: Actor = Depends(authenticated)) -> ConnectionTestResponse:
        definition = connections.test(actor, connection_id)
        capabilities = adapters[definition.connection_id].capabilities()
        return ConnectionTestResponse(
            status="ready",
            connection=_connection(definition),
            capabilities=ConnectorCapabilitiesResponse(
                driver=capabilities.driver,
                driver_version=capabilities.driver_version,
                supported_source_versions=list(capabilities.supported_source_versions),
                consistency_modes=list(capabilities.consistency_modes),
                pushdown=list(capabilities.pushdown),
                read_only_enforced=capabilities.read_only_enforced,
            ),
        )

    @app.get(
        "/{connection_id}/catalog",
        response_model=CatalogResponse,
        operation_id="discover_source_catalog",
    )
    def discover(connection_id: UUID, actor: Actor = Depends(authenticated)) -> CatalogResponse:
        return CatalogResponse(
            objects=[
                CatalogObjectResponse(
                    schema_name=item.schema_name,
                    object_name=item.object_name,
                    object_type=item.object_type,
                    columns=list(item.columns),
                )
                for item in connections.discover(actor, connection_id)
            ]
        )

    @app.post(
        "/{connection_id}/preview",
        response_model=PreviewResponse,
        operation_id="preview_source_object",
    )
    def preview(
        connection_id: UUID,
        payload: PreviewRequest,
        actor: Actor = Depends(authenticated),
    ) -> PreviewResponse:
        rows = connections.preview(
            actor,
            connection_id,
            schema_name=payload.schema_name,
            object_name=payload.object_name,
            columns=tuple(payload.columns),
            limit=payload.limit,
        )
        return PreviewResponse(rows=list(rows))

    @app.post(
        "/{connection_id}/sessions",
        response_model=SessionResponse,
        operation_id="begin_source_extraction_session",
    )
    def begin_session(
        connection_id: UUID, actor: Actor = Depends(authenticated)
    ) -> SessionResponse:
        session = connections.begin_session(actor, connection_id)
        sessions[session.session_id] = (connection_id, session)
        return _session(session)

    @app.post(
        "/{connection_id}/extract",
        response_model=ExtractResponse,
        operation_id="extract_source_object",
    )
    def extract(
        connection_id: UUID,
        payload: ExtractRequest,
        actor: Actor = Depends(authenticated),
    ) -> ExtractResponse:
        stored = sessions.get(payload.session_id)
        if stored is None or stored[0] != connection_id:
            raise SourceIntakeFailure("EXTRACTION_SESSION_INVALID")
        rows = connections.extract(
            actor,
            connection_id,
            session=stored[1],
            schema_name=payload.schema_name,
            object_name=payload.object_name,
            columns=tuple(payload.columns),
            limit=payload.limit,
        )
        digest = hashlib.sha256(
            json.dumps(rows, sort_keys=True, separators=(",", ":"), default=str).encode()
        ).hexdigest()
        return ExtractResponse(row_count=len(rows), content_hash=digest)

    @app.post(
        "/{connection_id}/sessions/close",
        response_model=SessionResponse,
        operation_id="close_source_extraction_session",
    )
    def close_session(
        connection_id: UUID,
        payload: CloseSessionRequest,
        actor: Actor = Depends(authenticated),
    ) -> SessionResponse:
        stored = sessions.get(payload.session_id)
        if stored is None or stored[0] != connection_id:
            raise SourceIntakeFailure("EXTRACTION_SESSION_INVALID")
        closed = connections.close_session(
            actor,
            connection_id,
            session=stored[1],
            outcome=payload.outcome,
        )
        sessions.pop(payload.session_id, None)
        return _session(closed)

    _ = (failure_handler, create, test, discover, preview, begin_session, extract, close_session)
    return app
