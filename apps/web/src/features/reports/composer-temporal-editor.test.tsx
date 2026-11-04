import {render,screen,fireEvent,waitFor,cleanup} from '@testing-library/react';
import {QueryClient,QueryClientProvider} from '@tanstack/react-query';
import {afterEach,expect,it,vi} from 'vitest';
import type {composerReports as C} from '@custometry/contracts';
import {ComposerBuilder} from './ComposerBuilder';
const api=vi.hoisted(()=>({validate:vi.fn(),context:vi.fn(),workspaceContext:vi.fn(),calendar:vi.fn()}));
vi.mock('./composer-api',()=>({composerApi:api}));
vi.mock('./report-api',()=>({csrf:()=>'',reportApi:{context:api.context}}));
vi.mock('./workspace-api',()=>({workspaceContext:api.workspaceContext,workspaceCalendar:{get:api.calendar}}));
vi.mock('./ReceiptFilterEditor',()=>({ReceiptFilterEditor:()=>null}));
vi.mock('./StoreScopePicker',()=>({StoreScopePicker:()=>null}));
afterEach(()=>{cleanup();vi.clearAllMocks();});
const previous:C.TemporalSettingsV2={mode:'previous_period',previous_period_basis:'local_date_duration',incomplete_period_policy:'exclude'};
function fixture(base:C.WorkspaceRunRequest['alignment'],modern:C.TemporalSettingsV2|null,local?:C.ContextOverride,locked=false):C.ComposerDefinitionV1 {
 const metric={metric_id:'net_revenue' as const,version_id:'metric',content_hash:'a'.repeat(64)};
 return {document_id:'doc',title:'Report',creator_principal_id:'principal',default_page_id:'page',profile:'workbook_report',brand_profile:{id:'brand',content_hash:'a'.repeat(64)},company_pack:{id:'pack',content_hash:'b'.repeat(64)},pages:[{page_id:'page',order:0,title:'Page',layout:'flow'}],sections:[{section_id:'section',page_id:'page',order:0,title:'Section'}],
 blocks:[{block_id:'block',section_id:'section',block_type:'table',order:0,source:{definition_id:'source',metric_ref:metric},presentation:{title:'Original'}}],definitions:[{definition_id:'source',query:{semantic_dataset_version_id:'dataset',local_store_ids:null,common:{starts_on:'2025-01-01',ends_on:'2025-01-31',store_ids:null},grain:'month',calendar_basis:locked?'fiscal':'calendar',calendar_ref:{version_id:'calendar',content_hash:'b'.repeat(64)},alignment:base,...(modern?{time_comparison:modern}:{}),metric_refs:[metric]}}],
 scopes:{schema_version:'composer-scopes/v1',contexts:[{binding_id:'parent',target:{kind:'document',id:'doc'},context:{alignment:'none',...(locked?{calendar_basis:'calendar' as const}:{})},locked_fields:locked?['alignment','calendar_basis']:[]},...(local?[{binding_id:'local',target:{kind:'block' as const,id:'block'},context:local}]:[])]}};
}
it.each([
 ['new base with explicit legacy none',fixture('none',previous,{alignment:'none'}),'none'],
 ['legacy base overridden by parent',fixture('previous_year_same_dates',null),'inherit'],
 ['legacy base overridden by locked parent',fixture('previous_year_same_dates',null,undefined,true),'inherit'],
] as const)('preserves untouched comparison when editing %s',async(_name,d,selection)=>{
 api.context.mockResolvedValue({datasets:[{id:'dataset',label:'Retail'}]});api.workspaceContext.mockResolvedValue({metrics:d.definitions[0].query.metric_refs,stores:[]});api.calendar.mockResolvedValue({calendar:{version_id:'calendar',content_hash:'b'.repeat(64)}});api.validate.mockResolvedValue({valid:true});const commit=vi.fn();
 render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><ComposerBuilder definition={d} block={d.blocks[0]} locale="en" close={vi.fn()} commit={commit} onValidating={vi.fn()}/></QueryClientProvider>);
 await waitFor(()=>expect((screen.getByRole('button',{name:'Continue'}) as HTMLButtonElement).disabled).toBe(false));fireEvent.click(screen.getByRole('button',{name:'Continue'}));await waitFor(()=>expect((screen.getByRole('button',{name:'Continue'}) as HTMLButtonElement).disabled).toBe(false));fireEvent.click(screen.getByRole('button',{name:'Continue'}));
 expect((screen.getByLabelText('Temporal comparison') as HTMLSelectElement).value).toBe(selection);fireEvent.change(screen.getByLabelText('Block title'),{target:{value:'Renamed'}});fireEvent.click(screen.getByRole('button',{name:'Update block'}));await waitFor(()=>expect(commit).toHaveBeenCalled());
 const candidate=api.validate.mock.calls[0][0];expect(candidate.scopes).toEqual(d.scopes);expect(candidate.definitions[0].query.calendar_basis).toBe(d.definitions[0].query.calendar_basis);expect(candidate.definitions[0].query.alignment).toBe(d.definitions[0].query.alignment);expect(candidate.definitions[0].query.time_comparison).toEqual(d.definitions[0].query.time_comparison);expect(candidate.blocks[0].presentation.title).toBe('Renamed');
});

