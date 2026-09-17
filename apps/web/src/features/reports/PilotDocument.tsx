import {useEffect,useRef,useState} from 'react';
import * as echarts from 'echarts/core';
import {LineChart} from 'echarts/charts';
import {GridComponent,TooltipComponent,LegendComponent,DataZoomComponent,TitleComponent,AriaComponent} from 'echarts/components';
import {SVGRenderer} from 'echarts/renderers';
import {compileLineChart} from '@custometry/chart-compiler';
import {reportCopy} from './copy';
import {checkReferences} from './ReportChart';
import type {Actor,References,Result} from './report-api';
import documentSource from './pilot/document.html?raw';
import {mountPilot} from './pilot/runtime';
echarts.use([LineChart,GridComponent,TooltipComponent,LegendComponent,DataZoomComponent,TitleComponent,AriaComponent,SVGRenderer]);
export interface PilotModel {
 locale:'ru'|'en';title:string;source:string;start:string;end:string;store:string;comparison:string;
 result?:Result;refs?:References;actor:Actor;status:string;error?:string;hint:string;
 busy:boolean;preview:boolean;focus:boolean;unapplied:boolean;conflict:boolean;stores:readonly {id:string;label:string}[];
}
export interface PilotActions {
 apply:(value:{period:{grain:string;value:string};store:string;comparison:'none'|'previous_year_same_dates'})=>void;
 library:()=>void;draft:PilotActions['apply'];save:(title:string)=>void;reload:()=>void;preview:()=>void;title:(title:string)=>void;
 locale:(locale:'ru'|'en')=>void;urlChanged:(href:string)=>void;
}
const escape=(v:unknown)=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
function tableRows(model:PilotModel,locale:'ru'|'en',prior=false){
 const c=reportCopy[locale];const result=model.result;const daily=prior?result?.comparison?.daily:result?.daily;if(!result||!daily)return `<caption>${escape(c.pending)}</caption>`;
 const values=(daily:Result['daily'],prior=false)=>(['net_revenue','receipt_count','average_receipt'] as const).map(k=>`<tr><th scope="row">${escape(prior?c.prior+' · ':'')}${escape(c[k])}${k==='receipt_count'?'':' · EUR'}</th>${daily.map(r=>`<td data-metric="${k}" data-date="${r.date}" data-value="${escape(r[k])}">${r[k]===null?'—':escape(new Intl.NumberFormat(locale,{maximumFractionDigits:k==='receipt_count'?0:2}).format(Number(r[k])))}</td>`).join('')}</tr>`).join('')+`<tr><th scope="row">${escape(prior?c.prior+' · ':'')}${escape(c.state)}</th>${daily.map(r=>`<td>${escape(c[r.state])}</td>`).join('')}</tr>`;
 return `<caption>${escape(prior?c.prior:c.current)} · EUR · UTC</caption><thead><tr><th scope="col">${escape(c.date)}</th>${daily.map(r=>`<th scope="col">${r.date}</th>`).join('')}</tr></thead><tbody>${values(daily,prior)}</tbody>`;
}
export function PilotDocument({model,actions}:{model:PilotModel;actions:PilotActions}){
 const frame=useRef<HTMLIFrameElement>(null);const current=useRef({model,actions});current.current={model,actions};
 const runtime=useRef<ReturnType<typeof mountPilot>|undefined>(undefined);const chart=useRef<ReturnType<typeof compileLineChart>['option']|undefined>(undefined);
 const [loaded,setLoaded]=useState(0);
 useEffect(()=>{let cancelled=false;chart.current=undefined;if(!model.result||!model.refs){runtime.current?.update();return;}
  const {result,refs,actor}=model;
  void checkReferences(refs).then(()=>{
   const metric=result.metrics[0];if(!refs.company_pack.payload.metric_versions.some(m=>m.version_id===metric.version_id&&m.content_hash===metric.content_hash))throw Error('METRIC_REFERENCE_MISMATCH');
   const compiled=compileLineChart(refs.chart_spec.payload,{workspaceId:actor.workspace_id,ownerPrincipalId:actor.principal_id,policyHash:result.policy_hash,artifactId:String(result.manifest.artifact_id),artifactHash:String(result.manifest.content_hash),parameters:result.parameters,metricVersionId:String(metric.version_id),metricHash:String(metric.content_hash),daily:result.daily,comparison:result.comparison?.daily??null},{locale:model.locale,primary:'#66b9d3',comparison:'#a8b3ba',text:'#999a9e',grid:'#292a2e'});
   if(cancelled)return;chart.current=compiled.option;runtime.current?.update();frame.current?.setAttribute('data-chart-ready','true');
  }).catch(()=>{if(!cancelled){chart.current=undefined;frame.current?.setAttribute('data-chart-ready','false');}});
  return()=>{cancelled=true;};
 },[model.result,model.refs,model.actor,model.locale]);
 useEffect(()=>{
  const document=frame.current?.contentDocument;const window=frame.current?.contentWindow;if(!document||!window||!loaded)return;
  const bridge={model:()=>current.current.model,url:()=>globalThis.location.href,
   library:()=>current.current.actions.library(),
   title:(title:string)=>current.current.actions.title(title),locale:(locale:'ru'|'en')=>current.current.actions.locale(locale),
   draft:(value:Parameters<PilotActions['apply']>[0])=>current.current.actions.draft(value),
   apply:(value:Parameters<PilotActions['apply']>[0])=>current.current.actions.apply(value),save:(title:string)=>current.current.actions.save(title),reload:()=>current.current.actions.reload(),preview:()=>current.current.actions.preview(),urlChanged:(href:string)=>current.current.actions.urlChanged(href),
   range:()=>{const m=current.current.model;const p=m.result?.parameters.period as Record<string,string>|undefined;return `${p?.starts_on??m.start} — ${p?.ends_on??m.end}`;},
   chart:()=>chart.current,
   tableRows:(locale:'ru'|'en')=>tableRows(current.current.model,locale),
   table:(locale:'ru'|'en')=>{const m=current.current.model;return `<table>${tableRows(m,locale)}</table>${m.result?.comparison?`<table>${tableRows(m,locale,true)}</table>`:''}`;},
   trust:(locale:'ru'|'en')=>{const c=reportCopy[locale];const r=current.current.model.result;if(!r)return `<p>${escape(c.pending)}</p>`;const q=r.trust.quality_accounting as Record<string,unknown>;return `<h4>${escape(c.trust)}</h4><p>${escape(c.limitation)}</p><p>${escape(c.locked)}</p><h4>${escape(c.accounting)}</h4><p>${escape(q.product_relationship_eligible_count)} / ${escape(q.denominator)}</p><h4>${escape(c.quarantined)}</h4><p>${escape(q.quarantined_count)}</p><h4>${escape(c.state)}</h4><p>${escape(c[r.coverage.status])} · ${r.coverage.declared_complete_days} / ${r.coverage.period_days}</p><p>${escape(c.policy)}</p><p>${escape(c.methodology)}</p><p>${escape(c.resultId)}: ${escape(r.result_id)}</p><p style="overflow-wrap:anywhere">${escape(c.hash)}: ${escape(r.manifest.content_hash)}</p>`;},
  };
  runtime.current=mountPilot(document,window,bridge,echarts);
  return()=>{runtime.current?.dispose();runtime.current=undefined;};
 },[loaded]);
 useEffect(()=>{runtime.current?.update();},[model]);
 return <iframe ref={frame} title={model.locale==='ru'?'Отчёт':'Report'} srcDoc={documentSource} onLoad={()=>setLoaded(n=>n+1)} style={{position:'fixed',inset:0,width:'100%',height:'100dvh',border:0}} data-pilot-source="b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700"/>;
}
