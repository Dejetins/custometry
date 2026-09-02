import {
  AlertCircle,
  BellRing,
  Check,
  CheckCheck,
  ExternalLink,
  Inbox,
  RefreshCw,
  ShieldAlert,
  X,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  NotificationApiError,
  notificationApi,
  type NotificationApiClient,
  type NotificationCapabilities,
  type NotificationCategory,
  type NotificationFilters,
  type NotificationItem,
  type NotificationSeverity,
} from "./notification-api";
import {
  categoryLabel,
  notificationCopy,
  notificationMessage,
  severityLabel,
  type NotificationLanguage,
} from "./notification-copy";
import { resolveNotificationDeepLink } from "./notification-deep-link";
import "./notifications.css";

type BooleanFilter = "all" | "true" | "false";
type InboxPhase = "loading" | "ready" | "forbidden" | "failed";

interface InboxState {
  readonly phase: InboxPhase;
  readonly items: readonly NotificationItem[];
  readonly visibleCount: number;
  readonly unreadCount: number;
  readonly unreadCapped: boolean;
  readonly capabilities?: NotificationCapabilities;
  readonly refreshing: boolean;
  readonly degraded: boolean;
}

interface NotificationInboxProps {
  readonly workspaceKey?: string;
  readonly api?: Pick<NotificationApiClient, "capabilities" | "list" | "unreadCount" | "mutate">;
}

const severities: readonly NotificationSeverity[] = ["info", "warning", "critical"];
const categories: readonly NotificationCategory[] = [
  "run", "data_quality", "data_freshness", "forecast", "schedule", "system", "security", "admin",
];

function optionalBoolean(value: BooleanFilter): boolean | undefined {
  return value === "all" ? undefined : value === "true";
}

function upsert(items: readonly NotificationItem[], updated: NotificationItem): readonly NotificationItem[] {
  return items.map((item) => item.notification_id === updated.notification_id ? updated : item);
}

