import {it,expect} from 'vitest';
import type {Definition} from './composer-state';
import {arrangeBlocks} from './composer-layout';
import {overlap,startHistory,record,travel} from './composer-structure';
import {queryKey} from './composer-state';
const id=()=>crypto.randomUUID();
function fixture():Definition{
 const doc=id(),page=id(),section=id(),source=id(),metric={metric_id:'net_revenue' as const,version_id:id(),content_hash:'a'.repeat(64)},ref={id:id(),content_hash:'a'.repeat(64)};
 return {document_id:doc,creator_principal_id:id(),profile:'workbook_report',title:'Document',default_page_id:page,brand_profile:ref,company_pack:ref,chapters:[],pages:[{page_id:page,order:0,title:'One',layout:'dashboard_grid'}],sections:[{section_id:section,page_id:page,order:0,title:'Results'}],definitions:[{definition_id:source,query:{semantic_dataset_version_id:id(),common:{starts_on:'2025-01-01',ends_on:'2025-01-31',store_ids:null},local_store_ids:null,grain:'day',calendar_ref:{version_id:id(),content_hash:'a'.repeat(64)},calendar_basis:'calendar',alignment:'none',metric_refs:[metric]}}],blocks:[{block_id:id(),section_id:section,order:0,block_type:'table',source:{definition_id:source,metric_ref:metric},presentation:{title:'Revenue'},placement:{column:0,span:6,row:0,row_span:1}}]};
}

function three(){const d=fixture();return {...d,blocks:[0,1,2].map((n)=>({...d.blocks[0],block_id:`b${n}`,order:n,placement:{column:n%2*6,span:6,row:Math.floor(n/2),row_span:1}}))};}
it('moves full and half-width blocks, preserving queries, IDs and source data',()=>{const d=three();const sized=arrangeBlocks(d,'b0',{span:12});const next=arrangeBlocks(sized,'b2',{before:'b0'});expect(next.blocks.slice().sort((a,b)=>a.order-b.order).map(b=>b.block_id)).toEqual(['b2','b0','b1']);for(const b of next.blocks){expect(queryKey(next,b)).toBe(queryKey(d,d.blocks.find(o=>o.block_id===b.block_id)!));for(const other of next.blocks.filter(o=>o!==b))expect(overlap(b.placement!,other.placement!)).toBe(false);}expect(d.blocks[0].placement.span).toBe(6);});
it('resizes both dimensions and shifts neighbors without overlap',()=>{const d=three(),next=arrangeBlocks(d,'b0',{span:9,rows:2});expect(next.blocks[0].placement).toEqual({column:0,row:0,span:9,row_span:2});expect(next.blocks[1].placement!.row).toBeGreaterThanOrEqual(2);});
it('preserves locked neighbors and rejects reordering them',()=>{const d=three();d.blocks[1]={...d.blocks[1],locked:true};const next=arrangeBlocks(d,'b0',{span:12});expect(next.blocks[1]).toEqual(d.blocks[1]);expect(()=>arrangeBlocks(d,'b1',{span:3})).toThrow();expect(()=>arrangeBlocks(d,'b2',{before:'b0'})).toThrow();});
it('rejects invalid sizes and cross-section destinations',()=>{const d=three();expect(()=>arrangeBlocks(d,'b0',{span:13})).toThrow();expect(()=>arrangeBlocks(d,'b0',{rows:0})).toThrow();expect(()=>arrangeBlocks(d,'b0',{before:'unknown'})).toThrow();});
it('layout changes participate in undo and redo',()=>{const d=three(),next=arrangeBlocks(d,'b0',{span:3});const history=record(startHistory(d),next);const undo=travel(history,'undo');expect(undo.present).toEqual(d);expect(travel(undo,'redo').present).toEqual(next);});
it('flow pages support reordering without converting layout or scopes',()=>{const base=three();const d:Definition={...base,pages:[{...base.pages[0],layout:'flow'}]};const next=arrangeBlocks(d,'b2',{before:'b0'});expect(next.pages).toEqual(d.pages);expect(next.blocks.find(b=>b.block_id==='b2')!.order).toBe(0);expect(()=>arrangeBlocks(d,'b0',{span:12})).toThrow();});
