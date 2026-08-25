import {
  Activity,
  BarChart3,
  ChevronLeft,
  ChevronRight,
  CircleHelp,
  Database,
  Ellipsis,
  FileChartColumn,
  LayoutDashboard,
  Network,
  Search,
  Settings,
  Tags,
  TrendingUp,
  X,
} from "lucide-react";
import { useEffect, useRef, useState, type PropsWithChildren } from "react";
import { useTranslation } from "react-i18next";
import { Link, NavLink, useLocation, useNavigationType } from "react-router-dom";

import { defaultUiThemeId, SemanticThemeBoundary } from "@custometry/ui-foundation";

import type { ApplicationShellProfile } from "../router/route-resolution";

const defaultWorkspaceKey = "northwind-retail";
const focusMemory = new Map<string, { readonly key?: string; readonly scrollY: number }>();

const navigation = [
  { labelKey: "navOverview", suffix: "overview", icon: LayoutDashboard },
  { labelKey: "navDataFoundation", suffix: "connections", icon: Database },
  { labelKey: "navAnalytics", suffix: "analytics/sales", icon: BarChart3 },
  { labelKey: "navForecasting", suffix: "forecasts", icon: TrendingUp },
  { labelKey: "navPromotions", suffix: "promotions", icon: Tags },
  { labelKey: "navDashboards", suffix: "dashboards", icon: FileChartColumn },
  { labelKey: "navPipelines", suffix: "pipelines", icon: Network },
  { labelKey: "navOperations", suffix: "runs", icon: Activity },
] as const;

interface ApiStatus {
  readonly label: "checking" | "ready" | "unavailable";
  readonly version?: string;
}

interface ApplicationShellProps extends PropsWithChildren {
  readonly profile: ApplicationShellProfile;
  readonly pageTitle: string;
  readonly workspaceKey?: string;
}

function memoryKey(key: string, pathname: string, search: string): string {
  return key === "default" ? `${pathname}${search}` : key;
}

