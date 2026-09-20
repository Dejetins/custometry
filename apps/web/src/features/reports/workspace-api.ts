import {configuredReports as W, workspaceCalendar as C} from '@custometry/contracts';
import {protectedFetch} from './report-api';
export const workspaceReports = new W.WorkspaceReportClient('/api/reports', protectedFetch);
export const workspaceCalendar = new C.WorkspaceCalendarClient('/api/semantic', protectedFetch);
export interface WorkspaceContext {stores:readonly {id:string;label:string}[];metrics:readonly (W.MetricRef & {unit:string})[]}
async function read<T>(path:string):Promise<T>{const response=await protectedFetch('/api/analytics/metric-workspace/v2'+path);if(!response.ok){const e=await response.json() as {code:string};throw new W.WorkspaceRequestError(e.code,response.status,false);}return response.json() as Promise<T>;}
export const workspaceContext=(dataset:string)=>read<WorkspaceContext>(`/datasets/${encodeURIComponent(dataset)}/context`);
export async function workspaceResults(dataset:string,bindings:readonly W.CardResultBinding[]):Promise<ReadonlyMap<string,W.WorkspaceResultV2>>{
 const results=await Promise.all([...new Set(bindings.map(b=>b.result.result_id))].map(id=>read<W.WorkspaceResultV2>(`/datasets/${encodeURIComponent(dataset)}/results/${encodeURIComponent(id)}`)));
 for(const binding of bindings){const r=results.find(r=>r.result_id===binding.result.result_id);if(!r||r.manifest.content_hash!==binding.result.manifest.content_hash||r.manifest.artifact_id!==binding.result.manifest.artifact_id||!r.metric_refs.some(m=>m.version_id===binding.metric_ref.version_id&&m.content_hash===binding.metric_ref.content_hash))throw Error('RESULT_BINDING_MISMATCH');}
 return new Map(results.map(r=>[r.result_id,r]));
}
export function queryIdentity(d:W.ConfiguredReportV2):string{return JSON.stringify([d.semantic_dataset_version_id,d.calendar_basis,d.calendar_ref,d.common_context,d.grain,d.selection?.mode==='single'?d.selection.temporal:'none',d.worksets.flatMap(s=>s.cards.map(c=>[c.card_id,c.metric_ref,c.local_store_ids])).sort((a,b)=>String(a[0]).localeCompare(String(b[0])))]);}
export function move<T>(items:readonly T[],index:number,delta:number):T[]{const next=[...items];const target=index+delta;if(target<0||target>=next.length)return next;[next[index],next[target]]=[next[target],next[index]];return next;}
export function copyWorkset(set:W.Workset):W.Workset{return {...set,workset_id:crypto.randomUUID(),cards:set.cards.map(c=>({...c,card_id:crypto.randomUUID()}))};}
export function orderedResultIds(definition:W.ConfiguredReportV2,bindings:readonly W.CardResultBinding[]):string[]{return definition.worksets.flatMap(s=>s.cards.map(card=>{const binding=bindings.find(b=>b.card_id===card.card_id);if(!binding)throw Error('INCOMPLETE_CARD_BINDINGS');return binding.result.result_id;}));}

export function viewDefinition(base:W.ConfiguredReportV2,view:W.SavedViewV1):W.ConfiguredReportV2{return {...base,calendar_ref:view.calendar_ref,calendar_basis:view.calendar_basis,common_context:{starts_on:view.query_context.starts_on,ends_on:view.query_context.ends_on,store_ids:view.query_context.store_ids},grain:view.query_context.grain,default_workset_id:view.display.active_workset_id,selection:view.display.selection,worksets:base.worksets.map(set=>({...set,cards:[...set.cards].sort((a,b)=>view.display.card_order.indexOf(a.card_id)-view.display.card_order.indexOf(b.card_id))}))};}
