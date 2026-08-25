import type {
  FeatureRouteImportMap,
  FeatureRouteModule,
} from "./feature-route-contract";

const discoveredFeatureRoutes = import.meta.glob<FeatureRouteModule>(
  "../../features/**/*.feature-route.tsx",
);

function expectedSuffix(routeId: string): string {
  return `/${routeId}.feature-route.tsx`;
}

export async function loadFeatureRoute(
  routeId: string,
  imports: FeatureRouteImportMap = discoveredFeatureRoutes,
): Promise<FeatureRouteModule | undefined> {
  const matches = Object.entries(imports).filter(([path]) =>
    path.endsWith(expectedSuffix(routeId)),
  );

  if (matches.length === 0) return undefined;
  if (matches.length > 1) {
    throw new Error(`Duplicate feature route modules for ${routeId}`);
  }

  const module = await matches[0][1]();
  if (module.routeId !== routeId) {
    throw new Error(
      `Feature route module ${matches[0][0]} declares ${module.routeId}; expected ${routeId}`,
    );
  }
  return module;
}
