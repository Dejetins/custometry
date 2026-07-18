---
document_family_id: CUSTOMETRY-UI-BLUEPRINT
document_id: CUSTOMETRY-UI-BLUEPRINT-RU
title: Custometry — UI/UX blueprint Web-платформы
ui_spec_version: 0.6.1-draft
source_product_spec: 0.9.1-draft
source_documents:
  - ./custometry-technical-blueprint-ru.md
  - ./custometry-technical-blueprint-human-ru.md
status: active_design_iteration
normative: false
language: ru
created_at: 2026-07-15
updated_at: 2026-07-19
target: responsive_desktop_first_web_application
design_tool: penpot
design_phase: phase_1_foundations_components_screens
---

# Custometry — полный UI/UX blueprint Web-платформы

## 0. Статус и назначение

Этот документ переводит продуктовый blueprint Custometry `0.9.1-draft` в проектируемую структуру Web UI: информационную архитектуру, маршруты, страницы, компоненты, состояния, взаимодействия, accessibility, responsive-поведение и план Penpot-рендеров.

Документ является производным design-контрактом и не изменяет нормативную продуктовую спецификацию. Если UI-решение противоречит `custometry-technical-blueprint-ru.md`, действует machine blueprint. Новая бизнес-функция сначала должна появиться в двух продуктовых blueprint, а уже затем — здесь.

Текущий результат Phase 1:

- действующий Penpot baseline содержит Foundations темы «Иней / Frost», библиотеку компонентов и 91 route-level frame; полный product target содержит **110 основных route-level страниц**;
- отдельно определены overlays, drawers, modals и обязательные состояния;
- в Penpot синхронизированы 47 pages, 68 local components, 91 route-level frame, 5 system surfaces и 23 overlay/state frame;
- добавлены canonical URL/history, production motion, system/help surfaces и navigation guards;
- expanded sidebar переведён на Lucide icon + label, collapsed/tablet sidebar — на icon-only без буквенных сокращений;
- report-like surfaces получили общий compact header/context/KPI geometry contract с совпадающими separators и большей first-viewport data area;
- собраны семь обязательных representative prototype flows с route navigation, transient overlays и return-to-origin;
- полный structural QA существующих 91 route frames и 5 system surfaces пройден для W03 baseline revision 124; 19 route backlog frames, comments/data-treatment overlays, новые presentation/import/access/branding surfaces и additive treatment/segmentation delta существующих Analytics/Segments frames требуют следующей Penpot-синхронизации и visual QA.

## 1. Design brief

### 1.1. Продукт

Custometry — self-hosted операционная система B2C retail-аналитики: семантические данные, единые метрики и методики, исследования от общего к частному, качество, прогнозирование, воспроизводимые отчёты и управляемое выполнение процессов. B2B sales остаётся отдельным будущим расширением.

### 1.2. Пользовательский результат

Интерфейс должен позволять пройти полный путь без Python:

```text
подключить данные
→ изучить каталог
→ описать семантическую модель
→ проверить качество
→ выбрать утверждённые метрики и методику
→ определить population, обработку выбросов и способ сегментации
→ выполнить research от общего к частному или прогноз
→ зафиксировать evidence-linked findings
→ понять достоверность результата
→ опубликовать branded dashboard/report и выдать доступ
→ обсудить результат в comments без расширения прав
→ отправить email или выгрузить XLSX
→ диагностировать run и инфраструктуру
```

### 1.3. Целевые пользователи

| Сокращение | Роль | Главная задача в UI |
|---|---|---|
| `IA` | Installation Administrator | Установка, сервисы, плагины, backup и global policies без неявного доступа к workspace data |
| `WA` | Workspace Administrator | Users, roles, report/dashboard access, connections, policies и branding без аналитического authoring по умолчанию |
| `DS` | Data Steward | Catalog, mapping, data contracts, Data Guide и Data Quality |
| `AN` | Analyst | Метрики, методики, research, сегменты, dashboards, reports, comments, send и exports без управления connections/access grants |
| `ML` | ML Analyst | Forecast specifications, backtests, models и monitoring |
| `OP` | Operator | Runs, schedules, attempts, queues, recovery и acknowledgements |
| `VW` | Viewer | Просмотр и комментарии к разрешённым non-PII результатам без изменения definitions/snapshots |

Один пользователь может иметь несколько ролей. Навигация и действия формируются из effective permissions, но расположение разрешённых функций остаётся стабильным.

## 2. Разбор предоставленных референсов

Четыре изображения задают визуальное направление, но не являются готовой спецификацией.

### 2.1. Что сохраняем

- desktop-first application shell;
- постоянная левая навигация и верхняя utility bar;
- компактная, но не перегруженная enterprise analytical density;
- спокойные поверхности, тонкие границы и один основной accent;
- KPI cards, таблицы, tabs, right-side details panels;
- графики как часть рабочего процесса, а не декоративный hero;
- status badges и operational health без неоновой перегрузки;
- master-detail для Catalog, Metrics, Notifications и Runs;
- wizard/stepper для onboarding и сложного mapping;
- canvas только там, где он действительно нужен — Pipelines.

### 2.2. Что корректируем по blueprint

| В референсах | В итоговом UI |
|---|---|
| Несколько несовместимых вариантов sidebar | Один permission-aware navigation contract |
| Смешаны `Data`, `Models`, `Settings`, `Admin` | Явные продуктовые домены и стабильные группы |
| Нет разделения lifecycle/readiness/execution status | Три отдельных status surfaces |
| Previous period toggle не объясняет политику сравнения | Versioned comparison editor с coverage/compatibility |
| Показан только простой filter bar | Searchable typed Filter Registry и expression chips |
| Нет системного Result Trust | На каждом reportable result есть compact trigger; полный Trust drawer открывается по запросу |
| Светлый визуальный default | В design-артефакте закреплена единственная тема `frost`; прочие цветовые профили не входят в текущий scope |
| Логотип является частью generated mock | До официального asset используется text-only wordmark |

### 2.3. Визуальный характер

Рабочее название направления: **Calm Analytical Workbench**.

- профессиональный и спокойный;
- data-dense, но с чёткой иерархией;
- без декоративных gradients и glassmorphism;
- без чрезмерной карточности: карточка означает самостоятельный блок;
- операционные проблемы видны, но не окрашивают весь экран в красный;
- данные и ограничения важнее иллюстраций.

## 3. Основные UX-принципы

1. **Explain before block.** Недоступная функция сообщает evidence, порог и следующее действие.
2. **Guided first.** Основной путь — forms и guided flows; canvas — продвинутый режим Pipeline.
3. **One result, many surfaces.** Web, email и XLSX используют один snapshot и одни данные.
4. **Trust is visible.** Freshness, quality, grain, filters, timezone, currency, lineage и limitations доступны рядом с результатом.
5. **No hidden compute.** Тяжёлый запуск имеет preflight, объём, ресурсы, progress, ETA/confidence и cancel.
6. **No status soup.** Lifecycle definition, readiness данных и execution state визуально разделены.
7. **Permissions do not surprise.** Disabled используется только для временного состояния; forbidden функция скрыта либо объяснена отдельным permission state.
8. **Tables are first-class.** Любой chart имеет доступное табличное представление.
9. **Keyboard is a primary input.** Все основные flows работают без drag-only и hover-only действий.
10. **Localization is structural.** Layout допускает длинные русские строки, plural forms и future RTL.

### 3.1. Что берём из Apple HIG, а что не копируем

Apple HIG используется как craft-check, а не как platform skin для Web. Берём: ясную визуальную иерархию, deference к content, предсказуемую navigation history, немедленную обратную связь, заметный focus, reduced motion, сохранение context и достаточные hit targets. Для Custometry это означает спокойный shell, минимум декоративного motion, route-backed Focus, понятный Back/Escape, status рядом с обновляемым block и progressive disclosure сложных controls.

Не копируем macOS/iOS chrome, native-only gestures, hidden hover-only actions, full-screen slide stacks и platform-specific icons без Web semantics. Web/WCAG, keyboard, browser history, enterprise density, en/ru и self-hosted constraints имеют приоритет.

## 4. Информационная архитектура

### 4.1. Основная навигация

```text
Overview

Data Foundation
  Connections
  Data Catalog
  Datasets
  Metrics
  Filter Fields
  Data Guides
  Data Quality

Analytics
  Analysis Library
  Sales
  Customer Base
  RFM
  Cohorts
  Lifecycle
  Basket
  Stores & Channels
  Margin & Discounts
  Segments

Forecasting
Promotions
Dashboards
Reports & Exports
Pipelines

Operations
  Runs
  Schedules
  Notifications

Administration
  Installation
  Workspaces
  Access & Policies
  Capacity
  Runtime
  Plugins
  Storage & Backup
  Audit
  Localization & Themes
```

Sidebar показывает только разрешённые группы. В `expanded` каждый item содержит Lucide icon и полное локализованное название; в `collapsed` остаются те же icons без текста. Буквенные сокращения (`OV`, `DF`, `AN` и подобные) запрещены. Icon identity, порядок и route не меняются между состояниями; active item имеет контрастный selection marker и `aria-current`. Для icon-only item обязательны локализованные accessible name, tooltip по hover/focus, visible focus и hit area не менее 40×40 CSS px. Группа раскрывается автоматически при переходе на вложенный route и сохраняет состояние пользователя. Sidebar имеет три состояния: `expanded`, `collapsed` и `hidden`; выбор сохраняется для пользователя. В `hidden` остаётся доступный keyboard/focusable control для возврата навигации без перезагрузки страницы.

### 4.2. Глобальный application shell

| Область | Содержимое |
|---|---|
| Верхняя строка | Text wordmark, workspace switcher, global search/command palette, help, notifications, user menu |
| Sidebar | Permission-aware navigation, expanded/collapsed/hidden control, active route, environment marker при необходимости |
| Page header | Breadcrumb, title, description/status, primary action и secondary actions |
| Context bar | Dataset/version, date range, comparison, filters, timezone/currency, saved view |
| Main content | Fluid page grid с ограничением читаемости long-form blocks |
| Context panel | Right drawer 360–480 px для detail/lineage/issue/node без потери списка |
| Progress surface | Persistent operation drawer; run продолжается после ухода со страницы |

### 4.3. Global search

`Cmd/Ctrl + K` открывает command palette с секциями:

- navigation;
- datasets, metrics, reports, dashboards, pipelines и runs;
- разрешённые filter fields;
- recent items;
- actions, доступные текущей роли.

Search не показывает существование запрещённых resources. Для фильтров используется typed Filter Explorer, а не свободная строка SQL.

### 4.4. URL, history и workspace routing contract

