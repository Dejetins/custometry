import type { FeatureRouteProps } from "../feature-route-contract";
import { NotificationInbox } from "../../../features/notifications/NotificationInbox";

export function NotificationsRoute({ resolution }: FeatureRouteProps): React.JSX.Element {
  return <NotificationInbox workspaceKey={resolution.workspaceKey ?? "northwind-retail"} />;
}
