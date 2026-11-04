type Value = string | number | null | undefined;
function numeric(value: Value): number | null {
 if(value == null || value === '') return null;
 const n=Number(value);
 return Number.isFinite(n)?n:null;
}
function display(n:number,locale:'ru'|'en',digits:number,signed=false){
 return new Intl.NumberFormat(locale,{maximumFractionDigits:digits,signDisplay:signed?'exceptZero':'auto'}).format(Object.is(n,-0)?0:n);
}
/** Compact KPI presentation only; source values and calculations remain unchanged. */
export function metricNumber(value:Value,locale:'ru'|'en',signed=false):string{
 const n=numeric(value);
 if(n===null)return '—';
 const magnitude=Math.abs(n);
 let scale=magnitude>=1e9?3:magnitude>=1e6?2:magnitude>=1e3?1:0;
 let rounded=Math.round((magnitude/1000**scale)* (scale?10:1))/(scale?10:1);
 if(rounded>=1000&&scale<3){scale++;rounded=1;}
 return display(n<0?-rounded:rounded,locale,scale?1:0,signed)+['','k','m','b'][scale];
}
export function fullMetricNumber(value:Value,locale:'ru'|'en'):string{
 const n=numeric(value);
 return n===null?'—':display((n<0?-1:1)*Math.round(Math.abs(n)),locale,0);
}
/** Input is percentage points (7.25 means 7.25%), not a ratio. */
export function percentNumber(value:Value,locale:'ru'|'en',signed=false):string{
 const n=numeric(value);
 if(n===null)return '—';
 const rounded=(n<0?-1:1)*Math.round(Math.abs(n)*10)/10;
 return display(rounded,locale,1,signed)+'%';
}
