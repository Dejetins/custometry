---
document_family_id: CUSTOMETRY-UI-BLUEPRINT
document_id: CUSTOMETRY-UI-BLUEPRINT-RU
title: Custometry — UI/UX blueprint Web-платформы
ui_spec_version: 0.7.0-draft
source_product_spec: 0.9.4-draft
source_documents:
  - ./custometry-technical-blueprint-ru.md
  - ./custometry-technical-blueprint-human-ru.md
status: active_design_iteration
normative: false
language: ru
created_at: 2026-07-15
updated_at: 2026-08-02
target: responsive_desktop_first_web_application
design_tool: browser_html_code_components
design_phase: phase_1_html_first_foundations_components_screens
---

# Custometry — полный UI/UX blueprint Web-платформы

## 0. Статус и назначение

Этот документ переводит продуктовый blueprint Custometry `0.9.4-draft` в проектируемую структуру Web UI: информационную архитектуру, маршруты, страницы, компоненты, состояния, взаимодействия, accessibility, responsive-поведение и HTML-first план прототипирования и повторного использования UI.

Документ является производным design-контрактом и не изменяет нормативную продуктовую спецификацию. Если UI-решение противоречит `custometry-technical-blueprint-ru.md`, действует machine blueprint. Новая бизнес-функция сначала должна появиться в двух продуктовых blueprint, а уже затем — здесь.

Текущий исторический design baseline и новый target:

- Penpot file `7cd71457-8d32-8044-8008-549f83bb4645`: W08 исторически принят на revision `181`, repair/recovery установил W10 start baseline `197`, а W10 принят на terminal revision `213`; Frost Foundations, components и **116 route-level страниц** сохраняются как accepted historical evidence и route/domain input;
- отдельно определены overlays, drawers, modals и обязательные состояния;
- W05 подтвердил 110 routes, 25 overlays и 5 system surfaces без duplicate/missing/orphan UI-ID и visual QA всех 140 stable surfaces;
- добавлены canonical URL/history, production motion, system/help surfaces и navigation guards;
- expanded sidebar переведён на Lucide icon + label, collapsed/tablet sidebar — на icon-only без буквенных сокращений;
- report-like surfaces получили общий compact header/context/KPI geometry contract с совпадающими separators и большей first-viewport data area;
- собраны восемь representative prototype flows с route navigation, transient overlays и return-to-origin;
- W06 подтвердил compact ordered MetricGroup tables и on-demand Result Trust, W08 на revision `181` — C24, flow 09 и discount/PVM delta, а W10 на revision `213` — C25, flow 10 и organization/People delta; browser/runtime/accessibility-runtime proof ещё отсутствует;
- историческая delta `0.9.3/0.6.3` полностью представлена в Penpot: шесть organization/department/People route IDs, UI-CAP-021/022, C25 и flow 10 прошли W10 visual/structural acceptance без изменения исполняемых продуктовых контрактов;
- UI target `0.7.0` заменяет foundation/shell/theme/interaction contract на общий Linear-workspace standard: React/TypeScript/Vite/MobX/TanStack Query/styled-components, четыре themes `abyss|graphite|frost|paper`, Inter Variable, resizable panels, keyboard-first navigation и измеримый perceived-performance contract; current delivery идёт slice-first от принятого responsive HTML к reusable code components, registry/manifests, browser acceptance и затем production implementation.

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

Company
  Organization
  People & Creators

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
  Products
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

Sidebar показывает только разрешённые группы. В `expanded` каждый item содержит Lucide icon и полное локализованное название; в `collapsed` остаются те же icons без текста. Буквенные сокращения (`OV`, `DF`, `AN` и подобные) запрещены. Icon identity, порядок и route не меняются между состояниями; active item имеет контрастный selection marker и `aria-current="page"`. Sales, Products и Forecasts используют разные semantic icons. Для icon-only item обязательны локализованные accessible name, tooltip по hover/focus, visible focus и hit area не менее 40×40 CSS px. Группа раскрывается автоматически при переходе на вложенный route и сохраняет состояние пользователя.

