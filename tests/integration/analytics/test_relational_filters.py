"""Actual Parquet/DuckDB foundation proof; access grants are synthetic trusted seams."""

from dataclasses import replace
import hashlib
from pathlib import Path
from threading import Event
from typing import Any, Generic, Generator, Literal, TypeVar, cast
from uuid import UUID, uuid4
import pytest
import pyarrow as _pa  # pyright: ignore[reportMissingTypeStubs]
import pyarrow.parquet as _pq  # pyright: ignore[reportMissingTypeStubs]
from pydantic import ValidationError
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import (
    FlatInputGrant,
    FlatPredicate,
    FilterValue,
    MaterializedFilterBinding,
    FlatFilterRequest,
)
from packages.contracts.analytics.relational_filters import (
    RelationalFilterRequest,
    RelationalInputGrant,
    RelationalResourcePolicy,
    RelationalFilterResult,
    RelationshipInput,
    ScopedPredicate,
    ScopedBoolean,
    ScopedNot,
    CorrelatedExists,
)
from packages.contracts.analytics.aggregate_filters import AggregateFilterRequest
from packages.contracts.analytics.sequence_filters import SequenceFilterRequest
from packages.contracts.analytics.receipt_cohorts import CohortFilterRequest
from packages.contracts.semantic.filter_fields import (
    FlatFilterRegistry,
    FilterFieldVersion,
    Operator,
)
from packages.contracts.semantic.relationships import FilterRelationshipVersion
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter


pa: Any = _pa
pq: Any = _pq
GrantT = TypeVar("GrantT", bound=RelationalInputGrant)


class Access(Generic[GrantT]):
    def __init__(self, grant: GrantT):
        self.grant = grant
        self.calls = 0
        self.changed = False

    def authorize(self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID) -> GrantT:
        self.calls += 1
        if self.changed and self.calls > 1:
            return replace(
                self.grant,
                entities=(
                    replace(self.grant.entities[0], policy_revision="revoked"),
                    *self.grant.entities[1:],
                ),
            )
        return self.grant


FilterSetup = tuple[DuckDBRelationalFilter, Access[GrantT], UUID, UUID, UUID, Path]
RelationalSetup = FilterSetup[RelationalInputGrant]


@pytest.fixture
def setup(tmp_path: Path) -> RelationalSetup:
    workspace, actor, dataset = uuid4(), uuid4(), uuid4()
    policy = RelationalResourcePolicy(
        version_id=uuid4(),
        max_rows=100,
        max_input_bytes=1024 * 1024,
        max_nodes=32,
        max_depth=12,
        max_values=100,
        memory_mb=64,
        threads=1,
        timeout_ms=5000,
        max_entities=2,
        max_correlations=8,
        max_fan_out=10,
        max_estimated_work=1000,
    )
    tables = {
        "Receipt": pa.table(
            {"id": ["a", "b", "c", "n", "secret"], "allowed": [True, True, True, True, False]}
        ),
        "ReceiptItem": pa.table(
            {
                "id": ["a1", "a2", "b1", "n1", "s1", "hidden"],
                "parent": ["a", "a", "b", "n", "secret", "c"],
                "color": pa.array(["red", "blue", "red", None, "red", "red"], pa.string()),
                "quantity": pa.array([5, 10, 10, 10, 10, 10], pa.int64()),
                "allowed": [True, True, True, True, True, False],
            }
        ),
    }
    entities: list[FlatInputGrant] = []
    for entity, table in tables.items():
        fields: list[FilterFieldVersion] = []
        for column in table.column_names:
            dtype = (
                "integer"
                if column == "quantity"
                else "boolean"
                if column == "allowed"
                else "string"
            )
            fields.append(
                FilterFieldVersion(
                    field_id=f"{entity}.{column}",
                    version_id=uuid4(),
                    entity=entity,
                    column=column,
                    data_type=dtype,
                    operators=("eq", "ge", "is_null"),
                    null_policy="unknown",
                )
            )
        registry = FlatFilterRegistry(
            version_id=uuid4(), dataset_version_id=dataset, entity=entity, fields=tuple(fields)
        )
        path = tmp_path / f"{entity}.parquet"
        pq.write_table(table, path)
        allowed = next(f for f in fields if f.column == "allowed")
        entities.append(
            FlatInputGrant(
                workspace_id=workspace,
                actor_id=actor,
                policy_revision="policy",
                binding=MaterializedFilterBinding(
                    workspace_id=workspace,
                    entity=entity,
                    artifact_id=uuid4(),
                    relative_uri=path.name,
                    content_hash=hashlib.sha256(path.read_bytes()).hexdigest(),
                ),
                registry=registry,
                resource_policy=policy,
                row_id_column="id",
                row_ceiling=FlatPredicate(
                    field_id=allowed.field_id,
                    field_version_id=allowed.version_id,
                    operator="eq",
                    values=(FilterValue(data_type="boolean", value=True),),
                ),
            )
        )
    relationship = FilterRelationshipVersion(
        relationship_id="receipt.items",
        version_id=uuid4(),
        parent_entity="Receipt",
        child_entity="ReceiptItem",
        parent_fields=("Receipt.id",),
        child_fields=("ReceiptItem.parent",),
        policy_version_id=uuid4(),
    )
    grant = RelationalInputGrant(
        entities=tuple(entities),
        relationships=(RelationshipInput(relationship, True, "a" * 64),),
        resource_policy=policy,
    )
    access = Access(grant)
    engine = DuckDBRelationalFilter(artifact_root=tmp_path, access=access)
    return engine, access, workspace, actor, dataset, tmp_path


