"""Composer contracts use the existing deterministic Pydantic/TypeScript pipeline."""
import hashlib
import json
from typing import Any
from packages.contracts.presentation.composer import (
    ComposerDefinitionV1, ComposerSaveRequest, ComposerApplyRequest, ComposerApplyResponse,
    ComposerReportResponse, ComposerEditorResponse, ComposerPrepareResponse, ComposerPreflightResponse,
)
from tools.custometry_quality.check_contract_drift import render_typescript


def outputs() -> dict[str, bytes]:
    from custometry_api.config import Settings
    from custometry_api.reports.router import create_reports_app

    def encoded(value: object) -> bytes:
        return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()

    api: dict[str, Any] = create_reports_app(Settings()).openapi()
    api = {**api, "info": {"title": "Custometry Composer API", "version": "1.0.0"},
           "paths": {"/api/reports" + p: v for p, v in api["paths"].items() if p.startswith("/composer/v1/")}}
    types = render_typescript({**api, "paths": {}}, source_digest=hashlib.sha256(encoded(api)).hexdigest(),
                              schema_ids=[]).decode().split("export class FoundationApiClient")[0]
    result = {"packages/contracts/openapi/composer.openapi.json": encoded(api)}
    for name, model in {
        "analytical-authoring-v1": ComposerDefinitionV1, "composer-save-v1": ComposerSaveRequest,
        "composer-apply-v1": ComposerApplyRequest, "composer-result-v1": ComposerApplyResponse,
        "composed-report-v1": ComposerReportResponse, "composer-editor-v1": ComposerEditorResponse,
        "composer-prepare-v1": ComposerPrepareResponse, "composer-preflight-v1": ComposerPreflightResponse,
    }.items():
        result[f"packages/contracts/schemas/{name}.schema.json"] = encoded(model.model_json_schema())
    result["packages/contracts/src/composer-client.ts"] = (types + '''
export class ComposerRequestError extends Error {
  constructor(public readonly code: string, public readonly status: number, public readonly retryable: boolean) { super(code); this.name = "ComposerRequestError"; }
}
export class ComposerClient {
  constructor(private readonly baseUrl: string, private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis)) {}
  private async request<T>(path: string, body?: unknown, csrf?: string, signal?: AbortSignal): Promise<T> {
    const response = await this.fetcher(`${this.baseUrl}/composer/v1${path}`, {
      signal, method: body === undefined ? "GET" : "POST", credentials: "same-origin", cache: "no-store",
      headers: body === undefined ? {} : {"Content-Type":"application/json","X-CSRF-Token":csrf ?? ""},
      ...(body === undefined ? {} : {body:JSON.stringify(body)}),
    });
    if (!response.ok) { const failure = await response.json() as {code?: string; retryable?: boolean}; throw new ComposerRequestError(failure.code ?? `COMPOSER_HTTP_${response.status}`,response.status,failure.retryable === true); }
    return response.json() as Promise<T>;
  }
  filterCatalog(dataset: string, search: string, signal?: AbortSignal): Promise<FilterCatalogResponse> { return this.request(`/filters/${encodeURIComponent(dataset)}/catalog?search=${encodeURIComponent(search)}`,undefined,undefined,signal); }
  filterPreview(body: FilterPreviewRequest, csrf: string, signal?: AbortSignal): Promise<FilterPreviewResponse> { return this.request("/filters/preview",body,csrf,signal); }
  filterFacets(body: FilterFacetRequest, csrf: string, signal?: AbortSignal): Promise<FilterFacetResponse> { return this.request("/filters/facets",body,csrf,signal); }
  relationalFilterCatalog(dataset: string, search: string, signal?: AbortSignal): Promise<RelationalCatalogResponse> { return this.request(`/filters/v2/${encodeURIComponent(dataset)}/catalog?search=${encodeURIComponent(search)}`,undefined,undefined,signal); }
  relationalFilterPreview(body: RelationalPreviewRequest, csrf: string, signal?: AbortSignal): Promise<RelationalPreviewResponse> { return this.request("/filters/v2/preview",body,csrf,signal); }
  relationalFilterFacets(body: RelationalFacetRequest, csrf: string, signal?: AbortSignal): Promise<RelationalFacetResponse> { return this.request("/filters/v2/facets",body,csrf,signal); }
  aggregateFilterCatalog(dataset: string, search: string, signal?: AbortSignal): Promise<AggregateCatalogResponse> { return this.request(`/filters/v3/${encodeURIComponent(dataset)}/catalog?search=${encodeURIComponent(search)}`,undefined,undefined,signal); }
  aggregateFilterPreview(body: AggregatePreviewRequest, csrf: string, signal?: AbortSignal): Promise<AggregatePreviewResponse> { return this.request("/filters/v3/preview",body,csrf,signal); }
  aggregateFilterFacets(body: AggregateFacetRequest, csrf: string, signal?: AbortSignal): Promise<RelationalFacetResponse> { return this.request("/filters/v3/facets",body,csrf,signal); }
  cohortFilterCatalog(dataset: string, search: string, signal?: AbortSignal): Promise<CohortCatalogResponse> { return this.request(`/filters/v4/${encodeURIComponent(dataset)}/catalog?search=${encodeURIComponent(search)}`,undefined,undefined,signal); }
  cohortFilterPreview(body: CohortPreviewRequest, csrf: string, signal?: AbortSignal): Promise<CohortPreviewResponse> { return this.request("/filters/v4/preview",body,csrf,signal); }
  cohortFilterFacets(body: CohortFacetRequest, csrf: string, signal?: AbortSignal): Promise<RelationalFacetResponse> { return this.request("/filters/v4/facets",body,csrf,signal); }
  customerEventCatalog(dataset: string, search: string, signal?: AbortSignal): Promise<CustomerEventCatalog> { return this.request(`/filters/customer-events/v1/${encodeURIComponent(dataset)}/catalog?search=${encodeURIComponent(search)}`,undefined,undefined,signal); }
  customerEventPreview(body: CustomerEventPreviewRequest, csrf: string, signal?: AbortSignal): Promise<CustomerEventPreviewResponse> { return this.request("/filters/customer-events/v1/preview",body,csrf,signal); }
  prepare(body: NewWorkspaceRequest, csrf: string): Promise<ComposerPrepareResponse> { return this.request("/prepare",body,csrf); }
  compare(body: ComposerCompareRequest, csrf: string, signal?: AbortSignal): Promise<CardComparisonV1> { return this.request("/compare",body,csrf,signal); }
  validate(definition: ComposerDefinitionV1, csrf: string, signal?: AbortSignal): Promise<ComposerValidationResponse> { return this.request("/validate",definition,csrf,signal); }
  savedPreflight(id: string, snapshot: string, block: string, signal?: AbortSignal): Promise<ComposerPreflightResponse> { return this.request(`/${encodeURIComponent(id)}/snapshots/${encodeURIComponent(snapshot)}/blocks/${encodeURIComponent(block)}/preflight`,undefined,undefined,signal); }
  preflight(body: ComposerApplyRequest, csrf: string, signal?: AbortSignal): Promise<ComposerPreflightResponse> { return this.request("/preflight",body,csrf,signal); }
  apply(body: ComposerApplyRequest, csrf: string, signal?: AbortSignal): Promise<ComposerApplyResponse> { return this.request("/apply",body,csrf,signal); }
  save(body: ComposerSaveRequest, csrf: string): Promise<ComposerReportResponse> { return this.request("/versions",body,csrf); }
  get(id: string, signal?: AbortSignal): Promise<ComposerEditorResponse> { return this.request(`/${encodeURIComponent(id)}`,undefined,undefined,signal); }
  snapshot(id: string, snapshot: string, signal?: AbortSignal): Promise<ComposerEditorResponse> { return this.request(`/${encodeURIComponent(id)}/snapshots/${encodeURIComponent(snapshot)}`,undefined,undefined,signal); }
  result(id: string, snapshot: string, block: string, signal?: AbortSignal): Promise<ComposerApplyResponse> { return this.request(`/${encodeURIComponent(id)}/snapshots/${encodeURIComponent(snapshot)}/blocks/${encodeURIComponent(block)}/result`,undefined,undefined,signal); }
}
''').encode()
    return result
