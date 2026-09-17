import { reportPilotCopy } from '@custometry/localization';
import { useEffect, useRef, useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { pilotSymbols } from './pilot-symbols';
import { reportApi } from './report-api';
import './pilot.css';

export function PilotIcon({name, small = false}: {name: string; small?: boolean}) {
  return <svg className={`icon${small ? ' icon--small' : ''}`} aria-hidden="true"><use href={`#i-${name}`}/></svg>;
}
export function PilotFrame({children, workspace, locale, switchLocale, title}: {
  children: ReactNode; workspace?: string; locale: 'ru'|'en'; switchLocale: () => void; title: string;
}) {
  const [section, setSection] = useState<number | null>(null);
  const trigger = useRef<HTMLButtonElement | null>(null);
  const ru = locale === 'ru';
  const names = ru ? ['Обзор', 'Аналитика', 'Модели и аудитории', 'Результаты', 'Данные и управление', 'Помощь', 'Профиль'] : ['Overview', 'Analytics', 'Models & audiences', 'Results', 'Data & management', 'Help', 'Profile'];
  const icons = ['home', 'analytics', 'layers', 'results', 'server', 'help', 'user'];
  const close = () => { setSection(null); trigger.current?.focus(); };
  useEffect(() => { document.title = `${title} · Custometry`; document.documentElement.lang = locale; }, [title,locale]);
  useEffect(() => { const escape = (e: KeyboardEvent) => { if(e.key === 'Escape') close(); }; window.addEventListener('keydown',escape); return () => window.removeEventListener('keydown',escape); }, []);
  const rail = (index: number) => <button className="rail-button" type="button" key={icons[index]} aria-label={names[index]} title={names[index]} aria-current={index===1 ? 'page' : undefined} aria-expanded={section===index} onClick={(e)=>{trigger.current=e.currentTarget;setSection(section===index?null:index);}}>{index===6?<span className="avatar">AN</span>:<PilotIcon name={icons[index]}/>}</button>;
  return <div className="report-pilot"><a className="pilot-skip-link" href="#report-main">{reportPilotCopy[locale].skipToReport}</a><div dangerouslySetInnerHTML={{__html:pilotSymbols}}/>
    <div className="pilot-app-shell" data-sidebar="collapsed" data-nav-context={section!==null?'open':'closed'}>
      <aside className="pilot-sidebar"><div className="rail-brand">C</div><nav className="rail-nav" aria-label={reportPilotCopy[locale].navigation}><button className="rail-button" disabled title={reportPilotCopy[locale].searchIsNotAvailable} aria-label={reportPilotCopy[locale].search}><PilotIcon name="search"/></button>{[0,1,2,3,4].map(rail)}<div className="rail-separator"/>{workspace?<Link className="rail-button" to={`/w/${workspace}/notifications`} aria-label={reportPilotCopy[locale].notifications}><PilotIcon name="bell"/></Link>:null}</nav><div className="rail-footer">{[5,6].map(rail)}</div></aside>
      {section!==null&&<><div className="nav-context-backdrop" onClick={close}/><section className="nav-context-panel" aria-label={names[section]}><header className="nav-context-header"><h2>{names[section]}</h2><button className="icon-button" aria-label={reportPilotCopy[locale].closeSectionMenu} onClick={close}><PilotIcon name="x"/></button></header><div className="nav-context-body">
        {section===6?<><button className="nav-context-link" onClick={switchLocale}><PilotIcon name="globe"/><span>{reportPilotCopy[locale].language}</span></button>{workspace&&<button className="nav-context-link" onClick={()=>{void reportApi.logout().catch(()=>{});close();}}>{reportPilotCopy[locale].signOut}</button>}</>:section===5?<a className="nav-context-link" href={`/docs/${ru?'ru/':''}user-guide/reports/`}><PilotIcon name="help"/><span>{reportPilotCopy[locale].reportHelp}</span></a>:<><Link className="nav-context-link" to={workspace?`/w/${workspace}/reports`:'/auth/sign-in'} onClick={close}><PilotIcon name="file"/><span>{reportPilotCopy[locale].reports}</span></Link>{section===0&&<Link className="nav-context-link" to="/" onClick={close}>{reportPilotCopy[locale].home}</Link>}</>}
      </div></section></>}{children}
    </div>
  </div>;
}

export function PilotPopover({label, icon, children, summary, className = ''}: {label: string; icon: string; children: ReactNode; summary?: string; className?: string}) {
  const dialog = useRef<HTMLDialogElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const [open,setOpen] = useState(false);
  const close = () => {dialog.current?.close();setOpen(false);trigger.current?.focus();};
  const show = () => {const el=dialog.current;const button=trigger.current;if(!el||!button)return;const box=button.getBoundingClientRect();el.style.left=`${Math.max(8,Math.min(box.left,window.innerWidth-306))}px`;el.style.top=`${Math.min(box.bottom+6,window.innerHeight-280)}px`;el.showModal();setOpen(true);};
  return <><button ref={trigger} className={`context-chip ${className}`} aria-label={label} aria-expanded={open} onClick={show}><PilotIcon name={icon} small/>{summary&&<strong>{summary}</strong>}</button><dialog ref={dialog} className="menu-popover report-popover" aria-label={label} onCancel={(e)=>{e.preventDefault();close();}} onClick={(e)=>{if(e.target===e.currentTarget)close();}}><header className="menu-heading"><strong>{label}</strong></header><div className="menu-section">{children}</div></dialog></>;
}
