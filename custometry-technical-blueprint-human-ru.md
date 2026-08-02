---
document_family_id: CUSTOMETRY-TECH-BLUEPRINT
document_id: custometry-technical-blueprint-human-ru
spec_version: 0.9.4-draft
representation: human
normative: false
status: draft
language: ru
created_at: 2026-07-14
updated_at: 2026-08-01
source_of_truth:
  document_id: CUSTOMETRY-TECH-BLUEPRINT-MACHINE-RU
  path: ./custometry-technical-blueprint-ru.md
  expected_spec_version: 0.9.4-draft
project_name: Custometry
license_target: Apache-2.0
---

# Custometry — полный технический план платформы

> Это человекочитаемое смысловое зеркало спецификации `0.9.4-draft`. Нормативным источником истины является [машиночитаемый blueprint](./custometry-technical-blueprint-ru.md). Обе версии относятся к семейству `CUSTOMETRY-TECH-BLUEPRINT`, имеют одинаковый `spec_version` и одинаковый набор нормативных requirement ID. При любом расхождении действует machine-версия.

## 0. Как читать этот документ

Документ описывает открытый self-hosted продукт Custometry целиком: пользовательские пути, модель данных, аналитику и прогнозирование, выполнение процессов, безопасность, эксплуатацию, интерфейс, этапы выпуска и критерии готовности. Он рассчитан на разработчиков, аналитиков, ML- и data-инженеров, тестировщиков, DevOps-инженеров, владельцев продукта и будущих контрибьюторов.

Machine-версия использует нормативные слова `MUST`, `SHOULD` и `MAY`. Здесь они передаются обычным языком, но стабильные ID сохранены без изменений.

| ID | Как понимать правило |
|---|---|
| DOC-RULE-001 | `MUST` означает обязательное требование |
| DOC-RULE-002 | `SHOULD` означает рекомендуемый подход; отклонение оформляется ADR |
| DOC-RULE-003 | `MAY` означает необязательную возможность |
| DOC-RULE-004 | Источником истины о run state является PostgreSQL, а не очередь |
| DOC-RULE-005 | Источником истины опубликованной логики является её неизменяемая версия |
| DOC-RULE-006 | Результат воспроизводится по версиям входов, конфигурации и кода |
| DOC-RULE-007 | Machine-документ нормативен, human-документ объясняет тот же набор требований |
| DOC-RULE-008 | CI проверяет версию, взаимные ссылки и совпадение requirement ID |
| DOC-RULE-009 | Одна инсталляция изолированно обслуживает несколько workspaces |
| DOC-RULE-010 | Новое обязательство сначала появляется в machine-версии; human-версия не вводит собственных требований |

## 1. Что представляет собой Custometry

Custometry — открытая self-hosted low-code операционная система B2C retail-аналитики. Она превращает разрозненные клиентские и транзакционные данные, локальные методики и повторяющиеся ad hoc-запросы в управляемый цикл: бизнес-вопрос, утверждённая методика, воспроизводимое исследование, проверенный вывод, опубликованный аналитический продукт и доступный бизнесу результат.

Модель B2C retail является текущей канонической моделью. Будущее расширение на B2B sales добавляется отдельными сущностями и контрактами: `Customer`, `Receipt`, `Product`, `Store` и `Channel` не переименовываются в `Account`, `Lead` или `Opportunity`.

Главная ценность — не canvas сам по себе, а общее понимание клиента, идентификаторов, чека, позиции, товара, магазина, канала, календаря, продаж, возвратов, скидок, себестоимости, активности, когорт, сегментов и прогнозируемых метрик.

### 1.1. Цели проекта

| ID | Цель |
|---|---|
| GOAL-001 | Подключать существующие данные без переноса всей инфраструктуры компании внутрь платформы |
| GOAL-002 | Работать с неполными данными и явно объяснять доступные, ограниченные и недоступные функции |
| GOAL-003 | Давать типовую аналитику без написания Python |
| GOAL-004 | Расширяться через Python SDK и доверенные плагины |
| GOAL-005 | Версионировать и воспроизводить расчёты |
| GOAL-006 | Проверять прогнозы временным backtesting и baseline-моделями |
| GOAL-007 | Работать на одном self-hosted сервере и масштабироваться воркерами в пределах поддерживаемой topology |
| GOAL-008 | Не связывать бизнес-логику с одной СУБД или ML-библиотекой |
| GOAL-009 | Изолированно обслуживать несколько workspaces в одной инсталляции |
| GOAL-010 | Иметь полный английский и русский интерфейс и добавлять языки каталогами, не меняя доменный код |
| GOAL-011 | Стандартизировать аналитическую работу через реестры метрик и методик, Analysis Case, evidence-linked findings и повторно используемые аналитические продукты |
| GOAL-012 | Кастомизировать инсталляцию через versioned BrandProfile и CompanyPack без fork кода или отдельного customer image |
| GOAL-013 | Дать аналитикам единое research-пространство от общего к частному с таблицами, графиками, группами метрик, выводами и воспроизводимой публикацией |

### 1.2. Границы продукта

Текущий scope сознательно исключает персонализированные маркетинговые механики (`NON-GOAL-001`), массовые email/SMS/push-рассылки (`NON-GOAL-002`), промокоды и бонусные начисления (`NON-GOAL-003`), TDA и persistent homology (`NON-GOAL-004`), полноценную real-time CDP (`NON-GOAL-005`), замену DWH (`NON-GOAL-006`), полный аналог Airflow, dbt, JupyterLab или BI (`NON-GOAL-007`), произвольный недоверенный Python из браузера (`NON-GOAL-008`) и автоматическое доказательство причинности (`NON-GOAL-009`). Также до и включая v1 исключены Dash как production UI/runtime (`NON-GOAL-010`), Plotly как core chart dependency (`NON-GOAL-011`) и ECharts-GL/WebGL/GPU analytical compute (`NON-GOAL-012`). B2B sales ontology остаётся отдельным будущим расширением (`NON-GOAL-013`); public activation runtime, reverse ETL marketplace и campaign orchestration не входят в открытый core (`NON-GOAL-014`); cloud/SaaS, Kubernetes и multi-host distribution не входят в текущую модель распространения (`NON-GOAL-015`). Post-v1 Plotly возможен только как trusted renderer plugin. Операционные уведомления и ручная персональная отправка одного воспроизводимого отчёта не являются массовой marketing-рассылкой. Promotion Journal регистрирует внешние акции, но не запускает механику, не выбирает аудиторию и не начисляет бонусы.

## 2. Пользователи и сценарии

### 2.1. Роли

| Роль | Ответственность | Граница |
|---|---|---|
| Installation Administrator | Bootstrap, глобальные политики, плагины, health, backup и installation lifecycle | Не получает workspace membership, PII или аналитические данные автоматически |
| Workspace Administrator | Пользователи, роли, object access, подключения, секреты и workspace policies | Не создаёт аналитический контент и не получает PII без отдельного разрешения |
| Data Steward | Семантическая модель, Data Quality, Data Guide и data contracts | Не управляет пользователями или connections без отдельной административной роли |
| Analyst | Исследования, методики, метрики, сегменты, dashboards, reports, comments, отправка и export | Не меняет connections/secrets и не назначает доступ другим пользователям |
| ML Analyst | Возможности Analyst плюс backtesting, модели и прогнозы | Не управляет пользователями или connections |
| Operator | Runs, расписания, очереди и восстановление | Не редактирует definitions, access policy и raw PII |
| Viewer | Просмотр выданных reports/dashboards и комментарии | Не видит raw PII и не меняет definitions или filters, зафиксированные автором |

### 2.2. Основные сценарии

| ID | Сценарий и результат |
|---|---|
| UC-001 | Workspace Administrator создаёт read-only connection или загружает файл и получает проверенный каталог объектов |
| UC-002 | Data Steward публикует semantic dataset и capability matrix |
| UC-003 | Data Steward получает QualityReport и решение gate |
| UC-004 | Analyst запускает клиентскую аналитику и получает таблицы, метрики, сегменты и графики |
| UC-005 | ML Analyst сравнивает модели и публикует прогноз с интервалами |
| UC-006 | Analyst публикует повторяемый DAG и расписание |
| UC-007 | Разрешённый артефакт выгружается в CSV/Parquet или читается через внутренний authenticated result API |
| UC-008 | Installation Administrator по одноразовому bootstrap token создаёт первого администратора, workspace, locale/timezone и onboarding checklist |
| UC-009 | Data Steward исправляет failed QualityReport, повторяет проверку либо оформляет временный auditable waiver |
| UC-010 | Operator диагностирует run и выполняет retry, cancel, rerun либо фиксирует восстановление |
| UC-011 | Analyst делится versioned dashboard или published report snapshot внутри workspace; immutable reference и audit сохраняются |
| UC-012 | Analyst сравнивает reportable результат с явно выровненным аналогичным периодом прошлого года и получает delta/coverage diagnostics |
| UC-013 | Analyst ведёт versioned Promotion Journal с окнами, каналами и immutable audience binding и видит timeline overlay |
| UC-014 | Analyst вручную отправляет immutable report snapshot от verified user email получателям разрешённых доменов |
| UC-015 | Analyst экспортирует любой reportable snapshot в единый XLSX с данными, графиками, metadata и Data Guide |
| UC-016 | Workspace Administrator публикует versioned Markdown Data Guide по утверждённому шаблону |
| UC-017 | Analyst получает Web ECharts chart, email PNG или native/raster XLSX chart из одного immutable ChartSpec и chart-data artifact |
| UC-018 | Analyst раскрывает разрешённый chart, table или range timeline в Focus / Explore mode, исследует его локальными filters и controls, экспортирует и возвращается в исходный контекст |
| UC-019 | Analyst создаёт, рецензирует и публикует versioned аналитическую методику с владельцем, формулами, assumptions, применимостью и evidence |
| UC-020 | Analyst ведёт Analysis Case от общего обзора к детализации, сохраняет блоки evidence и превращает подтверждённые findings в dashboard/report |
| UC-021 | Viewer оставляет комментарий к разрешённому report/dashboard без доступа к raw PII или изменения immutable snapshot |
| UC-022 | Workspace Administrator назначает и отзывает доступ к reports/dashboards, не получая право редактировать их содержание |
| UC-023 | Installation Administrator публикует BrandProfile/CompanyPack, а Workspace Administrator по отдельному разрешению назначает допустимую published version; Web, email, XLSX и локальная документация получают одну pinned identity |
| UC-024 | Workspace Administrator импортирует данные через опубликованный CSV/XLSX template, а платформа отклоняет неизвестные sheets/columns, формулы и macros |
| UC-025 | Analyst задаёт population, grain, metric/feature, окно, peer scope и quantile/IQR/MAD policy, получает immutable bounds и sensitivity preview, после чего явно применяет flag/exclude/winsorize без изменения canonical data/metric |
| UC-026 | Analyst строит rule/RFM/bucket/KMeans segment либо stratified distribution с требуемым числом групп и получает versioned definition, diagnostics, profiles и immutable membership/distribution artifact |
| UC-027 | Analyst исследует promo/loyalty/bonus/other components, stacking, discount cap и price-volume-mix по ReceiptItem с pinned policy, reconciliation, `vs LY` и Result Trust |
| UC-028 | Workspace Administrator ведёт versioned company/division/department/team tree, primary assignments, leadership scopes, department data policies и bounded cross-department grants с effective-access preview |
| UC-029 | Department Leader или отдельно уполномоченный пользователь открывает People & Creators и видит privacy-safe activity и только разрешённые отчёты/dashboards без raw audit и ranking |

### 2.3. Сквозные пользовательские пути

| ID | Путь | Когда он завершён |
|---|---|---|
| JOURNEY-001 | Первый bootstrap: одноразовый token, первый admin, язык, format locale, timezone, первый workspace и optional demo dataset | Пользователь видит Overview и следующее действие; checklist можно продолжить позже |
| JOURNEY-002 | Dataset onboarding: connection, catalog/profile, mapping, keys/namespaces, relationships, metrics, returns/currency/identity, sample validation, publication и full quality gate | Dataset получает `trusted`, `degraded` или `blocked` и evidence capabilities |
| JOURNEY-003 | Quality remediation: нарушение, redacted sample, переход к mapping/rule, owner/comment, fix или time-bounded waiver, повтор и сравнение | Gate разрешил run, разрешил degraded mode либо оставил объяснимую блокировку |
| JOURNEY-004 | Guided analysis: template, dataset, preflight, parameters/estimate, общий execution engine, Result Trust, сохранение/share/schedule/export | Сохранены AnalysisVersion и immutable manifest |
| JOURNEY-005 | Forecast lifecycle: series preview, candidates/backtest, baseline comparison, champion approval, monitoring, retrain/promote/rollback | Champion, причины выбора, ограничения и policy доступны для аудита |
| JOURNEY-006 | Operator recovery: queues/schedules/attempts/workers, cancel/retry/rerun, cleanup и acknowledgement | Run терминален, действие и причина находятся в audit |
| JOURNEY-007 | Governed research: вопрос, Analysis Case, pinned method/metrics/data, исследование от общего к частному, reviewed findings и публикация аналитического продукта | Опубликованный результат воспроизводим, выводы отделены от комментариев и связаны с evidence |

Для всех путей действуют общие UX-требования:

- `UX-JOURNEY-001`: wizard сохраняет draft после завершённого шага и позволяет продолжить позже;
- `UX-JOURNEY-002`: empty, loading, degraded, forbidden и failed state объясняют причину и следующее действие;
- `UX-JOURNEY-003`: guided forms создают те же versioned node/pipeline specifications и используют тот же engine, что canvas;
- `UX-JOURNEY-004`: до тяжёлого запуска видны capability preflight, оценка объёма и resource limits;
- `UX-JOURNEY-007`: Research Workspace имеет outline/sections и не превращается в бесконечный dashboard canvas;
- `UX-JOURNEY-008`: утверждённые FindingVersion визуально и семантически отделены от discussion comments;
- `UX-JOURNEY-009`: Viewer комментирует только уже разрешённый объект и не получает через thread скрытые values, facets или PII;
- `UX-JOURNEY-010`: управление access policy находится в административной поверхности и не смешивается с authoring/publish actions аналитика;
- `UX-JOURNEY-005`: Result Trust Panel показывает дату результата, freshness, quality, ограничения, версии, grain, filters, timezone, currency и lineage;
- `UX-JOURNEY-006`: из контекста доступны ответы «Почему функция недоступна?», «Почему это число?» и «На что повлияет публикация?».

### 2.4. Жизненный цикл объектов и readiness

Версионируемые определения проходят `draft → validating → published → deprecated → archived`. Published-версия неизменяема; clone создаёт новый draft; update draft защищён revision/ETag; publish формирует diff и impact report; pinned зависимости сами не переключаются на `latest`.

Readiness данных — отдельное измерение: `sample_validated`, `materializing`, `trusted`, `degraded`, `blocked`, `stale`. `draft` и `published` относятся к lifecycle конфигурации, а не к readiness; публикация конфигурации ещё не означает доверенные данные.

| ID | Обязательное поведение |
|---|---|
| OBJ-STATE-001 | API отклоняет невозможный переход stable code и возвращает допустимые действия пользователя |
| OBJ-STATE-002 | Публикация создаёт diff, dependency impact report и audit event |
| OBJ-STATE-003 | Definition с зависимостями не удаляется; применяется deprecation и управляемая миграция |
| OBJ-STATE-004 | UI не смешивает lifecycle definition, readiness данных и execution state в один `status` |
| OBJ-STATE-005 | Concurrent draft edits защищены optimistic locking через revision или ETag |

Connection отдельно имеет configuration states `draft/active/disabled/archived` и operational states `untested/testing/ready/degraded/unreachable`. Schedule имеет lifecycle и health, export — свой immutable request и execution state, model version — lifecycle и monitoring status, notification — delivery/read/acknowledgement state.

## 3. Базовые архитектурные принципы

| ID | Принцип простыми словами |
|---|---|
| ARCH-PRINCIPLE-001 | Сначала модульный монолит с контрактами между доменами |
| ARCH-PRINCIPLE-002 | Control plane отделён от тяжёлых worker-вычислений |
| ARCH-PRINCIPLE-003 | Метаданные живут в PostgreSQL, крупные данные — в Parquet |
| ARCH-PRINCIPLE-004 | Published definitions неизменяемы |
| ARCH-PRINCIPLE-005 | Каждый результат воспроизводим по manifest |
| ARCH-PRINCIPLE-006 | Фильтры, projection и безопасная агрегация по возможности выполняются в источнике |
| ARCH-PRINCIPLE-007 | У каждого набора объявлены grain и key |
| ARCH-PRINCIPLE-008 | Валюта, timezone, returns, activity и metric semantics задаются явно |
| ARCH-PRINCIPLE-009 | Plugin — доверенный server-side код |
| ARCH-PRINCIPLE-010 | Side effects идемпотентны |
| ARCH-PRINCIPLE-011 | Каждый workspace-scoped объект, request, task и artifact несёт `workspace_id`; cross-workspace access закрыт |
| ARCH-PRINCIPLE-012 | Guided UI и canvas используют один execution engine |
| ARCH-PRINCIPLE-013 | IDs, enum, manifests, cache keys и вычисления не зависят от языка UI |
| ARCH-PRINCIPLE-014 | Намерение dispatch задачи записывается в PostgreSQL в одной транзакции с control-plane state |

```mermaid
flowchart TB
    User["Пользователь"] --> Web["Web UI"]
    Web --> API["Control API"]
    API --> Meta["PostgreSQL"]
    Meta --> Dispatcher["Outbox Dispatcher"]
    Dispatcher --> Queue["Valkey"]
    Queue --> DataWorker["Data Worker"]
    Queue --> MLWorker["ML Worker"]
    DataWorker --> Sources["БД и файлы"]
    DataWorker --> Artifacts["Local artifacts"]
    MLWorker --> Artifacts
    Scheduler["Scheduler"] --> Meta
    Reconciler["Run Reconciler"] --> Meta
```

## 4. Как данные проходят через платформу

| Слой | Что хранит | Поведение |
|---|---|---|
| Source | SQL tables, CSV, Parquet, XLSX | Изменяется внешней системой |
| Landing | Извлечённые partitioned Parquet | Append/replace по manifest |
| Semantic | Mapping, relationships, metrics и business rules | Версионируется в metadata/JSON |
| Mart | Предметные витрины | Immutable per run |
| Result | Метрики, сегменты, forecasts и models | Immutable per run |
| Presentation | Chart/dashboard specs и exports | Версионируется |

### 4.1. Паспорт артефакта

Manifest фиксирует широкую категорию (`landing`, `mart`, `analysis`, `segment`, `quality`, `forecast`, `model`, `presentation`, `export`) отдельно от точного `artifact_schema_id` и его semver. Он также содержит `workspace_id`, run/node/attempt, UTC-время, только локальный относительный URI, формат, размеры, partitions, grain/key, event range, `content_hash`, `schema_fingerprint`, input artifact IDs, nullable `semantic_dataset_version_id`, pipeline/code/lockfile/parameters versions, PII class и retention.

Для partitioned artifact отдельный partition manifest содержит собственный `workspace_id` и перечисляет ожидаемые ключи, URI, row/byte counts, hashes и временные границы каждой части, а также общий hash и время commit.

| ID | Инвариант публикации |
|---|---|
| ARTIFACT-001 | Artifact и partition manifest становятся видимыми одним atomic metadata commit после проверки всех partitions |
| ARTIFACT-002 | Missing, extra или hash-mismatched partition блокирует весь commit |
| ARTIFACT-003 | Committed path нельзя перезаписать; idempotent retry возвращает старый artifact только при совпадении content/parameters hashes |
| ARTIFACT-004 | Каждый tabular artifact объявляет grain, ожидание primary key и schema fingerprint |

## 5. Каноническая модель данных

### 5.1. Общие правила

Перед аналитикой данные разных компаний приводятся к общей логической модели.

| ID | Правило |
|---|---|
| DATA-RULE-001 | Идентификаторы становятся строковым логическим типом без потери исходного значения |
| DATA-RULE-002 | Все timestamps имеют timezone, внутри платформы используется UTC |
| DATA-RULE-003 | Деньги имеют валюту строки либо объявленную валюту dataset |
| DATA-RULE-004 | Returns/cancellations представлены status или signed measure по явной политике |
| DATA-RULE-005 | У сущности объявлены grain, primary key и ожидание uniqueness |
| DATA-RULE-006 | Произвольные attributes допустимы, но часто используемые поля получают semantic role |
| DATA-RULE-007 | Unknown не превращается автоматически в `0` или `false` |
| DATA-RULE-008 | Внешний ID квалифицируется стабильным `source_system_id`; display name подключения не является namespace |
| DATA-RULE-009 | SCD-строка имеет version key либо составной ключ с `valid_from`; business ID не является PK версии |
| DATA-RULE-010 | Temporal join выбирает ровно одну версию dimension на event time и блокирует пересечение validity intervals |
| DATA-RULE-011 | FK к source entity включает `source_system_id`, если нет опубликованного crosswalk в canonical ID |

### 5.2. Клиент — ENTITY-CUSTOMER

Одна строка соответствует одной версии клиента. Primary key — `customer_version_id`; natural key — `[source_system_id, customer_id]`; уникальность версии — `[source_system_id, customer_id, valid_from]`. Обязательны `customer_version_id`, `source_system_id`, `customer_id`, `valid_from`. Дополнительно поддерживаются даты создания и действия, birth date, gender, region/city, registration channel, loyalty level, status и attributes. Email, phone и внешний person ID являются прямыми PII, birth date и city — квази-идентификаторами.

Customer может быть SCD или current snapshot. Для snapshot без source validity платформа создаёт synthetic interval от extraction batch boundary до `null` и фиксирует это ограничение в lineage.

### 5.3. Идентификация клиентов — ENTITY-CUSTOMER-IDENTITY

Identity mapping связывает source identity с canonical customer. Ключ строки включает `identity_mapping_version_id`, `source_system_id`, `source_customer_id` и `valid_from`; обязательны также `canonical_customer_id`. Public MVP поддерживает детерминированный mapping, вероятностное разрешение личности не входит в v1 target.

Версия mapping имеет отдельные `identity_mapping_version_id` и stable `identity_mapping_id`, `workspace_id`, монотонную version, lifecycle `draft/published/deprecated/archived`, effective time, source namespaces, conflict policy, merge/split events и lineage.

| ID | Инвариант identity mapping |
|---|---|
| IDENTITY-001 | Published mapping immutable и записывается во входной manifest каждой клиентской витрины |
| IDENTITY-002 | Merge/split создаёт новую mapping version и impact report, не переписывая историю |
| IDENTITY-003 | Один source identity нельзя одновременно связать с несколькими canonical IDs в одном effective interval |
| IDENTITY-004 | До публикации UI показывает unmatched, conflicted и remapped counts |
| IDENTITY-005 | В одной mapping version интервалы одного source identity не пересекаются и дают не более одного effective canonical customer в момент времени |

### 5.4. Чек — ENTITY-RECEIPT

Одна строка — один чек; ключ `[source_system_id, receipt_id]`. Обязательны source namespace, ID и `occurred_at`. Опциональны customer/store/channel, gross/discount/net/tax/cost, quantity, currency, status и `source_updated_at`. Ключ уникален в dataset version, будущая дата ограничена tolerance, а reconciliation net revenue задаётся пользователем.

### 5.5. Позиция — ENTITY-RECEIPT-ITEM

Одна строка — позиция чека; ключ `[source_system_id, receipt_id, line_id]`. Product обязателен для product/basket analytics. Помимо quantity/gross/net/cost строка может прямо содержать базовую unit/line price, promo/loyalty/bonus/other amounts, promo flag и promotion reference. Если line ID отсутствует, wizard предлагает стабильный составной ключ; номер строки нельзя использовать при нестабильном порядке incremental source.

`ENTITY-RECEIPT-ITEM-DISCOUNT-COMPONENT` нормализует wide source в одну строку на line и component. Component имеет тип promotion/loyalty/bonus redemption/other, amount, attribution mode `direct|rule_derived|residual_proxy|total_only|unavailable`, policy/evidence и optional PromotionVersion. Списание бонусов отличается от бонусного начисления: accrual не является скидкой или способом оплаты и не попадает в этот fact.

### 5.6. Товар — ENTITY-PRODUCT

Product — версионируемая сущность с `product_version_id`, natural key `[source_system_id, product_id]` и version key `[source_system_id, product_id, valid_from]`. Дополнительно хранятся name, category/subcategory, brand, manufacturer, unit, validity и attributes.

### 5.7. Магазин — ENTITY-STORE

Store строится аналогично: `store_version_id`, `[source_system_id, store_id]`, `valid_from`, optional name/type/format/region/city/opened/closed/timezone/validity/attributes. Для current Product и Store применяется synthetic validity; intervals одной natural key не пересекаются.

### 5.8. Канал — ENTITY-CHANNEL

Channel имеет ключ `[source_system_id, channel_id]`, optional name, attributes и нормализованную группу `online`, `offline`, `marketplace` или `other`. Он может быть справочником либо полем Receipt, но значения нормализуются стабильно.

### 5.9. Календарь — ENTITY-CALENDAR

Calendar генерируется платформой с grain `one_row_per_date`. В нём есть year, quarter, month, ISO week, weekday, days in period, weekend/holiday flags, holiday name и optional fiscal period.