Route registry имеет четыре области:

| Scope | Canonical form | Примеры |
|---|---|---|
| Public/auth | Без workspace | `/auth/sign-in`, `/bootstrap`, `/invites/:token` |
| Global user | Без workspace | `/profile/security`, `/notifications`, `/notifications/preferences`, `/help` |
| Installation | `/admin/*` либо `/audit` | `/admin/system`, `/admin/services`, `/audit` |
| Workspace | `/w/:workspaceKey/*` | `/w/:workspaceKey/overview`, `/w/:workspaceKey/analytics/sales` |

Машиночитаемый route contract разделён на три слоя. `packages/contracts/routes/ui-routes.json` остаётся компактным реестром identity/URL/title/release/status, `packages/contracts/routes/ui-route-contracts.json` хранит исполняемую политику family/shell, role hints, permissions, guards, states, history/query, Focus и Penpot status для всех 110 страниц, а `packages/contracts/routes/ui-surface-contracts.json` доказывает полное покрытие route, overlay, system и cross-surface capability surfaces. Portable schemas находятся рядом; семантический валидатор проверяет паритет с этим документом, все `UC-001…024`, product permission catalog и en/ru titles. Role hints используются только для discoverability и не заменяют API authorization.

`workspaceKey` — неизменяемый opaque public identifier. Display name может меняться и не участвует в URL. Наличие ключа в URL не даёт доступ: guard до data fetch проверяет authenticated membership, effective permission и resource scope. Таблицы §9 показывают route suffix для читаемости; если строка не относится к public/global/installation scopes, её канонический URL строится как `/w/:workspaceKey` + указанный suffix.

History policy:

- переход к resource, самостоятельной tab и Focus surface делает `push`;
- presentation-only query, pagination/status refresh и transient menu/popover используют `replace` либо не меняют URL;
- разрешённые query keys: `view`, `tab`, `focus`, `sort`, `page`, `saved_view`;
- raw PII, secrets, source values и unredacted filter values в URL запрещены;
- сложный устойчивый filter state передаётся через authorized Saved View ID; временный share state — через opaque short-lived reference;
- Focus открывается на origin route как `?focus=<block_id>` и является полноэкранной route surface, не modal;
- Close, Escape и browser Back восстанавливают route, block anchor, scroll и keyboard focus; direct deep link закрывается на parent route с focus на page heading;
- workspace switch сохраняет suffix только когда target workspace разрешает resource/capability, иначе ведёт на target Overview с безопасным объяснением;
- `returnTo` только same-origin и allowlisted; session expiry хранит opaque reference и повторно проверяет permission после login.

Все редакторы с dirty draft регистрируют navigation guard для sidebar route, workspace switch, Back, reload и close. Confirmation предлагает `Stay`, `Discard` и `Save draft`, если сохранение поддерживается. После route change обновляются document title, breadcrumb/current-location semantics и focus; shell/sidebar/topbar не remount-ятся.

## 5. Layout и responsive contract

### 5.1. Master viewport

Все основные Penpot frames создаются в `1440 × 900`. Это не фиксированный runtime viewport, а общий размер visual review.

| Диапазон | Поведение |
|---|---|
| `≥1440` | Sidebar 240 px по умолчанию; пользователь может свернуть или полностью скрыть его, content становится fluid, правый inspector может быть закреплён |
| `1280–1439` | Sidebar 224 px, content cards перестраиваются 4→3 columns |
| `1024–1279` | Sidebar 72 px в collapsed icon-only state: центрированные 20 px icons без сокращений; inspectors становятся drawers, secondary panels уходят ниже |
| `768–1023` | Tablet landscape: read/review flows полные; сложные editors используют sequential panels |
| `<768` | Viewer/approval/read-only flows; canvas, model mapping и report composition предлагают открыть desktop |

Ни один layout не полагается на горизонтальный scroll всей страницы. Горизонтальный scroll допустим внутри data grid, timeline и canvas с явным affordance.

### 5.2. Grid

- content padding: 24 px desktop, 16 px tablet;
- base spacing unit: 4 px;
- common gaps: 8, 12, 16, 24, 32 px;
- card radius: 8 px;
- controls: 36 px compact, 40 px default, 44 px touch-priority;
- primary content uses 12-column grid;
- data tables и canvas могут занимать всю доступную ширину.

Desktop reporting density для master frame `1440×900`:

- compact header metadata/title/action начинается на `80 px` от верхней границы frame и занимает не более `88 px` после topbar;
- context bar: `48 px`;
- Compact KPI Strip: `64 px`;
- vertical gaps между context, KPI и primary data block: `12–16 px`;
- primary chart/table/editor начинается не ниже `308–320 px`;
- четыре KPI используют общие column boundaries `256 / 526 / 796 px` внутри контейнера `1136 px`; Context Bar использует те же boundaries;
- декоративный empty space не резервируется вместо данных; высота block определяется содержимым, viewport и состоянием.

Значения утверждены как design/Penpot geometry для UI blueprint `0.6.1-draft`; при runtime-реализации они переходят в versioned production tokens после browser/accessibility verification без изменения зафиксированной плотности и иерархии.

## 6. Design system

### 6.1. Темы

Нормативный registry содержит шесть профилей:

| Theme | Scheme | Назначение |
|---|---|---|
| `graphite` | dark | Product UI default |
| `abyss` | dark | Самый глубокий контрастный operational режим |
| `slate` | dark | Более мягкий dark режим |
| `frost` | light | Холодный светлый UI |
| `paper` | light | Email/XLSX default; вне текущего UI design scope |
| `sand` | light | Тёплый светлый режим |

Penpot variables и design tokens для темы `frost` должны повторять соответствующий профиль machine `theme_registry`. Компоненты используют только semantic aliases: `canvas`, `background`, `surface`, `line`, `text`, `muted`, `accent`, `focus`, status и chart roles.

Дополнительно до component build должны быть определены отсутствующие в сыром palette registry aliases из `THEME-003`: `success`, `warning`, `error`, `info`, `positive`, `negative` и color-blind-safe categorical chart series. Они являются design tokens, а не новыми бизнес-правилами.

### 6.2. Typography

Базовый шрифт Penpot-макета: `Inter` с системными fallback. Причины — доступность en/ru начертаний, нейтральность, читаемость плотных таблиц и визуальная близость к референсам. Название font bundle должно быть отдельно закреплено в product/runtime contract до implementation.

| Token | Size / line | Weight | Использование |
|---|---|---|---|
| `display-sm` | 28 / 36 | 600 | Auth и onboarding welcome |
| `heading-xl` | 24 / 32 | 600 | Page title |
| `heading-lg` | 20 / 28 | 600 | Major section |
| `heading-md` | 16 / 24 | 600 | Card/inspector title |
| `body-lg` | 16 / 24 | 400 | Help, descriptions, Data Guide |
| `body` | 14 / 20 | 400 | Main application text |
| `body-strong` | 14 / 20 | 600 | Labels and emphasis |
| `caption` | 12 / 16 | 400 | Metadata, table secondary text |
| `code` | 13 / 20 | 500 mono | IDs, expressions, hashes, schemas |

Zoom до 200% не ломает flow. Таблицы не используют текст меньше 12 px.

### 6.3. Icons и brand

