import {
  Activity,
  AlertCircle,
  Ban,
  CheckCircle2,
  Clock3,
  Inbox,
  RefreshCw,
  RotateCcw,
  ShieldAlert,
  Square,
  X,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  OperatorRunsApiError,
  operatorRunsApi,
  type OperatorRun,
  type OperatorRunDetail,
  type OperatorRunsApiClient,
  type QueueSummary,
  type RetryMode,
  type RunCapabilities,
  type RunFilters,
  type RunState,
} from "./operator-runs-api";
import {
  attemptStateLabel,
  freshnessLabel,
  operatorRunsCopy,
  retryModeLabel,
  runStateLabel,
  type OperatorRunsLanguage,
} from "./operator-runs-copy";
import "./operator-runs.css";

type PagePhase = "loading" | "ready" | "forbidden" | "failed";

interface PageState {
  readonly phase: PagePhase;
  readonly runs: readonly OperatorRun[];
  readonly visibleCount: number;
  readonly summary?: QueueSummary;
  readonly capabilities?: RunCapabilities;
  readonly refreshing: boolean;
  readonly refreshDegraded: boolean;
}

interface OperatorRunsProps {
  readonly workspaceKey?: string;
  readonly api?: Pick<OperatorRunsApiClient, "capabilities" | "list" | "summary" | "detail" | "mutate">;
}

const filterStates: readonly RunState[] = [
  "QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELLING", "CANCELLED", "PARTIAL",
];
const executionKinds = ["ingestion", "pipeline", "analytics", "forecast"] as const;
const terminalStates = new Set<RunState>(["SUCCEEDED", "FAILED", "CANCELLED", "PARTIAL"]);
const retryStates = new Set<RunState>(["FAILED", "CANCELLED", "PARTIAL"]);

function replaceRun(items: readonly OperatorRun[], run: OperatorRun): readonly OperatorRun[] {
  return items.map((item) => item.run_id === run.run_id ? run : item);
}

function stateTone(state: RunState): string {
  if (state === "FAILED") return "negative";
  if (state === "CANCELLING" || state === "PARTIAL") return "warning";
  if (state === "SUCCEEDED") return "positive";
  return "neutral";
}

