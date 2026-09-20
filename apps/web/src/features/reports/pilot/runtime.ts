// @ts-nocheck
// Generated from the preserved pilot b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700; run scripts/generate-pilot.mjs.
export function mountPilot(document, window, bridge, echarts) {
window.echarts=echarts;
let innerWidth=window.innerWidth,innerHeight=window.innerHeight;window.addEventListener('resize',()=>{innerWidth=window.innerWidth;innerHeight=window.innerHeight;});
// Browser globals belong to the isolated source document, never the application shell.
const requestAnimationFrame=window.requestAnimationFrame.bind(window);
const cancelAnimationFrame=window.cancelAnimationFrame.bind(window);
const setTimeout=window.setTimeout.bind(window);
const clearTimeout=window.clearTimeout.bind(window);
const addEventListener=window.addEventListener.bind(window);
const navigator=window.navigator;
const Element=window.Element;
const HTMLElement=window.HTMLElement;
const location=new URL(bridge.url());
const history={state:null,pushState(state,_,href){this.state=state;location.href=new URL(href,location).href;bridge.urlChanged(location.href);},replaceState(state,_,href){this.state=state;location.href=new URL(href,location).href;bridge.urlChanged(location.href);},back(){location.searchParams.delete('focus');location.searchParams.delete('focus-section');bridge.urlChanged(location.href);showFocusSurface();}};
// Pilot preferences are presentation only and deliberately disappear on unmount.
const preferences=new Map();
const localStorage={getItem:key=>preferences.get(key)??null,setItem:(key,value)=>preferences.set(key,value),removeItem:key=>preferences.delete(key)};
const unavailable=()=>locale==='ru'?'Данные недоступны для этого источника':'Data unavailable for this source';
const escapeText=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const emptyOption=()=>({animation:false,title:{text:unavailable(),textStyle:{fontSize:11,color:'#999a9e'},left:'center',top:'center'},series:[]});
const unavailableTable=id=>{const node=document.getElementById(id);if(node)node.innerHTML=`<caption>${unavailable()}</caption>`;};
const realTable=()=>bridge.table(locale);


    const uiText = {
      ru: {
        current: '2025 · факт', plan: 'План 2025', onlyActual: 'Только факт', selected: (count, total) => `Выбрано: ${count} из ${total}`, limit: 'Выберите хотя бы одну метрику.', saved: 'Личный KPI-вид сохранён для этого пользователя.', defaultStatus: 'Опубликованный default: 8 метрик', personal: 'Личный', collapse: 'Свернуть боковую панель', expand: 'Развернуть боковую панель', copied: 'Ссылка на immutable snapshot текущего report state скопирована.', copyFallback: 'Ссылка на snapshot подготовлена. Clipboard недоступен в этом preview.', applied: 'Контекст применён к пилотному представлению.', reset: 'Контекст возвращён к published default.', placeholder: 'Этот раздел показан в навигации, но не входит в текущий экран пилота.', tableExport: format => `Таблица сохранена в ${format.toUpperCase()}.`, imageExport: format => `График сохранён в ${format.toUpperCase()}.`, email: 'Preflight ссылки пройден. Реальная отправка в пилоте не выполняется.', up: 'Выше', down: 'Ниже', chartError: 'Apache ECharts не загрузился.', rows: 'строк', primary: 'Основное сравнение'
      },
      en: {
        current: '2025 · actual', plan: 'Plan 2025', onlyActual: 'Actual only', selected: (count, total) => `Selected: ${count} of ${total}`, limit: 'Select at least one metric.', saved: 'Personal KPI view saved for this user.', defaultStatus: 'Published default: 8 metrics', personal: 'Personal', collapse: 'Collapse sidebar', expand: 'Expand sidebar', copied: 'Immutable snapshot link for the current report state copied.', copyFallback: 'Snapshot link prepared. Clipboard is unavailable in this preview.', applied: 'Context applied to the pilot view.', reset: 'Context returned to the published default.', placeholder: 'This section is represented in navigation but is outside the current pilot screen.', tableExport: format => `Table saved as ${format.toUpperCase()}.`, imageExport: format => `Chart saved as ${format.toUpperCase()}.`, email: 'Link preflight passed. The pilot does not perform a real delivery.', up: 'Up', down: 'Down', chartError: 'Apache ECharts failed to load.', rows: 'rows', primary: 'Primary comparison'
      }
    };

    const comparisonMeta = {
      plan: { ru: 'План 2025', en: 'Plan 2025', color: '#d6aa62', lineType: 'dashed' },
      previous: { ru: 'Предыдущий период', en: 'Previous period', color: '#7fc6dc', lineType: 'dashed', sourceId: '2024' },
      '2024': { ru: '2024', en: '2024', color: '#9aa4ad', lineType: 'dashed' },
      '2023': { ru: '2023', en: '2023', color: '#9d8cc2', lineType: 'dotted' },
      '2022': { ru: '2022', en: '2022', color: '#74777d', lineType: 'dotted' }
    };

    const styleTemplates = {
      default: { label: { ru: 'Опубликованный · Graphite', en: 'Published · Graphite' }, fontScale: 1, background: '#111214', text: '#a7a7ad', muted: '#85868d', grid: '#25262a', axis: '#3a3b40', tooltip: '#242529', palette: ['#66b9d3', '#d6aa62', '#9aa4ad', '#9d8cc2', '#cf7a85', '#74777d'], heatmap: ['#1c2429', '#28536a', '#66b9d3', '#d7edf4'] },
      contrast: { label: { ru: 'Высокий контраст', en: 'High contrast' }, fontScale: 1.08, background: '#080a0c', text: '#f8fafc', muted: '#c4ced6', grid: '#46515b', axis: '#9eabb5', tooltip: '#14181c', palette: ['#72e4ff', '#ffd166', '#ff92b0', '#b8a1ff', '#8ce99a', '#ff9f68'], heatmap: ['#0a1015', '#006983', '#00b6dd', '#eafaff'] },
      presentation: { label: { ru: 'Презентация · крупный текст', en: 'Presentation · large type' }, fontScale: 1.25, background: '#101216', text: '#f2f5f7', muted: '#bdc7ce', grid: '#39434b', axis: '#87949e', tooltip: '#20252a', palette: ['#77d7f2', '#f4c66f', '#aeb9c2', '#b7a1df', '#ef94a2', '#8ca3ad'], heatmap: ['#172128', '#276479', '#77d7f2', '#e5f8fd'] },
      calm: { label: { ru: 'Спокойная палитра', en: 'Calm palette' }, fontScale: 1.04, background: '#111518', text: '#dce7eb', muted: '#9fb1b8', grid: '#29363b', axis: '#50636a', tooltip: '#1b2529', palette: ['#83bdc9', '#b7a77d', '#829ba3', '#9b93b4', '#bb8790', '#6f858b'], heatmap: ['#182326', '#34545b', '#83bdc9', '#deedf0'] }
    };

    const storeMeta = {
      central: { ru: 'Центральный', en: 'Central' },
      north: { ru: 'Северный', en: 'North' },
      online: { ru: 'Онлайн', en: 'Online' }
    };

    const quickFilterSpecs = {
      channels: { label: { ru: 'Каналы', en: 'Channels' }, all: { ru: 'Все каналы', en: 'All channels' }, values: { retail: { ru: 'Розница', en: 'Retail' }, ecommerce: { ru: 'E-commerce', en: 'E-commerce' } } },
      segments: { label: { ru: 'Сегмент клиента', en: 'Customer segment' }, all: { ru: 'Все сегменты', en: 'All segments' }, values: { high: { ru: 'Высокая ценность', en: 'High value' }, core: { ru: 'Ядро', en: 'Core' }, risk: { ru: 'Под риском', en: 'At risk' } } },
      categories: { label: { ru: 'Категория товара', en: 'Product category' }, all: { ru: 'Все категории', en: 'All categories' }, values: { grocery: { ru: 'Продукты', en: 'Grocery' }, home: { ru: 'Дом', en: 'Home' }, beauty: { ru: 'Красота', en: 'Beauty' } } },
      coverage: { label: { ru: 'Покрытие данных', en: 'Data coverage' }, all: { ru: 'Любое покрытие', en: 'Any coverage' }, values: { full: { ru: 'Полное', en: 'Full' }, partial: { ru: 'Частичное', en: 'Partial' } } }
    };

    const advancedFilterCatalog = {
      customer_segment: { group: { ru: 'Клиент', en: 'Customer' }, label: { ru: 'Сегмент клиента', en: 'Customer segment' }, type: 'enum', values: { high: { ru: 'Высокая ценность', en: 'High value' }, core: { ru: 'Ядро', en: 'Core' }, new: { ru: 'Новые', en: 'New' }, risk: { ru: 'Под риском', en: 'At risk' }, dormant: { ru: 'Спящие', en: 'Dormant' } } },
      lifecycle_state: { group: { ru: 'Клиент', en: 'Customer' }, label: { ru: 'Состояние жизненного цикла', en: 'Lifecycle state' }, type: 'enum', values: { active: { ru: 'Активный', en: 'Active' }, retained: { ru: 'Удержанный', en: 'Retained' }, reactivated: { ru: 'Реактивированный', en: 'Reactivated' }, churned: { ru: 'Ушедший', en: 'Churned' } } },
      loyalty_member: { group: { ru: 'Клиент', en: 'Customer' }, label: { ru: 'Участник программы лояльности', en: 'Loyalty member' }, type: 'boolean', values: { yes: { ru: 'Да', en: 'Yes' }, no: { ru: 'Нет', en: 'No' } } },
      city: { group: { ru: 'Клиент', en: 'Customer' }, label: { ru: 'Город', en: 'City' }, type: 'enum', values: { moscow: { ru: 'Москва', en: 'Moscow' }, spb: { ru: 'Санкт-Петербург', en: 'Saint Petersburg' }, kazan: { ru: 'Казань', en: 'Kazan' } } },
      order_amount: { group: { ru: 'Заказы', en: 'Orders' }, label: { ru: 'Сумма заказа', en: 'Order amount' }, type: 'number', defaultValue: 2000, nestedHint: { ru: 'Уточнение относится к тому же заказу: статус, магазин или товарная позиция.', en: 'Nested refinement applies to the same order: status, store or line item.' } },
      order_status: { group: { ru: 'Заказы', en: 'Orders' }, label: { ru: 'Статус заказа', en: 'Order status' }, type: 'enum', values: { paid: { ru: 'Оплачен', en: 'Paid' }, completed: { ru: 'Завершён', en: 'Completed' }, returned: { ru: 'Возврат', en: 'Returned' } }, nestedHint: { ru: 'Статус и дополнительные условия проверяются внутри одного заказа.', en: 'Status and refinements are evaluated inside the same order.' } },
      purchase_recency: { group: { ru: 'Заказы', en: 'Orders' }, label: { ru: 'Последняя покупка', en: 'Last purchase' }, type: 'date', values: { d30: { ru: 'За последние 30 дней', en: 'In the last 30 days' }, d90: { ru: 'За последние 90 дней', en: 'In the last 90 days' }, y1: { ru: 'За последний год', en: 'In the last year' } } },
      product_category: { group: { ru: 'Товары', en: 'Products' }, label: { ru: 'Категория товара', en: 'Product category' }, type: 'enum', values: { grocery: { ru: 'Продукты', en: 'Grocery' }, home: { ru: 'Дом', en: 'Home' }, beauty: { ru: 'Красота', en: 'Beauty' } }, nestedHint: { ru: 'Категория относится к позиции того же заказа.', en: 'Category applies to a line item in the same order.' } },
      channel: { group: { ru: 'Коммуникации', en: 'Communications' }, label: { ru: 'Канал', en: 'Channel' }, type: 'enum', values: { retail: { ru: 'Розница', en: 'Retail' }, ecommerce: { ru: 'E-commerce', en: 'E-commerce' }, marketplace: { ru: 'Маркетплейсы', en: 'Marketplaces' } } },
      email_valid: { group: { ru: 'Коммуникации', en: 'Communications' }, label: { ru: 'Email заполнен и валиден', en: 'Email is present and valid' }, type: 'boolean', values: { yes: { ru: 'Да', en: 'Yes' }, no: { ru: 'Нет', en: 'No' } } },
      data_coverage: { group: { ru: 'Качество данных', en: 'Data quality' }, label: { ru: 'Покрытие данных', en: 'Data coverage' }, type: 'enum', values: { full: { ru: 'Полное', en: 'Full' }, partial: { ru: 'Частичное', en: 'Partial' } } }
    };

    const advancedOperators = {
      enum: [{ id: 'is', ru: 'равно', en: 'is' }, { id: 'is_not', ru: 'не равно', en: 'is not' }],
      boolean: [{ id: 'is', ru: 'равно', en: 'is' }],
      number: [{ id: 'gte', ru: 'не меньше', en: 'at least' }, { id: 'lte', ru: 'не больше', en: 'at most' }, { id: 'eq', ru: 'равно', en: 'equals' }],
      date: [{ id: 'within', ru: 'в периоде', en: 'within' }, { id: 'not_within', ru: 'не в периоде', en: 'not within' }]
    };

    const lifecycleCategories = {
      ru: ['Активные', 'Новые', 'Удержанные', 'Реактивированные', 'Под риском', 'Ушедшие'],
      en: ['Active', 'New', 'Retained', 'Reactivated', 'At risk', 'Churned']
    };

    const lifecycleSeries = {"2022":[null,null,null,null,null,null],"2023":[null,null,null,null,null,null],"2024":[null,null,null,null,null,null],"current":[null,null,null,null,null,null],"plan":[null,null,null,null,null,null]};

    const lifecycleTotals = {"2022":null,"2023":null,"2024":null,"current":null,"plan":null};
    const lifecycleValue = ["—","—","—","—","—","—"];
    const lifecycleReceipt = ["—","—","—","—","—","—"];
    const lifecycleFrequency = ["—","—","—","—","—","—"];
    const lifecycleMetricSeries = {"revenue":{"2022":[null,null,null,null,null,null],"2023":[null,null,null,null,null,null],"2024":[null,null,null,null,null,null],"current":[null,null,null,null,null,null],"plan":[null,null,null,null,null,null]},"receipt":{"2022":[null,null,null,null,null,null],"2023":[null,null,null,null,null,null],"2024":[null,null,null,null,null,null],"current":[null,null,null,null,null,null],"plan":[null,null,null,null,null,null]},"frequency":{"2022":[null,null,null,null,null,null],"2023":[null,null,null,null,null,null],"2024":[null,null,null,null,null,null],"current":[null,null,null,null,null,null],"plan":[null,null,null,null,null,null]}};
    const lifecycleMetricMeta = {
      customers: { ru: 'Клиенты', en: 'Customers' },
      share: { ru: 'Доля', en: 'Share' },
      revenue: { ru: 'Выручка', en: 'Revenue' },
      receipt: { ru: 'Средний чек', en: 'Average receipt' },
      frequency: { ru: 'Частота', en: 'Frequency' }
    };
    const groupByMeta = {
      none: { ru: 'Без группировки', en: 'No breakdown' },
      channel: { ru: 'Канал', en: 'Channel' },
      segment: { ru: 'Сегмент', en: 'Segment' },
      channel_segment: { ru: 'Канал → сегмент', en: 'Channel → segment' },
      store: { ru: 'Магазин', en: 'Store' }
    };
    const groupDimensionCatalog = {
      channel: { label: { ru: 'Канал', en: 'Channel' }, hint: { ru: 'Розница, E-commerce, маркетплейсы', en: 'Retail, E-commerce, marketplaces' } },
      store: { label: { ru: 'Магазин', en: 'Store' }, hint: { ru: 'Выбранные торговые точки', en: 'Selected stores' } },
      segment: { label: { ru: 'Сегмент', en: 'Segment' }, hint: { ru: 'Сегменты клиентской базы', en: 'Customer base segments' } },
      category: { label: { ru: 'Категория товара', en: 'Product category' }, hint: { ru: 'Категория последней покупки', en: 'Last purchase category' } },
      city: { label: { ru: 'Город', en: 'City' }, hint: { ru: 'Город магазина или доставки', en: 'Store or delivery city' } },
      loyalty: { label: { ru: 'Уровень лояльности', en: 'Loyalty tier' }, hint: { ru: 'Gold, Silver, Base', en: 'Gold, Silver, Base' } }
    };

    const monthlyData = {"active":{"2022":[null,null,null,null,null,null,null,null,null,null,null,null],"2023":[null,null,null,null,null,null,null,null,null,null,null,null],"2024":[null,null,null,null,null,null,null,null,null,null,null,null],"label":{"ru":"Активные клиенты","en":"Active customers"},"unit":{"ru":"K","en":"K"},"decimals":null,"current":[null,null,null,null,null,null,null,null,null,null,null,null],"plan":[null,null,null,null,null,null,null,null,null,null,null,null]},"retention":{"2022":[null,null,null,null,null,null,null,null,null,null,null,null],"2023":[null,null,null,null,null,null,null,null,null,null,null,null],"2024":[null,null,null,null,null,null,null,null,null,null,null,null],"label":{"ru":"Удержание","en":"Retention"},"unit":{"ru":"%","en":"%"},"decimals":null,"current":[null,null,null,null,null,null,null,null,null,null,null,null],"plan":[null,null,null,null,null,null,null,null,null,null,null,null]},"new":{"2022":[null,null,null,null,null,null,null,null,null,null,null,null],"2023":[null,null,null,null,null,null,null,null,null,null,null,null],"2024":[null,null,null,null,null,null,null,null,null,null,null,null],"label":{"ru":"Новые клиенты","en":"New customers"},"unit":{"ru":"K","en":"K"},"decimals":null,"current":[null,null,null,null,null,null,null,null,null,null,null,null],"plan":[null,null,null,null,null,null,null,null,null,null,null,null]},"reactivated":{"2022":[null,null,null,null,null,null,null,null,null,null,null,null],"2023":[null,null,null,null,null,null,null,null,null,null,null,null],"2024":[null,null,null,null,null,null,null,null,null,null,null,null],"label":{"ru":"Реактивированные","en":"Reactivated"},"unit":{"ru":"K","en":"K"},"decimals":null,"current":[null,null,null,null,null,null,null,null,null,null,null,null],"plan":[null,null,null,null,null,null,null,null,null,null,null,null]}};

    const quarterData = {"retained":[null,null,null,null],"new":[null,null,null,null],"reactivated":[null,null,null,null]};

    const segments = [{"id":"high","name":{"ru":"Высокая ценность","en":"High value"},"customers":null,"share":null,"receipt":null,"frequency":null,"retention":null,"color":"—"},{"id":"core","name":{"ru":"Ядро","en":"Core"},"customers":null,"share":null,"receipt":null,"frequency":null,"retention":null,"color":"—"},{"id":"new","name":{"ru":"Новые","en":"New"},"customers":null,"share":null,"receipt":null,"frequency":null,"retention":null,"color":"—"},{"id":"risk","name":{"ru":"Под риском","en":"At risk"},"customers":null,"share":null,"receipt":null,"frequency":null,"retention":null,"color":"—"},{"id":"dormant","name":{"ru":"Спящие","en":"Dormant"},"customers":null,"share":null,"receipt":null,"frequency":null,"retention":null,"color":"—"}];

    const migrationMatrix = [[null,null,null,null,null],[null,null,null,null,null],[null,null,null,null,null],[null,null,null,null,null],[null,null,null,null,null]];

    const metrics = [{"id":"active","label":{"ru":"Активные клиенты","en":"Active customers"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"total","label":{"ru":"Клиенты всего","en":"Total customers"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"retention","label":{"ru":"Удержание","en":"Retention"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"avg_receipt","label":{"ru":"Средний чек","en":"Average receipt"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"frequency","label":{"ru":"Частота клиентов","en":"Customer frequency"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"revenue_customer","label":{"ru":"Выручка на клиента","en":"Revenue per customer"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"new","label":{"ru":"Новые клиенты","en":"New customers"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"reactivated","label":{"ru":"Реактивированные","en":"Reactivated"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"at_risk","label":{"ru":"Под риском","en":"At risk"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"repeat","label":{"ru":"Повторные клиенты","en":"Repeat customers"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"churned","label":{"ru":"Ушедшие","en":"Churned"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}},{"id":"revenue","label":{"ru":"Выручка клиентов","en":"Customer revenue"},"value":{"ru":"—","en":"—"},"meta":{"ru":"Данные недоступны","en":"Data unavailable"},"deltas":{}}];

    const defaultMetricIds = ['active', 'total', 'retention', 'avg_receipt', 'frequency', 'revenue_customer', 'new', 'reactivated'];
    const storageKey = 'custometry.pilot-v2.personal-kpi.demo-user.r7';
    const navStorageKey = 'custometry.pilot-v2.sidebar-groups.demo-user.r7';
    const maxKpis = metrics.length;
    const shell = document.querySelector('.app-shell');
    const workspace = document.getElementById('workspace');
    const reportScroll = document.getElementById('report-scroll');
    const kpiStrip = document.getElementById('kpi-strip');
    const personalPill = document.getElementById('personal-view-pill');
    const metricPicker = document.getElementById('metric-picker');
    const kpiStatus = document.getElementById('kpi-status');
    const chartInstances = {};
    const chartLegendState = {};
    const chartLegendModels = {};
    const chartLegendBindings = new Set();
    const forcedExternalLegend = new Set();
    const legendMeasureCanvas = document.createElement('canvas');
    const observedChartElements = new WeakSet();
    const observedChartSurfaceWidths = new Map();
    let adaptiveSurfaceResizeFrame = 0;
    const chartResizeObserver = typeof ResizeObserver === 'function' ? new ResizeObserver(entries => {
      entries.forEach(entry => {
        const chart = chartInstances[entry.target.id];
        if (chart && entry.contentRect.width > 0 && entry.contentRect.height > 0) {
          chart.resize();
          const surfaceWidth = Math.round(entry.target.closest('.chart-stage')?.clientWidth || entry.contentRect.width);
          if (observedChartSurfaceWidths.get(entry.target.id) !== surfaceWidth) {
            observedChartSurfaceWidths.set(entry.target.id, surfaceWidth);
            cancelAnimationFrame(adaptiveSurfaceResizeFrame);
            adaptiveSurfaceResizeFrame = requestAnimationFrame(() => updateAllCharts());
          }
        }
      });
    }) : null;
    const pageScroll = {};
    let locale = 'ru';
    let currentPage = (location.hash || '#overview').slice(1);
    if (!['overview', 'dynamics', 'segments', 'findings'].includes(currentPage)) currentPage = 'overview';
    let selectedMetricIds = loadMetricIds();
    let draftMetricIds = [...selectedMetricIds];
    let primaryComparison = '2024';
    let selectedComparisons = new Set(['plan', '2024']);
    let overviewChartType = 'trend';
    let overviewChartTypeManual = false;
    let dynamicsChartType = 'line';
    let segmentsChartType = 'horizontal';
    let lifecycleMetric = 'customers';
    let lifecycleValueFormat = 'values';
    let lifecyclePercentBasis = 'parent';
    let lifecycleComparisonMode = 'none';
    let lifecycleDeltaDisplay = 'both';
    let lifecycleDeltaBase = null;
    let groupDimensions = ['channel', 'segment'];
    let groupBy = 'channel_segment';
    let focusSource = 'overview';
    let focusTrigger = null;
    let focusAnchor = 'chart';
    let pendingFocusRestore = false;
    let selectedStores = new Set();
    let reportPeriod = { grain: 'year', value: '2025' };
    const analyticalScopes = ['overview', 'lifecycle', 'dynamics', 'quarter', 'segments', 'migration'];
    const chartPeriodOverrides = Object.fromEntries(analyticalScopes.map(id => [id, { grain: 'inherit', comparison: 'inherit' }]));
    const chartGroupOverrides = Object.fromEntries(analyticalScopes.map(id => [id, 'inherit']));
    let reportStyleTemplate = 'default';
    const chartStyleOverrides = Object.fromEntries(analyticalScopes.map(id => [id, 'inherit']));
    const chartPaletteOverrides = Object.fromEntries(analyticalScopes.map(id => [id, 'inherit']));
    let reportPalette = 'graphite';
    const reportReadability = { size: 'default', values: 'default', labels: 'default', axes: 'default', table: 'default' };
    const dataPalettes = {
      graphite: ['#66b9d3', '#d6aa62', '#9aa4ad', '#9d8cc2', '#cf7a85', '#74777d'],
      ocean: ['#4dc4dd', '#277da1', '#90be6d', '#f9c74f', '#f9844a', '#8f9aa3'],
      warm: ['#e07a5f', '#f2cc8f', '#81b29a', '#a88bc3', '#d992b0', '#76848d'],
      vivid: ['#34d7eb', '#ffd166', '#ef476f', '#9b8cff', '#68d391', '#ff9f5a']
    };
    const analysisViewStorageKey = 'custometry.pilot-v2.personal-analysis-view.demo-user.r11';
    chartPeriodOverrides.overview.grain = 'month';
    chartPeriodOverrides.overview.comparison = 'none';
    chartPeriodOverrides.lifecycle.grain = 'month';
    chartGroupOverrides.overview = 'inherit';
    chartGroupOverrides.lifecycle = 'inherit';
    let quickFilters = { channels: null, segments: null, categories: null, coverage: null };
    let activeQuickFilter = 'segments';
    let advancedFilterLogic = 'and';
    let advancedGroups = [];
    let appliedAdvancedGroups = [];
    let personalAnalysisViewActive = false;

    function loadMetricIds() {
      try {
        const stored = JSON.parse(localStorage.getItem(storageKey));
        if (Array.isArray(stored) && stored.length && stored.length <= maxKpis && stored.every(id => metrics.some(metric => metric.id === id))) return stored;
      } catch (_) {}
      return [...defaultMetricIds];
    }

    function isPersonalView() { return JSON.stringify(selectedMetricIds) !== JSON.stringify(defaultMetricIds); }
    function defaultPeriodValue(grain) {
      if (grain === 'day') return '2025-12-31';
      if (grain === 'week') return '2025-W52';
      if (grain === 'month') return '2025-12';
      if (grain === 'quarter') return '2025-Q4';
      return '2025';
    }
    function periodParts(value = reportPeriod.value) {
      if (/^\d{4}$/.test(value)) return { year: Number(value), month: 12, day: 31, week: 52, quarter: 4 };
      if (/^\d{4}-W\d{2}$/.test(value)) { const [year, week] = value.split('-W').map(Number); return { year, month: Math.min(12, Math.ceil(week / 4.34)), day: 31, week, quarter: Math.min(4, Math.ceil(week / 13)) }; }
      if (/^\d{4}-Q[1-4]$/.test(value)) { const [year, quarter] = value.split('-Q').map(Number); return { year, month: quarter * 3, quarter }; }
      const [year, month, day = 28] = value.split('-').map(Number);
      return { year, month, day, week: Math.min(52, Math.max(1, Math.ceil(((month - 1) * 30.4 + day) / 7))), quarter: Math.ceil(month / 3) };
    }
    function effectiveChartPeriod(scope = null) {
      const grain = scope ? effectiveChartGrain(scope) : reportPeriod.grain;
      const parts = periodParts(reportPeriod.value);
      const value = grain === 'year' ? String(parts.year)
        : grain === 'quarter' ? `${parts.year}-Q${parts.quarter}`
        : grain === 'month' ? `${parts.year}-${String(parts.month).padStart(2, '0')}`
        : grain === 'week' ? `${parts.year}-W${String(parts.week || 52).padStart(2, '0')}`
        : `${parts.year}-${String(parts.month).padStart(2, '0')}-${String(parts.day || 28).padStart(2, '0')}`;
      return { grain, value, ...periodParts(value) };
    }
    function sourceForYear(year) { return Number(year) === 2025 ? 'current' : String(year); }
    function periodValueOptions(grain) {
      if (grain === 'day') return ['2025-12-31', '2025-12-30', '2025-12-29', '2025-12-28', '2025-12-27', '2025-12-26', '2025-12-25'];
      if (grain === 'week') return ['2025-W52', '2025-W51', '2025-W50', '2025-W49', '2025-W48', '2025-W47'];
      if (grain === 'month') return ['2025-12', '2025-11', '2025-10', '2025-09', '2025-08', '2025-07'];
      if (grain === 'quarter') return ['2025-Q4', '2025-Q3', '2025-Q2', '2025-Q1', '2024-Q4'];
      return ['2025', '2024', '2023', '2022'];
    }
    function periodValueLabel(value = reportPeriod.value, yearOffset = 0) {
      if (/^\d{4}$/.test(value)) return String(Number(value) - yearOffset);
      if (/^\d{4}-W\d{2}$/.test(value)) { const [year, week] = value.split('-W'); return `${locale === 'ru' ? 'Неделя' : 'Week'} ${Number(week)} · ${Number(year) - yearOffset}`; }
      if (/^\d{4}-Q[1-4]$/.test(value)) { const [year, quarter] = value.split('-'); return `${quarter} ${Number(year) - yearOffset}`; }
      const [year, month, day] = value.split('-');
      const monthIndex = Math.max(0, Number(month) - 1);
      const names = locale === 'ru' ? ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'] : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      if (day) return `${Number(day)} ${names[monthIndex].toLocaleLowerCase(localeCode())} ${Number(year) - yearOffset}`;
      return `${names[monthIndex]} ${Number(year) - yearOffset}`;
    }
    function previousPeriodLabel(grain = reportPeriod.grain, value = reportPeriod.value) {
      if (grain === 'year') return String(Number(value) - 1);
      if (grain === 'day') { const date = new Date(`${value}T12:00:00Z`); date.setUTCDate(date.getUTCDate() - 1); return periodValueLabel(date.toISOString().slice(0, 10)); }
      if (grain === 'week') { const [year, weekRaw] = value.split('-W'); const week = Number(weekRaw); return `${locale === 'ru' ? 'Неделя' : 'Week'} ${week > 1 ? week - 1 : 52} · ${week > 1 ? year : Number(year) - 1}`; }
      if (grain === 'quarter') { const [year, qRaw] = value.split('-Q'); const q = Number(qRaw); return q > 1 ? `Q${q - 1} ${year}` : `Q4 ${Number(year) - 1}`; }
      const [year, monthRaw] = value.split('-'); const month = Number(monthRaw); const prev = month > 1 ? month - 1 : 12; const prevYear = month > 1 ? Number(year) : Number(year) - 1;
      const names = locale === 'ru' ? ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'] : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return `${names[prev - 1]} ${prevYear}`;
    }
    function comparisonLabel(id, scope = null) {
      if (!id || !comparisonMeta[id]) return uiText[locale].onlyActual;
      const { grain, value } = effectiveChartPeriod(scope);
      if (id === 'previous') return previousPeriodLabel(grain, value);
      if (id === 'plan') return `${locale === 'ru' ? 'План' : 'Plan'} · ${periodValueLabel(value)}`;
      if (/^202[2-4]$/.test(id)) return periodValueLabel(value, 2025 - Number(id));
      return comparisonMeta[id][locale];
    }
    function currentLabel(scope = null) {
      const { value } = effectiveChartPeriod(scope);
      return `${periodValueLabel(value)} · ${locale === 'ru' ? 'факт' : 'actual'}`;
    }
    function seriesSourceId(id, scope = null) {
      const period = effectiveChartPeriod(scope);
      if (id === 'current') return sourceForYear(period.year);
      if (id === 'previous') return sourceForYear(period.year - (period.grain === 'year' ? 1 : 0));
      return comparisonMeta[id]?.sourceId || id;
    }
    function comparisonScale(id, scope) {
      if (id === 'plan') return 1.02;
      if (id === 'previous') return effectiveChartGrain(scope) === 'day' ? .996 : effectiveChartGrain(scope) === 'week' ? .992 : effectiveChartGrain(scope) === 'month' ? .985 : effectiveChartGrain(scope) === 'quarter' ? .96 : .92;
      return ({ '2024': .92, '2023': .86, '2022': .80 })[id] || 1;
    }
    function effectiveChartGrain(scope) { return chartPeriodOverrides[scope]?.grain === 'inherit' ? reportPeriod.grain : chartPeriodOverrides[scope]?.grain || reportPeriod.grain; }
    function dimensionsFromLegacy(value) {
      if (!value || value === 'none') return [];
      if (value === 'channel_segment') return ['channel', 'segment'];
      return value.split('_').filter(id => groupDimensionCatalog[id]);
    }
    function syncLegacyGroupBy() {
      groupBy = groupDimensions.length ? (groupDimensions.join('_') === 'channel_segment' ? 'channel_segment' : groupDimensions.join('_')) : 'none';
    }
    function groupingLabel(dimensions = groupDimensions) {
      if (!dimensions.length) return groupByMeta.none[locale];
      return dimensions.map(id => groupDimensionCatalog[id]?.label[locale] || id).join(' → ');
    }
    function effectiveGroupingDimensions(scope = null) {
      if (!scope || chartGroupOverrides[scope] === 'inherit') return [...groupDimensions];
      if (chartGroupOverrides[scope] === 'none') return [];
      return dimensionsFromLegacy(chartGroupOverrides[scope]);
    }
    function effectiveGroupBy(scope) {
      const dimensions = effectiveGroupingDimensions(scope);
      return dimensions.length ? dimensions.join('_') : 'none';
    }
    function effectiveStyleId(scope) { return chartStyleOverrides[scope] === 'inherit' ? reportStyleTemplate : chartStyleOverrides[scope] || reportStyleTemplate; }
    function styleTemplate(scope) { return styleTemplates[effectiveStyleId(scope)] || styleTemplates.default; }
    function dataPalette(scope) {
      const paletteId = chartPaletteOverrides[scope] === 'inherit' ? reportPalette : chartPaletteOverrides[scope];
      return dataPalettes[paletteId] || styleTemplate(scope).palette;
    }
    function seriesColor(scope, id, index = 0) {
      const palette = dataPalette(scope);
      if (id === 'current') return palette[0];
      if (id === 'plan') return palette[1];
      return palette[Math.min(index + 2, palette.length - 1)];
    }
    function chartComparisonIds(scope) {
      const mode = chartPeriodOverrides[scope]?.comparison || 'inherit';
      if (mode === 'none') return [];
      if (mode === 'previous') return ['previous'];
      if (mode === 'prior-year') return ['2024'];
      return getSelectedComparisonIds();
    }
    function chartTimeSummary(scope) {
      const ids = chartComparisonIds(scope);
      const comparison = ids.length ? ids.map(id => comparisonLabel(id, scope)).join(' · ') : uiText[locale].onlyActual;
      return `${currentLabel(scope)} · ${comparison}`;
    }
    function localeCode() { return locale === 'ru' ? 'ru-RU' : 'en-US'; }
    function formatInteger(value) { return new Intl.NumberFormat(localeCode(), { maximumFractionDigits: 0 }).format(value); }
    function formatSignedInteger(value) { return `${value > 0 ? '+' : value < 0 ? '−' : ''}${formatInteger(Math.abs(value))}`; }
    function formatSignedPct(value) { return `${value > 0 ? '+' : value < 0 ? '−' : ''}${Math.abs(value).toLocaleString(localeCode(), { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`; }
    function formatCompact(value) {
      if (value >= 1000000000) return `${(value / 1000000000).toLocaleString(localeCode(), { maximumFractionDigits: 1 })}MM`;
      if (value >= 1000000) return `${(value / 1000000).toLocaleString(localeCode(), { maximumFractionDigits: 1 })}M`;
      if (value >= 1000) return `${(value / 1000).toLocaleString(localeCode(), { maximumFractionDigits: 1 })}K`;
      return formatInteger(value);
    }
    function formatMetricValue(value, unit = '') {
      if (value == null) return '—';
      if (unit === '%') return `${value.toLocaleString(localeCode(), { maximumFractionDigits: 1 })}%`;
      if (unit === 'K') return `${value.toLocaleString(localeCode(), { maximumFractionDigits: 1 })}K`;
      return formatCompact(value);
    }

    function selectedPeriodIds() {
      const selected = new Set(['current', ...getSelectedComparisonIds()]);
      return ['2022', '2023', '2024', 'previous', 'plan', 'current'].filter(id => selected.has(id));
    }

    function periodLabel(id) { return id === 'current' ? currentLabel() : comparisonLabel(id); }

    function dimensionItems(dimension) {
      if (dimension === 'channel') return [
        { id: 'retail', label: locale === 'ru' ? 'Розница' : 'Retail', factor: .48 },
        { id: 'ecommerce', label: 'E-commerce', factor: .31 },
        { id: 'marketplaces', label: locale === 'ru' ? 'Маркетплейсы' : 'Marketplaces', factor: .21 }
      ];
      if (dimension === 'segment') return segments.map((segment, index) => ({ id: segment.id, label: segment.name[locale], factor: [.24, .28, .16, .14, .18][index] }));
      if (dimension === 'store') {
        const all = [
          { id: 'central', label: storeMeta.central[locale], factor: .42 },
          { id: 'north', label: storeMeta.north[locale], factor: .33 },
          { id: 'online', label: storeMeta.online[locale], factor: .25 }
        ];
        return selectedStores.size ? all.filter(item => selectedStores.has(item.id)) : all;
      }
      if (dimension === 'category') return [
        { id: 'fashion', label: locale === 'ru' ? 'Одежда' : 'Fashion', factor: .39 },
        { id: 'home', label: locale === 'ru' ? 'Дом' : 'Home', factor: .34 },
        { id: 'beauty', label: locale === 'ru' ? 'Красота' : 'Beauty', factor: .27 }
      ];
      if (dimension === 'city') return [
        { id: 'moscow', label: locale === 'ru' ? 'Москва' : 'Moscow', factor: .46 },
        { id: 'spb', label: locale === 'ru' ? 'Санкт-Петербург' : 'Saint Petersburg', factor: .31 },
        { id: 'regions', label: locale === 'ru' ? 'Другие города' : 'Other cities', factor: .23 }
      ];
      if (dimension === 'loyalty') return [
        { id: 'gold', label: 'Gold', factor: .24 },
        { id: 'silver', label: 'Silver', factor: .35 },
        { id: 'base', label: 'Base', factor: .41 }
      ];
      return [];
    }

    function groupingItems(scope = null) {
      const dimensions = effectiveGroupingDimensions(scope);
      const usable = scope === 'segments' ? dimensions.filter(id => id !== 'segment') : dimensions;
      return dimensionItems(usable[0]);
    }

    function scaleGroupDatum(datum, factor, rate = false) {
      const scale = value => rate === 'keep' ? value : rate ? Number((value * (1 + (factor - .33) * .12)).toFixed(1)) : Math.round(value * factor);
      if (typeof datum === 'number') return scale(datum);
      if (datum && typeof datum === 'object' && typeof datum.value === 'number') return { ...datum, value: scale(datum.value) };
      return datum;
    }

    function grainLabel(grain, short = false) {
      const labels = {
        day: { ru: short ? 'День' : 'По дням', en: short ? 'Day' : 'Daily' },
        week: { ru: short ? 'Неделя' : 'По неделям', en: short ? 'Week' : 'Weekly' },
        month: { ru: short ? 'Месяц' : 'По месяцам', en: short ? 'Month' : 'Monthly' },
        quarter: { ru: short ? 'Квартал' : 'По кварталам', en: short ? 'Quarter' : 'Quarterly' },
        year: { ru: short ? 'Год' : 'По годам', en: short ? 'Year' : 'Yearly' }
      };
      return labels[grain]?.[locale] || grain;
    }

    function periodCountLabel(count) {
      if (locale !== 'ru') return `${count} periods`;
      const mod10 = count % 10;
      const mod100 = count % 100;
      const noun = mod10 === 1 && mod100 !== 11 ? 'период' : mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14) ? 'периода' : 'периодов';
      return `${count} ${noun}`;
    }

    function readabilityScale(scope, kind) {
      const level = reportReadability.size || reportReadability[kind] || 'default';
      return level === 'small' ? .9 : level === 'large' ? 1.45 : 1;
    }

    function syncReadabilitySize(size = reportReadability.size) {
      const next = ['small', 'default', 'large'].includes(size) ? size : 'default';
      reportReadability.size = next;
      ['values', 'labels', 'axes', 'table'].forEach(kind => { reportReadability[kind] = next; });
      return next;
    }

    function smallMultipleDimensions(scope, focus = false) {
      const size = readabilityScale(scope, 'values');
      const needsAdaptiveSpacing = scope === 'segments' && segmentsChartType === 'horizontal';
      const density = needsAdaptiveSpacing ? Math.max(1, size * 1.1) : 1;
      const rowHeight = Math.round((focus ? 360 : 286) * density);
      const firstTop = focus ? 78 : 64;
      const gridHeight = Math.round((focus ? 290 : 220) * density);
      return { rowHeight, firstTop, gridHeight };
    }

    function datumNumber(datum) {
      if (typeof datum === 'number') return datum;
      if (datum && typeof datum === 'object' && typeof datum.value === 'number') return datum.value;
      return null;
    }

    function niceAxisStep(value) {
      if (!Number.isFinite(value) || value <= 0) return 1;
      const power = 10 ** Math.floor(Math.log10(value));
      const scaled = value / power;
      return (scaled <= 1 ? 1 : scaled <= 2 ? 2 : scaled <= 2.5 ? 2.5 : scaled <= 5 ? 5 : 10) * power;
    }

    function niceAxisCeiling(value) {
      if (!Number.isFinite(value) || value <= 0) return 1;
      const power = 10 ** Math.floor(Math.log10(value));
      const scaled = value / power;
      const candidates = [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10];
      return (candidates.find(candidate => scaled <= candidate) || 10) * power;
    }

    function sharedValueBounds(series, groups, rate, scaledAxis = false) {
      const values = [];
      groups.forEach(group => {
        const stacks = new Map();
        series.forEach((item, seriesIndex) => {
          const scaled = (item.data || []).map(datum => datumNumber(scaleGroupDatum(datum, group.factor, rate)));
          if (item.stack) {
            if (!stacks.has(item.stack)) stacks.set(item.stack, []);
            const totals = stacks.get(item.stack);
            scaled.forEach((value, index) => { if (Number.isFinite(value)) totals[index] = (totals[index] || 0) + value; });
          } else {
            scaled.forEach(value => { if (Number.isFinite(value)) values.push(value); });
          }
        });
        stacks.forEach(totals => totals.forEach(value => { if (Number.isFinite(value)) values.push(value); }));
      });
      if (!values.length) return {};
      const rawMin = Math.min(...values);
      const rawMax = Math.max(...values);
      if (!scaledAxis || rawMin <= 0 || rawMax === rawMin) return { min: 0, max: niceAxisCeiling(rawMax * 1.12) };
      const span = rawMax - rawMin;
      const padding = Math.max(span * .12, rawMax * .025);
      const step = niceAxisStep((span + padding * 2) / 5);
      return { min: Math.max(0, Math.floor((rawMin - padding) / step) * step), max: Math.ceil((rawMax + padding) / step) * step };
    }

    function periodColumnBuckets(grain = effectiveChartGrain('lifecycle')) {
      const period = effectiveChartPeriod('lifecycle');
      const monthNames = locale === 'ru' ? ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'] : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      if (grain === 'day') {
        const count = Math.min(14, period.day || 31);
        return Array.from({ length: count }, (_, index) => {
          const day = (period.day || 31) - count + index + 1;
          return { id: `${period.year}-${String(period.month).padStart(2, '0')}-${String(day).padStart(2, '0')}`, label: `${day} ${monthNames[period.month - 1]}`, index, count };
        });
      }
      if (grain === 'week') {
        const count = Math.min(13, period.week || 52);
        return Array.from({ length: count }, (_, index) => { const week = (period.week || 52) - count + index + 1; return { id: `${period.year}-W${String(week).padStart(2, '0')}`, label: `${locale === 'ru' ? 'Н' : 'W'}${week}`, index, count }; });
      }
      if (grain === 'month') return monthNames.slice(0, period.month).map((label, index, values) => ({ id: `${period.year}-${String(index + 1).padStart(2, '0')}`, label, index, count: values.length }));
      if (grain === 'quarter') return Array.from({ length: period.quarter }, (_, index) => ({ id: `${period.year}-Q${index + 1}`, label: `Q${index + 1}`, index, count: period.quarter }));
      return ['2022', '2023', '2024', String(period.year)].map((label, index, values) => ({ id: label, label, index, count: values.length }));
    }

    function applySmallMultiples(option, focus = false, rate = false, scope = 'overview') {
      const groups = groupingItems(scope);
      if (!groups.length || Array.isArray(option.xAxis) || Array.isArray(option.yAxis)) return option;
      const { rowHeight, firstTop, gridHeight } = smallMultipleDimensions(scope, focus);
      const originalGrid = option.grid || {};
      const originalXAxis = option.xAxis;
      const originalYAxis = option.yAxis;
      const sharedMetric = originalYAxis?.name || (locale === 'ru' ? 'Значение' : 'Value');
      const originalSeries = option.series || [];
      option.title = groups.map((group, index) => ({
        text: group.label,
        left: focus ? 18 : 10,
        top: firstTop - 28 + index * rowHeight,
        textStyle: { color: '#d5d5d9', fontSize: focus ? 13 : 11, fontWeight: 600 }
      }));
      const compactViewport = innerWidth <= 480;
      const labelGutter = ['overview', 'dynamics'].includes(scope) ? (compactViewport ? 116 : focus ? 230 : 180) : scope === 'segments' ? (compactViewport ? 72 : focus ? 150 : 110) : originalGrid.right;
      option.grid = groups.map((group, index) => ({ ...originalGrid, right: labelGutter, top: firstTop + index * rowHeight, height: gridHeight, bottom: undefined }));
      const valueAxis = originalXAxis?.type === 'value' ? originalXAxis : originalYAxis?.type === 'value' ? originalYAxis : null;
      const sharedBounds = valueAxis ? sharedValueBounds(originalSeries, groups, rate, Boolean(valueAxis.scale)) : {};
      option.xAxis = groups.map((group, index) => ({ ...originalXAxis, ...(originalXAxis?.type === 'value' ? sharedBounds : {}), scale: false, gridIndex: index }));
      option.yAxis = groups.map((group, index) => ({ ...originalYAxis, ...(originalYAxis?.type === 'value' ? sharedBounds : {}), scale: false, name: undefined, gridIndex: index }));
      option.series = groups.flatMap((group, groupIndex) => originalSeries.map((series, seriesIndex) => ({
        ...series,
        name: series.name,
        stack: series.stack ? `${series.stack}-group-${groupIndex}` : undefined,
        xAxisIndex: groupIndex,
        yAxisIndex: groupIndex,
        data: (series.data || []).map(datum => scaleGroupDatum(datum, group.factor, rate)),
        endLabel: series.endLabel ? { ...series.endLabel, show: scope === 'dynamics' ? true : series.endLabel.show } : undefined
      })));
      option.tooltip = { ...option.tooltip, confine: true };
      delete option.dataZoom;
      option.graphic = [{ type: 'text', left: 'center', top: 38, silent: true, style: { text: locale === 'ru' ? `${sharedMetric} · единая метрика · общая шкала` : `${sharedMetric} · shared metric · common scale`, fill: styleTemplate(scope).muted, fontSize: focus ? 11 : 9, fontWeight: 500 } }];
      return option;
    }

    function storeSummary() { if(!selectedStores.size)return locale==='ru'?'Все магазины':'All stores';return [...selectedStores].map(id=>storeMeta[id]?.[locale]??(locale==='ru'?'Выбранный магазин':'Selected store')).join(' · '); }

    function activeFilterCount() {
      return Object.values(quickFilters).filter(Boolean).length + appliedAdvancedGroups.reduce((sum, group) => sum + group.conditions.length, 0);
    }

    function quickFilterLabel(key) {
      const value = quickFilters[key];
      return value ? quickFilterSpecs[key].values[value][locale] : quickFilterSpecs[key].all[locale];
    }

    function conditionLabel(condition) {
      const spec = advancedFilterCatalog[condition.field];
      const field = spec?.label[locale] || condition.field;
      const operator = (advancedOperators[spec?.type] || []).find(item => item.id === condition.operator)?.[locale] || condition.operator;
      const value = spec?.values?.[condition.value]?.[locale] || condition.value;
      return `${field} ${operator} ${value}`;
    }

    function expressionSummary(groups = advancedGroups) {
      if (!groups.length) return locale === 'ru' ? 'Черновик пуст' : 'Draft is empty';
      const groupJoin = advancedFilterLogic === 'and' ? (locale === 'ru' ? ' И ' : ' AND ') : (locale === 'ru' ? ' ИЛИ ' : ' OR ');
      return groups.map(group => {
        const join = group.logic === 'and' ? (locale === 'ru' ? ' И ' : ' AND ') : (locale === 'ru' ? ' ИЛИ ' : ' OR ');
        return `(${group.conditions.map(conditionLabel).join(join)})`;
      }).join(groupJoin);
    }

    function appliedFilterSummary() {
      const quick = Object.keys(quickFilters).filter(key => quickFilters[key]).map(key => `${quickFilterSpecs[key].label[locale]}: ${quickFilterLabel(key)}`);
      const advanced = appliedAdvancedGroups.flatMap(group => group.conditions.map(conditionLabel));
      const all = [...quick, ...advanced];
      if (!all.length) return locale === 'ru' ? 'Применённых условий нет' : 'No applied conditions';
      return `${advanced.length > 1 ? advancedFilterLogic.toUpperCase() + ' · ' : ''}${all.join(' · ')}`;
    }

    function reportState() {
      return {
        snapshot: 'v12',
        author: { id: 'analyst-elena-kovacs', displayName: 'Elena Kovacs' },
        tab: currentPage,
        period: { ...reportPeriod },
        comparisons: getSelectedComparisonIds(),
        stores: [...selectedStores],
        groupBy,
        groupDimensions: [...groupDimensions],
        quickFilters: Object.fromEntries(Object.entries(quickFilters).filter(([, value]) => value)),
        advancedFilterLogic,
        advancedGroups: appliedAdvancedGroups,
        chartPeriodOverrides,
        chartGroupOverrides,
        chartPaletteOverrides,
        reportPalette,
        reportReadability,
        chartTypes: { overview: overviewChartType, dynamics: dynamicsChartType, segments: segmentsChartType },
        styleTemplate: reportStyleTemplate,
        chartStyleOverrides,
        lifecycle: {
          metric: lifecycleMetric,
          valueFormat: lifecycleValueFormat,
          percentBasis: lifecyclePercentBasis,
          comparisonMode: lifecycleComparisonMode,
          deltaDisplay: lifecycleDeltaDisplay,
          deltaBase: lifecycleDeltaBase
        }
      };
    }

    function buildSnapshotUrl() { return location.href; }

    function storedAnalysisView() { return null; }

    function renderSavedAnalysisView() { document.getElementById('personal-analysis-view-row').hidden=true;document.getElementById('published-analysis-view-row').querySelector('strong').textContent=locale==='ru'?'Точный предпросмотр':'Exact preview';document.getElementById('published-analysis-view-row').querySelector('small').textContent=''; }

    function saveAnalysisView() { bridge.save(document.querySelector('.title-row h1').textContent); }

    function applyStoredAnalysisView() { bridge.preview(); }

    function shareStateMarkup() {
      const comparison = comparisonSummary();
      return `<strong>${locale === 'ru' ? 'В ссылку войдут' : 'The link includes'}</strong><span>${locale === 'ru' ? 'Вкладка' : 'Tab'}: ${document.querySelector(`[data-page="${currentPage}"]`)?.textContent || currentPage} · ${periodValueLabel()}</span><span>${locale === 'ru' ? 'Сравнение' : 'Comparison'}: ${comparison}</span><span>${locale === 'ru' ? 'Магазины' : 'Stores'}: ${storeSummary()}</span><span>${locale === 'ru' ? 'Группировки' : 'Breakdowns'}: ${groupingLabel()}</span><span>${locale === 'ru' ? 'Фильтры' : 'Filters'}: ${appliedFilterSummary()}</span>`;
    }

    function updateSharePreview() { document.querySelectorAll('#share-dialog input,#share-dialog button:not([data-dialog-close])').forEach(n=>{n.disabled=true;n.title=unavailable();}); }

    function showToast(message) {
      const toast = document.getElementById('toast');
      toast.textContent = message;
      toast.hidden = false;
      clearTimeout(showToast.timer);
      showToast.timer = setTimeout(() => { toast.hidden = true; }, 2500);
    }

    function renderKpis() {
      kpiStrip.innerHTML = '';
      document.getElementById('kpi-context').textContent = primaryComparison ? `${periodValueLabel()} · vs ${comparisonLabel(primaryComparison)}` : `${periodValueLabel()} · ${uiText[locale].onlyActual}`;
      selectedMetricIds.forEach(id => {
        const metric = metrics.find(item => item.id === id);
        const item = document.createElement('article');
        item.className = 'kpi';
        const deltaInfo = primaryComparison ? metric.deltas[primaryComparison] : null;
        const deltaText = deltaInfo ? ` · ${deltaInfo[0]} vs ${comparisonLabel(primaryComparison)}` : '';
        item.title = `${metric.label[locale]} · ${metric.value[locale]}${deltaText} · ${metric.meta[locale]}`;
        item.setAttribute('aria-label', item.title);
        item.innerHTML = `<span class="kpi-label">${metric.label[locale]}</span><div class="kpi-value-row"><strong class="kpi-value">${metric.value[locale]}</strong>${deltaInfo ? `<span class="kpi-delta tone-${deltaInfo[1]}">${deltaInfo[0]}</span>` : ''}</div><span class="kpi-meta">${metric.meta[locale]}${primaryComparison ? ` · vs ${comparisonLabel(primaryComparison)}` : ''}</span>`;
        kpiStrip.appendChild(item);
      });
      personalPill.hidden = !isPersonalView();
      personalPill.textContent = uiText[locale].personal;
    }

    function renderPicker() {
      metricPicker.innerHTML = '';
      const orderedIds = [...draftMetricIds, ...metrics.map(metric => metric.id).filter(id => !draftMetricIds.includes(id))];
      orderedIds.forEach(id => {
        const metric = metrics.find(item => item.id === id);
        const checked = draftMetricIds.includes(id);
        const index = draftMetricIds.indexOf(id);
        const row = document.createElement('label');
        row.className = 'metric-option';
        row.innerHTML = `<input type="checkbox" value="${id}" ${checked ? 'checked' : ''}><span><strong>${metric.label[locale]}</strong><span>${metric.value[locale]} · ${metric.meta[locale]}</span></span><span class="order-actions"><button type="button" data-move="up" data-id="${id}" ${!checked || index === 0 ? 'disabled' : ''}>${uiText[locale].up}</button><button type="button" data-move="down" data-id="${id}" ${!checked || index === draftMetricIds.length - 1 ? 'disabled' : ''}>${uiText[locale].down}</button></span>`;
        const checkbox = row.querySelector('input');
        checkbox.addEventListener('change', () => {
          if (!checkbox.checked && draftMetricIds.length === 1) {
            checkbox.checked = true;
            kpiStatus.textContent = uiText[locale].limit;
            return;
          }
          if (checkbox.checked && draftMetricIds.length >= maxKpis) {
            checkbox.checked = false;
            kpiStatus.textContent = uiText[locale].limit;
            return;
          }
          draftMetricIds = checkbox.checked ? [...draftMetricIds, id] : draftMetricIds.filter(metricId => metricId !== id);
          if (!draftMetricIds.length) draftMetricIds = [defaultMetricIds[0]];
          renderPicker();
        });
        metricPicker.appendChild(row);
      });
          kpiStatus.textContent = uiText[locale].selected(draftMetricIds.length, metrics.length);
      metricPicker.querySelectorAll('[data-move]').forEach(button => button.addEventListener('click', event => {
        event.preventDefault();
        const index = draftMetricIds.indexOf(button.dataset.id);
        const target = index + (button.dataset.move === 'up' ? -1 : 1);
        if (index < 0 || target < 0 || target >= draftMetricIds.length) return;
        [draftMetricIds[index], draftMetricIds[target]] = [draftMetricIds[target], draftMetricIds[index]];
        renderPicker();
      }));
    }

    function getSelectedComparisonIds() { return [...selectedComparisons].filter(id => comparisonMeta[id]); }
    function comparisonSummary() {
      const ids = getSelectedComparisonIds();
      if (!ids.length) return uiText[locale].onlyActual;
      if (ids.length <= 2) return ids.map(comparisonLabel).join(' · ');
      return `${comparisonLabel(ids[0])} · ${comparisonLabel(ids[1])} · +${ids.length - 2}`;
    }

    function renderQuickFilterValues(key = activeQuickFilter) {
      activeQuickFilter = quickFilterSpecs[key] ? key : 'segments';
      document.querySelectorAll('[data-filter-category]').forEach(button => button.classList.toggle('is-hovered', button.dataset.filterCategory === activeQuickFilter));
      const spec = quickFilterSpecs[activeQuickFilter];
      document.getElementById('quick-filter-heading').textContent = spec.label[locale];
      const values = document.getElementById('quick-filter-values');
      const options = [[null, spec.all[locale]], ...Object.entries(spec.values).map(([id, label]) => [id, label[locale]])];
      values.innerHTML = options.map(([id, label]) => `<button class="menu-row${quickFilters[activeQuickFilter] === id ? ' is-selected' : ''}" type="button" data-quick-filter-value="${id || ''}"><svg class="icon icon--small menu-selection" aria-hidden="true"><use href="#i-check"/></svg><span>${label}</span></button>`).join('');
      values.querySelectorAll('[data-quick-filter-value]').forEach(button => button.addEventListener('click', () => {
        quickFilters[activeQuickFilter] = button.dataset.quickFilterValue || null;
        updateReportStateUi();
        renderQuickFilterValues(activeQuickFilter);
      }));
    }

    function renderPeriodControls() {
      document.querySelectorAll('[data-period-grain]').forEach(button => button.setAttribute('aria-pressed', button.dataset.periodGrain === reportPeriod.grain ? 'true' : 'false'));
      const values = document.getElementById('period-value-list');
      values.innerHTML = periodValueOptions(reportPeriod.grain).map(value => `<button class="menu-row${value === reportPeriod.value ? ' is-selected' : ''}" type="button" data-period-value="${value}" aria-pressed="${value === reportPeriod.value}"><svg class="icon icon--small menu-selection" aria-hidden="true"><use href="#i-check"/></svg><span>${periodValueLabel(value)}</span>${value === defaultPeriodValue(reportPeriod.grain) ? `<kbd>${locale === 'ru' ? 'Текущий' : 'Current'}</kbd>` : ''}</button>`).join('');
      values.querySelectorAll('[data-period-value]').forEach(button => button.addEventListener('click', () => {
        reportPeriod.value = button.dataset.periodValue;
        renderPeriodControls();
        updateContextSummary();
        dismissPopover(document.getElementById('period-popover'), true);
      }));
      document.getElementById('period-grain-select').value = reportPeriod.grain;
      const inspectorPeriod = document.getElementById('period-select');
      inspectorPeriod.innerHTML = periodValueOptions(reportPeriod.grain).map(value => `<option value="${value}" ${value === reportPeriod.value ? 'selected' : ''}>${periodValueLabel(value)}</option>`).join('');
      document.getElementById('period-summary').textContent = periodValueLabel();
      document.getElementById('period-menu-open').setAttribute('aria-label', `${locale === 'ru' ? 'Период' : 'Period'}: ${periodValueLabel()}`);
      document.querySelectorAll('[data-chart-period]').forEach(select => {
        const scope = select.dataset.chartPeriod;
        if (!select.querySelector('option[value="day"]')) select.insertAdjacentHTML('beforeend', '<option value="day"></option><option value="week"></option>');
        select.value = chartPeriodOverrides[scope].grain;
        const reportGrain = grainLabel(reportPeriod.grain, true).toLocaleLowerCase(localeCode());
        [...select.options].forEach(option => { option.textContent = option.value === 'inherit' ? `${locale === 'ru' ? 'Как в отчёте' : 'As report'} · ${reportGrain}` : grainLabel(option.value, true); });
      });
      document.querySelectorAll('[data-chart-comparison]').forEach(select => {
        const scope = select.dataset.chartComparison;
        select.value = chartPeriodOverrides[scope].comparison;
        const labels = locale === 'ru' ? [`Как в отчёте · ${comparisonSummary()}`, 'Предыдущий период', 'Прошлый год', 'Без сравнения'] : [`As report · ${comparisonSummary()}`, 'Previous period', 'Prior year', 'No comparison'];
        [...select.options].forEach((option, index) => { option.textContent = labels[index]; });
      });
      document.querySelectorAll('[data-quick-comparison]').forEach(input => {
        const label = input.closest('label')?.querySelector('span');
        if (label) label.textContent = comparisonLabel(input.value);
      });
      document.querySelectorAll('input[name="comparison"]').forEach(input => {
        const label = input.closest('label')?.querySelector('span');
        if (label) label.textContent = comparisonLabel(input.value);
      });
      [...document.getElementById('primary-comparison').options].forEach(option => { option.textContent = comparisonLabel(option.value); });
      renderStyleControls();
      renderBlockCommandBars();
    }

    function renderStyleControls() {
      document.querySelectorAll('.chart-period-controls').forEach(container => {
        const scope = container.querySelector('[data-chart-period]')?.dataset.chartPeriod;
        if (!scope || container.querySelector('[data-chart-style]')) return;
        const select = document.createElement('select');
        select.className = 'compact-control';
        select.dataset.chartStyle = scope;
        select.setAttribute('aria-label', locale === 'ru' ? 'Шаблон оформления графика' : 'Chart style template');
        select.innerHTML = '<option value="inherit"></option><option value="contrast"></option><option value="presentation"></option><option value="calm"></option>';
        container.appendChild(select);
      });
      workspace.dataset.reportStyle = reportStyleTemplate;
      const reportSelect = document.getElementById('report-style-select');
      if (reportSelect) reportSelect.value = reportStyleTemplate;
      document.querySelectorAll('[data-chart-style]').forEach(select => {
        const scope = select.dataset.chartStyle;
        select.value = chartStyleOverrides[scope];
        const reportLabel = styleTemplates[reportStyleTemplate].label[locale];
        const labels = locale === 'ru' ? [`Как в отчёте · ${reportLabel}`, 'Высокий контраст', 'Презентация', 'Спокойная палитра'] : [`As report · ${reportLabel}`, 'High contrast', 'Presentation', 'Calm palette'];
        [...select.options].forEach((option, index) => { option.textContent = labels[index]; });
        select.closest('.panel')?.setAttribute('data-effective-style', effectiveStyleId(scope));
        if (!select.dataset.bound) {
          select.dataset.bound = 'true';
          select.addEventListener('change', event => { chartStyleOverrides[scope] = event.target.value; renderStyleControls(); updateAllCharts(); updateReportStateUi(); });
        }
      });
    }

    function renderReportReadabilityControls() {
      const size = syncReadabilitySize(reportReadability.size || reportReadability.values);
      ['values', 'labels', 'axes', 'table'].forEach(kind => {
        const datasetKey = `readability${kind[0].toUpperCase()}${kind.slice(1)}`;
        workspace.dataset[datasetKey] = size;
        document.body.dataset[datasetKey] = size;
      });
      const sizes = {
        small: { short: 'S', ru: 'Мелкий размер (S)', en: 'Small size (S)' },
        default: { short: 'M', ru: 'Средний размер (M)', en: 'Medium size (M)' },
        large: { short: 'L', ru: 'Крупный размер (L)', en: 'Large size (L)' }
      };
      const paletteNames = { graphite: { ru: 'Graphite', en: 'Graphite' }, ocean: { ru: 'Ocean', en: 'Ocean' }, warm: { ru: 'Тёплая', en: 'Warm' }, vivid: { ru: 'Яркая', en: 'Vivid' } };
      if (!dataPalettes[reportPalette]) reportPalette = 'graphite';
      const paletteControls = document.getElementById('report-palette-controls');
      paletteControls.innerHTML = `<div class="block-choice-grid" data-report-palette>${Object.keys(paletteNames).map(value => { const swatches = dataPalettes[value].slice(0, 4).map(color => `<i style="background:${color}"></i>`).join(''); return blockChoice(value, reportPalette, paletteNames[value][locale], `<span class="palette-choice" aria-hidden="true">${swatches}</span>`); }).join('')}</div>`;
      paletteControls.querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => {
        reportPalette = button.dataset.value;
        Object.keys(chartPaletteOverrides).forEach(scope => { chartPaletteOverrides[scope] = 'inherit'; });
        renderReportReadabilityControls();
        refreshAnalyticalSurfaces();
      }));
      const controls = document.getElementById('report-readability-controls');
      controls.innerHTML = `<div class="block-choice-grid block-choice-grid--sizes" data-report-readability-size>${Object.keys(sizes).map(value => { const selected = value === size; const stateLabel = selected ? `${locale === 'ru' ? 'Выбрано' : 'Selected'}: ${sizes[value][locale]}` : sizes[value][locale]; return `<button class="block-choice" type="button" data-value="${value}" aria-label="${stateLabel}" title="${stateLabel}" aria-pressed="${selected}">${sizes[value].short}</button>`; }).join('')}</div>`;
      controls.querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => {
        syncReadabilitySize(button.dataset.value);
        renderReportReadabilityControls();
        renderKpis();
        renderLifecycleTable();
        renderOverviewTable();
        renderDynamicsTable();
        renderQuarterTable();
        renderSegmentTables();
        updateAllCharts();
        updateSharePreview();
      }));
      const active = reportPalette !== 'graphite' || size !== 'default';
      const summary = `${locale === 'ru' ? 'Оформление аналитических данных' : 'Analytical data appearance'}: ${paletteNames[reportPalette][locale]} · ${sizes[size].short}`;
      const trigger = document.getElementById('appearance-menu-open');
      trigger.dataset.active = active ? 'true' : 'false';
      trigger.setAttribute('aria-label', summary);
      trigger.title = summary;
    }

    function blockChoice(value, current, label, extra = '') {
      return `<button class="block-choice" type="button" data-value="${value}" aria-pressed="${value === current}">${extra}${label}</button>`;
    }

    function refreshAnalyticalSurfaces() {
      renderOverviewTable();
      renderLifecycleTable();
      renderDynamicsTable();
      renderQuarterTable();
      renderSegmentTables();
      syncChartSettingsPopover();
      updateAllCharts();
      updateReportStateUi();
    }

    function renderBlockCommandBars() {
      document.querySelectorAll('.chart-period-controls').forEach(container => {
        const periodSelect = container.querySelector('[data-chart-period]');
        const comparisonSelect = container.querySelector('[data-chart-comparison]');
        if (!periodSelect || !comparisonSelect) return;
        const scope = periodSelect.dataset.chartPeriod;
        container.classList.add('is-enhanced');
        if (!container.querySelector('[data-command="period"]')) {
          container.insertAdjacentHTML('beforeend', `
            <details class="block-command" data-command="period"><summary><svg class="icon icon--small" aria-hidden="true"><use href="#i-calendar"/></svg></summary><div class="block-command-menu"></div></details>
            <details class="block-command" data-command="comparison"><summary><svg class="icon icon--small" aria-hidden="true"><use href="#i-compare"/></svg></summary><div class="block-command-menu"></div></details>
            <details class="block-command" data-command="group"><summary><svg class="icon icon--small" aria-hidden="true"><use href="#i-data-model"/></svg></summary><div class="block-command-menu"></div></details>`);
        }
        const periodCommand = container.querySelector('[data-command="period"]');
        const comparisonCommand = container.querySelector('[data-command="comparison"]');
        const groupCommand = container.querySelector('[data-command="group"]');
        container.querySelector('[data-command="appearance"]')?.remove();
        container.querySelectorAll('.block-command').forEach(command => {
          if (command.dataset.toggleBound) return;
          command.dataset.toggleBound = 'true';
          command.addEventListener('toggle', () => { if (command.open) document.querySelectorAll('.block-command[open]').forEach(other => { if (other !== command) other.removeAttribute('open'); }); });
        });
        const periodOverride = chartPeriodOverrides[scope].grain !== 'inherit';
        const comparisonOverride = chartPeriodOverrides[scope].comparison !== 'inherit';
        periodCommand.dataset.override = String(periodOverride);
        comparisonCommand.dataset.override = String(comparisonOverride);
        groupCommand.dataset.override = String(chartGroupOverrides[scope] !== 'inherit');
        periodCommand.querySelector('summary').setAttribute('aria-label', `${locale === 'ru' ? 'Данные и период блока' : 'Block data and period'}: ${grainLabel(effectiveChartGrain(scope), true)}${periodOverride ? `, ${locale === 'ru' ? 'локально' : 'local override'}` : ''}`);
        comparisonCommand.querySelector('summary').setAttribute('aria-label', `${locale === 'ru' ? 'Сравнение блока' : 'Block comparison'}: ${chartComparisonIds(scope).length ? chartComparisonIds(scope).map(id => comparisonLabel(id, scope)).join(', ') : uiText[locale].onlyActual}${comparisonOverride ? `, ${locale === 'ru' ? 'локально' : 'local override'}` : ''}`);
        groupCommand.querySelector('summary').setAttribute('aria-label', `${locale === 'ru' ? 'Группировка блока' : 'Block breakdown'}: ${groupingLabel(effectiveGroupingDimensions(scope))}`);
        [periodCommand, comparisonCommand, groupCommand].forEach(command => {
          const summary = command.querySelector('summary');
          summary.title = summary.getAttribute('aria-label');
        });
        periodCommand.querySelector('.block-command-menu').innerHTML = `<strong class="block-menu-heading">${locale === 'ru' ? 'Данные и период' : 'Data and period'}</strong><p class="block-menu-status">${periodOverride ? '<span class="override-mark"></span>' : ''}${periodOverride ? (locale === 'ru' ? 'Локальная настройка блока' : 'Local block override') : `${locale === 'ru' ? 'Настройки отчёта' : 'Report settings'} · ${grainLabel(reportPeriod.grain, true)}`}</p><div class="block-choice-grid block-choice-grid--grain">${['inherit', 'day', 'week', 'month', 'quarter', 'year'].map(value => blockChoice(value, chartPeriodOverrides[scope].grain, value === 'inherit' ? `${locale === 'ru' ? 'Отчёт' : 'Report'} · ${grainLabel(reportPeriod.grain, true)}` : grainLabel(value, true))).join('')}</div>`;
        comparisonCommand.querySelector('.block-command-menu').innerHTML = `<strong class="block-menu-heading">${locale === 'ru' ? 'Сравнение' : 'Comparison'}</strong><div class="block-choice-grid">${[['inherit', `${locale === 'ru' ? 'Отчёт' : 'Report'} · ${comparisonSummary()}`], ['none', uiText[locale].onlyActual], ['previous', locale === 'ru' ? 'Предыдущий период' : 'Previous period'], ['prior-year', locale === 'ru' ? 'Прошлый год' : 'Prior year']].map(([value, label]) => blockChoice(value, chartPeriodOverrides[scope].comparison, label)).join('')}</div>`;
        groupCommand.querySelector('.block-command-menu').innerHTML = `<strong class="block-menu-heading">${locale === 'ru' ? 'Группировка' : 'Breakdown'}</strong><p class="block-menu-status">${chartGroupOverrides[scope] === 'inherit' ? `${locale === 'ru' ? 'Порядок отчёта' : 'Report order'} · ${groupingLabel()}` : (locale === 'ru' ? 'Группировка отключена локально' : 'Breakdown disabled locally')}</p><div class="block-choice-grid">${[['inherit', `${locale === 'ru' ? 'Порядок отчёта' : 'Report order'} · ${groupingLabel()}`], ['none', groupByMeta.none[locale]]].map(([value, label]) => blockChoice(value, chartGroupOverrides[scope], label)).join('')}</div><p class="menu-note">${locale === 'ru' ? 'Добавление и порядок измерений настраиваются в верхней панели отчёта.' : 'Add and reorder dimensions in the report toolbar.'}</p>`;
        periodCommand.querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { periodSelect.value = button.dataset.value; periodSelect.dispatchEvent(new Event('change', { bubbles: true })); periodCommand.removeAttribute('open'); }));
        comparisonCommand.querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { comparisonSelect.value = button.dataset.value; comparisonSelect.dispatchEvent(new Event('change', { bubbles: true })); comparisonCommand.removeAttribute('open'); }));
        groupCommand.querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { chartGroupOverrides[scope] = button.dataset.value; groupCommand.removeAttribute('open'); refreshAnalyticalSurfaces(); renderBlockCommandBars(); }));
      });
    }

    function renderLifecycleControlState() {
      document.querySelectorAll('#lifecycle-panel .block-command').forEach(command => {
        if (command.dataset.toggleBound) return;
        command.dataset.toggleBound = 'true';
        command.addEventListener('toggle', () => { if (command.open) document.querySelectorAll('.block-command[open]').forEach(other => { if (other !== command) other.removeAttribute('open'); }); });
      });
      const grain = chartPeriodOverrides.lifecycle.grain;
      const grainChoices = document.getElementById('lifecycle-grain-choices');
      grainChoices.innerHTML = ['inherit', 'day', 'week', 'month', 'quarter', 'year'].map(value => blockChoice(value, grain, value === 'inherit' ? `${locale === 'ru' ? 'Отчёт' : 'Report'} · ${grainLabel(reportPeriod.grain, true)}` : grainLabel(value, true))).join('');
      document.getElementById('lifecycle-period-status').innerHTML = `${grain !== 'inherit' ? '<span class="override-mark"></span>' : ''}${grain === 'inherit' ? `${locale === 'ru' ? 'Настройки отчёта' : 'Report settings'} · ${grainLabel(reportPeriod.grain, true)}` : (locale === 'ru' ? 'Локальная детализация блока' : 'Local block grain')}`;
      document.getElementById('lifecycle-period-command').dataset.override = String(grain !== 'inherit');
      document.getElementById('lifecycle-comparison-command').dataset.override = String(lifecycleComparisonMode !== 'none');
      document.getElementById('lifecycle-values-command').dataset.override = String(lifecycleValueFormat !== 'values' || lifecycleDeltaDisplay !== 'both');
      const lifecycleCommandLabels = {
        'lifecycle-period-command': `${locale === 'ru' ? 'Данные и период таблицы' : 'Table data and period'}: ${grainLabel(effectiveChartGrain('lifecycle'), true)}`,
        'lifecycle-comparison-command': `${locale === 'ru' ? 'Сравнение таблицы' : 'Table comparison'}: ${lifecycleComparisonMode === 'none' ? (locale === 'ru' ? 'без сравнения' : 'none') : lifecycleComparisonMode === 'previous' ? (locale === 'ru' ? 'к предыдущему периоду' : 'previous period') : (locale === 'ru' ? 'к выбранной базе' : 'selected base')}`,
        'lifecycle-values-command': `${locale === 'ru' ? 'Формат значений таблицы' : 'Table value format'}: ${lifecycleValueFormat === 'values' ? (locale === 'ru' ? 'значения' : 'values') : (locale === 'ru' ? 'проценты' : 'percent')}`
      };
      Object.entries(lifecycleCommandLabels).forEach(([id, label]) => {
        const summary = document.querySelector(`#${id} summary`);
        summary.setAttribute('aria-label', label);
        summary.title = label;
      });
      document.getElementById('lifecycle-comparison-choices').innerHTML = [['none', locale === 'ru' ? 'Без сравнения' : 'No comparison'], ['previous', locale === 'ru' ? 'К предыдущему' : 'Previous period'], ['base', locale === 'ru' ? 'К выбранной базе' : 'Selected base']].map(([value, label]) => blockChoice(value, lifecycleComparisonMode, label)).join('');
      document.getElementById('lifecycle-format-choices').innerHTML = [['values', locale === 'ru' ? 'Значения' : 'Values'], ['percent', locale === 'ru' ? 'Проценты' : 'Percent']].map(([value, label]) => blockChoice(value, lifecycleValueFormat, label)).join('');
      document.getElementById('lifecycle-percent-basis-wrap').hidden = lifecycleValueFormat !== 'percent';
      document.getElementById('lifecycle-percent-basis-choices').innerHTML = [['selection', locale === 'ru' ? 'Всей выборки' : 'Selection'], ['parent', locale === 'ru' ? 'Родительской строки' : 'Parent row'], ['column', locale === 'ru' ? 'Видимого столбца' : 'Visible column']].map(([value, label]) => blockChoice(value, lifecyclePercentBasis, label)).join('');
      document.getElementById('lifecycle-delta-display-choices').innerHTML = [['absolute', locale === 'ru' ? 'Абсолютная' : 'Absolute'], ['relative', locale === 'ru' ? 'Процентная' : 'Relative'], ['both', locale === 'ru' ? 'Обе' : 'Both']].map(([value, label]) => blockChoice(value, lifecycleDeltaDisplay, label)).join('');
      grainChoices.querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { chartPeriodOverrides.lifecycle.grain = button.dataset.value; document.getElementById('lifecycle-period-command').removeAttribute('open'); renderLifecycleTable(); updateReportStateUi(); }));
      document.getElementById('lifecycle-comparison-choices').querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { lifecycleComparisonMode = button.dataset.value; document.getElementById('lifecycle-comparison-command').removeAttribute('open'); renderLifecycleTable(); updateReportStateUi(); }));
      document.getElementById('lifecycle-format-choices').querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { lifecycleValueFormat = button.dataset.value; renderLifecycleTable(); }));
      document.getElementById('lifecycle-percent-basis-choices').querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { lifecyclePercentBasis = button.dataset.value; renderLifecycleTable(); }));
      document.getElementById('lifecycle-delta-display-choices').querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => { lifecycleDeltaDisplay = button.dataset.value; renderLifecycleTable(); }));
    }

    function createAdvancedCondition(field = 'customer_segment') {
      const spec = advancedFilterCatalog[field];
      return { field, operator: advancedOperators[spec.type][0].id, value: spec.defaultValue ?? Object.keys(spec.values || {})[0] ?? '' };
    }

    function createAdvancedGroup(field = 'customer_segment', logic = 'and') {
      return { logic, conditions: [createAdvancedCondition(field)] };
    }

    function advancedFieldOptions(selected) {
      const grouped = {};
      Object.entries(advancedFilterCatalog).forEach(([id, spec]) => { (grouped[spec.group[locale]] ||= []).push([id, spec]); });
      return Object.entries(grouped).map(([group, fields]) => `<optgroup label="${group}">${fields.map(([id, spec]) => `<option value="${id}" ${selected === id ? 'selected' : ''}>${spec.label[locale]}</option>`).join('')}</optgroup>`).join('');
    }

    function advancedValueControl(condition) {
      const spec = advancedFilterCatalog[condition.field];
      if (spec.type === 'number') return `<input type="number" min="0" step="100" value="${condition.value}" data-condition-value aria-label="${locale === 'ru' ? 'Значение условия' : 'Condition value'}">`;
      const options = Object.entries(spec.values || {}).map(([id, label]) => `<option value="${id}" ${condition.value === id ? 'selected' : ''}>${label[locale]}</option>`).join('');
      return `<select data-condition-value aria-label="${locale === 'ru' ? 'Значение условия' : 'Condition value'}">${options}</select>`;
    }

    function renderAdvancedConditions() {
      const list = document.getElementById('advanced-condition-list');
      if (!advancedGroups.length) {
        list.innerHTML = `<div class="applied-state">${locale === 'ru' ? 'Добавьте фильтр или независимую группу ИЛИ. Поля сгруппированы по сущностям, а уточнения сохраняют область одного события или заказа.' : 'Add a filter or an independent OR group. Fields are grouped by entity, and refinements preserve one event or order scope.'}</div>`;
      } else {
        list.innerHTML = advancedGroups.map((group, groupIndex) => `<section class="filter-group" data-filter-group="${groupIndex}"><div class="filter-group-header"><strong>${locale === 'ru' ? 'Группа' : 'Group'} ${groupIndex + 1}</strong><div class="panel-actions"><select data-group-logic aria-label="${locale === 'ru' ? 'Логика группы' : 'Group logic'}"><option value="and" ${group.logic === 'and' ? 'selected' : ''}>${locale === 'ru' ? 'И · все условия' : 'AND · all conditions'}</option><option value="or" ${group.logic === 'or' ? 'selected' : ''}>${locale === 'ru' ? 'ИЛИ · любое условие' : 'OR · any condition'}</option></select><button class="icon-button" type="button" data-group-remove aria-label="${locale === 'ru' ? 'Удалить группу' : 'Remove group'}"><svg class="icon icon--small" aria-hidden="true"><use href="#i-x"/></svg></button></div></div>${group.conditions.map((condition, conditionIndex) => { const spec = advancedFilterCatalog[condition.field]; const operators = advancedOperators[spec.type].map(item => `<option value="${item.id}" ${condition.operator === item.id ? 'selected' : ''}>${item[locale]}</option>`).join(''); return `<div data-condition-index="${conditionIndex}"><div class="condition-row"><select data-condition-field aria-label="${locale === 'ru' ? 'Поле условия' : 'Condition field'}">${advancedFieldOptions(condition.field)}</select><select data-condition-operator aria-label="${locale === 'ru' ? 'Оператор условия' : 'Condition operator'}">${operators}</select>${advancedValueControl(condition)}<button class="icon-button" type="button" data-condition-remove aria-label="${locale === 'ru' ? 'Удалить условие' : 'Remove condition'}"><svg class="icon icon--small" aria-hidden="true"><use href="#i-x"/></svg></button></div>${spec.nestedHint ? `<div class="nested-condition">${spec.nestedHint[locale]}</div>` : ''}</div>`; }).join('')}<button class="text-button text-button--quiet" type="button" data-group-condition-add><svg class="icon icon--small" aria-hidden="true"><use href="#i-plus"/></svg><span>${locale === 'ru' ? 'Добавить условие в группу' : 'Add condition to group'}</span></button></section>`).join('');
      }
      list.querySelectorAll('[data-filter-group]').forEach(groupNode => {
        const groupIndex = Number(groupNode.dataset.filterGroup);
        groupNode.querySelector('[data-group-logic]').addEventListener('change', event => { advancedGroups[groupIndex].logic = event.target.value; renderAdvancedConditions(); });
        groupNode.querySelector('[data-group-remove]').addEventListener('click', () => { advancedGroups.splice(groupIndex, 1); renderAdvancedConditions(); });
        groupNode.querySelector('[data-group-condition-add]').addEventListener('click', () => { advancedGroups[groupIndex].conditions.push(createAdvancedCondition()); renderAdvancedConditions(); });
        groupNode.querySelectorAll('[data-condition-index]').forEach(conditionNode => {
          const conditionIndex = Number(conditionNode.dataset.conditionIndex);
          conditionNode.querySelector('[data-condition-field]').addEventListener('change', event => { advancedGroups[groupIndex].conditions[conditionIndex] = createAdvancedCondition(event.target.value); renderAdvancedConditions(); });
          conditionNode.querySelector('[data-condition-operator]').addEventListener('change', event => { advancedGroups[groupIndex].conditions[conditionIndex].operator = event.target.value; renderAdvancedConditions(); });
          conditionNode.querySelector('[data-condition-value]').addEventListener('change', event => { advancedGroups[groupIndex].conditions[conditionIndex].value = event.target.value; renderAdvancedConditions(); });
          conditionNode.querySelector('[data-condition-remove]').addEventListener('click', () => { advancedGroups[groupIndex].conditions.splice(conditionIndex, 1); if (!advancedGroups[groupIndex].conditions.length) advancedGroups.splice(groupIndex, 1); renderAdvancedConditions(); });
        });
      });
      document.getElementById('advanced-filter-logic').value = advancedFilterLogic;
      const conditionCount = advancedGroups.reduce((sum, group) => sum + group.conditions.length, 0);
      const estimate = conditionCount ? Math.round(254210 / (1 + conditionCount * .62)) : 254210;
      document.getElementById('advanced-filter-summary').innerHTML = `<strong>${locale === 'ru' ? 'Черновик выражения' : 'Expression draft'}</strong><span>${expressionSummary()}</span><span class="filter-preview-count">${locale === 'ru' ? 'Предварительная оценка' : 'Preview estimate'}: ${formatInteger(estimate)} ${locale === 'ru' ? 'клиентов' : 'customers'}</span>`;
      document.getElementById('applied-filter-state').textContent = `${locale === 'ru' ? 'Применено' : 'Applied'}: ${appliedFilterSummary()}`;
    }

    function renderGroupingControls() {
      syncLegacyGroupBy();
      const selected = document.getElementById('grouping-selected-list');
      selected.innerHTML = groupDimensions.length ? groupDimensions.map((id, index) => {
        const meta = groupDimensionCatalog[id];
        return `<div class="grouping-order-row" data-group-dimension="${id}"><span class="grouping-order-index" aria-hidden="true">${index + 1}</span><span class="grouping-order-copy"><strong>${meta.label[locale]}</strong><small>${meta.hint[locale]}</small></span><span class="grouping-order-actions"><button type="button" data-group-move="up" ${index === 0 ? 'disabled' : ''} aria-label="${locale === 'ru' ? `Поднять ${meta.label[locale]}` : `Move ${meta.label[locale]} up`}"><svg class="icon icon--small" aria-hidden="true"><use href="#i-chevron"/></svg></button><button type="button" data-group-move="down" ${index === groupDimensions.length - 1 ? 'disabled' : ''} aria-label="${locale === 'ru' ? `Опустить ${meta.label[locale]}` : `Move ${meta.label[locale]} down`}"><svg class="icon icon--small" aria-hidden="true"><use href="#i-chevron"/></svg></button><button type="button" data-group-remove="${id}" aria-label="${locale === 'ru' ? `Удалить ${meta.label[locale]}` : `Remove ${meta.label[locale]}`}"><svg class="icon icon--small" aria-hidden="true"><use href="#i-x"/></svg></button></span></div>`;
      }).join('') : `<div class="grouping-empty">${locale === 'ru' ? 'Группировки не выбраны — данные показаны единым итогом.' : 'No breakdowns selected — data is shown as one total.'}</div>`;
      const available = document.getElementById('grouping-available-list');
      available.innerHTML = Object.entries(groupDimensionCatalog).map(([id, meta]) => `<button class="menu-row" type="button" data-group-add="${id}" ${groupDimensions.includes(id) ? 'disabled' : ''}><svg class="icon icon--small" aria-hidden="true"><use href="#i-plus"/></svg><span>${meta.label[locale]}</span></button>`).join('');
      selected.querySelectorAll('[data-group-move]').forEach(button => button.addEventListener('click', () => {
        const row = button.closest('[data-group-dimension]');
        const index = groupDimensions.indexOf(row.dataset.groupDimension);
        const target = button.dataset.groupMove === 'up' ? index - 1 : index + 1;
        if (target < 0 || target >= groupDimensions.length) return;
        [groupDimensions[index], groupDimensions[target]] = [groupDimensions[target], groupDimensions[index]];
        refreshAnalyticalSurfaces();
      }));
      selected.querySelectorAll('[data-group-remove]').forEach(button => button.addEventListener('click', () => {
        groupDimensions = groupDimensions.filter(id => id !== button.dataset.groupRemove);
        refreshAnalyticalSurfaces();
      }));
      available.querySelectorAll('[data-group-add]').forEach(button => button.addEventListener('click', () => {
        if (!groupDimensions.includes(button.dataset.groupAdd)) groupDimensions.push(button.dataset.groupAdd);
        refreshAnalyticalSurfaces();
      }));
    }

    function updateReportStateUi() {
      const stores = storeSummary();
      const filterCount = activeFilterCount();
      document.getElementById('stores-summary').textContent = stores;
      document.getElementById('stores-menu-open').setAttribute('aria-label', `${locale === 'ru' ? 'Магазины' : 'Stores'}: ${stores}`);
      document.getElementById('filters-summary').textContent = `${locale === 'ru' ? 'Фильтры' : 'Filters'}: ${filterCount}`;
      document.getElementById('filters-menu-open').setAttribute('aria-label', `${locale === 'ru' ? 'Фильтры' : 'Filters'}: ${filterCount}`);
      renderGroupingControls();
      document.getElementById('groupby-summary').textContent = groupingLabel();
      document.getElementById('groupby-menu-open').setAttribute('aria-label', `${locale === 'ru' ? 'Группировки' : 'Breakdowns'}: ${groupingLabel()}`);
      document.getElementById('groupby-menu-open').dataset.active = groupDimensions.length ? 'true' : 'false';
      document.getElementById('focus-groupby-chip').textContent = groupingLabel();
      document.getElementById('focus-context').textContent = `Customer 360 · ${periodValueLabel()} · ${comparisonSummary()} · ${stores}`;
      document.getElementById('focus-content').dataset.grouped = groupDimensions.length ? 'true' : 'false';
      document.getElementById('applied-filter-state').textContent = appliedFilterSummary();
      updateSharePreview();
      renderSavedAnalysisView();
      renderReportReadabilityControls();
    }

    function updateContextSummary() {
      document.querySelectorAll('[data-quick-comparison]').forEach(input => { input.checked = selectedComparisons.has(input.value); });
      document.getElementById('comparison-summary').textContent = comparisonSummary();
      document.getElementById('comparison-menu-open').setAttribute('aria-label', `${locale === 'ru' ? 'Сравнение' : 'Comparison'}: ${comparisonSummary()}`);
      document.getElementById('focus-state-chip').textContent = comparisonSummary();
      document.getElementById('focus-context').textContent = `Customer 360 · ${periodValueLabel()} · ${comparisonSummary()} · ${storeSummary()}`;
      if (!overviewChartTypeManual) overviewChartType = 'trend';
      renderPeriodControls();
      syncChartSettingsPopover();
      const onlyActual = selectedComparisons.size === 0;
      document.getElementById('only-actual-toggle').setAttribute('aria-pressed', onlyActual ? 'true' : 'false');
      document.getElementById('only-actual-toggle').classList.toggle('is-selected', onlyActual);
      document.getElementById('context-only-actual').checked = onlyActual;
      document.getElementById('primary-comparison').disabled = onlyActual;
      document.getElementById('context-comparison').classList.toggle('is-disabled', onlyActual);
      renderKpis();
      renderLifecycleTable();
      renderOverviewTable();
      renderDynamicsTable();
      renderQuarterTable();
      renderSegmentTables();
      updateReportStateUi();
      updateAllCharts();
    }

    function commonTooltipFormatter(params, unit = '') {
      const title = params[0]?.axisValueLabel || '';
      const rows = params.map(param => {
        const value = typeof param.value === 'number' ? (unit ? `${param.value.toLocaleString(localeCode())}${unit}` : formatCompact(param.value)) : param.value;
        return `<div style="display:flex;justify-content:space-between;gap:18px"><span>${param.marker}${param.seriesName}</span><strong>${value}</strong></div>`;
      }).join('');
      return `<strong>${title}</strong>${rows}`;
    }

    function aggregateMetric(values, metricKey, start, end) {
      const slice = values.slice(start, end);
      if (!slice.length) return null;
      return ['new', 'reactivated'].includes(metricKey) ? Number(slice.reduce((sum, value) => sum + value, 0).toFixed(1)) : slice[slice.length - 1];
    }

    function closedPeriodFixtureValues(source, metricKey, buckets, grain) {
      const lastMonthly = source[Math.max(0, effectiveChartPeriod('dynamics').month - 1)] ?? source[source.length - 1];
      return buckets.map((bucket, index) => {
        const progress = buckets.length <= 1 ? 1 : index / (buckets.length - 1);
        if (grain === 'day') {
          const ratio = ['new', 'reactivated'].includes(metricKey) ? .055 + progress * .012 : .82 + progress * .18;
          return Number((lastMonthly * ratio).toFixed(1));
        }
        if (grain === 'week') {
          const ratio = ['new', 'reactivated'].includes(metricKey) ? .22 + progress * .045 : .78 + progress * .22;
          return Number((lastMonthly * ratio).toFixed(1));
        }
        return lastMonthly;
      });
    }

    function dynamicsView(metricKey, scope = 'dynamics') {
      const metric = monthlyData[metricKey];
      const period = effectiveChartPeriod(scope);
      const ids = ['current', ...chartComparisonIds(scope)];
      const months = locale === 'ru' ? ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'] : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      if (period.grain === 'day' || period.grain === 'week') {
        const buckets = periodColumnBuckets(period.grain);
        const series = Object.fromEntries(ids.map(id => {
          const source = metric[seriesSourceId(id, scope)] || metric.current;
          const values = closedPeriodFixtureValues(source, metricKey, buckets, period.grain);
          return [id, id === 'previous' ? [null, ...values.slice(0, -1)] : values];
        }));
        return { grain: period.grain, categories: buckets.map(bucket => bucket.label), ids, series };
      }
      if (period.grain === 'year') {
        const end = period.month || 12;
        const series = Object.fromEntries(ids.map(id => {
          const sourceId = id === 'plan' ? 'plan' : id === 'previous' ? sourceForYear(period.year - 1) : seriesSourceId(id, scope);
          return [id, (metric[sourceId] || metric.current).slice(0, end)];
        }));
        return { grain: 'month', periodGrain: 'year', categories: months.slice(0, end), ids, series };
      }
      const end = period.grain === 'month' ? period.month : period.quarter;
      const categories = period.grain === 'month' ? months.slice(0, end) : Array.from({ length: end }, (_, index) => `Q${index + 1}`);
      const series = {};
      ids.forEach(id => {
        const sourceId = seriesSourceId(id, scope);
        const source = metric[sourceId] || metric.current;
        const values = period.grain === 'month'
          ? source.slice(0, end)
          : Array.from({ length: end }, (_, index) => aggregateMetric(source, metricKey, index * 3, index * 3 + 3));
        series[id] = id === 'previous' ? [null, ...values.slice(0, -1)] : values;
      });
      return { grain: period.grain, categories, ids, series };
    }

    function contributionView(scope = 'quarter') {
      const period = effectiveChartPeriod(scope);
      const components = ['retained', 'new', 'reactivated'];
      if (period.grain === 'day' || period.grain === 'week') {
        const buckets = periodColumnBuckets(period.grain);
        const divisor = period.grain === 'day' ? 90 : 13;
        return { grain: period.grain, categories: buckets.map(bucket => bucket.label), values: Object.fromEntries(components.map(key => [key, buckets.map((bucket, index) => Math.round(quarterData[key][period.quarter - 1] / divisor * (.88 + index / Math.max(1, buckets.length - 1) * .24)))])) };
      }
      if (period.grain === 'quarter') return { grain: 'quarter', categories: Array.from({ length: period.quarter }, (_, index) => `Q${index + 1}`), values: Object.fromEntries(components.map(key => [key, quarterData[key].slice(0, period.quarter)])) };
      if (period.grain === 'month') {
        const months = locale === 'ru' ? ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'] : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const weights = [.31, .33, .36];
        return { grain: 'month', categories: months.slice(0, period.month), values: Object.fromEntries(components.map(key => [key, Array.from({ length: period.month }, (_, index) => Math.round(quarterData[key][Math.floor(index / 3)] * weights[index % 3]))])) };
      }
      return { grain: 'quarter', periodGrain: 'year', categories: ['Q1', 'Q2', 'Q3', 'Q4'], values: Object.fromEntries(components.map(key => [key, [...quarterData[key]]])) };
    }

    function chartBase(focus = false, scope = 'overview') {
      const style = styleTemplate(scope);
      const scale = style.fontScale * readabilityScale(scope, 'axes');
      const legendScale = style.fontScale * readabilityScale(scope, 'labels');
      return {
        animation: false,
        backgroundColor: style.background,
        textStyle: { fontFamily: 'Inter, system-ui, sans-serif', color: style.text, fontSize: Math.round(11 * scale) },
        aria: { enabled: true, decal: { show: true } },
        tooltip: { trigger: 'axis', confine: true, backgroundColor: style.tooltip, borderColor: style.axis, extraCssText: 'box-shadow:0 18px 44px rgba(0,0,0,.42);border-radius:9px', textStyle: { color: style.text, fontSize: Math.round((focus ? 13 : 11) * scale) } },
        legend: { type: 'scroll', top: focus ? 12 : 8, textStyle: { fontSize: Math.round((focus ? 13 : 11) * legendScale), color: style.text }, itemWidth: focus ? 24 : 18, itemHeight: focus ? 11 : 9, itemGap: focus ? 20 : 10 },
        grid: { left: focus ? 64 : 46, right: focus ? 34 : 12, top: focus ? 62 : 48, bottom: focus ? 52 : 38, containLabel: true },
        xAxis: { axisLine: { lineStyle: { color: style.axis } }, axisTick: { show: false }, axisLabel: { color: style.muted, fontSize: Math.round((focus ? 12 : 10) * scale), margin: focus ? 14 : 8 } },
        yAxis: { splitLine: { lineStyle: { color: style.grid } }, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: style.muted, fontSize: Math.round((focus ? 12 : 10) * scale), margin: focus ? 12 : 8 } }
      };
    }

    function uniqueLegendSeries(option) {
      const unique = new Map();
      (option.series || []).forEach((series, index) => {
        if (!series?.name || unique.has(series.name)) return;
        unique.set(series.name, { ...series, legendSeriesIndex: index });
      });
      return [...unique.values()];
    }

    function legendSeriesColor(series, scope, index) {
      const itemColor = typeof series.itemStyle?.color === 'string' ? series.itemStyle.color : null;
      const lineColor = typeof series.lineStyle?.color === 'string' ? series.lineStyle.color : null;
      return itemColor || lineColor || styleTemplate(scope).palette[index % styleTemplate(scope).palette.length];
    }

    function legendStateKey(id) {
      return id === 'focus-chart' ? `${focusSource}-chart` : id;
    }

    function stableLegendSeriesKey(series, index) {
      const meta = series.legendMeta;
      if (meta?.metricId && meta?.scenarioId) return `${meta.metricId}:${meta.scenarioId}:${index}`;
      return `${series.type || 'series'}:${index}`;
    }

    function legendDatumNumber(datum) {
      const value = datum && typeof datum === 'object' && !Array.isArray(datum) && 'value' in datum ? datum.value : datum;
      if (Array.isArray(value)) return Number(value[value.length - 1]);
      return Number(value);
    }

    function latestLegendValue(series) {
      const data = series.data || [];
      for (let index = data.length - 1; index >= 0; index -= 1) {
        const value = legendDatumNumber(data[index]);
        if (Number.isFinite(value)) return value;
      }
      return null;
    }

    function legendValueText(series, option) {
      const value = latestLegendValue(series);
      if (!Number.isFinite(value)) return '—';
      const axes = Array.isArray(option.yAxis) ? option.yAxis : [option.yAxis];
      const unit = axes.find(axis => axis?.name)?.name || '';
      if (unit === '%') return `${value.toLocaleString(localeCode(), { maximumFractionDigits: 1 })}%`;
      return formatCompact(value);
    }

    function endLabelCollisionRisk(option, surfaceWidth, surfaceHeight) {
      const endSeries = uniqueLegendSeries(option).filter(series => series.endLabel?.show !== false && series.endLabel);
      if (!endSeries.length) return false;
      const rightGutter = Number((Array.isArray(option.grid) ? option.grid[0] : option.grid)?.right) || 12;
      const context = legendMeasureCanvas.getContext('2d');
      context.font = `${Math.max(...endSeries.map(series => Number(series.endLabel?.fontSize) || 11))}px Inter, system-ui, sans-serif`;
      const labels = endSeries.map(series => `${series.name} · ${legendValueText(series, option)}`);
      const widest = Math.max(...labels.map(label => context.measureText(label).width));
      if (widest + 18 > rightGutter || surfaceWidth - widest < 360) return true;
      const latest = endSeries.map(latestLegendValue).filter(Number.isFinite);
      if (latest.length < 2) return false;
      const minimum = Math.min(...latest);
      const maximum = Math.max(...latest);
      if (maximum === minimum) return true;
      const plotHeight = Math.max(120, surfaceHeight - 104);
      const positions = latest.map(value => (maximum - value) / (maximum - minimum) * plotHeight).sort((a, b) => a - b);
      return positions.some((position, index) => index > 0 && position - positions[index - 1] < 19);
    }

    function adaptiveLegendModel(scope, option, focus = false, id = '') {
      const legendOption = Array.isArray(option.legend) ? option.legend[0] : option.legend;
      if (legendOption?.show === false) return null;
      const rawSeries = uniqueLegendSeries(option);
      if (!rawSeries.length) return null;
      const stage = document.getElementById(id)?.closest('.chart-stage');
      const surfaceWidth = stage?.clientWidth || document.getElementById(id)?.clientWidth || 0;
      const surfaceHeight = document.getElementById(id)?.clientHeight || 286;
      const entries = rawSeries.map((series, index) => ({
        key: stableLegendSeriesKey(series, index),
        name: series.name,
        value: legendValueText(series, option),
        series,
        index
      }));
      const semanticEntries = entries.filter(entry => entry.series.legendMeta?.metricId && entry.series.legendMeta?.scenarioId);
      const measuredRisk = rawSeries.length <= 4 && endLabelCollisionRisk(option, surfaceWidth, surfaceHeight);
      const external = forcedExternalLegend.has(id) || rawSeries.length >= 5 || measuredRisk || semanticEntries.length === rawSeries.length && rawSeries.length > 4;
      const panelWidth = document.body.dataset.readabilityValues === 'large' ? 276 : document.body.dataset.readabilityValues === 'small' ? 220 : 240;
      const minimumPlotWidth = focus ? 620 : 480;
      const placement = external && surfaceWidth - panelWidth >= minimumPlotWidth && surfaceWidth >= (focus ? 980 : 820) ? 'right' : 'bottom';
      const base = {
        external,
        mode: semanticEntries.length === rawSeries.length && rawSeries.length > 4 ? 'factorized' : 'series',
        placement,
        measuredRisk,
        seriesNames: entries.map(entry => entry.name),
        series: entries.map(entry => ({ key: entry.key, name: entry.name })),
        rows: []
      };
      if (!external) return base;
      if (base.mode === 'factorized') {
        const metrics = new Map();
        semanticEntries.forEach(entry => {
          const meta = entry.series.legendMeta;
          if (!metrics.has(meta.metricId)) metrics.set(meta.metricId, {
            label: meta.metricLabel,
            color: meta.metricColor,
            seriesNames: [],
            items: []
          });
          const metric = metrics.get(meta.metricId);
          metric.seriesNames.push(entry.name);
          metric.items.push({
            key: `series:${entry.key}`,
            label: meta.scenarioLabel,
            accessibleLabel: `${meta.metricLabel} · ${meta.scenarioLabel}`,
            value: entry.value,
            color: meta.metricColor,
            scenario: meta.scenarioStyle,
            seriesNames: [entry.name]
          });
        });
        base.rows = [...metrics.entries()].map(([metricId, metric]) => ({
          key: `metric:${metricId}`,
          label: metric.label,
          color: metric.color,
          seriesNames: metric.seriesNames,
          items: metric.items
        }));
        return base;
      }
      base.rows = [{
        label: locale === 'ru' ? 'Серии' : 'Series',
        items: entries.map(entry => ({
          key: `series:${entry.key}`,
          label: entry.name,
          value: entry.value,
          color: legendSeriesColor(entry.series, scope, entry.index),
          seriesNames: [entry.name]
        }))
      }];
      return base;
    }

    function prepareAdaptiveLegend(id, scope, option, focus = false) {
      const stateId = legendStateKey(id);
      const previousModel = chartLegendModels[id];
      const previousState = chartLegendState[stateId] || {};
      const stableSelection = new Map((previousModel?.series || []).map(item => [item.key, previousState[item.name] !== false]));
      const model = adaptiveLegendModel(scope, option, focus, id);
      chartLegendModels[id] = model;
      const currentState = {};
      (model?.series || []).forEach(item => { currentState[item.name] = stableSelection.has(item.key) ? stableSelection.get(item.key) : previousState[item.name] !== false; });
      chartLegendState[stateId] = currentState;
      if (!model) return option;
      const sourceLegend = Array.isArray(option.legend) ? option.legend[0] || {} : option.legend || {};
      option.legend = {
        ...sourceLegend,
        show: !model.external,
        type: 'plain',
        orient: 'horizontal',
        left: 'center',
        top: focus ? 12 : 8,
        selected: Object.fromEntries(model.seriesNames.map(name => [name, currentState[name] !== false]))
      };
      if (model.external) {
        (option.series || []).forEach(series => {
          if (series.endLabel) series.endLabel = { ...series.endLabel, show: false };
        });
        const grids = Array.isArray(option.grid) ? option.grid : [option.grid];
        grids.filter(Boolean).forEach(grid => { if (typeof grid.right === 'number' && grid.right > 70) grid.right = focus ? 44 : 24; });
      }
      return option;
    }

    function legendButtonState(state, seriesNames) {
      const selected = seriesNames.filter(name => state[name] !== false).length;
      return selected === 0 ? 'false' : selected === seriesNames.length ? 'true' : 'mixed';
    }

    function syncAdaptiveLegendUi(id, model) {
      const root = document.querySelector(`[data-adaptive-legend-for="${id}"]`);
      if (!root || !model) return;
      const state = chartLegendState[legendStateKey(id)] || {};
      root.querySelectorAll('[data-legend-series]').forEach(button => {
        const names = JSON.parse(button.dataset.legendSeries);
        const pressed = legendButtonState(state, names);
        button.setAttribute('aria-pressed', pressed);
        const label = button.dataset.legendLabel;
        const value = button.dataset.legendValue;
        const stateLabel = pressed === 'false' ? (locale === 'ru' ? 'скрыто' : 'hidden') : pressed === 'mixed' ? (locale === 'ru' ? 'частично показано' : 'partially shown') : (locale === 'ru' ? 'показано' : 'shown');
        button.setAttribute('aria-label', `${label}${value ? `, ${value}` : ''}, ${stateLabel}`);
      });
      const selectedCount = model.seriesNames.filter(name => state[name] !== false).length;
      const count = root.querySelector('.series-panel-count');
      if (count) count.textContent = `${selectedCount}/${model.seriesNames.length}`;
    }

    function buildAdaptiveLegendRow(id, row, chart, model) {
      const state = chartLegendState[legendStateKey(id)];
      const rowElement = document.createElement('div');
      rowElement.className = 'adaptive-legend-row';
      rowElement.setAttribute('role', 'group');
      rowElement.setAttribute('aria-label', row.label);
      const rowLabel = document.createElement(row.seriesNames ? 'button' : 'span');
      rowLabel.className = 'adaptive-legend-row-label';
      rowLabel.textContent = row.label;
      if (row.seriesNames) {
        rowLabel.type = 'button';
        rowLabel.dataset.actionable = 'true';
        rowLabel.dataset.legendSeries = JSON.stringify(row.seriesNames);
        rowLabel.dataset.legendLabel = row.label;
        rowLabel.dataset.legendValue = '';
        rowLabel.dataset.legendControlKey = row.key;
        if (row.color) rowLabel.style.setProperty('--legend-color', row.color);
      }
      const items = document.createElement('div');
      items.className = 'adaptive-legend-items';
      row.items.forEach(item => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'adaptive-legend-item';
        button.dataset.legendSeries = JSON.stringify(item.seriesNames);
        button.dataset.legendLabel = item.accessibleLabel || item.label;
        button.dataset.legendValue = item.value || '';
        button.dataset.legendControlKey = item.key;
        button.setAttribute('aria-pressed', legendButtonState(state, item.seriesNames));
        button.title = item.accessibleLabel || item.label;
        const swatch = document.createElement('span');
        swatch.className = 'adaptive-legend-swatch';
        swatch.setAttribute('aria-hidden', 'true');
        if (item.color) swatch.style.setProperty('--legend-color', item.color);
        if (item.scenario) swatch.dataset.scenario = item.scenario;
        const label = document.createElement('span');
        label.className = 'adaptive-legend-item-label';
        label.textContent = item.label;
        const value = document.createElement('span');
        value.className = 'adaptive-legend-item-value';
        value.textContent = item.value || '—';
        button.append(swatch, label, value);
        const highlight = () => item.seriesNames.forEach(name => chart.dispatchAction({ type: 'highlight', seriesName: name }));
        const downplay = () => item.seriesNames.forEach(name => chart.dispatchAction({ type: 'downplay', seriesName: name }));
        button.addEventListener('pointerenter', highlight);
        button.addEventListener('pointerleave', downplay);
        button.addEventListener('focus', highlight);
        button.addEventListener('blur', downplay);
        button.addEventListener('click', () => {
          const nextSelected = !item.seriesNames.every(name => state[name] !== false);
          const selectedCount = model.seriesNames.filter(name => state[name] !== false).length;
          const selectedInItem = item.seriesNames.filter(name => state[name] !== false).length;
          if (!nextSelected && selectedCount <= selectedInItem) {
            const status = document.querySelector(`[data-adaptive-legend-for="${id}"] [role="status"]`);
            if (status) status.textContent = locale === 'ru' ? 'Нужно оставить хотя бы одну видимую серию' : 'Keep at least one series visible';
            return;
          }
          item.seriesNames.forEach(name => {
            state[name] = nextSelected;
            chart.dispatchAction({ type: nextSelected ? 'legendSelect' : 'legendUnSelect', name });
          });
          syncAdaptiveLegendUi(id, model);
          const status = document.querySelector(`[data-adaptive-legend-for="${id}"] [role="status"]`);
          if (status) status.textContent = `${item.label}: ${nextSelected ? (locale === 'ru' ? 'показано' : 'shown') : (locale === 'ru' ? 'скрыто' : 'hidden')}`;
        });
        items.appendChild(button);
      });
      if (row.seriesNames) {
        const toggleRow = () => {
          const nextSelected = !row.seriesNames.every(name => state[name] !== false);
          const selectedCount = model.seriesNames.filter(name => state[name] !== false).length;
          const selectedInRow = row.seriesNames.filter(name => state[name] !== false).length;
          if (!nextSelected && selectedCount <= selectedInRow) return;
          row.seriesNames.forEach(name => {
            state[name] = nextSelected;
            chart.dispatchAction({ type: nextSelected ? 'legendSelect' : 'legendUnSelect', name });
          });
          syncAdaptiveLegendUi(id, model);
        };
        rowLabel.addEventListener('pointerenter', () => row.seriesNames.forEach(name => chart.dispatchAction({ type: 'highlight', seriesName: name })));
        rowLabel.addEventListener('pointerleave', () => row.seriesNames.forEach(name => chart.dispatchAction({ type: 'downplay', seriesName: name })));
        rowLabel.addEventListener('focus', () => row.seriesNames.forEach(name => chart.dispatchAction({ type: 'highlight', seriesName: name })));
        rowLabel.addEventListener('blur', () => row.seriesNames.forEach(name => chart.dispatchAction({ type: 'downplay', seriesName: name })));
        rowLabel.addEventListener('click', toggleRow);
      }
      rowElement.append(rowLabel, items);
      return rowElement;
    }

    function renderAdaptiveLegend(id, model, chart, focus = false) {
      const element = document.getElementById(id);
      const stage = element?.closest('.chart-stage');
      const activeControlKey = document.activeElement?.closest?.(`[data-adaptive-legend-for="${id}"]`) ? document.activeElement.dataset.legendControlKey : null;
      stage?.querySelector(':scope > .adaptive-legend-host')?.remove();
      stage?.classList.remove('has-adaptive-legend');
      stage?.classList.remove('has-series-panel-right', 'has-series-panel-bottom');
      if (!model?.external || !stage) return;
      const host = document.createElement('div');
      host.className = 'adaptive-legend-host series-panel';
      host.dataset.adaptiveLegendFor = id;
      host.setAttribute('aria-label', locale === 'ru' ? 'Управление сериями графика' : 'Chart series controls');
      host.setAttribute('role', 'group');
      const header = document.createElement('div');
      header.className = 'series-panel-header';
      const title = document.createElement('span');
      title.className = 'series-panel-title';
      title.textContent = locale === 'ru' ? 'Серии' : 'Series';
      const count = document.createElement('span');
      count.className = 'series-panel-count';
      header.append(title, count);
      const body = document.createElement('div');
      body.className = 'series-panel-body';
      const legend = document.createElement('div');
      legend.className = `adaptive-legend adaptive-legend--${model.mode}`;
      const appendRows = target => model.rows.forEach(row => target.appendChild(buildAdaptiveLegendRow(id, row, chart, model)));
      appendRows(legend);
      body.appendChild(legend);
      const footer = document.createElement('div');
      footer.className = 'series-panel-footer';
      footer.textContent = locale === 'ru' ? 'Наведите или сфокусируйте строку, чтобы выделить серию' : 'Hover or focus a row to highlight its series';
      host.append(header, body, footer);
      const status = document.createElement('span');
      status.className = 'sr-only';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      host.appendChild(status);
      stage.appendChild(host);
      stage.classList.add('has-adaptive-legend', model.placement === 'right' ? 'has-series-panel-right' : 'has-series-panel-bottom');
      syncAdaptiveLegendUi(id, model);
      requestAnimationFrame(() => {
        chart.resize();
        if (activeControlKey) host.querySelector(`[data-legend-control-key="${CSS.escape(activeControlKey)}"]`)?.focus();
      });
    }

    function overviewOption(focus=false) { const data=bridge.chart(locale,focus);if(!data)return emptyOption();const base=chartBase(focus,'overview');const palette=dataPalette('overview');base.xAxis={...base.xAxis,...data.xAxis,axisLabel:base.xAxis.axisLabel,axisLine:base.xAxis.axisLine,axisTick:base.xAxis.axisTick};base.yAxis={...base.yAxis,name:'EUR'};base.legend={...base.legend,data:data.legend.data};base.tooltip=data.tooltip;base.series=data.series.map((s,index)=>({...s,lineStyle:{...s.lineStyle,width:focus?3:2.4,color:palette[index%palette.length]},itemStyle:{color:palette[index%palette.length]},symbol:'none'}));return base; }

    function dynamicsOption() { return emptyOption(); }

    function quarterOption() { return emptyOption(); }

    function segmentsOption() { return emptyOption(); }

    const focusRegistry = {
      overview: {
        urlId: 'customer-lifecycle',
        title: { ru: 'Focus · Состав клиентской базы', en: 'Focus · Customer lifecycle composition' },
        chartLabel: { ru: 'Состав клиентской базы в focus-режиме', en: 'Customer lifecycle composition in focus mode' },
        option: () => overviewOption(true),
        table: renderOverviewFocusTable,
        csv: () => csvFor('overview')
      },
      dynamics: {
        urlId: 'monthly-dynamics',
        title: { ru: 'Focus · Динамика по месяцам', en: 'Focus · Monthly dynamics' },
        chartLabel: { ru: 'Динамика по месяцам в focus-режиме', en: 'Monthly dynamics in focus mode' },
        option: () => dynamicsOption(true),
        table: renderDynamicsTable,
        csv: () => csvFor('dynamics')
      },
      quarter: {
        urlId: 'quarter-contribution',
        title: { ru: 'Focus · Вклад в активную базу по кварталам', en: 'Focus · Quarterly contribution to active base' },
        chartLabel: { ru: 'Вклад в активную базу по кварталам в focus-режиме', en: 'Quarterly contribution in focus mode' },
        option: () => quarterOption(true),
        table: renderQuarterTable,
        csv: () => csvFor('quarter')
      },
      segments: {
        urlId: 'segment-size',
        title: { ru: 'Focus · Размер сегментов', en: 'Focus · Segment size' },
        chartLabel: { ru: 'Размер сегментов в focus-режиме', en: 'Segment size in focus mode' },
        option: () => segmentsOption(true),
        table: renderSegmentTables,
        csv: () => csvFor('segments')
      }
    };

    function focusConfig(source = focusSource) { return focusRegistry[source] || focusRegistry.overview; }
    function focusSourceFromUrl(value) { return Object.keys(focusRegistry).find(key => focusRegistry[key].urlId === value) || null; }

    function renderedEndLabelsCollide(id, model) {
      const element = document.getElementById(id);
      const svg = element?.querySelector('svg');
      if (!svg || !model?.seriesNames?.length) return false;
      const chartRect = element.getBoundingClientRect();
      const labels = [...svg.querySelectorAll('text')]
        .filter(text => model.seriesNames.some(name => text.textContent.startsWith(name)))
        .map(text => text.getBoundingClientRect())
        .filter(rect => rect.left > chartRect.left + chartRect.width * .55 && rect.top > chartRect.top + 56 && rect.width > 0 && rect.height > 0);
      if (labels.some(rect => rect.left < chartRect.left || rect.right > chartRect.right - 1 || rect.top < chartRect.top || rect.bottom > chartRect.bottom)) return true;
      for (let index = 0; index < labels.length; index += 1) {
        for (let otherIndex = index + 1; otherIndex < labels.length; otherIndex += 1) {
          const a = labels[index];
          const b = labels[otherIndex];
          const horizontal = Math.min(a.right, b.right) - Math.max(a.left, b.left);
          const vertical = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
          if (horizontal > 0 && vertical > -3) return true;
        }
      }
      return false;
    }

    function ensureChart(id, optionFactory) {
      const element = document.getElementById(id);
      if (!element || element.offsetWidth === 0) return null;
      const scope = id === 'focus-chart' ? focusSource : id.replace('-chart', '').replace('overview', 'overview').replace('segments', 'segments');
      const groupCount = groupingItems(scope).length;
      element.classList.toggle('is-grouped', groupCount > 0);
      element.parentElement?.classList.toggle('is-grouped', groupCount > 0);
      if (groupCount) {
        const { rowHeight, firstTop, gridHeight } = smallMultipleDimensions(scope, id === 'focus-chart');
        const height = Math.max(id === 'focus-chart' ? 1160 : 940, firstTop + (groupCount - 1) * rowHeight + gridHeight + 60);
        element.style.height = `${height}px`;
        element.style.minHeight = `${height}px`;
        if (element.parentElement) element.parentElement.style.minHeight = `${height}px`;
      } else {
        element.style.removeProperty('height');
        element.style.removeProperty('min-height');
        element.parentElement?.style.removeProperty('min-height');
      }
      if (!window.echarts) {
        element.innerHTML = `<div class="chart-fallback">${uiText[locale].chartError}</div>`;
        return null;
      }
      if (!chartInstances[id]) chartInstances[id] = echarts.init(element, null, { renderer: 'svg' });
      if (!chartLegendBindings.has(id)) {
        chartLegendBindings.add(id);
        chartInstances[id].on('legendselectchanged', params => {
          const stateId = legendStateKey(id);
          chartLegendState[stateId] = { ...(chartLegendState[stateId] || {}), ...params.selected };
          syncAdaptiveLegendUi(id, chartLegendModels[id]);
        });
      }
      if (chartResizeObserver && !observedChartElements.has(element)) {
        observedChartElements.add(element);
        chartResizeObserver.observe(element);
      }
      const focus = id === 'focus-chart';
      const option = prepareAdaptiveLegend(id, scope, optionFactory(), focus);
      chartInstances[id].setOption(option, true);
      chartInstances[id].resize();
      renderAdaptiveLegend(id, chartLegendModels[id], chartInstances[id], focus);
      if (!chartLegendModels[id]?.external) requestAnimationFrame(() => {
        if (!forcedExternalLegend.has(id) && renderedEndLabelsCollide(id, chartLegendModels[id])) {
          forcedExternalLegend.add(id);
          ensureChart(id, optionFactory);
        }
      });
      return chartInstances[id];
    }

    function ensureChartsForPage(page) {
      requestAnimationFrame(() => {
        if (page === 'overview') ensureChart('overview-chart', () => overviewOption(false));
        if (page === 'dynamics') {
          ensureChart('dynamics-chart', () => dynamicsOption(false));
          ensureChart('quarter-chart', quarterOption);
        }
        if (page === 'segments') ensureChart('segments-chart', segmentsOption);
      });
    }

    function updateAllCharts() {
      if (chartInstances['overview-chart']) ensureChart('overview-chart', () => overviewOption(false));
      if (chartInstances['dynamics-chart']) ensureChart('dynamics-chart', () => dynamicsOption(false));
      if (chartInstances['quarter-chart']) ensureChart('quarter-chart', () => quarterOption(false));
      if (chartInstances['segments-chart']) ensureChart('segments-chart', () => segmentsOption(false));
      if (chartInstances['focus-chart'] && !document.getElementById('focus-surface').hidden) ensureChart('focus-chart', () => focusConfig().option());
    }

    let sharedTableGridFrame = 0;
    const tableMeasureCanvas = document.createElement('canvas');

    function clearSharedTableGrid(table) {
      table.removeAttribute('data-shared-table-grid');
      table.removeAttribute('data-shared-table-signature');
      table.style.removeProperty('--shared-table-width');
      table.style.removeProperty('--shared-stub-width');
      table.style.removeProperty('--shared-value-column-width');
      table.querySelector(':scope > colgroup[data-shared-table-grid]')?.remove();
    }

    function tableColumnSignature(table) {
      const headerRow = table.tHead?.rows[table.tHead.rows.length - 1];
      if (!headerRow || headerRow.cells.length < 3) return null;
      const columns = [...headerRow.cells].slice(1).map(cell => cell.textContent.trim().replace(/\s+/g, ' '));
      if (!columns.every(Boolean)) return null;
      const page = table.closest('[data-page-panel]')?.dataset.pagePanel || (table.closest('#focus-surface') ? 'focus' : 'report');
      return `${page}::${columns.join('\u241f')}`;
    }

    function intrinsicCellWidth(cell) {
      const content = cell.querySelector('.table-row-label span, .profile-name') || cell;
      const contentStyle = getComputedStyle(content);
      const context = tableMeasureCanvas.getContext('2d');
      context.font = `${contentStyle.fontStyle} ${contentStyle.fontWeight} ${contentStyle.fontSize} ${contentStyle.fontFamily}`;
      const contentWidth = context.measureText(content.textContent.trim().replace(/\s+/g, ' ')).width;
      const cellStyle = getComputedStyle(cell);
      const padding = parseFloat(cellStyle.paddingInlineStart) + parseFloat(cellStyle.paddingInlineEnd);
      const hierarchyAllowance = cell.querySelector('.table-row-label, .profile-name') ? 14 : 0;
      return Math.ceil(contentWidth + padding + hierarchyAllowance);
    }

    function syncSharedTableGeometry() { 
      const allTables = [...document.querySelectorAll('table')];
      allTables.forEach(clearSharedTableGrid);
      const groups = new Map();
      allTables.filter(table => table.getClientRects().length && table.closest('[hidden]') === null).forEach(table => {
        const signature = tableColumnSignature(table);
        if (!signature) return;
        if (!groups.has(signature)) groups.set(signature, []);
        groups.get(signature).push(table);
      });
      groups.forEach((tables, signature) => {
        if (!tables.length) return;
        const columnCount = tables[0].tHead.rows[tables[0].tHead.rows.length - 1].cells.length - 1;
        if (!columnCount || tables.some(table => table.tHead.rows[table.tHead.rows.length - 1].cells.length !== columnCount + 1)) return;
        let sharedWidth = Math.max(...tables.map(table => table.getBoundingClientRect().width));
        const naturalStubWidth = Math.max(...tables.flatMap(table => [...table.rows].flatMap(row => {
          const cell = row.cells[0];
          return cell && !cell.hasAttribute('colspan') ? [intrinsicCellWidth(cell)] : [];
        })));
        const minimumTrackWidth = 96;
        const minimumStubWidth = innerWidth <= 720 ? 168 : 192;
        const stubWidth = Math.max(minimumStubWidth, naturalStubWidth);
        sharedWidth = Math.max(sharedWidth, stubWidth + columnCount * minimumTrackWidth);
        const valueColumnWidth = (sharedWidth - stubWidth) / columnCount;
        tables.forEach(table => {
          const colgroup = document.createElement('colgroup');
          colgroup.dataset.sharedTableGrid = '';
          colgroup.innerHTML = '<col>' + '<col>'.repeat(columnCount);
          table.insertBefore(colgroup, table.firstChild);
          table.dataset.sharedTableGrid = 'true';
          table.dataset.sharedTableSignature = signature;
          table.style.setProperty('--shared-table-width', `${sharedWidth.toFixed(3)}px`);
          table.style.setProperty('--shared-stub-width', `${stubWidth.toFixed(3)}px`);
          table.style.setProperty('--shared-value-column-width', `${valueColumnWidth.toFixed(3)}px`);
        });
      });
     }

    function scheduleSharedTableGeometry() {
      cancelAnimationFrame(sharedTableGridFrame);
      sharedTableGridFrame = requestAnimationFrame(() => {
        sharedTableGridFrame = 0;
        syncSharedTableGeometry();
      });
    }

    const sharedTableResizeObserver = typeof ResizeObserver === 'function'
      ? new ResizeObserver(() => scheduleSharedTableGeometry())
      : null;
    document.querySelectorAll('.report-page > .panel, .focus-section').forEach(panel => sharedTableResizeObserver?.observe(panel));

    function tableMarkup(headers, rows, className = '') {
      scheduleSharedTableGeometry();
      return `<table class="${className}"><thead><tr>${headers.map(header => `<th>${header}</th>`).join('')}</tr></thead><tbody>${rows.map((row, rowIndex) => `<tr class="${rowIndex === 0 && row[0] === (locale === 'ru' ? 'Итого' : 'Total') ? 'table-total' : ''}">${row.map((cell, index) => `<td${index === 0 ? ' scope="row"' : ''}>${cell}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
    }

    function renderOverviewTable() { document.getElementById('overview-chart-table').innerHTML=realTable();scheduleSharedTableGeometry(); }

    function lifecycleRowGroups() {
      const lifecycleRows = lifecycleCategories[locale].map((label, index) => ({ id: `state-${index}`, label, factor: lifecycleSeries.current[index] / lifecycleTotals.current, categoryIndex: index }));
      const segmentRows = segments.map((segment, index) => ({ id: `segment-${segment.id}`, label: segment.name[locale], factor: segment.customers / lifecycleTotals.current, segmentIndex: index }));
      const dimensions = effectiveGroupingDimensions('lifecycle');
      if (!dimensions.length) return [{ id: 'lifecycle', label: locale === 'ru' ? 'Состояния жизненного цикла' : 'Lifecycle states', factor: 1, rows: lifecycleRows.map(row => ({ ...row, parentFactor: 1 })) }];
      const [primary, ...remaining] = dimensions;
      const primaryItems = dimensionItems(primary);
      const combinations = remaining.reduce((rows, dimension) => rows.flatMap(row => dimensionItems(dimension).map(item => ({ id: `${row.id}-${item.id}`, label: row.label ? `${row.label} · ${item.label}` : item.label, factor: row.factor * item.factor, segmentIndex: dimension === 'segment' ? segments.findIndex(segment => segment.id === item.id) : row.segmentIndex }))), [{ id: '', label: '', factor: 1 }]);
      return primaryItems.map(item => {
        const primarySegmentIndex = primary === 'segment' ? segments.findIndex(segment => segment.id === item.id) : undefined;
        const sourceRows = remaining.length ? combinations.map(row => ({ ...row, segmentIndex: row.segmentIndex ?? primarySegmentIndex })) : lifecycleRows;
        return { ...item, rows: sourceRows.map((row, rowIndex) => ({ ...row, id: `${item.id}-${row.id || rowIndex}`, factor: row.factor * item.factor, parentFactor: item.factor, breakdownFactor: row.factor, segmentIndex: row.segmentIndex ?? primarySegmentIndex })) };
      });
    }

    function lifecycleRowBase(metric, row) {
      if (row.segmentIndex !== undefined) {
        const segment = segments[row.segmentIndex];
        if (metric === 'customers') return lifecycleTotals.current * row.factor;
        if (metric === 'revenue') return segment.customers * segment.receipt * segment.frequency * (row.breakdownFactor || 1);
        if (metric === 'receipt') return segment.receipt;
        return segment.frequency;
      }
      const index = row.categoryIndex ?? 0;
      if (metric === 'customers') return lifecycleTotals.current * row.factor;
      if (metric === 'revenue') return lifecycleMetricSeries.revenue.current[index] * (row.parentFactor || 1);
      return lifecycleMetricSeries[metric].current[index] * (1 + ((row.parentFactor || .33) - .33) * .08);
    }

    function lifecycleBucketFactor(bucket, metric) {
      const progress = bucket.count <= 1 ? 1 : bucket.index / (bucket.count - 1);
      if (effectiveChartGrain('lifecycle') === 'year') return [.80, .86, .92, 1][bucket.index] || 1;
      return ['receipt', 'frequency'].includes(metric) ? .94 + progress * .06 : .82 + progress * .18;
    }

    function lifecyclePeriodFactor(periodId, row, bucket) {
      if (!periodId || periodId === 'current') return 1;
      const base = comparisonScale(periodId, 'lifecycle');
      const rowVariation = ((row.categoryIndex ?? row.segmentIndex ?? 0) - 2) * .008;
      const bucketVariation = (bucket.index - Math.max(0, bucket.count - 1) / 2) * .002;
      return Math.max(.68, base + rowVariation + bucketVariation);
    }

    function lifecycleRawValue(metric, row, bucket, periodId = 'current') {
      const value = lifecycleRowBase(metric, row) * lifecycleBucketFactor(bucket, metric) * lifecyclePeriodFactor(periodId, row, bucket);
      return ['receipt', 'frequency'].includes(metric) ? value : Math.round(value);
    }

    function lifecycleDenominator(metric, row, bucket, groups, periodId = 'current') {
      if (lifecyclePercentBasis === 'selection') {
        if (metric === 'customers') return lifecycleTotals.current * lifecycleBucketFactor(bucket, metric) * lifecyclePeriodFactor(periodId, row, bucket);
        return groups.flatMap(group => group.rows).reduce((sum, candidate) => sum + lifecycleRawValue(metric, candidate, bucket, periodId), 0);
      }
      if (lifecyclePercentBasis === 'parent') {
        const parent = groups.find(group => group.rows.some(candidate => candidate.id === row.id));
        return parent?.rows.reduce((sum, candidate) => sum + lifecycleRawValue(metric, candidate, bucket, periodId), 0) || 0;
      }
      return groups.flatMap(group => group.rows).reduce((sum, candidate) => sum + lifecycleRawValue(metric, candidate, bucket, periodId), 0);
    }

    function formatLifecycleMetric(metric, value) {
      if (metric === 'customers') return formatInteger(Math.round(value));
      if (metric === 'revenue') return `₽${formatCompact(Math.round(value))}`;
      if (metric === 'receipt') return `₽${formatInteger(Math.round(value))}`;
      return `${value.toLocaleString(localeCode(), { minimumFractionDigits: 1, maximumFractionDigits: 1 })}`;
    }

    function lifecycleDisplayValue(metric, row, bucket, groups, periodId = 'current') {
      const raw = lifecycleRawValue(metric, row, bucket, periodId);
      if (lifecycleValueFormat === 'values') return { raw, display: formatLifecycleMetric(metric, raw), numeric: raw, unit: metric === 'customers' ? (locale === 'ru' ? 'клиентов' : 'customers') : '' };
      const denominator = lifecycleDenominator(metric, row, bucket, groups, periodId);
      const share = denominator ? raw / denominator * 100 : 0;
      return { raw, display: `${share.toLocaleString(localeCode(), { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`, numeric: share, unit: '%' };
    }

    function lifecycleCellMarkup(metric, row, bucket, referenceBucket, groups, referencePeriodId = 'current') {
      const current = lifecycleDisplayValue(metric, row, bucket, groups);
      if (!referenceBucket || lifecycleComparisonMode === 'none') return `<span class="analytic-cell"><strong>${current.display}</strong></span>`;
      const reference = lifecycleDisplayValue(metric, row, referenceBucket, groups, referencePeriodId);
      const absolute = current.numeric - reference.numeric;
      const relative = reference.numeric ? (current.numeric - reference.numeric) / reference.numeric * 100 : null;
      const tone = absolute >= 0 ? 'positive' : 'negative';
      const absoluteText = lifecycleValueFormat === 'percent'
        ? `${absolute > 0 ? '+' : absolute < 0 ? '−' : ''}${Math.abs(absolute).toLocaleString(localeCode(), { minimumFractionDigits: 1, maximumFractionDigits: 1 })} ${locale === 'ru' ? 'п.п.' : 'pp'}`
        : metric === 'customers' ? formatSignedInteger(Math.round(absolute)) : metric === 'revenue' ? `${absolute >= 0 ? '+' : '−'}₽${formatCompact(Math.abs(absolute))}` : `${absolute > 0 ? '+' : absolute < 0 ? '−' : ''}${Math.abs(absolute).toLocaleString(localeCode(), { maximumFractionDigits: 1 })}`;
      const relativeText = relative === null ? '—' : formatSignedPct(relative);
      const deltaText = lifecycleDeltaDisplay === 'absolute' ? absoluteText : lifecycleDeltaDisplay === 'relative' ? relativeText : `${absoluteText} · ${relativeText}`;
      return `<span class="analytic-cell"><strong>${current.display}</strong><small class="tone-${tone}">${deltaText}</small></span>`;
    }

    function lifecycleBaseLabel(id) {
      const period = effectiveChartPeriod('lifecycle');
      if (['month', 'quarter'].includes(effectiveChartGrain('lifecycle'))) {
        if (id === 'plan') return `${locale === 'ru' ? 'План' : 'Plan'} · ${period.year}`;
        if (/^202[2-4]$/.test(id)) return id;
      }
      return comparisonLabel(id, 'lifecycle');
    }

    function syncLifecycleBaseOptions() {
      const select = document.getElementById('lifecycle-delta-base');
      const bases = getSelectedComparisonIds().filter(id => id !== 'previous');
      if (!bases.length) bases.push('2024');
      if (!bases.includes(lifecycleDeltaBase)) lifecycleDeltaBase = bases.includes(primaryComparison) ? primaryComparison : bases[0];
      select.innerHTML = bases.map(id => `<option value="${id}" ${id === lifecycleDeltaBase ? 'selected' : ''}>${lifecycleBaseLabel(id)}</option>`).join('');
      document.getElementById('lifecycle-base-wrap').hidden = lifecycleComparisonMode !== 'base';
    }

    function buildLifecycleTableMarkup() { return realTable(); }

    function renderOverviewFocusTable() { setFocusTableMarkup(realTable()); }

    function renderLifecycleTable() { document.getElementById('lifecycle-table').innerHTML=bridge.tableRows(locale);document.getElementById('lifecycle-range').textContent=bridge.range();document.getElementById('lifecycle-footnote').textContent='EUR · UTC';scheduleSharedTableGeometry(); }

    function setFocusTableMarkup(markup) {
      const groups = groupingItems(focusSource);
      document.getElementById('focus-table').innerHTML = groups.length
        ? `<div class="focus-table-groups">${groups.map(group => `<section class="focus-table-group"><h3>${group.label}</h3><div class="data-table-wrap">${markup}</div></section>`).join('')}</div>`
        : `<div class="data-table-wrap">${markup}</div>`;
    }

    function renderDynamicsTable() { unavailableTable('dynamics-table'); }

    function renderQuarterTable() { unavailableTable('quarter-table'); }

    function renderSegmentTables() { document.querySelectorAll('#page-segments table').forEach(t=>{t.innerHTML=`<caption>${unavailable()}</caption>`;}); }

    function renderMigrationMatrix() { document.querySelectorAll('#page-segments table').forEach(t=>{t.innerHTML=`<caption>${unavailable()}</caption>`;}); }

    function syncExportControls(scope, view) {
      document.querySelectorAll(`.adaptive-export[data-export-scope="${scope}"]`).forEach(details => {
        details.removeAttribute('open');
        details.querySelectorAll('[data-export-options]').forEach(options => { options.hidden = options.dataset.exportOptions !== view; });
        const summary = details.querySelector('summary');
        const label = view === 'table'
          ? (locale === 'ru' ? 'Скачать таблицу' : 'Download table')
          : (locale === 'ru' ? 'Скачать график' : 'Download chart');
        summary.setAttribute('aria-label', label);
        summary.title = label;
      });
    }

    function syncAllExportControls() {
      document.querySelectorAll('.adaptive-export[data-export-scope]').forEach(details => {
        const scope = details.dataset.exportScope;
        const selected = document.querySelector(`[data-view-button="${scope}"][aria-pressed="true"]`);
        syncExportControls(scope, selected?.dataset.view === 'table' ? 'table' : 'chart');
      });
      document.querySelectorAll('.table-export > summary').forEach(summary => {
        const label = locale === 'ru' ? 'Скачать таблицу' : 'Download table';
        summary.setAttribute('aria-label', label);
        summary.title = label;
      });
      document.querySelectorAll('.chart-only-export > summary, #focus-chart-section .chart-export > summary').forEach(summary => {
        const label = locale === 'ru' ? 'Скачать график' : 'Download chart';
        summary.setAttribute('aria-label', label);
        summary.title = label;
      });
      document.querySelectorAll('[data-chart-export]').forEach(button => { button.setAttribute('aria-label', `${locale === 'ru' ? 'Скачать график как' : 'Download chart as'} ${button.dataset.format.toUpperCase()}`); });
      document.querySelectorAll('[data-table-export]').forEach(button => { button.setAttribute('aria-label', `${locale === 'ru' ? 'Скачать таблицу как' : 'Download table as'} ${button.dataset.format.toUpperCase()}`); });
    }

    function setView(group, view) {
      document.querySelectorAll(`[data-view-button="${group}"]`).forEach(button => button.setAttribute('aria-pressed', button.dataset.view === view ? 'true' : 'false'));
      document.querySelectorAll(`[data-chart-view="${group}"]`).forEach(element => { element.hidden = view !== 'chart'; });
      document.querySelectorAll(`[data-table-view="${group}"]`).forEach(element => { element.hidden = view !== 'table'; });
      syncExportControls(group, view);
      scheduleSharedTableGeometry();
      if (view === 'chart') {
        if (group === 'overview') ensureChart('overview-chart', () => overviewOption(false));
        if (group === 'dynamics') ensureChart('dynamics-chart', () => dynamicsOption(false));
        if (group === 'quarter') ensureChart('quarter-chart', quarterOption);
        if (group === 'segments') ensureChart('segments-chart', segmentsOption);
        if (group === 'focus') ensureChart('focus-chart', () => focusConfig().option());
      }
    }

    function activatePage(page, push = true, focusTab = false) {
      if (!['overview', 'dynamics', 'segments', 'findings'].includes(page)) return;
      pageScroll[currentPage] = reportScroll.scrollTop;
      currentPage = page;
      document.querySelectorAll('[data-page-panel]').forEach(panel => { panel.hidden = panel.dataset.pagePanel !== page; });
      document.querySelectorAll('[data-page]').forEach(tab => {
        const active = tab.dataset.page === page;
        tab.setAttribute('aria-selected', active ? 'true' : 'false');
        tab.tabIndex = active ? 0 : -1;
        if (active && focusTab) tab.focus();
      });
      if (push && location.hash !== `#${page}`) history.pushState({ page }, '', `${location.pathname}${location.search}#${page}`);
      requestAnimationFrame(() => { reportScroll.scrollTop = pageScroll[page] || 0; ensureChartsForPage(page); scheduleSharedTableGeometry(); });
    }

    function activateInspectorPanel(name = 'context') {
      const requested = document.querySelector(`[data-inspector-panel="${name}"]`) ? name : 'context';
      document.querySelectorAll('[data-inspector-tab]').forEach(button => {
        const active = button.dataset.inspectorTab === requested;
        button.setAttribute('aria-selected', active ? 'true' : 'false');
        button.tabIndex = active ? 0 : -1;
      });
      document.querySelectorAll('[data-inspector-panel]').forEach(panel => { panel.hidden = panel.dataset.inspectorPanel !== requested; });
    }

    function openContext(target) {
      const panel = ['filters', 'discussion', 'trust', 'saved'].includes(target) ? target : 'context';
      activateInspectorPanel(panel);
      workspace.dataset.context = 'open';
      const drawer = document.getElementById('context-drawer');
      drawer.inert = false;
      drawer.setAttribute('aria-hidden', 'false');
      const toggle = document.getElementById('context-open');
      toggle.setAttribute('aria-expanded', 'true');
      const toggleLabel = locale === 'ru' ? 'Закрыть инспектор отчёта' : 'Close report inspector';
      toggle.setAttribute('aria-label', toggleLabel);
      toggle.title = toggleLabel;
      if (target && panel === 'context') requestAnimationFrame(() => document.getElementById(`context-${target}`)?.scrollIntoView({ block: 'start' }));
      requestAnimationFrame(() => Object.values(chartInstances).forEach(chart => chart.resize()));
    }

    function closeContext(returnFocus = true) {
      workspace.dataset.context = 'closed';
      const drawer = document.getElementById('context-drawer');
      drawer.setAttribute('aria-hidden', 'true');
      drawer.inert = true;
      const toggle = document.getElementById('context-open');
      toggle.setAttribute('aria-expanded', 'false');
      const toggleLabel = locale === 'ru' ? 'Открыть инспектор отчёта' : 'Open report inspector';
      toggle.setAttribute('aria-label', toggleLabel);
      toggle.title = toggleLabel;
      if (returnFocus) toggle.focus();
      requestAnimationFrame(() => Object.values(chartInstances).forEach(chart => chart.resize()));
    }

    function applyComparisonControls(event) {
      const checked = [...document.querySelectorAll('input[name="comparison"]:checked')].map(input => input.value);
      selectedComparisons = new Set(checked);
      if (event?.target?.id === 'primary-comparison') {
        primaryComparison = event.target.value;
        selectedComparisons.add(primaryComparison);
      } else if (!selectedComparisons.size) {
        primaryComparison = null;
      } else if (!primaryComparison || !selectedComparisons.has(primaryComparison)) {
        primaryComparison = selectedComparisons.has('2024') ? '2024' : checked[0];
      }
      if (primaryComparison) document.getElementById('primary-comparison').value = primaryComparison;
      document.querySelectorAll('input[name="comparison"]').forEach(input => { input.checked = selectedComparisons.has(input.value); });
      updateContextSummary();
    }

    function setOnlyActual() {
      selectedComparisons.clear();
      primaryComparison = null;
      document.querySelectorAll('input[name="comparison"], [data-quick-comparison]').forEach(input => { input.checked = false; });
      updateContextSummary();
    }

    function resetContext() {
      primaryComparison = '2024';
      selectedComparisons = new Set(['plan', '2024']);
      selectedStores.clear();
      groupBy = 'none';
      quickFilters = { channels: null, segments: null, categories: null, coverage: null };
      advancedGroups = [];
      appliedAdvancedGroups = [];
      advancedFilterLogic = 'and';
      reportPeriod = { grain: 'year', value: '2025' };
      Object.values(chartPeriodOverrides).forEach(override => { override.grain = 'inherit'; override.comparison = 'inherit'; });
      reportStyleTemplate = 'default';
      Object.keys(chartStyleOverrides).forEach(scope => { chartStyleOverrides[scope] = 'inherit'; });
      document.getElementById('primary-comparison').value = '2024';
      document.querySelectorAll('input[name="comparison"]').forEach(input => { input.checked = selectedComparisons.has(input.value); });
      document.getElementById('all-stores').checked = true;
      document.querySelectorAll('[data-store-option]').forEach(input => { input.checked = false; });
      renderQuickFilterValues();
      renderAdvancedConditions();
      updateContextSummary();
      showToast(uiText[locale].reset);
    }

    function openFocus(source, trigger, anchor = 'chart') {
      focusSource = focusRegistry[source] ? source : 'overview';
      focusTrigger = trigger || document.activeElement;
      focusAnchor = anchor === 'table' ? 'table' : 'chart';
      const url = new URL(buildSnapshotUrl());
      url.searchParams.set('focus', focusConfig().urlId);
      url.searchParams.set('focus-section', focusAnchor);
      history.pushState({ focus: focusSource }, '', `${url.pathname}${url.search}${url.hash}`);
      showFocusSurface();
    }

    function showFocusSurface() {
      const focus = new URL(location.href).searchParams.get('focus');
      const requestedAnchor = new URL(location.href).searchParams.get('focus-section');
      const surface = document.getElementById('focus-surface');
      const source = focusSourceFromUrl(focus);
      if (!source) {
        surface.hidden = true;
        shell.inert = false;
        chartInstances['focus-chart']?.clear();
        document.getElementById('focus-table').innerHTML = '';
        if (pendingFocusRestore && focusTrigger?.isConnected) focusTrigger.focus();
        pendingFocusRestore = false;
        requestAnimationFrame(() => updateAllCharts());
        return;
      }
      focusSource = source;
      focusAnchor = requestedAnchor === 'table' ? 'table' : 'chart';
      const config = focusConfig();
      chartInstances['focus-chart']?.clear();
      document.getElementById('focus-table').innerHTML = '';
      surface.hidden = false;
      shell.inert = true;
      document.getElementById('focus-content').dataset.grouped = groupingItems(focusSource).length ? 'true' : 'false';
      document.getElementById('focus-title').textContent = config.title[locale];
      document.getElementById('focus-chart').setAttribute('aria-label', config.chartLabel[locale]);
      config.table();
      requestAnimationFrame(() => {
        ensureChart('focus-chart', () => config.option());
        const target = document.getElementById(focusAnchor === 'table' ? 'focus-table-section' : 'focus-chart-section');
        target?.scrollIntoView({ block: 'start' });
      });
      document.getElementById('focus-close').focus();
    }

    function closeFocus() {
      pendingFocusRestore = true;
      if (history.state?.focus && new URL(location.href).searchParams.has('focus')) history.back();
      else {
        const url = new URL(location.href);
        url.searchParams.delete('focus');
        url.searchParams.delete('focus-section');
        history.replaceState({ page: currentPage }, '', `${url.pathname}${url.search}${url.hash}`);
        showFocusSurface();
      }
    }

    function spreadsheetSafeValue(value) {
      const text = String(value ?? '');
      return /^[=+\-@]/.test(text) ? `'${text}` : text;
    }

    function rowsToCsv(rows) {
      const escapeCell = value => `"${spreadsheetSafeValue(value).replaceAll('"', '""')}"`;
      return rows.map(row => row.map(escapeCell).join(',')).join('\n');
    }

    function rowsFor(kind) {
      if (kind === 'focus') return rowsFor(focusSource || 'overview');
      if (kind === 'overview') {
        const ids = chartComparisonIds('overview');
        return [['State', currentLabel('overview'), ...ids.map(id => comparisonLabel(id, 'overview'))], ...lifecycleCategories.en.map((name, index) => [name, lifecycleSeries[seriesSourceId('current', 'overview')][index], ...ids.map(id => lifecycleSeries[seriesSourceId(id, 'overview')][index])])];
      }
      if (kind === 'dynamics') {
        const metricKey = document.getElementById('dynamics-metric').value;
        const view = dynamicsView(metricKey, 'dynamics');
        return [['Period', ...view.ids.map(id => id === 'current' ? currentLabel('dynamics') : comparisonLabel(id, 'dynamics'))], ...view.categories.map((category, index) => [category, ...view.ids.map(id => view.series[id][index] ?? '')])];
      }
      if (kind === 'quarter') {
        const view = contributionView('quarter');
        const ids = chartComparisonIds('quarter');
        return [['Period', 'Retained', 'New', 'Reactivated', currentLabel('quarter'), ...ids.map(id => comparisonLabel(id, 'quarter'))], ...view.categories.map((category, index) => {
          const total = view.values.retained[index] + view.values.new[index] + view.values.reactivated[index];
          return [category, view.values.retained[index], view.values.new[index], view.values.reactivated[index], total, ...ids.map(id => Math.round(total * comparisonScale(id, 'quarter')))];
        })];
      }
      if (kind === 'segments' || kind === 'profile') {
        const ids = chartComparisonIds('segments');
        return [['Segment', currentLabel('segments'), ...ids.map(id => comparisonLabel(id, 'segments')), 'Share', 'Average receipt', 'Frequency per period', 'Retention'], ...segments.map(segment => [segment.name.en, segment.customers, ...ids.map(id => Math.round(segment.customers * comparisonScale(id, 'segments'))), segment.share, segment.receipt, segment.frequency, segment.retention])];
      }
      if (kind === 'migration') {
        const comparisonId = chartComparisonIds('migration')[0] || null;
        return [['From', 'To', 'Customers', 'Comparison', 'Delta percent'], ...migrationMatrix.flatMap((origin, fromIndex) => origin.map((current, toIndex) => {
          const comparison = comparisonId ? Math.max(0, Math.round(current * comparisonScale(comparisonId, 'migration') * (1 + (toIndex - fromIndex) * .008))) : '';
          return [segments[fromIndex].name.en, segments[toIndex].name.en, current, comparison, comparison ? Number((((current - comparison) / comparison) * 100).toFixed(1)) : ''];
        }))];
      }
      if (kind === 'lifecycle') {
        const buckets = periodColumnBuckets();
        const groups = lifecycleRowGroups();
        return [['Group', 'Row', ...buckets.map(bucket => bucket.label)], ...groups.flatMap(group => group.rows.map(row => [group.label, row.label, ...buckets.map(bucket => lifecycleDisplayValue(lifecycleMetric, row, bucket, groups).display)]))];
      }
      return [['State', 'Customers 2025', 'Share', 'Frequency per period'], ...lifecycleCategories.en.map((name, index) => [name, lifecycleSeries.current[index], Number((lifecycleSeries.current[index] / lifecycleTotals.current * 100).toFixed(1)), lifecycleFrequency[index]])];
    }

    function csvFor(kind) { return rowsToCsv(rowsFor(kind)); }

    function xmlEscape(value) {
      return String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&apos;');
    }

    function excelColumnName(index) {
      let value = index + 1;
      let name = '';
      while (value) { value -= 1; name = String.fromCharCode(65 + (value % 26)) + name; value = Math.floor(value / 26); }
      return name;
    }

    function worksheetXml(rows) {
      const columnCount = Math.max(1, ...rows.map(row => row.length));
      const rowCount = Math.max(1, rows.length);
      const columnWidths = Array.from({ length: columnCount }, (_, columnIndex) => Math.min(42, Math.max(10, ...rows.map(row => String(row[columnIndex] ?? '').length + 2))));
      const sheetRows = rows.map((row, rowIndex) => `<row r="${rowIndex + 1}">${row.map((value, columnIndex) => {
        const reference = `${excelColumnName(columnIndex)}${rowIndex + 1}`;
        if (typeof value === 'number' && Number.isFinite(value)) return `<c r="${reference}"><v>${value}</v></c>`;
        return `<c r="${reference}" t="inlineStr"><is><t xml:space="preserve">${xmlEscape(spreadsheetSafeValue(value))}</t></is></c>`;
      }).join('')}</row>`).join('');
      return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><dimension ref="A1:${excelColumnName(columnCount - 1)}${rowCount}"/><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>${columnWidths.map((width, index) => `<col min="${index + 1}" max="${index + 1}" width="${width}" customWidth="1"/>`).join('')}</cols><sheetData>${sheetRows}</sheetData><autoFilter ref="A1:${excelColumnName(columnCount - 1)}${rowCount}"/></worksheet>`;
    }

    const crc32Table = Array.from({ length: 256 }, (_, initial) => {
      let value = initial;
      for (let bit = 0; bit < 8; bit += 1) value = (value & 1) ? (0xedb88320 ^ (value >>> 1)) : (value >>> 1);
      return value >>> 0;
    });

    function crc32(bytes) {
      let value = 0xffffffff;
      bytes.forEach(byte => { value = crc32Table[(value ^ byte) & 0xff] ^ (value >>> 8); });
      return (value ^ 0xffffffff) >>> 0;
    }

    function appendUint16(target, value) { target.push(value & 0xff, (value >>> 8) & 0xff); }
    function appendUint32(target, value) { target.push(value & 0xff, (value >>> 8) & 0xff, (value >>> 16) & 0xff, (value >>> 24) & 0xff); }

    function storedZip(entries, mimeType) {
      const encoder = new TextEncoder();
      const localParts = [];
      const centralParts = [];
      let offset = 0;
      let centralSize = 0;
      entries.forEach(entry => {
        const name = encoder.encode(entry.name);
        const data = typeof entry.data === 'string' ? encoder.encode(entry.data) : entry.data;
        const checksum = crc32(data);
        const localHeader = [];
        appendUint32(localHeader, 0x04034b50); appendUint16(localHeader, 20); appendUint16(localHeader, 0); appendUint16(localHeader, 0); appendUint16(localHeader, 0); appendUint16(localHeader, 0x21); appendUint32(localHeader, checksum); appendUint32(localHeader, data.length); appendUint32(localHeader, data.length); appendUint16(localHeader, name.length); appendUint16(localHeader, 0);
        const localBytes = new Uint8Array(localHeader);
        localParts.push(localBytes, name, data);

        const centralHeader = [];
        appendUint32(centralHeader, 0x02014b50); appendUint16(centralHeader, 20); appendUint16(centralHeader, 20); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0x21); appendUint32(centralHeader, checksum); appendUint32(centralHeader, data.length); appendUint32(centralHeader, data.length); appendUint16(centralHeader, name.length); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint32(centralHeader, 0); appendUint32(centralHeader, offset);
        const centralBytes = new Uint8Array(centralHeader);
        centralParts.push(centralBytes, name);
        centralSize += centralBytes.length + name.length;
        offset += localBytes.length + name.length + data.length;
      });
      const end = [];
      appendUint32(end, 0x06054b50); appendUint16(end, 0); appendUint16(end, 0); appendUint16(end, entries.length); appendUint16(end, entries.length); appendUint32(end, centralSize); appendUint32(end, offset); appendUint16(end, 0);
      return new Blob([...localParts, ...centralParts, new Uint8Array(end)], { type: mimeType });
    }

    function xlsxFor(kind) {
      const rows = rowsFor(kind);
      const sheetName = 'Data';
      return storedZip([
        { name: '[Content_Types].xml', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>` },
        { name: '_rels/.rels', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>` },
        { name: 'xl/workbook.xml', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="${sheetName}" sheetId="1" r:id="rId1"/></sheets></workbook>` },
        { name: 'xl/_rels/workbook.xml.rels', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>` },
        { name: 'xl/worksheets/sheet1.xml', data: worksheetXml(rows) }
      ], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    }

    function downloadBlob() { showToast(unavailable()); }

    function exportTable() { showToast(unavailable()); }

    function svgWithAdaptiveLegend(svg, model, state, width, height) {
      if (!model?.external) return { svg, width, height };
      const margin = 22;
      const labelColumn = width >= 720 ? 112 : 22;
      const lineHeight = 27;
      let y = height + 30;
      const fragments = [];
      const definitions = [];
      model.rows.forEach((row, rowIndex) => {
        const visibleItems = row.items.filter(item => legendButtonState(state, item.seriesNames) !== 'false');
        if (!visibleItems.length) return;
        const rowStart = y;
        let x = labelColumn;
        fragments.push(`<text x="${margin}" y="${rowStart}" fill="#85868d" font-family="Inter,system-ui,sans-serif" font-size="11" font-weight="600">${xmlEscape(row.label)}</text>`);
        visibleItems.forEach((item, itemIndex) => {
          const itemText = `${item.label}${item.value ? ` · ${item.value}` : ''}`;
          const itemWidth = Math.min(Math.max(112, 44 + itemText.length * 6.7), Math.max(140, width - labelColumn - margin));
          if (x + itemWidth > width - margin && x > labelColumn) { x = labelColumn; y += lineHeight; }
          const opacity = 1;
          let fill = xmlEscape(item.color || '#9aa4ad');
          if (item.scenario === 'plan') {
            const patternId = `legend-plan-${rowIndex}-${itemIndex}`;
            definitions.push(`<pattern id="${patternId}" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#473a27"/><path d="M-1 1L1-1M0 6L6 0M5 7L7 5" stroke="#d6aa62" stroke-width="1.2"/></pattern>`);
            fill = `url(#${patternId})`;
          } else if (item.scenario === 'history') {
            const patternId = `legend-history-${rowIndex}-${itemIndex}`;
            definitions.push(`<pattern id="${patternId}" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#34383c"/><circle cx="2" cy="2" r="1" fill="#aeb4ba"/></pattern>`);
            fill = `url(#${patternId})`;
          }
          fragments.push(`<g opacity="${opacity}"><rect x="${x}" y="${y - 9}" width="18" height="9" rx="4" fill="${fill}" stroke="#ffffff" stroke-opacity=".18"/><text x="${x + 25}" y="${y}" fill="#c5c7cb" font-family="Inter,system-ui,sans-serif" font-size="11">${xmlEscape(itemText)}</text></g>`);
          x += itemWidth;
        });
        y += lineHeight;
      });
      const exportHeight = y + 7;
      const legendHeight = exportHeight - height;
      const layer = `<defs>${definitions.join('')}</defs><g><rect x="0" y="${height}" width="${width}" height="${legendHeight}" fill="#111214"/><path d="M0 ${height + .5}H${width}" stroke="#292a2e"/>${fragments.join('')}</g>`;
      const expanded = svg
        .replace(/height="[\d.]+"/, `height="${exportHeight}"`)
        .replace(/viewBox="0 0 [\d.]+ [\d.]+"/, `viewBox="0 0 ${width} ${exportHeight}"`)
        .replace('</svg>', `${layer}</svg>`);
      return { svg: expanded, width, height: exportHeight };
    }

    async function exportChart(button) {
      const chartId = button.dataset.chartExport;
      const chart = chartInstances[chartId];
      if (!chart) return;
      const format = button.dataset.format;
      const filename = `custometry-${button.dataset.exportName}-2025.${format}`;
      const artifact = svgWithAdaptiveLegend(chart.renderToSVGString({ useViewBox: true }), chartLegendModels[chartId], chartLegendState[legendStateKey(chartId)] || {}, chart.getWidth(), chart.getHeight());
      const svg = artifact.svg;
      if (format === 'svg') {
        downloadBlob(new Blob([svg], { type: 'image/svg+xml;charset=utf-8' }), filename);
      } else {
        const svgUrl = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml;charset=utf-8' }));
        const image = new Image();
        await new Promise((resolve, reject) => {
          image.onload = resolve;
          image.onerror = reject;
          image.src = svgUrl;
        });
        const ratio = 2;
        const width = artifact.width;
        const height = artifact.height;
        const canvas = document.createElement('canvas');
        canvas.width = width * ratio;
        canvas.height = height * ratio;
        const context = canvas.getContext('2d');
        context.scale(ratio, ratio);
        context.fillStyle = '#111214';
        context.fillRect(0, 0, width, height);
        context.drawImage(image, 0, 0, width, height);
        URL.revokeObjectURL(svgUrl);
        const png = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
        downloadBlob(png, filename);
      }
      button.closest('details')?.removeAttribute('open');
      showToast(uiText[locale].imageExport(format));
    }

    function applyLocale(nextLocale) {
      locale = nextLocale;
      document.documentElement.lang = locale;
      document.documentElement.dataset.locale = locale;
      document.querySelectorAll('[data-ru][data-en]').forEach(node => { node.textContent = node.dataset[locale]; });
      document.querySelectorAll('[data-ru-label][data-en-label]').forEach(node => { node.setAttribute('aria-label', node.dataset[`${locale}Label`]); });
      document.querySelectorAll('[data-ru-placeholder][data-en-placeholder]').forEach(node => { node.placeholder = node.dataset[`${locale}Placeholder`]; });
      document.querySelectorAll('.sidebar button[aria-label]').forEach(node => { node.title = node.getAttribute('aria-label'); });
      syncAllExportControls();
      document.getElementById('locale-summary').textContent = locale === 'ru' ? 'Русский' : 'English';
      const metricSelect = document.getElementById('dynamics-metric');
      [...metricSelect.options].forEach(option => { option.textContent = monthlyData[option.value].label[locale]; });
      updateSidebarLabel();
      const inspectorToggle = document.getElementById('context-open');
      const inspectorLabel = workspace.dataset.context === 'open' ? (locale === 'ru' ? 'Закрыть инспектор отчёта' : 'Close report inspector') : (locale === 'ru' ? 'Открыть инспектор отчёта' : 'Open report inspector');
      inspectorToggle.setAttribute('aria-label', inspectorLabel);
      inspectorToggle.title = inspectorLabel;
      renderKpis();
      renderPicker();
      renderLifecycleTable();
      renderOverviewTable();
      renderDynamicsTable();
      renderQuarterTable();
      renderSegmentTables();
      renderQuickFilterValues();
      renderAdvancedConditions();
      updateContextSummary();
      if (!document.getElementById('focus-surface').hidden) showFocusSurface();
    }

    const navigationSections = {
      overview: {
        title: { ru: 'Обзор', en: 'Overview' },
        items: [
          { id: 'workspace-overview', icon: 'i-home', label: { ru: 'Обзор рабочего пространства', en: 'Workspace overview' } },
          { id: 'recent-activity', icon: 'i-cycle', label: { ru: 'Последняя активность', en: 'Recent activity' } }
        ]
      },
      analytics: {
        title: { ru: 'Аналитика', en: 'Analytics' },
        items: [
          { id: 'customer-base', icon: 'i-users', label: { ru: 'Клиентская база', en: 'Customer base' }, current: true },
          { id: 'analytics-reports', icon: 'i-analytics', label: { ru: 'Аналитические отчёты', en: 'Analytics reports' }, children: [
            { id: 'sales', icon: 'i-receipt', label: { ru: 'Продажи', en: 'Sales' } },
            { id: 'rfm', icon: 'i-rfm', label: { ru: 'RFM', en: 'RFM' } },
            { id: 'cohorts', icon: 'i-cohort', label: { ru: 'Когорты', en: 'Cohorts' } },
            { id: 'lifecycle', icon: 'i-cycle', label: { ru: 'Жизненный цикл', en: 'Lifecycle' } },
            { id: 'basket', icon: 'i-basket', label: { ru: 'Корзина', en: 'Basket' } },
            { id: 'stores-channels', icon: 'i-store', label: { ru: 'Магазины и каналы', en: 'Stores & channels' } },
            { id: 'margin-discounts', icon: 'i-percent', label: { ru: 'Маржа и скидки', en: 'Margin & discounts' } },
            { id: 'products-categories', icon: 'i-package', label: { ru: 'Товары и категории', en: 'Products & categories' } }
          ], open: true }
        ]
      },
      models: {
        title: { ru: 'Модели и аудитории', en: 'Models & audiences' },
        items: [
          { id: 'segments', icon: 'i-cohort', label: { ru: 'Сегменты', en: 'Segments' } },
          { id: 'forecasting', icon: 'i-forecast', label: { ru: 'Прогнозирование', en: 'Forecasting' } }
        ]
      },
      results: {
        title: { ru: 'Результаты', en: 'Results' },
        items: [
          { id: 'dashboards', icon: 'i-dashboard', label: { ru: 'Дашборды', en: 'Dashboards' } },
          { id: 'reports-export', icon: 'i-file', label: { ru: 'Отчёты и экспорт', en: 'Reports & exports' } }
        ]
      },
      system: {
        title: { ru: 'Данные и управление', en: 'Data & management' },
        items: [
          { id: 'data-foundation', icon: 'i-database', label: { ru: 'Данные', en: 'Data' }, children: [
            { id: 'sources-catalog', icon: 'i-database', label: { ru: 'Источники и каталог', en: 'Sources & catalog' } },
            { id: 'models-metrics', icon: 'i-data-model', label: { ru: 'Модели и метрики', en: 'Models & metrics' } },
            { id: 'data-quality', icon: 'i-quality', label: { ru: 'Качество данных', en: 'Data quality' } }
          ], open: true },
          { id: 'operations', icon: 'i-settings', label: { ru: 'Управление', en: 'Management' }, children: [
            { id: 'pipelines-runs', icon: 'i-pipeline', label: { ru: 'Pipelines и запуски', en: 'Pipelines & runs' } },
            { id: 'administration', icon: 'i-settings', label: { ru: 'Администрирование', en: 'Administration' } }
          ] }
        ]
      },
      help: {
        title: { ru: 'Помощь', en: 'Help' },
        items: [
          { id: 'help-center', icon: 'i-help', label: { ru: 'Справочный центр', en: 'Help center' } },
          { id: 'support', icon: 'i-message', label: { ru: 'Поддержка', en: 'Support' } }
        ]
      },
      profile: {
        title: { ru: 'Профиль', en: 'Profile' },
        items: [
          { id: 'profile-settings', icon: 'i-settings', label: { ru: 'Настройки профиля', en: 'Profile settings' } },
          { id: 'access', icon: 'i-shield', label: { ru: 'Доступ и роли', en: 'Access & roles' } }
        ]
      }
    };
    let openNavigationSection = null;
    let navigationTrigger = null;

    function navigationItemMarkup(item, child = false) {
      const label = item.label[locale];
      if (item.children) {
        return `<details class="nav-context-disclosure" data-nav-disclosure="${item.id}"${item.open ? ' open' : ''}><summary><svg class="icon icon--small" aria-hidden="true"><use href="#${item.icon}"/></svg><span>${label}</span><svg class="icon icon--small nav-chevron" aria-hidden="true"><use href="#i-chevron"/></svg></summary><div class="nav-context-children">${item.children.map(childItem => navigationItemMarkup(childItem, true)).join('')}</div></details>`;
      }
      return `<button class="nav-context-link" type="button" data-nav-destination="${item.id}"${item.current ? ' aria-current="page"' : ''}><svg class="icon icon--small" aria-hidden="true"><use href="#${item.icon}"/></svg><span>${label}</span>${child ? '' : '<span aria-hidden="true">›</span>'}</button>`;
    }

    function bindNavigationDestinations() {
      document.querySelectorAll('#nav-context-body [data-nav-destination]').forEach(button => button.addEventListener('click', () => {
        if (button.dataset.navDestination !== 'customer-base') showToast(uiText[locale].placeholder);
        if (matchMedia('(max-width: 820px)').matches) closeNavigationContext(true);
      }));
    }

    function renderNavigationContext(section, switching = false) {
      const spec = navigationSections[section];
      if (!spec) return;
      const panel = document.getElementById('nav-context-panel');
      if (switching) panel.classList.add('is-switching');
      document.getElementById('nav-context-title').textContent = spec.title[locale];
      document.getElementById('nav-context-body').innerHTML = `<div class="nav-context-list">${spec.items.map(item => navigationItemMarkup(item)).join('')}</div>`;
      bindNavigationDestinations();
      document.getElementById('nav-context-status').textContent = `${spec.title[locale]} · ${locale === 'ru' ? 'меню раздела обновлено' : 'section menu updated'}`;
      if (switching) requestAnimationFrame(() => panel.classList.remove('is-switching'));
    }

    function setNarrowNavigationModal(active) {
      const narrow = matchMedia('(max-width: 820px)').matches;
      workspace.inert = Boolean(active && narrow);
      document.getElementById('nav-context-backdrop').hidden = !(active && narrow);
    }

    function openNavigationContext(section, trigger) {
      if (openNavigationSection === section && shell.dataset.navContext === 'open') {
        closeNavigationContext(true);
        return;
      }
      const switching = shell.dataset.navContext === 'open';
      openNavigationSection = section;
      navigationTrigger = trigger;
      document.querySelectorAll('[data-nav-root]').forEach(button => button.setAttribute('aria-expanded', button === trigger ? 'true' : 'false'));
      renderNavigationContext(section, switching);
      shell.dataset.navContext = 'open';
      document.getElementById('nav-context-panel').setAttribute('aria-hidden', 'false');
      document.getElementById('nav-context-panel').inert = false;
      setNarrowNavigationModal(true);
    }

    function closeNavigationContext(returnFocus = false) {
      shell.dataset.navContext = 'closed';
      document.querySelectorAll('[data-nav-root]').forEach(button => button.setAttribute('aria-expanded', 'false'));
      document.getElementById('nav-context-panel').setAttribute('aria-hidden', 'true');
      document.getElementById('nav-context-panel').inert = true;
      setNarrowNavigationModal(false);
      const trigger = navigationTrigger;
      openNavigationSection = null;
      if (returnFocus) trigger?.focus();
    }

    function updateSidebarLabel() {
      document.querySelectorAll('.sidebar button[aria-label]').forEach(button => { button.title = button.getAttribute('aria-label'); });
      if (openNavigationSection) renderNavigationContext(openNavigationSection);
    }

    function restoreNavigationState() {
      localStorage.removeItem(navStorageKey);
      shell.dataset.sidebar = 'rail';
      shell.dataset.navContext = 'closed';
      document.getElementById('nav-context-panel').setAttribute('aria-hidden', 'true');
      document.getElementById('nav-context-panel').inert = true;
      setNarrowNavigationModal(false);
    }

    let activePopover = null;

    function dismissPopover(popover = activePopover, returnFocus = false) {
      if (!popover) return;
      const trigger = document.getElementById(popover.dataset.triggerId || '');
      if (popover.matches(':popover-open')) popover.hidePopover();
      if (activePopover === popover) activePopover = null;
      trigger?.setAttribute('aria-expanded', 'false');
      if (returnFocus) trigger?.focus();
    }

    function closeMenuPopovers(except = null) {
      document.querySelectorAll('.menu-popover:popover-open').forEach(popover => {
        if (popover !== except) dismissPopover(popover);
      });
    }

    function positionPopover(trigger, popover) {
      const triggerRect = trigger.getBoundingClientRect();
      const popoverRect = popover.getBoundingClientRect();
      const gap = 7;
      const edge = 10;
      let left = triggerRect.left;
      if (popover.classList.contains('filter-popover') || trigger.id === 'view-menu-open' || trigger.id === 'appearance-menu-open' || popover.id === 'chart-settings-popover') left = triggerRect.right - popoverRect.width;
      left = Math.max(edge, Math.min(left, innerWidth - popoverRect.width - edge));
      let top = triggerRect.bottom + gap;
      if (top + popoverRect.height > innerHeight - edge) top = Math.max(edge, triggerRect.top - popoverRect.height - gap);
      popover.style.left = `${Math.round(left)}px`;
      popover.style.top = `${Math.round(top)}px`;
    }

    function openAnchoredPopover(trigger, popover, focus = true) {
      const wasOpen = activePopover === popover && popover.matches(':popover-open');
      if (activePopover && activePopover !== popover) dismissPopover(activePopover);
      closeMenuPopovers(popover);
      if (wasOpen) { dismissPopover(popover, true); return; }
      popover.dataset.triggerId = trigger.id;
      popover.showPopover();
      activePopover = popover;
      positionPopover(trigger, popover);
      trigger.setAttribute('aria-expanded', 'true');
      if (focus) requestAnimationFrame(() => {
        if (activePopover === popover && popover.matches(':popover-open')) popover.querySelector('button:not([disabled]), input:not([disabled])')?.focus();
      });
    }

    function openKpiPopover(trigger) {
      const popover = document.getElementById('kpi-popover');
      draftMetricIds = [...selectedMetricIds];
      renderPicker();
      openAnchoredPopover(trigger, popover);
    }

    document.addEventListener('pointerdown', () => { document.documentElement.dataset.inputModality = 'pointer'; }, true);
    document.addEventListener('keydown', event => {
      if (['Tab', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Home', 'End', 'Enter', ' '].includes(event.key)) document.documentElement.dataset.inputModality = 'keyboard';
    }, true);

    document.querySelectorAll('[data-nav-root]').forEach(button => button.addEventListener('click', () => openNavigationContext(button.dataset.navRoot, button)));
    document.getElementById('nav-context-close').addEventListener('click', () => closeNavigationContext(true));
    document.getElementById('nav-context-backdrop').addEventListener('pointerdown', () => closeNavigationContext(true));
    document.addEventListener('pointerdown', event => {
      if (shell.dataset.navContext !== 'open' || matchMedia('(max-width: 820px)').matches) return;
      if (event.target.closest('#nav-context-panel, .sidebar')) return;
      closeNavigationContext(false);
    }, true);
    document.getElementById('locale-toggle').addEventListener('click', () => applyLocale(locale === 'ru' ? 'en' : 'ru'));

    document.querySelectorAll('[data-page]').forEach((tab, index, tabs) => {
      tab.addEventListener('click', () => activatePage(tab.dataset.page));
      tab.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let target = index;
        if (event.key === 'ArrowLeft') target = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'ArrowRight') target = (index + 1) % tabs.length;
        if (event.key === 'Home') target = 0;
        if (event.key === 'End') target = tabs.length - 1;
        activatePage(tabs[target].dataset.page, true, true);
      });
    });

    document.querySelectorAll('[data-view-button]').forEach(button => button.addEventListener('click', () => setView(button.dataset.viewButton, button.dataset.view)));
    let activeChartSettingsScope = 'overview';
    const chartTypeCatalog = {
      overview: [
        { id: 'trend', icon: 'i-line', ru: 'Динамика · small multiples', en: 'Trend · small multiples' },
        { id: 'bar', icon: 'i-bars', ru: 'Снимок · столбцы', en: 'Snapshot · bars' },
        { id: 'composition', icon: 'i-composition', ru: 'Состав 100%', en: '100% composition' },
        { id: 'heatmap', icon: 'i-heatmap', ru: 'Тепловая карта', en: 'Heatmap' }
      ],
      dynamics: [
        { id: 'line', icon: 'i-line', ru: 'Линия', en: 'Line' },
        { id: 'bar', icon: 'i-bars', ru: 'Столбцы', en: 'Bars' }
      ],
      segments: [
        { id: 'horizontal', icon: 'i-horizontal-bars', ru: 'Горизонтальные столбцы', en: 'Horizontal bars' },
        { id: 'vertical', icon: 'i-bars', ru: 'Вертикальные столбцы', en: 'Vertical columns' }
      ]
    };
    function currentChartType(scope) {
      return scope === 'dynamics' ? dynamicsChartType : scope === 'segments' ? segmentsChartType : overviewChartType;
    }
    function renderChartSettingsPopover(scope = activeChartSettingsScope) {
      activeChartSettingsScope = chartTypeCatalog[scope] ? scope : 'overview';
      const catalog = chartTypeCatalog[activeChartSettingsScope];
      const current = currentChartType(activeChartSettingsScope);
      const scopeNames = { overview: { ru: 'Обзор', en: 'Overview' }, dynamics: { ru: 'Динамика', en: 'Dynamics' }, segments: { ru: 'Сегменты', en: 'Segments' } };
      document.getElementById('chart-settings-heading').textContent = `${locale === 'ru' ? 'Настройки графика' : 'Chart settings'} · ${scopeNames[activeChartSettingsScope][locale]}`;
      const options = document.getElementById('chart-settings-options');
      options.innerHTML = catalog.map(item => `<button class="menu-row${item.id === current ? ' is-selected' : ''}" type="button" data-chart-type="${item.id}" aria-pressed="${item.id === current}"><svg class="icon icon--small" aria-hidden="true"><use href="#${item.icon}"/></svg><span>${item[locale]}</span><svg class="icon menu-selection" aria-hidden="true"><use href="#i-check"/></svg></button>`).join('') + (activeChartSettingsScope === 'overview' ? `<div class="menu-separator"></div><button class="menu-row" id="insight-menu-toggle" type="button" aria-pressed="${!document.getElementById('overview-insight').hidden}"><svg class="icon icon--small" aria-hidden="true"><use href="#i-eye"/></svg><span>${locale === 'ru' ? 'Проверенный вывод' : 'Reviewed finding'}</span><svg class="icon menu-selection" aria-hidden="true"><use href="#i-check"/></svg></button><div class="menu-note">${locale === 'ru' ? 'Вывод — ручная заметка аналитика. По умолчанию она скрыта.' : 'The finding is an analyst-authored note and is hidden by default.'}</div>` : '');
      options.querySelectorAll('[data-chart-type]').forEach(button => button.addEventListener('click', () => {
        if (activeChartSettingsScope === 'overview') { overviewChartType = button.dataset.chartType; overviewChartTypeManual = true; }
        if (activeChartSettingsScope === 'dynamics') dynamicsChartType = button.dataset.chartType === 'bar' ? 'bar' : 'line';
        if (activeChartSettingsScope === 'segments') segmentsChartType = button.dataset.chartType === 'vertical' ? 'vertical' : 'horizontal';
        syncChartSettingsPopover();
        renderOverviewTable();
        renderDynamicsTable();
        renderSegmentTables();
        updateAllCharts();
        dismissPopover(document.getElementById('chart-settings-popover'), true);
      }));
      document.getElementById('insight-menu-toggle')?.addEventListener('click', () => setInsightVisible(document.getElementById('overview-insight').hidden));
    }
    function syncChartSettingsPopover() {
      const overviewLabels = Object.fromEntries(chartTypeCatalog.overview.map(item => [item.id, item]));
      document.getElementById('overview-subtitle').textContent = `${chartTimeSummary('overview')} · ${overviewLabels[overviewChartType][locale]}`;
      document.querySelectorAll('[data-chart-settings-scope]').forEach(trigger => {
        const scope = trigger.dataset.chartSettingsScope;
        const item = chartTypeCatalog[scope].find(candidate => candidate.id === currentChartType(scope));
        const label = `${locale === 'ru' ? 'Настройки графика' : 'Chart settings'}: ${item[locale]}`;
        trigger.setAttribute('aria-label', label);
        trigger.title = label;
      });
      const popover = document.getElementById('chart-settings-popover');
      if (popover.matches(':popover-open')) renderChartSettingsPopover(activeChartSettingsScope);
    }
    function setInsightVisible(visible) {
      const insight = document.getElementById('overview-insight');
      insight.hidden = !visible;
      document.getElementById('insight-toggle').setAttribute('aria-expanded', visible ? 'true' : 'false');
      document.getElementById('insight-menu-toggle')?.setAttribute('aria-pressed', visible ? 'true' : 'false');
    }
    document.querySelectorAll('[data-chart-settings-scope]').forEach(trigger => trigger.addEventListener('click', () => {
      renderChartSettingsPopover(trigger.dataset.chartSettingsScope);
      openAnchoredPopover(trigger, document.getElementById('chart-settings-popover'));
    }));
    document.getElementById('lifecycle-metric').addEventListener('change', event => { lifecycleMetric = event.target.value; renderLifecycleTable(); });
    document.getElementById('lifecycle-delta-base').addEventListener('change', event => { lifecycleDeltaBase = event.target.value; renderLifecycleTable(); });
    document.getElementById('dynamics-metric').addEventListener('change', () => { renderDynamicsTable(); if (chartInstances['dynamics-chart']) chartInstances['dynamics-chart'].setOption(dynamicsOption(false), true); if (focusSource === 'dynamics' && chartInstances['focus-chart']) chartInstances['focus-chart'].setOption(dynamicsOption(true), true); });

    document.getElementById('insight-toggle').addEventListener('click', () => setInsightVisible(document.getElementById('overview-insight').hidden));

    document.getElementById('context-open').addEventListener('click', () => workspace.dataset.context === 'open' ? closeContext() : openContext());
    document.querySelectorAll('[data-inspector-tab]').forEach((button, index, tabs) => {
      button.addEventListener('click', () => activateInspectorPanel(button.dataset.inspectorTab));
      button.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let target = index;
        if (event.key === 'ArrowLeft') target = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'ArrowRight') target = (index + 1) % tabs.length;
        if (event.key === 'Home') target = 0;
        if (event.key === 'End') target = tabs.length - 1;
        activateInspectorPanel(tabs[target].dataset.inspectorTab);
        tabs[target].focus();
      });
    });
    document.querySelectorAll('[data-context-jump]').forEach(button => button.addEventListener('click', () => openContext(button.dataset.contextJump)));
    document.querySelectorAll('[data-scroll-target]').forEach(button => button.addEventListener('click', () => { closeContext(false); document.getElementById(button.dataset.scrollTarget)?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }));
    document.querySelectorAll('input[name="comparison"]').forEach(input => input.addEventListener('change', applyComparisonControls));
    document.getElementById('primary-comparison').addEventListener('change', applyComparisonControls);
    document.getElementById('context-only-actual').addEventListener('change', event => {
      if (event.target.checked) setOnlyActual();
      else { selectedComparisons = new Set(['2024']); primaryComparison = '2024'; document.querySelector('input[name="comparison"][value="2024"]').checked = true; updateContextSummary(); }
    });
    document.getElementById('context-apply').addEventListener('click', () => {
      appliedAdvancedGroups = structuredClone(advancedGroups);
      applyComparisonControls();
      renderAdvancedConditions();
      closeContext();
      showToast(uiText[locale].applied);
    });
    document.getElementById('context-reset').addEventListener('click', resetContext);
    document.getElementById('report-style-select').addEventListener('change', event => {
      reportStyleTemplate = styleTemplates[event.target.value] ? event.target.value : 'default';
      renderStyleControls();
      updateAllCharts();
      updateReportStateUi();
    });

    document.querySelectorAll('[data-toolbar-menu]').forEach(trigger => trigger.addEventListener('click', () => {
      openAnchoredPopover(trigger, document.getElementById(`${trigger.dataset.toolbarMenu}-popover`));
    }));
    document.querySelectorAll('[data-period-grain]').forEach(button => button.addEventListener('click', () => {
      reportPeriod.grain = button.dataset.periodGrain;
      reportPeriod.value = defaultPeriodValue(reportPeriod.grain);
      updateContextSummary();
    }));
    document.getElementById('period-grain-select').addEventListener('change', event => {
      reportPeriod.grain = event.target.value;
      reportPeriod.value = defaultPeriodValue(reportPeriod.grain);
      updateContextSummary();
    });
    document.getElementById('period-select').addEventListener('change', event => {
      reportPeriod.value = event.target.value;
      updateContextSummary();
    });
    document.querySelectorAll('[data-chart-period]').forEach(select => select.addEventListener('change', event => {
      chartPeriodOverrides[event.target.dataset.chartPeriod].grain = event.target.value;
      renderOverviewTable(); renderDynamicsTable(); renderQuarterTable(); renderSegmentTables(); syncChartSettingsPopover(); updateAllCharts(); updateReportStateUi();
    }));
    document.querySelectorAll('[data-chart-comparison]').forEach(select => select.addEventListener('change', event => {
      chartPeriodOverrides[event.target.dataset.chartComparison].comparison = event.target.value;
      renderOverviewTable(); renderDynamicsTable(); renderQuarterTable(); renderSegmentTables(); syncChartSettingsPopover(); updateAllCharts(); updateReportStateUi();
    }));
    document.querySelectorAll('.menu-popover').forEach(popover => popover.addEventListener('toggle', event => {
      if (event.newState !== 'closed') return;
      const trigger = document.getElementById(popover.dataset.triggerId || '');
      trigger?.setAttribute('aria-expanded', 'false');
      if (activePopover === popover) activePopover = null;
    }));
    document.querySelectorAll('[data-popover-close]').forEach(button => button.addEventListener('click', () => dismissPopover(document.getElementById(button.dataset.popoverClose), true)));
    document.addEventListener('pointerdown', event => {
      document.querySelectorAll('.block-command[open], .chart-export[open]').forEach(details => {
        if (!details.contains(event.target)) details.removeAttribute('open');
      });
      if (!activePopover?.matches(':popover-open')) return;
      const trigger = document.getElementById(activePopover.dataset.triggerId || '');
      if (!activePopover.contains(event.target) && !trigger?.contains(event.target)) dismissPopover(activePopover);
    }, true);
    document.querySelectorAll('[data-open-inspector]').forEach(button => button.addEventListener('click', () => {
      closeMenuPopovers();
      openContext(button.dataset.openInspector);
    }));
    document.querySelectorAll('[data-filter-category]').forEach(button => button.addEventListener('click', () => renderQuickFilterValues(button.dataset.filterCategory)));
    document.querySelectorAll('[data-quick-comparison]').forEach(input => input.addEventListener('change', () => {
      const checked = [...document.querySelectorAll('[data-quick-comparison]:checked')].map(item => item.value);
      selectedComparisons = new Set(checked);
      primaryComparison = checked.length ? (selectedComparisons.has(primaryComparison) ? primaryComparison : selectedComparisons.has('2024') ? '2024' : checked[0]) : null;
      if (primaryComparison) document.getElementById('primary-comparison').value = primaryComparison;
      document.querySelectorAll('input[name="comparison"]').forEach(item => { item.checked = selectedComparisons.has(item.value); });
      updateContextSummary();
    }));
    document.getElementById('only-actual-toggle').addEventListener('click', setOnlyActual);

    document.getElementById('all-stores').addEventListener('change', event => {
      if (event.target.checked) {
        selectedStores.clear();
        document.querySelectorAll('[data-store-option]').forEach(input => { input.checked = false; });
      } else if (!selectedStores.size) event.target.checked = true;
      updateReportStateUi();
      if (groupDimensions.includes('store')) { renderLifecycleTable(); updateAllCharts(); }
    });
    document.querySelectorAll('[data-store-option]').forEach(input => input.addEventListener('change', () => {
      selectedStores = new Set([...document.querySelectorAll('[data-store-option]:checked')].map(item => item.value));
      document.getElementById('all-stores').checked = selectedStores.size === 0;
      updateReportStateUi();
      if (groupDimensions.includes('store')) { renderLifecycleTable(); updateAllCharts(); }
    }));

    document.getElementById('advanced-filter-logic').addEventListener('change', event => { advancedFilterLogic = event.target.value; renderAdvancedConditions(); });
    document.getElementById('advanced-condition-add').addEventListener('click', () => {
      if (!advancedGroups.length) advancedGroups.push(createAdvancedGroup());
      else advancedGroups[0].conditions.push(createAdvancedCondition());
      renderAdvancedConditions();
    });
    document.getElementById('advanced-group-add').addEventListener('click', () => { advancedGroups.push(createAdvancedGroup('order_status', 'and')); renderAdvancedConditions(); });
    document.getElementById('advanced-filter-search').addEventListener('keydown', event => {
      if (event.key !== 'Enter') return;
      event.preventDefault();
      const needle = event.target.value.trim().toLocaleLowerCase(localeCode());
      const match = Object.entries(advancedFilterCatalog).find(([, spec]) => [spec.label[locale], spec.group[locale], spec.nestedHint?.[locale]].filter(Boolean).some(value => value.toLocaleLowerCase(localeCode()).includes(needle)));
      if (!match) { showToast(locale === 'ru' ? 'Признак не найден' : 'Field not found'); return; }
      if (!advancedGroups.length) advancedGroups.push(createAdvancedGroup(match[0]));
      else advancedGroups[0].conditions.push(createAdvancedCondition(match[0]));
      event.target.value = '';
      renderAdvancedConditions();
    });
    document.getElementById('advanced-filter-reset').addEventListener('click', () => { advancedGroups = []; advancedFilterLogic = 'and'; renderAdvancedConditions(); });

    document.getElementById('copy-link').addEventListener('click', async () => {
      const snapshotUrl = buildSnapshotUrl();
      try { await navigator.clipboard.writeText(snapshotUrl); showToast(uiText[locale].copied); }
      catch (_) { showToast(uiText[locale].copyFallback); }
    });

    const kpiPopover = document.getElementById('kpi-popover');
    document.getElementById('kpi-open').addEventListener('click', event => openKpiPopover(event.currentTarget));
    document.getElementById('view-kpi-open').addEventListener('click', () => { dismissPopover(document.getElementById('view-popover')); openKpiPopover(document.getElementById('view-menu-open')); });
    document.getElementById('kpi-save').addEventListener('click', () => { selectedMetricIds = [...draftMetricIds]; localStorage.setItem(storageKey, JSON.stringify(selectedMetricIds)); renderKpis(); kpiStatus.textContent = uiText[locale].saved; setTimeout(() => dismissPopover(kpiPopover), 140); });
    document.getElementById('kpi-reset').addEventListener('click', () => { selectedMetricIds = [...defaultMetricIds]; draftMetricIds = [...defaultMetricIds]; localStorage.removeItem(storageKey); renderKpis(); renderPicker(); kpiStatus.textContent = uiText[locale].defaultStatus; });
    document.getElementById('save-analysis-view').addEventListener('click', () => { saveAnalysisView(); dismissPopover(document.getElementById('view-popover'), true); });
    document.getElementById('personal-analysis-view-row').addEventListener('click', applyStoredAnalysisView);
    document.getElementById('published-analysis-view-row').addEventListener('click', () => { personalAnalysisViewActive = false; renderSavedAnalysisView(); showToast(locale === 'ru' ? 'Применён опубликованный вид' : 'Published view applied'); });

    document.getElementById('comments-open').addEventListener('click', () => document.getElementById('comments-dialog').showModal());
    document.getElementById('comments-inline').addEventListener('click', () => document.getElementById('comments-dialog').showModal());
    document.getElementById('trust-open').addEventListener('click', () => document.getElementById('trust-dialog').showModal());
    document.getElementById('focus-trust').addEventListener('click', () => document.getElementById('trust-dialog').showModal());
    document.getElementById('email-open').addEventListener('click', () => { updateSharePreview(); document.getElementById('email-dialog').showModal(); });
    document.getElementById('email-form').addEventListener('submit', event => { event.preventDefault(); document.getElementById('email-dialog').close(); showToast(uiText[locale].email); });
    document.querySelectorAll('[data-dialog-close]').forEach(button => button.addEventListener('click', () => document.getElementById(button.dataset.dialogClose).close()));
    document.querySelectorAll('[data-focus-open]').forEach(button => button.addEventListener('click', () => {
      const tableView = document.querySelector(`[data-table-view="${button.dataset.focusOpen}"]`);
      const anchor = button.dataset.focusOpen !== 'overview' && tableView && !tableView.hidden ? 'table' : button.dataset.focusAnchor;
      openFocus(button.dataset.focusOpen, button, anchor);
    }));
    document.querySelectorAll('[data-focus-jump]').forEach(button => button.addEventListener('click', () => {
      focusAnchor = button.dataset.focusJump === 'table' ? 'table' : 'chart';
      document.getElementById(focusAnchor === 'table' ? 'focus-table-section' : 'focus-chart-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
    document.getElementById('focus-close').addEventListener('click', closeFocus);
    document.getElementById('focus-reset').addEventListener('click', () => chartInstances['focus-chart']?.dispatchAction({ type: 'dataZoom', start: 0, end: 100 }));
    document.querySelectorAll('[data-table-export]').forEach(button => button.addEventListener('click', () => exportTable(button)));
    document.querySelectorAll('[data-chart-export]').forEach(button => button.addEventListener('click', () => exportChart(button)));
    document.querySelectorAll('[data-placeholder-nav]').forEach(button => button.addEventListener('click', () => showToast(uiText[locale].placeholder)));

    document.addEventListener('keydown', event => {
      const focusSurface = document.getElementById('focus-surface');
      const navPanel = document.getElementById('nav-context-panel');
      if (shell.dataset.navContext === 'open' && matchMedia('(max-width: 820px)').matches && event.key === 'Tab') {
        const focusable = [...navPanel.querySelectorAll('button:not([disabled]), summary, a[href], [tabindex="0"]')].filter(element => element.offsetParent !== null);
        if (focusable.length) {
          const first = focusable[0];
          const last = focusable[focusable.length - 1];
          if (!navPanel.contains(document.activeElement)) { event.preventDefault(); first.focus(); return; }
          if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); return; }
          if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); return; }
        }
      }
      if (!focusSurface.hidden && event.key === 'Tab') {
        const focusable = [...focusSurface.querySelectorAll('button:not([disabled]), a[href], select:not([disabled]), input:not([disabled]), [tabindex="0"]')].filter(element => element.offsetParent !== null);
        if (focusable.length) {
          const first = focusable[0];
          const last = focusable[focusable.length - 1];
          if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); return; }
          if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); return; }
        }
      }
      if (event.key !== 'Escape') return;
      if (shell.dataset.navContext === 'open') { event.preventDefault(); closeNavigationContext(true); return; }
      const openDetails = document.querySelector('.block-command[open], .chart-export[open]');
      if (openDetails) { event.preventDefault(); openDetails.removeAttribute('open'); openDetails.querySelector('summary')?.focus(); return; }
      if (activePopover?.matches(':popover-open')) { event.preventDefault(); dismissPopover(activePopover, true); return; }
      if (document.querySelector('dialog[open]')) return;
      if (!document.getElementById('focus-surface').hidden) { closeFocus(); return; }
      if (workspace.dataset.context === 'open') closeContext();
    });

    let adaptiveChartResizeFrame = 0;
    addEventListener('popstate', () => { showFocusSurface(); activatePage((location.hash || '#overview').slice(1), false); });
    addEventListener('resize', () => {
      setNarrowNavigationModal(shell.dataset.navContext === 'open');
      Object.values(chartInstances).forEach(chart => chart.resize());
      scheduleSharedTableGeometry();
      cancelAnimationFrame(adaptiveChartResizeFrame);
      adaptiveChartResizeFrame = requestAnimationFrame(() => updateAllCharts());
    });

    restoreNavigationState();
    renderQuarterTable();
    renderSegmentTables();
    applyLocale('ru');
    activatePage(currentPage, false);
    showFocusSurface();
  
