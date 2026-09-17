from pathlib import Path
from unittest.mock import Mock
from uuid import UUID, uuid4
import pytest
from apps.worker_data.vertical_slice import DataPipelineRunner
from packages.analytics_core.application.service import AnalyticsService
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from tests.integration.data_pipeline.conftest import DataPipelineRuntime
from tests.integration.data_pipeline.test_retail_report import request_for


def test_real_context_discovery_isolation_and_store_integrity(
    data_pipeline_runtime: DataPipelineRuntime, tmp_path: Path
):
    runtime = data_pipeline_runtime
    intake = DataPipelineRunner(
        connector=runtime.connector,
        connect=runtime.connect,
        artifact_store=LocalArtifactStore(tmp_path),
    ).run(request_for(runtime))
    semantic = PostgresSalesSemanticRepository(runtime.connect)
    service = AnalyticsService(
        projections=Mock(),
        artifacts=Mock(),
        results=Mock(),
        result_store=Mock(),
        sales_semantics=semantic,
        sales_artifacts=SalesArtifactStore(runtime.connect, tmp_path),
    )

    def context_for(
        workspace: UUID = runtime.workspace_id,
        permissions: frozenset[str] = frozenset({"analysis.read", "analysis.run"}),
    ):
        return service.sales_report_context(
            workspace_id=workspace, principal_id=runtime.actor_id, permissions=permissions
        )

    context = context_for()
    assert [d["id"] for d in context["datasets"]] == [str(intake.semantic_dataset_version_id)]
    assert len(context["datasets"][0]["stores"]) == 20
    assert context_for(workspace=uuid4())["datasets"] == []
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        context_for(permissions=frozenset())
    assert intake.semantic_dataset_version_id is not None
    source = semantic.sales_projection(
        workspace_id=runtime.workspace_id, version_id=intake.semantic_dataset_version_id
    )
    store = next(b for b in source["bindings"] if b["entity"] == "Store")
    with runtime.connect() as conn:
        row = conn.execute(
            "SELECT relative_uri FROM artifact_manifests WHERE id=%s", (store["artifact_id"],)
        ).fetchone()
        assert row is not None
        uri = str(row[0])
    path = tmp_path / str(uri)
    original = path.read_bytes()
    try:
        path.write_bytes(b"corrupt-owned-test-store")
        with pytest.raises(AnalyticsFailure, match="ARTIFACT_INTEGRITY_FAILED"):
            context_for()
        path.unlink()
        with pytest.raises(AnalyticsFailure, match="ARTIFACT_UNAVAILABLE"):
            context_for()
    finally:
        path.write_bytes(original)
    assert context_for() == context
