import type {Definition} from './composer-state';
import {isLocked,overlap} from './composer-structure';
export type LayoutChange={before?:string;after?:string;span?:number;rows?:number};
/** Repack only the current section; keep inherited scopes and locked placements intact. */
export function arrangeBlocks(d:Definition,id:string,change:LayoutChange):Definition {
 const source=d.blocks.find(b=>b.block_id===id);
 if(!source||isLocked(d,{kind:'block',id}))throw Error('Block is locked or missing');
 const section=d.sections.find(s=>s.section_id===source.section_id)!;
 const grid=d.pages.find(p=>p.page_id===section.page_id)?.layout==='dashboard_grid';
 if((change.span!==undefined||change.rows!==undefined)&&!grid)throw Error('Resize requires grid layout');
 if(change.span!==undefined&&(!Number.isInteger(change.span)||change.span<1||change.span>12)||change.rows!==undefined&&(!Number.isInteger(change.rows)||change.rows<1||change.rows>12))throw Error('Invalid size');
 const blocks=d.blocks.filter(b=>b.section_id===source.section_id).slice().sort((a,b)=>a.order-b.order);
 const destination=change.before??change.after;
 if(destination&&destination!==id){const at=blocks.findIndex(b=>b.block_id===destination);if(at<0)throw Error('Move within the current section');const item=blocks.splice(blocks.findIndex(b=>b.block_id===id),1)[0];const to=blocks.findIndex(b=>b.block_id===destination);blocks.splice(to+(change.after?1:0),0,item);}
 const locked=blocks.filter(b=>isLocked(d,{kind:'block',id:b.block_id}));
 const occupied=locked.flatMap(b=>b.placement?[b.placement]:[]);
 let row=0,column=0;
 const updates=new Map(blocks.map((b,order)=>{
  if(locked.includes(b)){if(b.order!==order)throw Error('Move would reorder a locked block');return [b.block_id,b] as const;}
  if(!grid)return [b.block_id,{...b,order}] as const;
  const span=b.block_id===id?change.span??b.placement?.span??6:b.placement?.span??6;
  const rows=b.block_id===id?change.rows??b.placement?.row_span??1:b.placement?.row_span??1;
  for(;;){if(column+span>12){row++;column=0;}const p={column,span,row,row_span:rows};if(!occupied.some(other=>overlap(p,other))){occupied.push(p);column+=span;return [b.block_id,{...b,order,placement:p}] as const;}column++;}
 }));
 return {...d,blocks:d.blocks.map(b=>updates.get(b.block_id)??b)};
}
