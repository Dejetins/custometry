from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from typing import cast
from uuid import uuid4

from fastapi.testclient import TestClient

from apps.worker_data import DataPipelineRunner
from custometry_api.analytics.router import create_analytics_app
from custometry_api.config import Settings
from packages.analytics_core.application.service import AnalyticsService
from packages.analytics_core.infrastructure.local import LocalAnalyticsArtifactStore
from packages.analytics_core.infrastructure.postgres import PostgresAnalyticsRepository
from packages.artifacts import LocalArtifactStore
from packages.data_quality.domain.model import QualityWaiver
from packages.data_quality.infrastructure.postgres import PostgresQualityRepository
from packages.identity_access.domain.policy import Actor
from packages.ingestion.domain.model import ExtractionBatchRequest
from tests.integration.data_pipeline.conftest import DataPipelineRuntime


class TokenIdentity:
    def __init__(self, *, owner: Actor, hidden: Actor) -> None:
        self._actors = {"owner-token": owner, "hidden-token": hidden}

    def authenticate(self, token: str) -> Actor:
        return self._actors[token]


def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _request(semantic_version_id: str, result_type: str) -> dict[str, object]:
    return {
        "result_type": result_type,
        "semantic_dataset_version_id": semantic_version_id,
        "comparison": {
            "mode": "previous_year_calendar_aligned",
            "current_period": {"starts_on": "2025-01-01", "ends_on": "2025-12-31"},
            "comparison_period": {"starts_on": "2024-01-01", "ends_on": "2024-12-31"},
            "timezone": "UTC",
            "calendar_version_id": str(uuid4()),
            "incomplete_period_policy": "explicit_partial",
            "leap_day_policy": "calendar_map",
            "iso_week_53_policy": "explicit_partial",
            "definition_compatibility_policy": "require_same_versions",
        },
        "filters": [],
        "rfm_score_bins": 5,
        "rfm_frequency_measure": "receipt_count",
        "rfm_segment_rule_set_version": "rfm-retail-v1",
    }


def _metric(payload: dict[str, object], metric_id: str) -> dict[str, object]:
    groups = cast(list[dict[str, object]], payload["metric_groups"])
    for group in groups:
        metrics = cast(list[dict[str, object]], group["metrics"])
        for metric in metrics:
            if metric["metric_id"] == metric_id:
                return metric
    raise AssertionError(metric_id)


def test_real_postgresql_filesystem_and_authenticated_projection_boundary(
    tmp_path: Path, data_pipeline_runtime: DataPipelineRuntime
) -> None:
    waiver = QualityWaiver(
        waiver_id=uuid4(),
        workspace_id=data_pipeline_runtime.workspace_id,
        rule_id="receipt_item.product.reference",
        status="active",
        expires_at=datetime.now(UTC) + timedelta(hours=1),
        approved_by=data_pipeline_runtime.actor_id,
        reason_code="DEMO_FIXTURE_KNOWN_MISSING_PRODUCT",
    )
    PostgresQualityRepository(data_pipeline_runtime.connect).save_waiver(waiver)
    source_system_id = uuid4()
    batch = ExtractionBatchRequest(
        batch_id=uuid4(),
        workspace_id=data_pipeline_runtime.workspace_id,
        connection_id=data_pipeline_runtime.create_connection(source_system_id),
        source_system_id=source_system_id,
        semantic_dataset_id=uuid4(),
        idempotency_key=f"w16-source-{uuid4()}",
    )
    artifact_root = (tmp_path / "artifacts").resolve()
    publication = DataPipelineRunner(
        connector=data_pipeline_runtime.connector,
        connect=data_pipeline_runtime.connect,
        artifact_store=LocalArtifactStore(artifact_root),
    ).run(batch)
    assert publication.semantic_dataset_version_id is not None

    repository = PostgresAnalyticsRepository(data_pipeline_runtime.connect)
    store = LocalAnalyticsArtifactStore(artifact_root)
    analytics = AnalyticsService(
        projections=repository,
        artifacts=store,
        results=repository,
        result_store=store,
    )
    hidden_principal = uuid4()
    identity = TokenIdentity(
        owner=Actor(
            principal_id=data_pipeline_runtime.actor_id,
            workspace_id=data_pipeline_runtime.workspace_id,
            email="owner@example.test",
            permissions=frozenset({"analysis.run", "analysis.read"}),
        ),
        hidden=Actor(
            principal_id=hidden_principal,
            workspace_id=data_pipeline_runtime.workspace_id,
            email="hidden@example.test",
            permissions=frozenset({"analysis.run", "analysis.read"}),
        ),
    )
    app = create_analytics_app(
        Settings(analytics_artifact_root=artifact_root),
        identity_service=identity,  # type: ignore[arg-type]
        analytics_service=analytics,
    )
    with TestClient(app, base_url="http://testserver") as client:
        assert client.get("/results").status_code == 401
        created: dict[str, dict[str, object]] = {}
        requests: dict[str, dict[str, object]] = {}
        for result_type in ("sales", "customer", "rfm"):
            requests[result_type] = _request(
                str(publication.semantic_dataset_version_id), result_type
            )
            response = client.post(
                "/results",
                headers=_headers("owner-token"),
                json=requests[result_type],
            )
            assert response.status_code == 200, response.text
            created[result_type] = cast(dict[str, object], response.json())

        sales = created["sales"]
        revenue = _metric(sales, "net_revenue")
        expected = json.loads(Path("tests/golden/retail-demo-manifest.json").read_text())[
            "expected_kpis"
        ]["receipt_net_amount"]
        assert Decimal(str(revenue["current_value"])) + Decimal(
            str(revenue["comparison_value"])
        ) == Decimal(expected)
        metric_groups = cast(list[dict[str, object]], sales["metric_groups"])
        assert [group["group_order"] for group in metric_groups] == [10, 20]
        assert created["rfm"]["rfm_profiles"]

        exact_second = client.post(
            "/results", headers=_headers("owner-token"), json=requests["sales"]
        )
        assert exact_second.json()["result_id"] == sales["result_id"]
        assert exact_second.json()["manifest"] == sales["manifest"]

        result_id = sales["result_id"]
        owner_get = client.get(f"/results/{result_id}", headers=_headers("owner-token"))
        hidden_get = client.get(f"/results/{result_id}", headers=_headers("hidden-token"))
        hidden_list = client.get("/results", headers=_headers("hidden-token"))
        assert owner_get.status_code == 200
        assert hidden_get.status_code == 404
        assert hidden_list.status_code == 200
        assert hidden_list.json() == {"results": [], "visible_count": 0}

    manifest = cast(dict[str, object], sales["manifest"])
    result_path = artifact_root / str(manifest["relative_uri"])
    assert result_path.is_file()
    assert hashlib.sha256(result_path.read_bytes()).hexdigest() == manifest["content_hash"]
    with data_pipeline_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT count(*), count(DISTINCT request_hash), count(DISTINCT storage_uri) FROM analytics_results WHERE workspace_id = %s",
            (data_pipeline_runtime.workspace_id,),
        )
        row = cursor.fetchone()
        assert row is not None
        total, identities, storage_paths = cast(tuple[int, int, int], row)
        assert total == identities == storage_paths
        assert total == 3
