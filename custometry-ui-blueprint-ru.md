---
document_family_id: CUSTOMETRY-UI-BLUEPRINT
document_id: CUSTOMETRY-UI-BLUEPRINT-RU
title: Custometry — требования к Web UI и целевая концепция
ui_spec_version: 0.8.0-draft
source_product_spec: 0.10.0-draft
source_documents:
  - ./custometry-technical-blueprint-ru.md
  - ./custometry-technical-blueprint-human-ru.md
  - ./docs/architecture/ui/target-pilot/manifest.json
status: accepted_ui_requirements
normative: false
language: ru
created_at: 2026-07-15
updated_at: 2026-09-04
artifact_role: product_ui_requirements_and_current_inventory
program_route: ticket_first
active_program: null
current_execution_route: docs/architecture/ui/custometry-web-implementation-source-contract-v1.md
visual_authority:
  status: accepted_target_ui_concept
  source_evidence_mode: renderable_html
  scope: demonstrated_composition_behavior_and_visual_language
  manifest: ./docs/architecture/ui/target-pilot/manifest.json
target: adaptive_responsive_web_application
mobile_scope: unauthorized
---

# Custometry — требования к Web UI и целевая концепция

## 0. Статус и назначение

Этот документ переводит продуктовый blueprint Custometry `0.10.0-draft` в исходные требования к Web UI: пользовательские результаты, роли, journeys, данные, текущие поверхности, состояния, действия, permissions, accessibility, localization и responsive-приоритеты.

Документ является производным источником UI-требований и не изменяет нормативную продуктовую спецификацию. Если UI-требование противоречит `custometry-technical-blueprint-ru.md`, действует machine blueprint. Новая бизнес-функция сначала появляется в machine blueprint и его human mirror, затем получает UI-представление здесь.

В этом документе сейчас зафиксированы:

- текущий продуктовый и функциональный baseline;
- текущий реестр `117` route-level страниц, `25` overlays, `5` system surfaces и `22` cross-surface capabilities;
- обязательные lifecycle, data, permission, loading, empty, partial, error, recovery и terminal states;
- сквозные требования к аналитике, исследованиям, прогнозам, отчётам, операциям, администрированию, accessibility и localization;
- историческое evidence W03-W10 как свидетельство прежнего покрытия, но не как текущая визуальная власть;
- принятая capability expansion: общий multi-page Analytical Document, universal block builder, точные notes/annotations/discussions, time-aware segmentation, Products/Categories/Assortment/Inventory, digital acquisition/retail journeys, unit economics, adoption и analytical-performance administration;
- финальный интерактивный RU/EN пилот как целевая UI-концепция, включая показанную композицию, навигацию, аналитические взаимодействия и визуальный язык.