function formatDate(language: OperatorRunsLanguage, value: string): string {
  return new Intl.DateTimeFormat(language, { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

export function OperatorRuns({ workspaceKey = "northwind-retail", api = operatorRunsApi }: OperatorRunsProps): React.JSX.Element {
  const { i18n } = useTranslation();
  const language: OperatorRunsLanguage = i18n.resolvedLanguage === "ru" ? "ru" : "en";
  const text = operatorRunsCopy(language);
  const [stateFilter, setStateFilter] = useState<RunState | "all">("all");
  const [kindFilter, setKindFilter] = useState("");
  const [traceFilter, setTraceFilter] = useState("");
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedId, setSelectedId] = useState<string>();
  const [detail, setDetail] = useState<OperatorRunDetail>();
  const [detailLoading, setDetailLoading] = useState(false);
  const [reason, setReason] = useState("");
  const [retryMode, setRetryMode] = useState<RetryMode>("failed_nodes");
  const [actionPending, setActionPending] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [page, setPage] = useState<PageState>({
    phase: "loading", runs: [], visibleCount: 0, refreshing: false, refreshDegraded: false,
  });
  const dialogRef = useRef<HTMLDialogElement>(null);
  const detailTriggerRef = useRef<HTMLButtonElement | null>(null);

  const filters = useMemo<RunFilters>(() => ({
    states: stateFilter === "all" ? undefined : [stateFilter],
    executionKind: kindFilter || undefined,
    safeTraceId: traceFilter.trim() || undefined,
  }), [kindFilter, stateFilter, traceFilter]);

  const load = useCallback(async (preserve = false, automatic = false): Promise<void> => {
    setPage((current) => ({
      ...current,
      phase: preserve && current.runs.length > 0 ? "ready" : "loading",
      refreshing: preserve,
      refreshDegraded: false,
    }));
    try {
      const [capabilities, listing, summary] = await Promise.all([
        api.capabilities(), api.list(filters), api.summary(),
      ]);
      setPage({
        phase: "ready",
        runs: listing.runs,
        visibleCount: listing.visible_count,
        summary,
        capabilities,
        refreshing: false,
        refreshDegraded: false,
      });
      if (automatic) setStatusMessage(text.autoRefreshed);
    } catch (error) {
      const forbidden = error instanceof OperatorRunsApiError && (error.status === 401 || error.status === 403);
      setPage((current) => {
        if (!forbidden && preserve && current.runs.length > 0) {
          return { ...current, phase: "ready", refreshing: false, refreshDegraded: true };
        }
        return {
          ...current,
          phase: forbidden ? "forbidden" : "failed",
          runs: [], visibleCount: 0, summary: undefined,
          refreshing: false, refreshDegraded: false,
        };
      });
    }
  }, [api, filters, text.autoRefreshed]);

  useEffect(() => { void load(); }, [load]);
  useEffect(() => {
    if (!autoRefresh || page.phase !== "ready") return undefined;
    const timer = window.setInterval(() => { void load(true, true); }, 5_000);
    return () => window.clearInterval(timer);
  }, [autoRefresh, load, page.phase]);

  const openDetails = async (run: OperatorRun, trigger: HTMLButtonElement): Promise<void> => {
    detailTriggerRef.current = trigger;
    setSelectedId(run.run_id);
    setDetail(undefined);
    setReason("");
    setDetailLoading(true);
    try {
      setDetail(await api.detail(run.run_id));
    } catch (error) {
      setStatusMessage(error instanceof OperatorRunsApiError ? error.code : text.actionFailed);
    } finally {
      setDetailLoading(false);
    }
  };

  useEffect(() => {
    const dialog = dialogRef.current;
    if (selectedId && dialog && !dialog.open) {
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    }
    if (!selectedId && dialog?.open) {
      if (typeof dialog.close === "function") dialog.close();
      else dialog.removeAttribute("open");
    }
  }, [selectedId]);

  const closeDetails = (): void => {
    setSelectedId(undefined);
    setDetail(undefined);
    window.requestAnimationFrame(() => detailTriggerRef.current?.focus());
  };

  const performAction = async (action: "cancel" | "retry"): Promise<void> => {
    if (!detail) return;
    const normalizedReason = reason.trim();
    if (normalizedReason.length < 3) {
      setStatusMessage(text.reasonRequired);
      document.getElementById("operator-action-reason")?.focus();
      return;
    }
    setActionPending(true);
    setStatusMessage(text.actionWorking);
    try {
      const updated = await api.mutate(detail, action, normalizedReason, retryMode);
      setPage((current) => ({ ...current, runs: replaceRun(current.runs, updated) }));
      setStatusMessage(action === "cancel" ? text.cancelled : text.retried);
      if (action === "cancel") setDetail(await api.detail(updated.run_id));
      else {
        await load(true);
        setDetail(await api.detail(updated.run_id));
        setSelectedId(updated.run_id);
      }
      setReason("");
    } catch (error) {
      if (error instanceof OperatorRunsApiError && (error.status === 401 || error.status === 403)) {
        setStatusMessage(text.actionForbidden);
      } else if (error instanceof OperatorRunsApiError && error.status === 409) {
        setStatusMessage(text.actionConflict);
        await load(true);
        try { setDetail(await api.detail(detail.run_id)); } catch { closeDetails(); }
      } else {
        setStatusMessage(text.actionFailed);
      }
    } finally {
      setActionPending(false);
    }
  };

  const canCancel = page.capabilities?.permissions.has("run.cancel") ?? false;
  const canRetry = page.capabilities?.permissions.has("run.retry") ?? false;
  const canFullRerun = page.capabilities?.permissions.has("run.create") ?? false;
  const summary = page.summary;

  return (
    <section className="operator-runs" aria-labelledby="operator-runs-title" data-workspace-key={workspaceKey}>
      <header className="operator-runs__heading">
        <div>
          <span className="operator-runs__eyebrow"><Activity aria-hidden="true" size={15} />{text.eyebrow}</span>
          <h1 id="operator-runs-title" tabIndex={-1}>{text.title}</h1>
          <p>{text.description}</p>
        </div>
        <button className="operator-button" type="button" onClick={() => void load(true)} disabled={page.refreshing}>
          <RefreshCw className={page.refreshing ? "operator-spinner" : undefined} aria-hidden="true" size={16} />
          {page.refreshing ? text.refreshing : text.refresh}
        </button>
      </header>

      <div className="operator-live sr-only" role="status" aria-atomic="true">{statusMessage}</div>

      {summary && (
        <section className="operator-queue" aria-label={text.lanes}>
          <dl>
            <div><dt>{text.visible}</dt><dd>{page.visibleCount}</dd></div>
            <div><dt>{text.queued}</dt><dd>{summary.counts.QUEUED ?? 0}</dd></div>
            <div><dt>{text.running}</dt><dd>{summary.counts.RUNNING ?? 0}</dd></div>
            <div><dt>{text.failed}</dt><dd>{summary.counts.FAILED ?? 0}</dd></div>
            <div><dt>{text.oldest}</dt><dd>{summary.oldest_queued_age_seconds === null ? "—" : `${summary.oldest_queued_age_seconds} ${text.seconds}`}</dd></div>
          </dl>
          <p><Clock3 aria-hidden="true" size={14} /> {text.observed}: <time dateTime={summary.observed_at}>{formatDate(language, summary.observed_at)}</time> · <strong>{freshnessLabel(language, summary.freshness)}</strong></p>
          <ul aria-label={text.lanes}>{Object.entries(summary.lane_counts).map(([lane, count]) => <li key={lane}><code>{lane}</code><span>{count}</span></li>)}</ul>
        </section>
      )}

      <form className="operator-filters" aria-label={text.filters} onSubmit={(event) => event.preventDefault()}>
        <label>{text.state}<select value={stateFilter} onChange={(event) => setStateFilter(event.target.value as RunState | "all")}>
          <option value="all">{text.all}</option>
          {filterStates.map((value) => <option key={value} value={value}>{runStateLabel(language, value)}</option>)}
        </select></label>
        <label>{text.kind}<select value={kindFilter} onChange={(event) => setKindFilter(event.target.value)}>
          <option value="">{text.anyKind}</option>
          {executionKinds.map((value) => <option key={value} value={value}>{value}</option>)}
        </select></label>
        <label className="operator-filters__trace">{text.trace}<input value={traceFilter} placeholder={text.tracePlaceholder} onChange={(event) => setTraceFilter(event.target.value)} /></label>
        <label className="operator-checkbox"><input type="checkbox" checked={autoRefresh} onChange={(event) => setAutoRefresh(event.target.checked)} /> <span>{text.autoRefresh}</span></label>
        <button type="button" onClick={() => { setStateFilter("all"); setKindFilter(""); setTraceFilter(""); }}>{text.clear}</button>
      </form>

      {page.refreshDegraded && <div className="operator-callout operator-callout--warning" role="status"><AlertCircle aria-hidden="true" /><div><strong>{text.refreshDegradedTitle}</strong><p>{text.refreshDegradedBody}</p></div></div>}
      {summary?.freshness === "stale" && <div className="operator-callout operator-callout--warning" role="status"><Clock3 aria-hidden="true" /><div><strong>{text.staleTitle}</strong><p>{text.staleBody}</p></div></div>}
      {summary?.freshness === "degraded" && <div className="operator-callout operator-callout--warning" role="status"><AlertCircle aria-hidden="true" /><div><strong>{text.degradedTitle}</strong><p>{text.degradedBody}</p></div></div>}

      {page.phase === "loading" && <div className="operator-state" role="status" aria-busy="true"><RefreshCw className="operator-spinner" aria-hidden="true" /><strong>{text.loading}</strong></div>}
      {page.phase === "forbidden" && <div className="operator-state" role="alert"><ShieldAlert aria-hidden="true" /><strong>{text.forbiddenTitle}</strong><p>{text.forbiddenBody}</p></div>}
      {page.phase === "failed" && <div className="operator-state" role="alert"><AlertCircle aria-hidden="true" /><strong>{text.failedTitle}</strong><p>{text.failedBody}</p><button className="operator-button operator-button--primary" type="button" onClick={() => void load()}>{text.retryLoad}</button></div>}
      {page.phase === "ready" && page.runs.length === 0 && <div className="operator-state"><Inbox aria-hidden="true" /><strong>{text.emptyTitle}</strong><p>{text.emptyBody}</p></div>}

      {page.phase === "ready" && page.runs.length > 0 && (
        <ul className="operator-run-list" aria-busy={page.refreshing}>
          {page.runs.map((run) => (
            <li className="operator-run" key={run.run_id}>
              <span className={`operator-status operator-status--${stateTone(run.state)}`}><span aria-hidden="true" />{runStateLabel(language, run.state)}</span>
              <div className="operator-run__main">
                <div><strong>{run.safe_title}</strong><span><code>{run.execution_kind}</code> · <code>{run.lane}</code></span></div>
                <dl>
                  <div><dt>{text.updated}</dt><dd><time dateTime={run.updated_at}>{formatDate(language, run.updated_at)}</time></dd></div>
                  <div><dt>{text.trace}</dt><dd>{run.safe_trace_id ? <code>{run.safe_trace_id}</code> : text.traceUnavailable}</dd></div>
                  {run.retry_of_id && <div><dt>{text.retryOfRun}</dt><dd><code>{run.retry_of_id}</code></dd></div>}
                </dl>
              </div>
              <button className="operator-detail-trigger" type="button" onClick={(event) => void openDetails(run, event.currentTarget)}>{text.details}<span aria-hidden="true">→</span></button>
            </li>
          ))}
        </ul>
      )}

      <dialog className="operator-drawer" ref={dialogRef} aria-labelledby="operator-detail-title" onCancel={(event) => { event.preventDefault(); closeDetails(); }} onClose={closeDetails}>
        <div className="operator-drawer__content">
          <header><div><span>{detail ? runStateLabel(language, detail.state) : text.loading}</span><h2 id="operator-detail-title">{text.detailsTitle}</h2></div><button type="button" onClick={closeDetails} aria-label={text.close}><X aria-hidden="true" /></button></header>
          {detailLoading && <div className="operator-detail-loading" role="status" aria-busy="true"><RefreshCw className="operator-spinner" aria-hidden="true" />{text.loading}</div>}
          {detail && <>
            <h3>{detail.safe_title}</h3>
            <dl className="operator-detail-grid">
              <div><dt>{text.runId}</dt><dd><code>{detail.run_id}</code></dd></div>
              <div><dt>{text.owner}</dt><dd><code>{detail.owner_principal_id}</code></dd></div>
              <div><dt>{text.trace}</dt><dd>{detail.safe_trace_id ? <code>{detail.safe_trace_id}</code> : text.traceUnavailable}</dd></div>
              <div><dt>{text.retryOfRun}</dt><dd>{detail.retry_of_id ? <code>{detail.retry_of_id}</code> : text.noAncestor}</dd></div>
              {detail.retry_mode && <div><dt>{text.retryMode}</dt><dd>{retryModeLabel(language, detail.retry_mode)}</dd></div>}
              <div><dt>{text.created}</dt><dd><time dateTime={detail.created_at}>{formatDate(language, detail.created_at)}</time></dd></div>
            </dl>
            <ol className="operator-attempts">
              {detail.attempts.map((attempt) => <li key={attempt.attempt_id}>
                <header><strong>{text.attempt} {attempt.attempt_number}</strong><span className={`operator-status operator-status--${attempt.state === "FAILED" ? "negative" : attempt.state === "SUCCEEDED" ? "positive" : "neutral"}`}>{attemptStateLabel(language, attempt.state)}</span></header>
                <dl>
                  <div><dt>{text.attemptId}</dt><dd><code>{attempt.attempt_id}</code></dd></div>
                  <div><dt>{text.retryOfAttempt}</dt><dd>{attempt.retry_of_id ? <code>{attempt.retry_of_id}</code> : text.noAncestor}</dd></div>
                  <div><dt>{text.fencing}</dt><dd>{attempt.fencing_token}</dd></div>
                  <div><dt>{text.lease}</dt><dd>{attempt.lease_expires_at ? formatDate(language, attempt.lease_expires_at) : text.noLease}</dd></div>
                  <div><dt>{text.failure}</dt><dd>{attempt.failure_code ? <><code>{attempt.failure_code}</code><span>{text.resourceFailure}</span></> : text.noFailure}</dd></div>
                  {attempt.observed_limit !== null && attempt.observed_limit !== undefined && <div><dt>{text.observedLimit}</dt><dd>{attempt.observed_limit}</dd></div>}
                  {attempt.configured_limit !== null && attempt.configured_limit !== undefined && <div><dt>{text.configuredLimit}</dt><dd>{attempt.configured_limit}</dd></div>}
                  {attempt.safe_remediation && <div><dt>{text.remediation}</dt><dd>{attempt.safe_remediation}</dd></div>}
                </dl>
              </li>)}
            </ol>
            <form className="operator-actions" onSubmit={(event) => event.preventDefault()}>
              <label htmlFor="operator-action-reason">{text.actionReason}</label>
              <p id="operator-action-hint">{text.actionReasonHint}</p>
              <textarea id="operator-action-reason" value={reason} minLength={3} maxLength={500} aria-describedby="operator-action-hint" placeholder={text.actionReasonPlaceholder} onChange={(event) => setReason(event.target.value)} />
              {retryStates.has(detail.state) && canRetry && <label>{text.mode}<select value={retryMode} onChange={(event) => setRetryMode(event.target.value as RetryMode)}><option value="failed_nodes">{text.failedNodes}</option>{canFullRerun && <option value="full_rerun">{text.fullRerun}</option>}</select></label>}
              <div>
                {!terminalStates.has(detail.state) && detail.state !== "CANCELLING" && canCancel && <button type="button" disabled={actionPending} onClick={() => void performAction("cancel")}><Square aria-hidden="true" />{text.cancel}</button>}
                {retryStates.has(detail.state) && canRetry && <button className="operator-button--primary" type="button" disabled={actionPending} onClick={() => void performAction("retry")}><RotateCcw aria-hidden="true" />{text.retry}</button>}
              </div>
              {!canCancel && !terminalStates.has(detail.state) && <p className="operator-permission-note"><Ban aria-hidden="true" />{text.permissionCancel}</p>}
              {!canRetry && retryStates.has(detail.state) && <p className="operator-permission-note"><Ban aria-hidden="true" />{text.permissionRetry}</p>}
              {canCancel && (terminalStates.has(detail.state) || detail.state === "CANCELLING") && <p className="operator-permission-note"><CheckCircle2 aria-hidden="true" />{text.cannotCancel}</p>}
              {canRetry && !retryStates.has(detail.state) && <p className="operator-permission-note"><Ban aria-hidden="true" />{text.cannotRetry}</p>}
            </form>
          </>}
        </div>
      </dialog>
    </section>
  );
}
