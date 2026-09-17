"""Same-session, same-origin owned draft APIs; app composition wires owner ports."""

from __future__ import annotations
import json
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Annotated
from uuid import UUID
import psycopg
from fastapi import Depends, FastAPI, Header, Query, Request, Response
from fastapi.responses import JSONResponse
from custometry_api.config import Settings
from custometry_api.analytics.router import build_analytics_services
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from packages.artifacts.infrastructure.document_snapshots import DocumentSnapshotArtifacts
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.presentation import (
    DraftResponse,
    PrepareRequest,
    PreparedResponse,
    PresentationFailure,
    ReportList,
    SaveRequest,
)
from packages.identity_access.application.service import IdentityFailure, IdentityService
from packages.identity_access.domain.policy import Actor
from packages.presentation.application.reports import ReportService
from packages.presentation.infrastructure.postgres import PostgresReportRepository


def create_reports_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    report_service: ReportService | None = None,
) -> FastAPI:
    identity, analytics = build_analytics_services(settings)

    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    brand = json.loads(
        (
            Path(__file__).resolve().parents[5]
            / "packages/presentation/infrastructure/system-brand.v1.json"
        ).read_text()
    )
    service = report_service or ReportService(
        PostgresReportRepository(connect),
        analytics,
        DocumentSnapshotArtifacts(connect, settings.analytics_artifact_root),
        brand,
    )
    auth = IdentityHTTPAdapter(identity_service or identity, settings)
    app = FastAPI(
        title="Custometry Draft Reports API", version="1.0.0", docs_url=None, redoc_url=None
    )

    @app.middleware("http")
    async def no_store(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(PresentationFailure)
    @app.exception_handler(AnalyticsFailure)
    @app.exception_handler(IdentityFailure)
    async def failure(
        _: Request, exc: PresentationFailure | AnalyticsFailure | IdentityFailure
    ) -> JSONResponse:
        code = exc.code
        status = 400
        if code == "AUTHENTICATION_FAILED":
            status = 401
        elif code in {"FORBIDDEN", "CSRF_FAILED"}:
            status = 403
        elif code == "NOT_FOUND":
            status = 404
        elif code.endswith("CONFLICT"):
            status = 409
        elif code in {"STORAGE_UNAVAILABLE", "RESULT_STORAGE_UNAVAILABLE"}:
            status = 503
        return JSONResponse(status_code=status, content={"code": code})

    @app.exception_handler(psycopg.Error)
    async def database_failure(_: Request, exc: psycopg.Error) -> JSONResponse:
        return JSONResponse(status_code=503, content={"code": "STORAGE_UNAVAILABLE"})

    def actor(request: Request, authorization: Annotated[str | None, Header()] = None) -> Actor:
        _ = authorization
        return auth.authenticate(request)

    @app.post("/prepare", response_model=PreparedResponse, operation_id="prepare_report_v1")
    def prepare(request: PrepareRequest, a: Actor = Depends(actor)) -> dict[str, object]:
        return service.prepare(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            result_id=request.result_id,
        )

    @app.post("/", response_model=DraftResponse, operation_id="create_report_v1")
    def create(request: SaveRequest, a: Actor = Depends(actor)) -> dict[str, object]:
        return service.save(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            request=request,
        )

    @app.get("/", response_model=ReportList, operation_id="list_reports_v1")
    def listing(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        a: Actor = Depends(actor),
    ) -> dict[str, object]:
        return service.list(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            offset=offset,
            limit=limit,
        )

    @app.get("/{report_id}", response_model=DraftResponse, operation_id="get_report_v1")
    def get(report_id: UUID, a: Actor = Depends(actor)) -> dict[str, object]:
        return service.get(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            report_id=report_id,
        )

    @app.post("/{report_id}/versions", response_model=DraftResponse, operation_id="save_report_v1")
    def save(report_id: UUID, request: SaveRequest, a: Actor = Depends(actor)) -> dict[str, object]:
        return service.save(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            request=request,
            report_id=report_id,
        )

    @app.get(
        "/{report_id}/snapshots/{snapshot_id}",
        response_model=DraftResponse,
        operation_id="preview_report_v1",
    )
    def preview(
        report_id: UUID,
        snapshot_id: UUID,
        version_id: UUID | None = None,
        page_id: UUID | None = None,
        block_id: UUID | None = None,
        a: Actor = Depends(actor),
    ) -> dict[str, object]:
        saved = service.get(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            report_id=report_id,
            snapshot_id=snapshot_id,
        )
        if (
            (version_id is not None and str(version_id) != saved["version_id"])
            or (page_id is not None and str(page_id) != saved["composition"]["default_page_id"])
            or (
                block_id is not None
                and str(block_id) not in {b["block_id"] for b in saved["composition"]["blocks"]}
            )
        ):
            raise PresentationFailure("NOT_FOUND")
        return saved

    _ = no_store, failure, database_failure, prepare, create, listing, get, save, preview
    return app
