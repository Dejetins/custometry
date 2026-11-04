"""All v2 report operations share request-authenticated object/data enforcement."""

from uuid import UUID
from typing import Any, cast
from fastapi import APIRouter, Request
from custometry_api.reports.encoding import report_json_response
from custometry_api.config import Settings
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.reports.workspace_composition import build_workspace
from custometry_api.reports.prepared import PreparedAnalyticsService
from packages.contracts.analytics.workspace import WorkspaceResultV2
from packages.contracts.presentation.workspace import (
    WorkspaceEditorResponse,
    NewWorkspaceRequest,
    NewWorkspaceResponse,
    CreatorApplyRequest,
    ReportActor,
    WorkspaceApplyRequest,
    WorkspaceApplyResponse,
    WorkspaceSaveRequest,
    WorkspaceReportResponse,
    SaveViewRequest,
    SavedViewV1,
)


def workspace_reports_router(settings: Settings, auth: IdentityHTTPAdapter, brand: dict[str, Any]) -> APIRouter:
    router = APIRouter(prefix="/v2")

    def services(request: Request):
        actor = auth.authenticate(request)
        service, analytics = build_workspace(settings, auth, request)
        return actor, service, analytics

    def open_editor(report_id: UUID, request: Request, snapshot_id: UUID | None = None):
        a, service, analytics = services(request)
        editor = service.get(a.workspace_id, a.principal_id, report_id, snapshot_id)
        ready: list[WorkspaceResultV2] = []
        # These results have already been checked while verifying this document.
        # Reuse that request's objects; no cross-request cache or extra compute.
        if isinstance(editor.report.root, WorkspaceReportResponse) and editor.definition is not None:
            definition = editor.definition
            active = next((w for w in definition.worksets if w.workset_id == definition.default_workset_id), None)
            cards: set[UUID] = {c.card_id for c in active.cards} if active is not None else set()
            ids = dict.fromkeys(b.result.result_id for b in editor.report.root.composition.bindings_by_card if b.card_id in cards)
            size = 2
            for result_id in list(ids) if len(ids) <= 32 else []:
                result = analytics.get(workspace_id=a.workspace_id, principal_id=a.principal_id,
                    dataset_id=definition.semantic_dataset_version_id, result_id=result_id)
                result_bytes = cast(PreparedAnalyticsService, analytics).encoded_size(result) + (1 if ready else 0)
                if size + result_bytes > 2 * 1024 * 1024:
                    ready.clear()
                    break
                ready.append(result)
                size += result_bytes
        response = WorkspaceEditorResponse(
            report=editor.report, definition=editor.definition, base_definition=editor.base_definition,
            capabilities=editor.capabilities, saved_view_revision=editor.saved_view_revision,
            ready_results=ready,
            actor=ReportActor(workspace_id=a.workspace_id, principal_id=a.principal_id, permissions=sorted(a.permissions)),
        )
        # Encode the validated model directly; avoid another full Python dict tree
        # and stdlib JSON pass over the embedded immutable results.
        return report_json_response(response.model_dump_json(), request)

    @router.post("/new/prepare", response_model=NewWorkspaceResponse)
    def prepare_new(body: NewWorkspaceRequest, request: Request):
        a, service, _ = services(request)
        definition = service.new_definition(a.workspace_id, a.principal_id, body, brand)
        return NewWorkspaceResponse(definition=definition, actor=ReportActor(
            workspace_id=a.workspace_id, principal_id=a.principal_id, permissions=sorted(a.permissions)))

    @router.post("/new/apply", response_model=WorkspaceApplyResponse)
    def apply_new(body: CreatorApplyRequest, request: Request):
        a, service, _ = services(request)
        return service.apply_new(a.workspace_id, a.principal_id, body)

    @router.post("/new/versions", response_model=WorkspaceReportResponse)
    def save_new(body: WorkspaceSaveRequest, request: Request):
        from packages.contracts.presentation import PresentationFailure
        if body.expected_revision != 0:
            raise PresentationFailure("REVISION_CONFLICT")
        a, service, _ = services(request)
        return service.save(a.workspace_id, a.principal_id, body.definition.report_id, body)

    @router.get("/{report_id}", response_model=WorkspaceEditorResponse)
    def get(report_id: UUID, request: Request):
        return open_editor(report_id, request)

    @router.get("/{report_id}/snapshots/{snapshot_id}", response_model=WorkspaceEditorResponse)
    def snapshot(report_id: UUID, snapshot_id: UUID, request: Request):
        return open_editor(report_id, request, snapshot_id)

    @router.post("/{report_id}/apply", response_model=WorkspaceApplyResponse)
    def apply(report_id: UUID, body: WorkspaceApplyRequest, request: Request):
        a, s, _ = services(request)
        return s.apply(a.workspace_id, a.principal_id, report_id, body)

    @router.post("/{report_id}/versions", response_model=WorkspaceReportResponse)
    def save(report_id: UUID, body: WorkspaceSaveRequest, request: Request):
        a, s, _ = services(request)
        return s.save(a.workspace_id, a.principal_id, report_id, body)

    @router.get("/{report_id}/saved-views", response_model=list[SavedViewV1])
    def views(report_id: UUID, request: Request):
        a, s, _ = services(request)
        return s.views(a.workspace_id, a.principal_id, report_id)

    @router.post("/{report_id}/saved-views", response_model=SavedViewV1)
    def create_view(report_id: UUID, body: SaveViewRequest, request: Request):
        a, s, _ = services(request)
        return s.save_view(a.workspace_id, a.principal_id, report_id, body)

    @router.post("/{report_id}/saved-views/{saved_view_id}/versions", response_model=SavedViewV1)
    def save_view(report_id: UUID, saved_view_id: UUID, body: SaveViewRequest, request: Request):
        a, s, _ = services(request)
        return s.save_view(a.workspace_id, a.principal_id, report_id, body, saved_view_id)

    _ = get, snapshot, apply, save, views, create_view, save_view, prepare_new, apply_new, save_new
    return router
