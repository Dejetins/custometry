import {it,expect} from 'vitest';
import type {Definition} from './composer-state';
import {canvasGeometry,canvasRows,canvasDefinition,canvasLayout,commitCanvas,resizeCanvas,addContent} from './composer-canvas';
import {overlap,startHistory,record,travel} from './composer-structure';
import {queryKey} from './composer-state';
const id=()=>crypto.randomUUID();
function fixture():Definition{
 const doc=id(),page=id(),section=id(),source=id(),metric={metric_id:'net_revenue' as const,version_id:id(),content_hash:'a'.repeat(64)},ref={id:id(),content_hash:'a'.repeat(64)};
 return {document_id:doc,creator_principal_id:id(),profile:'workbook_report',title:'Document',default_page_id:page,brand_profile:ref,company_pack:ref,chapters:[],pages:[{page_id:page,order:0,title:'One',layout:'dashboard_grid'}],sections:[{section_id:section,page_id:page,order:0,title:'Results'}],definitions:[{definition_id:source,query:{semantic_dataset_version_id:id(),common:{starts_on:'2025-01-01',ends_on:'2025-01-31',store_ids:null},local_store_ids:null,grain:'day',calendar_ref:{version_id:id(),content_hash:'a'.repeat(64)},calendar_basis:'calendar',alignment:'none',metric_refs:[metric]}}],blocks:[{block_id:id(),section_id:section,order:0,block_type:'table',source:{definition_id:source,metric_ref:metric},presentation:{title:'Revenue'},placement:{column:0,span:6,row:0,row_span:1}}]};
}

it('migrates legacy geometry once without changing analytical identity',()=>{const old=fixture(),d=canvasDefinition(old);expect(d.grid_columns).toBe(24);expect(d.blocks[0].placement).toEqual({column:0,span:12,row:0,row_span:8});expect(canvasDefinition(d)).toBe(d);expect(queryKey(d,d.blocks[0])).toBe(queryKey(old,old.blocks[0]));});
it('places text and filters in the shared grid; history restores additions',()=>{const d=canvasDefinition(fixture()),text=addContent(d,d.sections[0].section_id,'text','ru'),next=addContent(text,d.sections[0].section_id,'filter','ru');expect(next.blocks).toHaveLength(3);for(const b of next.blocks)for(const other of next.blocks.filter(o=>o!==b))expect(overlap(b.placement!,other.placement!)).toBe(false);expect(travel(record(startHistory(d),next),'undo').present).toEqual(d);});
it('keyboard size changes preserve locked neighbors and reject overlaps',()=>{const d=canvasDefinition(fixture()),text=addContent(d,d.sections[0].section_id,'text','en');const locked={...text,blocks:text.blocks.map((b,i)=>i?{...b,locked:true}:b)};expect(()=>resizeCanvas(locked,d.blocks[0].block_id,{row_span:12})).toThrow();expect(resizeCanvas(locked,d.blocks[0].block_id,{span:24}).blocks[1]).toEqual(locked.blocks[1]);});
it('rejects incomplete gesture layouts and preserves keys on moves',()=>{const d=canvasDefinition(fixture()),layout=canvasLayout(d,d.sections[0].section_id);expect(()=>commitCanvas(d,d.sections[0].section_id,[])).toThrow();layout[0].x=1;const next=commitCanvas(d,d.sections[0].section_id,layout);expect(next.blocks[0].placement?.column).toBe(1);expect(queryKey(next,next.blocks[0])).toBe(queryKey(d,d.blocks[0]));});

it('rejects moving or resizing into unlocked neighbors without displacing them',()=>{
 const d=canvasDefinition(fixture()),next=addContent(d,d.sections[0].section_id,'text','en'),before=structuredClone(next),block=next.blocks[0];
 expect(()=>resizeCanvas(next,block.block_id,{row:1})).toThrow('Overlap');
 expect(()=>resizeCanvas(next,block.block_id,{row_span:9})).toThrow('Overlap');
 expect(next).toEqual(before);
 const moved=resizeCanvas(next,block.block_id,{row:10});
 expect(moved.blocks[0].placement?.row).toBe(10);
 expect(moved.blocks[1]).toEqual(next.blocks[1]);
});

it('keeps row height stable across notebook and large monitor widths',()=>{for(const width of [600,940,1200,2200,2622])expect(canvasRows(width)).toBe(40);});

it('keeps minimum metric pixels at laptop and large widths without changing cell positions',()=>{
 const d=canvasDefinition(fixture());const metric={...d.blocks[0],block_type:'metric' as const,placement:{column:16,row:2,span:4,row_span:3}};
 for(const viewport of [940,1010,1800]){
  const g=canvasGeometry([metric],viewport);
  expect((g.width+6)/24*4-6).toBeGreaterThanOrEqual(140);
  expect((g.rowHeight+6)*3-6).toBeGreaterThanOrEqual(140);
  expect(g.metricMinW).toBeLessThanOrEqual(4);
 }
 expect(metric.placement).toEqual({column:16,row:2,span:4,row_span:3});
 expect(canvasGeometry([{...metric,placement:{...metric.placement,span:8}}],940).width).toBe(940);
 expect(canvasGeometry([],940)).toMatchObject({width:940,rowHeight:40});
});

it('permits four-column metrics on a notebook without enlarging the canvas',()=>{
 const d=canvasDefinition(fixture());const metric={...d.blocks[0],block_type:'metric' as const,placement:{column:16,row:2,span:4,row_span:3}};
 const geometry=canvasGeometry([metric],940);
 expect(geometry.width).toBe(940);expect(geometry.metricMinW).toBe(4);
 expect(canvasLayout({...d,blocks:[metric]},metric.section_id,940)[0].minW).toBe(4);
 expect(geometry.rowHeight).toBe(43);
});

it('allows metrics to shrink to two rows without changing other row geometry',()=>{
 const d=canvasDefinition(fixture());const metric={...d.blocks[0],block_type:'metric' as const,placement:{column:0,row:0,span:4,row_span:3}};
 const before=canvasGeometry([metric],940),short={...metric,placement:{...metric.placement,row_span:2}};
 const after=canvasGeometry([short],940);
 expect(canvasLayout({...d,blocks:[metric]},metric.section_id,940)[0].minH).toBe(2);
 expect(after.rowHeight).toBe(before.rowHeight);
 expect(after.metricMinH).toBe(2);expect(after.rowHeight*2+6).toBe(92);
});
