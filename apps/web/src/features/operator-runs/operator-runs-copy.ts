import type { AttemptState, QueueFreshness, RetryMode, RunState } from "./operator-runs-api";

export type OperatorRunsLanguage = "en" | "ru";

const copy = {
  en: {
    eyebrow: "Operations · UI-OPS-001", title: "Operator Center",
    description: "Monitor durable execution state, queue pressure, attempts, and permitted recovery actions.",
    refresh: "Refresh", refreshing: "Refreshing", autoRefresh: "Auto-refresh every 5 seconds",
    filters: "Run filters", state: "State", kind: "Execution kind", trace: "Trace identity",
    all: "All", anyKind: "Any kind", tracePlaceholder: "Exact safe trace ID", clear: "Clear filters",
    visible: "visible runs", queued: "queued", running: "running", failed: "failed",
    oldest: "oldest queued", seconds: "seconds", observed: "Observed", lanes: "Queue lanes",
    loading: "Loading operator runs", emptyTitle: "No runs match this view",
    emptyBody: "Try clearing filters or wait for a permitted run to enter the workspace queue.",
    forbiddenTitle: "Operator Center is unavailable",
    forbiddenBody: "Your current policy does not grant run.read for this workspace.",
    failedTitle: "Runs could not be loaded", failedBody: "Execution Control did not return a safe response. Retry the request.",
    retryLoad: "Retry loading", staleTitle: "Queue summary is stale", staleBody: "Run state remains durable, but queue timing may be delayed.",
    degradedTitle: "Queue summary is degraded", degradedBody: "Durable run state is shown; queue projection precision is unavailable.",
    refreshDegradedTitle: "Refresh failed", refreshDegradedBody: "Previously loaded durable state remains visible and may now be stale.",
    details: "Inspect run", detailsTitle: "Run and attempt ancestry", close: "Close run details",
    runId: "Run ID", owner: "Owner", lane: "Lane", created: "Created", updated: "Updated",
    retryOfRun: "Retry of run", retryMode: "Retry mode", noAncestor: "Original run",
    attempt: "Attempt", attemptId: "Attempt ID", retryOfAttempt: "Retry of attempt", fencing: "Fencing token",
    lease: "Lease expires", noLease: "No active lease", failure: "Failure", remediation: "Safe remediation",
    resourceFailure: "The attempt exceeded an enforced resource limit.", observedLimit: "Observed limit", configuredLimit: "Configured limit",
    noFailure: "No bounded failure code", actionReason: "Audit reason", actionReasonHint: "3–500 characters; stored with the durable transition.",
    actionReasonPlaceholder: "Reason for this operator action", cancel: "Cancel run", retry: "Retry run",
    mode: "Retry scope", failedNodes: "Failed nodes", fullRerun: "Full rerun", actionWorking: "Applying durable action",
    cancelled: "Cancellation requested; state is CANCELLING until cleanup completes.",
    retried: "Retry created a new run with ancestry.", actionForbidden: "This action is not permitted by the current policy.",
    actionConflict: "The run changed before the action. Fresh durable state has been loaded.",
    actionFailed: "The action failed without claiming a state transition.", reasonRequired: "Enter an audit reason of at least 3 characters.",
    cannotCancel: "Cancellation is unavailable for this state.", cannotRetry: "Retry is available only for failed, cancelled, or partial runs.",
    permissionCancel: "The current policy does not grant run.cancel.", permissionRetry: "The current policy does not grant run.retry.",
    traceUnavailable: "No safe trace identity", autoRefreshed: "Operator runs refreshed automatically.",
  },
  ru: {
    eyebrow: "Операции · UI-OPS-001", title: "Центр оператора",
    description: "Контроль сохранённого состояния запусков, очереди, попыток и разрешённых действий восстановления.",
    refresh: "Обновить", refreshing: "Обновление", autoRefresh: "Автообновление каждые 5 секунд",
    filters: "Фильтры запусков", state: "Состояние", kind: "Тип выполнения", trace: "Идентификатор трассировки",
    all: "Все", anyKind: "Любой тип", tracePlaceholder: "Точный безопасный trace ID", clear: "Сбросить фильтры",
    visible: "видимых запусков", queued: "в очереди", running: "выполняются", failed: "с ошибкой",
    oldest: "старейший в очереди", seconds: "сек.", observed: "Наблюдение", lanes: "Линии очереди",
    loading: "Загрузка запусков", emptyTitle: "Нет запусков для выбранного представления",
    emptyBody: "Сбросьте фильтры или дождитесь доступного запуска в очереди workspace.",
    forbiddenTitle: "Центр оператора недоступен", forbiddenBody: "Текущая политика не предоставляет run.read в этом workspace.",
    failedTitle: "Не удалось загрузить запуски", failedBody: "Execution Control не вернул безопасный ответ. Повторите запрос.",
    retryLoad: "Повторить загрузку", staleTitle: "Сводка очереди устарела", staleBody: "Состояние запусков остаётся сохранённым, но время очереди может запаздывать.",
    degradedTitle: "Сводка очереди деградировала", degradedBody: "Сохранённые состояния доступны, но точность проекции очереди недоступна.",
    refreshDegradedTitle: "Обновление не удалось", refreshDegradedBody: "Ранее загруженное состояние остаётся доступным и может быть устаревшим.",
    details: "Открыть запуск", detailsTitle: "Связи запуска и попыток", close: "Закрыть сведения о запуске",
    runId: "ID запуска", owner: "Владелец", lane: "Линия", created: "Создан", updated: "Обновлён",
    retryOfRun: "Повтор запуска", retryMode: "Режим повтора", noAncestor: "Исходный запуск",
    attempt: "Попытка", attemptId: "ID попытки", retryOfAttempt: "Повтор попытки", fencing: "Fencing token",
    lease: "Окончание lease", noLease: "Активного lease нет", failure: "Ошибка", remediation: "Безопасная рекомендация",
    resourceFailure: "Попытка превысила установленный лимит ресурсов.", observedLimit: "Наблюдаемый лимит", configuredLimit: "Настроенный лимит",
    noFailure: "Нет ограниченного кода ошибки", actionReason: "Причина для аудита", actionReasonHint: "3–500 символов; сохраняется вместе с переходом состояния.",
    actionReasonPlaceholder: "Причина действия оператора", cancel: "Отменить запуск", retry: "Повторить запуск",
    mode: "Объём повтора", failedNodes: "Только ошибочные узлы", fullRerun: "Полный повтор", actionWorking: "Сохранение действия",
    cancelled: "Отмена запрошена; состояние CANCELLING сохраняется до завершения очистки.",
    retried: "Создан новый запуск со ссылкой на исходный.", actionForbidden: "Действие запрещено текущей политикой.",
    actionConflict: "Запуск изменился до действия. Загружено актуальное сохранённое состояние.",
    actionFailed: "Действие завершилось ошибкой без заявления об изменении состояния.", reasonRequired: "Введите причину для аудита не короче 3 символов.",
    cannotCancel: "Отмена недоступна для этого состояния.", cannotRetry: "Повтор доступен только для запусков с ошибкой, отменённых или частичных.",
    permissionCancel: "Текущая политика не предоставляет run.cancel.", permissionRetry: "Текущая политика не предоставляет run.retry.",
    traceUnavailable: "Безопасный trace ID отсутствует", autoRefreshed: "Запуски обновлены автоматически.",
  },
} as const;

