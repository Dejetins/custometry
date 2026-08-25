import { BookOpen, CircleHelp, Database, ShieldCheck, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import type { RouteDefinition } from "@custometry/contracts";

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

export function FoundationHome(): React.JSX.Element {
  const { t } = useTranslation();
  return (
    <section className="hero-card" aria-labelledby="foundation-title">
      <span className="badge"><Sparkles aria-hidden="true" size={15} />{t("foundationBadge")}</span>
      <h1 id="foundation-title" tabIndex={-1}>{t("foundationTitle")}</h1>
      <p>{t("foundationDescription")}</p>
      <div className="hero-actions">
        <a className="primary-button" href="/docs/"><BookOpen aria-hidden="true" size={17} />{t("openDocumentation")}</a>
        <Link className="secondary-button" to="/help"><CircleHelp aria-hidden="true" size={17} />{t("help")}</Link>
      </div>
      <div className="foundation-grid" aria-label={t("foundationCapabilities")}>
        <article><ShieldCheck aria-hidden="true" /><strong>{t("localFirst")}</strong><span>{t("localFirstDescription")}</span></article>
        <article><Database aria-hidden="true" /><strong>{t("realBoundaries")}</strong><span>{t("realBoundariesDescription")}</span></article>
        <article><BookOpen aria-hidden="true" /><strong>{t("shippedGuidance")}</strong><span>{t("shippedGuidanceDescription")}</span></article>
      </div>
    </section>
  );
}

export function HelpSurface(): React.JSX.Element {
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
      <h1 id="help-title" tabIndex={-1}>{t("helpTitle")}</h1>
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

export function PlannedSurface({ route }: { readonly route: RouteDefinition }): React.JSX.Element {
  const { t } = useTranslation();
  const title = t(route.title_key, { ns: "routeTitles" });
  const spikeHref = route.id === "UI-AN-003" ? `${route.path.replace(":workspaceKey", "northwind-retail")}?view=linear-spike` : undefined;
  return (
    <section className="content-card" aria-labelledby="planned-title">
      <div className="surface-heading">
        <div><span className="eyebrow">{route.id} · {route.release}</span><h1 id="planned-title" tabIndex={-1}>{title}</h1></div>
        <span className="planned-badge">{t("plannedSurface")}</span>
      </div>
      <p>{t("plannedSurfaceDescription")}</p>
      {spikeHref && <Link className="primary-button" data-testid="open-architecture-spike" to={spikeHref}>Open frontend architecture spike</Link>}
      <dl className="route-contract">
        <div><dt>{t("canonicalRoute")}</dt><dd>{route.path}</dd></div>
        <div><dt>{t("lifecycle")}</dt><dd>{route.status}</dd></div>
      </dl>
    </section>
  );
}
