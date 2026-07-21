"""Stable HTTP contracts for organization hierarchy and effective access."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Header, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from packages.contracts.organization import ORGANIZATION_API_VERSION
from packages.identity_access.application.organization import OrganizationFailure, OrganizationService
from packages.identity_access.application.service import IdentityService
from packages.identity_access.domain.policy import Actor
from packages.identity_access.infrastructure.organization_postgres import (
    PostgresOrganizationRepository,
)
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorResponse(StrictModel):
    code: str


class UnitCreateRequest(StrictModel):
    key: str = Field(min_length=2, max_length=80)
    kind: Literal["company", "division", "department", "team"]
    parent_org_unit_id: UUID | None = None
    display_name: str = Field(min_length=1, max_length=160)
    effective_from: datetime | None = None


class UnitVersionRequest(StrictModel):
    expected_version: int = Field(ge=1)
    parent_org_unit_id: UUID | None = None
    display_name: str = Field(min_length=1, max_length=160)
    effective_from: datetime | None = None


class UnitLifecycleRequest(StrictModel):
    expected_version: int = Field(ge=1)
    status: Literal["inactive", "merged"]
    successor_org_unit_id: UUID | None = None
    effective_from: datetime | None = None


class UnitResponse(StrictModel):
    org_unit_id: UUID
    workspace_id: UUID
    key: str
    version: int
    kind: Literal["company", "division", "department", "team"]
    parent_org_unit_id: UUID | None
    display_name: str
    status: Literal["active", "inactive", "merged"]
    effective_from: datetime
    effective_to: datetime | None
    successor_org_unit_id: UUID | None


class UnitListResponse(StrictModel):
    units: list[UnitResponse]


class PrimaryAssignmentRequest(StrictModel):
    principal_id: UUID
    org_unit_id: UUID
    effective_from: datetime | None = None
    effective_to: datetime | None = None


class TransferRequest(StrictModel):
    org_unit_id: UUID
    effective_at: datetime | None = None


class DeactivateRequest(StrictModel):
    status: Literal["suspended", "departed"]
    effective_at: datetime | None = None


class AssignmentResponse(StrictModel):
    assignment_id: UUID | None = None
    principal_id: UUID
    org_unit_id: UUID | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    status: str | None = None
    handover_tasks: int = 0


class LeadershipRequest(StrictModel):
    principal_id: UUID
    org_unit_id: UUID
    scope_mode: Literal["unit", "subtree", "workspace"]
    permissions: list[str] = Field(min_length=1, max_length=64)
    reason: str = Field(min_length=1, max_length=500)
    effective_from: datetime | None = None
    effective_to: datetime | None = None


class LeadershipResponse(StrictModel):
    leadership_assignment_id: UUID
    principal_id: UUID
    org_unit_id: UUID
    scope_mode: Literal["unit", "subtree", "workspace"]
    permissions: list[str]
    reason: str
    effective_from: datetime
    effective_to: datetime | None


class PolicyDraftRequest(StrictModel):
    policy_id: UUID | None = None
    org_unit_id: UUID
    expected_version: int | None = Field(default=None, ge=1)
    allowed_actions: list[str] = Field(min_length=1, max_length=128)
    row_scope_refs: list[str] = Field(default_factory=list, max_length=128)
    column_policy_refs: list[str] = Field(default_factory=list, max_length=128)
    pii_allowed: bool = False
    include_descendants: bool = False
    effective_from: datetime | None = None


class PolicyPublishRequest(StrictModel):
    expected_version: int = Field(ge=1)
    effective_from: datetime | None = None


class PolicyResponse(StrictModel):
    policy_id: UUID
    org_unit_id: UUID
    version: int
    status: Literal["draft", "published", "deprecated"]
    allowed_actions: list[str]
    row_scope_refs: list[str]
    column_policy_refs: list[str]
    pii_allowed: bool
    include_descendants: bool
    effective_from: datetime


class GrantCreateRequest(StrictModel):
    subject_type: Literal["principal", "org_unit"]
    subject_id: UUID
    target_org_unit_id: UUID
    resource_type: str | None = Field(default=None, min_length=1, max_length=80)
    resource_id: UUID | None = None
    actions: list[str] = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=500)
    effective_from: datetime | None = None
    expires_at: datetime | None = None


class GrantResponse(StrictModel):
    grant_id: UUID
    version: int
    subject_type: Literal["principal", "org_unit"] | None = None
    subject_id: UUID | None = None
    target_org_unit_id: UUID | None = None
    resource_type: str | None = None
    resource_id: UUID | None = None
    actions: list[str] = Field(default_factory=list)
    reason: str | None = None
    effective_from: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None


class GrantRevokeRequest(StrictModel):
    expected_version: int = Field(ge=1)


class OwnershipRequest(StrictModel):
    resource_type: str = Field(min_length=1, max_length=80)
    resource_id: UUID
    creator_principal_id: UUID
    owner_type: Literal["principal", "org_unit", "workspace_legacy"]
    owner_id: UUID
    allowed_actions: list[str] = Field(min_length=1, max_length=128)
    required_row_scope_refs: list[str] = Field(default_factory=list, max_length=128)
    required_column_policy_refs: list[str] = Field(default_factory=list, max_length=128)
    requires_pii: bool = False
    effective_from: datetime | None = None


class OwnershipResponse(StrictModel):
    binding_id: UUID
    resource_type: str
    resource_id: UUID
    creator_principal_id: UUID
    owner_type: Literal["principal", "org_unit", "workspace_legacy"]
    owner_id: UUID
    allowed_actions: list[str]
    required_row_scope_refs: list[str]
    required_column_policy_refs: list[str]
    requires_pii: bool
    version: int
    effective_from: datetime


class AccessDecisionRequest(StrictModel):
    target_org_unit_id: UUID
    action: str = Field(min_length=1, max_length=120)
    resource_type: str | None = Field(default=None, min_length=1, max_length=80)
    resource_id: UUID | None = None


class AccessLayer(StrictModel):
    layer: str
    allowed: bool


class AccessDecisionResponse(StrictModel):
    allowed: bool
    denied_by: list[str]
    layers: list[AccessLayer]


class VisibilitySearchRequest(StrictModel):
    action: str = Field(min_length=1, max_length=120)
    resource_type: str = Field(min_length=1, max_length=80)
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=200)


class VisibleResource(StrictModel):
    resource_type: str
    resource_id: UUID
    org_unit_id: UUID


class VisibilitySearchResponse(StrictModel):
    resources: list[VisibleResource]
    visible_count: int = Field(ge=0)


def _services(settings: Settings) -> tuple[IdentityService, OrganizationService]:
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
    organization = OrganizationService(PostgresOrganizationRepository(connect))
    return identity, organization


def _status_for(code: str) -> int:
    if code == "AUTHENTICATION_FAILED":
        return status.HTTP_401_UNAUTHORIZED
    if code == "FORBIDDEN":
        return status.HTTP_403_FORBIDDEN
    if code == "NOT_FOUND":
        return status.HTTP_404_NOT_FOUND
    if code == "CONFLICT":
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def create_organization_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    organization_service: OrganizationService | None = None,
) -> FastAPI:
    """Build the independently versioned Organization API boundary."""

    default_identity, default_organization = _services(settings)
    identity = identity_service or default_identity
    organization = organization_service or default_organization
    app = FastAPI(
        title="Custometry Organization API",
        version=ORGANIZATION_API_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(OrganizationFailure)
    async def organization_failure_handler(_: Request, exc: OrganizationFailure) -> JSONResponse:
        return JSONResponse(status_code=_status_for(exc.code), content={"code": exc.code})

    def authenticated(authorization: Annotated[str | None, Header()] = None) -> Actor:
        if authorization is None:
            raise OrganizationFailure("AUTHENTICATION_FAILED")
        scheme, _, raw = authorization.partition(" ")
        if scheme.casefold() != "bearer" or not raw:
            raise OrganizationFailure("AUTHENTICATION_FAILED")
        try:
            return identity.authenticate(raw)
        except Exception as exc:
            raise OrganizationFailure("AUTHENTICATION_FAILED") from exc

    @app.post(
        "/units", response_model=UnitResponse, operation_id="create_organization_unit"
    )
    def create_unit(
        payload: UnitCreateRequest, actor: Actor = Depends(authenticated)
    ) -> UnitResponse:
        return UnitResponse.model_validate(
            organization.create_unit(actor, **payload.model_dump())
        )

    @app.get("/units", response_model=UnitListResponse, operation_id="list_organization_units")
    def list_units(actor: Actor = Depends(authenticated)) -> UnitListResponse:
        return UnitListResponse(
            units=[UnitResponse.model_validate(item) for item in organization.list_units(actor)]
        )

    @app.post(
        "/units/{org_unit_id}/versions",
        response_model=UnitResponse,
        operation_id="version_organization_unit",
    )
    def version_unit(
        org_unit_id: UUID,
        payload: UnitVersionRequest,
        actor: Actor = Depends(authenticated),
    ) -> UnitResponse:
        return UnitResponse.model_validate(
            organization.version_unit(actor, org_unit_id=org_unit_id, **payload.model_dump())
        )

    @app.post(
        "/units/{org_unit_id}/lifecycle",
        response_model=UnitResponse,
        operation_id="close_or_merge_organization_unit",
    )
    def close_unit(
        org_unit_id: UUID,
        payload: UnitLifecycleRequest,
        actor: Actor = Depends(authenticated),
    ) -> UnitResponse:
        return UnitResponse.model_validate(
            organization.close_unit(actor, org_unit_id=org_unit_id, **payload.model_dump())
        )

    @app.post(
        "/primary-assignments",
        response_model=AssignmentResponse,
        operation_id="assign_primary_organization_unit",
    )
    def assign_primary(
        payload: PrimaryAssignmentRequest, actor: Actor = Depends(authenticated)
    ) -> AssignmentResponse:
        return AssignmentResponse.model_validate(
            organization.assign_primary(actor, **payload.model_dump())
        )

    @app.post(
        "/members/{principal_id}/transfer",
        response_model=AssignmentResponse,
        operation_id="transfer_organization_member",
    )
    def transfer_member(
        principal_id: UUID,
        payload: TransferRequest,
        actor: Actor = Depends(authenticated),
    ) -> AssignmentResponse:
        return AssignmentResponse.model_validate(
            organization.transfer_member(actor, principal_id=principal_id, **payload.model_dump())
        )

    @app.post(
        "/members/{principal_id}/deactivate",
        response_model=AssignmentResponse,
        operation_id="deactivate_organization_member",
    )
    def deactivate_member(
        principal_id: UUID,
        payload: DeactivateRequest,
        actor: Actor = Depends(authenticated),
    ) -> AssignmentResponse:
        return AssignmentResponse.model_validate(
            organization.deactivate_member(
                actor, principal_id=principal_id, **payload.model_dump()
            )
        )

    @app.post(
        "/leadership-assignments",
        response_model=LeadershipResponse,
        operation_id="assign_organization_leadership",
    )
    def assign_leadership(
        payload: LeadershipRequest, actor: Actor = Depends(authenticated)
    ) -> LeadershipResponse:
        values = payload.model_dump()
        values["permissions"] = tuple(values["permissions"])
        return LeadershipResponse.model_validate(
            organization.assign_leadership(actor, **values)
        )

    @app.post(
        "/department-policies/drafts",
        response_model=PolicyResponse,
        operation_id="draft_department_data_policy",
    )
    def draft_policy(
        payload: PolicyDraftRequest, actor: Actor = Depends(authenticated)
    ) -> PolicyResponse:
        values = payload.model_dump()
        for key in ("allowed_actions", "row_scope_refs", "column_policy_refs"):
            values[key] = tuple(values[key])
        return PolicyResponse.model_validate(
            organization.create_policy_draft(actor, **values)
        )

    @app.post(
        "/department-policies/{policy_id}/publish",
        response_model=PolicyResponse,
        operation_id="publish_department_data_policy",
    )
    def publish_policy(
        policy_id: UUID,
        payload: PolicyPublishRequest,
        actor: Actor = Depends(authenticated),
    ) -> PolicyResponse:
        return PolicyResponse.model_validate(
            organization.publish_policy(actor, policy_id=policy_id, **payload.model_dump())
        )

    @app.post(
        "/cross-department-grants",
        response_model=GrantResponse,
        operation_id="create_cross_department_grant",
    )
    def create_grant(
        payload: GrantCreateRequest, actor: Actor = Depends(authenticated)
    ) -> GrantResponse:
        values = payload.model_dump()
        values["actions"] = tuple(values["actions"])
        return GrantResponse.model_validate(organization.create_grant(actor, **values))

    @app.post(
        "/cross-department-grants/{grant_id}/revoke",
        response_model=GrantResponse,
        operation_id="revoke_cross_department_grant",
    )
    def revoke_grant(
        grant_id: UUID,
        payload: GrantRevokeRequest,
        actor: Actor = Depends(authenticated),
    ) -> GrantResponse:
        return GrantResponse.model_validate(
            organization.revoke_grant(actor, grant_id=grant_id, **payload.model_dump())
        )

    @app.post(
        "/resource-ownership",
        response_model=OwnershipResponse,
        operation_id="bind_organization_resource_owner",
    )
    def bind_resource(
        payload: OwnershipRequest, actor: Actor = Depends(authenticated)
    ) -> OwnershipResponse:
        values = payload.model_dump()
        for key in (
            "allowed_actions",
            "required_row_scope_refs",
            "required_column_policy_refs",
        ):
            values[key] = tuple(values[key])
        return OwnershipResponse.model_validate(
            organization.bind_resource(actor, **values)
        )

    @app.post(
        "/access/decide",
        response_model=AccessDecisionResponse,
        operation_id="explain_effective_organization_access",
    )
    def decide_access(
        payload: AccessDecisionRequest, actor: Actor = Depends(authenticated)
    ) -> AccessDecisionResponse:
        decision = organization.decide_access(actor, **payload.model_dump())
        return AccessDecisionResponse(
            allowed=decision.allowed,
            denied_by=list(decision.denied_by),
            layers=[AccessLayer(layer=name, allowed=allowed) for name, allowed in decision.layers],
        )

    @app.post(
        "/resource-visibility/search",
        response_model=VisibilitySearchResponse,
        operation_id="filter_visible_organization_resources",
    )
    def filter_visible(
        payload: VisibilitySearchRequest, actor: Actor = Depends(authenticated)
    ) -> VisibilitySearchResponse:
        visible, count = organization.filter_visible_resources(
            actor,
            action=payload.action,
            resource_type=payload.resource_type,
            offset=payload.offset,
            limit=payload.limit,
        )
        return VisibilitySearchResponse(
            resources=[
                VisibleResource(
                    resource_type=item.resource_type,
                    resource_id=item.resource_id,
                    org_unit_id=item.org_unit_id,
                )
                for item in visible
            ],
            visible_count=count,
        )

    _ = (
        organization_failure_handler,
        create_unit,
        list_units,
        version_unit,
        close_unit,
        assign_primary,
        transfer_member,
        deactivate_member,
        assign_leadership,
        draft_policy,
        publish_policy,
        create_grant,
        revoke_grant,
        bind_resource,
        decide_access,
        filter_visible,
    )
    return app
