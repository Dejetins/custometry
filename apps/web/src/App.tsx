import {
  Activity,
  BarChart3,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  CircleHelp,
  Database,
  FileChartColumn,
  LayoutDashboard,
  Ellipsis,
  Network,
  Search,
  Settings,
  ShieldCheck,
  Sparkles,
  Tags,
  TrendingUp,
  X,
} from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, matchPath, useLocation } from "react-router-dom";

import { routeRegistry, type RouteDefinition } from "@custometry/contracts";

import { ArchitectureSpike } from "./architecture-spike/ArchitectureSpike";

const workspaceKey = "northwind-retail";

const navigation = [
  { labelKey: "navOverview", path: `/w/${workspaceKey}/overview`, icon: LayoutDashboard },
  { labelKey: "navDataFoundation", path: `/w/${workspaceKey}/connections`, icon: Database },
  { labelKey: "navAnalytics", path: `/w/${workspaceKey}/analytics/sales`, icon: BarChart3 },
  { labelKey: "navForecasting", path: `/w/${workspaceKey}/forecasts`, icon: TrendingUp },
  { labelKey: "navPromotions", path: `/w/${workspaceKey}/promotions`, icon: Tags },
  { labelKey: "navDashboards", path: `/w/${workspaceKey}/dashboards`, icon: FileChartColumn },
  { labelKey: "navPipelines", path: `/w/${workspaceKey}/pipelines`, icon: Network },
  { labelKey: "navOperations", path: `/w/${workspaceKey}/runs`, icon: Activity },
  { labelKey: "navAdministration", path: "/admin", icon: Settings },
] as const;

interface ApiStatus {
  readonly label: "checking" | "ready" | "unavailable";
  readonly version?: string;
}

function canonicalToRuntimePath(path: string): string {
  return path.replace(":workspaceKey", workspaceKey);
}

function findRoute(pathname: string): RouteDefinition | undefined {
  return routeRegistry.routes.find((route) =>
    matchPath({ path: canonicalToRuntimePath(route.path), end: true }, pathname),
  );
}

function FoundationHome(): React.JSX.Element {
  const { t } = useTranslation();
  return (
    <section className="hero-card" aria-labelledby="foundation-title">
      <span className="badge"><Sparkles aria-hidden="true" size={15} />{t("foundationBadge")}</span>
      <h1 id="foundation-title">{t("foundationTitle")}</h1>
      <p>{t("foundationDescription")}</p>
      <div className="hero-actions">
        <a className="primary-button" href="/docs/">
          <BookOpen aria-hidden="true" size={17} />
          {t("openDocumentation")}
        </a>
        <Link className="secondary-button" to="/help">
          <CircleHelp aria-hidden="true" size={17} />
          {t("help")}
        </Link>
      </div>
      <div className="foundation-grid" aria-label={t("foundationCapabilities")}>
        <article><ShieldCheck aria-hidden="true" /><strong>{t("localFirst")}</strong><span>{t("localFirstDescription")}</span></article>
        <article><Database aria-hidden="true" /><strong>{t("realBoundaries")}</strong><span>{t("realBoundariesDescription")}</span></article>
        <article><BookOpen aria-hidden="true" /><strong>{t("shippedGuidance")}</strong><span>{t("shippedGuidanceDescription")}</span></article>
      </div>
    </section>
  );
}

interface HelpIndexDocument {
  readonly path: string;
  readonly title: string;
  readonly visibility: "public" | "authenticated";
  readonly locale?: string;
}

interface HelpIndex {
  readonly documents: readonly HelpIndexDocument[];
}

