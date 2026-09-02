import { AlertTriangle, CheckCircle2, Clock3, Database, FileKey2, Inbox, Plus, RefreshCw, Search, ShieldAlert } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {
  ConnectionsApiError,
  type ConnectionCapabilities,
  type ConnectionCatalogPort,
  type ConnectionCatalogResult,
  type ConnectionListItem,
  type ConnectionStatus,
  type ConnectorId,
} from "./connections-api";
import { connectionCopy, connectionStatuses, connectionStatusLabel, connectorIds, connectorLabel, type ConnectionLanguage } from "./connection-copy";
import { w14SourceIntakeApi } from "./connections-api";
import "./connections.css";

type ListPhase = "loading" | "ready" | "unavailable" | "forbidden" | "failed";
interface ListState { readonly phase: ListPhase; readonly result?: ConnectionCatalogResult; readonly capabilities?: ConnectionCapabilities; readonly refreshing: boolean; }

function formatDate(language: ConnectionLanguage, value: string): string {
  return new Intl.DateTimeFormat(language, { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

function statusTone(status: ConnectionStatus): string {
  if (status === "ready") return "positive";
  if (status === "failed") return "negative";
  if (status === "stale" || status === "degraded") return "warning";
  return "neutral";
}

interface ConnectionsListProps { readonly workspaceKey: string; readonly api?: ConnectionCatalogPort; readonly fixture?: boolean; }
export function ConnectionsList({ workspaceKey, api = w14SourceIntakeApi, fixture = false }: ConnectionsListProps): React.JSX.Element {
  const { i18n } = useTranslation();
  const language: ConnectionLanguage = i18n.resolvedLanguage === "ru" ? "ru" : "en";
  const text = connectionCopy(language);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<ConnectionStatus | "all">("all");
  const [owner, setOwner] = useState("all");
  const [state, setState] = useState<ListState>({ phase: "loading", refreshing: false });
  const [announcement, setAnnouncement] = useState("");

  const load = useCallback(async (preserve = false): Promise<void> => {
    setState((current) => ({ ...current, phase: preserve && current.result ? current.phase : "loading", refreshing: preserve }));
    try {
      const [capabilities, result] = await Promise.all([api.capabilities(), api.list()]);
      if (!capabilities.permissions.has("connection.read_metadata")) throw new ConnectionsApiError(403, "FORBIDDEN");
      setState({ phase: result.support === "unavailable" ? "unavailable" : "ready", result, capabilities, refreshing: false });
      if (preserve) setAnnouncement(text.refresh);
    } catch (error) {
      const forbidden = error instanceof ConnectionsApiError && (error.status === 401 || error.status === 403);
      setState({ phase: forbidden ? "forbidden" : "failed", refreshing: false });
    }
  }, [api, text.refresh]);

  useEffect(() => { void load(); }, [load]);
  const items = state.result?.connections ?? [];
  const owners = useMemo(() => [...new Set(items.map((item) => item.ownerLabel))].sort(), [items]);
  const filtered = useMemo(() => {
    const normalized = query.trim().toLocaleLowerCase(language);
    return items.filter((item) => {
      const matchesSearch = !normalized || [item.displayName, item.connectorId, item.ownerLabel].some((value) => value.toLocaleLowerCase(language).includes(normalized));
      return matchesSearch && (status === "all" || item.status === status) && (owner === "all" || item.ownerLabel === owner);
    });
  }, [items, language, owner, query, status]);
  const canManage = state.capabilities?.permissions.has("connection.manage") ?? false;
  const hasFilters = query.length > 0 || status !== "all" || owner !== "all";
  const clearFilters = (): void => { setQuery(""); setStatus("all"); setOwner("all"); };

  return (
    <section className="connections" aria-labelledby="connections-title" data-workspace-key={workspaceKey} data-proof-boundary={fixture ? "presentation-fixture" : "w14-production-adapter"}>
      <header className="connections-heading">
        <div><span className="connections-eyebrow"><Database aria-hidden="true" size={15} />{text.eyebrow}</span><h1 id="connections-title" tabIndex={-1}>{text.title}</h1><p>{text.description}</p></div>
        <div className="connections-heading__actions">
          <button type="button" className="connections-button" disabled={state.refreshing} onClick={() => void load(true)}><RefreshCw className={state.refreshing ? "connections-spinner" : undefined} aria-hidden="true" size={16} />{state.refreshing ? text.refreshing : text.refresh}</button>
          {canManage && <Link className="connections-button connections-button--primary" to={`/w/${workspaceKey}/connections/new`}><Plus aria-hidden="true" size={16} />{text.add}</Link>}
        </div>
      </header>
      <div className="sr-only" role="status" aria-atomic="true">{announcement}</div>
      {fixture && <div className="connections-fixture" role="note"><strong>{text.fixture}</strong><span>{text.fixtureNote}</span></div>}

      {state.phase === "ready" && <form className="connections-filters" aria-label={text.search} onSubmit={(event) => event.preventDefault()}>
        <label className="connections-search"><span>{text.search}</span><span><Search aria-hidden="true" size={16} /><input type="search" value={query} placeholder={text.searchPlaceholder} onChange={(event) => setQuery(event.target.value)} /></span></label>
        <label><span>{text.status}</span><select value={status} onChange={(event) => setStatus(event.target.value as ConnectionStatus | "all")}><option value="all">{text.all}</option>{connectionStatuses.map((value) => <option key={value} value={value}>{connectionStatusLabel(language, value)}</option>)}</select></label>
        <label><span>{text.owner}</span><select value={owner} onChange={(event) => setOwner(event.target.value)}><option value="all">{text.all}</option>{owners.map((value) => <option key={value}>{value}</option>)}</select></label>
        <button type="button" onClick={clearFilters} disabled={!hasFilters}>{text.clear}</button>
      </form>}

      {state.phase === "loading" && <ConnectionState icon={<RefreshCw className="connections-spinner" aria-hidden="true" />} title={text.loading} busy />}
      {state.phase === "unavailable" && <ConnectionState icon={<AlertTriangle aria-hidden="true" />} title={text.unavailableTitle} body={text.unavailableBody} code={state.result?.stableCode}>{canManage && <Link className="connections-button connections-button--primary" to={`/w/${workspaceKey}/connections/new`}>{text.add}</Link>}</ConnectionState>}
      {state.phase === "forbidden" && <ConnectionState icon={<ShieldAlert aria-hidden="true" />} title={text.forbiddenTitle} body={text.forbiddenBody} alert />}
      {state.phase === "failed" && <ConnectionState icon={<AlertTriangle aria-hidden="true" />} title={text.failedTitle} body={text.failedBody} alert><button className="connections-button connections-button--primary" type="button" onClick={() => void load()}>{text.retry}</button></ConnectionState>}
      {state.phase === "ready" && filtered.length === 0 && <ConnectionState icon={<Inbox aria-hidden="true" />} title={hasFilters ? text.filteredEmptyTitle : text.emptyTitle} body={hasFilters ? text.filteredEmptyBody : text.emptyBody}>{hasFilters && <button className="connections-button" type="button" onClick={clearFilters}>{text.clear}</button>}{!hasFilters && canManage && <Link className="connections-button connections-button--primary" to={`/w/${workspaceKey}/connections/new`}>{text.add}</Link>}</ConnectionState>}
      {state.phase === "ready" && filtered.length > 0 && <ul className="connection-list" aria-busy={state.refreshing}>{filtered.map((item) => <ConnectionCard key={item.connectionId} item={item} language={language} text={text} />)}</ul>}
    </section>
  );
}

function ConnectionState({ icon, title, body, code, busy = false, alert = false, children }: { readonly icon: React.ReactNode; readonly title: string; readonly body?: string; readonly code?: string; readonly busy?: boolean; readonly alert?: boolean; readonly children?: React.ReactNode }): React.JSX.Element {
  return <div className="connections-state" role={alert ? "alert" : "status"} aria-busy={busy || undefined}>{icon}<strong>{title}</strong>{body && <p>{body}</p>}{code && <p><code>{code}</code></p>}{children}</div>;
}

function ConnectionCard({ item, language, text }: { readonly item: ConnectionListItem; readonly language: ConnectionLanguage; readonly text: ReturnType<typeof connectionCopy> }): React.JSX.Element {
  return <li className="connection-card">
    <div className="connection-card__title"><span className={`connection-status connection-status--${statusTone(item.status)}`}><span aria-hidden="true" />{connectionStatusLabel(language, item.status)}</span><strong>{item.displayName}</strong><span>{connectorLabel(language, item.connectorId)}</span></div>
    <dl><div><dt>{text.owner}</dt><dd>{item.ownerLabel}</dd></div><div><dt>{text.updated}</dt><dd><time dateTime={item.updatedAt}>{formatDate(language, item.updatedAt)}</time></dd></div><div><dt><FileKey2 aria-hidden="true" size={14} />Credential</dt><dd>{item.secretReferencePresent ? text.safeCredentials : text.noCredentials}</dd></div></dl>
    <button type="button" disabled title={text.open}>{text.open}</button>
  </li>;
}

interface ConnectionEditorProps { readonly workspaceKey: string; readonly api?: ConnectionCatalogPort; readonly fixture?: boolean; }
interface EditorFields { connectorId: ConnectorId; displayName: string; profileRef: string; secretRef: string; templateVersion: string; }
type FieldErrors = Partial<Record<keyof EditorFields, string>>;
const referencePattern = /^[a-z][a-z0-9_.-]{2,79}$/;

interface ConnectionDraft {
  readonly connectorId: ConnectorId;
  readonly displayName: string;
  readonly profileRef: string;
  readonly templateVersion: string;
}

function draftKey(workspaceKey: string): string { return `custometry:w33:connection-draft:${workspaceKey}`; }

function readDraft(workspaceKey: string): ConnectionDraft | undefined {
  try {
    const value = window.sessionStorage.getItem(draftKey(workspaceKey));
    if (!value) return undefined;
    const draft = JSON.parse(value) as Partial<ConnectionDraft>;
    if (!connectorIds.includes(draft.connectorId as ConnectorId)) return undefined;
    if (typeof draft.displayName !== "string" || typeof draft.profileRef !== "string" || typeof draft.templateVersion !== "string") return undefined;
    return draft as ConnectionDraft;
  } catch {
    return undefined;
  }
}

export function ConnectionEditor({ workspaceKey, api = w14SourceIntakeApi, fixture = false }: ConnectionEditorProps): React.JSX.Element {
  const { i18n } = useTranslation();
  const language: ConnectionLanguage = i18n.resolvedLanguage === "ru" ? "ru" : "en";
  const text = connectionCopy(language);
  const [capabilities, setCapabilities] = useState<ConnectionCapabilities>();
  const [phase, setPhase] = useState<"loading" | "ready" | "forbidden" | "failed">("loading");
  const [fields, setFields] = useState<EditorFields>({ connectorId: "postgresql", displayName: "", profileRef: "", secretRef: "", templateVersion: "" });
  const [errors, setErrors] = useState<FieldErrors>({});
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");
  const [testResult, setTestResult] = useState<{ readonly driver: string; readonly readOnly: boolean; readonly objectCount: number; readonly name: string }>();
  const summaryRef = useRef<HTMLDivElement>(null);

  useEffect(() => { void api.capabilities().then((value) => { setCapabilities(value); setPhase(value.permissions.has("connection.read_metadata") ? "ready" : "forbidden"); }).catch((error) => setPhase(error instanceof ConnectionsApiError && (error.status === 401 || error.status === 403) ? "forbidden" : "failed")); }, [api]);
  useEffect(() => {
    const draft = readDraft(workspaceKey);
    if (draft) setFields({ ...draft, secretRef: "" });
  }, [workspaceKey]);
  const canManage = capabilities?.permissions.has("connection.manage") ?? false;
  const templateMode = fields.connectorId === "csv_template" || fields.connectorId === "xlsx_template";
  const realMode = fields.connectorId === "postgresql";
  const setField = <K extends keyof EditorFields>(key: K, value: EditorFields[K]): void => {
    setFields((current) => ({ ...current, [key]: value }));
    setErrors((current) => { const next = { ...current }; delete next[key]; return next; });
    setTestResult(undefined);
  };

  const validate = (forTest: boolean): FieldErrors => {
    const next: FieldErrors = {};
    if (!fields.displayName.trim()) next.displayName = text.required;
    if (realMode) {
      if (!fields.profileRef.trim()) next.profileRef = text.required; else if (!referencePattern.test(fields.profileRef)) next.profileRef = text.invalidReference;
      if (!fields.secretRef.trim()) next.secretRef = text.required; else if (!referencePattern.test(fields.secretRef)) next.secretRef = text.invalidReference;
    }
    if (templateMode && !fields.templateVersion.trim()) next.templateVersion = text.required;
    if (forTest && !realMode) next.connectorId = text.unsupported;
    return next;
  };

  const focusErrors = (next: FieldErrors): void => {
    setErrors(next);
    window.requestAnimationFrame(() => summaryRef.current?.focus());
  };
  const saveDraft = (): void => {
    const next = validate(false);
    if (Object.keys(next).length > 0) { focusErrors(next); return; }
    const draft: ConnectionDraft = { connectorId: fields.connectorId, displayName: fields.displayName, profileRef: fields.profileRef, templateVersion: fields.templateVersion };
    try { window.sessionStorage.setItem(draftKey(workspaceKey), JSON.stringify(draft)); }
    catch { /* The in-memory form remains usable when browser storage is unavailable. */ }
    setMessage(text.draftSaved);
  };
  const testAndSave = async (): Promise<void> => {
    const next = validate(true); if (Object.keys(next).length > 0) { focusErrors(next); return; }
    setPending(true); setMessage(text.saving); setTestResult(undefined);
    try {
      const created = await api.create({ connector_id: "postgresql", display_name: fields.displayName.trim(), profile_ref: fields.profileRef, secret_ref: fields.secretRef });
      const [tested, catalog] = await Promise.all([api.test(created.connection_id), api.discover(created.connection_id)]);
      setFields((current) => ({ ...current, secretRef: "" }));
      setTestResult({ driver: `${tested.capabilities.driver} ${tested.capabilities.driver_version}`, readOnly: tested.capabilities.read_only_enforced, objectCount: catalog.objects.length, name: tested.connection.display_name });
      setMessage(text.testReady);
    } catch (error) { setMessage(`${text.testFailed} ${text.stableCode}: ${error instanceof ConnectionsApiError ? error.code : "SOURCE_INTAKE_UNAVAILABLE"}`); }
    finally { setPending(false); }
  };

  if (phase === "loading") return <section className="connections"><ConnectionState icon={<RefreshCw className="connections-spinner" aria-hidden="true" />} title={text.loading} busy /></section>;
  if (phase === "forbidden") return <section className="connections"><h1 tabIndex={-1}>{text.editorTitle}</h1><ConnectionState icon={<ShieldAlert aria-hidden="true" />} title={text.forbiddenTitle} body={text.forbiddenBody} alert /></section>;
  if (phase === "failed") return <section className="connections"><h1 tabIndex={-1}>{text.editorTitle}</h1><ConnectionState icon={<AlertTriangle aria-hidden="true" />} title={text.failedTitle} body={text.failedBody} alert /></section>;

  return <section className="connections connection-editor" aria-labelledby="connection-editor-title" data-proof-boundary={fixture ? "presentation-fixture" : "w14-production-adapter"}>
    <Link className="connections-back" to={`/w/${workspaceKey}/connections`}>← {text.back}</Link>
    <header className="connections-heading"><div><span className="connections-eyebrow"><Database aria-hidden="true" size={15} />UI-DATA-002</span><h1 id="connection-editor-title" tabIndex={-1}>{text.editorTitle}</h1><p>{text.editorDescription}</p></div></header>
    {fixture && <div className="connections-fixture" role="note"><strong>{text.fixture}</strong><span>{text.fixtureNote}</span></div>}
    {!canManage && <div className="connections-callout" role="note"><ShieldAlert aria-hidden="true" /><div><strong>{text.permissionTitle}</strong><p>{text.permissionBody}</p></div></div>}
    {Object.keys(errors).length > 0 && <div className="connections-error-summary" ref={summaryRef} tabIndex={-1} role="alert"><strong>{text.validationTitle}</strong><ul>{Object.entries(errors).map(([key, value]) => <li key={key}><a href={`#connection-${key}`}>{value}</a></li>)}</ul></div>}
    <form className="connection-form" onSubmit={(event) => event.preventDefault()} noValidate>
      <div className="connection-field"><label htmlFor="connection-connectorId">{text.connector}</label><select id="connection-connectorId" value={fields.connectorId} onChange={(event) => setField("connectorId", event.target.value as ConnectorId)} aria-invalid={Boolean(errors.connectorId)} aria-describedby={errors.connectorId ? "connection-connectorId-error" : undefined}>{connectorIds.map((id) => <option key={id} value={id}>{connectorLabel(language, id)}</option>)}</select>{errors.connectorId && <small id="connection-connectorId-error" className="connection-field-error">{errors.connectorId}</small>}</div>
      <div className="connection-field"><label htmlFor="connection-displayName">{text.displayName}</label><input id="connection-displayName" value={fields.displayName} maxLength={160} onChange={(event) => setField("displayName", event.target.value)} aria-invalid={Boolean(errors.displayName)} aria-describedby={errors.displayName ? "connection-displayName-error" : undefined} />{errors.displayName && <small id="connection-displayName-error" className="connection-field-error">{errors.displayName}</small>}</div>
      {realMode && <><div className="connection-field"><label htmlFor="connection-profileRef">{text.profileRef}</label><input id="connection-profileRef" value={fields.profileRef} autoComplete="off" spellCheck={false} onChange={(event) => setField("profileRef", event.target.value)} aria-invalid={Boolean(errors.profileRef)} aria-describedby={`connection-profile-hint${errors.profileRef ? " connection-profileRef-error" : ""}`} /><small id="connection-profile-hint">{text.profileHint}</small>{errors.profileRef && <small id="connection-profileRef-error" className="connection-field-error">{errors.profileRef}</small>}</div>
      <div className="connection-field"><label htmlFor="connection-secretRef">{text.secretRef}</label><input id="connection-secretRef" value={fields.secretRef} type="text" autoComplete="off" spellCheck={false} onChange={(event) => setField("secretRef", event.target.value)} aria-invalid={Boolean(errors.secretRef)} aria-describedby={`connection-secret-hint${errors.secretRef ? " connection-secretRef-error" : ""}`} /><small id="connection-secret-hint">{text.secretHint}</small>{errors.secretRef && <small id="connection-secretRef-error" className="connection-field-error">{errors.secretRef}</small>}</div></>}
      {templateMode && <div className="connection-field"><label htmlFor="connection-templateVersion">{text.templateVersion}</label><input id="connection-templateVersion" value={fields.templateVersion} onChange={(event) => setField("templateVersion", event.target.value)} aria-invalid={Boolean(errors.templateVersion)} aria-describedby={`connection-template-hint${errors.templateVersion ? " connection-templateVersion-error" : ""}`} /><small id="connection-template-hint">{text.templateHint}</small>{errors.templateVersion && <small id="connection-templateVersion-error" className="connection-field-error">{errors.templateVersion}</small>}</div>}
      {!realMode && <div className="connections-callout" role="note"><Clock3 aria-hidden="true" /><div><strong>{text.unsupportedTitle}</strong><p>{text.unsupportedBody}</p></div></div>}
      <div className="connection-form__actions"><button type="button" className="connections-button" onClick={saveDraft}>{text.saveDraft}</button><button type="button" className="connections-button connections-button--primary" disabled={!canManage || pending || !realMode} onClick={() => void testAndSave()}>{pending && <RefreshCw className="connections-spinner" aria-hidden="true" size={16} />}{pending ? text.saving : text.testSave}</button></div>
    </form>
    <div className="connections-live" role="status" aria-live="polite">{message}</div>
    {testResult && <section className="connection-test-result" aria-labelledby="connection-test-title"><CheckCircle2 aria-hidden="true" /><div><h2 id="connection-test-title">{text.testReady}</h2><p>{testResult.name} · {text.redaction}</p><dl><div><dt>{text.driver}</dt><dd>{testResult.driver}</dd></div><div><dt>{text.readOnly}</dt><dd>{testResult.readOnly ? text.yes : text.no}</dd></div><div><dt>Catalog</dt><dd>{testResult.objectCount} {text.objects}</dd></div></dl></div></section>}
  </section>;
}
