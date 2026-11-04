import {metricNumber,percentNumber} from './metric-number';
import type {configuredReports as W} from '@custometry/contracts';
import {aggregateYearChange,direction,signed} from './workspace-presentation';
import {workspaceReason} from './workspace-copy';
export function CardYearChange({binding,result,enabled,applied,loading,locale}:{binding?:W.CardResultBinding;result?:W.WorkspaceResultV2;enabled:boolean;applied:boolean;loading:boolean;locale:'ru'|'en'}){
 const ru=locale==='ru';const label=ru?'к году назад':'vs prior year';
 const state=!enabled?(ru?'Сравнение выключено':'YoY off'):!applied?(loading?(ru?'Обновляем сравнение…':'Updating comparison…'):''):loading&&!result?(ru?'Загрузка сравнения':'Loading YoY'):null;
 const change=state!==null?null:aggregateYearChange(binding,result);
 const reason=state??(change?.reason_codes.map(code=>workspaceReason(locale,code)).join('; ')||(!change?(ru?'Сравнение недоступно':'Comparison unavailable'):''));
 const delta=(value:string|null|undefined,percent=false)=><span className={'mw-change-'+direction(value)}>{percent?percentNumber(value,locale,true):metricNumber(value,locale,true)}</span>;
 const description=state??`${signed(change?.absolute_delta,locale,0)} · ${signed(change?.relative_delta_percent,locale,1)}${change?.relative_delta_percent!=null?'%':''} ${label}${reason?' · '+reason:''}`;
 const unavailable=change?.absolute_delta==null&&change?.relative_delta_percent==null;
 const brief=change?.reason_codes.includes('COVERAGE_INCOMPLETE')?(ru?'Недостаточно данных':'Insufficient data'):(ru?'Сравнение недоступно':'Comparison unavailable');
 const zeroBaseline=change?.reason_codes.includes('ZERO_BASELINE');
 return <div className="mw-card-yoy" aria-label={description} title={description}>{state!==null?<span>{state}</span>:unavailable?<span>{brief} · {label}</span>:<>{delta(change?.absolute_delta)}<span> · </span>{delta(change?.relative_delta_percent,true)}<small> {label}{zeroBaseline?(ru?' · база 0':' · baseline 0'):''}</small></>}</div>;
}
