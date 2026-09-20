"""Generate S01 contracts with the existing Pydantic/OpenAPI/TypeScript pipeline."""

import hashlib
import json
from pathlib import Path
from typing import Any
from pydantic import BaseModel
from tools.custometry_quality.check_contract_drift import render_typescript
from packages.contracts.presentation.workspace import (
    AnalyticalDocumentComposition,
    ChartSpec,
    ConfiguredReportV2,
    SavedViewV1,
    WorkspaceApplyRequest,
    WorkspaceApplyResponse,
    WorkspaceSaveRequest,
    SaveViewRequest,
    VersionedReport,
)
from packages.contracts.analytics.workspace import (
    WorkspaceResultV2,
    CardComparisonV1,
    WorkspaceRunRequest,
    WorkspaceApplyResult,
)

MODELS: dict[str, type[BaseModel]] = {
    "configured-report-v2": ConfiguredReportV2,
    "analytical-document-composition-versions": AnalyticalDocumentComposition,
    "chart-spec-versions": ChartSpec,
    "saved-view-v1": SavedViewV1,
    "workspace-apply-v2": WorkspaceApplyRequest,
    "workspace-apply-response-v2": WorkspaceApplyResponse,
    "workspace-save-v2": WorkspaceSaveRequest,
    "saved-view-save-v1": SaveViewRequest,
    "report-versions": VersionedReport,
    "metric-workspace-v2": WorkspaceResultV2,
    "analytics-workspace-run-v2": WorkspaceRunRequest,
    "analytics-workspace-apply-v2": WorkspaceApplyResult,
    "card-comparison-v1": CardComparisonV1,
}


def _json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def _types(api: dict[str, Any]) -> str:
    return (
        render_typescript(
            {**api, "paths": {}},
            source_digest=hashlib.sha256(_json(api)).hexdigest(),
            schema_ids=[],
        )
        .decode()
        .split("export class FoundationApiClient")[0]
    )


def outputs() -> dict[str, bytes]:
    from custometry_api.config import Settings
    from custometry_api.semantic.router import create_semantic_app

    result: dict[str, bytes] = {}
    schemas: dict[str, Any] = {}
    for name, model in MODELS.items():
        result[f"packages/contracts/schemas/{name}.schema.json"] = _json(model.model_json_schema())
        schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
        schemas.update(schema.pop("$defs", {}))
        schemas[model.__name__] = schema
    # Component catalogue only. Deliberately no advertised/mounted v2 operations.
    api = {
        "openapi": "3.1.0",
        "info": {"title": "Custometry Workspace Contracts (unmounted)", "version": "2.0.0"},
        "paths": {},
        "components": {"schemas": schemas},
    }
    result["packages/contracts/openapi/workspace.openapi.json"] = _json(api)
    result["packages/contracts/src/workspace-contracts.ts"] = (
        _types(api).rstrip("\n") + "\n"
    ).encode()
    calendar = create_semantic_app(Settings()).openapi()
    result["packages/contracts/openapi/workspace-calendar.openapi.json"] = _json(calendar)
    client = (
        _types(calendar)
        + """export class WorkspaceCalendarClient {
  public constructor(private readonly baseUrl: string, private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis)) {}
  private async request<T>(path: string, input?: unknown, csrf?: string): Promise<T> {
    const response = await this.fetcher(`${this.baseUrl}${path}`, {
      method: input === undefined ? "GET" : "POST", credentials: "same-origin", cache: "no-store",
      headers: input === undefined ? {} : {"Content-Type": "application/json", "X-CSRF-Token": csrf ?? ""},
      ...(input === undefined ? {} : {body: JSON.stringify(input)}),
    });
    if (!response.ok) { const error = await response.json() as {code?: string}; throw new Error(error.code ?? `CALENDAR_HTTP_${response.status}`); }
    return response.json() as Promise<T>;
  }
  public get(): Promise<WorkspaceCalendarDefault> { return this.request("/workspace-calendar/v1"); }
  public version(id: string, hash: string): Promise<BusinessCalendarVersion> { return this.request(`/workspace-calendar/v1/versions/${encodeURIComponent(id)}?content_hash=${encodeURIComponent(hash)}`); }
  public update(input: UpdateCalendarRequest, csrf: string): Promise<WorkspaceCalendarDefault> { return this.request("/workspace-calendar/v1/versions", input, csrf); }
}
"""
    )
    result["packages/contracts/src/workspace-calendar-client.ts"] = client.encode()
    return result


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    for path, content in outputs().items():
        (root / path).write_bytes(content)
