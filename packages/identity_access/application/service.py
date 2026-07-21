"""Local-authentication and workspace application service."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol
from uuid import UUID, uuid4

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from packages.identity_access.domain.policy import (
    Actor,
    PolicyViolation,
    permissions_for_roles,
    require_grant_ceiling,
    require_permission,
    require_workspace,
)


class IdentityFailure(RuntimeError):
    """Safe application failure with a stable public code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class RepositoryConflict(RuntimeError):
    """Persistence invariant conflict translated at the application boundary."""


@dataclass(frozen=True, slots=True)
class Credential:
    principal_id: UUID
    email: str
    password_hash: str
    active: bool
    installation_admin: bool


@dataclass(frozen=True, slots=True)
class Invitation:
    invitation_id: UUID
    workspace_id: UUID
    email: str
    roles: tuple[str, ...]
    expires_at: datetime
    accepted: bool
    revoked: bool


@dataclass(frozen=True, slots=True)
class SessionTokens:
    session_id: UUID
    workspace_id: UUID
    access_token: str
    refresh_token: str
    csrf_token: str
    access_expires_at: datetime
    absolute_expires_at: datetime


@dataclass(frozen=True, slots=True)
class BootstrapOutcome:
    principal_id: UUID
    workspace_id: UUID
    workspace_key: str


@dataclass(frozen=True, slots=True)
class WorkspaceOutcome:
    workspace_id: UUID
    workspace_key: str
    name: str


@dataclass(frozen=True, slots=True)
class InvitationOutcome:
    invitation_id: UUID
    workspace_id: UUID
    token: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ApiTokenOutcome:
    token_id: UUID
    workspace_id: UUID
    token: str
    scopes: tuple[str, ...]
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class PasswordResetOutcome:
    reset_id: UUID
    token: str
    expires_at: datetime


class IdentityRepository(Protocol):
    """Port owned by Identity & Workspace application code."""

    def bootstrap(
        self,
        *,
        principal_id: UUID,
        email: str,
        password_hash: str,
        workspace_id: UUID,
        workspace_key: str,
        workspace_name: str,
        at: datetime,
    ) -> BootstrapOutcome: ...

    def create_workspace(
        self,
        *,
        actor: Actor,
        workspace_id: UUID,
        workspace_key: str,
        name: str,
        at: datetime,
    ) -> WorkspaceOutcome: ...

    def credential_for_login(self, email: str, workspace_id: UUID) -> Credential | None: ...

    def credential_by_email(self, email: str) -> Credential | None: ...

    def create_session(
        self,
        *,
        session_id: UUID,
        family_id: UUID,
        principal_id: UUID,
        workspace_id: UUID,
        access_hash: str,
        refresh_hash: str,
        csrf_hash: str,
        device_label: str,
        access_expires_at: datetime,
        absolute_expires_at: datetime,
        at: datetime,
    ) -> None: ...

    def actor_for_access(self, token_hash: str, at: datetime) -> Actor | None: ...

    def actor_for_api_token(self, token_hash: str, at: datetime) -> Actor | None: ...

    def rotate_session(
        self,
        *,
        presented_hash: str,
        presented_csrf_hash: str,
        access_hash: str,
        refresh_hash: str,
        csrf_hash: str,
        access_expires_at: datetime,
        at: datetime,
    ) -> tuple[UUID, UUID, datetime]: ...

    def revoke_session(self, actor: Actor, session_id: UUID, at: datetime) -> bool: ...

    def revoke_current_refresh(self, refresh_hash: str, csrf_hash: str, at: datetime) -> bool: ...

    def revoke_all_sessions(self, principal_id: UUID, at: datetime) -> int: ...

    def list_sessions(self, actor: Actor, principal_id: UUID | None) -> list[dict[str, object]]: ...

    def create_invitation(
        self,
        *,
        actor: Actor,
        invitation_id: UUID,
        email: str,
        roles: tuple[str, ...],
        token_hash: str,
        expires_at: datetime,
        at: datetime,
    ) -> None: ...

    def invitation_for_token(self, token_hash: str) -> Invitation | None: ...

    def revoke_invitation(self, actor: Actor, invitation_id: UUID, at: datetime) -> bool: ...

    def accept_invitation(
        self,
        *,
        invitation: Invitation,
        token_hash: str,
        principal_id: UUID,
        password_hash: str | None,
        at: datetime,
    ) -> UUID: ...

    def list_members(self, actor: Actor, workspace_id: UUID) -> list[dict[str, object]]: ...

    def create_api_token(
        self,
        *,
        actor: Actor,
        token_id: UUID,
        name: str,
        token_hash: str,
        scopes: tuple[str, ...],
        expires_at: datetime,
        at: datetime,
    ) -> None: ...

    def revoke_api_token(self, actor: Actor, token_id: UUID, at: datetime) -> bool: ...

    def change_password(self, principal_id: UUID, password_hash: str, at: datetime) -> None: ...

    def create_password_reset(
        self,
        *,
        actor: Actor,
        reset_id: UUID,
        principal_id: UUID,
        token_hash: str,
        expires_at: datetime,
        at: datetime,
    ) -> None: ...

    def consume_password_reset(self, token_hash: str, password_hash: str, at: datetime) -> UUID: ...


