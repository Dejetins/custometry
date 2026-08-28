from pathlib import Path

from custometry_api.config import Settings
from custometry_api.main import create_app
from custometry_api.runs.router import create_runs_app
from packages.contracts.execution import EXECUTION_CONTROL_API_VERSION
from packages.contracts.execution.generator import render_consumer, render_openapi


def test_execution_control_openapi_and_consumer_are_generated_without_drift() -> None:
    root = Path(__file__).resolve().parents[3]
    openapi = render_openapi()
    consumer = render_consumer(openapi)

    assert openapi == (root / "packages/contracts/openapi/execution-control.openapi.json").read_bytes()
    assert consumer == (root / "packages/contracts/src/execution-control.ts").read_bytes()

    schema = create_runs_app(Settings(version="0.1.0-dev.0")).openapi()
    assert schema["info"]["version"] == EXECUTION_CONTROL_API_VERSION
    assert set(schema["paths"]) == {
        "/queue-summary",
        "/runs",
        "/runs/{run_id}",
        "/runs/{run_id}/cancel",
        "/runs/{run_id}/retry",
    }
    assert schema["paths"]["/runs"]["get"]["operationId"] == "list_operator_runs"
    assert schema["paths"]["/runs/{run_id}/cancel"]["post"]["operationId"] == (
        "cancel_operator_run"
    )


def test_execution_control_provider_is_independently_versioned_and_mounted() -> None:
    parent = create_app(settings=Settings(version="0.1.0-dev.0"))

    assert "/execution/runs" not in parent.openapi()["paths"]
    assert any(getattr(route, "path", None) == "/execution" for route in parent.routes)


def test_contract_exposes_only_safe_operator_projection_and_stable_headers() -> None:
    schema = create_runs_app(Settings(version="0.1.0-dev.0")).openapi()
    run = schema["components"]["schemas"]["RunResponse"]
    listing = schema["components"]["schemas"]["RunListResponse"]
    cancel = schema["paths"]["/runs/{run_id}/cancel"]["post"]

    assert "visible_count" in listing["required"]
    assert "total_count" not in listing["properties"]
    assert {"safe_title", "safe_trace_id", "retry_of_id", "revision"}.issubset(
        run["required"]
    )
    assert not {"inputs", "artifacts", "logs", "source_values"}.intersection(
        run["properties"]
    )
    header_names = {
        item["name"] for item in cancel["parameters"] if item["in"] == "header"
    }
    assert {"Authorization", "X-Request-ID", "X-Contract-Version", "Idempotency-Key"}.issubset(
        header_names
    )
