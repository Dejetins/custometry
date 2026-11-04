import {describe,it,expect} from 'vitest';
import type {Definition} from './composer-state';
import {queryKey} from './composer-state';
import {structure,descendants,isLocked,isHidden,identity,nodes,overlap,startHistory,record,travel,type Target} from './composer-structure';
const id=()=>crypto.randomUUID();
function fixture():Definition{
 const doc=id(),page=id(),section=id(),source=id(),metric={metric_id:'net_revenue' as const,version_id:id(),content_hash:'a'.repeat(64)},ref={id:id(),content_hash:'a'.repeat(64)};
 return {document_id:doc,creator_principal_id:id(),profile:'workbook_report',title:'Document',default_page_id:page,brand_profile:ref,company_pack:ref,chapters:[],pages:[{page_id:page,order:0,title:'One',layout:'dashboard_grid'}],sections:[{section_id:section,page_id:page,order:0,title:'Results'}],definitions:[{definition_id:source,query:{semantic_dataset_version_id:id(),common:{starts_on:'2025-01-01',ends_on:'2025-01-31',store_ids:null},local_store_ids:null,grain:'day',calendar_ref:{version_id:id(),content_hash:'a'.repeat(64)},calendar_basis:'calendar',alignment:'none',metric_refs:[metric]}}],blocks:[{block_id:id(),section_id:section,order:0,block_type:'table',source:{definition_id:source,metric_ref:metric},presentation:{title:'Revenue'},placement:{column:0,span:6,row:0,row_span:1}}]};
}
function valid(d:Definition){
 const all=(['chapter','page','section','block'] as const).flatMap(k=>nodes(d,k).map(identity));all.push(...d.definitions.map(n=>n.definition_id));expect(new Set(all).size).toBe(all.length);
 for(const b of d.blocks){expect(d.sections.some(s=>s.section_id===b.section_id)).toBe(true);expect(d.definitions.some(s=>s.definition_id===b.source!.definition_id)).toBe(true);if(b.placement)for(const other of d.blocks.filter(o=>o.block_id!==b.block_id&&o.section_id===b.section_id&&o.placement))expect(overlap(b.placement,other.placement!)).toBe(false);}
 expect(d.pages.some(p=>p.page_id===d.default_page_id&&!isHidden(d,{kind:'page',id:p.page_id}))).toBe(true);
}
describe('C03 immutable hierarchy commands',()=>{
 it('chapter add after deletion keeps unique order and locked nodes unchanged',()=>{
  let d=fixture();d=structure(d,{type:'add',kind:'chapter',title:'A'});d=structure(d,{type:'add',kind:'chapter',title:'B'});d=structure(d,{type:'delete',target:{kind:'chapter',id:d.chapters![0].chapter_id}});d=structure(d,{type:'add',kind:'chapter',title:'C'});expect(new Set(d.chapters!.map(c=>c.order)).size).toBe(2);
  const b=d.chapters![0];d=structure(d,{type:'flag',target:{kind:'chapter',id:b.chapter_id},flag:'locked',value:true});expect(()=>structure(d,{type:'reorder',target:{kind:'chapter',id:d.chapters![1].chapter_id},direction:-1})).toThrow('Unlock affected items first');
 });
 it('copies a nested page with fresh node/source IDs and origin, preserving analytical identity',()=>{
  let d=fixture();const page:Target={kind:'page',id:d.pages[0].page_id};d=structure(d,{type:'add',kind:'section',parent:{kind:'section',id:d.sections[0].section_id},title:'Nested'});const before=JSON.stringify(d);
  const next=structure(d,{type:'duplicate',target:page,snapshot:id()});valid(next);expect(JSON.stringify(d)).toBe(before);expect(next.pages).toHaveLength(2);expect(next.sections).toHaveLength(4);expect(next.blocks).toHaveLength(2);
  expect(next.pages[1].copied_from?.node_id).toBe(page.id);expect(next.sections[3].parent_section_id).toBe(next.sections[2].section_id);expect(queryKey(next,next.blocks[1])).toBe(queryKey(d,d.blocks[0]));expect(next.blocks[1].source!.definition_id).not.toBe(d.blocks[0].source!.definition_id);
 });
 it('moves sections across layout types and rejects cycles atomically',()=>{
  let d=fixture();d=structure(d,{type:'add',kind:'page',title:'Two'});const section:Target={kind:'section',id:d.sections[0].section_id};d=structure(d,{type:'add',kind:'section',parent:section,title:'Nested'});const child=d.sections.at(-1)!;
  expect(()=>structure(d,{type:'move',target:section,parent:{kind:'section',id:child.section_id}})).toThrow('Invalid destination');
  const next=structure(d,{type:'move',target:section,parent:{kind:'page',id:d.pages[1].page_id}});valid(next);expect(next.blocks[0].placement).toBeNull();expect(next.sections.find(s=>s.section_id===child.section_id)?.page_id).toBe(d.pages[1].page_id);
 });
 it('preserves custom grid geometry for nested section moves, same-layout selection and block reorder',()=>{
  let d=fixture();const section:Target={kind:'section',id:d.sections[0].section_id};
  d=structure(d,{type:'add',kind:'section',parent:section,title:'Nested'});const nested=d.sections.at(-1)!;
  d=structure(d,{type:'move',target:{kind:'block',id:d.blocks[0].block_id},parent:{kind:'section',id:nested.section_id}});
  const placement={column:3,span:4,row:7,row_span:3};d=structure(d,{type:'placement',block:d.blocks[0].block_id,placement});
  d=structure(d,{type:'add',kind:'page',title:'Grid two'});const page=d.pages.at(-1)!;
  d=structure(d,{type:'layout',page:page.page_id,layout:'dashboard_grid'});const before=JSON.stringify(d);
  let next=structure(d,{type:'move',target:section,parent:{kind:'page',id:page.page_id}});
  expect(next.blocks[0].placement).toEqual(placement);expect(JSON.stringify(d)).toBe(before);valid(next);
  next=structure(next,{type:'move',target:section,parent:{kind:'section',id:next.sections.find(s=>s.page_id===page.page_id&&s.section_id!==section.id&&s.section_id!==nested.section_id)!.section_id}});
  expect(next.blocks[0].placement).toEqual(placement);
  next=structure(next,{type:'layout',page:page.page_id,layout:'dashboard_grid'});
  next=structure(next,{type:'move',target:{kind:'block',id:next.blocks[0].block_id},parent:{kind:'section',id:nested.section_id}});
  expect(next.blocks[0].placement).toEqual(placement);valid(next);
 });
 it('layout, profile, density and history never change analytical identity',()=>{
  const d=fixture(),key=queryKey(d,d.blocks[0]);let h=startHistory(d);
  for(const layout of ['flow','narrative','dashboard_grid'] as const)h=record(h,structure(h.present,{type:'layout',page:d.pages[0].page_id,layout}));
  h=record(h,structure(h.present,{type:'profile',profile:'narrative_research'}));h=record(h,structure(h.present,{type:'density',block:d.blocks[0].block_id,density:'compact'}));
  valid(h.present);expect(queryKey(h.present,h.present.blocks[0])).toBe(key);const end=h.present;for(let i=0;i<5;i++)h=travel(h,'undo');expect(h.present).toEqual(d);for(let i=0;i<5;i++)h=travel(h,'redo');expect(h.present).toEqual(end);
 });
 it('deletion with Undo restores exact IDs, results inputs and subtree order',()=>{
  const d=fixture();const two=structure(d,{type:'duplicate',target:{kind:'page',id:d.pages[0].page_id}});const h=record(startHistory(two),structure(two,{type:'delete',target:{kind:'page',id:d.pages[0].page_id}}));valid(h.present);expect(h.present.blocks).toHaveLength(1);expect(travel(h,'undo').present).toEqual(two);expect(()=>structure(d,{type:'delete',target:{kind:'page',id:d.pages[0].page_id}})).toThrow('Keep one visible page');
 });
 it('locks apply through ancestry and hidden default selects another visible page',()=>{
  let d=fixture();d=structure(d,{type:'duplicate',target:{kind:'page',id:d.pages[0].page_id}});const page:Target={kind:'page',id:d.pages[0].page_id},block:Target={kind:'block',id:d.blocks[0].block_id};
  d=structure(d,{type:'flag',target:page,flag:'hidden',value:true});expect(d.default_page_id).toBe(d.pages[1].page_id);expect(isHidden(d,block)).toBe(true);d=structure(d,{type:'flag',target:page,flag:'locked',value:true});expect(isLocked(d,block)).toBe(true);
  expect(()=>structure(d,{type:'delete',target:block})).toThrow();expect(()=>structure(d,{type:'flag',target:block,flag:'locked',value:false})).toThrow();d=structure(d,{type:'flag',target:page,flag:'locked',value:false});expect(isLocked(d,block)).toBe(false);
 });
 it('rejects overlap/out-of-grid resize and preserves independent reading order',()=>{
  let d=fixture();d=structure(d,{type:'duplicate',target:{kind:'block',id:d.blocks[0].block_id}});const block=d.blocks[0];expect(()=>structure(d,{type:'placement',block:block.block_id,placement:{column:0,span:12,row:0}})).toThrow();expect(()=>structure(d,{type:'placement',block:block.block_id,placement:{column:10,span:6,row:4}})).toThrow();
  const next=structure(d,{type:'placement',block:block.block_id,placement:{column:0,span:12,row:2}});valid(next);expect(next.blocks[0].order).toBe(block.order);expect(queryKey(next,next.blocks[0])).toBe(queryKey(d,block));
 });
 it('groups pages into chapters and bounds history without a document cardinality cap',()=>{
  let d=fixture();d=structure(d,{type:'add',kind:'chapter',title:'Group'});d=structure(d,{type:'move',target:{kind:'page',id:d.pages[0].page_id},parent:{kind:'chapter',id:d.chapters![0].chapter_id}});expect(descendants(d,{kind:'chapter',id:d.chapters![0].chapter_id})).toHaveLength(3);
  let h=startHistory(d);for(let i=0;i<60;i++)h=record(h,structure(h.present,{type:'rename',target:{kind:'page',id:d.pages[0].page_id},title:String(i)}));expect(h.past).toHaveLength(50);expect(h.revision).toBe(60);
 });
});
