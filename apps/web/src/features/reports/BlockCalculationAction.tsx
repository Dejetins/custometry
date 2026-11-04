type Props={location:'header'|'menu';ready:boolean;failed:boolean;loading:boolean;preview:boolean;disabled:boolean;locale:'ru'|'en';run:()=>void};
export function BlockCalculationAction(p:Props){
 const needed=!p.ready||p.failed||p.loading;
 if(p.preview&&!p.failed||p.location==='header'&&!needed||p.location==='menu'&&(needed||p.preview))return null;
 const ru=p.locale==='ru';
 const label=p.loading?(ru?'Расчёт…':'Calculating…'):p.failed?(ru?'Повторить':'Retry'):p.ready?(ru?'Пересчитать':'Recalculate'):(ru?'Рассчитать':'Calculate');
 return <button disabled={p.loading||p.disabled} onClick={p.run}>{label}</button>;
}
