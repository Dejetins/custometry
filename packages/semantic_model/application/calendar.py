"""Immutable calendar meaning; authentication is resolved by the Identity adapter."""

import hashlib
import json
from uuid import UUID, uuid5
from packages.contracts.semantic import (
    BusinessCalendarProfile,
    BusinessCalendarVersion,
    CalendarActor,
    CalendarFailure,
    CalendarRef,
    CalendarRepository,
    UpdateCalendarRequest,
    WorkspaceCalendarDefault,
)


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
    ).hexdigest()


def initial_calendar_id(workspace_id: UUID) -> UUID:
    return uuid5(workspace_id, "business-calendar/v1/initial-january")


class WorkspaceCalendarService:
    def __init__(self, repository: CalendarRepository) -> None:
        self.repository = repository

    @staticmethod
    def _authorize(workspace_id: UUID, actor: CalendarActor, permission: str) -> None:
        if actor.workspace_id != workspace_id or permission not in actor.permissions:
            raise CalendarFailure("FORBIDDEN")

    def provision(self, workspace_id: UUID) -> None:
        profile = BusinessCalendarProfile()
        self.repository.provision(
            workspace_id,
            initial_calendar_id(workspace_id),
            profile,
            digest(profile.model_dump(mode="json")),
        )

    def get_default(self, workspace_id: UUID, actor: CalendarActor) -> WorkspaceCalendarDefault:
        self._authorize(workspace_id, actor, "workspace.read")
        try:
            return self.repository.get_default(workspace_id)
        except CalendarFailure as exc:
            if exc.code != "NOT_FOUND":
                raise
            # Recover an interrupted post-Identity initialization or an old writer's
            # newly created workspace. This cannot replace an existing default.
            self.provision(workspace_id)
            return self.repository.get_default(workspace_id)

    def get_version(self, ref: CalendarRef, actor: CalendarActor) -> BusinessCalendarVersion:
        self._authorize(actor.workspace_id, actor, "workspace.read")
        version = self.repository.get_version(actor.workspace_id, ref.version_id)
        if version.content_hash != ref.content_hash:
            raise CalendarFailure("NOT_FOUND")
        return version

    def update_default(
        self, request: UpdateCalendarRequest, actor: CalendarActor
    ) -> WorkspaceCalendarDefault:
        self._authorize(actor.workspace_id, actor, "workspace.manage")
        # Actor-bound replay: a key cannot reveal another administrator's response.
        request_hash = digest({"actor": str(actor.principal_id), **request.model_dump(mode="json")})
        return self.repository.update_default(
            actor.workspace_id,
            actor.principal_id,
            request,
            digest(request.profile.model_dump(mode="json")),
            request_hash,
        )