def predicate(
    grant: RelationalInputGrant,
    scope: UUID,
    field: str,
    value: str | int | bool,
    operator: Operator = "eq",
) -> ScopedPredicate:
    f = next(f for e in grant.entities for f in e.registry.fields if f.field_id == field)
    return ScopedPredicate(
        node_id=uuid4(),
        scope_id=scope,
        field_id=field,
        field_version_id=f.version_id,
        operator=operator,
        values=(FilterValue(data_type=f.data_type, value=value),),
    )


def exists(
    grant: RelationalInputGrant,
    scope: UUID,
    *,
    both: bool = True,
    kind: Literal["exists", "not_exists"] = "exists",
    field: str = "ReceiptItem.color",
    value: str | int | bool = "red",
) -> CorrelatedExists:
    child = uuid4()
    r = grant.relationships[0].relationship
    pred: ScopedPredicate | ScopedBoolean = predicate(grant, child, field, value)
    if both:
        pred = ScopedBoolean(
            node_id=uuid4(),
            scope_id=child,
            kind="and",
            children=(pred, predicate(grant, child, "ReceiptItem.quantity", 10, "ge")),
        )
    return CorrelatedExists(
        node_id=uuid4(),
        scope_id=scope,
        parent_scope_id=scope,
        child_scope_id=child,
        child_entity="ReceiptItem",
        relationship_id=r.relationship_id,
        relationship_version_id=r.version_id,
        kind=kind,
        predicate=pred,
    )


def request(
    setup: RelationalSetup, kind: Literal["exists", "not_exists"] = "exists", complete: bool = True
) -> RelationalFilterRequest:
    _, access, w, _, d, _ = setup
    if not complete:
        access.grant = replace(
            access.grant, relationships=(replace(access.grant.relationships[0], complete=False),)
        )
    scope = uuid4()
    return RelationalFilterRequest(
        workspace_id=w,
        dataset_version_id=d,
        root_entity="Receipt",
        root_scope_id=scope,
        registry_versions={e.registry.entity: e.registry.version_id for e in access.grant.entities},
        expression=exists(access.grant, scope, kind=kind),
    )


def run(
    setup: FilterSetup[GrantT],
    query: RelationalFilterRequest
    | AggregateFilterRequest
    | SequenceFilterRequest
    | CohortFilterRequest,
) -> RelationalFilterResult:
    return setup[0].execute(query, actor_id=setup[3])


def test_empty_grant_fails_with_binding_error(setup: RelationalSetup):
    query = request(setup)
    setup[1].grant = replace(setup[1].grant, entities=())
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_BINDING"):
        run(setup, query)


def test_same_row_conjunction_differs_from_independent_exists_and_keeps_root_grain(
    setup: RelationalSetup,
):
    query = request(setup)
    same = run(setup, query)
    assert (
        same.matched_ids == ("b",)
        and same.not_matched_count == 2
        and same.unknown_count == 1
        and same.authorized_count == 4
    )
    grant = setup[1].grant
    left = exists(grant, query.root_scope_id, both=False)
    right = exists(grant, query.root_scope_id, both=False, field="ReceiptItem.quantity", value=10)
    independent = query.model_copy(
        update={
            "expression": ScopedBoolean(
                node_id=uuid4(), scope_id=query.root_scope_id, kind="and", children=(left, right)
            )
        }
    )
    result = run(setup, independent)
    assert result.matched_ids == ("a", "b") and result.authorized_count == 4
    assert "secret" not in result.matched_ids and "c" not in result.matched_ids


