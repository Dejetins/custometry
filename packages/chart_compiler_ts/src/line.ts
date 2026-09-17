/** Closed renderer-neutral input -> derived ECharts options. No browser or engine dependency. */
export interface DailyRow {
  readonly date: string;
  readonly net_revenue: string | null;
  readonly receipt_count: string | null;
  readonly average_receipt: string | null;
  readonly state: string;
}

export interface LineData {
  readonly workspaceId: string;
  readonly ownerPrincipalId: string;
  readonly policyHash: string;
  readonly artifactId: string;
  readonly artifactHash: string;
  readonly parameters: Readonly<Record<string, unknown>>;
  readonly metricVersionId: string;
  readonly metricHash: string;
  readonly daily: readonly DailyRow[];
  readonly comparison: readonly DailyRow[] | null;
}

/** Resolved by the Web adapter from the pinned system BrandProfile/CompanyPack. */
export interface LineRenderProfile {
  readonly locale: "ru" | "en";
  readonly primary: string;
  readonly comparison: string;
  readonly text: string;
  readonly grid: string;
}

export class ChartCompileError extends Error {
  constructor() { super("UNSUPPORTED_OR_MISMATCHED_LINE_CHART"); }
}

function requireValid(condition: unknown): asserts condition {
  if (!condition) throw new ChartCompileError();
}

function object(value: unknown): Record<string, unknown> {
  requireValid(value !== null && typeof value === "object" && !Array.isArray(value));
  requireValid(Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null);
  return value as Record<string, unknown>;
}

