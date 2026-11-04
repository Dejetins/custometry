"""Real Parquet storage precision may be narrower than its logical decimal field."""

from dataclasses import replace
from decimal import Decimal
import hashlib
from threading import Event
from time import monotonic
import pytest
import pyarrow as pa
import pyarrow.parquet as pq
from packages.contracts.analytics import AnalyticsFailure
from packages.analytics_core.infrastructure.columnar_filters import read_admitted_input
from tests.integration.analytics.test_relational_filters import setup as setup


@pytest.mark.parametrize(
    "precision,scale,allowed", [(8, 3, True), (18, 3, True), (19, 3, False), (8, 2, False)]
)
def test_only_same_scale_lossless_precision_widening(setup, precision, scale, allowed):
    _, access, _, _, _, root = setup
    grant = access.grant.entities[1]
    path = root / grant.binding.relative_uri
    table = pq.read_table(path)
    col = table.schema.get_field_index("quantity")
    table = table.set_column(
        col,
        "quantity",
        pa.array([Decimal("10")] * table.num_rows, type=pa.decimal128(precision, scale)),
    )
    pq.write_table(table, path)
    grant = replace(
        grant,
        binding=replace(grant.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()),
        registry=grant.registry.model_copy(
            update={
                "fields": tuple(
                    f.model_copy(
                        update={"data_type": "decimal", "decimal_precision": 18, "decimal_scale": 3}
                    )
                    if f.column == "quantity"
                    else f
                    for f in grant.registry.fields
                )
            }
        ),
    )

    def read(widen=False):
        return read_admitted_input(
            root, grant, Event(), monotonic() + 10, widen_decimal_precision=widen
        )

    if allowed:
        result = read(True)
        field = next(i for i, f in enumerate(grant.registry.fields) if f.column == "quantity")
        assert result[f"f{field}"].type == pa.decimal128(18, 3)
        assert result[f"f{field}"].to_pylist() == [Decimal("10.000")] * table.num_rows
    else:
        with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_SCHEMA"):
            read(True)
    if (precision, scale) != (18, 3):
        with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_SCHEMA"):
            read()
