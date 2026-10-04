"""All v2 report operations share request-authenticated object/data enforcement."""

from uuid import UUID
from fastapi import APIRouter, Request
from custometry_api.config import Settings
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.reports.workspace_composition import build_workspace
from packages.contracts.presentation.workspace import (
    WorkspaceEditorResponse,
    WorkspaceApplyRequest,
    WorkspaceApplyResponse,
    WorkspaceSaveRequest,
    WorkspaceReportResponse,
    SaveViewRequest,
    SavedViewV1,
)


def workspace_reports_router(settings: Settings, auth: IdentityHTTPAdapter) -> APIRouter:
    router = APIRouter(prefix="/v2")

    def services(request: Request):
        actor = auth.authenticate(request)
        service, _ = build_workspace(settings, auth, request)
        return actor, service

    @router.get("/{report_id}", response_model=WorkspaceEditorResponse)
    def get(report_id: UUID, request: Request):
        a, s = services(request)
        return s.get(a.workspace_id, a.principal_id, report_id)

    @router.get("/{report_id}/snapshots/{snapshot_id}", response_model=WorkspaceEditorResponse)
    def snapshot(report_id: UUID, snapshot_id: UUID, request: Request):
        a, s = services(request)
        return s.get(a.workspace_id, a.principal_id, report_id, snapshot_id)

    @router.post("/{report_id}/apply", response_model=WorkspaceApplyResponse)
    def apply(report_id: UUID, body: WorkspaceApplyRequest, request: Request):
        a, s = services(request)
        return s.apply(a.workspace_id, a.principal_id, report_id, body)

    @router.post("/{report_id}/versions", response_model=WorkspaceReportResponse)
    def save(report_id: UUID, body: WorkspaceSaveRequest, request: Request):
        a, s = services(request)
        return s.save(a.workspace_id, a.principal_id, report_id, body)

    @router.get("/{report_id}/saved-views", response_model=list[SavedViewV1])
    def views(report_id: UUID, request: Request):
        a, s = services(request)
        return s.views(a.workspace_id, a.principal_id, report_id)

    @router.post("/{report_id}/saved-views", response_model=SavedViewV1)
    def create_view(report_id: UUID, body: SaveViewRequest, request: Request):
        a, s = services(request)
        return s.save_view(a.workspace_id, a.principal_id, report_id, body)

    @router.post("/{report_id}/saved-views/{saved_view_id}/versions", response_model=SavedViewV1)
    def save_view(report_id: UUID, saved_view_id: UUID, body: SaveViewRequest, request: Request):
        a, s = services(request)
        return s.save_view(a.workspace_id, a.principal_id, report_id, body, saved_view_id)

    _ = get, snapshot, apply, save, views, create_view, save_view
    return router