### 5.10. Дополнительные измерения

| Сущность | Назначение | V1 target |
|---|---|---|
| CurrencyRate | Версионированное FX-приведение по effective date | Обязательно только при cross-currency aggregation |
| Promotion | Аналитика скидок и промопериодов | Опционально |
| Region | Географическая иерархия | Опционально |
| CustomerSegmentSnapshot | Историческое membership | Обязательно |
| ExternalRegressor | Погода, промодни, магазины, цены | Желательно для forecast |

Promotion Journal хранит stable `promotion_id`, immutable versions, external campaign ID, title/type/objective, planned и actual windows в IANA timezone, несколько channels, optional store/product/region scope, budget/tags/source и аудиторию `all_customers|segment_snapshot|customer_list_artifact`. Клиент всегда означает `canonical_customer_id`; исторические segment/list audiences не пересчитываются задним числом.

| ID | Инвариант Promotion Journal |
|---|---|
| PROMO-001 | Published version immutable; period/channel/audience/mechanic change создаёт новую version с diff/audit |
| PROMO-002 | Несколько planned/actual windows валидируют timezone и start/end |
| PROMO-003 | Одна акция может иметь несколько locale-neutral Channel bindings |
| PROMO-004 | Audience — all customers либо immutable segment/customer-list snapshot на canonical customer |
| PROMO-005 | Timeline фильтруется по period/status/channel/promotion/segment/customer без утечки PII/закрытых rows |
| PROMO-006 | Overlap сохраняется и диагностируется, но не разрешается скрытым приоритетом |
| PROMO-007 | Promo можно показывать overlay/regressor, но нельзя объявлять causal effect |
| PROMO-008 | Import идемпотентен и публикует rejected-row report |
| PROMO-009 | Journal имеет owner/permissions/audit/retention; published history архивируется, не hard-delete |

### 5.11. Reconciliation

Платформа сравнивает net revenue и quantity шапки с суммой позиций, проверяет orphan items и неизвестные товары. Для денег задаётся absolute/relative tolerance, а unknown products могут быть warning либо error.

## 6. Семантический набор данных

### 6.1. Версия semantic dataset

`SemanticDatasetVersion` имеет явные `semantic_dataset_version_id`, stable `dataset_id`, `workspace_id`, version и author/time. Он неизменяемо описывает source bindings, entities, joins, field mappings, filters, metrics, business rules, timezone, default currency, return и anonymous-customer policies и schema fingerprint. Lifecycle: `draft`, `validating`, `published`, `deprecated`, `archived`; concurrent edits защищены `revision`.

### 6.2. Relationships и cardinality

Каждая связь объявляет стороны, join fields, `1:1`/`1:N`/`N:1`, поведение missing key, допустимый unmatched ratio и temporal policy. Sample проверяется до публикации, full cardinality — при первой materialization; duplicate amplification измеряется явно.

### 6.3. Единый Metric Registry

Метрика хранит отдельные `metric_version_id` и stable `metric_id`, `workspace_id`, version, lifecycle `draft/validating/published/deprecated/archived`, независимый certification `candidate|verified|canonical|deprecated`, `revision`, author/time, английский и русский labels, вид метрики, исходную сущность и grain, expression, допустимые aggregations, time aggregation, filters, dimensions, unit, currency и null policies. Published candidate не становится verified автоматически; certification фиксирует owner/reviewers, reference datasets, reconciliation, robustness и replacement evidence.

Системная `net_revenue` на grain одного чека допускает slicing по date/store/channel, но запрещает product/category/brand. Товарная выручка регистрируется отдельной `item_net_revenue` на `ReceiptItem` с grain одной строки чека и сверяется с header-level total; planner не вправе молча подменять одну метрику другой.

| Вид | Пример | Как агрегируется |
|---|---|---|
| `additive_measure` | revenue, units | Сумма только по разрешённым dimensions/time |
| `semi_additive_measure` | balance, active-base snapshot | Не суммируется по времени без явной last/first/average policy |
| `event_count` | receipt count | Считает строки на заявленном уникальном grain |
| `distinct_count` | customer count | Пересчитывается на целевом grain, готовые counts не суммируются |
| `derived_ratio` | average receipt, margin rate | Пересчитывается из numerator/denominator |

| ID | Правило метрики |
|---|---|
| METRIC-001 | Объявляются kind, source grain, aggregations, time policy, unit и dimensions |
| METRIC-002 | Ratio ссылается на versioned numerator/denominator и пересчитывается на target grain |
| METRIC-003 | Недопустимая сумма distinct/semi-additive metric блокируется с объяснением |
| METRIC-004 | Изменение expression, filters, returns, unit или aggregation создаёт новую immutable version |
| METRIC-005 | Multi-currency money не агрегируется без group-by-currency или versioned FX policy |
| METRIC-006 | FX lineage содержит rate source/version, effective-date join, target currency и missing-rate policy |
| METRIC-007 | System metric имеет English и Russian labels; IDs и expressions не переводятся |
| METRIC-008 | Receipt-grain metric запрещает product/category/brand dimensions; item slicing использует отдельную ReceiptItem-grain metric с reconciliation к header total |

Базовый registry содержит gross/net revenue, receipt/customer/active-customer counts, units, average receipt, revenue per customer, margin, base-price GMV, commercial discount, customer benefit, promo/loyalty/bonus components и repeat-customer rate.

#### Числовое представление и стабильные группы метрик

Typed raw value остаётся источником истины, а форматирование задаётся versioned `NumberFormatSpec`. Денежные значения, counts, ratios, percentages, durations и averages получают единый locale-aware формат во всех каналах. По умолчанию `75,44%` отображается как `75%`, `4,27%` — как `4,3%`, а `0,234%` — как `0,23%`; ненулевое значение нельзя превращать в ложный `0%`. K/M/B или тыс./млн/млрд применяются только как presentation layer, а tooltip/detail и typed XLSX sheet сохраняют полную точность.

`MetricGroupVersion` задаёт стабильные идентификаторы групп, порядок групп и порядок метрик внутри каждой группы. Поэтому Finance всегда может показывать, например, Margin перед Revenue, а Client — AOV перед customer measures, независимо от Web, email или XLSX.

| ID | Правило представления |
|---|---|
| METRIC-009 | NumberFormatSpec versioned, locale-aware и одинаков для Web/email/XLSX |
| METRIC-010 | Adaptive percentage precision не скрывает ненулевое значение как `0%` |
| METRIC-011 | Compact suffix не изменяет raw typed value и раскрывает full value |
| METRIC-012 | Money, counts, ratios, durations и averages имеют типовые semantic defaults с разрешённым metric override |
| METRIC-013 | XLSX data sheets сохраняют numeric cells и полную точность; formatting не материализуется как text |
| METRIC-014 | MetricGroupVersion фиксирует group order и metric order внутри группы |
| METRIC-015 | Один group/order contract используется в Web, email, reports и XLSX |
| METRIC-016 | Presentation override может менять label/order/visibility, но не expression, grain, unit или permissions метрики |
| METRIC-017 | Lifecycle и certification независимы; publication не означает verified/canonical |
| METRIC-018 | Certification transition фиксирует reviewers/evidence/replacement/impact без переписывания historical metrics |
| METRIC-019 | Direct, policy-derived и residual-proxy values имеют разные origin/quality/coverage labels |
| METRIC-020 | Proxy раскрывает derivation, exclusions, residual, sensitivity и пределы применимости |

#### Versioned политика скидок

`DiscountPolicyVersion` выбирается semantic dataset/CompanyPack на effective interval и фиксирует component catalog, source bindings, stacking matrix, precedence, accounting treatment, base-price role, cap, tolerance/rounding, returns, historical/simulated breach actions и residual policy. Используются три разные истины: `commercial_discount_amount = promo + loyalty + other`, `customer_benefit_amount = commercial discount + bonus redemption` и source/policy-governed `recognized_net_revenue`. Неоднозначный label «total discount» запрещён.

Для первого внедрения допускается installation-local CompanyPack с `promo+loyalty=false`, `promo+bonus=true`, `loyalty+bonus=true`, bonus-only, precedence promo→loyalty и cap 50% от base-price для promo/loyalty/bonus. Это configuration example, не встроенный default и не fork продукта.

| ID | Инвариант скидочной модели |
|---|---|
| DISCOUNT-001 | Component analytics работает на ReceiptItem grain и объявленной base price; header allocation только versioned |
| DISCOUNT-002 | Promo/loyalty/bonus redemption/other хранятся раздельно, unknown не становится zero |
| DISCOUNT-003 | Bonus accrual отделён от redemption и не считается скидкой |
| DISCOUNT-004 | Каждый component имеет direct/rule-derived/residual/total-only/unavailable attribution и evidence |
| DISCOUNT-005 | DiscountPolicyVersion immutable, effective intervals не пересекаются и pin-ятся в result identity/lineage |
| DISCOUNT-006 | Stacking matrix и precedence запрещают hidden priority и double attribution |
| DISCOUNT-007 | Cap объявляет rate/base/components/tolerance/rounding/returns/actions; core не hardcode-ит 50% |
| DISCOUNT-008 | Commercial discount, customer benefit и recognized net revenue не смешиваются одним total |
| DISCOUNT-009 | Aggregate rate — ratio of sums, не среднее row rates |
| DISCOUNT-010 | Share/penetration/depth/overlap имеют explicit denominator и не суммируют пересечения |
| DISCOUNT-011 | Historical breach сохраняет source и excess diagnostics без automatic clamp |
| DISCOUNT-012 | Unexplained history может degrade/block trust; simulated breach блокирует publication |
| DISCOUNT-013 | Returns/cancels/negative quantity/zero base/currency имеют отдельные eligibility/sign rules |
| DISCOUNT-014 | Sale promo может ссылаться на PromotionVersion, но timeline overlap сам не атрибутирует promo |
| DISCOUNT-015 | Current и vs LY по умолчанию используют одну semantics/policy; drift явно предупреждается |
| DISCOUNT-016 | Reconciliation показывает source total, known components, residual, net и coverage/tolerance |
| DISCOUNT-017 | Result Trust/email/XLSX раскрывают policy, attribution, coverage, cap, formulas, PVM и limitations |
| DISCOUNT-018 | Price base/components/margin/cap идут в стабильном MetricGroupVersion order |
| DISCOUNT-019 | Capability различает full/partial/total-only/unavailable component analytics |
| DISCOUNT-020 | Company defaults приходят через versioned pack/policy без customer-specific core |

#### Реестр аналитических методик

`AnalysisMethodVersion` хранит цель, область применимости, availability `native_v1|template_v1|future_extension|unsupported`, family/evidence ceiling, входные сущности и метрики, шаги, assumptions, exclusions, thresholds, representativeness, robustness/sensitivity, validation и interpretation guidance. `AnalysisCase` фиксирует бизнес-вопрос, scope, участников, pinned data/method/metric/filter versions и связанное evidence. `FindingVersion` — рецензируемый вывод с evidence и limitations; discussion comment остаётся отдельной сущностью. `AnalyticalProduct` связывает опубликованные dashboard/report/research artifacts с использованной методикой.

| ID | Контракт методологии |
|---|---|
| METHOD-001 | Method имеет stable ID и immutable version lifecycle |
| METHOD-002 | Публикация требует owner, purpose, applicability, steps, inputs, assumptions, limitations и validation evidence |
| METHOD-003 | AnalysisCase pin-ит method/data/metric/filter versions, а не использует latest неявно |
| METHOD-004 | Method change создаёт новую version и impact для зависимых продуктов |
| METHOD-005 | FindingVersion отделён от comment и содержит evidence, author, review status и limitations |
| METHOD-006 | AnalyticalProduct раскрывает method/metric/data lineage и Result Trust |
| METHOD-007 | Deprecation не удаляет историческую воспроизводимость и предлагает replacement |
| METHOD-008 | MethodologyRegistry стандартизирует работу, но не делает causal claim без отдельного доказательства |
| METHOD-009 | Method/capability явно объявляет native/template/future/unsupported и не выдаёт future за runnable |
| METHOD-010 | Default v1 pack покрывает descriptive/YoY/cohorts/RFM/basket/discount-PVM/outlier/bucket-strata-KMeans/research |
| METHOD-011 | Published method имеет соразмерный robustness/sensitivity plan |
| METHOD-012 | Target/observed population, coverage, missingness, selection и запрещённые generalizations раскрыты |
| METHOD-013 | V1 даёт governed distributions, допустимые confidence intervals/differences/correlation с sample/multiple-test limitations |
| METHOD-014 | DiD/event study/matching/synthetic control, causal ML/HTE, uplift, propensity/churn, advanced migration, multivariate anomaly и automated decisions остаются future_extension |

Default MethodologyPack содержит native v1 recipes и template v1 reviews для representativeness, proxy quality и findings. Future contracts можно каталогизировать для архитектурной совместимости, но нельзя запускать или показывать как готовый функционал.

### 6.4. Capability Engine

Capability возвращает `available`, `degraded` или `unavailable` не только по наличию полей, но и по evidence текущей materialization. Evaluation фиксирует `workspace_id`, `principal_id`, `effective_policy_version`, semantic dataset/run, time, schema, mapping, quality, freshness, permissions, history coverage, currency, volume и resource-policy evidence, blocker/limitation codes и suggested actions.

| ID | Требование capability |
|---|---|
| CAPABILITY-001 | Решение учитывает schema, mapping, quality, freshness, текущие permissions зафиксированных `principal_id` и `effective_policy_version`, history, currency, volume и workspace limits |
| CAPABILITY-002 | Причина имеет stable code, evidence, threshold и suggested action |
| CAPABILITY-003 | Evaluation обновляется после mapping, materialization, QualityReport, permission или policy change |
| CAPABILITY-004 | Preflight фиксируется во входном manifest запуска |

Продажи доступны по дате и денежной метрике даже без клиента; RFM требует Customer/Receipt и monetary measure; basket — receipt items и product; store/channel analytics требуют соответствующие keys; revenue forecast может деградировать до univariate baseline; customer forecast блокируется при плохой идентификации.

### 6.5. Поисковый реестр фильтров

Любой reportable result использует единый `FilterFieldRegistry`. В нём поле связано с published semantic dataset/entity, имеет stable/versioned ID, type, allowed operators, versioned null policy, hierarchy binding, relative-date policy с anchor/timezone/calendar, labels/description, cardinality, PII class, facet policy, pushdown capability и список применимых анализов. Выражения поддерживают `AND/OR/NOT`, typed hierarchy operators и relative-date windows. «Любое поле» означает любое опубликованное `filterable` поле, доступное effective policy пользователя, а не произвольную source column.

| ID | Инвариант фильтрации |
|---|---|
| FILTER-001 | Filters передаются versioned typed expression tree; arbitrary SQL/string из basic UI запрещён |
| FILTER-002 | Search находит только разрешённые fields по ID/entity/label/description/type |
| FILTER-003 | Backend проверяет operator/value по type, versioned null policy, hierarchy binding и relative-date policy независимо от UI |
| FILTER-004 | Expression, registry/hierarchy/calendar versions, relative-date anchor и timezone входят в analysis/report spec, manifest, request hash и cache key |
| FILTER-005 | Facets/counts/search применяют authorization до aggregation/pagination |
| FILTER-006 | Planner делает safe pushdown либо typed Polars/DuckDB execution с volume preflight |
| FILTER-007 | High-cardinality fields используют search-only/bounded lookup, не полный browser distinct list |
| FILTER-008 | UI показывает applied/default/locked filters, resulting grain и estimated rows; hidden business rule только versioned metric rule |
| FILTER-009 | Focus / Explore позволяет draft local filters без изменения parent report до Apply to report; Reset возвращает inherited state, Undo отменяет последнее draft-действие |
| FILTER-010 | Apply to report повторно валидирует filters и authorization на backend и обновляет normalized spec/request identity; system/locked filters видимы и не могут быть удалены либо ослаблены |

## 7. Подключение и загрузка данных

### 7.1. Источники v1 target

Пользовательские source modes v1 строго ограничены PostgreSQL, Microsoft SQL Server, MySQL/MariaDB, ClickHouse и governed CSV/XLSX templates. Parquet остаётся внутренним artifact/export format, а не пользовательским source connector. Yandex Metrica заранее получает отдельные future boundaries для агрегированного Reporting API и raw Logs API, но не присутствует в v1 runtime. Snowflake, BigQuery, Oracle, arbitrary spreadsheet ingestion и CDC также не входят в v1.

`FileImportTemplateVersion` фиксирует допустимые sheets/columns, types, required fields, header aliases, row/file limits, locale/date/decimal rules и безопасную preview policy. Формулы, macros, external links, неизвестные sheets/columns и неутверждённые schema guesses отклоняются до materialization.

| ID | Connector boundary |
|---|---|
| CONNECTOR-001 | v1 поддерживает ровно четыре SQL connectors и два governed file-template modes |
| CONNECTOR-002 | Каждый SQL connector имеет read-only posture, supported-version matrix и реальную release integration evidence |
| CONNECTOR-003 | CSV/XLSX import разрешён только через published FileImportTemplateVersion |
| CONNECTOR-004 | Template import не исполняет formulas/macros и отклоняет unknown structure без silent inference |
| CONNECTOR-005 | Yandex Metrica Reporting и Logs проектируются как разные future capabilities и не обещаются в v1 |
| CONNECTOR-006 | Parquet является внутренним artifact/export contract, а не source picker option v1 |

### 7.2. Connector contract

```python
class SourceConnector(Protocol):
    def capabilities(self) -> ConnectorCapabilities: ...
    def test(self, request: ConnectionTest) -> ConnectionTestResult: ...
    def discover(self, request: DiscoveryRequest) -> CatalogSnapshot: ...
    def preview(self, request: PreviewRequest) -> DataBatch: ...
    def estimate(self, request: ExtractRequest) -> ExtractEstimate: ...
    def begin_extraction_session(self, request: ExtractionSessionRequest) -> ExtractionSession: ...
    def extract(self, request: ExtractRequest, session: ExtractionSession) -> Iterator[ArrowBatch]: ...
    def close_extraction_session(self, session: ExtractionSession, outcome: ExtractionOutcome) -> None: ...
```

Constructor только принимает зависимости и проверяет инварианты. Multi-table чтение выполняется через одну явно открытую `ExtractionSession`: она хранит `session_id`, `workspace_id`, immutable `source_system_id`, consistency mode, непрозрачный secret snapshot token, состояния `created/active/committed/aborted/expired` и временные границы. Connector завершает её commit либо abort; expired session не публикует artifact или watermark, а token не попадает в artifacts, logs или UI. Connection/import binding получает immutable `source_system_id`; rename не меняет namespace, а повторная загрузка файла явно переиспользует binding либо создаёт новый.

### 7.3. Режимы загрузки

Поддерживаются full snapshot, append, incremental watermark с lookback, partition refresh и upsert. CDC до v1 target не входит. Incremental policy хранит field, successful watermark, lookback, dedup key с source namespace, latest-version rule, delete policy и UTC.

### 7.4. Консистентный extraction batch

Batch фиксирует `workspace_id`, connection/source namespace, consistency mode, opaque snapshot token, start time, objects, lower и candidate upper watermarks, landing artifacts, validation report и state от `created` до `committed/failed/cancelled`.

| ID | Инвариант ingestion |
|---|---|
| INGEST-001 | Связанные таблицы желательно читать из одного DB snapshot/checkpoint; mode записывается в manifest |
| INGEST-002 | Без общего snapshot используется `best_effort_validated` с временными границами и reconciliation до публикации |
| INGEST-003 | Candidate watermark продвигается одной PostgreSQL transaction после commit всех partitions и обязательных validations |
| INGEST-004 | Failed/partial/cancelled batch не двигает successful watermark, temp files очищаются retention |
| INGEST-005 | Retry использует прежние bounds либо новый batch; смешивание границ запрещено |
| INGEST-006 | Snapshot token и secrets не попадают в UI, logs и artifacts |
| INGEST-007 | Multi-table extraction использует одну `ExtractionSession` и завершает её commit/abort; expired session не публикует artifact или watermark |

### 7.5. Schema drift и extraction security

Новое неиспользуемое поле даёт warning; удалённое mapped field, несовместимый тип или изменённый PK блокируют; compatible widening предупреждает. Source account read-only; preview ограничен по rows/time/bytes; custom SQL — один read-only statement и по возможности AST validation; DB permissions остаются последней защитой; DSN/password шифруются; PII preview маскируется по роли.

## 8. Хранение и артефакты

PostgreSQL хранит users, RBAC, metadata, versions, run states, schedules, manifests и audit. Local Parquet storage хранит landing, marts, segments, forecasts и exports. Valkey служит broker/cache/locks, но не источником истины. Source DB остаётся внешним источником.

### 8.1. Только локальный Artifact Store до v1 target

```python
class LocalArtifactStore(Protocol):
    def begin(self, request: ArtifactWriteRequest) -> ArtifactWriter: ...
    def commit(self, writer: ArtifactWriter) -> ArtifactManifest: ...
    def abort(self, writer: ArtifactWriter) -> None: ...
    def open(self, artifact_id: UUID) -> ArtifactReader: ...
    def delete_expired(self, policy: RetentionPolicy) -> DeletionReport: ...
```

Запись идёт во временный path и публикуется атомарно. Для vertical alpha, public MVP и v1 target поддерживается только local filesystem на одном сервере с shared persistent volume, deployment-configured root и platform-generated relative paths без user fragments.

Текущая спецификация не обещает remote/object storage adapter. S3-compatible storage может появиться только по отдельному будущему ADR, который определит atomicity, consistency, credentials, migration и distributed topology.

Retention различает published outputs, temporary node data, preview, exports, models и audit. Нельзя удалить единственный вход опубликованного результата до окончания воспроизводимого срока.

## 9. Low-code pipeline engine

Pipeline — DAG из типизированных узлов. Поддерживаются source, semantic, transform, quality, mart, customer/sales analytics, segmentation, forecasting, visualization и output nodes. У node есть stable type/version, English/Russian label, category, JSON Schema конфигурации, typed ports, queue/resource profile, determinism/cache/cancel flags и PII access. Backend повторяет всю validation, даже если форму сгенерировал frontend.

### 9.1. Базовые transformations и engines

Select, filter, derive, join, aggregate, deduplicate, date spine, window, pivot и union проверяют schema, keys, null policy, cardinality, amplification, resulting grain, leakage cutoff и size limits. Source DB используется для pushdown, DuckDB — для SQL по Parquet и больших joins/group by, Polars — для lazy domain transforms. Каждый node публикует выбранный backend и explain summary.

```python
class PipelineNode(Protocol):
    def specification(self) -> NodeSpecification: ...
    def validate(self, request: NodeValidationRequest) -> ValidationReport: ...
    def execute(self, context: NodeExecutionContext, inputs: NodeInputs) -> NodeResult: ...
```

PipelineVersion имеет явные `pipeline_version_id`, stable `pipeline_id`, `workspace_id`, version, общий lifecycle/revision и pinned `semantic_dataset_version_id`, а также nodes/edges, parameter schema, validation report и author/time. Publish проверяет acyclic graph, обязательные ports, типы artifacts, capabilities, наличие secrets без их значений, resource policy, output conflicts и установленные node versions.

### 9.2. Execution states и надёжная доставка

Run проходит `CREATED`, `VALIDATING`, `QUEUED`, `RUNNING`, при отмене `CANCELLING`, затем `SUCCEEDED`, `FAILED`, `CANCELLED` или `PARTIAL`. Node дополнительно использует `PENDING`, `READY`, `RETRY_WAIT`, `SKIPPED` и `CACHED`.

| ID | Инвариант execution state |
|---|---|
| EXEC-STATE-001 | Run/node transition выполняется compare-and-set по state/revision; недопустимый переход возвращает stable error code |
| EXEC-STATE-002 | Terminal state неизменяем: automatic retry до terminal создаёт новый `attempt_id` через `RETRY_WAIT→READY`, а manual retry завершённого run/node создаёт новую execution record с новым run/node ID, initial state и `retry_of_id` |
| EXEC-STATE-003 | Aggregate state run вычисляется по зафиксированным node states и declared partial policy одной PostgreSQL transaction |
| EXEC-STATE-004 | `PARTIAL` требует успешную publishable branch и явную policy; failure обязательной branch не маскируется как `SUCCEEDED` |
| EXEC-STATE-005 | `CACHED` разрешён после проверки workspace/policy-scoped key, manifest, content hash и authorization |
| EXEC-STATE-006 | `CANCELLING` сохраняется до остановки либо fencing active attempts; `CANCELLED` не сообщается раньше cleanup policy |
| EXEC-STATE-007 | Каждый transition пишет time, actor/service, reason, request ID и previous/new state в audit/state history |

API создаёт run в PostgreSQL. Orchestrator валидирует preflight и одной transaction создаёт ready node и `task_outbox`. Dispatcher доставляет at-least-once команду в Valkey/Celery. Worker берёт lease с монотонным fencing token, выполняет изолированный attempt и может публиковать только с актуальным token. Orchestrator одной transaction открывает следующие nodes. Reconciler восстанавливает потерянную delivery, expired lease, incomplete commit и незавершённый aggregate state.

