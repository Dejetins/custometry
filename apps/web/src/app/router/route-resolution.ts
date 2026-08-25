import { matchPath } from "react-router-dom";

import {
  routeRegistry,
  type RouteDefinition,
} from "@custometry/contracts";

import routeContractsDocument from "../../../../../packages/contracts/routes/ui-route-contracts.json";

export type ApplicationShellProfile =
  | "auth"
  | "global"
  | "installation"
  | "setup"
  | "workspace"
  | "focus"
  | "system";

export type SystemSurfaceKind =
  | "forbidden"
  | "not-found"
  | "session-expired"
  | "maintenance"
  | "upgrade-required";

interface AuthorizationContract {
  readonly mode: string;
  readonly entry_permissions_any: readonly string[];
  readonly action_permissions: readonly string[];
  readonly object_scoped: boolean;
}

export interface ExecutableRouteContract {
  readonly id: string;
  readonly path: string;
  readonly title_key: string;
  readonly family: string;
  readonly shell_profile: "auth" | "global" | "installation" | "setup" | "workspace";
  readonly navigation_group: string;
  readonly authorization: AuthorizationContract;
  readonly guard_profile: string;
  readonly state_profile: string;
  readonly navigation_profile: string;
  readonly query_profile: string;
  readonly focus_explore: string;
}

interface QueryProfile {
  readonly allowed_keys: readonly string[];
}

interface RouteContractsDocument {
  readonly schema_version: string;
  readonly routes: readonly ExecutableRouteContract[];
  readonly profiles: {
    readonly queries: Readonly<Record<string, QueryProfile>>;
  };
}

const routeContracts = routeContractsDocument as RouteContractsDocument;

export interface ResolvedApplicationRoute {
  readonly kind: "route";
  readonly route: RouteDefinition;
  readonly contract: ExecutableRouteContract;
  readonly shellProfile: ApplicationShellProfile;
  readonly workspaceKey?: string;
  readonly query: URLSearchParams;
  readonly compatibilityView?: "linear-spike" | "html-prototype";
  readonly systemFixture?: Exclude<SystemSurfaceKind, "not-found">;
}

export interface ResolvedFoundationRoute {
  readonly kind: "foundation";
  readonly shellProfile: "global";
  readonly query: URLSearchParams;
}

export interface UnresolvedApplicationRoute {
  readonly kind: "system";
  readonly shellProfile: "system";
  readonly systemSurface: "not-found";
  readonly stableCode: "SYS-404-PATH" | "SYS-404-QUERY";
  readonly query: URLSearchParams;
}

export type ApplicationRouteResolution =
  | ResolvedApplicationRoute
  | ResolvedFoundationRoute
  | UnresolvedApplicationRoute;

const compatibilityViews = new Set(["linear-spike", "html-prototype"]);
const systemFixtures = new Map<string, Exclude<SystemSurfaceKind, "not-found">>([
  ["w31-forbidden", "forbidden"],
  ["w31-session-expired", "session-expired"],
  ["w31-maintenance", "maintenance"],
  ["w31-upgrade-required", "upgrade-required"],
]);

function matchIdentityRoute(pathname: string): {
  readonly route: RouteDefinition;
  readonly workspaceKey?: string;
} | undefined {
  for (const route of routeRegistry.routes) {
    const match = matchPath({ path: route.path, end: true }, pathname);
    if (match) return { route, workspaceKey: match.params.workspaceKey };
  }
  return undefined;
}

function executableContract(routeId: string): ExecutableRouteContract {
  const contract = routeContracts.routes.find((candidate) => candidate.id === routeId);
  if (!contract) throw new Error(`Executable route contract missing for ${routeId}`);
  return contract;
}

function queryIsAllowed(contract: ExecutableRouteContract, query: URLSearchParams): boolean {
  const profile = routeContracts.profiles.queries[contract.query_profile];
  if (!profile) throw new Error(`Query profile missing for ${contract.id}`);
  return [...query.keys()].every((key) => profile.allowed_keys.includes(key));
}

function shellProfileFor(
  contract: ExecutableRouteContract,
  query: URLSearchParams,
): ApplicationShellProfile {
  if (query.has("focus") && contract.focus_explore !== "not_applicable") return "focus";
  if (contract.id === "UI-AUTH-002" || contract.id === "UI-AUTH-005") return "setup";
  return contract.shell_profile;
}

export function resolveApplicationRoute(
  pathname: string,
  search = "",
): ApplicationRouteResolution {
  const query = new URLSearchParams(search);
  if (pathname === "/") return { kind: "foundation", shellProfile: "global", query };

  const identity = matchIdentityRoute(pathname);
  if (!identity) {
    return { kind: "system", shellProfile: "system", systemSurface: "not-found", stableCode: "SYS-404-PATH", query };
  }

  const contract = executableContract(identity.route.id);
  if (!queryIsAllowed(contract, query)) {
    return { kind: "system", shellProfile: "system", systemSurface: "not-found", stableCode: "SYS-404-QUERY", query };
  }

  const view = query.get("view");
  const compatibilityView = view && compatibilityViews.has(view)
    ? (view as ResolvedApplicationRoute["compatibilityView"])
    : undefined;
  const systemFixture = import.meta.env.DEV && view ? systemFixtures.get(view) : undefined;

  return {
    kind: "route",
    route: identity.route,
    contract,
    shellProfile: systemFixture ? "system" : shellProfileFor(contract, query),
    workspaceKey: identity.workspaceKey,
    query,
    compatibilityView,
    systemFixture,
  };
}

export function routeContractSchemaVersion(): string {
  return routeContracts.schema_version;
}
