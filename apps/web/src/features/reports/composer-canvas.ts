import type {composerReports as C} from '@custometry/contracts';
import type {Layout} from 'react-grid-layout';
import {isLocked,overlap} from './composer-structure';
import type {Definition} from './composer-state';
// Row height is independent of monitor width; placements remain in grid units.
export const canvasRows=(_width:number)=>40;
/** Translate legacy units in memory; immutable saved snapshots are never rewritten. */
export function canvasDefinition(d:Definition):Definition {
 if(d.grid_columns===24)return d;
 return {...d,grid_columns:24,blocks:d.blocks.map(b=>({...b,placement:b.placement?{column:(b.placement.column??0)*2,span:(b.placement.span??12)*2,row:(b.placement.row??0)*8,row_span:(b.placement.row_span??1)*8}:null}))};
}
/** Preserve saved cell positions; expand the canvas rather than displacing neighbors. */
export function canvasGeometry(blocks:readonly C.ComposerBlock[],available:number){
 const metrics=blocks.filter(b=>b.block_type==='metric'&&b.placement);
 const width=Math.max(available,...metrics.map(b=>Math.ceil(146*24/(b.placement!.span??24)-6)));
 const rowHeight=Math.max(metrics.length?43:canvasRows(width),...metrics.map(b=>Math.ceil(98/(b.placement!.row_span??3)-6)));
 return {width,rowHeight,metricMinW:Math.ceil(146/((width+6)/24)),metricMinH:Math.ceil(98/(rowHeight+6))};
}
export function canvasLayout(d:Definition,section:string,width?:number):Layout[]{return d.blocks.filter(b=>b.section_id===section&&b.placement).map(b=>({i:b.block_id,x:b.placement!.column??0,y:b.placement!.row??0,w:b.placement!.span??24,h:b.placement!.row_span??8,minW:b.block_type==='metric'&&width?canvasGeometry(d.blocks.filter(v=>v.section_id===section),width).metricMinW:Math.min(b.placement!.span??24,b.block_type==='filter'?8:4),minH:Math.min(b.placement!.row_span??8,b.block_type==='metric'?2:b.source?5:b.block_type==='text'?1:2),static:isLocked(d,{kind:'block',id:b.block_id})}));}
export function commitCanvas(d:Definition,section:string,layout:Layout[]):Definition {
 const existing=d.blocks.filter(b=>b.section_id===section);
 if(layout.length!==existing.length||new Set(layout.map(l=>l.i)).size!==existing.length)throw Error('Invalid layout');
 const placements=new Map(layout.map(l=>[l.i,{column:l.x,row:l.y,span:l.w,row_span:l.h}]));
 for(const b of existing){const p=placements.get(b.block_id);if(!p||![p.column,p.row,p.span,p.row_span].every(Number.isInteger)||p.column<0||p.row<0||p.span<1||p.row_span<1||p.column+p.span>24)throw Error('Invalid position');
  if(isLocked(d,{kind:'block',id:b.block_id})&&JSON.stringify(p)!==JSON.stringify({column:b.placement?.column??0,row:b.placement?.row??0,span:b.placement?.span??24,row_span:b.placement?.row_span??8}))throw Error('Locked block');
  for(const other of existing)if(other.block_id!==b.block_id&&placements.has(other.block_id)&&overlap(p,placements.get(other.block_id)!))throw Error('Overlap');
 }
 return {...d,blocks:d.blocks.map(b=>placements.has(b.block_id)?{...b,placement:placements.get(b.block_id)!}:b)};
}
/** Keyboard counterpart: reject occupied cells without moving neighboring blocks. */
export function resizeCanvas(d:Definition,id:string,patch:Partial<C.GridPlacement>):Definition {
 const b=d.blocks.find(b=>b.block_id===id)!;if(!b?.placement||isLocked(d,{kind:'block',id}))throw Error('Unavailable');
 const list=canvasLayout(d,b.section_id),item=list.find(l=>l.i===id)!;
 item.w=patch.span??item.w;item.h=patch.row_span??item.h;item.x=Math.min(patch.column??item.x,24-item.w);item.y=patch.row??item.y;
 return commitCanvas(d,b.section_id,list);
}
export function addContent(d:Definition,section:string,type:'text'|'filter',locale:'ru'|'en'):Definition {
 if(isLocked(d,{kind:'section',id:section}))throw Error('Locked section');
 const dataset=d.definitions[0]?.query.semantic_dataset_version_id;
 if(type==='filter'&&!dataset)throw Error('Add an analytical block first');
 const grid=d.pages.find(p=>p.page_id===d.sections.find(s=>s.section_id===section)?.page_id)?.layout==='dashboard_grid';
 const block:C.ComposerBlock={block_id:crypto.randomUUID(),section_id:section,order:Math.max(-1,...d.blocks.filter(b=>b.section_id===section).map(b=>b.order))+1,block_type:type,presentation:{title:locale==='ru'?(type==='text'?'Новый текст':'Магазин'):(type==='text'?'New text':'Store')},...(type==='text'?{text:locale==='ru'?'Добавьте пояснение к отчёту.':'Add context to your report.'}:{control:{semantic_dataset_version_id:dataset!,target_block_ids:[],store_ids:null}}),placement:grid?{column:0,row:Math.max(0,...d.blocks.filter(b=>b.section_id===section).map(b=>(b.placement?.row??0)+(b.placement?.row_span??0))),span:24,row_span:type==='filter'?2:1}:null};
 return {...d,blocks:[...d.blocks,block]};
}