Sidebar имеет три состояния: `expanded`, `collapsed` и `hidden`. В expanded состоянии его pointer-resize ограничен диапазоном примерно `208–320 px`; separator имеет keyboard step/reset и double-click reset, а presentation preference сохраняется для пользователя. В `hidden` остаётся доступный keyboard/focusable control для возврата навигации без перезагрузки страницы. Global Search и Notifications находятся в utility area непосредственно под workspace identity, а Help и user menu — в стабильном footer sidebar. Page header не дублирует эти действия.

### 4.2. Глобальный application shell

| Область | Содержимое |
|---|---|
| Sidebar identity | Text wordmark и workspace switcher |
| Sidebar utility | Global search/command palette и notifications непосредственно после workspace identity |
| Sidebar navigation | Permission-aware groups, expanded/collapsed/hidden и resize control, active route, environment marker при необходимости |
| Sidebar footer | Help и user menu в стабильной нижней области |
| Page header | Breadcrumb, title, description/status, primary action и secondary actions |
| Context bar | Dataset/version, date range, comparison, filters, timezone/currency, saved view; `UI-AN-003` не дублирует Dataset отдельным control и переносит dataset/version в compact Result Trust trigger |
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

Машиночитаемый route contract разделён на три слоя. `packages/contracts/routes/ui-routes.json` остаётся компактным реестром identity/URL/title/release/status, `packages/contracts/routes/ui-route-contracts.json` хранит исполняемую политику family/shell, role hints, permissions, guards, states, history/query, Focus и design status для всех 117 target страниц, а `packages/contracts/routes/ui-surface-contracts.json` доказывает полное покрытие route, overlay, system и cross-surface capability surfaces. Portable schemas находятся рядом; семантический валидатор проверяет паритет с этим документом, все `UC-001…029`, product permission catalog и en/ru titles. Role hints используются только для discoverability и не заменяют API authorization. Historical Penpot baseline по-прежнему содержит 116 принятых route frames; новый `UI-AN-015` имеет `backlog` design status до собственного accepted HTML/component/browser stage.

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
| `≥1440` | Sidebar около 240 px по умолчанию; пользователь может pointer-resize его в bounded диапазоне около 208–320 px, свернуть в icon rail или полностью скрыть; правый inspector также может иметь bounded resize |
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

Значения утверждены как design/Penpot geometry для UI blueprint `0.7.0-draft`; при runtime-реализации они переходят в versioned production tokens после browser/accessibility verification без изменения зафиксированной плотности и иерархии.

## 6. Design system

### 6.1. Темы

Нормативный registry содержит ровно четыре профиля от near-black до bright-light:

| Theme | Scheme | Назначение |
|---|---|---|
| `graphite` | dark | Product UI default |
| `abyss` | dark | Самый глубокий контрастный operational режим |
| `frost` | light | Холодный светлый UI |
| `paper` | light | Яркий дневной UI и Email/XLSX default |

Production CSS tokens для всех четырёх themes должны повторять machine `theme_registry`. Каждый screen строится один раз на semantic aliases `canvas`, `background`, `surface`, `line`, `text`, `muted`, `accent`, `focus`, status и chart roles; representative browser matrix проверяет все themes без дублирования всех 117 target routes.

Дополнительно до component build должны быть определены отсутствующие в сыром palette registry aliases из `THEME-003`: `success`, `warning`, `error`, `info`, `positive`, `negative` и color-blind-safe categorical chart series. Они являются design tokens, а не новыми бизнес-правилами.

### 6.2. Typography

Базовый шрифт: self-hosted versioned `Inter Variable` с системными fallback. Причины — доступность en/ru начертаний, нейтральность, читаемость плотных таблиц и визуальная близость к референсам. Использование font-файлов Linear запрещено; собственный bundle и license metadata входят в runtime/render identity.

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
- Code foundation использует четыре production theme modes `abyss|graphite|frost|paper`; BrandProfile states показывают semantic overrides и browser preview, а не требуют дублировать все 117 target screens для каждого клиента.

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
| Organization | Org Tree, Unit Card, Membership Assignment, Leadership Scope, Data Policy Summary, Effective Access Preview, Handover Status |
| People | Contributor Card, People Directory Row, Activity Summary, Owned/Created Asset List, Scope/Privacy Badge |

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