| ID | Инвариант dispatch |
|---|---|
| EXEC-DISPATCH-001 | State transition и outbox record фиксируются одной PostgreSQL transaction |
| EXEC-DISPATCH-002 | Worker ожидает duplicate delivery и дедуплицирует по node run, attempt и fencing token |
| EXEC-DISPATCH-003 | Fencing token монотонен; stale worker не публикует artifact/state |
| EXEC-DISPATCH-004 | Reconciler находит pending outbox, queued без delivery, expired running lease, terminal node без commit и incomplete run |
| EXEC-DISPATCH-005 | Reconciliation идемпотентен, bounded и отражён в audit/metrics |

Cache key состоит из `workspace_id`, `effective_policy_version`, node type/version, normalized config, ordered input hashes, semantic version и code version. Cache запрещён для non-deterministic node без seed, preview, source без snapshot guarantee и mutable side effect без idempotency policy. Network/timeout/worker-lost errors могут повторяться с bounded backoff; validation и OOM автоматически не повторяются.

Schedule хранит `workspace_id`, pinned pipeline version, `revision`, cron, IANA timezone, parameters, lifecycle `draft/enabled/paused/disabled/archived`, отдельный derived health `healthy/misfired/failing/blocked`, misfire/concurrency policies, nullable `next_run_at` и `last_evaluated_at` в PostgreSQL.

| ID | Инвариант schedule |
|---|---|
| SCHEDULE-001 | Lifecycle и derived health хранятся и показываются отдельно; boolean enabled не является persistent source of truth |
| SCHEDULE-002 | Только enabled schedule создаёт новые runs; уже созданные runs у paused/disabled/archived следуют своей cancellation policy |
| SCHEDULE-003 | Claim due schedule, следующий occurrence, run и `task_outbox` создаются атомарно с защитой от duplicate claim |
| SCHEDULE-004 | Cron, timezone, parameters и policies меняются через revision/ETag и audit event |
| SCHEDULE-005 | Health выводится из claim/run evidence и thresholds, а не выставляется пользователем |

Scheduled run и outbox создаются одной transaction; scheduler не пишет напрямую в queue. DST поведение тестируется.

### 9.3. Plugins

Plugin может добавить connector, node, metric pack, forecast model, export adapter и UI metadata. Он обнаруживается Python entry point, объявляет compatible `core_api_version`, а до v1 target требует restart. Английский catalog обязателен; bundled/official plugin также обязан иметь полный русский. Сторонний plugin без русского использует English fallback с предупреждением; namespace имеет вид `plugin.<plugin_id>`.

### 9.4. Cancellation и resource isolation

Cooperative cancellation проверяется до source query, между batches, перед partition commit и между model folds. После grace period выполняется hard stop child process, попытка driver-level DB cancel, abort writer и cleanup temp/lease. Terminal state может быть `CANCELLED`, `FAILED` либо `PARTIAL`; `PARTIAL` допустим только при declared partial policy и уже committed publishable branch.

| ID | Требование cancellation |
|---|---|
| EXEC-CANCEL-001 | Тяжёлый node работает в child process или эквивалентной изоляции |
| EXEC-CANCEL-002 | Runtime применяет timeout, memory, temp disk, output size и source-query limits |
| EXEC-CANCEL-003 | Активный DB statement отменяется штатно, затем process завершается после grace period |
| EXEC-CANCEL-004 | Cancelled attempt не публикует manifests; committed outputs становятся orphan candidates по retention |
| EXEC-CANCEL-005 | Cancel API идемпотентен; terminal run не возвращается в `CANCELLING` |
| EXEC-CANCEL-006 | Resource breach возвращает stable code, observed/configured limits и safe remediation |

## 10. Контроль качества данных

Data Quality — gate между источником и доверенной аналитикой. Проверяются schema, keys, references, domains, numeric ranges, time coverage, header/line reconciliation, freshness и drift.

Rule имеет отдельные `rule_version_id` и stable `rule_id`, `workspace_id`, version, lifecycle `draft/validating/published/deprecated/archived`, `revision`, author/time, entity, full/sample/partition scope, safe expression, severity, threshold, action `record/block_publish/block_run`, null policy и owner. QualityReport сохраняет `workspace_id`, канонический `semantic_dataset_version_id`, run, passed/warning/failed, gate decision `allow/allow_degraded/block`, rows, results каждого rule, redacted sample artifact и profile. Пользовательские rules компилируются из безопасного expression tree в source SQL, Polars или DuckDB; SQL-конкатенация запрещена.

### 10.1. Remediation и временные waivers

Quality issue хранит `workspace_id`, report/rule, status, owner, link к mapping/rule, audit-referenced comments и first/last seen. Waiver использует канонический `semantic_dataset_version_id` и ограничен workspace, rule version, optional partition scope, reason/ticket, requester, expiry и optional maximum failed ratio. Для `pending` approval/rejection fields равны `null`; `active` требует `approved_by` и `approved_at`; `rejected` — `rejected_by`, `rejected_at` и `rejection_reason`. Решение immutable и auditable; статусы waiver: `pending`, `active`, `rejected`, `expired`, `revoked`.

| ID | Требование remediation |
|---|---|
| DQ-REMEDIATE-001 | Failed rule связан с mapping/rule и показывает redacted sample, history, owner и affected capabilities |
| DQ-REMEDIATE-002 | Разрешён rerun отдельного rule/gate через тот же execution engine |
| DQ-REMEDIATE-003 | Waiver ограничен rule/dataset/scope/threshold/expiry и требует отдельного permission |
| DQ-REMEDIATE-004 | Expired/revoked waiver не влияет на новые gates, но остаётся в audit |
| DQ-REMEDIATE-005 | Workspace isolation, missing PK, bad artifact hash и executable security policy нельзя waived |
| DQ-REMEDIATE-006 | Gate перечисляет waiver IDs и оставшиеся limitations; скрыто подавлять ошибку нельзя |
| DQ-REMEDIATE-007 | Failure samples маскируют PII и требуют отдельного permission |
| DQ-REMEDIATE-008 | Pending имеет null approval/rejection; active требует approval, rejected — reject actor/time/reason; решения immutable и auditable |

Degraded gate status передаётся downstream и остаётся видимым в результате и Result Trust Panel.

## 11. Аналитические витрины

Каждая mart объявляет stable type/version, grain, key, period, metric versions, lineage, null/return policies, timezone, currency и quality.

### 11.1. Канонические facts

`receipt_header_fact` имеет grain одного source receipt и владеет header measures. `receipt_item_fact` имеет grain source receipt line и владеет line measures. `customer_receipt_fact` объединяет canonical customer, source receipt и конкретную identity mapping version.

| ID | Защита от double counting |
|---|---|
| MART-GRAIN-001 | Receipt-level measures агрегируются из header fact и не повторяются на lines |
| MART-GRAIN-002 | Item analytics использует item fact; header measures доступны после receipt aggregation или checked allocation |
| MART-GRAIN-003 | Header-to-items join объявляет `1:N` и amplification report |
| MART-GRAIN-004 | Customers считаются по canonical ID, receipts — по source system плюс receipt ID |
| MART-GRAIN-005 | Planner выбирает fact по source grain metric и блокирует ambiguous mixed-grain query |
| MART-GRAIN-006 | Customer-level marts и segment snapshots после identity resolution используют `canonical_customer_id` в grain, primary key и outputs; неоднозначный `customer_id` запрещён |
| MART-GRAIN-007 | Period mart объявляет period, `fact_scope` и полный ordered tuple materialized dimension keys как primary key и отклоняет collision |
| MART-GRAIN-008 | Discount component fact связывается полным line key и агрегируется до join, не размножая base/net measures |

### 11.2. Стандартные marts

| ID | Grain, назначение и ключевые поля |
|---|---|
| MART-CUSTOMER-TRANSACTION | Одна строка на canonical customer и source receipt; customer/source/receipt, UTC/local date, store/channel, amounts, quantity, eligibility; зависит от semantic/identity/return versions |
| MART-CUSTOMER-PERIOD-ACTIVITY | Customer × day/week/month; receipt/purchase-day counts, revenue, units, margin, active/first flags и last purchase as of period |
| MART-CUSTOMER-FEATURES | Customer × as-of date; окна 30/90/180/365 дней, RFM-like features, tenure, interpurchase, channel shares и preferences; только события до cutoff |
| MART-RECEIPT-FEATURES | Один source receipt; counts товаров/категорий, units, net revenue, discount share и margin из header/item facts и Product |
| MART-SALES-PERIOD | Period × dimensions с явным `receipt_header` или `receipt_item` fact scope; mixed header/item metrics строятся без размножения |
| MART-SEGMENT-MEMBERSHIP | Segment version × snapshot date × customer с score и assignment reason |

Canonical primary keys: customer transaction — `[canonical_customer_id, source_system_id, receipt_id]`; customer-period — `[canonical_customer_id, period_start, frequency]`; customer features — `[canonical_customer_id, as_of_date]`; receipt features — `[source_system_id, receipt_id]`; segment snapshot — `[segment_version_id, snapshot_date, canonical_customer_id]`. Sales-period mart использует `[period_start, fact_scope, materialized_dimension_key_tuple]`, где tuple содержит все реально materialized dimension keys в объявленном порядке. Одна materialization имеет один `fact_scope`; product/category требуют item fact, а header metrics сначала агрегируются на receipt grain.

`first_purchase_flag` и новые клиенты помечают left censoring при недостаточной предыстории. Historical dimensions и segment membership выбираются на дату события, а не по сегодняшнему значению.

## 12. Аналитические модули

Каждый анализ получает typed artifacts, immutable specification и Metric Registry version; публикует result table, metric set, chart specs, diagnostics и manifest. Он детерминирован при seed, не имеет hidden filters и всегда фиксирует as-of/comparison periods.

Любой reportable analytics/forecast/dashboard/QualityReport принимает `TimeComparisonSpec` либо explicit `none`. Поддерживаются same dates, calendar-aligned, ISO-week-aligned, fiscal-period и comparable-elapsed-days сравнения с прошлым годом. Результат материализуется как immutable `ComparisonArtifact`: он хранит normalized/resolved spec, фактические границы обоих периодов, timezone, calendar/policy hash, metric/activity/segment/dataset/filter versions, coverage и limitation codes. Именно его ID pin-ится в `ReportSnapshot`. Operator/Admin telemetry не входит в reportable scope.

| ID | Инвариант сравнения периодов |
|---|---|
| COMPARE-001 | Каждый reportable result принимает versioned spec либо explicit none; hidden shift запрещён |
| COMPARE-002 | Calendar mapping явно обрабатывает leap day, ISO week 53, fiscal periods, timezone и calendar version |
| COMPARE-003 | Неполный текущий период сравнивается только по explicit policy |
| COMPARE-004 | Output содержит current/comparison, absolute/percent delta, coverage и comparability; missing не равен zero без domain rule |
| COMPARE-005 | Immutable artifact фиксирует resolved spec/periods, timezone, calendar/policy hash и metric/activity/segment/dataset/filter versions; несовместимость блокируется либо требует auditable rebase |
| COMPARE-006 | Capability отдельно проверяет history, quality, permissions и definition compatibility обоих периодов |
| COMPARE-007 | UI/email/XLSX показывают одинаковые mode/limitations из одного comparison artifact |

| ID | Назначение, вход и ключевой результат |
|---|---|
| ANALYTICS-SALES-OVERVIEW | MART-SALES-PERIOD → KPI, trend, contribution и comparison; revenue раскладывается как customers × receipts per customer × average receipt |
| ANALYTICS-CUSTOMER-BASE | MART-CUSTOMER-PERIOD-ACTIVITY → active/new/retained/reactivated/at-risk/churned, value, frequency и tenure по versioned activity definition |
| ANALYTICS-RFM | MART-CUSTOMER-TRANSACTION → R/F/M scores и snapshots; explicit as-of, deterministic ties, fixed thresholds для сравнения |
| ANALYTICS-COHORT | Customer transactions → cohort matrix, sizes, cumulative value и retention с различением logo/revenue/repeat и right censoring |
| ANALYTICS-LIFECYCLE | Customer period activity → customer state, transitions, counts/revenue и flows; state machine валидирует priorities и impossible transitions |
| ANALYTICS-BASKET | ReceiptItem + optional Receipt/Product/segments → basket KPIs, pairs, optional rules и affinity; сначала sparse pair aggregation |
| ANALYTICS-STORE-CHANNEL | Sales mart → scorecards, channel membership/migration и optional same-store growth с единым canonical customer и workday normalization |
| ANALYTICS-SEGMENT-RULES | Customer feature snapshot + optional treatment version → membership/profile/overlap; serializable Polars expression tree и explicit overlap policy |
| ANALYTICS-SEGMENT-CLUSTER | V1 CPU KMeans с explicit K, versioned preprocessing/treatment/seed, fit/assignment policy, profiles, centers, stability, silhouette и immutable membership snapshot |
| ANALYTICS-ABC-XYZ | Post-v1 классификация customer/product/store по value/variability с concentration/Pareto outputs |
| ANALYTICS-MARGIN-DISCOUNT | V1 component discount/margin analytics: base price, commercial discount, customer benefit, components, overlap, depth, cap, attribution coverage и PVM; correlation не объявляется causal effect |
| ANALYTICS-SEGMENT-MIGRATION | Stored snapshots → transitions, inflow/outflow и stability без пересчёта истории новыми правилами |
| ANALYTICS-CUSTOM-BUILDER | Typed mart + allowed filters/dimensions/metrics/date/comparison/top/sort → reproducible ad hoc table, metrics и chart |

Custom Builder разрешает только MetricRegistry/draft-validated metrics и published semantic joins, блокирует non-additive aggregation и показывает resulting grain/estimated rows до запуска.

Discount module фильтруется по period/`vs LY`, channel/store/product/category/brand,
customer/segment, component, stacking combination, attribution mode, policy,
discount band и cap state. V1 `PriceVolumeMixSpecVersion` использует объявленный
method/order; default `portfolio_laspeyres_price_last_v1` разлагает delta на
aggregate volume, mix, price, assortment и residual. New/discontinued items,
missing price, UOM, returns и currency обрабатываются explicit policy. Иной
symmetric/Shapley method является новой version, а не скрытой заменой.

| ID | Инвариант PVM |
|---|---|
| PVM-001 | Version pin-ит method/order, periods, grain, product identity и quantity/price/revenue metrics |
| PVM-002 | Price+volume+mix+assortment+residual сходятся с observed delta в tolerance |
| PVM-003 | New/discontinued/missing/zero/UOM cases используют explicit policy без hidden imputation |
| PVM-004 | Returns/currency/tax/base-price definitions одинаково pin-ятся во всех effects |
| PVM-005 | Filters, `vs LY` и drill-down сохраняют parent reconciliation без double counting |
| PVM-006 | Result Trust/export раскрывают formula order, coverage, assortment, residual и non-causal limitation |

### 12.1. Governed population и обработка выбросов

Выбросы не являются обычным display filter и не исправляют source data. Analyst сначала выбирает population, entity grain, metric/feature, observation window и peer scope, затем создаёт immutable `PopulationTreatmentSpecVersion`. V1 поддерживает quantile, IQR и MAD; стандартный z-score не является default для скошенных retail-распределений. Новая policy по умолчанию только помечает наблюдения. `Exclude` и `Winsorize` требуют явного выбора и preview влияния на количество клиентов/заказов, долю выручки, метрики, распределение и resolved bounds.

| ID | Инвариант обработки выбросов |
|---|---|
| OUTLIER-001 | Immutable treatment не изменяет source artifacts, canonical entities или MetricDefinitionVersion |
| OUTLIER-002 | Grain, feature/metric, window/as-of, reference population и peer scope всегда зафиксированы |
| OUTLIER-003 | V1 методы — quantile, IQR и MAD; mean/std z-score не является default |
| OUTLIER-004 | Tail, ties, minimum population, bounds и approximate-quantile evidence входят в specification/result |
| OUTLIER-005 | Действия — flag/exclude/winsorize; default — flag, остальные требуют impact preview |
| OUTLIER-006 | DQ-invalid rows обрабатываются отдельно; статистический outlier не доказывает ошибку и не удаляет VIP молча |
| OUTLIER-007 | Preview показывает before/after count, customer/order/value share, metric delta, distribution и bounds |
| OUTLIER-008 | `vs LY` по умолчанию применяет одни pinned bounds; independent-period bounds только explicit exploratory |
| OUTLIER-009 | Result Trust, SegmentSnapshot, ReportSnapshot, email и XLSX README раскрывают treatment version, scope, bounds, impact и limitations |
| OUTLIER-010 | Member preview/drill/export повторно применяет object/row/PII policy и не раскрывает denied facets |
| OUTLIER-011 | Расчёт CPU vectorized/pushdown через Polars/DuckDB/NumPy; browser и row-wise Python не считаются default compute path |
| OUTLIER-012 | Fit и assignment populations различаются: extremes можно убрать из fit, затем назначить с outlier flag, distance/confidence и sensitivity evidence |

Forecast residual anomalies остаются отдельной time-series policy и не используют эти cross-sectional bounds автоматически.

### 12.2. Buckets, strata и KMeans

`SegmentationDefinitionVersion` объединяет rule, RFM, bucket и KMeans definitions. Любой published membership snapshot pin-ит population, inputs, treatment, preprocessing/model/code и as-of. Bucket mode поддерживает quantile, equal-width и custom thresholds. Stratified distribution сначала является исследовательским `DistributionArtifact`; выбранную ячейку Analyst может явно сохранить как segment. KMeans является первым кластерным методом v1 и принимает точное K. Платформа может показать K-1/K/K+1 diagnostics, но не меняет K без решения Analyst. HDBSCAN, Gaussian Mixture, automatic K и multivariate anomaly detection остаются post-v1.

| ID | Инвариант сегментации |
|---|---|
| SEGMENT-001 | Published definition pin-ит method, population, features, treatment, as-of, group count и seed |
| SEGMENT-002 | Membership snapshot immutable и содержит definition/input/treatment/preprocessing/model/code/member-grain bindings |
| SEGMENT-003 | Bucket methods v1: quantile, equal-width и custom thresholds |
| SEGMENT-004 | Quantile/equal-width требуют group count; custom thresholds задают количество групп и валидируют gaps/overlaps |
| SEGMENT-005 | Ordered labels, missing bucket, inclusivity и tie policy обязательны |
| SEGMENT-006 | Dynamic bounds допустимы для exploration; published recurring segment pin-ит resolved bounds либо fixed thresholds |
| SEGMENT-007 | Stratified distribution по умолчанию является AnalysisVersion artifact, не постоянным segment |
| SEGMENT-008 | Global boundaries — default для сравнимости; within-stratum quantiles явно означают relative rank |
| SEGMENT-009 | Strata имеют dimension/cardinality limits, minimum-cell privacy и `Other`/blocked policy |
| SEGMENT-010 | Selected bucket/stratum cell сохраняется как segment только явным действием с lineage |
| SEGMENT-011 | V1 clustering начинается с CPU KMeans и exact K; diagnostic candidates не меняют K молча |
| SEGMENT-012 | Preprocessing version-ит feature order, missing/log1p/scaling и запрещает IDs, raw PII и leakage |
| SEGMENT-013 | Result содержит membership, profiles, centers, sizes, distance/confidence, preprocessing, stability и silhouette/limitation |
| SEGMENT-014 | Business label versioned отдельно; numeric cluster ID не является стабильным смыслом |
| SEGMENT-015 | Retrain создаёт новый snapshot; cross-version mapping требует profile matching и analyst approval |
| SEGMENT-016 | Frozen-model assignment и full retrain — разные operations и result identities |
| SEGMENT-017 | GMM/HDBSCAN/automatic K/Isolation Forest/multivariate anomaly detection остаются post-v1 |
| SEGMENT-018 | Preview сравнивает profiles/sizes/stability/business sensitivity с/без treatment и блокирует invalid publication |

### 12.3. Research Workspace — от общего к частному

Research Workspace — governed block document поверх тех же artifacts, metrics, ChartSpec и report contracts, а не notebook kernel и не второй dashboard engine. Analyst начинает с вопроса и общего обзора, добавляет sections, metric groups, charts и tables, углубляется фильтрами/drill-down, фиксирует evidence-linked findings и собирает из подтверждённых блоков аналитический продукт. Narrative, methodology, limitations и conclusions являются first-class blocks.

| ID | Research invariant |
|---|---|
| RESEARCH-001 | ResearchDocumentVersion immutable после публикации; изменение создаёт новую version |
| RESEARCH-002 | Документ pin-ит AnalysisCase, data, method, metric, filter, comparison и evidence versions |
| RESEARCH-003 | Blocks используют общий reportable artifact/ChartSpec/table contract и не копируют вычислительную логику |
| RESEARCH-004 | Outline и sections поддерживают явный путь overview → diagnostic → detail → conclusion |
| RESEARCH-005 | FindingVersion требует evidence и review status; comment не становится finding автоматически |
| RESEARCH-006 | Viewer comments наследуют object/row/PII policy и проходят DLP/audit |
| RESEARCH-007 | Research blocks публикуются в dashboard/report без потери lineage и Result Trust |
| RESEARCH-008 | Export использует pinned snapshot; browser DOM scraping и hidden notebook state запрещены |

## 13. Прогнозирование

Forecasting строит series из зарегистрированной метрики, заполняет календарь, создаёт time-safe features, делает rolling backtest, сравнивает baselines и CatBoost, рассчитывает intervals, ведёт registry, batch prediction и monitoring. Он не является business planning или causal engine.

### 13.1. Forecast specification и series

Specification имеет отдельные `forecast_spec_version_id` и stable `forecast_id`, `workspace_id`, version, lifecycle `draft/validating/published/deprecated/archived`, `revision`, pinned `semantic_dataset_version_id` и author/time. Она фиксирует target, frequency/horizon/history, complete-period policy, dimensions/hierarchy, known-future и observed regressors, missing-period policy, candidates, rolling windows/step/horizon, selection metric/bias constraints, interval levels и seed.

Можно прогнозировать net revenue, receipts, average receipt как ratio, active/new/reactivated/churned customers, units и hierarchical store/category sales. TimeSeriesBuilder выдаёт одну строку на series/period с target, regressors и completeness. Missing period не означает zero без domain rule; current incomplete period не входит автоматически; first-purchase series отмечает left censoring.

FeatureBuilder создаёт lags 1/2/3/6/12, rolling means/std, calendar/trend и configured regressors. У любого feature есть `availability_time`; будущее относительно forecast origin запрещено.

```python
class ForecastModel(Protocol):
    def identity(self) -> ForecastModelIdentity: ...
    def fit(self, request: ForecastFitRequest) -> FittedForecastModel: ...
    def predict(self, model: FittedForecastModel, request: ForecastPredictRequest) -> ForecastFrame: ...
    def diagnostics(self, model: FittedForecastModel) -> ModelDiagnostics: ...
```

V1 target включает Naive, Seasonal Naive, moving average, ETS/AutoETS, AutoARIMA и CatBoostRegressor; optional Theta, Croston, seasonal-window average и linear trend.

CatBoost использует time sorting, fixed seed, time split вместо random K-fold, train-only preprocessing, later validation for early stopping и сохранённый feature order/model binary. Feature importance — diagnostic, не causal explanation.

### 13.2. Backtest, intervals и registry

Backtest result принадлежит `workspace_id` и ссылается на существующий immutable `forecast_spec_version_id` того же workspace; каждый fold хранит train/forecast boundaries и metrics by horizon. Считаются MAE, RMSE, WAPE, sMAPE и bias overall, по fold/horizon/series group. Если CatBoost не даёт минимального улучшения либо нарушает constraints, выбирается простой baseline.

Statistical intervals используют model method; CatBoost до v1 может использовать empirical residual quantiles. Coverage проверяется, interval не показывается как гарантия.

Model Registry хранит `model_version_id`, `workspace_id`, FK на тот же immutable `forecast_spec_version_id`, algorithm/library, training run/data/model artifacts, feature schema, hyperparameters, backtest metrics, status и creation time в PostgreSQL. Cross-workspace либо dangling forecast-spec FK запрещён. MLflow возможен только позднее.

Monitoring считает actual-vs-forecast, coverage, WAPE/bias, residual trend, missing regressors, model age и feature drift. Retraining manual/scheduled/quality-triggered; previous champion сохраняется, auto-promotion до v1 выключено и требует comparison/audit.

Post-v1: декомпозиция `active = retained + new + reactivated`, hierarchical reconciliation bottom-up/top-down/MinT и отдельные what-if scenarios. В v1 независимые hierarchy forecasts допустимы только с предупреждением.

## 14. Визуализация, dashboards и экспорт

### 14.1. Chart specification

Канонический visual contract — собственный versioned, renderer-neutral и theme-neutral `ChartSpec`, а не ECharts `option` и не изображение. Он фиксирует source/data artifacts, schema/grain/size, dimensions/measures, axes/series/annotations, comparison, interaction, semantic styles, accessibility и export policy. ECharts option, SVG, PNG и native Excel chart являются только derived render artifacts с compiler/renderer/theme/locale/timezone/render-profile versions и content hash.

Семь подтверждённых границ:

1. Apache ECharts — единственный v1 Web chart engine.
2. Dash отсутствует в production dependencies/runtime и application lifecycle.
3. Plotly возможен только после v1 как trusted renderer plugin, не core dependency.
4. Product-owned `ChartSpec` компилируется в ECharts; raw library option не является source of truth.
5. Promotion Journal использует отдельный `range_timeline` chart type.
6. Web рендерит SVG/Canvas, email получает PNG из deterministic SSR SVG, XLSX — lossless native chart либо PNG из того же static pipeline.
7. ECharts-GL/WebGL и GPU analytics не используются; aggregation/sampling/level-of-detail выполняются на backend CPU.

