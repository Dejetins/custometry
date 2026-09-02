import {
  AlertCircle,
  BarChart3,
  CalendarRange,
  CheckCircle2,
  Database,
  Gauge,
  Inbox,
  LockKeyhole,
  RefreshCw,
  ShieldCheck,
  ShoppingBag,
  Store,
  Tags,
  TrendingUp,
  X,
  type LucideIcon,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  SalesAnalyticsApiError,
  metricById,
  salesAnalyticsApi,
  type ComparisonMode,
  type SalesAnalyticsApiClient,
  type SalesAnalyticsResult,
  type SalesCapabilities,
  type SalesFilterRequest,
  type SalesRunRequest,
} from "./analytics-sales-api";
import { salesCopy, type SalesLanguage } from "./analytics-sales-copy";
import "./sales-overview.css";

type PagePhase = "loading" | "empty" | "ready" | "forbidden" | "failed";

interface PageState {
  readonly phase: PagePhase;
  readonly result?: SalesAnalyticsResult;
  readonly capabilities?: SalesCapabilities;
  readonly refreshing: boolean;
  readonly refreshDegraded: boolean;
}

interface FilterState {
  readonly currentStart: string;
  readonly currentEnd: string;
  readonly comparisonMode: ComparisonMode;
  readonly comparisonStart: string;
  readonly comparisonEnd: string;
  readonly store: string;
  readonly channel: string;
}

interface SalesOverviewProps {
  readonly workspaceKey?: string;
  readonly api?: Pick<SalesAnalyticsApiClient, "capabilities" | "latest" | "run">;
}

function filterStateFrom(result: SalesAnalyticsResult): FilterState {
  return {
    currentStart: result.resolved_current_period.starts_on,
    currentEnd: result.resolved_current_period.ends_on,
    comparisonMode: result.applied_comparison_mode,
    comparisonStart: result.resolved_comparison_period?.starts_on ?? "",
    comparisonEnd: result.resolved_comparison_period?.ends_on ?? "",
    store: "",
    channel: "",
  };
}

function formatMetric(language: SalesLanguage, value: string | null | undefined): string {
  if (value === null || value === undefined) return "—";
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return value;
  return new Intl.NumberFormat(language, { maximumFractionDigits: 2 }).format(parsed);
}

function formatPercent(language: SalesLanguage, value: string | null | undefined): string {
  if (value === null || value === undefined) return "—";
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return value;
  const prefix = parsed > 0 ? "+" : "";
  return `${prefix}${new Intl.NumberFormat(language, { maximumFractionDigits: 1 }).format(parsed)}%`;
}

function periodLabel(result: SalesAnalyticsResult, comparison = false): string {
  const period = comparison ? result.resolved_comparison_period : result.resolved_current_period;
  return period ? `${period.starts_on} — ${period.ends_on}` : "—";
}

function StatePanel({ icon: Icon, title, body, action }: {
  readonly icon: typeof Inbox;
  readonly title: string;
  readonly body: string;
  readonly action?: React.ReactNode;
}): React.JSX.Element {
  return <div className="sales-state" role="status"><Icon aria-hidden="true" /><strong>{title}</strong><p>{body}</p>{action}</div>;
}

