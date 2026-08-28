"""PostgreSQL projection, state, idempotency, and audit-intent persistence."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, LiteralString, cast
from uuid import UUID, uuid4

from psycopg import Connection, sql
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.contracts.notifications import (
    AuditIntent,
    DeepLinkDescriptor,
    NotificationActor,
    NotificationEvent,
    NotificationFailure,
    RecipientCandidate,
)
from packages.notifications.domain.model import (
    NotificationItem,
    NotificationQuery,
    ProjectionOutcome,
)


Connect = Callable[[], Connection[Any]]


class PostgresNotificationStore:
    """Own all Notifications tables without reading another context's schema."""

    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    @staticmethod
    def _item(row: Any) -> NotificationItem:
        parameters = tuple(sorted(dict(row["message_parameters"]).items()))
        route_id = row["deep_link_route_id"]
        deep_link = None
        if route_id is not None:
            deep_link = DeepLinkDescriptor(
                route_id=str(route_id),
                parameters=tuple(sorted(dict(row["deep_link_parameters"]).items())),
            )
        return NotificationItem(
            notification_id=UUID(str(row["id"])),
            workspace_id=UUID(str(row["workspace_id"])),
            recipient_id=UUID(str(row["recipient_id"])),
            recipient_policy_version=str(row["recipient_policy_version"]),
            preference_reference=(
                None if row["preference_reference"] is None else str(row["preference_reference"])
            ),
            latest_event_id=UUID(str(row["latest_event_id"])),
            source_owner=str(row["source_owner"]),
            source_type=str(row["source_type"]),
            resource_type=str(row["resource_type"]),
            resource_id=str(row["resource_id"]),
            severity=str(row["severity"]),  # type: ignore[arg-type]
            category=str(row["category"]),  # type: ignore[arg-type]
            occurred_at=row["occurred_at"],
            message_code=str(row["message_code"]),
            message_parameters=parameters,
            group_key=str(row["group_key"]),
            source_event_count=int(row["source_event_count"]),
            deep_link=deep_link,
            trace_id=None if row["trace_id"] is None else str(row["trace_id"]),
            resolved=bool(row["resolved"]),
            read_at=row["read_at"],
            dismissed_at=row["dismissed_at"],
            acknowledged_at=row["acknowledged_at"],
            revision=int(row["revision"]),
            freshness=str(row["freshness"]),
        )

    @staticmethod
    def _event_values(event: NotificationEvent) -> tuple[object, ...]:
        link = event.deep_link
        return (
            event.event_id,
            event.source_owner,
            event.source_type,
            event.source_version,
            event.workspace_id,
            event.resource_type,
            event.resource_id,
            event.severity,
            event.category,
            event.occurred_at,
            event.message_code,
            Jsonb(dict(event.message_parameters)),
            event.group_key,
            None if link is None else link.route_id,
            Jsonb({} if link is None else dict(link.parameters)),
            event.trace_id,
            event.resolved,
        )

    def project_event(
        self, event: NotificationEvent, recipients: tuple[RecipientCandidate, ...]
    ) -> ProjectionOutcome:
        projected: list[UUID] = []
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                INSERT INTO notification_source_events
                  (id, source_owner, source_type, source_version, workspace_id,
                   resource_type, resource_id, severity, category, occurred_at,
                   message_code, message_parameters, group_key, deep_link_route_id,
                   deep_link_parameters, trace_id, resolved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING RETURNING id
                """,
                self._event_values(event),
            )
            if cursor.fetchone() is None:
                return ProjectionOutcome(True, 0, ())

            for candidate in recipients:
                recipient_id = candidate.principal_id
                cursor.execute(
                    """
                    SELECT * FROM notification_inbox_items
                    WHERE workspace_id = %s AND recipient_id = %s AND group_key = %s
                    FOR UPDATE
                    """,
                    (event.workspace_id, recipient_id, event.group_key),
                )
                existing = cursor.fetchone()
                link = event.deep_link
                if existing is None:
                    notification_id = uuid4()
                    cursor.execute(
                        """
                        INSERT INTO notification_inbox_items
                          (id, workspace_id, recipient_id, recipient_policy_version,
                           preference_reference, latest_event_id, source_owner,
                           source_type, resource_type, resource_id, severity, category,
                           occurred_at, message_code, message_parameters, group_key,
                           source_event_count, deep_link_route_id, deep_link_parameters,
                           trace_id, resolved, revision, freshness)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, 1, %s, %s, %s, %s, 1, 'fresh')
                        """,
                        (
                            notification_id,
                            event.workspace_id,
                            recipient_id,
                            candidate.policy_version,
                            candidate.preference_reference,
                            event.event_id,
                            event.source_owner,
                            event.source_type,
                            event.resource_type,
                            event.resource_id,
                            event.severity,
                            event.category,
                            event.occurred_at,
                            event.message_code,
                            Jsonb(dict(event.message_parameters)),
                            event.group_key,
                            None if link is None else link.route_id,
                            Jsonb({} if link is None else dict(link.parameters)),
                            event.trace_id,
                            event.resolved,
                        ),
                    )
                else:
                    notification_id = UUID(str(existing["id"]))
                    newer = (event.occurred_at, str(event.event_id)) > (
                        existing["occurred_at"],
                        str(existing["latest_event_id"]),
                    )
                    if newer:
                        cursor.execute(
                            """
                            UPDATE notification_inbox_items SET
                              recipient_policy_version = %s, preference_reference = %s,
                              latest_event_id = %s, source_owner = %s, source_type = %s,
                              resource_type = %s, resource_id = %s, severity = %s,
                              category = %s, occurred_at = %s, message_code = %s,
                              message_parameters = %s, source_event_count = source_event_count + 1,
                              deep_link_route_id = %s, deep_link_parameters = %s,
                              trace_id = %s, resolved = %s, revision = revision + 1,
                              freshness = 'fresh', updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                            """,
                            (
                                candidate.policy_version,
                                candidate.preference_reference,
                                event.event_id,
                                event.source_owner,
                                event.source_type,
                                event.resource_type,
                                event.resource_id,
                                event.severity,
                                event.category,
                                event.occurred_at,
                                event.message_code,
                                Jsonb(dict(event.message_parameters)),
                                None if link is None else link.route_id,
                                Jsonb({} if link is None else dict(link.parameters)),
                                event.trace_id,
                                event.resolved,
                                notification_id,
                            ),
                        )
                    else:
                        cursor.execute(
                            """
                            UPDATE notification_inbox_items
                            SET recipient_policy_version = %s, preference_reference = %s,
                                source_event_count = source_event_count + 1,
                                revision = revision + 1, updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                            """,
                            (
                                candidate.policy_version,
                                candidate.preference_reference,
                                notification_id,
                            ),
                        )
                cursor.execute(
                    """
                    INSERT INTO notification_item_events (notification_id, event_id)
                    VALUES (%s, %s)
                    """,
                    (notification_id, event.event_id),
                )
                projected.append(notification_id)
        return ProjectionOutcome(False, len(projected), tuple(projected))

    @staticmethod
    def _predicate(query: NotificationQuery) -> tuple[str, list[object]]:
        where: list[str] = []
        values: list[object] = []
        if query.severities:
            where.append("severity = ANY(%s)")
            values.append(list(query.severities))
        if query.categories:
            where.append("category = ANY(%s)")
            values.append(list(query.categories))
        for field, value in (
            ("read_at", query.read),
            ("dismissed_at", query.dismissed),
            ("acknowledged_at", query.acknowledged),
        ):
            if value is not None:
                where.append(f"{field} IS {'NOT ' if value else ''}NULL")
        if query.resolved is not None:
            where.append("resolved = %s")
            values.append(query.resolved)
        if query.workspace_id is not None:
            where.append("workspace_id = %s")
            values.append(query.workspace_id)
        if query.occurred_from is not None:
            where.append("occurred_at >= %s")
            values.append(query.occurred_from)
        if query.occurred_to is not None:
            where.append("occurred_at < %s")
            values.append(query.occurred_to)
        return (" AND " + " AND ".join(where) if where else ""), values

    def list_candidates(
        self, principal_id: UUID, query: NotificationQuery
    ) -> tuple[NotificationItem, ...]:
        suffix, values = self._predicate(query)
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                sql.SQL(
                    """
                SELECT * FROM notification_inbox_items
                WHERE recipient_id = %s{}
                ORDER BY occurred_at DESC, id DESC LIMIT 1000
                """
                ).format(sql.SQL(cast(LiteralString, suffix))),
                (principal_id, *values),
            )
            rows = cursor.fetchall()
        return tuple(self._item(row) for row in rows)

    def get_for_recipient(self, principal_id: UUID, notification_id: UUID) -> NotificationItem:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "SELECT * FROM notification_inbox_items WHERE id = %s AND recipient_id = %s",
                (notification_id, principal_id),
            )
            row = cursor.fetchone()
        if row is None:
            raise NotificationFailure("NOT_FOUND")
        return self._item(row)

    def mutate(
        self,
        actor: NotificationActor,
        *,
        notification_id: UUID,
        action: str,
        expected_revision: int,
        reason_code: str | None,
        request_id: str,
        idempotency_key: str,
        payload_hash: str,
    ) -> tuple[NotificationItem, AuditIntent | None]:
        if action not in {"read", "dismiss", "acknowledge"}:
            raise NotificationFailure("INVALID_INPUT")
        at = datetime.now(UTC)
        route = f"notification.{action}"
        audit_intent: AuditIntent | None = None
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT payload_hash, response_notification_id
                FROM notification_idempotency
                WHERE actor_id = %s AND route = %s AND idempotency_key = %s
                """,
                (actor.principal_id, route, idempotency_key),
            )
            replay = cursor.fetchone()
            if replay is not None:
                if str(replay["payload_hash"]) != payload_hash:
                    raise NotificationFailure("IDEMPOTENCY_CONFLICT")
                cursor.execute(
                    """
                    SELECT * FROM notification_inbox_items
                    WHERE id = %s AND recipient_id = %s
                    """,
                    (replay["response_notification_id"], actor.principal_id),
                )
                row = cursor.fetchone()
                if row is None:
                    raise NotificationFailure("NOT_FOUND")
                return self._item(row), None

            cursor.execute(
                """
                SELECT * FROM notification_inbox_items
                WHERE id = %s AND recipient_id = %s FOR UPDATE
                """,
                (notification_id, actor.principal_id),
            )
            current = cursor.fetchone()
            if current is None:
                raise NotificationFailure("NOT_FOUND")
            if int(current["revision"]) != expected_revision:
                raise NotificationFailure(
                    "STALE_REVISION", current_revision=int(current["revision"])
                )
            column = {
                "read": "read_at",
                "dismiss": "dismissed_at",
                "acknowledge": "acknowledged_at",
            }[action]
            changed = current[column] is None
            if changed:
                cursor.execute(
                    sql.SQL(
                        """
                    UPDATE notification_inbox_items
                    SET {} = %s, revision = revision + 1,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s RETURNING *
                    """
                    ).format(sql.Identifier(column)),
                    (at, notification_id),
                )
                result = cursor.fetchone()
            else:
                result = current
            assert result is not None
            cursor.execute(
                """
                INSERT INTO notification_idempotency
                  (actor_id, route, idempotency_key, payload_hash, response_notification_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    actor.principal_id,
                    route,
                    idempotency_key,
                    payload_hash,
                    notification_id,
                ),
            )
            if changed and action in {"acknowledge", "dismiss"}:
                assert reason_code is not None
                audit_action = (
                    "notification.acknowledged"
                    if action == "acknowledge"
                    else "notification.dismissed"
                )
                audit_id = uuid4()
                cursor.execute(
                    """
                    INSERT INTO notification_audit_outbox
                      (id, action, workspace_id, actor_id, notification_id,
                       reason_code, request_id, occurred_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        audit_id,
                        audit_action,
                        result["workspace_id"],
                        actor.principal_id,
                        notification_id,
                        reason_code,
                        request_id,
                        at,
                    ),
                )
                audit_intent = AuditIntent(
                    action=audit_action,  # type: ignore[arg-type]
                    workspace_id=UUID(str(result["workspace_id"])),
                    actor_id=actor.principal_id,
                    notification_id=notification_id,
                    reason_code=reason_code,
                    request_id=request_id,
                    occurred_at=at,
                )
        return self._item(result), audit_intent


__all__ = ["PostgresNotificationStore"]