`range_timeline` хранит lane field, promotion version, start/end, planned/actual, status, immutable audience reference, overlap policy, visible-window state и detail action. Multi-channel promotions занимают соответствующие lanes; overlap отображается stack/swimlane/density summary. Overlay акции на аналитическом chart остаётся descriptive и не получает causal label. Это не ECharts `timeline` component для frame switching: Web adapter использует заранее зарегистрированный trusted range-series renderer.

Renderer boundaries:

- presentation domain владеет одним versioned TypeScript workspace package `packages/chart_compiler_ts`; его один immutable build импортируют и `SVC-WEB`, и embedded Node consumer report worker, независимые Web/SSR compiler implementations запрещены;
- `SVC-WEB` компилирует validated ChartSpec этим shared package только в allowlisted ECharts SVG/Canvas option;
- `SVC-REPORT-WORKER` содержит bounded Node ECharts SSR adapter, а не отдельный network service;
- static path: ChartSpec + immutable data + render profile → SSR SVG → PNG;
- email использует PNG, direct SVG embed запрещён;
- XLSX mapper создаёт native chart только при lossless mapping, иначе переиспользует тот же PNG pipeline и всегда сохраняет underlying typed sheet;
- identical ChartSpec/data, compiler build, renderer build и render profile, включая bundled-font hash, переиспользует content-addressed render artifact; изменение любого из этих значений создаёт новую render identity.

Render manifest фиксирует `compiler_contract_version`, `compiler_implementation_id`, `compiler_build_digest`, `renderer_id`, `renderer_version`, `renderer_build_digest`, theme, locale, timezone, size/scale и `font_bundle_id`/`font_bundle_hash`. Renderer использует только поставляемые versioned en/ru fonts, а не системные или remote fonts.

```python
class ChartCompilerPort(Protocol): ...
class ChartStaticRendererPort(Protocol): ...
class WorkbookChartRendererPort(Protocol): ...
```

ChartSpec не принимает JavaScript functions, `renderItem`, raw ECharts/Plotly option, HTML/CSS formatter, arbitrary URL/assets, executable expression или unbounded regex. Большие данные сначала детерминированно агрегируются, sampled либо materialized как level-of-detail artifact на backend CPU; browser получает bounded display data и повторно авторизованный visible-window fetch.

| ID | Chart invariant |
|---|---|
| CHART-001 | Product-owned versioned ChartSpec — единственный canonical visual contract; library options/images/workbook charts только derived |
| CHART-002 | Published spec/data immutable и content-addressed; schema/data, compiler implementation/build, renderer build, bundled fonts, theme/locale/timezone/profile входят в manifest/identity |
| CHART-003 | Spec фиксирует binding/schema/grain/size/dimensions/measures/units/reduction/comparison/access без hidden client metric logic |
| CHART-004 | Apache ECharts — единственный Web chart engine до и включая v1 |
| CHART-005 | Dash исключён из production dependencies/runtime/routing/state/callback architecture |
| CHART-006 | Plotly не core dependency; post-v1 только trusted renderer plugin через общий contract |
| CHART-007 | `range_timeline` — отдельный versioned type, не ECharts timeline-frame component |
| CHART-008 | Promotion timeline поддерживает planned/actual, channels, pinned audiences, overlap, visible window, details и descriptive overlay |
| CHART-009 | Один presentation-owned TypeScript compiler package используется Web и embedded Node; независимые implementations запрещены, identical input/build даёт identical option hash |
| CHART-010 | Raw options/functions/HTML/CSS/URLs/assets/regex запрещены; special charts только registered trusted renderer IDs |
| CHART-011 | Web использует SVG/Canvas по versioned measured policy без изменения data/hash semantics |
| CHART-012 | Static ECharts SSR bounded и встроен в report worker без отдельного network service/Chrome по умолчанию |
| CHART-013 | Email получает PNG из SSR SVG; XLSX — lossless native chart либо same-pipeline PNG с underlying data |
| CHART-014 | ChartSpec использует semantic color/style roles; theme разрешается только renderer-ом и pin-ится в manifest |
| CHART-015 | Каждый chart имеет localized summary, units/limitations и accessible table; hover/color не единственный смысл |
| CHART-016 | Browser получает bounded data; aggregation/sample/LOD выполняются backend CPU, visible-window fetch повторно авторизуется |
| CHART-017 | ECharts-GL/WebGL/GPU analytics выключены до v1; browser SVG/Canvas не выполняет analytical reduction |
| CHART-018 | Static adapter без network, с batch/dimension/output/temp/memory/CPU/time limits, cancellation и cleanup partial artifacts |
| CHART-019 | Release gate проверяет schema/security, shared-compiler option hash Web/SSR, SVG/Canvas semantics, SSR→PNG, font/render-build cache invalidation, range timeline, native/raster XLSX, themes/a11y и golden parity |

#### 14.1.1. Полноэкранный Focus / Explore mode

Любой разрешённый reportable chart, table и `range_timeline` можно раскрыть на весь viewport приложения. Это не browser F11, не отдельный результат и не повод для автоматического пересчёта: режим продолжает показывать тот же source binding, comparison, permissions, filters и Result Trust, а при закрытии возвращает пользователя к исходному блоку.

В header всегда находятся title, current period, компактный `vs LY`, все applied/system/locked filters, Result Trust, export и close. Поиск фильтра использует единый FilterFieldRegistry и видит любое разрешённое effective policy поле, но не раскрывает forbidden fields или их facets. Локальные filters сначала живут как draft: `Apply to report` применяет их к отчёту через backend validation, `Reset` возвращает inherited state, `Undo` отменяет последнее draft-действие.

Для charts доступны разрешённые `ChartSpec` управление legend, zoom, pan, brush и drill-down; для tables — columns, sorting, density, pinning и pagination. Пользователь может переключаться `Chart ↔ Data table`, не меняя source binding, filters, comparison, grain, units, freshness, permissions и Result Trust.

Состояние, меняющее сам результат, входит в normalized spec, manifest, request hash и cache key. Масштаб, выбранные series, brush, представление, columns, density, pinning и pagination остаются временным presentation state и сохраняются только через versioned Saved View. Entering focus mode не переносит business metrics/aggregation/sample/LOD в browser и не даёт новых data permissions.

| ID | Focus / Explore invariant |
|---|---|
| FOCUS-001 | Каждый разрешённый reportable chart/table/range timeline имеет Focus / Explore во всём application viewport с исходными binding/comparison/permissions/context |
| FOCUS-002 | Header показывает title, period, `vs LY`, applied/system/locked filters, Result Trust, export и close |
| FOCUS-003 | Filter search находит любое разрешённое поле registry без раскрытия forbidden fields/facets/counts |
| FOCUS-004 | Draft local filters имеют Apply to report, Reset и Undo; до Apply parent report/persisted state не меняется |
| FOCUS-005 | Apply повторяет backend validation/authorization, обновляет normalized request identity, а нужный compute выполняется backend CPU с ProgressEvent/ETA |
| FOCUS-006 | Chart controls legend/zoom/pan/brush/drill-down следуют allowlisted ChartSpec capabilities; reset возвращает declared initial view, browser analytics запрещена |
| FOCUS-007 | Table controls включают columns/sort/density/pinning/pagination с server-side authorization, bounded query и PII policy |
| FOCUS-008 | Chart ↔ Data table сохраняет source/filter/comparison/grain/units/permissions/freshness/Result Trust и явно раскрывает любое неизбежное различие |
| FOCUS-009 | Close/Escape/Back возвращают route, block, scroll и keyboard focus; выход с draft filters следует явному confirm/discard policy |
| FOCUS-010 | Все controls keyboard-operable, имеют visible focus/names, non-hover values, textual summary/table alternative и работают при 200% zoom |
| FOCUS-011 | Режим имеет loading/empty/filtered-empty/warning/degraded/blocked/failed/forbidden/stale/partial states без overlap |
| FOCUS-012 | Presentation state ephemeral и не входит в request/cache identity; persist только через versioned Saved View, result filters следуют FILTER-004/010 |

Не входят в этот scope: raw SQL, расширение прав, скрытие system/locked filters, client-side authoritative analytics, второй chart engine, browser/OS fullscreen ownership и неявная запись exploration state в published report.

Замена прежнего `chart_artifact.option` на canonical `ChartSpec` — `breaking-change` artifact/port contract. Runtime migration отсутствует, потому что репозиторий остаётся Foundation scaffold. Старый shape не реализуется и dual-write запрещён. Если внешний prototype consumer уже существует, он должен регенерировать visual из source binding либо пройти явный one-time adapter. Rollback после первого production ChartSpec требует отдельной обратной миграции persisted references.

### 14.2. Dashboard как versioned product object

Public MVP имеет templates для Overview, Sales, Customer Base, RFM, Cohorts, Lifecycle, Basket, Stores/Channels и Forecast. Свободный BI drag-and-drop не обязателен до v1.

DashboardVersion хранит отдельные `dashboard_version_id` и stable `dashboard_id`, version, lifecycle/revision, `workspace_id`, localized title/description, layout schema/layout, global filter schema, widgets, access/freshness policies и author/time. Widget имеет type, pinned либо latest-successful source binding, projection, local filters и visualization.

| ID | Dashboard invariant |
|---|---|
| DASHBOARD-001 | Published dashboard immutable, layout/widget change создаёт version |
| DASHBOARD-002 | Widget объявляет pinned result либо latest successful by spec и показывает resolved artifact |
| DASHBOARD-003 | Filters валидируются по schema и сохраняются воспроизводимо |
| DASHBOARD-004 | Dashboard не расширяет доступ к underlying artifact/PII; действует пересечение policies |
| DASHBOARD-005 | Stale/degraded/failed refresh/missing artifact явно виден без подмены данных |
| DASHBOARD-006 | Любой drag-and-drop имеет keyboard-accessible альтернативу |
| DASHBOARD-007 | Dashboard поддерживает ordered sections и heterogeneous metric-group/chart/table/finding/conclusion/methodology blocks |
| DASHBOARD-008 | Metric groups и порядок берутся из MetricGroupVersion и одинаковы во всех render channels |
| DASHBOARD-009 | Published finding визуально и семантически отличается от discussion comment |
| DASHBOARD-010 | Управление access grants требует отдельного administrative permission и не следует из права edit/publish |
| DASHBOARD-011 | Viewer может комментировать только разрешённую non-PII projection и не меняет snapshot |
| DASHBOARD-012 | Comment thread сохраняет object/block/version anchor, visibility, moderation state и audit без копирования hidden values |

### 14.3. Export

CSV использует `UTF-8` и UI row limit, Parquet — основной large-data format, JSON — только для небольших внутренних authenticated results. Public MVP и v1 не записывают в внешнюю DB. Database destination export и публичный read-only result API относятся к post-v1 и требуют отдельных security/transactionality ADR.

#### Распространение продукта и private future activation

Текущий продукт распространяется только как self-hosted single-server installation. Ручная отправка reports и выгрузка CSV/Parquet/XLSX остаются публичным core. Audience activation, reverse ETL destination marketplace, campaign orchestration, licensing/control-plane mechanics и другие будущие коммерческие варианты не описываются детально в открытом репозитории.

Локальный путь `.private/distribution-activation/` игнорируется Git только для защиты от случайного commit. Это не security boundary: нормативные private materials должны храниться в отдельном access-controlled repository/storage.

| ID | Private future boundary |
|---|---|
| PRIVATE-FUTURE-001 | v1 distribution — только documented self-host install без mandatory external control plane |
| PRIVATE-FUTURE-002 | Report email/XLSX/CSV/Parquet не зависит от private activation package, license heartbeat или managed service |
| PRIVATE-FUTURE-003 | Public contracts резервируют extension boundaries, но не публикуют destination catalogue, commercial policy или activation implementation |
| PRIVATE-FUTURE-004 | Authoritative private artifacts хранятся отдельно с access control; `.gitignore` лишь предотвращает случайный commit |
| PRIVATE-FUTURE-005 | Будущий activation runtime требует отдельной product/security/consent/audit specification и не наследует report-delivery permission |

### 14.4. Universal Report Composition

Web, email и XLSX не собирают отчёт независимо. `ReportDefinitionVersion` описывает ordered sections и versioned blocks `heading|text|metric|metric_group|table|chart|finding|conclusion|methodology|quality|forecast_status|metadata|data_guide`, а каждый binding pin-ит artifact, projection, filters, comparison, metrics, schema/grain, unit/format и lineage policies и PII class. До render создаётся immutable `ReportSnapshot`; его `resolved_blocks[]` однозначно связывает каждый `block_id` с source artifact/projection/filter/comparison, canonical ChartSpec ID/hash, schema/grain, row/column counts, units/formats, lineage и PII class. Snapshot также фиксирует BrandProfile/CompanyPack, Data Guide, theme, locale/timezone/currency и renderer contract. UI редактирует эту specification; DOM scraping и raw library options запрещены.

```python
class ReportRendererPort(Protocol):
    def preflight(self, request: ReportRenderRequest) -> ReportRenderPreflight: ...
    def render(self, request: ReportRenderRequest) -> RenderedReportArtifact: ...

class ReportDeliveryPort(Protocol):
    def submit(self, request: ReportDeliverySubmitRequest) -> ReportDeliverySubmission: ...
    def reconcile(self, request: ReportDeliveryReconcileRequest) -> ReportDeliveryReconciliation: ...
```

| ID | Report invariant |
|---|---|
| REPORT-001 | Published definition immutable; block/binding/layout/default-theme change создаёт version |
| REPORT-002 | Snapshot разрешает каждый block с artifacts/filters/metrics/comparison/ChartSpec/schema/size/units/lineage/PII и фиксирует locale/timezone/currency/theme/renderer |
| REPORT-003 | Web/email/XLSX используют один snapshot, ChartSpec и chart-data artifacts; DOM scraping/raw options/channel-specific metric logic запрещены |
| REPORT-004 | Data block объявляет schema, grain, size, units/formats, lineage и PII class |
| REPORT-005 | Permission — пересечение report/source/row/object/PII/export policies и проверяется перед render/download/send |
| REPORT-006 | Rendered artifact имеет manifest/hash/renderer/size/retention/snapshot reference |
| REPORT-007 | Reportable scope: analytics, forecasts, dashboards, QualityReport; не Operator/Admin telemetry |
| REPORT-008 | Result Trust показывает as-of/freshness/quality/filters/comparison/limitations/lineage |
| REPORT-009 | Render asynchronous с preflight/cancel/progress/resource/idempotency/stable errors |
| REPORT-010 | Retention чистит rendered artifacts, но не definition/snapshot metadata/redacted audit |
| REPORT-011 | Sections и heterogeneous blocks сохраняют author-defined research narrative и stable order |
| REPORT-012 | Metric-group, number-format и finding blocks разрешаются по pinned versions и не вычисляются отдельно в renderer |
| REPORT-013 | Snapshot фиксирует BrandProfileVersion/CompanyPackVersion и одинаковую identity во всех render channels |
| REPORT-014 | Report access policy управляется отдельно от content authoring; наличие edit/publish не даёт grant/revoke authority |

### 14.5. Пользовательский email-отчёт

Это user-initiated workflow, а не operational notification и не marketing campaign. Installation Administrator публикует global maximum recipient-domain allowlist, Workspace Administrator может только сузить его, отсутствие policy означает deny. Sender identity связана с user/workspace, verified и отдельно transport-authorized. `From` равен адресу пользователя; silent system fallback и замена требования одним `Reply-To` запрещены.

Delivery pin-ит ReportSnapshot, actor/sender, redacted recipient/domain hashes, policy versions, HTML/text/attachments, payload/idempotency hashes, state и safe provider metadata. Нормализованный список `To` хранится отдельно как durable encrypted short-retention snapshot с key version и доступен только scoped report-delivery worker; это позволяет пережить restart до submit. До submit adapter сохраняет encrypted idempotency handle, а для unknown-state reconciliation — encrypted provider locator. После retention expiry они удаляются с audit удаления, и остаются только redacted hashes/outcome. Transport без доказуемого idempotency/reconciliation contract для пользовательского email не допускается.

| ID | Report email invariant |
|---|---|
| REPORT-MAIL-001 | Только явное authenticated-user действие; bulk/scheduled marketing и audience expansion запрещены |
| REPORT-MAIL-002 | From — verified transport-authorized user email; system-sender fallback запрещён |
| REPORT-MAIL-003 | Installation allowlist — global ceiling, workspace только сужает; no policy = deny |
| REPORT-MAIL-004 | Domain нормализуется case-insensitive/IDNA с explicit subdomain и confusable validation |
| REPORT-MAIL-005 | Перед render/submit повторно проверяются send/source/domain/PII/DLP/sender/transport policies |
| REPORT-MAIL-006 | Accessible HTML/plain text и inline PNG из deterministic ECharts SSR SVG; direct SVG/remote executable content запрещены |
| REPORT-MAIL-007 | Delivery имеет persisted encrypted adapter idempotency handle; retry только bounded known-retryable failure |
| REPORT-MAIL-008 | Unknown result reconciles по persisted encrypted locator/handle и не повторяется вслепую до explicit duplicate-warning action |
| REPORT-MAIL-009 | Recipient snapshot/handles encrypted, versioned, scoped и short-retention; обычный audit хранит только redacted hashes/outcome без full address/body/PII rows |
| REPORT-MAIL-010 | Secrets, SMTP credentials, full provider response и recipient list не попадают в telemetry/diagnostics |
| REPORT-MAIL-011 | Queue/duration/outcome/policy metrics имеют alerts и versioned runbook |

### 14.6. Универсальный XLSX

XLSX реализуется последней функциональной частью v1 target поверх уже стабильного ReportSnapshot. Один `XlsxRendererPort` строит workbook `README`, `Contents`, `Summary`, typed block sheets, charts и `Metadata/Lineage`. `README` автоматически и аккуратно объясняет назначение отчёта, as-of/freshness, безопасное описание источников, все применённые и locked filters, comparison, definitions/groups/units метрик, grain, методику, quality/limitations, lineage и автора. Native chart используется только при lossless mapping canonical `ChartSpec`; иначе применяется PNG из того же bounded static renderer pipeline с сохранённым typed data sheet.

| ID | XLSX invariant |
|---|---|
| XLSX-001 | Один render path для всех reportable snapshots; module-specific generators запрещены |
| XLSX-002 | Обязательны README/Data Guide, Contents, Summary, data blocks, charts, Metadata/Lineage |
| XLSX-003 | Data sheet имеет canonical typed columns, stable table name, grain, formats и source binding |
| XLSX-004 | Native chart только lossless; иначе same-static-renderer PNG и underlying typed data |
| XLSX-005 | Overflow split на deterministic sheets, silent truncation запрещён |
| XLSX-006 | Preflight оценивает rows/columns/sheets/charts/memory/temp/final size и блокирует unsafe render |
| XLSX-007 | Formula injection нейтрализуется; business metrics — materialized values, formulas только controlled technical ranges |
| XLSX-008 | Sheet/table names safe/unique/deterministic, mapping сокращений находится в Contents |
| XLSX-009 | Release gate проверяет OOXML/openability/tables/charts/formulas и golden parity Web/email/XLSX |
| XLSX-010 | README собирается автоматически из ReportSnapshot, Data Guide и Methodology, а не пишется вручную для каждого модуля |
| XLSX-011 | README не раскрывает host/DSN/secrets/raw query, hidden policy filters или недоступную PII |
| XLSX-012 | Metric groups и порядок одинаковы с Web/email; merged headers не разрушают machine-readable typed tables |
| XLSX-013 | Display formats используют NumberFormatSpec, но cells остаются numeric с полной точностью |
| XLSX-014 | BrandProfile применяется к cover/README/summary безопасно и не меняет canonical data schema |

## 15. Web-интерфейс

Guided mode ведёт аналитика через connections, semantic model, quality, sales/customer/RFM/cohort/segment/forecast flows. Pipeline mode предназначен для повторяемых DAG, но не заменяет предметные мастера.

Разделы продукта: Overview, Connections, Data Catalog, Data Model, Metrics, Data Quality, Analytics, Promotion Journal, Segments, Forecasts, Reports, Pipelines, Runs/Operator Center, Notifications, Data Guide, Admin и Profile. В Profile независимо настраиваются language, format locale, timezone, theme, sessions и API tokens.

Любой result view показывает as-of date, freshness, quality, draft/published version, filters, metric version, degraded limitations, fact против forecast, interval отдельно от point prediction, PII только по permission, понятную ошибку и trace ID. Object lifecycle, dataset readiness и run state не смешиваются. Progress public MVP передаётся SSE через `GET /api/v1/runs/{run_id}/events`, fallback — polling.

### Application shell и плотность отчётности

| ID | Инвариант |
|---|---|
| UI-SHELL-001 | Expanded sidebar показывает стабильную outline icon и полное локализованное название; collapsed использует те же icons без текста, а буквенные сокращения и инициалы вместо navigation icons запрещены |
| UI-SHELL-002 | Icon-only navigation имеет локализованные accessible name и tooltip по hover/focus, visible focus, `aria-current` и hit area не менее 40×40 CSS px; collapse не меняет порядок, route, authorization или focus semantics |
| UI-SHELL-003 | Core Web navigation использует одну pinned OSS/web-distributable family и versioned semantic mapping; для v1 это Lucide через `lucide-react`, без смешивания families, emoji и platform-proprietary assets без license/accessibility review |
| UI-SHELL-004 | Global Search и Notifications находятся в sidebar сразу после workspace identity; Help и user menu закреплены в footer sidebar; page header не дублирует эти действия |
| UI-SHELL-005 | Sidebar поддерживает expanded/collapsed/hidden, pointer resize примерно 208–320 px, keyboard step/reset, сохранение presentation preference и доступное восстановление без изменения route, прав, порядка или current-item semantics |
| UI-SHELL-006 | Analytics navigation включает отдельные Sales, Customers, Products и Forecasts; Sales, Products и Forecasts имеют разные Lucide icons, активный route — `aria-current="page"` |
| UI-DENSITY-001 | Reportable result и каждый `UI-AN` route используют compact page-header/context и KPI, когда применимо, чтобы primary visualization, table или editor начинались в первом desktop viewport; декоративный пустой space не вытесняет рабочие данные |
| UI-DENSITY-002 | Четыре primary KPI по умолчанию находятся в одном Compact KPI Strip с общей baseline, согласованными column boundaries/dividers и коротким `vs LY`; четыре высокие самостоятельные cards не используются как default report header |
| UI-DENSITY-003 | Report surfaces используют общие versioned geometry/spacing tokens; context/KPI separators и baselines совпадают, per-page ad hoc spacing запрещён; правило обязательно для `UI-DQ-001` и `UI-AN-001…012`, включая compact header/context на screens без KPI |
| UI-DENSITY-004 | `UI-AN-003` не показывает отдельные Dataset control и Result Trust row; dataset/version, trust/freshness и last update объединены в компактный result-level trigger, доступный в Chart и Data и открывающий полный Trust drawer |

### Data Guide

`DataGuideVersion` имеет workspace либо semantic-dataset scope, template schema, default locale, Markdown/HTML artifacts, optional pinned dataset version и validation report. Template требует purpose, owner/contacts, sources, freshness/SLA, timezone/calendar/currency, entities/grain/keys, metrics, returns/cancellations, DQ limitations, PII/access, known limitations и change history.

| ID | Data Guide invariant |
|---|---|
| DATA-GUIDE-001 | Только bounded UTF-8 Markdown с обязательными template sections |
| DATA-GUIDE-002 | Raw HTML/scripts/iframes/executable content/arbitrary remote assets запрещены; renderer sanitizes allowlist subset |
| DATA-GUIDE-003 | Published guide immutable; upload/binding change создаёт version с diff/audit |
| DATA-GUIDE-004 | Scope workspace/dataset; links только на разрешённые versioned entities/metrics без secrets/PII samples |
| DATA-GUIDE-005 | Dataset version change показывает stale/review-required до compatible guide publication |
| DATA-GUIDE-006 | Guide виден в Data Catalog/Result Trust и входит ссылкой/выдержкой в email/XLSX README |
| DATA-GUIDE-007 | User-authored default locale explicit; automatic translation отсутствует |
| DATA-GUIDE-008 | Publish требует отдельного permission, PII/secret scan и audit template/version/content hash |

### Progress и ETA

Compute UX действует для всех пользовательски наблюдаемых вычислений. Любая asynchronous compute operation публикует `ProgressEvent` с run/node/stage, monotonic sequence, completed/total units, stage/overall percent, throughput, ETA/confidence, locale-neutral message и terminal state. Быстрая synchronous compute operation показывает accessible busy/loading state; percent/ETA могут отсутствовать. Если оценка ненадёжна, UI показывает indeterminate state, а не выдуманные числа.