Frontend architecture определяется ADR-0007. Финальный пилот сохранён в `docs/architecture/ui/target-pilot/` и является целевой концепцией, а не только визуальным ориентиром. Он не показывает все экраны и не доказывает готовность production-кода. G0–G6 программа и её материалы удалены по решению владельца 2026-09-04; восстановление из Git описано в `docs/architecture/ui/ui-program-retirement.md`. Продуктовые требования и рабочий код сохранены, дальнейшее приведение UI к концепции выполняется обычными implementation tickets.

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
→ создать или выбрать versioned product/category hierarchy, assortment и segment snapshot
→ выполнить research от общего к частному или прогноз
→ зафиксировать evidence-linked findings
→ понять достоверность результата
→ собрать Dashboard, многостраничный Workbook/Report или narrative Research через один guided block builder
→ организовать chapters, page tabs, sections и blocks и опубликовать один immutable root snapshot
→ назначить requester/executor и обсудить document/page/block/data через notes, annotations, comments, mentions, likes и follows без расширения прав
→ увидеть privacy-safe adoption и permission-filtered activity
→ связать impression/click/session/install/app/web с online/offline purchase/refund/repeat и посчитать governed unit economics
→ увидеть reuse/materialization plan и стоимость только действительно нового compute
→ поставить metric watch без внешнего activation
→ отправить email или выгрузить XLSX
→ диагностировать run и инфраструктуру
```

### 1.3. Целевые пользователи

| Сокращение | Роль | Главная задача в UI |
|---|---|---|
| `IA` | Installation Administrator | Установка, сервисы, плагины, backup, global policies и suppressed aggregate adoption/capacity без неявного доступа к workspace data/identity |
| `WA` | Workspace Administrator | Users, roles, report/dashboard access, connections, policies, branding и scoped aggregate-first adoption без аналитического authoring по умолчанию |
| `DS` | Data Steward | Catalog, mapping, data contracts, Data Guide и Data Quality |
| `AN` | Analyst | Метрики, методики, research, сегменты, dashboards, reports, requester/executor collaboration, watches, send и exports без управления connections/access grants |
| `ML` | ML Analyst | Forecast specifications, backtests, models и monitoring |
| `OP` | Operator | Runs, schedules, attempts, queues, recovery и acknowledgements |
| `VW` | Viewer | Просмотр, comments, likes, follows, feed и watches для разрешённых non-PII результатов без изменения definitions/snapshots |

Один пользователь может иметь несколько ролей. Навигация и действия формируются из effective permissions, но расположение разрешённых функций остаётся стабильным.

## 2. Принятые требования и целевая концепция

### 2.1. Принятое направление

- строится цельный продукт с максимальным покрытием responsive Web;
- текущий функциональный baseline используется как исходное evidence, а не как потолок;
- Dashboard, Workbook/Report и Research обязаны использовать один document/page/section/block composer, но разные presentation profiles и reading journeys;
- Workbook/Report поддерживает большое число страниц-вкладок, chapter groups, overview/search/overflow, reorder/duplicate/hide/lock/group и deep links до page/block;
- universal block builder всегда начинает с subject/data product → metric(s)+grain → dimensions+period, затем условно добавляет Segment и опционально filters/comparison/presentation с trust/performance/reuse preflight;
- analyst note, data annotation, discussion comment и reviewed finding являются разными объектами; refresh не переносит anchor на новые данные автоматически;
- сегменты создаются и пересчитываются в отдельной части платформы, имеют definition/run/schedule/snapshot history и explicit pinned/latest-successful bindings для повторного использования;
- foundation включает Digital Acquisition & App, Products/Categories/Assortment/Inventory, governed unit economics, adoption и analytical-performance administration;
- целевое покрытие обязано включать routes, route flows, persistent shells, route-backed transients, overlays, system-state families, internal/non-visual surfaces и обоснованные historical exclusions;
- каждая поверхность получает source-backed purpose, data meaning, roles, permissions, regions, states, actions, outcomes, failure и recovery;
- mobile-specific information architecture и composition не входят в scope без отдельной текущей авторизации.

### 2.2. Текущие источники

| Область | Источник | Роль |
|---|---|---|
| Product meaning и обязательства | `custometry-technical-blueprint-ru.md` | Нормативный источник |
| Объясняющее представление | `custometry-technical-blueprint-human-ru.md` | Синхронизированное зеркало |
| Текущие UI requirements и inventory | Этот документ | Принятые требования, подлежат расширению |
| Route identity и execution policy | `packages/contracts/routes/ui-routes.json`, `ui-route-contracts.json` | Текущий исполняемый inventory, не доказательство полного target coverage |
| Surface coverage | `packages/contracts/routes/ui-surface-contracts.json` | Current-state evidence, не permanent ceiling |
| Исторический дизайн W03-W10 | `.codex/delivery/evidence/` | Historical-only, не visual authority |
| Принятый RU/EN HTML-пилот | `docs/architecture/ui/target-pilot/manifest.json` | Целевая композиция, поведение и визуальный язык показанного UI; не backend/architecture proof |
| Текущий Web-код | `apps/web/**` | Implementation evidence, не target baseline |

### 2.3. Зафиксированный scope и critical journeys

Материально необходимых owner inputs для этой requirements-итерации не осталось: продуктовый смысл, capability scope и целевая UI-концепция приняты. В included scope входят adaptive Web, все текущие surfaces, document profiles/composer, segment lifecycle/reuse, collaboration, digital acquisition/unit economics, product/category/assortment/inventory, adoption и analytical performance. Excluded: mobile-specific IA, presentation/story profile, B2B ontology, activation/reverse ETL, arbitrary browser code/notebooks и автоматические causal claims.

Приоритетные продуктовые journeys: `data-to-trusted-result`, `compose-large-workbook`, `publish-review-collaborate`, `refresh-with-stable-anchors`, `define-recalculate-reuse-segment`, `digital-to-offline-unit-economics`, `product-category-assortment-inventory`, `open-100x30-document-without-duplicate-compute`, `adoption-and-performance-operations`. Это требования, а не утверждение об их реализации.

Повторный intake и новая G-программа не требуются. Агент использует принятые требования, ADR-0007, целевой пилот и конкретный ready ticket. Нельзя требовать от владельца повторного описания уже принятого scope.

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

### 3.1. Политика внешних визуальных референсов

Внешний продукт, design system или platform guideline может стать только source-backed visual-language reference либо craft-check после явного выбора. Он не переносит в Custometry чужие сущности, тексты, assets, branding, source code, скрытые permission rules или platform-specific interaction без Web semantics. Один референсный экран не заменяет platform baseline и полный atlas.

Принятый финальный пилот задаёт показанные композицию, сетку, навигацию, панели, controls, Focus/Explore, charts/tables и визуальный язык. Для соответствующих поверхностей это целевая концепция, а не набор необязательных stylistic hints. Для отсутствующих экранов сохраняются продуктовые требования и применяются согласованные паттерны пилота; одинаковая композиция для всех экранов не навязывается. Fixture-данные и прототипные действия не заменяют production-контракты и browser evidence реализации.

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
  Customer Base
  RFM
  Cohorts
  Lifecycle
  Basket
  Stores & Channels
  Margin & Discounts
  Products, Categories & Assortment

Digital Acquisition & App
  Journey & Funnel
  Acquisition & Campaigns
  Attribution Comparison
  Unit Economics
  Identity & Cost Coverage

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
  Workspace Adoption
  Analytical Performance
```

Навигация показывает только разрешённые группы, но не используется как источник authorization. Показанные в пилоте композиция, navigation/context panels и collapse behavior являются целевыми. Для полного набора destinations, effective permissions, focus behavior, workspace switching и safe recovery действуют продуктовые контракты. Icon-only состояние обязано иметь локализованное accessible name, tooltip по hover/focus, visible focus и достаточную hit area. Отсутствующие в пилоте состояния уточняются в соответствующем implementation ticket.

### 4.2. Глобальный application shell

| Область | Содержимое |
|---|---|
| Product/global controls | Product identity, workspace switch, global search/command access, help, notifications и user menu; показанная композиция определяется целевым пилотом |
| Primary navigation | Permission-aware destinations, current location и доступный способ перехода/возврата |
| Page header | Breadcrumb, title, description/status, primary action и secondary actions |
| Context bar | Dataset/version, date range, comparison, filters, timezone/currency, saved view |
| Main content | Fluid page grid с ограничением читаемости long-form blocks |
| Context/detail surface | Detail, lineage, issue или node context без потери owning surface; placement определяется responsive contract |
| Progress surface | Persistent operation access; run продолжается после ухода со страницы |

### 4.3. Global search

Глобальный поиск и command access должны быть доступны с keyboard shortcut, объявленным в принятом baseline, и покрывать:

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

Машиночитаемый route contract разделён на три слоя. `packages/contracts/routes/ui-routes.json` остаётся компактным реестром identity/URL/title/release/status, `packages/contracts/routes/ui-route-contracts.json` хранит текущую исполняемую политику family/shell, role hints, permissions, guards, states, history/query и Focus для 117 известных страниц, а `packages/contracts/routes/ui-surface-contracts.json` хранит текущее покрытие routes, overlays, system surfaces и cross-surface capabilities. Portable schemas находятся рядом; семантический валидатор проверяет паритет с этим документом, все `UC-001…029`, product permission catalog и en/ru titles. Эти manifests являются current-state inventory и не доказывают полноту целевого покрытия. Role hints используются только для discoverability и не заменяют API authorization.

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

## 5. Adaptive Web и responsive requirements

Responsive Web обязателен. ADR-0007 задаёт диапазон 768–1920 CSS px и endpoint anchors; shell transformations, component queries и density behaviors проверяются для изменяемой реализации. Mobile-specific information architecture остаётся `unauthorized`.

Для реализации действуют следующие инварианты:

- reading order, user outcomes, primary actions, permission boundaries и data meaning сохраняются на всём принятом Web-диапазоне;
- сложные editors могут переходить к последовательным regions, если это не удаляет capability и не выдаёт новый mobile scope;
- горизонтальный scroll всей страницы не используется как основная responsive-стратегия; bounded data grids, timelines и canvases имеют явный affordance;
- content priorities задаются для каждой screen/state пары, а breakpoints выводятся из content pressure и принятого shell contract;
- keyboard, zoom/reflow, focus order, reduced motion и accessible alternatives проверяются на anchor viewports;
- фиксированные widths/heights допускаются только с source-backed причиной и responsive exception.

## 6. Platform UI — концепция и требования к реализации

Целевая концепция — сохранённый финальный пилот; архитектура — ADR-0007. Показанные shell, navigation, layout, controls и interactions приняты как target. Production tokens/components, отсутствующие состояния, responsive transformations, accessibility и copy policies реализуются и проверяются в bounded tickets без G0–G6.

### 6.1. Themes и semantic tokens

- показанная палитра пилота является целевой; runtime theme identifiers/defaults не меняются этой редакцией и приводятся к концепции отдельной реализацией;
- компоненты и ChartSpec используют semantic roles, а не hardcoded product colors;
- каждый принятый theme покрывает canvas/surface/text/border/accent/focus/status/positive-negative/chart roles и проверяется на contrast и color-blind-safe alternatives;
- theme preference не меняет domain values, run/artifact identity или cache identity;
- report/email/XLSX rendering pin-ит выбранный theme/brand version в snapshot и artifact identity;
- BrandProfile использует validated versioned semantic overrides, а raw CSS/HTML/JavaScript, remote fonts и untrusted runtime injection запрещены.

### 6.2. Typography, icons и assets

- typography наследует показанный пилотом характер; production font files, лицензии, fallback и en/ru metrics фиксируются при реализации;
- en/ru coverage, 200% zoom/reflow, dense-table readability и deterministic report rendering обязательны;
- одна согласованная icon system получает version/commit, semantic mapping, sizes, optical rules и license provenance;
- незнакомое действие не обозначается только icon, а status не кодируется только цветом или движением;
- official brand assets либо явно принятый temporary identity проходят sanitization, provenance и Web/email/XLSX/docs parity.

### 6.3. Layout, components и interaction patterns

- пилот определяет показанные shell regions, grid, spacing и layering; непоказанные variants и responsive transformations реализуются согласно продуктовым constraints;
- каждый reusable component определяет variants, size classes, internal elements, required interaction states, content rules и accessibility behavior;
- overlays, menus, dialogs, drawers, tooltips, tables, forms, charts, tabs и splitters получают placement, dismissal, focus, keyboard и state contracts;
- exact geometry и visual properties наблюдаются из принятого source evidence, а не изобретаются вручную;
- показанные palette, radius и shadow сверяются с пилотом; непоказанные motion states уточняются в implementation ticket.

### 6.4. Motion и perceived performance

- motion language, duration и easing сейчас не выбраны;
- feedback не задерживает action outcome, focus или live-region update;
- reduced-motion variant обязателен для каждого meaningful transition;
- charts не интерполируют изменение domain/axis или плотные/live data так, чтобы промежуточный кадр выглядел достоверным значением;
- performance budgets определяются для critical journeys и отдельно измеряют input feedback, client dispatch, network/API wait, response/SSE-to-paint и final interaction latency;
- previous authorized data либо reserved layout сохраняются при refresh без выдачи stale/optimistic presentation за persisted terminal truth.

## 7. Библиотека компонентов

### 7.1. Foundations

- semantic color roles и принятые theme modes;
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
| Analytical documents | Chapter Tree, Page Tab Strip, Page Overview/Search, Section, Block Catalog, Block Toolbar, Filter Scope Indicator, Document Open Plan, Publish Preflight |
| Collaboration | Analyst Note, Data Annotation Marker/Anchor Detail, Discussion Thread/Reply, Mention, Resolve/Reopen, Stale Anchor Banner, Re-anchor Diff |
| Segments | Segment Definition Summary, Run History, Schedule Status, Snapshot Picker, Binding Mode, Entrants/Exits, Migration/Overlap/Drift, Used By |
| Product analytics | Product Hierarchy, Category/SKU Table, Assortment Matrix, Inventory/Availability State, ABC/XYZ Matrix, Price/Markdown, Lifecycle Timeline, Affinity/Substitution Matrix |
| Digital | Journey/Funnel, Attribution Scope Switch, Campaign/Creative Breakdown, Identity/Cost Coverage, Unit Economics Ladder, Actual/Attributed/Scenario Legend |
| Administration | Adoption Summary, Content Usage Table, Materialization Hit Rate, Slow Document/Block, Avoided Work, Wasted Precompute, High-cost Request |
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

- когда surface использует primary KPI, они группируются в компактный strip, а не автоматически превращаются в ряд высоких декоративных cards; число KPI определяется metric group и задачей, а не universal `4`;
- published presentation задаёт default KPI-набор, но пользователь может сохранить личный выбор и порядок разрешённых compatible metrics в versioned personal Saved View; личная настройка явно помечается, сбрасывается к default и не меняет shared publication либо вид других пользователей;
- label, typed value, period/comparison и trust state читаются как одна compact group; full value остаётся доступным;
- Context Bar, KPI group и primary content используют согласованные alignment lines, но exact geometry определяется screen contract;
- primary visualization получает приоритет в первом рабочем viewport и не вытесняется декоративным whitespace;
- sample table показывает data rows и range/pagination status в pilot-compatible view; production placement зависит от document profile/page composition;
- Result Trust остаётся optional compact trigger и не резервирует постоянную широкую колонку;
- calm density является общим visual-language anchor, но fixed `KPI → chart → table` не является универсальным layout contract.

### 8.5.2. Metric groups, adaptive numbers и research narrative

- один `MetricGroupVersion` определяет group heading, group order и metric order; UI не сортирует метрики автоматически по label или текущему значению;
- KPI label, unit, aggregation и time basis берутся из MetricVersion и resolved period: годовая частота показывается как значение за выбранный год/период и не получает `/мес.`, если metric version не задаёт месячную нормализацию;
- visibility/order уже разрешённых KPI projections остаются presentation state; выбор метрики, которой нет в resolved result, проходит backend preflight и меняет normalized request/cache identity;
- compact display использует `NumberFormatSpec`: `75,44% → 75%`, `4,27% → 4,3%`, `0,234% → 0,23%`; non-zero value не отображается как `0%`;
- compact suffix (`K/M/B`, `тыс./млн/млрд`) не заменяет full value: оно доступно в tooltip/detail, accessible description и Data table;
- Research/Dashboard/Report используют ordered sections и heterogeneous blocks `narrative`, `metric_group`, `chart`, `table`, `finding`, `conclusion`, `methodology` и `result_trust`;
- approved Finding имеет author/review/evidence/limitations surface; comment имеет avatar/time/thread/resolve surface и никогда не выглядит как утверждённый вывод;
- Viewer может открыть и добавить comment только к разрешённой non-PII projection; comment drawer не показывает hidden filters, denied facets или raw source values;
- report/dashboard access находится в отдельной admin surface; Analyst видит effective access summary, но не grant/revoke controls.

### 8.5.3. Analytical document profiles, pages и collaboration

- `dashboard` — compact monitoring composition с live/pinned bindings и ограниченным authoring chrome;
- `workbook_report` — главы и большое число ordered page tabs; доступны overview/search/overflow, reorder, duplicate, hide, lock и group с keyboard alternatives;
- `narrative_research` — outline, long-form narrative и evidence-linked findings, но те же page/section/block/filter/snapshot contracts;
- deep link и Back/Close сохраняют exact document version/snapshot, page, optional block, scroll и focus;
- document/page/block filters показывают scope, inheritance и effective set; personal/shared Custom View не мутирует publication;
- analyst note публикуется с document version; data annotation pin-ит artifact/semantic data key; discussion остаётся отдельно; finding/conclusion проходит review;
- refresh показывает old/new context и не перемещает comments/annotations автоматически; explicit re-anchor имеет diff и audit;
- like доступен только в header published document version; rating, dislike, block/comment/cell reaction и employee score отсутствуют.

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

Количество известных routes не является потолком будущего atlas. Самостоятельный route обязателен, когда surface имеет durable entity/version lifecycle, должен открываться из notification/audit/deep link, требует собственных Back/refresh/unsaved semantics либо имеет независимую permission boundary и достаточно сложное состояние для bookmark/recovery. Transient подтверждение или inspector остаётся modal/drawer; повторяемое поведение таблиц, графиков и отчётов становится cross-surface capability. Каждый UI-visible use case обязан иметь binding хотя бы к одному из этих типов поверхности; совпадение количества строк между двумя JSON не является доказательством полноты.

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
| UI-AN-015 | `/analytics/products` | Products | V1 | AN, VW | Product/category hierarchy version, category/SKU performance, assortment/store clusters, inventory/availability, sell-through/DOI/turnover, ABC/XYZ, price/markdown/margin, lifecycle, affinity/substitution, promo overlays и Result Trust |

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
| UI-ADMIN-011 | `/admin/localization-themes` | Localization and themes | MVP/V1 | IA, WA | en/ru coverage, workspace defaults, accepted theme registry, report default, accessibility validation status |
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

**Итого: 117 основных route-level страниц.** Исторический W10 зафиксировал прежний inventory `116/25/5`; позднее current route registry добавил planned `UI-AN-015 Products`, поэтому фактический current inventory теперь `117/25/5`. Это не доказательство полноты целевого inventory и не означает, что остальные принятые target families уже имеют exact route identities.

### 9.16. Обязательное дополнительное продуктовое покрытие

Implementation tickets должны определить route/embedded/overlay identity и не могут исключить следующие результаты:

| Target family | Минимальное покрытие |
|---|---|
| Analytical Documents | Library/create, profile choice, chapter/page manager, page/block deep link, Custom Views, publish diff/root snapshot, large-document open plan |
| Collaboration | Document/page/block/data discussions, replies/mentions/resolve, analyst notes, annotations, stale anchor/re-anchor, approved-summary publication |
| Segmentation | Definition/run/schedule/snapshot history, pinned/latest binding, profiles, trends, entrants/exits, migration/overlap/drift, permission-filtered Used by |
| Digital Acquisition & App | Journey/funnel, first-user vs session scope, campaign/ad-group/creative, Web/iOS/Android reconciliation, identity/event/cost coverage |
| Unit Economics | CAC/CPI/CPA/ROAS/ROI/LTV/CM/payback, cohort/activity views, actual vs attributed vs scenario, assumptions and residuals |
| Products & Categories | Hierarchy versions, category/SKU performance, assortment/store clusters, inventory/availability, ABC/XYZ, price/markdown/margin, lifecycle, affinity/substitution, promo overlays |
| Adoption | Total/unique/repeat/active viewers, meaningful-view semantics, comments/likes/follows, freshness/trend, never/rarely used assets без ratings |
| Analytical Performance | Reuse/materialization hit, avoided work, slow documents/blocks, staleness, high-cost requests, wasted precompute и resource lanes |

## 10. Overlays, drawers и modals

Они не считаются отдельными route-level страницами, но получают собственные screen/state contracts и проверку в implementation tickets. `UI-OVR-020` исторически сохраняет prefix `OVR`, однако реализуется как route-backed surface, а не modal/overlay в DOM.

| ID | Surface | Вызывается из | Основные требования |
|---|---|---|---|
| UI-OVR-001 | Workspace switcher | Global shell | ROUTE-010 |
| UI-OVR-002 | Global command palette | Global shell | ROUTE-003, ROUTE-005, RBAC-006 |
| UI-OVR-003 | Searchable Filter Explorer | Любой reportable result | FILTER-002, FILTER-005, FILTER-007, FILTER-008, FILTER-011, FILTER-012 |
| UI-OVR-004 | Filter expression editor | Analytics/dashboard/report | FILTER-001, FILTER-003, FILTER-004, FILTER-009…012 |
| UI-OVR-005 | Period and comparison editor | Любой reportable result | UC-012, COMPARE-001…010 |
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

Эти capabilities не создают самостоятельную страницу только ради повторения одного control pattern, но являются обязательными машиночитаемыми bindings и будущими component/state contracts.

| ID | Capability | Применимость | Основные требования |
|---|---|---|---|
| UI-CAP-001 | Workspace routing, guards and return | Все protected routes | ROUTE-001…012, RBAC-002 |
| UI-CAP-002 | Searchable typed filters | Все разрешённые reportable datasets/results | FILTER-001…012 |
| UI-CAP-003 | Shared and block-local period comparison | Любая аналитическая отчётность | UC-012, COMPARE-001…010 |
| UI-CAP-004 | Metric groups and adaptive formats | Web/email/XLSX metric and table blocks | METRIC-009…016 |
| UI-CAP-005 | ChartSpec visualization | Все reportable visual blocks | UC-017, CHART-001…020 |
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

Принятый target delta пока не имеет новых стабильных `UI-*` IDs: exact identities определяются при проектировании соответствующих implementation tickets. Необходимо покрыть минимум девять surface families: analytical-document profiles/hierarchy; workbook pages/tabs/chapters; universal block builder; notes/annotations/discussions; segment runs/snapshots/bindings; digital journey/acquisition/unit economics; products/categories/assortment/inventory; materialization/reuse preflight; adoption и analytical-performance administration. Current manifests расширяются одновременно с реальными surface contracts, а не фиктивными свидетельствами готовности.

## 11. Страница аналитического результата

Все специализированные analytics pages используют общий data/trust vocabulary, но не один фиксированный layout. Pilot-compatible compact result MAY использовать следующую композицию:

```text
Page header
Context bar
  Dataset/version
  Period
  Comparison (`vs LY`)
  Search filters
  Saved view
Compact KPI strip: один общий контейнер, четыре ячейки без отдельных крупных cards
  Personal view: выбрать/упорядочить доступные KPI, сбросить к published default
Primary chart area
Secondary decomposition/chart
Data table
Compact Result Trust trigger; optional drawer on demand
Actions: save, dashboard, report, export
```

Если Result Inspector открыт как соседняя pane, его header MUST совпадать по высоте и baseline с Page header, а строка inspector tabs — со строкой report tabs/context bar. Inspector использует достаточную рабочую ширину для typed filter builder и адаптивно переходит в overlay на узком viewport; открытие/закрытие не должно создавать ложное перемещение основной области. Один toggle управляет обоими состояниями.

Inspector разделяет `Контекст`, `Фильтры`, `Обсуждение`, `Доверие` и `Виды`: typed filter builder начинается сверху собственной вкладки, а не после длинного контекста. В `Поделиться снимком` постоянно видны только `Копировать ссылку` и `Email-preflight ссылки`; resolved state снимка раскрывается по запросу. `Виды` позволяют применить versioned visual template на уровне отчёта и local override блока; конструктор палитр/типографики является отдельной Settings surface. Заметки и методика показывают permission-safe автора отчёта, дату обновления и publication version.

Это один screen pattern, а не форма каждого документа. Workbook page может быть narrative/table-first, comparison-first, scenario-first или mixed; Dashboard остаётся compact monitoring surface; Research использует outline/long-form evidence. Любая композиция сохраняет явные data bindings, filter scopes, Result Trust, accessible table alternatives и deterministic reading order.

### 11.1. Comparison

- default action: «Сравнить с аналогичным периодом прошлого года»;
- компактная подпись сравнения во всех локалях — `vs LY`; полная локализованная расшифровка используется в tooltip, accessible name и comparison editor;
- editor показывает resolved current/comparison ranges, timezone, calendar и coverage;
- delta содержит абсолютное и относительное изменение;
- неполный либо несовместимый период имеет warning/blocked state;
- comparison style одинаков для KPI, charts и tables.
- один report-level control задаёт shared grain/current period/comparison для всех вкладок;
- каждый chart/table block явно показывает `inherit` либо local month/quarter/year и comparison override; effective period всегда попадает в snapshot/export;
- `inherit` подписывается конкретно как «Как в отчёте · месяц/квартал/год», без несуществующего периода «общий»; смена grain меняет реальные bucket boundaries, число точек и строки таблицы, а chart/table/export читают один bucketed artifact;
- segment size и полная migration matrix используют exact current/comparison snapshots, показывают дельты и не скрывают возможные переходы.

### 11.2. Filters

- search по label, field name, entity, description и aliases;
- только разрешённые published fields;
- typed operator/value controls;
- hierarchy breadcrumb;
- null policy видна пользователю;
- sensitive facets/counts не раскрываются;
- active filters отображаются chips с keyboard removal;
- saved view pin-ит filter expression/version.
- catalog группируется по business entity и поддерживает поиск по label/description/aliases;
- AND/OR выражаются явными группами, а вложенные условия одного события/заказа сохраняют общий container scope;
- system/inherited filters, draft expression, applied expression и предварительная оценка результата визуально разделены; Apply повторно валидирует expression на backend.

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

Большой analytical document дополнительно следует такому contract:

- initial route загружает shell, permission-filtered page index и только active page; denied/hidden metadata не выдаётся через tabs, gaps или counts;
- direct deep link сразу гидратирует target page/block; соседняя page MAY prefetch только bounded policy, и prefetch не считается meaningful view;
- page switch отменяет ненужный client request, но не отменяет shared single-flight compute; одинаковые blocks/pages используют один operation link;
- внутри active page применяются bounded concurrency, block skeletons и virtualization/lazy fetch; browser не монтирует все страницы;
- page tabs имеют keyboard navigation, overflow/search/overview и chapter grouping; на узкой ширине они переходят в доступный overflow/list, а не обрезаются;
- `DocumentOpenPlan` показывает reuse/compute/last-good/blocked по page/block, freshness и ожидаемые resources без навязывания технических деталей обычному Viewer;
- design/benchmark envelope — 100 pages × 30 blocks/page с cold/warm open/switch, DOM/memory/request counts, duplicate-compute proof, RU/EN/pseudo-locale и 200% zoom; это не обещание unlimited и не hard production limit.

## 13. Forms и builders

### 13.1. Wizard

- sidebar либо top stepper;
- autosave только после валидного шага;
- Back/Continue не теряют данные;
- step error summary фокусируется и связывается с полями;
- unfinished draft можно продолжить из library;
- final step показывает normalized summary и impact.

Для действия `Add analytical block` общий wizard имеет обязательный порядок:

```text
1 Subject / data product
2 Metrics and grain
3 Dimensions and period
4 Population / Segment — только когда требуется
5 Filters — optional
6 Comparison — optional
7 Presentation — optional
8 Trust, performance and reuse preflight → Add
```

Guided и Advanced показывают один normalized `BlockDefinition` и сохраняют selections при переключении. Preflight показывает capability/permission blockers, grain, rows/bytes/time class, freshness, compatible artifact и planned compute. Draft resumable, но autosave не запускает compute. `Add` всегда называет destination page/section и reuse outcome.

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
1 Definition scope & observation-window policy
2 Features & Metrics
3 Data Treatment
4 Method & Group Count
5 Preview & Validation
6 Publish
```

- Step 1 фиксирует dataset/version, entity grain, eligible population и reusable observation-window policy; exact as-of задаётся SegmentRun, а не переписывает definition.
- Step 2 разрешает только опубликованные features/metrics, показывает type, missingness, PII class и запрещает identifiers/leakage.
- Step 3 использует `UI-OVR-025`; default `Flag only`, а `Exclude/Winsorize` требуют impact acknowledgement.
- Step 4 предлагает rule, RFM, quantile/equal-width/custom bucket и KMeans; exact group count обязателен там, где это применимо. HDBSCAN/GMM/automatic-K controls в v1 отсутствуют.
- Step 5 показывает bucket/distribution/cluster profiles, sizes, center/feature distinctions, stability, silhouette/limitation, treatment sensitivity, minimum-cell privacy и blockers. Для KMeans diagnostic K-1/K/K+1 не меняет выбранный K.
- Step 6 показывает normalized immutable definition, pinned boundaries/treatment/preprocessing/seed, downstream impact и publish diff.

`UI-SEG-003` использует tabs `Overview`, `Definition`, `Runs & Schedule`, `Profiles`, `Members`, `Snapshots & Migration`, `Diagnostics`, `Usage`. Header показывает definition version, last successful, next run, failed/paused state, selected snapshot и binding mode. Trends включают size/value, entrants/exits, migration, overlap и drift. `Members` и excluded/flagged observations загружаются только после authorization и PII policy. Frozen-model assignment и full retrain имеют разные actions и confirmation copy; retrain создаёт новый snapshot и не переименовывает historical cluster IDs. Published Workbook/Research выбирает `pinned_snapshot`; live Dashboard может явно выбрать `latest_successful`, но publish preflight показывает resolved snapshot и freshness. `Used by` permission-filtered и не раскрывает denied assets.

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
- каждый responsive anchor и large-document state проверяется на RU, EN и pseudo-locale expansion; tabs, breadcrumbs, primary/overflow actions, trust badges и table chrome не clipping-ся и не исчезают;
- CSS logical properties используются с начала проекта.

### 14.3. Content style

- короткие action labels: «Проверить», «Опубликовать», «Повторить узел»;
- destructive действия называют объект и последствие;
- empty state объясняет prerequisite;
- technical details доступны по раскрытию, но stable code сохраняется;
- причинность не утверждается без соответствующего метода;
- `warning`, `degraded` и `failed` не используются как синонимы.

## 15. Обязательные состояния

Каждая из 117 известных route-level страниц и каждая новая поверхность будущего atlas проектируется минимум для применимых состояний; system surfaces используют отдельные contracts §10.1:

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

## 16. Реализация и проверка

Активной G-программы нет. Она удалена по текущему решению владельца.
`active_program: null` не означает отсутствие принятого дизайна: финальный
пилот — целевая UI-концепция. Текущий execution route определён в
`docs/architecture/ui/custometry-web-implementation-source-contract-v1.md`;
статус исполнения берётся только из frontmatter конкретного тикета.

Каждый implementation ticket использует минимальный релевантный контекст:

- purpose, user outcomes, domain entities и included/excluded scope;
- затронутые routes/screens, роли, permissions, data reads/writes/computed values;
- entry/exit, transitions, states, actions, outcomes, failures и recovery;
- показанные в пилоте regions, controls и interactions;
- accessibility, locales, responsive priorities и performance constraints;
- материальные unresolved inputs, которые нельзя вывести из принятых источников.

Текущие manifests фиксируют `117` routes, `25` overlays, `5` system surfaces,
`22` cross-surface capabilities и `29` use-case bindings. Это нижняя граница
известного coverage, не permanent ceiling и не свидетельство полной реализации.
Нельзя терять persistent shells, route flows, route-backed transients,
internal/non-visual surfaces и обоснованные historical exclusions.
Исторические W03-W10 и revision `213` сохраняют evidence прежнего покрытия,
но не подтверждают соответствие нынешней концепции.

Browser proof создаётся один раз в изменяемом implementation boundary:
критические состояния и действия, RU/EN, console/network, keyboard/focus,
accessibility smoke и применимые anchors 768/1920 CSS px. Это не полная
WCAG-сертификация, не доказательство backend authorization, performance или
deployment. Не требуются family review boards, G-stage receipts и
every-state-by-every-viewport screenshots.

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
| Analytical documents/builders | GOAL-017, ANALYTICAL-DOC-001…012, BLOCK-BUILDER-001…008 |
| Collaboration/adoption/annotations | GOAL-014, COLLAB-001…023, WATCH-001…006, AC-046…047 |
| Segments over time | SEGMENT-001…026 |
| Products/categories/assortment | GOAL-018, PRODUCT-ANALYTICS-001…012 |
| Compute reuse/materialization | GOAL-015, MATERIALIZE-001…019, AC-048 |
| Digital journey/marketing/unit economics | GOAL-016, DIGITAL-001…015, ATTRIBUTION-001…010, UNIT-ECON-001…014, ASSUMPTION-001…006, V1-AC-044…047 |

## 18. Оставшиеся вопросы реализации

### 18.1. Что уже известно

- нормативные product machine/human blueprints;
- роли, use cases, journeys, permissions, data contracts, lifecycle и acceptance requirements;
- current-state route/surface manifests и localization catalogs;
- широкий функциональный baseline аналитики, data foundation, quality, forecasting, research, reporting, operations и administration;
- принятые базовые contracts для collaboration/adoption/watches, compute reuse/materialization и digital-to-offline attribution/unit economics;
- историческое route/domain coverage W03-W10;
- принятый product path и hash-pinned финальный интерактивный RU/EN пилот как целевая концепция;
- responsive Web как единственная сейчас авторизованная UI-платформа.

### 18.2. Что ещё предстоит реализовать и проверить

Пилот уже сохранён в репозитории, frontend architecture и диапазон Web
определены ADR-0007. Нужны проверка расхождений рабочего UI с концепцией и
bounded implementation tickets. Реальные состояния, permissions, API,
responsive, accessibility и performance проверяются на работающем продукте.

Текущие `117/25/5/22` manifests не являются полным покрытием новых capabilities.
Проектирование и реализация должны учесть как минимум:

- chapter/page/tab document composition, universal block builder, Custom Views и 100x30 open/publish path;
- requester/executor, analyst notes, data annotations, anchored discussions/replies/re-anchor, mentions/likes/follows и permission-filtered activity feed;
- segment definition/run/schedule/snapshot/binding/trend/migration/usage;
- products/categories/assortment/inventory/availability/ABC-XYZ/pricing/lifecycle/affinity;
- workspace/install adoption, metric watches и governed assumption input/review;
- materialization/reuse observability, freshness/last-good, invalidation, off-peak policy и interactive/precompute capacity;
- event taxonomy, web/app journeys/funnels, identity coverage, touch/spend/cost reconciliation, attribution comparison и unit economics.

### 18.3. Решения, которые не переносятся автоматически

Показанные в финальном пилоте композиция, панели, controls и visual choices имеют текущий target status. ADR-0007 сохраняет frontend technology decisions. G-boards, старые themes и historical design receipts не являются дополнительной authority. Рабочий код не откатывается; его соответствие концепции и полнота покрытия проверяются последующими tickets.

## 19. Contract impact текущей редакции

| Поверхность | Классификация | Пояснение |
|---|---|---|
| Product/API/ports/persistence | `additive plus planned schema-v2 breaking targets` | Новые product/category/digital/collaboration поля additive; common composition и SegmentSnapshot identity требуют future versioned migration, legacy read adapters и отдельного implementation evidence |
| Documentation/design authority | `breaking-change` | G-программа и её материалы удалены; финальный пилот принят как target concept, продуктовые требования и рабочий код сохранены |
| Current route/surface identity | `compatible current-state evidence` | 117/25/5/22 сохраняются для traceability, но не являются target ceiling или доказательством реализации |
| Browser-visible target | `accepted_target_ui_concept` | Финальный пилот принят как концепция; conformance production-кода пока не доказан |
| Frontend architecture | `accepted for current Web implementation` | ADR-0007 фиксирует текущий responsive-Web stack и ownership; изменение этих решений требует отдельного source-backed architecture decision |
| Request hash/cache identity | `new compatible namespace required` | Document/page/filter/segment/materialization versions входят в future normalized identity; zoom/legend/tab chrome остаются presentation-only |
| Mobile scope | `unauthorized` | Адаптивный Web обязателен; mobile-specific IA/composition не добавлены |
| Rollback | `documentation recovery only` | Возврат старого target требует нового owner decision; Git history сама по себе не создаёт authority |

## 20. Следующий шаг

Принятые product/UI requirements и целевая концепция не требуют повторного
проектирования через G0–G6. Следующий шаг — узкая оценка расхождений
рабочего frontend с пилотом и обычные implementation tickets для приведения
к концепции и полного продуктового покрытия. Эта редакция не создаёт W39,
prompt pack, ledger или новую UI-программу.

Observed proof этой редакции ограничен согласованностью источников,
сохранением требований и переносом пилота. Он не подтверждает полную готовность
UI, production conformance, accessibility, performance или deployment.
