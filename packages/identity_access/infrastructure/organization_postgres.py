"""PostgreSQL adapter for organization hierarchy and effective access."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.identity_access.application.organization import ResourceCandidate
from packages.identity_access.application.service import RepositoryConflict
from packages.identity_access.domain.policy import Actor, permissions_for_roles


Connect = Callable[[], Connection[Any]]


class PostgresOrganizationRepository:
    """Own organization state and enforce workspace predicates transactionally."""

    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    @staticmethod
    def _lock_workspace(cursor: Any, workspace_id: UUID) -> None:
        cursor.execute(
            "SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))",
            (f"organization:{workspace_id}",),
        )

    @staticmethod
    def _audit(
        cursor: Any,
        *,
        actor: Actor,
        action: str,
        resource_type: str,
        resource_id: UUID,
        metadata: dict[str, object] | None = None,
    ) -> None:
        cursor.execute(
            """
            INSERT INTO identity_audit_events
              (id, workspace_id, actor_id, action, resource_type, resource_id,
               succeeded, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE, %s)
            """,
            (
                uuid4(),
                actor.workspace_id,
                actor.principal_id,
                action,
                resource_type,
                str(resource_id),
                Jsonb(metadata or {}),
            ),
        )

    @staticmethod
    def _unit(cursor: Any, workspace_id: UUID, org_unit_id: UUID, *, lock: bool = False) -> Any:
        cursor.execute(
            f"""
            SELECT u.id, u.workspace_id, u.key, u.current_version, v.kind,
                   v.parent_org_unit_id, v.display_name, v.status,
                   v.effective_from, v.effective_to, v.successor_org_unit_id
            FROM organization_units AS u
            JOIN organization_unit_versions AS v
              ON v.org_unit_id = u.id AND v.version = u.current_version
            WHERE u.id = %s AND u.workspace_id = %s
            {"FOR UPDATE OF u" if lock else ""}
            """,
            (org_unit_id, workspace_id),
        )
        row = cursor.fetchone()
        if row is None:
            raise RepositoryConflict("workspace-mismatch")
        return row

    @classmethod
    def _active_unit(cls, cursor: Any, workspace_id: UUID, org_unit_id: UUID) -> Any:
        row = cls._unit(cursor, workspace_id, org_unit_id)
        if row["status"] != "active":
            raise RepositoryConflict("not-found")
        return row

    @staticmethod
    def _is_descendant(cursor: Any, descendant_id: UUID, ancestor_id: UUID) -> bool:
        cursor.execute(
            """
            WITH RECURSIVE lineage(id) AS (
              SELECT %s::uuid
              UNION ALL
              SELECT v.parent_org_unit_id
              FROM lineage AS l
              JOIN organization_units AS u ON u.id = l.id
              JOIN organization_unit_versions AS v
                ON v.org_unit_id = u.id AND v.version = u.current_version
              WHERE v.parent_org_unit_id IS NOT NULL
            )
            SELECT EXISTS (SELECT 1 FROM lineage WHERE id = %s) AS matches
            """,
            (descendant_id, ancestor_id),
        )
        row = cursor.fetchone()
        return bool(row and row["matches"])

    @staticmethod
    def _membership(cursor: Any, workspace_id: UUID, principal_id: UUID) -> Any:
        cursor.execute(
            """
            SELECT status FROM identity_memberships
            WHERE workspace_id = %s AND principal_id = %s
            """,
            (workspace_id, principal_id),
        )
        row = cursor.fetchone()
        if row is None:
            raise RepositoryConflict("not-found")
        return row

    @staticmethod
    def _serialize_unit(row: Any) -> dict[str, object]:
        return {
            "org_unit_id": UUID(str(row["id"])),
            "workspace_id": UUID(str(row["workspace_id"])),
            "key": str(row["key"]),
            "version": int(row["current_version"]),
            "kind": str(row["kind"]),
            "parent_org_unit_id": (
                UUID(str(row["parent_org_unit_id"]))
                if row["parent_org_unit_id"] is not None
                else None
            ),
            "display_name": str(row["display_name"]),
            "status": str(row["status"]),
            "effective_from": row["effective_from"],
            "effective_to": row["effective_to"],
            "successor_org_unit_id": (
                UUID(str(row["successor_org_unit_id"]))
                if row["successor_org_unit_id"] is not None
                else None
            ),
        }

    @staticmethod
    def _allowed_parent(child_kind: str, parent_kind: str) -> bool:
        allowed = {
            "division": {"company"},
            "department": {"company", "division"},
            "team": {"department", "team"},
        }
        return parent_kind in allowed.get(child_kind, set())

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
    ) -> dict[str, object]:
        try:
            with self._connect() as connection, connection.transaction():
                with connection.cursor(row_factory=dict_row) as cursor:
                    self._lock_workspace(cursor, actor.workspace_id)
                    if parent_org_unit_id is None:
                        cursor.execute(
                            """
                            SELECT 1 FROM organization_units AS u
                            JOIN organization_unit_versions AS v
                              ON v.org_unit_id = u.id AND v.version = u.current_version
                            WHERE u.workspace_id = %s AND v.kind = 'company'
                            LIMIT 1
                            """,
                            (actor.workspace_id,),
                        )
                        if cursor.fetchone() is not None:
                            raise RepositoryConflict("root-exists")
                    else:
                        parent = self._active_unit(
                            cursor, actor.workspace_id, parent_org_unit_id
                        )
                        if not self._allowed_parent(kind, str(parent["kind"])):
                            raise RepositoryConflict("invalid-parent-kind")
                    cursor.execute(
                        """
                        INSERT INTO organization_units
                          (id, workspace_id, key, current_version, created_at, updated_at)
                        VALUES (%s, %s, %s, 1, %s, %s)
                        """,
                        (org_unit_id, actor.workspace_id, key, effective_from, effective_from),
                    )
                    cursor.execute(
                        """
                        INSERT INTO organization_unit_versions
                          (org_unit_id, version, kind, parent_org_unit_id, display_name,
                           status, effective_from, created_by, created_at)
                        VALUES (%s, 1, %s, %s, %s, 'active', %s, %s, %s)
                        """,
                        (
                            org_unit_id,
                            kind,
                            parent_org_unit_id,
                            display_name,
                            effective_from,
                            actor.principal_id,
                            effective_from,
                        ),
                    )
                    self._audit(
                        cursor,
                        actor=actor,
                        action="organization.unit.created",
                        resource_type="org_unit",
                        resource_id=org_unit_id,
                        metadata={"version": 1, "kind": kind},
                    )
                    row = self._unit(cursor, actor.workspace_id, org_unit_id)
            return self._serialize_unit(row)
        except psycopg.errors.UniqueViolation as exc:
            raise RepositoryConflict("unit-conflict") from exc

    def version_unit(
        self,
        *,
        actor: Actor,
        org_unit_id: UUID,
        expected_version: int,
        parent_org_unit_id: UUID | None,
        display_name: str,
        effective_from: datetime,
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                self._lock_workspace(cursor, actor.workspace_id)
                current = self._unit(cursor, actor.workspace_id, org_unit_id, lock=True)
                if int(current["current_version"]) != expected_version:
                    raise RepositoryConflict("stale-version")
                kind = str(current["kind"])
                if kind == "company" and parent_org_unit_id is not None:
                    raise RepositoryConflict("invalid-parent-kind")
                if kind != "company":
                    if parent_org_unit_id is None:
                        raise RepositoryConflict("invalid-parent-kind")
                    parent = self._active_unit(cursor, actor.workspace_id, parent_org_unit_id)
                    if not self._allowed_parent(kind, str(parent["kind"])):
                        raise RepositoryConflict("invalid-parent-kind")
                    if self._is_descendant(cursor, parent_org_unit_id, org_unit_id):
                        raise RepositoryConflict("cycle")
                next_version = expected_version + 1
                cursor.execute(
                    """
                    UPDATE organization_unit_versions SET effective_to = %s
                    WHERE org_unit_id = %s AND version = %s
                      AND (effective_to IS NULL OR effective_to > %s)
                    """,
                    (effective_from, org_unit_id, expected_version, effective_from),
                )
                cursor.execute(
                    """
                    INSERT INTO organization_unit_versions
                      (org_unit_id, version, kind, parent_org_unit_id, display_name,
                       status, effective_from, successor_org_unit_id, created_by, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        org_unit_id,
                        next_version,
                        kind,
                        parent_org_unit_id,
                        display_name,
                        current["status"],
                        effective_from,
                        current["successor_org_unit_id"],
                        actor.principal_id,
                        effective_from,
                    ),
                )
                cursor.execute(
                    """
                    UPDATE organization_units
                    SET current_version = %s, updated_at = %s WHERE id = %s
                    """,
                    (next_version, effective_from, org_unit_id),
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.unit.versioned",
                    resource_type="org_unit",
                    resource_id=org_unit_id,
                    metadata={"from_version": expected_version, "to_version": next_version},
                )
                row = self._unit(cursor, actor.workspace_id, org_unit_id)
        return self._serialize_unit(row)

    def close_unit(
        self,
        *,
        actor: Actor,
        org_unit_id: UUID,
        expected_version: int,
        status: str,
        successor_org_unit_id: UUID | None,
        effective_from: datetime,
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                self._lock_workspace(cursor, actor.workspace_id)
                current = self._unit(cursor, actor.workspace_id, org_unit_id, lock=True)
                if int(current["current_version"]) != expected_version:
                    raise RepositoryConflict("stale-version")
                if current["kind"] == "company":
                    raise RepositoryConflict("handover-required")
                cursor.execute(
                    """
                    SELECT EXISTS (
                      SELECT 1 FROM organization_primary_assignments
                      WHERE workspace_id = %s AND org_unit_id = %s
                        AND effective_from <= %s
                        AND (effective_to IS NULL OR effective_to > %s)
                      UNION ALL
                      SELECT 1 FROM organization_resource_ownership_bindings
                      WHERE workspace_id = %s AND owner_type = 'org_unit' AND owner_id = %s
                        AND effective_from <= %s
                        AND (effective_to IS NULL OR effective_to > %s)
                    ) AS has_dependants
                    """,
                    (
                        actor.workspace_id,
                        org_unit_id,
                        effective_from,
                        effective_from,
                        actor.workspace_id,
                        org_unit_id,
                        effective_from,
                        effective_from,
                    ),
                )
                dependant_row = cursor.fetchone()
                if dependant_row is None:
                    raise RepositoryConflict("not-found")
                has_dependants = bool(dependant_row["has_dependants"])
                if has_dependants and successor_org_unit_id is None:
                    raise RepositoryConflict("handover-required")
                if successor_org_unit_id is not None:
                    if successor_org_unit_id == org_unit_id:
                        raise RepositoryConflict("handover-required")
                    successor = self._active_unit(
                        cursor, actor.workspace_id, successor_org_unit_id
                    )
                    if successor["kind"] not in {"department", "team"}:
                        raise RepositoryConflict("handover-required")
                    cursor.execute(
                        """
                        SELECT principal_id FROM organization_primary_assignments
                        WHERE workspace_id = %s AND org_unit_id = %s
                          AND effective_from <= %s
                          AND (effective_to IS NULL OR effective_to > %s)
                        FOR UPDATE
                        """,
                        (actor.workspace_id, org_unit_id, effective_from, effective_from),
                    )
                    principals = [UUID(str(row["principal_id"])) for row in cursor.fetchall()]
                    cursor.execute(
                        """
                        UPDATE organization_primary_assignments
                        SET effective_to = %s, updated_at = %s
                        WHERE workspace_id = %s AND org_unit_id = %s
                          AND effective_from < %s
                          AND (effective_to IS NULL OR effective_to > %s)
                        """,
                        (
                            effective_from,
                            effective_from,
                            actor.workspace_id,
                            org_unit_id,
                            effective_from,
                            effective_from,
                        ),
                    )
                    for principal_id in principals:
                        cursor.execute(
                            """
                            INSERT INTO organization_primary_assignments
                              (id, workspace_id, principal_id, org_unit_id, effective_from,
                               assigned_by, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                uuid4(),
                                actor.workspace_id,
                                principal_id,
                                successor_org_unit_id,
                                effective_from,
                                actor.principal_id,
                                effective_from,
                                effective_from,
                            ),
                        )
                    cursor.execute(
                        """
                        SELECT * FROM organization_resource_ownership_bindings
                        WHERE workspace_id = %s AND owner_type = 'org_unit' AND owner_id = %s
                          AND effective_from <= %s
                          AND (effective_to IS NULL OR effective_to > %s)
                        FOR UPDATE
                        """,
                        (actor.workspace_id, org_unit_id, effective_from, effective_from),
                    )
                    bindings = cursor.fetchall()
                    for binding in bindings:
                        cursor.execute(
                            """
                            UPDATE organization_resource_ownership_bindings
                            SET effective_to = %s, updated_at = %s WHERE id = %s
                            """,
                            (effective_from, effective_from, binding["id"]),
                        )
                        cursor.execute(
                            """
                            INSERT INTO organization_resource_ownership_bindings
                              (id, workspace_id, resource_type, resource_id,
                               creator_principal_id, owner_type, owner_id, allowed_actions,
                               required_row_scope_refs, required_column_policy_refs,
                               requires_pii, effective_from, version, bound_by,
                               created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, 'org_unit', %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                uuid4(),
                                actor.workspace_id,
                                binding["resource_type"],
                                binding["resource_id"],
                                binding["creator_principal_id"],
                                successor_org_unit_id,
                                Jsonb(binding["allowed_actions"]),
                                Jsonb(binding["required_row_scope_refs"]),
                                Jsonb(binding["required_column_policy_refs"]),
                                binding["requires_pii"],
                                effective_from,
                                int(binding["version"]) + 1,
                                actor.principal_id,
                                effective_from,
                                effective_from,
                            ),
                        )
                next_version = expected_version + 1
                cursor.execute(
                    """
                    UPDATE organization_unit_versions SET effective_to = %s
                    WHERE org_unit_id = %s AND version = %s
                    """,
                    (effective_from, org_unit_id, expected_version),
                )
                cursor.execute(
                    """
                    INSERT INTO organization_unit_versions
                      (org_unit_id, version, kind, parent_org_unit_id, display_name,
                       status, effective_from, successor_org_unit_id, created_by, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        org_unit_id,
                        next_version,
                        current["kind"],
                        current["parent_org_unit_id"],
                        current["display_name"],
                        status,
                        effective_from,
                        successor_org_unit_id,
                        actor.principal_id,
                        effective_from,
                    ),
                )
                cursor.execute(
                    """
                    UPDATE organization_units
                    SET current_version = %s, updated_at = %s WHERE id = %s
                    """,
                    (next_version, effective_from, org_unit_id),
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.unit.closed",
                    resource_type="org_unit",
                    resource_id=org_unit_id,
                    metadata={"status": status, "successor": str(successor_org_unit_id or "")},
                )
                row = self._unit(cursor, actor.workspace_id, org_unit_id)
        return self._serialize_unit(row)

    def list_units(self, actor: Actor) -> list[dict[str, object]]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT u.id, u.workspace_id, u.key, u.current_version, v.kind,
                       v.parent_org_unit_id, v.display_name, v.status,
                       v.effective_from, v.effective_to, v.successor_org_unit_id
                FROM organization_units AS u
                JOIN organization_unit_versions AS v
                  ON v.org_unit_id = u.id AND v.version = u.current_version
                WHERE u.workspace_id = %s
                ORDER BY v.kind, u.key
                """,
                (actor.workspace_id,),
            )
            rows = cursor.fetchall()
        return [self._serialize_unit(row) for row in rows]

    def assign_primary(
        self,
        *,
        actor: Actor,
        assignment_id: UUID,
        principal_id: UUID,
        org_unit_id: UUID,
        effective_from: datetime,
        effective_to: datetime | None,
    ) -> dict[str, object]:
        try:
            with self._connect() as connection, connection.transaction():
                with connection.cursor(row_factory=dict_row) as cursor:
                    member = self._membership(cursor, actor.workspace_id, principal_id)
                    if member["status"] != "active":
                        raise RepositoryConflict("not-found")
                    unit = self._active_unit(cursor, actor.workspace_id, org_unit_id)
                    if unit["kind"] not in {"department", "team"}:
                        raise RepositoryConflict("invalid-primary-unit")
                    cursor.execute(
                        """
                        SELECT id, effective_from, needs_department_assignment
                        FROM organization_primary_assignments
                        WHERE workspace_id = %s AND principal_id = %s
                          AND effective_from <= %s
                          AND (effective_to IS NULL OR effective_to > %s)
                        FOR UPDATE
                        """,
                        (actor.workspace_id, principal_id, effective_from, effective_from),
                    )
                    current = cursor.fetchone()
                    if current is not None and bool(current["needs_department_assignment"]):
                        if current["effective_from"] >= effective_from:
                            cursor.execute(
                                "DELETE FROM organization_primary_assignments WHERE id = %s",
                                (current["id"],),
                            )
                        else:
                            cursor.execute(
                                """
                                UPDATE organization_primary_assignments
                                SET effective_to = %s, updated_at = %s WHERE id = %s
                                """,
                                (effective_from, effective_from, current["id"]),
                            )
                    cursor.execute(
                        """
                        INSERT INTO organization_primary_assignments
                          (id, workspace_id, principal_id, org_unit_id, effective_from,
                           effective_to, assigned_by, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            assignment_id,
                            actor.workspace_id,
                            principal_id,
                            org_unit_id,
                            effective_from,
                            effective_to,
                            actor.principal_id,
                            effective_from,
                            effective_from,
                        ),
                    )
                    self._audit(
                        cursor,
                        actor=actor,
                        action="organization.primary_assigned",
                        resource_type="org_assignment",
                        resource_id=assignment_id,
                        metadata={"principal_id": str(principal_id), "org_unit_id": str(org_unit_id)},
                    )
            return {
                "assignment_id": assignment_id,
                "principal_id": principal_id,
                "org_unit_id": org_unit_id,
                "effective_from": effective_from,
                "effective_to": effective_to,
            }
        except psycopg.errors.ExclusionViolation as exc:
            raise RepositoryConflict("overlapping-primary") from exc

    @staticmethod
    def _create_handover_tasks(
        cursor: Any,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        reason: str,
        successor_org_unit_id: UUID | None,
    ) -> int:
        cursor.execute(
            """
            INSERT INTO organization_ownership_handover_tasks
              (id, workspace_id, resource_type, resource_id, principal_id, reason,
               successor_org_unit_id)
            SELECT gen_random_uuid(), workspace_id, resource_type, resource_id,
                   creator_principal_id, %s, %s
            FROM organization_resource_ownership_bindings
            WHERE workspace_id = %s AND creator_principal_id = %s
              AND owner_type = 'principal' AND owner_id = %s
              AND effective_to IS NULL
            ON CONFLICT DO NOTHING
            """,
            (
                reason,
                successor_org_unit_id,
                workspace_id,
                principal_id,
                principal_id,
            ),
        )
        return int(cursor.rowcount)

    def transfer_member(
        self,
        *,
        actor: Actor,
        principal_id: UUID,
        org_unit_id: UUID,
        effective_at: datetime,
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                member = self._membership(cursor, actor.workspace_id, principal_id)
                if member["status"] != "active":
                    raise RepositoryConflict("not-found")
                unit = self._active_unit(cursor, actor.workspace_id, org_unit_id)
                if unit["kind"] not in {"department", "team"}:
                    raise RepositoryConflict("invalid-primary-unit")
                cursor.execute(
                    """
                    SELECT id, org_unit_id FROM organization_primary_assignments
                    WHERE workspace_id = %s AND principal_id = %s
                      AND effective_from <= %s
                      AND (effective_to IS NULL OR effective_to > %s)
                    FOR UPDATE
                    """,
                    (actor.workspace_id, principal_id, effective_at, effective_at),
                )
                current = cursor.fetchone()
                if current is None:
                    raise RepositoryConflict("not-found")
                cursor.execute(
                    """
                    UPDATE organization_primary_assignments
                    SET effective_to = %s, updated_at = %s WHERE id = %s
                    """,
                    (effective_at, effective_at, current["id"]),
                )
                assignment_id = uuid4()
                cursor.execute(
                    """
                    INSERT INTO organization_primary_assignments
                      (id, workspace_id, principal_id, org_unit_id, effective_from,
                       assigned_by, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        assignment_id,
                        actor.workspace_id,
                        principal_id,
                        org_unit_id,
                        effective_at,
                        actor.principal_id,
                        effective_at,
                        effective_at,
                    ),
                )
                handovers = self._create_handover_tasks(
                    cursor,
                    workspace_id=actor.workspace_id,
                    principal_id=principal_id,
                    reason="transfer",
                    successor_org_unit_id=org_unit_id,
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.member.transferred",
                    resource_type="principal",
                    resource_id=principal_id,
                    metadata={
                        "from_org_unit_id": str(current["org_unit_id"]),
                        "to_org_unit_id": str(org_unit_id),
                        "handover_tasks": handovers,
                    },
                )
        return {
            "assignment_id": assignment_id,
            "principal_id": principal_id,
            "org_unit_id": org_unit_id,
            "effective_from": effective_at,
            "handover_tasks": handovers,
        }

    def deactivate_member(
        self,
        *,
        actor: Actor,
        principal_id: UUID,
        status: str,
        effective_at: datetime,
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                member = self._membership(cursor, actor.workspace_id, principal_id)
                if member["status"] != "active":
                    raise RepositoryConflict("not-found")
                cursor.execute(
                    """
                    UPDATE identity_memberships SET status = %s, updated_at = %s
                    WHERE workspace_id = %s AND principal_id = %s
                    """,
                    (status, effective_at, actor.workspace_id, principal_id),
                )
                cursor.execute(
                    """
                    UPDATE organization_primary_assignments
                    SET effective_to = %s, updated_at = %s
                    WHERE workspace_id = %s AND principal_id = %s
                      AND effective_from < %s
                      AND (effective_to IS NULL OR effective_to > %s)
                    """,
                    (
                        effective_at,
                        effective_at,
                        actor.workspace_id,
                        principal_id,
                        effective_at,
                        effective_at,
                    ),
                )
                handovers = self._create_handover_tasks(
                    cursor,
                    workspace_id=actor.workspace_id,
                    principal_id=principal_id,
                    reason=status,
                    successor_org_unit_id=None,
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action=f"organization.member.{status}",
                    resource_type="principal",
                    resource_id=principal_id,
                    metadata={"handover_tasks": handovers},
                )
        return {"principal_id": principal_id, "status": status, "handover_tasks": handovers}

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
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                member = self._membership(cursor, actor.workspace_id, principal_id)
                if member["status"] != "active":
                    raise RepositoryConflict("not-found")
                self._active_unit(cursor, actor.workspace_id, org_unit_id)
                cursor.execute(
                    """
                    SELECT role FROM identity_role_assignments
                    WHERE workspace_id = %s AND principal_id = %s
                    """,
                    (actor.workspace_id, principal_id),
                )
                subject_roles = [str(row["role"]) for row in cursor.fetchall()]
                subject_permissions = permissions_for_roles(subject_roles)
                if not set(permissions).issubset(subject_permissions):
                    raise RepositoryConflict("permission-ceiling")
                cursor.execute(
                    """
                    INSERT INTO organization_leadership_assignments
                      (id, workspace_id, principal_id, org_unit_id, scope_mode,
                       permissions, reason, effective_from, effective_to, assigned_by,
                       created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        assignment_id,
                        actor.workspace_id,
                        principal_id,
                        org_unit_id,
                        scope_mode,
                        Jsonb(list(permissions)),
                        reason,
                        effective_from,
                        effective_to,
                        actor.principal_id,
                        effective_from,
                        effective_from,
                    ),
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.leadership.assigned",
                    resource_type="leadership_assignment",
                    resource_id=assignment_id,
                    metadata={"scope_mode": scope_mode, "org_unit_id": str(org_unit_id)},
                )
        return {
            "leadership_assignment_id": assignment_id,
            "principal_id": principal_id,
            "org_unit_id": org_unit_id,
            "scope_mode": scope_mode,
            "permissions": list(permissions),
            "reason": reason,
            "effective_from": effective_from,
            "effective_to": effective_to,
        }

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
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                self._active_unit(cursor, actor.workspace_id, org_unit_id)
                if expected_version is None:
                    cursor.execute(
                        """
                        INSERT INTO organization_department_policies
                          (id, workspace_id, org_unit_id, current_version,
                           created_at, updated_at)
                        VALUES (%s, %s, %s, 1, %s, %s)
                        """,
                        (
                            policy_id,
                            actor.workspace_id,
                            org_unit_id,
                            effective_from,
                            effective_from,
                        ),
                    )
                    version = 1
                else:
                    cursor.execute(
                        """
                        SELECT current_version, org_unit_id
                        FROM organization_department_policies
                        WHERE id = %s AND workspace_id = %s
                        FOR UPDATE
                        """,
                        (policy_id, actor.workspace_id),
                    )
                    policy = cursor.fetchone()
                    if policy is None:
                        raise RepositoryConflict("not-found")
                    if UUID(str(policy["org_unit_id"])) != org_unit_id:
                        raise RepositoryConflict("workspace-mismatch")
                    if int(policy["current_version"]) != expected_version:
                        raise RepositoryConflict("stale-version")
                    version = expected_version + 1
                    cursor.execute(
                        """
                        UPDATE organization_department_policies
                        SET current_version = %s, updated_at = %s WHERE id = %s
                        """,
                        (version, effective_from, policy_id),
                    )
                cursor.execute(
                    """
                    INSERT INTO organization_department_policy_versions
                      (policy_id, version, status, allowed_actions, row_scope_refs,
                       column_policy_refs, pii_allowed, include_descendants,
                       effective_from, created_by, created_at)
                    VALUES (%s, %s, 'draft', %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        policy_id,
                        version,
                        Jsonb(list(allowed_actions)),
                        Jsonb(list(row_scope_refs)),
                        Jsonb(list(column_policy_refs)),
                        pii_allowed,
                        include_descendants,
                        effective_from,
                        actor.principal_id,
                        effective_from,
                    ),
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.policy.drafted",
                    resource_type="department_policy",
                    resource_id=policy_id,
                    metadata={"version": version},
                )
        return {
            "policy_id": policy_id,
            "org_unit_id": org_unit_id,
            "version": version,
            "status": "draft",
            "allowed_actions": list(allowed_actions),
            "row_scope_refs": list(row_scope_refs),
            "column_policy_refs": list(column_policy_refs),
            "pii_allowed": pii_allowed,
            "include_descendants": include_descendants,
            "effective_from": effective_from,
        }

    def publish_policy(
        self,
        *,
        actor: Actor,
        policy_id: UUID,
        expected_version: int,
        effective_from: datetime,
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT p.org_unit_id, p.current_version, v.status
                    FROM organization_department_policies AS p
                    JOIN organization_department_policy_versions AS v
                      ON v.policy_id = p.id AND v.version = p.current_version
                    WHERE p.id = %s AND p.workspace_id = %s
                    FOR UPDATE OF p, v
                    """,
                    (policy_id, actor.workspace_id),
                )
                policy = cursor.fetchone()
                if policy is None:
                    raise RepositoryConflict("not-found")
                if int(policy["current_version"]) != expected_version:
                    raise RepositoryConflict("stale-version")
                if policy["status"] != "draft":
                    raise RepositoryConflict("policy-not-draft")
                cursor.execute(
                    """
                    UPDATE organization_department_policy_versions AS v
                    SET status = 'deprecated', effective_to = %s
                    FROM organization_department_policies AS p
                    WHERE p.id = v.policy_id AND p.workspace_id = %s
                      AND p.org_unit_id = %s AND v.status = 'published'
                      AND (v.effective_to IS NULL OR v.effective_to > %s)
                    """,
                    (
                        effective_from,
                        actor.workspace_id,
                        policy["org_unit_id"],
                        effective_from,
                    ),
                )
                cursor.execute(
                    """
                    UPDATE organization_department_policy_versions
                    SET status = 'published', effective_from = %s,
                        published_by = %s, published_at = %s
                    WHERE policy_id = %s AND version = %s
                    RETURNING allowed_actions, row_scope_refs, column_policy_refs,
                              pii_allowed, include_descendants
                    """,
                    (
                        effective_from,
                        actor.principal_id,
                        effective_from,
                        policy_id,
                        expected_version,
                    ),
                )
                values = cursor.fetchone()
                if values is None:
                    raise RepositoryConflict("not-found")
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.policy.published",
                    resource_type="department_policy",
                    resource_id=policy_id,
                    metadata={"version": expected_version},
                )
        return {
            "policy_id": policy_id,
            "org_unit_id": UUID(str(policy["org_unit_id"])),
            "version": expected_version,
            "status": "published",
            "allowed_actions": list(values["allowed_actions"]),
            "row_scope_refs": list(values["row_scope_refs"]),
            "column_policy_refs": list(values["column_policy_refs"]),
            "pii_allowed": bool(values["pii_allowed"]),
            "include_descendants": bool(values["include_descendants"]),
            "effective_from": effective_from,
        }

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
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                self._active_unit(cursor, actor.workspace_id, target_org_unit_id)
                if subject_type == "principal":
                    self._membership(cursor, actor.workspace_id, subject_id)
                else:
                    self._active_unit(cursor, actor.workspace_id, subject_id)
                cursor.execute(
                    """
                    INSERT INTO organization_cross_department_grants
                      (id, workspace_id, subject_type, subject_id, target_org_unit_id,
                       resource_type, resource_id, actions, reason, issued_by,
                       effective_from, expires_at, version, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s)
                    """,
                    (
                        grant_id,
                        actor.workspace_id,
                        subject_type,
                        subject_id,
                        target_org_unit_id,
                        resource_type,
                        resource_id,
                        Jsonb(list(actions)),
                        reason,
                        actor.principal_id,
                        effective_from,
                        expires_at,
                        effective_from,
                        effective_from,
                    ),
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.grant.created",
                    resource_type="cross_department_grant",
                    resource_id=grant_id,
                    metadata={"reason": reason, "target_org_unit_id": str(target_org_unit_id)},
                )
        return {
            "grant_id": grant_id,
            "version": 1,
            "subject_type": subject_type,
            "subject_id": subject_id,
            "target_org_unit_id": target_org_unit_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "actions": list(actions),
            "reason": reason,
            "effective_from": effective_from,
            "expires_at": expires_at,
            "revoked_at": None,
        }

    def revoke_grant(
        self, *, actor: Actor, grant_id: UUID, expected_version: int, at: datetime
    ) -> dict[str, object]:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT version, revoked_at FROM organization_cross_department_grants
                    WHERE id = %s AND workspace_id = %s FOR UPDATE
                    """,
                    (grant_id, actor.workspace_id),
                )
                grant = cursor.fetchone()
                if grant is None:
                    raise RepositoryConflict("not-found")
                if int(grant["version"]) != expected_version:
                    raise RepositoryConflict("stale-version")
                if grant["revoked_at"] is not None:
                    raise RepositoryConflict("stale-version")
                next_version = expected_version + 1
                cursor.execute(
                    """
                    UPDATE organization_cross_department_grants
                    SET revoked_at = %s, revoked_by = %s, version = %s, updated_at = %s
                    WHERE id = %s
                    """,
                    (at, actor.principal_id, next_version, at, grant_id),
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.grant.revoked",
                    resource_type="cross_department_grant",
                    resource_id=grant_id,
                    metadata={"version": next_version},
                )
        return {"grant_id": grant_id, "version": next_version, "revoked_at": at}

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
    ) -> dict[str, object]:
        if not resource_type:
            raise RepositoryConflict("invalid-resource")
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                self._membership(cursor, actor.workspace_id, creator_principal_id)
                if owner_type == "principal":
                    self._membership(cursor, actor.workspace_id, owner_id)
                elif owner_type == "org_unit":
                    self._active_unit(cursor, actor.workspace_id, owner_id)
                elif owner_id != actor.workspace_id:
                    raise RepositoryConflict("workspace-mismatch")
                cursor.execute(
                    """
                    SELECT id, creator_principal_id, version
                    FROM organization_resource_ownership_bindings
                    WHERE workspace_id = %s AND resource_type = %s AND resource_id = %s
                      AND effective_to IS NULL
                    FOR UPDATE
                    """,
                    (actor.workspace_id, resource_type, resource_id),
                )
                current = cursor.fetchone()
                version = 1
                if current is not None:
                    if UUID(str(current["creator_principal_id"])) != creator_principal_id:
                        raise RepositoryConflict("creator-immutable")
                    version = int(current["version"]) + 1
                    cursor.execute(
                        """
                        UPDATE organization_resource_ownership_bindings
                        SET effective_to = %s, updated_at = %s WHERE id = %s
                        """,
                        (effective_from, effective_from, current["id"]),
                    )
                cursor.execute(
                    """
                    INSERT INTO organization_resource_ownership_bindings
                      (id, workspace_id, resource_type, resource_id, creator_principal_id,
                       owner_type, owner_id, allowed_actions, required_row_scope_refs,
                       required_column_policy_refs, requires_pii, effective_from,
                       version, bound_by, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s)
                    """,
                    (
                        binding_id,
                        actor.workspace_id,
                        resource_type,
                        resource_id,
                        creator_principal_id,
                        owner_type,
                        owner_id,
                        Jsonb(list(allowed_actions)),
                        Jsonb(list(required_row_scope_refs)),
                        Jsonb(list(required_column_policy_refs)),
                        requires_pii,
                        effective_from,
                        version,
                        actor.principal_id,
                        effective_from,
                        effective_from,
                    ),
                )
                self._audit(
                    cursor,
                    actor=actor,
                    action="organization.ownership.bound",
                    resource_type=resource_type,
                    resource_id=resource_id,
                    metadata={"owner_type": owner_type, "owner_id": str(owner_id)},
                )
        return {
            "binding_id": binding_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "creator_principal_id": creator_principal_id,
            "owner_type": owner_type,
            "owner_id": owner_id,
            "allowed_actions": list(allowed_actions),
            "required_row_scope_refs": list(required_row_scope_refs),
            "required_column_policy_refs": list(required_column_policy_refs),
            "requires_pii": requires_pii,
            "version": version,
            "effective_from": effective_from,
        }

    def list_resource_candidates(
        self,
        *,
        actor: Actor,
        resource_type: str,
        at: datetime,
    ) -> list[ResourceCandidate]:
        """Load authoritative current bindings before visibility filtering."""

        candidates: list[ResourceCandidate] = []
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT resource_type, resource_id, owner_type, owner_id
                FROM organization_resource_ownership_bindings
                WHERE workspace_id = %s AND resource_type = %s
                  AND effective_from <= %s
                  AND (effective_to IS NULL OR effective_to > %s)
                ORDER BY resource_id
                """,
                (actor.workspace_id, resource_type, at, at),
            )
            for binding in cursor.fetchall():
                owner_type = str(binding["owner_type"])
                owner_id = UUID(str(binding["owner_id"]))
                org_unit_id: UUID | None = None
                if owner_type == "org_unit":
                    org_unit_id = owner_id
                elif owner_type == "principal":
                    cursor.execute(
                        """
                        SELECT org_unit_id
                        FROM organization_primary_assignments
                        WHERE workspace_id = %s AND principal_id = %s
                          AND effective_from <= %s
                          AND (effective_to IS NULL OR effective_to > %s)
                          AND needs_department_assignment = FALSE
                        ORDER BY effective_from DESC LIMIT 1
                        """,
                        (actor.workspace_id, owner_id, at, at),
                    )
                    primary = cursor.fetchone()
                    if primary is not None:
                        org_unit_id = UUID(str(primary["org_unit_id"]))
                elif owner_id == actor.workspace_id:
                    cursor.execute(
                        """
                        SELECT u.id
                        FROM organization_units AS u
                        JOIN organization_unit_versions AS v
                          ON v.org_unit_id = u.id AND v.version = u.current_version
                        WHERE u.workspace_id = %s AND v.kind = 'company'
                          AND v.status = 'active'
                        LIMIT 1
                        """,
                        (actor.workspace_id,),
                    )
                    root = cursor.fetchone()
                    if root is not None:
                        org_unit_id = UUID(str(root["id"]))
                if org_unit_id is not None:
                    candidates.append(
                        ResourceCandidate(
                            resource_type=str(binding["resource_type"]),
                            resource_id=UUID(str(binding["resource_id"])),
                            org_unit_id=org_unit_id,
                        )
                    )
        return candidates

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
    ) -> dict[str, bool]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            self._active_unit(cursor, actor.workspace_id, target_org_unit_id)
            cursor.execute(
                """
                SELECT status FROM identity_memberships
                WHERE workspace_id = %s AND principal_id = %s
                """,
                (actor.workspace_id, actor.principal_id),
            )
            membership = cursor.fetchone()
            active_membership = bool(membership and membership["status"] == "active")
            cursor.execute(
                """
                SELECT org_unit_id, needs_department_assignment
                FROM organization_primary_assignments
                WHERE workspace_id = %s AND principal_id = %s
                  AND effective_from <= %s
                  AND (effective_to IS NULL OR effective_to > %s)
                ORDER BY effective_from DESC LIMIT 1
                """,
                (actor.workspace_id, actor.principal_id, at, at),
            )
            primary = cursor.fetchone()
            primary_id = UUID(str(primary["org_unit_id"])) if primary is not None else None
            primary_ready = bool(
                primary is not None and not bool(primary["needs_department_assignment"])
            )
            own_scope = bool(
                primary_ready
                and primary_id is not None
                and self._is_descendant(cursor, primary_id, target_org_unit_id)
            )

            cursor.execute(
                """
                SELECT org_unit_id, scope_mode, permissions
                FROM organization_leadership_assignments
                WHERE workspace_id = %s AND principal_id = %s
                  AND effective_from <= %s
                  AND (effective_to IS NULL OR effective_to > %s)
                """,
                (actor.workspace_id, actor.principal_id, at, at),
            )
            leadership_covers = False
            for leadership in cursor.fetchall():
                scope_mode = str(leadership["scope_mode"])
                unit_id = UUID(str(leadership["org_unit_id"]))
                covers = scope_mode == "workspace" or (
                    scope_mode == "unit" and unit_id == target_org_unit_id
                )
                covers = covers or (
                    scope_mode == "subtree"
                    and self._is_descendant(cursor, target_org_unit_id, unit_id)
                )
                leadership_permissions = {
                    str(value) for value in leadership["permissions"]
                }
                if covers and functional_permission in leadership_permissions:
                    leadership_covers = True

            object_policy = False
            export_policy = False
            resource_requires_pii = True
            required_row_scope_refs: tuple[str, ...] = ()
            required_column_policy_refs: tuple[str, ...] = ()
            if resource_type is not None and resource_id is not None:
                cursor.execute(
                    """
                    SELECT owner_type, owner_id, allowed_actions,
                           required_row_scope_refs, required_column_policy_refs,
                           requires_pii
                    FROM organization_resource_ownership_bindings
                    WHERE workspace_id = %s AND resource_type = %s AND resource_id = %s
                      AND effective_from <= %s
                      AND (effective_to IS NULL OR effective_to > %s)
                    ORDER BY version DESC LIMIT 1
                    """,
                    (actor.workspace_id, resource_type, resource_id, at, at),
                )
                binding = cursor.fetchone()
                if binding is not None:
                    owner_type = str(binding["owner_type"])
                    owner_id = UUID(str(binding["owner_id"]))
                    owner_matches = owner_type == "org_unit" and self._is_descendant(
                        cursor, target_org_unit_id, owner_id
                    )
                    if owner_type == "principal":
                        cursor.execute(
                            """
                            SELECT org_unit_id
                            FROM organization_primary_assignments
                            WHERE workspace_id = %s AND principal_id = %s
                              AND effective_from <= %s
                              AND (effective_to IS NULL OR effective_to > %s)
                            ORDER BY effective_from DESC LIMIT 1
                            """,
                            (actor.workspace_id, owner_id, at, at),
                        )
                        owner_primary = cursor.fetchone()
                        owner_matches = bool(
                            owner_id == actor.principal_id
                            and
                            owner_primary
                            and UUID(str(owner_primary["org_unit_id"]))
                            == target_org_unit_id
                        )
                    if owner_type == "workspace_legacy":
                        owner_matches = False
                    object_actions = {
                        str(value) for value in binding["allowed_actions"]
                    }
                    object_policy = owner_matches and action in object_actions
                    export_policy = not action.startswith("export") or action in object_actions
                    required_row_scope_refs = tuple(
                        str(value) for value in binding["required_row_scope_refs"]
                    )
                    required_column_policy_refs = tuple(
                        str(value) for value in binding["required_column_policy_refs"]
                    )
                    resource_requires_pii = bool(binding["requires_pii"])

            cursor.execute(
                """
                WITH RECURSIVE lineage(id, distance) AS (
                  SELECT %s::uuid, 0
                  UNION ALL
                  SELECT v.parent_org_unit_id, l.distance + 1
                  FROM lineage AS l
                  JOIN organization_units AS u ON u.id = l.id
                  JOIN organization_unit_versions AS v
                    ON v.org_unit_id = u.id AND v.version = u.current_version
                  WHERE v.parent_org_unit_id IS NOT NULL
                )
                SELECT v.allowed_actions, v.row_scope_refs, v.column_policy_refs,
                       v.pii_allowed, v.include_descendants
                FROM lineage AS l
                JOIN organization_department_policies AS p ON p.org_unit_id = l.id
                JOIN organization_department_policy_versions AS v
                  ON v.policy_id = p.id
                WHERE p.workspace_id = %s AND v.status = 'published'
                  AND v.effective_from <= %s
                  AND (v.effective_to IS NULL OR v.effective_to > %s)
                  AND (l.distance = 0 OR v.include_descendants)
                ORDER BY l.distance ASC, v.version DESC
                LIMIT 1
                """,
                (target_org_unit_id, actor.workspace_id, at, at),
            )
            policy = cursor.fetchone()
            policy_fresh = policy is not None
            department_policy = False
            row_policy = False
            column_policy = False
            policy_pii = False
            if policy is not None:
                actions = {str(value) for value in policy["allowed_actions"]}
                rows = {str(value) for value in policy["row_scope_refs"]}
                columns = {str(value) for value in policy["column_policy_refs"]}
                department_policy = action in actions
                row_policy = set(required_row_scope_refs).issubset(rows)
                column_policy = set(required_column_policy_refs).issubset(columns)
                policy_pii = bool(policy["pii_allowed"])

            grant_allowed = False
            if active_membership and primary_ready and primary_id is not None:
                cursor.execute(
                    """
                    SELECT subject_type, subject_id, resource_type, resource_id, actions
                    FROM organization_cross_department_grants
                    WHERE workspace_id = %s AND target_org_unit_id = %s
                      AND effective_from <= %s
                      AND (expires_at IS NULL OR expires_at > %s)
                      AND revoked_at IS NULL
                    """,
                    (actor.workspace_id, target_org_unit_id, at, at),
                )
                for grant in cursor.fetchall():
                    subject_match = (
                        grant["subject_type"] == "principal"
                        and UUID(str(grant["subject_id"])) == actor.principal_id
                    ) or (
                        grant["subject_type"] == "org_unit"
                        and self._is_descendant(
                            cursor, primary_id, UUID(str(grant["subject_id"]))
                        )
                    )
                    resource_match = grant["resource_id"] is None or (
                        resource_id is not None
                        and UUID(str(grant["resource_id"])) == resource_id
                        and str(grant["resource_type"]) == resource_type
                    )
                    if subject_match and resource_match and action in {
                        str(value) for value in grant["actions"]
                    }:
                        grant_allowed = True
                        break

        return {
            "functional_permission": actor.allows(functional_permission),
            "active_membership": active_membership and primary_ready,
            "organization_scope": own_scope or leadership_covers,
            "department_policy": department_policy,
            "cross_department_grant": grant_allowed,
            "object_policy": object_policy,
            "row_policy": row_policy,
            "column_policy": column_policy,
            "export_policy": export_policy,
            "policy_fresh": policy_fresh,
            "pii_ceiling": (not resource_requires_pii)
            or (policy_pii and actor.allows("pii.read")),
        }
