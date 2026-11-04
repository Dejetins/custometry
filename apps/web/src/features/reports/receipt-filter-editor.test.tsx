import {render,screen,fireEvent,waitFor,cleanup,act} from '@testing-library/react';
import {QueryClient,QueryClientProvider} from '@tanstack/react-query';
import {afterEach,beforeEach,expect,it,vi} from 'vitest';
import {ReceiptFilterEditor} from './ReceiptFilterEditor';
const api=vi.hoisted(()=>({filterCatalog:vi.fn(),filterPreview:vi.fn(),filterFacets:vi.fn()}));
vi.mock('./composer-api',()=>({composerApi:api}));vi.mock('./report-api',()=>({csrf:()=>''}));
const predicate={kind:'predicate' as const,field_id:'Receipt.status',field_version_id:'field',operator:'eq' as const,values:[{data_type:'string' as const,value:'completed'}]};
const value={schema_version:'receipt-filter/v1' as const,registry_version_id:'registry',expression:predicate};
beforeEach(()=>{vi.clearAllMocks();api.filterCatalog.mockResolvedValue({registry_version_id:'registry',dataset_version_id:'dataset',mandatory_expression:predicate,resource_policy_version_id:'policy',fields:[{field:{field_id:'Receipt.status',version_id:'field',entity:'Receipt',column:'status',data_type:'string',operators:['eq','ne','is_null'],null_policy:'not_matched'},label:{en:'Receipt status',ru:'Статус чека'},description:{en:'Published receipt status',ru:'Статус'}}]});});
afterEach(cleanup);
function show(onChange=vi.fn()) {render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><ReceiptFilterEditor dataset="dataset" value={value} locale="en" onChange={onChange}/></QueryClientProvider>);return onChange;}
it('editing and Reset/Undo preserve parent until explicit validated apply',async()=>{
 const change=show();await screen.findByText(/Mandatory access restrictions/);const input=screen.getAllByLabelText('Value')[0];
 fireEvent.change(input,{target:{value:'draft'}});expect(change).not.toHaveBeenCalled();fireEvent.click(screen.getByText('Reset to initial'));expect((screen.getAllByLabelText('Value')[0] as HTMLInputElement).value).toBe('completed');fireEvent.click(screen.getByText('Undo change'));expect((screen.getAllByLabelText('Value')[0] as HTMLInputElement).value).toBe('draft');
 api.filterPreview.mockResolvedValue({request_hash:'hash',matched_count:2,authorized_count:5,unknown_count:0,not_matched_count:3,preview_kind:'exact'});
 fireEvent.click(screen.getByText('Apply filter to block'));await waitFor(()=>expect(change).toHaveBeenCalledWith(expect.objectContaining({expression:expect.objectContaining({values:[{data_type:'string',value:'draft'}]})})));
});
it('aborts superseded preview and refuses late success or late error',async()=>{
 show();await screen.findByText(/Mandatory access restrictions/);let finish!:(value:unknown)=>void;api.filterPreview.mockImplementation(()=>new Promise(resolve=>{finish=resolve;}));
 fireEvent.click(screen.getByText('Check draft'));await waitFor(()=>expect(api.filterPreview).toHaveBeenCalledOnce());const signal=api.filterPreview.mock.calls[0][2] as AbortSignal;
 fireEvent.change(screen.getAllByLabelText('Value')[0],{target:{value:'new-context'}});expect(signal.aborted).toBe(true);
 await act(async()=>finish({request_hash:'old',matched_count:999,authorized_count:999,unknown_count:0}));expect(screen.queryByText(/999/)).toBeNull();
});
