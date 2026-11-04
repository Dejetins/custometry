import json
from pathlib import Path
from custometry_api.config import Settings
from custometry_api.reports.router import create_reports_app
from packages.contracts.presentation import (
    SaveRequest,
    LineChartSpecV1,
    SystemBrandProfileV1,
    SystemCompanyPackV1,
    AnalyticalDocumentCompositionV1,
)
from packages.contracts.generate_reports_client import render

ROOT = Path(__file__).resolve().parents[3]


def test_versioned_provider_schema_and_client_drift() -> None:
    api = create_reports_app(Settings()).openapi()
    assert api == json.loads((ROOT / "packages/contracts/openapi/reports.openapi.json").read_text())
    for filename, model in [
        ("draft-report-save", SaveRequest),
        ("line-chart-spec", LineChartSpecV1),
        ("system-brand-profile", SystemBrandProfileV1),
        ("system-company-pack", SystemCompanyPackV1),
        ("analytical-document-composition", AnalyticalDocumentCompositionV1),
    ]:
        assert model.model_json_schema() == json.loads(
            (ROOT / f"packages/contracts/schemas/{filename}.schema.json").read_text()
        )
    assert (ROOT / "packages/contracts/src/reports-client.ts").read_bytes() == render(ROOT)
    assert set(api["paths"]) == {
        '/',
        '/composer/v1/apply',
        '/composer/v1/compare',
        '/composer/v1/filters/customer-events/v1/preview',
        '/composer/v1/filters/customer-events/v1/{dataset_id}/catalog',
        '/composer/v1/filters/facets',
        '/composer/v1/filters/preview',
        '/composer/v1/filters/v2/facets',
        '/composer/v1/filters/v2/preview',
        '/composer/v1/filters/v2/{dataset_id}/catalog',
        '/composer/v1/filters/v3/facets',
        '/composer/v1/filters/v3/preview',
        '/composer/v1/filters/v3/{dataset_id}/catalog',
        '/composer/v1/filters/v4/facets',
        '/composer/v1/filters/v4/preview',
        '/composer/v1/filters/v4/{dataset_id}/catalog',
        '/composer/v1/filters/{dataset_id}/catalog',
        '/composer/v1/preflight',
        '/composer/v1/prepare',
        '/composer/v1/validate',
        '/composer/v1/versions',
        '/composer/v1/{report_id}',
        '/composer/v1/{report_id}/snapshots/{snapshot_id}',
        '/composer/v1/{report_id}/snapshots/{snapshot_id}/blocks/{block_id}/preflight',
        '/composer/v1/{report_id}/snapshots/{snapshot_id}/blocks/{block_id}/result',
        '/prepare',
        '/v2/new/apply',
        '/v2/new/prepare',
        '/v2/new/versions',
        '/v2/{report_id}',
        '/v2/{report_id}/apply',
        '/v2/{report_id}/saved-views',
        '/v2/{report_id}/saved-views/{saved_view_id}/versions',
        '/v2/{report_id}/snapshots/{snapshot_id}',
        '/v2/{report_id}/versions',
        '/{report_id}',
        '/{report_id}/snapshots/{snapshot_id}',
        '/{report_id}/versions',
    }
    assert api["components"]["schemas"]["SaveRequest"]["additionalProperties"] is False
