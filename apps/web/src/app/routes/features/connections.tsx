import type { FeatureRouteProps } from "../feature-route-contract";
import { ConnectionEditor, ConnectionsList } from "../../../features/connections/Connections";
import { ConnectionPresentationFixture } from "../../../features/connections/connection-fixtures";

function adapterFor(view: string | null): { readonly api?: ConnectionPresentationFixture; readonly fixture: boolean } {
  if (!import.meta.env.DEV || !view?.startsWith("w33-")) return { fixture: false };
  return { api: new ConnectionPresentationFixture(view), fixture: true };
}

export function ConnectionsRoute({ resolution }: FeatureRouteProps): React.JSX.Element {
  const selected = adapterFor(resolution.query.get("view"));
  return <ConnectionsList workspaceKey={resolution.workspaceKey ?? "northwind-retail"} api={selected.api} fixture={selected.fixture} />;
}

export function ConnectionEditorRoute({ resolution }: FeatureRouteProps): React.JSX.Element {
  const selected = adapterFor(resolution.query.get("view"));
  return <ConnectionEditor workspaceKey={resolution.workspaceKey ?? "northwind-retail"} api={selected.api} fixture={selected.fixture} />;
}