export function SalesOverview({ workspaceKey = "northwind-retail", api = salesAnalyticsApi }: SalesOverviewProps): React.JSX.Element {
  const { i18n } = useTranslation();
  const language: SalesLanguage = i18n.resolvedLanguage === "ru" ? "ru" : "en";
  const text = salesCopy(language);
  const [page, setPage] = useState<PageState>({ phase: "loading", refreshing: false, refreshDegraded: false });
  const [filters, setFilters] = useState<FilterState>();
  const [applying, setApplying] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [validationMessage, setValidationMessage] = useState("");
  const trustRef = useRef<HTMLDialogElement>(null);
  const trustTriggerRef = useRef<HTMLButtonElement>(null);

  const load = useCallback(async (preserve = false): Promise<void> => {
    setPage((current) => ({
      ...current,
      phase: preserve && current.result ? "ready" : "loading",
      refreshing: preserve,
      refreshDegraded: false,
    }));
    try {
      const [capabilities, result] = await Promise.all([api.capabilities(), api.latest()]);
      setPage({
        phase: result ? "ready" : "empty",
        result,
        capabilities,
        refreshing: false,
        refreshDegraded: false,
      });
      if (result) setFilters((current) => current ?? filterStateFrom(result));
      if (preserve) setStatusMessage(text.statusUpdate);
    } catch (error) {
      const forbidden = error instanceof SalesAnalyticsApiError && [401, 403, 404].includes(error.status);
      setPage((current) => {
        if (!forbidden && preserve && current.result) {
          return { ...current, phase: "ready", refreshing: false, refreshDegraded: true };
        }
        return {
          phase: forbidden ? "forbidden" : "failed",
          refreshing: false,
          refreshDegraded: false,
        };
      });
    }
  }, [api, text.statusUpdate]);

  useEffect(() => { void load(); }, [load]);

  const result = page.result;
  const canRun = page.capabilities?.permissions.has("analysis.run") ?? false;
  const revenue = result ? metricById(result, "net_revenue") : undefined;
  const orders = result ? metricById(result, "receipt_count") : undefined;
  const averageOrder = result ? metricById(result, "average_receipt") : undefined;
  const discount = result ? metricById(result, "discount_amount") : undefined;
  const breakdowns: readonly { readonly icon: LucideIcon; readonly label: string }[] = [
    { icon: ShoppingBag, label: text.product },
    { icon: Store, label: text.storeBreakdown },
    { icon: BarChart3, label: text.channelBreakdown },
  ];

  const trustState = useMemo(() => {
    if (!result) return "ready" as const;
    if (result.freshness.status === "stale") return "stale" as const;
    if (result.freshness.status === "degraded" || result.quality.decision !== "passed" || result.comparability_status !== "comparable") return "degraded" as const;
    return "ready" as const;
  }, [result]);

  const openTrust = (): void => {
    const dialog = trustRef.current;
    if (!dialog) return;
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "");
  };

  const closeTrust = (): void => {
    const dialog = trustRef.current;
    if (dialog?.open && typeof dialog.close === "function") dialog.close();
    else dialog?.removeAttribute("open");
    window.requestAnimationFrame(() => trustTriggerRef.current?.focus());
  };

  const updateFilter = <K extends keyof FilterState>(key: K, value: FilterState[K]): void => {
    setFilters((current) => current ? { ...current, [key]: value } : current);
  };

  const apply = async (event: React.FormEvent): Promise<void> => {
    event.preventDefault();
    if (!result || !filters || !canRun) return;
    if (filters.currentStart > filters.currentEnd || (filters.comparisonMode !== "none" && filters.comparisonStart > filters.comparisonEnd)) {
      setValidationMessage(text.invalidPeriod);
      document.getElementById("sales-current-start")?.focus();
      return;
    }
    setValidationMessage("");
    const typedFilters: SalesFilterRequest[] = [];
    if (filters.store.trim()) typedFilters.push({ field: "store_id", operator: "eq", value: filters.store.trim() });
    if (filters.channel.trim()) typedFilters.push({ field: "channel_id", operator: "eq", value: filters.channel.trim() });
    const payload: SalesRunRequest = {
      result_type: "sales",
      semantic_dataset_version_id: result.semantic_dataset_version_id,
      comparison: {
        mode: filters.comparisonMode,
        current_period: { starts_on: filters.currentStart, ends_on: filters.currentEnd },
        comparison_period: filters.comparisonMode === "none" ? null : { starts_on: filters.comparisonStart, ends_on: filters.comparisonEnd },
        timezone: result.timezone,
        calendar_version_id: result.calendar_version_id,
        incomplete_period_policy: "explicit_partial",
        leap_day_policy: "calendar_map",
        iso_week_53_policy: "explicit_partial",
        definition_compatibility_policy: "require_same_versions",
      },
      filters: typedFilters,
      rfm_score_bins: 5,
      rfm_frequency_measure: "receipt_count",
      rfm_segment_rule_set_version: "rfm-retail-v1",
    };
    setApplying(true);
    try {
      const next = await api.run(payload);
      setPage((current) => ({ ...current, phase: "ready", result: next, refreshDegraded: false }));
      setStatusMessage(text.statusUpdate);
    } catch (error) {
      if (error instanceof SalesAnalyticsApiError && [401, 403, 404].includes(error.status)) {
        setPage({ phase: "forbidden", refreshing: false, refreshDegraded: false });
      } else {
        setPage((current) => ({ ...current, refreshDegraded: true }));
      }
    } finally {
      setApplying(false);
    }
  };

  return (
    <section className="sales-overview" aria-labelledby="sales-overview-title" data-workspace-key={workspaceKey} data-page-state={page.phase}>
      <header className="sales-heading">
        <div>
          <span className="sales-eyebrow"><BarChart3 aria-hidden="true" size={15} />{text.eyebrow}</span>
          <h1 id="sales-overview-title" tabIndex={-1}>{text.title}</h1>
          <p>{text.description}</p>
        </div>
        <div className="sales-heading__actions">
          {result && <button ref={trustTriggerRef} className="sales-button" type="button" onClick={openTrust}><ShieldCheck aria-hidden="true" size={16} />{text.openTrust}</button>}
          <button className="sales-button" type="button" onClick={() => void load(Boolean(result))} disabled={page.refreshing}>
            <RefreshCw className={page.refreshing ? "sales-spinner" : undefined} aria-hidden="true" size={16} />
            {page.refreshing ? text.refreshing : text.refresh}
          </button>
        </div>
      </header>

      <div className="sr-only" role="status" aria-atomic="true">{statusMessage}</div>

      {page.refreshDegraded && <div className="sales-callout sales-callout--warning" role="status"><AlertCircle aria-hidden="true" /><div><strong>{text.degraded}</strong><p>{text.refreshFailed}</p></div></div>}
      {result && trustState !== "ready" && <div className="sales-callout sales-callout--warning" role="status"><AlertCircle aria-hidden="true" /><div><strong>{trustState === "stale" ? text.stale : text.degraded}</strong><p>{result.limitation_codes.join(", ") || text.notClassified}</p></div></div>}

      {page.phase === "loading" && <StatePanel icon={Gauge} title={text.firstLoading} body={text.loadingBody} />}
      {page.phase === "empty" && <StatePanel icon={Inbox} title={text.empty} body={text.emptyBody} />}
      {page.phase === "forbidden" && <StatePanel icon={LockKeyhole} title={text.forbidden} body={text.forbiddenBody} action={<button className="sales-button" type="button" onClick={() => void load()}>{text.retry}</button>} />}
      {page.phase === "failed" && <StatePanel icon={AlertCircle} title={text.failed} body={text.failedBody} action={<button className="sales-button" type="button" onClick={() => void load()}>{text.retry}</button>} />}

      {result && filters && page.phase === "ready" && <>
        <section className="sales-context" aria-label={text.filters}>
          <div className="sales-context__summary">
            <span><CalendarRange aria-hidden="true" size={15} />{periodLabel(result)}</span>
            <span className={`sales-trust-state sales-trust-state--${trustState}`}><span aria-hidden="true" />{trustState === "stale" ? text.stale : trustState === "degraded" ? text.degraded : text.ready}</span>
            <span>{text.sourceBoundary}</span>
          </div>
          <form className="sales-filters" aria-label={text.filters} onSubmit={(event) => void apply(event)}>
            <label>{text.currentStart}<input id="sales-current-start" type="date" value={filters.currentStart} onChange={(event) => updateFilter("currentStart", event.target.value)} disabled={!canRun || applying} aria-invalid={Boolean(validationMessage)} aria-describedby={validationMessage ? "sales-filter-error" : undefined} /></label>
            <label>{text.currentEnd}<input type="date" value={filters.currentEnd} onChange={(event) => updateFilter("currentEnd", event.target.value)} disabled={!canRun || applying} /></label>
            <label>{text.comparison}<select value={filters.comparisonMode} onChange={(event) => updateFilter("comparisonMode", event.target.value as ComparisonMode)} disabled={!canRun || applying}><option value="previous_year_calendar_aligned">{text.calendarAligned}</option><option value="none">{text.noComparison}</option></select></label>
            <label>{text.comparisonStart}<input type="date" value={filters.comparisonStart} onChange={(event) => updateFilter("comparisonStart", event.target.value)} disabled={!canRun || applying || filters.comparisonMode === "none"} /></label>
            <label>{text.comparisonEnd}<input type="date" value={filters.comparisonEnd} onChange={(event) => updateFilter("comparisonEnd", event.target.value)} disabled={!canRun || applying || filters.comparisonMode === "none"} /></label>
            <label>{text.store}<input value={filters.store} placeholder={text.optional} onChange={(event) => updateFilter("store", event.target.value)} disabled={!canRun || applying} /></label>
            <label>{text.channel}<input value={filters.channel} placeholder={text.optional} onChange={(event) => updateFilter("channel", event.target.value)} disabled={!canRun || applying} /></label>
            <button className="sales-button sales-button--primary" type="submit" disabled={!canRun || applying}>{applying ? text.applying : text.apply}</button>
          </form>
          {validationMessage && <p className="sales-filter-error" id="sales-filter-error" role="alert">{validationMessage}</p>}
          {!canRun && <p className="sales-policy-note"><LockKeyhole aria-hidden="true" size={15} />{text.readOnly}</p>}
        </section>

        <dl className="sales-kpi-strip" aria-label={`${text.revenue}, ${text.orders}, ${text.aov}, ${text.margin}`}>
          <div><dt>{text.revenue}</dt><dd>{formatMetric(language, revenue?.current_value)}</dd><span>{text.vsLy}: {formatPercent(language, revenue?.percent_change)}</span></div>
          <div><dt>{text.orders}</dt><dd>{formatMetric(language, orders?.current_value)}</dd><span>{text.vsLy}: {formatPercent(language, orders?.percent_change)}</span></div>
          <div><dt>{text.aov}</dt><dd>{formatMetric(language, averageOrder?.current_value)}</dd><span>{text.vsLy}: {formatPercent(language, averageOrder?.percent_change)}</span></div>
          <div className="is-unavailable"><dt>{text.margin}</dt><dd>{text.unavailable}</dd><span>{text.marginUnavailable}</span></div>
        </dl>

        <div className="sales-analysis-grid">
          <section className="sales-panel sales-panel--trend" aria-labelledby="sales-trend-title"><header><div><span>{text.trend}</span><h2 id="sales-trend-title">{text.trend}</h2></div><TrendingUp aria-hidden="true" /></header><div className="sales-unavailable"><Database aria-hidden="true" /><p>{text.trendUnavailable}</p></div></section>
          <section className="sales-panel" aria-labelledby="sales-contribution-title"><header><div><span>{text.contribution}</span><h2 id="sales-contribution-title">{text.contribution}</h2></div><Tags aria-hidden="true" /></header><dl className="sales-contribution"><div><dt>{text.delta}</dt><dd>{formatMetric(language, revenue?.absolute_change)}</dd></div><div><dt>{text.discount}</dt><dd>{formatMetric(language, discount?.current_value)}</dd></div></dl><p className="sales-panel__note">{text.contributionUnavailable}</p></section>
        </div>

        <section className="sales-breakdowns" aria-labelledby="sales-breakdowns-title"><header><span>{text.breakdowns}</span><h2 id="sales-breakdowns-title">{text.breakdowns}</h2></header><div>{breakdowns.map(({ icon: Icon, label }) => <article key={label}><Icon aria-hidden="true" /><strong>{label}</strong><p>{text.breakdownUnavailable}</p></article>)}</div></section>

        <dialog className="sales-trust-drawer" ref={trustRef} aria-labelledby="sales-trust-title" onCancel={closeTrust} onClose={() => trustTriggerRef.current?.focus()}>
          <div className="sales-trust-drawer__content">
            <header><div><span>{text.result}</span><h2 id="sales-trust-title">{text.trust}</h2></div><button type="button" onClick={closeTrust} aria-label={text.closeTrust}><X aria-hidden="true" /></button></header>
            <p className="sales-immutable"><CheckCircle2 aria-hidden="true" />{text.immutable} · <code>{result.result_id}</code></p>
            <dl className="sales-trust-grid">
              <div><dt>{text.period}</dt><dd>{periodLabel(result)}</dd></div>
              <div><dt>{text.comparisonPeriod}</dt><dd>{periodLabel(result, true)}</dd></div>
              <div><dt>{text.comparability}</dt><dd>{result.comparability_status === "comparable" ? text.comparable : result.comparability_status === "partial" ? text.partial : text.notComparable}</dd></div>
              <div><dt>{text.coverage}</dt><dd>{result.current_coverage.observed_days}/{result.current_coverage.period_days} {text.observedDays}</dd></div>
              <div><dt>{text.quality}</dt><dd>{result.quality.decision ?? text.notClassified}</dd></div>
              <div><dt>{text.freshness}</dt><dd>{result.freshness.status ?? text.notClassified}</dd></div>
              <div><dt>{text.lastEvent}</dt><dd>{result.freshness.max_event_date ?? "—"}</dd></div>
              <div><dt>{text.grain}</dt><dd>{result.lineage.fact_scope ?? "—"}</dd></div>
              <div><dt>{text.policy}</dt><dd><code>{result.policy_hash}</code></dd></div>
              <div><dt>{text.filterHash}</dt><dd><code>{result.normalized_filter_expression_hash}</code></dd></div>
            </dl>
            <section><h3>{text.discountSemantics}</h3><p>{text.totalOnly}</p></section>
            <section><h3>{text.pvm}</h3><p>{text.pvmUnavailable}</p></section>
          </div>
        </dialog>
      </>}
    </section>
  );
}
