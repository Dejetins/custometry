import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";
import { BookOpen, CheckCircle2, Circle, CircleAlert, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import { InstallationFrame, InstallationPanel, InstallationButton, InstallationLink, InstallationStatusMark } from "@custometry/ui-foundation";
import { readInstallationStatus } from "./status";

const Header = styled.header`
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
  gap: 16px; padding: 12px 18px; border-radius: 15px; background: var(--entry-surface);
  & strong { font-size: 12px; letter-spacing: .07em; }
  & label { display: flex; gap: 8px; align-items: center; color: var(--entry-secondary); }
  & select { min-height: 32px; padding: 4px 9px; border: 1px solid var(--entry-border); border-radius: 7px; background: var(--entry-module); color: var(--entry-text); }
`;
const Main = styled.main`
  width: min(100%, 720px); margin: 40px auto; display: grid; gap: 16px;
  & .entry-heading { display: grid; gap: 8px; padding-inline: 4px; }
  & .entry-summary { display: flex; gap: 10px; align-items: baseline; }
  & .entry-details { display: grid; gap: 16px; margin: 24px 0; }
  & .entry-details > div { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px 20px; }
  & dt { color: var(--entry-secondary); }
  & dd { margin: 0; overflow-wrap: anywhere; min-width: 0; }
  & .entry-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  & .entry-note { display: grid; gap: 8px; }
  & .entry-meta { padding: 4px; margin: 0; }
  @media (max-width: 480px) { margin-block: 24px; }
`;

function Entry(): React.JSX.Element {
  const { t, i18n } = useTranslation();
  const [manualCheck, setManualCheck] = useState(false);
  const query = useQuery({
    queryKey: ["installation-status"], queryFn: ({ signal }) => readInstallationStatus(signal),
    retry: false, refetchInterval: 10000, refetchOnWindowFocus: true, staleTime: 0,
    gcTime: 0, networkMode: "always",
  });
  // React Query retains data after refetch errors. Never render it as current truth.
  const checking = query.isPending || (manualCheck && query.isFetching);
  const status = query.isError || checking ? undefined : query.data;
  const state = checking ? "checking" : query.isError ? "unavailable" : status?.state === "ready_for_bootstrap" ? "ready" : "notReady";
  const [announcement, setAnnouncement] = useState("");
  useEffect(() => { setAnnouncement(t(`installation.${state}`)); }, [state, t]);
  useEffect(() => { document.documentElement.lang = i18n.resolvedLanguage ?? "en"; document.title = `Custometry — ${t("installation.title")}`; }, [i18n.resolvedLanguage, t]);
  const componentKeys = ["database", "schema", "storage"] as const;
  return <InstallationFrame>
    <a className="entry-skip" href="#installation-main">{t("installation.skip")}</a>
    <Header><strong>Custometry</strong><label htmlFor="installation-language">{t("installation.language")}<select id="installation-language" value={i18n.resolvedLanguage} onChange={event => { void i18n.changeLanguage(event.target.value); window.localStorage.setItem("custometry-language", event.target.value); }}><option value="en">English</option><option value="ru">Русский</option></select></label></Header>
    <Main id="installation-main" tabIndex={-1}>
      <div className="entry-heading"><h1>{t("installation.title")}</h1><p className="entry-secondary">{t("installation.intro")}</p></div>
      <InstallationPanel aria-labelledby="installation-status-title">
        <div className="entry-summary"><InstallationStatusMark $state={status?.state === "ready_for_bootstrap" ? "ready" : status ? "not_ready" : "unknown"}>{status?.state === "ready_for_bootstrap" ? <CheckCircle2 aria-hidden="true" /> : status || query.isError ? <CircleAlert aria-hidden="true" /> : <Circle aria-hidden="true" />}</InstallationStatusMark><h2 id="installation-status-title" role="status" aria-live="polite" aria-atomic="true">{announcement}</h2></div>
        <dl className="entry-details">{componentKeys.map(key => {
          const component = status?.components[key] ?? "unknown";
          return <div key={key}><dt>{t(`installation.components.${key}`)}</dt><dd><InstallationStatusMark $state={component}>{component === "ready" ? <CheckCircle2 aria-hidden="true" /> : component === "not_ready" ? <CircleAlert aria-hidden="true" /> : <Circle aria-hidden="true" />}{t(`installation.componentState.${component}`)}</InstallationStatusMark></dd></div>;
        })}</dl>
        <p className="entry-secondary">{t(`installation.description.${state}`)}</p>
        <div className="entry-actions" style={{ marginBlockStart: 20 }}><InstallationButton type="button" aria-disabled={query.isFetching} onClick={() => { if (!query.isFetching) { setManualCheck(true); void query.refetch().finally(() => setManualCheck(false)); } }}><RefreshCw aria-hidden="true" />{t("installation.retry")}</InstallationButton><InstallationLink href={t("installation.helpHref")}><BookOpen aria-hidden="true" />{t("installation.help")}</InstallationLink></div>
      </InstallationPanel>
      <InstallationPanel className="entry-note"><h2>{t("installation.nextTitle")}</h2><p className="entry-secondary">{t("installation.nextDescription")}</p></InstallationPanel>
      <dl className="entry-details entry-meta"><div><dt>{t("installation.version")}</dt><dd>{status?.version ?? t("installation.unknown")}</dd></div><div><dt>{t("installation.address")}</dt><dd>{window.location.origin}</dd></div></dl>
    </Main>
  </InstallationFrame>;
}
export function InstallationEntry(): React.JSX.Element {
  const [client] = useState(() => new QueryClient());
  return <QueryClientProvider client={client}><Entry /></QueryClientProvider>;
}
