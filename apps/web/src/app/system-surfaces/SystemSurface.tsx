import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";

import type { SystemSurfaceKind } from "../router/route-resolution";

interface SystemSurfaceProps {
  readonly kind: SystemSurfaceKind;
  readonly stableCode?: string;
  readonly workspaceKey?: string;
  readonly fixture?: boolean;
}

const surfaceIds: Readonly<Record<SystemSurfaceKind, string>> = {
  forbidden: "UI-SYS-001",
  "not-found": "UI-SYS-002",
  "session-expired": "UI-SYS-003",
  maintenance: "UI-SYS-004",
  "upgrade-required": "UI-SYS-005",
};

export function SystemSurface({
  kind,
  stableCode,
  workspaceKey = "northwind-retail",
  fixture = false,
}: SystemSurfaceProps): React.JSX.Element {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const overviewHref = `/w/${workspaceKey}/overview`;

  useEffect(() => {
    if (kind !== "session-expired") return;
    for (const key of Object.keys(window.sessionStorage)) {
      if (key.startsWith("custometry-protected-presentation:")) {
        window.sessionStorage.removeItem(key);
      }
    }
  }, [kind]);

  return (
    <section
      className={`system-surface system-surface--${kind}`}
      aria-labelledby="system-surface-title"
      data-system-surface={surfaceIds[kind]}
    >
      <div className="system-surface__signal" aria-hidden="true" />
      <div className="system-surface__body">
        <p className="eyebrow">{surfaceIds[kind]} · {t(`system.${kind}.eyebrow`)}</p>
        <h1 id="system-surface-title" tabIndex={-1}>{t(`system.${kind}.title`)}</h1>
        <p>{t(`system.${kind}.description`)}</p>
        {fixture && <p className="fixture-disclosure" role="note">{t("system.fixtureDisclosure")}</p>}

        {kind === "maintenance" && (
          <dl className="system-details">
            <div><dt>{t("system.maintenance.scopeLabel")}</dt><dd>{t("system.maintenance.scope")}</dd></div>
            <div><dt>{t("system.maintenance.lastUpdateLabel")}</dt><dd>2026-08-24 14:20 UTC</dd></div>
            <div><dt>{t("system.maintenance.nextReviewLabel")}</dt><dd>2026-08-24 14:35 UTC</dd></div>
          </dl>
        )}

        {kind === "upgrade-required" && (
          <dl className="system-details">
            <div><dt>{t("system.upgrade-required.currentLabel")}</dt><dd>web-contract/1</dd></div>
            <div><dt>{t("system.upgrade-required.requiredLabel")}</dt><dd>web-contract/2</dd></div>
          </dl>
        )}

        <p className="support-code"><span>{t("system.supportCode")}</span><code>{stableCode ?? `W31-${surfaceIds[kind]}`}</code></p>

        <div className="system-actions">
          {(kind === "forbidden" || kind === "not-found") && (
            <button className="secondary-button" type="button" onClick={() => navigate(-1)}>{t("system.back")}</button>
          )}
          {kind === "session-expired" && <Link className="primary-button" to="/auth/sign-in">{t("system.signIn")}</Link>}
          {kind === "maintenance" && (
            <button className="secondary-button" type="button" onClick={() => window.location.reload()}>{t("system.refreshStatus")}</button>
          )}
          <Link className="secondary-button" to={overviewHref}>{t("system.allowedOverview")}</Link>
          {(kind === "maintenance" || kind === "upgrade-required") && (
            <Link className="secondary-button" to="/help">{t("system.openRunbook")}</Link>
          )}
        </div>
      </div>
    </section>
  );
}