// Source controls bind to explicit application actions. No fixture calculation
// or prototype storage participates in the report's result or saved identity.
let synchronizing=false;
function refreshData(){
 const model=bridge.model();
 if(model.workspace){if(locale!==model.locale)applyLocale(model.locale);const title=document.querySelector(".title-row h1");title.removeAttribute("data-ru");title.removeAttribute("data-en");title.textContent=model.title;document.querySelector(".status-pill").textContent=model.status;
  const values={'period-summary':model.workspaceChrome.period,'comparison-summary':model.workspaceChrome.comparison,'stores-summary':model.workspaceChrome.stores,'groupby-summary':model.workspaceChrome.grain,'filters-summary':locale==='ru'?'Контекст':'Context'};
  for(const [id,value] of Object.entries(values)){const n=document.getElementById(id);n.textContent=value;const b=n.closest('button');b.removeAttribute('data-ru-label');b.removeAttribute('data-en-label');b.setAttribute('aria-label',value);}
  document.querySelectorAll('[data-chart-export],[data-table-export],#share-open,#comments-open,#trust-open').forEach(n=>{n.disabled=true;n.title=locale==='ru'?'Недоступно':'Unavailable';});
  document.querySelectorAll('#comments-open [aria-hidden=true]:not(svg)').forEach(n=>n.textContent='0');
  const save=document.getElementById('save-analysis-view');save.disabled=model.busy||model.unapplied||model.preview||model.conflict;
  document.querySelectorAll('[data-page="dynamics"],[data-page="segments"],[data-page="findings"]').forEach(n=>{n.disabled=true;n.title=locale==='ru'?'Недоступно для этого отчёта':'Unavailable for this report';});
  return;}
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
 if(bridge.model().workspace&&target.matches('#period-menu-open,#stores-menu-open,#filters-menu-open,#groupby-menu-open,#comparison-menu-open,#context-open')){event.preventDefault();event.stopImmediatePropagation();bridge.inspector(target.id==='comparison-menu-open'?'chart':target.id==='context-open'?'set':'context',target);return;}
 if(bridge.model().workspace&&target.matches('[data-nav-destination=administration]')){event.preventDefault();event.stopImmediatePropagation();const settings=document.getElementById('workspace-calendar-settings');if(settings)settings.open=true;settings?.scrollIntoView();document.getElementById('workspace-calendar-settings')?.focus();return;}
 if(bridge.model().workspace&&target.matches('#save-analysis-view')){event.preventDefault();event.stopImmediatePropagation();bridge.save(bridge.model().title);return;}
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

}
