import {ReportPeriodPicker} from './ReportPeriodPicker';
import {useEffect,useLayoutEffect,useRef,useState,type ReactNode} from 'react';
import {createPortal} from 'react-dom';
import workspaceStyle from './workspace.css?raw';
import navigationStyle from './navigation-dock.css?raw';
import navigationShellStyle from './navigation-shell.css?raw';
import controlFocusStyle from './control-focus.css?raw';
import * as echarts from 'echarts/core';
import {LineChart} from 'echarts/charts';
import {GridComponent,TooltipComponent,LegendComponent,DataZoomComponent,TitleComponent,AriaComponent} from 'echarts/components';
import {SVGRenderer} from 'echarts/renderers';
import {compileLineChart} from '@custometry/chart-compiler';
import {reportCopy} from './copy';
import {checkReferences} from './ReportChart';
import type {Actor,References,Result} from './report-api';
import {noteReportInteraction} from './report-api';
import documentSource from './pilot/document.html?raw';
import {mountPilot} from './pilot/runtime';
// Prototype fixture markup cannot paint before the application bridge replaces it.
const safeDocument=documentSource.replace('</head>','<style id="initial-paint-guard">body{visibility:hidden}</style></head>');
echarts.use([LineChart,GridComponent,TooltipComponent,LegendComponent,DataZoomComponent,TitleComponent,AriaComponent,SVGRenderer]);
export interface PilotModel {
 workspace?:boolean;documentPages?:boolean;workspaceChrome?:{period:string;comparison:string;stores:string;grain:string;unavailable:string};
 locale:'ru'|'en';title:string;source:string;start:string;end:string;store:string;comparison:string;
 result?:Result;refs?:References;actor:Actor;status:string;error?:string;hint:string;
 busy:boolean;preview:boolean;focus:boolean;unapplied:boolean;conflict:boolean;stores:readonly {id:string;label:string}[];
}
export interface PilotActions {
 period?:(start:string,end:string)=>void;
 inspector?:(panel:'set'|'card'|'chart'|'context',trigger?:HTMLElement)=>void;
 apply:(value:{period:{grain:string;value:string};store:string;comparison:'none'|'previous_year_same_dates'})=>void;
 library:()=>void;draft:PilotActions['apply'];save:(title:string)=>void;reload:()=>void;preview:()=>void;title:(title:string)=>void;
 locale:(locale:'ru'|'en')=>void;urlChanged:(href:string)=>void;
}
const escape=(v:unknown)=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
function tableRows(model:PilotModel,locale:'ru'|'en',prior=false){
 const c=reportCopy[locale];const result=model.result;const daily=prior?result?.comparison?.daily:result?.daily;if(!result||!daily)return `<caption>${escape(c.pending)}</caption>`;
 const values=(daily:Result['daily'],prior=false)=>(['net_revenue','receipt_count','average_receipt'] as const).map(k=>`<tr><th scope="row">${escape(prior?c.prior+' · ':'')}${escape(c[k])}</th>${daily.map(r=>`<td data-metric="${k}" data-date="${r.date}" data-value="${escape(r[k])}">${r[k]===null?'—':escape(new Intl.NumberFormat(locale,{maximumFractionDigits:k==='receipt_count'?0:2}).format(Number(r[k])))}</td>`).join('')}</tr>`).join('')+`<tr><th scope="row">${escape(prior?c.prior+' · ':'')}${escape(c.state)}</th>${daily.map(r=>`<td>${escape(c[r.state])}</td>`).join('')}</tr>`;
 return `<caption>${escape(prior?c.prior:c.current)}</caption><thead><tr><th scope="col">${escape(c.date)}</th>${daily.map(r=>`<th scope="col">${r.date}</th>`).join('')}</tr></thead><tbody>${values(daily,prior)}</tbody>`;
}
export function PilotDocument({model,actions,children,inspector,focusContent,headerTitle,headerActions,dataContext,worksetControls,visualizationControls,inspectorOpen=false,filtersOpen=false}:{model:PilotModel;actions:PilotActions;children?:ReactNode;inspector?:ReactNode;focusContent?:ReactNode;headerTitle?:ReactNode;headerActions?:ReactNode;dataContext?:ReactNode;worksetControls?:ReactNode;visualizationControls?:ReactNode;inspectorOpen?:boolean;filtersOpen?:boolean}){
 const [worksetSlot,setWorksetSlot]=useState<HTMLElement|null>(null);
 const [visualizationSlot,setVisualizationSlot]=useState<HTMLElement|null>(null);
 const [contextSlot,setContextSlot]=useState<HTMLElement|null>(null);
 const [periodAnchor,setPeriodAnchor]=useState<HTMLElement|null>(null);
 const [slot,setSlot]=useState<HTMLElement|null>(null);const [inspectorSlot,setInspectorSlot]=useState<HTMLElement|null>(null);
 const [titleSlot,setTitleSlot]=useState<HTMLElement|null>(null);const [actionsSlot,setActionsSlot]=useState<HTMLElement|null>(null);
 const frame=useRef<HTMLIFrameElement>(null);const current=useRef({model,actions});current.current={model,actions};
 const runtime=useRef<ReturnType<typeof mountPilot>|undefined>(undefined);const chart=useRef<ReturnType<typeof compileLineChart>['option']|undefined>(undefined);
 const [loaded,setLoaded]=useState(0);
 useEffect(()=>{let cancelled=false;chart.current=undefined;if(model.workspace)return;if(!model.result||!model.refs){runtime.current?.update();return;}
  const {result,refs,actor}=model;
  void checkReferences(refs).then(()=>{
   const metric=result.metrics[0];if(!refs.company_pack.payload.metric_versions.some(m=>m.version_id===metric.version_id&&m.content_hash===metric.content_hash))throw Error('METRIC_REFERENCE_MISMATCH');
   const compiled=compileLineChart(refs.chart_spec.payload,{workspaceId:actor.workspace_id,ownerPrincipalId:actor.principal_id,policyHash:result.policy_hash,artifactId:String(result.manifest.artifact_id),artifactHash:String(result.manifest.content_hash),parameters:result.parameters,metricVersionId:String(metric.version_id),metricHash:String(metric.content_hash),daily:result.daily,comparison:result.comparison?.daily??null},{locale:model.locale,primary:'#66b9d3',comparison:'#a8b3ba',text:'#999a9e',grid:'#292a2e'});
   if(cancelled)return;chart.current=compiled.option;runtime.current?.update();frame.current?.setAttribute('data-chart-ready','true');
  }).catch(()=>{if(!cancelled){chart.current=undefined;frame.current?.setAttribute('data-chart-ready','false');}});
  return()=>{cancelled=true;};
 },[model.result,model.refs,model.actor,model.locale,model.workspace]);
 useLayoutEffect(()=>{
  const document=frame.current?.contentDocument;const window=frame.current?.contentWindow;if(!document||!window||!loaded)return;
  const bridge={inspector:(panel:'set'|'card'|'chart'|'context',trigger?:HTMLElement)=>current.current.actions.inspector?.(panel,trigger),model:()=>current.current.model,url:()=>globalThis.location.href,
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
  const interaction=(event:Event)=>{if(event.isTrusted)noteReportInteraction();};
  document.addEventListener('pointerdown',interaction,true);document.addEventListener('keydown',interaction,true);
  const navigationSheet=document.createElement("style");navigationSheet.textContent=navigationShellStyle+navigationStyle+controlFocusStyle;document.head.append(navigationSheet);
  const periodClick=(event:Event)=>{const target=(event.target as Element).closest<HTMLElement>('#period-menu-open');if(!target)return;event.preventDefault();event.stopImmediatePropagation();if(target.hasAttribute('disabled')||current.current.model.preview||current.current.model.busy)return;setPeriodAnchor(old=>old?null:target);};
  document.addEventListener('click',periodClick,true);
  runtime.current=mountPilot(document,window,bridge,echarts);
  const reportWorkspace=document.getElementById("workspace")!;const reportHeader=document.querySelector<HTMLElement>(".page-header")!;reportHeader.classList.add("mw-global-header");reportWorkspace.prepend(reportHeader);
  if(current.current.model.workspace){document.body.dataset.workspaceV2="true";const style=document.createElement("style");style.textContent=workspaceStyle;document.head.append(style);const slot=document.createElement("div");slot.id="workspace-v2";document.getElementById("page-overview")!.append(slot);setSlot(slot);const workspace=document.getElementById("workspace")!;const dock=document.createElement("div");dock.className="mw-inspector-slot";workspace.append(dock);setInspectorSlot(dock);const title=document.createElement("div");title.className="mw-title-slot";reportHeader.querySelector(".title-row h1")!.after(title);setTitleSlot(title);const actions=document.createElement("div");actions.className="mw-header-tools";reportHeader.querySelector(".header-actions")!.prepend(actions);setActionsSlot(actions);
   const context=document.createElement('div');context.className='mw-data-context';
   const navigation=document.querySelector('.report-navigation-row')!;
   const commandRow=document.createElement('div');commandRow.className='mw-command-row';navigation.after(commandRow);
   const group=(ru:string,en:string)=>{const block=document.createElement('section');block.className='mw-command-block';const label=document.createElement('small');label.className='mw-command-label';label.id='mw-command-label-'+commandRow.children.length;block.setAttribute('aria-labelledby',label.id);label.dataset.ru=ru;label.dataset.en=en;label.textContent=current.current.model.locale==='ru'?ru:en;block.append(label);commandRow.append(block);return block;};
   group('Данные','Data').append(context);
   const sets=document.createElement('div');sets.className='mw mw-command-controls';group('Набор и метрики','Set & metrics').append(sets);setWorksetSlot(sets);
   const visualization=document.createElement('div');visualization.className='mw mw-command-controls';group('Вид результата','Result view').append(visualization);setVisualizationSlot(visualization);
   context.append(document.getElementById('period-menu-open')!);
   const controls=document.createElement('div');controls.className='mw-data-controls mw';context.append(controls);setContextSlot(controls);
   const filters=document.getElementById('stores-menu-open')!;context.append(filters);
   filters.querySelector('use')!.setAttribute('href','#i-filter');
   reportHeader.querySelector('.header-actions')!.insertBefore(document.getElementById('view-menu-open')!,document.getElementById('context-open'));
  }
  if(current.current.model.documentPages){const legacyPage=document.getElementById('page-overview');legacyPage?.removeAttribute('role');legacyPage?.removeAttribute('aria-labelledby');document.querySelector<HTMLElement>('.report-navigation-row')?.setAttribute('hidden','');}
  if(!current.current.model.workspace)document.getElementById('initial-paint-guard')?.remove();
  return()=>{document.removeEventListener('click',periodClick,true);document.removeEventListener('pointerdown',interaction,true);document.removeEventListener('keydown',interaction,true);runtime.current?.dispose();runtime.current=undefined;};
 },[loaded]);
 useLayoutEffect(()=>{const doc=frame.current?.contentDocument;const workspace=doc?.getElementById('workspace');if(!workspace||!model.workspace)return;workspace.dataset.reportInspector=inspectorOpen?'open':'closed';const filters=doc!.getElementById('stores-menu-open');filters?.setAttribute('aria-expanded',String(filtersOpen));filters?.setAttribute('aria-controls','workspace-inspector');const toggle=doc!.getElementById('context-open');toggle?.setAttribute('aria-expanded',String(inspectorOpen));toggle?.setAttribute('aria-controls','workspace-inspector');if(current.current.model.workspace&&toggle){const en=inspectorOpen?'Close report inspector':'Open report inspector';const ru=inspectorOpen?'Закрыть инспектор отчёта':'Открыть инспектор отчёта';toggle.setAttribute('data-en-label',en);toggle.setAttribute('data-ru-label',ru);toggle.setAttribute('aria-label',model.locale==='ru'?ru:en);toggle.title=model.locale==='ru'?ru:en;}const media=frame.current!.contentWindow!.matchMedia('(max-width:1100px)');const sync=()=>{const content=doc!.getElementById('report-scroll');if(content)content.inert=inspectorOpen&&media.matches;const commands=doc!.querySelector<HTMLElement>('.mw-command-row');if(commands)commands.inert=inspectorOpen&&media.matches;};sync();media.addEventListener('change',sync);return()=>media.removeEventListener('change',sync);},[loaded,inspectorOpen,filtersOpen,inspectorSlot,model.locale]);
 useLayoutEffect(()=>{const start=performance.now();runtime.current?.update();if(model.workspace){const doc=frame.current?.contentDocument;const filters=doc?.getElementById('stores-menu-open');const summary=doc?.getElementById('stores-summary');if(filters&&summary){summary.textContent=model.locale==='ru'?'Фильтры':'Filters';filters.setAttribute('aria-label',(model.locale==='ru'?'Фильтры · Магазин: ':'Filters · Store: ')+model.workspaceChrome?.stores);filters.title=filters.getAttribute('aria-label')!;}}performance.clearMeasures('custometry.report.chrome');performance.measure('custometry.report.chrome',{start,end:performance.now()});},[model]);
 useLayoutEffect(()=>{const legacy=titleSlot?.previousElementSibling as HTMLElement|undefined;if(legacy)legacy.hidden=Boolean(headerTitle);},[titleSlot,headerTitle]);
 // Reveal the workspace only after its portal content and styles have mounted.
 useLayoutEffect(()=>{if(slot&&inspectorSlot&&titleSlot&&actionsSlot)slot.ownerDocument.getElementById('initial-paint-guard')?.remove();},[slot,inspectorSlot,titleSlot,actionsSlot]);
 const focusOpen=Boolean(focusContent);
 useLayoutEffect(()=>{const workspace=inspectorSlot?.parentElement;if(!workspace||!focusOpen)return;const siblings=[...workspace.children].filter((element):element is HTMLElement=>element instanceof workspace.ownerDocument.defaultView!.HTMLElement&&!element.classList.contains('mw-focus'));const previous=siblings.map(element=>element.inert);siblings.forEach(element=>{element.inert=true;});return()=>siblings.forEach((element,index)=>{element.inert=previous[index];});},[inspectorSlot,focusOpen]);
 return <>{worksetSlot&&worksetControls?createPortal(worksetControls,worksetSlot):null}{visualizationSlot&&visualizationControls?createPortal(visualizationControls,visualizationSlot):null}{contextSlot&&dataContext?createPortal(dataContext,contextSlot):null}{periodAnchor&&createPortal(<ReportPeriodPicker anchor={periodAnchor} start={model.start} end={model.end} locale={model.locale} onClose={()=>setPeriodAnchor(null)} onSelect={(start,end)=>{if(current.current.model.workspace)current.current.actions.period?.(start,end);else runtime.current?.setRange(start,end);}}/>,periodAnchor.ownerDocument.body)}<iframe ref={frame} title={model.locale==='ru'?'Отчёт':'Report'} srcDoc={safeDocument} onLoad={()=>setLoaded(n=>n+1)} style={{position:'fixed',inset:0,width:'100%',height:'100dvh',border:0}} data-pilot-source="b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700"/>{titleSlot&&headerTitle?createPortal(headerTitle,titleSlot):null}{actionsSlot&&headerActions?createPortal(headerActions,actionsSlot):null}{slot&&children?createPortal(children,slot):null}{inspectorSlot&&inspector?createPortal(inspector,inspectorSlot):null}{inspectorSlot?.parentElement&&focusContent?createPortal(focusContent,inspectorSlot.parentElement):null}</>;
}
