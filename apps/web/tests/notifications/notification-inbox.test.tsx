import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import "../../src/i18n";
import i18n from "../../src/i18n";
import { NotificationInbox } from "../../src/features/notifications/NotificationInbox";
import {
  NotificationApiError,
  type NotificationItem,
} from "../../src/features/notifications/notification-api";

const critical: NotificationItem = {
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
  read: true,
  dismissed: false,
  acknowledged: false,
  revision: 2,
  freshness: "fresh",
  deep_link: { status: "available", route_id: "UI-OPS-002", parameters: { run_id: "run-42" } },
};

function apiFixture(items: readonly NotificationItem[] = [critical]) {
  return {
    capabilities: vi.fn().mockResolvedValue({
      workspaceId: critical.workspace_id,
      permissions: new Set(["notification.read", "notification.acknowledge"]),
    }),
    list: vi.fn().mockResolvedValue({ items, visible_count: items.length }),
    unreadCount: vi.fn().mockResolvedValue({ unread_count: 1, capped: false }),
    mutate: vi.fn().mockImplementation(async (item: NotificationItem, action: string) => ({
      ...item,
      read: action === "read" ? true : item.read,
      dismissed: action === "dismiss" ? true : item.dismissed,
      acknowledged: action === "acknowledge" ? true : item.acknowledged,
      revision: item.revision + 1,
    })),
  };
}

beforeEach(() => { void i18n.changeLanguage("en"); });
afterEach(cleanup);

describe("W35 production notification inbox", () => {
  it("renders duplicate groups and applies severity/category/state filters", async () => {
    const api = apiFixture();
    render(<MemoryRouter><NotificationInbox api={api} /></MemoryRouter>);

    expect(await screen.findByText("A run failed and needs review.")).toBeVisible();
    expect(screen.getByText("2 events in group")).toBeVisible();
    const filters = screen.getByRole("form", { name: "Notification filters" });
    fireEvent.change(within(filters).getByLabelText("Severity"), { target: { value: "critical" } });
    fireEvent.change(within(filters).getByLabelText("Acknowledgement"), { target: { value: "false" } });
    await waitFor(() => expect(api.list).toHaveBeenLastCalledWith(expect.objectContaining({
      severity: "critical", acknowledged: false,
    })));
  });

  it("uses permission-aware actions, persists returned state, and emits safe navigation", async () => {
    const api = apiFixture();
    render(<MemoryRouter><NotificationInbox api={api} /></MemoryRouter>);
    fireEvent.click(await screen.findByRole("button", { name: "View details" }));

    expect(screen.getByRole("link", { name: "Open related run" })).toHaveAttribute(
      "href", "/w/northwind-retail/runs/run-42",
    );
    fireEvent.click(screen.getByRole("button", { name: "Acknowledge" }));
    await waitFor(() => expect(api.mutate).toHaveBeenCalledWith(critical, "acknowledge"));
    expect(await screen.findByText("Acknowledged")).toBeVisible();
  });

  it("presents empty, stale/degraded, forbidden, and failed states without pretending they are success", async () => {
    const staleApi = apiFixture([{ ...critical, freshness: "stale" }]);
    const view = render(<MemoryRouter><NotificationInbox api={staleApi} /></MemoryRouter>);
    expect(await screen.findByText("Some notification data may be delayed")).toBeVisible();
    view.unmount();

    const emptyApi = apiFixture([]);
    const emptyView = render(<MemoryRouter><NotificationInbox api={emptyApi} /></MemoryRouter>);
    expect(await screen.findByText("No notifications match this view")).toBeVisible();
    emptyView.unmount();

    const forbiddenApi = apiFixture();
    forbiddenApi.capabilities.mockRejectedValue(new NotificationApiError(403, "FORBIDDEN"));
    const forbiddenView = render(<MemoryRouter><NotificationInbox api={forbiddenApi} /></MemoryRouter>);
    expect(await screen.findByRole("alert")).toHaveTextContent("Notification inbox is unavailable");
    forbiddenView.unmount();

    const failedApi = apiFixture();
    failedApi.list.mockRejectedValue(new NotificationApiError(503, "DEPENDENCY_UNAVAILABLE"));
    render(<MemoryRouter><NotificationInbox api={failedApi} /></MemoryRouter>);
    expect(await screen.findByRole("alert")).toHaveTextContent("Notifications could not be loaded");
  });

  it("switches all feature copy to Russian without changing stable codes", async () => {
    await i18n.changeLanguage("ru");
    const api = apiFixture();
    render(<MemoryRouter><NotificationInbox api={api} /></MemoryRouter>);
    expect(await screen.findByRole("heading", { level: 1, name: "Центр уведомлений" })).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Открыть подробности" }));
    expect(screen.getByText("RUN_FAILED")).toBeVisible();
    expect(screen.getAllByText("Запуск завершился с ошибкой и требует проверки.")).toHaveLength(2);
  });
});
