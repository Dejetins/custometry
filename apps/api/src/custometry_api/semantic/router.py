"""The only new mounted S01 API: current-workspace fiscal settings."""

from collections.abc import Awaitable, Callable
from uuid import UUID
import psycopg
from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from custometry_api.config import Settings
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.identity.router import create_identity_service
from packages.contracts.semantic import (
    BusinessCalendarVersion,
    CalendarFailure,
    CalendarError,
    CalendarRef,
    Hash,
    UpdateCalendarRequest,
    WorkspaceCalendarDefault,
)
from packages.identity_access.application.service import IdentityFailure
from packages.identity_access.domain.policy import Actor
from packages.semantic_model.application.calendar import WorkspaceCalendarService
from packages.semantic_model.infrastructure.calendar import PostgresCalendarRepository


def build_calendar_service(settings: Settings) -> WorkspaceCalendarService:
    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    return WorkspaceCalendarService(PostgresCalendarRepository(connect))


def create_semantic_app(settings: Settings) -> FastAPI:
    service = build_calendar_service(settings)
    auth = IdentityHTTPAdapter(create_identity_service(settings), settings)
    app = FastAPI(
        title="Custometry Workspace Calendar API", version="1.0.0", docs_url=None, redoc_url=None
    )

    @app.middleware("http")
    async def no_store(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(CalendarFailure)
    @app.exception_handler(IdentityFailure)
    async def failure(_: Request, exc: CalendarFailure | IdentityFailure) -> JSONResponse:
        code = exc.code
        status = (
            409
            if code.endswith("CONFLICT")
            else {
                "AUTHENTICATION_FAILED": 401,
                "FORBIDDEN": 403,
                "CSRF_FAILED": 403,
                "NOT_FOUND": 404,
            }.get(code, 400)
        )
        return JSONResponse(status_code=status, content={"code": code})

    @app.exception_handler(psycopg.Error)
    async def unavailable(_: Request, exc: psycopg.Error) -> JSONResponse:
        return JSONResponse(status_code=503, content={"code": "STORAGE_UNAVAILABLE"})

    def actor(request: Request) -> Actor:
        return auth.authenticate(request)

    @app.get(
        "/workspace-calendar/v1",
        response_model=WorkspaceCalendarDefault,
        operation_id="get_workspace_calendar_v1",
        responses={
            401: {"model": CalendarError},
            403: {"model": CalendarError},
            404: {"model": CalendarError},
            503: {"model": CalendarError},
        },
    )
    def default(a: Actor = Depends(actor)) -> WorkspaceCalendarDefault:
        return service.get_default(a.workspace_id, a)

    @app.get(
        "/workspace-calendar/v1/versions/{version_id}",
        response_model=BusinessCalendarVersion,
        operation_id="get_workspace_calendar_version_v1",
        responses={
            401: {"model": CalendarError},
            403: {"model": CalendarError},
            404: {"model": CalendarError},
            503: {"model": CalendarError},
        },
    )
    def version(
        version_id: UUID, content_hash: Hash, a: Actor = Depends(actor)
    ) -> BusinessCalendarVersion:
        return service.get_version(CalendarRef(version_id=version_id, content_hash=content_hash), a)

    @app.post(
        "/workspace-calendar/v1/versions",
        response_model=WorkspaceCalendarDefault,
        operation_id="update_workspace_calendar_v1",
        responses={
            401: {"model": CalendarError},
            403: {"model": CalendarError},
            404: {"model": CalendarError},
            409: {"model": CalendarError},
            503: {"model": CalendarError},
        },
    )
    def update(
        request: UpdateCalendarRequest, a: Actor = Depends(actor)
    ) -> WorkspaceCalendarDefault:
        return service.update_default(request, a)

    _ = no_store, failure, unavailable, default, version, update
    return app