function helpDocumentHref(path: string): string {
  const relative = path.replace(/^docs\//, "").replace(/\.md$/, "");
  if (relative === "index") return "/docs/";
  return `/docs/${relative.replace(/\/index$/, "")}/`;
}

function HelpSurface(): React.JSX.Element {
  const { t } = useTranslation();
  const [documents, setDocuments] = useState<readonly HelpIndexDocument[]>([]);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    void fetch("/help-index.json", { signal: controller.signal, headers: { Accept: "application/json" } })
      .then(async (response) => {
        if (!response.ok) throw new Error("help index unavailable");
        const index = (await response.json()) as HelpIndex;
        setDocuments(index.documents.filter((document) => document.visibility === "public"));
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === "AbortError") return;
        setFailed(true);
      });
    return () => controller.abort();
  }, []);

  return (
    <section className="content-card" aria-labelledby="help-title">
      <span className="eyebrow">UI-HELP-001 · Foundation</span>
      <h1 id="help-title">{t("helpTitle")}</h1>
      <p>{t("helpDescription")}</p>
      <a className="primary-button" href="/docs/">{t("openDocumentation")}</a>
      {failed && <p role="status">{t("helpIndexUnavailable")}</p>}
      {documents.length > 0 && (
        <ul className="help-links" aria-label={t("publicHelpArticles")}>
          {documents.map((document) => (
            <li key={`${document.locale ?? "unknown"}:${document.path}`}>
              <a href={helpDocumentHref(document.path)}>{document.title}</a>
              {document.locale && <span>{document.locale.toUpperCase()}</span>}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function PlannedSurface({
  route,
  spikeHref,
}: {
  readonly route: RouteDefinition;
  readonly spikeHref?: string;
}): React.JSX.Element {
  const { t } = useTranslation();
  const title = t(route.title_key, { ns: "routeTitles" });
  return (
    <section className="content-card" aria-labelledby="planned-title">
      <div className="surface-heading">
        <div>
          <span className="eyebrow">{route.id} · {route.release}</span>
          <h1 id="planned-title">{title}</h1>
        </div>
        <span className="planned-badge">{t("plannedSurface")}</span>
      </div>
      <p>{t("plannedSurfaceDescription")}</p>
      {spikeHref && (
        <Link className="primary-button" data-testid="open-architecture-spike" to={spikeHref}>
          Open frontend architecture spike
        </Link>
      )}
      <dl className="route-contract">
        <div><dt>{t("canonicalRoute")}</dt><dd>{route.path}</dd></div>
        <div><dt>{t("lifecycle")}</dt><dd>{route.status}</dd></div>
      </dl>
    </section>
  );
}

function NotFound(): React.JSX.Element {
  const { t } = useTranslation();
  return (
    <section className="content-card" aria-labelledby="not-found-title">
      <span className="eyebrow">UI-SYS-002</span>
      <h1 id="not-found-title">{t("notFoundTitle")}</h1>
      <p>{t("notFoundDescription")}</p>
      <Link className="secondary-button" to="/">{t("returnToFoundation")}</Link>
    </section>
  );
}

export function App(): React.JSX.Element {
  const location = useLocation();
  const { i18n, t } = useTranslation();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [apiStatus, setApiStatus] = useState<ApiStatus>({ label: "checking" });
  const mobileMenuRef = useRef<HTMLDialogElement>(null);
  const route = useMemo(() => findRoute(location.pathname), [location.pathname]);
  const architectureSpikeActive =
    route?.id === "UI-AN-003" && new URLSearchParams(location.search).get("view") === "linear-spike";

  useEffect(() => {
    const controller = new AbortController();
    void fetch("/api/health/ready", { signal: controller.signal, headers: { Accept: "application/json" } })
      .then(async (response) => {
        if (!response.ok) throw new Error("not ready");
        const payload = (await response.json()) as { version?: string };
        setApiStatus({ label: "ready", version: payload.version });
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === "AbortError") return;
        setApiStatus({ label: "unavailable" });
      });
    return () => controller.abort();
  }, []);

  const switchLanguage = (): void => {
    const nextLanguage = i18n.language === "ru" ? "en" : "ru";
    window.localStorage.setItem("custometry-language", nextLanguage);
    void i18n.changeLanguage(nextLanguage);
  };

  const openMobileMenu = (): void => {
    const dialog = mobileMenuRef.current;
    setMobileMenuOpen(true);
    if (!dialog) return;
    if (!dialog.open) {
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    }
  };

  const closeMobileMenu = (): void => {
    const dialog = mobileMenuRef.current;
    setMobileMenuOpen(false);
    if (!dialog) return;
    if (dialog.open && typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
  };

  useEffect(() => {
    closeMobileMenu();
  }, [location.pathname]);

  if (architectureSpikeActive) {
    return <ArchitectureSpike fallbackHref={location.pathname} />;
  }

  let content: React.JSX.Element;
  if (location.pathname === "/") content = <FoundationHome />;
  else if (location.pathname === "/help") content = <HelpSurface />;
  else if (route) {
    const spikeHref = route.id === "UI-AN-003"
      ? `${location.pathname}?view=linear-spike`
      : undefined;
    content = <PlannedSurface route={route} spikeHref={spikeHref} />;
  }
  else content = <NotFound />;

  return (
    <div className={sidebarOpen ? "app-shell" : "app-shell sidebar-collapsed"}>
      <aside className="sidebar" aria-label={t("navigation")}>
        <Link to="/" className="brand" aria-label="Custometry Foundation">
          <span className="brand-mark">C</span>
          {sidebarOpen && <span>{t("brand")}</span>}
        </Link>
        {sidebarOpen && <span className="workspace-label">{t("workspace")}</span>}
        <nav>
          {navigation.map(({ labelKey, path, icon: Icon }) => {
            const label = t(labelKey);
            return (
            <Link key={path} to={path} className={location.pathname === path ? "nav-item active" : "nav-item"} title={label} aria-label={!sidebarOpen ? label : undefined}>
              <Icon aria-hidden="true" size={18} />
              {sidebarOpen && <span>{label}</span>}
            </Link>
          );})}
          <button
            className="mobile-more-button"
            type="button"
            aria-controls="mobile-navigation-menu"
            aria-expanded={mobileMenuOpen}
            aria-label={t("moreNavigation")}
            onClick={openMobileMenu}
          >
            <Ellipsis aria-hidden="true" size={20} />
          </button>
        </nav>
        <button className="sidebar-toggle" type="button" onClick={() => setSidebarOpen((open) => !open)} aria-label={sidebarOpen ? t("collapseNavigation") : t("expandNavigation")}>
          {sidebarOpen ? <ChevronLeft aria-hidden="true" /> : <ChevronRight aria-hidden="true" />}
          {sidebarOpen && <span>{t("collapseNavigation")}</span>}
        </button>
      </aside>
      <dialog
        className="mobile-nav-dialog"
        id="mobile-navigation-menu"
        ref={mobileMenuRef}
        aria-labelledby="mobile-navigation-title"
        onCancel={() => setMobileMenuOpen(false)}
        onClose={() => setMobileMenuOpen(false)}
      >
        <div className="mobile-menu-heading">
          <h2 id="mobile-navigation-title">{t("allSections")}</h2>
          <button type="button" onClick={closeMobileMenu} aria-label={t("closeMenu")}>
            <X aria-hidden="true" size={20} />
          </button>
        </div>
        <nav className="mobile-menu-list" aria-label={t("allSections")}>
          {navigation.map(({ labelKey, path, icon: Icon }) => {
            const label = t(labelKey);
            return (
              <Link
                key={path}
                to={path}
                className={location.pathname === path ? "mobile-menu-link active" : "mobile-menu-link"}
                onClick={closeMobileMenu}
              >
                <Icon aria-hidden="true" size={19} />
                <span>{label}</span>
              </Link>
            );
          })}
        </nav>
      </dialog>
      <header className="topbar">
        <Link to="/" className="mobile-brand" aria-label="Custometry Foundation">
          <span className="brand-mark">C</span>
        </Link>
        <button className="workspace-button" type="button">{t("workspace")}</button>
        <label className="search-control">
          <Search aria-hidden="true" size={17} />
          <span className="sr-only">{t("searchLabel")}</span>
          <input type="search" placeholder={t("searchPlaceholder")} disabled aria-describedby="search-status" />
        </label>
        <span className="sr-only" id="search-status">{t("searchPlanned")}</span>
        <span className={`api-status ${apiStatus.label}`} aria-live="polite">
          <span aria-hidden="true" />
          <span>{t("apiStatus")}: {t(`status${apiStatus.label[0].toUpperCase()}${apiStatus.label.slice(1)}`)}</span>
          {apiStatus.version && <span className="api-status-version">· {apiStatus.version}</span>}
        </span>
        <button className="language-button" type="button" onClick={switchLanguage}>{i18n.language === "ru" ? "EN" : "RU"}</button>
      </header>
      <main className="main-content" key={location.pathname}>{content}</main>
    </div>
  );
}
