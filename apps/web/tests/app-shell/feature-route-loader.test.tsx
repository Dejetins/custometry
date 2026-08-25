import type { ComponentType } from "react";
import { describe, expect, it } from "vitest";

import type { FeatureRouteImportMap, FeatureRouteProps } from "../../src/app/routes/feature-route-contract";
import { loadFeatureRoute } from "../../src/app/routes/feature-route-loader";

const RouteComponent: ComponentType<FeatureRouteProps> = () => <h1>Feature route</h1>;

describe("W31 lazy feature route seam", () => {
  it("discovers a route module by stable route ID without a central registry", async () => {
    const imports: FeatureRouteImportMap = {
      "../../features/analytics/UI-AN-003.feature-route.tsx": async () => ({
        routeId: "UI-AN-003",
        default: RouteComponent,
      }),
    };
    const module = await loadFeatureRoute("UI-AN-003", imports);
    expect(module?.routeId).toBe("UI-AN-003");
    expect(module?.default).toBe(RouteComponent);
  });

  it("keeps the planned compatibility surface when no feature module exists", async () => {
    await expect(loadFeatureRoute("UI-CORE-001", {})).resolves.toBeUndefined();
  });

  it("rejects a filename/export identity mismatch", async () => {
    const imports: FeatureRouteImportMap = {
      "../../features/analytics/UI-AN-003.feature-route.tsx": async () => ({
        routeId: "UI-AN-004",
        default: RouteComponent,
      }),
    };
    await expect(loadFeatureRoute("UI-AN-003", imports)).rejects.toThrow(/declares UI-AN-004/);
  });
});