def token_hash(token: str) -> str:
    """Return the only representation allowed in persistence."""

    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class IdentityService:
    """Coordinates local auth while persistence enforces transaction races."""

    def __init__(
        self,
        repository: IdentityRepository,
        *,
        bootstrap_secret: str | None,
        access_ttl: timedelta = timedelta(minutes=15),
        refresh_ttl: timedelta = timedelta(days=30),
        password_hasher: PasswordHasher | None = None,
    ) -> None:
        self._repository = repository
        self._bootstrap_secret = bootstrap_secret
        self._access_ttl = access_ttl
        self._refresh_ttl = refresh_ttl
        self._password_hasher = password_hasher or PasswordHasher()

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC)

    @staticmethod
    def _secret() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def _email(value: str) -> str:
        normalized = value.strip().casefold()
        if not normalized or len(normalized) > 320 or "@" not in normalized:
            raise IdentityFailure("INVALID_INPUT")
        return normalized

    @staticmethod
    def _workspace_key(value: str) -> str:
        normalized = value.strip().casefold()
        if not (3 <= len(normalized) <= 63):
            raise IdentityFailure("INVALID_INPUT")
        allowed = normalized[0].isalpha() and normalized[-1].isalnum()
        allowed = allowed and all(
            character.isalnum() or character == "-" for character in normalized
        )
        if not allowed:
            raise IdentityFailure("INVALID_INPUT")
        return normalized

    def _hash_password(self, password: str) -> str:
        if len(password) < 12 or len(password) > 1024:
            raise IdentityFailure("INVALID_INPUT")
        return self._password_hasher.hash(password)

    def _verify_password(self, password_hash: str, password: str) -> bool:
        try:
            return self._password_hasher.verify(password_hash, password)
        except (InvalidHashError, VerificationError, VerifyMismatchError):
            return False

    def bootstrap(
        self,
        *,
        presented_secret: str,
        email: str,
        password: str,
        workspace_key: str,
        workspace_name: str,
    ) -> BootstrapOutcome:
        if not self._bootstrap_secret or not hmac.compare_digest(
            presented_secret, self._bootstrap_secret
        ):
            raise IdentityFailure("BOOTSTRAP_UNAVAILABLE")
        at = self._now()
        try:
            return self._repository.bootstrap(
                principal_id=uuid4(),
                email=self._email(email),
                password_hash=self._hash_password(password),
                workspace_id=uuid4(),
                workspace_key=self._workspace_key(workspace_key),
                workspace_name=workspace_name.strip(),
                at=at,
            )
        except RepositoryConflict as exc:
            raise IdentityFailure("BOOTSTRAP_UNAVAILABLE") from exc

    def create_workspace(self, actor: Actor, *, key: str, name: str) -> WorkspaceOutcome:
        if not actor.installation_admin:
            raise IdentityFailure("FORBIDDEN")
        try:
            return self._repository.create_workspace(
                actor=actor,
                workspace_id=uuid4(),
                workspace_key=self._workspace_key(key),
                name=name.strip(),
                at=self._now(),
            )
        except RepositoryConflict as exc:
            raise IdentityFailure("CONFLICT") from exc

    def login(
        self, *, email: str, password: str, workspace_id: UUID, device_label: str
    ) -> SessionTokens:
        credential = self._repository.credential_for_login(self._email(email), workspace_id)
        if (
            credential is None
            or not credential.active
            or not self._verify_password(credential.password_hash, password)
        ):
            raise IdentityFailure("AUTHENTICATION_FAILED")
        at = self._now()
        access = self._secret()
        refresh = self._secret()
        csrf = self._secret()
        session_id = uuid4()
        absolute_expires_at = at + self._refresh_ttl
        access_expires_at = at + self._access_ttl
        self._repository.create_session(
            session_id=session_id,
            family_id=uuid4(),
            principal_id=credential.principal_id,
            workspace_id=workspace_id,
            access_hash=token_hash(access),
            refresh_hash=token_hash(refresh),
            csrf_hash=token_hash(csrf),
            device_label=(device_label.strip() or "unknown")[:160],
            access_expires_at=access_expires_at,
            absolute_expires_at=absolute_expires_at,
            at=at,
        )
        return SessionTokens(
            session_id=session_id,
            workspace_id=workspace_id,
            access_token=access,
            refresh_token=refresh,
            csrf_token=csrf,
            access_expires_at=access_expires_at,
            absolute_expires_at=absolute_expires_at,
        )

    def authenticate(self, raw_token: str) -> Actor:
        digest = token_hash(raw_token)
        at = self._now()
        actor = self._repository.actor_for_access(digest, at)
        if actor is None:
            actor = self._repository.actor_for_api_token(digest, at)
        if actor is None:
            raise IdentityFailure("AUTHENTICATION_FAILED")
        return actor

    def verify_csrf(self, actor: Actor, raw_csrf: str | None) -> None:
        if actor.token_kind != "session":
            return
        if not raw_csrf or not actor.csrf_token_hash:
            raise IdentityFailure("CSRF_FAILED")
        if not hmac.compare_digest(token_hash(raw_csrf), actor.csrf_token_hash):
            raise IdentityFailure("CSRF_FAILED")

    def refresh(self, raw_refresh: str, raw_csrf: str) -> SessionTokens:
        at = self._now()
        access = self._secret()
        refresh = self._secret()
        csrf = self._secret()
        try:
            session_id, workspace_id, absolute_expires_at = self._repository.rotate_session(
                presented_hash=token_hash(raw_refresh),
                presented_csrf_hash=token_hash(raw_csrf),
                access_hash=token_hash(access),
                refresh_hash=token_hash(refresh),
                csrf_hash=token_hash(csrf),
                access_expires_at=at + self._access_ttl,
                at=at,
            )
        except RepositoryConflict as exc:
            code = str(exc)
            if code == "refresh-reuse":
                raise IdentityFailure("REFRESH_REUSE_DETECTED") from exc
            raise IdentityFailure("AUTHENTICATION_FAILED") from exc
        return SessionTokens(
            session_id=session_id,
            workspace_id=workspace_id,
            access_token=access,
            refresh_token=refresh,
            csrf_token=csrf,
            access_expires_at=at + self._access_ttl,
            absolute_expires_at=absolute_expires_at,
        )

    def logout(self, raw_refresh: str, raw_csrf: str) -> None:
        if not self._repository.revoke_current_refresh(
            token_hash(raw_refresh), token_hash(raw_csrf), self._now()
        ):
            raise IdentityFailure("AUTHENTICATION_FAILED")

    def logout_all(self, actor: Actor) -> int:
        require_permission(actor, "session.manage_own")
        return self._repository.revoke_all_sessions(actor.principal_id, self._now())

    def list_sessions(
        self, actor: Actor, principal_id: UUID | None = None
    ) -> list[dict[str, object]]:
        target = principal_id or actor.principal_id
        if target != actor.principal_id:
            require_permission(actor, "workspace.sessions.manage")
        else:
            require_permission(actor, "session.manage_own")
        return self._repository.list_sessions(actor, target)

    def revoke_session(self, actor: Actor, session_id: UUID) -> None:
        require_permission(actor, "session.manage_own")
        if not self._repository.revoke_session(actor, session_id, self._now()):
            raise IdentityFailure("NOT_FOUND")

    def invite(
        self,
        actor: Actor,
        *,
        workspace_id: UUID,
        email: str,
        roles: list[str],
        expires_in_hours: int,
    ) -> InvitationOutcome:
        try:
            require_workspace(actor, workspace_id)
            require_permission(actor, "workspace.members.manage")
            require_permission(actor, "workspace.roles.assign")
            normalized = require_grant_ceiling(actor, roles)
        except PolicyViolation as exc:
            raise IdentityFailure("FORBIDDEN") from exc
        at = self._now()
        token = self._secret()
        invitation_id = uuid4()
        expires_at = at + timedelta(hours=expires_in_hours)
        self._repository.create_invitation(
            actor=actor,
            invitation_id=invitation_id,
            email=self._email(email),
            roles=normalized,
            token_hash=token_hash(token),
            expires_at=expires_at,
            at=at,
        )
        return InvitationOutcome(invitation_id, workspace_id, token, expires_at)

    def accept_invitation(self, *, token: str, password: str) -> UUID:
        digest = token_hash(token)
        invitation = self._repository.invitation_for_token(digest)
        if invitation is None or invitation.accepted or invitation.revoked:
            raise IdentityFailure("INVITATION_INVALID")
        if invitation.expires_at <= self._now():
            raise IdentityFailure("INVITATION_INVALID")
        existing = self._repository.credential_by_email(invitation.email)
        password_hash: str | None
        if existing is None:
            principal_id = uuid4()
            password_hash = self._hash_password(password)
        else:
            if not existing.active or not self._verify_password(existing.password_hash, password):
                raise IdentityFailure("INVITATION_INVALID")
            principal_id = existing.principal_id
            password_hash = None
        try:
            return self._repository.accept_invitation(
                invitation=invitation,
                token_hash=digest,
                principal_id=principal_id,
                password_hash=password_hash,
                at=self._now(),
            )
        except RepositoryConflict as exc:
            raise IdentityFailure("INVITATION_INVALID") from exc

    def revoke_invitation(self, actor: Actor, invitation_id: UUID) -> None:
        try:
            require_permission(actor, "workspace.members.manage")
        except PolicyViolation as exc:
            raise IdentityFailure("FORBIDDEN") from exc
        if not self._repository.revoke_invitation(actor, invitation_id, self._now()):
            raise IdentityFailure("NOT_FOUND")

    def list_members(self, actor: Actor, workspace_id: UUID) -> list[dict[str, object]]:
        try:
            require_workspace(actor, workspace_id)
            require_permission(actor, "workspace.members.read")
        except PolicyViolation as exc:
            raise IdentityFailure("NOT_FOUND") from exc
        return self._repository.list_members(actor, workspace_id)

    def issue_api_token(
        self,
        actor: Actor,
        *,
        name: str,
        scopes: list[str],
        expires_in_hours: int,
    ) -> ApiTokenOutcome:
        try:
            require_permission(actor, "api_token.manage_own")
        except PolicyViolation as exc:
            raise IdentityFailure("FORBIDDEN") from exc
        normalized_scopes = tuple(sorted(set(scopes)))
        if not normalized_scopes or not set(normalized_scopes).issubset(actor.permissions):
            raise IdentityFailure("FORBIDDEN")
        at = self._now()
        raw = self._secret()
        token_id = uuid4()
        expires_at = at + timedelta(hours=expires_in_hours)
        self._repository.create_api_token(
            actor=actor,
            token_id=token_id,
            name=name.strip(),
            token_hash=token_hash(raw),
            scopes=normalized_scopes,
            expires_at=expires_at,
            at=at,
        )
        return ApiTokenOutcome(token_id, actor.workspace_id, raw, normalized_scopes, expires_at)

    def revoke_api_token(self, actor: Actor, token_id: UUID) -> None:
        try:
            require_permission(actor, "api_token.manage_own")
        except PolicyViolation as exc:
            raise IdentityFailure("FORBIDDEN") from exc
        if not self._repository.revoke_api_token(actor, token_id, self._now()):
            raise IdentityFailure("NOT_FOUND")

    def change_password(self, actor: Actor, *, current: str, replacement: str) -> None:
        try:
            require_permission(actor, "password.change_own")
        except PolicyViolation as exc:
            raise IdentityFailure("FORBIDDEN") from exc
        credential = self._repository.credential_by_email(actor.email)
        if credential is None or not self._verify_password(credential.password_hash, current):
            raise IdentityFailure("AUTHENTICATION_FAILED")
        self._repository.change_password(
            actor.principal_id, self._hash_password(replacement), self._now()
        )

    def create_password_reset(
        self, actor: Actor, *, principal_id: UUID, expires_in_minutes: int
    ) -> PasswordResetOutcome:
        try:
            require_permission(actor, "workspace.password_reset.manage")
        except PolicyViolation as exc:
            raise IdentityFailure("FORBIDDEN") from exc
        at = self._now()
        raw = self._secret()
        reset_id = uuid4()
        expires_at = at + timedelta(minutes=expires_in_minutes)
        try:
            self._repository.create_password_reset(
                actor=actor,
                reset_id=reset_id,
                principal_id=principal_id,
                token_hash=token_hash(raw),
                expires_at=expires_at,
                at=at,
            )
        except RepositoryConflict as exc:
            raise IdentityFailure("NOT_FOUND") from exc
        return PasswordResetOutcome(reset_id, raw, expires_at)

    def consume_password_reset(self, *, token: str, replacement: str) -> UUID:
        try:
            return self._repository.consume_password_reset(
                token_hash(token), self._hash_password(replacement), self._now()
            )
        except RepositoryConflict as exc:
            raise IdentityFailure("PASSWORD_RESET_INVALID") from exc


def actor_from_roles(
    *,
    principal_id: UUID,
    workspace_id: UUID,
    email: str,
    roles: list[str],
    installation_admin: bool,
    session_id: UUID | None = None,
    csrf_token_hash: str | None = None,
    token_kind: str = "session",
) -> Actor:
    """Build an actor only after active membership was established by the adapter."""

    return Actor(
        principal_id=principal_id,
        workspace_id=workspace_id,
        email=email,
        permissions=permissions_for_roles(roles),
        installation_admin=installation_admin,
        session_id=session_id,
        csrf_token_hash=csrf_token_hash,
        token_kind=token_kind,
    )