| ID | Progress invariant |
|---|---|
| PROGRESS-001 | Любая user-observable asynchronous compute operation публикует versioned events; synchronous compute имеет accessible loading state |
| PROGRESS-002 | Unknown total даёт null percent/ETA и indeterminate UI |
| PROGRESS-003 | ETA имеет confidence, основан на throughput/history и не является SLA |
| PROGRESS-004 | Overall percent monotonic; total revision объясняется event reason |
| PROGRESS-005 | SSE reconnect использует Last-Event-ID/cursor; polling читает PostgreSQL snapshot |
| PROGRESS-006 | UI показывает stage/elapsed/progress/ETA/cancel и не прекращает run при уходе со страницы |
| PROGRESS-007 | Animation respects reduced motion, live-region announcements throttled |
| PROGRESS-008 | Events bounded; их потеря не меняет authoritative run state |

### Цветовые профили

Custometry и Roehub используют единый набор из четырёх палитр от near-black до bright-light: `abyss`, `graphite`, `frost`, `paper`. Machine blueprint фиксирует исходные palette values. UI default — `graphite`, email/XLSX default — `paper`; user может выбрать любую тему. Компоненты используют semantic tokens, а `ChartSpec` остаётся theme-neutral.

| ID | Theme invariant |
|---|---|
| THEME-001 | Registry содержит ровно четыре profiles: abyss, graphite, frost, paper; graphite UI default, paper report default |
| THEME-002 | Компоненты используют semantic canvas/surface/text/border/accent/focus/status/chart tokens |
| THEME-003 | Themes имеют status/positive-negative/color-blind chart tokens и WCAG AA validation |
| THEME-004 | Authenticated preference хранится в profile; local browser value только до входа/fallback |
| THEME-005 | Theme switch без reload и без изменения analytics/run/artifact/cache identity |
| THEME-006 | ChartSpec theme-neutral; renderer pin-ит theme в report manifest |
| THEME-007 | Email/XLSX default paper можно заменить одной из четырёх themes; theme входит в snapshot/hash |
| THEME-008 | Switcher/focus/status/charts проходят en/ru, keyboard, reduced-motion, contrast и table-alternative gates для четырёх profiles |

### White-label: BrandProfile и CompanyPack

`BrandProfileVersion` охватывает display name и short name продукта, logo variants, favicon, optional custom icon pack, bundled fonts, base theme, semantic token overrides, login/onboarding, email, report/XLSX/docs, support/legal и optional custom domain. `CompanyPackVersion` объединяет branding, semantic mappings, metric/method/group packs, role policies, dashboard/report templates, governed file-import templates, Data Guides и connection profiles без secrets.

Это конфигурация, а не customer-specific fork. Assets проходят MIME/signature/size/dimension/sanitization checks, SVG ограничен allowlist subset, remote URLs/raw CSS/HTML/JS запрещены. Опубликованный report snapshot pin-ит brand/company-pack version и content hashes.

| ID | White-label invariant |
|---|---|
| BRAND-001 | BrandProfile имеет stable ID, immutable versions и preview/publish lifecycle |
| BRAND-002 | Logo/favicon/icon/font assets content-addressed, sanitized и хранят provenance/license metadata |
| BRAND-003 | Цвета меняют только semantic tokens и проходят contrast/status/chart accessibility gates |
| BRAND-004 | Raw CSS, HTML, JavaScript и remote asset fetch запрещены |
| BRAND-005 | Web, login, email, report, XLSX и local docs используют один published brand contract |
| BRAND-006 | ReportSnapshot pin-ит BrandProfileVersion и renderer identity для воспроизводимости |
| BRAND-007 | CompanyPack не содержит secrets, PII, hostnames или customer data и валидируется до install |
| BRAND-008 | Обновление CompanyPack показывает diff/impact и не меняет published definitions задним числом |
| BRAND-009 | Powered-by, support/legal и custom-domain policy versioned и не обходят license/security notices |

### 15.1. Интернационализация и локализация

English — default и fallback; русский обязателен полностью. Внешние locale tags соответствуют `BCP-47`. Frontend использует `i18next` и `react-i18next`, backend-generated presentation — gettext/Babel. Domain core остаётся locale-neutral, автоматический перевод пользовательского контента выключен.

| Настройка | Пример | Что определяет |
|---|---|---|
| `language` | `en`, `ru` | Текст UI |
| `format_locale` | `en-US`, `en-GB`, `ru-RU` | Даты, числа, проценты, plural forms |
| `timezone` | `Europe/Tallinn` | Отображение времени и schedules |
| `currency` | `EUR`, `RUB` | Dataset/metric policy, не выводится из языка |

Язык выбирается так: user preference → workspace default → сохранённая anonymous preference до входа → `en`. `Accept-Language` может подсказать язык первого экрана, но не меняет fallback. User values приоритетнее workspace defaults; dataset timezone/currency/calendar остаются semantic settings.

Catalogs лежат по namespaces `common`, `connections`, `quality`, `analytics`, `forecasts`, `admin` внутри `packages/localization/locales/{locale}`. Ключи семантические, например `runs.status.failed`; строки с параметрами/plurals хранятся целиком, translated fragments не конкатенируются. Formatting выполняют `Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat` и Babel.

System metrics/nodes/rules/templates/official plugins имеют English и Russian. User content имеет обязательный source `default_locale` и optional translations. API fields, IDs, enum, permission/error/event codes, Parquet columns, manifest fields, source names и cache keys не переводятся.

| ID | Требование i18n |
|---|---|
| I18N-001 | English — default/fallback, русский полностью покрывает shipped UI и backend-generated text |
| I18N-002 | Frontend использует i18next/react-i18next и JSON namespaces; locale-specific branches в product code запрещены |
| I18N-003 | Backend-generated email/HTML/PDF использует gettext catalogs и Babel formatting |
| I18N-004 | API/logs/audit/manifests/events хранят stable codes/params, перевод выполняется на presentation boundary |
| I18N-005 | Смена языка не требует relogin и не меняет analytics, business calendar, run/artifact hashes или cache key |
| I18N-006 | Language, format locale, timezone и currency хранятся независимо |
| I18N-007 | CSV по умолчанию имеет canonical headers, optional localized headers требуют явных locale/metadata; Parquet/JSON canonical |
| I18N-008 | Новый язык добавляется registry entry, namespaces/gettext/built-in translations и parity/pseudo/E2E checks без domain changes |
| I18N-009 | CI проверяет placeholders, plural branches и 100% en/ru coverage; missing release key — ошибка |
| I18N-010 | Layout использует CSS logical properties и direction из registry, заранее поддерживая RTL |
| I18N-011 | Plugin keys изолированы `plugin.<plugin_id>`; English обязателен всем, Russian — bundled/official plugins |

### 15.2. Accessibility

Web UI соответствует WCAG 2.2 Level AA, включая onboarding, forms, grids, charts, canvas, dialogs и Operator Center.

| ID | Требование WCAG |
|---|---|
| A11Y-001 | Все функции доступны keyboard с visible focus и logical order |
| A11Y-002 | Canvas/dashboard drag-and-drop имеет add/connect/move/reorder/delete команды без dragging |
| A11Y-003 | Цвет не единственный status signal; text/icon/pattern и AA contrast обязательны |
| A11Y-004 | Forms имеют связанные labels/instructions/errors; после submit focus переходит к error summary |
| A11Y-005 | Async progress/completion/notifications объявляются уместным live region без шума |
| A11Y-006 | Chart имеет localized summary, units/limitations и accessible table; hover/tooltip/color не единственный смысл |
| A11Y-007 | Grid поддерживает header associations, keyboard navigation, sort/filter announcements и virtualization accessibility |
| A11Y-008 | UI работает при 200% zoom/reflow и учитывает reduced motion |
| A11Y-009 | Localized aria labels/names проходят en/ru parity |
| A11Y-010 | CI запускает automated checks, release journey — ручной keyboard/screen-reader smoke |

### 15.3. Операционные уведомления

Они информируют об эксплуатации платформы и не являются массовой рассылкой из `NON-GOAL-002`. Event хранит nullable workspace для installation-scoped события, stable event code/severity, resource, actor, time, dedup key, locale-neutral params и trace.

Delivery хранит nullable `workspace_id`, target `user|workspace`, nullable recipient, канал `in_app|email|webhook`, pinned endpoint version и redacted snapshot hash, payload schema/hash, states `pending/delivering/delivered/failed/read/acknowledged/dismissed`, attempt count, next retry, stable error code и delivery/read/acknowledgement times. Public MVP активирует только `in_app`; `v1_target` активирует `in_app`, `email` и `webhook`.

Email/webhook endpoint — immutable version с workspace/owner scope, encrypted destination, status `active/disabled/revoked` и optional signing-secret reference. Каждая delivery attempt фиксирует endpoint version/snapshot, attempt number, `started/succeeded/retryable_failure/permanent_failure`, times, safe response class/provider hash, error code и retryability. In-app endpoint не нужен; email рендерится Babel/gettext в языке получателя, webhook получает versioned locale-neutral envelope с event ID, timestamp и signature. Secret, полный destination и response body не попадают в delivery/audit logs.

| ID | Notification behavior |
|---|---|
| NOTIFY-001 | Public MVP включает inbox, unread count, deep links, read/dismiss/acknowledge и preferences |
| NOTIFY-002 | Events покрывают failed/stuck runs, DQ gate, stale data, forecast degradation, disabled schedule, worker/storage health и sensitive admin actions |
| NOTIFY-003 | Delivery дедуплицируется и группируется; retry не создаёт бесконечные копии |
| NOTIFY-004 | Recipient определяется membership/role/ownership/preferences; notification не раскрывает закрытый resource/PII |
| NOTIFY-005 | Event хранит codes/params, UI переводит текст на текущий язык |
| NOTIFY-006 | Email и webhook входят в `v1_target`, следующую версию после public MVP; до неё обязательного delivery runtime нет |
| NOTIFY-007 | Critical acknowledgement и admin dismissal попадают в audit |
| NOTIFY-008 | Public MVP активирует только in-app; email/webhook adapters, endpoint management и retries обязательны в `v1_target` |
| NOTIFY-009 | Email/webhook фиксируют immutable endpoint version/hash, bounded attempts, exponential backoff, stable error и terminal failure без secret/response body |
| NOTIFY-010 | Webhook использует HTTPS, timestamped signature, event ID как idempotency key, rotation-ready secret и SSRF/redirect controls из `SEC-006` |
| NOTIFY-011 | Operational email идёт только на verified destination, использует язык получателя с English fallback, authenticated deep link и не служит marketing campaign |
| NOTIFY-012 | Change/revocation endpoint создаёт новую immutable version только для новых delivery; history хранит redacted snapshot hash |
| NOTIFY-013 | In-app требует recipient и null endpoint; email — verified recipient и endpoint version; webhook — workspace target и endpoint version, recipient optional |
| NOTIFY-014 | Управление workspace-каналами показывает availability, immutable endpoint versions, verification/health, категории, последний bounded test и revoke/rotate без раскрытия destination/secret |
| NOTIFY-015 | Test delivery, rotation, disable и revoke permission-checked/audited; test использует отдельный event code, bounded attempts и тот же SSRF/signature/redaction contract без изменения production history |

### 15.4. Admin и Operator Center

Installation admin видит bootstrap/security, release/schema versions, service/worker/queue/outbox/reconciler health, local storage, migrations/upgrades/licenses, backup drills, plugins, localization, detected CPU/global cap и global report-recipient domains. Workspace admin управляет members/roles/invites/tokens, connections/secrets/policies, report/dashboard access, resource/retention, notification policies, narrowed recipient domains, sender identities, branding/company packs и report quotas; аналитический контент он не создаёт без отдельной роли. Operator работает с runs, attempts, workers, retry/cancel/rerun и redacted logs/traces.

| ID | Admin invariant |
|---|---|
| ADMIN-001 | Health view показывает versions, dependency readiness, queue age, outbox lag, reconciliation, heartbeat, disk и backup age |
| ADMIN-002 | Diagnostics download redacted, time-limited и audited, без secrets/raw PII/source values |
| ADMIN-003 | Retry/cancel/schedule disable/session-token revoke/plugin change/waiver/restore требуют permission и audit reason |
| ADMIN-004 | Destructive action показывает dependency impact и confirmation; bulk возвращает результат каждого ресурса |
| ADMIN-005 | Operator сравнивает attempts и выбирает retry failed node либо full rerun |
| ADMIN-006 | UI показывает orphan temp files, но разрешает только policy cleanup, не произвольный path deletion |
| ADMIN-007 | Restore выполняется в maintenance mode либо test environment и заканчивается integrity verification |
| ADMIN-008 | Installation admin видит CPU evidence и может только уменьшить cap; workspace не расширяет его |
| ADMIN-009 | Global report-domain allowlist versioned/default-deny/audited; workspace только сужает |
| ADMIN-010 | System lifecycle показывает release/schema versions, migrations, compatibility/readiness, upgrade requirement, licenses/SBOM/provenance и versioned runbooks; blind upgrade без preflight/backup/rollback запрещён |
| ADMIN-011 | Maintenance/upgrade имеют owner/reason/timestamps/affected scope/read-only policy/status; enter/exit/migrate/rollback требуют permission, confirmation и audit reason |

### 15.5. URL, workspace routing и browser history

Маршруты делятся на четыре семейства. Auth/bootstrap/invites являются public/auth; profile, global notifications и Help — global-user; `/admin/*` и `/audit` — installation; все ресурсы workspace имеют префикс `/w/:workspaceKey/*`. `workspaceKey` — неизменяемый публичный opaque identifier, но не доказательство доступа: authorization всегда повторно проверяется по membership, effective permissions и resource.

| ID | Route/history invariant |
|---|---|
| ROUTE-001 | Registry разделяет public/auth, global-user, installation и workspace; workspace resources используют `/w/:workspaceKey/*` |
| ROUTE-002 | `workspaceKey` immutable/opaque, но не authorization proof; guards разрешают resolved workspace/resource |
| ROUTE-003 | Protected guard выполняется до data fetch/render и не раскрывает существование, title, count, facet или cached denied content |
| ROUTE-004 | Resource/tab/Focus deep links создают history entry; presentation replace, transient menu/popover и refresh history не засоряют |
| ROUTE-005 | URL содержит только allowlisted stable state; raw PII/secrets/source values/filter values запрещены, complex filters идут через Saved View либо opaque short-lived reference |
| ROUTE-006 | Focus / Explore — route-backed full-viewport surface, не nested modal; Close/Escape/Back восстанавливают origin route/block/scroll/focus и direct-link fallback |
| ROUTE-007 | Drawer получает route/query только для deep-linkable resource/recoverable workflow; transient surfaces canonical URL не меняют |
| ROUTE-008 | Dirty draft защищён при route/workspace/Back/reload/close и предлагает Stay, Discard или Save draft |
| ROUTE-009 | Navigation обновляет title/breadcrumb/current location, восстанавливает focus/scroll либо page heading; shell/sidebar/topbar не remount-ятся |
| ROUTE-010 | Workspace switch сохраняет route suffix только при разрешённом target resource/capability, иначе ведёт на Overview с безопасным объяснением |
| ROUTE-011 | `returnTo` same-origin/allowlisted; session-expired хранит safe opaque reference и повторно проверяет authorization после login |
| ROUTE-012 | Route schema versioned; rename имеет redirects/deprecation, а после stable bookmarks требует migration/telemetry/rollback |

### 15.6. Motion, refresh и reduced motion

Production motion использует пять tokens: `none=0`, `fast=120`, `route=160`, `panel=220`, `slow=240` ms. Стандартный easing — `cubic-bezier(0.2, 0, 0, 1)`, exit — `cubic-bezier(0.4, 0, 1, 1)`. Motion является feedback, но не заменяет текст, status, focus или данные.

| ID | Motion invariant |
|---|---|
| MOTION-001 | Только versioned semantic tokens/easing; motion не несёт уникальный status/hierarchy/completion |
| MOTION-002 | Route сохраняет shell/sidebar/topbar; main content получает fade 120–160 ms, без full-screen slide |
| MOTION-003 | Sidebar expand/collapse 180–220 ms, без bounce/overshoot/blur; hidden state имеет restore control |
| MOTION-004 | Tabs indicator 120–160 ms, previous data остаются до готовности нового content и маркируются stale |
| MOTION-005 | Drawer 200–240 ms; modal fade + минимальный scale 160–200 ms; popover/menu 100–140 ms; focus semantics немедленные |
| MOTION-006 | Focus открывается как route surface без nested-modal/full-screen slide; Back/Escape следуют ROUTE-006 |
| MOTION-007 | Chart безопасно анимируется 160–240 ms только при стабильном domain/axis и малой density; dense/live/domain/policy changes без misleading interpolation |
| MOTION-008 | Табличные строки не «летают»; refresh использует краткую non-color-only highlight и текстовый status/timestamp |
| MOTION-009 | Refresh сохраняет previous authorized data, показывает local loading/freshness/status и блокирует недействительные stale controls |
| MOTION-010 | Skeleton преимущественно first load; refresh использует reserved layout и stale-while-revalidate, без reduced-motion shimmer |
| MOTION-011 | Reduced motion убирает translate/scale/bounce/shimmer/continuous charts; остаётся fade/status до 80 ms либо instant |
| MOTION-012 | Motion bounded/cancellable и тестируется keyboard/zoom/en/ru/reduced; live region не ждёт окончания animation |

### 15.7. System surfaces, Help и shortcuts

System surfaces не выглядят как пустая обычная страница: они объясняют scope воздействия, дают безопасную следующую action и stable support code, не раскрывая stack trace, внутренние paths, resource existence или migration secrets.

| ID | System surface |
|---|---|
| SYS-UI-001 | 403 остаётся на requested URL, не подтверждает resource и предлагает Back/разрешённый Overview/request-access guidance |
| SYS-UI-002 | 404 безопасно различает invalid route/client incompatibility; suggestions берутся только из разрешённой local history |
| SYS-UI-003 | Session expired очищает protected cache, хранит safe opaque return reference и после login повторяет permissions/draft recovery |
| SYS-UI-004 | Maintenance показывает safe owner message, scope, timestamps, read-only/status actions и bounded refresh с reduced motion |
| SYS-UI-005 | Upgrade required блокирует incompatible mutations, показывает current/required compatibility и admin runbook без sensitive migration details |

| ID | Help invariant |
|---|---|
| HELP-001 | `/help` ищет по shipped versioned docs, contextual help, разрешённым Data Guide и stable codes без внешней сети по умолчанию |
| HELP-002 | Shortcuts discoverable, searchable, platform-aware; ни один core action не требует помнить shortcut |
| HELP-003 | Help соответствует active release/locale/permissions и не индексирует denied features, secrets, source values или PII |
| HELP-004 | Contextual Help/shortcuts/support info доступны keyboard/screen reader, copy/print-safe и имеют deterministic deep links без поломки Back history |

## 16. API

Все endpoints начинаются с `/api/v1`. Это internal authenticated API для Web UI и доверенной automation, не публичный read-only result API.

| Resource | Основные операции |
|---|---|
| `/auth`, `/auth/sessions`, `/auth/api-tokens` | Bootstrap, login/refresh/logout/reset/profile, sessions, scoped tokens |
| `/workspaces`, `/workspaces/{id}/invites` | Workspaces, members, policies, invites |
| `/connections`, `/catalogs` | Metadata, test, discover, snapshots, preview |
| `/datasets`, `/metrics`, `/metric-groups`, `/number-formats`, `/filter-fields` | Draft/validate/publish/capabilities, metric/group/format versions и searchable typed filters |
| `/quality-rules`, `/quality-reports` | Rules, execution, reports и samples |
| `/pipelines`, `/runs`, `/artifacts` | Definitions, run/cancel/retry/events, metadata/preview/download |
| `/methodologies`, `/analysis-cases`, `/research-documents`, `/comments` | Methods, governed research, findings/publication и object-scoped discussion threads |
| `/analyses`, `/population-treatments`, `/segmentation-previews`, `/chart-specs`, `/promotions`, `/segments`, `/forecasts`, `/models` | Analyses, treatment bounds/sensitivity, bucket/stratified/KMeans preflight, validated ChartSpec, Promotion timeline, segment snapshots/profiles/migrations и forecasting/model registry |
| `/reports`, `/report-deliveries`, `/exports`, `/dashboards`, `/access-policies` | Report/dashboard definitions, object grants, snapshots/email и CSV/Parquet/JSON/XLSX jobs |
| `/brand-profiles`, `/company-packs` | Sanitized assets/tokens, preview, validation, version diff/impact и publish |
| `/data-guides`, `/file-import-templates` | Markdown guides и governed CSV/XLSX template validation/publication/versions |
| `/notifications` | Inbox, unread, preferences, read/acknowledge/dismiss |
| `/admin/plugins`, `/admin/operations`, `/audit` | Plugins, health/workers/outbox/reconciler/storage/backups и audit |

Response содержит `data` и `meta.request_id/api_version`. Error содержит stable `code`, safe English fallback `message`, locale-neutral `params`, optional `details`, `retryable` и request ID. Frontend переводит code+params; stack trace не возвращается.

Workspace scope берётся из authenticated membership/path/resource, а не из body. Collections используют opaque cursor, bounded page size, deterministic order, allowlisted typed sort/filter. Draft mutations требуют ETag/If-Match. Long commands отвечают `202` и status URL. Run/retry/report-render/report-email/export create используют scoped `Idempotency-Key`. Upload/download streamed и bounded.

| ID | API contract |
|---|---|
| API-001 | Collection имеет bounded pagination и deterministic order |
| API-002 | Filter/sort allowlisted и typed, SQL fragments запрещены |
| API-003 | Repeatable side effect поддерживает Idempotency-Key с actor/workspace/route/payload hash scope |
| API-004 | Long command отвечает 202/status URL, HTTP не ждёт compute result |
| API-005 | Draft mutation требует ETag/If-Match и сообщает current revision при conflict |
| API-006 | Download заново проверяет artifact/PII permission и безопасный filename |
| API-007 | Body/query/upload/response limits документированы и имеют stable errors |
| API-008 | Rate limits разделены для auth/reset, preview, run, report render/email, export и diagnostics |
| API-009 | OpenAPI описывает errors, scopes, pagination, idempotency и async responses |
| API-010 | Internal JSON result bounded по rows/bytes и не заменяет CSV/Parquet |

## 17. Сервисы и ответственность

| ID | Процесс и роль |
|---|---|
| SVC-WEB | React SPA: forms, canvas, tables и единственный v1 Web chart adapter ECharts SVG/Canvas через shared `packages/chart_compiler_ts` |
| SVC-API | FastAPI: auth, metadata, validation, commands, JSON/SSE |
| SVC-SCHEDULER | Claims due schedules и создаёт run/outbox records в PostgreSQL |
| SVC-ORCHESTRATOR | Отдельный process для DAG readiness и state transitions |
| SVC-OUTBOX | Доставляет PostgreSQL outbox в Valkey |
| SVC-RECONCILER | Идемпотентно чинит delivery, leases и aggregate states |
| SVC-DATA-WORKER | Extraction, transforms, DQ, marts и analytics |
| SVC-ML-WORKER | Clustering, backtests, fit/predict |
| SVC-REPORT-WORKER | Report composition, shared compiler в bounded embedded Node ECharts SSR, bundled fonts, SVG→PNG, XLSX native/raster, email и reconciliation |
| SVC-POSTGRES | Durable control-plane state |
| SVC-VALKEY | Broker, cache и ephemeral locks |
| SVC-ARTIFACTS | Только local immutable bulk objects на persistent volume |
| SVC-PROXY | Secretless/state-free инфраструктурный Edge-адаптер входа: TLS, routing и limits только к фиксированному Web upstream; это не bounded context и не новый продуктовый микросервис |
| SVC-OTEL | Optional telemetry collector |

Backend разбит на domains: identity/access, который также владеет OrgUnit, memberships, leadership, department policies, grants, ownership и privacy-safe contributor projection; connections/catalog; semantic model с metrics/groups/formats/filter registry; data documentation и file-import templates; ingestion; execution с outbox/leases/reconciliation; artifacts; DQ; analytics; methodology/research с cases/findings/comments/products; Promotion Journal; forecasting; presentation, владеющий canonical ChartSpec/compiler ports, dashboards/reports/access policies/branding/company packs и render metadata; report delivery; notifications; audit. Один domain не читает private tables другого напрямую — только contract/repository. Нового deployable organization service не создаётся.

PostgreSQL содержит users/roles/workspaces/members/invites/sessions/reset tokens/API tokens; OrgUnit/structure versions, primary memberships, leadership assignments, department data policies, cross-department grants, resource ownership bindings и contributor projections; connections/secrets/catalogs; semantic/identity/metric/group/format/filter/capability versions и diffs/impacts; extraction batches/watermarks; quality rules/reports/issues/waivers; pipelines/schedules/runs/nodes/outbox/leases/reconciliation/idempotency; artifact manifests/dependencies; analyses/methodologies/cases/research documents/findings/decisions/analytical products/comments/segments/promotions/windows/audience bindings; forecasts/backtests/models/monitoring; ChartSpec/render-artifact metadata; dashboard/report definitions/access policies/snapshots/rendered artifacts/email policies/senders/deliveries; brand profiles/assets/company packs; exports/Data Guides/file-import templates; notifications; plugins и audit.

## 18. Технические зависимости

### 18.1. Backend и data engine

Python 3.12, FastAPI/Uvicorn, Pydantic/settings, SQLAlchemy Core без ORM/ActiveRecord, Alembic, psycopg, pyodbc, pinned MySQL driver, `clickhouse-connect`, Celery, redis-py, croniter и httpx образуют runtime. Polars — основной dataframe engine, PyArrow — Arrow/Parquet interchange, DuckDB — local OLAP, optional ConnectorX/ADBC — ускорение extraction, sqlglot — SQL AST, а выбранный bounded XLSX reader/renderer не исполняет formulas/macros. Pandas допустим только на compatibility boundary.

