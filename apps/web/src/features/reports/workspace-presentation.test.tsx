import {describe,it,expect} from 'vitest';
import {render,cleanup} from '@testing-library/react';
import type {configuredReports as W} from '@custometry/contracts';
import {aggregateYearChange,lineAxisRange,direction,signed,adjacentChange} from './workspace-presentation';
import {CardYearChange} from './CardYearChange';
const delta=(absolute:string|null,percent:string|null,reasons:string[]=[])=>({absolute_delta:absolute,relative_delta_percent:percent,reason_codes:reasons});
const binding={bucket_projection:'receipt_count',result:{result_id:'receipts'}} as W.CardResultBinding;
const result={result_id:'receipts',temporal:{alignment:'previous_year_same_dates',changes:{receipt_count:delta('5','2.44'),net_revenue:delta('-999','-99')}}} as unknown as W.WorkspaceResultV2;
describe('server aggregate display',()=>{
 it('uses the bound card metric aggregate, not selected chart or bucket percentages',()=>{expect(aggregateYearChange(binding,result)).toEqual(delta('5','2.44'));expect(aggregateYearChange({...binding,result:{...binding.result,result_id:'other'}},result)).toBeNull();});
 it('keeps null/malformed data unknown and zero neutral',()=>{expect(aggregateYearChange(binding,{...result,temporal:{...result.temporal!,changes:{receipt_count:delta('Infinity',null)}}})).toBeNull();expect(direction('0')).toBe('neutral');expect(direction('-0')).toBe('neutral');expect(signed(null,'en')).toBe('—');expect(signed('5','en')).toBe('+5');expect(signed('-2','en')).toBe('-2');expect(signed('0.001','en')).toBe('+0.001');expect(signed('-0.001','en')).toBe('-0.001');});
 it.each([[null,null,['COVERAGE_INCOMPLETE'],'Insufficient data'],['10',null,['ZERO_BASELINE'],'baseline 0'],['0','0',[],'0 · 0%'],['-4','-20',[],'-4 · -20%']] as const)('renders aggregate %s / %s without inventing values',(a,b,codes,text)=>{
  const r={...result,temporal:{...result.temporal!,changes:{receipt_count:delta(a,b,[...codes])}}};const {container}=render(<CardYearChange binding={binding} result={r} enabled applied loading={false} locale="en"/>);expect(container.textContent).toContain(text);expect(container.textContent).not.toContain('Infinity');cleanup();
 });
 it('suppresses YoY for disabled comparison or unapplied context',()=>{const {container,rerender}=render(<CardYearChange binding={binding} result={result} enabled={false} applied loading={false} locale="en"/>);expect(container.textContent).toBe('YoY off');rerender(<CardYearChange binding={binding} result={result} enabled applied={false} loading={false} locale="en"/>);expect(container.textContent).toBe('');cleanup();});
});
describe('owner presentation precision',()=>{
 it('rounds card deltas to whole units and percentage deltas to at most one decimal without scaling',()=>{expect(signed('10991.68','en',0)).toBe('+10,992');expect(signed('33.3922697','en',1)).toBe('+33.4');expect(signed('-1.59574468','en',1)).toBe('-1.6');expect(signed('0','en',1)).toBe('0');expect(signed('1000000.52','en',0)).toBe('+1,000,001');});
});
describe('zero-inclusive line axes',()=>{
 it.each([['6','7'],['0','0'],['6','6'],['-7','-6'],['-2','3'],['0.002','0.004']])('contains zero and all finite values %j',(...values)=>{const range=lineAxisRange(values);expect(range.min).toBeLessThanOrEqual(Math.min(0,...values.map(Number)));expect(range.max).toBeGreaterThanOrEqual(Math.max(0,...values.map(Number)));expect(range.max).toBeGreaterThan(range.min);expect(range.interval).toBeGreaterThan(0);});
 it('count axis starts at zero with integral ticks',()=>{const range=lineAxisRange(['6','7'],true);expect(range.min).toBe(0);expect(Number.isInteger(range.interval)).toBe(true);});
 it('revenue dips retain a visible zero baseline',()=>{const range=lineAxisRange(['1099.3','1498.6']);expect(range.min).toBe(0);expect(range.max).toBeGreaterThan(1498.6);});
 it('empty/unknown does not invent observations',()=>{expect(lineAxisRange([null,'NaN'])).toEqual({min:0,max:1,interval:.25});});
 it('independent units retain their separate magnitudes',()=>{expect(lineAxisRange(['6','7'],true).max).toBeLessThan(lineAxisRange(['6000','7000']).max);});
});

describe('adjacent plotted value comparison',()=>{
 it('compares to the immediate value and keeps the sign',()=>{expect(adjacentChange('90','100')).toEqual({absolute:'-10',relative:'-10'});expect(adjacentChange('-90','-100')).toEqual({absolute:'10',relative:'10'});});
 it('does not invent percentages at zero or values across missing points',()=>{expect(adjacentChange('5','0')).toEqual({absolute:'5',relative:null});expect(adjacentChange('5',null)).toBeNull();expect(adjacentChange(null,'5')).toBeNull();});
});
