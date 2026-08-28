import type {
  NotificationCategory,
  NotificationItem,
  NotificationSeverity,
} from "./notification-api";

export type NotificationLanguage = "en" | "ru";

const copy = {
  en: {
    eyebrow: "Operations",
    title: "Notification Inbox",
    description: "Permission-filtered operational events across your active workspaces.",
    refresh: "Refresh",
    refreshing: "Refreshing notifications",
    filters: "Notification filters",
    severity: "Severity",
    category: "Category",
    read: "Read state",
    acknowledged: "Acknowledgement",
    resolved: "Resolution",
    all: "All",
    yes: "Yes",
    no: "No",
    unread: "Unread",
    readValue: "Read",
    loading: "Loading notifications",
    emptyTitle: "No notifications match this view",
    emptyBody: "Clear filters or refresh to check for new operational events.",
    clearFilters: "Clear filters",
    forbiddenTitle: "Notification inbox is unavailable",
    forbiddenBody: "Your current session does not have notification.read.",
    failedTitle: "Notifications could not be loaded",
    failedBody: "The previous data was not replaced. Retry when the dependency is available.",
    retry: "Retry",
    degradedTitle: "Some notification data may be delayed",
    degradedBody: "Stale or degraded items remain visible with their freshness status.",
    visible: "visible",
    unreadCount: "unread",
    groupEvents: "events in group",
    details: "View details",
    close: "Close details",
    detailsTitle: "Notification details",
    source: "Source",
    occurred: "Occurred",
    freshness: "Freshness",
    trace: "Trace ID",
    stableCode: "Stable code",
    deepLink: "Open related run",
    deepLinkUnavailable: "The related resource link is unavailable or cannot be resolved safely.",
    markRead: "Mark as read",
    dismiss: "Dismiss",
    acknowledge: "Acknowledge",
    acknowledgementUnavailable: "Acknowledgement requires notification.acknowledge.",
    actionWorking: "Updating notification",
    actionRead: "Notification marked as read.",
    actionDismissed: "Notification dismissed.",
    actionAcknowledged: "Notification acknowledged.",
    actionForbidden: "The action is no longer permitted. Data was refreshed.",
    actionFailed: "The notification could not be updated. Refresh and try again.",
    statusResolved: "Resolved",
    statusAcknowledged: "Acknowledged",
    statusDismissed: "Dismissed",
  },
  ru: {
    eyebrow: "Операции",
    title: "Центр уведомлений",
    description: "Операционные события из доступных рабочих пространств с проверкой прав.",
    refresh: "Обновить",
    refreshing: "Уведомления обновляются",
    filters: "Фильтры уведомлений",
    severity: "Важность",
    category: "Категория",
    read: "Прочитано",
    acknowledged: "Подтверждено",
    resolved: "Разрешено",
    all: "Все",
    yes: "Да",
    no: "Нет",
    unread: "Не прочитано",
    readValue: "Прочитано",
    loading: "Уведомления загружаются",
    emptyTitle: "В этом представлении нет уведомлений",
    emptyBody: "Сбросьте фильтры или обновите список, чтобы проверить новые события.",
    clearFilters: "Сбросить фильтры",
    forbiddenTitle: "Центр уведомлений недоступен",
    forbiddenBody: "У текущей сессии нет разрешения notification.read.",
    failedTitle: "Не удалось загрузить уведомления",
    failedBody: "Предыдущие данные не заменены. Повторите попытку, когда сервис станет доступен.",
    retry: "Повторить",
    degradedTitle: "Часть уведомлений может поступать с задержкой",
    degradedBody: "Устаревшие и ограниченные данные остаются видимыми с отметкой свежести.",
    visible: "доступно",
    unreadCount: "не прочитано",
    groupEvents: "событий в группе",
    details: "Открыть подробности",
    close: "Закрыть подробности",
    detailsTitle: "Подробности уведомления",
    source: "Источник",
    occurred: "Произошло",
    freshness: "Свежесть",
    trace: "Trace ID",
    stableCode: "Стабильный код",
    deepLink: "Открыть связанный запуск",
    deepLinkUnavailable: "Ссылка на связанный ресурс недоступна или не может быть безопасно разрешена.",
    markRead: "Отметить прочитанным",
    dismiss: "Скрыть",
    acknowledge: "Подтвердить",
    acknowledgementUnavailable: "Для подтверждения требуется notification.acknowledge.",
    actionWorking: "Уведомление обновляется",
    actionRead: "Уведомление отмечено прочитанным.",
    actionDismissed: "Уведомление скрыто.",
    actionAcknowledged: "Уведомление подтверждено.",
    actionForbidden: "Действие больше не разрешено. Данные обновлены.",
    actionFailed: "Не удалось обновить уведомление. Обновите данные и повторите попытку.",
    statusResolved: "Разрешено",
    statusAcknowledged: "Подтверждено",
    statusDismissed: "Скрыто",
  },
} as const;

export function notificationCopy(language: NotificationLanguage): typeof copy.en {
  return copy[language] as typeof copy.en;
}

const severityLabels: Record<NotificationLanguage, Record<NotificationSeverity, string>> = {
  en: { info: "Info", warning: "Warning", critical: "Critical" },
  ru: { info: "Информация", warning: "Предупреждение", critical: "Критическое" },
};

const categoryLabels: Record<NotificationLanguage, Record<NotificationCategory, string>> = {
  en: {
    run: "Runs", data_quality: "Data quality", data_freshness: "Data freshness",
    forecast: "Forecasts", schedule: "Schedules", system: "System", security: "Security", admin: "Administration",
  },
  ru: {
    run: "Запуски", data_quality: "Качество данных", data_freshness: "Свежесть данных",
    forecast: "Прогнозы", schedule: "Расписания", system: "Система", security: "Безопасность", admin: "Администрирование",
  },
};

export function severityLabel(language: NotificationLanguage, value: NotificationSeverity): string {
  return severityLabels[language][value];
}

export function categoryLabel(language: NotificationLanguage, value: NotificationCategory): string {
  return categoryLabels[language][value];
}

export function notificationMessage(language: NotificationLanguage, item: NotificationItem): string {
  const messages: Record<NotificationLanguage, Record<string, string>> = {
    en: {
      RUN_FAILED: "A run failed and needs review.",
      RUN_STUCK: "A run appears stuck and needs operator attention.",
      RUN_RECOVERED: "A previously failing run recovered.",
    },
    ru: {
      RUN_FAILED: "Запуск завершился с ошибкой и требует проверки.",
      RUN_STUCK: "Запуск, вероятно, завис и требует внимания оператора.",
      RUN_RECOVERED: "Ранее проблемный запуск восстановлен.",
    },
  };
  return messages[language][item.message_code] ?? item.message_code;
}
