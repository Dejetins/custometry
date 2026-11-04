"""Real engine/admission tests; no mocked SQL execution or retained runtime data."""

from dataclasses import replace
from decimal import Decimal
import hashlib
from threading import Event
from uuid import uuid4

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from pydantic import ValidationError

from packages.analytics_core.infrastructure.columnar_filters import (
    DuckDBFlatFilter,
    isolated_connection,
)
from packages.contracts.analytics import AnalyticsFailure, SemanticArtifactBinding
from packages.contracts.analytics.columnar_filters import (
    FilterResourcePolicy,
    FilterValue,
    FlatBoolean,
    FlatFilterRequest,
    FlatInputGrant,
    FlatNot,
    FlatPredicate,
)
from packages.contracts.semantic.filter_fields import FilterFieldVersion, FlatFilterRegistry


class Access:
    def __init__(self, grant):
        self.grant = grant
        self.calls = 0
        self.revoke = False

    def authorize(self, **kwargs):
        self.calls += 1
        if self.revoke and self.calls > 1:
            raise AnalyticsFailure("FORBIDDEN")
        assert kwargs == {
            "workspace_id": self.grant.workspace_id,
            "actor_id": self.grant.actor_id,
            "dataset_version_id": self.grant.registry.dataset_version_id,
        }
        return self.grant


@pytest.fixture
def setup(tmp_path):
    fields = (
        FilterFieldVersion(
            field_id="allowed",
            version_id=uuid4(),
            entity="Receipt",
            column="allowed",
            data_type="boolean",
            operators=("eq",),
            null_policy="not_matched",
        ),
        FilterFieldVersion(
            field_id="amount",
            version_id=uuid4(),
            entity="Receipt",
            column="amount",
            data_type="decimal",
            operators=("eq", "gt", "is_null"),
            null_policy="not_matched",
            known_column="known",
        ),
        FilterFieldVersion(
            field_id="label",
            version_id=uuid4(),
            entity="Receipt",
            column="label",
            data_type="string",
            operators=("eq", "in"),
            null_policy="unknown",
        ),
    )
    registry = FlatFilterRegistry(
        version_id=uuid4(), dataset_version_id=uuid4(), entity="Receipt", fields=fields
    )
    table = pa.table(
        {
            "id": pa.array(["a", "b", "c", "d", "secret"], pa.string()),
            "amount": pa.array(
                [Decimal("1.01"), Decimal("1.02"), None, Decimal("9.99"), Decimal("1.01")],
                pa.decimal128(18, 2),
            ),
            "known": pa.array([True, True, True, False, True], pa.bool_()),
            "allowed": pa.array([True, True, True, True, False], pa.bool_()),
            "label": pa.array(["first", "second", None, "fourth", "hidden"], pa.string()),
        }
    )
    artifact = tmp_path / "input.parquet"
    pq.write_table(table, artifact)
    binding = SemanticArtifactBinding(
        entity="Receipt",
        artifact_id=uuid4(),
        relative_uri=artifact.name,
        content_hash=hashlib.sha256(artifact.read_bytes()).hexdigest(),
        source_system_id=uuid4(),
    )
    policy = FilterResourcePolicy(
        version_id=uuid4(),
        max_rows=100,
        max_input_bytes=1024 * 1024,
        max_nodes=30,
        max_depth=10,
        max_values=100,
        memory_mb=64,
        threads=1,
        timeout_ms=5000,
    )
    ceiling = FlatPredicate(
        field_id="allowed",
        field_version_id=fields[0].version_id,
        operator="eq",
        values=(FilterValue(data_type="boolean", value=True),),
    )
    grant = FlatInputGrant(
        workspace_id=uuid4(),
        actor_id=uuid4(),
        policy_revision="policy-1",
        binding=binding,
        registry=registry,
        resource_policy=policy,
        row_ceiling=ceiling,
        row_id_column="id",
    )
    access = Access(grant)
    engine = DuckDBFlatFilter(artifact_root=tmp_path, access=access)
    request = FlatFilterRequest(
        workspace_id=grant.workspace_id,
        dataset_version_id=registry.dataset_version_id,
        registry_version_id=registry.version_id,
        expression=FlatPredicate(
            field_id="amount",
            field_version_id=fields[1].version_id,
            operator="eq",
            values=(FilterValue(data_type="decimal", value="1.01"),),
        ),
    )
    return engine, access, request, artifact


def run(setup, expression=None, **kwargs):
    engine, access, request, _ = setup
    if expression is not None:
        request = request.model_copy(update={"expression": expression})
    return engine.execute(request, actor_id=access.grant.actor_id, **kwargs)


