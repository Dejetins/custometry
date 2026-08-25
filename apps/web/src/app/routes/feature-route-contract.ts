import type { ComponentType } from "react";

import type { ResolvedApplicationRoute } from "../router/route-resolution";

export interface FeatureRouteProps {
  readonly resolution: ResolvedApplicationRoute;
}

/**
 * A feature slice registers itself by adding
 * `apps/web/src/features/<slice>/<UI-ID>.feature-route.tsx`.
 * The shell discovers that file lazily; no central registry edit is required.
 */
export interface FeatureRouteModule {
  readonly routeId: string;
  readonly default: ComponentType<FeatureRouteProps>;
}

export type FeatureRouteImport = () => Promise<FeatureRouteModule>;
export type FeatureRouteImportMap = Readonly<Record<string, FeatureRouteImport>>;