@pytest.mark.parametrize(
    "kind,complete,matched,false,unknown",
    [
        ("exists", True, ("b",), 2, 1),
        ("not_exists", True, ("a", "c"), 1, 1),
        ("exists", False, ("b",), 0, 3),
        ("not_exists", False, (), 1, 3),
    ],
)
def test_complete_incomplete_and_not_unknown_truth_table(
    setup: RelationalSetup,
    kind: Literal["exists", "not_exists"],
    complete: bool,
    matched: tuple[str, ...],
    false: int,
    unknown: int,
):
    result = run(setup, request(setup, kind, complete))
    assert (result.matched_ids, result.not_matched_count, result.unknown_count) == (
        matched,
        false,
        unknown,
    )
    assert bool(result.limitation_codes) == (not complete)


def test_reordering_boolean_preserves_identity_scope_changes_do_not(setup: RelationalSetup):
    query = request(setup)
    engine = setup[0]
    actor = setup[3]
    inner = cast(ScopedBoolean, cast(CorrelatedExists, query.expression).predicate)
    reordered = query.model_copy(
        update={
            "expression": query.expression.model_copy(
                update={
                    "predicate": inner.model_copy(
                        update={"children": tuple(reversed(inner.children))}
                    )
                }
            )
        }
    )
    assert engine.fingerprint(query, actor_id=actor) == engine.fingerprint(
        reordered, actor_id=actor
    )
    assert run(setup, query).matched_ids == run(setup, reordered).matched_ids
    moved = query.model_copy(
        update={
            "expression": query.expression.model_copy(
                update={"predicate": inner.model_copy(update={"scope_id": query.root_scope_id})}
            )
        }
    )
    with pytest.raises(AnalyticsFailure, match="SCOPE_INVALID"):
        run(setup, moved)
    with pytest.raises(ValidationError):
        FlatFilterRequest.model_validate(query.model_dump(mode="json"))


@pytest.mark.parametrize(
    "change,code",
    [
        ("scope", "SCOPE_INVALID"),
        ("relationship", "RELATIONSHIP_BINDING"),
        ("registry", "REGISTRY_BINDING"),
        ("field", "FIELD_FORBIDDEN"),
        ("operand", "OPERAND_TYPE"),
        ("duplicate", "SCOPE_INVALID"),
    ],
)
def test_typed_scope_and_dependency_rejections_before_input_read(
    setup: RelationalSetup, change: str, code: str
):
    query = request(setup)
    node = cast(CorrelatedExists, query.expression)
    inner = cast(ScopedBoolean, node.predicate)
    pred = inner.children[0]
    if change == "scope":
        node = node.model_copy(update={"parent_scope_id": uuid4()})
    if change == "relationship":
        node = node.model_copy(update={"relationship_version_id": uuid4()})
    if change == "registry":
        query = query.model_copy(update={"registry_versions": {}})
    if change == "field":
        node = node.model_copy(
            update={"predicate": pred.model_copy(update={"field_id": "forbidden"})}
        )
    if change == "operand":
        node = node.model_copy(
            update={
                "predicate": pred.model_copy(
                    update={"values": (FilterValue(data_type="integer", value=5),)}
                )
            }
        )
    if change == "duplicate":
        node = node.model_copy(
            update={"predicate": inner.model_copy(update={"children": (pred, pred)})}
        )
    query = query.model_copy(update={"expression": node})
    for path in setup[-1].glob("*.parquet"):
        path.unlink()
    with pytest.raises(AnalyticsFailure, match=code):
        run(setup, query)


@pytest.mark.parametrize(
    "setting,value,code",
    [
        ("max_depth", 1, "PLAN_LIMIT"),
        ("max_nodes", 1, "PLAN_LIMIT"),
        ("max_values", 1, "PLAN_LIMIT"),
        ("max_fan_out", 1, "FAN_OUT_LIMIT"),
        ("max_estimated_work", 1, "WORK_LIMIT"),
        ("max_rows", 4, "INPUT_LIMIT"),
        ("max_input_bytes", 10, "INPUT_LIMIT"),
    ],
)
def test_bounded_resource_admission(setup: RelationalSetup, setting: str, value: int, code: str):
    query = request(setup)
    access = setup[1]
    access.grant = replace(
        access.grant,
        resource_policy=access.grant.resource_policy.model_copy(update={setting: value}),
    )
    with pytest.raises(AnalyticsFailure, match=code):
        run(setup, query)


