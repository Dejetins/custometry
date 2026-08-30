import type { ConnectionStatus, ConnectorId } from "./connections-api";

export type ConnectionLanguage = "en" | "ru";

const copy = {
  en: {
    eyebrow: "Data · connections", title: "Connections", description: "Governed source references, health, ownership, and safe next actions.",
    add: "Add connection", refresh: "Refresh", refreshing: "Refreshing", search: "Search connections", searchPlaceholder: "Name, connector, or owner", status: "Status", owner: "Owner", all: "All", clear: "Clear filters",
    fixture: "Presentation fixture", fixtureNote: "This list demonstrates UI states only; it is not W14 persistence proof.",
    unavailableTitle: "Connection listing is not available in W14", unavailableBody: "The production adapter will not invent a list endpoint. You can create and test a PostgreSQL connection through the real W14 boundary.",
    loading: "Loading connections", emptyTitle: "No connections yet", emptyBody: "Add the first governed source reference for this workspace.", filteredEmptyTitle: "No connections match these filters", filteredEmptyBody: "Clear filters to restore the full authorized view.",
    forbiddenTitle: "Connections are unavailable", forbiddenBody: "Your current session does not have connection.read_metadata.", failedTitle: "Connections could not be loaded", failedBody: "No protected or stale data was substituted. Retry when the dependency is available.", retry: "Retry",
    degradedTitle: "Connection metadata is degraded", staleTitle: "Connection snapshot is stale", safeCredentials: "Secret reference present", noCredentials: "No secret reference", updated: "Updated", open: "Open connection",
    back: "Back to connections", editorTitle: "New connection", editorDescription: "Choose a governed connector and use references only. Never paste a password, DSN, or token.",
    connector: "Connector", displayName: "Display name", profileRef: "Network profile reference", profileHint: "Resolved server-side; host, port, and DSN are not exposed here.", secretRef: "Credential reference", secretHint: "Enter an existing secret identifier, never the secret value.", templateVersion: "Published template version", templateHint: "Required for governed CSV/XLSX intake; file upload is outside this route.",
    saveDraft: "Save draft", testSave: "Save and test", saving: "Saving and testing", draftSaved: "Draft saved in this tab only; the credential reference was not stored. W14 has no persisted draft lifecycle.",
    unsupportedTitle: "Connector is not active at this boundary", unsupportedBody: "Only PostgreSQL create/test is implemented by W14. Template modes retain a local draft; other providers require a later accepted backend slice.",
    permissionTitle: "Read-only connection access", permissionBody: "connection.manage is required to save or test a connection.",
    validationTitle: "Review the highlighted fields", required: "This field is required.", invalidReference: "Use 3–80 lowercase letters, digits, dots, underscores, or hyphens; start with a letter.", unsupported: "This connector cannot be persisted or tested by W14.",
    testReady: "Connection persisted and read-only test passed", redaction: "Credential and network references were not returned by the API.", objects: "catalog objects discovered", driver: "Driver", readOnly: "Read-only enforced", yes: "Yes", no: "No", stableCode: "Stable code", testFailed: "The connection could not be saved or tested safely.",
  },
  ru: {
    eyebrow: "Данные · подключения", title: "Подключения", description: "Управляемые ссылки на источники, состояние, владельцы и безопасные следующие действия.",
    add: "Добавить подключение", refresh: "Обновить", refreshing: "Обновление", search: "Поиск подключений", searchPlaceholder: "Название, коннектор или владелец", status: "Статус", owner: "Владелец", all: "Все", clear: "Сбросить фильтры",
    fixture: "Презентационный fixture", fixtureNote: "Этот список демонстрирует только состояния UI и не доказывает persistence W14.",
    unavailableTitle: "Список подключений недоступен в W14", unavailableBody: "Production adapter не выдумывает list endpoint. Через реальную границу W14 можно создать и проверить PostgreSQL-подключение.",
    loading: "Загружаем подключения", emptyTitle: "Подключений пока нет", emptyBody: "Добавьте первую управляемую ссылку на источник для этого workspace.", filteredEmptyTitle: "Подключения не найдены", filteredEmptyBody: "Сбросьте фильтры, чтобы вернуть полный разрешённый список.",
    forbiddenTitle: "Подключения недоступны", forbiddenBody: "У текущей сессии нет разрешения connection.read_metadata.", failedTitle: "Не удалось загрузить подключения", failedBody: "Защищённые или устаревшие данные не подставлялись. Повторите попытку после восстановления зависимости.", retry: "Повторить",
    degradedTitle: "Метаданные подключений ограничены", staleTitle: "Snapshot подключений устарел", safeCredentials: "Ссылка на секрет задана", noCredentials: "Ссылка на секрет отсутствует", updated: "Обновлено", open: "Открыть подключение",
    back: "К подключениям", editorTitle: "Новое подключение", editorDescription: "Выберите управляемый коннектор и используйте только ссылки. Не вставляйте пароль, DSN или токен.",
    connector: "Коннектор", displayName: "Название", profileRef: "Ссылка на сетевой профиль", profileHint: "Разрешается на сервере; host, port и DSN здесь не раскрываются.", secretRef: "Ссылка на credential", secretHint: "Укажите идентификатор существующего секрета, но не его значение.", templateVersion: "Версия опубликованного шаблона", templateHint: "Обязательна для управляемого CSV/XLSX intake; загрузка файла не входит в этот route.",
    saveDraft: "Сохранить черновик", testSave: "Сохранить и проверить", saving: "Сохраняем и проверяем", draftSaved: "Черновик сохранён только в этой вкладке; ссылка на credential не записана. В W14 нет persisted draft lifecycle.",
    unsupportedTitle: "Коннектор не активен на этой границе", unsupportedBody: "W14 реализует create/test только для PostgreSQL. Template modes сохраняют локальный черновик; другим провайдерам нужен следующий принятый backend slice.",
    permissionTitle: "Доступ только для чтения", permissionBody: "Для сохранения или проверки требуется connection.manage.",
    validationTitle: "Проверьте отмеченные поля", required: "Заполните это поле.", invalidReference: "Используйте 3–80 строчных букв, цифр, точек, подчёркиваний или дефисов; начните с буквы.", unsupported: "W14 не может сохранить или проверить этот коннектор.",
    testReady: "Подключение сохранено, read-only проверка пройдена", redaction: "API не вернул ссылки на credential и сетевой профиль.", objects: "объектов каталога найдено", driver: "Драйвер", readOnly: "Read-only включён", yes: "Да", no: "Нет", stableCode: "Стабильный код", testFailed: "Не удалось безопасно сохранить или проверить подключение.",
  },
} as const;

