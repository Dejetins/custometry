import {describe,it,expect} from 'vitest';
import {quickPeriod} from './ReportPeriodPicker';
import {pilotPeriod} from './pilot-period';
describe('calendar shortcuts',()=>{
 it('starts weeks on Monday across year boundaries',()=>expect(quickPeriod('week',false,new Date(2025,0,1))).toEqual({start:'2024-12-30',end:'2025-01-05'}));
 it('handles leap February and previous year',()=>{expect(quickPeriod('month',true,new Date(2024,2,1))).toEqual({start:'2024-02-01',end:'2024-02-29'});expect(quickPeriod('year',true,new Date(2025,0,1))).toEqual({start:'2024-01-01',end:'2024-12-31'});});
 it('selects calendar quarters and retains custom dates',()=>{expect(quickPeriod('quarter',true,new Date(2025,0,1))).toEqual({start:'2024-10-01',end:'2024-12-31'});expect(pilotPeriod({grain:'custom',value:'2025-02-03/2025-02-21'})).toEqual({start:'2025-02-03',end:'2025-02-21'});});
});
