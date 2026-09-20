"""Identity-owned projection of current organization and data policy decisions."""

from __future__ import annotations
import hashlib
import json
from collections.abc import Callable
from typing import Any, Protocol
from uuid import UUID
from packages.contracts.identity.access import ResourceAccess
from packages.identity_access.application.service import RepositoryConflict
from packages.identity_access.domain.policy import Actor
from packages.identity_access.domain.organization import AccessInputs, effective_access


class ResourceAccessRepository(Protocol):
    def resource_context(
        self,
        actor: Actor,
        resource_type: str,
        resource_id: UUID,
        action: str,
        legacy_creator: UUID | None,
    ) -> dict[str, Any]: ...


class ResourceAccessService:
    def __init__(self, repository: ResourceAccessRepository, actor: Callable[[], Actor]):
        self.repository, self.actor = repository, actor

    def resolve_resource(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        resource_type: str,
        resource_id: UUID,
        action: str,
        legacy_creator: UUID | None = None,
    ) -> ResourceAccess:
        actor = self.actor()  # Reauthenticate: session revocation and token ceilings stay current.
        if (actor.workspace_id, actor.principal_id) != (workspace_id, principal_id):
            return ResourceAccess(False, "0" * 64, (), frozenset())
        try:
            context = self.repository.resource_context(
                actor, resource_type, resource_id, action, legacy_creator
            )
        except RepositoryConflict:
            return ResourceAccess(False, "0" * 64, (), actor.permissions)
        allowed = effective_access(AccessInputs(**context["layers"])).allowed
        detail = context["detail"]
        stores: set[str] | None = None
        for refs in detail.get("row_scopes", []):
            if refs:
                if any(
                    not isinstance(r, str)
                    or not r.startswith("store:")
                    or not 1 <= len(r[6:]) <= 128
                    for r in refs
                ):
                    allowed = False
                else:
                    values = {r[6:] for r in refs}
                    stores = values if stores is None else stores & values
        if any(detail.get("column_scopes", [])):
            allowed = False
        fingerprint = hashlib.sha256(
            json.dumps(
                {
                    "resource": [resource_type, str(resource_id)],
                    "workspace": str(workspace_id),
                    "actor": str(principal_id),
                    "context": context,
                },
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode()
        ).hexdigest()
        return ResourceAccess(
            allowed,
            fingerprint,
            None if stores is None else tuple(sorted(stores)),
            actor.permissions,
        )
