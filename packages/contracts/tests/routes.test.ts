import { describe, expect, it } from "vitest";

import { routeRegistry } from "../src/index";

describe("canonical route registry", () => {
  it("contains the 110 normative route-level UI entries", () => {
    expect(routeRegistry.routes).toHaveLength(110);
    expect(new Set(routeRegistry.routes.map((route) => route.id)).size).toBe(110);
  });

  it("uses canonical workspace paths and known lifecycle states", () => {
    const sales = routeRegistry.routes.find((route) => route.id === "UI-AN-003");
    expect(sales?.path).toBe("/w/:workspaceKey/analytics/sales");
    expect(sales?.title_key).toBe("UI-AN-003");
    expect(["foundation", "planned", "implemented"]).toContain(sales?.status);
  });

  it("uses one locale-neutral title key per registered route", () => {
    const registeredRoutes = [
      ...routeRegistry.routes,
      ...routeRegistry.foundation_utility_routes,
    ];
    const titleKeys = registeredRoutes.map((route) => route.title_key);

    expect(new Set(titleKeys).size).toBe(registeredRoutes.length);
    expect(titleKeys.every((key) => /^(UI-[A-Z]+-\d{3}|FOUNDATION-[A-Z][A-Z-]*)$/.test(key))).toBe(true);
  });
});
