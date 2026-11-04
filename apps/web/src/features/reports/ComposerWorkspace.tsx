import {metricNumber,fullMetricNumber} from './metric-number';
import {useCallback,useEffect,useRef,useState} from 'react';
import {useQuery} from '@tanstack/react-query';
import {useLocation,useNavigate} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import {composerReports as C} from '@custometry/contracts';
import {PilotDocument} from './PilotDocument';
import {ComposerPending as PendingWorkspace} from './ComposerPending';
import {WorkspacePlot,WorkspaceTable} from './WorkspaceProjection';
import {useAutomaticRefresh} from './useAutomaticRefresh';
import {CardYearChange} from './CardYearChange';
import {workspaceUnit,workspaceReason} from './workspace-copy';
import {BlockCalculationAction} from './BlockCalculationAction';
import {ComposerBlockTitle} from './ComposerBlockTitle';
import {ComposerDeleteDialog} from './ComposerDeleteDialog';
import {ComposerCanvas} from './ComposerCanvas';
import {ComposerInspector,ControlBody} from './ComposerInspector';
import {canvasDefinition,addContent} from './composer-canvas';
import {Plus,LineChart,Table2,Type,Filter,Undo2,Redo2,Save,Eye,ChevronDown,Hash,LayoutGrid} from 'lucide-react';
import {arrangeBlocks,type LayoutChange} from './composer-layout';
import {pairKey,type PairResult} from './ComposerPair';
import {composerApi as api} from './composer-api';
import {record,startHistory,travel,isLocked,isHidden,orderedSections,sectionDepth,type History} from './composer-structure';
import {describeFilter} from './ReceiptFilterEditor';
import {ComposerBuilder} from './ComposerBuilder';
import {reportApi,csrf,accessStore} from './report-api';
import {composerCopy} from './composer-copy';
import {duplicate,removeBlock,queryKey,projectionDefinition,type Definition} from './composer-state';
import styles from './composer.css?raw';
type DraftMemory={definition:Definition;version?:C.ComposerReportResponse;pending:C.ComposerSaveRequest|null;conflict:boolean;history:History|null;comparison?:PairResult};
const drafts=new Map<string,DraftMemory>();
accessStore.subscribe(()=>{if(!accessStore.reconciling())drafts.clear();});
type Ready={key:string;result:C.WorkspaceResultV2;binding:C.CardResultBinding};

