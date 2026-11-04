import type {configuredReports as W} from '@custometry/contracts';
export type Change=Pick<W.ComparisonValues,'absolute_delta'|'relative_delta_percent'|'reason_codes'>;
export const finite=(value:unknown):number|null=>typeof value==='string'&&value.trim()!==''&&Number.isFinite(Number(value))?Number(value):null;
export function direction(value:unknown):'positive'|'negative'|'neutral'{const n=finite(value);return n===null||n===0?'neutral':n>0?'positive':'negative';}
export function signed(value:unknown,locale:'ru'|'en',digits?:number):string{const n=finite(value);return n===null?'—':new Intl.NumberFormat(locale,{...(digits!==undefined?{maximumFractionDigits:digits}:n!==0&&Math.abs(n)<.01?{maximumSignificantDigits:2}:{maximumFractionDigits:2}),signDisplay:'exceptZero'}).format(n===0?0:n);}
export function aggregateYearChange(binding:W.CardResultBinding|undefined,result:W.WorkspaceResultV2|undefined):Change|null{
 if(!binding||!result||result.result_id!==binding.result.result_id||result.temporal?.alignment!=='previous_year_same_dates')return null;
 const value=result.temporal.changes[binding.bucket_projection];if(!value||typeof value!=='object')return null;
 const change=value as Record<string,unknown>;
 if(!['absolute_delta','relative_delta_percent'].every(k=>change[k]===null||finite(change[k])!==null)||!Array.isArray(change.reason_codes)||!change.reason_codes.every(c=>typeof c==='string'))return null;
 return change as Change;
}
// Only axis bounds are derived here; server values and deltas are never changed.
export function lineAxisRange(values:readonly (string|null)[],integer=false):{min:number;max:number;interval:number}{
 const numbers=values.map(finite).filter((n):n is number=>n!==null);
 if(!numbers.length)return {min:0,max:1,interval:integer?1:.25};
 const low=Math.min(0,...numbers),high=Math.max(0,...numbers),span=high-low;
 if(span===0)return {min:0,max:1,interval:integer?1:.25};
 const padding=span>0?span*.12:Math.max(Math.abs(low)*.1,integer?1:.1);
 const lower=low<0?low-padding:0,upper=high>0?high+padding:0;
 const target=(upper-lower)/4;
 const magnitude=10**Math.floor(Math.log10(target));
 const step=[1,2,2.5,5,10].find(n=>n*magnitude>=target)!*magnitude;
 const interval=integer?Math.max(1,Math.ceil(step)):step;
 const round=(n:number)=>Number(n.toPrecision(12));
 return {min:round(Math.floor(lower/interval)*interval),max:round(Math.ceil(upper/interval)*interval),interval:round(interval)};
}

// Display-only comparison of adjacent plotted points; never skip missing buckets.
export function adjacentChange(current:unknown,previous:unknown){
 const value=finite(current),baseline=finite(previous);
 if(value===null||baseline===null)return null;
 const absolute=value-baseline;
 return {absolute:String(absolute),relative:baseline===0?null:String(absolute/Math.abs(baseline)*100)};
}
