import {describe,it,expect} from 'vitest';
import type {configuredReports as W} from '@custometry/contracts';
import {copyWorkset,queryIdentity,viewDefinition,orderedResultIds} from './workspace-api';
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
