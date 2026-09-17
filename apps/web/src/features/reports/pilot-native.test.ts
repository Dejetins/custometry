import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {describe,it,expect} from 'vitest';
import {pilotPeriod} from './pilot-period';
describe('native pilot integration',()=>{
 it('retains the entire source document, removing executable script tags only',()=>{
  const original=readFileSync(resolve(process.cwd(),'../../docs/architecture/ui/target-pilot/ru/source.html'),'utf8');
  const adapted=readFileSync(resolve(process.cwd(),'src/features/reports/pilot/document.html'),'utf8');
  expect(adapted).toBe(original.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g,''));
 });
 it('maps native calendar selections to API dates including ISO weeks and leap years',()=>{
  expect(pilotPeriod({grain:'week',value:'2025-W01'})).toEqual({start:'2024-12-30',end:'2025-01-05'});
  expect(pilotPeriod({grain:'month',value:'2024-02'})).toEqual({start:'2024-02-01',end:'2024-02-29'});
  expect(pilotPeriod({grain:'quarter',value:'2025-Q2'})).toEqual({start:'2025-04-01',end:'2025-06-30'});
  expect(pilotPeriod({grain:'day',value:'2025-11-30'})).toEqual({start:'2025-11-30',end:'2025-11-30'});
 });
});
