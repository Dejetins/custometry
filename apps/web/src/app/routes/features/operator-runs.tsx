import type { FeatureRouteProps } from "../feature-route-contract";
import { OperatorRuns } from "../../../features/operator-runs/OperatorRuns";

export function OperatorRunsRoute({ resolution }: FeatureRouteProps): React.JSX.Element {
  return <OperatorRuns workspaceKey={resolution.workspaceKey ?? "northwind-retail"} />;
}
