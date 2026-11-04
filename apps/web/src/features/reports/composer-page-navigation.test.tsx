import {render,screen,fireEvent,cleanup} from '@testing-library/react';
import {afterEach,expect,it,vi} from 'vitest';
import {ComposerStructure} from './ComposerStructure';
import type {Definition} from './composer-state';
afterEach(cleanup);
function setup(count:number){
 const ref={id:'ref',content_hash:'a'.repeat(64)};
 const definition:Definition={document_id:'doc',creator_principal_id:'author',title:'Report',profile:'workbook_report',default_page_id:'p0',brand_profile:ref,company_pack:ref,sections:[],blocks:[],definitions:[],pages:Array.from({length:count},(_,i)=>({page_id:`p${i}`,order:i,title:`Page ${i+1}`,layout:'flow'}))};
 const activate=vi.fn();render(<ComposerStructure definition={definition} activePage="p0" activate={activate} commit={vi.fn()} locale="en" readOnly busy={false} undo={vi.fn()} redo={vi.fn()} canUndo={false} canRedo={false}/>);return activate;
}
it('single-page saved report keeps its tab without redundant search and selector',()=>{
 setup(1);expect(screen.getByRole('tab',{name:'Page 1'}).getAttribute('aria-selected')).toBe('true');expect(screen.queryByRole('searchbox')).toBeNull();expect(screen.queryByRole('combobox',{name:'All pages'})).toBeNull();
});
it('multi-page navigation retains search, direct selection and arrow navigation',()=>{
 const activate=setup(3);fireEvent.keyDown(screen.getByRole('tab',{name:'Page 1'}),{key:'ArrowRight'});expect(activate).toHaveBeenCalledWith('p1');fireEvent.change(screen.getByRole('searchbox'),{target:{value:'Page 3'}});expect(screen.queryByRole('tab',{name:'Page 1'})).toBeNull();fireEvent.click(screen.getByRole('tab',{name:'Page 3'}));expect(activate).toHaveBeenCalledWith('p2');fireEvent.change(screen.getByRole('combobox',{name:'All pages'}),{target:{value:'p0'}});expect(activate).toHaveBeenCalledWith('p0');
});
