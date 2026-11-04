"""Compose current relational access with immutable public aggregate semantics."""

from uuid import UUID
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.aggregate_filters import AggregateInputGrant
from packages.contracts.analytics.relational_filters import RelationalFilterAccess
from packages.contracts.analytics.retail_aggregate import RetailAggregatesSemanticPort


class PublishedRetailAggregateAccess:
    def __init__(self, base: RelationalFilterAccess, semantics: RetailAggregatesSemanticPort):
        self.base, self.semantics = base, semantics

    def authorize(
        self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID
    ) -> AggregateInputGrant:
        grant = self.base.authorize(
            workspace_id=workspace_id, actor_id=actor_id, dataset_version_id=dataset_version_id
        )
        published = self.semantics.retail_aggregate_projection(
            workspace_id=workspace_id, dataset_version_id=dataset_version_id
        )
        if (
            len(grant.entities) != len(published.relations.entities)
            or grant.relationships != published.relations.relationships
            or grant.compatibility_registry_versions
            != (published.relations.legacy_registry_version_id,)
        ):
            raise AnalyticsFailure("FILTER_AGGREGATE_BINDING")
        for entity, source in zip(grant.entities, published.relations.entities, strict=True):
            if (
                entity.registry != source.registry
                or entity.binding.artifact_id != source.artifact_id
                or entity.binding.content_hash != source.content_hash
                or entity.row_id_column != source.row_id_column
            ):
                raise AnalyticsFailure("FILTER_AGGREGATE_BINDING")
        return AggregateInputGrant(
            grant.entities,
            grant.relationships,
            grant.resource_policy,
            grant.compatibility_registry_versions,
            published.counts,
        )
