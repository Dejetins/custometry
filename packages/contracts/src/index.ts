import routeRegistryDocument from "../routes/ui-routes.json";

export type RouteStatus = "foundation" | "planned" | "implemented";

export interface RouteDefinition {
  readonly id: string;
  readonly path: string;
  readonly title_key: string;
  readonly release: string;
  readonly status: RouteStatus;
}

export interface RouteRegistryDocument {
  readonly schema_version: string;
  readonly workspace_key_parameter: string;
  readonly routes: readonly RouteDefinition[];
  readonly foundation_utility_routes: readonly RouteDefinition[];
}

export const routeRegistry = routeRegistryDocument as RouteRegistryDocument;

export * from "./foundation-client";
export * from "./execution-control";

export * as salesReports from "./analytics-client";

export * as draftReports from "./reports-client";
export * as reportSales from "./sales-report-client";
export * as metricWorkspace from "./workspace-contracts";
export * as workspaceCalendar from "./workspace-calendar-client";
