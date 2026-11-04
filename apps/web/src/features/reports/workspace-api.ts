import {configuredReports as W, workspaceCalendar as C} from '@custometry/contracts';
import {protectedFetch} from './report-api';
export const workspaceReports = new W.WorkspaceReportClient('/api/reports', protectedFetch);
export const workspaceCalendar = new C.WorkspaceCalendarClient('/api/semantic', protectedFetch);
export interface WorkspaceContext {stores:readonly {id:string;label:string}[];metrics:readonly (W.MetricRef & {unit:string})[]}
async function read<T>(path:string,signal?:AbortSignal):Promise<T>{const response=await protectedFetch('/api/analytics/metric-workspace/v2'+path,{signal});if(!response.ok){const e=await response.json() as {code:string};throw new W.WorkspaceRequestError(e.code,response.status,false);}return response.json() as Promise<T>;}
export const workspaceContext=(dataset:string)=>read<WorkspaceContext>(`/datasets/${encodeURIComponent(dataset)}/context`);
export async function workspaceResults(dataset:string,bindings:readonly W.CardResultBinding[],signal?:AbortSignal):Promise<ReadonlyMap<string,W.WorkspaceResultV2>>{
 if(!bindings.length)return new Map();
 const controller=new AbortController();const abort=()=>controller.abort();if(signal?.aborted)controller.abort();signal?.addEventListener('abort',abort,{once:true});
 const ids=[...new Set(bindings.map(b=>b.result.result_id))];
 if(ids.length>32){signal?.removeEventListener('abort',abort);throw Error('ACTIVE_RESULT_ENTRY_LIMIT');}
 const results:W.WorkspaceResultV2[]=[];let next=0;let bytes=0;
 // One query owns the active payload. Inactive query data is immediately removed.
 // Four in-flight reads, 2 MiB per response and 16 MiB combined admission budget.
 try {await Promise.all(Array.from({length:Math.min(4,ids.length)},async()=>{
  while(next<ids.length){const id=ids[next++];if(controller.signal.aborted)throw new DOMException('Aborted','AbortError');
   const r=await read<W.WorkspaceResultV2>(`/datasets/${encodeURIComponent(dataset)}/results/${encodeURIComponent(id)}`,controller.signal);
   const size=new TextEncoder().encode(JSON.stringify(r)).byteLength;
   bytes+=size;if(size>2*1024*1024||bytes>16*1024*1024)throw Error('ACTIVE_RESULT_PAYLOAD_LIMIT');results.push(r);
  }
 }));}catch(error){controller.abort();throw error;}finally{signal?.removeEventListener('abort',abort);}
 const verified=verifiedResultMap(bindings,results);if(!verified)throw Error('RESULT_BINDING_MISMATCH');return verified;
}
export function verifiedResultMap(bindings:readonly W.CardResultBinding[],results:readonly W.WorkspaceResultV2[]):ReadonlyMap<string,W.WorkspaceResultV2>|undefined{
 if(!bindings.length)return undefined;
 for(const binding of bindings){const r=results.find(r=>r.result_id===binding.result.result_id);if(!r||r.manifest.content_hash!==binding.result.manifest.content_hash||r.manifest.artifact_id!==binding.result.manifest.artifact_id||!r.metric_refs.some(m=>m.version_id===binding.metric_ref.version_id&&m.content_hash===binding.metric_ref.content_hash))return undefined;}
 const active=new Set(bindings.map(b=>b.result.result_id));return new Map(results.filter(r=>active.has(r.result_id)).map(r=>[r.result_id,r]));
}
export function queryIdentity(d:W.ConfiguredReportV2):string{return JSON.stringify([d.semantic_dataset_version_id,d.calendar_basis,d.calendar_ref,d.common_context,d.grain,d.selection?.mode==='single'?d.selection.temporal:'none',d.worksets.flatMap(s=>s.cards.map(c=>[c.card_id,c.metric_ref,c.local_store_ids])).sort((a,b)=>String(a[0]).localeCompare(String(b[0])))]);}
export function move<T>(items:readonly T[],index:number,delta:number):T[]{const next=[...items];const target=index+delta;if(target<0||target>=next.length)return next;[next[index],next[target]]=[next[target],next[index]];return next;}
function uniqueWorksetName(sets:readonly W.Workset[],base:W.Workset['name']):W.Workset['name']{
 for(let n=1;;n++){const name={ru:base.ru.slice(0,185)+' '+n,en:base.en.slice(0,185)+' '+n};if(!sets.some(s=>s.name.ru===name.ru||s.name.en===name.en))return name;}
}
export function unfinishedWorkset(sets:readonly W.Workset[],owner:string):W.Workset|undefined{
 return sets.find(s=>s.owner_principal_id===owner&&s.visibility==='personal'&&s.cards.length===0&&/^New workset(?: [1-9]\d*)?$/.test(s.name.en)&&s.name.ru==='Новый набор'+s.name.en.slice('New workset'.length));
}
export function newWorkset(sets:readonly W.Workset[],owner:string):W.Workset{
 return unfinishedWorkset(sets,owner)??{workset_id:crypto.randomUUID(),owner_principal_id:owner,visibility:'personal',name:uniqueWorksetName(sets,{ru:'Новый набор',en:'New workset'}),cards:[]};
}
export function copyWorkset(set:W.Workset,sets:readonly W.Workset[]=[set]):W.Workset{return {...set,name:uniqueWorksetName(sets,{ru:set.name.ru.slice(0,175)+' — копия',en:set.name.en.slice(0,175)+' — copy'}),workset_id:crypto.randomUUID(),cards:set.cards.map(c=>({...c,card_id:crypto.randomUUID()}))};}
export function orderedResultIds(definition:W.ConfiguredReportV2,bindings:readonly W.CardResultBinding[]):string[]{return definition.worksets.flatMap(s=>s.cards.map(card=>{const binding=bindings.find(b=>b.card_id===card.card_id);if(!binding)throw Error('INCOMPLETE_CARD_BINDINGS');return binding.result.result_id;}));}

export function viewDefinition(base:W.ConfiguredReportV2,view:W.SavedViewV1):W.ConfiguredReportV2{return {...base,calendar_ref:view.calendar_ref,calendar_basis:view.calendar_basis,common_context:{starts_on:view.query_context.starts_on,ends_on:view.query_context.ends_on,store_ids:view.query_context.store_ids},grain:view.query_context.grain,default_workset_id:view.display.active_workset_id,selection:view.display.selection,worksets:base.worksets.map(set=>({...set,cards:[...set.cards].sort((a,b)=>view.display.card_order.indexOf(a.card_id)-view.display.card_order.indexOf(b.card_id))}))};}
