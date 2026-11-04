"""Verify the published receipt registry bridge against admitted customer events."""

from uuid import UUID
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.receipt_cohorts import ReceiptCohortGrant
from custometry_api.analytics.customer_event_access import PublishedCustomerEventAccess
from packages.contracts.analytics.retail_aggregate import RetailAggregatesSemanticPort


class PublishedReceiptCohortAccess:
    def __init__(self, base: PublishedCustomerEventAccess, semantics: RetailAggregatesSemanticPort):
        self.base, self.semantics = base, semantics

    def authorize(
        self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID
    ) -> ReceiptCohortGrant:
        grant = self.base.authorize(
            workspace_id=workspace_id, actor_id=actor_id, dataset_version_id=dataset_version_id
        )
        if len(grant.root_restrictions) != 1:
            raise AnalyticsFailure("FILTER_COHORT_BINDING")
        source = self.semantics.retail_aggregate_projection(
            workspace_id=workspace_id, dataset_version_id=dataset_version_id
        )
        if (
            tuple(e.registry.entity for e in source.relations.entities)
            != ("Receipt", "ReceiptItem")
            or tuple(r for r in grant.relationships if r.relationship.parent_entity == "Receipt")
            != source.relations.relationships
            or grant.counts != source.counts
        ):
            raise AnalyticsFailure("FILTER_COHORT_REGISTRY_BRIDGE")
        offered = {e.registry.entity: e for e in grant.entities}
        for old in source.relations.entities:
            current = offered.get(old.registry.entity)
            if (
                current is None
                or current.binding.artifact_id != old.artifact_id
                or current.binding.content_hash != old.content_hash
                or current.row_id_column != old.row_id_column
                or current.registry.dataset_version_id != old.registry.dataset_version_id
                or any(f not in current.registry.fields for f in old.registry.fields)
                or (old.registry.entity == "ReceiptItem" and current.registry != old.registry)
            ):
                raise AnalyticsFailure("FILTER_COHORT_REGISTRY_BRIDGE")
        self.base.recheck(
            workspace_id=workspace_id,
            actor_id=actor_id,
            dataset_version_id=dataset_version_id,
            grant=grant,
        )
        return ReceiptCohortGrant(
            entities=grant.entities,
            relationships=grant.relationships,
            resource_policy=grant.resource_policy,
            counts=grant.counts,
            events=grant.events,
            compatibility_registry_versions=(source.relations.legacy_registry_version_id,),
            root_restrictions=grant.root_restrictions,
            facet_fields=tuple(
                (e.registry.entity, f.field_id)
                for e in source.relations.entities
                for f in e.registry.fields
                if f.column not in {"customer_id", "customer_version_id"}
            ),
            receipt_registry_versions=tuple(
                (e.registry.entity, e.registry.version_id) for e in source.relations.entities
            ),
        )