export function NotificationInbox({
  workspaceKey = "northwind-retail",
  api = notificationApi,
}: NotificationInboxProps): React.JSX.Element {
  const { i18n } = useTranslation();
  const language: NotificationLanguage = i18n.resolvedLanguage === "ru" ? "ru" : "en";
  const text = notificationCopy(language);
  const [severity, setSeverity] = useState<NotificationSeverity | "all">("all");
  const [category, setCategory] = useState<NotificationCategory | "all">("all");
  const [read, setRead] = useState<BooleanFilter>("all");
  const [acknowledged, setAcknowledged] = useState<BooleanFilter>("all");
  const [resolved, setResolved] = useState<BooleanFilter>("all");
  const [selectedId, setSelectedId] = useState<string>();
  const [statusMessage, setStatusMessage] = useState("");
  const [actionPending, setActionPending] = useState(false);
  const [state, setState] = useState<InboxState>({
    phase: "loading", items: [], visibleCount: 0, unreadCount: 0,
    unreadCapped: false, refreshing: false, degraded: false,
  });
  const dialogRef = useRef<HTMLDialogElement>(null);
  const detailTriggerRef = useRef<HTMLElement | null>(null);

  const filters = useMemo<NotificationFilters>(() => ({
    severity: severity === "all" ? undefined : severity,
    category: category === "all" ? undefined : category,
    read: optionalBoolean(read),
    acknowledged: optionalBoolean(acknowledged),
    resolved: optionalBoolean(resolved),
  }), [acknowledged, category, read, resolved, severity]);

  const load = useCallback(async (preserve = false): Promise<void> => {
    setState((current) => ({
      ...current,
      phase: preserve && current.items.length > 0 ? "ready" : "loading",
      refreshing: preserve,
      degraded: false,
    }));
    try {
      const [capabilities, listing, unreadSummary] = await Promise.all([
        api.capabilities(), api.list(filters), api.unreadCount(),
      ]);
      setState({
        phase: "ready",
        items: listing.items,
        visibleCount: listing.visible_count,
        unreadCount: unreadSummary.unread_count,
        unreadCapped: unreadSummary.capped,
        capabilities,
        refreshing: false,
        degraded: listing.items.some((item) => item.freshness !== "fresh"),
      });
    } catch (error) {
      const forbidden = error instanceof NotificationApiError
        && (error.status === 401 || error.status === 403);
      setState((current) => {
        if (!forbidden && preserve && current.items.length > 0) {
          return { ...current, phase: "ready", refreshing: false, degraded: true };
        }
        return {
          ...current,
          phase: forbidden ? "forbidden" : "failed",
          refreshing: false,
          degraded: false,
          items: [],
          visibleCount: 0,
          unreadCount: 0,
        };
      });
    }
  }, [api, filters]);

  useEffect(() => { void load(); }, [load]);

  const selected = state.items.find((item) => item.notification_id === selectedId);
  const deepLink = selected
    ? resolveNotificationDeepLink(selected.deep_link, workspaceKey)
    : undefined;
  const canAcknowledge = state.capabilities?.permissions.has("notification.acknowledge") ?? false;

  useEffect(() => {
    const dialog = dialogRef.current;
    if (selected && dialog && !dialog.open) {
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    }
    if (!selected && dialog?.open) {
      if (typeof dialog.close === "function") dialog.close();
      else dialog.removeAttribute("open");
    }
  }, [selected]);

  const closeDetails = (): void => {
    setSelectedId(undefined);
    const trigger = detailTriggerRef.current;
    window.requestAnimationFrame(() => trigger?.focus());
  };

  const openDetails = (item: NotificationItem, trigger: HTMLElement): void => {
    detailTriggerRef.current = trigger;
    setSelectedId(item.notification_id);
    if (!item.read) {
      void performAction(item, "read", false);
    }
  };

  const performAction = async (
    item: NotificationItem,
    action: "read" | "dismiss" | "acknowledge",
    announce = true,
  ): Promise<void> => {
    setActionPending(true);
    if (announce) setStatusMessage(text.actionWorking);
    try {
      const updated = await api.mutate(item, action);
      setState((current) => ({
        ...current,
        items: upsert(current.items, updated),
        unreadCount: action === "read" && !item.read
          ? Math.max(0, current.unreadCount - 1)
          : current.unreadCount,
      }));
      if (announce) {
        setStatusMessage(
          action === "read" ? text.actionRead
            : action === "dismiss" ? text.actionDismissed
              : text.actionAcknowledged,
        );
      }
    } catch (error) {
      if (error instanceof NotificationApiError && (error.status === 403 || error.status === 409)) {
        setStatusMessage(text.actionForbidden);
        await load(true);
      } else if (announce) {
        setStatusMessage(text.actionFailed);
      }
    } finally {
      setActionPending(false);
    }
  };

  const clearFilters = (): void => {
    setSeverity("all");
    setCategory("all");
    setRead("all");
    setAcknowledged("all");
    setResolved("all");
  };

  return (
    <section className="notification-inbox" aria-labelledby="notification-inbox-title">
      <div className="notification-heading">
        <div>
          <span className="notification-eyebrow"><BellRing aria-hidden="true" size={15} />{text.eyebrow}</span>
          <h1 id="notification-inbox-title" tabIndex={-1}>{text.title}</h1>
          <p>{text.description}</p>
        </div>
        <button
          className="notification-button notification-button--secondary"
          type="button"
          onClick={() => void load(true)}
          disabled={state.refreshing}
        >
          <RefreshCw aria-hidden="true" size={16} />
          {state.refreshing ? text.refreshing : text.refresh}
        </button>
      </div>

      <div className="notification-summary" aria-live="polite">
        <span><strong>{state.visibleCount}</strong> {text.visible}</span>
        <span><strong>{state.unreadCount}{state.unreadCapped ? "+" : ""}</strong> {text.unreadCount}</span>
      </div>

      <form className="notification-filters" aria-label={text.filters} onSubmit={(event) => event.preventDefault()}>
        <label>{text.severity}<select value={severity} onChange={(event) => setSeverity(event.target.value as NotificationSeverity | "all")}>
          <option value="all">{text.all}</option>
          {severities.map((value) => <option key={value} value={value}>{severityLabel(language, value)}</option>)}
        </select></label>
        <label>{text.category}<select value={category} onChange={(event) => setCategory(event.target.value as NotificationCategory | "all")}>
          <option value="all">{text.all}</option>
          {categories.map((value) => <option key={value} value={value}>{categoryLabel(language, value)}</option>)}
        </select></label>
        {([
          [text.read, read, setRead],
          [text.acknowledged, acknowledged, setAcknowledged],
          [text.resolved, resolved, setResolved],
        ] as const).map(([label, value, setter]) => (
          <label key={label}>{label}<select value={value} onChange={(event) => setter(event.target.value as BooleanFilter)}>
            <option value="all">{text.all}</option><option value="true">{text.yes}</option><option value="false">{text.no}</option>
          </select></label>
        ))}
      </form>

      <div className="sr-only" role="status" aria-atomic="true">{statusMessage}</div>

      {state.degraded && (
        <div className="notification-callout notification-callout--warning" role="status">
          <AlertCircle aria-hidden="true" /><div><strong>{text.degradedTitle}</strong><p>{text.degradedBody}</p></div>
        </div>
      )}

      {state.phase === "loading" && (
        <div className="notification-state" aria-busy="true" role="status">
          <RefreshCw className="notification-spinner" aria-hidden="true" /><strong>{text.loading}</strong>
        </div>
      )}

      {state.phase === "forbidden" && (
        <div className="notification-state" role="alert">
          <ShieldAlert aria-hidden="true" /><strong>{text.forbiddenTitle}</strong><p>{text.forbiddenBody}</p>
        </div>
      )}

      {state.phase === "failed" && (
        <div className="notification-state" role="alert">
          <AlertCircle aria-hidden="true" /><strong>{text.failedTitle}</strong><p>{text.failedBody}</p>
          <button className="notification-button notification-button--primary" type="button" onClick={() => void load()}>{text.retry}</button>
        </div>
      )}

      {state.phase === "ready" && state.items.length === 0 && (
        <div className="notification-state">
          <Inbox aria-hidden="true" /><strong>{text.emptyTitle}</strong><p>{text.emptyBody}</p>
          <button className="notification-button notification-button--secondary" type="button" onClick={clearFilters}>{text.clearFilters}</button>
        </div>
      )}

      {state.phase === "ready" && state.items.length > 0 && (
        <ul className="notification-list" aria-busy={state.refreshing}>
          {state.items.map((item) => (
            <li key={item.notification_id} className={`notification-card notification-card--${item.severity} ${item.read ? "is-read" : "is-unread"}`}>
              <span className="notification-severity" aria-label={severityLabel(language, item.severity)}><span aria-hidden="true" /></span>
              <div className="notification-card__body">
                <div className="notification-card__meta">
                  <span>{categoryLabel(language, item.category)}</span>
                  <time dateTime={item.occurred_at}>{new Intl.DateTimeFormat(language, { dateStyle: "medium", timeStyle: "short" }).format(new Date(item.occurred_at))}</time>
                </div>
                <strong>{notificationMessage(language, item)}</strong>
                <div className="notification-card__badges">
                  <span>{item.read ? text.readValue : text.unread}</span>
                  {item.source_event_count > 1 && <span>{item.source_event_count} {text.groupEvents}</span>}
                  {item.resolved && <span><Check aria-hidden="true" />{text.statusResolved}</span>}
                  {item.acknowledged && <span><CheckCheck aria-hidden="true" />{text.statusAcknowledged}</span>}
                  {item.dismissed && <span>{text.statusDismissed}</span>}
                </div>
              </div>
              <button className="notification-detail-trigger" type="button" onClick={(event) => openDetails(item, event.currentTarget)}>
                {text.details}<span aria-hidden="true">→</span>
              </button>
            </li>
          ))}
        </ul>
      )}

      <dialog
        className="notification-drawer"
        ref={dialogRef}
        aria-labelledby="notification-detail-title"
        onCancel={(event) => { event.preventDefault(); closeDetails(); }}
        onClose={closeDetails}
      >
        {selected && (
          <div className="notification-drawer__content">
            <header>
              <div><span>{severityLabel(language, selected.severity)}</span><h2 id="notification-detail-title">{text.detailsTitle}</h2></div>
              <button type="button" onClick={closeDetails} aria-label={text.close}><X aria-hidden="true" /></button>
            </header>
            <p className="notification-detail-message">{notificationMessage(language, selected)}</p>
            <dl>
              <div><dt>{text.stableCode}</dt><dd><code>{selected.message_code}</code></dd></div>
              <div><dt>{text.source}</dt><dd>{selected.source_owner} · {selected.source_type}</dd></div>
              <div><dt>{text.occurred}</dt><dd><time dateTime={selected.occurred_at}>{new Intl.DateTimeFormat(language, { dateStyle: "long", timeStyle: "medium" }).format(new Date(selected.occurred_at))}</time></dd></div>
              <div><dt>{text.freshness}</dt><dd>{selected.freshness}</dd></div>
              {selected.trace_id && <div><dt>{text.trace}</dt><dd><code>{selected.trace_id}</code></dd></div>}
            </dl>
            {deepLink ? (
              <Link className="notification-deep-link" to={deepLink} onClick={closeDetails}><ExternalLink aria-hidden="true" />{text.deepLink}</Link>
            ) : <p className="notification-link-unavailable">{text.deepLinkUnavailable}</p>}
            <div className="notification-actions">
              {!selected.read && <button type="button" disabled={actionPending} onClick={() => void performAction(selected, "read")}><Check aria-hidden="true" />{text.markRead}</button>}
              {!selected.dismissed && <button type="button" disabled={actionPending} onClick={() => void performAction(selected, "dismiss")}><X aria-hidden="true" />{text.dismiss}</button>}
              {selected.severity === "critical" && !selected.acknowledged && canAcknowledge && (
                <button className="notification-button--primary" type="button" disabled={actionPending} onClick={() => void performAction(selected, "acknowledge")}><CheckCheck aria-hidden="true" />{text.acknowledge}</button>
              )}
            </div>
            {selected.severity === "critical" && !canAcknowledge && <p className="notification-permission-note">{text.acknowledgementUnavailable}</p>}
          </div>
        )}
      </dialog>
    </section>
  );
}
