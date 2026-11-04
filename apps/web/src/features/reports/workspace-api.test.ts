import {describe,it,expect} from 'vitest';
import type {configuredReports as W} from '@custometry/contracts';
import {copyWorkset,queryIdentity,viewDefinition,orderedResultIds,verifiedResultMap} from './workspace-api';
const card=(id:string,stores:string[]|null):W.Card=>({card_id:id,local_store_ids:stores,metric_ref:{metric_id:'net_revenue',version_id:'metric-version',content_hash:'metric-hash'}});
const set:W.Workset={workset_id:'set',name:{ru:'Набор',en:'Set'},visibility:'personal',owner_principal_id:'owner',cards:[card('a',null),card('b',[])]};
const definition:W.ConfiguredReportV2={schema_version:'configured-report/v2',report_id:'report',creator_principal_id:'owner',title:'Report',default_workset_id:'set',base_snapshot_ref:{snapshot_id:'snapshot',version_id:'version',manifest:{artifact_id:'artifact',content_hash:'hash'}},brand_profile:{id:'brand',content_hash:'hash'},company_pack:{id:'pack',content_hash:'hash'},semantic_dataset_version_id:'dataset',calendar_basis:'fiscal',calendar_ref:{version_id:'cal',content_hash:'hash'},common_context:{starts_on:'2025-01-01',ends_on:'2025-01-31',store_ids:null},grain:'month',selection:{mode:'single',card_id:'a',temporal:'none',display:'series'},worksets:[set]};
describe('configured report query/display separation',()=>{
 it('order and labels reuse results, while empty scope, fiscal adoption and grain require Apply',()=>{
  expect(queryIdentity({...definition,title:'Renamed',worksets:[{...set,cards:[...set.cards].reverse()}]})).toBe(queryIdentity(definition));
  expect(queryIdentity({...definition,calendar_ref:{version_id:'next',content_hash:'next'}})).not.toBe(queryIdentity(definition));
  expect(queryIdentity({...definition,grain:'quarter'})).not.toBe(queryIdentity(definition));
  expect(queryIdentity({...definition,worksets:[{...set,cards:[card('a',[]),set.cards[1]]}]})).not.toBe(queryIdentity(definition));
 });
 it('copy preserves immutable formula and inheritance while allocating all instance identities',()=>{
  const copied=copyWorkset(set);expect(copied.workset_id).not.toBe(set.workset_id);
  expect(copied.cards.map(c=>c.card_id)).not.toContain('a');expect(copied.cards.map(c=>c.card_id)).not.toContain('b');
  expect(copied.cards.map(c=>c.metric_ref)).toEqual(set.cards.map(c=>c.metric_ref));expect(copied.cards.map(c=>c.local_store_ids)).toEqual([null,[]]);
 });
});

it('restores the selected view query/calendar/display instead of the base defaults',()=>{
 const view:W.SavedViewV1={schema_version:'saved-view/v1',saved_view_id:'view',version_id:'view-version',revision:2,workspace_id:'workspace',owner_principal_id:'reader',report_id:'report',document_version_id:'document',document_content_hash:'hash',calendar_ref:{version_id:'pinned',content_hash:'pinned-hash'},calendar_basis:'calendar',page_ids:[],result_scope:[],query_context:{starts_on:'2024-04-01',ends_on:'2024-06-30',store_ids:[],grain:'quarter'},display:{active_workset_id:'set',card_order:['b','a'],hidden_card_ids:[],representation:'table',density:'comfortable',selection:{mode:'single',card_id:'b',temporal:'none',display:'series'}}};
 const restored=viewDefinition(definition,view);
 expect(restored.common_context).toEqual({starts_on:'2024-04-01',ends_on:'2024-06-30',store_ids:[]});expect(restored.calendar_ref).toEqual(view.calendar_ref);expect(restored.grain).toBe('quarter');expect(restored.selection).toEqual(view.display.selection);expect(restored.worksets[0].cards.map(c=>c.card_id)).toEqual(['b','a']);
 expect(()=>orderedResultIds(restored,[])).toThrow('INCOMPLETE_CARD_BINDINGS');
});


it('embedded results preserve immutable binding checks without copying inactive data',()=>{
 const metric=card('a',null).metric_ref;
 const binding={card_id:'a',metric_ref:metric,result:{result_id:'r',schema_version:'metric-workspace/v2',manifest:{artifact_id:'artifact',content_hash:'hash'}}} as W.CardResultBinding;
 const result={result_id:'r',manifest:{artifact_id:'artifact',content_hash:'hash'},metric_refs:[metric]} as unknown as W.WorkspaceResultV2;
 const map=verifiedResultMap([binding],[result,{...result,result_id:'inactive'}]);
 expect(map?.size).toBe(1);expect(map?.get('r')).toBe(result);
 expect(verifiedResultMap([binding],[{...result,result_id:'different'}])).toBeUndefined();
 expect(verifiedResultMap([binding],[{...result,manifest:{artifact_id:'artifact',content_hash:'different'}}])).toBeUndefined();
 expect(verifiedResultMap([binding],[{...result,metric_refs:[{...metric,version_id:'different'}]}])).toBeUndefined();
});

it('Add reuses only an unfinished personal default workset and preserves existing sets',async()=>{
 const {newWorkset}=await import('./workspace-api');const original=structuredClone(set);
 const first=newWorkset([set],'owner');expect(first.cards).toEqual([]);
 expect(newWorkset([set,first],'owner')).toBe(first);
 expect(set).toEqual(original);
 const renamed={...first,name:{...first.name,en:'Planned comparison'}};
 expect(newWorkset([set,renamed],'owner').workset_id).not.toBe(first.workset_id);
 const filled={...first,cards:[card('new-card',null)]};
 const second=newWorkset([set,filled],'owner');expect(second.name.en).not.toBe(first.name.en);
 expect(newWorkset([first],'other-owner').workset_id).not.toBe(first.workset_id);
 const old={...first,name:{ru:'Новый набор',en:'New workset'}};
 expect(newWorkset([old],'owner')).toBe(old);
});
it('explicit copies retain data and receive distinct bilingual labels',()=>{
 const one=copyWorkset(set,[set]);const two=copyWorkset(set,[set,one]);
 expect(new Set([set.name.ru,one.name.ru,two.name.ru]).size).toBe(3);
 expect(new Set([set.name.en,one.name.en,two.name.en]).size).toBe(3);
 expect(one.cards.map(c=>c.metric_ref)).toEqual(set.cards.map(c=>c.metric_ref));
 expect(two.cards.map(c=>c.card_id)).not.toEqual(one.cards.map(c=>c.card_id));
});
