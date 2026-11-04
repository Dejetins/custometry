"""Correlated DuckDB predicates over admitted immutable columnar inputs."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
from threading import Event, Thread
from time import monotonic
from typing import Any, NoReturn
from uuid import UUID
import duckdb
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.retail_relational import (
    RelationalFacetQuery,
    RelationalFacetResponse,
)
from packages.contracts.analytics.retail_filter import FilterFacetValue
from packages.contracts.analytics.columnar_filters import (
    MaterializedFilterBinding,
    FlatPredicate,
    canonical_flat_expression,
)
from packages.contracts.analytics.relational_filters import (
    RelationalFilterAccess,
    RelationalFilterRequest,
    RelationalFilterResult,
    RelationalInputGrant,
    RelationalResourcePolicy,
    ScopedExpression,
    ScopedPredicate,
    ScopedBoolean,
    ScopedNot,
    CorrelatedExists,
    canonical_scoped_expression,
)
from packages.contracts.analytics.aggregate_filters import (
    AggregateFilterRequest,
    AggregateInputGrant,
    AggregateExpression,
    AggregateBoolean,
    AggregateNot,
    AggregateExists,
    AggregateCompare,
    ScopedCount,
    CountRatio,
    AggregateScalar,
    canonical_aggregate_expression,
)
from packages.contracts.analytics.sequence_filters import (
    SequenceFilterRequest,
    SequenceInputGrant,
    SequenceExpression,
    SequenceBoolean,
    SequenceNot,
    SequenceExists,
    BehavioralSequence,
    canonical_sequence_expression,
)
from packages.contracts.analytics.receipt_cohorts import (
    CohortFilterRequest,
    ReceiptCohortGrant,
    CohortExpression,
    CohortBoolean,
    CohortNot,
    CohortExists,
    CustomerEventMembership,
)
from packages.analytics_core.infrastructure.receipt_cohorts import compile_cohort
from packages.contracts.semantic.filter_events import EventTimeFieldVersion
from packages.contracts.semantic.nullable_relationships import NullableFilterRelationshipVersion
from packages.contracts.analytics.customer_events import RootRestrictedSequenceGrant
from packages.analytics_core.infrastructure.sequence_filters import compile_sequence
from packages.analytics_core.infrastructure.columnar_filters import (
    FlatCompiler,
    isolated_connection,
    read_admitted_input,
    check_execution,
    pa,
)


def fail(code: str) -> NoReturn:
    raise AnalyticsFailure(code)


def identity(
    request: RelationalFilterRequest
    | AggregateFilterRequest
    | SequenceFilterRequest
    | CohortFilterRequest,
    actor: UUID,
    grant: RelationalInputGrant,
) -> str:
    value = dict(
        engine="duckdb-correlated/v2",
        engine_version=duckdb.__version__,
        decimal_storage="lossless-precision-widening-same-scale/v1",
        actor=str(actor),
        request=request.model_dump(mode="json", exclude={"expression"}, exclude_none=True),
        expression=(
            canonical_sequence_expression(request.expression)
            if isinstance(request, (SequenceFilterRequest, CohortFilterRequest))
            else canonical_aggregate_expression(request.expression)
            if isinstance(request, AggregateFilterRequest)
            else canonical_scoped_expression(request.expression)
        ),
        **(
            {
                "aggregate_counts": [
                    dict(
                        definition=c.definition.model_dump(mode="json"),
                        observation=c.observation.model_dump(mode="json"),
                        evidence_hash=c.evidence_hash,
                    )
                    for c in sorted(grant.counts, key=lambda c: str(c.definition.version_id))
                ]
            }
            if isinstance(grant, AggregateInputGrant)
            else {}
        ),
        **(
            {
                "sequence_events": [
                    dict(
                        definition=e.definition.model_dump(mode="json"),
                        observation=e.observation.model_dump(mode="json"),
                        complete=e.complete,
                        evidence_hash=e.evidence_hash,
                    )
                    for e in sorted(grant.events, key=lambda e: str(e.definition.version_id))
                ],
                "sequence_estimation": "parent-rows-times-fanout-with-negative-probes-times-steps/v1",
            }
            if isinstance(grant, SequenceInputGrant)
            else {}
        ),
        **(
            {"root_restrictions": [r.model_dump(mode="json") for r in grant.root_restrictions]}
            if isinstance(grant, (RootRestrictedSequenceGrant, ReceiptCohortGrant))
            else {}
        ),
        **(
            {
                "cohort_registry_bridge": [(k, str(v)) for k, v in grant.receipt_registry_versions],
                "cohort_materialization": "customer-once-per-leaf/v1",
                "cohort_facet_fields": sorted(grant.facet_fields),
            }
            if isinstance(grant, ReceiptCohortGrant)
            else {}
        ),
        resources=grant.resource_policy.model_dump(mode="json"),
        **(
            {
                "compatibility_registries": sorted(
                    str(v) for v in grant.compatibility_registry_versions
                )
            }
            if grant.compatibility_registry_versions
            else {}
        ),
        entities=[
            dict(
                entity=e.registry.entity,
                registry=e.registry.model_dump(mode="json"),
                artifact=str(e.binding.artifact_id),
                content=e.binding.content_hash,
                policy=e.policy_revision,
                input_resources=e.resource_policy.model_dump(mode="json"),
                row_id=e.row_id_column,
                ceiling=canonical_flat_expression(e.row_ceiling),
            )
            for e in sorted(grant.entities, key=lambda e: e.registry.entity)
        ],
        relationships=[
            dict(
                meaning=r.relationship.model_dump(mode="json"),
                complete=r.complete,
                completeness_hash=r.completeness_hash,
            )
            for r in sorted(grant.relationships, key=lambda r: r.relationship.relationship_id)
        ],
    )
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def execution_policy(grant: RelationalInputGrant) -> RelationalResourcePolicy:
    """The compound query obeys every input's execution ceiling as well as its own."""
    fields = ("max_nodes", "max_depth", "max_values", "memory_mb", "threads", "timeout_ms")
    return grant.resource_policy.model_copy(
        update={
            key: min(
                [
                    getattr(grant.resource_policy, key),
                    *(getattr(e.resource_policy, key) for e in grant.entities),
                ]
            )
            for key in fields
        }
    )