function Block({definition,block,locale,saved,selected,select,edit,copy,remove,ready,onReady,onLoaded,onRunning,preview,busy,canApply,layout}:{layout:(change:LayoutChange)=>void;definition:Definition;block:C.ComposerBlock;locale:'ru'|'en';saved?:C.ComposerReportResponse;selected:boolean;select:()=>void;edit:(trigger:HTMLElement)=>void;copy:()=>void;remove:()=>void;ready?:Ready;onReady:(value:Ready)=>void;onLoaded:(id:string,value:Ready)=>void;onRunning:(id:string,running:boolean)=>void;preview:boolean;busy:boolean;canApply:boolean}){
 const c=composerCopy[locale],key=queryKey(definition,block),current=useRef(key);current.current=key;
 const [running,setRunning]=useState(false),[error,setError]=useState(false);const controller=useRef<AbortController|null>(null);
 const savedBlock=saved?.definition.blocks.find(b=>b.block_id===block.block_id)??saved?.definition.blocks.find(b=>queryKey(saved.definition,b)===key&&saved.results.some(r=>r.block_id===b.block_id));
 const reference=saved?.results.find(r=>r.block_id===savedBlock?.block_id);
 const exact=Boolean(savedBlock&&reference&&queryKey(saved!.definition,savedBlock)===key);
 const loaded=useQuery({queryKey:['composer-result',definition.document_id,saved?.snapshot_id,block.block_id,key],enabled:exact&&ready?.key!==key,
  queryFn:({signal})=>api.result(definition.document_id,saved!.snapshot_id,savedBlock!.block_id,signal),refetchOnWindowFocus:false,refetchOnReconnect:false});
 useEffect(()=>{if(exact&&loaded.data)onLoaded(block.block_id,{key,result:loaded.data.result,binding:{...loaded.data.binding,card_id:block.block_id}});},[exact,loaded.data,key,block.block_id,onLoaded]);
 useEffect(()=>{setError(false);setRunning(false);controller.current?.abort();return()=>controller.current?.abort();},[key]);
 const value=ready?.key===key?ready:exact?loaded.data:undefined;
 const result=value?.result;
 useEffect(()=>{onRunning(block.block_id,running);return()=>onRunning(block.block_id,false);},[running,block.block_id,onRunning]);
 const apply=async()=>{controller.current?.abort();const call=new AbortController();controller.current=call;setRunning(true);setError(false);
  try{const response=await api.apply({contract_version:'analytical-authoring/v1',definition,block_id:block.block_id},csrf(),call.signal);if(current.current===key&&!call.signal.aborted)onReady({key,result:response.result,binding:response.binding});}
  catch{if(!call.signal.aborted&&current.current===key)setError(true);}finally{if(controller.current===call)setRunning(false);}
 };
 useAutomaticRefresh(key,!preview&&canApply&&!result&&!error&&!loaded.isError&&!exact,busy||running||loaded.isFetching,()=>void apply());
 const calculation={ready:Boolean(result),failed:error||loaded.isError,loading:running||loaded.isFetching,preview,disabled:busy||(!canApply&&!(loaded.isError&&!result)),locale,run:()=>void (loaded.isError&&!result?loaded.refetch():apply())};
 const receiptFilter=definition.definitions.find(d=>d.definition_id===block.source!.definition_id)?.query.receipt_filter;
 const projection=projectionDefinition(definition,block,result?.effective_context);const binding=value?.binding;
 const refs=block.presentation.chart_type==='combo'&&block.block_type==='chart'?(definition.definitions.find(d=>d.definition_id===block.source?.definition_id)?.query.metric_refs??[]):[block.source!.metric_ref];
 const multiSeries=refs.length>1;const bindings:C.CardResultBinding[]=binding?(multiSeries?refs.map(ref=>({...binding,card_id:block.block_id+':'+ref.metric_id,metric_ref:ref,bucket_projection:ref.metric_id,unit:ref.metric_id==='receipt_count'?'receipt':ref.metric_id==='average_receipt'?'EUR/receipt':'EUR'})):[binding]):[];
 const props={presentation:block.presentation,multiSeries,totals:refs.map(ref=>result?.totals[ref.metric_id]??null),definition:projection,bindings,results:new Map(result?[[result.result_id,result]]:[]),comparison:null,locale};
 const total=result?.totals[block.source!.metric_ref.metric_id];
 const formatted=metricNumber(total,locale);
 if(block.block_type==='metric')return <div className="kpi-card composer-metric-body"><span className="mw-card-select"><ComposerBlockTitle presentation={block.presentation}/></span><strong className="kpi-value" title={fullMetricNumber(total,locale)}>{formatted}</strong>{Boolean(result?.temporal||result?.temporal_v2)&&<CardYearChange binding={binding} result={result} locale={locale} enabled applied={Boolean(result)} loading={running||loaded.isFetching}/>}{binding&&binding.readiness!=='ready'&&<small>{workspaceReason(locale,binding.readiness)}</small>}{(running||loaded.isFetching)&&<span role="status">{c.loading}</span>}{(error||loaded.isError)&&<p role="alert">{c.error}</p>}<BlockCalculationAction location="header" {...calculation}/></div>;
 return <div className="composer-data-block">
 <header className="composer-toolbar">{((block.presentation.show_title!==false&&block.presentation.title.trim())||block.presentation.description?.trim())&&<h2><ComposerBlockTitle presentation={block.presentation}/></h2>}<BlockCalculationAction location="header" {...calculation}/></header>
 {receiptFilter&&<p>{locale==='ru'?'Фильтр чеков':'Receipt filter'}: {describeFilter(receiptFilter.expression,[],locale)}</p>}
 {(running||loaded.isFetching||!result&&!error&&!loaded.isError)&&<p role="status">{running||loaded.isFetching?c.loading:c.pending}</p>}
 {(error||loaded.isError)&&<p role="alert">{c.error}</p>}
 {result?.trust.reason_codes.includes('COVERAGE_INTERSECTING_UTC_SOURCE_DAYS')&&<details className="composer-calculation-note"><summary>{locale==='ru'?'Особенности расчёта':'Calculation notes'}</summary><p>{result.effective_context.timezone}. {locale==='ru'?'Полнота локального дня проверяется по всем пересекающимся UTC-дням источника. Фильтр даты чека использует UTC.':'Local-day coverage requires every intersecting UTC source day. Receipt date filters use UTC.'}</p></details>}
 {result?.receipt_selection&&<aside className="receipt-selection-evidence" aria-label={locale==='ru'?'Полнота отбора чеков':'Receipt selection coverage'}><p>{locale==='ru'?`Во всём доступном наборе подтверждено чеков: ${result.receipt_selection.matched_count}. Неизвестно: ${result.receipt_selection.unknown_count}. Показатели за выбранный период рассчитаны только по подтверждённым чекам.`:`Across the authorized dataset, confirmed receipts: ${result.receipt_selection.matched_count}. Unknown: ${result.receipt_selection.unknown_count}. Values for the selected period use confirmed receipts only.`}</p>{result.receipt_selection.limitation_codes.length>0&&<p>{locale==='ru'?'История неполная. Соответствие условиям не установлено для неизвестной части набора.':'History is incomplete. Membership is undetermined for the unknown part of the dataset.'}</p>}</aside>}
 {result&&block.block_type==='chart'&&<div className="composer-chart-total"><strong>{formatted}</strong><small>{workspaceUnit(locale,binding?.unit??'')}</small></div>}
 {result&&(block.block_type==='table'?<WorkspaceTable {...props} compact/>:<WorkspacePlot {...props} compact reveal chartType={block.presentation.chart_type??'line'}/>)}
 </div>;
}