it('stores explicit fiscal basis and comparison together above a parent calendar default',async()=>{
 const original=fixture('none',null);const d={...original,scopes:{...original.scopes!,contexts:[{binding_id:'parent',target:{kind:'document' as const,id:'doc'},context:{calendar_basis:'calendar' as const}}]}};
 api.context.mockResolvedValue({datasets:[{id:'dataset',label:'Retail'}]});api.workspaceContext.mockResolvedValue({metrics:d.definitions[0].query.metric_refs,stores:[]});api.calendar.mockResolvedValue({calendar:{version_id:'calendar',content_hash:'b'.repeat(64)}});api.validate.mockResolvedValue({valid:true});const commit=vi.fn();
 render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><ComposerBuilder definition={d} block={d.blocks[0]} locale="en" close={vi.fn()} commit={commit} onValidating={vi.fn()}/></QueryClientProvider>);
 await waitFor(()=>expect((screen.getByRole('button',{name:'Continue'}) as HTMLButtonElement).disabled).toBe(false));fireEvent.click(screen.getByRole('button',{name:'Continue'}));await waitFor(()=>expect((screen.getByRole('button',{name:'Continue'}) as HTMLButtonElement).disabled).toBe(false));fireEvent.click(screen.getByRole('button',{name:'Continue'}));
 expect((screen.getByLabelText('Calendar basis') as HTMLSelectElement).value).toBe('inherit');fireEvent.change(screen.getByLabelText('Calendar basis'),{target:{value:'fiscal'}});fireEvent.change(screen.getByLabelText('Temporal comparison'),{target:{value:'previous_year_fiscal_period'}});fireEvent.click(screen.getByRole('button',{name:'Update block'}));await waitFor(()=>expect(commit).toHaveBeenCalled());
 const candidate=api.validate.mock.calls[0][0] as C.ComposerDefinitionV1;const local=candidate.scopes!.contexts!.find(c=>c.target.id==='block')!;expect(local.context.calendar_basis).toBe('fiscal');expect(local.context.time_comparison!.mode).toBe('previous_year_fiscal_period');expect(candidate.scopes!.contexts![0]).toEqual(d.scopes.contexts[0]);
});

it('keeps report editing free of company setup and current-calendar reads',async()=>{
 const d=fixture('none',null);api.context.mockResolvedValue({datasets:[{id:'dataset',label:'Retail'}]});api.workspaceContext.mockResolvedValue({metrics:d.definitions[0].query.metric_refs,stores:[]});api.validate.mockResolvedValue({valid:true});const commit=vi.fn();
 render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><ComposerBuilder definition={d} block={d.blocks[0]} locale="en" close={vi.fn()} commit={commit} onValidating={vi.fn()}/></QueryClientProvider>);
 await waitFor(()=>expect((screen.getByRole('button',{name:'Continue'}) as HTMLButtonElement).disabled).toBe(false));fireEvent.click(screen.getByRole('button',{name:'Continue'}));await waitFor(()=>expect((screen.getByRole('button',{name:'Continue'}) as HTMLButtonElement).disabled).toBe(false));fireEvent.click(screen.getByRole('button',{name:'Continue'}));
 expect(screen.queryByLabelText('Calendar version')).toBeNull();expect(screen.queryByLabelText('IANA time zone')).toBeNull();expect(api.calendar).not.toHaveBeenCalled();fireEvent.change(screen.getByLabelText('Block title'),{target:{value:'Renamed'}});fireEvent.click(screen.getByRole('button',{name:'Update block'}));await waitFor(()=>expect(commit).toHaveBeenCalled());
 const candidate=api.validate.mock.calls[0][0] as C.ComposerDefinitionV1;expect(candidate.definitions[0].query.calendar_ref).toEqual(d.definitions[0].query.calendar_ref);
});

it('edits existing data in one form without nested wizard navigation, preserving title and layout',async()=>{
 const d=fixture('none',previous);api.context.mockResolvedValue({datasets:[{id:'dataset',label:'Retail'}]});api.workspaceContext.mockResolvedValue({metrics:d.definitions[0].query.metric_refs,stores:[]});api.validate.mockResolvedValue({valid:true});const commit=vi.fn();
 const client=new QueryClient({defaultOptions:{queries:{retry:false}}});
 const props={embedded:true,definition:d,block:d.blocks[0],locale:'en' as const,close:vi.fn(),commit,onValidating:vi.fn()};
 const view=render(<QueryClientProvider client={client}><ComposerBuilder {...props}/></QueryClientProvider>);
 await waitFor(()=>expect((screen.getByRole('button',{name:'Update block'}) as HTMLButtonElement).disabled).toBe(false));
 expect(screen.queryByRole('complementary')).toBeNull();expect(screen.queryByRole('button',{name:'Continue'})).toBeNull();expect(screen.queryByRole('button',{name:'Close settings'})).toBeNull();
 expect(screen.getByLabelText('Data product')).toBeTruthy();expect(screen.getByLabelText('Grain')).toBeTruthy();expect(screen.getByLabelText('Start date')).toBeTruthy();
 const changed={...d,blocks:[{...d.blocks[0],block_type:'chart' as const,presentation:{title:'Renamed in inspector'}}]};
 view.rerender(<QueryClientProvider client={client}><ComposerBuilder {...props} definition={changed} block={changed.blocks[0]}/></QueryClientProvider>);
 fireEvent.change(screen.getByLabelText('Grain'),{target:{value:'quarter'}});fireEvent.click(screen.getByRole('button',{name:'Update block'}));
 await waitFor(()=>expect(commit).toHaveBeenCalledOnce());const result=commit.mock.calls[0][0] as C.ComposerDefinitionV1;
 expect(result.blocks[0].presentation.title).toBe('Renamed in inspector');expect(result.blocks[0].block_id).toBe('block');expect(result.blocks[0].block_type).toBe('chart');expect(result.definitions[0].query.grain).toBe('quarter');expect(result.definitions[0].query.time_comparison).toEqual(previous);
});
