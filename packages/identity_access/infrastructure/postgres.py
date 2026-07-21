"""PostgreSQL adapter for the Identity and Workspace application port."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
import hmac
from typing import Any
from uuid import UUID, uuid4

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.identity_access.application.service import (
    BootstrapOutcome,
    Credential,
    Invitation,
    RepositoryConflict,
    WorkspaceOutcome,
    actor_from_roles,
)
from packages.identity_access.domain.policy import Actor, permissions_for_roles


Connect = Callable[[], Connection[Any]]


class PostgresIdentityRepository:
    """Persist identity state with transaction-scoped workspace predicates."""

    _BOOTSTRAP_LOCK = 2026072112

    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    @staticmethod
    def _audit(
        cursor: Any,
        *,
        workspace_id: UUID | None,
        actor_id: UUID | None,
        action: str,
        resource_type: str,
        resource_id: str,
        succeeded: bool = True,
        metadata: dict[str, object] | None = None,
    ) -> None:
        cursor.execute(
            """
            INSERT INTO identity_audit_events
                (id, workspace_id, actor_id, action, resource_type, resource_id,
                 succeeded, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                uuid4(),
                workspace_id,
                actor_id,
                action,
                resource_type,
                resource_id,
                succeeded,
                Jsonb(metadata or {}),
            ),
        )

    @staticmethod
    def _roles(cursor: Any, principal_id: UUID, workspace_id: UUID) -> list[str]:
        cursor.execute(
            """
            SELECT role
            FROM identity_role_assignments
            WHERE principal_id = %s AND workspace_id = %s
            ORDER BY role
            """,
            (principal_id, workspace_id),
        )
        return [str(row["role"]) for row in cursor.fetchall()]

    @staticmethod
    def _ensure_legacy_root_assignment(
        cursor: Any,
        *,
        workspace_id: UUID,
        workspace_name: str,
        principal_id: UUID,
        at: datetime,
    ) -> None:
        """Keep active memberships total while fail-closing legacy root scope."""

        cursor.execute(
            """
            SELECT id FROM organization_units
            WHERE workspace_id = %s AND key = 'company'
            """,
            (workspace_id,),
        )
        root = cursor.fetchone()
        if root is None:
            root_id = uuid4()
            cursor.execute(
                """
                INSERT INTO organization_units
                  (id, workspace_id, key, current_version, created_at, updated_at)
                VALUES (%s, %s, 'company', 1, %s, %s)
                """,
                (root_id, workspace_id, at, at),
            )
            cursor.execute(
                """
                INSERT INTO organization_unit_versions
                  (org_unit_id, version, kind, parent_org_unit_id, display_name,
                   status, effective_from, created_by, created_at)
                VALUES (%s, 1, 'company', NULL, %s, 'active', %s, %s, %s)
                """,
                (root_id, workspace_name, at, principal_id, at),
            )
        else:
            root_id = UUID(str(root["id"]))
        cursor.execute(
            """
            INSERT INTO organization_primary_assignments
              (id, workspace_id, principal_id, org_unit_id, effective_from,
               needs_department_assignment, assigned_by, created_at, updated_at)
            SELECT %s, %s, %s, %s, %s, TRUE, %s, %s, %s
            WHERE NOT EXISTS (
              SELECT 1 FROM organization_primary_assignments
              WHERE workspace_id = %s AND principal_id = %s
                AND effective_from <= %s
                AND (effective_to IS NULL OR effective_to > %s)
            )
            """,
            (
                uuid4(),
                workspace_id,
                principal_id,
                root_id,
                at,
                principal_id,
                at,
                at,
                workspace_id,
                principal_id,
                at,
                at,
            ),
        )

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
    ) -> BootstrapOutcome:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT pg_advisory_xact_lock(%s)", (self._BOOTSTRAP_LOCK,))
                cursor.execute("SELECT EXISTS (SELECT 1 FROM identity_principals) AS initialized")
                initialized = cursor.fetchone()
                if initialized is not None and bool(initialized["initialized"]):
                    raise RepositoryConflict("bootstrap-disabled")
                cursor.execute(
                    """
                    INSERT INTO identity_principals
                        (id, email, password_hash, installation_admin, active, created_at, updated_at)
                    VALUES (%s, %s, %s, TRUE, TRUE, %s, %s)
                    """,
                    (principal_id, email, password_hash, at, at),
                )
                cursor.execute(
                    """
                    INSERT INTO identity_workspaces (id, key, name, active, created_at, updated_at)
                    VALUES (%s, %s, %s, TRUE, %s, %s)
                    """,
                    (workspace_id, workspace_key, workspace_name, at, at),
                )
                cursor.execute(
                    """
                    INSERT INTO identity_memberships
                        (workspace_id, principal_id, status, created_at, updated_at)
                    VALUES (%s, %s, 'active', %s, %s)
                    """,
                    (workspace_id, principal_id, at, at),
                )
                cursor.execute(
                    """
                    INSERT INTO identity_role_assignments
                        (workspace_id, principal_id, role, assigned_by, created_at, updated_at)
                    VALUES (%s, %s, 'workspace_owner', %s, %s, %s)
                    """,
                    (workspace_id, principal_id, principal_id, at, at),
                )
                self._ensure_legacy_root_assignment(
                    cursor,
                    workspace_id=workspace_id,
                    workspace_name=workspace_name,
                    principal_id=principal_id,
                    at=at,
                )
                cursor.execute(
                    """
                    INSERT INTO identity_bootstrap_state
                        (singleton, principal_id, workspace_id, completed_at)
                    VALUES (TRUE, %s, %s, %s)
                    """,
                    (principal_id, workspace_id, at),
                )
                self._audit(
                    cursor,
                    workspace_id=workspace_id,
                    actor_id=principal_id,
                    action="identity.bootstrap.completed",
                    resource_type="workspace",
                    resource_id=str(workspace_id),
                )
        return BootstrapOutcome(principal_id, workspace_id, workspace_key)

    def create_workspace(
        self,
        *,
        actor: Actor,
        workspace_id: UUID,
        workspace_key: str,
        name: str,
        at: datetime,
    ) -> WorkspaceOutcome:
        try:
            with self._connect() as connection, connection.transaction():
                with connection.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                        """
                        INSERT INTO identity_workspaces
                            (id, key, name, active, created_at, updated_at)
                        VALUES (%s, %s, %s, TRUE, %s, %s)
                        """,
                        (workspace_id, workspace_key, name, at, at),
                    )
                    cursor.execute(
                        """
                        INSERT INTO identity_memberships
                            (workspace_id, principal_id, status, created_at, updated_at)
                        VALUES (%s, %s, 'active', %s, %s)
                        """,
                        (workspace_id, actor.principal_id, at, at),
                    )
                    cursor.execute(
                        """
                        INSERT INTO identity_role_assignments
                            (workspace_id, principal_id, role, assigned_by, created_at, updated_at)
                        VALUES (%s, %s, 'workspace_owner', %s, %s, %s)
                        """,
                        (workspace_id, actor.principal_id, actor.principal_id, at, at),
                    )
                    self._ensure_legacy_root_assignment(
                        cursor,
                        workspace_id=workspace_id,
                        workspace_name=name,
                        principal_id=actor.principal_id,
                        at=at,
                    )
                    self._audit(
                        cursor,
                        workspace_id=workspace_id,
                        actor_id=actor.principal_id,
                        action="workspace.created",
                        resource_type="workspace",
                        resource_id=str(workspace_id),
                    )
        except Exception as exc:
            if getattr(exc, "sqlstate", None) == "23505":
                raise RepositoryConflict("workspace-conflict") from exc
            raise
        return WorkspaceOutcome(workspace_id, workspace_key, name)

    def credential_for_login(self, email: str, workspace_id: UUID) -> Credential | None:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT p.id, p.email, p.password_hash, p.active, p.installation_admin
                FROM identity_principals AS p
                JOIN identity_memberships AS m ON m.principal_id = p.id
                JOIN identity_workspaces AS w ON w.id = m.workspace_id
                WHERE p.email = %s AND m.workspace_id = %s
                  AND m.status = 'active' AND w.active AND p.active
                """,
                (email, workspace_id),
            )
            row = cursor.fetchone()
        return self._credential(row)

    def credential_by_email(self, email: str) -> Credential | None:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash, active, installation_admin
                FROM identity_principals WHERE email = %s
                """,
                (email,),
            )
            row = cursor.fetchone()
        return self._credential(row)

    @staticmethod
    def _credential(row: dict[str, object] | None) -> Credential | None:
        if row is None:
            return None
        return Credential(
            principal_id=UUID(str(row["id"])),
            email=str(row["email"]),
            password_hash=str(row["password_hash"]),
            active=bool(row["active"]),
            installation_admin=bool(row["installation_admin"]),
        )

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
    ) -> None:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO identity_sessions
                        (id, family_id, principal_id, workspace_id, access_token_hash,
                         refresh_token_hash, csrf_token_hash, device_label, access_expires_at,
                         absolute_expires_at, last_seen_at, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        session_id,
                        family_id,
                        principal_id,
                        workspace_id,
                        access_hash,
                        refresh_hash,
                        csrf_hash,
                        device_label,
                        access_expires_at,
                        absolute_expires_at,
                        at,
                        at,
                        at,
                    ),
                )
                self._audit(
                    cursor,
                    workspace_id=workspace_id,
                    actor_id=principal_id,
                    action="session.created",
                    resource_type="session",
                    resource_id=str(session_id),
                )

    def actor_for_access(self, token_hash: str, at: datetime) -> Actor | None:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT s.id AS session_id, s.workspace_id, s.csrf_token_hash,
                           p.id AS principal_id, p.email, p.installation_admin
                    FROM identity_sessions AS s
                    JOIN identity_principals AS p ON p.id = s.principal_id
                    JOIN identity_memberships AS m
                      ON m.principal_id = s.principal_id AND m.workspace_id = s.workspace_id
                    JOIN identity_workspaces AS w ON w.id = s.workspace_id
                    WHERE s.access_token_hash = %s AND s.revoked_at IS NULL
                      AND s.access_expires_at > %s AND s.absolute_expires_at > %s
                      AND p.active AND m.status = 'active' AND w.active
                    """,
                    (token_hash, at, at),
                )
                row = cursor.fetchone()
                if row is None:
                    return None
                principal_id = UUID(str(row["principal_id"]))
                workspace_id = UUID(str(row["workspace_id"]))
                roles = self._roles(cursor, principal_id, workspace_id)
                if not roles:
                    return None
                cursor.execute(
                    "UPDATE identity_sessions SET last_seen_at = %s, updated_at = %s WHERE id = %s",
                    (at, at, row["session_id"]),
                )
                return actor_from_roles(
                    principal_id=principal_id,
                    workspace_id=workspace_id,
                    email=str(row["email"]),
                    roles=roles,
                    installation_admin=bool(row["installation_admin"]),
                    session_id=UUID(str(row["session_id"])),
                    csrf_token_hash=str(row["csrf_token_hash"]),
                )

    def actor_for_api_token(self, token_hash: str, at: datetime) -> Actor | None:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT t.id AS token_id, t.workspace_id, t.scopes,
                           p.id AS principal_id, p.email, p.installation_admin
                    FROM identity_api_tokens AS t
                    JOIN identity_principals AS p ON p.id = t.principal_id
                    JOIN identity_memberships AS m
                      ON m.principal_id = t.principal_id AND m.workspace_id = t.workspace_id
                    JOIN identity_workspaces AS w ON w.id = t.workspace_id
                    WHERE t.token_hash = %s AND t.revoked_at IS NULL AND t.expires_at > %s
                      AND p.active AND m.status = 'active' AND w.active
                    """,
                    (token_hash, at),
                )
                row = cursor.fetchone()
                if row is None:
                    return None
                principal_id = UUID(str(row["principal_id"]))
                workspace_id = UUID(str(row["workspace_id"]))
                roles = self._roles(cursor, principal_id, workspace_id)
                if not roles:
                    return None
                permitted = permissions_for_roles(roles).intersection(
                    str(scope) for scope in row["scopes"]
                )
                if not permitted:
                    return None
                cursor.execute(
                    "UPDATE identity_api_tokens SET last_used_at = %s, updated_at = %s WHERE id = %s",
                    (at, at, row["token_id"]),
                )
                return Actor(
                    principal_id=principal_id,
                    workspace_id=workspace_id,
                    email=str(row["email"]),
                    permissions=frozenset(permitted),
                    installation_admin=False,
                    token_kind="api_token",
                )

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
    ) -> tuple[UUID, UUID, datetime]:
        reused = False
        outcome: tuple[UUID, UUID, datetime] | None = None
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT id, family_id, principal_id, workspace_id, absolute_expires_at,
                           revoked_at, csrf_token_hash
                    FROM identity_sessions
                    WHERE refresh_token_hash = %s
                    FOR UPDATE
                    """,
                    (presented_hash,),
                )
                row = cursor.fetchone()
                if row is None:
                    cursor.execute(
                        """
                        SELECT h.family_id, s.workspace_id, s.principal_id
                        FROM identity_refresh_history AS h
                        JOIN identity_sessions AS s ON s.id = h.session_id
                        WHERE h.token_hash = %s
                        FOR UPDATE OF s
                        """,
                        (presented_hash,),
                    )
                    replay = cursor.fetchone()
                    if replay is None:
                        raise RepositoryConflict("refresh-invalid")
                    cursor.execute(
                        """
                        UPDATE identity_sessions
                        SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                        WHERE family_id = %s
                        """,
                        (at, at, replay["family_id"]),
                    )
                    self._audit(
                        cursor,
                        workspace_id=UUID(str(replay["workspace_id"])),
                        actor_id=UUID(str(replay["principal_id"])),
                        action="session.refresh_reuse_detected",
                        resource_type="session_family",
                        resource_id=str(replay["family_id"]),
                    )
                    reused = True
                elif row["revoked_at"] is not None or row["absolute_expires_at"] <= at:
                    raise RepositoryConflict("refresh-invalid")
                elif not hmac.compare_digest(str(row["csrf_token_hash"]), presented_csrf_hash):
                    raise RepositoryConflict("refresh-invalid")
                else:
                    cursor.execute(
                        """
                        INSERT INTO identity_refresh_history
                            (token_hash, session_id, family_id, rotated_at)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (presented_hash, row["id"], row["family_id"], at),
                    )
                    cursor.execute(
                        """
                        UPDATE identity_sessions
                        SET access_token_hash = %s, refresh_token_hash = %s,
                            csrf_token_hash = %s, access_expires_at = %s,
                            last_seen_at = %s, updated_at = %s
                        WHERE id = %s
                        """,
                        (
                            access_hash,
                            refresh_hash,
                            csrf_hash,
                            access_expires_at,
                            at,
                            at,
                            row["id"],
                        ),
                    )
                    self._audit(
                        cursor,
                        workspace_id=UUID(str(row["workspace_id"])),
                        actor_id=UUID(str(row["principal_id"])),
                        action="session.rotated",
                        resource_type="session",
                        resource_id=str(row["id"]),
                    )
                    outcome = (
                        UUID(str(row["id"])),
                        UUID(str(row["workspace_id"])),
                        row["absolute_expires_at"],
                    )
        if reused:
            raise RepositoryConflict("refresh-reuse")
        if outcome is None:
            raise RepositoryConflict("refresh-invalid")
        return outcome

    def revoke_session(self, actor: Actor, session_id: UUID, at: datetime) -> bool:
        can_manage_workspace = "workspace.sessions.manage" in actor.permissions
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE identity_sessions
                    SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                    WHERE id = %s AND workspace_id = %s
                      AND (%s OR principal_id = %s)
                    RETURNING principal_id
                    """,
                    (
                        at,
                        at,
                        session_id,
                        actor.workspace_id,
                        can_manage_workspace,
                        actor.principal_id,
                    ),
                )
                row = cursor.fetchone()
                if row is None:
                    return False
                self._audit(
                    cursor,
                    workspace_id=actor.workspace_id,
                    actor_id=actor.principal_id,
                    action="session.revoked",
                    resource_type="session",
                    resource_id=str(session_id),
                )
                return True

    def revoke_current_refresh(self, refresh_hash: str, csrf_hash: str, at: datetime) -> bool:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE identity_sessions
                    SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                    WHERE refresh_token_hash = %s AND csrf_token_hash = %s
                      AND revoked_at IS NULL
                    RETURNING id, workspace_id, principal_id
                    """,
                    (at, at, refresh_hash, csrf_hash),
                )
                row = cursor.fetchone()
                if row is None:
                    return False
                self._audit(
                    cursor,
                    workspace_id=UUID(str(row["workspace_id"])),
                    actor_id=UUID(str(row["principal_id"])),
                    action="session.logout",
                    resource_type="session",
                    resource_id=str(row["id"]),
                )
                return True

    def revoke_all_sessions(self, principal_id: UUID, at: datetime) -> int:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE identity_sessions
                    SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                    WHERE principal_id = %s AND revoked_at IS NULL
                    """,
                    (at, at, principal_id),
                )
                count = cursor.rowcount
                self._audit(
                    cursor,
                    workspace_id=None,
                    actor_id=principal_id,
                    action="session.logout_all",
                    resource_type="principal",
                    resource_id=str(principal_id),
                    metadata={"revoked_count": count},
                )
                return count

    def list_sessions(self, actor: Actor, principal_id: UUID | None) -> list[dict[str, object]]:
        target = principal_id or actor.principal_id
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, device_label, created_at, last_seen_at, absolute_expires_at,
                       revoked_at IS NOT NULL AS revoked
                FROM identity_sessions
                WHERE workspace_id = %s AND principal_id = %s
                ORDER BY created_at DESC
                """,
                (actor.workspace_id, target),
            )
            return [dict(row) for row in cursor.fetchall()]

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
    ) -> None:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO identity_invitations
                        (id, workspace_id, email, token_hash, roles, invited_by,
                         expires_at, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        invitation_id,
                        actor.workspace_id,
                        email,
                        token_hash,
                        Jsonb(list(roles)),
                        actor.principal_id,
                        expires_at,
                        at,
                        at,
                    ),
                )
                self._audit(
                    cursor,
                    workspace_id=actor.workspace_id,
                    actor_id=actor.principal_id,
                    action="invitation.created",
                    resource_type="invitation",
                    resource_id=str(invitation_id),
                    metadata={"roles": list(roles)},
                )

    def invitation_for_token(self, token_hash: str) -> Invitation | None:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, workspace_id, email, roles, expires_at,
                       accepted_at IS NOT NULL AS accepted,
                       revoked_at IS NOT NULL AS revoked
                FROM identity_invitations WHERE token_hash = %s
                """,
                (token_hash,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return Invitation(
            invitation_id=UUID(str(row["id"])),
            workspace_id=UUID(str(row["workspace_id"])),
            email=str(row["email"]),
            roles=tuple(str(role) for role in row["roles"]),
            expires_at=row["expires_at"],
            accepted=bool(row["accepted"]),
            revoked=bool(row["revoked"]),
        )

    def revoke_invitation(self, actor: Actor, invitation_id: UUID, at: datetime) -> bool:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE identity_invitations
                    SET revoked_at = %s, updated_at = %s
                    WHERE id = %s AND workspace_id = %s
                      AND accepted_at IS NULL AND revoked_at IS NULL
                    RETURNING id
                    """,
                    (at, at, invitation_id, actor.workspace_id),
                )
                if cursor.fetchone() is None:
                    return False
                self._audit(
                    cursor,
                    workspace_id=actor.workspace_id,
                    actor_id=actor.principal_id,
                    action="invitation.revoked",
                    resource_type="invitation",
                    resource_id=str(invitation_id),
                )
                return True

    def accept_invitation(
        self,
        *,
        invitation: Invitation,
        token_hash: str,
        principal_id: UUID,
        password_hash: str | None,
        at: datetime,
    ) -> UUID:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT i.id, i.workspace_id, i.email, i.roles, i.expires_at,
                           i.accepted_at, i.revoked_at, w.name AS workspace_name
                    FROM identity_invitations AS i
                    JOIN identity_workspaces AS w ON w.id = i.workspace_id
                    WHERE i.token_hash = %s FOR UPDATE OF i
                    """,
                    (token_hash,),
                )
                row = cursor.fetchone()
                if (
                    row is None
                    or UUID(str(row["id"])) != invitation.invitation_id
                    or row["accepted_at"] is not None
                    or row["revoked_at"] is not None
                    or row["expires_at"] <= at
                ):
                    raise RepositoryConflict("invitation-invalid")
                if password_hash is not None:
                    cursor.execute(
                        """
                        INSERT INTO identity_principals
                            (id, email, password_hash, installation_admin, active,
                             created_at, updated_at)
                        VALUES (%s, %s, %s, FALSE, TRUE, %s, %s)
                        """,
                        (principal_id, row["email"], password_hash, at, at),
                    )
                cursor.execute(
                    """
                    INSERT INTO identity_memberships
                        (workspace_id, principal_id, status, created_at, updated_at)
                    VALUES (%s, %s, 'active', %s, %s)
                    ON CONFLICT (workspace_id, principal_id) DO NOTHING
                    """,
                    (row["workspace_id"], principal_id, at, at),
                )
                for role in row["roles"]:
                    cursor.execute(
                        """
                        INSERT INTO identity_role_assignments
                            (workspace_id, principal_id, role, assigned_by, created_at, updated_at)
                        VALUES (%s, %s, %s, NULL, %s, %s)
                        ON CONFLICT (workspace_id, principal_id, role) DO NOTHING
                        """,
                        (row["workspace_id"], principal_id, role, at, at),
                    )
                self._ensure_legacy_root_assignment(
                    cursor,
                    workspace_id=UUID(str(row["workspace_id"])),
                    workspace_name=str(row["workspace_name"]),
                    principal_id=principal_id,
                    at=at,
                )
                cursor.execute(
                    """
                    UPDATE identity_invitations SET accepted_at = %s, updated_at = %s
                    WHERE id = %s
                    """,
                    (at, at, row["id"]),
                )
                self._audit(
                    cursor,
                    workspace_id=UUID(str(row["workspace_id"])),
                    actor_id=principal_id,
                    action="invitation.accepted",
                    resource_type="invitation",
                    resource_id=str(row["id"]),
                )
        return principal_id

    def list_members(self, actor: Actor, workspace_id: UUID) -> list[dict[str, object]]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT p.id, p.email, m.status,
                       COALESCE(array_agg(r.role ORDER BY r.role)
                         FILTER (WHERE r.role IS NOT NULL), ARRAY[]::varchar[]) AS roles
                FROM identity_memberships AS m
                JOIN identity_principals AS p ON p.id = m.principal_id
                LEFT JOIN identity_role_assignments AS r
                  ON r.workspace_id = m.workspace_id AND r.principal_id = m.principal_id
                WHERE m.workspace_id = %s
                GROUP BY p.id, p.email, m.status
                ORDER BY p.email
                """,
                (workspace_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

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
    ) -> None:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO identity_api_tokens
                        (id, workspace_id, principal_id, name, token_hash, scopes,
                         expires_at, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        token_id,
                        actor.workspace_id,
                        actor.principal_id,
                        name,
                        token_hash,
                        Jsonb(list(scopes)),
                        expires_at,
                        at,
                        at,
                    ),
                )
                self._audit(
                    cursor,
                    workspace_id=actor.workspace_id,
                    actor_id=actor.principal_id,
                    action="api_token.created",
                    resource_type="api_token",
                    resource_id=str(token_id),
                    metadata={"scopes": list(scopes)},
                )

    def revoke_api_token(self, actor: Actor, token_id: UUID, at: datetime) -> bool:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE identity_api_tokens
                    SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                    WHERE id = %s AND workspace_id = %s AND principal_id = %s
                    RETURNING id
                    """,
                    (at, at, token_id, actor.workspace_id, actor.principal_id),
                )
                if cursor.fetchone() is None:
                    return False
                self._audit(
                    cursor,
                    workspace_id=actor.workspace_id,
                    actor_id=actor.principal_id,
                    action="api_token.revoked",
                    resource_type="api_token",
                    resource_id=str(token_id),
                )
                return True

    def change_password(self, principal_id: UUID, password_hash: str, at: datetime) -> None:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE identity_principals SET password_hash = %s, updated_at = %s
                    WHERE id = %s AND active
                    """,
                    (password_hash, at, principal_id),
                )
                cursor.execute(
                    """
                    UPDATE identity_sessions SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                    WHERE principal_id = %s
                    """,
                    (at, at, principal_id),
                )
                self._audit(
                    cursor,
                    workspace_id=None,
                    actor_id=principal_id,
                    action="password.changed",
                    resource_type="principal",
                    resource_id=str(principal_id),
                )

    def create_password_reset(
        self,
        *,
        actor: Actor,
        reset_id: UUID,
        principal_id: UUID,
        token_hash: str,
        expires_at: datetime,
        at: datetime,
    ) -> None:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT 1 FROM identity_memberships
                    WHERE workspace_id = %s AND principal_id = %s AND status = 'active'
                    """,
                    (actor.workspace_id, principal_id),
                )
                if cursor.fetchone() is None:
                    raise RepositoryConflict("principal-not-found")
                cursor.execute(
                    """
                    UPDATE identity_password_resets
                    SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                    WHERE principal_id = %s AND used_at IS NULL AND revoked_at IS NULL
                    """,
                    (at, at, principal_id),
                )
                cursor.execute(
                    """
                    INSERT INTO identity_password_resets
                        (id, principal_id, token_hash, expires_at, created_by, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (reset_id, principal_id, token_hash, expires_at, actor.principal_id, at, at),
                )
                self._audit(
                    cursor,
                    workspace_id=actor.workspace_id,
                    actor_id=actor.principal_id,
                    action="password_reset.created",
                    resource_type="principal",
                    resource_id=str(principal_id),
                )

    def consume_password_reset(self, token_hash: str, password_hash: str, at: datetime) -> UUID:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT id, principal_id FROM identity_password_resets
                    WHERE token_hash = %s AND used_at IS NULL AND revoked_at IS NULL
                      AND expires_at > %s
                    FOR UPDATE
                    """,
                    (token_hash, at),
                )
                row = cursor.fetchone()
                if row is None:
                    raise RepositoryConflict("password-reset-invalid")
                principal_id = UUID(str(row["principal_id"]))
                cursor.execute(
                    "UPDATE identity_password_resets SET used_at = %s, updated_at = %s WHERE id = %s",
                    (at, at, row["id"]),
                )
                cursor.execute(
                    "UPDATE identity_principals SET password_hash = %s, updated_at = %s WHERE id = %s",
                    (password_hash, at, principal_id),
                )
                cursor.execute(
                    """
                    UPDATE identity_sessions SET revoked_at = COALESCE(revoked_at, %s), updated_at = %s
                    WHERE principal_id = %s
                    """,
                    (at, at, principal_id),
                )
                self._audit(
                    cursor,
                    workspace_id=None,
                    actor_id=principal_id,
                    action="password_reset.consumed",
                    resource_type="principal",
                    resource_id=str(principal_id),
                )
                return principal_id
