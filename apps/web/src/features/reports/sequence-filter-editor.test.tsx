import {render,screen,fireEvent,waitFor,cleanup} from '@testing-library/react';
import {QueryClient,QueryClientProvider} from '@tanstack/react-query';
import {afterEach,beforeEach,expect,it,vi} from 'vitest';
import type {composerReports as C} from '@custometry/contracts';
import {ReceiptFilterEditor} from './ReceiptFilterEditor';
import {addCustomerSequence} from './sequence-filter-tree';
const api=vi.hoisted(()=>({cohortFilterCatalog:vi.fn(),cohortFilterPreview:vi.fn(),cohortFilterFacets:vi.fn(),filterCatalog:vi.fn()}));
vi.mock('./composer-api',()=>({composerApi:api}));vi.mock('./report-api',()=>({csrf:()=>''}));
const field=(column:string):C.CatalogField=>({field:{field_id:`Receipt.${column}`,version_id:column,entity:'Receipt',column,data_type:'string',operators:['eq','ne','is_not_null'],null_policy:'unknown'},label:{en:column,ru:column},description:{en:column,ru:column}});
const cutoff='2026-10-07T18:25:25.440829Z';
const catalog:C.CohortCatalogResponse={schema_version:'receipt-filter-catalog/v4',dataset_version_id:'dataset',root_entity:'Receipt',registry_versions:{Customer:'c',Receipt:'new',ReceiptItem:'items'},receipt_registry_versions:{Receipt:'old',ReceiptItem:'items'},legacy_registry_version_id:'legacy',fields:['receipt_id','store_id','status','customer_id'].map(field),facet_field_ids:{Receipt:['Receipt.store_id','Receipt.status'],ReceiptItem:[]},relationships:[{relationship:{relationship_id:'customer.receipts',version_id:'edge',parent_entity:'Customer',child_entity:'Receipt',parent_fields:['Customer.customer_id'],child_fields:['Receipt.customer_id'],policy_version_id:'policy',nullable_child_fields:['Receipt.customer_id']},label:{en:'Customer receipts',ru:'Чеки клиента'},complete:false,completeness_hash:'hash'}],events:[{definition:{event_id:'receipt.observed',version_id:'event',entity:'Receipt',relationship_version_id:'edge',time_field:{field_id:'Receipt.event_time',version_id:'time',entity:'Receipt',column:'receipt_datetime'}},observation:{starts_at:'2025-01-01T00:00:00Z',ends_at:cutoff,observation_as_of:cutoff,knowledge_as_of:cutoff},complete:false,evidence_hash:'hash',label:{en:'Observed receipt',ru:'Наблюдаемый чек'},description:{en:'Current',ru:'Текущие'}}],counts:[],mandatory_expressions:{},universe:{version_id:'universe',root_entity:'Customer',relationship_id:'customer.receipts',relationship_version_id:'edge'},resource_policy_version_id:'policy',limitation_codes:[]};
beforeEach(()=>{vi.clearAllMocks();api.cohortFilterCatalog.mockResolvedValue(catalog);api.filterCatalog.mockResolvedValue({fields:[],registry_version_id:'legacy'});api.cohortFilterPreview.mockResolvedValue({schema_version:'receipt-filter-preview/v4',request_hash:'hash',matched_count:2,authorized_count:5,unknown_count:3,not_matched_count:0,limitation_codes:['EVENT_HISTORY_UNCERTIFIED']});});
afterEach(cleanup);
async function show(){const change=vi.fn();render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><ReceiptFilterEditor dataset="dataset" value={null} locale="en" onChange={change}/></QueryClientProvider>);await screen.findByText('Add customer sequence');fireEvent.click(screen.getByText('Add customer sequence'));await screen.findByText('Customer event sequence');return change;}
it('edits exact windows, positive/negative steps and property bindings before explicit Apply',async()=>{
 const change=await show();fireEvent.change(screen.getByLabelText('History window'),{target:{value:'relative'}});const start=screen.getByLabelText('Start: seconds before snapshot');start.focus();fireEvent.change(start,{target:{value:'315360000'}});expect(document.activeElement).toBe(start);
 fireEvent.click(screen.getByText('Add event'));fireEvent.click(screen.getByText('Add same-property binding'));fireEvent.click(screen.getByText('Add absent event'));
 fireEvent.click(screen.getByText('Apply filter to block'));await waitFor(()=>expect(change).toHaveBeenCalledOnce());const value=change.mock.calls[0]![0] as C.CohortReceiptFilterInput;expect(value.schema_version).toBe('receipt-filter/v4');const sequence=(value.expression as C.CustomerEventMembership).predicate as C.BehavioralSequence;
 expect(sequence.window.ends_at).toBe(cutoff);expect(sequence.steps).toHaveLength(3);expect(sequence.bindings).toHaveLength(1);expect(sequence.steps[2]).toMatchObject({kind:'negative',after_step_id:sequence.steps[1]!.step_id});
});
it('invalid visible duration prevents submitting the previous valid value',async()=>{
 await show();fireEvent.change(screen.getByLabelText('History window'),{target:{value:'relative'}});fireEvent.change(screen.getByLabelText('Start: seconds before snapshot'),{target:{value:'0.0000001'}});fireEvent.click(screen.getByText('Apply filter to block'));expect(api.cohortFilterPreview).not.toHaveBeenCalled();expect(screen.getByText('Enter seconds with up to 6 decimal places.')).toBeTruthy();
});
it('resets and undoes draft sequence; excludes customer identity from value lookup',async()=>{
 await show();fireEvent.click(screen.getByText('Reset to initial'));expect(screen.queryByText('Customer event sequence')).toBeNull();fireEvent.click(screen.getByText('Undo change'));expect(screen.getByText('Customer event sequence')).toBeTruthy();
 const selects=screen.getAllByLabelText('Field');const facet=selects[selects.length-1] as HTMLSelectElement;expect([...facet.options].map(o=>o.value)).toEqual(['Receipt.store_id','Receipt.status']);
});

it.each(['receipt-filter/v2','receipt-filter/v3'] as const)('promotes %s with an absent optional legacy pin while preserving its registry',schema=>{
 const old={schema_version:schema,root_scope_id:'root',registry_versions:catalog.receipt_registry_versions,legacy_registry_version_id:null,expression:{kind:'predicate',node_id:'node',scope_id:'root',field_id:'Receipt.status',field_version_id:'status',operator:'eq',values:[{data_type:'string',value:'completed'}]}} as C.RelationalReceiptFilterInput|C.AggregateReceiptFilterInput;
 const next=addCustomerSequence(old,catalog);expect(next.promoted_registry_sets).toEqual([old.registry_versions]);expect(next.legacy_registry_version_id).toBe('legacy');
 expect(()=>addCustomerSequence({...old,legacy_registry_version_id:'conflicting'},catalog)).toThrow('Filter registry changed');
});
