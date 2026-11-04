import {useState} from 'react';
import {QueryClient,QueryClientProvider} from '@tanstack/react-query';
import {render,screen,fireEvent,cleanup} from '@testing-library/react';
import {afterEach,expect,it} from 'vitest';
import type {Definition} from './composer-state';
import {ComposerInspector} from './ComposerInspector';
afterEach(cleanup);
const id=()=>crypto.randomUUID();
function fixture():Definition{
 const doc=id(),page=id(),section=id(),source=id(),metric={metric_id:'net_revenue' as const,version_id:id(),content_hash:'a'.repeat(64)},ref={id:id(),content_hash:'a'.repeat(64)};
 return {document_id:doc,creator_principal_id:id(),profile:'workbook_report',title:'Document',default_page_id:page,brand_profile:ref,company_pack:ref,chapters:[],pages:[{page_id:page,order:0,title:'One',layout:'dashboard_grid'}],sections:[{section_id:section,page_id:page,order:0,title:'Results'}],definitions:[{definition_id:source,query:{semantic_dataset_version_id:id(),common:{starts_on:'2025-01-01',ends_on:'2025-01-31',store_ids:null},local_store_ids:null,grain:'day',calendar_ref:{version_id:id(),content_hash:'a'.repeat(64)},calendar_basis:'calendar',alignment:'none',metric_refs:[metric]}}],blocks:[{block_id:id(),section_id:section,order:0,block_type:'table',source:{definition_id:source,metric_ref:metric},presentation:{title:'Revenue'},placement:{column:0,span:6,row:0,row_span:1}}]};
}


it('updates text before blur while preserving the focused textarea and caret',()=>{
 const base=fixture();const initial:Definition={...base,blocks:[{...base.blocks[0],block_type:'text',source:null,text:'Раз два'}]};
 function Editor(){const [d,setD]=useState(initial);return <><ComposerInspector definition={d} block={d.blocks[0]} locale="ru" busy={false} commit={setD} close={()=>{}} onValidating={()=>{}}/><output data-testid="canvas-text">{d.blocks[0].text}</output></>;}
 render(<QueryClientProvider client={new QueryClient()}><Editor/></QueryClientProvider>);
 expect(screen.queryByRole('button',{name:'Блок'})).toBeNull();
 const input=screen.getByLabelText('Текст') as HTMLTextAreaElement;input.focus();
 fireEvent.change(input,{target:{value:'Раз два три'}});
 expect(screen.getByTestId('canvas-text').textContent).toBe('Раз два три');
 expect(screen.getByLabelText('Текст')).toBe(input);expect(document.activeElement).toBe(input);
 input.setSelectionRange(4,4);fireEvent.change(input,{target:{value:'Раз ещё два три',selectionStart:8,selectionEnd:8}});
 expect(screen.getByTestId('canvas-text').textContent).toBe('Раз ещё два три');expect(input.selectionStart).toBe(8);
 fireEvent.change(input,{target:{value:''}});expect(screen.getByTestId('canvas-text').textContent).toBe('');
});
