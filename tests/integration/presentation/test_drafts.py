from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import date
import json
import os
from pathlib import Path
import subprocess
from typing import Any
from uuid import UUID, uuid4
import pytest
from apps.worker_data.vertical_slice import DataPipelineRunner
from packages.analytics_core.application.service import AnalyticsService
from packages.analytics_core.infrastructure.local import LocalAnalyticsArtifactStore
from packages.analytics_core.infrastructure.postgres import PostgresAnalyticsRepository
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.artifacts.infrastructure.document_snapshots import DocumentSnapshotArtifacts
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sales_report import SalesReportRequest
from packages.contracts.presentation import PresentationFailure, SaveRequest
from packages.presentation.application.reports import ReportService
from packages.presentation.infrastructure.postgres import PostgresReportRepository
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from tests.integration.data_pipeline.conftest import DataPipelineRuntime
from tests.integration.data_pipeline.test_retail_report import request_for

ROOT = Path(__file__).resolve().parents[3]


def scalar(connection: Any, query: str, params: tuple[Any, ...] = ()) -> Any:
    row = connection.execute(query, params).fetchone()
    assert row is not None
    return row[0]


def test_migration_real_versions_conflicts_and_faults(
    data_pipeline_runtime: DataPipelineRuntime, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime = data_pipeline_runtime
    intake = DataPipelineRunner(
        connector=runtime.connector,
        connect=runtime.connect,
        artifact_store=LocalArtifactStore(tmp_path),
    ).run(request_for(runtime))
    assert intake.semantic_dataset_version_id is not None
    repository = PostgresAnalyticsRepository(runtime.connect)
    local = LocalAnalyticsArtifactStore(tmp_path)
    analytics = AnalyticsService(
        projections=repository,
        artifacts=local,
        results=repository,
        result_store=local,
        sales_semantics=PostgresSalesSemanticRepository(runtime.connect),
        sales_results=repository,
        sales_artifacts=SalesArtifactStore(runtime.connect, tmp_path),
    )
    actor: dict[str, Any] = {
        "workspace_id": runtime.workspace_id,
        "principal_id": runtime.actor_id,
        "permissions": frozenset({"analysis.read", "analysis.run", "report.read", "report.manage"}),
    }
    result = analytics.run_sales_report(
        **actor,
        request=SalesReportRequest(
            intake.semantic_dataset_version_id, comparison="previous_year_same_dates"
        ),
    )
    # The harness starts this freshly owned database at the actual previous head.
    with runtime.connect() as c:
        assert scalar(c, "SELECT version_num FROM alembic_version") == "0011_presentation_drafts"
        before = scalar(c, "SELECT count(*) FROM artifact_manifests")
    command = [
        "uv",
        "run",
        "--locked",
        "--package",
        "custometry-api",
        "alembic",
        "-c",
        "migrations/alembic.ini",
        "upgrade",
        "head",
    ]
    for _ in range(2):
        completed = subprocess.run(command, env=os.environ.copy(), capture_output=True, text=True)
        assert completed.returncode == 0, "owned migration failed"
    with runtime.connect() as c:
        assert scalar(c, "SELECT count(*) FROM artifact_manifests") == before
    assert analytics.get_sales_report(**actor, result_id=UUID(result["result_id"])) == result
    brand = json.loads(
        (ROOT / "packages/presentation/infrastructure/system-brand.v1.json").read_text()
    )
    artifacts = DocumentSnapshotArtifacts(runtime.connect, tmp_path)
    reports = ReportService(PostgresReportRepository(runtime.connect), analytics, artifacts, brand)
    refs = reports.prepare(**actor, result_id=UUID(result["result_id"]))
    request = SaveRequest(
        contract_version="draft-report/v1",
        result_id=result["result_id"],
        title="First report",
        expected_revision=0,
        idempotency_key=uuid4(),
        **{
            name: refs[name]["reference"]
            for name in ("chart_spec", "brand_profile", "company_pack")
        },
    )
    for name in ("chart_spec", "brand_profile", "company_pack"):
        invalid = request.model_copy(
            update={name: request.chart_spec.model_copy(update={"id": uuid4()})}
        )
        with pytest.raises(PresentationFailure, match="INVALID_REFERENCE"):
            reports.save(**actor, request=invalid)
    # Known records with incompatible canonical bindings are also rejected.
    from packages.presentation.domain.reports import versioned

    altered = deepcopy(refs["chart_spec"]["payload"])
    altered["interaction"]["formatter"] = "<script>unsafe</script>"
    rogue_chart = PostgresReportRepository(runtime.connect).put_reference(
        runtime.workspace_id, runtime.actor_id, versioned("chart_spec", altered)
    )
    incompatible = SaveRequest.model_validate(
        {**request.model_dump(mode="json"), "chart_spec": rogue_chart["reference"]}
    )
    with pytest.raises(PresentationFailure, match="INVALID_CHART_BINDING"):
        reports.save(**actor, request=incompatible)
    other_brand = PostgresReportRepository(runtime.connect).put_reference(
        runtime.workspace_id,
        runtime.actor_id,
        versioned("brand_profile", {**brand, "name": "Other version"}),
    )
    incompatible = SaveRequest.model_validate(
        {**request.model_dump(mode="json"), "brand_profile": other_brand["reference"]}
    )
    with pytest.raises(PresentationFailure, match="INVALID_DEFAULT_BINDING"):
        reports.save(**actor, request=incompatible)

    def duplicate(_: int) -> dict[str, Any]:
        return reports.save(**actor, request=request)

    with ThreadPoolExecutor(max_workers=4) as pool:
        duplicates = list(pool.map(duplicate, range(4)))
    saved = duplicates[0]
    assert all(x == saved for x in duplicates)
    report_id = UUID(saved["report_id"])
    assert saved["result"] == result
    assert saved["references"] == refs
    assert saved["result"]["trust"]["quality_accounting"]["quarantined_count"] == 5
    assert len(saved["snapshot"]["resolved_document_context"]["lineage"]["bindings"]) == 6
    with pytest.raises(PresentationFailure, match="IDEMPOTENCY_CONFLICT"):
        reports.save(**actor, request=request.model_copy(update={"title": "Different"}))
    second_result = analytics.run_sales_report(
        **actor,
        request=SalesReportRequest(
            intake.semantic_dataset_version_id, date(2025, 6, 1), date(2025, 6, 30)
        ),
    )
    second_refs = reports.prepare(**actor, result_id=UUID(second_result["result_id"]))
    edit = SaveRequest.model_validate(
        {
            **request.model_dump(mode="json"),
            "expected_revision": 1,
            "result_id": second_result["result_id"],
            "idempotency_key": str(uuid4()),
            "title": "Edited",
            **{
                name: second_refs[name]["reference"]
                for name in ("chart_spec", "brand_profile", "company_pack")
            },
        }
    )

    def edit_once(_: int) -> dict[str, Any] | str:
        try:
            return reports.save(
                **actor,
                report_id=report_id,
                request=edit.model_copy(update={"idempotency_key": uuid4()}),
            )
        except PresentationFailure as exc:
            return exc.code

    with ThreadPoolExecutor(max_workers=2) as pool:
        contenders = list(pool.map(edit_once, range(2)))
    assert sum(x == "REVISION_CONFLICT" for x in contenders) == 1
    latest = reports.get(**actor, report_id=report_id)
    assert latest["revision"] == 2
    assert latest["result"] == second_result
    assert [b["block_id"] for b in latest["composition"]["blocks"]] == [
        b["block_id"] for b in saved["composition"]["blocks"]
    ]

    # Real DB transaction dies after inserting a version but before switching latest.
    def crash() -> None:
        raise RuntimeError("CRASH_BEFORE_SWITCH")

    crashing = ReportService(
        PostgresReportRepository(runtime.connect, checkpoint=crash), analytics, artifacts, brand
    )
    update = edit.model_copy(update={"expected_revision": 2, "idempotency_key": uuid4()})
    with pytest.raises(RuntimeError, match="CRASH_BEFORE_SWITCH"):
        crashing.save(**actor, report_id=report_id, request=update)
    assert reports.get(**actor, report_id=report_id) == latest
    with runtime.connect() as c:
        assert (
            scalar(
                c, "SELECT count(*) FROM presentation_versions WHERE document_id=%s", (report_id,)
            )
            == 2
        )

    # A fresh service can reopen both versions with computation and source files disabled.
    def forbidden_compute(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("COMPUTE_OR_SOURCE_ACCESS")

    monkeypatch.setattr(analytics, "run_sales_report", forbidden_compute)
    monkeypatch.setattr(PostgresSalesSemanticRepository, "sales_projection", forbidden_compute)
    restarted = ReportService(
        PostgresReportRepository(runtime.connect),
        analytics,
        DocumentSnapshotArtifacts(runtime.connect, tmp_path),
        {},
    )
    for manifest in intake.artifact_manifests:
        (tmp_path / manifest.relative_uri).unlink()
    assert restarted.get(**actor, report_id=report_id) == latest
    assert (
        restarted.get(**actor, report_id=report_id, snapshot_id=UUID(saved["snapshot_id"])) == saved
    )
    assert restarted.list(**actor, offset=0, limit=1)["visible_count"] == 1
    outsider: dict[str, Any] = {**actor, "principal_id": uuid4()}
    assert restarted.list(**outsider, offset=0, limit=10) == {"reports": [], "visible_count": 0}
    with pytest.raises(PresentationFailure, match="NOT_FOUND"):
        restarted.get(**outsider, report_id=report_id)
    foreign: dict[str, Any] = {**actor, "workspace_id": uuid4()}
    with pytest.raises(PresentationFailure, match="NOT_FOUND"):
        restarted.get(**foreign, report_id=report_id)
    denied = {**actor, "permissions": actor["permissions"] - {"report.manage"}}
    with pytest.raises(PresentationFailure, match="FORBIDDEN"):
        restarted.save(**denied, report_id=report_id, request=update)
    policy_changed = {**actor, "permissions": actor["permissions"] | {"new.permission"}}
    assert restarted.list(**policy_changed, offset=0, limit=10)["visible_count"] == 0
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        restarted.get(**policy_changed, report_id=report_id)
    # Corrupt and absent root/page/result bytes are distinct failures, never fallback.
    for artifact_id in (
        latest["manifest"]["artifact_id"],
        latest["page_snapshot"]["analytical_page_snapshot_id"],
        second_result["manifest"]["artifact_id"],
    ):
        path = tmp_path / "objects" / f"{artifact_id}.json"
        raw = path.read_bytes()
        path.write_bytes(b"corrupt")
        with pytest.raises((PresentationFailure, AnalyticsFailure)):
            restarted.get(**actor, report_id=report_id)
        path.unlink()
        with pytest.raises((PresentationFailure, AnalyticsFailure)):
            restarted.get(**actor, report_id=report_id)
        path.write_bytes(raw)
    # Genuine filesystem staging obstruction prevents save while latest remains intact.
    staging = tmp_path / ".staging"
    staging.rmdir()
    staging.write_text("unavailable")
    try:
        with pytest.raises(PresentationFailure, match="STORAGE_UNAVAILABLE"):
            restarted.save(**actor, report_id=report_id, request=update)
    finally:
        staging.unlink()
        staging.mkdir()
    assert restarted.get(**actor, report_id=report_id) == latest
    # Metadata alteration is detected against the immutable root manifest.
    corrupt = deepcopy(latest)
    corrupt["title"] = "tampered"
    with runtime.connect() as c:
        from psycopg.types.json import Jsonb

        c.execute(
            "UPDATE presentation_versions SET payload=%s WHERE id=%s",
            (Jsonb(corrupt), latest["version_id"]),
        )
    with pytest.raises(PresentationFailure, match="ARTIFACT_CORRUPT"):
        restarted.get(**actor, report_id=report_id)
    with runtime.connect() as c:
        c.execute(
            "UPDATE presentation_versions SET payload=%s WHERE id=%s",
            (Jsonb(latest), latest["version_id"]),
        )
    downgrade = subprocess.run(
        command[:-2] + ["downgrade", "0010_sales_report"], capture_output=True, text=True
    )
    assert downgrade.returncode != 0
    assert restarted.get(**actor, report_id=report_id) == latest
    # Clean only records in this disposable fixture's own workspace for its teardown.
    with runtime.connect() as c:
        c.execute(
            "UPDATE presentation_documents SET latest_version_id=NULL WHERE workspace_id=%s",
            (runtime.workspace_id,),
        )
        c.execute(
            "DELETE FROM presentation_versions WHERE document_id IN (SELECT id FROM presentation_documents WHERE workspace_id=%s)",
            (runtime.workspace_id,),
        )
        c.execute(
            "DELETE FROM presentation_documents WHERE workspace_id=%s", (runtime.workspace_id,)
        )
        c.execute(
            "DELETE FROM presentation_references WHERE workspace_id=%s", (runtime.workspace_id,)
        )
