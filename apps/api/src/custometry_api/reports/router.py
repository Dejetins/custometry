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
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from custometry_api.analytics.workspace_errors import workspace_error
from custometry_api.config import Settings
from custometry_api.analytics.router import build_analytics_services
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.semantic import CalendarFailure
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


def create_reports_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    report_service: ReportService | None = None,
) -> FastAPI:
    identity, _ = build_analytics_services(settings)

    brand_path = (
        Path(__file__).resolve().parents[5]
        / "packages/presentation/infrastructure/system-brand.v1.json"
    )
    if not brand_path.is_file():
        brand_path = (
            Path(__file__).resolve().parents[2]
            / "packages/presentation/infrastructure/system-brand.v1.json"
        )
    brand = json.loads(brand_path.read_text())
    auth = IdentityHTTPAdapter(identity_service or identity, settings)
    app = FastAPI(
        title="Custometry Draft Reports API", version="1.0.0", docs_url=None, redoc_url=None
    )

    @app.middleware("http")
    async def no_store(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if (
            "/v2/" in request.url.path
            and request.method == "POST"
            and len(await request.body()) > 1024 * 1024
        ):
            return workspace_error("WORKSPACE_LIMIT_EXCEEDED")
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(PresentationFailure)
    @app.exception_handler(AnalyticsFailure)
    @app.exception_handler(CalendarFailure)
    @app.exception_handler(IdentityFailure)
    async def failure(
        request: Request,
        exc: PresentationFailure | AnalyticsFailure | IdentityFailure | CalendarFailure,
    ) -> JSONResponse:
        if "/v2/" in request.url.path:
            return workspace_error(exc.code, exc.__cause__)
        code = exc.code
        status = 400
        if code == "AUTHENTICATION_FAILED":
            status = 401
        elif code in {"FORBIDDEN", "CSRF_FAILED"}:
            status = 403
        elif code == "NOT_FOUND":
            status = 404
        elif code.endswith("CONFLICT") or code == "REPORT_VERSION_UPGRADE_REQUIRED":
            status = 409
        elif code in {"STORAGE_UNAVAILABLE", "RESULT_STORAGE_UNAVAILABLE"}:
            status = 503
        return JSONResponse(status_code=status, content={"code": code})

    @app.exception_handler(psycopg.Error)
    async def database_failure(request: Request, exc: psycopg.Error) -> JSONResponse:
        if "/v2/" in request.url.path:
            return workspace_error("STORAGE_UNAVAILABLE")
        return JSONResponse(status_code=503, content={"code": "STORAGE_UNAVAILABLE"})

    @app.exception_handler(RequestValidationError)
    async def validation_failure(request: Request, exc: RequestValidationError) -> Response:
        if "/v2/" in request.url.path:
            exceeded = any(
                "WORKSPACE_LIMIT_EXCEEDED" in str(e.get("msg", ""))
                or e.get("type") == "too_long"
                and any(
                    k in e.get("loc", ())
                    for k in ("worksets", "cards", "store_ids", "local_store_ids")
                )
                for e in exc.errors()
            )
            if exceeded:
                return workspace_error("WORKSPACE_LIMIT_EXCEEDED")
            return JSONResponse(
                status_code=422, content={"code": "INVALID_INPUT", "retryable": False}
            )
        return await request_validation_exception_handler(request, exc)

    def actor(request: Request, authorization: Annotated[str | None, Header()] = None) -> Actor:
        _ = authorization
        return auth.authenticate(request)

    from custometry_api.reports.workspace_router import workspace_reports_router

    app.include_router(workspace_reports_router(settings, auth))

    def current_service(request: Request) -> ReportService:
        if report_service is not None:
            return report_service
        from custometry_api.reports.workspace_composition import guarded_legacy

        return guarded_legacy(settings, auth, request, brand)

    @app.post("/prepare", response_model=PreparedResponse, operation_id="prepare_report_v1")
    def prepare(
        request: PrepareRequest, http: Request, a: Actor = Depends(actor)
    ) -> dict[str, object]:
        return current_service(http).prepare(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            result_id=request.result_id,
        )

    @app.post("/", response_model=DraftResponse, operation_id="create_report_v1")
    def create(request: SaveRequest, http: Request, a: Actor = Depends(actor)) -> dict[str, object]:
        return current_service(http).save(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            request=request,
        )

    @app.get("/", response_model=ReportList, operation_id="list_reports_v1")
    def listing(
        http: Request,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        a: Actor = Depends(actor),
    ) -> dict[str, object]:
        return current_service(http).list(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            offset=offset,
            limit=limit,
        )

    @app.get("/{report_id}", response_model=DraftResponse, operation_id="get_report_v1")
    def get(report_id: UUID, http: Request, a: Actor = Depends(actor)) -> dict[str, object]:
        return current_service(http).get(
            workspace_id=a.workspace_id,
            principal_id=a.principal_id,
            permissions=a.permissions,
            report_id=report_id,
        )

    @app.post("/{report_id}/versions", response_model=DraftResponse, operation_id="save_report_v1")
    def save(
        report_id: UUID, request: SaveRequest, http_request: Request, a: Actor = Depends(actor)
    ) -> dict[str, object]:
        if report_service is None:
            from custometry_api.reports.workspace_composition import build_workspace

            current, _ = build_workspace(settings, auth, http_request)
            current.guard(a.workspace_id, a.principal_id, report_id, write=True)
        return current_service(http_request).save(
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
        http: Request,
        version_id: UUID | None = None,
        page_id: UUID | None = None,
        block_id: UUID | None = None,
        a: Actor = Depends(actor),
    ) -> dict[str, object]:
        saved = current_service(http).get(
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

    _ = (
        no_store,
        failure,
        database_failure,
        validation_failure,
        prepare,
        create,
        listing,
        get,
        save,
        preview,
    )
    return app