### 9.2.1. Organization и People — 4 страницы

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-ORG-001 | `/organization` | Organization | MVP/V1 | all | Permission-filtered company/division/department/team tree, member/leader counts after policy filtering, status/successor, own primary department, open unit; no hidden counts |
| UI-ORG-002 | `/organization/:orgUnitKey` | Department Hub | MVP/V1 | allowed | Unit summary, leadership, members, owned reports/dashboards, data scope, activity aggregate, child units and transfer/history states; actions depend on explicit permissions |
| UI-PEOPLE-001 | `/people` | People & Creators | V1 | all | Compact searchable contributor cards/table, primary department, role hints, visible created/owned assets, privacy-safe activity and scope filter; no ranking/leaderboard/score |
| UI-PEOPLE-002 | `/people/:principalId` | Contributor Profile | V1 | allowed | Profile/department/role badges, privacy explanation, visible reports/dashboards, created versus owned, activity summary, collaboration and last activity; self/leader/grantee policy is evaluated independently and inaccessible assets/counts are omitted |

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

### 9.5. Analytics и Research — 15 страниц

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
| UI-AN-010 | `/analytics/margin-discounts` | Margin and Discounts | V1 | AN, VW | Base price/recognized revenue, commercial discount/customer benefit, promo/loyalty/bonus/other breakdown, amount/rate/share/penetration, stacking overlap, depth, cap breaches, margin, PVM, vs LY, attribution coverage and Result Trust |
| UI-AN-011 | `/analyses/custom` | Custom Builder | V1 | AN, DS | Dataset/population, metric/features, dimensions, typed filters, outlier policy, bucket/stratified mode, comparison, chart/table choice, preflight |
| UI-AN-012 | `/analyses/:id/results/:runId` | Result detail and trust | MVP | allowed | Immutable result, ChartSpec/table/distribution, treatment chip and sensitivity, filters, YoY diagnostics, limitations, lineage, save/report/export |
| UI-AN-013 | `/research` | Research Cases | MVP | AN, VW | Questions/cases, owner/status, pinned method/dataset, findings, related analytical products, create/open/filter |
| UI-AN-014 | `/research/:id` | Research Workspace | MVP | AN, VW | Outline/sections, narrative, metric groups, charts/tables/distributions, treatment evidence, drill/filter, findings vs comments, publish to dashboard/report/segment |
| UI-AN-015 | `/analytics/products` | Products | V1 | AN, VW | Product/category/brand contribution, revenue/orders/AOV/margin, `vs LY`, product/store/channel context and Result Trust |

Products является отдельным стабильным navigation/route identity для товарной аналитики. Он переиспользует утверждённую product/category/brand семантику Sales, Basket, Margin and Discounts и Custom Builder; произвольная новая товарная иерархия по-прежнему требует отдельного продуктового решения.

Для `UI-AN-003` действует принятая композиционная конкретизация: standalone Dataset control и standalone Result Trust row отсутствуют. Dataset/version, trust/freshness и дата-время последнего обновления объединяются в компактный result-level trigger в правой части блока результата; trigger остаётся доступным при `Chart ↔ Data` и открывает полный Trust drawer. Embedded Sales показывает revenue/orders/AOV/margin, trend и переключаемый contribution breakdown по channel/store/product. Chart и table имеют отдельные route-backed Focus / Explore actions; focus сохраняет period, `vs LY`, applied context, representation и return-to-origin.

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

