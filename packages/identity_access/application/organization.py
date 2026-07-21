"""Application commands for organization hierarchy and effective access."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID, uuid4

from packages.identity_access.application.service import RepositoryConflict
from packages.identity_access.domain.organization import (
    AccessInputs,
    EffectiveAccessDecision,
    OrganizationInvariant,
    effective_access,
    required_functional_permission,
    validate_unit_shape,
)
from packages.identity_access.domain.policy import Actor, PolicyViolation, require_permission


class OrganizationFailure(RuntimeError):
    """Safe application failure with a stable public code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ResourceCandidate:
    resource_type: str
    resource_id: UUID
    org_unit_id: UUID


class OrganizationRepository(Protocol):
    """Port owned by Identity, Organization & Access application code."""

    def create_unit(
        self,
        *,
        actor: Actor,
        org_unit_id: UUID,
        key: str,
        kind: str,
        parent_org_unit_id: UUID | None,
        display_name: str,
        effective_from: datetime,
    ) -> dict[str, object]: ...

    def version_unit(
        self,
        *,
        actor: Actor,
        org_unit_id: UUID,
        expected_version: int,
        parent_org_unit_id: UUID | None,
        display_name: str,
        effective_from: datetime,
    ) -> dict[str, object]: ...

    def close_unit(
        self,
        *,
        actor: Actor,
        org_unit_id: UUID,
        expected_version: int,
        status: str,
        successor_org_unit_id: UUID | None,
        effective_from: datetime,
    ) -> dict[str, object]: ...

    def list_units(self, actor: Actor) -> list[dict[str, object]]: ...

    def assign_primary(
        self,
        *,
        actor: Actor,
        assignment_id: UUID,
        principal_id: UUID,
        org_unit_id: UUID,
        effective_from: datetime,
        effective_to: datetime | None,
    ) -> dict[str, object]: ...

    def transfer_member(
        self,
        *,
        actor: Actor,
        principal_id: UUID,
        org_unit_id: UUID,
        effective_at: datetime,
    ) -> dict[str, object]: ...

    def deactivate_member(
        self,
        *,
        actor: Actor,
        principal_id: UUID,
        status: str,
        effective_at: datetime,
    ) -> dict[str, object]: ...

    def assign_leadership(
        self,
        *,
        actor: Actor,
        assignment_id: UUID,
        principal_id: UUID,
        org_unit_id: UUID,
        scope_mode: str,
        permissions: tuple[str, ...],
        reason: str,
        effective_from: datetime,
        effective_to: datetime | None,
    ) -> dict[str, object]: ...

    def create_policy_draft(
        self,
        *,
        actor: Actor,
        policy_id: UUID,
        org_unit_id: UUID,
        expected_version: int | None,
        allowed_actions: tuple[str, ...],
        row_scope_refs: tuple[str, ...],
        column_policy_refs: tuple[str, ...],
        pii_allowed: bool,
        include_descendants: bool,
        effective_from: datetime,
    ) -> dict[str, object]: ...

    def publish_policy(
        self,
        *,
        actor: Actor,
        policy_id: UUID,
        expected_version: int,
        effective_from: datetime,
    ) -> dict[str, object]: ...

    def create_grant(
        self,
        *,
        actor: Actor,
        grant_id: UUID,
        subject_type: str,
        subject_id: UUID,
        target_org_unit_id: UUID,
        resource_type: str | None,
        resource_id: UUID | None,
        actions: tuple[str, ...],
        reason: str,
        effective_from: datetime,
        expires_at: datetime | None,
    ) -> dict[str, object]: ...

    def revoke_grant(
        self, *, actor: Actor, grant_id: UUID, expected_version: int, at: datetime
    ) -> dict[str, object]: ...

    def bind_resource(
        self,
        *,
        actor: Actor,
        binding_id: UUID,
        resource_type: str,
        resource_id: UUID,
        creator_principal_id: UUID,
        owner_type: str,
        owner_id: UUID,
        allowed_actions: tuple[str, ...],
        required_row_scope_refs: tuple[str, ...],
        required_column_policy_refs: tuple[str, ...],
        requires_pii: bool,
        effective_from: datetime,
    ) -> dict[str, object]: ...

    def access_context(
        self,
        *,
        actor: Actor,
        target_org_unit_id: UUID,
        functional_permission: str,
        action: str,
        resource_type: str | None,
        resource_id: UUID | None,
        at: datetime,
    ) -> dict[str, bool]: ...

    def list_resource_candidates(
        self,
        *,
        actor: Actor,
        resource_type: str,
        at: datetime,
    ) -> list[ResourceCandidate]: ...


