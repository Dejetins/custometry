export const ANALYTICS_API_VERSION = "1.0.0" as const;

export type ComparisonMode =
  | "none"
  | "previous_year_same_dates"
  | "previous_year_calendar_aligned"
  | "previous_year_iso_week_aligned"
  | "previous_year_fiscal_period"
  | "previous_year_comparable_elapsed_days";

export interface SalesMetricProjection {
  readonly metric_id: string;
  readonly metric_order: number;
  readonly current_value: string | null;
  readonly comparison_value: string | null;
  readonly absolute_change: string | null;
  readonly percent_change: string | null;
  readonly compact_current: string | null;
  readonly compact_comparison: string | null;
  readonly limitation_codes: readonly string[];
}

export interface SalesMetricGroupProjection {
  readonly group_id: string;
  readonly group_order: number;
  readonly metrics: readonly SalesMetricProjection[];
}

export interface SalesAnalyticsResult {
  readonly result_id: string;
  readonly result_type: "sales";
  readonly semantic_dataset_version_id: string;
  readonly request_hash: string;
  readonly policy_hash: string;
  readonly applied_comparison_mode: ComparisonMode;
  readonly resolved_current_period: Readonly<{ starts_on: string; ends_on: string }>;
  readonly resolved_comparison_period: Readonly<{ starts_on: string; ends_on: string }> | null;
  readonly timezone: string;
  readonly calendar_version_id: string;
  readonly comparison_policy_hash: string;
  readonly normalized_filter_expression_hash: string;
  readonly metric_groups: readonly SalesMetricGroupProjection[];
  readonly current_coverage: Readonly<{ observed_days: number; period_days: number }>;
  readonly comparison_coverage: Readonly<{ observed_days: number; period_days: number }> | null;
  readonly comparability_status: "comparable" | "partial" | "not_comparable";
  readonly limitation_codes: readonly string[];
  readonly quality: Readonly<{
    decision?: string;
    capabilities?: Readonly<Record<string, string>>;
  }>;
  readonly freshness: Readonly<{
    max_event_date?: string | null;
    status?: "fresh" | "stale" | "degraded";
  }>;
  readonly lineage: Readonly<{
    source_artifact_ids?: readonly string[];
    source_content_hashes?: Readonly<Record<string, string>>;
    canonical_customer_key?: string;
    fact_scope?: string;
  }>;
  readonly manifest: Readonly<{
    relative_uri: string;
    content_hash: string;
    byte_size: number;
    immutable: boolean;
  }>;
}

interface AnalyticsResultListResponse {
  readonly results: readonly (SalesAnalyticsResult | { readonly result_type: string })[];
  readonly visible_count: number;
}

interface IdentityMeResponse {
  readonly workspace_id: string;
  readonly permissions: readonly string[];
}

interface ErrorResponse {
  readonly code?: string;
}

export interface SalesCapabilities {
  readonly workspaceId: string;
  readonly permissions: ReadonlySet<string>;
}

export interface SalesFilterRequest {
  readonly field: "store_id" | "channel_id" | "currency" | "status" | "net_amount";
  readonly operator: "eq" | "in" | "gte" | "lte";
  readonly value: string | readonly string[];
}

export interface SalesRunRequest {
  readonly result_type: "sales";
  readonly semantic_dataset_version_id: string;
  readonly comparison: Readonly<{
    mode: ComparisonMode;
    current_period: Readonly<{ starts_on: string; ends_on: string }>;
    comparison_period: Readonly<{ starts_on: string; ends_on: string }> | null;
    timezone: string;
    calendar_version_id: string;
    incomplete_period_policy: "exclude" | "comparable_elapsed_days" | "explicit_partial";
    leap_day_policy: "calendar_map" | "exclude" | "merge_with_feb_28";
    iso_week_53_policy: "calendar_map" | "exclude" | "explicit_partial";
    definition_compatibility_policy: "require_same_versions" | "allow_explicit_rebase";
  }>;
  readonly filters: readonly SalesFilterRequest[];
  readonly rfm_score_bins: 5;
  readonly rfm_frequency_measure: "receipt_count";
  readonly rfm_segment_rule_set_version: "rfm-retail-v1";
}

export class SalesAnalyticsApiError extends Error {
  public constructor(public readonly status: number, public readonly code: string) {
    super(code);
    this.name = "SalesAnalyticsApiError";
  }
}

function requestIdentity(): string {
  const generated = globalThis.crypto?.randomUUID?.();
  return generated ? `w32-${generated}` : `w32-${Date.now().toString(36)}`;
}

async function errorFrom(response: Response): Promise<SalesAnalyticsApiError> {
  let payload: ErrorResponse = {};
  try {
    payload = (await response.json()) as ErrorResponse;
  } catch {
    // A non-JSON gateway response still gets a stable presentation code.
  }
  return new SalesAnalyticsApiError(response.status, payload.code ?? `HTTP_${response.status}`);
}

function isSalesResult(value: SalesAnalyticsResult | { readonly result_type: string }): value is SalesAnalyticsResult {
  return value.result_type === "sales";
}

export class SalesAnalyticsApiClient {
  public constructor(
    private readonly analyticsBase = "/api/analytics",
    private readonly identityBase = "/api/identity",
    private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis),
  ) {}

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const headers = new Headers(init.headers);
    headers.set("Accept", "application/json");
    headers.set("X-Contract-Version", ANALYTICS_API_VERSION);
    headers.set("X-Request-ID", requestIdentity());
    const response = await this.fetcher(`${this.analyticsBase}${path}`, {
      ...init,
      credentials: "same-origin",
      headers,
    });
    if (!response.ok) throw await errorFrom(response);
    return (await response.json()) as T;
  }

  public async capabilities(): Promise<SalesCapabilities> {
    const response = await this.fetcher(`${this.identityBase}/me`, {
      method: "GET",
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw await errorFrom(response);
    const payload = (await response.json()) as IdentityMeResponse;
    return { workspaceId: payload.workspace_id, permissions: new Set(payload.permissions) };
  }

  public async latest(): Promise<SalesAnalyticsResult | undefined> {
    const payload = await this.request<AnalyticsResultListResponse>("/results?offset=0&limit=50", { method: "GET" });
    return payload.results.find(isSalesResult);
  }

  public run(payload: SalesRunRequest): Promise<SalesAnalyticsResult> {
    return this.request("/results", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  }
}

export function metricById(result: SalesAnalyticsResult, metricId: string): SalesMetricProjection | undefined {
  return result.metric_groups.flatMap((group) => group.metrics).find((metric) => metric.metric_id === metricId);
}

export const salesAnalyticsApi = new SalesAnalyticsApiClient();