### 9.14. Administration — 20 страниц

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
| UI-ADMIN-011 | `/admin/localization-themes` | Localization and themes | MVP/V1 | IA, WA | en/ru coverage, workspace defaults, four themes, report default, accessibility validation status |
| UI-ADMIN-012 | `/admin/system` | System lifecycle and upgrades | MVP/V1 | IA, OP | App/release/schema versions, compatibility, migrations, maintenance, upgrade requirement, license/SBOM/provenance, preflight, runbooks and guarded rollback |
| UI-ADMIN-013 | `/settings/branding` | Workspace Branding Assignment | MVP/V1 | WA | Allowed published profile, workspace preview, effective identity, impact, assign/rollback/reset without asset or CompanyPack editing |
| UI-ADMIN-014 | `/admin/brand-profiles` | Brand Profile Registry | MVP/V1 | IA | Installation/workspace profiles, lifecycle, base theme, asset/contrast status, usage impact, create and open |
| UI-ADMIN-015 | `/admin/brand-profiles/:id` | Brand Profile editor/detail | MVP/V1 | IA | Product identity, sanitized assets/icons/fonts, semantic tokens, login/email/report/XLSX/docs previews, validate, diff, publish and rollback |
| UI-ADMIN-016 | `/admin/company-packs` | Company Pack Registry | MVP/V1 | IA | Pack versions, compatibility, installed/bound workspaces, included config refs, manifest hash, import and create |
| UI-ADMIN-017 | `/admin/company-packs/:id` | Company Pack detail/preflight | MVP/V1 | IA | Contents without secrets/data, compatibility preflight, diff/impact, validate, publish, install/upgrade/rollback and export |
| UI-ADMIN-018 | `/access/:resourceType/:resourceId` | Report/Dashboard Access Policy | MVP | WA | Allowlisted resource type, grants/groups/expiry, effective-access preview, PII ceiling, diff, grant/revoke and audit deep link without content editing |
| UI-ADMIN-019 | `/settings/organization` | Organization Settings | MVP/V1 | WA | Draft/versioned hierarchy, unit lifecycle, primary member assignments, leadership scopes, validation, impact preview, publish and successor mapping |
| UI-ADMIN-020 | `/settings/organization/:orgUnitKey` | Department Access & Ownership | MVP/V1 | WA | DepartmentDataPolicy, dataset/row/column/PII ceilings, bounded cross-department grants, publication defaults, ownership handover, effective-access preview and audit |

### 9.15. Help — 1 страница

| ID | Route | Страница | Фаза | Роли | Основное содержимое и действия |
|---|---|---|---|---|---|
| UI-HELP-001 | `/help` | Help Center and keyboard shortcuts | MVP/V1 | all | Permission-aware search по shipped docs/Data Guides/codes, contextual help, shortcut reference, version/support and deterministic deep links |

**Итого: 117 target route-level страниц.** W08 подтвердил accepted baseline из 110 route frames, 25 overlays и 5 system surfaces на revision `181`. Product/UI delta `0.9.3/0.6.3` добавила шесть route identities без нового overlay или system surface и два reusable capabilities. W10 создал эти шесть frames, C25 и flow 10 и принят на revision `213` с historical design inventory `116/25/5`. `UI-AN-015` добавлен как route-contract backlog и не считается принятой browser composition до собственной HTML acceptance и registered-component proof.

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
| UI-CAP-020 | Discount components, cap and PVM trust | Mapping/policies/metrics/methods, Margin & Discounts, Result/Research/export | UC-027, DISCOUNT-001…020, PVM-001…006, METRIC-017…020, METHOD-009…014 |
| UI-CAP-021 | Organization-scoped effective access and ownership | Shell/navigation, organization/admin/access, libraries, report/dashboard/detail/actions | UC-028, RBAC-019…028, TEST-INV-076…084 |
| UI-CAP-022 | Privacy-safe People & Creators | Organization/People, report/dashboard libraries, contributor cards/profile | UC-029, RBAC-022, RBAC-027, TEST-INV-078…088 |

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

### 11.3.1. Discount components, cap и PVM

