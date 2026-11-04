import {describe,it,expect} from 'vitest';
import {rowsToCsv} from './result-export';
describe('pilot CSV export safety',()=>{
 it('escapes quoted multiline labels and neutralizes formulas including leading whitespace',()=>{const csv=rowsToCsv([['Period','Value'],['a,"b"\nc',1.25],[' =HYPERLINK("x")',-12],['@SUM(A1)',0]]);expect(csv).toContain('"a,""b""\nc","1.25"');expect(csv).toContain('"\' =HYPERLINK(""x"")","-12"');expect(csv).toContain('"\'@SUM(A1)","0"');});
 it('preserves null-as-blank and exact high precision decimal text',()=>{expect(rowsToCsv([['','123456789012345.6789']])).toBe('\ufeff"","123456789012345.6789"');});
});
