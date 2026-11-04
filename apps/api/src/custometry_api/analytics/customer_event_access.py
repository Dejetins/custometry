"""Current Identity/Artifact admission for the explicit observed-customer universe."""

from collections.abc import Sequence
from uuid import UUID
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import (
    FilterArtifactAdmission,
    FlatInputGrant,
    FlatPredicate,
    FlatBoolean,
    FilterValue,
)
from packages.contracts.analytics.customer_events import (
    CustomerEventsSemanticPort,
    RootRestrictedSequenceGrant,
)
from packages.contracts.analytics.relational_filters import RelationalResourcePolicy
from packages.contracts.identity.access import ResourceAccessPort
from packages.contracts.semantic.filter_fields import Operator
from packages.contracts.semantic.nullable_relationships import NullableFilterRelationshipVersion


class PublishedCustomerEventAccess:
    def __init__(
        self,
        *,
        identity: ResourceAccessPort,
        semantics: CustomerEventsSemanticPort,
        artifacts: FilterArtifactAdmission,
        resource_policy: RelationalResourcePolicy,
        require_run: bool = True,
    ):
        self.identity, self.semantics, self.artifacts = identity, semantics, artifacts
        self.resource_policy, self.require_run = resource_policy, require_run

    def current_decision(self, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID):
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
        return decision

    def recheck(
        self,
        *,
        workspace_id: UUID,
        actor_id: UUID,
        dataset_version_id: UUID,
        grant: RootRestrictedSequenceGrant,
    ) -> None:
        """Re-read Identity after additional immutable metadata reads, without new metadata IO."""
        decision = self.current_decision(workspace_id, actor_id, dataset_version_id)
        if any(e.policy_revision != decision.policy_hash for e in grant.entities):
            raise AnalyticsFailure("FILTER_POLICY_CHANGED")

    def authorize(
        self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID
    ) -> RootRestrictedSequenceGrant:
        decision = self.current_decision(workspace_id, actor_id, dataset_version_id)
        published = self.semantics.customer_events_projection(
            workspace_id=workspace_id, dataset_version_id=dataset_version_id
        )
        if (
            tuple(e.registry.entity for e in published.entities)
            != ("Customer", "Receipt", "ReceiptItem")
            or len(published.relationships) != 2
            or tuple(
                (r.relationship.parent_entity, r.relationship.child_entity)
                for r in published.relationships
            )
            != (("Customer", "Receipt"), ("Receipt", "ReceiptItem"))
        ):
            raise AnalyticsFailure("FILTER_CUSTOMER_EVENT_BINDING")
        customer_edge = published.relationships[0].relationship
        if (
            not isinstance(customer_edge, NullableFilterRelationshipVersion)
            or customer_edge.nullable_child_fields != ("Receipt.customer_id",)
            or (
                published.universe.root_entity,
                published.universe.relationship_id,
                published.universe.relationship_version_id,
            )
            != ("Customer", customer_edge.relationship_id, customer_edge.version_id)
        ):
            raise AnalyticsFailure("FILTER_CUSTOMER_EVENT_BINDING")
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

            def condition(name: str, operator: Operator, values: Sequence[str] = ()):
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
        return RootRestrictedSequenceGrant(
            entities=tuple(entities),
            relationships=published.relationships,
            resource_policy=self.resource_policy,
            counts=published.counts,
            events=published.events,
            root_restrictions=(published.universe,),
        )
