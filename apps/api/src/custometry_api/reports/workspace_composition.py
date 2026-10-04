"""Request-scoped public-port adapters; each access decision reauthenticates."""

from typing import Any
from uuid import UUID
import psycopg
from fastapi import Request
from custometry_api.config import Settings
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.analytics.workspace_access import IdentityWorkspaceAccess
from packages.identity_access.application.resource_access import ResourceAccessService
from packages.identity_access.infrastructure.resource_access import PostgresResourceAccessRepository
from packages.analytics_core.application.workspace_service import WorkspaceAnalyticsService
from packages.analytics_core.application.snapshot_verification import SnapshotResultVerifier
from packages.analytics_core.infrastructure.postgres import PostgresAnalyticsRepository
from packages.artifacts.infrastructure.workspace import WorkspaceArtifactStore
from packages.artifacts.infrastructure.document_snapshots import DocumentSnapshotArtifacts
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from packages.semantic_model.infrastructure.calendar import PostgresCalendarRepository
from packages.semantic_model.application.calendar import WorkspaceCalendarService
from packages.presentation.application.workspace import WorkspaceReportService
from packages.presentation.infrastructure.workspace import PostgresWorkspaceRepository
from packages.contracts.analytics.workspace import (
    WorkspaceAccess,
    WorkspaceCardRequest,
    WorkspaceApplyResult,
    WorkspaceRunRequest,
    WorkspaceResultV2,
    CardResultBinding,
    CardComparisonV1,
)


class WorkspaceResultsAdapter:
    def __init__(
        self,
        service: WorkspaceAnalyticsService,
        verifier: SnapshotResultVerifier,
        dataset_access: IdentityWorkspaceAccess,
    ):
        self.service, self.verifier = service, verifier
        self.dataset_access = dataset_access

    def authorize_base(
        self, workspace: UUID, actor: UUID, owner: UUID, result: dict[str, Any]
    ) -> None:
        self.verifier.verify(
            workspace_id=workspace, principal_id=actor, result_owner=owner, stored=result
        )
        if actor == owner:
            self.dataset_access.legacy_scopes[
                (workspace, actor, UUID(result["semantic_dataset_version_id"]))
            ] = (owner, result["parameters"]["store_id"])

    def resolve(
        self, workspace: UUID, actor: UUID, dataset: UUID, run: bool = False
    ) -> WorkspaceAccess:
        return self.service.resolve_access(workspace, actor, dataset, "run" if run else "read")

    def apply(
        self, workspace: UUID, actor: UUID, cards: list[WorkspaceCardRequest]
    ) -> WorkspaceApplyResult:
        return self.service.apply(workspace_id=workspace, principal_id=actor, cards=cards)

    def verify(
        self, workspace: UUID, actor: UUID, query: WorkspaceRunRequest, result: UUID
    ) -> WorkspaceResultV2:
        return self.service.verify_query(
            workspace_id=workspace, principal_id=actor, request=query, result_id=result
        )

    def compare(
        self,
        workspace: UUID,
        actor: UUID,
        dataset: UUID,
        left: CardResultBinding,
        right: CardResultBinding | None,
    ) -> CardComparisonV1:
        return self.service.compare(
            workspace_id=workspace, principal_id=actor, dataset_id=dataset, left=left, right=right
        )

    def verify_comparison(
        self, workspace: UUID, actor: UUID, dataset: UUID, value: CardComparisonV1
    ) -> None:
        self.service.get(
            workspace_id=workspace,
            principal_id=actor,
            dataset_id=dataset,
            result_id=value.left.result.result_id,
        )
        self.service.get(
            workspace_id=workspace,
            principal_id=actor,
            dataset_id=dataset,
            result_id=value.right.result.result_id,
        )
        self.service.artifacts.verify_workspace(
            workspace_id=workspace, payload=value.model_dump(mode="json")
        )

    def legacy(
        self, workspace: UUID, actor: UUID, owner: UUID, result: dict[str, Any]
    ) -> WorkspaceAccess:
        return self.verifier.verify(
            workspace_id=workspace, principal_id=actor, result_owner=owner, stored=result
        )


