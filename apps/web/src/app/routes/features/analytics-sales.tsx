import type { FeatureRouteProps } from "../feature-route-contract";
import { SalesOverview } from "../../../features/analytics-sales/SalesOverview";

export function AnalyticsSalesRoute({ resolution }: FeatureRouteProps): React.JSX.Element {
  return <SalesOverview workspaceKey={resolution.workspaceKey ?? "northwind-retail"} />;
}
