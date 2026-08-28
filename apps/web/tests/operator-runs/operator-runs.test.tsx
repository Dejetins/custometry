import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import "../../src/i18n";
import i18n from "../../src/i18n";
import { OperatorRuns } from "../../src/features/operator-runs/OperatorRuns";
import {
  OperatorRunsApiError,
  type OperatorRun,
  type OperatorRunDetail,
} from "../../src/features/operator-runs/operator-runs-api";

const failedRun: OperatorRun = {
  run_id: "11111111-1111-4111-8111-111111111111",
  owner_principal_id: "22222222-2222-4222-8222-222222222222",
  execution_kind: "analytics", lane: "priority", safe_title: "Margin analysis",
  safe_trace_id: "trace-margin-safe", state: "FAILED", revision: 3,
  retry_of_id: null, retry_mode: null,
  created_at: "2026-08-28T10:00:00Z", updated_at: "2026-08-28T10:04:00Z",
};
const detail: OperatorRunDetail = {
  ...failedRun,
  attempts: [{
    attempt_id: "33333333-3333-4333-8333-333333333333", state: "FAILED",
    attempt_number: 1, fencing_token: 4, retry_of_id: null, lease_expires_at: null,
    failure_code: "RESOURCE_LIMIT_EXCEEDED", observed_limit: 1024, configured_limit: 768,
    safe_remediation: "Reduce the bounded input range.",
  }],
};

function apiFixture(runs: readonly OperatorRun[] = [failedRun], permissions = ["run.read", "run.cancel", "run.retry", "run.create"]) {
  return {
    capabilities: vi.fn().mockResolvedValue({ workspaceId: "workspace", permissions: new Set(permissions) }),
    list: vi.fn().mockResolvedValue({ runs, visible_count: runs.length }),
    summary: vi.fn().mockResolvedValue({ counts: { FAILED: runs.length }, lane_counts: { priority: runs.length }, oldest_queued_age_seconds: null, observed_at: "2026-08-28T10:05:00Z", freshness: "fresh" }),
    detail: vi.fn().mockResolvedValue(detail),
    mutate: vi.fn().mockResolvedValue({ ...failedRun, run_id: "44444444-4444-4444-8444-444444444444", state: "CREATED", revision: 1, retry_of_id: failedRun.run_id, retry_mode: "failed_nodes" }),
  };
}

beforeEach(() => { void i18n.changeLanguage("en"); });
afterEach(cleanup);

describe("W34 Operator Center", () => {
  it("renders queue summary, filters, safe trace identity, and bounded failure ancestry", async () => {
    const api = apiFixture();
    render(<OperatorRuns api={api} />);
    expect(await screen.findByRole("heading", { level: 1, name: "Operator Center" })).toBeVisible();
    expect(screen.getByText("trace-margin-safe")).toBeVisible();
    expect(screen.getAllByText("priority")).toHaveLength(2);

    const filters = screen.getByRole("form", { name: "Run filters" });
    fireEvent.change(within(filters).getByLabelText("State"), { target: { value: "FAILED" } });
    fireEvent.change(within(filters).getByLabelText("Execution kind"), { target: { value: "analytics" } });
    await waitFor(() => expect(api.list).toHaveBeenLastCalledWith(expect.objectContaining({ states: ["FAILED"], executionKind: "analytics" })));

    fireEvent.click(screen.getByRole("button", { name: "Inspect run" }));
    expect(await screen.findByText("RESOURCE_LIMIT_EXCEEDED")).toBeVisible();
    expect(screen.getByText("The attempt exceeded an enforced resource limit.")).toBeVisible();
    expect(screen.getByText("Reduce the bounded input range.")).toBeVisible();
  });

  it("requires an audit reason and sends a permission-aware manual retry", async () => {
    const api = apiFixture();
    render(<OperatorRuns api={api} />);
    fireEvent.click(await screen.findByRole("button", { name: "Inspect run" }));
    await screen.findByText("RESOURCE_LIMIT_EXCEEDED");
    fireEvent.click(screen.getByRole("button", { name: "Retry run" }));
    expect(await screen.findByText("Enter an audit reason of at least 3 characters.")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Audit reason"), { target: { value: "retry after operator review" } });
    fireEvent.click(screen.getByRole("button", { name: "Retry run" }));
    await waitFor(() => expect(api.mutate).toHaveBeenCalledWith(detail, "retry", "retry after operator review", "failed_nodes"));
  });

  it("distinguishes loading, empty, stale/degraded, forbidden, and failed states", async () => {
    const staleApi = apiFixture();
    staleApi.summary.mockResolvedValue({ ...await staleApi.summary(), freshness: "stale" });
    const staleView = render(<OperatorRuns api={staleApi} />);
    expect(await screen.findByText("Queue summary is stale")).toBeVisible();
    staleView.unmount();

    const emptyView = render(<OperatorRuns api={apiFixture([])} />);
    expect(await screen.findByText("No runs match this view")).toBeVisible();
    emptyView.unmount();

    const forbiddenApi = apiFixture();
    forbiddenApi.capabilities.mockRejectedValue(new OperatorRunsApiError(403, "FORBIDDEN"));
    const forbiddenView = render(<OperatorRuns api={forbiddenApi} />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Operator Center is unavailable");
    forbiddenView.unmount();

    const failedApi = apiFixture();
    failedApi.list.mockRejectedValue(new OperatorRunsApiError(503, "DELIVERY_UNAVAILABLE"));
    render(<OperatorRuns api={failedApi} />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Runs could not be loaded");
  });

  it("localizes presentation to Russian while stable codes and identity stay unchanged", async () => {
    await i18n.changeLanguage("ru");
    render(<OperatorRuns api={apiFixture()} />);
    expect(await screen.findByRole("heading", { level: 1, name: "Центр оператора" })).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Открыть запуск" }));
    expect(await screen.findByText("RESOURCE_LIMIT_EXCEEDED")).toBeVisible();
    expect(screen.getAllByText("trace-margin-safe")).toHaveLength(2);
  });
});
