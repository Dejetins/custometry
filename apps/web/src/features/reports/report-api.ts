import { QueryClient } from '@tanstack/react-query';
import { draftReports, type reportSales } from '@custometry/contracts';

export const reportQueries = new QueryClient({ defaultOptions: { queries: { retry: false, staleTime: 0, gcTime: 300000 }, mutations: { retry: false } } });
let generation = 0;
let denied = false;
const listeners = new Set<() => void>();
export const accessStore = { subscribe: (fn: () => void) => { listeners.add(fn); return () => { listeners.delete(fn); }; }, get: () => denied };
export function clearReportAccess(block = true): void {
  generation += 1; denied = block;
  reportQueries.clear(); listeners.forEach((fn) => fn());
}
export class ReportError extends Error {
  constructor(public status: number, public code: string) { super(code); }
}
export function csrf(): string {
  return decodeURIComponent(document.cookie.split('; ').find((part) => part.startsWith('custometry_csrf='))?.split('=')[1] ?? '');
}
export const protectedFetch: typeof fetch = async (input, init) => {
  const epoch = generation;
  const response = await fetch(input, { ...init, credentials: 'same-origin', cache: 'no-store' });
  if (response.status === 401 || response.status === 403) clearReportAccess();
  if (epoch !== generation || denied) throw new ReportError(response.status, 'ACCESS_DENIED');
  const json=response.json.bind(response);
  response.json=async()=>{const payload:unknown=await json();if(epoch!==generation||denied)throw new ReportError(response.status,'ACCESS_DENIED');return payload;};
  return response;
};
async function request<T>(url: string, input?: unknown): Promise<T> {
  const response = await protectedFetch(url, { method: input === undefined ? 'GET' : 'POST',
    headers: input === undefined ? {} : { 'Content-Type': 'application/json', 'X-CSRF-Token': csrf() },
    ...(input === undefined ? {} : {body: JSON.stringify(input)}) });
  if (!response.ok) { const payload = await response.json().catch(() => ({})) as {code?: string}; throw new ReportError(response.status, payload.code ?? 'UNAVAILABLE'); }
  return response.json() as Promise<T>;
}
export interface Actor { workspace_id: string; principal_id: string; permissions: string[] }
export const reportApi = {
  me: () => request<Actor>('/api/identity/me'),
  context: () => request<reportSales.SalesContext>('/api/analytics/sales-report-context/v1'),
  run: (input: reportSales.SalesRunRequest) => request<reportSales.SalesResponse>('/api/analytics/sales-reports/v1', input),
  drafts: new draftReports.DraftReportClient('/api/reports', protectedFetch),
  async login(workspace: string, email: string, password: string): Promise<string> {
    const response = await fetch('/api/identity/login', { method: 'POST', credentials: 'same-origin', headers: {'Content-Type':'application/json'}, body: JSON.stringify({workspace_id: workspace, email, password, device_label: 'report-workspace'}) });
    if (!response.ok) throw new ReportError(response.status, 'LOGIN_FAILED');
    const result = await response.json() as {workspace_id: string};
    clearReportAccess(false); return result.workspace_id;
  },
  async logout(): Promise<void> { try { await request('/api/identity/logout', {}); } finally { clearReportAccess(); } },
};
export type Result = reportSales.SalesResponse;
export type Draft = draftReports.DraftResponse;
export type References = draftReports.PreparedResponse;
export function resultOf(draft: Draft): Result { return draft.result as unknown as Result; }
