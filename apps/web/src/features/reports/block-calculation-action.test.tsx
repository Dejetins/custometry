import {render,screen,cleanup,fireEvent} from '@testing-library/react';
import {afterEach,it,expect,vi} from 'vitest';
import {BlockCalculationAction} from './BlockCalculationAction';
afterEach(cleanup);
const base={ready:true,failed:false,loading:false,preview:false,disabled:false,locale:'en' as const,run:vi.fn()};
it('ready blocks expose recalculation only in the menu',()=>{const run=vi.fn();render(<><BlockCalculationAction {...base} location="header" run={run}/><BlockCalculationAction {...base} location="menu" run={run}/></>);expect(screen.getAllByRole('button')).toHaveLength(1);fireEvent.click(screen.getByRole('button',{name:'Recalculate'}));expect(run).toHaveBeenCalledOnce();});
it('changed query exposes Calculate in the header, not a duplicate in menu',()=>{render(<><BlockCalculationAction {...base} ready={false} location="header"/><BlockCalculationAction {...base} ready={false} location="menu"/></>);expect(screen.getAllByRole('button')).toHaveLength(1);expect(screen.getByRole('button',{name:'Calculate'})).toBeTruthy();});
it('loading blocks prevent duplicate requests',()=>{const run=vi.fn();render(<BlockCalculationAction {...base} loading location="header" run={run}/>);fireEvent.click(screen.getByRole('button'));expect(run).not.toHaveBeenCalled();});
it('saved preview offers retry only for a failed result read',()=>{const {rerender}=render(<BlockCalculationAction {...base} preview location="header"/>);expect(screen.queryByRole('button')).toBeNull();rerender(<BlockCalculationAction {...base} preview failed location="header"/>);expect(screen.getByRole('button',{name:'Retry'})).toBeTruthy();});
