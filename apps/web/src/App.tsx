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
import { HelpSurface, PlannedSurface } from "./app/shell/CompatibilitySurfaces";
import { InstallationEntry } from "./features/installation/InstallationEntry";
import { SalesOverviewPrototype } from "./sales-overview-prototype/SalesOverviewPrototype";

export function App(): React.JSX.Element {
  const location = useLocation();
  const { t } = useTranslation();
  const resolution = useMemo(
    () => resolveApplicationRoute(location.pathname, location.search),
    [location.pathname, location.search],
  );
  const [featureModule, setFeatureModule] = useState<FeatureRouteModule>();
  const featureId = resolution.kind === "route" ? resolution.route.id : undefined;

  useEffect(() => {
    let active = true;
    setFeatureModule(undefined);
    if (resolution.kind !== "route") return () => { active = false; };
    void loadFeatureRoute(resolution.route.id).then((module) => {
      if (active) setFeatureModule(module);
    });
    return () => { active = false; };
  }, [featureId]);

  if (resolution.kind === "route" && resolution.compatibilityView === "html-prototype") {
    return <SalesOverviewPrototype />;
  }
  if (resolution.kind === "route" && resolution.compatibilityView === "linear-spike") {
    return <ArchitectureSpike fallbackHref={location.pathname} />;
  }

  if (resolution.kind === "route" && (resolution.route.id.startsWith("UI-RPT-") || resolution.route.id === "UI-AUTH-001") && featureModule?.routeId !== resolution.route.id) {
    return <main aria-busy="true"><p role="status">{t("statusChecking")}</p></main>;
  }

  let content: React.JSX.Element;
  let pageTitle = t("foundationTitle");
  let workspaceKey: string | undefined;

  if (resolution.kind === "foundation") {
    return <InstallationEntry />;
  } else if (resolution.kind === "system") {
    pageTitle = t("system.not-found.title");
    content = <SystemSurface kind="not-found" stableCode={resolution.stableCode} />;
  } else {
    workspaceKey = resolution.workspaceKey;
    pageTitle = t(resolution.route.title_key, { ns: "routeTitles" });
    if (resolution.systemFixture) {
      pageTitle = t(`system.${resolution.systemFixture}.title`);
      content = <SystemSurface kind={resolution.systemFixture} workspaceKey={workspaceKey} fixture />;
    } else if (featureModule?.routeId === resolution.route.id) {
      const FeatureRoute = featureModule.default;
      content = <FeatureRoute resolution={resolution} />;
    } else if (resolution.route.id === "UI-HELP-001") {
      content = <HelpSurface />;
    } else {
      content = <PlannedSurface route={resolution.route} />;
    }
  }

  if (resolution.kind === "route" && (resolution.route.id.startsWith("UI-RPT-") || resolution.route.id === "UI-AUTH-001") && featureModule) return content;

  return (
    <ApplicationShell profile={resolution.shellProfile} pageTitle={pageTitle} workspaceKey={workspaceKey}>
      <span className="contract-version" aria-hidden="true">route-contract/{routeContractSchemaVersion()}</span>
      {content}
    </ApplicationShell>
  );
}
