import {render,screen,fireEvent,cleanup} from '@testing-library/react';
import {afterEach,expect,it,vi} from 'vitest';
import {ComposerBlockMenu} from './ComposerBlockMenu';
afterEach(cleanup);
function setup(){
 const action=vi.fn();const rendered=render(<section className="composer"><button>Outside</button><ComposerBlockMenu className="composer-size-menu" label="Layout A"><button onClick={action}>Half</button><div data-menu-keep-open><button>Increase</button></div></ComposerBlockMenu><ComposerBlockMenu className="composer-actions-menu" label="Actions B"><button>Recalculate</button></ComposerBlockMenu></section>);
 const first=screen.getByText('Layout A');const second=screen.getByText('Actions B');
 const open=()=>rendered.container.querySelectorAll('details[open]');
 return {...rendered,first,second,open,action};
}
it('switches between blocks and menu types without accumulating disclosures; repeat click closes',()=>{
 const {first,second,open}=setup();fireEvent.click(first);expect(open()).toHaveLength(1);
 fireEvent.click(second);expect(open()).toHaveLength(1);expect(open()[0].textContent).toContain('Actions B');
 fireEvent.click(first);expect(open()).toHaveLength(1);expect(open()[0].textContent).toContain('Layout A');
 fireEvent.click(first);expect(open()).toHaveLength(0);
});
it('dismisses on outside pointer or keyboard focus, but preserves internal interaction',()=>{
 const {first,open}=setup();fireEvent.click(first);fireEvent.pointerDown(screen.getByText('Increase'));expect(open()).toHaveLength(1);
 fireEvent.pointerDown(screen.getByText('Outside'));expect(open()).toHaveLength(0);
 fireEvent.click(first);screen.getByText('Outside').focus();expect(open()).toHaveLength(0);
});
it('Escape closes from inside and returns focus to its trigger',()=>{
 const {first,open}=setup();fireEvent.click(first);const action=screen.getByText('Half');action.focus();fireEvent.keyDown(action,{key:'Escape'});
 expect(open()).toHaveLength(0);expect(document.activeElement).toBe(first);
});
it('keeps open and follows its anchor on scroll and resize, without reacting to internal scroll',()=>{
 const {first,open,container}=setup();fireEvent.click(first);
 const panel=container.querySelector('details > div') as HTMLElement;
 let top=300;vi.spyOn(first,'getBoundingClientRect').mockImplementation(()=>({left:100,bottom:top} as DOMRect));
 fireEvent.scroll(document);expect(open()).toHaveLength(1);expect(panel.style.top).toBe('306px');
 top=240;fireEvent.scroll(document);expect(open()).toHaveLength(1);expect(panel.style.top).toBe('246px');
 top=200;fireEvent.scroll(panel);expect(panel.style.top).toBe('246px');
 fireEvent(window,new Event('resize'));expect(open()).toHaveLength(1);expect(panel.style.top).toBe('206px');
});
it('selection executes once then closes; height stepper stays open',()=>{
 const {first,open,action}=setup();fireEvent.click(first);fireEvent.click(screen.getByText('Increase'));expect(open()).toHaveLength(1);
 const half=screen.getByText('Half');half.focus();fireEvent.click(half);expect(action).toHaveBeenCalledTimes(1);expect(open()).toHaveLength(0);expect(document.activeElement).toBe(first);
});
it('removes document listeners on unmount',()=>{
 const {first,unmount}=setup();fireEvent.click(first);const remove=vi.spyOn(document,'removeEventListener');unmount();
 expect(remove).toHaveBeenCalledWith('pointerdown',expect.any(Function),true);
 expect(remove).toHaveBeenCalledWith('keydown',expect.any(Function));remove.mockRestore();
});
