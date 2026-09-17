from pathlib import Path
from unittest.mock import Mock
from uuid import uuid4
import pytest
from packages.analytics_core.application.service import AnalyticsService
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.generate_sales_report_client import render
from custometry_api.analytics.sales_models import SalesContext


def service():
    semantic, artifacts = Mock(), Mock()
    app = AnalyticsService(
        projections=Mock(),
        artifacts=Mock(),
        results=Mock(),
        result_store=Mock(),
        sales_semantics=semantic,
        sales_artifacts=artifacts,
    )
    return app, semantic, artifacts


def test_context_authorizes_before_discovery_and_never_computes():
    app, semantic, artifacts = service()
    actor = dict(workspace_id=uuid4(), principal_id=uuid4())
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        app.sales_report_context(**actor, permissions=frozenset({"analysis.read"}))
    semantic.sales_versions.assert_not_called()
    artifacts.read_sales_inputs.assert_not_called()
    semantic.sales_versions.return_value = []
    reply = app.sales_report_context(
        **actor, permissions=frozenset({"analysis.read", "analysis.run"})
    )
    assert reply["datasets"] == []
    semantic.sales_versions.assert_called_once_with(workspace_id=actor["workspace_id"])
    artifacts.commit_sales.assert_not_called()
    SalesContext.model_validate(reply)


def test_context_pins_published_store_artifact_and_propagates_failure():
    app, semantic, artifacts = service()
    actor = dict(
        workspace_id=uuid4(),
        principal_id=uuid4(),
        permissions=frozenset({"analysis.read", "analysis.run"}),
    )
    version = uuid4()
    binding = {"entity": "Store", "artifact_id": str(uuid4()), "content_hash": "a" * 64}
    semantic.sales_versions.return_value = [{"id": str(version), "version": 2}]
    semantic.sales_projection.return_value = {"bindings": [binding, {"entity": "Receipt"}]}
    artifacts.read_sales_inputs.return_value = {
        "Store": ({"store_id": "7", "store_name": "Store Seven"},)
    }
    result = app.sales_report_context(**actor)
    assert result["datasets"][0]["stores"] == [{"id": "7", "label": "Store Seven"}]
    semantic.sales_projection.assert_called_once_with(
        workspace_id=actor["workspace_id"], version_id=version
    )
    artifacts.read_sales_inputs.assert_called_once_with(
        workspace_id=actor["workspace_id"], bindings=[binding], supporting_artifacts=[]
    )
    artifacts.read_sales_inputs.side_effect = AnalyticsFailure("ARTIFACT_UNAVAILABLE")
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_UNAVAILABLE"):
        app.sales_report_context(**actor)


def test_generated_sales_context_types_match_provider():
    root = Path(__file__).resolve().parents[3]
    assert (root / "packages/contracts/src/sales-report-client.ts").read_bytes() == render()
