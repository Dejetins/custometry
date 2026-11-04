"""Resource rejection precedes Python row materialization and eager legacy reads."""

from time import monotonic
from unittest.mock import Mock
from uuid import uuid4

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from packages.artifacts.infrastructure import bounded_sales
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import FilterResourcePolicy, FlatPredicate
from packages.contracts.analytics.retail_filter import ReceiptFilterInput
from packages.analytics_core.application.workspace_service import WorkspaceAnalyticsService
from tests.unit.analytics.test_workspace_calculation import fixture


def policy(**updates):
    values = dict(
        version_id=uuid4(),
        max_rows=100,
        max_input_bytes=1024 * 1024,
        max_nodes=64,
        max_depth=12,
        max_values=1000,
        memory_mb=64,
        threads=1,
        timeout_ms=10000,
    )
    return FilterResourcePolicy(**(values | updates))


def raw(table):
    sink = pa.BufferOutputStream()
    pq.write_table(table, sink)
    return sink.getvalue().to_pybytes()


def test_metadata_limit_rejects_before_any_table_becomes_python_rows(monkeypatch):
    rows = Mock(side_effect=AssertionError("must not materialize"))
    monkeypatch.setattr(bounded_sales, "_rows", rows)
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_LIMIT"):
        bounded_sales.bounded_tables(
            {
                "Store": raw(pa.table({"id": ["1"]})),
                "Receipt": raw(pa.table({"id": ["1", "2", "3"]})),
            },
            policy(max_rows=2),
            metadata_only=False,
            deadline=monotonic() + 10,
        )
    rows.assert_not_called()


def test_dictionary_expansion_rejects_before_python_rows(monkeypatch):
    rows = Mock(side_effect=AssertionError("must not materialize"))
    monkeypatch.setattr(bounded_sales, "_rows", rows)
    data = raw(pa.table({"value": ["x" * 1000] * 1000}))
    assert len(data) < 100_000
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_LIMIT"):
        bounded_sales.bounded_tables(
            {"Receipt": data},
            policy(max_rows=2000, max_input_bytes=100_000),
            metadata_only=False,
            deadline=monotonic() + 10,
        )
    rows.assert_not_called()


def test_metadata_only_reads_store_without_receipt_rows():
    result = bounded_sales.bounded_tables(
        {
            "Store": raw(pa.table({"store_id": ["1"]})),
            "Receipt": raw(pa.table({"receipt_id": ["a"]})),
        },
        policy(),
        metadata_only=True,
        deadline=monotonic() + 10,
    )
    assert result == {"Store": ({"store_id": "1"},), "Receipt": ()}


def test_filtered_query_does_not_invoke_unbounded_legacy_loader():
    request, source, _, access, _ = fixture()
    request = request.model_copy(
        update={
            "receipt_filter": ReceiptFilterInput(
                registry_version_id=uuid4(),
                expression=FlatPredicate(
                    field_id="Receipt.status", field_version_id=uuid4(), operator="is_null"
                ),
            )
        }
    )
    semantics = Mock()
    semantics.sales_projection.return_value = source
    artifacts = Mock()
    filters = Mock()
    filters.inputs.side_effect = AnalyticsFailure("FILTER_INPUT_LIMIT")
    service = WorkspaceAnalyticsService(
        semantics=semantics,
        results=Mock(),
        artifacts=artifacts,
        calendars=Mock(),
        access=Mock(),
        receipt_filters=filters,
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_LIMIT"):
        service.query_inputs(access, request)
    artifacts.read_sales_inputs.assert_not_called()


def test_full_preflight_bounds_store_before_identity_decodes_or_filter_inputs():
    from custometry_api.analytics.workspace_access import IdentityWorkspaceAccess
    from packages.contracts.identity.access import ResourceAccess

    request, source, _, access, _ = fixture()
    request = request.model_copy(
        update={
            "receipt_filter": ReceiptFilterInput(
                registry_version_id=uuid4(),
                expression=FlatPredicate(
                    field_id="Receipt.status", field_version_id=uuid4(), operator="is_null"
                ),
            )
        }
    )
    semantics = Mock()
    semantics.sales_projection.return_value = source
    artifacts = Mock()
    filters = Mock()
    identity = Mock()
    identity.resolve_resource.return_value = ResourceAccess(
        True, "a" * 64, None, frozenset({"analysis.read", "analysis.run"})
    )
    limit = policy(max_rows=1)
    raw_store = raw(pa.table({"store_id": ["1", "2"]}))
    bounded = Mock()
    bounded.read_bounded_sales_inputs.side_effect = lambda **kw: bounded_sales.bounded_tables(
        {"Store": raw_store}, kw["policy"], metadata_only=True, deadline=monotonic() + 10
    )
    dataset_access = IdentityWorkspaceAccess(
        identity, semantics, artifacts, store_reader=bounded, store_policy=limit
    )
    service = WorkspaceAnalyticsService(
        semantics=semantics,
        results=Mock(),
        artifacts=artifacts,
        calendars=Mock(),
        access=dataset_access,
        receipt_filters=filters,
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_LIMIT"):
        service.preflight(
            workspace_id=access.workspace_id, principal_id=access.principal_id, request=request
        )
    artifacts.read_sales_inputs.assert_not_called()
    filters.inputs.assert_not_called()