def build_workspace(
    settings: Settings, auth: IdentityHTTPAdapter, request: Request
) -> tuple[WorkspaceReportService, WorkspaceAnalyticsService]:
    def connect() -> psycopg.Connection[Any]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    access = ResourceAccessService(
        PostgresResourceAccessRepository(connect), lambda: auth.authenticate(request)
    )
    semantics = PostgresSalesSemanticRepository(connect)
    results = PostgresAnalyticsRepository(connect)
    artifacts = WorkspaceArtifactStore(connect, settings.analytics_artifact_root)
    calendars = WorkspaceCalendarService(PostgresCalendarRepository(connect))
    dataset_access = IdentityWorkspaceAccess(access, semantics, artifacts)
    analytics = WorkspaceAnalyticsService(
        semantics=semantics,
        results=results,
        artifacts=artifacts,
        calendars=calendars,
        access=dataset_access,
    )
    presentation = WorkspaceReportService(
        PostgresWorkspaceRepository(connect),
        WorkspaceResultsAdapter(
            analytics,
            SnapshotResultVerifier(analytics, results, artifacts, dataset_access.resolve_legacy),
            dataset_access,
        ),
        access,
        DocumentSnapshotArtifacts(connect, settings.analytics_artifact_root),
        calendars,
    )
    return presentation, analytics


def guarded_legacy(
    settings: Settings, auth: IdentityHTTPAdapter, request: Request, brand: dict[str, Any]
):
    """Preserve v1 bytes while applying the current creator/object/data boundary."""
    from custometry_api.analytics.router import build_analytics_services
    from packages.presentation.application.reports import ReportService
    from packages.presentation.infrastructure.postgres import PostgresReportRepository
    from packages.contracts.presentation import PresentationFailure, SaveRequest

    workspace, _ = build_workspace(settings, auth, request)
    _, analytics = build_analytics_services(settings)
    auth.authenticate(request)

    class GuardedLegacy(ReportService):
        def _result(
            self,
            workspace_id: UUID,
            principal_id: UUID,
            permissions: frozenset[str],
            result_id: UUID,
        ) -> dict[str, Any]:
            result = super()._result(workspace_id, principal_id, permissions, result_id)
            workspace.results.legacy(workspace_id, principal_id, principal_id, result)
            return result

        def get(
            self,
            *,
            workspace_id: UUID,
            principal_id: UUID,
            permissions: frozenset[str],
            report_id: UUID,
            snapshot_id: UUID | None = None,
        ) -> dict[str, Any]:
            self._require(permissions)
            saved = workspace.visible(workspace_id, principal_id, report_id, snapshot_id)
            if saved["contract_version"] != "draft-report/v1":
                raise PresentationFailure("REPORT_VERSION_UPGRADE_REQUIRED")
            return saved

        def save(
            self,
            *,
            workspace_id: UUID,
            principal_id: UUID,
            permissions: frozenset[str],
            request: SaveRequest,
            report_id: UUID | None = None,
        ) -> dict[str, Any]:
            def check() -> None:
                current = auth.authenticate(http_request)
                if (
                    current.principal_id != principal_id
                    or not {"report.manage", "report.read", "analysis.read"} <= current.permissions
                ):
                    raise PresentationFailure("FORBIDDEN")
                if report_id is not None:
                    workspace.guard(workspace_id, principal_id, report_id, write=True)
                self._result(workspace_id, principal_id, current.permissions, request.result_id)

            check()
            self._repository = PostgresReportRepository(
                workspace.repository._connect, checkpoint=check
            )
            saved = super().save(
                workspace_id=workspace_id,
                principal_id=principal_id,
                permissions=permissions,
                request=request,
                report_id=report_id,
            )
            check()
            workspace.guard(workspace_id, principal_id, UUID(saved["report_id"]), write=True)
            return saved

        def list(
            self,
            *,
            workspace_id: UUID,
            principal_id: UUID,
            permissions: frozenset[str],
            offset: int,
            limit: int,
        ) -> dict[str, Any]:
            from packages.contracts.analytics import AnalyticsFailure

            self._require(permissions)
            values: list[dict[str, Any]] = []
            for report_id in workspace.repository.all_candidates(workspace_id):
                try:
                    saved = workspace.visible(workspace_id, principal_id, report_id)
                except (PresentationFailure, AnalyticsFailure) as exc:
                    if exc.code in {"FORBIDDEN", "NOT_FOUND", "ARTIFACT_NOT_VISIBLE"}:
                        continue
                    raise
                values.append(
                    {
                        **{
                            k: saved[k]
                            for k in (
                                "report_id",
                                "revision",
                                "version_id",
                                "snapshot_id",
                                "saved_at",
                            )
                        },
                        "title": saved["title"]
                        if saved["contract_version"] == "draft-report/v1"
                        else saved["composition"]["definition"]["title"],
                        "lifecycle": "owned_draft_preview",
                    }
                )
            values.sort(key=lambda r: (r["saved_at"], r["report_id"]), reverse=True)
            return {"reports": values[offset : offset + limit], "visible_count": len(values)}

    http_request = request
    return GuardedLegacy(
        PostgresReportRepository(workspace.repository._connect),
        analytics,
        workspace.artifacts,
        brand,
    )