class Compiler:
    def __init__(
        self,
        request: RelationalFilterRequest
        | AggregateFilterRequest
        | SequenceFilterRequest
        | CohortFilterRequest,
        actor: UUID,
        grant: RelationalInputGrant,
        *,
        root_depth: int = 1,
    ):
        self.request, self.actor = request, actor
        self.preludes: list[str] = []
        self.prelude_parameters: list[object] = []
        self.grant = grant
        self.policy = execution_policy(grant)
        self.entities = {e.registry.entity: (i, e) for i, e in enumerate(grant.entities)}
        self.relationships = {r.relationship.relationship_id: r for r in grant.relationships}
        self.parameters: list[object] = []
        self.nodes: set[UUID] = set()
        self.scopes = {request.root_scope_id}
        self.correlations = 0
        self.used: set[str] = set()
        self.limitations: set[str] = set()
        policy = self.policy
        if (
            not grant.entities
            or len(grant.entities) > policy.max_entities
            or len(self.entities) != len(grant.entities)
            or len(self.relationships) != len(grant.relationships)
        ):
            fail("FILTER_INPUT_BINDING")
        if request.root_entity not in self.entities or request.registry_versions != {
            e.registry.entity: e.registry.version_id for e in grant.entities
        }:
            fail("FILTER_REGISTRY_BINDING")
        if (
            request.compatibility_registry_version_id is not None
            and request.compatibility_registry_version_id
            not in grant.compatibility_registry_versions
        ):
            fail("FILTER_COMPATIBILITY_REGISTRY_BINDING")
        if isinstance(request, CohortFilterRequest):
            if (
                not isinstance(grant, ReceiptCohortGrant)
                or not grant.receipt_registry_versions
                or request.receipt_registry_versions != dict(grant.receipt_registry_versions)
                or any(
                    v != dict(grant.receipt_registry_versions)
                    for v in request.promoted_registry_sets
                )
            ):
                fail("FILTER_COHORT_REGISTRY_BRIDGE")
        elif isinstance(grant, ReceiptCohortGrant):
            fail("FILTER_COHORT_CAPABILITY")
        for e in grant.entities:
            if not isinstance(e.binding, MaterializedFilterBinding):
                fail("FILTER_INPUT_BINDING")
            if (
                e.workspace_id,
                e.actor_id,
                e.registry.dataset_version_id,
                e.binding.workspace_id,
                e.binding.entity,
            ) != (
                request.workspace_id,
                actor,
                request.dataset_version_id,
                request.workspace_id,
                e.registry.entity,
            ) or not e.policy_revision:
                fail("FILTER_INPUT_BINDING")
        for relation in grant.relationships:
            r = relation.relationship
            if (
                r.parent_entity not in self.entities
                or r.child_entity not in self.entities
                or type(relation.complete) is not bool
                or len(relation.completeness_hash) != 64
                or any(c not in "0123456789abcdef" for c in relation.completeness_hash)
            ):
                fail("FILTER_RELATIONSHIP_BINDING")
            for parent, child in zip(r.parent_fields, r.child_fields, strict=True):
                left = self.field(r.parent_entity, parent)[1]
                right = self.field(r.child_entity, child)[1]
                if left.known_column is not None or right.known_column is not None:
                    fail("FILTER_RELATIONSHIP_KEY_UNKNOWN")
                if (left.data_type, left.decimal_precision, left.decimal_scale) != (
                    right.data_type,
                    right.decimal_precision,
                    right.decimal_scale,
                ):
                    fail("FILTER_RELATIONSHIP_TYPE")
        self.event_times: dict[str, tuple[EventTimeFieldVersion, ...]] = {}
        self.sequence_work: list[tuple[str, int, int]] = []
        if isinstance(grant, SequenceInputGrant):
            seen_events: set[UUID] = set()
            for event in grant.events:
                definition = event.definition
                if (
                    definition.version_id in seen_events
                    or definition.entity not in self.entities
                    or type(event.complete) is not bool
                    or len(event.evidence_hash) != 64
                    or any(c not in "0123456789abcdef" for c in event.evidence_hash)
                ):
                    fail("FILTER_EVENT_BINDING")
                seen_events.add(definition.version_id)
                fields = self.event_times.get(definition.entity, ())
                matches = [
                    f
                    for f in fields
                    if f.field_id == definition.time_field.field_id
                    or f.version_id == definition.time_field.version_id
                ]
                if matches and matches != [definition.time_field]:
                    fail("FILTER_EVENT_TIME_BINDING")
                if not matches:
                    self.event_times[definition.entity] = (*fields, definition.time_field)
        self.expression = self.compile(
            request.expression, request.root_entity, request.root_scope_id, "s0", root_depth
        )
        self.ceiling = self.flat(
            grant.entities[self.entities[request.root_entity][0]].row_ceiling,
            request.root_entity,
            "s0",
        )

        if isinstance(grant, RootRestrictedSequenceGrant):
            if not grant.root_restrictions:
                fail("FILTER_ROOT_POLICY_BINDING")
            for restriction in grant.root_restrictions:
                relation = self.relationships.get(restriction.relationship_id)
                if relation is None:
                    fail("FILTER_ROOT_POLICY_BINDING")
                r = relation.relationship
                if (restriction.root_entity, r.parent_entity, r.version_id) != (
                    request.root_entity,
                    request.root_entity,
                    restriction.relationship_version_id,
                ):
                    fail("FILTER_ROOT_POLICY_BINDING")
                self.used.add(r.relationship_id)
                self.correlations += 1
                if self.correlations > self.policy.max_correlations:
                    fail("FILTER_PLAN_LIMIT")
                child_alias = f"mandatory{self.correlations}"
                child_ceiling = self.flat(
                    self.entities[r.child_entity][1].row_ceiling, r.child_entity, child_alias
                )
                keys = " AND ".join(
                    f"{self.column(r.parent_entity, p, 's0')}={self.column(r.child_entity, k, child_alias)}"
                    for p, k in zip(r.parent_fields, r.child_fields, strict=True)
                )
                self.ceiling = f"({self.ceiling}) AND EXISTS (SELECT 1 FROM input_{self.entities[r.child_entity][0]} {child_alias} WHERE {keys} AND ({child_ceiling}) IS TRUE)"

    def field(self, entity: str, name: str):
        fields = self.entities[entity][1].registry.fields
        found = next(((i, f) for i, f in enumerate(fields) if f.field_id == name), None)
        if found is None:
            fail("FILTER_FIELD_FORBIDDEN")
        assert found is not None
        return found

    def column(self, entity: str, name: str, alias: str) -> str:
        return f'{alias}."f{self.field(entity, name)[0]}"'

    def flat(self, node: Any, entity: str, alias: str) -> str:
        compiler = FlatCompiler(self.entities[entity][1])
        sql = compiler.compile(node)
        self.parameters.extend(compiler.parameters)
        if len(self.parameters) + len(self.prelude_parameters) > self.policy.max_values:
            fail("FILTER_PLAN_LIMIT")
        for i, _ in enumerate(self.entities[entity][1].registry.fields):
            sql = sql.replace(f'"f{i}"', f'{alias}."f{i}"').replace(f'"k{i}"', f'{alias}."k{i}"')
        return sql

    def compile(
        self,
        node: ScopedExpression | AggregateExpression | SequenceExpression | CohortExpression,
        entity: str,
        scope: UUID,
        alias: str,
        depth: int,
    ) -> str:
        if node.node_id in self.nodes or node.scope_id != scope:
            fail("FILTER_SCOPE_INVALID")
        self.nodes.add(node.node_id)
        if depth > self.policy.max_depth or len(self.nodes) > self.policy.max_nodes:
            fail("FILTER_PLAN_LIMIT")
        if isinstance(node, ScopedPredicate):
            return self.flat(
                FlatPredicate.model_validate(node.model_dump(exclude={"node_id", "scope_id"})),
                entity,
                alias,
            )
        if isinstance(node, (ScopedBoolean, AggregateBoolean, SequenceBoolean, CohortBoolean)):
            joiner = " AND " if node.kind == "and" else " OR "
            return (
                "("
                + joiner.join(
                    self.compile(c, entity, scope, alias, depth + 1) for c in node.children
                )
                + ")"
            )
        if isinstance(node, (ScopedNot, AggregateNot, SequenceNot, CohortNot)):
            return f"(NOT {self.compile(node.child, entity, scope, alias, depth + 1)})"
        if isinstance(node, CustomerEventMembership):
            return compile_cohort(self, node, entity, alias, depth)
        if isinstance(node, BehavioralSequence):
            return compile_sequence(self, node, entity, scope, alias, depth)
        if isinstance(node, AggregateCompare):
            return self.aggregate_compare(node, entity, scope, alias, depth)
        assert isinstance(node, (CorrelatedExists, AggregateExists, SequenceExists, CohortExists))
        self.correlations += 1
        if self.correlations > self.policy.max_correlations:
            fail("FILTER_PLAN_LIMIT")
        relation = self.relationships.get(node.relationship_id)
        if relation is None:
            fail("FILTER_RELATIONSHIP_FORBIDDEN")
        assert relation is not None
        r = relation.relationship
        if node.parent_scope_id != scope or node.child_scope_id in self.scopes:
            fail("FILTER_SCOPE_INVALID")
        if (r.parent_entity, r.child_entity, r.version_id) != (
            entity,
            node.child_entity,
            node.relationship_version_id,
        ):
            fail("FILTER_RELATIONSHIP_BINDING")
        self.scopes.add(node.child_scope_id)
        self.used.add(r.relationship_id)
        child_alias = f"s{self.correlations}"
        predicate = self.compile(
            node.predicate, node.child_entity, node.child_scope_id, child_alias, depth + 1
        )
        ceiling = self.flat(
            self.entities[node.child_entity][1].row_ceiling, node.child_entity, child_alias
        )
        keys = " AND ".join(
            f"{self.column(entity, p, alias)}={self.column(node.child_entity, c, child_alias)}"
            for p, c in zip(r.parent_fields, r.child_fields, strict=True)
        )
        table = f"input_{self.entities[node.child_entity][0]}"
        sql = f"(SELECT CASE WHEN bool_or(evaluated) IS TRUE THEN TRUE WHEN count(*) FILTER (WHERE evaluated IS NULL)>0 OR {'FALSE' if relation.complete else 'TRUE'} THEN NULL ELSE FALSE END FROM (SELECT {predicate} AS evaluated FROM {table} {child_alias} WHERE {keys} AND ({ceiling}) IS TRUE) related)"
        return f"(NOT {sql})" if node.kind == "not_exists" else sql

    def aggregate_count(
        self, node: ScopedCount, entity: str, scope: UUID, alias: str, depth: int
    ) -> tuple[str, str]:
        if not isinstance(self.grant, AggregateInputGrant):
            fail("FILTER_AGGREGATE_CAPABILITY")
        offered = [
            c for c in self.grant.counts if c.definition.version_id == node.definition.version_id
        ]
        if len(offered) != 1 or offered[0].definition != node.definition:
            fail("FILTER_AGGREGATE_BINDING")
        supplied = offered[0]
        definition, observation = supplied.definition, supplied.observation
        if len(supplied.evidence_hash) != 64 or any(
            c not in "0123456789abcdef" for c in supplied.evidence_hash
        ):
            fail("FILTER_AGGREGATE_BINDING")
        if (node.window.observation_as_of, node.window.knowledge_as_of) != (
            observation.observation_as_of,
            observation.knowledge_as_of,
        ):
            fail("FILTER_AGGREGATE_AS_OF")
        relation = self.relationships.get(node.relationship_id)
        if relation is None:
            fail("FILTER_RELATIONSHIP_FORBIDDEN")
        r = relation.relationship
        if (r.parent_entity, r.child_entity, r.version_id) != (
            entity,
            node.child_entity,
            node.relationship_version_id,
        ) or (definition.relationship_version_id, definition.child_entity) != (
            r.version_id,
            r.child_entity,
        ):
            fail("FILTER_AGGREGATE_BINDING")
        if node.parent_scope_id != scope or node.child_scope_id in self.scopes:
            fail("FILTER_SCOPE_INVALID")
        self.scopes.add(node.child_scope_id)
        self.correlations += 1
        if self.correlations > self.policy.max_correlations:
            fail("FILTER_PLAN_LIMIT")
        self.used.add(r.relationship_id)
        child_alias = f"s{self.correlations}"
        predicate = self.compile(
            node.predicate, node.child_entity, node.child_scope_id, child_alias, depth + 1
        )
        time_entity = entity if definition.time_entity == "parent" else node.child_entity
        time_alias = alias if definition.time_entity == "parent" else child_alias
        ti, time_field = self.field(time_entity, definition.time_field.field_id)
        if (
            time_field.version_id != definition.time_field.version_id
            or time_field.data_type != "date"
        ):
            fail("FILTER_AGGREGATE_TIME_FIELD")
        time_column = self.column(time_entity, time_field.field_id, time_alias)
        time_sql = f"({time_column} >= ? AND {time_column} < ?)"
        if time_field.known_column is not None:
            time_sql = f'CASE WHEN {time_alias}."k{ti}" IS TRUE THEN {time_sql} ELSE NULL END'
        self.parameters.extend([node.window.starts_at.date(), node.window.ends_at.date()])
        grain: list[str] = []
        unknown: list[str] = []
        nonnull: list[str] = []
        for ref in definition.grain_fields:
            i, field = self.field(node.child_entity, ref.field_id)
            if field.version_id != ref.version_id:
                fail("FILTER_AGGREGATE_GRAIN")
            column = self.column(node.child_entity, ref.field_id, child_alias)
            grain.append(column)
            nonnull.append(f"{column} IS NOT NULL")
            if field.known_column is not None:
                unknown.append(f'{child_alias}."k{i}" IS NOT TRUE')
            if definition.null_policy == "unknown":
                unknown.append(f"{column} IS NULL")
        child = self.entities[node.child_entity][1]
        if definition.kind == "count" and (
            len(definition.grain_fields) != 1
            or self.field(node.child_entity, definition.grain_fields[0].field_id)[1].column
            != child.row_id_column
        ):
            fail("FILTER_AGGREGATE_GRAIN")
        ceiling = self.flat(child.row_ceiling, node.child_entity, child_alias)
        if len(self.parameters) + len(self.prelude_parameters) > self.policy.max_values:
            fail("FILTER_PLAN_LIMIT")
        keys = " AND ".join(
            f"{self.column(entity, p, alias)}={self.column(node.child_entity, c, child_alias)}"
            for p, c in zip(r.parent_fields, r.child_fields, strict=True)
        )
        complete = (
            relation.complete
            and observation.starts_at <= node.window.starts_at
            and node.window.ends_at <= observation.ends_at
        )
        if not complete:
            self.limitations.add("AGGREGATE_WINDOW_INCOMPLETE")
        self.limitations.add("AGGREGATE_VALUE_UNAVAILABLE")
        table = f"input_{self.entities[node.child_entity][0]}"
        grain_sql = grain[0] if len(grain) == 1 else "(" + ",".join(grain) + ")"
        inner = f"SELECT (({predicate}) AND ({time_sql})) AS evaluated,({' OR '.join(unknown) or 'FALSE'}) AS grain_unknown,({' AND '.join(nonnull)}) AS grain_present,{grain_sql} AS grain FROM {table} {child_alias} WHERE {keys} AND ({ceiling}) IS TRUE"
        count = (
            "count(*) FILTER (WHERE evaluated IS TRUE)"
            if definition.kind == "count"
            else "count(DISTINCT grain) FILTER (WHERE evaluated IS TRUE AND grain_present)"
        )
        result = f"(SELECT CASE WHEN {'FALSE' if complete else 'TRUE'} OR count(*) FILTER (WHERE evaluated IS NULL OR (evaluated IS TRUE AND grain_unknown))>0 THEN NULL ELSE {count} END FROM ({inner}) counted)"
        return result, definition.unit

    def aggregate_operand(
        self,
        node: ScopedCount | CountRatio | AggregateScalar,
        entity: str,
        scope: UUID,
        alias: str,
        depth: int,
    ) -> tuple[str, str, str]:
        if isinstance(node, AggregateScalar):
            self.parameters.append(node.value)
            return "CAST(? AS DECIMAL(18,6))", "1", node.unit
        if isinstance(node, ScopedCount):
            sql, unit = self.aggregate_count(node, entity, scope, alias, depth)
            return sql, "1", unit
        numerator, numerator_unit = self.aggregate_count(
            node.numerator, entity, scope, alias, depth
        )
        denominator, denominator_unit = self.aggregate_count(
            node.denominator, entity, scope, alias, depth
        )
        if numerator_unit != denominator_unit:
            fail("FILTER_AGGREGATE_UNIT")
        return numerator, denominator, "ratio"

    def aggregate_compare(
        self, node: AggregateCompare, entity: str, scope: UUID, alias: str, depth: int
    ) -> str:
        # Counts and decimal scalar bounds keep both exact cross-products inside
        # DECIMAL(38,12), including ratio-to-ratio comparisons without division.
        if self.policy.max_rows > 1_000_000_000:
            fail("FILTER_AGGREGATE_NUMERIC_BOUND")
        ln, ld, lu = self.aggregate_operand(node.left, entity, scope, alias, depth)
        rn, rd, ru = self.aggregate_operand(node.right, entity, scope, alias, depth)
        if lu != ru:
            fail("FILTER_AGGREGATE_UNIT")
        if len(self.parameters) + len(self.prelude_parameters) > self.policy.max_values:
            fail("FILTER_PLAN_LIMIT")
        operator = {"eq": "=", "ne": "<>", "lt": "<", "le": "<=", "gt": ">", "ge": ">="}[
            node.operator
        ]
        operands = f"SELECT {ln} AS ln,{ld} AS ld,{rn} AS rn,{rd} AS rd"
        return f"(SELECT CASE WHEN ld=0 OR rd=0 THEN NULL ELSE CAST(ln AS DECIMAL(38,6))*CAST(rd AS DECIMAL(38,6)) {operator} CAST(rn AS DECIMAL(38,6))*CAST(ld AS DECIMAL(38,6)) END FROM ({operands}) operands)"


