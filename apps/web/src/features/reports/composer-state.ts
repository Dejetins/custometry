import type {composerReports as C, configuredReports as W} from '@custometry/contracts';
import {pruneScopes,copyScopes,receiptScopes} from './composer-scope-state';

export type Definition=C.ComposerDefinitionV1;
export function scopeInputs(d:Definition,block:C.ComposerBlock){
 const chain=[block.block_id];let section=d.sections.find(s=>s.section_id===block.section_id);
 const page=d.pages.find(p=>p.page_id===section?.page_id);
 while(section&&!chain.includes(section.section_id)){chain.push(section.section_id);section=d.sections.find(s=>s.section_id===section?.parent_section_id);}
 if(page){chain.push(page.page_id);if(page.chapter_id)chain.push(page.chapter_id);}chain.push(d.document_id);chain.reverse();
 const ids=new Set(chain);
 const filters=d.scopes?.filters?.filter(f=>ids.has(f.target.id)||f.linked_target_block_ids?.includes(block.block_id)).slice().sort((a,b)=>a.binding_id.localeCompare(b.binding_id))??[];
 const contexts=d.scopes?.contexts?.filter(c=>ids.has(c.target.id)).slice().sort((a,b)=>a.binding_id.localeCompare(b.binding_id))??[];
 const receipt_filters=receiptScopes(d).filter(f=>ids.has(f.target.id)||f.linked_target_block_ids?.includes(block.block_id)).slice().sort((a,b)=>a.binding_id.localeCompare(b.binding_id));
 const targets=new Set([...filters,...receipt_filters,...contexts].map(b=>b.target.id));
 return filters.length||contexts.length||receipt_filters.length?{ancestry:chain.filter(id=>targets.has(id)),filters,contexts,...(receipt_filters.length?{receipt_filters}:{})}:null;
}
export const queryKey=(d:Definition,block:C.ComposerBlock)=>JSON.stringify([
 d.definitions.find(s=>s.definition_id===block.source?.definition_id)?.query,block.source?.metric_ref,scopeInputs(d,block),...d.blocks.filter(b=>b.control?.target_block_ids.includes(block.block_id)&&b.control.store_ids!==null).map(b=>[b.block_id,b.control?.store_ids]),
]);
export function removeBlock(d:Definition,id:string,preserveScopes=false):Definition {
 const blocks=d.blocks.filter(b=>b.block_id!==id).map(b=>b.control&&!preserveScopes?{...b,control:{...b.control,target_block_ids:b.control.target_block_ids.filter(t=>t!==id)}}:b);const used=new Set(blocks.map(b=>b.source?.definition_id));
 const next={...d,blocks,definitions:d.definitions.filter(s=>used.has(s.definition_id))};return preserveScopes?next:pruneScopes(next,new Set([id]));
}
export function nextPlacement(d:Definition,section:string,width?:number,height?:number):C.GridPlacement|null {
 const page=d.pages.find(p=>p.page_id===d.sections.find(s=>s.section_id===section)?.page_id);
 if(page?.layout!=='dashboard_grid')return null;
 const blocks=d.blocks.filter(b=>b.section_id===section);
 const span=width??(d.grid_columns??12)/2,rows=height??(d.grid_columns===24?8:1);
 for(let row=0;;row++)for(let column=0;column+span<=(d.grid_columns??12);column++){
  if(!blocks.some(b=>b.placement&&column<(b.placement.column??0)+(b.placement.span??12)&&(b.placement.column??0)<column+span&&row<(b.placement.row??0)+(b.placement.row_span??1)&&(b.placement.row??0)<row+rows))return {column,span,row,row_span:rows};
 }
}
export function duplicate(d:Definition,id:string):Definition {
 const block=d.blocks.find(b=>b.block_id===id)!;const source=d.definitions.find(s=>s.definition_id===block.source?.definition_id)!;
 const sourceId=crypto.randomUUID();const copy:C.ComposerBlock={...structuredClone(block),block_id:crypto.randomUUID(),copied_from:{node_id:block.block_id,snapshot_id:null},locked:false,order:Math.max(-1,...d.blocks.filter(b=>b.section_id===block.section_id).map(b=>b.order))+1,placement:nextPlacement(d,block.section_id,block.placement?.span,block.placement?.row_span),...(block.source?{source:{...block.source,definition_id:sourceId}}:{})};
 return copyScopes(d,{...d,blocks:[...d.blocks,copy],definitions:source?[...d.definitions,{...structuredClone(source),definition_id:sourceId}]:d.definitions},new Map([[id,copy.block_id]]));
}
/** Reuse the established metric result renderer without creating another options compiler. */
export function projectionDefinition(d:Definition,b:C.ComposerBlock,effective?:C.EffectiveContext):W.ConfiguredReportV2 {
 const source=d.definitions.find(s=>s.definition_id===b.source?.definition_id)!.query;
 const q=effective?{...source,common:{starts_on:effective.starts_on,ends_on:effective.ends_on,store_ids:effective.store_ids},local_store_ids:null,
 grain:effective.grain,calendar_ref:effective.calendar_ref,calendar_basis:effective.calendar_basis,alignment:effective.alignment}:source;
 return {schema_version:'configured-report/v2',report_id:d.document_id,creator_principal_id:d.creator_principal_id,title:d.title,
  semantic_dataset_version_id:q.semantic_dataset_version_id,common_context:q.common,grain:q.grain,calendar_ref:q.calendar_ref,calendar_basis:q.calendar_basis,
  worksets:[{workset_id:b.section_id,name:{en:'Block',ru:'Блок'},visibility:'personal',owner_principal_id:d.creator_principal_id,cards:[{card_id:b.block_id,metric_ref:b.source!.metric_ref,local_store_ids:q.local_store_ids,population_binding:null,target_action_binding:null}]}],
  default_workset_id:b.section_id,selection:{mode:'single',card_id:b.block_id,temporal:q.alignment,display:'series'},brand_profile:d.brand_profile,company_pack:d.company_pack,base_snapshot_ref:null};
}
