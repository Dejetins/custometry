import {describe,it,expect} from 'vitest';
import {metricNumber,fullMetricNumber,percentNumber} from './metric-number';
describe('metric presentation policy',()=>{
 it.each([[1,'1'],[7.68,'8'],[183.7,'184'],[999,'999'],[999.5,'1k'],[1000,'1k'],[1250,'1.3k'],[2144,'2.1k'],[12480,'12.5k'],[393858.68,'393.9k'],[999950,'1m'],[2144000,'2.1m'],[999999999,'1b'],[12480000000,'12.5b'],[100000000000,'100b'],[-393858.68,'-393.9k'],[0,'0']] as const)('formats %s',(n,expected)=>expect(metricNumber(n,'en')).toBe(expected));
 it('localizes decimals but keeps suffixes',()=>expect(metricNumber(393858.68,'ru')).toBe('393,9k'));
 it('keeps full rounded value on hover',()=>expect(fullMetricNumber(393858.68,'en')).toBe('393,859'));
 it('formats signed changes',()=>expect(metricNumber(33561,'en',true)).toBe('+33.6k'));
 it.each([null,undefined,'',NaN,Infinity])('does not manufacture missing values: %s',n=>expect(metricNumber(n,'en')).toBe('—'));
 it('caps percentages and removes trailing zeros and negative zero',()=>{
  expect(percentNumber(7.95,'en')).toBe('8%');
  expect(percentNumber(-7.94,'ru',true)).toBe('-7,9%');
  expect(percentNumber(-.01,'en',true)).toBe('0%');
 });
});
