import { describe, expect, it } from "vitest";

import type { NotificationDeepLink } from "../../src/features/notifications/notification-api";
import { resolveNotificationDeepLink } from "../../src/features/notifications/notification-deep-link";

describe("W35 safe notification deep links", () => {
  it("maps allowlisted W37 run parameters to the canonical W31 route", () => {
    expect(resolveNotificationDeepLink({
      status: "available", route_id: "UI-OPS-002", parameters: { run_id: "run-42" },
    }, "northwind-retail")).toBe("/w/northwind-retail/runs/run-42");
  });

  it.each<NotificationDeepLink>([
    { status: "available", route_id: "https://evil.example", parameters: {} },
    { status: "available", route_id: "UI-OPS-002", parameters: { run_id: "../secret" } },
    { status: "available", route_id: "UI-OPS-002", parameters: { run_id: "safe", returnTo: "evil" } },
    { status: "unavailable", route_id: "UI-OPS-002", parameters: { run_id: "safe" } },
  ])("rejects unavailable, arbitrary, traversal, and extra-parameter links", (link) => {
    expect(resolveNotificationDeepLink(link, "northwind-retail")).toBeUndefined();
  });
});
