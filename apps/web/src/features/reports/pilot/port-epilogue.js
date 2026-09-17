// Source controls bind to explicit application actions. No fixture calculation
// or prototype storage participates in the report's result or saved identity.
let synchronizing=false;
function refreshData(){
 const model=bridge.model();
 const next=model.locale;
 if(locale!==next)applyLocale(next);
 const number=(value,digits=2)=>value==null?'—':new Intl.NumberFormat(locale,{maximumFractionDigits:digits,minimumFractionDigits:digits}).format(Number(value));
 metrics.forEach(metric=>{metric.value={ru:'—',en:'—'};metric.deltas={};metric.meta={ru:'Данные недоступны',en:'Data unavailable'};});
 const bindings=[['active','net_revenue','Выручка нетто','Net revenue'],['total','receipt_count','Чеки','Receipts'],['avg_receipt','average_receipt','Средний чек','Average receipt']];
 for(const [id,key,ru,en] of bindings){const metric=metrics.find(m=>m.id===id);metric.label={ru,en};const value=number(model.result?.totals[key],key==='receipt_count'?0:2);metric.value={ru:value,en:value};metric.meta={ru:key==='receipt_count'?'Чеки':'EUR',en:key==='receipt_count'?'Receipts':'EUR'};}
 renderKpis();if(model.result)document.getElementById('kpi-context').textContent=String(model.result.parameters.period.starts_on).slice(0,4)+' · EUR';renderOverviewTable();renderLifecycleTable();
 const title=document.querySelector('.title-row h1');title.removeAttribute('data-ru');title.removeAttribute('data-en');if(document.activeElement!==title)title.textContent=model.title;
 title.contentEditable=String(!model.preview&&!model.busy);title.setAttribute('role','textbox');title.setAttribute('aria-label',locale==='ru'?'Название отчёта':'Report title');
 const status=document.querySelector('.status-pill');status.removeAttribute('data-ru');status.removeAttribute('data-en');status.textContent=model.status;
 const texts=[['#page-overview .page-intro h2',locale==='ru'?'Продажи по чекам':'Receipt sales'],['#page-overview .page-intro p',bridge.range()+' · EUR · UTC'],['#overview-visual-panel h3',locale==='ru'?'Выручка по дням':'Daily net revenue'],['#overview-subtitle','EUR · UTC'],['#lifecycle-subtitle','EUR · UTC'],['#lifecycle-panel h3',locale==='ru'?'Данные по дням':'Daily data']];
 for(const [selector,value] of texts){const n=document.querySelector(selector);n.removeAttribute('data-ru');n.removeAttribute('data-en');n.textContent=value;}
 document.querySelectorAll('#trust-dialog .dialog-body,#inspector-panel-trust .drawer-section').forEach(n=>{n.innerHTML=bridge.trust(locale);});
 document.querySelector('#trust-dialog .dialog-header p').textContent=model.title;document.getElementById('dataset-select').innerHTML=`<option>${escapeText(model.source)}</option>`;document.getElementById('dataset-select').disabled=true;
 document.querySelectorAll('#page-findings .narrative p,#page-findings .narrative li,#page-findings .narrative h3,#context-source,#context-author').forEach(n=>{n.textContent=unavailable();});
 document.querySelectorAll('[data-chart-export],[data-table-export],#share-open,#copy-link,#advanced-condition-add,#advanced-group-add,#advanced-filter-search,#advanced-filter-logic,[data-filter-category],[data-group-add],[data-group-remove],#lifecycle-metric').forEach(n=>{n.disabled=true;n.title=unavailable();});
 document.querySelectorAll('[data-quick-comparison],input[name=comparison]').forEach(n=>{n.disabled=!['2024','prior-year'].includes(n.value);n.title=n.disabled?unavailable():'';});
 const save=document.getElementById('save-analysis-view');save.disabled=model.busy||model.unapplied||model.preview||model.conflict;save.querySelector('span').textContent=locale==='ru'?'Сохранить':'Save';
 document.getElementById('context-apply').disabled=model.busy||model.preview;document.getElementById('kpi-save').disabled=true;document.getElementById('kpi-save').title=unavailable();const viewLabel=document.querySelector('#view-popover > .menu-row.is-selected span');if(viewLabel)viewLabel.textContent=locale==='ru'?'Предпросмотр черновика':'Draft preview';focusRegistry.overview.title[locale]=locale==='ru'?'Focus · Выручка по дням':'Focus · Daily net revenue';document.getElementById('focus-context').textContent=model.title+' · '+bridge.range()+' · EUR';
 document.getElementById('saved-view-status').textContent=model.error||'';document.getElementById('saved-view-status').setAttribute('role',model.error?'alert':'status');document.querySelector('#overview-visual-panel .chart-summary').textContent=model.result?.totals.receipt_count===null?(locale==='ru'?'В этом периоде нет подходящих чеков.':'No eligible receipts in this period.'):(locale==='ru'?'Данные рассчитаны сервером · EUR · UTC':'Server-calculated data · EUR · UTC');
 document.getElementById('applied-filter-state').textContent=model.error||model.hint;
 document.getElementById('context-reset').textContent=model.conflict?(locale==='ru'?'Загрузить сохранённый':'Reload saved draft'):(locale==='ru'?'Сбросить':'Reset');
 document.querySelectorAll('.avatar').forEach(n=>{n.textContent='AN';});
 document.querySelectorAll('#comments-open [aria-hidden=true]:not(svg)').forEach(n=>{n.textContent='0';});
 document.querySelectorAll('#inspector-panel-discussion .drawer-label').forEach(n=>{n.textContent=unavailable();});document.querySelectorAll('.comment,.comment-item').forEach(n=>{n.textContent=unavailable();});
 updateAllCharts();
}
function enforceCapabilities(){
 document.querySelectorAll('#filters-popover input,#filters-popover [data-filter-value],#groupby-popover button,#context-filters input,#context-filters select,#context-filters button,[data-chart-type]:not([data-chart-type="trend"]),#insight-menu-toggle,#lifecycle-period-command button,#lifecycle-comparison-command button,#lifecycle-values-command button').forEach(n=>{n.disabled=true;n.title=unavailable();});
}
const capabilityObserver=new MutationObserver(enforceCapabilities);capabilityObserver.observe(document.body,{childList:true,subtree:true});enforceCapabilities();
const actions=(event)=>{
 const target=event.target.closest('button,a,summary');if(!target)return;
 if(target.matches('[data-nav-destination=sales],[data-nav-destination=reports-export]')){event.preventDefault();event.stopImmediatePropagation();bridge.library();}
 if(target.matches('#context-apply')){event.preventDefault();event.stopImmediatePropagation();closeContext();bridge.apply({period:reportPeriod,store:[...selectedStores][0]||'',comparison:selectedComparisons.size?'previous_year_same_dates':'none'});}
 if(target.matches('#published-analysis-view-row')){event.preventDefault();event.stopImmediatePropagation();bridge.preview();}
 if(target.matches('#context-reset')&&bridge.model().conflict){event.preventDefault();event.stopImmediatePropagation();bridge.reload();}
 if(target.matches('[data-chart-export],[data-table-export],#share-open')){event.preventDefault();event.stopImmediatePropagation();showToast(unavailable());}
};
document.addEventListener('click',actions,true);
document.getElementById('locale-toggle').addEventListener('click',()=>{bridge.locale(locale);refreshData();});
document.querySelector('.title-row h1').addEventListener('input',event=>bridge.title(event.target.textContent));
const stores=document.getElementById('stores-popover');
const choices=stores.querySelectorAll('[data-store-option]');
const prototype=choices[0]?.closest('label');
const holder=prototype?.parentElement;
if(holder&&prototype){const template=prototype.cloneNode(true);choices.forEach(n=>n.closest('label')?.remove());for(const store of bridge.model().stores){const row=template.cloneNode(true);const input=row.querySelector('input');input.value=store.id;input.checked=false;input.type='radio';input.name='real-store';const label=row.querySelector('span');if(label)label.textContent=store.label;storeMeta[store.id]={ru:store.label,en:store.label};input.addEventListener('change',()=>{selectedStores=new Set([store.id]);document.getElementById('all-stores').checked=false;updateReportStateUi();});holder.append(row);}}
selectedComparisons=new Set(bridge.model().comparison==='none'?[]:['2024']);primaryComparison=selectedComparisons.size?'2024':null;
reportPeriod={grain:'year',value:bridge.model().start.slice(0,4)};selectedStores=new Set(bridge.model().store?[bridge.model().store]:[]);
groupDimensions=[];syncLegacyGroupBy();
updateContextSummary();refreshData();
let inputIdentity=JSON.stringify([reportPeriod,[...selectedStores],[...selectedComparisons]]);
const onDraft=()=>queueMicrotask(()=>{const key=JSON.stringify([reportPeriod,[...selectedStores],[...selectedComparisons]]);if(key===inputIdentity)return;inputIdentity=key;bridge.draft({period:reportPeriod,store:[...selectedStores][0]||'',comparison:selectedComparisons.size?'previous_year_same_dates':'none'});});
document.addEventListener('change',onDraft);document.addEventListener('click',onDraft);
return {update(){if(synchronizing)return;synchronizing=true;try{refreshData();const wants=bridge.model().focus;if(wants!==Boolean(focusSourceFromUrl(location.searchParams.get('focus')))){if(wants)location.searchParams.set('focus',focusConfig().urlId);else {location.searchParams.delete('focus');pendingFocusRestore=true;}showFocusSurface();}}finally{synchronizing=false;}},dispose(){document.removeEventListener('click',actions,true);document.removeEventListener('change',onDraft);document.removeEventListener('click',onDraft);capabilityObserver.disconnect();chartResizeObserver?.disconnect();Object.values(chartInstances).forEach(c=>c.dispose());}};
