"""Current resource projection from Identity-owned tables and organization evaluator."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID
from psycopg.rows import dict_row
from packages.identity_access.domain.policy import Actor
from packages.identity_access.domain.organization import required_functional_permission
from packages.identity_access.infrastructure.organization_postgres import (
    PostgresOrganizationRepository,
)


class PostgresResourceAccessRepository(PostgresOrganizationRepository):
    def resource_context(
        self,
        actor: Actor,
        resource_type: str,
        resource_id: UUID,
        action: str,
        legacy_creator: UUID | None,
    ) -> dict[str, Any]:
        at = datetime.now(UTC)
        permission = required_functional_permission(resource_type, action)
        with self._connect() as c, c.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT status FROM identity_memberships
                WHERE workspace_id=%s AND principal_id=%s""",
                (actor.workspace_id, actor.principal_id),
            )
            member = cur.fetchone()
            cur.execute(
                """SELECT * FROM organization_resource_ownership_bindings
                WHERE workspace_id=%s AND resource_type=%s AND resource_id=%s
                AND effective_from<=%s AND (effective_to IS NULL OR effective_to>%s)
                ORDER BY version DESC LIMIT 1""",
                (actor.workspace_id, resource_type, resource_id, at, at),
            )
            binding = cur.fetchone()
            cur.execute(
                "SELECT EXISTS(SELECT 1 FROM organization_resource_ownership_bindings WHERE workspace_id=%s AND resource_type=%s AND resource_id=%s)",
                (actor.workspace_id, resource_type, resource_id),
            )
            history = cur.fetchone()
            had_binding = bool(history and history["exists"])
            if binding and binding["owner_type"] == "org_unit":
                target = binding["owner_id"]
            elif binding and binding["owner_type"] == "principal":
                cur.execute(
                    """SELECT org_unit_id FROM organization_primary_assignments
                    WHERE workspace_id=%s AND principal_id=%s AND effective_from<=%s
                    AND (effective_to IS NULL OR effective_to>%s) ORDER BY effective_from DESC LIMIT 1""",
                    (actor.workspace_id, binding["owner_id"], at, at),
                )
                primary = cur.fetchone()
                target = primary["org_unit_id"] if primary else None
            else:
                target = None
        legacy = (
            not had_binding
            and binding is None
            and legacy_creator == actor.principal_id
            and resource_type in {"report", "analysis"}
        )
        if target is None:
            layers = dict(
                functional_permission=actor.allows(permission),
                active_membership=bool(member and member["status"] == "active"),
                organization_scope=legacy,
                department_policy=legacy,
                cross_department_grant=False,
                object_policy=legacy,
                row_policy=legacy,
                column_policy=legacy,
                export_policy=legacy,
                pii_policy=legacy,
                policy_fresh=legacy,
            )
            return {
                "layers": layers,
                "detail": {"legacy_creator": str(legacy_creator), "binding": str(binding)},
            }
        raw = self.access_context(
            actor=actor,
            target_org_unit_id=target,
            functional_permission=permission,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            at=at,
            projection_details=True,
        )
        detail = raw.pop("projection")
        policy: dict[str, Any] = detail["policy"] or {}
        bound: dict[str, Any] = detail["binding"] or {}
        detail["row_scopes"] = [
            policy.get("row_scope_refs", []),
            bound.get("required_row_scope_refs", []),
        ]
        detail["column_scopes"] = [
            policy.get("column_policy_refs", []),
            bound.get("required_column_policy_refs", []),
        ]
        raw["pii_policy"] = raw.pop("pii_ceiling")
        return {"layers": raw, "detail": detail}
