from concurrent.futures import ThreadPoolExecutor
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from apps.worker_data.vertical_slice import DataPipelineRunner
from packages.analytics_core.application.service import AnalyticsService
from packages.analytics_core.infrastructure.local import LocalAnalyticsArtifactStore
from packages.analytics_core.infrastructure.postgres import PostgresAnalyticsRepository
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sales_report import SalesReportRequest
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from tests.integration.data_pipeline.test_retail_report import request_for


def test_real_report_oracle_concurrency_and_artifact_failures(
    data_pipeline_runtime, tmp_path: Path
):
    runtime = data_pipeline_runtime
    runner = DataPipelineRunner(
        connector=runtime.connector,
        connect=runtime.connect,
        artifact_store=LocalArtifactStore(tmp_path),
    )
    intake = request_for(runtime)
    prepared = runner.run(intake)
    repository = PostgresAnalyticsRepository(runtime.connect)
    artifacts = SalesArtifactStore(runtime.connect, tmp_path)
    service = AnalyticsService(
        projections=repository,
        artifacts=LocalAnalyticsArtifactStore(tmp_path),
        results=repository,
        result_store=LocalAnalyticsArtifactStore(tmp_path),
        sales_semantics=PostgresSalesSemanticRepository(runtime.connect),
        sales_results=repository,
        sales_artifacts=artifacts,
    )
    actor = dict(
        workspace_id=runtime.workspace_id,
        principal_id=runtime.actor_id,
        permissions=frozenset({"analysis.read", "analysis.run"}),
    )
    request = SalesReportRequest(
        prepared.semantic_dataset_version_id, comparison="previous_year_same_dates"
    )
    # All contenders use the same production services, DB uniqueness and immutable files.
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(
            pool.map(lambda _: service.run_sales_report(**actor, request=request), range(4))
        )
    assert all(r == results[0] for r in results)
    result = results[0]
    assert len(result["daily"]) == 334
    assert result["trust"]["quality_accounting"]["quarantined_count"] == 5
    assert result["comparability_status"] == "comparable"
    # Independent readonly source SQL: receipt headers only, no production helper.
    import psycopg

    target = runtime.connector._target
    with psycopg.connect(
        host=target.host,
        port=target.port,
        dbname=target.dbname,
        user=target.user,
        password=target.password,
    ) as source:
        source.execute("SET TRANSACTION READ ONLY")
        for store, start, end in (
            (None, date(2025, 1, 1), date(2025, 11, 30)),
            ("1", date(2025, 1, 1), date(2025, 11, 30)),
            (None, date(2024, 1, 1), date(2024, 11, 30)),
            (None, date(2025, 6, 1), date(2025, 6, 30)),
        ):
            calculated = service.run_sales_report(
                **actor,
                request=SalesReportRequest(prepared.semantic_dataset_version_id, start, end, store),
            )
            row = source.execute(
                """SELECT sum(net_amount), count(DISTINCT receipt_id), count(*) FILTER(WHERE customer_id IS NULL)
               FROM retail.receipts WHERE status='completed' AND currency='EUR'
               AND (receipt_datetime AT TIME ZONE 'UTC')::date BETWEEN %s AND %s
               AND (%s::text IS NULL OR store_id::text=%s)""",
                (start, end, store, store),
            ).fetchone()
            assert Decimal(calculated["totals"]["net_revenue"]) == row[0]
            assert Decimal(calculated["totals"]["receipt_count"]) == row[1]
            assert Decimal(calculated["totals"]["average_receipt"]) == row[0] / row[1]
            assert row[2] > 0
            assert (
                sum(
                    Decimal(d["net_revenue"])
                    for d in calculated["daily"]
                    if d["net_revenue"] is not None
                )
                == row[0]
            )
        assert source.execute(
            "SELECT min(n),max(n) FROM (SELECT count(*) n FROM retail.receipt_items GROUP BY receipt_id) x"
        ).fetchone() == (3, 3)
    assert service.run_sales_report(**actor, request=request) == result
    assert service.get_sales_report(**actor, result_id=UUID(result["result_id"])) == result
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        service.get_sales_report(
            **{**actor, "permissions": frozenset({"analysis.read"})},
            result_id=UUID(result["result_id"]),
        )
    with pytest.raises(AnalyticsFailure, match="NOT_FOUND"):
        service.get_sales_report(
            **{**actor, "principal_id": uuid4()}, result_id=UUID(result["result_id"])
        )
    changed_policy = service.run_sales_report(
        **{**actor, "permissions": actor["permissions"] | {"extra.permission"}}, request=request
    )
    assert changed_policy["result_id"] != result["result_id"]
    # Controlled next-input snapshot over real source rows; the source DB is never mutated.
    from plugins.connector_postgresql.adapter import PostgreSQLConnector

    class NextSnapshot(PostgreSQLConnector):
        def extract(self, **kwargs):
            rows = super().extract(**kwargs)
            if kwargs["object_name"] == "receipts":
                return tuple(
                    {
                        **r,
                        "net_amount": r["net_amount"] + Decimal(1),
                        "gross_amount": r["gross_amount"] + Decimal(1),
                    }
                    for r in rows
                )
            return rows

    next_runner = DataPipelineRunner(
        connector=NextSnapshot(runtime.connector._target),
        connect=runtime.connect,
        artifact_store=LocalArtifactStore(tmp_path),
    )
    newer = next_runner.run(request_for(runtime))
    assert newer.semantic_dataset_version_id != prepared.semantic_dataset_version_id
    updated = service.run_sales_report(
        **actor,
        request=SalesReportRequest(
            newer.semantic_dataset_version_id, comparison="previous_year_same_dates"
        ),
    )
    assert Decimal(updated["totals"]["net_revenue"]) == Decimal(
        result["totals"]["net_revenue"]
    ) + Decimal(result["totals"]["receipt_count"])
    assert updated["result_id"] != result["result_id"]
    assert service.get_sales_report(**actor, result_id=UUID(result["result_id"])) == result
    assert runner.run(intake).semantic_dataset_version_id == prepared.semantic_dataset_version_id
    receipt = next(m for m in prepared.artifact_manifests if m.entity == "Receipt")
    path = tmp_path / receipt.relative_uri
    saved = path.read_bytes()
    path.write_bytes(b"invalid")
    try:
        with pytest.raises(AnalyticsFailure, match="ARTIFACT_INTEGRITY_FAILED"):
            service.run_sales_report(**actor, request=request)
        assert service.get_sales_report(**actor, result_id=UUID(result["result_id"])) == result
    finally:
        path.write_bytes(saved)
    path.unlink()
    try:
        with pytest.raises(AnalyticsFailure, match="ARTIFACT_UNAVAILABLE"):
            service.run_sales_report(**actor, request=request)
    finally:
        path.write_bytes(saved)
    with pytest.raises(AnalyticsFailure, match="SEMANTIC_DATASET_NOT_FOUND"):
        service.run_sales_report(**{**actor, "workspace_id": uuid4()}, request=request)
    output = tmp_path / result["manifest"]["relative_uri"]
    output.unlink()
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_UNAVAILABLE"):
        service.get_sales_report(**actor, result_id=UUID(result["result_id"]))
