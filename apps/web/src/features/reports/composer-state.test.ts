import {withBlockComparison} from './composer-temporal';
import {describe,it,expect} from 'vitest';
import {duplicate,removeBlock,queryKey,projectionDefinition,type Definition} from './composer-state';
const id=()=>crypto.randomUUID();
function fixture():Definition {
 const doc=id(),page=id(),section=id(),source=id(),metric={metric_id:'net_revenue' as const,version_id:id(),content_hash:'a'.repeat(64)},ref={id:id(),content_hash:'a'.repeat(64)};
 return {document_id:doc,creator_principal_id:id(),profile:'workbook_report',title:'Test',default_page_id:page,brand_profile:ref,company_pack:ref,
 pages:[{page_id:page,order:0,title:'Overview',layout:'dashboard_grid'}],sections:[{section_id:section,page_id:page,order:0,title:'Results'}],
 definitions:[{definition_id:source,query:{semantic_dataset_version_id:id(),common:{starts_on:'2025-01-01',ends_on:'2025-01-31',store_ids:null},local_store_ids:null,grain:'day',calendar_ref:{version_id:id(),content_hash:'a'.repeat(64)},calendar_basis:'calendar',alignment:'none',metric_refs:[metric]}}],
 blocks:[{block_id:id(),section_id:section,order:0,block_type:'table',source:{definition_id:source,metric_ref:metric},presentation:{title:'Table'},placement:{column:0,span:6,row:0,row_span:1}}]};
}
describe('composer authoring state',()=>{
 it('duplicates independent inputs and allocates a nonoverlapping destination',()=>{
  const d=fixture(),before=JSON.stringify(d),next=duplicate(d,d.blocks[0].block_id),copy=next.blocks[1];
  expect(copy.block_id).not.toBe(d.blocks[0].block_id);expect(copy.source!.definition_id).not.toBe(d.blocks[0].source!.definition_id);
  expect(copy.placement).toEqual({column:6,span:6,row:0,row_span:1});expect(queryKey(next,copy)).toBe(queryKey(d,d.blocks[0]));expect(JSON.stringify(d)).toBe(before);
 });
 it('presentation changes preserve semantic identity; grain changes invalidate it',()=>{
  const d=fixture(),key=queryKey(d,d.blocks[0]);const changed={...d,blocks:[{...d.blocks[0],presentation:{title:'Other'},placement:{column:6,span:6,row:0}}]};
  expect(queryKey(changed,changed.blocks[0])).toBe(key);const semantic={...changed,definitions:[{...changed.definitions[0],query:{...changed.definitions[0].query,grain:'month' as const}}]};expect(queryKey(semantic,semantic.blocks[0])).not.toBe(key);
 });
 it('removes unreferenced inputs and projects a standalone table without inventing values',()=>{
  const d=fixture(),projection=projectionDefinition(d,d.blocks[0]);expect(projection.worksets[0].cards[0].card_id).toBe(d.blocks[0].block_id);expect(projection.selection?.mode).toBe('single');
  expect(removeBlock(d,d.blocks[0].block_id).definitions).toEqual([]);
 });
});

describe('C04 scope lifecycle',()=>{
 it('isolates block invalidation and preserves result-context projection',()=>{
  let d=fixture();d=duplicate(d,d.blocks[0].block_id);const first=d.blocks[0],second=d.blocks[1],base=queryKey(d,second);
  const changed:Definition={...d,scopes:{contexts:[{binding_id:id(),target:{kind:'block',id:first.block_id},context:{grain:'month',alignment:'previous_year_same_dates'}}]}};
  expect(queryKey(changed,first)).not.toBe(queryKey(d,first));expect(queryKey(changed,second)).toBe(base);
  const q=d.definitions[0].query;const projection=projectionDefinition(changed,first,{...q.common,store_ids:['a'],grain:'month',calendar_ref:q.calendar_ref,calendar_basis:q.calendar_basis,alignment:'previous_year_same_dates'});
  expect(projection.grain).toBe('month');expect(projection.common_context.store_ids).toEqual(['a']);expect(projection.selection?.mode==='single'&&projection.selection.temporal).toBe('previous_year_same_dates');
 });
 it('invalidates reversed nested scope precedence while retaining unscoped layout identity',()=>{
  const base=fixture(),outer=base.sections[0],inner={...outer,section_id:id(),parent_section_id:outer.section_id,title:'Inner'};
  const nested:Definition={...base,sections:[outer,inner],blocks:[{...base.blocks[0],section_id:inner.section_id}]};
  const scoped:Definition={...nested,scopes:{contexts:[{binding_id:id(),target:{kind:'section',id:outer.section_id},context:{grain:'month'}},{binding_id:id(),target:{kind:'section',id:inner.section_id},context:{grain:'day'}}]}};
  const reverse=(d:Definition):Definition=>({...d,sections:[{...outer,parent_section_id:inner.section_id},{...inner,parent_section_id:null}],blocks:[{...d.blocks[0],section_id:outer.section_id}]});
  expect(queryKey(scoped,scoped.blocks[0])).not.toBe(queryKey(reverse(scoped),reverse(scoped).blocks[0]));
  expect(queryKey(nested,nested.blocks[0])).toBe(queryKey(reverse(nested),reverse(nested).blocks[0]));
 });
 it('copies local and incoming linked constraints independently without external target effects',()=>{
  let d=fixture();d=duplicate(d,d.blocks[0].block_id);const first=d.blocks[0],second=d.blocks[1],dataset=d.definitions[0].query.semantic_dataset_version_id;
  d={...d,scopes:{filters:[{binding_id:id(),target:{kind:'block',id:first.block_id},order:0,filter:{semantic_dataset_version_id:dataset,expression:{kind:'store_in',values:['a']}},linked_target_block_ids:[second.block_id]}]}};
  const copied=duplicate(d,second.block_id),copy=copied.blocks[2],local=copied.scopes!.filters!.find(f=>f.target.id===copy.block_id)!;
  expect(local.filter.expression).toEqual(d.scopes!.filters![0].filter.expression);expect(local.binding_id).not.toBe(d.scopes!.filters![0].binding_id);expect(local.linked_target_block_ids).toEqual([]);
  expect(copied.scopes!.filters![0].linked_target_block_ids).toEqual([second.block_id]);
  const donorCopy=duplicate(d,first.block_id);expect(donorCopy.scopes!.filters!.find(f=>f.target.id===donorCopy.blocks[2].block_id)?.linked_target_block_ids).toEqual([]);
 });
 it('prunes deleted targets and retains scopes during in-place block editing',()=>{
  let d=fixture();d=duplicate(d,d.blocks[0].block_id);const block=d.blocks[0];d={...d,scopes:{contexts:[{binding_id:id(),target:{kind:'block',id:block.block_id},context:{grain:'month'}}]}};
  expect(removeBlock(d,block.block_id).scopes?.contexts).toEqual([]);expect(removeBlock(d,block.block_id,true).scopes?.contexts).toEqual(d.scopes?.contexts);
  const locked:Definition={...d,scopes:{contexts:[{...d.scopes!.contexts![0],locked_fields:['grain']}]}};expect(()=>removeBlock(locked,block.block_id)).toThrow('Locked scope constraint');
 });
});