`UI-AN-010` использует один compact result pattern, но не сворачивает разные
экономические понятия в «total discount». Context Bar показывает dataset/policy,
period, `vs LY` и filters. KPI strip имеет максимум четыре компактные ячейки:
base-price GMV, recognized net revenue, commercial discount и customer benefit;
остальные показатели находятся в ordered MetricGroup table и charts.

Основная композиция:

1. component bridge/stacked view для promo, loyalty, bonus redemption и other;
2. table с amount, eligible base, rate, share, penetration, `vs LY`, attribution
   mode/coverage и full typed value;
3. stacking overlap matrix и discount-depth distribution;
4. cap diagnostics с policy/base/rate/tolerance, breach count/amount/share и
   отдельным historical/simulated state;
5. exact-reconciled PVM waterfall/table с price, volume, mix, assortment,
   residual и comparable coverage;
6. margin/recognized-revenue view, linked drill-down и on-demand Result Trust.

Direct/rule-derived/residual/total-only/unavailable имеют различимые badges и
не полагаются только на цвет. Proxy и partial coverage всегда видны рядом с
числом и раскрываются в Result Trust. Historical breach показывается как source
fact и diagnostic, а не исправленный value; simulated breach блокирует publish.
Promotion Journal overlap может быть contextual overlay, но не создаёт promo
attribution без sale-level flag/direct mapping.

Authoring path распределён по существующим routes: `UI-DATA-008` mapping,
`UI-DATA-010` effective policy/stacking/cap, `UI-DATA-013…014` metric
certification/proxy evidence, `UI-DATA-021…022` method availability/robustness,
`UI-AN-002/011` setup, `UI-AN-012` immutable result и `UI-AN-014` research.
Отдельный URL только ради этой configuration chain не создаётся.

В `UI-AN-002` analysis identity размещается внутри штатной Configuration,
а capability preflight и продолжение — внутри штатных validation/right-rail
regions. В `UI-AN-011` builder pins остаются внутри Configuration, а
MetricGroup availability, cap и table preview — внутри существующих правых
regions. W08 methodology content не должен добавляться полноширинным слоем,
перекрывающим Configuration, Metric groups или compact Result Trust.

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

### 13.5. Organization, department access и People & Creators

Company navigation объединяет `Organization` и `People & Creators`, но не смешивает admin configuration и business browsing. `UI-ORG-001/002` доступны в policy-filtered read mode всем members; edit actions появляются только при `organization.manage` или более узком delegated permission. `UI-ADMIN-019/020` являются полноценными editor routes с dirty guard, version diff, impact preview, publish и audit.

Organization tree:

- показывает `company/division/department/team`, active/inactive/merged status, primary member и leader labels; counts вычисляются после visibility filtering и MAY быть заменены на `Restricted`;
- selection открывает Department Hub, а не nested modal; Back сохраняет expanded nodes, scroll и focus;
- member assignment требует ровно один primary department/team; transfer preview показывает lost/gained scopes, grants to review и published-resource handover;
- leadership editor задаёт unit, `include descendants`, effective dates и reason; слово `Manager` само по себе не выдаёт permission;
- Department Access отображает data/object/row-column/PII ceilings отдельными слоями и итоговый allow/deny с объяснением без hidden values;
- cross-department grant требует subject, bounded resource/data/actions, reason, start/expiry и preview; indefinite grant требует более строгого policy permission.

People & Creators:

- default presentation — compact card grid с avatar/initials, name, primary department, visible role hints, visible dashboard/report counts и recent activity; table alternative обязательна;
- sorting по name/department/recent activity разрешена только внутри effective scope; ranking, leaderboard, productivity score, percentile и comparison-to-peers отсутствуют;
- contributor profile разделяет `Created by`, `Owned by department`, `Collaborated on` и не включает inaccessible asset в count;
- self-view, leader-view и explicit-grantee view имеют явный privacy/scope badge; Workspace Administrator без `organization.activity.read` видит configuration, но не activity;
- loading/empty/filtered-empty/partial/forbidden/inactive/transferred states имеют объяснение и безопасное next action; удалённый/уволенный пользователь не исчезает из historical attribution.

