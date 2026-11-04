import {fireEvent,render,screen,cleanup} from '@testing-library/react';
import {afterEach,beforeEach,it,expect,vi} from 'vitest';
import {VisualizationViewMenu} from './VisualizationViewMenu';
beforeEach(()=>{
 Object.defineProperty(HTMLElement.prototype,'showPopover',{configurable:true,value:vi.fn()});
 Object.defineProperty(HTMLElement.prototype,'hidePopover',{configurable:true,value:vi.fn()});
});
afterEach(()=>{cleanup();vi.restoreAllMocks();});
it('focuses the first applicable setting and restores the trigger on Escape',()=>{
 render(<VisualizationViewMenu locale="en" table={false}><label>Grain<select defaultValue="day"><option>day</option></select></label></VisualizationViewMenu>);
 const trigger=screen.getByRole('button',{name:'View'});const grain=screen.getByRole('combobox',{name:'Grain'});
 fireEvent.click(trigger);expect(HTMLElement.prototype.showPopover).toHaveBeenCalledOnce();expect(document.activeElement).toBe(grain);
 fireEvent.keyDown(grain,{key:'Escape'});expect(HTMLElement.prototype.hidePopover).toHaveBeenCalledOnce();expect(document.activeElement).toBe(trigger);
});
it('keeps controlled settings connected through mode changes without resetting them',()=>{
 const change=vi.fn();const settings=<label>Grain<select value="week" onChange={change}><option>day</option><option>week</option></select></label>;
 const view=render(<VisualizationViewMenu locale="en" table={false}>{settings}</VisualizationViewMenu>);
 fireEvent.change(screen.getByRole('combobox'),{target:{value:'day'}});expect(change).toHaveBeenCalledOnce();
 view.rerender(<VisualizationViewMenu locale="en" table>{settings}</VisualizationViewMenu>);
 expect((screen.getByRole('combobox') as HTMLSelectElement).value).toBe('week');
});
