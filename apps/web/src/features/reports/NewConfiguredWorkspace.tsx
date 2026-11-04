import {useLayoutEffect,useState} from 'react';
import {useQuery} from '@tanstack/react-query';
import {useLocation,useNavigate} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import {ConfiguredWorkspace,PendingWorkspace} from './ConfiguredWorkspace';
import {reportApi,csrf} from './report-api';
import {workspaceReports} from './workspace-api';
import {PilotFrame} from './PilotChrome';

/** Preparation resolves authorized defaults; only Save creates the document. */
export function NewConfiguredWorkspace({workspace,trusted,channelUnavailable,retryChannel}:{workspace:string;trusted:boolean;channelUnavailable:boolean;retryChannel:()=>void}){
 const {i18n}=useTranslation();const locale=i18n.resolvedLanguage==='ru'?'ru':'en';const ru=locale==='ru';
 const location=useLocation();const template=location.state?.template==='blank'?'blank':'sales';
 const navigate=useNavigate();
 const [reportId]=useState(()=>typeof location.state?.draftId==='string'?location.state.draftId:crypto.randomUUID());
 useLayoutEffect(()=>{if(location.state?.draftId!==reportId)navigate(location.pathname+location.search,{replace:true,state:{...location.state,draftId:reportId}});},[location.pathname,location.search,location.state,reportId,navigate]);const [selected,setSelected]=useState('');
 const source=useQuery({queryKey:['new-report-sources',workspace],queryFn:reportApi.context,enabled:trusted,refetchOnWindowFocus:false,refetchOnReconnect:false});
 const dataset=selected||(source.data?.datasets.length===1?source.data.datasets[0].id:'');
 const prepared=useQuery({queryKey:['new-workspace',workspace,reportId,dataset,template],enabled:trusted&&Boolean(dataset&&source.data),refetchOnWindowFocus:false,refetchOnReconnect:false,
  queryFn:()=>workspaceReports.prepareNew({report_id:reportId,semantic_dataset_version_id:dataset,template,locale,common_context:{starts_on:String(source.data!.default_period.starts_on),ends_on:String(source.data!.default_period.ends_on),store_ids:null}},csrf())});
 if(!trusted)return <PendingWorkspace locale={locale} error={channelUnavailable?(ru?'Не удалось проверить доступ.':'Could not verify access.'):undefined} retry={channelUnavailable?retryChannel:undefined} showSignIn={false}/>;
 if(source.isError||prepared.isError)return <PendingWorkspace locale={locale} error={ru?'Не удалось подготовить новый отчёт. Проверьте доступ к источнику данных.':'Could not prepare the report. Check source access.'} retry={()=>void (source.isError?source.refetch():prepared.refetch())}/>;
 if(source.data&&!dataset)return <PilotFrame workspace={workspace} title={ru?'Новый отчёт':'New report'} locale={locale} switchLocale={()=>void i18n.changeLanguage(ru?'en':'ru')}><section className="workspace report-library-workspace"><h1>{ru?'Источник данных':'Data source'}</h1>{source.data.datasets.length?<label>{ru?'Выберите источник для отчёта':'Choose the report source'}<select value={selected} onChange={event=>setSelected(event.target.value)}><option value="">{ru?'Выберите источник':'Choose a source'}</option>{source.data.datasets.map(item=><option key={item.id} value={item.id}>{item.label}</option>)}</select></label>:<p>{ru?'Нет доступных источников данных.':'No data sources are available.'}</p>}</section></PilotFrame>;
 if(!prepared.data)return <PendingWorkspace locale={locale}/>;
 return <ConfiguredWorkspace workspace={workspace} actor={prepared.data.actor} initialDefinition={prepared.data.definition} sourceLabel={source.data?.datasets.find(item=>item.id===dataset)?.label} preview={false} trusted={trusted}/>;
}