`C25 Organization, Access & People` содержит Org Tree, Unit Card, Membership/Leadership Assignment, Data Policy Summary, Effective Access Preview, Handover Status, Contributor Card и Activity Summary. Flow 10: `Organization → Department Hub → People → Contributor Profile → visible report → Back`, плюс admin branch `Organization Settings → transfer preview → access/ownership handover → publish`.

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

Каждая из 117 target route-level страниц проектируется минимум для применимых состояний; system surfaces используют отдельные contracts §10.1:

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

## 16. HTML-first UI delivery contract

### 16.1. Source of truth и stable identity

Historical accepted inventory `116/25/5` с W10 terminal revision `213` сохраняется как immutable evidence прежней композиции и route/domain coverage, но не является operational source для UI `0.7.0`. Единственный accepted visual source для текущего slice — W27 responsive HTML для `UI-AN-003`, его репозиторные source paths и browser evidence.

Целевой reusable source — versioned React/HTML components и semantic CSS tokens в `packages/ui-foundation/**`, machine-readable component/screen manifests в `packages/contracts/ui-design/**` и browser component catalog в `apps/web/**`. Каждый public component имеет stable code ID, typed props/states, token bindings, accessibility contract и DOM provenance attribute. Screen manifest ссылается на component IDs и props, но не копирует visible markup.

### 16.1.1. Slice-first foundation boundary

Global all-route catalog не является prerequisite. Каждый новый route или material composition delta сначала фиксируется в product/executable contracts, затем реализуется как isolated responsive HTML candidate, проходит fresh-browser validation и получает explicit product-owner acceptance. После acceptance только доказанные tokens, icons, primitives, patterns и compositions повышаются до reusable code foundation.

### 16.1.2. HTML-first screen acceptance cycle

1. Normative blueprint и executable contracts фиксируют scope, semantics, states и proof boundary.
2. Isolated responsive HTML candidate реализует выбранную композицию и проходит focused tests и fresh-browser review.
3. Product owner явно принимает либо возвращает HTML candidate на доработку.
4. Accepted decisions извлекаются в semantic CSS tokens, typed reusable components, registry/manifests и component catalog.
5. Accepted source screen пересобирается из этих компонентов без копирования markup.
6. Same-viewport DOM/visual browser QA доказывает структурную и визуальную эквивалентность.
7. Вторая composition собирается из того же registry, чтобы доказать реальное reuse.

HTML candidate не становится production implementation автоматически. Реальный ECharts rendering, command palette, More page actions, typed filter expressions/chips и внешние share/email/download/export side effects входят в последующие implementation tickets по мере появления соответствующего production boundary.

### 16.2. Целевая repository structure

```text
packages/ui-foundation/
  tokens/          semantic CSS tokens and four theme modes
  components/      primitives and reusable analytical patterns
packages/contracts/ui-design/
  token-registry   portable token identities and schema
  icon-registry    registered Lucide identities
  component-registry and schema
  screen-manifests and schema
  browser QA receipts
apps/web/
  UI Lab           inspectable component catalog
  accepted screens and second-composition reuse proof
```

W27 Sales Overview остаётся rollback visual reference. W29 извлекает из него foundation, пересобирает Sales Overview и рендерит Focus/Explore как вторую composition. W22 может начать production shell только после accepted W29 evidence.

### 16.3. Component strategy

Foundation применяет dependency direction `tokens → primitives → analytical patterns → screen compositions`. Repeated UI всегда создаётся как typed code component; screens и catalog используют те же imports. Компоненты связываются с semantic tokens, а не hardcoded fills/spacing/radii. В текущем scope поддерживаются ровно `abyss`, `graphite`, `frost`, `paper`.

### 16.4. Render output

W29 рендерит из registered components: Sales Overview Chart/Data, Result Trust drawer, Focus chart/breakdown, expanded/collapsed/hidden/resized Sidebar и compact `1024 × 768` state. Focus/Explore обязан использовать те же shell, toolbar, chart, data/trust primitives и token IDs; скопированный markup и duplicate private components не считаются reuse proof.

