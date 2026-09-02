"""Authenticated, permission-filtered in-app notification inbox API."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Header, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from packages.contracts.notifications import (
    NOTIFICATIONS_API_VERSION,
    DeepLinkDescriptor,
    NotificationActor,
    NotificationFailure,
)
from packages.identity_access.application.service import IdentityService
from packages.identity_access.domain.policy import Actor
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from packages.notifications.application.service import NotificationInboxService
from packages.notifications.domain.model import NotificationQuery, VisibleNotification
from packages.notifications.infrastructure.postgres import PostgresNotificationStore


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorResponse(StrictModel):
    code: str
    current_revision: int | None = None


class DeepLinkResponse(StrictModel):
    status: Literal["available", "unavailable"]
    route_id: str | None = None
    parameters: dict[str, str] | None = None


class NotificationResponse(StrictModel):
    notification_id: UUID
    workspace_id: UUID
    latest_event_id: UUID
    source_owner: str
    source_type: str
    severity: Literal["info", "warning", "critical"]
    category: Literal[
        "run",
        "data_quality",
        "data_freshness",
        "forecast",
        "schedule",
        "system",
        "security",
        "admin",
    ]
    occurred_at: datetime
    message_code: str
    message_parameters: dict[str, str | int | bool]
    group_key: str
    source_event_count: int = Field(ge=1)
    trace_id: str | None
    resolved: bool
    read: bool
    dismissed: bool
    acknowledged: bool
    revision: int = Field(ge=1)
    freshness: Literal["fresh", "stale", "degraded"]
    deep_link: DeepLinkResponse

    @classmethod
    def from_visible(cls, value: VisibleNotification) -> "NotificationResponse":
        item = value.item
        link = item.deep_link if value.deep_link_status == "available" else None
        return cls(
            notification_id=item.notification_id,
            workspace_id=item.workspace_id,
            latest_event_id=item.latest_event_id,
            source_owner=item.source_owner,
            source_type=item.source_type,
            severity=item.severity,
            category=item.category,
            occurred_at=item.occurred_at,
            message_code=item.message_code,
            message_parameters=dict(item.message_parameters),
            group_key=item.group_key,
            source_event_count=item.source_event_count,
            trace_id=item.trace_id,
            resolved=item.resolved,
            read=item.read_at is not None,
            dismissed=item.dismissed_at is not None,
            acknowledged=item.acknowledged_at is not None,
            revision=item.revision,
            freshness=item.freshness,  # type: ignore[arg-type]
            deep_link=DeepLinkResponse(
                status=value.deep_link_status,  # type: ignore[arg-type]
                route_id=None if link is None else link.route_id,
                parameters=None if link is None else dict(link.parameters),
            ),
        )


class NotificationListResponse(StrictModel):
    items: list[NotificationResponse]
    visible_count: int = Field(ge=0)


class UnreadCountResponse(StrictModel):
    unread_count: int = Field(ge=0, le=999)
    capped: bool


class StateRequest(StrictModel):
    expected_revision: int = Field(ge=1)


class ReasonedStateRequest(StateRequest):
    reason_code: str = Field(min_length=3, max_length=80)


@dataclass(frozen=True, slots=True)
class RequestContext:
    actor: NotificationActor
    request_id: str


class SessionWorkspaceNotificationAccess:
    """Fail-closed adapter over the current public Identity actor projection."""

    RESOURCE_PERMISSIONS = {
        "run": "run.read",
        "dataset": "dataset.read",
        "forecast": "forecast.read",
        "schedule": "schedule.read",
        "system": "installation.diagnostics.read",
        "security": "audit.read",
        "admin": "audit.read",
    }

    def require(self, actor: NotificationActor, action: str) -> None:
        if action not in actor.permissions:
            raise NotificationFailure("FORBIDDEN")

    def can_access(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
    ) -> bool:
        del resource_id
        permission = self.RESOURCE_PERMISSIONS.get(resource_type)
        return workspace_id in actor.active_workspace_ids and (
            permission is None or permission in actor.permissions
        )

    def can_disclose_deep_link(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
        deep_link: DeepLinkDescriptor,
    ) -> bool:
        del deep_link
        return self.can_access(
            actor,
            workspace_id=workspace_id,
            resource_type=resource_type,
            resource_id=resource_id,
        )


def _services(settings: Settings) -> tuple[IdentityService, NotificationInboxService]:
    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    identity = IdentityService(PostgresIdentityRepository(connect), bootstrap_secret=None)
    notifications = NotificationInboxService(
        PostgresNotificationStore(connect), SessionWorkspaceNotificationAccess()
    )
    return identity, notifications


def _status_for(code: str) -> int:
    if code == "AUTHENTICATION_FAILED":
        return status.HTTP_401_UNAUTHORIZED
    if code == "FORBIDDEN":
        return status.HTTP_403_FORBIDDEN
    if code == "NOT_FOUND":
        return status.HTTP_404_NOT_FOUND
    if code in {"IDEMPOTENCY_CONFLICT", "STALE_REVISION"}:
        return status.HTTP_409_CONFLICT
    if code in {"RECIPIENT_RESOLUTION_UNAVAILABLE", "DEPENDENCY_UNAVAILABLE"}:
        return status.HTTP_503_SERVICE_UNAVAILABLE
    return status.HTTP_400_BAD_REQUEST


def _payload_hash(route: str, payload: BaseModel) -> str:
    canonical = json.dumps(
        {"route": route, "payload": payload.model_dump(mode="json")},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


def _policy_version(actor: Actor) -> str:
    value = json.dumps(
        {
            "workspace_id": str(actor.workspace_id),
            "permissions": sorted(actor.permissions),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(value.encode()).hexdigest()


def create_notifications_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    notification_service: NotificationInboxService | None = None,
) -> FastAPI:
    default_identity, default_notifications = _services(settings)
    identity = identity_service or default_identity
    notifications = notification_service or default_notifications
    app = FastAPI(
        title="Custometry In-App Notifications API",
        version=NOTIFICATIONS_API_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(NotificationFailure)
    async def notification_failure_handler(_: Request, exc: NotificationFailure) -> JSONResponse:
        payload = ErrorResponse(code=exc.code, current_revision=exc.current_revision)
        return JSONResponse(
            status_code=_status_for(exc.code),
            content=payload.model_dump(exclude_none=True),
        )

    def authenticated(
        authorization: Annotated[str | None, Header(alias="Authorization")] = None,
        request_id: Annotated[str | None, Header(alias="X-Request-ID")] = None,
        contract_version: Annotated[str | None, Header(alias="X-Contract-Version")] = None,
    ) -> RequestContext:
        if request_id is None or not request_id.strip() or len(request_id) > 128:
            raise NotificationFailure("REQUEST_ID_REQUIRED")
        if contract_version != NOTIFICATIONS_API_VERSION:
            raise NotificationFailure("CONTRACT_VERSION_MISMATCH")
        if authorization is None:
            raise NotificationFailure("AUTHENTICATION_FAILED")
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer" or not token:
            raise NotificationFailure("AUTHENTICATION_FAILED")
        try:
            resolved = identity.authenticate(token)
        except Exception as exc:
            raise NotificationFailure("AUTHENTICATION_FAILED") from exc
        return RequestContext(
            actor=NotificationActor(
                principal_id=resolved.principal_id,
                permissions=resolved.permissions,
                policy_version=_policy_version(resolved),
                active_workspace_ids=(resolved.workspace_id,),
            ),
            request_id=request_id.strip(),
        )

    @app.get("/items", response_model=NotificationListResponse, operation_id="list_notifications")
    def list_items(
        severity: Annotated[list[Literal["info", "warning", "critical"]] | None, Query()] = None,
        category: Annotated[
            list[
                Literal[
                    "run",
                    "data_quality",
                    "data_freshness",
                    "forecast",
                    "schedule",
                    "system",
                    "security",
                    "admin",
                ]
            ]
            | None,
            Query(),
        ] = None,
        read: bool | None = None,
        dismissed: bool | None = None,
        acknowledged: bool | None = None,
        resolved: bool | None = None,
        workspace_id: UUID | None = None,
        occurred_from: datetime | None = None,
        occurred_to: datetime | None = None,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        context: RequestContext = Depends(authenticated),
    ) -> NotificationListResponse:
        items, count = notifications.list_items(
            context.actor,
            NotificationQuery(
                severities=tuple(severity or ()),
                categories=tuple(category or ()),
                read=read,
                dismissed=dismissed,
                acknowledged=acknowledged,
                resolved=resolved,
                workspace_id=workspace_id,
                occurred_from=occurred_from,
                occurred_to=occurred_to,
                offset=offset,
                limit=limit,
            ),
        )
        return NotificationListResponse(
            items=[NotificationResponse.from_visible(item) for item in items],
            visible_count=count,
        )

    @app.get("/unread-count", response_model=UnreadCountResponse, operation_id="get_unread_count")
    def unread_count(context: RequestContext = Depends(authenticated)) -> UnreadCountResponse:
        count = notifications.unread_count(context.actor)
        return UnreadCountResponse(unread_count=count, capped=count == 999)

    @app.get(
        "/items/{notification_id}",
        response_model=NotificationResponse,
        operation_id="get_notification",
    )
    def get_item(
        notification_id: UUID, context: RequestContext = Depends(authenticated)
    ) -> NotificationResponse:
        return NotificationResponse.from_visible(
            notifications.get_item(context.actor, notification_id)
        )

    def mutate(
        notification_id: UUID,
        action: str,
        payload: StateRequest,
        idempotency_key: str | None,
        context: RequestContext,
    ) -> NotificationResponse:
        if idempotency_key is None:
            raise NotificationFailure("IDEMPOTENCY_KEY_REQUIRED")
        reason = payload.reason_code if isinstance(payload, ReasonedStateRequest) else None
        return NotificationResponse.from_visible(
            notifications.mutate(
                context.actor,
                notification_id=notification_id,
                action=action,
                expected_revision=payload.expected_revision,
                reason_code=reason,
                request_id=context.request_id,
                idempotency_key=idempotency_key,
                payload_hash=_payload_hash(f"/items/{notification_id}/{action}", payload),
            )
        )

    @app.post(
        "/items/{notification_id}/read",
        response_model=NotificationResponse,
        operation_id="mark_notification_read",
    )
    def mark_read(
        notification_id: UUID,
        payload: StateRequest,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        context: RequestContext = Depends(authenticated),
    ) -> NotificationResponse:
        return mutate(notification_id, "read", payload, idempotency_key, context)

    @app.post(
        "/items/{notification_id}/dismiss",
        response_model=NotificationResponse,
        operation_id="dismiss_notification",
    )
    def dismiss(
        notification_id: UUID,
        payload: ReasonedStateRequest,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        context: RequestContext = Depends(authenticated),
    ) -> NotificationResponse:
        return mutate(notification_id, "dismiss", payload, idempotency_key, context)

    @app.post(
        "/items/{notification_id}/acknowledge",
        response_model=NotificationResponse,
        operation_id="acknowledge_notification",
    )
    def acknowledge(
        notification_id: UUID,
        payload: ReasonedStateRequest,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        context: RequestContext = Depends(authenticated),
    ) -> NotificationResponse:
        return mutate(notification_id, "acknowledge", payload, idempotency_key, context)

    _ = (
        notification_failure_handler,
        list_items,
        unread_count,
        get_item,
        mark_read,
        dismiss,
        acknowledge,
    )
    return app


__all__ = ["SessionWorkspaceNotificationAccess", "create_notifications_app"]
