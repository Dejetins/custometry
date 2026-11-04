import {render,screen,waitFor,cleanup} from '@testing-library/react';
import {QueryClient,QueryClientProvider} from '@tanstack/react-query';
import {MemoryRouter} from 'react-router-dom';
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest';
const api=vi.hoisted(()=>({context:vi.fn(),prepareNew:vi.fn(),editor:vi.fn()}));
vi.mock('./report-api',()=>({reportApi:{context:api.context},csrf:()=>''}));
vi.mock('./workspace-api',()=>({workspaceReports:{prepareNew:api.prepareNew}}));
vi.mock('./ConfiguredWorkspace',()=>({ConfiguredWorkspace:(props:unknown)=>{api.editor(props);return <div>Shared editor</div>;},PendingWorkspace:()=> <div>Preparing</div>}));
vi.mock('./PilotChrome',()=>({PilotFrame:({children}:{children:React.ReactNode})=><div>{children}</div>}));
vi.mock('react-i18next',()=>({useTranslation:()=>({i18n:{resolvedLanguage:'ru'}})}));
import {NewConfiguredWorkspace} from './NewConfiguredWorkspace';
function show(template='sales',trusted=true){return render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><MemoryRouter initialEntries={[{pathname:'/w/workspace/reports/new/edit',state:{template}}]}><NewConfiguredWorkspace workspace="workspace" trusted={trusted} channelUnavailable={false} retryChannel={()=>{}}/></MemoryRouter></QueryClientProvider>);}
beforeEach(()=>{vi.clearAllMocks();api.context.mockResolvedValue({datasets:[{id:'dataset',label:'Northwind'}],default_period:{starts_on:'2025-01-01',ends_on:'2025-11-30'}});api.prepareNew.mockResolvedValue({actor:{principal_id:'author',workspace_id:'workspace'},definition:{report_id:'new-id',title:'New report'}});});
afterEach(cleanup);
describe('new reports use the configured editor',()=>{
 it.each(['blank','sales'])('prepares %s from authorized source defaults and opens the shared editor',async template=>{show(template);await screen.findByText('Shared editor');expect(api.prepareNew).toHaveBeenCalledWith(expect.objectContaining({template,semantic_dataset_version_id:'dataset',common_context:{starts_on:'2025-01-01',ends_on:'2025-11-30',store_ids:null}}),'');expect(api.editor).toHaveBeenCalledWith(expect.objectContaining({workspace:'workspace',preview:false,initialDefinition:{report_id:'new-id',title:'New report'}}));});
 it('does not prepare before session access is trusted',async()=>{show('sales',false);await waitFor(()=>expect(screen.getByText('Preparing')).toBeDefined());expect(api.context).not.toHaveBeenCalled();expect(api.prepareNew).not.toHaveBeenCalled();});
 it('does not silently choose among multiple sources',async()=>{api.context.mockResolvedValue({datasets:[{id:'one',label:'First'},{id:'two',label:'Second'}],default_period:{}});show();await screen.findByText('Выберите источник для отчёта');expect(api.prepareNew).not.toHaveBeenCalled();});
});
