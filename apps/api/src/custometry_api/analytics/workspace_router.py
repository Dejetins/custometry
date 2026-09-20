"""Unmounted v2 adapters. S03 must supply current report/object/data access and CSRF."""

from __future__ import annotations
from typing import Any, Callable
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from packages.analytics_core.application.workspace_service import WorkspaceAnalyticsService
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.workspace import (
    WorkspaceRunRequest,
    WorkspaceResultV2,
    CardResultBinding,
    CardComparisonV1,
)
from packages.contracts.semantic import Strict, CalendarFailure


class CompareRequest(Strict):
    semantic_dataset_version_id: UUID
    left: CardResultBinding
    right: CardResultBinding | None


def workspace_router(
    service: WorkspaceAnalyticsService,
    *,
    read_actor: Callable[..., Any],
    run_actor: Callable[..., Any],
) -> APIRouter:
    """No default auth dependency; never mounted by create_app in S02.

    S03 supplies report/object-aware dependencies; run_actor must also check CSRF.
    The service separately resolves current dataset access before/after all work.
    """
    router = APIRouter(prefix="/workspace/v2")

    def error(exc: AnalyticsFailure | CalendarFailure) -> JSONResponse:
        code = 403 if exc.code == "FORBIDDEN" else 404 if exc.code == "NOT_FOUND" else 409
        return JSONResponse(status_code=code, content={"code": exc.code})

    @router.post("/results", response_model=WorkspaceResultV2)
    def run(body: WorkspaceRunRequest, actor: Any = Depends(run_actor)) -> Any:
        try:
            return service.run(
                workspace_id=actor.workspace_id, principal_id=actor.principal_id, request=body
            )
        except (AnalyticsFailure, CalendarFailure) as exc:
            return error(exc)

    @router.get("/datasets/{dataset_id}/results/{result_id}", response_model=WorkspaceResultV2)
    def result(dataset_id: UUID, result_id: UUID, actor: Any = Depends(read_actor)) -> Any:
        try:
            return service.get(
                workspace_id=actor.workspace_id,
                principal_id=actor.principal_id,
                dataset_id=dataset_id,
                result_id=result_id,
            )
        except (AnalyticsFailure, CalendarFailure) as exc:
            return error(exc)

    @router.get("/datasets/{dataset_id}/context")
    def context(dataset_id: UUID, actor: Any = Depends(read_actor)) -> Any:
        try:
            return service.context(
                workspace_id=actor.workspace_id,
                principal_id=actor.principal_id,
                dataset_id=dataset_id,
            )
        except (AnalyticsFailure, CalendarFailure) as exc:
            return error(exc)

    @router.get("/datasets/{dataset_id}/catalog")
    def catalog(dataset_id: UUID, actor: Any = Depends(read_actor)) -> Any:
        try:
            return {
                "metrics": service.context(
                    workspace_id=actor.workspace_id,
                    principal_id=actor.principal_id,
                    dataset_id=dataset_id,
                )["metrics"]
            }
        except (AnalyticsFailure, CalendarFailure) as exc:
            return error(exc)

    @router.post("/comparisons", response_model=CardComparisonV1)
    def compare(body: CompareRequest, actor: Any = Depends(run_actor)) -> Any:
        try:
            return service.compare(
                workspace_id=actor.workspace_id,
                principal_id=actor.principal_id,
                dataset_id=body.semantic_dataset_version_id,
                left=body.left,
                right=body.right,
            )
        except (AnalyticsFailure, CalendarFailure) as exc:
            return error(exc)

    _ = (run, result, context, catalog, compare)  # decorators register these handlers
    return router