### 16.5. Prototype flows

Текущий accepted slice моделирует `Sales → Focus chart/breakdown → return` и on-demand Result Trust disclosure. Prototype interaction не заменяет runtime contract: Focus/deep links, Back/Escape, drawer focus management и side effects доказываются в production browser implementation.

### 16.6. Browser QA matrix

Same-viewport QA проверяет exact route/title/control order, DOM component provenance, no clipping/overlap, Russian long-copy fit, Sidebar state affordances, stable semantic icon identities, compact KPI/Chart/Data/Trust/Focus composition, `1440 × 900` и `1024 × 768` reflow, console/network health и four-theme token compatibility. Screenshot diff доказывает visual equivalence с W27 accepted source, а structural receipt — реальное использование registry/components. Authorization, API, persistence, measured performance и external side effects остаются отдельной implementation boundary.

## 17. Traceability к product blueprint

| UI-область | Основные источники |
|---|---|
| Roles/navigation | §2.1, RBAC, AUTH |
| Organization/People | UC-028/029, RBAC-019…028, TEST-INV-076…088, V1-AC-037…043 |
| Onboarding | JOURNEY-001, UC-008, UX-JOURNEY-001 |
| Data Foundation | JOURNEY-002, UC-024, Connection/Catalog/Semantic/Metric/MetricGroup/NumberFormat/FileImportTemplate/Filter contracts |
| Quality | JOURNEY-003, DQ contracts, UC-003/009 |
| Analytics, Segments и Research | §12, UC-004/012/017…020/025/026/027, OUTLIER, SEGMENT, DISCOUNT, PVM, METHOD, RESEARCH, comparison/filter/chart/FOCUS contracts |
| Forecasting | JOURNEY-005, §13, ForecastSpec/Backtest/Model Registry |
| Promotion Journal | UC-013, PROMO, `range_timeline` |
| Dashboards/comments/access | DASHBOARD-007…012, RBAC-009…015, UC-021/022 |
| Reports/email/XLSX | UC-014/015/027, REPORT, REPORT-MAIL, XLSX-001…014, METRIC-009…020, DISCOUNT-017, PVM-006 |
| Pipelines/runs | JOURNEY-006, PIPELINE, RUN/EXEC/PROGRESS |
| Notifications | NOTIFY, RESOLVED-007 |
| Admin/operations | OPS, COMPUTE, access policies, BrandProfile/CompanyPack, backup, plugins и audit |
| Branding/i18n/a11y | BRAND, CompanyPack, THEME, I18N, A11Y, RESOLVED-006/008/016/027 |
| URL/history/workspaces | ROUTE-001…012, TEST-INV-050, V1-AC-017 |
| Motion/loading | MOTION-001…012, PROGRESS, TEST-INV-051, V1-AC-018 |
| System/help/lifecycle | SYS-UI-001…005, HELP-001…004, ADMIN-010…011, NOTIFY-014…015, V1-AC-019 |

## 18. Phase 0 gap analysis и решения перед HTML-first component foundation

### 18.1. Что существовало в репозитории до HTML-first пилота

- нормативные machine/human blueprint;
- four-theme palette registry;
- роли, journeys, APIs, states и acceptance contracts;
- React/pnpm workspace scaffold без UI implementation.

### 18.2. Что существует в Linear reference archive

- dark authenticated shell, expanded/collapsed navigation и hover states;
- list/table, settings, popover, modal, combobox, tabs и right detail pane;
- user-confirmed pointer-resizable sidebar intent;
- source archive SHA-256 и per-image hashes в `docs/architecture/ui/linear-workspace-reference-manifest-v1.json`.

### 18.3. Что отсутствует

- production implementation identity и runtime artifact package;
- production component catalog, code registry и screen manifests beyond the accepted `UI-AN-003` HTML slice;
- official logo SVG/brand pack;
- all-four-theme captures, command palette, keyboard/focus snapshots, motion recordings, error/loading/session state references и measured geometry;
- browser implementation и perceived-performance baseline;
- утверждённый mobile authoring scope.

