import {useEffect,useRef,useState} from 'react';
import {useQuery} from '@tanstack/react-query';
import type {composerReports as C} from '@custometry/contracts';
import type {FilterInput} from './receipt-filter-tree';
import {reportApi,csrf} from './report-api';
import {composerApi} from './composer-api';
import {workspaceContext,workspaceCalendar} from './workspace-api';
import {metricNames} from './workspace-copy';
import {withBlockComparison,initialBlockComparison,withBlockCalendarBasis,initialBlockCalendarBasis} from './composer-temporal';
import {TemporalSettingsEditor} from './TemporalSettingsEditor';
import {ReceiptFilterEditor} from './ReceiptFilterEditor';
import {StoreScopePicker} from './StoreScopePicker';
import {composerCopy} from './composer-copy';
import {isLocked} from './composer-structure';
import {nextPlacement,removeBlock,type Definition} from './composer-state';

export function ComposerBuilder({definition,block,locale,close,commit,disabled=false,destination,onValidating,embedded=false,initialKind="chart"}:{embedded?:boolean;initialKind?:"chart"|"table"|"metric";definition:Definition;block?:C.ComposerBlock;locale:'ru'|'en';close:()=>void;onValidating:(token:string,active:boolean)=>void;commit:(next:Definition,id:string)=>void;disabled?:boolean;destination?:string}){
 const c=composerCopy[locale];const source=definition.definitions.find(d=>d.definition_id===block?.source?.definition_id);
 const [step,setStep]=useState(0);const [dataset,setDataset]=useState(source?.query.semantic_dataset_version_id??'');
 const [metric,setMetric]=useState(block?.source?.metric_ref.metric_id??'net_revenue');const [grain,setGrain]=useState<C.WorkspaceRunRequest['grain']>(source?.query.grain??'day');
 const [start,setStart]=useState(source?.query.common.starts_on??'');const [end,setEnd]=useState(source?.query.common.ends_on??'');
 const [stores,setStores]=useState<readonly string[]|null>(source?.query.local_store_ids??null);
 const initialComparison=initialBlockComparison(definition,block);
 const [calendarBasis,setCalendarBasis]=useState<'calendar'|'fiscal'|null>(initialBlockCalendarBasis(definition,block));
 const [basisChanged,setBasisChanged]=useState(false);
 const [comparisonChanged,setComparisonChanged]=useState(false);
 const [alignment,setAlignment]=useState<'none'|'previous_year_same_dates'|null>(initialComparison.alignment);
 const [timeComparison,setTimeComparison]=useState<C.TemporalSettingsV2|null>(initialComparison.settings);
 const [receiptFilter,setReceiptFilter]=useState<FilterInput|null>(source?.query.receipt_filter??null);
 const [title,setTitle]=useState(block?.presentation.title??'');const [kind,setKind]=useState<'chart'|'table'|'metric'>(block?.source?block.block_type as 'chart'|'table'|'metric':initialKind);
 const [section,setSection]=useState(block?.section_id??destination??definition.sections.find(s=>!isLocked(definition,{kind:'section',id:s.section_id}))?.section_id??'');const [error,setError]=useState('');
 const heading=useRef<HTMLHeadingElement>(null);useEffect(()=>{if(!embedded)heading.current?.focus();},[step,embedded]);
 const products=useQuery({queryKey:['composer-products'],queryFn:reportApi.context});
 const context=useQuery({queryKey:['composer-context',dataset],queryFn:()=>workspaceContext(dataset),enabled:Boolean(dataset)});
 const calendar=useQuery({queryKey:['composer-calendar'],queryFn:()=>workspaceCalendar.get(),enabled:!source});
 const calendarRef=source?.query.calendar_ref??(calendar.data?{version_id:calendar.data.calendar.version_id,content_hash:calendar.data.calendar.content_hash}:undefined);
 const readyDataset=dataset||(products.data?.datasets.length===1?products.data.datasets[0].id:'');
 useEffect(()=>{if(!dataset&&readyDataset)setDataset(readyDataset);},[dataset,readyDataset]);
 useEffect(()=>{if(products.data&&!source){setStart(String(products.data.default_period.starts_on));setEnd(String(products.data.default_period.ends_on));}},[products.data,source]);
 const [filterPending,setFilterPending]=useState(false);
 const [validating,setValidating]=useState(false);const controller=useRef<AbortController|null>(null),current=useRef(definition);current.current=definition;
 const [validationToken]=useState(()=>crypto.randomUUID());
 useEffect(()=>()=>{controller.current?.abort();onValidating(validationToken,false);},[onValidating,validationToken]);
 const sourceReady=Boolean(context.data?.metrics.some(m=>m.metric_id===metric));
 const stepReady=embedded?Boolean(dataset&&sourceReady&&calendarRef):step===0?Boolean(dataset&&products.data?.datasets.some(p=>p.id===dataset)):step===1?sourceReady:sourceReady&&Boolean(calendarRef);
 const submit=async()=>{
  const selected=context.data?.metrics.find(m=>m.metric_id===metric);
  if(disabled||filterPending||(block&&isLocked(definition,{kind:'block',id:block.block_id}))||!selected||!calendarRef||!section||isLocked(definition,{kind:'section',id:section})||!start||!end||end<start||Date.parse(end)-Date.parse(start)>=366*86400000){setError(c.invalid);return;}
  const sourceId=crypto.randomUUID(),id=block?.block_id??crypto.randomUUID();
  const base=block?removeBlock(definition,block.block_id,true):definition;
  const ref={metric_id:selected.metric_id,version_id:selected.version_id,content_hash:selected.content_hash};
  const query:C.WorkspaceRunRequest={semantic_dataset_version_id:dataset,common:{starts_on:start,ends_on:end,store_ids:source?.query.common.store_ids??null},local_store_ids:stores,
   ...(receiptFilter?{receipt_filter:receiptFilter}:{}),grain,calendar_ref:calendarRef,calendar_basis:basisChanged?'calendar':source?.query.calendar_basis??'calendar',alignment:comparisonChanged?'none':source?.query.alignment??'none',...(!comparisonChanged&&source?.query.time_comparison?{time_comparison:source.query.time_comparison}:{}),metric_refs:[ref,...(source?.query.semantic_dataset_version_id===dataset?source.query.metric_refs.filter(m=>m.metric_id!==ref.metric_id&&m.metric_id!==block?.source?.metric_ref.metric_id):[])]};
  const next:C.ComposerBlock={...block,block_id:id,block_type:embedded&&block?block.block_type:kind,section_id:section,order:block?.section_id===section?block.order:Math.max(-1,...base.blocks.filter(b=>b.section_id===section).map(b=>b.order))+1,
   source:{definition_id:sourceId,metric_ref:ref},presentation:{...block?.presentation,title:embedded&&block?block.presentation.title:title.trim()||metricNames[locale][metric]},placement:block?.section_id===section?block.placement:nextPlacement(base,section,kind==='metric'?6:12,kind==='metric'?3:8)};
  const updated:Definition={...base,blocks:[...base.blocks,next],definitions:[...base.definitions,{definition_id:sourceId,provider:'metric-workspace/v2',query}]};
  const comparisonUpdate=comparisonChanged?withBlockComparison(updated,id,timeComparison,alignment):updated;
  const candidate=basisChanged?withBlockCalendarBasis(comparisonUpdate,id,calendarBasis):comparisonUpdate;
  controller.current?.abort();const call=new AbortController();controller.current=call;setValidating(true);onValidating(validationToken,true);
  try{await composerApi.validate(candidate,csrf(),call.signal);if(!call.signal.aborted&&current.current===definition)commit(candidate,id);}
  catch{if(!call.signal.aborted)setError(c.invalid);}finally{if(controller.current===call){setValidating(false);onValidating(validationToken,false);}}
 };
 const Container=embedded?'div':'aside';
 return <Container id={embedded?undefined:"workspace-inspector"} className={embedded?"composer-builder composer-builder-embedded":"mw-inspector composer-builder"} onKeyDown={e=>{if(e.key==='Escape'){e.stopPropagation();close();}}}>
 {!embedded&&<div className="composer-toolbar"><h2 ref={heading} tabIndex={-1}>{c.settings} · {step+1}/3</h2><button onClick={close} aria-label={c.close}>×</button></div>}
 <form className="composer-builder-form" onSubmit={e=>{e.preventDefault();if(disabled||validating||filterPending||!stepReady)return;setError('');if(!embedded&&step<2)setStep(step+1);else void submit();}}>
 {(embedded||step===0)&&<fieldset disabled={disabled||validating}><legend>{c.subject}</legend><p>{c.retail}</p><label>{c.product}<select aria-label={c.product} required value={dataset} onChange={e=>{setDataset(e.target.value);setStores(null);setReceiptFilter(null);}}><option value="">{c.choose}</option>{products.data?.datasets.map(p=><option key={p.id} value={p.id}>{p.label}</option>)}</select></label>{products.isError?<p role="alert">{c.error}<button type="button" onClick={()=>void products.refetch()}>{c.retry}</button></p>:null}</fieldset>}{(embedded||step===1)&&<fieldset disabled={disabled||validating}><legend>{locale==='ru'?'Показатель и группировка':'Measure and grouping'}</legend><label>{c.metric}<select aria-label={c.metric} value={metric} onChange={e=>setMetric(e.target.value as typeof metric)}>{context.data?.metrics.map(m=><option key={m.metric_id} value={m.metric_id}>{metricNames[locale][m.metric_id]}</option>)}</select></label><label>{c.grain}<select aria-label={c.grain} value={grain} onChange={e=>setGrain(e.target.value as typeof grain)}>{(['day','week','month','quarter','half_year','year'] as const).map((g,i)=><option key={g} value={g}>{locale==='ru'?['День','Неделя','Месяц','Квартал','Полугодие','Год'][i]:['Day','Week','Month','Quarter','Half year','Year'][i]}</option>)}</select></label>{context.isError&&<p role="alert">{c.error}<button type="button" onClick={()=>void context.refetch()}>{c.retry}</button></p>}</fieldset>}{(embedded||step===2)&&<fieldset disabled={disabled||validating}><legend>{c.period}</legend><p>{c.dimensions}</p><label>{c.from}<input type="date" required value={start} onChange={e=>setStart(e.target.value)}/></label><label>{c.to}<input type="date" required min={start} value={end} onChange={e=>setEnd(e.target.value)}/></label><label>{locale==='ru'?'Календарная основа':'Calendar basis'}<select aria-label={locale==='ru'?'Календарная основа':'Calendar basis'} value={calendarBasis??'inherit'} onChange={e=>{setBasisChanged(true);setCalendarBasis(e.target.value==='inherit'?null:e.target.value as 'calendar'|'fiscal');}}><option value="inherit">{locale==='ru'?'Наследовать':'Inherit'}</option><option value="calendar">{locale==='ru'?'Календарная':'Calendar'}</option><option value="fiscal">{locale==='ru'?'Финансовая':'Fiscal'}</option></select></label><TemporalSettingsEditor settings={timeComparison} alignment={alignment} change={(settings,legacy)=>{setComparisonChanged(true);setTimeComparison(settings);setAlignment(legacy);}} locale={locale} label={locale==='ru'?'Сравнение периодов':'Temporal comparison'} inherit disabled={disabled||validating}/><StoreScopePicker disabled={disabled||validating} label={c.store} value={stores} onChange={setStores} stores={context.data?.stores??[]} locale={locale}/><ReceiptFilterEditor key={dataset} dataset={dataset} onPending={setFilterPending} disabled={disabled||validating} value={receiptFilter} onChange={setReceiptFilter} locale={locale}/>{!embedded&&<><label>{c.kind}<select aria-label={c.kind} value={kind} onChange={e=>setKind(e.target.value as typeof kind)}><option value="chart">{c.chart}</option><option value="table">{c.table}</option><option value="metric">{locale==='ru'?'Метрика':'Metric'}</option></select></label><label>{c.name}<input maxLength={200} value={title} onChange={e=>setTitle(e.target.value)}/></label><label>{c.destination}<select aria-label={c.destination} value={section} onChange={e=>setSection(e.target.value)}>{definition.sections.map(s=><option key={s.section_id} value={s.section_id} disabled={isLocked(definition,{kind:'section',id:s.section_id})}>{definition.pages.find(p=>p.page_id===s.page_id)?.title} · {s.title}</option>)}</select></label></>}</fieldset>}
 <p role="alert">{error}</p>{!stepReady&&<p role="status">{c.loading}</p>}{step===2&&calendar.isError&&<p role="alert">{c.error}<button type="button" onClick={()=>void calendar.refetch()}>{c.retry}</button></p>}<div className="composer-toolbar composer-form-actions">{!embedded&&step>0&&<button type="button" onClick={()=>setStep(step-1)}>{c.back}</button>}<button className="composer-primary" disabled={disabled||validating||filterPending||!stepReady} type="submit">{!embedded&&step<2?c.next:block?c.update:c.done}</button></div>
 </form></Container>;
}