export function ApplicationShell({
  children,
  profile,
  pageTitle,
  workspaceKey = defaultWorkspaceKey,
}: ApplicationShellProps): React.JSX.Element {
  const { i18n, t } = useTranslation();
  const location = useLocation();
  const navigationType = useNavigationType();
  const [sidebarOpen, setSidebarOpen] = useState(() => window.localStorage.getItem("custometry-shell-sidebar") !== "collapsed");
  const [allSectionsOpen, setAllSectionsOpen] = useState(false);
  const [apiStatus, setApiStatus] = useState<ApiStatus>({ label: "checking" });
  const allSectionsRef = useRef<HTMLDialogElement>(null);
  const firstRender = useRef(true);
  const currentMemoryKey = memoryKey(location.key, location.pathname, location.search);
  const showWorkspaceChrome = !["auth", "setup"].includes(profile);

  useEffect(() => {
    document.title = `${pageTitle} · Custometry`;
    document.documentElement.lang = i18n.resolvedLanguage === "ru" ? "ru" : "en";
  }, [i18n.resolvedLanguage, pageTitle]);

  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return undefined;
    }
    const frame = window.requestAnimationFrame(() => {
      if (navigationType === "POP") {
        const prior = focusMemory.get(currentMemoryKey);
        if (prior?.key) {
          document.querySelector<HTMLElement>(`[data-focus-key="${CSS.escape(prior.key)}"]`)?.focus();
        } else {
          document.querySelector<HTMLElement>("main h1")?.focus();
        }
        window.scrollTo({ top: prior?.scrollY ?? 0, behavior: "instant" });
      } else {
        document.querySelector<HTMLElement>("main h1")?.focus();
        window.scrollTo({ top: 0, behavior: "instant" });
      }
    });
    return () => window.cancelAnimationFrame(frame);
  }, [currentMemoryKey, navigationType]);

  useEffect(() => () => {
    const active = document.activeElement as HTMLElement | null;
    focusMemory.set(currentMemoryKey, { key: active?.dataset.focusKey, scrollY: window.scrollY });
  }, [currentMemoryKey]);

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

  const setSidebar = (open: boolean): void => {
    setSidebarOpen(open);
    window.localStorage.setItem("custometry-shell-sidebar", open ? "expanded" : "collapsed");
  };

  const switchLanguage = (): void => {
    const nextLanguage = i18n.resolvedLanguage === "ru" ? "en" : "ru";
    window.localStorage.setItem("custometry-language", nextLanguage);
    void i18n.changeLanguage(nextLanguage);
  };

  const openAllSections = (): void => {
    const dialog = allSectionsRef.current;
    setAllSectionsOpen(true);
    if (dialog && !dialog.open) {
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    }
  };

  const closeAllSections = (): void => {
    const dialog = allSectionsRef.current;
    setAllSectionsOpen(false);
    if (dialog?.open && typeof dialog.close === "function") dialog.close();
    else dialog?.removeAttribute("open");
  };

  return (
    <SemanticThemeBoundary themeId={defaultUiThemeId}>
      <a className="skip-link" href="#main-content">{t("skipToContent")}</a>
      <div className={`app-shell ${sidebarOpen ? "sidebar-expanded" : "sidebar-collapsed"}`} data-shell-profile={profile}>
        {showWorkspaceChrome && (
          <aside className="sidebar" aria-label={t("navigation")}>
            <Link to="/" className="brand" aria-label={t("brand")} data-focus-key="brand-home"><span className="brand-mark">C</span>{sidebarOpen && <span>{t("brand")}</span>}</Link>
            {sidebarOpen && <span className="workspace-label">{t("workspace")}</span>}
            <nav aria-label={t("primaryNavigation")}>
              {navigation.map(({ labelKey, suffix, icon: Icon }) => {
                const path = `/w/${workspaceKey}/${suffix}`;
                const label = t(labelKey);
                return (
                  <NavLink key={path} to={path} className={({ isActive }) => isActive ? "nav-item active" : "nav-item"} title={label} aria-label={!sidebarOpen ? label : undefined} data-focus-key={`nav-${suffix}`}>
                    <Icon aria-hidden="true" size={18} /><span className={sidebarOpen ? undefined : "sr-only"}>{label}</span>
                  </NavLink>
                );
              })}
              <NavLink to="/admin" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"} title={t("navAdministration")} aria-label={!sidebarOpen ? t("navAdministration") : undefined} data-focus-key="nav-administration">
                <Settings aria-hidden="true" size={18} /><span className={sidebarOpen ? undefined : "sr-only"}>{t("navAdministration")}</span>
              </NavLink>
              <button className="all-sections-button" type="button" aria-controls="all-sections-menu" aria-expanded={allSectionsOpen} aria-label={t("moreNavigation")} onClick={openAllSections} data-focus-key="all-sections">
                <Ellipsis aria-hidden="true" size={20} /><span className={sidebarOpen ? undefined : "sr-only"}>{t("moreNavigation")}</span>
              </button>
            </nav>
            <div className="sidebar-footer">
              <Link to="/help" className="nav-item" data-focus-key="nav-help"><CircleHelp aria-hidden="true" size={18} /><span className={sidebarOpen ? undefined : "sr-only"}>{t("help")}</span></Link>
              <button className="sidebar-toggle" type="button" onClick={() => setSidebar(!sidebarOpen)} aria-label={sidebarOpen ? t("collapseNavigation") : t("expandNavigation")} data-focus-key="sidebar-toggle">
                {sidebarOpen ? <ChevronLeft aria-hidden="true" /> : <ChevronRight aria-hidden="true" />}{sidebarOpen && <span>{t("collapseNavigation")}</span>}
              </button>
            </div>
          </aside>
        )}

        <dialog className="all-sections-dialog" id="all-sections-menu" ref={allSectionsRef} aria-labelledby="all-sections-title" onCancel={closeAllSections} onClose={() => setAllSectionsOpen(false)}>
          <header><h2 id="all-sections-title">{t("allSections")}</h2><button type="button" onClick={closeAllSections} aria-label={t("closeMenu")}><X aria-hidden="true" size={20} /></button></header>
          <nav aria-label={t("allSections")}>
            {[...navigation.map((item) => ({ ...item, path: `/w/${workspaceKey}/${item.suffix}` })), { labelKey: "navAdministration", path: "/admin", icon: Settings }].map(({ labelKey, path, icon: Icon }) => (
              <Link key={path} to={path} onClick={closeAllSections}><Icon aria-hidden="true" size={18} />{t(labelKey)}</Link>
            ))}
          </nav>
        </dialog>

        <header className="topbar">
          {!showWorkspaceChrome && <Link to="/" className="auth-brand" aria-label={t("brand")}><span className="brand-mark">C</span><strong>{t("brand")}</strong></Link>}
          {showWorkspaceChrome && <span className="workspace-context">{t("workspace")}</span>}
          {showWorkspaceChrome && (
            <label className="search-control"><Search aria-hidden="true" size={17} /><span className="sr-only">{t("searchLabel")}</span><input type="search" placeholder={t("searchPlaceholder")} disabled aria-describedby="search-status" /></label>
          )}
          <span className="sr-only" id="search-status">{t("searchPlanned")}</span>
          <span className={`api-status ${apiStatus.label}`} role="status"><span aria-hidden="true" /><span>{t("apiStatus")}: {t(`status${apiStatus.label[0].toUpperCase()}${apiStatus.label.slice(1)}`)}</span>{apiStatus.version && <span className="api-status-version">· {apiStatus.version}</span>}</span>
          <button className="language-button" type="button" onClick={switchLanguage} aria-label={t("switchLanguage")} data-focus-key="language-toggle">{i18n.resolvedLanguage === "ru" ? "EN" : "RU"}</button>
        </header>

        <main className="main-content" id="main-content" tabIndex={-1}>{children}</main>
      </div>
    </SemanticThemeBoundary>
  );
}