### 18.2. Analytics, security и observability

NumPy/SciPy обязательны, statsmodels желателен, scikit-learn/CatBoost/StatsForecast обязательны, holidays желателен, mlxtend optional, Optuna и MLflow — post-v1. Password hashing использует Argon2; PyJWT подписывает и проверяет только short-lived local access JWT, тогда как opaque refresh tokens сверяются с hash/session records без JWT decoding. Future OIDC использует Authlib только после v1 и approved provider contract; secrets — `cryptography` с `AES-GCM`, uploads — python-multipart. Structured telemetry строится на structlog, prometheus-client и OpenTelemetry FastAPI/Celery instrumentation.

### 18.3. Frontend и localization

Node.js active LTS, React, TypeScript, Vite, MobX, styled-components, i18next/react-i18next, React Flow, TanStack Query, `lucide-react`, Apache ECharts core и Playwright обязательны. Lucide является единственной core outline icon family с versioned semantic mapping для navigation/actions. Node используется для frontend build и bounded ECharts SSR внутри report-worker image. Presentation-owned `@custometry/chart-compiler` из `packages/chart_compiler_ts` является единственной ChartSpec→ECharts implementation для обоих consumers; versioned bundled en/ru Inter Variable pack обеспечивает одинаковую typographic layout. TanStack Table, Zod и React Hook Form желательны. Dash, Plotly core, ECharts-GL и WebGL chart runtime отсутствуют в v1 lockfile. Конкретный network-disabled SVG→PNG rasterizer выбирается fidelity/performance/security spike без изменения ChartSpec. Accessibility regression использует axe-core/`@axe-core/playwright`. Backend-generated text при его появлении использует Python gettext catalogs и Babel; domain/API errors и events остаются locale-neutral.

MobX отвечает за быстрый local/workspace state: навигацию, command palette,
геометрию панелей и обратимое optimistic feedback. TanStack Query отвечает за
authoritative REST/SSE snapshots, invalidation, cancellation и
stale-while-revalidate. UI не может сам выдать право, подтвердить persistence,
run, delivery или terminal result. styled-components строит typed composition,
а четыре темы и white-label разрешаются через semantic CSS custom properties.

| ID | Frontend architecture invariant |
|---|---|
| WEB-ARCH-001 | Authenticated Web использует React/TypeScript/Vite/MobX/TanStack Query/styled-components; backend и REST/SSE планы не меняются |
| WEB-ARCH-002 | MobX владеет client/workspace state, server-state adapter — authoritative snapshots; frontend не принимает authorization/terminal decisions |
| WEB-ARCH-003 | Themes/white-label используют semantic CSS variables; arbitrary CSS/JS, remote fonts и untrusted styles запрещены |
| WEB-ARCH-004 | Route migration обратима, сохраняет deep links/history/Back/refresh и fallback до полного browser evidence |
| WEB-ARCH-005 | Linear задаёт измеримую fidelity, но его branding/entities/assets/text/source/undocumented policy не копируются |
| WEB-ARCH-006 | Sidebar/detail panes имеют bounded pointer resize, persisted preference, reset и keyboard alternative без влияния на permissions/routes |

| ID | Perceived-performance invariant |
|---|---|
| WEB-PERF-001 | Evidence фиксирует hardware/browser/viewport/CPU/RAM/data/sample/cold-warm-cache и p50/p75/p95, разделяя client/network/API/render |
| WEB-PERF-002 | Feedback target p75 <= 50 ms/p95 <= 100 ms; recurring main-thread tasks > 50 ms в accepted journey запрещены |
| WEB-PERF-003 | Warm navigation acknowledgement target p75 <= 100 ms/p95 <= 200 ms; uncached route truthful acknowledges within 100 ms |
| WEB-PERF-004 | Dispatch target p75 <= 20 ms/p95 <= 50 ms; response/SSE-to-paint target p75 <= 100 ms/p95 <= 200 ms |
| WEB-PERF-005 | Representative INP p75 <= 100 ms, hard ceiling 200 ms; animations target 60 fps без recurring jank |
| WEB-PERF-006 | Refresh сохраняет authorized data/reserved layout, отделяет client overhead от backend wait и не выдаёт optimistic/stale state за terminal truth |

### 18.4. Toolchain и лицензии

Python packages/lock — `uv`/`uv.lock`; frontend — `pnpm`/`pnpm-lock.yaml`; Ruff, mypy/Pyright, pytest, Hypothesis, Testcontainers, Playwright, OpenAPI, Docker и Docker Compose. Lockfiles pinned; automated dependency updates для data/ML проходят regression benchmarks.

Проект лицензируется Apache 2.0. По умолчанию допустимы Apache-2.0, ISC, MIT, `BSD-2-Clause`, `BSD-3-Clause` и PostgreSQL License. `MPL-2.0` и LGPL требуют review. AGPL, SSPL и source-available non-OSS запрещены без architecture/legal decision. CI формирует SBOM и license report. Для Lucide сохраняются upstream ISC и унаследованные Feather MIT notices в `THIRD_PARTY_NOTICES`; SF Symbols не включаются в Web assets/dependencies из-за Apple-platform distribution boundary.

## 19. Почему выбран этот стек

| ID | Решение | Смысл |
|---|---|---|
| ADR-001 | Modular monolith | Реалистичен для небольшой команды; services выделяются по доказанной необходимости |
| ADR-002 | PostgreSQL control plane | Транзакции, migrations и будущий RLS; SQLite только tests |
| ADR-003 | Parquet artifacts | Открытый columnar format; массовые данные не складываются в PostgreSQL |
| ADR-004 | Polars + DuckDB | Lazy Python transforms и local OLAP; Pandas не core engine |
| ADR-005 | Celery + Valkey | Понятный task stack; authoritative state остаётся в PostgreSQL |
| ADR-006 | React Flow | Готовый MIT canvas вместо дорогой собственной реализации |
| ADR-007 | Собственное semantic/metric core | Главная ценность Custometry, не обязательная dbt-зависимость |
| ADR-008 | Lightweight model registry | Меньше обязательных services; MLflow позже |
| ADR-009 | Guided before canvas | Сначала аналитические journeys, а не generic ETL clone |
| ADR-010 | Multi-workspace installation | Несколько изолированных команд в одной self-hosted инсталляции |
| ADR-011 | Local filesystem through v1 | Сначала доказать atomicity, recovery и backup одного сервера; remote storage — будущий ADR |
| ADR-012 | English default, Russian required | Международная база и обязательное русское покрытие; single-language продукт запрещён |
| ADR-013 | Product-owned ChartSpec + ECharts adapters | Один смысловой контракт для Web/email/XLSX; raw ECharts option больше не source of truth |

До v1 не используются Airflow runtime, FastAPI background tasks для тяжёлых jobs, DuckDB как control DB, Valkey как final run state, remote/object artifact storage, multi-host workers, arbitrary notebooks и пользовательский код. Dash не используется как второй application framework; Plotly возможен только post-v1 plugin; ECharts-GL/WebGL/GPU analytics запрещены.

## 20. Безопасность и приватность

Threat model включает утечку secrets, SQL injection, IDOR/workspace/department bypass, hidden counts соседнего отдела, неконтролируемый cross-department grant, превращение contributor analytics в employee surveillance, session/token theft и refresh replay, CSRF, brute force, excessive preview, cross-workspace/PII leaks, report email на запрещённый/confusable domain, spoofed sender, duplicate after unknown submit, executable/raw chart options, chart callbacks/URLs/regex, SSR/raster resource exhaustion или remote fetch, trusted plugin risk, path traversal, CSV/XLSX formula injection, unsafe Markdown/email HTML, unsafe model deserialization и SSRF.

### 20.1. RBAC и multi-workspace isolation

Permissions разделяют installation/workspace management, members/roles, organization read/manage/assignment/leadership/data-policy/delegation/ownership/activity, connections/secrets, file-import templates/import execution, dataset/quality/waiver, metric definitions/groups/number formats/methodologies, analytics/promotions/segments/forecasts/pipelines/runs, PII, artifacts, report read/manage/send/XLSX/email-policy, Data Guide read/publish, exports/dashboards/notifications, global BrandProfile/CompanyPack management, workspace brand assignment, tokens/plugins/audit. Installation Administrator не получает автоматический доступ к workspace data. Functional role, organization membership и leadership assignment независимы; effective access пересекает role, organization, data, object, row/column и PII ceilings, а deny побеждает allow.

| ID | RBAC invariant |
|---|---|
| RBAC-001 | Workspace-scoped metadata, artifacts, tasks, cache, notifications и audit несут workspace ID |
| RBAC-002 | Central policy service проверяет list/detail/action; worker повторяет check перед sensitive access |
| RBAC-003 | Installation role не означает membership; support grant time-bounded и audited |
| RBAC-004 | Actor не выдаёт permission выше собственных в scope, кроме bootstrap policy |
| RBAC-005 | PII preview/download, segment export, report send/XLSX, Data Guide publish, email policy, waiver, tokens и diagnostics — отдельные permissions |
| RBAC-006 | List/count/search фильтруют rows до pagination/aggregation, не раскрывая существование objects |
| RBAC-007 | RLS желательно как defense-in-depth после transaction-local workspace context; app auth остаётся |
| RBAC-008 | Cache/idempotency scope включает workspace ID и effective policy version |
| RBAC-009 | Workspace Administrator default bundle ограничен users/roles/object access/connections/policies и не включает analytical authoring или PII |
| RBAC-010 | Analyst создаёт metrics/methods/research/segments/dashboards/reports, но не управляет connections, users, role assignments или access grants |
| RBAC-011 | Viewer читает только granted projections, может comment и никогда не получает raw PII |
| RBAC-012 | Report/dashboard access policy versioned, auditable, default-deny и управляется отдельным administrative permission |
| RBAC-013 | PII — explicit scoped expiring grant; role name сам по себе не раскрывает raw fields |
| RBAC-014 | Comment create/read/resolve отдельно проверяются и не расширяют access к source artifact или hidden filters |
| RBAC-015 | Effective-access preview и audit объясняют role, object, row, PII и expiry decisions без раскрытия denied data |
| RBAC-016 | Metric, MetricGroup и NumberFormat используют отдельные read/manage/publish permissions; dataset management не меняет их неявно |
| RBAC-017 | FileImportTemplate lifecycle и import execution разделены permissions и не наследуются автоматически от connection management |
| RBAC-018 | Global BrandProfile/CompanyPack management отделён от workspace `brand.assign`, который выбирает только разрешённую published version |
| RBAC-019 | Functional role, department membership и leadership — независимые измерения; названия отделов не создают новые role bundles |
| RBAC-020 | Effective access — пересечение role, workspace, organization, DepartmentDataPolicy, ObjectAccessPolicy, row/column и PII ceilings; deny wins |
| RBAC-021 | Каждый active member имеет ровно один primary department/team; orphan member не читает business data |
| RBAC-022 | Department Leader — effective-dated scoped assignment для unit и optional subtree, а не глобальная роль |
| RBAC-023 | CrossDepartmentGrant bounded, reasoned, effective-dated/expiring и не повышает role/PII ceiling |
| RBAC-024 | Personal drafts остаются personal; published resource по умолчанию department-owned, creator attribution immutable |
| RBAC-025 | Snapshot read не означает dataset/edit/run/drill-down/raw artifact/PII permission |
| RBAC-026 | Transfer/deactivation прекращает старый scope, переоценивает grants и запускает ownership handover без переписывания истории |
| RBAC-027 | ContributorActivityProjection агрегирована и redacted; raw audit, hidden counts, peer ranking и productivity score запрещены |
| RBAC-028 | Workspace Administrator конфигурирует organization, но не получает activity/business content/PII автоматически |

### 20.2. Организационная структура, ownership и privacy

`OrgUnit` образует workspace-scoped дерево `company → division → department → team` с effective dates, status и successor mapping; hard delete запрещён. Для активного пользователя существует ровно одно primary assignment. Leadership assignment отдельно задаёт unit, optional descendants и срок действия. `DepartmentDataPolicyVersion` определяет dataset/row/column/PII ceiling и default visibility, а `CrossDepartmentGrant` временно расширяет только явно указанный allow scope.

Автор и владелец ресурса различаются. Draft личный; новая публикация по умолчанию принадлежит primary department автора; legacy objects получают `workspace_legacy` до аудита. Transfer сохраняет creator attribution, закрывает старый доступ и создаёт handover для published resources.

People & Creators читает отдельную `ContributorActivitySummary`, построенную из allowlisted redacted domain events. Профиль показывает доступные отчёты/dashboards и безопасные агрегаты только самому сотруднику, scoped leader или explicit grantee. Рейтинги, leaderboard, productivity score, hidden counts и raw audit feed не входят в продукт.

### 20.3. Local auth и будущий OIDC boundary

Local auth входит в public MVP. Общий `IdentityProvider` normalizes platform principal, но OIDC/Keycloak/Authlib runtime относится к post-v1 и отдельному security ADR.

Bootstrap работает только при zero users и защищён одноразовым deployment token. Invite хранится hash-only, workspace/identity/grants/expiry и single-use. Password использует Argon2id. Access short-lived, refresh opaque rotating hash-only с session/device/absolute expiry/revocation. API token показывается один раз, hash-only, workspace/scopes/expiry/last use/revocation.

| ID | Auth lifecycle |
|---|---|
| AUTH-001 | Bootstrap необратимо отключается после первого admin; recovery только host-level documented procedure |
| AUTH-002 | Invite single-use/expiring/revocable, не выше grants inviter, acceptance audited |
| AUTH-003 | Public MVP имеет password change и admin/host one-time reset; self-service email ждёт email channel |
| AUTH-004 | Password/reset/privilege increase/refresh replay отзывает применимые sessions/token family |
| AUTH-005 | Refresh rotation обнаруживает reuse; user/admin могут list/revoke sessions по permission |
| AUTH-006 | Browser auth использует Secure HttpOnly SameSite cookies, CSRF token и Origin validation |
| AUTH-007 | API token workspace-scoped, expiring, least-privilege, shown once, hash-only и revocable |
| AUTH-008 | Login/reset/invite/token endpoints rate-limited, с generic failure и безопасными security metrics |
| AUTH-009 | Logout отзывает текущую refresh session; доступны logout-all и admin revoke |
| AUTH-010 | CORS allowlist deployment-configured; wildcard origin с credentials запрещён |
| AUTH-011 | OIDC post-v1, но provider contract и normalized-principal tests существуют заранее |

### 20.4. Secrets, PII, files, plugins и audit

Encrypted secret payload/reference хранится в PostgreSQL, master key — только environment/file secret. Envelope использует authenticated encryption, key version и rotation; plaintext не возвращается и редактируется из logs/traces. Vault/KMS — post-v1.

PII classes: `none`, `internal`, `personal`, `sensitive`; artifact наследует максимальный класс, если node доказуемо не anonymizes/aggregates. Upload проверяется streaming size/hash/content, XLSX bounded, archives до v1 запрещены, user name не становится path. Plugin — trusted process code; настоящий sandbox не входит в v1.

Audit event хранит event/time, `scope_type` installation/workspace, nullable workspace только для installation scope, actor/action/resource/request, before/after hashes, success/failure и redacted metadata. Cross-workspace support создаёт отдельный workspace audit.

| ID | Дополнительный security control |
|---|---|
| SEC-001 | Proxy завершает TLS и ставит HSTS/CSP/frame/nosniff/referrer policies |
| SEC-002 | Artifact UUID-path нормализуется под root и защищён от traversal/symlink escape |
| SEC-003 | Upload проходит quarantine streaming size/hash/type checks до manifest |
| SEC-004 | CSV neutralizes formula prefixes reversible escaping |
| SEC-005 | Недоверенный pickle/joblib запрещён, model formats/versions allowlisted |
| SEC-006 | Outbound HTTP применяет scheme/host/DNS/IP/redirect controls и egress policy |
| SEC-007 | Secret plaintext минимально живёт только в разрешённом process и редактируется в telemetry |
| SEC-008 | Encryption envelope хранит key version и меняет key без смены logical secret ID |
| SEC-009 | Official release публикует SBOM, vulnerability report и signed provenance; critical finding блокирует |
| SEC-010 | Audit append-only на application level, с retention и gap/tamper detection |
| SEC-011 | Sensitive export имеет limits, purpose/reason, audit, short retention и re-authorization |
| SEC-012 | User errors/traces не раскрывают paths, DSN, SQL params, secrets и raw PII |
| SEC-013 | Installation audit имеет `scope_type=installation` и null `workspace_id`; любое действие с workspace data создаёт workspace-scoped event с ненулевым workspace ID |
| SEC-014 | ChartSpec/API отклоняют raw options/functions/renderItem/HTML/CSS/URLs/assets/expressions/regex; adapters принимают только validated allowlist |
| SEC-015 | Static chart renderer без network, с read-only runtime, resource/time/path/workspace limits и cleanup partial SVG/PNG |
| SEC-016 | Edge/proxy остаётся secretless/state-free инфраструктурным ingress-адаптером без бизнес-логики и пользовательского upstream, а не отдельным bounded context или продуктовым микросервисом |
| SEC-017 | Путь разделён на разные internal networks `edge_to_web` и `web_to_api`; Edge не имеет общей сети с API, control-plane, PostgreSQL, Valkey или workers |
| SEC-018 | Compose не считается portable ingress-only или Edge egress-denial механизмом; production требует target-specific firewall/CNI-equivalent policy и positive/negative runtime evidence |

## 21. Наблюдаемость и эксплуатация

Structured log содержит timestamp, level, service/environment, request/trace/workspace/run/node IDs, event code, safe message и duration. PII/secrets запрещены.

Metrics покрывают API latency/errors/pools/auth/export; queue age/tasks/retries/heartbeats/cancel/outbox/leases/reconciler; extraction/artifacts/cache/DQ/freshness/partitions/local bytes-inodes/orphans; forecast training/model/WAPE/bias/coverage/age; notifications/auth replay/rate limits. Для visual/report surface отдельно измеряются ChartSpec validation/compile failures, SVG/Canvas selection/bounded-data rejects, SSR SVG→PNG queue/duration/timeout/cancel/failure/RSS/temp/cache, XLSX native-vs-raster/parity failures, report bytes/retention, email outcomes/policies, CPU allocation и progress/ETA quality.

Health endpoints: `/health/live`, `/health/ready`, `/health/dependencies`. Liveness не проверяет externals; readiness отвечает за безопасный приём requests; details доступны admin.

Backup включает PostgreSQL, local artifacts, master key/KMS config, deployment config и plugin list. Backup без регулярного restore drill не считается проверенным.

| ID | Operations requirement |
|---|---|
| OPS-001 | Versioned runbooks покрывают DB/queue/outbox/worker/disk/hash/migration/restore incidents |
| OPS-002 | Readiness false при unsafe mutations, но documented read-only metadata может остаться |
| OPS-003 | Disk low/high watermarks заранее блокируют heavy runs и создают critical notification |
| OPS-004 | Backup manifest связывает DB/artifact snapshots, key/release/schema versions и verification |
| OPS-005 | Recovery test проверяет manifests, isolation, secret decrypt, published definitions и sample result |
| OPS-006 | SLO thresholds ставятся после baseline, но metric names и owners существуют в public MVP |
| OPS-007 | V1 runbooks покрывают report backlog, XLSX limit, mail unavailable, sender authorization и unknown delivery |
| OPS-008 | V1 runbook покрывает invalid/unsupported ChartSpec, renderer backlog, SSR/raster timeout/crash, bounded-data reject, parity failure и safe cleanup/retry |

## 22. Тестирование

Test pyramid включает pytest unit/property/contract/API, Testcontainers integrations, golden Parquet, forecast regression, Vitest components, Playwright E2E, i18next/gettext localization, axe/manual accessibility, security scans, Compose recovery fault injection и dedicated performance benchmarks. Отдельные chart gates проверяют valid/invalid ChartSpec, executable/network-field rejection, bounded data, identical compiled-option hash одного shared compiler build в Web/SSR, Web SVG/Canvas semantics, range timeline, SSR SVG→PNG, bundled-font/compiler/renderer-build identity invalidation, XLSX native/raster mapping и four-theme accessibility. Report gates проверяют golden parity Web/email/XLSX, OOXML/openability/charts/split/formula-injection и email transport на test adapter плюс approved real-boundary canary. Реальные PostgreSQL, MSSQL, MySQL/MariaDB и ClickHouse connector matrices обязательны; CSV/XLSX templates проходят security fixtures. Mocks не заменяют release evidence.

### 22.1. Обязательные инварианты