export function ComposerWorkspace({workspace,trusted,preview=false}:{workspace:string;trusted:boolean;preview?:boolean}){
 const {i18n}=useTranslation(),locale=i18n.resolvedLanguage==='ru'?'ru':'en',c=composerCopy[locale];
 const location=useLocation(),navigate=useNavigate(),id=location.pathname.split('/')[4],snapshot=preview?location.pathname.split('/')[6]:undefined;
 const memoryKey=workspace+location.pathname;const memory=drafts.get(memoryKey);
 const isNew=id==='new';const [newId]=useState(()=>memory?.definition.document_id??crypto.randomUUID());const [dataset,setDataset]=useState('');
 const products=useQuery({queryKey:['composer-products',workspace],queryFn:reportApi.context,enabled:trusted&&isNew});
 const chosen=dataset||(products.data?.datasets.length===1?products.data.datasets[0].id:'');
 const prepared=useQuery({queryKey:['composer-new',workspace,newId,chosen],enabled:trusted&&isNew&&Boolean(chosen&&products.data),
  queryFn:()=>api.prepare({report_id:newId,semantic_dataset_version_id:chosen,template:'blank',locale,common_context:{starts_on:String(products.data!.default_period.starts_on),ends_on:String(products.data!.default_period.ends_on),store_ids:null}},csrf()),refetchOnWindowFocus:false,refetchOnReconnect:false});
 const editor=useQuery({queryKey:['composer-editor',workspace,id,snapshot],enabled:trusted&&!isNew,
  queryFn:({signal})=>snapshot?api.snapshot(id,snapshot,signal):api.get(id,signal),refetchOnMount:new URLSearchParams(location.search).get('view')==='composer',refetchOnWindowFocus:false,refetchOnReconnect:false});
 const initial=prepared.data?.definition??editor.data?.report.definition;
 const actor=prepared.data?.actor??editor.data?.actor;
 const capabilities=prepared.data?.capabilities??editor.data?.capabilities;
 const readOnly=preview||capabilities?.definition_edit!==true;
 const [draft,setDraft]=useState<Definition|null>(memory?.definition??null);const d=draft??(initial?canvasDefinition(initial):undefined);
 const [history,setHistory]=useState<History|null>(memory?.history??null);
 const [saved,setSaved]=useState<C.ComposerReportResponse|undefined>(memory?.version);const version=saved??editor.data?.report;
 const [dirty,setDirty]=useState(isNew||Boolean(memory)),[saving,setSaving]=useState(false),[notice,setNotice]=useState(memory?.pending?c.saveError:''),[conflict,setConflict]=useState(memory?.conflict??false);
 const [pendingDelete,setPendingDelete]=useState<string|null>(null);
 const [inspectorTab,setInspectorTab]=useState<'data'|'visual'>('data');
 const [selected,setSelected]=useState<string|null>(null),[builder,setBuilder]=useState<string|null>(null);const [palette,setPalette]=useState(false);const [settingsOpen,setSettingsOpen]=useState(()=>window.innerWidth>1100);
 useEffect(()=>{setBuilder(null);},[location.search]);
 const [ready,setReady]=useState<Record<string,Ready>>({});const trigger=useRef<HTMLElement|null>(null);const title=useRef<HTMLInputElement|null>(null);
 const [comparison,setComparison]=useState<PairResult|undefined>(memory?.comparison);
 const [comparing,setComparing]=useState(false);
 const pending=useRef<C.ComposerSaveRequest|null>(memory?.pending??null);
 const locked=saving||pending.current!==null;
 const mutationBlocked=useRef(false);mutationBlocked.current=locked||readOnly;
 const validations=useRef(new Set<string>());const [validating,setValidating]=useState(false);
 const onValidating=useCallback((token:string,active:boolean)=>{if(active)validations.current.add(token);else validations.current.delete(token);setValidating(validations.current.size>0);},[]);
 const [runningBlocks,setRunningBlocks]=useState<Set<string>>(()=>new Set());
 const onRunning=useCallback((blockId:string,running:boolean)=>setRunningBlocks(old=>{if(old.has(blockId)===running)return old;const next=new Set(old);if(running)next.add(blockId);else next.delete(blockId);return next;}),[]);
 const latestDraft=useRef({d,version,dirty,conflict,history,comparison});latestDraft.current={d,version,dirty,conflict,history,comparison};
 useEffect(()=>{const unsubscribe=accessStore.subscribe(()=>{const current=latestDraft.current;if(accessStore.reconciling()&&current.d&&current.dirty)drafts.set(memoryKey,{definition:current.d,version:current.version,pending:pending.current,conflict:current.conflict,history:current.history,comparison:current.comparison});else drafts.delete(memoryKey);});return()=>{unsubscribe();if(!accessStore.reconciling())drafts.delete(memoryKey);};},[memoryKey]);
 const close=()=>{setBuilder(null);requestAnimationFrame(()=>trigger.current?.focus());};
 const remember=useCallback((id:string,value:Ready)=>setReady(old=>old[id]?.key===value.key&&old[id].result.result_id===value.result.result_id?old:{...old,[id]:value}),[]);
 const install=(value:Definition)=>{if(builder&&builder!=='new'&&!value.blocks.some(b=>b.block_id===builder)){setBuilder(null);title.current?.focus();}const search=new URLSearchParams(location.search);const page=search.get('page');if(page&&!value.pages.some(p=>p.page_id===page)){search.set('page',value.default_page_id);navigate({pathname:location.pathname,search:search.toString()},{replace:true});}setDraft(value);setDirty(!version||JSON.stringify(value)!==JSON.stringify(canvasDefinition(version.definition))||resultRefs(value).some(ref=>version.results.find(saved=>saved.block_id===ref.block_id)?.result_id!==ref.result_id));setReady(old=>{const next:Record<string,Ready>={...old};for(const b of value.blocks){if(!b.source)continue;const key=queryKey(value,b);const match=Object.values(old).find(r=>r.key===key);if(match)next[b.block_id]={...match,binding:{...match.binding,card_id:b.block_id}};}return next;});};
 const editGroup=useRef({active:false,recorded:false});
 const update=(value:Definition)=>{if(mutationBlocked.current||!d)return;const grouped=editGroup.current.active&&editGroup.current.recorded;editGroup.current.recorded=editGroup.current.active;setHistory(old=>grouped&&old?{...old,present:value,future:[]}:record(old??startHistory(d),value));install(value);};
 const stepHistory=(direction:'undo'|'redo')=>{editGroup.current={active:false,recorded:false};if(locked||readOnly||!history)return;const next=travel(history,direction);setHistory(next);install(next.present);};
 useEffect(()=>{if(!dirty)return;const before=(event:BeforeUnloadEvent)=>event.preventDefault();window.addEventListener('beforeunload',before);return()=>window.removeEventListener('beforeunload',before);},[dirty]);
 const resultRefs=(d:Definition):C.ComposerResultRef[]=>d.blocks.filter(b=>b.source).flatMap(b=>{const value=ready[b.block_id];if(value?.key===queryKey(d,b))return [{block_id:b.block_id,result_id:value.result.result_id}];
   const old=version?.definition.blocks.find(o=>o.source&&queryKey(version.definition,o)===queryKey(d,b)&&version.results.some(r=>r.block_id===o.block_id)),ref=version?.results.find(r=>r.block_id===old?.block_id);
   return old&&ref?[{...ref,block_id:b.block_id}]:[];});
 const save=async()=>{if(!d||saving||comparing||validations.current.size>0||runningBlocks.size>0||conflict||readOnly)return;mutationBlocked.current=true;setSaving(true);setNotice('');
  const results=resultRefs(d);const key=pairKey(d,results);
  const verified=comparison?.key===key?comparison.value:version?.comparison&&pairKey(version.definition,version.results)===key?version.comparison:undefined;
  const input={...(verified?{comparison:verified}:{}),contract_version:'analytical-authoring/v1' as const,definition:d,expected_revision:version?.revision??0,results};
  if(!pending.current)pending.current={...input,idempotency_key:crypto.randomUUID()};
  const body=pending.current;
  try{const value=await api.save(body,csrf());setSaved(value);setDirty(false);setHistory(null);pending.current=null;if(isNew)navigate(`/w/${workspace}/reports/${value.report_id}/edit?view=composer`,{replace:true});
  }catch(e){if(e instanceof C.ComposerRequestError&&e.status>=400&&e.status<500&&e.status!==409)pending.current=null;setConflict(e instanceof C.ComposerRequestError&&e.status===409);setNotice(e instanceof C.ComposerRequestError&&e.status===409?c.conflict:c.saveError);}finally{setSaving(false);}
 };
 if(!trusted)return <PendingWorkspace locale={locale}/>;
 if(products.isError||prepared.isError||editor.isError)return <PendingWorkspace locale={locale} error={c.error} retry={()=>void (isNew?(products.isError?products.refetch():prepared.refetch()):editor.refetch())}/>;
 if(isNew&&products.data&&!chosen)return <PilotDocument model={{workspace:true,locale,title:c.add,source:'',start:'',end:'',store:'',comparison:'none',actor:{workspace_id:workspace,principal_id:'',permissions:[]},status:'',hint:'',busy:false,preview:true,focus:false,unapplied:true,conflict:false,stores:[]}} actions={{library:()=>navigate(`/w/${workspace}/reports`),title:()=>{},locale:l=>void i18n.changeLanguage(l),draft:()=>{},apply:()=>{},save:()=>{},reload:()=>{},preview:()=>{},urlChanged:()=>{}}}><section className="composer"><style>{styles}</style><label>{c.product}<select value={dataset} onChange={e=>setDataset(e.target.value)}><option value="">{c.choose}</option>{products.data.datasets.map(p=><option key={p.id} value={p.id}>{p.label}</option>)}</select></label>{!products.data.datasets.length&&<p>{c.noSources}</p>}</section></PilotDocument>;
 if(!d||!actor)return <PendingWorkspace locale={locale}/>;
 if(actor.workspace_id!==workspace||actor.principal_id!==d.creator_principal_id)return <PendingWorkspace locale={locale} error={c.error}/>;
 const requestedPage=new URLSearchParams(location.search).get('page');
 const requestedExists=!requestedPage||d.pages.some(p=>p.page_id===requestedPage);
 const activePage=requestedPage&&requestedExists?requestedPage:d.default_page_id;
 if((!requestedExists&&!draft)||readOnly&&isHidden(d,{kind:'page',id:activePage}))return <PendingWorkspace locale={locale} error={c.error}/>;
 const pageLocked=isLocked(d,{kind:'page',id:activePage});
 const activate=(page:string)=>{const search=new URLSearchParams(location.search);search.set('page',page);navigate({pathname:location.pathname,search:search.toString()});};
 const add=(target:HTMLElement)=>{if(validations.current.size||locked||readOnly||pageLocked)return;trigger.current=target;setPalette(p=>!p);};
 const chosenBlock=d.blocks.find(b=>b.block_id===selected);
 const destination=d.sections.find(s=>s.page_id===activePage&&!isLocked(d,{kind:'section',id:s.section_id}))?.section_id;
 const patchContent=(block:C.ComposerBlock,patch:Partial<C.ComposerBlock>)=>{if(!readOnly&&!locked&&!isLocked(d,{kind:'block',id:block.block_id}))update({...d,blocks:d.blocks.map(b=>b.block_id===block.block_id?{...b,...patch}:b)});};
 const addKind=(kind:'chart'|'table'|'metric'|'text'|'filter')=>{setPalette(false);if(!destination)return;if(kind==='chart'||kind==='table'||kind==='metric'){setBuilder('new:'+kind);return;}try{const next=addContent(d,destination,kind,locale);update(next);setSelected(next.blocks.at(-1)!.block_id);setInspectorTab('data');setBuilder(null);}catch{setNotice(locale==='ru'?'Сначала добавьте график или таблицу с источником данных.':'Add a chart or table with a data source first.');}};
 const copyBlock=(id:string)=>{if(readOnly||locked||isLocked(d,{kind:'block',id}))return;try{const next=duplicate(d,id);update(next);setSelected(next.blocks.at(-1)!.block_id);}catch{setNotice(c.invalid);}};
 const deleteBlock=(id:string)=>{if(!readOnly&&!locked&&!isLocked(d,{kind:'block',id}))setPendingDelete(id);};
 const confirmDelete=()=>{const id=pendingDelete;setPendingDelete(null);if(!id||readOnly||locked||isLocked(d,{kind:'block',id}))return;try{update(removeBlock(d,id));if(selected===id)setSelected(null);title.current?.focus();}catch{setNotice(c.invalid);}};
 return <PilotDocument headerTitle={<input className="mw-report-title" ref={title} aria-label={c.title} maxLength={200} value={d.title} disabled={readOnly||locked} onChange={e=>update({...d,title:e.target.value})}/>} headerActions={<div className="composer-toolbar"><span role="status">{saving?c.loading:dirty?c.unsaved:c.saved}</span>{!readOnly&&<button disabled={saving||comparing||validating||runningBlocks.size>0||conflict} className="composer-save" onClick={()=>void save()}><Save size={16}/>{c.save}</button>}{version&&<button onClick={()=>{if(!dirty||confirm(c.discard))navigate(`/w/${workspace}/reports/${d.document_id}/snapshots/${version.snapshot_id}?view=composer&page=${activePage}`);}}><Eye size={16}/>{c.preview}</button>}</div>}
 worksetControls={!readOnly&&<div className="composer-command-bar"><button className="composer-add-trigger" aria-expanded={palette} disabled={locked||validating||pageLocked} onClick={e=>add(e.currentTarget)}><Plus size={16}/>{c.add}<ChevronDown size={14}/></button><span className="composer-command-divider"/><button aria-label={locale==='ru'?'Отменить':'Undo'} title={locale==='ru'?'Отменить':'Undo'} disabled={locked||!history?.past.length} onClick={()=>stepHistory('undo')}><Undo2 size={17}/></button><button aria-label={locale==='ru'?'Повторить':'Redo'} title={locale==='ru'?'Повторить':'Redo'} disabled={locked||!history?.future.length} onClick={()=>stepHistory('redo')}><Redo2 size={17}/></button><span className="composer-command-hint">{locale==='ru'?'Перетаскивайте блок, меняйте размер за угол':'Drag the block; resize by the corner'}</span></div>}

 inspectorOpen={!readOnly&&(settingsOpen||selected!==null||builder!==null)} inspector={!readOnly&&(settingsOpen||selected!==null||builder!==null)&&(builder?.startsWith('new:')?<ComposerBuilder onValidating={onValidating} key={builder} initialKind={builder==='new:metric'?'metric':builder==='new:table'?'table':'chart'} definition={d} destination={destination} locale={locale} disabled={locked} close={close} commit={(next,blockId)=>{update(next);setSelected(blockId);setInspectorTab('data');close();}}/>:<ComposerInspector onEdit={active=>{editGroup.current={active,recorded:false};}} tab={inspectorTab} onTab={setInspectorTab} definition={d} block={chosenBlock} locale={locale} busy={locked} close={()=>{setSelected(null);setSettingsOpen(false);}} commit={update} onValidating={onValidating}/>)}
 model={{workspace:true,documentPages:true,workspaceChrome:{period:'',comparison:'',stores:'',grain:'',unavailable:''},locale,title:d.title,source:'',start:'',end:'',store:'',comparison:'none',actor,status:dirty?c.unsaved:c.saved,hint:'',busy:locked,preview,focus:false,unapplied:false,conflict,stores:[]}}
 actions={{library:()=>{if(!dirty||confirm(c.discard))navigate(`/w/${workspace}/reports`);},title:t=>update({...d,title:t}),locale:l=>void i18n.changeLanguage(l),draft:()=>{},apply:()=>{},save:()=>void save(),reload:()=>{if(confirm(c.discard)){setDraft(null);setHistory(null);setReady({});setSaved(undefined);setDirty(false);setConflict(false);setNotice('');pending.current=null;void editor.refetch();}},preview:()=>{},urlChanged:()=>{},inspector:()=>{if(settingsOpen||selected!==null||builder!==null){close();setSelected(null);setSettingsOpen(false);}else setSettingsOpen(true);}}}>
 <section className="composer composer-prototype" data-profile={d.profile} data-read-only={readOnly}><style>{styles}</style><div className="composer-page-heading"><LayoutGrid size={15}/><span>{locale==='ru'?'Обзор':'Overview'}</span></div>{d.pages.filter(p=>!readOnly||!isHidden(d,{kind:'page',id:p.page_id})).length>1&&<nav className="composer-page-tabs" aria-label={locale==='ru'?'Страницы отчёта':'Report pages'}>{d.pages.filter(p=>!readOnly||!isHidden(d,{kind:'page',id:p.page_id})).map(page=><button key={page.page_id} aria-current={page.page_id===activePage?'page':undefined} onClick={()=>activate(page.page_id)}>{page.title}</button>)}</nav>}{notice&&<p role="alert">{notice}</p>}{conflict&&<button onClick={()=>{if(confirm(c.discard)){setDraft(null);setHistory(null);setSaved(undefined);setDirty(false);setConflict(false);setNotice('');setReady({});pending.current=null;void editor.refetch();}}}>{c.reload}</button>}

 {!readOnly&&palette&&<div className="composer-add-palette" role="dialog" aria-label={c.add}>{([['metric',Hash,locale==='ru'?'Метрика':'Metric'],['chart',LineChart,locale==='ru'?'График':'Chart'],['table',Table2,locale==='ru'?'Таблица':'Table'],['text',Type,locale==='ru'?'Текст':'Text'],['filter',Filter,locale==='ru'?'Локальный фильтр':'Local filter']] as const).map(([kind,Icon,label])=><button key={kind} onClick={()=>addKind(kind)}><Icon size={18}/>{label}<Plus size={14}/></button>)}</div>}
 {!d.blocks.length&&<p>{c.empty}</p>}
 {d.pages.filter(p=>p.page_id===activePage).map(page=><section key={page.page_id} role="tabpanel" id={`page-panel-${page.page_id}`} aria-label={page.title} data-layout={page.layout}>{orderedSections(d,page.page_id).filter(s=>!readOnly||!isHidden(d,{kind:'section',id:s.section_id})).map(section=><section key={section.section_id} className="composer-section" aria-label={section.title} style={{marginInlineStart:sectionDepth(d,section.section_id)*12}}>{orderedSections(d,page.page_id).length>1&&<h2>{section.title}</h2>}<ComposerCanvas copy={copyBlock} remove={deleteBlock} definition={d} section={section.section_id} blocks={d.blocks.filter(b=>b.section_id===section.section_id&&(!readOnly||!isHidden(d,{kind:'block',id:b.block_id}))).slice().sort((a,b)=>a.order-b.order)} selected={selected} select={(id,tab)=>{setSelected(id);setBuilder(null);if(tab)setInspectorTab(tab);}} readOnly={readOnly} busy={locked} locale={locale} commit={update} render={block=>block.source? <Block key={block.block_id} definition={d} block={block} locale={locale} saved={version} selected={selected===block.block_id} select={()=>setSelected(block.block_id)} edit={element=>{trigger.current=element;setSelected(block.block_id);setBuilder(block.block_id);}} copy={()=>copyBlock(block.block_id)} remove={()=>deleteBlock(block.block_id)} ready={ready[block.block_id]} onReady={value=>{setReady(old=>({...old,[block.block_id]:value}));setDirty(true);}} onLoaded={remember} onRunning={onRunning} preview={readOnly} busy={locked||isLocked(d,{kind:'block',id:block.block_id})} canApply={capabilities?.block_apply===true} layout={change=>{try{update(arrangeBlocks(d,block.block_id,change));setNotice('');}catch{setNotice(locale==='ru'?'Не удалось изменить раскладку: проверьте блокировки блоков.':'Cannot change layout: check block locks.');}}}/>:block.block_type==='text'?<div style={{textAlign:block.presentation.visual?.text_align,fontSize:block.presentation.visual?.text_size==='large'?18:block.presentation.visual?.text_size==='small'?11:undefined}} className={`composer-text-body ${(block.placement?.row_span??3)===1?'is-compact':''} ${block.text_style==='callout'?'callout':''}`}>{((block.presentation.show_title!==false&&block.presentation.title.trim())||block.presentation.description?.trim())&&<h2><ComposerBlockTitle presentation={block.presentation}/></h2>}<p>{block.text}</p></div>:<ControlBody compact block={block} locale={locale} disabled={readOnly||locked||isLocked(d,{kind:'block',id:block.block_id})} change={patch=>patchContent(block,patch)}/>}/></section>)}</section>)}
 {pendingDelete&&<ComposerDeleteDialog name={d.blocks.find(b=>b.block_id===pendingDelete)?.presentation.title||(locale==='ru'?'Без названия':'Untitled')} locale={locale} cancel={()=>setPendingDelete(null)} confirm={confirmDelete}/>}
 </section></PilotDocument>;
}