class OrganizationService:
    """Coordinates organization mutations and fail-closed access decisions."""

    def __init__(self, repository: OrganizationRepository) -> None:
        self._repository = repository

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC)

    @classmethod
    def _immediate(cls, value: datetime | None) -> datetime:
        now = cls._now()
        if value is not None and value > now:
            raise OrganizationFailure("INVALID_INPUT")
        return value or now

    @staticmethod
    def _require(actor: Actor, permission: str) -> None:
        try:
            require_permission(actor, permission)
        except PolicyViolation as exc:
            raise OrganizationFailure("FORBIDDEN") from exc

    @staticmethod
    def _translate(exc: RepositoryConflict) -> OrganizationFailure:
        code = str(exc)
        if code in {"not-found", "workspace-mismatch", "hidden"}:
            return OrganizationFailure("NOT_FOUND")
        if code in {"stale-version", "overlapping-primary", "cycle", "handover-required"}:
            return OrganizationFailure("CONFLICT")
        return OrganizationFailure("INVALID_INPUT")

    def create_unit(
        self,
        actor: Actor,
        *,
        key: str,
        kind: str,
        parent_org_unit_id: UUID | None,
        display_name: str,
        effective_from: datetime | None = None,
    ) -> dict[str, object]:
        self._require(actor, "organization.manage")
        try:
            normalized_key, normalized_kind, normalized_name = validate_unit_shape(
                key=key,
                kind=kind,
                display_name=display_name,
                parent_org_unit_id=parent_org_unit_id,
            )
            return self._repository.create_unit(
                actor=actor,
                org_unit_id=uuid4(),
                key=normalized_key,
                kind=normalized_kind,
                parent_org_unit_id=parent_org_unit_id,
                display_name=normalized_name,
                effective_from=self._immediate(effective_from),
            )
        except OrganizationInvariant as exc:
            raise OrganizationFailure("INVALID_INPUT") from exc
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def version_unit(
        self,
        actor: Actor,
        *,
        org_unit_id: UUID,
        expected_version: int,
        parent_org_unit_id: UUID | None,
        display_name: str,
        effective_from: datetime | None = None,
    ) -> dict[str, object]:
        self._require(actor, "organization.manage")
        if expected_version < 1 or not display_name.strip():
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.version_unit(
                actor=actor,
                org_unit_id=org_unit_id,
                expected_version=expected_version,
                parent_org_unit_id=parent_org_unit_id,
                display_name=display_name.strip(),
                effective_from=self._immediate(effective_from),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def close_unit(
        self,
        actor: Actor,
        *,
        org_unit_id: UUID,
        expected_version: int,
        status: str,
        successor_org_unit_id: UUID | None,
        effective_from: datetime | None = None,
    ) -> dict[str, object]:
        self._require(actor, "organization.manage")
        if status not in {"inactive", "merged"} or expected_version < 1:
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.close_unit(
                actor=actor,
                org_unit_id=org_unit_id,
                expected_version=expected_version,
                status=status,
                successor_org_unit_id=successor_org_unit_id,
                effective_from=self._immediate(effective_from),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def list_units(self, actor: Actor) -> list[dict[str, object]]:
        self._require(actor, "organization.read")
        return self._repository.list_units(actor)

    def assign_primary(
        self,
        actor: Actor,
        *,
        principal_id: UUID,
        org_unit_id: UUID,
        effective_from: datetime | None = None,
        effective_to: datetime | None = None,
    ) -> dict[str, object]:
        self._require(actor, "organization.members.assign")
        at = self._immediate(effective_from)
        if effective_to is not None and effective_to <= at:
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.assign_primary(
                actor=actor,
                assignment_id=uuid4(),
                principal_id=principal_id,
                org_unit_id=org_unit_id,
                effective_from=at,
                effective_to=effective_to,
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def transfer_member(
        self, actor: Actor, *, principal_id: UUID, org_unit_id: UUID, effective_at: datetime | None
    ) -> dict[str, object]:
        self._require(actor, "organization.members.assign")
        try:
            return self._repository.transfer_member(
                actor=actor,
                principal_id=principal_id,
                org_unit_id=org_unit_id,
                effective_at=self._immediate(effective_at),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def deactivate_member(
        self, actor: Actor, *, principal_id: UUID, status: str, effective_at: datetime | None
    ) -> dict[str, object]:
        self._require(actor, "organization.members.assign")
        if status not in {"suspended", "departed"}:
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.deactivate_member(
                actor=actor,
                principal_id=principal_id,
                status=status,
                effective_at=self._immediate(effective_at),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def assign_leadership(
        self,
        actor: Actor,
        *,
        principal_id: UUID,
        org_unit_id: UUID,
        scope_mode: str,
        permissions: tuple[str, ...],
        reason: str,
        effective_from: datetime | None,
        effective_to: datetime | None,
    ) -> dict[str, object]:
        self._require(actor, "organization.leadership.assign")
        at = effective_from or self._now()
        if (
            scope_mode not in {"unit", "subtree", "workspace"}
            or not permissions
            or not set(permissions).issubset(actor.permissions)
            or any(permission.startswith("pii.") for permission in permissions)
            or not reason.strip()
            or (effective_to is not None and effective_to <= at)
        ):
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.assign_leadership(
                actor=actor,
                assignment_id=uuid4(),
                principal_id=principal_id,
                org_unit_id=org_unit_id,
                scope_mode=scope_mode,
                permissions=tuple(sorted(set(permissions))),
                reason=reason.strip(),
                effective_from=at,
                effective_to=effective_to,
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def create_policy_draft(
        self,
        actor: Actor,
        *,
        policy_id: UUID | None,
        org_unit_id: UUID,
        expected_version: int | None,
        allowed_actions: tuple[str, ...],
        row_scope_refs: tuple[str, ...],
        column_policy_refs: tuple[str, ...],
        pii_allowed: bool,
        include_descendants: bool,
        effective_from: datetime | None,
    ) -> dict[str, object]:
        self._require(actor, "organization.data_policy.manage")
        if not allowed_actions or (policy_id is None) != (expected_version is None):
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.create_policy_draft(
                actor=actor,
                policy_id=policy_id or uuid4(),
                org_unit_id=org_unit_id,
                expected_version=expected_version,
                allowed_actions=tuple(sorted(set(allowed_actions))),
                row_scope_refs=tuple(sorted(set(row_scope_refs))),
                column_policy_refs=tuple(sorted(set(column_policy_refs))),
                pii_allowed=pii_allowed,
                include_descendants=include_descendants,
                effective_from=self._immediate(effective_from),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def publish_policy(
        self,
        actor: Actor,
        *,
        policy_id: UUID,
        expected_version: int,
        effective_from: datetime | None,
    ) -> dict[str, object]:
        self._require(actor, "organization.data_policy.manage")
        try:
            return self._repository.publish_policy(
                actor=actor,
                policy_id=policy_id,
                expected_version=expected_version,
                effective_from=self._immediate(effective_from),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def create_grant(
        self,
        actor: Actor,
        *,
        subject_type: str,
        subject_id: UUID,
        target_org_unit_id: UUID,
        resource_type: str | None,
        resource_id: UUID | None,
        actions: tuple[str, ...],
        reason: str,
        effective_from: datetime | None,
        expires_at: datetime | None,
    ) -> dict[str, object]:
        self._require(actor, "organization.access.delegate")
        at = effective_from or self._now()
        if (
            subject_type not in {"principal", "org_unit"}
            or not actions
            or not reason.strip()
            or (resource_id is None) != (resource_type is None)
            or (expires_at is not None and expires_at <= at)
        ):
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.create_grant(
                actor=actor,
                grant_id=uuid4(),
                subject_type=subject_type,
                subject_id=subject_id,
                target_org_unit_id=target_org_unit_id,
                resource_type=resource_type,
                resource_id=resource_id,
                actions=tuple(sorted(set(actions))),
                reason=reason.strip(),
                effective_from=at,
                expires_at=expires_at,
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def revoke_grant(
        self, actor: Actor, *, grant_id: UUID, expected_version: int
    ) -> dict[str, object]:
        self._require(actor, "organization.access.delegate")
        try:
            return self._repository.revoke_grant(
                actor=actor, grant_id=grant_id, expected_version=expected_version, at=self._now()
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def bind_resource(
        self,
        actor: Actor,
        *,
        resource_type: str,
        resource_id: UUID,
        creator_principal_id: UUID,
        owner_type: str,
        owner_id: UUID,
        allowed_actions: tuple[str, ...],
        required_row_scope_refs: tuple[str, ...],
        required_column_policy_refs: tuple[str, ...],
        requires_pii: bool,
        effective_from: datetime | None,
    ) -> dict[str, object]:
        self._require(actor, "organization.ownership.manage")
        if (
            owner_type not in {"principal", "org_unit", "workspace_legacy"}
            or not resource_type.strip()
            or not allowed_actions
        ):
            raise OrganizationFailure("INVALID_INPUT")
        try:
            return self._repository.bind_resource(
                actor=actor,
                binding_id=uuid4(),
                resource_type=resource_type.strip(),
                resource_id=resource_id,
                creator_principal_id=creator_principal_id,
                owner_type=owner_type,
                owner_id=owner_id,
                allowed_actions=tuple(sorted(set(allowed_actions))),
                required_row_scope_refs=tuple(sorted(set(required_row_scope_refs))),
                required_column_policy_refs=tuple(
                    sorted(set(required_column_policy_refs))
                ),
                requires_pii=requires_pii,
                effective_from=effective_from or self._now(),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc

    def decide_access(
        self,
        actor: Actor,
        *,
        target_org_unit_id: UUID,
        action: str,
        resource_type: str | None,
        resource_id: UUID | None,
    ) -> EffectiveAccessDecision:
        if (resource_type is None) != (resource_id is None):
            raise OrganizationFailure("INVALID_INPUT")
        if resource_type is None:
            raise OrganizationFailure("INVALID_INPUT")
        try:
            functional_permission = required_functional_permission(resource_type, action)
        except OrganizationInvariant as exc:
            raise OrganizationFailure("INVALID_INPUT") from exc
        try:
            context = self._repository.access_context(
                actor=actor,
                target_org_unit_id=target_org_unit_id,
                functional_permission=functional_permission,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                at=self._now(),
            )
        except RepositoryConflict as exc:
            raise self._translate(exc) from exc
        return effective_access(
            AccessInputs(
                functional_permission=context["functional_permission"],
                active_membership=context["active_membership"],
                organization_scope=context["organization_scope"],
                department_policy=context["department_policy"],
                cross_department_grant=context["cross_department_grant"],
                object_policy=context["object_policy"],
                row_policy=context["row_policy"],
                column_policy=context["column_policy"],
                export_policy=context["export_policy"],
                pii_policy=context["pii_ceiling"],
                policy_fresh=context["policy_fresh"],
                explicit_denies=(),
            )
        )

    def filter_visible_resources(
        self,
        actor: Actor,
        *,
        action: str,
        resource_type: str,
        offset: int,
        limit: int,
    ) -> tuple[tuple[ResourceCandidate, ...], int]:
        if offset < 0 or limit < 1 or limit > 200:
            raise OrganizationFailure("INVALID_INPUT")
        candidates = self._repository.list_resource_candidates(
            actor=actor,
            resource_type=resource_type,
            at=self._now(),
        )
        visible: list[ResourceCandidate] = []
        try:
            required_functional_permission(resource_type, action)
        except OrganizationInvariant as exc:
            raise OrganizationFailure("INVALID_INPUT") from exc
        for candidate in candidates:
            decision = self.decide_access(
                actor,
                target_org_unit_id=candidate.org_unit_id,
                action=action,
                resource_type=candidate.resource_type,
                resource_id=candidate.resource_id,
            )
            if decision.allowed:
                visible.append(candidate)
        return tuple(visible[offset : offset + limit]), len(visible)