describe('Receipt scope lifecycle',()=>{
 const receipt=(d:Definition,target:string)=>({binding_id:id(),target:{kind:'block' as const,id:target},order:0,semantic_dataset_version_id:d.definitions[0].query.semantic_dataset_version_id,filter:{registry_version_id:id(),expression:{kind:'predicate' as const,field_id:'Receipt.status',field_version_id:id(),operator:'eq' as const,values:[{data_type:'string' as const,value:'completed'}]}}});
 it('invalidates local and linked blocks while leaving unrelated and layout identity intact',()=>{
  let d=fixture();d=duplicate(d,d.blocks[0].block_id);d=duplicate(d,d.blocks[0].block_id);const [a,b,c]=d.blocks;
  const next:Definition={...d,scopes:{schema_version:'composer-scopes/v2',receipt_filters:[{...receipt(d,a.block_id),linked_target_block_ids:[b.block_id]}]}};
  expect(queryKey(next,a)).not.toBe(queryKey(d,a));expect(queryKey(next,b)).not.toBe(queryKey(d,b));expect(queryKey(next,c)).toBe(queryKey(d,c));
  expect(queryKey({...next,title:'Other'},a)).toBe(queryKey(next,a));
 });
 it('duplicates incoming Receipt constraints independently and prunes removed links',()=>{
  let d=fixture();d=duplicate(d,d.blocks[0].block_id);const [a,b]=d.blocks;
  d={...d,scopes:{schema_version:'composer-scopes/v2',receipt_filters:[{...receipt(d,a.block_id),linked_target_block_ids:[b.block_id]}]}};
  const copied=duplicate(d,b.block_id),scope=copied.scopes?.schema_version==='composer-scopes/v2'?copied.scopes.receipt_filters:[];
  expect(scope).toHaveLength(2);expect(scope?.[1].target.id).toBe(copied.blocks[2].block_id);expect(scope?.[1].linked_target_block_ids).toEqual([]);expect(scope?.[1].filter).toEqual(scope?.[0].filter);
  const removed=removeBlock(d,b.block_id);expect(removed.scopes?.schema_version==='composer-scopes/v2'&&removed.scopes.receipt_filters?.[0].linked_target_block_ids).toEqual([]);
 });
 it('preserves saved Receipt lock during deletion and in-place edits',()=>{
  const d=fixture(),b=d.blocks[0];const locked:Definition={...d,scopes:{schema_version:'composer-scopes/v2',receipt_filters:[{...receipt(d,b.block_id),locked:true}]}};
  expect(()=>removeBlock(locked,b.block_id)).toThrow('Locked scope constraint');expect(removeBlock(locked,b.block_id,true).scopes).toEqual(locked.scopes);
 });
});

it('stores explicit block comparison at local scope and removes only its fields on inherit',()=>{
 const original=fixture(),id=original.blocks[0].block_id;
 const d:Definition={...original,scopes:{schema_version:'composer-scopes/v1',contexts:[{binding_id:crypto.randomUUID(),target:{kind:'document',id:original.document_id},context:{time_comparison:{mode:'previous_period',previous_period_basis:'local_date_duration',incomplete_period_policy:'exclude'}}},{binding_id:crypto.randomUUID(),target:{kind:'block',id},context:{grain:'month'}}]}};
 const settings={mode:'custom_period' as const,comparison_period:{starts_on:'2024-01-01',ends_on:'2024-01-31'},incomplete_period_policy:'exclude' as const};
 const local=withBlockComparison(d,id,settings,null),binding=local.scopes!.contexts![1];expect(binding.context).toEqual({grain:'month',time_comparison:settings});expect(local.scopes!.contexts![0]).toBe(d.scopes!.contexts![0]);
 const inherited=withBlockComparison(local,id,null,null);expect(inherited.scopes!.contexts![1]).toEqual({...binding,context:{grain:'month'}});
 const none=withBlockComparison(local,id,{mode:'none',incomplete_period_policy:'exclude'},null);expect(none.scopes!.contexts![1].context.time_comparison!.mode).toBe('none');
});
