"""Compose public Identity, Semantic and Artifact ports into Analytics scope."""

from typing import Literal
from uuid import UUID
from packages.contracts.identity.access import ResourceAccessPort
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import FilterResourcePolicy
from packages.contracts.analytics.retail_filter import BoundedSalesInputPort
from packages.contracts.analytics.workspace import WorkspaceAccess
from packages.contracts.analytics.sales_report import SalesSemanticPort, SalesArtifactPort


class IdentityWorkspaceAccess:
    def __init__(
        self,
        identity: ResourceAccessPort,
        semantics: SalesSemanticPort,
        artifacts: SalesArtifactPort,
        *, store_reader: BoundedSalesInputPort | None = None,
        store_policy: FilterResourcePolicy | None = None,
    ):
        self.identity, self.semantics, self.artifacts = identity, semantics, artifacts
        self.store_reader, self.store_policy = store_reader, store_policy
        self._stores: dict[tuple[UUID, UUID], set[str]] = {}
        self.legacy_scopes: dict[tuple[UUID, UUID, UUID], tuple[UUID, str | None]] = {}

    def resolve(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        dataset_id: UUID,
        action: Literal["read", "run"],
    ) -> WorkspaceAccess:
        legacy = self.legacy_scopes.get((workspace_id, principal_id, dataset_id))
        decision = self.identity.resolve_resource(
            workspace_id=workspace_id,
            principal_id=principal_id,
            resource_type="analysis",
            resource_id=dataset_id,
            action="run" if action == "run" else "view_snapshot",
            legacy_creator=legacy[0] if legacy else None,
        )
        if not decision.allowed:
            raise AnalyticsFailure("FORBIDDEN")
        stores = self.known_stores(workspace_id, dataset_id).copy()
        if legacy is not None and legacy[1] is not None:
            stores &= {legacy[1]}
        if decision.store_ids is not None:
            stores &= set(decision.store_ids)
        return WorkspaceAccess(
            workspace_id=workspace_id,
            principal_id=principal_id,
            semantic_dataset_version_id=dataset_id,
            policy_hash=decision.policy_hash,
            allowed_store_ids=sorted(stores),
            permissions=decision.permissions,
        )

    def resolve_legacy(
        self, workspace: UUID, actor: UUID, dataset: UUID, owner: UUID
    ) -> WorkspaceAccess:
        decision = self.identity.resolve_resource(
            workspace_id=workspace,
            principal_id=actor,
            resource_type="analysis",
            resource_id=dataset,
            action="view_snapshot",
            legacy_creator=owner,
        )
        if not decision.allowed:
            raise AnalyticsFailure("FORBIDDEN")
        stores = self.known_stores(workspace, dataset).copy()
        if decision.store_ids is not None:
            stores &= set(decision.store_ids)
        return WorkspaceAccess(
            workspace_id=workspace,
            principal_id=actor,
            semantic_dataset_version_id=dataset,
            policy_hash=decision.policy_hash,
            allowed_store_ids=sorted(stores),
            permissions=decision.permissions,
        )

    def known_stores(self, workspace: UUID, dataset: UUID) -> set[str]:
        # Request-scoped memo of immutable admitted Store identity, never a policy cache.
        key = (workspace, dataset)
        if key not in self._stores:
            source = self.semantics.sales_projection(workspace_id=workspace, version_id=dataset)
            bindings = [b for b in source["bindings"] if b["entity"] == "Store"]
            if self.store_reader is not None and self.store_policy is not None:
                inputs = self.store_reader.read_bounded_sales_inputs(workspace_id=workspace,
                    bindings=bindings, supporting_artifacts=[], policy=self.store_policy,
                    metadata_only=True)
            else:
                inputs = self.artifacts.read_sales_inputs(workspace_id=workspace,
                    bindings=bindings, supporting_artifacts=[])
            self._stores[key] = {str(s["store_id"]) for s in inputs["Store"]}
        return self._stores[key]