/** Sorting is for exact JSON equality, never for series/data ordering. */
function canonical(value: unknown, depth = 0): string {
  requireValid(depth < 24);
  if (value === null || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number") {
    requireValid(Number.isFinite(value));
    return JSON.stringify(value);
  }
  if (typeof value === "string") {
    requireValid(value.length < 4096 && !/[<>]|(?:https?|data|javascript):/i.test(value));
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return `[${value.map((item) => canonical(item, depth + 1)).join(",")}]`;
  const record = object(value);
  return `{${Object.keys(record).sort().map((key) => {
    requireValid(!/^(?:__proto__|constructor|prototype|option|formatter|renderItem|url|html)$/i.test(key));
    return `${JSON.stringify(key)}:${canonical(record[key], depth + 1)}`;
  }).join(",")}}`;
}

function equal(actual: unknown, expected: unknown): void {
  requireValid(canonical(actual) === canonical(expected));
}

const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const hash = /^[0-9a-f]{64}$/;
const states = new Set(["missing_calendar", "incomplete", "observed", "no_eligible_receipts", "comparison_unavailable"]);

function checkRows(rows: readonly DailyRow[]): void {
  requireValid(Array.isArray(rows) && rows.length <= 366);
  let previous = "";
  for (const row of rows) {
    equal(Object.keys(object(row)).sort(), ["average_receipt", "date", "net_revenue", "receipt_count", "state"]);
    requireValid(/^\d{4}-\d{2}-\d{2}$/.test(row.date) && row.date > previous);
    const day = new Date(`${row.date}T00:00:00Z`);
    requireValid(Number.isFinite(day.valueOf()) && day.toISOString().slice(0, 10) === row.date);
    requireValid(states.has(row.state));
    for (const field of ["net_revenue", "receipt_count", "average_receipt"] as const) {
      const value = row[field];
      requireValid(value === null || (typeof value === "string" && /^-?\d+(?:\.\d+)?$/.test(value) && Number.isFinite(Number(value))));
    }
    previous = row.date;
  }
}

/**
 * Spec validation deliberately accepts only the exact S03 canonical subset.
 * Extra nested fields fail closed; none are forwarded into engine options.
 * The caller must reauthorize the result and verify its reference/hash bindings.
 */
export function compileLineChart(specValue: unknown, data: LineData, profile: LineRenderProfile) {
  const spec = object(specValue);
  for (const value of [data.workspaceId, data.ownerPrincipalId, data.artifactId, data.metricVersionId, spec.chart_spec_id]) {
    requireValid(typeof value === "string" && uuid.test(value));
  }
  for (const value of [data.policyHash, data.artifactHash, data.metricHash]) requireValid(hash.test(value));
  requireValid(typeof spec.created_at === "string" && Number.isFinite(Date.parse(spec.created_at)));
  checkRows(data.daily);
  if (data.comparison !== null) checkRows(data.comparison);
  requireValid(profile.locale === "ru" || profile.locale === "en");
  for (const color of [profile.primary, profile.comparison, profile.text, profile.grid]) requireValid(/^#[0-9a-f]{6}$/i.test(color));

  equal(spec, {
    schema_version: "1.0.0", chart_type: "line", chart_spec_id: spec.chart_spec_id,
    workspace_id: data.workspaceId, created_at: spec.created_at,
    title_key: "analytics.net_revenue", title_override: null, description_key: null,
    source_binding: {
      source_artifact_id: data.artifactId, source_artifact_hash: data.artifactHash,
      projection: { current: "daily", comparison: "comparison.daily" },
      normalized_filter_expression: data.parameters,
      comparison_artifact_id: data.comparison === null ? null : data.artifactId,
    },
    chart_data: {
      data_artifact_id: data.artifactId, schema_id: "sales-report", schema_version: 1,
      grain: "date", row_count: data.daily.length, column_count: 5,
      deterministic_reduction: "none", reduction_policy_hash: null,
    },
    dimensions: [{ field: "date", type: "date", timezone: "UTC" }],
    measures: [{ field: "net_revenue", metric_version_id: data.metricVersionId,
      metric_content_hash: data.metricHash, unit: "EUR", number_format: { decimal_places: 2 } }],
    axes: [{ id: "date", dimension: "date" }, { id: "value", measure: "net_revenue", unit: "EUR" }],
    series: [{ id: "current", projection: "daily", x: "date", y: "net_revenue", color_role: "series-primary" },
      ...(data.comparison === null ? [] : [{ id: "comparison", projection: "comparison.daily", x: "date", y: "net_revenue", color_role: "series-comparison", alignment: "same_dates_previous_year" }])],
    annotations: [], range_timeline: null,
    interaction: { zoom: false, pan: false, brush: false, tooltip: true, legend_filter: false, drilldown_action_id: null },
    visual_semantics: {
      semantic_color_roles: ["series-primary", "series-comparison"],
      current_period_style: { line: "solid" }, comparison_period_style: { line: "dashed" },
      forecast_style: null, interval_style: null, promotion_style: null,
    },
    accessibility: { summary_key: "analytics.net_revenue", summary_params: {}, table_alternative: "required", series_descriptions: ["current", "comparison"] },
    export_policy: { email: "png_from_ssr_svg", xlsx: "native_when_lossless_else_same_png_pipeline", allow_raster_fallback: false },
    access_policy: { owner_principal_id: data.ownerPrincipalId, policy_hash: data.policyHash },
  });

  // Resolve the spec's same-calendar-date alignment, not positional array zip:
  // the previous year may contain an extra leap day. Keep its table unchanged.
  const priorByDate = new Map(data.comparison?.map((row) => [row.date, row]) ?? []);
  const comparisonValues = data.daily.map((row) => {
    const previousDate = `${String(Number(row.date.slice(0, 4)) - 1).padStart(4, "0")}${row.date.slice(4)}`;
    return priorByDate.get(previousDate)?.net_revenue ?? null;
  });
  const names = profile.locale === "ru" ? ["Текущий период", "Предыдущий год"] : ["Current period", "Previous year"];
  const line = (values: readonly (string | null)[], comparison: boolean) => ({
    id: comparison ? "comparison" : "current", name: names[comparison ? 1 : 0], type: "line" as const,
    data: values.map((value) => value === null ? null : Number(value)),
    connectNulls: false, showSymbol: false, smooth: false,
    lineStyle: { color: comparison ? profile.comparison : profile.primary, type: comparison ? "dashed" as const : "solid" as const },
    itemStyle: { color: comparison ? profile.comparison : profile.primary },
  });
  return {
    compilerContractVersion: "canonical-line/v1" as const,
    artifactId: data.artifactId, artifactHash: data.artifactHash,
    chartSpecId: spec.chart_spec_id as string,
    metricVersionId: data.metricVersionId, metricHash: data.metricHash, unit: "EUR" as const,
    // Original decimal strings remain exact for the accessible table.
    table: data.daily.map((row) => ({ ...row })),
    comparisonTable: data.comparison?.map((row) => ({ ...row })) ?? null,
    option: {
      animation: false, textStyle: { fontFamily: "Inter, system-ui, sans-serif", color: profile.text },
      grid: { left: 16, right: 20, top: 48, bottom: 20, containLabel: true },
      tooltip: { trigger: "axis" as const, renderMode: "richText" as const },
      legend: { top: 8, selectedMode: false, textStyle: { color: profile.text } },
      xAxis: { type: "category" as const, data: data.daily.map((row) => row.date), boundaryGap: false },
      yAxis: { type: "value" as const, name: "EUR", splitLine: { lineStyle: { color: profile.grid } } },
      series: [line(data.daily.map((row) => row.net_revenue), false), ...(data.comparison === null ? [] : [line(comparisonValues, true)])],
    },
  };
}
