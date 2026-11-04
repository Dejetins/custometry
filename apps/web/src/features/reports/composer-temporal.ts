import type {composerReports as C} from '@custometry/contracts';
import {scopeInputs,type Definition} from './composer-state';

/** Explicit block choices are local context overrides; null means inherit. */
export function withBlockComparison(d:Definition,id:string,settings:C.TemporalSettingsV2|null,alignment:'none'|'previous_year_same_dates'|null):Definition {
 const contexts=d.scopes?.contexts??[],previous=contexts.find(c=>c.target.kind==='block'&&c.target.id===id);
 const {time_comparison:_time,alignment:_legacy,...other}=previous?.context??{};
 const context:C.ContextOverride={...other,...(settings?{time_comparison:settings}:alignment?{alignment}: {})};
 if(!previous&&!Object.keys(context).length)return d;
 const next=contexts.filter(c=>c!==previous);
 if(Object.keys(context).length)next.push({binding_id:previous?.binding_id??crypto.randomUUID(),target:{kind:'block',id},context,locked_fields:previous?.locked_fields??[]});
 return {...d,scopes:{...d.scopes,schema_version:d.scopes?.schema_version??'composer-scopes/v1',contexts:next}};
}


export function initialBlockComparison(d:Definition,block?:C.ComposerBlock){
 const local=d.scopes?.contexts?.find(c=>c.target.kind==='block'&&c.target.id===block?.block_id)?.context;
 const hasComparison=(c:C.ContextOverride)=>c.time_comparison!=null||c.alignment!=null;
 if(local&&hasComparison(local))return {settings:local.time_comparison??null,alignment:local.alignment??null};
 if(block&&scopeInputs(d,block)?.contexts.some(c=>c.target.id!==block.block_id&&hasComparison(c.context)))return {settings:null,alignment:null};
 const source=d.definitions.find(s=>s.definition_id===block?.source?.definition_id)?.query;
 return {settings:source?.time_comparison??null,alignment:source?.alignment==='previous_year_same_dates'?'previous_year_same_dates' as const:null};
}


export function initialBlockCalendarBasis(d:Definition,block?:C.ComposerBlock):'calendar'|'fiscal'|null {
 const local=d.scopes?.contexts?.find(c=>c.target.kind==='block'&&c.target.id===block?.block_id)?.context.calendar_basis;
 if(local)return local;
 if(block&&scopeInputs(d,block)?.contexts.some(c=>c.target.id!==block.block_id&&c.context.calendar_basis))return null;
 return d.definitions.find(s=>s.definition_id===block?.source?.definition_id)?.query.calendar_basis??null;
}

export function withBlockCalendarBasis(d:Definition,id:string,basis:'calendar'|'fiscal'|null):Definition {
 const contexts=d.scopes?.contexts??[],previous=contexts.find(c=>c.target.kind==='block'&&c.target.id===id);
 const {calendar_basis:_basis,...other}=previous?.context??{};
 const context:C.ContextOverride={...other,...(basis?{calendar_basis:basis}:{})};
 if(!previous&&!Object.keys(context).length)return d;
 const next=contexts.filter(c=>c!==previous);
 if(Object.keys(context).length)next.push({binding_id:previous?.binding_id??crypto.randomUUID(),target:{kind:'block',id},context,locked_fields:previous?.locked_fields??[]});
 return {...d,scopes:{...d.scopes,schema_version:d.scopes?.schema_version??'composer-scopes/v1',contexts:next}};
}
