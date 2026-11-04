"""Budgeted Parquet admission before Python row materialization for filtered queries."""
from __future__ import annotations

from time import monotonic
from typing import Any

import pyarrow as _pa  # pyright: ignore[reportMissingTypeStubs]
import pyarrow.compute as _pc  # pyright: ignore[reportMissingTypeStubs]
import pyarrow.parquet as _pq  # pyright: ignore[reportMissingTypeStubs]

from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import FilterResourcePolicy

pa: Any = _pa
pc: Any = _pc
pq: Any = _pq


def _rows(table: Any) -> tuple[dict[str, Any], ...]:
    return tuple(table.to_pylist())


def bounded_tables(raw_inputs: dict[str, bytes], policy: FilterResourcePolicy,
                   *, metadata_only: bool, deadline: float) -> dict[str, Any]:
    files: dict[str, Any] = {}
    rows = size = 0
    # Inspect every input before decoding any row. Preserve string dictionaries
    # until their expanded size is checked; compressed size alone is insufficient.
    for entity, raw in raw_inputs.items():
        if monotonic() >= deadline:
            raise AnalyticsFailure("FILTER_TIMEOUT")
        schema = pq.read_schema(pa.BufferReader(raw))
        strings = [f.name for f in schema if pa.types.is_string(f.type)]
        file = pq.ParquetFile(pa.BufferReader(raw), read_dictionary=strings)
        meta = file.metadata
        rows += meta.num_rows
        size += sum(meta.row_group(i).total_byte_size for i in range(meta.num_row_groups))
        if rows > policy.max_rows or size > policy.max_input_bytes:
            raise AnalyticsFailure("FILTER_INPUT_LIMIT")
        files[entity] = file
    tables: dict[str, Any] = {}
    expanded = 0
    for entity, file in files.items():
        if metadata_only and entity != "Store":
            continue
        batches: list[Any] = []
        for batch in file.iter_batches(batch_size=512, use_threads=False):
            if monotonic() >= deadline:
                raise AnalyticsFailure("FILTER_TIMEOUT")
            columns: list[Any] = []
            for column in batch.columns:
                if pa.types.is_dictionary(column.type):
                    lengths = pc.take(pc.binary_length(column.dictionary), column.indices)
                    expanded += int(pc.sum(lengths).as_py() or 0) + 4 * (len(column) + 1) + (len(column) + 7) // 8
                else:
                    expanded += column.nbytes
                if expanded > policy.max_input_bytes:
                    raise AnalyticsFailure("FILTER_INPUT_LIMIT")
                columns.append(pc.cast(column, pa.string()) if pa.types.is_dictionary(column.type) else column)
            batches.append(pa.RecordBatch.from_arrays(columns, names=batch.schema.names))
        tables[entity] = pa.Table.from_batches(batches) if batches else None
    return {entity: _rows(tables[entity]) if tables.get(entity) is not None else () for entity in files}
