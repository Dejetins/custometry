"""Real six-table intake, isolated PostgreSQL oracle and immutable result evidence."""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from decimal import Decimal, localcontext
import json
import os
from pathlib import Path
from typing import Any, TypedDict, cast
from uuid import UUID, uuid4
import psycopg
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from custometry_api.analytics.workspace_router import workspace_router
from custometry_api.main import create_app
from apps.worker_data.vertical_slice import DataPipelineRunner
from packages.analytics_core.application.workspace_service import WorkspaceAnalyticsService
from packages.analytics_core.application.workspace_calculation import digest
from packages.analytics_core.infrastructure.postgres import PostgresAnalyticsRepository
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.artifacts.infrastructure.workspace import WorkspaceArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.workspace import (
    WorkspaceAccess,
    WorkspaceRunRequest,
    WorkspaceCardRequest,
    MetricRef,
)
from packages.contracts.semantic import (
    BusinessCalendarProfile,
    BusinessCalendarVersion,
    UpdateCalendarRequest,
)
from packages.semantic_model.application.calendar import WorkspaceCalendarService
from packages.semantic_model.infrastructure.calendar import PostgresCalendarRepository
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from tests.integration.data_pipeline.conftest import DataPipelineRuntime
from tests.integration.data_pipeline.test_retail_report import request_for


def source_connect(runtime: DataPipelineRuntime):
    target = cast(Any, runtime.connector)._target
    return psycopg.connect(
        host=target.host,
        port=target.port,
        dbname=target.dbname,
        user=target.user,
        password=target.password,
    )


class Access:
    """Explicit trusted test projection; S03 supplies real Identity implementation."""

    def __init__(self, value: WorkspaceAccess):
        self.value = value
        self.denied = False

    def resolve(
        self, *, workspace_id: UUID, principal_id: UUID, dataset_id: UUID, action: str
    ) -> WorkspaceAccess:
        if self.denied or (workspace_id, principal_id, dataset_id) != (
            self.value.workspace_id,
            self.value.principal_id,
            self.value.semantic_dataset_version_id,
        ):
            raise AnalyticsFailure("FORBIDDEN")
        return self.value


def seed_edges(runtime: DataPipelineRuntime) -> None:
    assert os.environ.get("MS004_S02_OWNED_DATABASE") == "1", "only task-owned disposable source"
    with source_connect(runtime) as c:
        # Source writes are exclusively synthetic task fixture setup, before production readonly intake.
        c.execute("TRUNCATE retail.receipts CASCADE")
        c.execute("DELETE FROM retail.calendar")
        c.execute("""INSERT INTO retail.calendar
          SELECT d::date,extract(isoyear FROM d)::int,extract(week FROM d)::int,date_trunc('month',d)::date,true
          FROM generate_series('2023-01-01'::date,'2025-12-31'::date,'1 day') d""")
        c.execute("""INSERT INTO retail.receipts
          (receipt_id,receipt_number,receipt_datetime,customer_id,store_id,channel_id,currency,gross_amount,discount_amount,net_amount,status,updated_at)
          SELECT n,'MS004-'||n,d + interval '12 hours',NULL,store,1,'EUR',amount,0,amount,'completed',d+interval '12 hours'
          FROM (SELECT row_number() OVER (ORDER BY d,store,i) n,d,store,
            (extract(year FROM d)-2020)*10 + i*7 AS amount
            FROM generate_series('2023-01-01'::date,'2025-12-31'::date,'1 day') d
            CROSS JOIN generate_series(1,3) store CROSS JOIN generate_series(1,3) i
            WHERE i <= 1 + extract(day FROM d)::int % 3) x""")
        c.execute("""INSERT INTO retail.receipt_items
          SELECT receipt_id*3+i,receipt_id,1,1,net_amount/3,0,net_amount/3 FROM retail.receipts CROSS JOIN generate_series(1,3) i""")
        # Known no-receipt baseline while Calendar declares complete.
        c.execute(
            "DELETE FROM retail.receipt_items WHERE receipt_id IN (SELECT receipt_id FROM retail.receipts WHERE store_id=2 AND receipt_datetime::date='2024-06-02')"
        )
        c.execute(
            "DELETE FROM retail.receipts WHERE store_id=2 AND receipt_datetime::date='2024-06-02'"
        )
        # Zero is real data, unlike empty. Missing Calendar day has no fact to keep intake admission valid.
        c.execute(
            "UPDATE retail.receipts SET net_amount=0,gross_amount=0 WHERE store_id=3 AND receipt_datetime::date='2024-06-03'"
        )
        c.execute(
            "UPDATE retail.calendar SET is_period_complete=false WHERE calendar_date='2023-01-02'"
        )
        c.execute(
            "DELETE FROM retail.receipt_items WHERE receipt_id IN (SELECT receipt_id FROM retail.receipts WHERE receipt_datetime::date='2023-01-03')"
        )
        c.execute("DELETE FROM retail.receipts WHERE receipt_datetime::date='2023-01-03'")
        c.execute("DELETE FROM retail.calendar WHERE calendar_date='2023-01-03'")
        c.execute(
            "UPDATE retail.receipt_items SET product_id=999999 WHERE receipt_item_id IN (SELECT receipt_item_id FROM retail.receipt_items ORDER BY receipt_item_id LIMIT 5)"
        )


