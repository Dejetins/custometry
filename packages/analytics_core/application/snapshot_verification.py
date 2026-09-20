"""Authorized exact legacy result projection for a Presentation-checked base snapshot.

This internal public port has no HTTP endpoint accepting an arbitrary result owner.
Presentation supplies a stored base binding only after checking report access.
"""

from typing import Any
from collections.abc import Callable
from packages.contracts.analytics.workspace import WorkspaceAccess
from uuid import UUID
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sales_report import SalesArtifactPort, SalesResultPort
from packages.analytics_core.application.workspace_service import WorkspaceAnalyticsService


class SnapshotResultVerifier:
    def __init__(
        self,
        workspace: WorkspaceAnalyticsService,
        results: SalesResultPort,
        artifacts: SalesArtifactPort,
        access: Callable[[UUID, UUID, UUID, UUID], WorkspaceAccess],
    ):
        self.workspace, self.results, self.artifacts = workspace, results, artifacts
        self.access = access

    def verify(
        self, *, workspace_id: UUID, principal_id: UUID, result_owner: UUID, stored: dict[str, Any]
    ) -> WorkspaceAccess:
        dataset = UUID(stored["semantic_dataset_version_id"])
        access = self.access(workspace_id, principal_id, dataset, result_owner)
        actual = self.results.get_sales(
            workspace_id=workspace_id,
            principal_id=result_owner,
            result_id=UUID(stored["result_id"]),
        )
        if actual != stored or actual["schema_version"] != "sales-report/v1":
            raise AnalyticsFailure("RESULT_BINDING_MISMATCH")
        _, inputs = self.workspace.verified_inputs(access)
        store = actual["parameters"]["store_id"]
        scope = {str(s["store_id"]) for s in inputs["Store"]} if store is None else {store}
        if not scope <= set(access.allowed_store_ids):
            raise AnalyticsFailure("FORBIDDEN")
        self.artifacts.verify_sales(workspace_id=workspace_id, payload=actual)
        if self.access(workspace_id, principal_id, dataset, result_owner) != access:
            raise AnalyticsFailure("FORBIDDEN")
        return access