export function operatorRunsCopy(language: OperatorRunsLanguage) { return copy[language]; }

const runLabels: Record<OperatorRunsLanguage, Record<RunState, string>> = {
  en: { CREATED: "Created", VALIDATING: "Validating", QUEUED: "Queued", RUNNING: "Running", CANCELLING: "Cancelling", SUCCEEDED: "Succeeded", FAILED: "Failed", CANCELLED: "Cancelled", PARTIAL: "Partial" },
  ru: { CREATED: "Создан", VALIDATING: "Проверяется", QUEUED: "В очереди", RUNNING: "Выполняется", CANCELLING: "Отменяется", SUCCEEDED: "Успешно", FAILED: "Ошибка", CANCELLED: "Отменён", PARTIAL: "Частично" },
};
const attemptLabels: Record<OperatorRunsLanguage, Record<AttemptState, string>> = {
  en: { PENDING: "Pending", READY: "Ready", RUNNING: "Running", RETRY_WAIT: "Retry wait", SUCCEEDED: "Succeeded", FAILED: "Failed", CANCELLED: "Cancelled" },
  ru: { PENDING: "Ожидает", READY: "Готова", RUNNING: "Выполняется", RETRY_WAIT: "Ожидает повтора", SUCCEEDED: "Успешно", FAILED: "Ошибка", CANCELLED: "Отменена" },
};
export function runStateLabel(language: OperatorRunsLanguage, state: RunState) { return runLabels[language][state]; }
export function attemptStateLabel(language: OperatorRunsLanguage, state: AttemptState) { return attemptLabels[language][state]; }
export function retryModeLabel(language: OperatorRunsLanguage, mode: RetryMode) {
  return mode === "failed_nodes" ? copy[language].failedNodes : copy[language].fullRerun;
}
export function freshnessLabel(language: OperatorRunsLanguage, freshness: QueueFreshness) {
  const labels = { en: { fresh: "Fresh", stale: "Stale", degraded: "Degraded" }, ru: { fresh: "Актуально", stale: "Устарело", degraded: "Деградация" } } as const;
  return labels[language][freshness];
}