class DuckDBRelationalFilter:
    def __init__(self, *, artifact_root: Path, access: RelationalFilterAccess):
        if not artifact_root.is_absolute() or artifact_root.is_symlink():
            fail("FILTER_ARTIFACT_ROOT")
        self.root = artifact_root.resolve(strict=True)
        self.access = access

    def fingerprint(
        self,
        request: RelationalFilterRequest
        | AggregateFilterRequest
        | SequenceFilterRequest
        | CohortFilterRequest,
        *,
        actor_id: UUID,
    ) -> str:
        grant = self.access.authorize(
            workspace_id=request.workspace_id,
            actor_id=actor_id,
            dataset_version_id=request.dataset_version_id,
        )
        Compiler(request, actor_id, grant)
        return identity(request, actor_id, grant)

    def execute(
        self,
        request: RelationalFilterRequest
        | AggregateFilterRequest
        | SequenceFilterRequest
        | CohortFilterRequest,
        *,
        actor_id: UUID,
        cancel: Event | None = None,
    ) -> RelationalFilterResult:
        result = self._execute(request, actor_id=actor_id, cancel=cancel)
        assert isinstance(result, RelationalFilterResult)
        return result

    def facets(
        self,
        request: RelationalFilterRequest
        | AggregateFilterRequest
        | SequenceFilterRequest
        | CohortFilterRequest,
        facet: RelationalFacetQuery,
        *,
        actor_id: UUID,
        cancel: Event | None = None,
    ) -> RelationalFacetResponse:
        result = self._execute(request, actor_id=actor_id, cancel=cancel, facet=facet)
        assert isinstance(result, RelationalFacetResponse)
        return result

    def _execute(
        self,
        request: RelationalFilterRequest
        | AggregateFilterRequest
        | SequenceFilterRequest
        | CohortFilterRequest,
        *,
        actor_id: UUID,
        cancel: Event | None = None,
        facet: RelationalFacetQuery | None = None,
    ) -> RelationalFilterResult | RelationalFacetResponse:
        cancel = cancel if cancel is not None else Event()
        grant = self.access.authorize(
            workspace_id=request.workspace_id,
            actor_id=actor_id,
            dataset_version_id=request.dataset_version_id,
        )
        compiler = Compiler(request, actor_id, grant)
        root = compiler.entities[request.root_entity][0]
        membership = f"SELECT s0.*,{compiler.expression} AS matched FROM input_{root} s0 WHERE ({compiler.ceiling}) IS TRUE"
        facet_sql = None
        if facet is not None:
            if (
                isinstance(grant, ReceiptCohortGrant)
                and (facet.entity, facet.field_id) not in grant.facet_fields
            ):
                fail("FILTER_FIELD_FORBIDDEN")
            if facet.entity not in compiler.entities:
                fail("FILTER_FIELD_FORBIDDEN")
            compiler.field(facet.entity, facet.field_id)
            alias = "m"
            source_sql = "matched_roots m"
            restriction = "m.matched IS TRUE"
            if facet.entity != request.root_entity:
                links = [
                    r.relationship
                    for r in grant.relationships
                    if r.relationship.parent_entity == request.root_entity
                    and r.relationship.child_entity == facet.entity
                ]
                if len(links) != 1:
                    fail("FILTER_RELATIONSHIP_FORBIDDEN")
                link = links[0]
                compiler.used.add(link.relationship_id)
                alias = "c"
                child_index, child = compiler.entities[facet.entity]
                keys = " AND ".join(
                    f"{compiler.column(link.parent_entity, p, 'm')}={compiler.column(link.child_entity, c, 'c')}"
                    for p, c in zip(link.parent_fields, link.child_fields, strict=True)
                )
                source_sql += f" JOIN input_{child_index} c ON {keys}"
                restriction += (
                    f" AND ({compiler.flat(child.row_ceiling, facet.entity, 'c')}) IS TRUE"
                )
            column = compiler.column(facet.entity, facet.field_id, alias)
            facet_sql = (
                f"WITH {','.join(compiler.preludes) + ',' if compiler.preludes else ''}matched_roots AS ({membership}) SELECT CAST({column} AS VARCHAR), count(*) "
                f"FROM {source_sql} WHERE {restriction} "
                f"AND (? = '' OR strpos(lower(CAST({column} AS VARCHAR)),lower(?)) > 0) "
                f"GROUP BY {column} ORDER BY CAST({column} AS VARCHAR) NULLS LAST LIMIT ? OFFSET ?"
            )
            compiler.parameters.extend([facet.search, facet.search, facet.limit + 1, facet.offset])
        policy = execution_policy(grant)
        if len(compiler.parameters) + len(compiler.prelude_parameters) > policy.max_values:
            fail("FILTER_PLAN_LIMIT")
        deadline = monotonic() + policy.timeout_ms / 1000

        def check() -> None:
            check_execution(cancel, deadline)

        check()
        # Conservative per-entity partition guarantees the combined byte/row allowance.
        quota = dict(
            max_rows=max(1, policy.max_rows // len(grant.entities)),
            max_input_bytes=max(1, policy.max_input_bytes // len(grant.entities)),
        )
        if policy.max_rows < len(grant.entities) or policy.max_input_bytes < len(grant.entities):
            fail("FILTER_INPUT_LIMIT")
        try:
            tables = [
                read_admitted_input(
                    self.root,
                    replace(
                        e,
                        resource_policy=e.resource_policy.model_copy(
                            update={
                                key: min(getattr(e.resource_policy, key), value)
                                for key, value in quota.items()
                            }
                        ),
                    ),
                    cancel,
                    deadline,
                    widen_decimal_precision=True,
                    event_times=compiler.event_times.get(e.registry.entity, ()),
                )
                for e in grant.entities
            ]
            general_work = sum(t.num_rows for t in tables) * (
                1 + compiler.correlations + int(facet is not None)
            )
            if general_work > policy.max_estimated_work:
                fail("FILTER_WORK_LIMIT")
            with isolated_connection(policy) as connection:
                for i, table in enumerate(tables):
                    connection.register(f"input_{i}", table)
                done = Event()

                def monitor():
                    while not done.wait(0.005):
                        if cancel.is_set() or monotonic() >= deadline:
                            connection.interrupt()

                watcher = Thread(target=monitor, daemon=True)
                watcher.start()
                try:
                    check()

                    def scalar(sql: str) -> int:
                        row = connection.execute(sql).fetchone()
                        if row is None:
                            fail("FILTER_EXECUTION_FAILED")
                        return int(row[0])

                    for i in range(len(tables)):
                        count, distinct = connection.execute(
                            f"SELECT count(*),count(DISTINCT row_id) FROM input_{i}"
                        ).fetchone() or (0, 0)
                        if count != distinct:
                            fail("FILTER_INPUT_ROW_ID")
                    fanouts: dict[str, int] = {}
                    for identifier in compiler.used:
                        r = compiler.relationships[identifier].relationship
                        pi = compiler.entities[r.parent_entity][0]
                        ci = compiler.entities[r.child_entity][0]
                        pk = ",".join(
                            compiler.column(r.parent_entity, k, "p") for k in r.parent_fields
                        )
                        ck = ",".join(
                            compiler.column(r.child_entity, k, "c") for k in r.child_fields
                        )
                        invalid = " OR ".join(
                            f"{compiler.column(r.parent_entity, k, 'p')} IS NULL"
                            for k in r.parent_fields
                        )
                        if scalar(f"SELECT count(*) FROM input_{pi} p WHERE {invalid}"):
                            fail("FILTER_RELATIONSHIP_KEYS")
                        if scalar(
                            f"SELECT count(*) FROM (SELECT {pk} FROM input_{pi} p GROUP BY {pk} HAVING count(*)>1)"
                        ):
                            fail("FILTER_RELATIONSHIP_CARDINALITY")
                        matches = " AND ".join(
                            f"{compiler.column(r.parent_entity, p, 'p')}={compiler.column(r.child_entity, c, 'c')}"
                            for p, c in zip(r.parent_fields, r.child_fields, strict=True)
                        )
                        unlinked = "FALSE"
                        if isinstance(r, NullableFilterRelationshipVersion):
                            unlinked = " AND ".join(
                                f"{compiler.column(r.child_entity, k, 'c')} IS {'NULL' if k in r.nullable_child_fields else 'NOT NULL'}"
                                for k in r.child_fields
                            )
                        if scalar(
                            f"SELECT count(*) FROM input_{ci} c WHERE NOT ({unlinked}) AND NOT EXISTS (SELECT 1 FROM input_{pi} p WHERE {matches})"
                        ):
                            fail("FILTER_RELATIONSHIP_KEYS")
                        fanout = scalar(
                            f"SELECT coalesce(max(n),0) FROM (SELECT count(*) n FROM input_{ci} c WHERE NOT ({unlinked}) GROUP BY {ck})"
                        )
                        fanouts[identifier] = fanout
                        if fanout > policy.max_fan_out:
                            fail("FILTER_FAN_OUT_LIMIT")
                    check()
                    sequence_work = sum(
                        tables[
                            compiler.entities[compiler.relationships[r].relationship.parent_entity][
                                0
                            ]
                        ].num_rows
                        * max(1, fanouts[r]) ** (positive + int(steps > positive))
                        * steps
                        for r, positive, steps in compiler.sequence_work
                    )
                    if (
                        sequence_work
                        + (general_work if isinstance(request, CohortFilterRequest) else 0)
                        > policy.max_estimated_work
                    ):
                        fail("FILTER_SEQUENCE_WORK_LIMIT")
                    rows = connection.execute(
                        facet_sql
                        or (
                            (
                                "WITH " + ",".join(compiler.preludes) + " "
                                if compiler.preludes
                                else ""
                            )
                            + f"SELECT row_id,matched FROM ({membership}) ORDER BY row_id"
                        ),
                        compiler.prelude_parameters + compiler.parameters,
                    ).fetchall()
                    check()
                finally:
                    done.set()
                    watcher.join()
            current = self.access.authorize(
                workspace_id=request.workspace_id,
                actor_id=actor_id,
                dataset_version_id=request.dataset_version_id,
            )
            if current != grant:
                fail("FILTER_POLICY_CHANGED")
            check()
            if facet is not None:
                return RelationalFacetResponse(
                    request_hash=identity(request, actor_id, grant),
                    values=[FilterFacetValue(value=r[0], count=r[1]) for r in rows[: facet.limit]],
                    has_more=len(rows) > facet.limit,
                    count_grain="matching_receipts"
                    if facet.entity == request.root_entity
                    else "observed_items_in_matching_receipts",
                )
            return RelationalFilterResult(
                request_hash=identity(request, actor_id, grant),
                matched_ids=tuple(r[0] for r in rows if r[1] is True),
                not_matched_count=sum(r[1] is False for r in rows),
                unknown_count=sum(r[1] is None for r in rows),
                authorized_count=len(rows),
                limitation_codes=tuple(
                    sorted(
                        (
                            {"RELATIONSHIP_HISTORY_INCOMPLETE"}
                            if any(not compiler.relationships[r].complete for r in compiler.used)
                            else set[str]()
                        )
                        | (compiler.limitations if any(r[1] is None for r in rows) else set[str]())
                    )
                ),
            )
        except duckdb.InterruptException:
            check()
            raise AnalyticsFailure("FILTER_CANCELLED") from None
        except duckdb.OutOfMemoryException:
            raise AnalyticsFailure("FILTER_RESOURCE_LIMIT") from None
        except (duckdb.Error, pa.ArrowException, ValueError, KeyError):
            raise AnalyticsFailure("FILTER_EXECUTION_FAILED") from None
