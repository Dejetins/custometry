import { describe, expect, it } from "vitest";

import routeRegistry from "../../contracts/routes/ui-routes.json";
import { foundationCatalogs, routeTitleCatalogs } from "../src/index";

describe("Foundation localization", () => {
  it("keeps English and Russian keys in parity", () => {
    expect(Object.keys(foundationCatalogs.en).sort()).toEqual(
      Object.keys(foundationCatalogs.ru).sort(),
    );
  });

  it("keeps route-title catalogs in parity with all registered routes", () => {
    const normativeTitleKeys = routeRegistry.routes.map((route) => route.title_key);
    const allTitleKeys = [
      ...normativeTitleKeys,
      ...routeRegistry.foundation_utility_routes.map((route) => route.title_key),
    ].sort();

    expect(normativeTitleKeys).toHaveLength(91);
    expect(Object.keys(routeTitleCatalogs.en).sort()).toEqual(allTitleKeys);
    expect(Object.keys(routeTitleCatalogs.ru).sort()).toEqual(allTitleKeys);
    expect(Object.values(routeTitleCatalogs.en).every((title) => title.trim().length > 0)).toBe(true);
    expect(Object.values(routeTitleCatalogs.ru).every((title) => title.trim().length > 0)).toBe(true);
  });
});