def test_policy_revalidation_and_precancel(setup: RelationalSetup):
    query = request(setup)
    setup[1].changed = True
    with pytest.raises(AnalyticsFailure, match="POLICY_CHANGED"):
        run(setup, query)
    setup[1].changed = False
    cancel = Event()
    cancel.set()
    with pytest.raises(AnalyticsFailure, match="CANCELLED"):
        setup[0].execute(query, actor_id=setup[3], cancel=cancel)


def test_corrupt_child_bytes_fail_integrity(setup: RelationalSetup):
    query = request(setup)
    (setup[-1] / "ReceiptItem.parquet").write_bytes(b"corrupt")
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_INTEGRITY"):
        run(setup, query)


@pytest.mark.parametrize("mode", ["cancel", "timeout"])
def test_interrupt_native_operation_and_recover(
    setup: RelationalSetup, monkeypatch: pytest.MonkeyPatch, mode: str
):
    """Controlled native workload exercises the monitor, not a mocked interruption."""
    import duckdb
    from contextlib import contextmanager
    from threading import Thread
    import packages.analytics_core.infrastructure.relational_filters as implementation

    started = Event()
    cancelled = Event()
    original = implementation.isolated_connection
    connections: list[Any] = []

    class Probe:
        def __init__(self, connection: Any):
            self.connection = connection
            self.first = True

        def register(self, *args: Any) -> Any:
            return self.connection.register(*args)

        def interrupt(self) -> Any:
            return self.connection.interrupt()

        def execute(self, *args: Any) -> Any:
            if self.first:
                self.first = False
                started.set()
                # 100M native arithmetic pairs; no filesystem or test data exposure.
                self.connection.execute(
                    "SELECT sum(i*j) FROM range(10000) a(i), range(10000) b(j)"
                ).fetchone()
            return self.connection.execute(*args)

    @contextmanager
    def instrumented(policy: RelationalResourcePolicy) -> Generator[Probe, None, None]:
        with original(policy) as connection:
            connections.append(connection)
            yield Probe(connection)

    monkeypatch.setattr(implementation, "isolated_connection", instrumented)
    access = setup[1]
    query = request(setup)
    if mode == "timeout":
        access.grant = replace(
            access.grant,
            resource_policy=access.grant.resource_policy.model_copy(update={"timeout_ms": 25}),
        )

    def cancel_active():
        if started.wait(2):
            cancelled.set()

    worker = Thread(target=cancel_active)
    if mode == "cancel":
        worker.start()
    try:
        with pytest.raises(
            AnalyticsFailure, match="^FILTER_CANCELLED$" if mode == "cancel" else "^FILTER_TIMEOUT$"
        ):
            setup[0].execute(query, actor_id=setup[3], cancel=cancelled)
    finally:
        if mode == "cancel":
            worker.join(timeout=3)
    assert connections
    with pytest.raises(duckdb.Error):
        connections[0].execute("SELECT 1")
    monkeypatch.setattr(implementation, "isolated_connection", original)
    access.grant = replace(
        access.grant,
        resource_policy=access.grant.resource_policy.model_copy(update={"timeout_ms": 5000}),
    )
    assert run(setup, query).matched_ids == ("b",)


def test_not_and_or_preserve_unknown_membership(setup: RelationalSetup):
    query = request(setup, complete=False)
    scope = query.root_scope_id
    negated = query.model_copy(
        update={"expression": ScopedNot(node_id=uuid4(), scope_id=scope, child=query.expression)}
    )
    assert run(setup, negated).unknown_count == 3
    true = predicate(setup[1].grant, scope, "Receipt.id", "c")
    either = query.model_copy(
        update={
            "expression": ScopedBoolean(
                node_id=uuid4(), scope_id=scope, kind="or", children=(query.expression, true)
            )
        }
    )
    result = run(setup, either)
    assert result.matched_ids == ("b", "c") and result.unknown_count == 2
    both = query.model_copy(
        update={
            "expression": ScopedBoolean(
                node_id=uuid4(), scope_id=scope, kind="and", children=(query.expression, true)
            )
        }
    )
    result = run(setup, both)
    assert result.matched_ids == () and result.not_matched_count == 3 and result.unknown_count == 1


