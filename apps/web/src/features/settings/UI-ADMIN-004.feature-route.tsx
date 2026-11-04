import './company-settings.css';
import {useSyncExternalStore} from 'react';
import {QueryClientProvider,useQuery} from '@tanstack/react-query';
import {Link} from 'react-router-dom';
import {useTranslation} from 'react-i18next';
import type {FeatureRouteProps} from '../../app/routes/feature-route-contract';
import {CalendarSettings} from '../reports/WorkspaceCalendar';
import {workspaceCalendar} from '../reports/workspace-api';
import {accessStore,reportApi,reportQueries} from '../reports/report-api';
import {useReportSession} from '../reports/session-channel';

export const routeId='UI-ADMIN-004';
function Settings({resolution}:FeatureRouteProps){
 const {i18n}=useTranslation(),locale=i18n.resolvedLanguage==='ru'?'ru':'en',ru=locale==='ru';
 const session=useReportSession(),denied=useSyncExternalStore(accessStore.subscribe,accessStore.get);
 const workspace=resolution.workspaceKey??'';
 const actor=useQuery({queryKey:['company-settings-actor',workspace,session.epoch],queryFn:reportApi.me,enabled:session.trusted&&!denied});
 const allowed=actor.data?.workspace_id===workspace&&actor.data.permissions.includes('workspace.manage');
 const calendar=useQuery({queryKey:['company-calendar',workspace,session.epoch],queryFn:()=>workspaceCalendar.get(),enabled:session.trusted&&!denied&&allowed});
 if(denied||actor.isError||actor.data&&!allowed)return <section><h1 tabIndex={-1}>{ru?'Настройки компании':'Company settings'}</h1><p role="alert">{ru?'Нет доступа к настройкам компании.':'Company settings access denied.'}</p><Link to="/auth/sign-in">{ru?'Войти':'Sign in'}</Link></section>;
 if(!session.trusted||!actor.data)return <section><p role="status">{ru?'Проверка доступа…':'Checking access…'}</p>{session.unavailable&&<button onClick={session.retry}>{ru?'Повторить':'Retry'}</button>}</section>;
 return <section><h1 tabIndex={-1}>{ru?'Настройки компании':'Company settings'}</h1><p>{ru?'Финансовый календарь и часовой пояс':'Financial calendar and time zone'}</p>{calendar.isError?<p role="alert">{ru?'Не удалось загрузить календарь.':'Could not load calendar.'}<button onClick={()=>void calendar.refetch()}>{ru?'Повторить':'Retry'}</button></p>:<CalendarSettings actor={actor.data} locale={locale} value={calendar.data} onSaved={()=>void calendar.refetch()}/>}<p><Link to={`/w/${workspace}/reports`}>{ru?'Отчёты':'Reports'}</Link></p></section>;
}
export default function CompanySettings(props:FeatureRouteProps){return <QueryClientProvider client={reportQueries}><Settings {...props}/></QueryClientProvider>;}
