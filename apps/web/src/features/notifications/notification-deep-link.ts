import type { NotificationDeepLink } from "./notification-api";

const SAFE_IDENTITY = /^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$/;

function exactParameters(
  value: Readonly<Record<string, string>>,
  expected: readonly string[],
): boolean {
  const keys = Object.keys(value).sort();
  return keys.length === expected.length
    && keys.every((key, index) => key === [...expected].sort()[index])
    && keys.every((key) => SAFE_IDENTITY.test(value[key]));
}

export function resolveNotificationDeepLink(
  link: NotificationDeepLink,
  workspaceKey: string,
): string | undefined {
  if (
    link.status !== "available"
    || !link.route_id
    || !link.parameters
    || !SAFE_IDENTITY.test(workspaceKey)
  ) return undefined;

  const parameters = link.parameters;
  if (link.route_id === "UI-OPS-001" && exactParameters(parameters, [])) {
    return `/w/${encodeURIComponent(workspaceKey)}/runs`;
  }
  if (link.route_id === "UI-OPS-002" && exactParameters(parameters, ["run_id"])) {
    return `/w/${encodeURIComponent(workspaceKey)}/runs/${encodeURIComponent(parameters.run_id)}`;
  }
  if (
    link.route_id === "UI-OPS-003"
    && exactParameters(parameters, ["run_id", "node_id", "attempt_id"])
  ) {
    return `/w/${encodeURIComponent(workspaceKey)}/runs/${encodeURIComponent(parameters.run_id)}`
      + `/nodes/${encodeURIComponent(parameters.node_id)}`
      + `/attempts/${encodeURIComponent(parameters.attempt_id)}`;
  }
  return undefined;
}
