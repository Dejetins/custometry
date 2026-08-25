import { describe, expect, it } from "vitest";

import { resolveApplicationRoute } from "../../src/app/router/route-resolution";

describe("W31 route resolution", () => {
  it.each([
    ["/auth/sign-in", "auth", "UI-AUTH-001", "public"],
    ["/help", "global", "UI-HELP-001", "authenticated_global"],
    ["/bootstrap", "setup", "UI-AUTH-002", "public"],
    ["/onboarding?step=profile", "setup", "UI-AUTH-005", "authenticated_global"],
    ["/w/opaque-workspace/overview", "workspace", "UI-CORE-001", "workspace_member"],
    ["/admin", "installation", "UI-ADMIN-001", "global_permission"],
    ["/w/opaque-workspace/analytics/sales?focus=revenue", "focus", "UI-AN-003", "workspace_object"],
  ])("resolves %s without treating presentation as authorization", (href, profile, routeId, guard) => {
    const url = new URL(href, "http://custometry.test");
    const result = resolveApplicationRoute(url.pathname, url.search);
    expect(result.kind).toBe("route");
    if (result.kind !== "route") return;
    expect(result.shellProfile).toBe(profile);
    expect(result.route.id).toBe(routeId);
    expect(result.contract.guard_profile).toBe(guard);
  });

  it("preserves a compatibility view and rejects non-allowlisted query state", () => {
    const compatible = resolveApplicationRoute(
      "/w/northwind-retail/analytics/sales",
      "?view=html-prototype",
    );
    expect(compatible.kind === "route" && compatible.compatibilityView).toBe("html-prototype");

    const rejected = resolveApplicationRoute(
      "/w/northwind-retail/analytics/sales",
      "?raw_customer_email=hidden@example.test",
    );
    expect(rejected).toMatchObject({ kind: "system", stableCode: "SYS-404-QUERY" });
  });

  it("exposes system state only as an explicit development fixture", () => {
    const result = resolveApplicationRoute(
      "/w/northwind-retail/overview",
      "?view=w31-forbidden",
    );
    expect(result).toMatchObject({ kind: "route", shellProfile: "system", systemFixture: "forbidden" });
  });
});
