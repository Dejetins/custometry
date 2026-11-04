import { QueryCache, QueryClient } from '@tanstack/react-query';
import { draftReports, type reportSales } from '@custometry/contracts';

const cacheSizes=new WeakMap<object,number>();
const reportCache=new QueryCache({onSuccess:(_data,query)=>{
 for(const old of reportCache.getAll()){if(old!==query&&!old.isActive())reportCache.remove(old);}
 let bytes=0;let entries=0;
 for(const item of reportCache.getAll()){
  const data=item.state.data;if(data===undefined)continue;entries++;
  let size=typeof data==='object'&&data!==null?cacheSizes.get(data):undefined;
  if(size===undefined){size=new TextEncoder().encode(JSON.stringify(data,(_key,value)=>value instanceof Map?[...value.entries()]:value)).byteLength;if(typeof data==='object'&&data!==null)cacheSizes.set(data,size);}
  bytes+=size;
 }
 const attemptedBytes=bytes;
 if(bytes>16*1024*1024||entries>32){const rejected=query.state.data;bytes-=typeof rejected==='object'&&rejected!==null?cacheSizes.get(rejected)??0:0;entries--;query.setState({data:undefined,error:new Error('REPORT_CACHE_BUDGET'),status:'error'});}
 // One aggregate observation, bounded independently of the browser performance buffer.
 if(typeof performance.measure==='function'){performance.clearMeasures('custometry.report.cache');performance.measure('custometry.report.cache',{start:performance.now(),end:performance.now(),detail:{bytes,entries,attemptedBytes,admitted:query.state.status==='success'}});}
}});
export const reportQueries = new QueryClient({ queryCache:reportCache, defaultOptions: { queries: { retry: false, staleTime: 0, gcTime: 0 }, mutations: { retry: false } } });
let generation = 0;
let denied = false;
let reconciling = false;
const listeners = new Set<() => void>();
let interactiveUntil = 0;
export function noteReportInteraction(): void { if(document.visibilityState === 'visible') interactiveUntil=performance.now()+1000; }
if(typeof window !== 'undefined') {
 window.addEventListener('pointerdown',event=>{if(event.isTrusted)noteReportInteraction();},true);
 window.addEventListener('keydown',event=>{if(event.isTrusted)noteReportInteraction();},true);
}

export const accessStore = { subscribe: (fn: () => void) => { listeners.add(fn); return () => { listeners.delete(fn); }; }, get: () => denied, reconciling: () => reconciling };
export function clearReportAccess(block = true, preserveDraft = false): void {
  generation += 1; denied = block; reconciling = !block && preserveDraft;
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
  const headers=new Headers(init?.headers);
  if(document.visibilityState==='visible'&&performance.now()<interactiveUntil){
    headers.set('X-Custometry-Activity','interactive');headers.set('X-CSRF-Token',csrf());
  }
  const response = await fetch(input, { ...init, headers, credentials: 'same-origin', cache: 'no-store' });
  if (response.status === 401 || response.status === 403) clearReportAccess();
  if (epoch !== generation || denied) throw new ReportError(response.status, 'ACCESS_DENIED');
  response.json=async()=>{
    const limit=String(input).includes('/results/')?2*1024*1024:16*1024*1024;
    const reader=response.body?.getReader();if(!reader)throw new ReportError(response.status,'EMPTY_RESPONSE');
    let total=0;const chunks:Uint8Array[]=[];
    try{while(true){const part=await reader.read();if(part.done)break;total+=part.value.byteLength;
      if(total>limit)throw new ReportError(413,'RESPONSE_PAYLOAD_LIMIT');chunks.push(part.value);
    }}catch(error){await reader.cancel();throw error;}
    if(epoch!==generation||denied)throw new ReportError(response.status,'ACCESS_DENIED');
    const bytes=new Uint8Array(total);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
    chunks.length=0;const payload:unknown=JSON.parse(new TextDecoder().decode(bytes));
    // Decoded wire bytes already account for this immutable response object.
    if(typeof payload==='object'&&payload!==null)cacheSizes.set(payload,total);
    if(epoch!==generation||denied)throw new ReportError(response.status,'ACCESS_DENIED');return payload;
  };
  return response;
};
async function request<T>(url: string, input?: unknown): Promise<T> {
  const response = await protectedFetch(url, { method: input === undefined ? 'GET' : 'POST',
    headers: input === undefined ? {} : { 'Content-Type': 'application/json', 'X-CSRF-Token': csrf() },
    ...(input === undefined ? {} : {body: JSON.stringify(input)}) });
  if (!response.ok) { const payload = await response.json().catch(() => ({})) as {code?: string}; throw new ReportError(response.status, payload.code ?? 'UNAVAILABLE'); }
  return response.json() as Promise<T>;
}
export interface Actor { workspace_id: string; principal_id: string; permissions: readonly string[] }
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