- единственная core outline icon family v1 — Lucide через pinned `lucide-react`;
- sidebar icons — 20 px, стандартный stroke 2 px, round caps/joins; остальные icons 16/20/24 px;
- semantic mapping sidebar: `House`, `Database`, `ChartNoAxesCombined`, `ChartSpline`, `BadgePercent`, `LayoutDashboard`, `FileChartColumn`, `Workflow`, `Activity`, `Settings`;
- expanded navigation использует icon + label; collapsed navigation может использовать icon-only только с accessible name, hover/focus tooltip и stable route identity;
- иконка никогда не является единственным label для незнакомого действия;
- status не выражается только icon или цветом;
- emoji, handcrafted SVG, смешивание icon families и псевдографика запрещены;
- SF Symbols не являются Web core asset: Apple-only license boundary несовместима с cross-platform self-hosted distribution;
- distribution сохраняет upstream Lucide ISC и унаследованные Feather MIT notices в `THIRD_PARTY_NOTICES`;
- canonical provenance: [Lucide](https://lucide.dev/), [upstream LICENSE](https://github.com/lucide-icons/lucide/blob/main/LICENSE), [Apple Design Resources License](https://developer.apple.com/support/downloads/terms/apple-design-resources/Apple-Design-Resources-License-20230621-English.pdf);
- до получения официального SVG используется text-only wordmark `Custometry`;
- runtime branding идёт через versioned BrandProfile: company product names, sanitized logos/favicon, optional sanitized custom icon pack, bundled fonts и semantic color overrides;
- raw CSS/HTML/JS, remote assets и customer-specific component forks запрещены; preview проверяет contrast, broken assets, fallback wordmark и Web/email/XLSX/docs parity;
- Penpot остаётся в одной production design theme `frost`; BrandProfile states показывают contract и preview, а не требуют дублировать все 110 screens для каждого клиента.

### 6.4. Elevation

- основной layout преимущественно плоский;
- border важнее shadow;
- `shadow_panel` используется для modal, popover, command palette и floating drawer;
- nested cards не получают отдельную тень;
- backdrop применяется только к modal, не к side inspector.

### 6.5. Motion

Semantic tokens:

| Token | Duration | Назначение |
|---|---:|---|
| `motion.none` | 0 ms | Immediate state |
| `motion.fast` | 120 ms | Menu, popover, indicator |
| `motion.route` | 160 ms | Main-content fade, modal base |
| `motion.panel` | 220 ms | Sidebar, drawer |
| `motion.slow` | 240 ms | Верхняя граница safe chart/panel transition |

Standard easing: `cubic-bezier(0.2, 0, 0, 1)`; exit: `cubic-bezier(0.4, 0, 1, 1)`. Компоненты не создают собственные duration tokens.

| Surface | Production transition | Reduced-motion variant |
|---|---|---|
| Route navigation | Shell/sidebar/topbar неподвижны; main content fade 120–160 ms | Fade ≤80 ms либо instant |
| Sidebar | Expand/collapse 180–220 ms, без bounce и text blur | Instant size/state change |
| Tabs | Indicator 120–160 ms; previous data сохраняются до ready | Instant indicator, status update |
| Drawer | Directional 200–240 ms | Без translate, fade ≤80 ms |
| Modal | Fade + минимальный scale 160–200 ms | Без scale, fade ≤80 ms |
| Popover/menu | 100–140 ms | Instant/fade ≤80 ms |
| Focus / Explore | Route-backed surface, без full-screen slide | То же, instant/fade |
| Charts | Только safe transition 160–240 ms при стабильном domain/axis и малой density | Без continuous/interpolated animation |
| Tables | Без перемещения строк; краткая highlight + textual status | Status и non-animated highlight |
| Loading/refresh | Previous data + local freshness/loading; skeleton преимущественно first load | Без shimmer; status/progress остаются |

Chart animation выключается при изменении domain/axis, dense series, live operational data и comparison policy, чтобы промежуточные кадры не выглядели как реальные значения. Refresh использует stale-while-revalidate и reserved layout; stale controls, которые больше нельзя безопасно применить, временно блокируются с объяснением. Motion не является единственным носителем status и не задерживает focus/live-region announcements.

## 7. Библиотека компонентов

### 7.1. Foundations

- color primitives и semantic mode темы `frost`; остальные профили нормативного registry остаются вне design scope;
- spacing, radii, sizing и opacity;
- typography и code styles;
- elevation/effects;
- focus ring;
- z-index usage documentation;
- chart semantic roles.

### 7.2. Reusable components

| Группа | Компоненты |
|---|---|
| Actions | Button, Icon Button, Split Button, Menu Item, Link |
| Inputs | Text Input, Textarea, Number, Select, Combobox, Date/Time, Password, Search |
| Choice | Checkbox, Radio, Toggle, Segmented Control, Chips |
| Navigation | App Sidebar / Expanded, App Sidebar / Collapsed, Nav Item / Icon+Label, Nav Item / Icon-only, Sidebar Toggle, Nav Group, Breadcrumb, Tabs, Pagination, Stepper |
| Data display | Badge, Status Pill, Avatar, Tooltip, Definition List, Code Value |
| Containers | Card, compact KPI Strip, Section, Accordion, Drawer, Modal, Popover, Focus / Explore Surface |
| Tables | Data Grid, Column Header, Sort, Selection, Row Actions, Virtualized state, Focus Table Toolbar |
| Filters | Filter Bar, Filter Chip, Field Search, Operator Picker, Value Picker, Expression Tree |
| Charts | Chart Frame, Legend, Tooltip, Annotation, Comparison style, Table Alternative, Focus Chart Toolbar |
| Feedback | Alert, Inline Message, Toast, Empty State, Skeleton, Spinner, Progress, ETA |
| System/help | System Surface, Session Banner, Maintenance Banner, Help Search Result, Shortcut Row, Unsaved Changes Guard |
| Trust | Compact Result Trust Trigger, optional Result Trust Drawer, Freshness Badge, Quality Badge, Lineage Link, Limitation List |
| Operations | Run Status, Attempt Timeline, Queue Health, Worker Card, Log Viewer |
| Builder | Pipeline Node, Port, Edge, Canvas Toolbar, Inspector, Validation Summary |
| Reports | Report Block, Block Toolbar, Snapshot Banner, Email Recipient Field, Export Preflight |
| Promotion | Range Timeline, Lane Header, Promotion Bar, Overlap Density, Audience Badge |

### 7.3. Component states

Каждый интерактивный компонент документирует:

```text
default
hover
pressed
focus-visible
selected
disabled
loading
error
read-only
```

Data-rich components дополнительно имеют `empty`, `partial`, `stale`, `degraded`, `forbidden` и `failed`.

## 8. Общие patterns

### 8.1. Page header

Одна primary action на уровне страницы. Остальные действия находятся в secondary buttons либо overflow menu. Destructive action не соседствует с primary без visual separation. На рабочих desktop screens ID/route metadata, title и primary action образуют один compact header block; длинное пояснение является optional/collapsible и не создаёт постоянную пустую полосу над Context Bar.

### 8.2. List/detail

Для Connections, Metrics, Reports, Forecasts, Notifications и Runs используется единый pattern:

- search/filter/saved view;
- bounded paginated или virtualized list;
- row selection;
- detail route либо right inspector;
- stable deep link;
- empty/loading/error/permission states.

### 8.3. Versioned object

Header всегда разделяет:

- lifecycle: draft/published/deprecated/archived;
- readiness/capability;
- последнюю execution information.

Действия `Validate`, `Publish`, `Clone draft`, `Deprecate` и `Archive` показываются только когда допустимы. Publish открывает diff + dependency impact и требует явного подтверждения.

### 8.4. Heavy operation

Перед запуском отображаются:

- capability decision;
- estimated rows/bytes/time class;
- effective CPU allocation и limits;
- cost/PII warnings;
- planned output;
- cancel semantics.

После запуска persistent operation drawer показывает stage, elapsed, percent или indeterminate, ETA/confidence, cancel и link to run.

### 8.5. Reportable result

Каждый analytics/forecast/dashboard/QualityReport screen содержит:

- explicit date range;
- searchable filters;
- comparison to previous year либо понятный blocker;
- ChartSpec-backed charts;
- table alternative;
- compact Result Trust trigger; полный panel открывается по запросу и не занимает постоянную колонку layout;
- save/share/report/export actions по permissions.

### 8.5.1. Reporting density

- четыре primary KPI находятся в одном контейнере высотой `64 px`, а не в четырёх самостоятельных высоких cards;
- KPI label находится на первой строке, value и короткий `vs LY` — на второй; все четыре cells используют общую baseline;
- Context Bar и KPI Strip используют одинаковые column boundaries/divider X coordinates; divider Y/height выравниваются внутри своего контейнера;
- primary visualization начинается в master `1440×900` на `y=308` и получает приоритет над декоративным whitespace;
- sample data table начинается на `y=684`, показывает минимум две data rows и range/pagination status; production height остаётся content- и viewport-aware;
- Result Trust остаётся optional compact trigger и не резервирует постоянную широкую колонку;
- contract применяется к `UI-DQ-001`, всем `UI-AN-001…014` и остальным report-like routes; list/wizard/builder screens без KPI используют тот же compact header, но собственный content template.

### 8.5.2. Metric groups, adaptive numbers и research narrative

- один `MetricGroupVersion` определяет group heading, group order и metric order; UI не сортирует метрики автоматически по label или текущему значению;
- compact display использует `NumberFormatSpec`: `75,44% → 75%`, `4,27% → 4,3%`, `0,234% → 0,23%`; non-zero value не отображается как `0%`;
- compact suffix (`K/M/B`, `тыс./млн/млрд`) не заменяет full value: оно доступно в tooltip/detail, accessible description и Data table;
- Research/Dashboard/Report используют ordered sections и heterogeneous blocks `narrative`, `metric_group`, `chart`, `table`, `finding`, `conclusion`, `methodology` и `result_trust`;
- approved Finding имеет author/review/evidence/limitations surface; comment имеет avatar/time/thread/resolve surface и никогда не выглядит как утверждённый вывод;
- Viewer может открыть и добавить comment только к разрешённой non-PII projection; comment drawer не показывает hidden filters, denied facets или raw source values;
- report/dashboard access находится в отдельной admin surface; Analyst видит effective access summary, но не grant/revoke controls.

### 8.6. Empty и blocked states

Empty state содержит причину, prerequisite и одну следующую primary action. Blocked state показывает stable error title, безопасное evidence, owner и remediation. Иллюстрация необязательна.

### 8.7. Navigation, unsaved changes и return-to-origin

- active sidebar item, breadcrumb, document title и route всегда согласованы;
- sidebar имеет `expanded`, `collapsed`, `hidden`; restore control остаётся keyboard/focusable;
- dirty draft guard срабатывает на route, workspace switch, Back, reload и close;
- `Stay` возвращает focus к источнику navigation, `Save draft` продолжает переход только после подтверждённого save, `Discard` явно называет теряемый объект;
- modal/drawer возвращает focus trigger; route-backed Focus возвращает block anchor, scroll и keyboard focus;
- browser Back не закрывает несколько transient layers по одной записи: transient popover/menu не создают history;
- page/tab data сохраняются во время refresh, пока authorization и schema не делают старое представление небезопасным.

### 8.8. Help и keyboard shortcuts

`Help` в topbar открывает компактное меню: contextual help, Search Help, Keyboard shortcuts, Data Guide, version/support. Полный `/help` ищет только по разрешённой shipped документации и Data Guides. Shortcut help открывается через `?` вне text input либо из Help menu; labels зависят от платформы (`⌘`/`Ctrl`). Shortcut никогда не является единственным способом выполнить действие.

Минимальные общие shortcuts:

- `Cmd/Ctrl + K` — command palette;
- `?` — shortcuts/help;
- `Esc` — закрыть transient surface либо вернуть из Focus по route contract;
- `G`, затем allowlisted domain key — опциональная sequence navigation, отключаемая в profile;
- table/chart-specific shortcuts показываются только при focus внутри соответствующего block.

### 4.5. Критерий route-backed surface

Количество Penpot frames не является потолком route registry. Самостоятельный route обязателен, когда surface имеет durable entity/version lifecycle, должен открываться из notification/audit/deep link, требует собственных Back/refresh/unsaved semantics либо имеет независимую permission boundary и достаточно сложное состояние для bookmark/recovery. Transient подтверждение или inspector остаётся modal/drawer; повторяемое поведение таблиц, графиков и отчётов становится cross-surface capability. Каждый UI-visible use case обязан иметь binding хотя бы к одному из этих типов поверхности; совпадение количества строк между двумя JSON не является доказательством полноты.

### 8.9. System и lifecycle surfaces

403, 404, session expired, maintenance и upgrade required имеют отдельные layouts и stable codes. Они не показывают пустой normal page, stack trace, raw path, migration SQL, denied resource title или cached protected content. Admin system lifecycle отдельно показывает release/schema versions, compatibility, migrations, licenses/SBOM/provenance, runbook и безопасный preflight; operational channel management — endpoint versions, health, categories, test, rotate/revoke и audit links без destination/secret.

## 9. Полный реестр страниц

Фаза `MVP` означает public MVP, `V1` — расширение до v1 target. Все изображения создаются как master desktop frames; multi-step steps и drawer states добавляются отдельными state frames.

### 9.1. Authentication и onboarding — 6 страниц

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-AUTH-001 | `/auth/sign-in` | Sign in | MVP | all | Email/password, remember, language, password help, self-hosted trust copy |
| UI-AUTH-002 | `/bootstrap` | First administrator bootstrap | MVP | IA | One-time token, first admin, password, first workspace, irreversible completion warning |
| UI-AUTH-003 | `/invites/:token` | Accept invitation | MVP | invited | Workspace/role summary, identity confirmation, password setup or sign-in, expiry/error |
| UI-AUTH-004 | `/auth/recovery` | Password recovery/reset | MVP | all | Host/admin reset token flow, password rules, generic security messages; no implied email reset before channel exists |
| UI-AUTH-005 | `/onboarding` | First-run onboarding | MVP | IA, WA | Account, workspace, locale/timezone, data/demo, finish; resumable checklist |
| UI-AUTH-006 | `/profile/security` | Profile, preferences and security | MVP | all | Profile, language/locale/timezone/theme, change password, sessions, scoped API tokens |

### 9.2. Home — 1 страница

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-CORE-001 | `/overview` | Workspace Overview | MVP | all | KPI summary, freshness, quality, recent runs, forecast alerts, onboarding checklist, role-specific next actions |

### 9.3. Data Foundation — 31 страница

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-DATA-001 | `/connections` | Connections | MVP | WA | PostgreSQL/MSSQL/MySQL/ClickHouse и CSV/XLSX template modes, status, test all, add, filter, owner; Yandex marked future-only |
| UI-DATA-002 | `/connections/new` | Connection editor | MVP | WA | Governed connector choice, read-only credentials reference, network parameters/template version, limits, test, save draft |
| UI-DATA-003 | `/connections/:id` | Connection detail | MVP | WA | Configuration, test history, catalog snapshots, health, permissions, disable/archive |
| UI-DATA-004 | `/catalog` | Data Catalog | MVP | WA, DS | Source/schema/object tree, search, freshness, row estimate, preview and discover |
| UI-DATA-005 | `/catalog/objects/:id` | Catalog object detail | MVP | DS | Columns, profile, null/distinct stats, lineage, constraints, sample policy |
| UI-DATA-006 | `/catalog/objects/:id/preview` | Bounded data preview | MVP | DS | Masked sample, column controls, row limit, PII warning, download restriction |
| UI-DATA-007 | `/datasets` | Semantic datasets | MVP | DS, AN | List, lifecycle/readiness/capabilities, versions, create/clone |
| UI-DATA-008 | `/datasets/:id/mapping` | Entity mapping wizard | MVP | DS | Customer/Receipt/ReceiptItem/Product/Store/Channel/Calendar mapping, namespace and keys |
| UI-DATA-009 | `/datasets/:id/relationships` | Relationship editor | MVP | DS | Cardinality, temporal joins, validity, collision checks, graph + accessible form alternative |
| UI-DATA-010 | `/datasets/:id/policies` | Semantic policies | MVP | DS | Returns, currency/FX, timezone/calendar, identity, activity and incomplete-period policies |
| UI-DATA-011 | `/datasets/:id/capabilities` | Capability and readiness | MVP | DS, AN, ML | Available/degraded/blocked functions, evidence, thresholds, suggested remediation |
| UI-DATA-012 | `/datasets/:id/versions` | Versions, diff and impact | MVP | DS | Draft/published history, schema drift, dependency impact, validate/publish/clone |
| UI-DATA-013 | `/metrics` | Metric Registry | MVP | DS, AN | Search, domain/kind/status/version, usage impact, import and create |
| UI-DATA-014 | `/metrics/:id` | Metric editor/detail | MVP | DS, AN | Expression tree, grain, aggregations, dimensions, currency/unit, NumberFormatSpec, MetricGroupVersion, labels, lineage, impact |
| UI-DATA-015 | `/filter-fields` | Filter Field Registry | V1 | DS, AN | Searchable fields, type/operators, hierarchy, null/facet/security policy and versions |
| UI-DATA-016 | `/data-guides` | Data Guides | V1 | DS, AN, VW | Dataset guides, published version, drift/review status, owner and locale |
| UI-DATA-017 | `/data-guides/:id/edit` | Data Guide editor | V1 | DS | Approved Markdown template, preview, validation, safe links/assets, publish |
| UI-DATA-018 | `/data-guides/:id` | Data Guide reader/history | V1 | allowed | Rendered guide, dataset/version binding, version history, drift banner |
| UI-DATA-019 | `/artifacts` | Artifact Library and detail | MVP | DS, AN, ML, OP | Category/schema/version, grain/key/PII, lineage, retention, bounded preview, authorized download and related run |
| UI-DATA-020 | `/datasets/:id` | Dataset Overview | MVP | DS, AN, ML | Canonical landing page: lifecycle/readiness, versions, freshness/quality, capabilities, mappings/policies, dependencies, Data Guide, recent runs and next action |
| UI-DATA-021 | `/methodologies` | Methodology Registry | MVP | AN, DS, VW | Search, domain/status/owner, purpose/applicability, versions, usage impact, create/review/publish by permission |
| UI-DATA-022 | `/methodologies/:id` | Method editor/detail | MVP | AN, DS, VW | Purpose, inputs, steps, assumptions, exclusions, thresholds, validation evidence, review, versions, usage impact and deprecation replacement |
| UI-DATA-023 | `/file-import-templates` | File Import Template Registry | MVP | WA, DS | Published/draft/deprecated templates, media type, entity pack, owner, compatibility, usage and create |
| UI-DATA-024 | `/file-import-templates/:id` | File Import Template editor/detail | MVP | WA, DS | Sheets/columns/types/aliases, locale parsing, limits, safe preview, validation, versions, publish/deprecate and impact |
| UI-DATA-025 | `/imports` | File Import History | MVP | WA, DS, OP | Template/file metadata without raw path, status, dataset target, validation result, rejected counts, owner, run and retry link |
| UI-DATA-026 | `/imports/new` | Governed File Import Wizard | MVP | WA | Template selection, bounded upload, preflight, mapping confirmation, unknown/formula/macro rejection, dataset target and submit |
| UI-DATA-027 | `/imports/:id` | File Import Result and Diagnostics | MVP | WA, DS, OP | Immutable input/template versions, validation evidence, rejected-row diagnostics, lineage, created artifacts, run status and safe retry |
| UI-DATA-028 | `/metric-groups` | Metric Group Registry | MVP/V1 | DS, AN, ML | Group versions, localized label, domain, stable group/metric order, usage impact, create and publish |
| UI-DATA-029 | `/metric-groups/:id` | Metric Group editor/detail | MVP/V1 | DS, AN, ML | Ordered metrics, boundaries, accessible headers, versions, presentation overrides, validation, diff/impact and publish |
| UI-DATA-030 | `/number-formats` | Number Format Registry | MVP/V1 | DS, AN, ML | System/workspace/metric scopes, value kind, locale/unit/currency, compact/precision policy, preview matrix and create |
| UI-DATA-031 | `/number-formats/:id` | Number Format editor/detail | MVP/V1 | DS, AN, ML | Adaptive precision, non-zero thresholds, full-value disclosure, chart/email/XLSX previews, versions, impact and publish |

### 9.4. Data Quality — 5 страниц

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-DQ-001 | `/data-quality` | Quality Overview | MVP | DS, OP | Readiness, score, category summary, failed rules, trends and next actions |
| UI-DQ-002 | `/quality-rules` | Quality rules | MVP | DS | Search, severity/action/scope/status, owner, execute, create |
| UI-DQ-003 | `/quality-rules/:id` | Rule editor/detail | MVP | DS | Safe expression tree, threshold, severity, blocking action, version lifecycle |
| UI-DQ-004 | `/quality-reports/:id` | QualityReport | MVP | DS, AN, OP | Gate decision, rules, redacted samples, comparison, trust/lineage, export |
| UI-DQ-005 | `/quality-issues/:id` | Issue remediation and waiver | MVP | DS, OP | Evidence, affected capabilities, owner/comments, fix link, expiring scoped waiver, rerun |

### 9.5. Analytics и Research — 14 страниц

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-AN-001 | `/analyses` | Analysis Library | MVP | AN, DS, VW | Templates, saved analyses, status, dataset, last result, owner, create/run |
| UI-AN-002 | `/analyses/new` | Guided analysis setup | MVP | AN | Template, dataset, population/grain, capability preflight, parameters, optional treatment, filters, comparison, resource estimate |
| UI-AN-003 | `/analytics/sales` | Sales Overview | MVP | AN, VW | Revenue/orders/AOV/margin, trend, contribution, product/store/channel breakdown, trust |
| UI-AN-004 | `/analytics/customers` | Customer Base | MVP | AN, VW | Active/new/retained/reactivated/at-risk/churned, value/frequency/tenure and flows |
| UI-AN-005 | `/analytics/rfm` | RFM | MVP | AN, VW | Version/as-of, score distribution, segment cards, scatter/table, rule link |
| UI-AN-006 | `/analytics/cohorts` | Cohorts | MVP | AN, VW | Origin/frequency/metric, retention/value heatmap, curve, censoring explanation |
| UI-AN-007 | `/analytics/lifecycle` | Lifecycle and churn | MVP | AN, VW | State counts/revenue, transition matrix/flows, versioned rule set and impossible transitions |
| UI-AN-008 | `/analytics/basket` | Basket Analytics | V1 | AN, VW | SKU/subcategory/category/brand level, basket KPIs, pairs, rules and affinity matrix |
| UI-AN-009 | `/analytics/stores-channels` | Stores and Channels | V1 | AN, VW | Scorecards, online/offline migration, comparable-store policy, operating-day normalization |
| UI-AN-010 | `/analytics/margin-discounts` | Margin and Discounts | V1 | AN, VW | Margin, discount depth, mix, contribution, negative/low-margin diagnostics |
| UI-AN-011 | `/analyses/custom` | Custom Builder | V1 | AN, DS | Dataset/population, metric/features, dimensions, typed filters, outlier policy, bucket/stratified mode, comparison, chart/table choice, preflight |
| UI-AN-012 | `/analyses/:id/results/:runId` | Result detail and trust | MVP | allowed | Immutable result, ChartSpec/table/distribution, treatment chip and sensitivity, filters, YoY diagnostics, limitations, lineage, save/report/export |
| UI-AN-013 | `/research` | Research Cases | MVP | AN, VW | Questions/cases, owner/status, pinned method/dataset, findings, related analytical products, create/open/filter |
| UI-AN-014 | `/research/:id` | Research Workspace | MVP | AN, VW | Outline/sections, narrative, metric groups, charts/tables/distributions, treatment evidence, drill/filter, findings vs comments, publish to dashboard/report/segment |

Товарная аналитика в текущем product blueprint реализуется через Sales, Basket и Custom Builder. Отдельная route-level страница «Products» пока не является нормативным модулем; произвольная товарная иерархия также остаётся отдельным будущим решением.

### 9.6. Segments — 3 страницы

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-SEG-001 | `/segments` | Segment Library | MVP | AN, VW | Rule/RFM/bucket/KMeans segments, versions, method/treatment, snapshot date, size/value, status, create |
| UI-SEG-002 | `/segments/new` | Segment Builder | MVP | AN | Population/features → Data Treatment → rule/RFM/bucket/KMeans method and group count → preview/sensitivity → publish |
| UI-SEG-003 | `/segments/:id` | Segment detail/snapshots | MVP | AN, VW | Overview, definition, profiles, authorized members, snapshots/migration, diagnostics, usage, frozen assignment/retrain and treatment evidence |

### 9.7. Forecasting — 7 страниц

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-FCST-001 | `/forecasts` | Forecast Library | MVP | ML, AN, VW | Targets/specs, champion, monitoring status, freshness, schedule, create |
| UI-FCST-002 | `/forecasts/new` | Forecast specification and series preview | MVP | ML | Target/frequency/horizon/dimensions/cutoff, history capability, gaps/outliers, candidates |
| UI-FCST-003 | `/forecasts/:id/backtests` | Backtest and model comparison | MVP | ML, AN | Folds, baseline vs candidates, WAPE/bias/MAE/RMSE/coverage, champion decision |
| UI-FCST-004 | `/forecasts/:id` | Forecast detail | MVP | ML, AN, VW | Actual/forecast/intervals, model/spec metadata, trust, filters/comparison, export/report |
| UI-FCST-005 | `/models/:id` | Model Registry detail | MVP | ML | Algorithm, artifacts, feature schema/order, hyperparameters, backtest and lifecycle |
| UI-FCST-006 | `/forecasts/:id/monitoring` | Forecast monitoring | MVP | ML, OP | Actual-vs-forecast, WAPE/bias/coverage/drift/model age, retrain/promote/rollback |
| UI-FCST-007 | `/models` | Model Registry | MVP | ML, AN, OP | Model versions, forecast spec, algorithm, lifecycle/champion, age/monitoring status, compare and open detail |

### 9.8. Promotion Journal — 3 страницы

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-PROMO-001 | `/promotions` | Promotion Journal | V1 | AN, WA, VW | `range_timeline`, list/table alternative, channel/customer/product filters, overlaps and planned/actual |
| UI-PROMO-002 | `/promotions/new` | Promotion editor | V1 | AN, WA | Definition, immutable version, windows, channels, stores/products/regions, audience binding |
| UI-PROMO-003 | `/promotions/:id` | Promotion detail/history | V1 | AN, WA, VW | Version history, planned/actual comparison, immutable audience, overlaps, analytics overlays, audit |

### 9.9. Dashboards — 3 страницы

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-DASH-001 | `/dashboards` | Dashboard Library | MVP | AN, VW | Templates/saved dashboards, pinned/latest policy, owner/version/freshness, create |
| UI-DASH-002 | `/dashboards/:id` | Dashboard Viewer | MVP | allowed | Ordered sections, metric groups, charts/tables, findings, comments, filters/comparison, trust, report/export and effective access summary |
| UI-DASH-003 | `/dashboards/:id/edit` | Dashboard Editor | MVP | AN | Sections/heterogeneous blocks, grid layout, widget bindings, filters, preview, diff/impact and publish; access grants absent |

### 9.10. Reports и exports — 7 страниц

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-RPT-001 | `/reports` | Report Library | V1 | AN, VW | Definitions, snapshots, deliveries, owner/version/updated, create |
| UI-RPT-002 | `/reports/:id/edit` | Report Composer | V1 | AN | Sections and narrative/metric-group/table/chart/finding/conclusion/methodology/quality/forecast/metadata/Data Guide blocks, bindings and preview |
| UI-RPT-003 | `/reports/:id/snapshots/:sid` | Report snapshot/preview | V1 | allowed | Immutable branded blocks, metric groups, comments, theme/locale/timezone, trust/lineage, send/export |
| UI-RPT-004 | `/reports/:id/send` | Send report by email | V1 | AN | Verified user sender, allowed-domain recipients, PII check, subject/message, preview, submit |
| UI-RPT-005 | `/report-deliveries` | Email delivery history/detail | V1 | AN, WA, OP | Queued/submitted/delivered/failed/unknown, policy evidence, safe retry/reconciliation |
| UI-RPT-006 | `/exports` | Export jobs and artifact detail | MVP/V1 | AN, VW, OP | CSV/Parquet/JSON/XLSX requests, preflight, progress, limits, download authorization, retention |
| UI-RPT-007 | `/settings/report-email` | Report email settings | V1 | IA, WA | Verified sender identities, transport authorization, global/workspace domain allowlists, provider health and audit links |

### 9.11. Pipelines и schedules — 4 страницы

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-PIPE-001 | `/pipelines` | Pipeline Library | MVP | AN, DS, ML, OP | Draft/published pipelines, validity, schedules, last run, owner, create |
| UI-PIPE-002 | `/pipelines/:id/edit` | Pipeline Canvas | V1 | AN, DS, ML | Accessible canvas, node library, ports/edges, inspector, validation, keyboard alternative |
| UI-PIPE-003 | `/pipelines/:id/versions` | Pipeline validation/publish | MVP | owners | Validation summary, normalized spec, diff/impact, clone/publish/deprecate |
| UI-PIPE-004 | `/schedules` | Schedules | MVP | AN, ML, OP | Lifecycle and health separately, cadence/timezone, next/last run, pause/resume/editor |

### 9.12. Operations — 4 страницы

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-OPS-001 | `/runs` | Operator Center | MVP | OP, owners | All/queued/running/succeeded/failed/cancelling, filters, auto-refresh, queue summary |
| UI-OPS-002 | `/runs/:id` | Run detail | MVP | OP, owners | DAG, attempts, progress/events/logs/metrics/artifacts, execution context, cancel/retry/rerun |
| UI-OPS-003 | `/runs/:id/nodes/:nodeId/attempts/:attemptId` | Node attempt detail | MVP | OP | Lease/fencing, input/output, safe error, resource evidence, logs, retry eligibility |
| UI-OPS-004 | `/admin/runtime` | Runtime health | MVP/V1 | IA, OP | Installation-scoped workers, queues, outbox, reconciler, scheduler, DB/artifacts, renderer/mail health and runbooks |

### 9.13. Notifications — 3 страницы

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-NOTIFY-001 | `/notifications` | Notification Inbox | MVP | all | Severity/category/read/ack/resolved filters, dedupe groups, deep links, details and acknowledge |
| UI-NOTIFY-002 | `/notifications/preferences` | Notification preferences | MVP/V1 | all | Per-category in-app preferences; email/webhook options появляются только когда channel enabled |
| UI-NOTIFY-003 | `/settings/notification-channels` | Operational notification channels | V1 | WA, OP | Channel availability, immutable endpoint versions, verification/health, categories, bounded test, rotate/disable/revoke and audit links without destination/secret disclosure |

### 9.14. Administration — 18 страниц

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-ADMIN-001 | `/admin` | Installation Overview | MVP | IA | Installation health, workspaces, events/day, storage, forecasts/day, backup and critical actions |
| UI-ADMIN-002 | `/admin/workspaces` | Workspaces | MVP | IA | List/create/disable, membership summary, quotas and audited support access boundary |
| UI-ADMIN-003 | `/settings/access` | Members, roles and invitations | MVP | IA, WA | Members, effective roles, invites, report/dashboard object grants, expiry/revoke, PII grant ceiling and session/token links |
| UI-ADMIN-004 | `/settings/policies` | Workspace and installation policies | MVP/V1 | IA, WA | PII/export, domain allowlist ceiling, retention, filter/facet and feature policies |
| UI-ADMIN-005 | `/admin/capacity` | CPU, resource limits and allocations | V1 | IA, WA, OP | Detected/effective cores, admin cap, allocations, saturation, invalid config evidence |
| UI-ADMIN-006 | `/admin/services` | Service health | MVP | IA, OP | API/scheduler/workers/PostgreSQL/Valkey/artifacts/proxy/OTel status and dependency detail |
| UI-ADMIN-007 | `/admin/workers` | Workers, queues, outbox and reconciler | MVP | IA, OP | Concurrency, heartbeat, queue age, leases, outbox backlog, reconciliation controls |
| UI-ADMIN-008 | `/admin/plugins` | Plugins | V1 | IA | Installed/available trusted plugins, compatibility, permissions, enable/disable and warning |
| UI-ADMIN-009 | `/admin/storage-backup` | Storage, retention, backup and restore | MVP | IA, OP | Capacity/watermarks/inodes/orphans, retention, backup manifests, drill status, restore action |
| UI-ADMIN-010 | `/audit` | Audit Explorer | MVP | IA, WA | Installation/workspace scopes, actor/action/resource/result/time filters, redacted detail/export |
| UI-ADMIN-011 | `/admin/localization-themes` | Localization and themes | MVP/V1 | IA, WA | en/ru coverage, workspace defaults, six themes, report default, accessibility validation status |
| UI-ADMIN-012 | `/admin/system` | System lifecycle and upgrades | MVP/V1 | IA, OP | App/release/schema versions, compatibility, migrations, maintenance, upgrade requirement, license/SBOM/provenance, preflight, runbooks and guarded rollback |
| UI-ADMIN-013 | `/settings/branding` | Workspace Branding Assignment | MVP/V1 | WA | Allowed published profile, workspace preview, effective identity, impact, assign/rollback/reset without asset or CompanyPack editing |
| UI-ADMIN-014 | `/admin/brand-profiles` | Brand Profile Registry | MVP/V1 | IA | Installation/workspace profiles, lifecycle, base theme, asset/contrast status, usage impact, create and open |
| UI-ADMIN-015 | `/admin/brand-profiles/:id` | Brand Profile editor/detail | MVP/V1 | IA | Product identity, sanitized assets/icons/fonts, semantic tokens, login/email/report/XLSX/docs previews, validate, diff, publish and rollback |
| UI-ADMIN-016 | `/admin/company-packs` | Company Pack Registry | MVP/V1 | IA | Pack versions, compatibility, installed/bound workspaces, included config refs, manifest hash, import and create |
| UI-ADMIN-017 | `/admin/company-packs/:id` | Company Pack detail/preflight | MVP/V1 | IA | Contents without secrets/data, compatibility preflight, diff/impact, validate, publish, install/upgrade/rollback and export |
| UI-ADMIN-018 | `/access/:resourceType/:resourceId` | Report/Dashboard Access Policy | MVP | WA | Allowlisted resource type, grants/groups/expiry, effective-access preview, PII ceiling, diff, grant/revoke and audit deep link without content editing |

### 9.15. Help — 1 страница

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-HELP-001 | `/help` | Help Center and keyboard shortcuts | MVP/V1 | all | Permission-aware search по shipped docs/Data Guides/codes, contextual help, shortcut reference, version/support and deterministic deep links |

**Итого: 110 основных route-level страниц.** Из них 91 уже существует в текущем Penpot baseline. Design backlog состоит из 19 routes: `UI-DATA-021…031`, `UI-AN-013…014` и `UI-ADMIN-013…018`. Пять system surfaces §10.1 проектируются отдельно и не увеличивают основной route count. Target non-route contract содержит 25 overlays, 5 system surfaces и 19 cross-surface capabilities; baseline revision 124 содержит 23 overlay/state frames, поэтому `UI-OVR-024` и `UI-OVR-025` являются design backlog.

## 10. Overlays, drawers и modals

Они не считаются отдельными route-level страницами, но получают собственные Penpot state frames. `UI-OVR-020` исторически сохраняет prefix `OVR`, однако реализуется как route-backed surface, а не modal/overlay в DOM.

| ID | Surface | Вызывается из | Основные требования |
|---|---|---|---|
| UI-OVR-001 | Workspace switcher | Global shell | ROUTE-010 |
| UI-OVR-002 | Global command palette | Global shell | ROUTE-003, ROUTE-005, RBAC-006 |
| UI-OVR-003 | Searchable Filter Explorer | Любой reportable result | FILTER-002, FILTER-005, FILTER-007, FILTER-008 |
| UI-OVR-004 | Filter expression editor | Analytics/dashboard/report | FILTER-001, FILTER-003, FILTER-004, FILTER-009, FILTER-010 |
| UI-OVR-005 | Previous-year comparison editor | Любой reportable result | UC-012, COMPARE-001…007 |
| UI-OVR-006 | Result Trust drawer | Result/dashboard/report/quality/forecast | REPORT-008, UX-JOURNEY-005 |
| UI-OVR-007 | Chart data table | Любой chart | CHART-015, A11Y-006, A11Y-007 |
| UI-OVR-008 | Publish diff and impact modal | Versioned definition | OBJ-STATE-002, UX-JOURNEY-006 |
| UI-OVR-009 | Clone/deprecate/archive modal | Versioned definition | OBJ-STATE-001, OBJ-STATE-003 |
| UI-OVR-010 | Operation progress drawer | Heavy operation | PROGRESS-001…008 |
| UI-OVR-011 | Cancel/retry/rerun confirmation | Runs и compute surfaces | PROGRESS-006 |
| UI-OVR-012 | Export preflight modal | Result/dashboard/report | UC-015, REPORT-009, XLSX-006, RBAC-005 |
| UI-OVR-013 | Email send confirmation | Report snapshot | UC-014, REPORT-MAIL-001…005, RBAC-005 |
| UI-OVR-014 | Promotion item detail drawer | Promotion Journal | UC-013, PROMO-001…009 |
| UI-OVR-015 | Pipeline node inspector | Pipeline Canvas | UC-006, OBJ-STATE-004 |
| UI-OVR-016 | Notification detail drawer | Inbox/global bell | NOTIFY-001…015 |
| UI-OVR-017 | Theme switcher | Profile/user menu | THEME-001…008 |
| UI-OVR-018 | Permission/forbidden explanation | Любая protected surface | RBAC-002, RBAC-006, UX-JOURNEY-006 |
| UI-OVR-019 | Destructive action confirmation | Delete/revoke/restore/rollback | OBJ-STATE-001, OBJ-STATE-003 |
| UI-OVR-020 | Full-screen Focus / Explore Surface | Любой reportable chart, table или range timeline | UC-018, FOCUS-001…012 |
| UI-OVR-021 | Help and contextual-help menu | Global topbar/current page | HELP-001, HELP-003, HELP-004 |
| UI-OVR-022 | Keyboard shortcuts reference | Help menu или `?` | HELP-002, HELP-004 |
| UI-OVR-023 | Unsaved changes confirmation | Route/workspace/Back/reload/close guard | ROUTE-008 |
| UI-OVR-024 | Discussion and comments drawer | Research/dashboard/report block or snapshot | UC-021, RESEARCH-005…007, RBAC-014 |
| UI-OVR-025 | Data treatment and sensitivity drawer | Guided/Custom analysis, Segment Builder, result/research block | UC-025, OUTLIER-001…012, SEGMENT-018 |

### 10.1. System surfaces — 5 state frames

| ID | Surface | Contract | Основные требования |
|---|---|---|---|
| UI-SYS-001 | 403 Forbidden | Requested URL, no existence leak, Back/allowed Overview/request-access guidance | SYS-UI-001 |
| UI-SYS-002 | 404 Not Found | Invalid route/client compatibility safe code, allowed-history suggestions only | SYS-UI-002 |
| UI-SYS-003 | Session expired | Protected cache cleared, sign-in, opaque return reference, re-authorize after login | SYS-UI-003 |
| UI-SYS-004 | Maintenance | Scope, last update/next review, read-only/status actions, bounded refresh | SYS-UI-004 |
| UI-SYS-005 | Upgrade required | Current/required compatibility, mutations blocked, admin runbook, safe user detail | SYS-UI-005 |

### 10.2. Cross-surface capability contracts

Эти capabilities не создают самостоятельную страницу только ради повторения одного control pattern, но являются обязательными машиночитаемыми bindings и Penpot component/state contracts.

| ID | Capability | Применимость | Основные требования |
|---|---|---|---|
| UI-CAP-001 | Workspace routing, guards and return | Все protected routes | ROUTE-001…012, RBAC-002 |
| UI-CAP-002 | Searchable typed filters | Все разрешённые reportable datasets/results | FILTER-001…010 |
| UI-CAP-003 | Previous-year comparison | Любая аналитическая отчётность | UC-012, COMPARE-001…007 |
| UI-CAP-004 | Metric groups and adaptive formats | Web/email/XLSX metric and table blocks | METRIC-009…016 |
| UI-CAP-005 | ChartSpec visualization | Все reportable visual blocks | UC-017, CHART-001…019 |
| UI-CAP-006 | Chart ↔ Data table | Каждый chart с accessible alternative | CHART-015, A11Y-006, A11Y-007 |
| UI-CAP-007 | Focus / Explore | Chart, table и range timeline | UC-018, FOCUS-001…012 |
| UI-CAP-008 | Result Trust | Analysis/research/dashboard/report/quality/forecast | REPORT-008, UX-JOURNEY-005 |
| UI-CAP-009 | Research composition and findings | Research/dashboard/report composition | UC-020, RESEARCH-001…008 |
| UI-CAP-010 | Object-scoped comments | Разрешённые research/dashboard/report blocks | UC-021, RESEARCH-005…007, UX-JOURNEY-009, RBAC-014 |
| UI-CAP-011 | Resource access policy | Reports и dashboards | UC-011, UC-022, UX-JOURNEY-010, DASHBOARD-010, RBAC-013, RBAC-015 |
| UI-CAP-012 | ReportSnapshot and export preflight | Reportable result/dashboard/report | UC-015, REPORT-001…014, XLSX-001, XLSX-006 |
| UI-CAP-013 | Verified-user report email | Published report snapshots | UC-014, REPORT-MAIL-001…011 |
| UI-CAP-014 | Progress, ETA and cancellation | Все тяжёлые CPU/job operations | PROGRESS-001…008, COMPUTE-001…010 |
| UI-CAP-015 | Effective brand resolution | Shell/login/email/report/XLSX/docs | UC-023, BRAND-001…009 |
| UI-CAP-016 | Authorized PII-safe rendering | Preview/filter/comment/export/send surfaces | RBAC-005, RBAC-011…015, DASHBOARD-011 |
| UI-CAP-017 | Localization, accessibility and reduced motion | Все routes, overlays и system surfaces | I18N-001…011, A11Y-001…010, MOTION-001…012 |
| UI-CAP-018 | Governed population and outlier treatment | Analysis/segment authoring, Result Trust, report/email/XLSX | UC-025, OUTLIER-001…012 |
| UI-CAP-019 | Bucket, stratified and KMeans segmentation | Custom Builder, Segment Builder/detail, Research | UC-026, SEGMENT-001…018 |

## 11. Страница аналитического результата

Все специализированные analytics pages используют один composition pattern:

```text
Page header
Context bar
  Dataset/version
  Period
  Comparison (`vs LY`)
  Search filters
  Saved view
Compact KPI strip: один общий контейнер, четыре ячейки без отдельных крупных cards
Primary chart area
Secondary decomposition/chart
Data table
Compact Result Trust trigger; optional drawer on demand
Actions: save, dashboard, report, export
```

### 11.1. Comparison

- default action: «Сравнить с аналогичным периодом прошлого года»;
- компактная подпись сравнения во всех локалях — `vs LY`; полная локализованная расшифровка используется в tooltip, accessible name и comparison editor;
- editor показывает resolved current/comparison ranges, timezone, calendar и coverage;
- delta содержит абсолютное и относительное изменение;
- неполный либо несовместимый период имеет warning/blocked state;
- comparison style одинаков для KPI, charts и tables.

### 11.2. Filters

- search по label, field name, entity, description и aliases;
- только разрешённые published fields;
- typed operator/value controls;
- hierarchy breadcrumb;
- null policy видна пользователю;
- sensitive facets/counts не раскрываются;
- active filters отображаются chips с keyboard removal;
- saved view pin-ит filter expression/version.

### 11.3. Data treatment и sensitivity

`Data Treatment` не маскируется под обычный filter chip. В authoring surfaces компактный treatment control показывает status `None`, `Flag`, `Exclude` либо `Winsorize`, method и affected share и открывает `UI-OVR-025`. В published/viewer result control становится inspect-only и ведёт к той же pinned version через Result Trust.

Drawer содержит population/grain/feature/window/peer scope, quantile/IQR/MAD method, tail и parameters, missing/zero/negative/returns policy, resolved bounds и action. До Apply/Publish обязательно показываются before/after count, customer/order/value shares, metric deltas, distribution overlay и warning о legitimate high-value customers. DQ-invalid rows отображаются отдельным слоем и не смешиваются со statistical outliers.

Для `vs LY` editor по умолчанию показывает `Shared pinned bounds`; режим `Independent exploratory bounds` требует явного выбора, warning и отдельной result identity. Member preview, excluded rows, drill-down и export доступны только после отдельной permission/PII проверки. Все heavy previews используют общий progress/ETA/cancel contract и сохраняют предыдущий preview во время refresh.

### 11.4. Charts

- ECharts — единственный Web renderer v1;
- `ChartSpec` остаётся source of truth;
- Web использует SVG/Canvas по policy;
- chart header содержит title, unit, info, actions и table toggle;
- tooltip не является единственным источником значения;
- line comparison различается dash/weight/label, не только цветом;
- `range_timeline` имеет lanes, visible window, overlap density и accessible table;
- loading/empty/error/too-dense states определены до implementation.

### 11.5. Full-screen Focus / Explore

Каждый reportable chart, table и `range_timeline` имеет заметное действие `Open in Focus`/«Развернуть». Оно делает history `push` того же origin route с `?focus=<block_id>` и открывает `UI-OVR-020` на весь viewport приложения. Это route-backed прикладной surface, не nested modal и не browser/OS fullscreen: global shell скрывается в compact return header, а Close, Escape и browser Back используют один return-to-origin contract.

Композиция:

```text
Focus header
  Close + return-to-origin
  Title
  Current period + `vs LY`
  Result Trust
  Export
Filter context
  Applied filters
  System filters
  Locked filters
  Search any permitted field
  Draft local filters
  Apply to report / Reset / Undo
View toolbar
  Chart ↔ Data table
  Chart: legend / zoom / pan / brush / drill-down / reset view
  Table: columns / sort / density / pinning / pagination
Primary content viewport
State/status region
```

Поведение и границы:

- header и controls остаются доступны при прокрутке, но не перекрывают content;
- все applied, system и locked filters видимы; system/locked chips нельзя удалить либо ослабить;
- field search показывает только разрешённые поля FilterFieldRegistry и поддерживает keyboard search/selection;
- локальные filters являются draft до `Apply to report`; `Reset` возвращает inherited filters, `Undo` откатывает последнее draft-действие;
- `Apply to report` может запустить server CPU compute; в этом случае UI использует общий progress/ETA contract и не блокирует Close без явного предупреждения о последствиях;
- chart controls появляются только при соответствующей capability в `ChartSpec`; brush/zoom не подменяют authoritative filters, пока пользователь явно не применил действие;
- table toolbar управляет columns, server-side sort, density, pinning и pagination и сохраняет PII/permission boundaries;
- `Chart ↔ Data table` сохраняет source, filter, comparison, grain, units, freshness, permissions и Result Trust;
- Result Trust открывается компактным trigger/drawer и не занимает постоянную широкую колонку;
- Export использует тот же reportable result и текущие applied result filters; presentation-only zoom/legend/table layout включаются только при явной поддержке export preflight;
- Close, Escape и browser Back возвращают route, scroll position, block anchor и keyboard focus; при неприменённых draft filters действует confirm/discard pattern;
- временные legend/zoom/brush/columns/density/pinning/pagination state не изменяют request hash и исчезают при закрытии, если пользователь не сохранил versioned Saved View.

Responsive:

- desktop: single-surface viewport с sticky header/toolbars и максимальной площадью данных;
- tablet: filters и secondary controls переходят в доступные drawers, основные actions остаются в header;
- узкий viewport: read/explore поддерживается, toolbars группируются в overflow; сложное редактирование filter expression может открыть отдельный full-height drawer;
- при 200% zoom не допускаются horizontal page scroll для chrome, overlap controls и недоступная Close action; таблица может иметь собственный явно обозначенный horizontal scroll.

Обязательные states: loading, empty, filtered-empty, warning, degraded, blocked, failed, forbidden, stale, partial data и compute in progress. Для chart всегда доступны textual summary и Data table; значения и actions не зависят только от hover, pointer или цвета.

## 12. Таблицы и большие данные

- sticky header и первая смысловая колонка, когда это помогает сравнению;
- column chooser, sort, typed filter, resize и density preference;
- server-side pagination/virtualization;
- row count и displayed range;
- безопасный copy без скрытого PII;
- export является отдельной authorized action;
- cell truncation имеет tooltip и keyboard-accessible expand;
- table не симулирует бесконечный список без loading/terminal state;
- empty, loading, partial, error и permission states не заменяются пустой сеткой.

## 13. Forms и builders

### 13.1. Wizard

- sidebar либо top stepper;
- autosave только после валидного шага;
- Back/Continue не теряют данные;
- step error summary фокусируется и связывается с полями;
- unfinished draft можно продолжить из library;
- final step показывает normalized summary и impact.

### 13.2. Expression builder

- AND/OR groups;
- typed field/operator/value;
- keyboard reorder controls;
- readable sentence preview;
- raw SQL только в отдельном advanced mode, если разрешён продуктовым contract;
- validation не зависит от цвета и показывает stable error code/help.

### 13.3. Pipeline canvas

- canvas является дополнительным представлением общей specification;
- node add/connect/delete доступны мышью и клавиатурой;
- list/outline alternative позволяет выполнить те же действия без drag;
- inspector содержит configuration, inputs/outputs, resources и validation;
- minimap и zoom не закрывают content;
- publish невозможен при errors/cycles/incompatible schema.

### 13.4. Population and Segmentation Builder

`UI-SEG-002` переиспользует общий wizard и не превращается в отдельный canvas:

```text
1 Population & As-of
2 Features & Metrics
3 Data Treatment
4 Method & Group Count
5 Preview & Validation
6 Publish
```

- Step 1 фиксирует dataset/version, entity grain, eligible population, observation window и as-of.
- Step 2 разрешает только опубликованные features/metrics, показывает type, missingness, PII class и запрещает identifiers/leakage.
- Step 3 использует `UI-OVR-025`; default `Flag only`, а `Exclude/Winsorize` требуют impact acknowledgement.
- Step 4 предлагает rule, RFM, quantile/equal-width/custom bucket и KMeans; exact group count обязателен там, где это применимо. HDBSCAN/GMM/automatic-K controls в v1 отсутствуют.
- Step 5 показывает bucket/distribution/cluster profiles, sizes, center/feature distinctions, stability, silhouette/limitation, treatment sensitivity, minimum-cell privacy и blockers. Для KMeans diagnostic K-1/K/K+1 не меняет выбранный K.
- Step 6 показывает normalized immutable definition, pinned boundaries/treatment/preprocessing/seed, downstream impact и publish diff.

`UI-SEG-003` использует tabs `Overview`, `Definition`, `Profiles`, `Members`, `Snapshots & Migration`, `Diagnostics`, `Usage`. `Members` и excluded/flagged observations загружаются только после authorization и PII policy. Frozen-model assignment и full retrain имеют разные actions и confirmation copy; retrain создаёт новый snapshot и не переименовывает historical cluster IDs.

Stratified distribution остаётся mode Custom Builder/Research, а не новым top-level route. Global bucket boundaries выбраны по умолчанию; within-stratum quantiles имеют явный `Relative rank within each stratum` label. Из selected cell можно выполнить `Save as segment`, после чего открывается normalized Segment Builder draft с lineage исходного DistributionArtifact.

## 14. Accessibility, i18n и content

### 14.1. Accessibility baseline

- WCAG 2.2 AA;
- skip link к main content;
- стабильный focus order и видимый focus ring;
- keyboard navigation для sidebar, tabs, grids, dialogs, canvas и charts;
- touch target не меньше 44×44 там, где ожидается touch;
- dialog имеет focus trap, initial focus и return focus;
- status announcements throttled;
- reduced motion;
- chart table alternative;
- error summary и inline field association;
- цвет никогда не является единственным сигналом.

### 14.2. Localization

- English — default/fallback, русский — полный;
- language, format locale, timezone и currency — независимые настройки;
- даты/числа/проценты форматируются locale-aware;
- machine IDs, enums, hashes, API fields и canonical CSV headers не переводятся;
- layout тестируется на длинных русских строках и pseudo-locale;
- CSS logical properties используются с начала проекта.

### 14.3. Content style

- короткие action labels: «Проверить», «Опубликовать», «Повторить узел»;
- destructive действия называют объект и последствие;
- empty state объясняет prerequisite;
- technical details доступны по раскрытию, но stable code сохраняется;
- причинность не утверждается без соответствующего метода;
- `warning`, `degraded` и `failed` не используются как синонимы.

## 15. Обязательные состояния

Каждая из 110 route-level страниц проектируется минимум для применимых состояний; system surfaces используют отдельные contracts §10.1:

| State | UI contract |
|---|---|
| Loading | Skeleton/reserved layout, accessible busy label |
| Empty-first-use | Причина, ценность и одна следующая action |
| Empty-filtered | Clear filters, сохранение исходного context |
| Success | Результат, timestamp/freshness и next action |
| Warning | Non-blocking issue с evidence |
| Degraded | Доступна ограниченная функция и перечислены ограничения |
| Blocked | Недоступно до remediation; stable reason/evidence/owner |
| Failed | Safe error, retry/recovery path и link to run |
| Forbidden | Нет раскрытия существования защищённых данных; permission guidance |
| Stale | Видна дата, причина и refresh action |
| Offline/dependency unavailable | Read-only/degraded behavior объяснено |
| Cancelling/cancelled | Progress и последствия partial artifacts |
| Concurrent edit | Revision conflict, compare/reload/clone actions |
| Unsaved navigation | Stay/Discard/Save draft с return focus и названным объектом |
| Session expired | Protected cache cleared, safe sign-in/return reference и re-authorization |
| Upgrade required | Read-only/degraded boundary, required version и admin/runbook action |

## 16. Penpot delivery contract

### 16.1. Новый файл

Целевое имя: `Custometry — Web UI Blueprint — Frost v0.6.1`. Канонический working file имеет Penpot file ID `7cd71457-8d32-8044-8008-549f83bb4645`; его техническое имя `custometry` может сохраняться до финального handoff.

### 16.2. Структура Penpot

```text
00 Cover
01 Getting Started
02 Foundations — Colors
03 Foundations — Typography
04 Foundations — Spacing & Effects
05 Foundations — Charts
--- Components
C00 Components Index
C01 Button
C02 Icon Button & Menu Item
C03 Text Field & Textarea
C04 Select & Combobox
C05 Date, Time & Period
C06 Choice Controls
C07 App Sidebar & Nav Item
C08 Breadcrumb, Tabs, Pagination & Stepper
C09 Badge, Status & Avatar
C10 Card, KPI Card & Section
C11 Modal, Drawer & Popover
C12 Data Grid
C13 Filter Builder
C14 Chart Frame & Table Alternative
C15 Feedback, Empty & Skeleton
C16 Progress & ETA
C17 Result Trust
C18 Pipeline Node, Port & Edge
C19 Report Block
C20 Promotion Range Timeline
C21 Operations Status & Attempt Timeline
C22 Focus / Explore Surface & Toolbars
C23 Population Treatment & Segmentation Diagnostics
--- Screens
19 Help & System Surfaces
20 Auth & Onboarding
21 Overview
22 Data Foundation
22A Methodology Registry
22B File Imports & Templates
22C Metric Presentation
23 Data Quality
24 Analytics
24A Research Workspace
25 Segments
26 Forecasting
27 Promotions
28 Dashboards
29 Reports & Exports
30 Pipelines
31 Operations
32 Notifications
33 Administration
33A Branding & Company Packs
33B Resource Access Policies
34 Responsive Samples
35 State Matrix
36 Theme Matrix
```

### 16.3. Component strategy

Foundations создаются раньше компонентов. Repeated UI создаётся как local component/component set; screen frames используют instances. Компоненты связываются с semantic variables, а не hardcoded fills/spacing/radii. В текущем scope поддерживается только тема `frost`.

### 16.4. Render output

- 110 individual desktop master images по текущему route contract; 91 уже существуют в baseline, 19 ожидают Penpot generation;
- 5 отдельные system-surface frames: 403, 404, session expired, maintenance, upgrade required;
- отдельные state/contact sheets для wizard steps, drawers, comments, Data Treatment/sensitivity, bucket/stratified/KMeans diagnostics и mandatory states;
- отдельные state frames Focus / Explore для chart, table, range timeline, filters draft/apply/undo и return-to-origin;
- responsive samples для Overview, Catalog, Analytics Result, Report Composer, Pipeline Canvas и Operator Center;
- representative analytics screen в единственной теме `frost`;
- naming: `UI-<DOMAIN>-<NNN>--<slug>--frost--1440x900.png`;
- Penpot frame name совпадает с ID и page title этого документа.

Один screen считается готовым только после visual screenshot review: нет clipping/overlap/placeholder copy, правильный font, theme tokens, component instances и доступные labels.

### 16.5. Prototype flows

Penpot prototype обязан иметь минимум следующие representative flows:

1. `Workspace Overview → Sales → Focus → Back to source block`;
2. `Dataset Overview → Capability → remediation link → Back`;
3. `Draft editor → sidebar navigation → UI-OVR-023 Stay/Save/Discard`;
4. `Topbar Help → UI-OVR-021 → UI-HELP-001 → UI-OVR-022`;
5. `Session expired → Sign in → safe return/re-authorization`;
6. `Admin System → maintenance/upgrade state → runbook/preflight`;
7. `Notification channels → bounded test → status/audit detail`.
8. `Segment Builder → treatment preview → bucket/KMeans diagnostics → publish → snapshot detail`.

Prototype interaction не заменяет runtime contract: Focus и deep links должны моделироваться navigation flow, transient modal/drawer — overlay flow, Back/Escape — явным return connection. Motion annotations используют только матрицу §6.5 и содержат reduced-motion note.

### 16.6. Visual QA matrix

Для всех 110 route frames и 5 system frames проверяются:

- уникальный ID, canonical route/scope, title, active navigation и primary action;
- отсутствие placeholder copy, clipping, unintended overlap и content вне frame;
- text alignment кнопок/controls, consistent row/column geometry, readable long ru copy;
- sidebar expanded/collapsed/hidden affordance и корректный restore control;
- expanded/collapsed используют один semantic icon mapping; collapsed и tablet sidebar не содержат буквенных сокращений, а icon-only items имеют accessible names и hover/focus tooltips;
- compact KPI strip, `vs LY`, optional Result Trust drawer и Focus trigger на reportable surfaces;
- Data Treatment chip/drawer не смешивается с обычными filters, показывает action/method/affected share и shared-vs-independent LY bounds;
- Context Bar и KPI Strip имеют одинаковые column boundary X coordinates; separator Y/height, KPI baselines и text placement едины внутри template;
- над chart/table/editor отсутствуют декоративные пустые полосы; `UI-DQ-001` и `UI-AN-001…014` отдельно проверяются на compact header и first-viewport data density;
- loading/empty/failed/forbidden/stale/dirty/reduced-motion applicability;
- `UI-AN-002/011/012/014` и `UI-SEG-001…003` проходят additive delta review для population/treatment/strata/KMeans, включая exact K, sensitivity, privacy и immutable snapshot semantics;
- component instances/semantic Frost tokens, focus names и minimum hit areas;
- representative desktop/tablet/mobile reflow без двойной navigation модели;
- prototype entry/return flow и route metadata.

QA receipt фиксирует `pass`, `pass_with_note` или `fix_required` для каждого frame. Structural MCP scan может подтвердить geometry/metadata, но итоговый `pass` требует visual export review; browser/runtime accessibility и motion acceptance остаются отдельной future implementation boundary.

## 17. Traceability к product blueprint

| UI-область | Основные источники |
|---|---|
| Roles/navigation | §2.1, RBAC, AUTH |
| Onboarding | JOURNEY-001, UC-008, UX-JOURNEY-001 |
| Data Foundation | JOURNEY-002, UC-024, Connection/Catalog/Semantic/Metric/MetricGroup/NumberFormat/FileImportTemplate/Filter contracts |
| Quality | JOURNEY-003, DQ contracts, UC-003/009 |
| Analytics, Segments и Research | §12, UC-004/012/017…020/025/026, OUTLIER, SEGMENT, METHOD, RESEARCH, comparison/filter/chart/FOCUS contracts |
| Forecasting | JOURNEY-005, §13, ForecastSpec/Backtest/Model Registry |
| Promotion Journal | UC-013, PROMO, `range_timeline` |
| Dashboards/comments/access | DASHBOARD-007…012, RBAC-009…015, UC-021/022 |
| Reports/email/XLSX | UC-014/015, REPORT, REPORT-MAIL, XLSX-001…014, METRIC-009…016 |
| Pipelines/runs | JOURNEY-006, PIPELINE, RUN/EXEC/PROGRESS |
| Notifications | NOTIFY, RESOLVED-007 |
| Admin/operations | OPS, COMPUTE, access policies, BrandProfile/CompanyPack, backup, plugins и audit |
| Branding/i18n/a11y | BRAND, CompanyPack, THEME, I18N, A11Y, RESOLVED-006/008/016/027 |
| URL/history/workspaces | ROUTE-001…012, TEST-INV-050, V1-AC-017 |
| Motion/loading | MOTION-001…012, PROGRESS, TEST-INV-051, V1-AC-018 |
| System/help/lifecycle | SYS-UI-001…005, HELP-001…004, ADMIN-010…011, NOTIFY-014…015, V1-AC-019 |

## 18. Phase 0 gap analysis и решения перед Penpot

### 18.1. Что существовало в репозитории до сборки Penpot

- нормативные machine/human blueprint;
- six-theme palette registry;
- роли, journeys, APIs, states и acceptance contracts;
- React/pnpm workspace scaffold без UI implementation.

### 18.2. Что существует в референсах, но не закреплено продуктовым contract

- generated logo mark;
- точная font family;
- светлая theme как default;
- точные component dimensions;
- окончательная grouping sidebar.

### 18.3. Что отсутствует

- финальное имя и sharing policy Penpot-файла;
- published component library для межпроектного reuse;
- official logo SVG/brand pack;
- browser implementation для capture/QA;
- утверждённый mobile authoring scope.

### 18.4. Утверждённые и применённые решения scope lock

1. Вести design-артефакт в Penpot через MCP и закрепить единый file ID для всех последующих итераций.
2. Построить 110 route-level master frames, 5 system surfaces и отдельные state frames; v1 включает KMeans exact-K, но post-v1 B2B/Yandex/activation/GMM/HDBSCAN/automatic-K/multivariate-anomaly/ABC-XYZ/OIDC/Kubernetes/public API UI не включать.
3. Использовать только тему `frost`; прочие цветовые профили остаются вне design scope.
4. Использовать Inter в Penpot; до runtime implementation закрепить font bundle отдельным product decision.
5. Использовать text-only wordmark до получения официального SVG; generated logo из референса не перерисовывать.
6. Считать route-level page единицей обязательного изображения; wizard steps и drawers поставлять state sheets, а не увеличивать основной счётчик страниц.
7. Использовать canonical `/w/:workspaceKey/*` routing, route-backed Focus, production motion matrix и Help/System contracts до следующей массовой генерации/export.
8. Использовать Lucide/`lucide-react` как единственную v1 core icon family; expanded sidebar показывает icon + label, collapsed/tablet — icon-only без сокращений.
9. Использовать единый compact reporting geometry contract: header metadata от `y=80`, Context Bar `48 px`, KPI Strip `64 px`, primary data block от `y=308`, совпадающие Context/KPI boundaries.

## 19. Contract impact текущего документа

| Поверхность | Классификация | Пояснение |
|---|---|---|
| Product/API/ports/persistence | `compatible-change` | Добавлены Methodology/Research, FileImportTemplate/import, MetricGroup/NumberFormat, comments/access и split branding routes/contracts; runtime API, DTO/persistence ещё не реализованы |
| Browser-visible behavior | `compatible-change` | Route-backed Focus, guards и motion matrix дополнены research narrative, adaptive formatting, comments/access separation и BrandProfile preview |
| Request hash/cache identity | `compatible-change` | Applied result filters используют общий normalized contract; presentation-only state явно исключён |
| URL/bookmark/history | `breaking-change` для будущих legacy URLs; сейчас `compatible-change` | Канонический workspace prefix `/w/:workspaceKey`; Foundation runtime и stable bookmarks отсутствуют, поэтому миграция выполняется до первого release consumer |
| Design tokens/defaults | `compatible-change` | Производный contract закрепляет одну production design theme `frost`, Lucide mapping, BrandProfile semantic overrides и common density geometry |
| Penpot/components/images | `compatible-change`, pending sync | W03 revision-124 baseline сохранён; 19 routes, comments/data-treatment drawers, C23, presentation/import/access/branding/research components и additive Analytics/Segments frame delta ещё должны быть добавлены и visual-QA проверены |
| Migration/rollback | `compatible-change` до runtime | До implementation rollback равен возврату docs/Penpot; после stable URLs нужны redirects/deprecation/telemetry, Saved View DTO — schema version |

## 20. Phase 0 exit criteria

Phase 0 завершена. Phase 1 активна. W03 принял read-only Penpot baseline revision `124`: 47 pages, 68 local components, 91 route frames, 5 system surfaces, 23 overlays/state frames и семь representative flows для contract set `0.9.0/0.6.0`. UI blueprint `0.6.1-draft` сохраняет 110 routes и добавляет governed population treatment, bucket/stratified/KMeans workflow, `UI-OVR-025`, `UI-CAP-018…019`, C23 и восьмой prototype flow поверх уже принятого backlog methodology/research/import/metric/branding/access/comments. W03 evidence не переписывается; следующий Penpot write ticket обязан загрузить новый contract set, добавить отсутствующие surfaces и провести additive review затронутых Analytics/Segments frames, structural scan и individual visual export review всех 110 routes. Browser/runtime accessibility-motion evidence остаётся отдельной future boundary.