@pytest.fixture
def s02_runtime(data_pipeline_runtime: DataPipelineRuntime):
    if os.environ.get("MS004_S02_OWNED_DATABASE") != "1":
        pytest.skip("requires run_s02.py isolated fixture")
    try:
        yield data_pipeline_runtime
    finally:
        # Our immutable calendar fixtures reference the actor; clean only this disposable DB.
        with data_pipeline_runtime.connect() as c:
            c.execute(
                "TRUNCATE semantic_workspace_calendar_defaults, semantic_business_calendar_versions CASCADE"
            )


def test_s02_real_corpus_oracle_and_artifacts(
    s02_runtime: DataPipelineRuntime, tmp_path: Path
) -> None:
    runtime = s02_runtime
    if os.environ.get("MS004_S02_OWNED_DATABASE") != "1":
        pytest.skip("requires run_s02.py isolated fixture")
    seed_edges(runtime)
    prepared = DataPipelineRunner(
        connector=runtime.connector,
        connect=runtime.connect,
        artifact_store=LocalArtifactStore(tmp_path),
    ).run(request_for(runtime))
    if prepared.state != "committed":
        with runtime.connect() as c:
            failure = c.execute(
                "SELECT violations FROM data_quality_reports WHERE id=%s",
                (prepared.quality_report_id,),
            ).fetchone()
            pytest.fail(str(failure))
    assert prepared.state == "committed" and prepared.semantic_dataset_version_id
    dataset = prepared.semantic_dataset_version_id
    access = Access(
        WorkspaceAccess(
            workspace_id=runtime.workspace_id,
            principal_id=runtime.actor_id,
            semantic_dataset_version_id=dataset,
            policy_hash=digest({"policy_version": 1, "stores": ["1", "2", "3"]}),
            allowed_store_ids=["1", "2", "3"],
            permissions=frozenset(
                {"workspace.read", "workspace.manage", "analysis.read", "analysis.run"}
            ),
        )
    )
    calendars = WorkspaceCalendarService(PostgresCalendarRepository(runtime.connect))
    calendars.provision(runtime.workspace_id)
    artifacts = WorkspaceArtifactStore(runtime.connect, tmp_path)
    semantics = PostgresSalesSemanticRepository(runtime.connect)
    source = semantics.sales_projection(workspace_id=runtime.workspace_id, version_id=dataset)
    service = WorkspaceAnalyticsService(
        semantics=semantics,
        results=PostgresAnalyticsRepository(runtime.connect),
        artifacts=artifacts,
        calendars=calendars,
        access=access,
    )

    class Actor(TypedDict):
        workspace_id: UUID
        principal_id: UUID

    actor: Actor = {"workspace_id": runtime.workspace_id, "principal_id": runtime.actor_id}
    refs = [
        MetricRef.model_validate({k: m[k] for k in ("metric_id", "version_id", "content_hash")})
        for m in source["metrics"]
    ]
    current = calendars.get_default(runtime.workspace_id, access.value)
    versions: list[BusinessCalendarVersion] = []
    for start in (1, 4, 10):
        for label in ("start_year", "end_year"):
            current = calendars.update_default(
                UpdateCalendarRequest(
                    profile=BusinessCalendarProfile(
                        fiscal_year_start_month=start, year_label=label
                    ),
                    expected_revision=current.revision,
                    idempotency_key=uuid4(),
                ),
                access.value,
            )
            versions.append(current.calendar)

    def request(
        start: str = "2025-01-01",
        end: str = "2025-11-30",
        grain: str = "day",
        stores: list[str] | None = None,
        local: list[str] | None = None,
        version: Any = None,
        basis: str = "fiscal",
        alignment: str = "previous_year_same_dates",
    ) -> WorkspaceRunRequest:
        version = version or versions[3]
        return WorkspaceRunRequest.model_validate(
            {
                "semantic_dataset_version_id": dataset,
                "common": {"starts_on": start, "ends_on": end, "store_ids": stores},
                "local_store_ids": local,
                "grain": grain,
                "calendar_ref": {
                    "version_id": version.version_id,
                    "content_hash": version.content_hash,
                },
                "calendar_basis": basis,
                "alignment": alignment,
                "metric_refs": refs,
            }
        )

    def run(req: WorkspaceRunRequest):
        return service.run(**actor, request=req)

    oracle_checks = 0
    with source_connect(runtime) as sql:
        sql.execute("SET TRANSACTION READ ONLY")
        actual_counts = sql.execute(
            """SELECT min(receipt_datetime)::date,max(receipt_datetime)::date,count(*),count(DISTINCT receipt_datetime::date),count(DISTINCT store_id) FROM retail.receipts WHERE status='completed' AND currency='EUR'"""
        ).fetchone()
        assert (
            actual_counts
            and actual_counts[0] == date(2023, 1, 1)
            and actual_counts[1] == date(2025, 12, 31)
        )
        store_coverage = sql.execute("""SELECT store_id,count(*),count(DISTINCT receipt_datetime::date),min(receipt_datetime)::date,max(receipt_datetime)::date
            FROM retail.receipts WHERE status='completed' AND currency='EUR' GROUP BY store_id ORDER BY store_id""").fetchall()
        calendar_counts = sql.execute(
            "SELECT count(*),count(*) FILTER(WHERE is_period_complete) FROM retail.calendar"
        ).fetchone()

        def oracle(ds: list[date], stores: list[str]):
            row = sql.execute(
                """SELECT sum(net_amount), count(DISTINCT receipt_id),count(DISTINCT (receipt_datetime AT TIME ZONE 'UTC')::date)
              FROM retail.receipts WHERE status='completed' AND currency='EUR' AND store_id::text=ANY(%s)
              AND (receipt_datetime AT TIME ZONE 'UTC')::date=ANY(%s)""",
                (stores, ds),
            ).fetchone()
            assert row
            return row

        # Independent SQL checks values, boundaries and completeness for all six grains/policies.
        for version in versions:
            for basis in ("calendar", "fiscal"):
                for grain in ("day", "week", "month", "quarter", "half_year", "year"):
                    result = run(
                        request("2024-12-27", "2025-07-06", grain, version=version, basis=basis)
                    )
                    for bucket in result.buckets:
                        ds = [
                            d.date
                            for d in result.daily
                            if bucket.effective_start <= d.date < bucket.effective_end_exclusive
                        ]
                        net, count, observed = oracle(ds, ["1", "2", "3"])
                        assert Decimal(bucket.values.net_revenue or "NaN") == net
                        assert Decimal(bucket.values.receipt_count or "NaN") == count
                        # Same rational rounded at documented server Decimal precision, independently from aggregation.

                        with localcontext() as ctx:
                            ctx.prec = 38
                            assert Decimal(bucket.values.average_receipt or "NaN") == net / Decimal(
                                count
                            )
                        assert bucket.coverage.observed_days == observed
                        assert (
                            bucket.coverage.expected_days
                            == bucket.coverage.calendar_days
                            == bucket.coverage.declared_complete_days
                            == len(ds)
                        )
                        assert bucket.coverage.state == "complete"
                        assert bucket.is_partial_bucket == (
                            bucket.bucket_start != bucket.effective_start
                            or bucket.bucket_end_exclusive != bucket.effective_end_exclusive
                        )
                        # PostgreSQL month arithmetic, separate from production boundary helper.
                        width = {"quarter": 3, "half_year": 6, "year": 12}.get(grain)
                        if width:
                            sm = version.profile.fiscal_year_start_month if basis == "fiscal" else 1
                            expected = sql.execute(
                                """WITH d AS (SELECT %s::date AS dt), f AS
                                (SELECT make_date(extract(year FROM dt)::int-(extract(month FROM dt)::int < %s)::int,%s,1) origin, dt FROM d), b AS
                                (SELECT origin + make_interval(months => ((extract(year FROM dt)::int-extract(year FROM origin)::int)*12+extract(month FROM dt)::int-extract(month FROM origin)::int)/%s*%s) AS bucket_begin FROM f)
                                SELECT bucket_begin::date,(bucket_begin+make_interval(months=>%s))::date FROM b""",
                                (ds[0], sm, sm, width, width, width),
                            ).fetchone()
                            assert expected == (bucket.bucket_start, bucket.bucket_end_exclusive)
                        if basis == "fiscal":
                            fiscal_start_year = ds[0].year - (
                                ds[0].month < version.profile.fiscal_year_start_month
                            )
                            expected_year = (
                                fiscal_start_year
                                if version.profile.year_label == "start_year"
                                or version.profile.fiscal_year_start_month == 1
                                else fiscal_start_year + 1
                            )
                            assert bucket.fiscal_year == expected_year
                            if grain in ("quarter", "half_year", "year"):
                                assert bucket.label.startswith(f"FY{expected_year}")
                                if grain == "quarter":
                                    assert (
                                        bucket.label
                                        == f"FY{expected_year} Q{bucket.fiscal_quarter}"
                                    )
                                if grain == "half_year":
                                    assert (
                                        bucket.label == f"FY{expected_year} H{bucket.fiscal_half}"
                                    )
                        oracle_checks += 1
                    assert result.temporal
                    # Independent source-SQL date sequence/mapping, not dates supplied by the result.
                    mapping_rows = sql.execute("""SELECT dt::date,(dt-interval '1 year')::date
                        FROM generate_series('2024-12-27'::date,'2025-07-06'::date,'1 day') dt ORDER BY dt""").fetchall()
                    expected_mapping = dict(mapping_rows)
                    assert [
                        (m.current_date, m.baseline_date) for m in result.temporal.mapping
                    ] == mapping_rows
                    expected_baseline = list(expected_mapping.values())
                    current_total, current_count, _ = oracle(
                        list(expected_mapping), ["1", "2", "3"]
                    )
                    assert Decimal(result.totals.net_revenue or "NaN") == current_total
                    assert Decimal(result.totals.receipt_count or "NaN") == current_count
                    with localcontext() as ctx:
                        ctx.prec = 38
                        assert Decimal(
                            result.totals.average_receipt or "NaN"
                        ) == current_total / Decimal(current_count)
                    assert result.temporal.baseline_dates == expected_baseline
                    base_total, base_count, _ = oracle(expected_baseline, ["1", "2", "3"])
                    assert Decimal(result.temporal.totals.net_revenue or "NaN") == base_total
                    assert Decimal(result.temporal.totals.receipt_count or "NaN") == base_count
                    current_buckets = {b.bucket_id: b for b in result.buckets}
                    for bucket in result.temporal.buckets:
                        cb = current_buckets[bucket.bucket_id]
                        independent_dates = [
                            prior
                            for current_day, prior in mapping_rows
                            if cb.effective_start <= current_day < cb.effective_end_exclusive
                        ]
                        assert bucket.baseline_dates == independent_dates
                        net, count, _ = oracle(independent_dates, ["1", "2", "3"])
                        assert Decimal(bucket.values.net_revenue or "NaN") == net
                        assert Decimal(bucket.values.receipt_count or "NaN") == count
                    assert result.temporal.changes["net_revenue"].absolute_delta is not None
        # Ratio counterexample: unequal daily counts must not be averaged.
        ratio = run(request("2025-01-01", "2025-01-03", "month"))
        assert (
            Decimal(ratio.totals.average_receipt or "NaN")
            != sum(Decimal(d.values.average_receipt or "NaN") for d in ratio.daily) / 3
        )
        positive = run(request())
        assert (
            positive.temporal
            and positive.temporal.totals.net_revenue
            and positive.totals.net_revenue
        )
        assert positive.temporal.changes["net_revenue"].relative_delta_percent is not None
        assert positive.temporal.excluded_baseline_dates == [date(2024, 2, 29)]
        baseline_net, _, _ = oracle(positive.temporal.baseline_dates, ["1", "2", "3"])
        assert Decimal(positive.temporal.totals.net_revenue) == baseline_net

    fiscal = run(request("2023-04-01", "2024-03-31", "year", version=versions[3], alignment="none"))
    assert (
        len(fiscal.buckets) == 1
        and fiscal.buckets[0].fiscal_year == 2024
        and not fiscal.buckets[0].clipped
    )
    assert fiscal.coverage.expected_days == fiscal.coverage.declared_complete_days == 366
    assert fiscal.coverage.state == "complete"
    leap = run(request("2024-02-28", "2024-03-01"))
    assert leap.temporal and leap.temporal.mapping[1].baseline_date is None
    assert "LEAP_DAY_SAME_DATE_UNAVAILABLE" in leap.temporal.changes["net_revenue"].reason_codes
    assert leap.temporal.buckets[0].changes["net_revenue"].absolute_delta is not None
    assert leap.temporal.buckets[1].changes["net_revenue"].absolute_delta is None
    missing = run(request("2025-06-02", "2025-06-02", stores=["2"]))
    assert (
        missing.temporal
        and missing.temporal.coverage.state == "complete"
        and missing.temporal.totals.net_revenue is None
    )
    assert "BASELINE_UNAVAILABLE" in missing.temporal.changes["net_revenue"].reason_codes
    zero = run(request("2025-06-03", "2025-06-03", stores=["3"]))
    assert (
        zero.temporal
        and zero.temporal.totals.net_revenue == "0"
        and zero.temporal.changes["net_revenue"].absolute_delta is not None
    )
    assert zero.temporal.changes["net_revenue"].relative_delta_percent is None
    assert "ZERO_BASELINE" in zero.temporal.changes["net_revenue"].reason_codes
    partial = run(request("2024-01-01", "2024-01-03"))
    assert (
        partial.temporal
        and partial.temporal.coverage.calendar_days == 2
        and partial.temporal.coverage.declared_complete_days == 1
    )
    assert "COVERAGE_INCOMPLETE" in partial.temporal.changes["net_revenue"].reason_codes
    partial_current = run(request("2023-01-01", "2023-01-03", alignment="none"))
    assert (
        partial_current.coverage.state == "partial"
        and partial_current.totals.net_revenue is not None
    )
    assert (
        partial_current.coverage.expected_days == 3
        and partial_current.coverage.calendar_days == 2
        and partial_current.coverage.declared_complete_days == 1
    )
    empty = run(request(stores=["1"], local=["2"]))
    assert empty.totals.net_revenue is None and "EMPTY_EFFECTIVE_SCOPE" in empty.trust.reason_codes
    assert run(request(stores=[])).totals.receipt_count is None
    inherited = run(request(stores=["1", "2"], local=["2", "3"]))
    assert inherited == run(request(stores=["2"]))
    with pytest.raises(AnalyticsFailure, match="STORE_NOT_AVAILABLE"):
        run(request(stores=["unknown"]))
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        run(request(stores=["4"]))

    def concurrent_run(_: int):
        return run(request("2025-05-01", "2025-05-31", "week"))

    with ThreadPoolExecutor(max_workers=4) as pool:
        concurrent = list(pool.map(concurrent_run, range(4)))
    assert all(r == concurrent[0] for r in concurrent)
    cards = [
        WorkspaceCardRequest(
            card_id=uuid4(),
            configuration_hash=digest({"copy": i}),
            metric_ref=refs[0],
            query=request(stores=None if i == 0 else ["1", "2", "3"]),
        )
        for i in range(2)
    ]
    applied = service.apply(**actor, cards=cards)
    assert len(applied.results) == 1 and len({b.card_id for b in applied.bindings}) == 2
    pair = service.compare(
        **actor, dataset_id=dataset, left=applied.bindings[0], right=applied.bindings[1]
    )
    assert pair.totals.absolute_delta == "0"
    temporal = service.compare(**actor, dataset_id=dataset, left=applied.bindings[0])
    assert applied.results[0].temporal is not None
    assert temporal.totals == applied.results[0].temporal.changes["net_revenue"]
    count_card = WorkspaceCardRequest(
        card_id=uuid4(),
        configuration_hash=digest({"count": 1}),
        metric_ref=refs[1],
        query=request(),
    )
    count_binding = service.apply(**actor, cards=[count_card]).bindings[0]
    mixed = service.compare(
        **actor, dataset_id=dataset, left=applied.bindings[0], right=count_binding
    )
    assert (
        mixed.comparability_status == "descriptive"
        and mixed.totals.absolute_delta is None
        and "UNIT_MISMATCH" in mixed.totals.reason_codes
    )
    # model_copy bypasses DTO validation, proving the application boundary also rejects forged unit/format.
    with pytest.raises(AnalyticsFailure, match="RESULT_BINDING_MISMATCH"):
        service.compare(
            **actor,
            dataset_id=dataset,
            left=applied.bindings[0],
            right=count_binding.model_copy(update={"unit": "EUR"}),
        )
    with pytest.raises(AnalyticsFailure, match="RESULT_BINDING_MISMATCH"):
        service.compare(
            **actor,
            dataset_id=dataset,
            left=applied.bindings[0].model_copy(update={"format": count_binding.format}),
            right=count_binding,
        )
    other_card = cards[1].model_copy(update={"query": request(version=versions[5])})
    other = service.apply(**actor, cards=[other_card]).bindings[0]
    mismatch = service.compare(**actor, dataset_id=dataset, left=applied.bindings[0], right=other)
    assert (
        mismatch.comparability_status == "unavailable"
        and not mismatch.buckets
        and "CALENDAR_MISMATCH" in mismatch.totals.reason_codes
    )
    # All admitted unit pairs remain descriptive, while period/grain mismatch blocks a shared chart.
    for first, second in ((0, 2), (1, 2)):
        pair_cards = [
            WorkspaceCardRequest(
                card_id=uuid4(),
                configuration_hash=digest({"metric": idx}),
                metric_ref=refs[idx],
                query=request(),
            )
            for idx in (first, second)
        ]
        bs = service.apply(**actor, cards=pair_cards).bindings
        comparison = service.compare(**actor, dataset_id=dataset, left=bs[0], right=bs[1])
        assert (
            comparison.comparability_status == "descriptive"
            and comparison.totals.absolute_delta is None
        )
    for changed, reason in (
        (request("2025-02-01", "2025-02-28"), "PERIOD_MISMATCH"),
        (request(grain="month"), "GRAIN_MISMATCH"),
    ):
        changed_card = cards[1].model_copy(update={"query": changed})
        binding = service.apply(**actor, cards=[changed_card]).bindings[0]
        comparison = service.compare(
            **actor, dataset_id=dataset, left=applied.bindings[0], right=binding
        )
        assert comparison.comparability_status == "unavailable" and not comparison.buckets
        assert reason in comparison.totals.reason_codes
    with runtime.connect() as c:
        row = c.execute(
            "SELECT count(*),min(contract_version) FROM analytics_sales_reports WHERE id=%s",
            (concurrent[0].result_id,),
        ).fetchone()
        assert row == (1, "metric-workspace/v2")
        assert c.execute(
            "SELECT count(*) FROM artifact_dependencies WHERE child_artifact_id=%s",
            (concurrent[0].result_id,),
        ).fetchone() == (6,)
    # Exercise the actual HTTP adapters only in an explicitly composed test app.
    # This does not claim production authentication/CSRF/object authorization (S03).
    app = FastAPI()

    def trusted_actor():
        return access.value

    app.include_router(workspace_router(service, read_actor=trusted_actor, run_actor=trusted_actor))
    with TestClient(app) as client:
        response = client.post("/workspace/v2/results", json=request().model_dump(mode="json"))
        assert response.status_code == 200 and response.json()["result_id"] == str(
            positive.result_id
        )
        assert (
            client.get(f"/workspace/v2/datasets/{dataset}/results/{positive.result_id}").json()
            == response.json()
        )
        assert len(client.get(f"/workspace/v2/datasets/{dataset}/catalog").json()["metrics"]) == 3
        assert len(client.get(f"/workspace/v2/datasets/{dataset}/context").json()["stores"]) == 3
        assert (
            client.post(
                "/workspace/v2/results",
                json={**request().model_dump(mode="json"), "policy_hash": "f" * 64},
            ).status_code
            == 422
        )
    receipt = next(m for m in prepared.artifact_manifests if m.entity == "Receipt")
    input_path = tmp_path / receipt.relative_uri
    saved = input_path.read_bytes()
    input_path.write_bytes(b"invalid")
    try:
        with pytest.raises(AnalyticsFailure, match="ARTIFACT_INTEGRITY_FAILED"):
            run(request())
    finally:
        input_path.write_bytes(saved)
    # Same actor/policy identity reuse, changed policy gets a new result, revoked access rejects exact reads.
    old = run(request())
    access.value = access.value.model_copy(update={"policy_hash": digest({"policy_version": 2})})
    assert run(request()).result_id != old.result_id
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        service.get(**actor, dataset_id=dataset, result_id=old.result_id)
    access.denied = True
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        run(request())
    access.denied = False
    current_result = run(request())
    path = tmp_path / "objects" / (str(current_result.result_id) + ".json")
    raw = path.read_bytes()
    path.write_bytes(b"corrupt")
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_INTEGRITY_FAILED"):
        run(request())
    path.write_bytes(raw)
    path.unlink()
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_UNAVAILABLE"):
        service.get(**actor, dataset_id=dataset, result_id=current_result.result_id)
    path.write_bytes(raw)
    # Corpus identity and actual measurements, never raw rows or credentials.
    assert calendar_counts
    evidence: dict[str, Any] = {
        "corpus": "ms004-retail/v1",
        "source_min_date": str(actual_counts[0]),
        "source_max_date": str(actual_counts[1]),
        "eligible_receipts": actual_counts[2],
        "store_coverage": [
            {
                "store_id": r[0],
                "eligible_receipts": r[1],
                "observed_days": r[2],
                "min_date": str(r[3]),
                "max_date": str(r[4]),
            }
            for r in store_coverage
        ],
        "observed_days": actual_counts[3],
        "observed_stores": actual_counts[4],
        "calendar_days": calendar_counts[0],
        "declared_complete_days": calendar_counts[1],
        "oracle_bucket_checks": oracle_checks,
        "semantic_dataset_version_id": str(dataset),
        "publication_hash": source["publication_hash"],
        "bindings": source["bindings"],
        "admitted_counts": {m.entity: m.row_count for m in prepared.artifact_manifests},
        "result_id": str(current_result.result_id),
        "result_manifest": current_result.manifest.model_dump(mode="json"),
    }
    destination = os.environ.get("MS004_S02_EVIDENCE_PATH")
    if destination:
        Path(destination).write_text(json.dumps(evidence, indent=2) + "\n")


def test_v2_routes_require_current_authentication() -> None:
    # S03 activates the actual app route (the reverse proxy adds /api externally).
    with TestClient(create_app()) as client:
        path = "/analytics/metric-workspace/v2"
        assert client.post(path + "/results", json={}).status_code == 401
        for suffix in ("context", "catalog"):
            assert (
                client.get(
                    path + "/datasets/00000000-0000-0000-0000-000000000001/" + suffix
                ).status_code
                == 401
            )
