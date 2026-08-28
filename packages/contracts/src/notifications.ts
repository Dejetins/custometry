// Generated from Notifications OpenAPI and event schema. Do not edit.
export const notificationsApiDigest = "691358bd61c2cc76af298042899782219bb5f329c76a7189bda672473e36ff86" as const;
export const notificationEventDigest = "1cbcef152a93283d91921a48414a7dfca23e31a170b234f686808aebf8ed0251" as const;
export const notificationOperations = {
  "acknowledge_notification": { method: "POST", path: "/items/{notification_id}/acknowledge" },
  "dismiss_notification": { method: "POST", path: "/items/{notification_id}/dismiss" },
  "get_notification": { method: "GET", path: "/items/{notification_id}" },
  "get_unread_count": { method: "GET", path: "/unread-count" },
  "list_notifications": { method: "GET", path: "/items" },
  "mark_notification_read": { method: "POST", path: "/items/{notification_id}/read" },
} as const;
export const notificationSchemaNames = ["DeepLinkResponse","HTTPValidationError","NotificationListResponse","NotificationResponse","ReasonedStateRequest","StateRequest","UnreadCountResponse","ValidationError"] as const;
