"""Current Identity/Artifact composition for the one published receipt-child edge."""

from __future__ import annotations
from uuid import UUID
from collections.abc import Sequence
from packages.contracts.semantic.filter_fields import Operator
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import (
    FilterArtifactAdmission,
    FlatInputGrant,
    FlatPredicate,
    FlatBoolean,
    FilterValue,
)
from packages.contracts.analytics.relational_filters import (
    RelationalInputGrant,
    RelationalResourcePolicy,
)
from packages.contracts.analytics.retail_relational import RetailRelationsSemanticPort
from packages.contracts.identity.access import ResourceAccessPort


class PublishedRetailRelationalAccess:
    def __init__(
        self,
        *,
        identity: ResourceAccessPort,
        semantics: RetailRelationsSemanticPort,
        artifacts: FilterArtifactAdmission,
        resource_policy: RelationalResourcePolicy,
        require_run: bool = True,
    ):
        self.identity, self.semantics, self.artifacts = identity, semantics, artifacts
        self.resource_policy, self.require_run = resource_policy, require_run

    def authorize(
        self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID
    ) -> RelationalInputGrant:
        decision = self.identity.resolve_resource(
            workspace_id=workspace_id,
            principal_id=actor_id,
            resource_type="analysis",
            resource_id=dataset_version_id,
            action="run" if self.require_run else "view_snapshot",
        )
        required = {"analysis.read", "analysis.run"} if self.require_run else {"analysis.read"}
        if not decision.allowed or not required <= decision.permissions:
            raise AnalyticsFailure("FORBIDDEN")
        published = self.semantics.retail_relational_projection(
            workspace_id=workspace_id, dataset_version_id=dataset_version_id
        )
        if (
            tuple(e.registry.entity for e in published.entities) != ("Receipt", "ReceiptItem")
            or len(published.relationships) != 1
            or (
                published.relationships[0].relationship.parent_entity,
                published.relationships[0].relationship.child_entity,
            )
            != ("Receipt", "ReceiptItem")
        ):
            raise AnalyticsFailure("FILTER_RELATIONSHIP_BINDING")
        entities: list[FlatInputGrant] = []
        for entity in published.entities:
            registry = entity.registry
            if registry.dataset_version_id != dataset_version_id:
                raise AnalyticsFailure("FILTER_INPUT_BINDING")
            binding = self.artifacts.admit_filter_input(
                workspace_id=workspace_id,
                artifact_id=entity.artifact_id,
                entity=registry.entity,
                content_hash=entity.content_hash,
            )
            if (
                binding.workspace_id,
                binding.artifact_id,
                binding.entity,
                binding.content_hash,
            ) != (workspace_id, entity.artifact_id, registry.entity, entity.content_hash):
                raise AnalyticsFailure("FILTER_INPUT_BINDING")
            fields = {f.column: f for f in registry.fields}

            def condition(
                name: str, operator: Operator, values: Sequence[str] = ()
            ) -> FlatPredicate:
                f = fields[name]
                return FlatPredicate(
                    field_id=f.field_id,
                    field_version_id=f.version_id,
                    operator=operator,
                    values=tuple(FilterValue(data_type="string", value=v) for v in values),
                )

            clauses = [condition("source_system_id", "eq", (entity.source_namespace,))]
            if registry.entity == "Receipt" and decision.store_ids is not None:
                if decision.store_ids:
                    clauses.append(condition("store_id", "in", sorted(set(decision.store_ids))))
                else:
                    clauses.extend(condition("store_id", op) for op in ("is_null", "is_not_null"))
            # Child output is never exposed independently: every predicate is
            # correlated to an authorized Receipt. No child-root API or facet.
            entities.append(
                FlatInputGrant(
                    workspace_id=workspace_id,
                    actor_id=actor_id,
                    policy_revision=decision.policy_hash,
                    binding=binding,
                    registry=registry,
                    resource_policy=self.resource_policy,
                    row_id_column=entity.row_id_column,
                    row_ceiling=FlatBoolean(kind="and", children=tuple(clauses)),
                )
            )
        return RelationalInputGrant(tuple(entities), published.relationships, self.resource_policy,
                                    (published.legacy_registry_version_id,))
