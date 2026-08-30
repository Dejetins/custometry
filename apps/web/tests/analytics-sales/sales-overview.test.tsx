import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import "../../src/i18n";
import i18n from "../../src/i18n";
import { SalesOverview } from "../../src/features/analytics-sales/SalesOverview";
import { SalesAnalyticsApiError, type SalesAnalyticsResult } from "../../src/features/analytics-sales/analytics-sales-api";

const metric = (metric_id: string, current_value: string, comparison_value: string, absolute_change: string, percent_change: string) => ({
  metric_id, metric_order: 10, current_value, comparison_value, absolute_change, percent_change,
  compact_current: current_value, compact_comparison: comparison_value, limitation_codes: [],
});

const result: SalesAnalyticsResult = {
  result_id: "11111111-1111-4111-8111-111111111111", result_type: "sales",
  semantic_dataset_version_id: "22222222-2222-4222-8222-222222222222",
  request_hash: "a".repeat(64), policy_hash: "b".repeat(64), applied_comparison_mode: "previous_year_calendar_aligned",
  resolved_current_period: { starts_on: "2025-01-01", ends_on: "2025-12-31" },
  resolved_comparison_period: { starts_on: "2024-01-01", ends_on: "2024-12-31" }, timezone: "UTC",
  calendar_version_id: "33333333-3333-4333-8333-333333333333", comparison_policy_hash: "c".repeat(64),
  normalized_filter_expression_hash: "d".repeat(64),
  metric_groups: [
    { group_id: "finance", group_order: 10, metrics: [metric("net_revenue", "450", "300", "150", "50"), metric("discount_amount", "30", "20", "10", "50")] },
    { group_id: "commerce", group_order: 20, metrics: [metric("receipt_count", "2", "2", "0", "0"), metric("average_receipt", "225", "150", "75", "50")] },
  ],
  current_coverage: { observed_days: 2, period_days: 365 }, comparison_coverage: { observed_days: 2, period_days: 366 },
  comparability_status: "comparable", limitation_codes: [], quality: { decision: "passed", capabilities: { sales: "available" } },
  freshness: { max_event_date: "2025-12-31" }, lineage: { fact_scope: "receipt_header", source_artifact_ids: ["artifact"] },
  manifest: { relative_uri: "analytics-results/result.json", content_hash: "e".repeat(64), byte_size: 42, immutable: true },
};

function apiFixture(value: SalesAnalyticsResult | null = result, permissions = ["analysis.read", "analysis.run"]) {
  return {
    capabilities: vi.fn().mockResolvedValue({ workspaceId: "workspace", permissions: new Set(permissions) }),
    latest: vi.fn().mockResolvedValue(value ?? undefined),
    run: vi.fn().mockResolvedValue(value ?? result),
  };
}

beforeEach(() => { void i18n.changeLanguage("en"); });
afterEach(cleanup);

describe("W32 production Sales Overview", () => {
  it("renders governed KPI order, unavailable boundaries, and Result Trust", async () => {
    render(<SalesOverview api={apiFixture()} />);
    expect(await screen.findByRole("heading", { level: 1, name: "Sales Overview" })).toBeVisible();
    const strip = document.querySelector(".sales-kpi-strip");
    expect(strip).toHaveTextContent("Revenue");
    expect(strip).toHaveTextContent("Orders");
    expect(strip).toHaveTextContent("Average order value");
    expect(strip).toHaveTextContent("Margin");
    expect(screen.getByText("W16 exposes governed period aggregates, not a time-series trend.")).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Open Result Trust" }));
    expect(screen.getByRole("dialog", { name: "Result Trust" })).toHaveTextContent("receipt_header");
    expect(screen.getByRole("dialog")).toHaveTextContent("PVM decomposition is not part of W16");
  });

  it("submits exact comparison and typed filters only with analysis.run", async () => {
    const api = apiFixture();
    render(<SalesOverview api={api} />);
    const form = await screen.findByRole("form", { name: "Period, comparison and filters" });
    fireEvent.change(within(form).getByLabelText("Store"), { target: { value: "store-7" } });
    fireEvent.change(within(form).getByLabelText("Channel"), { target: { value: "web" } });
    fireEvent.click(within(form).getByRole("button", { name: "Apply governed view" }));
    await waitFor(() => expect(api.run).toHaveBeenCalledOnce());
    expect(api.run).toHaveBeenCalledWith(expect.objectContaining({ filters: [
      { field: "store_id", operator: "eq", value: "store-7" },
      { field: "channel_id", operator: "eq", value: "web" },
    ] }));

    cleanup();
    render(<SalesOverview api={apiFixture(result, ["analysis.read"])} />);
    expect(await screen.findByText(/analysis\.read/)).toBeVisible();
    expect(screen.getByRole("button", { name: "Apply governed view" })).toBeDisabled();
  });

  it("keeps empty, stale/degraded, forbidden, and failed states truthful", async () => {
    const empty = render(<SalesOverview api={apiFixture(null)} />);
    expect(await screen.findByText("No visible sales result")).toBeVisible();
    empty.unmount();

    const degraded = render(<SalesOverview api={apiFixture({ ...result, comparability_status: "partial" })} />);
    expect((await screen.findAllByText("Result is degraded"))[0]).toBeVisible();
    degraded.unmount();

    const forbiddenApi = apiFixture();
    forbiddenApi.capabilities.mockRejectedValue(new SalesAnalyticsApiError(403, "FORBIDDEN"));
    const forbidden = render(<SalesOverview api={forbiddenApi} />);
    expect(await screen.findByText("Sales Overview is unavailable")).toBeVisible();
    forbidden.unmount();

    const failedApi = apiFixture();
    failedApi.latest.mockRejectedValue(new SalesAnalyticsApiError(503, "DEPENDENCY_UNAVAILABLE"));
    render(<SalesOverview api={failedApi} />);
    expect(await screen.findByText("Sales result could not be loaded")).toBeVisible();
  });

  it("switches all feature copy to Russian", async () => {
    await i18n.changeLanguage("ru");
    render(<SalesOverview api={apiFixture()} />);
    expect(await screen.findByRole("heading", { level: 1, name: "Обзор продаж" })).toBeVisible();
    expect(screen.getByLabelText("Магазин")).toBeVisible();
    expect(screen.getByText("Реальная агрегатная граница W16")).toBeVisible();
  });
});
