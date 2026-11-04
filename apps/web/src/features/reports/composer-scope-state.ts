import type {composerReports as C} from '@custometry/contracts';
type Definition=C.ComposerDefinitionV1;
type Filter=C.FilterScopeBinding|C.ReceiptScopeBinding;
export const receiptScopes=(d:Definition):readonly C.ReceiptScopeBinding[]=>d.scopes?.schema_version==='composer-scopes/v2'?(d.scopes.receipt_filters??[]):[];
const allFilters=(d:Definition):Filter[]=>[...(d.scopes?.filters??[]),...receiptScopes(d)];
const splitFilters=(d:Definition,filters:Filter[])=>({filters:filters.filter((f):f is C.FilterScopeBinding=>!('semantic_dataset_version_id' in f)),...(d.scopes?.schema_version==='composer-scopes/v2'?{receipt_filters:filters.filter((f):f is C.ReceiptScopeBinding=>'semantic_dataset_version_id' in f)}:{})});

export function pruneScopes(d:Definition,removed:ReadonlySet<string>):Definition {
 if(d.pair&&(removed.has(d.pair.left_block_id)||removed.has(d.pair.right_block_id)))d={...d,pair:null};
 if(!d.scopes)return d;
 const filters=allFilters(d),contexts=d.scopes.contexts??[];
 if(filters.some(f=>f.locked&&(removed.has(f.target.id)||f.linked_target_block_ids?.some(id=>removed.has(id))))||contexts.some(c=>c.locked_fields?.length&&removed.has(c.target.id)))throw Error('Locked scope constraint');
 const retained=filters.filter(f=>!removed.has(f.target.id));const ids=new Set(retained.map(f=>f.binding_id));
 return {...d,scopes:{...d.scopes,...splitFilters(d,retained.map(f=>({...f,linked_target_block_ids:f.linked_target_block_ids?.filter(id=>!removed.has(id)),replaces:f.replaces?.filter(id=>ids.has(id))}))),contexts:contexts.filter(c=>!removed.has(c.target.id))}};
}

export function copyScopes(before:Definition,next:Definition,ids:ReadonlyMap<string,string>):Definition {
 if(!before.scopes)return next;
 const original=allFilters(before);const copied=original.filter(f=>ids.has(f.target.id));const bindings=new Map(copied.map(f=>[f.binding_id,crypto.randomUUID()]));
 const filters:Filter[]=[...allFilters(next),...copied.map(f=>({...structuredClone(f),binding_id:bindings.get(f.binding_id)!,target:{...f.target,id:ids.get(f.target.id)!},replaces:f.replaces?.map(id=>bindings.get(id)??id),linked_target_block_ids:f.linked_target_block_ids?.filter(id=>ids.has(id)).map(id=>ids.get(id)!)}))];
 // Preserve incoming direct constraints as independent local copies, without wiring
 // edits of a duplicate back into the original document's linked targets.
 for(const f of original.filter(f=>!ids.has(f.target.id)))for(const target of f.linked_target_block_ids??[]){const copiedTarget=ids.get(target);if(!copiedTarget)continue;
  filters.push({...structuredClone(f),binding_id:crypto.randomUUID(),target:{kind:'block',id:copiedTarget},order:Math.max(-1,...filters.filter(f=>f.target.id===copiedTarget).map(f=>f.order))+1,combine_mode:'intersect',replaces:[],linked_target_block_ids:[]});
 }
 const contexts:C.ContextScopeBinding[]=[...(next.scopes?.contexts??[]),...(before.scopes.contexts??[]).filter(c=>ids.has(c.target.id)).map(c=>({...structuredClone(c),binding_id:crypto.randomUUID(),target:{...c.target,id:ids.get(c.target.id)!}}))];
 return {...next,scopes:{...before.scopes,...splitFilters(before,filters),contexts}};
}
