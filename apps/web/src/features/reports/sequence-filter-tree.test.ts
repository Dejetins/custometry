import {expect,it} from 'vitest';
import {utcMicros,microsUtc,relativeWindow,secondsMicros,validOrder,orderedSteps} from './sequence-filter-tree';
import type {composerReports as C} from '@custometry/contracts';
const anchor='2026-10-07T18:25:25.440829Z';
it('resolves publication-relative windows without rounding microseconds',()=>{
 const window=relativeWindow({kind:'fixed',timezone:'UTC',starts_at:'2025-01-01T00:00:00Z',ends_at:anchor,observation_as_of:anchor,knowledge_as_of:anchor},-1000001,-1);
 expect(window.anchor).toBe(anchor);expect(window.starts_at).toBe('2026-10-07T18:25:24.440828Z');expect(window.ends_at).toBe('2026-10-07T18:25:25.440828Z');
 expect(microsUtc(utcMicros(anchor))).toBe(anchor);expect(microsUtc(utcMicros('1969-12-31T23:59:59.999999Z'))).toBe('1969-12-31T23:59:59.999999Z');
});
it('parses exact gap seconds and refuses precision and policy overflow',()=>{
 expect(secondsMicros('1.000001')).toBe(1000001);expect(secondsMicros('315360000')).toBe(315360000000000);
 for(const value of ['','-1','0.0000001','315360001','NaN'])expect(()=>secondsMicros(value)).toThrow();
});
it('preserves negative anchors and makes a new first positive gapless',()=>{
 const first={kind:'positive',step_id:'a',gap:null} as C.PositiveStep,second={kind:'positive',step_id:'b',gap:{minimum_us:1,maximum_us:2}} as C.PositiveStep;
 const absent={kind:'negative',step_id:'n',after_step_id:'a'} as C.NegativeStep;
 expect(validOrder([first,absent,second])).toBe(true);expect(validOrder([second,absent,first])).toBe(false);expect(validOrder([absent])).toBe(false);
 expect(orderedSteps([second,first])[0]).toEqual({...second,gap:null});expect(orderedSteps([second,first])[1]).toEqual({...first,gap:{minimum_us:0,maximum_us:86400000000}});
});
