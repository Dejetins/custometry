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
    WorkspaceEditorResponse,
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
    "workspace-editor-v2": WorkspaceEditorResponse,
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
    from custometry_api.reports.router import create_reports_app
    from custometry_api.analytics.router import create_analytics_app

    reports = create_reports_app(Settings()).openapi()
    analytics = create_analytics_app(Settings()).openapi()
    paths: dict[str, Any] = {}
    for prefix, document, selector in (
        ("/api/reports", reports, "/v2/"),
        ("/api/analytics", analytics, "/metric-workspace/v2/"),
    ):
        schemas.update(document["components"]["schemas"])
        paths.update(
            {prefix + p: v for p, v in document["paths"].items() if p.startswith(selector)}
        )
    api = {
        "openapi": "3.1.0",
        "info": {"title": "Custometry Workspace API", "version": "2.0.0"},
        "paths": paths,
        "components": {"schemas": schemas},
    }
    result["packages/contracts/openapi/reports.openapi.json"] = _json(reports)
    result["packages/contracts/openapi/analytics.openapi.json"] = _json(analytics)
    result["packages/contracts/openapi/workspace.openapi.json"] = _json(api)
    result["packages/contracts/src/workspace-contracts.ts"] = (
        _types(api).rstrip("\n") + "\n"
    ).encode()
    result["packages/contracts/src/workspace-client.ts"] = (
        _types(api)
        + """
export class WorkspaceRequestError extends Error {
  public constructor(public readonly code: string, public readonly status: number, public readonly retryable: boolean) { super(code); this.name = "WorkspaceRequestError"; }
}
export class WorkspaceReportClient {
  public constructor(private readonly baseUrl: string, private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis)) {}
  private async request<T>(path: string, body?: unknown, csrf?: string): Promise<T> {
    const response = await this.fetcher(`${this.baseUrl}/v2${path}`, {
      method: body === undefined ? "GET" : "POST", credentials: "same-origin", cache: "no-store",
      headers: body === undefined ? {} : {"Content-Type":"application/json","X-CSRF-Token":csrf ?? ""},
      ...(body === undefined ? {} : {body:JSON.stringify(body)}),
    });
    if (!response.ok) { const failure = await response.json() as {code?: string; retryable?: boolean}; throw new WorkspaceRequestError(failure.code ?? `WORKSPACE_HTTP_${response.status}`, response.status, failure.retryable === true); }
    return response.json() as Promise<T>;
  }
  public get(id: string): Promise<WorkspaceEditorResponse> { return this.request(`/${encodeURIComponent(id)}`); }
  public preview(id: string, snapshot: string): Promise<WorkspaceEditorResponse> { return this.request(`/${encodeURIComponent(id)}/snapshots/${encodeURIComponent(snapshot)}`); }
  public apply(id: string, body: WorkspaceApplyRequest, csrf: string): Promise<WorkspaceApplyResponse> { return this.request(`/${encodeURIComponent(id)}/apply`,body,csrf); }
  public save(id: string, body: WorkspaceSaveRequest, csrf: string): Promise<WorkspaceReportResponse> { return this.request(`/${encodeURIComponent(id)}/versions`,body,csrf); }
  public views(id: string): Promise<SavedViewV1[]> { return this.request(`/${encodeURIComponent(id)}/saved-views`); }
  public saveView(id: string, body: SaveViewRequest, csrf: string, view?: string): Promise<SavedViewV1> { return this.request(`/${encodeURIComponent(id)}/saved-views${view ? `/${encodeURIComponent(view)}/versions` : ""}`,body,csrf); }
}
"""
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