@pytest.mark.parametrize(
    "corruption,code",
    [
        ("duplicate", "INPUT_ROW_ID"),
        ("orphan", "RELATIONSHIP_KEYS"),
        ("null", "RELATIONSHIP_KEYS"),
        ("parent_cardinality", "RELATIONSHIP_CARDINALITY"),
    ],
)
def test_actual_input_grain_and_relationship_key_preflight(
    setup: RelationalSetup, corruption: str, code: str
):
    query = request(setup)
    access = setup[1]
    entity = "Receipt" if corruption == "parent_cardinality" else "ReceiptItem"
    path = setup[-1] / f"{entity}.parquet"
    table = pq.read_table(path)
    if corruption == "duplicate":
        table = pa.concat_tables([table, table.slice(0, 1)])
    elif corruption in ("orphan", "null"):
        values = table["parent"].to_pylist()
        values[0] = "missing" if corruption == "orphan" else None
        table = table.set_column(
            table.schema.get_field_index("parent"), "parent", pa.array(values, pa.string())
        )
    else:
        # Different row IDs with duplicate published parent join keys.
        table = table.append_column("join_key", pa.array(["same", "same", "c", "n", "secret"]))
        parent = access.grant.entities[0]
        fields = (
            *parent.registry.fields,
            FilterFieldVersion(
                field_id="Receipt.join_key",
                version_id=uuid4(),
                entity="Receipt",
                column="join_key",
                data_type="string",
                operators=("eq",),
                null_policy="unknown",
            ),
        )
        parent = replace(parent, registry=parent.registry.model_copy(update={"fields": fields}))
        relation = access.grant.relationships[0]
        access.grant = replace(
            access.grant,
            entities=(parent, access.grant.entities[1]),
            relationships=(
                replace(
                    relation,
                    relationship=relation.relationship.model_copy(
                        update={"parent_fields": ("Receipt.join_key",)}
                    ),
                ),
            ),
        )
    pq.write_table(table, path)
    access.grant = replace(
        access.grant,
        entities=tuple(
            replace(
                e,
                binding=replace(
                    e.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()
                ),
            )
            if e.registry.entity == entity
            else e
            for e in access.grant.entities
        ),
    )
    with pytest.raises(AnalyticsFailure, match=code):
        run(setup, query)


def test_relationship_keys_cannot_depend_on_unknown_property_history(setup: RelationalSetup):
    query = request(setup)
    access = setup[1]
    parent = access.grant.entities[0]
    fields = tuple(
        f.model_copy(update={"known_column": "known"}) if f.field_id == "Receipt.id" else f
        for f in parent.registry.fields
    )
    access.grant = replace(
        access.grant,
        entities=(
            replace(parent, registry=parent.registry.model_copy(update={"fields": fields})),
            access.grant.entities[1],
        ),
    )
    with pytest.raises(AnalyticsFailure, match="RELATIONSHIP_KEY_UNKNOWN"):
        run(setup, query)


def test_policy_and_completeness_participate_in_identity(setup: RelationalSetup):
    query = request(setup)
    engine, access = setup[:2]
    before = engine.fingerprint(query, actor_id=setup[3])
    relation = access.grant.relationships[0]
    access.grant = replace(access.grant, relationships=(replace(relation, complete=False),))
    assert engine.fingerprint(query, actor_id=setup[3]) != before
    access.grant = replace(
        access.grant, relationships=(replace(relation, completeness_hash="b" * 64),)
    )
    assert engine.fingerprint(query, actor_id=setup[3]) != before


@pytest.mark.parametrize("field", ["workspace_id", "actor_id", "dataset_version_id"])
def test_grant_cannot_be_reused_for_foreign_request(setup: RelationalSetup, field: str):
    query = request(setup)
    kwargs: dict[str, Any] = {"actor_id": setup[3]}
    if field == "actor_id":
        kwargs[field] = uuid4()
    else:
        query = query.model_copy(update={field: uuid4()})
    with pytest.raises(AnalyticsFailure, match="INPUT_BINDING"):
        setup[0].execute(query, **kwargs)


