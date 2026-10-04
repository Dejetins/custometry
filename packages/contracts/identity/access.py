"""Public current resource/data ceiling; no Identity persistence escapes this port."""

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class ResourceAccess:
    allowed: bool
    policy_hash: str
    store_ids: tuple[str, ...] | None
    permissions: frozenset[str]


class ResourceAccessPort(Protocol):
    def resolve_resource(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        resource_type: str,
        resource_id: UUID,
        action: str,
        legacy_creator: UUID | None = None,
    ) -> ResourceAccess: ...