export function connectionCopy(language: ConnectionLanguage): typeof copy.en { return copy[language] as typeof copy.en; }

const connectors: Record<ConnectionLanguage, Record<ConnectorId, string>> = {
  en: { postgresql: "PostgreSQL", mssql: "Microsoft SQL Server", mysql: "MySQL / MariaDB", clickhouse: "ClickHouse", csv_template: "CSV template", xlsx_template: "XLSX template", yandex_metrica: "Yandex Metrica · future only" },
  ru: { postgresql: "PostgreSQL", mssql: "Microsoft SQL Server", mysql: "MySQL / MariaDB", clickhouse: "ClickHouse", csv_template: "CSV-шаблон", xlsx_template: "XLSX-шаблон", yandex_metrica: "Яндекс Метрика · только future" },
};
const statuses: Record<ConnectionLanguage, Record<ConnectionStatus, string>> = {
  en: { ready: "Ready", refreshing: "Refreshing", degraded: "Degraded", stale: "Stale", failed: "Failed", draft: "Draft" },
  ru: { ready: "Готово", refreshing: "Обновляется", degraded: "Ограничено", stale: "Устарело", failed: "Ошибка", draft: "Черновик" },
};

export const connectorIds: readonly ConnectorId[] = ["postgresql", "mssql", "mysql", "clickhouse", "csv_template", "xlsx_template", "yandex_metrica"];
export const connectionStatuses: readonly ConnectionStatus[] = ["ready", "refreshing", "degraded", "stale", "failed", "draft"];
export function connectorLabel(language: ConnectionLanguage, id: ConnectorId): string { return connectors[language][id]; }
export function connectionStatusLabel(language: ConnectionLanguage, status: ConnectionStatus): string { return statuses[language][status]; }
