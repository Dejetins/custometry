import { describe, expect, it, vi } from "vitest";

import {
  NotificationApiClient,
  NotificationApiError,
  type NotificationItem,
} from "../../src/features/notifications/notification-api";

const item: NotificationItem = {
  notification_id: "11111111-1111-4111-8111-111111111111",
  workspace_id: "22222222-2222-4222-8222-222222222222",
  latest_event_id: "33333333-3333-4333-8333-333333333333",
  source_owner: "execution",
  source_type: "execution.run.failed",
  severity: "critical",
  category: "run",
  occurred_at: "2026-08-28T10:00:00Z",
  message_code: "RUN_FAILED",
  message_parameters: { state_code: "FAILED" },
  group_key: "run:fixture",
  source_event_count: 2,
  trace_id: "trace-fixture",
  resolved: false,
  read: false,
  dismissed: false,
  acknowledged: false,
  revision: 2,
  freshness: "fresh",
  deep_link: { status: "available", route_id: "UI-OPS-002", parameters: { run_id: "fixture" } },
};

describe("W35 typed W37 notification adapter", () => {
  it("uses the generated operation path, typed filters, and mandatory contract headers", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(new Response(JSON.stringify({
      items: [item], visible_count: 1,
    }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const client = new NotificationApiClient("/api/notifications", "/api/identity", fetcher);

    await expect(client.list({
      severity: "critical", category: "run", read: false, acknowledged: false, resolved: false,
    })).resolves.toMatchObject({ visible_count: 1 });

    const [url, init] = fetcher.mock.calls[0];
    expect(String(url)).toContain("/api/notifications/items?");
    expect(String(url)).toContain("severity=critical");
    expect(String(url)).toContain("acknowledged=false");
    const headers = new Headers(init?.headers);
    expect(headers.get("X-Contract-Version")).toBe("1.0.0");
    expect(headers.get("X-Request-ID")).toMatch(/^w35-/);
  });

  it("sends revision, audit reason, and unique idempotency identity for acknowledgement", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(new Response(JSON.stringify({
      ...item, acknowledged: true, revision: 3,
    }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const client = new NotificationApiClient("/api/notifications", "/api/identity", fetcher);

    await client.mutate(item, "acknowledge");

    const [url, init] = fetcher.mock.calls[0];
    expect(url).toBe(`/api/notifications/items/${item.notification_id}/acknowledge`);
    expect(JSON.parse(String(init?.body))).toEqual({
      expected_revision: 2,
      reason_code: "OPERATOR_CONFIRMED",
    });
    expect(new Headers(init?.headers).get("Idempotency-Key")).toMatch(/^w35-acknowledge-/);
  });

  it("preserves W37 stable error code and current revision", async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(new Response(JSON.stringify({
      code: "STALE_REVISION", current_revision: 7,
    }), { status: 409, headers: { "Content-Type": "application/json" } }));
    const client = new NotificationApiClient("/api/notifications", "/api/identity", fetcher);

    const failure = await client.detail(item.notification_id).catch((error: unknown) => error);
    expect(failure).toBeInstanceOf(NotificationApiError);
    expect(failure).toMatchObject({ status: 409, code: "STALE_REVISION", currentRevision: 7 });
  });
});
