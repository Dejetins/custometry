"""Compose current Identity, Semantic and Artifact public ports for flat execution."""

from __future__ import annotations

from uuid import UUID

from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import (
    FilterArtifactAdmission,
    FilterResourcePolicy,
    FilterValue,
    FlatBoolean,
    FlatInputGrant,
    FlatPredicate,
    RetailFilterSemanticPort,
)
from packages.contracts.identity.access import ResourceAccessPort


class PublishedRetailFilterAccess:
    """Server-only composition. Not a client-configurable authorization adapter."""

    def __init__(
        self,
        *,
        identity: ResourceAccessPort,
        semantics: RetailFilterSemanticPort,
        artifacts: FilterArtifactAdmission,
        resource_policy: FilterResourcePolicy,
        require_run: bool = True,
    ):
        self.identity, self.semantics, self.artifacts = identity, semantics, artifacts
        self.resource_policy = resource_policy
        self.require_run = require_run

    def authorize(
        self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID
    ) -> FlatInputGrant:
        decision = self.identity.resolve_resource(
            workspace_id=workspace_id,
            principal_id=actor_id,
            resource_type="analysis",
            resource_id=dataset_version_id,
            action="run" if self.require_run else "view_snapshot",
        )
        if not decision.allowed or not ({"analysis.read", "analysis.run"} if self.require_run else {"analysis.read"}) <= decision.permissions:
            raise AnalyticsFailure("FORBIDDEN")
        published = self.semantics.retail_filter_projection(
            workspace_id=workspace_id, dataset_version_id=dataset_version_id
        )
        if published.registry.dataset_version_id != dataset_version_id:
            raise AnalyticsFailure("FILTER_INPUT_BINDING")
        binding = self.artifacts.admit_filter_input(
            workspace_id=workspace_id,
            artifact_id=published.artifact_id,
            entity=published.registry.entity,
            content_hash=published.content_hash,
        )
        if (
            binding.workspace_id != workspace_id
            or binding.entity != published.registry.entity
            or binding.artifact_id != published.artifact_id
            or binding.content_hash != published.content_hash
        ):
            raise AnalyticsFailure("FILTER_INPUT_BINDING")
        fields = {field.field_id: field for field in published.registry.fields}
        namespace = fields["Receipt.source_system_id"]
        store = fields["Receipt.store_id"]
        clauses = [
            FlatPredicate(
                field_id=namespace.field_id,
                field_version_id=namespace.version_id,
                operator="eq",
                values=(FilterValue(data_type="string", value=published.source_namespace),),
            )
        ]
        if decision.store_ids is not None:
            if decision.store_ids:
                clauses.append(
                    FlatPredicate(
                        field_id=store.field_id,
                        field_version_id=store.version_id,
                        operator="in",
                        values=tuple(
                            FilterValue(data_type="string", value=v)
                            for v in sorted(set(decision.store_ids))
                        ),
                    )
                )
            else:
                # An explicitly empty authorized universe must not mean unrestricted.
                clauses.extend(
                    FlatPredicate(
                        field_id=store.field_id, field_version_id=store.version_id, operator=op
                    )
                    for op in ("is_null", "is_not_null")
                )
        return FlatInputGrant(
            workspace_id=workspace_id,
            actor_id=actor_id,
            policy_revision=decision.policy_hash,
            binding=binding,
            registry=published.registry,
            resource_policy=self.resource_policy,
            row_ceiling=FlatBoolean(kind="and", children=tuple(clauses)),
            row_id_column=published.row_id_column,
        )
