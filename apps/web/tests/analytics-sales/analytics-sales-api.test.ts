import { describe, expect, it, vi } from "vitest";

import {
  SalesAnalyticsApiClient,
  SalesAnalyticsApiError,
  type SalesAnalyticsResult,
  type SalesRunRequest,
} from "../../src/features/analytics-sales/analytics-sales-api";

const result: SalesAnalyticsResult = {
  result_id: "11111111-1111-4111-8111-111111111111",
  result_type: "sales",
  semantic_dataset_version_id: "22222222-2222-4222-8222-222222222222",
  request_hash: "a".repeat(64), policy_hash: "b".repeat(64),
  applied_comparison_mode: "previous_year_calendar_aligned",
  resolved_current_period: { starts_on: "2025-01-01", ends_on: "2025-12-31" },
  resolved_comparison_period: { starts_on: "2024-01-01", ends_on: "2024-12-31" },
  timezone: "UTC", calendar_version_id: "33333333-3333-4333-8333-333333333333",
  comparison_policy_hash: "c".repeat(64), normalized_filter_expression_hash: "d".repeat(64),
  metric_groups: [], current_coverage: { observed_days: 2, period_days: 365 }, comparison_coverage: { observed_days: 2, period_days: 366 },
  comparability_status: "comparable", limitation_codes: [], quality: { decision: "passed", capabilities: {} },
  freshness: { max_event_date: "2025-12-31" }, lineage: { fact_scope: "receipt_header" },
  manifest: { relative_uri: "analytics-results/result.json", content_hash: "e".repeat(64), byte_size: 42, immutable: true },
};

describe("W32 typed W16 analytics adapter", () => {
  it("loads only the latest sales projection with mandatory contract headers", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(new Response(JSON.stringify({
      results: [{ ...result, result_type: "customer" }, result], visible_count: 2,
    }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const client = new SalesAnalyticsApiClient("/api/analytics", "/api/identity", fetcher);

    await expect(client.latest()).resolves.toEqual(result);
    const [url, init] = fetcher.mock.calls[0];
    expect(url).toBe("/api/analytics/results?offset=0&limit=50");
    const headers = new Headers(init?.headers);
    expect(headers.get("X-Contract-Version")).toBe("1.0.0");
    expect(headers.get("X-Request-ID")).toMatch(/^w32-/);
    expect(init?.credentials).toBe("same-origin");
  });

  it("posts exact period, comparison, and typed filters without calculating metrics", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(new Response(JSON.stringify(result), {
      status: 200, headers: { "Content-Type": "application/json" },
    }));
    const client = new SalesAnalyticsApiClient("/api/analytics", "/api/identity", fetcher);
    const payload: SalesRunRequest = {
      result_type: "sales", semantic_dataset_version_id: result.semantic_dataset_version_id,
      comparison: {
        mode: "previous_year_calendar_aligned",
        current_period: result.resolved_current_period,
        comparison_period: result.resolved_comparison_period,
        timezone: "UTC", calendar_version_id: result.calendar_version_id,
        incomplete_period_policy: "explicit_partial", leap_day_policy: "calendar_map",
        iso_week_53_policy: "explicit_partial", definition_compatibility_policy: "require_same_versions",
      },
      filters: [{ field: "channel_id", operator: "eq", value: "web" }],
      rfm_score_bins: 5, rfm_frequency_measure: "receipt_count", rfm_segment_rule_set_version: "rfm-retail-v1",
    };

    await client.run(payload);
    const [url, init] = fetcher.mock.calls[0];
    expect(url).toBe("/api/analytics/results");
    expect(init?.method).toBe("POST");
    expect(JSON.parse(String(init?.body))).toEqual(payload);
  });

  it("preserves W16 stable error codes", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(new Response(JSON.stringify({ code: "FORBIDDEN" }), {
      status: 403, headers: { "Content-Type": "application/json" },
    }));
    const client = new SalesAnalyticsApiClient("/api/analytics", "/api/identity", fetcher);
    const failure = await client.latest().catch((error: unknown) => error);
    expect(failure).toBeInstanceOf(SalesAnalyticsApiError);
    expect(failure).toMatchObject({ status: 403, code: "FORBIDDEN" });
  });
});
