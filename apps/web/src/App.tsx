import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";

import { ArchitectureSpike } from "./architecture-spike/ArchitectureSpike";
import {
  ApplicationShell,
  loadFeatureRoute,
  resolveApplicationRoute,
  routeContractSchemaVersion,
  SystemSurface,
  type FeatureRouteModule,
} from "./app/index";
import { FoundationHome, HelpSurface, PlannedSurface } from "./app/shell/CompatibilitySurfaces";
import { SalesOverviewPrototype } from "./sales-overview-prototype/SalesOverviewPrototype";

export function App(): React.JSX.Element {
  const location = useLocation();
  const { t } = useTranslation();
  const resolution = useMemo(
    () => resolveApplicationRoute(location.pathname, location.search),
    [location.pathname, location.search],
  );
  const [featureModule, setFeatureModule] = useState<FeatureRouteModule>();

  useEffect(() => {
    let active = true;
    setFeatureModule(undefined);
    if (resolution.kind !== "route") return () => { active = false; };
    void loadFeatureRoute(resolution.route.id).then((module) => {
      if (active) setFeatureModule(module);
    });
    return () => { active = false; };
  }, [resolution]);

  if (resolution.kind === "route" && resolution.compatibilityView === "html-prototype") {
    return <SalesOverviewPrototype />;
  }
  if (resolution.kind === "route" && resolution.compatibilityView === "linear-spike") {
    return <ArchitectureSpike fallbackHref={location.pathname} />;
  }

  let content: React.JSX.Element;
  let pageTitle = t("foundationTitle");
  let workspaceKey: string | undefined;

  if (resolution.kind === "foundation") {
    content = <FoundationHome />;
  } else if (resolution.kind === "system") {
    pageTitle = t("system.not-found.title");
    content = <SystemSurface kind="not-found" stableCode={resolution.stableCode} />;
  } else {
    workspaceKey = resolution.workspaceKey;
    pageTitle = t(resolution.route.title_key, { ns: "routeTitles" });
    if (resolution.systemFixture) {
      pageTitle = t(`system.${resolution.systemFixture}.title`);
      content = <SystemSurface kind={resolution.systemFixture} workspaceKey={workspaceKey} fixture />;
    } else if (featureModule) {
      const FeatureRoute = featureModule.default;
      content = <FeatureRoute resolution={resolution} />;
    } else if (resolution.route.id === "UI-HELP-001") {
      content = <HelpSurface />;
    } else {
      content = <PlannedSurface route={resolution.route} />;
    }
  }

  return (
    <ApplicationShell profile={resolution.shellProfile} pageTitle={pageTitle} workspaceKey={workspaceKey}>
      <span className="contract-version" aria-hidden="true">route-contract/{routeContractSchemaVersion()}</span>
      {content}
    </ApplicationShell>
  );
}