def test_exact_decimal_unknown_and_authorized_coverage(setup):
    result = run(setup)
    assert result.matched_ids == ("a",)
    assert (result.not_matched_count, result.unknown_count, result.authorized_count) == (2, 1, 4)
    assert setup[1].calls == 2
    assert result.preview_kind == "exact"


def test_not_unknown_and_null_policy_are_distinct(setup):
    expr = setup[2].expression
    result = run(setup, FlatNot(child=expr))
    assert result.matched_ids == ("b", "c")  # known NULL is not_matched under this field policy
    assert result.unknown_count == 1
    is_null = expr.model_copy(update={"operator": "is_null", "values": ()})
    result = run(setup, is_null)
    assert result.matched_ids == ("c",)
    assert result.unknown_count == 1


@pytest.mark.parametrize(
    "kind,negate,expected,unknown",
    [
        ("and", False, ("a",), 1),
        ("or", False, ("a",), 1),
        ("and", True, (), 1),
        ("or", True, ("a", "b", "c"), 1),
    ],
)
def test_boolean_three_valued_logic(setup, kind, negate, expected, unknown):
    expr = setup[2].expression
    result = run(
        setup, FlatBoolean(kind=kind, children=(expr, FlatNot(child=expr) if negate else expr))
    )
    assert result.matched_ids == expected
    assert result.unknown_count == unknown


def test_user_or_cannot_escape_mandatory_ceiling(setup):
    expr = setup[2].expression
    result = run(setup, FlatBoolean(kind="or", children=(expr, FlatNot(child=expr))))
    assert "secret" not in result.matched_ids
    assert result.authorized_count == 4


def test_identity_commutative_and_policy_sensitive(setup):
    expr = setup[2].expression
    a = run(setup, FlatBoolean(kind="or", children=(expr, FlatNot(child=expr))))
    b = run(setup, FlatBoolean(kind="or", children=(FlatNot(child=expr), expr)))
    assert a.request_hash == b.request_hash
    setup[1].grant = replace(setup[1].grant, policy_revision="policy-2")
    assert (
        run(setup, FlatBoolean(kind="or", children=(expr, FlatNot(child=expr)))).request_hash
        != a.request_hash
    )


def test_revoke_before_delivery(setup):
    setup[1].revoke = True
    with pytest.raises(AnalyticsFailure, match="^FORBIDDEN$"):
        run(setup)


@pytest.mark.parametrize(
    "change,code",
    [
        ({"field_id": "hidden"}, "FILTER_FIELD_FORBIDDEN"),
        ({"field_version_id": uuid4()}, "FILTER_FIELD_VERSION_OR_OPERATOR"),
        ({"operator": "lt"}, "FILTER_FIELD_VERSION_OR_OPERATOR"),
        ({"values": ()}, "FILTER_OPERAND_ARITY"),
        ({"values": (FilterValue(data_type="decimal", value="NaN"),)}, "FILTER_OPERAND_TYPE"),
        ({"values": (FilterValue(data_type="decimal", value="1.001"),)}, "FILTER_OPERAND_TYPE"),
        ({"values": (FilterValue(data_type="decimal", value="1e999"),)}, "FILTER_OPERAND_TYPE"),
        ({"values": (FilterValue(data_type="integer", value=1),)}, "FILTER_OPERAND_TYPE"),
    ],
)
def test_invalid_predicate_rejected_before_read(setup, change, code):
    setup[3].unlink()
    with pytest.raises(AnalyticsFailure, match=f"^{code}$"):
        run(setup, setup[2].expression.model_copy(update=change))


def test_bound_sql_value_and_untrusted_column_names(setup):
    field = setup[1].grant.registry.fields[2]
    expr = FlatPredicate(
        field_id=field.field_id,
        field_version_id=field.version_id,
        operator="eq",
        values=(FilterValue(data_type="string", value="'; COPY input_0 TO '/tmp/leak'; --"),),
    )
    result = run(setup, expr)
    assert result.matched_ids == ()
    assert result.unknown_count == 1
    # Provider source names are resolved in Arrow, never interpolated into SQL.
    table = pq.read_table(setup[3]).rename_columns(
        ["id", "amount", "known", "allowed", 'label";SELECT 1;--']
    )
    pq.write_table(table, setup[3])
    grant = setup[1].grant
    changed = field.model_copy(update={"column": 'label";SELECT 1;--'})
    setup[1].grant = replace(
        grant,
        registry=grant.registry.model_copy(
            update={"fields": (*grant.registry.fields[:2], changed)}
        ),
        binding=replace(
            grant.binding, content_hash=hashlib.sha256(setup[3].read_bytes()).hexdigest()
        ),
    )
    assert run(setup, expr).matched_ids == ()