| ID | Что должно всегда оставаться истинным |
|---|---|
| TEST-INV-001 | Join с lines не увеличивает receipt count |
| TEST-INV-002 | Segment members соответствуют overlap policy |
| TEST-INV-003 | RFM не видит события после as-of |
| TEST-INV-004 | Forecast features не видят будущее origin |
| TEST-INV-005 | Retry node не создаёт два successful manifests |
| TEST-INV-006 | Failed write не публикуется |
| TEST-INV-007 | Workspace A не читает metadata B |
| TEST-INV-008 | Overview revenue согласован с source mart в tolerance |
| TEST-INV-009 | Incomplete current period не входит в training без policy |
| TEST-INV-010 | Одинаковые source-local IDs разных namespaces не объединяются без identity mapping |
| TEST-INV-011 | Temporal join выбирает одну SCD version и отклоняет overlap |
| TEST-INV-012 | Distinct/semi-additive не суммируются, ratio пересчитывается |
| TEST-INV-013 | Cross-currency total blocked без group/FX policy |
| TEST-INV-014 | Crash между DB commit и queue publish восстанавливает outbox без потери run |
| TEST-INV-015 | Stale fencing worker не публикует manifest/state |
| TEST-INV-016 | Failed multi-table extraction не двигает watermark и не публикует partial partitions |
| TEST-INV-017 | Expired/revoked waiver не разрешает gate, non-waivable остаётся blocked |
| TEST-INV-018 | Isolation действует на list/count/search, artifacts, cache, idempotency, tasks, notifications, exports |
| TEST-INV-019 | Refresh reuse revokes family, no-CSRF mutation и revoked API token rejected |
| TEST-INV-020 | Hard-cancel child не оставляет committed output и не убивает long-lived worker |
| TEST-INV-021 | Dashboard не расширяет artifact permission и различает pinned/latest |
| TEST-INV-022 | en/ru keys/placeholders/plurals равны и journeys проходят в обоих языках |
| TEST-INV-023 | Language/format locale не меняют run/result/artifact/cache hashes |
| TEST-INV-024 | Guided и equivalent pipeline дают одинаковый normalized spec/result |
| TEST-INV-025 | Clean Compose install/migration/backup/restore проходят на release candidate |
| TEST-INV-026 | Receipt-grain revenue с product/category/brand отклоняется; отдельная item-grain revenue metric сходится с header total в policy tolerance |
| TEST-INV-027 | Invalid run/node/schedule transition отклоняется; terminal attempt не переписывается; schedule lifecycle и health независимы |
| TEST-INV-028 | Expired/aborted ExtractionSession не публикует artifact/watermark; committed multi-table batch доказывает общий session либо documented best-effort mode |
| TEST-INV-029 | Public MVP не активирует email/webhook; v1 delivery pins endpoint version, дедуплицируется, bounded-retry и проверяет webhook signature/SSRF |
| TEST-INV-030 | Каждый backtest/model ссылается на существующий immutable `forecast_spec_version_id` того же workspace |
| TEST-INV-031 | Customer marts/segments используют canonical customer и collision-free PK; sales-period key включает period, fact scope и все dimensions |
| TEST-INV-032 | Web/email/XLSX одного snapshot используют одни resolved blocks/artifacts/filters/metrics/comparison/schema/units/lineage и totals |
| TEST-INV-033 | Immutable comparison artifact pin-ит periods/timezone/calendar/policies/versions; YoY корректен для leap day/week53/fiscal/incomplete |
| TEST-INV-034 | Filter search/facets/hierarchy/relative-date/null policy не раскрывают запрещённое; versioned expression/anchor/timezone входят в identity/lineage |
| TEST-INV-035 | Promotion audience pinned, overlaps не теряются, overlay не получает causal label |
| TEST-INV-036 | Email rejected для unverified sender, forbidden domain или недостаточных PII/report rights |
| TEST-INV-037 | Crash ready/submit восстанавливает encrypted recipients; unknown submit reconciles по persisted adapter handle и не blind-retry |
| TEST-INV-038 | XLSX split не теряет/дублирует rows, formula text safe, workbook/chart data valid |
| TEST-INV-039 | Data Guide sanitizes active content и становится review-required при dataset drift |
| TEST-INV-040 | CPU detector/cap учитывает affinity/cgroup, pools соблюдают allocation, invalid cap rejected |
| TEST-INV-041 | Progress monotonic/reconnectable; unknown total даёт null percent/ETA; run state независим |
| TEST-INV-042 | Six themes проходят contrast/keyboard/chart-table checks; switch не меняет result/cache identity |
| TEST-INV-043 | Canonical ChartSpec не содержит raw options/functions/renderItem/HTML/CSS/URLs/assets/regex; invalid spec rejected до render |
| TEST-INV-044 | Один ChartSpec/data и immutable shared compiler build дают одинаковый option hash, values/styles в Web SVG/Canvas, SSR SVG, email PNG и XLSX native/raster |
| TEST-INV-045 | range_timeline совпадает с accessible table по planned/actual/channels/audiences/overlaps/visible window |
| TEST-INV-046 | SVG/Canvas policy не меняет semantics; Dash/Plotly core/ECharts-GL/WebGL отсутствуют, browser не считает business metrics |
| TEST-INV-047 | Email PNG идёт из SSR SVG; XLSX native lossless либо same-pipeline PNG с typed data без изменения totals |
| TEST-INV-048 | Static renderer без network/remote/system fonts, соблюдает limits/cancel и не публикует partial SVG/PNG; compiler/renderer/font hash rotation инвалидирует cache identity |
| TEST-INV-049 | Focus / Explore сохраняет source/comparison/permissions/trust при Chart↔Table, защищает system/locked filters, разделяет result/presentation identity и возвращает route/block/scroll/focus |
| TEST-INV-050 | Canonical routes, workspace switch, guards, deep links, Back/Forward, safe returnTo, dirty guard и Focus восстанавливают только разрешённый resource без metadata/query leaks |
| TEST-INV-051 | Motion/reduced-motion соблюдают tokens; shell сохраняется, refresh держит previous data/status, dense/live/domain charts не интерполируются, table rows не летают |
| TEST-INV-052 | System surfaces, Help/shortcuts, notification channels и admin lifecycle дают безопасные actions/codes, permissions/redaction и не раскрывают secrets/denied/migration internals |
| TEST-INV-053 | NumberFormatSpec одинаков на границах rounding/compact suffix и не превращает non-zero percentage в 0% |
| TEST-INV-054 | MetricGroupVersion сохраняет один group/metric order в Web/email/XLSX и не меняет metric semantics |
| TEST-INV-055 | XLSX README содержит safe sources, filters, metrics, methodology, quality и lineage без secrets/hidden policy/denied PII |
| TEST-INV-056 | Admin, Analyst и Viewer соблюдают разделение connections/access/content/PII и comment не расширяет права |
| TEST-INV-057 | Research document воспроизводим по pinned case/method/data/metric/filter/evidence versions, а comment не подменяет reviewed finding |
| TEST-INV-058 | Brand assets/tokens проходят sanitization/contrast и дают одинаковую pinned identity в Web/email/XLSX/docs |
| TEST-INV-059 | Четыре SQL connectors проходят real matrix; CSV/XLSX отклоняют unknown structure, formulas, macros и template violations |
| TEST-INV-060 | Public build/docs/index не содержат private activation artifacts или скрытой runtime dependency |
| TEST-INV-061 | Treatment не меняет canonical data/metric; pinned inputs/method/bounds/action/code воспроизводят flags/caps/exclusions и impact |
| TEST-INV-062 | Default `vs LY` использует shared bounds; independent exploratory bounds имеют отдельную identity и disclosure |
| TEST-INV-063 | Bucket membership детерминирован на ties/missing/boundaries, а published pinned bounds не пересчитываются молча |
| TEST-INV-064 | KMeans соблюдает exact K, feature order/preprocessing/seed/CPU, исключает ID/PII/leakage и публикует полный diagnostic snapshot |
| TEST-INV-065 | Excluded-from-fit extremes не исчезают из assignment без policy; post-fit сохраняет outlier/distance/confidence и sensitivity |
| TEST-INV-066 | Promo/loyalty/bonus/other сходятся с source total/net/base в tolerance; unknown не равен zero |
| TEST-INV-067 | Bonus accrual не попадает в redemption/discount, stacking/precedence не допускает double attribution |
| TEST-INV-068 | Aggregate rate является ratio-of-sums; average row rates и overlap double count ловятся golden tests |
| TEST-INV-069 | Historical cap breach сохраняется без clamp, simulated breach блокирует publication, включая boundary rounding/returns |
| TEST-INV-070 | Timeline overlap не создаёт promo attribution без sale flag/direct mapping |
| TEST-INV-071 | PVM effects сходятся с observed delta и детерминированно обрабатывают assortment/missing/UOM cases |
| TEST-INV-072 | Current/LY pin-ят compatible policy/method; drift меняет result identity и disclosure |
| TEST-INV-073 | Direct/derived/proxy/total-only/unavailable дают разные capability/trust outcomes во всех channels |
| TEST-INV-074 | Metric lifecycle/certification независимы, replacement сохраняет historical lineage |
| TEST-INV-075 | Future method не запускается и не показывается как implemented |
| TEST-INV-076 | У active member ровно одно primary department/team assignment; overlaps запрещены |
| TEST-INV-077 | Effective access пересекает role/organization/data/object/row-column/PII; deny не отменяется grant |
| TEST-INV-078 | People/resources list/count/search/pagination не раскрывают hidden departments или counts |
| TEST-INV-079 | Leader видит activity только своего scope и не получает raw AuditEvent/PII автоматически |
| TEST-INV-080 | CrossDepartmentGrant bounded, reasoned, expiring и после revoke не остаётся в cache |
| TEST-INV-081 | Snapshot read не выдаёт dataset/edit/run/drill-down/artifact/PII actions |
| TEST-INV-082 | Draft personal, publication department-owned, creator attribution immutable |
| TEST-INV-083 | Transfer прекращает старый scope, сохраняет attribution и создаёт ownership handover |
| TEST-INV-084 | Deactivated/merged OrgUnit сохраняет историю/successor; hard delete невозможен |
| TEST-INV-085 | Contributor projection redacted/allowlisted, без ranking/score/hidden refs/raw audit |
| TEST-INV-086 | Workspace Admin управляет structure без автоматического activity/content/PII access |
| TEST-INV-087 | Structure/data-policy versions используют ETag, immutable publish и auditable diff |
| TEST-INV-088 | Self/leader/grantee получают разные policy-correct contributor projections |

Golden datasets включают ideal, anonymous, returns, multi-currency, late corrections, duplicates, missing products, SCD, irregular/intermittent series, new store, incomplete month, duplicate source IDs, overlapping/gapped validity, разные metric kinds, percentage/compact-format boundaries, stable metric groups, YoY leap/week53/fiscal cases, overlapping promotions, skewed/zero-inflated/heavy-tail sales с legitimate VIP и DQ-invalid rows, quantile/IQR/MAD bounds/ties/missing, global/within-stratum/privacy-cardinality cases, exact-K/frozen/retrain KMeans fixtures, research findings/comments, low/high-cardinality sensitive filters, safe/unsafe Markdown и brand assets, multi-block reports, generated XLSX README/limits/injection/names, four themes, полный ChartSpec allowlist, invalid executable/network specs, range timeline, dense aggregate/sample/LOD, identical shared-compiler Web/SSR option hashes и Web/SSR/email/XLSX semantic outputs, а также bundled-font/compiler/renderer build rotation fixtures.

## 23. Производительность и масштабирование

Стратегия: pushdown, Arrow batches, partitioned Parquet, Polars lazy plans, DuckDB pruning, incremental partition rebuild, typed queues и workspace/run resource policies. Очереди разделены на metadata, data I/O, data compute, ML, export и reports с соответствующей concurrency. Backend следует `vectorized/native-engine first`: pushdown → Arrow → Polars/DuckDB для tabular → NumPy/SciPy для dense numerical kernels → measured Numba/JIT; production-size Python row loops требуют benchmark-обоснования.

Начальные profiles: small 1–2 GB/10 min/1 core, medium 2–8 GB/60 min/2–4 cores, large 8–32 GB/240 min/all available within policy с admin approval. Это policies, не гарантии.

До отдельного будущего decision compute работает только на CPU. Detector учитывает host logical cores, process affinity, cpuset и cgroup quota; default cap равен всем container-visible cores, а Installation Administrator может только уменьшить его. Scheduler выдаёт allocation с учётом memory/workspace/concurrent runs и синхронно ограничивает Polars, DuckDB, CatBoost, BLAS/OpenMP, joblib и child processes.

| ID | CPU/compute invariant |
|---|---|
| COMPUTE-001 | Alpha/MVP/v1 compute CPU-only; GPU/CUDA требует будущего blueprint/ADR |
| COMPUTE-002 | Detector учитывает host/affinity/cpuset/cgroup и возвращает минимум один safe core |
| COMPUTE-003 | No admin cap = all container-visible cores; cap только уменьшает detected capacity |
| COMPUTE-004 | Scheduler учитывает memory/quotas/active allocations и не oversubscribe молча |
| COMPUTE-005 | Один allocation ограничивает Polars/DuckDB/CatBoost/BLAS/OpenMP/joblib pools |
| COMPUTE-006 | Manifest хранит detected/effective/allocated cores, policy/backend/library/thread evidence |
| COMPUTE-007 | Tabular: pushdown/Arrow/Polars/DuckDB; dense kernels: NumPy/SciPy; row loops measured |
| COMPUTE-008 | Numba/JIT/SIMD/fastmath только после baseline/profile с correctness/tolerance/fallback |
| COMPUTE-009 | Admin UI показывает evidence/cap/allocations/saturation и отклоняет invalid cap |
| COMPUTE-010 | CPU policy versioned; thread-sensitive reductions входят в identity либо tolerance policy |

Benchmark до stable release использует минимум 500k customers, 10m receipts, 50m items, 100k products, 1k stores и 36 months. Измеряются extraction, incremental day, feature mart, RFM, quantile/IQR/MAD treatment, bucket/stratified aggregation, exact-K KMeans fit/profile/assignment с/без treatment, cohorts, basket pairs, forecast backtest, ChartSpec validation/compile, bounded chart data, SSR SVG batch, SVG→PNG, range timeline, dense SVG/Canvas smoke, peak RSS/temp/output и artifact size. SLO ставятся после реального baseline.

До v1 поддерживается один server: web/API, PostgreSQL, Valkey, local artifact volume, scheduler/orchestrator/outbox/reconciler, несколько local data worker processes, low-concurrency ML worker и bounded report worker. Multi-host/Kubernetes ждут отдельный distributed storage/execution ADR.

| ID | Scaling invariant |
|---|---|
| SCALE-001 | Concurrency ограничивается expected memory и quotas, не только CPU |
| SCALE-002 | Source connection имеет per-connection limit/backpressure |
| SCALE-003 | Local workers используют один canonical artifact root и supported atomic filesystem semantics |
| SCALE-004 | Deployment отклоняет remote worker до future distributed ADR |

## 24. Развёртывание

Production Docker Compose включает web, API, scheduler, orchestrator, outbox dispatcher, reconciler, data/ML/report workers, migration job, PostgreSQL, Valkey и infrastructure Edge/proxy. API/reconciler/workers используют общий artifact volume; master key и mail credentials поступают как file secret; наружу публикуется только Edge, PostgreSQL/Valkey остаются internal, а report worker имеет bounded outbound mail egress.

Edge — минимальный инфраструктурный адаптер входа, а не новый микросервис продукта. Он не получает secrets, состояние или бизнес-логику, работает с read-only runtime и проксирует только на зафиксированный Web upstream. Путь разделён на две сети: `edge_to_web` соединяет только Edge и Web, `web_to_api` — только Web и API. Поэтому Edge не может обратиться к API напрямую на уровне container network; Web остаётся единственным мостом.

При этом Docker Compose не умеет портативно выразить сеть «host может войти, но публикующий контейнер совсем не может выйти» для всех engines, включая Docker Desktop. Невнутренняя transport network Edge может дать ему ambient outbound route. Fixed upstream ограничивает поведение proxy, но не заменяет firewall. Поэтому Foundation честно доказывает сегментацию и отсутствие произвольного outbound у Web/API, но не называет Edge полностью лишённым egress.

Строгая production-граница создаётся отдельным hardening этапом: host firewall, CNI или эквивалентная policy разрешает Edge только нужный host ingress и соединение с Web, запрещает прямой доступ к API/control/data/Internet/private/link-local/metadata и подтверждается положительными и отрицательными runtime probes. До такого evidence production readiness по этой границе не заявляется.

Release Compose задаёт healthchecks, restart policies, non-root users, read-only root FS где возможно, bounded tmpfs/temp, log rotation, CPU/memory limits, volumes, dependency readiness и documented migration command.

Configuration разделяется на non-secret env, secret files/env, workspace runtime policies и versioned semantic/business configuration. ECharts/Node/shared compiler/rasterizer pin-ятся lockfile/image/build digest, разрешённые en/ru fonts поставляются versioned bundle; его hash вместе с compiler/renderer build digests входит в render identity, системные/remote fonts запрещены. Migration выполняется отдельным job, имеет compatibility window либо downtime; artifact schema version независима от PostgreSQL schema.

## 25. Структура репозитория и код

Monorepo содержит apps для API, scheduler, orchestrator, outbox dispatcher, reconciler, workers и web; packages для contracts, domains, execution/artifacts/DQ/analytics/forecast/presentation, единственного `chart_compiler_ts`, notifications/localization/plugin SDK; official plugins, migrations, Compose deploy, architecture/ADR/contracts/user docs и unit/contract/integration/golden/E2E/performance tests.

Public backend methods объявляются через Protocol/ABC; constructors только принимают dependencies и проверяют invariants; composition вместо implementation inheritance; persistence через SQLAlchemy Core repositories; domain не импортирует FastAPI/Celery/drivers; data transforms остаются functions с явными I/O; nondeterminism всегда имеет seed.

## 26. Roadmap: vertical alpha, public MVP и v1 target

Прежний широкий «MVP» теперь называется `v1_target`. До него есть два самостоятельных acceptance stage.

### 26.1. Vertical alpha

Проверяет production-shaped vertical slice на governed CSV/XLSX template: workspace-scoped contracts и first bootstrap, basic local auth/session revoke, Customer/Receipt/Calendar, full snapshot, базовые schema/key/date/reference checks, Sales Overview/active base/RFM, monthly revenue Seasonal Naive против CatBoost rolling backtest, единый guided/pipeline engine, local manifests, outbox/reconciler, bounded internal JSON/Parquet/minimal UI, locale-neutral contracts и структура en/ru catalogs в development Compose.

### 26.2. Public MVP

Добавляет несколько изолированных workspaces; полный local auth с invites/reset/sessions/scoped tokens и OIDC boundary без runtime; organization tree, primary departments, scoped leadership, department data policies и cross-department grants; PostgreSQL/MSSQL/MySQL/ClickHouse и governed CSV/XLSX templates; CustomerIdentity и item/product entities; full/incremental/partition refresh; полный основной DQ gate с remediation/waiver; sales/customer/RFM/cohorts/lifecycle/rule segments; Metric/Methodology Registry, Analysis Case и Research Workspace; основные forecasts с baselines/CatBoost, intervals, registry и monitoring; saved onboarding, guided analysis, Result Trust, template dashboards, object access/comments, BrandProfile/CompanyPack, schedules, Operator Center и in-app notifications; canonical workspace routing/history, system surfaces и unsaved-change guards; полный en/ru, WCAG 2.2 AA; web/CSV/Parquet/bounded internal JSON; production one-server Compose/local filesystem.

### 26.3. V1 target

Завершает Store/Channel/Promotion, append/upsert, drift history/issue workflow, store/channel, basic basket, component discount/cap/PVM, historical migration и Custom Builder; People & Creators с privacy-safe activity projection и ownership handover; governed quantile/IQR/MAD treatment, bucket segments, stratified distributions и CPU KMeans с exact K; metric certification/proxy quality, robustness/representativeness/basic statistical primitives и default MethodologyPack; universal previous-year comparison, searchable filters, NumberFormatSpec/MetricGroupVersion, полный forecast set, Promotion Journal, Data Guide, Research publication, branding/company packs, CPU-only capacity/admin cap, progress/ETA, четыре base themes, canonical ChartSpec, ECharts-only Web SVG/Canvas, range timeline, bounded SSR SVG→PNG, Report Composition, verified-sender/domain-allowlisted user email, production motion/reduced-motion, Help/shortcuts, admin system lifecycle, operational channel management, mature guided/canvas/templates, plugin SDK, full admin, benchmarks/restore/security/license gates, dashboards и notifications. Dash/Plotly core/ECharts-GL/WebGL отсутствуют. Универсальный XLSX report renderer с generated README является последней функциональной частью v1. Product distribution остаётся self-host-only; Yandex Metrica и B2B остаются future-only.

### 26.4. Реализационные phases

1. Foundation: monorepo/contracts/locale-neutral core, workspace DB/auth/RBAC, object access/comments, local artifacts/partition commit, run/outbox/fencing/reconciler, CPU/progress/theme/BrandProfile и canonical ChartSpec/compiler-port foundations, minimal guided shell, observability и Compose.
2. Vertical alpha: governed CSV/XLSX template discovery/mapping, full extraction/DQ/preflight, marts/analytics/RFM, forecast backtest, первый ChartSpec set и ECharts SVG/Canvas adapter, Result Trust и en/ru catalog structure.
3. Data onboarding/security public MVP: PostgreSQL/MSSQL/MySQL/ClickHouse connectors с integration CI, multi-workspace/local auth, organization/access foundation, identity/items/products, Filter Registry, Data Guide/FileImportTemplate, lifecycle/impact, incremental/drift/remediation, canonical routes/history/system surfaces/dirty guards, complete en/ru/WCAG/onboarding.
4. Product analytics public MVP: Metric/Methodology Registry, Analysis Case/Research Workspace, People & Creators/department ownership, marts/cohorts/lifecycle/segments, universal YoY, metric grouping/formatting, Promotion Journal first-class range timeline/overlays, forecast monitoring, dashboards/comments/schedules/Operator/in-app inbox, BrandProfile/CompanyPack, exports, backup/restore и production Compose.
5. Advanced low-code v1: accessible canvas, templates, Research publication, Custom Builder, governed outlier treatment, buckets/stratification/KMeans, basket/store/channel, component discount/cap/PVM, metric certification/proxy/robustness/representativeness, operational email/webhook и channel management, Report Composition, bounded embedded ECharts SSR→PNG, HTML/user report email, production motion, Help/shortcuts, admin lifecycle, plugin SDK и admin/diff UX.
6. Pre-XLSX hardening: analytics/treatment/segmentation/chart/report/CPU/email benchmarks, invalid ChartSpec security, cross-render/four-theme parity, restore/upgrades, a11y/i18n, mail canary/runbooks, MSSQL matrix, SBOM/provenance и документация.
7. Universal XLSX: последняя feature — canonical ChartSpec→native chart либо same-pipeline PNG, typed data sheet, sheet split, injection/openability/golden parity.
8. Final v1 acceptance: только full acceptance/security/performance/recovery/rollback evidence, без новых features.

Post-v1 остаются Yandex Metrica Reporting/Logs connectors, B2B sales ontology, DB destination export, OIDC/Keycloak implementation, Gaussian Mixture/HDBSCAN/automatic K/Isolation Forest/multivariate anomaly detection, DiD/event study/matching/synthetic control, causal ML/HTE, uplift, generic propensity/churn, advanced channel-migration economics и automated decision analysis, расширенный ABC/XYZ, comparable stores, hierarchical/scenario/decomposed forecasting, Optuna/MLflow, Vault/KMS, новые connectors, remote storage/distributed workers по будущему ADR и public result API. Detailed activation/distribution work ведётся только в отдельном private access-controlled контуре.

## 27. End-to-end сценарии

### 27.1. Первый запуск

One-time host token создаёт local installation admin и первый workspace. Пользователь выбирает language, format locale и timezone, при желании загружает demo dataset, а saved checklist приводит его в Overview с явным следующим шагом.

### 27.2. Основной demo flow

PostgreSQL/MSSQL/MySQL/ClickHouse либо governed CSV/XLSX template → catalog → Customer/Receipt/ReceiptItem mapping → schema/cardinality validation → landing Parquet → quality gate → approved metrics/method → Analysis Case/Research Workspace → transaction/features marts → active base/RFM → PopulationTreatment preview → bucket/stratified analysis либо KMeans exact K → immutable membership/diagnostics → cohorts/online-offline → previous-year comparison с shared treatment bounds → DiscountPolicy/component reconciliation → stacking/cap/PVM → reviewed findings → Promotion range timeline/overlay → forecast → canonical ChartSpec → ECharts Web SVG/Canvas → branded ReportSnapshot → comments/ACL → SSR SVG→email PNG → dashboard, Parquet и native/raster universal XLSX с generated README.

### 27.3. Incremental refresh

Scheduler claims due row и одной transaction создаёт run/outbox. Extraction читает lookback, пересобирает affected partitions, выполняет quality, invalidates dependent cache, перестраивает marts/analyses, сверяет forecast с actual и публикует новый immutable result.

### 27.4. Degraded dataset

Receipt без customer ID допускается в mapping, но Capability Engine блокирует customer analytics и сохраняет доступность sales/store/basket с явным объяснением.

### 27.5. DQ remediation

Critical rule → redacted sample/affected capabilities → fix либо scoped expiring waiver → authorized approval/audit → rerun тем же engine → сравнение report и пересчёт readiness/capabilities.

### 27.6. Forecast и operator lifecycle

Forecast проходит history/preflight, series preview, rolling comparison, manual champion, scheduled prediction/monitoring, degradation notification, retrain/compare и explicit promote/rollback. При expired worker lease Reconciler invalidates stale token; Operator сравнивает attempts, делает node retry/full rerun, проверяет artifacts/cleanup и acknowledges notification с audit reason.

## 28. Критерии приёмки public MVP

| ID | Public MVP считается готовым, когда… |
|---|---|
| AC-001 | PostgreSQL, MSSQL, MySQL/MariaDB и ClickHouse read-only sources, а также governed CSV/XLSX templates, доступны из Web UI |
| AC-002 | Semantic dataset создаётся и публикуется без code changes |
| AC-003 | Capability Engine объясняет доступность функций |
| AC-004 | Full/incremental создают extraction batch/partition manifests, watermark двигается после atomic commit |
| AC-005 | Removed mapped field блокирует run stable error |
| AC-006 | Critical DQ блокирует trusted analytics |
| AC-007 | Sales/customer/RFM/cohort/lifecycle используют один MetricRegistry |
| AC-008 | Results содержат as-of, lineage и code version |
| AC-009 | CatBoost сравнивается минимум с Seasonal Naive и statistical baseline |
| AC-010 | Backtest не использует future features |
| AC-011 | Queued/running run отменяется |
| AC-012 | Retry не дублирует successful artifact |
| AC-013 | Roles ограничивают PII preview/export |
| AC-014 | Clean-server Compose install проверен |
| AC-015 | PostgreSQL/artifacts backup успешно restore в test env |
| AC-016 | Golden metrics стабильны после clean install |
| AC-017 | One-time bootstrap создаёт первого admin/workspace и отключается |
| AC-018 | Два workspaces изолированы во всех metadata/data/operational surfaces |
| AC-019 | Local auth имеет invites/change-reset/rotating sessions/revoke-all/scoped tokens/CSRF |
| AC-020 | OIDC boundary contract-tested без OIDC runtime dependency |
| AC-021 | Source IDs/SCD joins проходят collision/overlap tests |
| AC-022 | Distinct/semi-additive/ratio и multi-currency aggregation применяют registered rules |
| AC-023 | Outbox/reconciler восстанавливает state-delivery crash, stale fence не публикует |
| AC-024 | DQ issue ведёт к source fix/waiver и rerun тем же engine |
| AC-025 | Guided и equivalent pipeline используют один normalized spec/engine/result |
| AC-026 | Dashboard version хранит layout/widgets/filters/access/bindings и не расширяет permissions |
| AC-027 | Inbox доставляет, дедуплицирует, локализует и acknowledges operational events |
| AC-028 | English default/fallback, en/ru 100%, switch без relogin |
| AC-029 | Core en/ru journeys WCAG AA и keyboard-operable, включая drag alternative |
| AC-030 | Operator Center показывает attempts/workers/queues/outbox/reconciler и audited recovery |
| AC-031 | Collections bounded, drafts ETag, side effects idempotent, long commands 202 |
| AC-032 | Есть CSV/Parquet/bounded internal JSON, нет DB write/public result API |
| AC-033 | Активен только local filesystem, remote workers rejected |
| AC-034 | Release Compose содержит все control/worker/storage/infrastructure Edge/migration components, разделяет `Edge → Web` и `Web → API` без прямой Edge→API adjacency, а production promotion имеет отдельное firewall/CNI hardening evidence |
| AC-035 | Real MSSQL matrix — protected release check |
| AC-036 | Cancel завершает child/DB statement и не публикует partial artifact |
| AC-037 | Run/node/schedule APIs отклоняют invalid transitions, не переписывают terminal attempts и показывают schedule lifecycle отдельно от health |
| AC-038 | Forecast spec проходит общий version lifecycle; backtest/model FK указывает immutable spec version того же workspace |
| AC-039 | Customer marts/segments используют canonical customer и явные PK; product revenue использует item-grain metric без размножения header measures |
| AC-040 | Public MVP активирует только in-app delivery; email/webhook endpoints и adapters выключены до `v1_target` |
| AC-041 | Workspace Administrator управляет membership/roles/report-dashboard access/connections, но без дополнительной роли не создаёт analytical content и не получает PII; Analyst не управляет connections/access assignments |
| AC-042 | Viewer читает только granted snapshots, не получает raw PII и создаёт audited sanitized comment без изменения immutable content |
| AC-043 | Methodology Registry публикует reviewed immutable method, а run/result pin-ит method либо limitation `unregistered_method` |
| AC-044 | Research Workspace создаёт reproducible outline/metric/chart/table/finding/conclusion document и публикует его через общий ReportSnapshot path |
| AC-045 | Installation BrandProfile/CompanyPack проходят asset/contrast/compatibility checks и меняют identity без fork, secrets или изменения аналитических значений |