def test_actual_preserved_flat_reader_rejects_correlated_nodes(setup: RelationalSetup):
    import importlib.util
    import sys
    from pathlib import Path

    spec = importlib.util.spec_from_file_location(
        "ms017_old_flat", Path(".codex/delivery/evidence/MS-017/preparation/flat-before.py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    query = request(setup)
    with pytest.raises(ValidationError):
        module.FlatFilterRequest.model_validate(query.model_dump(mode="json"))


def test_nested_related_scope_uses_correct_parent_alias(setup: RelationalSetup):
    _, access, w, a, d, root = setup
    grant = access.grant
    policy = grant.resource_policy.model_copy(update={"max_entities": 3})
    table = pa.table(
        {"id": ["t1", "t2"], "item": ["a1", "b1"], "tag": ["sale", "sale"], "allowed": [True, True]}
    )
    path = root / "Tag.parquet"
    pq.write_table(table, path)
    fields = tuple(
        FilterFieldVersion(
            field_id="Tag." + column,
            version_id=uuid4(),
            entity="Tag",
            column=column,
            data_type="boolean" if column == "allowed" else "string",
            operators=("eq",),
            null_policy="unknown",
        )
        for column in table.column_names
    )
    allowed = next(f for f in fields if f.column == "allowed")
    entity = FlatInputGrant(
        workspace_id=w,
        actor_id=a,
        policy_revision="policy",
        binding=MaterializedFilterBinding(
            workspace_id=w,
            entity="Tag",
            artifact_id=uuid4(),
            relative_uri=path.name,
            content_hash=hashlib.sha256(path.read_bytes()).hexdigest(),
        ),
        registry=FlatFilterRegistry(
            version_id=uuid4(), dataset_version_id=d, entity="Tag", fields=fields
        ),
        resource_policy=policy,
        row_id_column="id",
        row_ceiling=FlatPredicate(
            field_id=allowed.field_id,
            field_version_id=allowed.version_id,
            operator="eq",
            values=(FilterValue(data_type="boolean", value=True),),
        ),
    )
    relation = FilterRelationshipVersion(
        relationship_id="item.tags",
        version_id=uuid4(),
        parent_entity="ReceiptItem",
        child_entity="Tag",
        parent_fields=("ReceiptItem.id",),
        child_fields=("Tag.item",),
        policy_version_id=uuid4(),
    )
    access.grant = replace(
        grant,
        entities=(*grant.entities, entity),
        relationships=(*grant.relationships, RelationshipInput(relation, True, "b" * 64)),
        resource_policy=policy,
    )
    query = request(setup)
    outer = cast(CorrelatedExists, query.expression)
    child = outer.child_scope_id
    leaf = uuid4()
    nested = CorrelatedExists(
        node_id=uuid4(),
        scope_id=child,
        parent_scope_id=child,
        child_scope_id=leaf,
        child_entity="Tag",
        relationship_id=relation.relationship_id,
        relationship_version_id=relation.version_id,
        kind="exists",
        predicate=predicate(access.grant, leaf, "Tag.tag", "sale"),
    )
    outer = outer.model_copy(
        update={
            "predicate": ScopedBoolean(
                node_id=uuid4(),
                scope_id=child,
                kind="and",
                children=(predicate(access.grant, child, "ReceiptItem.quantity", 10, "ge"), nested),
            )
        }
    )
    result = run(setup, query.model_copy(update={"expression": outer}))
    assert result.matched_ids == ("b",) and result.authorized_count == 4


@pytest.mark.parametrize("field,value", [("max_rows", 1), ("max_input_bytes", 1), ("max_nodes", 1)])
def test_per_input_policy_cannot_be_relaxed_by_global_budget(
    setup: RelationalSetup, field: str, value: int
):
    query = request(setup)
    access = setup[1]
    entity = access.grant.entities[0]
    entity = replace(
        entity, resource_policy=entity.resource_policy.model_copy(update={field: value})
    )
    access.grant = replace(access.grant, entities=(entity, *access.grant.entities[1:]))
    with pytest.raises(AnalyticsFailure, match="INPUT_LIMIT|PLAN_LIMIT"):
        run(setup, query)


def test_per_input_resource_revision_changes_fingerprint(setup: RelationalSetup):
    query = request(setup)
    engine, access = setup[:2]
    before = engine.fingerprint(query, actor_id=setup[3])
    entity = access.grant.entities[0]
    entity = replace(
        entity, resource_policy=entity.resource_policy.model_copy(update={"version_id": uuid4()})
    )
    access.grant = replace(access.grant, entities=(entity, *access.grant.entities[1:]))
    assert engine.fingerprint(query, actor_id=setup[3]) != before
