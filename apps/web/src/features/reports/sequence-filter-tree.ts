import type {composerReports as C} from '@custometry/contracts';
import {type FilterInput,type CohortExpr,isRelated,isCohort,lift,group} from './receipt-filter-tree';
export const MAX_US=315360000000000;
export function utcMicros(iso:string):bigint {
 const match=/^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d{1,6}))?(?:Z|\+00:00)$/.exec(iso);
 if(!match)throw Error('UTC timestamp required');
 const ms=Date.parse(`${match[1]}Z`);if(!Number.isFinite(ms))throw Error('Invalid timestamp');
 return BigInt(ms)*1000n+BigInt((match[2]??'').padEnd(6,'0'));
}
export function microsUtc(value:bigint):string {
 const seconds=value/1000000n-(value<0n&&value%1000000n!==0n?1n:0n),fraction=value-seconds*1000000n;
 return `${new Date(Number(seconds)*1000).toISOString().slice(0,19)}.${fraction.toString().padStart(6,'0')}Z`;
}
export function secondsMicros(value:string):number {
 if(!/^\d+(\.\d{0,6})?$/.test(value))throw Error('Use nonnegative seconds with up to six decimals');
 const [whole,fraction='']=value.split('.');const micros=BigInt(whole!)*1000000n+BigInt(fraction.padEnd(6,'0'));
 if(micros>BigInt(MAX_US))throw Error('Interval too large');return Number(micros);
}
export function relativeWindow(window:C.FixedSequenceWindow|C.RelativeSequenceWindow,startOffset=-86400000000,endOffset=0):C.RelativeSequenceWindow {
 const anchor=window.observation_as_of;
 return {kind:'relative',policy:'publication_observation_as_of_elapsed_utc/v1',anchor,start_offset_us:startOffset,end_offset_us:endOffset,
  starts_at:microsUtc(utcMicros(anchor)+BigInt(startOffset)),ends_at:microsUtc(utcMicros(anchor)+BigInt(endOffset)),timezone:'UTC',observation_as_of:anchor,knowledge_as_of:window.knowledge_as_of};
}
export function positiveStep(catalog:C.CohortCatalogResponse,event=catalog.events[0],gap:C.SequenceGap|null=null):C.PositiveStep {
 if(!event)throw Error('Event unavailable');const field=catalog.fields.find(f=>f.field.field_id==='Receipt.receipt_id')?.field;
 if(!field)throw Error('Event field unavailable');const scope=crypto.randomUUID();
 return {kind:'positive',step_id:crypto.randomUUID(),child_scope_id:scope,event:event.definition,gap,
  predicate:{kind:'and',node_id:crypto.randomUUID(),scope_id:scope,children:[{kind:'predicate',node_id:crypto.randomUUID(),scope_id:scope,field_id:field.field_id,field_version_id:field.version_id,operator:'is_not_null',values:[]}]}};
}
export function addCustomerSequence(value:FilterInput|null,catalog:C.CohortCatalogResponse):C.CohortReceiptFilterInput {
 const equal=(a:Readonly<Record<string,unknown>>,b:Readonly<Record<string,unknown>>)=>Object.keys(a).length===Object.keys(b).length&&Object.entries(a).every(([k,v])=>b[k]===v);
 if(value&&!isRelated(value)&&value.registry_version_id!==catalog.legacy_registry_version_id)throw Error('Filter registry changed');
 if(value&&isRelated(value)&&(!equal(value.registry_versions,isCohort(value)?catalog.registry_versions:catalog.receipt_registry_versions)||(value.legacy_registry_version_id!=null&&value.legacy_registry_version_id!==catalog.legacy_registry_version_id)))throw Error('Filter registry changed');
 const event=catalog.events[0],edge=catalog.relationships.find(r=>r.relationship.parent_entity==='Customer'&&r.relationship.child_entity==='Receipt')?.relationship;
 if(!event||!edge)throw Error('Event unavailable');
 const root=value&&isRelated(value)?value.root_scope_id:crypto.randomUUID(),customer=crypto.randomUUID();
 const sequence:C.BehavioralSequence={kind:'sequence',node_id:crypto.randomUUID(),scope_id:customer,parent_scope_id:customer,relationship_id:edge.relationship_id,relationship_version_id:edge.version_id,child_entity:'Receipt',
  window:{kind:'fixed',timezone:'UTC',...event.observation},steps:[positiveStep(catalog,event)],bindings:[],tie_policy:'strict_event_time/v1'};
 const leaf:C.CustomerEventMembership={kind:'customer_event_membership',node_id:crypto.randomUUID(),scope_id:root,customer_scope_id:customer,relationship_id:edge.relationship_id,relationship_version_id:edge.version_id,predicate:sequence};
 const before=value?(isRelated(value)?value.expression:lift(value.expression,root)):null;
 const origins=value&&isCohort(value)?value.promoted_registry_sets??[]:value&&isRelated(value)?[value.registry_versions]:[];
 return {schema_version:'receipt-filter/v4',root_scope_id:root,registry_versions:catalog.registry_versions,receipt_registry_versions:catalog.receipt_registry_versions,promoted_registry_sets:origins,
  legacy_registry_version_id:catalog.legacy_registry_version_id,expression:before?group([before,leaf],root) as CohortExpr:leaf};
}
export function validOrder(steps:readonly (C.PositiveStep|C.NegativeStep)[]):boolean {
 let preceding:string|null=null;if(!steps.length)return false;
 for(const step of steps){if(!('after_step_id' in step))preceding=step.step_id;else if(!preceding||step.after_step_id!==preceding)return false;}return true;
}
export function orderedSteps(steps:readonly (C.PositiveStep|C.NegativeStep)[]):readonly (C.PositiveStep|C.NegativeStep)[] {
 if(!validOrder(steps))throw Error('Negative steps must follow their anchor');let positive=false;
 return steps.map(s=>{if('after_step_id' in s)return s;const result={...s,gap:positive?s.gap??{minimum_us:0,maximum_us:86400000000}:null};positive=true;return result;});
}