### 28.1. Критерии приёмки v1 target для отчётной платформы

| ID | V1 считается готовым, когда… |
|---|---|
| V1-AC-001 | Все reportable analytics/forecast/dashboard/DQ принимают explicit YoY spec либо объясняют blocker |
| V1-AC-002 | Filter search находит разрешённые fields, typed expressions и не раскрывает denied facets/counts |
| V1-AC-003 | Promotion Journal versioned, multi-window/channel, pinned audiences и timeline overlay без causal claim |
| V1-AC-004 | Markdown Data Guide безопасно versioned/rendered и review-required после dataset drift |
| V1-AC-005 | CPU detector/cap/allocation использует all container-visible default и предотвращает thread oversubscription |
| V1-AC-006 | Все user-observable compute показывают accessible loading; async дополнительно имеет progress/indeterminate/ETA/reconnect/cancel |
| V1-AC-007 | Six themes работают в core journeys; graphite UI/paper reports, WCAG/chart-table gates зелёные |
| V1-AC-008 | Web/email одного snapshot имеют одинаковые ChartSpec/chart-data/filters/comparison/metrics/lineage; email HTML+text+SSR-derived PNG accessible |
| V1-AC-009 | Email только verified transport-authorized user From и allowed domains с PII/audit checks |
| V1-AC-010 | Restart ready/submit восстанавливает encrypted recipients; unknown result reconciles по persisted adapter handle без blind retry |
| V1-AC-011 | XLSX содержит обязательные sheets и lossless native либо same-pipeline PNG charts с data; no truncation, safe split, openable |
| V1-AC-012 | Golden fixtures доказывают ChartSpec/totals/filter/comparison/lineage parity Web SVG/Canvas, email PNG и XLSX native/raster |
| V1-AC-013 | Dependency/runtime graph: только ECharts Web; нет Dash/Plotly core/ECharts-GL/WebGL/browser analytics |
| V1-AC-014 | ChartSpec проходит security validation; range timeline воспроизводит planned/actual/channels/audiences/overlap/window/table |
| V1-AC-015 | Bounded networkless SSR SVG→PNG соблюдает limits/cancel и не публикует partial artifacts после failure/crash |
| V1-AC-016 | Каждый reportable chart/table/range timeline имеет accessible Focus / Explore с title/period/vs LY, полным filter context, search, Apply/Reset/Undo, controls, trust/export и return-to-origin; identity boundaries проверены |
| V1-AC-017 | Canonical route registry, immutable workspaceKey, guards, safe query, deep links, Back/Forward, workspace switch, dirty guard и route-backed Focus проходят en/ru E2E без metadata leaks |
| V1-AC-018 | Motion matrix соблюдает durations/easing, сохраняет shell/previous data, не искажает charts/tables и имеет проверенный reduced-motion вариант |
| V1-AC-019 | 403/404/session/maintenance/upgrade, Help/shortcuts, admin lifecycle и operational channels имеют accessible permission-aware states, safe actions, redaction и audit evidence |
| V1-AC-020 | NumberFormatSpec одинаков в Web/email/XLSX, locale-aware сокращает числа и не превращает non-zero percent в 0%, сохраняя full typed value |
| V1-AC-021 | MetricGroupVersion сохраняет одинаковые group headers/order и accessible reading order во всех каналах |
| V1-AC-022 | XLSX README содержит safe sources, filters, metrics/groups, methodology, grain, quality, limitations, lineage и versions без secrets/PII |
| V1-AC-023 | Research document поддерживает summary→detail, linked filters, evidence-linked findings и отдельные viewer comments с immutable version |
| V1-AC-024 | Report/dashboard ACL управляется отдельно от authoring; revoke закрывает object, exports и comments без existence leak |
| V1-AC-025 | BrandProfile из одной pinned version кастомизирует Web/login/email/report/XLSX/docs/support и проходит visual/accessibility tests |
| V1-AC-026 | PostgreSQL/MSSQL/MySQL/ClickHouse/CSV-template/XLSX-template имеют release evidence; Yandex Metrica future-only |
| V1-AC-027 | Public release не содержит private activation artifacts и работает self-host без private package/license heartbeat |
| V1-AC-028 | Canonical model остаётся B2C retail; B2B entities отсутствуют и не переиспользуют существующие semantics |
| V1-AC-029 | Quantile/IQR/MAD treatment имеет default flag, sensitivity, explicit exclude/winsorize и раскрывает bounds/scope/impact во всех result/export channels без изменения canonical data |
| V1-AC-030 | Buckets поддерживают quantile/equal-width/custom с deterministic boundaries; strata используют global default/privacy-safe cells и сохраняются в segment только явно |
| V1-AC-031 | CPU KMeans принимает exact K и versioned features/preprocessing/treatment/seed, показывает diagnostics/sensitivity и создаёт новый immutable snapshot при retrain |
| V1-AC-032 | Promo/loyalty/bonus/other, commercial discount, customer benefit и recognized net revenue разделены и reconciliation-сведены без unknown-as-zero/accrual confusion |
| V1-AC-033 | Versioned stacking/precedence/cap/base/tolerance/returns сохраняет historical breaches, блокирует simulated breaches и остаётся configurable через CompanyPack |
| V1-AC-034 | UI-AN-010 показывает component rates/shares/penetration/overlap/depth/cap и vs LY через ratio-of-sums и stable groups/formats |
| V1-AC-035 | PVM точно сводит price/volume/mix/assortment/residual и раскрывает method/coverage/new-discontinued/missing/UOM/currency/returns |
| V1-AC-036 | Metric certification/proxy quality/representativeness/robustness/basic statistics/MethodologyPack доступны в v1, advanced methods остаются future-only |
| V1-AC-037 | Versioned company/division/department/team tree и один primary department имеют effective-dated transfer/merge lifecycle |
| V1-AC-038 | Organization-aware authorization не раскрывает hidden rows/counts и пересекает все policy ceilings |
| V1-AC-039 | Department Leader scoped к unit/subtree и не делегирует выше своего ceiling |
| V1-AC-040 | Cross-department grant bounded/reasoned/expiring, не меняет primary department и ceilings |
| V1-AC-041 | Ownership/creator/transfer/legacy migration deterministic и сохраняют историю |
| V1-AC-042 | People & Creators показывает privacy-safe assets/activity без ranking, score или raw audit |
| V1-AC-043 | Шесть Organization/People routes, effective-access states, C25 и flow 10 проходят design/runtime gates |

## 29. Закрытые пробелы исходного плана

| ID | Что было не определено | Чем закрыто |
|---|---|---|
| GAP-001 | Identity mapping | Versioned CustomerIdentity |
| GAP-002 | Grain | Grain/PK всех entities/marts |
| GAP-003 | Returns/cancellations | Semantic policies |
| GAP-004 | Currency/timezone | Canonical rules |
| GAP-005 | Late data/deletes | Lookback/delete policy |
| GAP-006 | Schema drift | Drift gate |
| GAP-007 | Единые метрики | MetricRegistry |
| GAP-008 | Immutable history | Manifests/snapshots |
| GAP-009 | DQ gate | Severity/threshold/action |
| GAP-010 | DAG state machine | Formal states |
| GAP-011 | Idempotency/cache | Content/policy-scoped keys |
| GAP-012 | PII/security | RBAC/classification/audit |
| GAP-013 | Forecast validation | Specification/rolling backtest |
| GAP-014 | Forecast monitoring | Actual-vs-forecast |
| GAP-015 | Incomplete period | Complete-period rule |
| GAP-016 | Hierarchy consistency | v1 warning, post-v1 reconciliation |
| GAP-017 | Backup/restore | Backup manifest/drill |
| GAP-018 | Licenses | SPDX/SBOM |
| GAP-019 | Performance limits | Reproducible benchmark |
| GAP-020 | Canvas-first risk | Guided-first |
| GAP-021 | User journeys/recovery | Saved onboarding, remediation, Operator Center |
| GAP-022 | Смешанные statuses | Separate lifecycle/readiness/execution |
| GAP-023 | Weak SCD/source keys | Version keys/namespaces |
| GAP-024 | Metric kinds | Aggregation constraints |
| GAP-025 | Silent multi-currency | FX/group blocker |
| GAP-026 | DB/queue race | Outbox/fencing/reconciler |
| GAP-027 | Multi-table snapshot boundary | Extraction session/batch и atomic watermark |
| GAP-028 | Artifact taxonomy/schema | Category/schema/version/partition manifest |
| GAP-029 | Header/item double count | Separate facts/planner |
| GAP-030 | DQ remediation | Issues/owner/rerun/waiver |
| GAP-031 | Dashboard reproducibility | DashboardVersion |
| GAP-032 | API consistency | Pagination/concurrency/idempotency contracts |
| GAP-033 | Auth lifecycle | Bootstrap/invites/reset/rotation/revoke/CSRF/tokens |
| GAP-034 | i18n | en/ru catalogs, locale-neutral core, Babel/gettext |
| GAP-035 | Accessibility | WCAG 2.2 AA |
| GAP-036 | Operational awareness | Notification event/delivery model |
| GAP-037 | Module-specific comparison | Universal TimeComparisonSpec/compatibility |
| GAP-038 | Promotion only optional dimension | Versioned journal/immutable audiences |
| GAP-039 | Нет searchable filter registry | Typed registry/expression tree |
| GAP-040 | Web/email/export могли расходиться | Report Composition/ReportSnapshot |
| GAP-041 | Нет user report-email contract | Verified sender/domain/DLP/unknown reconciliation |
| GAP-042 | Нет universal XLSX contract | Renderer/workbook/openability gates |
| GAP-043 | Нет управляемого Data Guide | Versioned sanitized template |
| GAP-044 | CPU/thread pools не координировались | Container detector/admin cap/allocation |
| GAP-045 | Progress без schema/ETA | Versioned event/confidence/reconnect |
| GAP-046 | Нет theme contract | Six semantic profiles/parity gates |
| GAP-047 | Raw ECharts option был canonical | Product-owned validated ChartSpec; library outputs derived only |
| GAP-048 | Web/static/XLSX renderer boundaries не разделены | ECharts Web, bounded SSR SVG→PNG и native-or-same-PNG XLSX ports |
| GAP-049 | Promotion timeline не имел chart type | First-class range_timeline и accessible table |
| GAP-050 | Форматирование метрик было компонентным | NumberFormatSpec, adaptive precision и full typed value |
| GAP-051 | Группы и порядок метрик дрейфовали | MetricGroupVersion и versioned presentation override |
| GAP-052 | У аналитиков не было общего реестра методик | MethodologyRegistry, review и immutable methods |
| GAP-053 | Ad hoc не становился reusable asset | AnalysisCase, ResearchDocument, Finding и AnalyticalProduct |
| GAP-054 | Dashboard не поддерживал research narrative | Ordered sections, heterogeneous blocks, findings и comments |
| GAP-055 | White-label ограничивался palette | BrandProfileVersion и CompanyPack без code fork |
| GAP-056 | XLSX README был неопределён | Автоматический structured README из snapshot/guide/method |
| GAP-057 | Admin/Analyst/Viewer permissions пересекались | Separate bundles, object ACL и explicit PII grant |
| GAP-058 | Connector scope был размытым | Четыре SQL + два governed template modes, Yandex future-only |
| GAP-059 | Distribution смешивалась с activation | Self-host-only public core и отдельная private boundary |
| GAP-060 | Выбросы были локальными filters | Immutable treatment, robust methods, default flag, shared LY bounds и sensitivity |
| GAP-061 | Buckets/strata/clusters не имели lifecycle | Versioned definitions/distributions/preprocessing/models/membership и exact K |
| GAP-062 | Общая скидка смешивала promo/loyalty/bonus и cap | Component fact, DiscountPolicyVersion, attribution и reconciliation |
| GAP-063 | PVM/proxy/method readiness не имели доказательного контракта | Versioned PVM, certification, proxy quality, MethodologyPack и availability class |
| GAP-064 | Роли не отражали структуру компании | Separate roles, OrgUnit tree и scoped leadership |
| GAP-065 | Department access смешивался с object ACL | Data policy intersection и bounded grants |
| GAP-066 | Ресурсы теряли owner при переводе автора | Creator/owner separation и handover lifecycle |
| GAP-067 | Creator showcase мог стать surveillance | Privacy-safe projection и anti-ranking policy |
| GAP-068 | Organization/People не имели UI contract | Six routes, UI-CAP-021/022, C25 и flow 10 |

## 30. Риски и решения

| ID | Риск | Снижение риска |
|---|---|---|
| RISK-001 | Широкий v1 принимают за первый release | Alpha/public MVP/v1 gates |
| RISK-002 | Плохие source schemas/keys | Mapping/drift/DQ/degraded mode |
| RISK-003 | Не хватает RAM одного сервера | Pushdown/partitions/lazy/resource profiles |
| RISK-004 | Canvas съедает frontend effort | Guided-first/limited nodes |
| RISK-005 | CatBoost создаёт ложное качество | Baselines/rolling/bias constraints |
| RISK-006 | MSSQL ODBC сложно устанавливать | Connector extra и release matrix |
| RISK-007 | Plugins ломают core | Versioned contracts/compatibility |
| RISK-008 | PII в logs/exports | Classification/masking/audit/security tests |
| RISK-009 | Local volume переполняется | Quotas/watermarks/retention/orphan cleanup/preflight |
| RISK-010 | en/ru и accessibility расходятся | CI parity/pseudo/dual-locale E2E/WCAG gates |
| RISK-011 | Universal filters/reports создают дорогие scans | Registry/pushdown/preflight/quotas/limits |
| RISK-012 | Promotion overlap принимают за causality | Immutable history/diagnostics/descriptive-only |
| RISK-013 | Email раскрывает PII или spoofed sender | Verified sender/domain/DLP/audit |
| RISK-014 | Unknown provider state даёт duplicate | Idempotency/unknown/reconcile/confirmation |
| RISK-015 | XLSX слишком велик/повреждён | Preflight/split/no truncation/openability |
| RISK-016 | Библиотеки занимают все cores независимо | Central capacity/allocation/thread limits |
| RISK-017 | Web/email/XLSX показывают разные цифры | One snapshot/shared artifacts/golden parity |
| RISK-018 | Library option становится hidden logic/executable attack surface | Allowlisted ChartSpec, no raw options/functions/HTML/URLs/regex |
| RISK-019 | SSR/raster исчерпывает CPU/RAM/temp или зависает | Bounded spec/data, no network, limits/cancel/cleanup/runbook |
| RISK-020 | Большой chart блокирует browser или даёт разные reductions | Backend CPU aggregate/sample/LOD, visible window и measured SVG/Canvas policy |
| RISK-021 | Adaptive formatting скрывает малое значение | Versioned rules, non-zero floor, full-value disclosure и golden boundaries |
| RISK-022 | Comment принимается за утверждённый вывод или раскрывает PII | Separate FindingVersion/comment, review, DLP, access re-check и audit |
| RISK-023 | White-label asset создаёт XSS/remote fetch/плохой contrast или fork | Sanitized content-addressed assets, semantic tokens и preview/gates |
| RISK-024 | Расширенная connector matrix превышает support capacity | Supported-version matrix, protected release jobs и закрытый connector scope |
| RISK-025 | Admin role обходит analytical/PII policy | Separate bundles, explicit expiring PII grant и access audit |
| RISK-026 | `.gitignore` принимают за защиту private материалов | Authoritative private storage отдельно; ignored root — только defense-in-depth |
| RISK-027 | Outlier policy удаляет реальных VIP или делает периоды несопоставимыми | Default flag, DQ separation, impact preview, pinned shared LY bounds и explicit fit/assignment populations |
| RISK-028 | Promo/loyalty/bonus считаются дважды или путаются с accrual | Component fact, accounting treatment, stacking/precedence и reconciliation |
| RISK-029 | Cap молча исправляет или скрывает historical sale | Immutable source, no-clamp diagnostics и simulated-publication block |
| RISK-030 | Residual/total-only показывается как точная attribution | Origin/coverage/certification/Result Trust disclosure |
| RISK-031 | PVM зависит от скрытого порядка и не сходится | Versioned order, exact reconciliation, assortment/residual и golden data |
| RISK-032 | Hierarchy зашивается в roles | Separate functional roles и scoped organization assignments |
| RISK-033 | Cross-department grant превышает ceilings | Central intersection, bounded grant, expiry/revoke tests |
| RISK-034 | Transfer оставляет старый access/orphan resources | Immediate rescope, handover и successor mapping |
| RISK-035 | People & Creators превращается в employee ranking | Redacted aggregates и запрет leaderboard/score |
| RISK-036 | Snapshot read принимают за underlying data access | Authorization каждого action отдельно |
| RISK-037 | Admin configuration обходит privacy | `organization.manage` отделён от activity/content/PII grants |

### 30.1. Зафиксированные решения

| ID | Решение |
|---|---|
| RESOLVED-001 | Название — Custometry |
| RESOLVED-002 | Базовая tenancy — несколько изолированных workspaces в одной инсталляции |
| RESOLVED-003 | Local auth public MVP; provider boundary сразу; OIDC/Keycloak post-v1 |
| RESOLVED-004 | External DB export post-v1 после отдельного ADR |
| RESOLVED-005 | Только local filesystem до v1; remote contract — будущий ADR |
| RESOLVED-006 | English default/fallback, Russian required; i18next frontend, Babel/gettext generated backend text |
| RESOLVED-007 | In-app входит в public MVP; email/webhook входят в следующую версию `v1_target` |
| RESOLVED-008 | Accessibility baseline — WCAG 2.2 AA |
| RESOLVED-009 | PostgreSQL polling/claim scheduler создаёт run/outbox одной transaction |
| RESOLVED-010 | Canonical chart format — product-owned validated ChartSpec; ECharts option только derived output |
| RESOLVED-011 | Promotion clients — canonical customer через all/immutable segment/immutable customer-list, без corporate-organization entity |
| RESOLVED-012 | Report email From — verified transport-authorized user email; иначе block без system fallback |
| RESOLVED-013 | Installation domain allowlist — global ceiling; workspace только сужает; no policy = deny |
| RESOLVED-014 | Reportable scope — analytics, forecasts, dashboards, QualityReport; не Admin/Operator telemetry |
| RESOLVED-015 | XLSX overflow — deterministic sheet split, no silent truncation, hard limit blocks |
| RESOLVED-016 | Graphite — UI default; paper — email/XLSX default; user-selected theme pinned в snapshot/manifest |
| RESOLVED-017 | Apache ECharts — единственный Web chart engine до и включая v1 |
| RESOLVED-018 | Dash исключён из production dependencies/runtime/routing/state/callback architecture |
| RESOLVED-019 | Plotly не core dependency; post-v1 только trusted renderer plugin через ChartSpec contract |
| RESOLVED-020 | Promotion timeline — first-class `range_timeline`, не timeline-frame component |
| RESOLVED-021 | Web SVG/Canvas; email PNG из SSR SVG; XLSX native lossless либо same-pipeline PNG |
| RESOLVED-022 | Нет ECharts-GL/WebGL до v1; analytics/aggregation/sample/LOD — backend CPU |
| RESOLVED-023 | Текущая ontology и v1 ориентированы на B2C retail; B2B sales — future additive extension |
| RESOLVED-024 | v1 sources: PostgreSQL, MSSQL, MySQL/MariaDB, ClickHouse и governed CSV/XLSX templates; Yandex Metrica — future Reporting/Logs boundary |
| RESOLVED-025 | Product distribution сейчас только self-host; cloud/SaaS/managed control plane не входят в v1 |
| RESOLVED-026 | Detailed activation/destination design private и хранится отдельно; `.private/` лишь предотвращает accidental commit |
| RESOLVED-027 | BrandProfile/CompanyPack охватывает Web/login/logo/icons/colors/fonts/email/report/XLSX/docs/support/legal без code fork |
| RESOLVED-028 | Admin управляет users/access/connections; Analyst создаёт content; Viewer читает и комментирует без raw PII |
| RESOLVED-029 | PII доступна только через explicit scoped expiring grant; Viewer/Operator raw PII не получают |
| RESOLVED-030 | Research Workspace — governed block document поверх общих contracts, не notebook или второй dashboard engine |
| RESOLVED-031 | NumberFormatSpec и MetricGroupVersion едины для Web/email/XLSX; raw value сохраняется, non-zero percent не становится 0% |
| RESOLVED-032 | Продукт строится как широкий кастомизируемый minimum product set, не как first-client fork или pilot KPI solution |
| RESOLVED-033 | V1 использует quantile/IQR/MAD и rule/bucket/stratified/KMeans exact-K workflow; GMM/HDBSCAN/automatic-K/multivariate anomalies остаются post-v1 |
| RESOLVED-034 | Promo/loyalty/bonus redemption/other — отдельные components; versioned policy управляет stacking/cap, historical facts не clamp-ятся, simulated breach блокируется |
| RESOLVED-035 | Commercial discount/customer benefit/recognized net revenue разделены; attribution quality обязательна, aggregate rate — ratio-of-sums |
| RESOLVED-036 | V1 включает discount/PVM и методологическое качество; advanced causal/uplift/anomaly/decision methods остаются future_extension |
| RESOLVED-037 | V1 organization — workspace tree company/division/department/team и один active primary department/team |
| RESOLVED-038 | Functional role и hierarchy независимы; Department Leader — scoped assignment |
| RESOLVED-039 | Effective access — policy intersection, deny wins |
| RESOLVED-040 | Cross-department access — bounded reasoned expiring allow grant |
| RESOLVED-041 | Draft personal, publication department-owned, creator immutable, transfer auditable |
| RESOLVED-042 | People & Creators использует redacted projection без raw audit/ranking/score |
| RESOLVED-043 | UI delta — six routes, UI-CAP-021/022, C25 и flow 10 приняты W10 на Penpot revision 213 с inventory 116/25/5 |

Открыты только `OPEN-007` — customer ID completeness threshold как workspace degraded policy, и `OPEN-008` — minimum history для forecast target как capability rule по frequency/seasonality/horizon.

## 31. Первый implementation slice

Vertical alpha берёт governed CSV/XLSX template, Customer/Receipt, guided JSON-backed semantic form, базовые key/date/reference quality rules, transaction mart, Sales Overview/active base/RFM, monthly revenue Seasonal Naive и CatBoost rolling backtest, bounded internal JSON/Parquet, первый canonical ChartSpec set и minimal Web UI через ECharts SVG/Canvas, общий guided/pipeline engine, outbox/fencing/reconciler и local artifacts. После доказанного slice добавляются все четыре SQL connectors, Methodology/Research, incremental, cohorts/lifecycle, governed treatment и bucket/stratified/KMeans segmentation, branding/reporting и полный forecast set. Slice — техническая последовательность, а не ограничение продукта под первого клиента.

## 32. Definition of Done нового модуля

Готовый модуль имеет versioned I/O contracts, owner, capability rule, lifecycle/actions/permissions; не использует hidden global state, фиксирует seed, structured errors, cancellation, workspace/idempotency, CPU/thread allocation и ProgressEvent/ETA для heavy work; объявляет grain/key/PII, manifest/lineage и, когда применимо, treatment bounds, preprocessing/model/seed/membership versions и sensitivity; имеет unit/contract/golden/negative/cross-workspace tests; logs/metrics/timeout/resource profile; guided/node UI, searchable typed filters, previous-year comparison и ReportSnapshot binding когда reportable, canonical ChartSpec/bounded chart data/ECharts renderer capability/textual summary/accessibility table когда visualized, en/ru keys, все четыре themes, keyboard/screen-reader path, все states и нужные notification events; документацию, examples и limitations.

## 33. Основные технологические стандарты

Нормативные ссылки machine-версии охватывают FastAPI, Pydantic, SQLAlchemy, Celery, Valkey, PostgreSQL RLS, Polars, DuckDB, React Flow, Apache ECharts core/Canvas/SVG/SSR/custom-series/security, i18next/react-i18next, Babel, BCP 47, ECMAScript Intl, WCAG 2.2, CatBoost, StatsForecast, Python entry points и OpenTelemetry instrumentation.

## 34. Итоговая формула продукта

```text
Source data
→ semantic mapping
→ quality gate
→ approved metrics and methodologies
→ analysis case and research from overview to detail
→ immutable analytical artifacts
→ reusable marts and metrics
→ customer/sales analytics
→ governed population treatment
→ bucket, stratified or exact-K segmentation
→ reproducible forecasting
→ canonical product-owned ChartSpec
→ ECharts Web SVG/Canvas and deterministic SSR-SVG-to-PNG
→ reviewed findings, comments and versioned report composition
→ BrandProfile and CompanyPack
→ verified-sender email
→ dashboards and native-or-raster universal XLSX with generated README
```

Custometry остаётся B2C retail analytical operating system, а не универсальным оркестратором или customer-specific проектом. Её главные differentiators — semantic model, единые metrics/methodology, research-to-product workflow, Result Trust, white-label без fork, воспроизводимость и корректная временная validation прогнозов.
