import type {configuredReports as W} from '@custometry/contracts';

/** Temporal comparison applies to the selected card; pair selection is separate. */
export function ReportComparisonControl({selection,disabled,locale,none,prior,onChange}:{selection:W.SingleSelection;disabled:boolean;locale:'ru'|'en';none:string;prior:string;onChange:(selection:W.SingleSelection)=>void}){
 return <label>{locale==='ru'?'Сравнение карточки':'Card comparison'}<select disabled={disabled} value={selection.temporal} onChange={event=>{
  const temporal=event.target.value as W.SingleSelection['temporal'];
  onChange({...selection,temporal,display:temporal==='none'?'series':selection.display});
 }}><option value="none">{none}</option><option value="previous_year_same_dates">{prior}</option></select></label>;
}