@pytest.mark.parametrize(
    "limits,code",
    [
        ({"max_rows": 4}, "FILTER_INPUT_LIMIT"),
        ({"max_input_bytes": 1}, "FILTER_INPUT_LIMIT"),
        ({"max_nodes": 1}, "FILTER_PLAN_LIMIT"),
        ({"max_values": 1}, "FILTER_PLAN_LIMIT"),
    ],
)
def test_resource_preflight(setup, limits, code):
    grant = setup[1].grant
    setup[1].grant = replace(grant, resource_policy=grant.resource_policy.model_copy(update=limits))
    with pytest.raises(AnalyticsFailure, match=f"^{code}$"):
        run(setup)


def test_depth_limit(setup):
    grant = setup[1].grant
    setup[1].grant = replace(
        grant, resource_policy=grant.resource_policy.model_copy(update={"max_depth": 1})
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_PLAN_LIMIT"):
        run(setup, FlatNot(child=setup[2].expression))


def test_integrity_failure_is_sanitized(setup):
    setup[3].write_bytes(b"sensitive provider data")
    with pytest.raises(AnalyticsFailure, match="^FILTER_ARTIFACT_INTEGRITY$"):
        run(setup)


@pytest.mark.parametrize("relative", ["../input.parquet", "/tmp/input.parquet"])
def test_path_escape_rejected(setup, relative):
    access = setup[1]
    access.grant = replace(
        access.grant, binding=replace(access.grant.binding, relative_uri=relative)
    )
    with pytest.raises(AnalyticsFailure, match="^FILTER_ARTIFACT_PATH$"):
        run(setup)


def test_symlink_rejected(setup):
    target = setup[3].with_name("link.parquet")
    target.symlink_to(setup[3])
    access = setup[1]
    access.grant = replace(
        access.grant, binding=replace(access.grant.binding, relative_uri=target.name)
    )
    with pytest.raises(AnalyticsFailure, match="^FILTER_ARTIFACT_UNAVAILABLE$"):
        run(setup)


def test_precancel_no_admission(setup):
    event = Event()
    event.set()
    with pytest.raises(AnalyticsFailure, match="^FILTER_CANCELLED$"):
        run(setup, cancel=event)
    assert setup[1].calls == 0


@pytest.mark.parametrize(
    "statement",
    [
        "SELECT * FROM read_csv('/etc/passwd')",
        "COPY (SELECT 1) TO '/tmp/custometry-forbidden.csv'",
        "INSTALL httpfs",
        "LOAD httpfs",
        "SET enable_external_access=true",
        "SET threads=8",
    ],
)
def test_engine_restrictions(setup, statement):
    with isolated_connection(setup[1].grant.resource_policy) as connection:
        with pytest.raises(duckdb.Error):
            connection.execute(statement)


def test_connections_are_isolated(setup):
    policy = setup[1].grant.resource_policy
    with isolated_connection(policy) as one, isolated_connection(policy) as two:
        one.execute("CREATE TABLE private_input AS SELECT 1")
        with pytest.raises(duckdb.Error):
            two.execute("SELECT * FROM private_input")


def test_unknown_nodes_and_coerced_values_rejected():
    with pytest.raises(ValidationError):
        FlatFilterRequest.model_validate(
            {
                "workspace_id": str(uuid4()),
                "dataset_version_id": str(uuid4()),
                "registry_version_id": str(uuid4()),
                "expression": {"kind": "sequence", "sql": "select 1"},
            }
        )
    with pytest.raises(ValidationError):
        FilterValue(data_type="decimal", value=1.01)


def rewrite_artifact(setup, table):
    pq.write_table(table, setup[3])
    access = setup[1]
    access.grant = replace(
        access.grant,
        binding=replace(
            access.grant.binding, content_hash=hashlib.sha256(setup[3].read_bytes()).hexdigest()
        ),
    )


@pytest.mark.parametrize(
    "bad_ids", [["a", "a", "c", "d", "secret"], ["a", None, "c", "d", "secret"]]
)
def test_unique_nonnull_root_grain(setup, bad_ids):
    table = pq.read_table(setup[3])
    rewrite_artifact(setup, table.set_column(0, "id", pa.array(bad_ids, pa.string())))
    with pytest.raises(AnalyticsFailure, match="^FILTER_INPUT_ROW_ID$"):
        run(setup)


def test_no_implicit_numeric_coercion(setup):
    table = pq.read_table(setup[3])
    rewrite_artifact(setup, table.set_column(1, "amount", pa.array([1.01] * 5, pa.float64())))
    with pytest.raises(AnalyticsFailure, match="^FILTER_INPUT_SCHEMA$"):
        run(setup)


def test_missing_column_rejected(setup):
    rewrite_artifact(setup, pq.read_table(setup[3]).drop_columns(["known"]))
    with pytest.raises(AnalyticsFailure, match="^FILTER_INPUT_SCHEMA$"):
        run(setup)


def test_registry_mismatch_before_artifact_read(setup):
    engine, access, request, artifact = setup
    artifact.unlink()
    with pytest.raises(AnalyticsFailure, match="^FILTER_INPUT_BINDING$"):
        engine.execute(
            request.model_copy(update={"registry_version_id": uuid4()}),
            actor_id=access.grant.actor_id,
        )


@pytest.mark.parametrize("mode", ["cancel", "timeout"])
def test_interrupt_native_operation_and_recover(setup, monkeypatch, mode):
    """Controlled native workload exercises the monitor, not a mocked interruption."""
    from contextlib import contextmanager
    from threading import Thread
    import packages.analytics_core.infrastructure.columnar_filters as implementation

    started = Event()
    cancelled = Event()
    original = implementation.isolated_connection
    connections = []

    class Probe:
        def __init__(self, connection):
            self.connection = connection
            self.first = True

        def register(self, *args):
            return self.connection.register(*args)

        def interrupt(self):
            return self.connection.interrupt()

        def execute(self, *args):
            if self.first:
                self.first = False
                started.set()
                # 100M native arithmetic pairs; no filesystem or test data exposure.
                self.connection.execute(
                    "SELECT sum(i*j) FROM range(10000) a(i), range(10000) b(j)"
                ).fetchone()
            return self.connection.execute(*args)

    @contextmanager
    def instrumented(policy):
        with original(policy) as connection:
            connections.append(connection)
            yield Probe(connection)

    monkeypatch.setattr(implementation, "isolated_connection", instrumented)
    access = setup[1]
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
            run(setup, cancel=cancelled)
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
    assert run(setup).matched_ids == ("a",)


def test_dictionary_expansion_rejected_before_cast(setup, monkeypatch):
    import packages.analytics_core.infrastructure.columnar_filters as implementation

    rows = 10000
    table = pa.table(
        {
            "id": pa.array([str(i) for i in range(rows)], pa.string()),
            "amount": pa.array([Decimal("1.01")] * rows, pa.decimal128(18, 2)),
            "known": pa.array([True] * rows, pa.bool_()),
            "allowed": pa.array([True] * rows, pa.bool_()),
            "label": pa.array(["x" * 4096] * rows, pa.string()),
        }
    )
    rewrite_artifact(setup, table)
    access = setup[1]
    access.grant = replace(
        access.grant,
        resource_policy=access.grant.resource_policy.model_copy(update={"max_rows": rows}),
    )
    assert setup[3].stat().st_size < 1024 * 1024
    casts = []
    original_cast = implementation.pc.cast

    def observed_cast(*args, **kwargs):
        casts.append(True)
        return original_cast(*args, **kwargs)

    monkeypatch.setattr(implementation.pc, "cast", observed_cast)
    with pytest.raises(AnalyticsFailure, match="^FILTER_INPUT_LIMIT$"):
        run(setup)
    assert not casts  # first 512-row dictionary expansion denied before materialization


def test_cancel_at_arrow_decode_boundary(setup, monkeypatch):
    import packages.analytics_core.infrastructure.columnar_filters as implementation

    cancelled = Event()
    original = implementation.pq.ParquetFile
    decoded = []

    class FileProbe:
        def __init__(self, *args, **kwargs):
            self.file = original(*args, **kwargs)
            self.metadata = self.file.metadata
            self.schema_arrow = self.file.schema_arrow

        def iter_batches(self, **kwargs):
            for batch in self.file.iter_batches(**kwargs):
                decoded.append(batch.num_rows)
                cancelled.set()
                yield batch

    monkeypatch.setattr(implementation.pq, "ParquetFile", FileProbe)
    with pytest.raises(AnalyticsFailure, match="^FILTER_CANCELLED$"):
        run(setup, cancel=cancelled)
    assert decoded
    assert setup[1].calls == 1  # never reaches delivery
