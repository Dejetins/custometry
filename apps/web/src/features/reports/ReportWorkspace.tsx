import { pilotPeriod } from './pilot-period';
import { PilotDocument } from './PilotDocument';
import { useEffect, useRef, useState, useSyncExternalStore, type ReactNode } from 'react';
import { QueryClientProvider, useMutation, useQuery } from '@tanstack/react-query';
import { Link, useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { PilotFrame, PilotIcon } from './PilotChrome';
import type { FeatureRouteProps } from '../../app/routes/feature-route-contract';
import { accessStore, reportApi, reportQueries, csrf, resultOf, type Actor, type Draft, type References, type Result } from './report-api';
import { reportCopy, type Copy } from './copy';
import './report.css';

function useCopy() { const { i18n }=useTranslation(); const locale:'ru'|'en'=i18n.resolvedLanguage === 'ru' ? 'ru' : 'en'; return {locale, c:reportCopy[locale], switchLocale:()=>{const next=locale==='ru'?'en':'ru';try{window.localStorage.setItem('custometry-language',next);}catch{/* Locale still works for this page when preferences are unavailable. */}void i18n.changeLanguage(next);}}; }
function Frame({children, workspace, title}: {children:ReactNode;workspace?:string;title:string}) {
  const {locale,switchLocale}=useCopy();
  return <PilotFrame workspace={workspace} title={title} locale={locale} switchLocale={switchLocale}>{children}</PilotFrame>;
}
function Login() {
  const {c}=useCopy(); const navigate=useNavigate(); const [workspace,setWorkspace]=useState('');const [email,setEmail]=useState('');const [password,setPassword]=useState('');
  const login=useMutation({mutationFn:()=>reportApi.login(workspace,email,password),onSuccess:(id)=>{setPassword('');navigate(`/w/${id}/reports`);}});
  return <Frame title={c.signIn}><section className="workspace report-login-workspace"><form className="report-login" onSubmit={(e)=>{e.preventDefault();login.mutate();}}><span className="report-eyebrow">Custometry</span><h1>{c.signIn}</h1><p>{c.loginHelp}</p><label>{c.workspace}<input required autoComplete="organization" value={workspace} onChange={(e)=>setWorkspace(e.target.value)}/></label><label>{c.email}<input required type="email" autoComplete="username" value={email} onChange={(e)=>setEmail(e.target.value)}/></label><label>{c.password}<input required type="password" autoComplete="current-password" value={password} onChange={(e)=>setPassword(e.target.value)}/></label><button className="primary" disabled={login.isPending}>{login.isPending?c.loading:c.signIn}</button>{login.error&&<p role="alert">{c.loginError}</p>}</form></section></Frame>;
}
function Protected({resolution}:FeatureRouteProps) {
  const {c}=useCopy();const denied=useSyncExternalStore(accessStore.subscribe,accessStore.get);const actor=useQuery({queryKey:['report-actor'],queryFn:reportApi.me,enabled:!denied,refetchInterval:10000});
  const workspace=resolution.workspaceKey ?? '';
  if(denied||actor.isError) return <Frame title={c.signIn}><div className="report-message"><p role="alert">{c.denied}</p><Link to="/auth/sign-in">{c.signIn}</Link></div></Frame>;
  if(!actor.data)return <Frame title={c.reports}><p role="status">{c.loading}</p></Frame>;
  if(actor.data.workspace_id!==workspace)return <Frame title={c.reports}><p role="alert">{c.workspaceMismatch}</p></Frame>;
  return resolution.route.id==='UI-RPT-001'?<Frame title={c.reports} workspace={workspace}><Library workspace={workspace}/></Frame>:<Editor key={window.location.pathname} workspace={workspace} actor={actor.data} preview={resolution.route.id==='UI-RPT-003'}/>;
}
function Library({workspace}:{workspace:string}) {
  const {c}=useCopy();const list=useQuery({queryKey:['reports',workspace],queryFn:()=>reportApi.drafts.list()});
  return <section className="workspace report-library-workspace"><header className="page-header"><span className="report-eyebrow">{c.reports}</span><h1>{c.library}</h1></header><section className="report-library"><Link className="report-template" to={`/w/${workspace}/reports/new/edit`}><PilotIcon name="analytics"/><h2>{c.template}</h2><span>{c.newReport} →</span></Link>{list.isPending&&<p role="status">{c.loading}</p>}{list.isError?<p role="alert">{c.unavailable}</p>:list.data?.reports.length===0?<p>{c.noReports}</p>:<ul>{list.data?.reports.map((r)=><li key={r.report_id}><Link to={`/w/${workspace}/reports/${r.report_id}/edit`}>{r.title}</Link><small>{c.saved} · {c.version} {r.revision}</small></li>)}</ul>}</section></section>;
}
interface Form {title:string;dataset:string;start:string;end:string;store:string;comparison:'none'|'previous_year_same_dates'}
function fromResult(title:string,result:Result):Form { const p=result.parameters.period as Record<string,string>;return {title,dataset:result.semantic_dataset_version_id,start:p.starts_on,end:p.ends_on,store:String(result.parameters.store_id??''),comparison:result.parameters.comparison as Form['comparison']}; }
const draftMemory=new Map<string,{form:Form;applied?:Form;resultKey?:string;baseRevision:number}>();
accessStore.subscribe(()=>draftMemory.clear());
function sameContext(a:Form,b:Form){return a.dataset===b.dataset&&a.start===b.start&&a.end===b.end&&a.store===b.store&&a.comparison===b.comparison;}
function Editor({workspace,actor,preview}:{workspace:string;actor:Actor;preview:boolean}) {
  const {c,locale,switchLocale}=useCopy();const location=useLocation();const navigate=useNavigate();const [params,setParams]=useSearchParams();const parts=location.pathname.split('/');const id=parts[4];const snapshot=preview?parts[6]:undefined;const isNew=id==='new';
  const saved=useQuery({queryKey:['report',workspace,id,snapshot,...(snapshot?[params.get('page')]:[])],queryFn:()=>snapshot?reportApi.drafts.preview(id,snapshot,params.has('page')?{page_id:params.get('page')!}:{}):reportApi.drafts.get(id),enabled:!isNew,refetchOnWindowFocus:false,refetchOnReconnect:false});
  const context=useQuery({queryKey:['report-context',workspace],queryFn:reportApi.context,enabled:!preview});
  const memoryKey=workspace+location.pathname;const memory=draftMemory.get(memoryKey);
  const [baseRevision,setBaseRevision]=useState(memory?.baseRevision??0);
  const [form,setForm]=useState<Form>(memory?.form??{title:c.template,dataset:'',start:'2025-01-01',end:'2025-11-30',store:'',comparison:'none'});
  const [initialized,setInitialized]=useState(Boolean(memory));const [applied,setApplied]=useState<Form|undefined>(memory?.applied);const [resultKey,setResultKey]=useState<string|undefined>(memory?.resultKey);const [dirty,setDirty]=useState(Boolean(memory));const [conflict,setConflict]=useState(false);
  const focus=Boolean(params.get('focus'));const table=params.get('tab')==='table';
  const appliedQuery=useQuery({queryKey:['report-applied',workspace,resultKey],queryFn:async()=>null as {result:Result;refs:References}|null,enabled:false});
  const display=resultKey?appliedQuery.data:(saved.data?{result:resultOf(saved.data),refs:saved.data.references}:undefined);
  const latestDraft=useRef({form,applied,resultKey,baseRevision,dirty});latestDraft.current={form,applied,resultKey,baseRevision,dirty};
  useEffect(()=>()=>{const latest=latestDraft.current;if(latest.dirty&&!accessStore.get())draftMemory.set(memoryKey,latest);else draftMemory.delete(memoryKey);},[memoryKey]);
  const result=display?.result;
  useEffect(()=>{if(saved.data&&!initialized){setForm(fromResult(saved.data.title,resultOf(saved.data)));setBaseRevision(saved.data.revision);setInitialized(true);}},[saved.data,initialized]);
  useEffect(()=>{if(isNew&&!form.dataset&&context.data?.datasets.length===1){setForm((f)=>({...f,dataset:context.data!.datasets[0].id,start:String(context.data!.default_period.starts_on),end:String(context.data!.default_period.ends_on)}));}},[context.data,isNew,form.dataset]);
  useEffect(()=>{if(!dirty)return;const before=(e:BeforeUnloadEvent)=>{e.preventDefault();};const anchor=(e:MouseEvent)=>{const a=(e.target as Element).closest('a');if(a&&a.pathname!==location.pathname&&!window.confirm(c.discard)){e.preventDefault();e.stopPropagation();}};window.addEventListener('beforeunload',before);document.addEventListener('click',anchor,true);return()=>{window.removeEventListener('beforeunload',before);document.removeEventListener('click',anchor,true);};},[dirty,c.discard,location.pathname]);
  const update=(patch:Partial<Form>)=>{setForm((f)=>({...f,...patch}));setDirty(true);};
  const calculate=useMutation({mutationFn:async(submitted:Form)=>{const data=await reportApi.run({semantic_dataset_version_id:submitted.dataset,starts_on:submitted.start,ends_on:submitted.end,store_id:submitted.store||null,comparison:submitted.comparison});const refs=await reportApi.drafts.prepare({contract_version:'draft-report/v1',result_id:data.result_id},csrf());return {submitted,data,refs};},onSuccess:({submitted,data,refs})=>{reportQueries.setQueryData(['report-applied',workspace,data.result_id],{result:data,refs});setResultKey(data.result_id);setApplied(submitted);setDirty(true);}});
  const saving=useMutation({mutationFn:async(title:string)=>{if(!display)throw Error('NO_RESULT');const request={contract_version:'draft-report/v1' as const,title:title.trim(),expected_revision:baseRevision,idempotency_key:crypto.randomUUID(),result_id:display.result.result_id,chart_spec:display.refs.chart_spec.reference,brand_profile:display.refs.brand_profile.reference,company_pack:display.refs.company_pack.reference};return isNew?reportApi.drafts.create(request,csrf()):reportApi.drafts.save(id,request,csrf());},onSuccess:(data)=>{setBaseRevision(data.revision);reportQueries.setQueryData(['report',workspace,data.report_id,undefined],data);setDirty(false);setConflict(false);setResultKey(undefined);setApplied(undefined);if(isNew)navigate(`/w/${workspace}/reports/${data.report_id}/edit`,{replace:true});},onError:(error)=>{if(error.message.includes('CONFLICT'))setConflict(true);}});
  const busy=calculate.isPending||saving.isPending;const unapplied=!result||!sameContext(form,applied??fromResult(form.title,result));
  const reload=async()=>{const data=await saved.refetch();if(data.data){setBaseRevision(data.data.revision);setForm(fromResult(data.data.title,resultOf(data.data)));setResultKey(undefined);setApplied(undefined);setConflict(false);setDirty(false);saving.reset();calculate.reset();}};
  if(saved.data&&((params.has('page')&&params.get('page')!==saved.data.composition.default_page_id)||(focus&&!saved.data.composition.blocks.some((b)=>b.block_id===params.get('focus')))))return <p role="alert">{c.unavailable}</p>;
  if(!isNew&&saved.isPending)return <p role="status">{c.loading}</p>;
  if(!isNew&&saved.isError)return <div className="report-message"><p role="alert">{c.unavailable}</p><button onClick={()=>{void saved.refetch();}}>{c.retry}</button></div>;
  if(!preview&&(!context.data||!form.dataset))return <Frame title={c.reports}><p role="status">{context.isError?c.noSource:c.loading}</p></Frame>;
  return <PilotDocument model={{locale,source:context.data?.datasets.find(d=>d.id===form.dataset)?.label??c.source,title:form.title,start:form.start,end:form.end,store:form.store,comparison:form.comparison,result,refs:display?.refs,actor,status:busy?c.calculating:dirty?c.unsaved:c.saved,error:conflict?c.conflict:(calculate.error||saving.error)?c.unavailable:undefined,hint:c.pending,busy,preview,focus,unapplied,conflict,stores:context.data?.datasets.find(d=>d.id===form.dataset)?.stores??[]}} actions={{
    library:()=>{if(!dirty||window.confirm(c.discard))navigate(`/w/${workspace}/reports`);},title:title=>update({title}),locale:next=>{if(next!==locale)switchLocale();},
    draft:({period,store,comparison})=>update({...pilotPeriod(period),store,comparison}),
    apply:({period,store,comparison})=>{const submitted={...form,...pilotPeriod(period),store,comparison};update(submitted);calculate.mutate(submitted);},
    save:title=>saving.mutate(title),reload:()=>{void reload();},preview:()=>{if(dirty&&!window.confirm(c.discard))return;if(saved.data)navigate(`/w/${workspace}/reports/${id}/snapshots/${saved.data.snapshot_id}?page=${saved.data.composition.default_page_id}`);},
    urlChanged:href=>{const url=new URL(href);const next=new URLSearchParams(params);if(url.searchParams.has('focus'))next.set('focus',saved.data?.composition.blocks.find(b=>b.block_type==='chart')?.block_id??'daily');else next.delete('focus');setParams(next);}
  }}/>;
}

export default function ReportRoute(props:FeatureRouteProps) {return <QueryClientProvider client={reportQueries}>{props.resolution.route.id==='UI-AUTH-001'?<Login/>:<Protected {...props}/>}</QueryClientProvider>;}
