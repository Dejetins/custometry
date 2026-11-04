import type {composerReports as C} from '@custometry/contracts';
export type FilterInput=C.ReceiptFilterInput|C.RelationalReceiptFilterInput|C.AggregateReceiptFilterInput|C.CohortReceiptFilterInput;
export type Flat=C.ReceiptFilterInput['expression'];
export type Scoped=C.AggregateReceiptFilterInput['expression'];
export type CohortExpr=C.CohortReceiptFilterInput['expression'];
export type SequenceExpr=C.CustomerEventMembership['predicate'];
export type Expression=Flat|Scoped|CohortExpr|SequenceExpr;
export type FilterCatalog=C.RelationalCatalogResponse|C.AggregateCatalogResponse|C.CohortCatalogResponse;
export type CountCatalog=C.AggregateCatalogResponse|C.CohortCatalogResponse;
export const isCohort=(value:FilterInput):value is C.CohortReceiptFilterInput=>value.schema_version==='receipt-filter/v4';
export const isRelated=(value:FilterInput):value is C.RelationalReceiptFilterInput|C.AggregateReceiptFilterInput|C.CohortReceiptFilterInput=>'root_scope_id' in value;
export function condition(field:C.FilterFieldVersion,scope?:string):Expression {
 return {kind:'predicate',field_id:field.field_id,field_version_id:field.version_id,operator:'eq',values:[{data_type:field.data_type,value:''}],...(scope?{node_id:crypto.randomUUID(),scope_id:scope}:{})};
}
export function group(children:readonly Expression[],scope?:string,kind:'and'|'or'='and'):Expression {
 return {kind,children,...(scope?{node_id:crypto.randomUUID(),scope_id:scope}:{})} as Expression;
}
export function lift(node:Flat,scope:string):Scoped {
 const base={...node,node_id:crypto.randomUUID(),scope_id:scope};
 if(node.kind==='and'||node.kind==='or')return {...base,children:node.children.map(c=>lift(c,scope))} as Scoped;
 if(node.kind==='not')return {...base,child:lift(node.child,scope)} as Scoped;
 return base as Scoped;
}
export function addRelated(value:FilterInput|null,catalog:FilterCatalog):C.RelationalReceiptFilterInput|C.AggregateReceiptFilterInput|C.CohortReceiptFilterInput {
 if(value&&!isRelated(value)&&value.registry_version_id!==catalog.legacy_registry_version_id)throw Error('Filter registry changed');
 if(value&&isRelated(value)&&Object.entries(value.registry_versions).some(([key,version])=>catalog.registry_versions[key]!==version))throw Error('Filter registry changed');
 const root=value&&isRelated(value)?value.root_scope_id:crypto.randomUUID(),child=crypto.randomUUID();
 const edge=catalog.relationships.find(r=>r.relationship.parent_entity==='Receipt'&&r.relationship.child_entity==='ReceiptItem')?.relationship;
 const field=catalog.fields.find(f=>f.field.field_id==='ReceiptItem.quantity')?.field;
 if(!edge||!field)throw Error('Relationship unavailable');
 const exists:C.AggregateExists={kind:'exists',node_id:crypto.randomUUID(),scope_id:root,parent_scope_id:root,child_scope_id:child,child_entity:edge.child_entity,relationship_id:edge.relationship_id,relationship_version_id:edge.version_id,predicate:group([condition(field,child)],child) as Scoped};
 const before=value?(isRelated(value)?value.expression:lift(value.expression,root)):null;
 if(value&&isCohort(value))return {...value,expression:before?group([before,exists],root) as CohortExpr:exists};
 return {schema_version:value&&isAggregate(value)?'receipt-filter/v3':'receipt-filter/v2',root_scope_id:root,registry_versions:catalog.registry_versions,legacy_registry_version_id:catalog.legacy_registry_version_id,expression:before?group([before,exists],root) as Scoped:exists} as C.RelationalReceiptFilterInput|C.AggregateReceiptFilterInput;
}

export const isAggregate=(value:FilterInput):value is C.AggregateReceiptFilterInput=>value.schema_version==='receipt-filter/v3';
export function makeCount(catalog:CountCatalog,root:string,selected=catalog.counts[0]):C.ScopedCount {
 if(!selected)throw Error('Count unavailable');
 const edge=catalog.relationships.find(r=>r.relationship.version_id===selected.definition.relationship_version_id)?.relationship;
 const field=catalog.fields.find(f=>f.field.field_id==='ReceiptItem.line_id')?.field;
 if(!edge||!field)throw Error('Count binding unavailable');
 const child=crypto.randomUUID();
 return {kind:'scoped_count',parent_scope_id:root,child_scope_id:child,child_entity:edge.child_entity,relationship_id:edge.relationship_id,relationship_version_id:edge.version_id,definition:selected.definition,
  window:{...selected.observation,timezone:'UTC'},predicate:group([{kind:'predicate',node_id:crypto.randomUUID(),scope_id:child,field_id:field.field_id,field_version_id:field.version_id,operator:'is_not_null',values:[]}],child) as Scoped};
}
export function addCount(value:FilterInput|null,catalog:CountCatalog):C.AggregateReceiptFilterInput|C.CohortReceiptFilterInput {
 if(value&&!isRelated(value)&&value.registry_version_id!==catalog.legacy_registry_version_id)throw Error('Filter registry changed');
 if(value&&isRelated(value)&&Object.entries(value.registry_versions).some(([key,version])=>catalog.registry_versions[key]!==version))throw Error('Filter registry changed');
 const root=value&&isRelated(value)?value.root_scope_id:crypto.randomUUID(),left=makeCount(catalog,root);
 const aggregate:C.AggregateCompare={kind:'aggregate_compare',node_id:crypto.randomUUID(),scope_id:root,left,operator:'ge',right:{kind:'scalar',unit:left.definition.unit,value:'1'}};
 const before=value?(isRelated(value)?value.expression:lift(value.expression,root)):null;
 if(value&&isCohort(value))return {...value,expression:before?group([before,aggregate],root) as CohortExpr:aggregate};
 return {schema_version:'receipt-filter/v3',root_scope_id:root,registry_versions:catalog.registry_versions,legacy_registry_version_id:catalog.legacy_registry_version_id,expression:before?group([before,aggregate],root) as Scoped:aggregate};
}
