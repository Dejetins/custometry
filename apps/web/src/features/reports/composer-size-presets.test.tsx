import {render,screen,fireEvent,cleanup} from '@testing-library/react';
import {afterEach,expect,it,vi} from 'vitest';
import {ComposerLayoutControls,snapBlockWidth} from './ComposerLayoutControls';
afterEach(cleanup);
it('offers four visual widths, preserving a custom saved width until selection',()=>{const change=vi.fn();const {container}=render(<ComposerLayoutControls id="b" title="Chart" span={2} rows={1} grid disabled={false} locale="en" change={change}/>);const details=container.querySelector('details')!;details.open=true;const group=screen.getByRole('group',{name:'Block width'});expect(group.querySelectorAll('button')).toHaveLength(4);expect(change).not.toHaveBeenCalled();fireEvent.click(screen.getByRole('button',{name:'Medium'}));expect(change).toHaveBeenCalledWith({span:6});expect(screen.queryByRole('combobox')).toBeNull();});
it('pointer widths snap to four readable sizes',()=>{expect([1,2,3,4,5,6,7,8,9,10,11,12,20].map(snapBlockWidth)).toEqual([3,3,3,3,6,6,6,9,9,9,12,12,12]);});
