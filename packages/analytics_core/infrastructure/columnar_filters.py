"""Real DuckDB flat filtering over verified, currently authorized Parquet inputs.

No SQL, paths, provider grants or resource configuration are accepted from a client.
The caller supplies a trusted access port; this adapter rechecks it before delivery.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
from threading import Event, Thread
from time import monotonic
from typing import Any, Generator, NoReturn
from uuid import UUID

import duckdb
import pyarrow as _pa  # pyright: ignore[reportMissingTypeStubs]
import pyarrow.compute as _pc  # pyright: ignore[reportMissingTypeStubs]
import pyarrow.parquet as _pq  # pyright: ignore[reportMissingTypeStubs]

from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import (
    FilterResourcePolicy,
    FilterValue,
    FlatExpression,
    FlatFilterAccess,
    FlatFilterRequest,
    FlatFilterResult,
    FlatInputGrant,
    FlatBoolean,
)
from packages.contracts.semantic.filter_fields import FilterFieldVersion
from packages.contracts.semantic.filter_events import EventTimeFieldVersion
from packages.contracts.analytics.columnar_filters import canonical_flat_expression
from packages.contracts.analytics.retail_filter import (
    FilterFacetQuery,
    FilterFacetResponse,
    FilterFacetValue,
)

# PyArrow 20 ships no stubs. Keep dynamic typing at this validated infrastructure edge.
pa: Any = _pa
pq: Any = _pq
pc: Any = _pc


def _fail(code: str) -> NoReturn:
    raise AnalyticsFailure(code)


def _identity(request: FlatFilterRequest, grant: FlatInputGrant) -> str:
    payload = {
        "engine": "duckdb-flat/v1",
        "engine_version": duckdb.__version__,
        "request": request.model_dump(mode="json", exclude={"expression"}),
        "expression": canonical_flat_expression(request.expression),
        "ceiling": canonical_flat_expression(grant.row_ceiling),
        "registry": grant.registry.model_dump(mode="json"),
        "resources": grant.resource_policy.model_dump(mode="json"),
        "actor": str(grant.actor_id),
        "policy": grant.policy_revision,
        "artifact": str(grant.binding.artifact_id),
        "content": grant.binding.content_hash,
        "row_id": grant.row_id_column,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _value(value: FilterValue, field: FilterFieldVersion) -> object:
    raw = value.value
    if value.data_type != field.data_type:
        _fail("FILTER_OPERAND_TYPE")
    if field.data_type == "string" and type(raw) is str:
        return raw
    if field.data_type == "boolean" and type(raw) is bool:
        return raw
    if field.data_type == "integer" and type(raw) is int and -(2**63) <= raw < 2**63:
        return raw
    if field.data_type == "date" and type(raw) is str:
        try:
            result = date.fromisoformat(raw)
            if result.isoformat() == raw:
                return result
        except ValueError:
            pass
    if field.data_type == "decimal" and type(raw) is str:
        try:
            number = Decimal(raw)
            if not number.is_finite():
                _fail("FILTER_OPERAND_TYPE")
            _, digits, exponent = number.as_tuple()
            if not isinstance(exponent, int):
                _fail("FILTER_OPERAND_TYPE")
            else:
                scale = max(-exponent, 0)
                width = max(len(digits) + exponent, 0) + field.decimal_scale
                if scale <= field.decimal_scale and width <= field.decimal_precision:
                    return number
        except InvalidOperation:
            pass
    _fail("FILTER_OPERAND_TYPE")


class FlatCompiler:
    def __init__(self, grant: FlatInputGrant) -> None:
        self.fields = {f.field_id: (i, f) for i, f in enumerate(grant.registry.fields)}
        self.policy = grant.resource_policy
        self.parameters: list[object] = []
        self.nodes = 0

    def compile(self, node: FlatExpression, depth: int = 1) -> str:
        self.nodes += 1
        if depth > self.policy.max_depth or self.nodes > self.policy.max_nodes:
            _fail("FILTER_PLAN_LIMIT")
        if node.kind == "not":
            return f"(NOT {self.compile(node.child, depth + 1)})"
        if isinstance(node, FlatBoolean):
            joiner = " AND " if node.kind == "and" else " OR "
            return "(" + joiner.join(self.compile(c, depth + 1) for c in node.children) + ")"
        entry = self.fields.get(node.field_id)
        if entry is None:
            _fail("FILTER_FIELD_FORBIDDEN")
        assert entry is not None
        index, field = entry
        if field.version_id != node.field_version_id or node.operator not in field.operators:
            _fail("FILTER_FIELD_VERSION_OR_OPERATOR")
        column = f'"f{index}"'
        if node.operator in {"is_null", "is_not_null"}:
            if node.values:
                _fail("FILTER_OPERAND_ARITY")
            operator = "IS NULL" if node.operator == "is_null" else "IS NOT NULL"
            sql = f"({column} {operator})"
        else:
            if not node.values or (node.operator != "in" and len(node.values) != 1):
                _fail("FILTER_OPERAND_ARITY")
            values = [_value(v, field) for v in node.values]
            if len(self.parameters) + len(values) > self.policy.max_values:
                _fail("FILTER_PLAN_LIMIT")
            self.parameters.extend(values)
            if node.operator == "in":
                sql = f"({column} IN ({','.join('?' for _ in values)}))"
            else:
                operator = {"eq": "=", "ne": "<>", "lt": "<", "le": "<=", "gt": ">", "ge": ">="}[
                    node.operator
                ]
                sql = f"({column} {operator} ?)"
            if field.null_policy == "not_matched":
                sql = f"coalesce({sql}, false)"
        if field.known_column is not None:
            sql = f'(CASE WHEN "k{index}" IS TRUE THEN {sql} ELSE NULL END)'
        return sql


@contextmanager
def isolated_connection(policy: FilterResourcePolicy) -> Generator[duckdb.DuckDBPyConnection]:
    """Settings are defense in depth; only generated bounded queries may be run."""
    connection = duckdb.connect(
        ":memory:",
        config={
            "enable_external_access": "false",
            "autoinstall_known_extensions": "false",
            "autoload_known_extensions": "false",
            "allow_community_extensions": "false",
            "allow_unsigned_extensions": "false",
            "allow_persistent_secrets": "false",
            "python_enable_replacements": "false",
            "threads": str(policy.threads),
            "memory_limit": f"{policy.memory_mb}MB",
            "temp_directory": "",
            "max_temp_directory_size": "0B",
        },
    )
    try:
        connection.execute("SET lock_configuration=true")
        yield connection
    finally:
        connection.close()


class DuckDBFlatFilter:
    def __init__(self, *, artifact_root: Path, access: FlatFilterAccess) -> None:
        if not artifact_root.is_absolute() or artifact_root.is_symlink():
            _fail("FILTER_ARTIFACT_ROOT")
        self.root = artifact_root.resolve(strict=True)
        self.access = access

    @staticmethod
    def _check_cancel(cancel: Event, deadline: float) -> None:
        check_execution(cancel, deadline)

    def _read(self, grant: FlatInputGrant, cancel: Event, deadline: float) -> Any:
        return read_admitted_input(self.root, grant, cancel, deadline)

    def fingerprint(self, request: FlatFilterRequest, *, actor_id: UUID) -> str:
        grant = self.access.authorize(
            workspace_id=request.workspace_id,
            actor_id=actor_id,
            dataset_version_id=request.dataset_version_id,
        )
        self._validate_grant(request, actor_id, grant)
        compiler = FlatCompiler(grant)
        compiler.compile(request.expression)
        compiler.compile(grant.row_ceiling)
        return _identity(request, grant)

    @staticmethod
    def _validate_grant(request: FlatFilterRequest, actor_id: UUID, grant: FlatInputGrant) -> None:
        if (
            grant.workspace_id != request.workspace_id
            or grant.actor_id != actor_id
            or grant.registry.dataset_version_id != request.dataset_version_id
            or grant.registry.version_id != request.registry_version_id
            or grant.binding.entity != grant.registry.entity
            or not grant.policy_revision
        ):
            _fail("FILTER_INPUT_BINDING")

    def execute(
        self, request: FlatFilterRequest, *, actor_id: UUID, cancel: Event | None = None
    ) -> FlatFilterResult:
        result = self._execute(request, actor_id=actor_id, cancel=cancel)
        assert isinstance(result, FlatFilterResult)
        return result

    def facets(
        self,
        request: FlatFilterRequest,
        facet: FilterFacetQuery,
        *,
        actor_id: UUID,
        cancel: Event | None = None,
    ) -> FilterFacetResponse:
        result = self._execute(request, actor_id=actor_id, cancel=cancel, facet=facet)
        assert isinstance(result, FilterFacetResponse)
        return result

    def _execute(
        self,
        request: FlatFilterRequest,
        *,
        actor_id: UUID,
        cancel: Event | None = None,
        facet: FilterFacetQuery | None = None,
    ) -> FlatFilterResult | FilterFacetResponse:
        cancel = cancel if cancel is not None else Event()
        if cancel.is_set():
            _fail("FILTER_CANCELLED")
        grant = self.access.authorize(
            workspace_id=request.workspace_id,
            actor_id=actor_id,
            dataset_version_id=request.dataset_version_id,
        )
        self._validate_grant(request, actor_id, grant)
        deadline = monotonic() + grant.resource_policy.timeout_ms / 1000
        compiler = FlatCompiler(grant)
        expression = compiler.compile(request.expression)
        ceiling = compiler.compile(grant.row_ceiling)
        parameters = compiler.parameters
        try:
            table = self._read(grant, cancel, deadline)
            with isolated_connection(grant.resource_policy) as connection:
                connection.register("input_0", table)
                done = Event()

                def monitor() -> None:
                    while not done.wait(0.005):
                        if cancel.is_set() or monotonic() >= deadline:
                            connection.interrupt()
                            # Interrupt can race with query start: keep interrupting until exit.

                watcher = Thread(target=monitor, daemon=True)
                watcher.start()
                try:
                    self._check_cancel(cancel, deadline)
                    count, distinct_count = connection.execute(
                        "SELECT count(*), count(DISTINCT row_id) FROM input_0"
                    ).fetchone() or (0, 0)
                    if count != distinct_count:
                        _fail("FILTER_INPUT_ROW_ID")
                    self._check_cancel(cancel, deadline)
                    # Projection cannot weaken the independently compiled ceiling.
                    sql = f"SELECT row_id, {expression} AS matched FROM input_0 WHERE ({ceiling}) IS TRUE ORDER BY row_id"
                    if facet is not None:
                        fields = {f.field_id: i for i, f in enumerate(grant.registry.fields)}
                        if facet.field_id not in fields:
                            _fail("FILTER_FIELD_FORBIDDEN")
                        column = f'"f{fields[facet.field_id]}"'
                        # Filter and security ceiling precede grouping and bounded pagination.
                        # Parameter order follows SELECT expression, ceiling, then lookup.
                        sql = (
                            f"WITH eligible AS (SELECT {column} AS value, {expression} AS matched "
                            f"FROM input_0 WHERE ({ceiling}) IS TRUE) "
                            "SELECT CAST(value AS VARCHAR), count(*) FROM eligible "
                            "WHERE matched IS TRUE AND (? = '' OR contains(lower(CAST(value AS VARCHAR)), lower(?))) "
                            "GROUP BY value ORDER BY CAST(value AS VARCHAR) NULLS LAST LIMIT ? OFFSET ?"
                        )
                        parameters = [
                            *parameters,
                            facet.search,
                            facet.search,
                            facet.limit + 1,
                            facet.offset,
                        ]
                    rows = connection.execute(sql, parameters).fetchall()
                    self._check_cancel(cancel, deadline)
                finally:
                    done.set()
                    watcher.join()
            current = self.access.authorize(
                workspace_id=request.workspace_id,
                actor_id=actor_id,
                dataset_version_id=request.dataset_version_id,
            )
            if current != grant:
                _fail("FILTER_POLICY_CHANGED")
            self._check_cancel(cancel, deadline)
            if facet is not None:
                return FilterFacetResponse(
                    request_hash=_identity(request, grant),
                    has_more=len(rows) > facet.limit,
                    values=[FilterFacetValue(value=r[0], count=r[1]) for r in rows[: facet.limit]],
                )
            return FlatFilterResult(
                request_hash=_identity(request, grant),
                matched_ids=tuple(row[0] for row in rows if row[1] is True),
                not_matched_count=sum(row[1] is False for row in rows),
                unknown_count=sum(row[1] is None for row in rows),
                authorized_count=len(rows),
            )
        except duckdb.InterruptException:
            self._check_cancel(cancel, deadline)
            raise AnalyticsFailure("FILTER_CANCELLED") from None
        except duckdb.OutOfMemoryException:
            raise AnalyticsFailure("FILTER_RESOURCE_LIMIT") from None
        except (duckdb.Error, pa.ArrowException, ValueError, KeyError):
            raise AnalyticsFailure("FILTER_EXECUTION_FAILED") from None


def read_admitted_input(
    root: Path,
    grant: FlatInputGrant,
    cancel: Event,
    deadline: float,
    *,
    widen_decimal_precision: bool = False,
    event_times: tuple[EventTimeFieldVersion, ...] = (),
) -> Any:
    """Open each path component without following symlinks; hash the exact bytes read."""
    path = PurePosixPath(grant.binding.relative_uri)
    if path.is_absolute() or not path.parts or any(p in {".", ".."} for p in path.parts):
        _fail("FILTER_ARTIFACT_PATH")
    descriptors: list[int] = []
    try:
        fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(fd)
        for part in path.parts[:-1]:
            fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            descriptors.append(fd)
        fd = os.open(path.parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        descriptors.append(fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            _fail("FILTER_ARTIFACT_PATH")
        if info.st_size > grant.resource_policy.max_input_bytes:
            _fail("FILTER_INPUT_LIMIT")
        chunks: list[bytes] = []
        size = 0
        while True:
            check_execution(cancel, deadline)
            chunk = os.read(fd, min(1024 * 1024, grant.resource_policy.max_input_bytes + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if size > grant.resource_policy.max_input_bytes:
                _fail("FILTER_INPUT_LIMIT")
        raw = b"".join(chunks)
    except OSError:
        raise AnalyticsFailure("FILTER_ARTIFACT_UNAVAILABLE") from None
    finally:
        for fd in reversed(descriptors):
            os.close(fd)
    if hashlib.sha256(raw).hexdigest() != grant.binding.content_hash:
        _fail("FILTER_ARTIFACT_INTEGRITY")
    check_execution(cancel, deadline)
    string_columns = {grant.row_id_column} | {
        field.column for field in grant.registry.fields if field.data_type == "string"
    }
    # Preserve dictionaries while decoding. A small dictionary may represent
    # gigabytes of repeated string bytes; never expand it before size preflight.
    parquet = pq.ParquetFile(pa.BufferReader(raw), read_dictionary=sorted(string_columns))
    metadata = parquet.metadata
    policy = grant.resource_policy
    if metadata.num_rows > policy.max_rows:
        _fail("FILTER_INPUT_LIMIT")
    if (
        sum(metadata.row_group(i).total_byte_size for i in range(metadata.num_row_groups))
        > policy.max_input_bytes
    ):
        _fail("FILTER_INPUT_LIMIT")
    columns = {grant.row_id_column}
    for field in grant.registry.fields:
        columns.add(field.column)
        if field.known_column:
            columns.add(field.known_column)
    for field in event_times:
        columns.add(field.column)
        if field.known_column:
            columns.add(field.known_column)
    schema = parquet.schema_arrow
    if len(set(schema.names)) != len(schema.names) or not columns <= set(schema.names):
        _fail("FILTER_INPUT_SCHEMA")
    expected_types = {grant.row_id_column: pa.string()}
    for field in grant.registry.fields:
        expected = {
            "string": pa.string(),
            "integer": pa.int64(),
            "boolean": pa.bool_(),
            "date": pa.date32(),
            "decimal": pa.decimal128(field.decimal_precision, field.decimal_scale),
        }[field.data_type]
        if field.column in expected_types and expected_types[field.column] != expected:
            _fail("FILTER_INPUT_SCHEMA")
        expected_types[field.column] = expected
        if field.known_column:
            if (
                field.known_column in expected_types
                and expected_types[field.known_column] != pa.bool_()
            ):
                _fail("FILTER_INPUT_SCHEMA")
            expected_types[field.known_column] = pa.bool_()
    for field in event_times:
        if field.entity != grant.registry.entity:
            _fail("FILTER_EVENT_TIME_BINDING")
        for name, expected in [
            (field.column, pa.timestamp("us", tz="UTC")),
            *([(field.known_column, pa.bool_())] if field.known_column else []),
        ]:
            if name in expected_types and expected_types[name] != expected:
                _fail("FILTER_INPUT_SCHEMA")
            expected_types[name] = expected
    for name, expected in expected_types.items():
        actual = schema.field(name).type
        if pa.types.is_dictionary(actual):
            actual = actual.value_type
        widening = (
            widen_decimal_precision
            and pa.types.is_decimal128(actual)
            and pa.types.is_decimal128(expected)
            and actual.scale == expected.scale
            and actual.precision <= expected.precision
        )
        if actual != expected and not widening:
            _fail("FILTER_INPUT_SCHEMA")
    batches: list[Any] = []
    expanded_bytes = 0
    # Fixed-width workspace for at most 512 rows at once, with cancellation
    # at each decode boundary. Output size is checked before dictionary casts.
    for batch in parquet.iter_batches(batch_size=512, columns=sorted(columns), use_threads=False):
        check_execution(cancel, deadline)
        for column in batch.columns:
            if pa.types.is_dictionary(column.type):
                lengths = pc.take(pc.binary_length(column.dictionary), column.indices)
                expanded_bytes += (
                    int(pc.sum(lengths).as_py() or 0)
                    + 4 * (len(column) + 1)
                    + (len(column) + 7) // 8
                )
            else:
                expanded_bytes += column.nbytes
        if expanded_bytes > policy.max_input_bytes:
            _fail("FILTER_INPUT_LIMIT")
        converted = [
            pc.cast(column, expected_types[name], safe=True)
            if column.type != expected_types[name]
            else column
            for name, column in zip(batch.schema.names, batch.columns, strict=True)
        ]
        batches.append(pa.RecordBatch.from_arrays(converted, names=batch.schema.names))
    check_execution(cancel, deadline)
    output_schema = pa.schema([(name, expected_types[name]) for name in sorted(columns)])
    table = pa.Table.from_batches(batches, schema=output_schema)
    arrays: list[Any] = []
    names: list[str] = []
    if len(set(table.column_names)) != len(table.column_names) or not columns <= set(
        table.column_names
    ):
        _fail("FILTER_INPUT_SCHEMA")
    row_id = table[grant.row_id_column]
    if row_id.type != pa.string() or row_id.null_count:
        _fail("FILTER_INPUT_ROW_ID")
    arrays.append(row_id)
    names.append("row_id")
    for i, field in enumerate(grant.registry.fields):
        column = table[field.column]
        expected = {
            "string": pa.string(),
            "integer": pa.int64(),
            "boolean": pa.bool_(),
            "date": pa.date32(),
            "decimal": pa.decimal128(field.decimal_precision, field.decimal_scale),
        }[field.data_type]
        if column.type != expected:
            _fail("FILTER_INPUT_SCHEMA")
        arrays.append(column)
        names.append(f"f{i}")
        if field.known_column is not None:
            known = table[field.known_column]
            if known.type != pa.bool_():
                _fail("FILTER_INPUT_SCHEMA")
            arrays.append(known)
            names.append(f"k{i}")
    for i, field in enumerate(event_times):
        # Exact native UTC microseconds, never a floating timestamp conversion.
        arrays.append(pc.cast(table[field.column], pa.int64(), safe=True))
        names.append(f"t{i}")
        if field.known_column:
            arrays.append(table[field.known_column])
            names.append(f"tk{i}")
    return pa.Table.from_arrays(arrays, names=names)


def check_execution(cancel: Event, deadline: float) -> None:
    if cancel.is_set():
        _fail("FILTER_CANCELLED")
    if monotonic() >= deadline:
        _fail("FILTER_TIMEOUT")
