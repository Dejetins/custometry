"""Authenticated, policy-filtered People & Creators API."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Header, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from packages.contracts.people import PEOPLE_API_VERSION, PeopleFailure, ViewerContext
from packages.identity_access.application.organization import OrganizationService
from packages.identity_access.application.service import IdentityService
from packages.identity_access.domain.policy import Actor
from packages.identity_access.infrastructure.contributor_postgres import (
    PostgresContributorAuthorization,
    PostgresContributorProjection,
)
from packages.identity_access.infrastructure.organization_postgres import (
    PostgresOrganizationRepository,
)
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from packages.presentation.application.people import PeopleService


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorResponse(StrictModel):
    code: str


class OrgUnitProjection(StrictModel):
    org_unit_id: UUID
    display_name: str


class VisibleResourceProjection(StrictModel):
    resource_type: Literal["dashboard", "report", "research"]
    resource_id: UUID
    title: str
    last_activity_at: datetime


class ActivityWindowProjection(StrictModel):
    window_days: Literal[30, 90]
    created_count: int = Field(ge=0)
    published_count: int = Field(ge=0)
    materially_updated_count: int = Field(ge=0)
    maintained_count: int = Field(ge=0)
    coauthored_count: int = Field(ge=0)
    reviewed_count: int = Field(ge=0)
    resolved_count: int = Field(ge=0)
    last_activity_at: datetime | None


class ActivityProjection(StrictModel):
    windows: list[ActivityWindowProjection] = Field(min_length=2, max_length=2)


class ContributorProfileResponse(StrictModel):
    principal_id: UUID
    display_name: str
    title: str | None
    primary_org_unit: OrgUnitProjection
    contribution_labels: list[str]
    expertise_domains: list[str]
    view_variant: Literal["public", "self", "leader", "grantee"]
    visible_resources: list[VisibleResourceProjection]
    visible_resource_count: int = Field(ge=0)
    activity: ActivityProjection | None
    projection_version: str = Field(pattern=r"^[0-9a-f]{64}$")
    projection_updated_at: datetime


class ContributorListResponse(StrictModel):
    people: list[ContributorProfileResponse]
    visible_count: int = Field(ge=0)


def _services(settings: Settings) -> tuple[IdentityService, PeopleService]:
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
    projection = PostgresContributorProjection(connect)
    organization = OrganizationService(PostgresOrganizationRepository(connect))
    authorization = PostgresContributorAuthorization(connect, organization)
    return identity, PeopleService(projection=projection, authorization=authorization)


def _status_for(code: str) -> int:
    if code == "AUTHENTICATION_FAILED":
        return status.HTTP_401_UNAUTHORIZED
    if code == "FORBIDDEN":
        return status.HTTP_403_FORBIDDEN
    if code == "NOT_FOUND":
        return status.HTTP_404_NOT_FOUND
    if code.endswith("CONFLICT"):
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def create_people_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    people_service: PeopleService | None = None,
) -> FastAPI:
    """Build the independently versioned People provider boundary."""

    default_identity, default_people = _services(settings)
    identity = identity_service or default_identity
    people = people_service or default_people
    app = FastAPI(
        title="Custometry People & Creators API",
        version=PEOPLE_API_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(PeopleFailure)
    async def people_failure_handler(_: Request, exc: PeopleFailure) -> JSONResponse:
        return JSONResponse(status_code=_status_for(exc.code), content={"code": exc.code})

    def authenticated(authorization: Annotated[str | None, Header()] = None) -> Actor:
        if authorization is None:
            raise PeopleFailure("AUTHENTICATION_FAILED")
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer" or not token:
            raise PeopleFailure("AUTHENTICATION_FAILED")
        try:
            return identity.authenticate(token)
        except Exception as exc:
            raise PeopleFailure("AUTHENTICATION_FAILED") from exc

    @app.get(
        "/contributors",
        response_model=ContributorListResponse,
        operation_id="list_people_contributors",
    )
    def list_people(
        search: Annotated[str | None, Query(max_length=120)] = None,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        actor: Actor = Depends(authenticated),
    ) -> ContributorListResponse:
        items, count = people.list_people(
            ViewerContext(
                principal_id=actor.principal_id,
                workspace_id=actor.workspace_id,
                permissions=actor.permissions,
            ),
            search=search,
            offset=offset,
            limit=limit,
        )
        return ContributorListResponse(
            people=[ContributorProfileResponse.model_validate(item) for item in items],
            visible_count=count,
        )

    @app.get(
        "/contributors/{principal_id}",
        response_model=ContributorProfileResponse,
        operation_id="get_people_contributor",
    )
    def get_person(
        principal_id: UUID, actor: Actor = Depends(authenticated)
    ) -> ContributorProfileResponse:
        return ContributorProfileResponse.model_validate(
            people.get_person(
                ViewerContext(
                    principal_id=actor.principal_id,
                    workspace_id=actor.workspace_id,
                    permissions=actor.permissions,
                ),
                principal_id=principal_id,
            )
        )

    _ = (people_failure_handler, list_people, get_person)
    return app


__all__ = ["create_people_app"]
