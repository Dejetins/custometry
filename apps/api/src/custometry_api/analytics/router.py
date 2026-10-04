"""Authenticated, policy-filtered projections for governed analytics results."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Header, Query, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import BaseModel, ConfigDict, Field, model_validator

from custometry_api.analytics.sales_models import SalesRunRequest, SalesResponse, SalesContext
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from custometry_api.config import Settings
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from packages.analytics_core.application.service import AnalyticsService
from packages.analytics_core.domain.model import (
    AnalyticsRequest,
    FilterPredicate,
    Period,
    TimeComparison,
)
from packages.analytics_core.infrastructure.local import LocalAnalyticsArtifactStore
from packages.analytics_core.infrastructure.postgres import PostgresAnalyticsRepository
from packages.contracts.analytics import ANALYTICS_API_VERSION, AnalyticsFailure
from packages.identity_access.application.service import IdentityFailure, IdentityService
from packages.identity_access.domain.policy import Actor
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorResponse(StrictModel):
    code: str


class PeriodRequest(StrictModel):
    starts_on: date
    ends_on: date


class TimeComparisonRequest(StrictModel):
    mode: Literal[
        "none",
        "previous_year_same_dates",
        "previous_year_calendar_aligned",
        "previous_year_iso_week_aligned",
        "previous_year_fiscal_period",
        "previous_year_comparable_elapsed_days",
    ]
    current_period: PeriodRequest
    comparison_period: PeriodRequest | None = None
    timezone: str = Field(min_length=1, max_length=80)
    calendar_version_id: UUID
    incomplete_period_policy: Literal["exclude", "comparable_elapsed_days", "explicit_partial"]
    leap_day_policy: Literal["calendar_map", "exclude", "merge_with_feb_28"]
    iso_week_53_policy: Literal["calendar_map", "exclude", "explicit_partial"]
    definition_compatibility_policy: Literal["require_same_versions", "allow_explicit_rebase"]


class TypedFilterRequest(StrictModel):
    field: Literal["store_id", "channel_id", "currency", "status", "net_amount"]
    operator: Literal["eq", "in", "gte", "lte"]
    value: str | Decimal | list[str]

    @model_validator(mode="after")
    def validate_typed_value(self) -> "TypedFilterRequest":
        categorical = self.field != "net_amount"
        if categorical and self.operator == "in" and not isinstance(self.value, list):
            raise ValueError("categorical in filter requires a list")
        if categorical and self.operator == "eq" and not isinstance(self.value, str):
            raise ValueError("categorical eq filter requires a string")
        if not categorical and self.operator == "in":
            raise ValueError("numeric filter does not support in")
        if not categorical and isinstance(self.value, list):
            raise ValueError("numeric filter requires a scalar")
        return self

    def domain(self) -> FilterPredicate:
        if self.field == "net_amount":
            value: str | Decimal | tuple[str, ...] = Decimal(str(self.value))
        elif isinstance(self.value, list):
            value = tuple(self.value)
        else:
            value = str(self.value)
        return FilterPredicate(field=self.field, operator=self.operator, value=value)


def _empty_typed_filters() -> list[TypedFilterRequest]:
    return []


class AnalyticsRunRequest(StrictModel):
    result_type: Literal["sales", "customer", "rfm"]
    semantic_dataset_version_id: UUID
    comparison: TimeComparisonRequest
    filters: list[TypedFilterRequest] = Field(default_factory=_empty_typed_filters, max_length=12)
    rfm_score_bins: int = Field(default=5, ge=2, le=10)
    rfm_frequency_measure: Literal["receipt_count", "purchase_day_count"] = "receipt_count"
    rfm_segment_rule_set_version: Literal["rfm-retail-v1"] = "rfm-retail-v1"

    def domain(self) -> AnalyticsRequest:
        comparison = self.comparison
        return AnalyticsRequest(
            result_type=self.result_type,
            semantic_dataset_version_id=self.semantic_dataset_version_id,
            comparison=TimeComparison(
                mode=comparison.mode,
                current_period=Period(**comparison.current_period.model_dump()),
                comparison_period=(
                    None
                    if comparison.comparison_period is None
                    else Period(**comparison.comparison_period.model_dump())
                ),
                timezone=comparison.timezone,
                calendar_version_id=comparison.calendar_version_id,
                incomplete_period_policy=comparison.incomplete_period_policy,
                leap_day_policy=comparison.leap_day_policy,
                iso_week_53_policy=comparison.iso_week_53_policy,
                definition_compatibility_policy=comparison.definition_compatibility_policy,
            ),
            filters=tuple(item.domain() for item in self.filters),
            rfm_score_bins=self.rfm_score_bins,
            rfm_frequency_measure=self.rfm_frequency_measure,
            rfm_segment_rule_set_version=self.rfm_segment_rule_set_version,
        )


class MetricProjection(StrictModel):
    metric_id: str
    metric_order: int
    current_value: str | None
    comparison_value: str | None
    absolute_change: str | None
    percent_change: str | None
    compact_current: str | None
    compact_comparison: str | None
    limitation_codes: list[str]


class MetricGroupProjection(StrictModel):
    group_id: str
    group_order: int
    metrics: list[MetricProjection]


class AnalyticsResultResponse(StrictModel):
    result_id: UUID
    result_type: Literal["sales", "customer", "rfm"]
    semantic_dataset_version_id: UUID
    request_hash: str
    policy_hash: str
    applied_comparison_mode: str
    resolved_current_period: dict[str, str]
    resolved_comparison_period: dict[str, str] | None
    timezone: str
    calendar_version_id: UUID
    comparison_policy_hash: str
    normalized_filter_expression_hash: str
    metric_groups: list[MetricGroupProjection]
    current_coverage: dict[str, int]
    comparison_coverage: dict[str, int] | None
    comparability_status: Literal["comparable", "partial", "not_comparable"]
    limitation_codes: list[str]
    quality: dict[str, object]
    freshness: dict[str, object]
    lineage: dict[str, object]
    rfm_profiles: list[dict[str, object]]
    manifest: dict[str, object]


class AnalyticsResultListResponse(StrictModel):
    results: list[AnalyticsResultResponse]
    visible_count: int = Field(ge=0)


def build_analytics_services(settings: Settings) -> tuple[IdentityService, AnalyticsService]:
    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    identity = IdentityService(PostgresIdentityRepository(connect), bootstrap_secret=None)
    repository = PostgresAnalyticsRepository(connect)
    artifacts = LocalAnalyticsArtifactStore(settings.analytics_artifact_root)
    return identity, AnalyticsService(
        projections=repository,
        artifacts=artifacts,
        results=repository,
        result_store=artifacts,
        sales_semantics=PostgresSalesSemanticRepository(connect),
        sales_results=repository,
        sales_artifacts=SalesArtifactStore(connect, settings.analytics_artifact_root),
    )


def _status_for(code: str) -> int:
    if code == "RESULT_STORAGE_UNAVAILABLE":
        return status.HTTP_503_SERVICE_UNAVAILABLE
    if code == "AUTHENTICATION_FAILED":
        return status.HTTP_401_UNAUTHORIZED
    if code in {"FORBIDDEN", "CSRF_FAILED"}:
        return status.HTTP_403_FORBIDDEN
    if code in {"NOT_FOUND", "SEMANTIC_DATASET_NOT_FOUND"}:
        return status.HTTP_404_NOT_FOUND
    if code.endswith("CONFLICT"):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def create_analytics_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    analytics_service: AnalyticsService | None = None,
) -> FastAPI:
    default_identity, default_analytics = build_analytics_services(settings)
    identity = identity_service or default_identity
    analytics = analytics_service or default_analytics
    app = FastAPI(
        title="Custometry Governed Analytics API",
        version=ANALYTICS_API_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(AnalyticsFailure)
    async def analytics_failure_handler(request: Request, exc: AnalyticsFailure) -> JSONResponse:
        if "/v2/" in request.url.path:
            from custometry_api.analytics.workspace_errors import workspace_error

            return workspace_error(exc.code, exc.__cause__)
        return JSONResponse(status_code=_status_for(exc.code), content={"code": exc.code})

    @app.exception_handler(IdentityFailure)
    async def identity_failure(request: Request, exc: IdentityFailure) -> JSONResponse:
        from custometry_api.analytics.workspace_errors import workspace_error

        return workspace_error(exc.code)

    @app.exception_handler(psycopg.Error)
    async def workspace_storage_failure(request: Request, exc: psycopg.Error) -> JSONResponse:
        from custometry_api.analytics.workspace_errors import workspace_error

        return workspace_error("STORAGE_UNAVAILABLE")

    @app.exception_handler(RequestValidationError)
    async def workspace_validation_failure(request: Request, exc: RequestValidationError):
        if "/v2/" in request.url.path:
            from custometry_api.analytics.workspace_errors import workspace_error

            if any(
                "WORKSPACE_LIMIT_EXCEEDED" in str(e.get("msg", ""))
                or e.get("type") == "too_long"
                and any(k in e.get("loc", ()) for k in ("store_ids", "local_store_ids"))
                for e in exc.errors()
            ):
                return workspace_error("WORKSPACE_LIMIT_EXCEEDED")
            return JSONResponse(
                status_code=422, content={"code": "INVALID_INPUT", "retryable": False}
            )
        return await request_validation_exception_handler(request, exc)

    http_auth = IdentityHTTPAdapter(identity, settings)

    def authenticated(
        request: Request,
        authorization: Annotated[str | None, Header()] = None,
    ) -> Actor:
        _ = authorization
        try:
            return http_auth.authenticate(request)
        except IdentityFailure as exc:
            raise AnalyticsFailure(exc.code) from exc

    from custometry_api.analytics.workspace_router import workspace_router
    from custometry_api.reports.workspace_composition import build_workspace

    app.include_router(
        workspace_router(
            None,
            read_actor=authenticated,
            run_actor=authenticated,
            service_factory=lambda request: build_workspace(settings, http_auth, request)[1],
            prefix="/metric-workspace/v2",
        )
    )

    @app.post(
        "/results",
        response_model=AnalyticsResultResponse,
        operation_id="run_governed_analytics",
    )
    def run_result(
        payload: AnalyticsRunRequest, actor: Actor = Depends(authenticated)
    ) -> AnalyticsResultResponse:
        return AnalyticsResultResponse.model_validate(
            analytics.run(
                workspace_id=actor.workspace_id,
                principal_id=actor.principal_id,
                permissions=actor.permissions,
                request=payload.domain(),
            )
        )

    @app.get(
        "/results/{result_id}",
        response_model=AnalyticsResultResponse,
        operation_id="get_governed_analytics_result",
    )
    def get_result(
        result_id: UUID, actor: Actor = Depends(authenticated)
    ) -> AnalyticsResultResponse:
        return AnalyticsResultResponse.model_validate(
            analytics.get(
                workspace_id=actor.workspace_id,
                principal_id=actor.principal_id,
                permissions=actor.permissions,
                result_id=result_id,
            )
        )

    @app.get(
        "/results",
        response_model=AnalyticsResultListResponse,
        operation_id="list_governed_analytics_results",
    )
    def list_results(
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        actor: Actor = Depends(authenticated),
    ) -> AnalyticsResultListResponse:
        results, count = analytics.list(
            workspace_id=actor.workspace_id,
            principal_id=actor.principal_id,
            permissions=actor.permissions,
            offset=offset,
            limit=limit,
        )
        return AnalyticsResultListResponse(
            results=[AnalyticsResultResponse.model_validate(item) for item in results],
            visible_count=count,
        )

    @app.get(
        "/sales-report-context/v1",
        response_model=SalesContext,
        operation_id="sales_report_context_v1",
    )
    def sales_context(actor: Actor = Depends(authenticated)) -> SalesContext:
        try:
            return SalesContext.model_validate(
                analytics.sales_report_context(
                    workspace_id=actor.workspace_id,
                    principal_id=actor.principal_id,
                    permissions=actor.permissions,
                )
            )
        except psycopg.Error as exc:
            raise AnalyticsFailure("RESULT_STORAGE_UNAVAILABLE") from exc

    @app.post("/sales-reports/v1", response_model=SalesResponse, operation_id="run_sales_report_v1")
    def run_sales_report(
        payload: SalesRunRequest, actor: Actor = Depends(authenticated)
    ) -> SalesResponse:
        try:
            return SalesResponse.model_validate(
                analytics.run_sales_report(
                    workspace_id=actor.workspace_id,
                    principal_id=actor.principal_id,
                    permissions=actor.permissions,
                    request=payload.domain(),
                )
            )
        except psycopg.Error as exc:
            raise AnalyticsFailure("RESULT_STORAGE_UNAVAILABLE") from exc

    @app.get(
        "/sales-reports/v1/{result_id}",
        response_model=SalesResponse,
        operation_id="get_sales_report_v1",
    )
    def get_sales_report(result_id: UUID, actor: Actor = Depends(authenticated)) -> SalesResponse:
        try:
            return SalesResponse.model_validate(
                analytics.get_sales_report(
                    workspace_id=actor.workspace_id,
                    principal_id=actor.principal_id,
                    permissions=actor.permissions,
                    result_id=result_id,
                )
            )
        except psycopg.Error as exc:
            raise AnalyticsFailure("RESULT_STORAGE_UNAVAILABLE") from exc

    _ = (
        analytics_failure_handler,
        identity_failure,
        workspace_storage_failure,
        workspace_validation_failure,
        run_result,
        get_result,
        list_results,
        run_sales_report,
        sales_context,
        get_sales_report,
    )
    return app
