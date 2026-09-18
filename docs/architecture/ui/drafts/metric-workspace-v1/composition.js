/* Local design prototype. All data and mutations are synthetic and in memory.
 * Production remains responsible for metric, comparison, permission and goal semantics.
 */
(() => {
  'use strict';
  const $ = (s, p = document) => p.querySelector(s);
  const esc = value => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const icon = name => `<svg class="icon icon--small" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const button = (action, label, name, cls = 'text-button') => `<button type="button" class="${cls}" data-action="${action}">${name ? icon(name) : ''}${label}</button>`;
  const clone = value => structuredClone(value);
  const catalog = {
    revenue: {name:'Выручка', unit:'€', note:'Сумма завершённых чеков', current:[1620,1740,1680,1960,2140,2090,2340,2410], previous:[1380,1450,1570,1680,1750,1840,2060,2150]},
    receipts: {name:'Количество чеков', unit:'чеков', note:'Завершённые чеки', current:[21400,22800,21900,24200,25700,25800,28100,29200], previous:[19000,19900,20600,21800,22400,23700,26400,27500]},
    average: {name:'Средний чек', unit:'€', note:'Выручка / количество чеков'}
  };
  const stores = {all:'Все магазины', center:'Центр', north:'Север', inherit:'Как в отчёте'};
  const months = ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг'];
  const initialSets = [
    {id:'sales',name:'Обзор продаж',scope:'Общий',cards:[{id:'r',metric:'revenue',store:'inherit'},{id:'n',metric:'receipts',store:'inherit'},{id:'a',metric:'average',store:'inherit'},{id:'c',metric:'revenue',store:'center',name:'Выручка · Центр'}]},
    {id:'stores',name:'Сравнение магазинов',scope:'Личный',cards:[{id:'sc',metric:'revenue',store:'center',name:'Выручка · Центр'},{id:'sn',metric:'revenue',store:'north',name:'Выручка · Север'},{id:'ac',metric:'average',store:'center',name:'Средний чек · Центр'}]}
  ];
  const state = {sets:clone(initialSets),set:'sales',primary:'r',secondary:'n',store:'all',period:'eight',mode:'period',delta:'connectors',view:'chart',panel:'set',open:innerWidth>1100,dirty:false,showPrevious:true,labels:false,focus:false,goals:[]};
  let saved = null, editCards = [], editingCard = null, chart = null, lastTrigger = null, toastTimer;
  const set = () => state.sets.find(s => s.id === state.set);
  const card = id => set().cards.find(c => c.id === id);
  const primary = () => card(state.primary) || set().cards[0];
  const secondary = () => card(state.secondary) || set().cards.find(c => c.id !== primary().id);
  const title = c => c.name || catalog[c.metric].name;
  const count = () => state.period === 'quarter' ? 3 : 8;
  const periodText = () => state.period === 'quarter' ? 'Янв — мар 2025' : 'Янв — авг 2025';
  const effective = c => c.store === 'inherit' ? state.store : state.store === 'all' || state.store === c.store ? c.store : null;
  const values = (c, previous = false) => {
    const store = effective(c);
    if (!store) return Array(count()).fill(null);
    const factor = store === 'center' ? .62 : store === 'north' ? .38 : 1;
    const key = previous ? 'previous' : 'current';
    return Array.from({length:count()}, (_, i) => c.metric === 'average'
      ? catalog.revenue[key][i] * 1000 / catalog.receipts[key][i]
      : catalog[c.metric][key][i] * (c.metric === 'revenue' ? 1000 : 1) * factor);
  };
  const sum = values => values.reduce((a,b) => a + b, 0);
  const total = (c, previous = false) => effective(c) === null ? null : c.metric === 'average'
    ? sum(values({...c,metric:'revenue'},previous)) / sum(values({...c,metric:'receipts'},previous)) : sum(values(c,previous));
  const number = (n, decimals = 0) => n === null ? '—' : new Intl.NumberFormat('ru-RU',{maximumFractionDigits:decimals,minimumFractionDigits:decimals}).format(n);
  const format = (n,c,compact=false) => n === null ? 'Нет данных' : compact && c.metric === 'revenue' ? `${number(n/1e6,2)} млн €` : `${number(n,c.metric === 'average'?2:0)}${c.metric==='receipts'?'':' €'}`;
  const delta = (a,b) => a === null || b === null || b === 0 ? null : (a-b)/Math.abs(b)*100;
  const deltaText = (a,b) => {const d=delta(a,b);return d===null?'Недоступно':`${d>0?'+':''}${number(d,1)} %`;};
  const localText = c => c.store === 'inherit' ? `Из отчёта · ${stores[state.store].toLowerCase()}` : `Свои фильтры · ${stores[c.store]}`;

  // Keep the actual pilot's CSS, SVG symbols, rail and header. Replace only the proposed document surfaces.
  const shell = $('.app-shell'), workspace = $('#workspace');
  for (const el of [...document.body.children]) if (el !== shell && el.tagName.toLowerCase() !== 'svg' && el.tagName !== 'SCRIPT') el.remove();
  for (const el of [...shell.children]) if (el !== workspace && !el.classList.contains('sidebar')) el.remove();
  for (const el of $('.sidebar').querySelectorAll('button')) {
    el.disabled = true;
    el.title = `${el.getAttribute('aria-label') || 'Раздел'} · вне этого драфта`;
    el.removeAttribute('aria-controls');
  }
  const header = $('.page-header').cloneNode(true);
  $('h1',header).textContent = 'Обзор продаж';
  $('.breadcrumb',header).textContent = 'Аналитика / Отчёты';
  const badge = $('.status-pill',header);badge.className='draft-badge';badge.textContent='Драфт · демоданные';
  $('.header-actions',header).innerHTML = button('reset','Сбросить',null) + button('save','Сохранить в макете','save') + `<button type="button" class="icon-button inspector-toggle" data-action="inspector" aria-label="Открыть инспектор отчёта">${icon('inspector-toggle')}</button>`;
  workspace.innerHTML = `<div class="workspace-chrome"></div><div class="report-scroll" id="report-scroll"><main class="report-main" id="report-main" tabindex="-1"></main></div><button class="draft-backdrop" data-action="close" aria-label="Закрыть инспектор"></button><aside class="context-drawer" aria-label="Инспектор отчёта"></aside>`;
  $('.workspace-chrome').append(header);
  $('.workspace-chrome').insertAdjacentHTML('beforeend', `<div class="draft-nav"><div class="report-tabs" aria-label="Страницы отчёта"><button class="report-tab" aria-current="page">Обзор</button><button class="report-tab" disabled title="Сегменты будут отдельным следующим функциональным блоком">Сегменты</button><button class="report-tab" data-action="notes">Заметки и методика</button></div><div class="draft-context"><button class="compact-control" data-action="context">${icon('calendar')}<span id="period-label"></span></button><button class="compact-control" data-action="context">${icon('store')}<span id="store-label"></span></button><button class="compact-control" data-action="context">${icon('filter')}Контекст отчёта</button></div></div>`);
  document.body.insertAdjacentHTML('beforeend','<div class="draft-toast" role="status" aria-live="polite" hidden></div>');

  function toast(text) { clearTimeout(toastTimer); $('.draft-toast').textContent=text;$('.draft-toast').hidden=false;toastTimer=setTimeout(()=>$('.draft-toast').hidden=true,4000); }
  function changed() {state.dirty=true;}
  function render() {
    chart?.dispose(); chart=null;
    $('#period-label').textContent=periodText();$('#store-label').textContent=stores[state.store];
    $('[data-action="save"]').innerHTML=icon('save')+(state.dirty?'Сохранить изменения':'Сохранить в макете');
    $('#report-main').innerHTML=`<div class="draft-intro"><div><h2>Метрики и динамика</h2><p>Один отчёт, несколько рабочих наборов. Выберите карточку для анализа.</p></div><span class="muted">${state.dirty?'Есть несохранённые изменения':saved?'Сохранено в этой вкладке':'Демонстрационный отчёт'}</span></div>
      <div class="workset-bar"><div class="workset-list" role="group" aria-label="Наборы метрик">${state.sets.map(s=>`<button class="workset-tab" data-set="${esc(s.id)}" aria-pressed="${state.set===s.id}">${esc(s.name)}</button>`).join('')}</div><button class="icon-button" data-action="copy" aria-label="Скопировать набор">${icon('plus')}</button>${button('catalog','Настроить набор','kpi')}</div>
      <div class="metric-rail" aria-label="Карточки метрик">${set().cards.map(c=>{const a=total(c),b=total(c,true);return `<article class="metric-card ${c.id===primary().id?'primary':state.mode==='pair'&&c.id===secondary()?.id?'secondary':''}"><button class="metric-select" data-card="${esc(c.id)}" aria-pressed="${c.id===primary().id||state.mode==='pair'&&c.id===secondary()?.id}"><span class="metric-name">${esc(title(c))}</span><strong class="metric-value">${format(a,c,true)}</strong><span class="metric-meta"><span class="${a>=b?'positive':'negative'}">${deltaText(a,b)}</span><span>к 2024</span></span><span class="metric-scope ${c.store==='inherit'?'':'local'}">${esc(localText(c))}</span></button><button class="icon-button metric-edit" data-edit="${esc(c.id)}" aria-label="Настроить ${esc(title(c))}">${icon('sliders')}</button></article>`;}).join('')}</div>
      <article class="panel draft-panel" id="analysis-panel"><header class="panel-header"><div><h3>${esc(title(primary()))}${state.mode==='pair'&&secondary()?` и ${esc(title(secondary()))}`:''}</h3><p>${periodText()} · по месяцам · ${state.mode==='pair'?'сравнение двух карточек':'сравнение с теми же месяцами 2024'}</p></div><div class="panel-actions"><div class="segmented" role="group" aria-label="Режим сравнения"><button data-mode="period" aria-pressed="${state.mode==='period'}">Периоды</button><button data-mode="pair" aria-pressed="${state.mode==='pair'}">Две метрики</button></div><div class="segmented" role="group" aria-label="Представление"><button data-view="chart" aria-pressed="${state.view==='chart'}">График</button><button data-view="table" aria-pressed="${state.view==='table'}">Таблица</button></div><button class="icon-button" data-action="chart" aria-label="Настроить график">${icon('chart-tune')}</button><button class="icon-button" data-action="focus" aria-label="${state.focus?'Закрыть Focus':'Развернуть график и таблицу'}">${icon(state.focus?'x':'expand')}</button></div></header>
      <div class="chart-body" ${state.view==='table'?'hidden':''}><div class="chart-context">${legend()}</div><div class="draft-chart" id="draft-chart" role="img" aria-label="Демонстрационная динамика; точные значения доступны в таблице"></div></div>
      <div class="chart-table-wrap" ${state.view==='chart'?'hidden':''}>${table()}</div><p class="chart-caption">${state.mode==='pair'?'Каждая линия сохраняет свою метрику, единицу и фильтры. Совпадение динамики не означает причинной связи.':state.delta==='trend'?'Прирост показан отдельной линией со шкалой процентов справа.':state.delta==='connectors'?'Соединители показывают относительное изменение в каждом месяце. Значения совпадают с таблицей.':'Выбраны значения без слоя прироста.'}</p></article>
      <div class="draft-support"><section class="support-block"><div class="support-heading"><h3>Цели набора <span class="muted">· пример</span></h3>${button('goal','Добавить цель','plus')}</div>${goals()}</section><section class="support-block"><div class="support-heading"><h3>Контекст результата</h3>${button('trust','Подробнее','shield')}</div><div class="trust-line">${icon('calendar')}<span>${periodText()} · завершённые чеки · EUR</span></div><div class="trust-line">${icon('filter')}<span>Общие фильтры наследуются. Собственные фильтры отмечены на каждой карточке.</span></div><div class="trust-line">${icon('eye')}<span>Все цифры в драфте синтетические. Данные рабочего сервиса здесь не используются.</span></div></section></div>
      <nav class="prototype-links" aria-label="Материалы драфта"><a href="../../target-pilot/ru/source.html" target="_blank">Исходный пилот ↗</a><a href="reference.html" target="_blank">Скриншоты-референсы ↗</a><button class="text-button" data-action="notes">Что изменится в реализации</button></nav>`;
    document.body.classList.toggle('draft-focus',state.focus);
    drawChart();renderInspector();
  }
  function legend() {
    const a=primary();let html=`<span><i class="legend-dot"></i>${esc(title(a))} · ${esc(stores[effective(a)]||'пустая выборка')}</span>`;
    if(state.mode==='pair'&&secondary())html+=`<span><i class="legend-dot secondary"></i>${esc(title(secondary()))} · ${esc(stores[effective(secondary())]||'пустая выборка')}</span>`;
    else {if(state.showPrevious)html+='<span><i class="legend-dot previous"></i>2024</span>';if(state.delta==='trend')html+='<span><i class="legend-dot delta"></i>Прирост, % · правая ось</span>';}
    return html;
  }
  function table() {
    const a=primary(),b=state.mode==='pair'?secondary():a,vs=values(a),bs=values(b||a,state.mode!=='pair');
    return `<table class="draft-table"><caption class="sr-only">Те же демонстрационные значения, что на графике</caption><thead><tr><th>Месяц</th><th>${esc(title(a))}, ${catalog[a.metric].unit}</th><th>${state.mode==='pair'?`${esc(title(b||a))}, ${catalog[(b||a).metric].unit}`:'2024'}</th>${state.mode==='period'?'<th>Разница</th><th>Прирост</th>':''}</tr></thead><tbody>${vs.map((v,i)=>`<tr><td>${months[i]}</td><td>${format(v,a)}</td><td>${format(bs[i],b||a)}</td>${state.mode==='period'?`<td>${v===null||bs[i]===null?'—':format(v-bs[i],a)}</td><td>${deltaText(v,bs[i])}</td>`:''}</tr>`).join('')}</tbody></table>`;
  }
  function drawChart() {
    if(state.view!=='chart')return;
    const el=$('#draft-chart'),a=primary(),b=secondary(),av=values(a),pv=values(a,true);
    if(av.every(v=>v===null)){el.innerHTML='<div class="draft-empty">Нет данных для этого пересечения<small>Общий фильтр отчёта и фильтр карточки выбирают разные магазины.</small></div>';return;}
    chart=echarts.init(el,null,{renderer:'svg'});
    const scale=(v,c)=>v===null?null:c.metric==='revenue'?v/1e6:c.metric==='receipts'?v/1000:v;
    const unit=c=>c.metric==='revenue'?'млн €':c.metric==='receipts'?'тыс. чеков':'€';
    const colors=['#65cce3','#81858d','#b6a3f5','#e9b981'];
    const yAxis=[{type:'value',name:unit(a),nameTextStyle:{color:'#a7a7ad',align:'left'},axisLabel:{color:'#8b8c93'},splitLine:{lineStyle:{color:'#292b30',type:'dashed'}}}];
    const line=(name,data,color,axis=0,dashed=false)=>({name,type:'line',data,yAxisIndex:axis,smooth:false,symbolSize:6,showSymbol:state.labels,lineStyle:{width:2,type:dashed?'dashed':'solid'},itemStyle:{color},label:{show:state.labels,color:'#c8c9ce',fontSize:10,formatter:p=>number(p.value,1)},emphasis:{focus:'series'}});
    const series=[line(`${title(a)} · 2025`,av.map(v=>scale(v,a)),colors[0])];
    if(state.mode==='pair'&&b){const separate=b.metric!==a.metric;
      if(separate)yAxis.push({type:'value',name:unit(b),position:'right',nameTextStyle:{color:colors[2],align:'right'},axisLabel:{color:colors[2]},splitLine:{show:false}});
      series.push(line(`${title(b)} · ${stores[effective(b)]||'нет данных'}`,values(b).map(v=>scale(v,b)),colors[2],separate?1:0));
    } else {
      if(state.showPrevious)series.push(line(`${title(a)} · 2024`,pv.map(v=>scale(v,a)),colors[1],0,true));
      if(state.delta==='connectors')series[0].markLine={silent:true,symbol:'none',animation:false,lineStyle:{type:'dashed',width:1,color:'#5d8f97'},label:{show:true,position:'middle',rotate:0,fontSize:10,color:'#9cddd0',backgroundColor:'#152027',padding:[3,4]},data:av.map((v,i)=>v===null||pv[i]===null?null:[{coord:[i,scale(pv[i],a)]},{coord:[i,scale(v,a)],label:{formatter:deltaText(v,pv[i])}}]).filter(Boolean)};
      if(state.delta==='trend'){yAxis.push({type:'value',name:'Прирост, %',position:'right',nameTextStyle:{color:colors[3],align:'right'},axisLabel:{color:colors[3],formatter:'{value} %'},splitLine:{show:false}});series.push(line('Прирост, %',av.map((v,i)=>delta(v,pv[i])),colors[3],1,true));}
    }
    chart.setOption({animation:false,textStyle:{fontFamily:'Inter, system-ui, sans-serif'},grid:{top:43,bottom:35,left:60,right:yAxis.length>1?75:25},tooltip:{trigger:'axis',backgroundColor:'#242529',borderColor:'#404249',textStyle:{color:'#f0f0f2',fontSize:12},formatter:params=>{const i=params[0].dataIndex;return `<strong>${months[i]} · демонстрация</strong><br>${esc(title(a))}: ${format(av[i],a)}<br>${state.mode==='pair'&&b?`${esc(title(b))}: ${format(values(b)[i],b)}`:`2024: ${format(pv[i],a)}<br>Разница: ${format(av[i]-pv[i],a)}<br>Прирост: ${deltaText(av[i],pv[i])}`}`;}},xAxis:{type:'category',boundaryGap:false,data:months.slice(0,count()),axisLine:{lineStyle:{color:'#393c42'}},axisTick:{show:false},axisLabel:{color:'#9699a1',margin:14}},yAxis,series});
  }
  function goals() {
    const list=state.goals.filter(g=>g.set===state.set);
    if(!list.length)return `<div class="goal-row"><div><strong>Выручка · 20 млн € за январь — август</strong><p>Пример размещения цели · все магазины · ответственный: аналитик</p></div><div class="goal-value">16 млн €<p>80 % от цели</p></div><div class="progress-track"><span style="width:80%"></span></div></div><p class="draft-notice">Цель привязана к собственной карточке и периоду. Это пример, не прогноз и не расчёт рабочего сервиса.</p>`;
    return list.map(g=>`<div class="goal-row"><div><strong>${esc(g.name)}</strong><p>${esc(g.period)} · ${esc(g.owner)} · ${esc(g.scope)}</p><p>${esc(g.hypothesis)}</p></div><div class="goal-value">${number(g.target)} ${esc(g.unit)}<p>Задан ориентир</p></div></div><p class="draft-notice">Сохранено только в макете. Фактический прогресс будет считать сервис.</p>`).join('');
  }
  function open(panel, trigger=null) {lastTrigger=trigger||document.activeElement;state.panel=panel;state.open=true;if(panel==='set')editCards=clone(set().cards);renderInspector();requestAnimationFrame(()=>$('#inspector-title')?.focus());}
  function close() {state.open=false;renderInspector();lastTrigger?.isConnected&&lastTrigger.focus();}
  const options=(items,value)=>Object.entries(items).map(([v,label])=>`<option value="${v}" ${v===value?'selected':''}>${esc(label)}</option>`).join('');
  function renderInspector() {
    workspace.dataset.context=state.open?'open':'closed';
    const drawer=$('.context-drawer');drawer.inert=!state.open;drawer.setAttribute('aria-hidden',String(!state.open));
    $('[data-action="inspector"]').setAttribute('aria-expanded',String(state.open));
    if(!state.open){requestAnimationFrame(()=>chart?.resize());return;}
    if(state.panel==='set'&&!editCards.length)editCards=clone(set().cards);
    drawer.innerHTML=`<header class="drawer-header"><div><h2 id="inspector-title" tabindex="-1">Инспектор отчёта</h2><p>Настройки выбранного набора</p></div><button class="icon-button" data-action="close" aria-label="Закрыть инспектор">${icon('x')}</button></header><nav class="draft-inspector-tabs" aria-label="Разделы инспектора">${[['set','Набор'],['card','Карточка'],['chart','График'],['goal','Цели']].map(([id,label])=>`<button data-panel="${id}" aria-pressed="${state.panel===id}">${label}</button>`).join('')}</nav><div class="draft-inspector-body">${panelContent()}</div><footer class="inspector-footer">${footer()}</footer>`;
    if(state.panel==='set')renderCatalog();
    requestAnimationFrame(()=>chart?.resize());
  }
  function panelContent() {
    if(state.panel==='set')return `<h3>${esc(set().name)}</h3><p>${set().scope} набор · порядок и настройки карточек сохраняются вместе.</p><input class="catalog-search" id="catalog-search" aria-label="Поиск метрики" placeholder="Найти метрику…"><div id="catalog-list"></div><div class="draft-notice">Одна метрика может появляться несколько раз с разными фильтрами. Стрелки меняют порядок карточек.</div>`;
    if(state.panel==='card'){
      const c=editingCard||primary();
      return `<h3>Настройка карточки</h3><p>Формула метрики общая. Фильтры и подпись принадлежат этой карточке.</p><div class="scope-box"><strong>${esc(catalog[c.metric].name)}</strong><br>${esc(catalog[c.metric].note)} · EUR</div><label class="draft-field">Подпись карточки<input id="card-name" value="${esc(title(c))}" maxlength="60"></label><h4>Фильтры карточки</h4><label class="draft-field">Магазин<select id="card-store">${options({inherit:'Как в отчёте',center:'Центр',north:'Север'},c.store)}</select><small>Свой фильтр сужает общий контекст отчёта.</small></label><div class="scope-box" id="effective-preview">${previewScope(c.store)}</div><label class="check-row"><input type="checkbox" id="bulk">Применить магазин ко всем карточкам набора</label><p id="bulk-preview" hidden>Будут изменены все ${set().cards.length} карточки. У всех трёх метрик есть фильтр магазина; несовместимых карточек нет.</p><p>«Применить» обновит текущий результат. «Сохранить в макете» отдельно запомнит конфигурацию в этой вкладке.</p>`;
    }
    if(state.panel==='chart')return `<h3>Сравнение и отображение</h3><p>${state.mode==='pair'?'Сопоставление двух карточек за один период.':'Одна карточка в текущем и предыдущем годах.'}</p><label class="draft-field">Режим<select id="chart-mode">${options({period:'Одна метрика · два периода',pair:'Две метрики · один период'},state.mode)}</select></label><div id="chart-period-fields" ${state.mode==='pair'?'hidden':''}><label class="check-row"><input type="checkbox" id="previous" ${state.showPrevious?'checked':''}>Показать линию 2024 года</label><label class="draft-field">Прирост<select id="delta-style">${options({connectors:'Разница между точками',trend:'Динамика прироста',off:'Не показывать'},state.delta)}</select><small>Для этого денежного показателя прирост — относительный, в %. Для долей потребуется отдельный выбор % / п. п.</small></label></div><div id="chart-pair-fields" ${state.mode!=='pair'?'hidden':''}><label class="draft-field">Вторая карточка<select id="second-card">${set().cards.filter(c=>c.id!==primary().id).map(c=>`<option value="${esc(c.id)}" ${c.id===secondary()?.id?'selected':''}>${esc(title(c))} · ${stores[c.store]}</option>`).join('')}</select></label><div class="scope-box">Одинаковая метрика — общая шкала. Разные метрики — подписанные левая и правая шкалы. Период и шаг времени совпадают.</div></div><label class="check-row"><input type="checkbox" id="labels" ${state.labels?'checked':''}>Подписать значения на линиях</label>`;
    if(state.panel==='context')return `<h3>Общий контекст отчёта</h3><p>Период и фильтры применяются ко всем карточкам, включая карточки со своей настройкой магазина.</p><label class="draft-field">Период<select id="report-period">${options({eight:'Январь — август 2025',quarter:'Январь — март 2025'},state.period)}</select></label><label class="draft-field">Магазины<select id="report-store">${options({all:'Все магазины',center:'Центр',north:'Север'},state.store)}</select></label><div class="scope-box">Сравнение: те же месяцы 2024 года.<br>Детализация: месяц.<br>Выборка: завершённые чеки в EUR.</div><p>Если общий и локальный фильтры выбирают разные магазины, карточка покажет пустое пересечение, а не нулевую выручку.</p>`;
    if(state.panel==='copy')return `<h3>Копия набора</h3><p>Карточки, их порядок и фильтры будут скопированы. Исходный набор сохранится.</p><label class="draft-field">Название<input id="copy-name" maxlength="60" value="${esc(set().name)} · копия"></label><label class="draft-field">Видимость<select id="copy-scope"><option value="Личный">Личный набор</option><option value="Общий">Общий набор рабочего пространства</option></select><small>В макете можно оценить оба варианта. Проверка прав будет на сервере.</small></label>`;
    if(state.panel==='goal')return `<h3>Новая цель</h3><p>Ориентир для конкретной карточки. Период цели не меняется при переключении периода отчёта.</p><label class="draft-field">Карточка<select id="goal-card">${set().cards.map(c=>`<option value="${esc(c.id)}">${esc(title(c))} · ${stores[c.store]}</option>`).join('')}</select></label><div class="scope-box">Пример правила: достичь значения не ниже заданного. В этой форме — цель по сумме выручки или числу чеков за период.</div><label class="draft-field">Целевое значение<input id="goal-target" type="number" min="1" step="1" value="20000000" required></label><div class="field-pair"><label class="draft-field">С<input type="date" id="goal-from" value="2025-01-01" required></label><label class="draft-field">По<input type="date" id="goal-to" value="2025-08-31" required></label></div><label class="draft-field">Ответственный<input id="goal-owner" value="Аналитик" maxlength="60" required></label><label class="draft-field">Видимость<select id="goal-scope"><option>Личная</option><option>Рабочее пространство</option></select></label><label class="draft-field">Гипотеза достижения<textarea id="goal-hypothesis" maxlength="400" placeholder="За счёт чего планируем достичь цели?"></textarea></label><p id="goal-error" role="alert"></p>`;
    if(state.panel==='notes')return `<h3>Что меняется</h3><h4>Сохраняем</h4><p>Оболочку пилота, навигацию, плотность, график / таблицу, Focus и правый инспектор. Текущий рабочий отчёт остаётся основой.</p><h4>Перерабатываем один раз</h4><p>Фиксированные KPI превращаем в настроенные карточки. Общие и локальные фильтры разделяем. Состояние отчёта расширяем наборами и сравнениями до финальной полировки.</p><h4>Добавляем</h4><p>Наборы, каталог карточек, сравнение двух метрик, прирост по точкам и цели. Сегменты затем подключаются как отдельный объект фильтрации, а не новый вариант этого экрана.</p><h4>Граница драфта</h4><p>Только локальная композиция на синтетических данных. Сохранение действует до перезагрузки страницы. Backend, права и формулы целей здесь не реализованы.</p>`;
    return `<h3>Доверие к результату</h3><div class="scope-box warning">Демонстрационные данные · не результат рабочего сервиса</div><p>Для драфта использованы три типа метрик первого отчёта: выручка, количество чеков, средний чек. Временные ряды придуманы для проверки композиции.</p><p>В реализации карточки будут ссылаться на зарегистрированные версии метрик, результаты — на реальные артефакты. Прирост, итог и прогресс цели рассчитывает сервис.</p><p>Скриншоты Mindbox используются как образец взаимодействий. Их финансовые данные не перенесены в макет.</p>`;
  }
  function previewScope(store) {const c={...primary(),store},s=effective(c);return `<strong>Итоговый контекст</strong><br>Отчёт: ${stores[state.store]}<br>Карточка: ${stores[store]}<br>${s===null?'Пустое пересечение — данных не будет':`Выборка: ${stores[s]} · ${periodText()}`}`;}
  function footer() {return ['notes','trust'].includes(state.panel)?button('close','Понятно',null,'text-button text-button--primary'):button('cancel','Отмена',null)+button('apply',state.panel==='copy'?'Создать копию':state.panel==='goal'?'Добавить в макет':'Применить',null,'text-button text-button--primary');}
  function renderCatalog() {
    const q=($('#catalog-search')?.value||'').toLocaleLowerCase('ru');
    $('#catalog-list').innerHTML=`<h4>В наборе · ${editCards.length}</h4>${editCards.map((c,i)=>`<div class="catalog-row"><span class="row-label">${esc(title(c))}<small>${stores[c.store]}</small></span><button class="icon-button" data-order="${i}" data-step="-1" aria-label="Выше: ${esc(title(c))}" ${i===0?'disabled':''}>↑</button><button class="icon-button" data-order="${i}" data-step="1" aria-label="Ниже: ${esc(title(c))}" ${i===editCards.length-1?'disabled':''}>↓</button><button class="icon-button" data-remove="${i}" aria-label="Удалить: ${esc(title(c))}" ${editCards.length===1?'disabled':''}>${icon('x')}</button></div>`).join('')}<h4>Каталог метрик</h4>${Object.entries(catalog).filter(([,m])=>m.name.toLocaleLowerCase('ru').includes(q)).map(([id,m])=>`<div class="catalog-row"><span class="row-label">${m.name}<small>${m.note}</small></span><button class="text-button" data-add="${id}">${icon('plus')}Добавить</button></div>`).join('')||'<p>Метрики не найдены. Попробуйте другое название.</p>'}`;
  }
  function apply() {
    switch(state.panel){
      case 'set': set().cards=clone(editCards);if(!card(state.primary))state.primary=set().cards[0].id;if(!card(state.secondary)||state.primary===state.secondary)state.secondary=set().cards.find(c=>c.id!==state.primary)?.id;if(set().cards.length<2)state.mode='period';break;
      case 'card': {const c=card((editingCard||primary()).id);c.name=$('#card-name').value.trim()||catalog[c.metric].name;c.store=$('#card-store').value;if($('#bulk').checked)set().cards.forEach(x=>x.store=c.store);editingCard=null;break;}
      case 'chart': state.mode=$('#chart-mode').value;state.delta=$('#delta-style').value;state.secondary=$('#second-card').value||state.secondary;state.showPrevious=$('#previous').checked;state.labels=$('#labels').checked;if(state.mode==='pair'&&!secondary()){toast('Добавьте ещё одну карточку в набор.');return;}break;
      case 'context':state.store=$('#report-store').value;state.period=$('#report-period').value;break;
      case 'copy':{const name=$('#copy-name').value.trim();if(!name){$('#copy-name').setCustomValidity('Введите название набора');$('#copy-name').reportValidity();return;}const s=clone(set());s.id=`set-${Date.now()}`;s.name=name;s.scope=$('#copy-scope').value;state.sets.push(s);state.set=s.id;break;}
      case 'goal':{const c=card($('#goal-card').value),target=Number($('#goal-target').value),from=$('#goal-from').value,to=$('#goal-to').value,owner=$('#goal-owner').value.trim();if(c.metric==='average'){$('#goal-error').textContent='Цель для среднего чека требует отдельного правила агрегации. В этом примере выберите выручку или количество чеков.';return;}if(!Number.isFinite(target)||target<=0||!from||!to||from>to||!owner){$('#goal-error').textContent='Укажите положительную цель, ответственного и период с началом не позже окончания.';return;}state.goals.push({set:state.set,name:title(c),target,unit:catalog[c.metric].unit,period:`${from} — ${to}`,owner,scope:$('#goal-scope').value,hypothesis:$('#goal-hypothesis').value.trim()});break;}
    }
    changed();render();toast(state.panel==='goal'?'Цель добавлена в макет. Серверный прогресс ещё не рассчитывается.':'Применено к текущему отчёту. Сохранение — отдельное действие.');
  }
  document.addEventListener('click',e=>{
    const b=e.target.closest('button');if(!b||b.disabled)return;
    if(b.dataset.set){state.set=b.dataset.set;state.primary=set().cards[0].id;state.secondary=set().cards[1]?.id;editingCard=null;editCards=clone(set().cards);state.mode='period';render();return;}
    if(b.dataset.card){if(state.mode==='pair'&&b.dataset.card!==state.primary)state.secondary=b.dataset.card;else {state.primary=b.dataset.card;if(state.secondary===state.primary)state.secondary=set().cards.find(c=>c.id!==state.primary)?.id;}editingCard=null;render();return;}
    if(b.dataset.edit){editingCard=clone(card(b.dataset.edit));open('card',b);return;}
    if(b.dataset.panel){if(b.dataset.panel==='card')editingCard=clone(primary());open(b.dataset.panel,b);return;}
    if(b.dataset.mode){if(b.dataset.mode==='pair'&&set().cards.length<2){toast('Добавьте вторую карточку через настройки набора.');return;}state.mode=b.dataset.mode;render();open('chart');return;}
    if(b.dataset.view){state.view=b.dataset.view;render();return;}
    if(b.dataset.add){editCards.push({id:`card-${Date.now()}`,metric:b.dataset.add,store:'inherit'});renderCatalog();return;}
    if(b.dataset.remove!==undefined){editCards.splice(Number(b.dataset.remove),1);renderCatalog();return;}
    if(b.dataset.order!==undefined){const i=Number(b.dataset.order),j=i+Number(b.dataset.step);[editCards[i],editCards[j]]=[editCards[j],editCards[i]];renderCatalog();$(`[data-order="${j}"][data-step="${b.dataset.step}"]`)?.focus();return;}
    switch(b.dataset.action){
      case 'catalog':open('set',b);break;
      case 'chart':case 'context':case 'copy':case 'goal':case 'notes':case 'trust':open(b.dataset.action,b);break;
      case 'inspector':state.open?close():open(state.panel,b);break;
      case 'close':case 'cancel':editingCard=null;editCards=clone(set().cards);close();break;
      case 'apply':apply();break;
      case 'save':saved=clone({sets:state.sets,store:state.store,period:state.period,goals:state.goals,mode:state.mode,delta:state.delta});state.dirty=false;render();toast('Конфигурация сохранена в памяти этой вкладки. После перезагрузки драфт сбросится.');break;
      case 'reset':state.sets=clone(initialSets);state.set='sales';state.primary='r';state.secondary='n';state.store='all';state.period='eight';state.mode='period';state.delta='connectors';state.view='chart';state.dirty=false;state.goals=[];editingCard=null;editCards=[];saved=null;state.panel='set';render();toast('Драфт возвращён к исходному состоянию.');break;
      case 'focus':state.focus=!state.focus;render();requestAnimationFrame(()=>$('[data-action="focus"]').focus());break;
    }
  });
  document.addEventListener('input',e=>{if(e.target.id==='catalog-search')renderCatalog();if(e.target.id==='copy-name')e.target.setCustomValidity('');});
  document.addEventListener('change',e=>{
    if(e.target.id==='card-store')$('#effective-preview').innerHTML=previewScope(e.target.value);
    if(e.target.id==='bulk')$('#bulk-preview').hidden=!e.target.checked;
    if(e.target.id==='chart-mode'){$('#chart-period-fields').hidden=e.target.value==='pair';$('#chart-pair-fields').hidden=e.target.value!=='pair';}
  });
  document.addEventListener('keydown',e=>{
    document.documentElement.dataset.inputModality='keyboard';
    if(e.key==='Escape'){if(state.focus){state.focus=false;render();$('[data-action="focus"]').focus();}else if(state.open)close();}
    if(e.key==='Tab'&&(state.focus||state.open&&innerWidth<=820)){
      const root=state.focus?$('#analysis-panel'):$('.context-drawer');const controls=[...root.querySelectorAll('button,input,select,textarea,a[href]')].filter(x=>!x.disabled&&x.getClientRects().length);const first=controls[0],last=controls.at(-1);
      if(e.shiftKey&&(document.activeElement===first||!root.contains(document.activeElement))){e.preventDefault();last.focus();}else if(!e.shiftKey&&(document.activeElement===last||!root.contains(document.activeElement))){e.preventDefault();first.focus();}
    }
  });
  document.addEventListener('pointerdown',()=>document.documentElement.dataset.inputModality='pointer');
  addEventListener('resize',()=>chart?.resize());
  render();
})();