### 18.4. Утверждённые и применённые решения scope lock

1. Сохранить W10 historical artifact как accepted evidence; вести UI `0.7.0` slice-first только через repository-owned HTML/React source, semantic CSS tokens, component registry/manifests и browser evidence.
2. Сохранять принятые historical `116/25/5` и добавить `UI-AN-015` как 117-й target route только через собственный HTML acceptance → component/registry promotion → browser QA cycle; W08 покрывает исторические первые 110, W10 добавил шесть Organization/People/Admin frames; post-v1 B2B/Yandex/activation/GMM/HDBSCAN/automatic-K/multivariate-anomaly/ABC-XYZ/OIDC/Kubernetes/public API UI не включать.
3. Использовать ровно четыре темы `abyss`, `graphite`, `frost`, `paper`; проверять representative matrix, не дублируя каждый route.
4. Использовать self-hosted versioned Inter Variable; Linear font files не копировать.
5. Использовать text-only wordmark до получения официального SVG; generated logo из референса не перерисовывать.
6. Считать route-level page единицей обязательного изображения; wizard steps и drawers поставлять state sheets, а не увеличивать основной счётчик страниц.
7. Использовать canonical `/w/:workspaceKey/*` routing, route-backed Focus, production motion matrix и Help/System contracts до следующей массовой генерации/export.
8. Использовать Lucide/`lucide-react` как единственную v1 core icon family; expanded sidebar показывает icon + label, collapsed/tablet — icon-only без сокращений.
9. Использовать единый compact reporting geometry contract: header metadata от `y=80`, Context Bar `48 px`, KPI Strip `64 px`, primary data block от `y=308`, совпадающие Context/KPI boundaries.
10. Использовать React/TypeScript/Vite/MobX/TanStack Query/styled-components, route-bounded fallback и performance budgets WEB-PERF-001…006; backend и W11-W17 не менять.

## 19. Contract impact текущего документа

| Поверхность | Классификация | Пояснение |
|---|---|---|
| Product/API/ports/persistence | `none` для UI transition | Backend, domain, REST/SSE и W11-W17 не меняются |
| Browser-visible behavior | `breaking-change with fallback` | Linear-workspace shell, panels, four themes, keyboard and motion replace the old composition route-by-route; stable route IDs remain |
| Request hash/cache identity | `compatible-change` | Applied result filters используют общий normalized contract; presentation-only state явно исключён |
| URL/bookmark/history | `breaking-change` для будущих legacy URLs; сейчас `compatible-change` | Канонический workspace prefix `/w/:workspaceKey`; Foundation runtime и stable bookmarks отсутствуют, поэтому миграция выполняется до первого release consumer |
| Design tokens/defaults | `breaking-change` before stable runtime | Six-theme/single-Frost historical target replaced by exactly abyss/graphite/frost/paper and semantic CSS variables |
| HTML/code foundations/components/manifests | `breaking-change before stable runtime` | Existing external-identity artifacts become historical-only; accepted responsive HTML slices add versioned tokens, components, manifests, catalog entries and browser receipts in the repository |
| Migration/rollback | `compatible route identities` | Existing shell remains fallback until each route slice has browser/a11y/performance evidence |

## 20. Phase 0 exit criteria

Historical Phase 0 design acceptance завершена: W08 принят на revision `181`, W10 — на terminal revision `213` с global `116/25/5`. Эти evidence подтверждают прежнюю композицию и route/domain coverage, но не новый Linear-workspace target. UI `0.7.0` использует transition cycle W19 reference completion → W20 architecture spike → W21 historical pilot → W24-W27 responsive HTML acceptance → W29 HTML-first UI foundation → W22 browser shell → W23 real Sales Analytics golden slice. Browser/runtime accessibility, authorization, persistence и performance не следуют из historical design evidence или HTML review сами по себе.
