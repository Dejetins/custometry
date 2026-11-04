"""Sequence SQL fragment for the shared authorized relational executor."""

from __future__ import annotations
from datetime import datetime, UTC
from typing import TYPE_CHECKING, NoReturn
from uuid import UUID
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sequence_filters import (
    BehavioralSequence,
    PositiveStep,
    SequenceInputGrant,
    EventInput,
)
from packages.contracts.semantic.filter_aggregates import AggregateFieldRef

if TYPE_CHECKING:
    from packages.analytics_core.infrastructure.relational_filters import Compiler


def fail(code: str) -> NoReturn:
    raise AnalyticsFailure(code)


def micros(value: datetime) -> int:
    delta = value - datetime(1970, 1, 1, tzinfo=UTC)
    return (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds


def compile_sequence(
    c: Compiler, node: BehavioralSequence, entity: str, scope: UUID, alias: str, depth: int
) -> str:
    if not isinstance(c.grant, SequenceInputGrant):
        fail("FILTER_SEQUENCE_CAPABILITY")
    relation = c.relationships.get(node.relationship_id)
    if relation is None:
        fail("FILTER_RELATIONSHIP_FORBIDDEN")
    assert relation is not None
    r = relation.relationship
    if node.parent_scope_id != scope:
        fail("FILTER_SCOPE_INVALID")
    if (r.parent_entity, r.child_entity, r.version_id) != (
        entity,
        node.child_entity,
        node.relationship_version_id,
    ):
        fail("FILTER_SEQUENCE_BINDING")
    c.used.add(r.relationship_id)
    supplied: list[EventInput] = []
    for step in node.steps:
        values = [e for e in c.grant.events if e.definition.version_id == step.event.version_id]
        if len(values) != 1 or values[0].definition != step.event:
            fail("FILTER_EVENT_BINDING")
        event = values[0]
        if (event.definition.entity, event.definition.relationship_version_id) != (
            node.child_entity,
            r.version_id,
        ):
            fail("FILTER_EVENT_BINDING")
        if (node.window.observation_as_of, node.window.knowledge_as_of) != (
            event.observation.observation_as_of,
            event.observation.knowledge_as_of,
        ):
            fail("FILTER_EVENT_AS_OF")
        supplied.append(event)
    c.sequence_work.append(
        (r.relationship_id, sum(isinstance(s, PositiveStep) for s in node.steps), len(node.steps))
    )
    # Bounds and trusted observation limits are values, not SQL identifiers.
    bounds = ["?::BIGINT AS lo", "?::BIGINT AS hi"]
    c.parameters.extend([micros(node.window.starts_at), micros(node.window.ends_at)])
    for i, event in enumerate(supplied):
        bounds.extend([f"?::BIGINT AS o{i}start", f"?::BIGINT AS o{i}end"])
        c.parameters.extend(
            [micros(event.observation.starts_at), micros(event.observation.ends_at)]
        )
        step = node.steps[i]
        if isinstance(step, PositiveStep):
            if step.gap is not None:
                bounds.extend([f"?::BIGINT AS g{i}min", f"?::BIGINT AS g{i}max"])
                c.parameters.extend([step.gap.minimum_us, step.gap.maximum_us])
        else:
            bounds.extend([f"?::BIGINT AS n{i}start", f"?::BIGINT AS n{i}end"])
            c.parameters.extend([step.starts_after_us, step.ends_after_us])
    ctes = ["bounds AS (SELECT " + ",".join(bounds) + ")"]
    positive: dict[UUID, tuple[str, PositiveStep]] = {}
    negative: list[str] = []
    previous = None
    guards: list[str] = []
    truth: list[str] = []
    unknown: list[str] = []
    for i, (step, event) in enumerate(zip(node.steps, supplied, strict=True)):
        if step.child_scope_id in c.scopes or step.step_id in c.nodes:
            fail("FILTER_SCOPE_INVALID")
        c.scopes.add(step.child_scope_id)
        c.nodes.add(step.step_id)
        c.correlations += 1
        if c.correlations > c.policy.max_correlations or len(c.nodes) > c.policy.max_nodes:
            fail("FILTER_PLAN_LIMIT")
        raw = f"s{c.correlations}"
        q = f"q{i}"
        pred = c.compile(step.predicate, node.child_entity, step.child_scope_id, raw, depth + 1)
        ceiling = c.flat(c.entities[node.child_entity][1].row_ceiling, node.child_entity, raw)
        ti = c.event_times[node.child_entity].index(event.definition.time_field)
        time = f'{raw}."t{ti}"'
        if event.definition.time_field.known_column:
            time = f'CASE WHEN {raw}."tk{ti}" IS TRUE THEN {time} ELSE NULL END'
        keys = " AND ".join(
            f"{c.column(entity, p, alias)}={c.column(node.child_entity, k, q)}"
            for p, k in zip(r.parent_fields, r.child_fields, strict=True)
        )
        ctes.append(
            f"{q} AS (SELECT {raw}.*,{pred} AS p,{time} AS event_time FROM input_{c.entities[node.child_entity][0]} {raw} WHERE ({ceiling}) IS TRUE)"
        )
        complete = (
            relation.complete
            and event.complete
            and event.observation.starts_at <= node.window.starts_at
            and event.observation.ends_at >= node.window.ends_at
        )
        if not complete:
            c.limitations.add("SEQUENCE_HISTORY_INCOMPLETE")
        if isinstance(step, PositiveStep):
            positive[step.step_id] = (q, step)
            guards.extend(
                [
                    keys,
                    f"{q}.event_time>=bounds.lo",
                    f"{q}.event_time<bounds.hi",
                    f"{q}.p IS NOT FALSE",
                ]
            )
            truth.append(f"{q}.p")
            if previous is not None:
                pq = positive[previous][0]
                assert step.gap is not None
                # Integers are model-validated bounded durations; bind them as values.
                guards.extend(
                    [
                        f"{q}.event_time>{pq}.event_time",
                        f"{q}.event_time-{pq}.event_time BETWEEN bounds.g{i}min AND bounds.g{i}max",
                    ]
                )
                for end in negative:
                    guards.append(f"{q}.event_time>={end}")
            previous = step.step_id
            negative = []
            unknown.append(
                "TRUE"
                if not complete
                else f"EXISTS (SELECT 1 FROM {q} WHERE {keys} AND p IS NOT FALSE AND event_time IS NULL)"
            )
        else:
            pq = positive[step.after_step_id][0]
            # Durations are validated integral microseconds. Keep SQL parameters in
            # expression order by collecting separate truth and guard fragments below.
            start = f"{pq}.event_time+bounds.n{i}start"
            end = f"{pq}.event_time+bounds.n{i}end"
            negative.append(end)
            certified = "TRUE" if relation.complete and event.complete else "FALSE"
            incomplete = f"NOT ({certified} AND {start}>=bounds.o{i}start AND {end}<=bounds.o{i}end AND {end}<=bounds.hi)"
            sibling_keys = " AND ".join(
                f"{c.column(node.child_entity, k, q)}={c.column(node.child_entity, k, pq)}"
                for k in r.child_fields
            )
            unknown_time = f"EXISTS (SELECT 1 FROM {q} WHERE {sibling_keys} AND p IS NOT FALSE AND event_time IS NULL)"
            truth.append(
                f"(SELECT CASE WHEN bool_or(p) IS TRUE THEN FALSE WHEN count(*) FILTER (WHERE p IS NULL)>0 OR {incomplete} OR {unknown_time} THEN NULL ELSE TRUE END FROM {q} WHERE {sibling_keys} AND event_time>{pq}.event_time AND event_time>={start} AND event_time<{end} AND event_time<bounds.hi)"
            )

    # Properties are resolved from the current authorized field registry.
    def field(step_id: UUID, ref: AggregateFieldRef):
        q = positive[step_id][0]
        i, f = c.field(node.child_entity, ref.field_id)
        if f.version_id != ref.version_id:
            fail("FILTER_SEQUENCE_PROPERTY_BINDING")
        if "eq" not in f.operators:
            fail("FILTER_SEQUENCE_PROPERTY_OPERATOR")
        known = f'{q}."k{i}" IS TRUE' if f.known_column else "TRUE"
        return f'{q}."f{i}"', known, f

    for binding in node.bindings:
        left, lk, lf = field(binding.left_step_id, binding.left_field)
        right, rk, rf = field(binding.right_step_id, binding.right_field)
        if (lf.data_type, lf.decimal_precision, lf.decimal_scale) != (
            rf.data_type,
            rf.decimal_precision,
            rf.decimal_scale,
        ):
            fail("FILTER_SEQUENCE_PROPERTY_TYPE")
        truth.append(f"(CASE WHEN {lk} AND {rk} THEN {left}={right} ELSE NULL END)")
    source = ",".join([q for q, _ in positive.values()] + ["bounds"])
    paths = (
        "SELECT "
        + " AND ".join(f"({t})" for t in truth)
        + f" AS matched FROM {source} WHERE "
        + " AND ".join(guards)
    )
    ctes.append("paths AS (" + paths + ")")
    fallback = " OR ".join(unknown)
    if len(c.parameters) > c.policy.max_values:
        fail("FILTER_PLAN_LIMIT")
    c.limitations.add("SEQUENCE_UNKNOWN_OBSERVATIONS_POSSIBLE")
    return (
        "(WITH "
        + ",".join(ctes)
        + f" SELECT CASE WHEN bool_or(matched) IS TRUE THEN TRUE WHEN count(*) FILTER (WHERE matched IS NULL)>0 OR ({fallback}) THEN NULL ELSE FALSE END FROM paths)"
    )
