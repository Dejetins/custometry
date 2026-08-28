import { describe, expect, it, vi } from "vitest";

import {
  OperatorRunsApiClient,
  OperatorRunsApiError,
  type OperatorRun,
} from "../../src/features/operator-runs/operator-runs-api";

const run: OperatorRun = {
  run_id: "11111111-1111-4111-8111-111111111111",
  owner_principal_id: "22222222-2222-4222-8222-222222222222",
  execution_kind: "ingestion", lane: "default", safe_title: "Retail import",
  safe_trace_id: "trace-retail", state: "RUNNING", revision: 2,
  retry_of_id: null, retry_mode: null,
  created_at: "2026-08-28T10:00:00Z", updated_at: "2026-08-28T10:01:00Z",
};

describe("W34 typed execution-control adapter", () => {
  it("uses generated operations, repeated state filters, and required boundary headers", async () => {
    const fetcher = vi.fn().mockResolvedValue(new Response(JSON.stringify({ runs: [run], visible_count: 1 }), { status: 200 }));
    const client = new OperatorRunsApiClient("/api/execution", "/api/identity", fetcher);
    await client.list({ states: ["QUEUED", "RUNNING"], executionKind: "ingestion", safeTraceId: "trace-retail" });

    const [url, init] = fetcher.mock.calls[0] as [string, RequestInit];
    expect(url).toContain("/api/execution/runs?");
    expect(url).toContain("states=QUEUED&states=RUNNING");
    expect(url).toContain("execution_kind=ingestion");
    expect(url).toContain("safe_trace_id=trace-retail");
    const headers = new Headers(init.headers);
    expect(headers.get("X-Contract-Version")).toBe("1.0.0");
    expect(headers.get("X-Request-ID")).toMatch(/^w34-/);
  });

  it("sends revision, audit reason, retry mode, and a scoped idempotency key", async () => {
    const fetcher = vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...run, state: "CREATED", retry_of_id: run.run_id }), { status: 200 }));
    const client = new OperatorRunsApiClient("/api/execution", "/api/identity", fetcher);
    await client.mutate({ ...run, state: "FAILED", revision: 3 }, "retry", "retry after bounded review", "failed_nodes");

    const [url, init] = fetcher.mock.calls[0] as [string, RequestInit];
    expect(url).toBe(`/api/execution/runs/${run.run_id}/retry`);
    expect(init.method).toBe("POST");
    expect(JSON.parse(String(init.body))).toEqual({ expected_revision: 3, reason: "retry after bounded review", mode: "failed_nodes" });
    expect(new Headers(init.headers).get("Idempotency-Key")).toMatch(/^w34-retry-/);
  });

  it("preserves stable server code and current state for safe conflict presentation", async () => {
    const fetcher = vi.fn().mockResolvedValue(new Response(JSON.stringify({ code: "STALE_REVISION", current_state: "SUCCEEDED" }), { status: 409 }));
    const client = new OperatorRunsApiClient("/api/execution", "/api/identity", fetcher);
    await expect(client.detail(run.run_id)).rejects.toEqual(expect.objectContaining<Partial<OperatorRunsApiError>>({ status: 409, code: "STALE_REVISION", currentState: "SUCCEEDED" }));
  });
});
