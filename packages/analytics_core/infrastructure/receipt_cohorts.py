"""Materialize each customer cohort once before looking up receipt membership."""

from __future__ import annotations
from dataclasses import fields
from typing import TYPE_CHECKING
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.customer_events import RootRestrictedSequenceGrant
from packages.contracts.analytics.receipt_cohorts import CustomerEventMembership, ReceiptCohortGrant
from packages.contracts.analytics.sequence_filters import SequenceFilterRequest

if TYPE_CHECKING:
    from packages.analytics_core.infrastructure.relational_filters import Compiler


def compile_cohort(
    c: Compiler, node: CustomerEventMembership, entity: str, alias: str, depth: int
) -> str:
    from packages.analytics_core.infrastructure.relational_filters import Compiler

    if not isinstance(c.grant, ReceiptCohortGrant):
        raise AnalyticsFailure("FILTER_COHORT_CAPABILITY")
    relation = c.relationships.get(node.relationship_id)
    if relation is None:
        raise AnalyticsFailure("FILTER_RELATIONSHIP_FORBIDDEN")
    r = relation.relationship
    if (entity, r.parent_entity, r.child_entity, r.version_id) != (
        "Receipt",
        "Customer",
        "Receipt",
        node.relationship_version_id,
    ):
        raise AnalyticsFailure("FILTER_COHORT_BINDING")
    if node.customer_scope_id in c.scopes:
        raise AnalyticsFailure("FILTER_SCOPE_INVALID")
    request = SequenceFilterRequest(
        workspace_id=c.request.workspace_id,
        dataset_version_id=c.request.dataset_version_id,
        root_entity="Customer",
        root_scope_id=node.customer_scope_id,
        registry_versions=c.request.registry_versions,
        expression=node.predicate,
    )
    grant = RootRestrictedSequenceGrant(
        **{f.name: getattr(c.grant, f.name) for f in fields(RootRestrictedSequenceGrant)}
    )
    nested = Compiler(request, c.actor, grant, root_depth=depth + 1)
    if c.nodes & nested.nodes or c.scopes & nested.scopes:
        raise AnalyticsFailure("FILTER_SCOPE_INVALID")
    c.nodes.update(nested.nodes)
    c.scopes.update(nested.scopes)
    c.correlations += nested.correlations + 1
    c.used.update(nested.used | {r.relationship_id})
    c.limitations.update(nested.limitations | {"OBSERVED_CUSTOMER_UNIVERSE"})
    c.sequence_work.extend(nested.sequence_work)
    c.prelude_parameters.extend(nested.parameters)
    if (
        len(c.nodes) > c.policy.max_nodes
        or c.correlations > c.policy.max_correlations
        or len(c.parameters) + len(c.prelude_parameters) > c.policy.max_values
    ):
        raise AnalyticsFailure("FILTER_PLAN_LIMIT")
    name = f"cohort_{len(c.preludes)}"
    c.preludes.append(
        f"{name} AS MATERIALIZED (SELECT s0.*,{nested.expression} AS matched FROM input_{c.entities['Customer'][0]} s0 WHERE ({nested.ceiling}) IS TRUE)"
    )
    keys = " AND ".join(
        f"{c.column('Customer', p, 'member')}={c.column(entity, k, alias)}"
        for p, k in zip(r.parent_fields, r.child_fields, strict=True)
    )
    return f"(SELECT member.matched FROM {name} member WHERE {keys})"
