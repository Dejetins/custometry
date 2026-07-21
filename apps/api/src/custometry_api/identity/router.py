"""Stable HTTP contracts for Identity and Workspace."""

from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timedelta
from threading import Lock
from time import monotonic
from typing import Annotated, cast
from uuid import UUID

import psycopg
from fastapi import Cookie, Depends, FastAPI, Header, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from packages.identity_access.application.service import IdentityFailure, IdentityService
from packages.identity_access.domain.policy import Actor
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository

ACCESS_COOKIE = "custometry_access"
REFRESH_COOKIE = "custometry_refresh"
CSRF_COOKIE = "custometry_csrf"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorResponse(StrictModel):
    code: str


class BootstrapRequest(StrictModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=12, max_length=1024)
    workspace_key: str = Field(min_length=3, max_length=63)
    workspace_name: str = Field(min_length=1, max_length=160)


class BootstrapResponse(StrictModel):
    principal_id: UUID
    workspace_id: UUID
    workspace_key: str


class LoginRequest(StrictModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=1024)
    workspace_id: UUID
    device_label: str = Field(default="browser", max_length=160)


class SessionResponse(StrictModel):
    session_id: UUID
    workspace_id: UUID
    access_expires_at: str
    absolute_expires_at: str
    csrf_token: str


class MeResponse(StrictModel):
    principal_id: UUID
    workspace_id: UUID
    email: str
    permissions: list[str]
    installation_admin: bool
    token_kind: str


class WorkspaceCreateRequest(StrictModel):
    key: str = Field(min_length=3, max_length=63)
    name: str = Field(min_length=1, max_length=160)


class WorkspaceResponse(StrictModel):
    workspace_id: UUID
    workspace_key: str
    name: str


class InvitationCreateRequest(StrictModel):
    workspace_id: UUID
    email: str = Field(min_length=3, max_length=320)
    roles: list[str] = Field(min_length=1, max_length=8)
    expires_in_hours: int = Field(default=72, ge=1, le=720)


class InvitationResponse(StrictModel):
    invitation_id: UUID
    workspace_id: UUID
    token: str
    expires_at: str


class InvitationAcceptRequest(StrictModel):
    token: str = Field(min_length=20, max_length=256)
    password: str = Field(min_length=12, max_length=1024)


class InvitationAcceptResponse(StrictModel):
    principal_id: UUID


class SessionView(StrictModel):
    id: UUID
    device_label: str
    created_at: str
    last_seen_at: str
    absolute_expires_at: str
    revoked: bool


class SessionListResponse(StrictModel):
    sessions: list[SessionView]


class CountResponse(StrictModel):
    count: int = Field(ge=0)


class MemberView(StrictModel):
    id: UUID
    email: str
    status: str
    roles: list[str]


class MemberListResponse(StrictModel):
    members: list[MemberView]


class ApiTokenCreateRequest(StrictModel):
    name: str = Field(min_length=1, max_length=120)
    scopes: list[str] = Field(min_length=1, max_length=64)
    expires_in_hours: int = Field(default=24, ge=1, le=2160)


class ApiTokenResponse(StrictModel):
    token_id: UUID
    workspace_id: UUID
    token: str
    scopes: list[str]
    expires_at: str


class PasswordChangeRequest(StrictModel):
    current_password: str = Field(min_length=1, max_length=1024)
    new_password: str = Field(min_length=12, max_length=1024)


class PasswordResetCreateRequest(StrictModel):
    principal_id: UUID
    expires_in_minutes: int = Field(default=30, ge=5, le=1440)


class PasswordResetResponse(StrictModel):
    reset_id: UUID
    token: str
    expires_at: str


class PasswordResetConsumeRequest(StrictModel):
    token: str = Field(min_length=20, max_length=256)
    new_password: str = Field(min_length=12, max_length=1024)


class PasswordResetConsumeResponse(StrictModel):
    principal_id: UUID


class SlidingWindowRateLimiter:
    """Small explicit single-process limiter for security-sensitive endpoints."""

    def __init__(self, requests: int, window_seconds: int) -> None:
        self._requests = requests
        self._window = float(window_seconds)
        self._entries: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> None:
        now = monotonic()
        with self._lock:
            entries = self._entries[key]
            while entries and entries[0] <= now - self._window:
                entries.popleft()
            if len(entries) >= self._requests:
                raise IdentityFailure("RATE_LIMITED")
            entries.append(now)


def _service(settings: Settings) -> IdentityService:
    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    try:
        bootstrap_secret = settings.read_bootstrap_token()
    except (OSError, ValueError):
        bootstrap_secret = None
    return IdentityService(
        PostgresIdentityRepository(connect),
        bootstrap_secret=bootstrap_secret,
        access_ttl=timedelta(seconds=settings.identity_access_ttl_seconds),
        refresh_ttl=timedelta(seconds=settings.identity_refresh_ttl_seconds),
    )


def _status_for(code: str) -> int:
    if code in {
        "AUTHENTICATION_FAILED",
        "REFRESH_REUSE_DETECTED",
        "INVITATION_INVALID",
        "PASSWORD_RESET_INVALID",
    }:
        return status.HTTP_401_UNAUTHORIZED
    if code in {"FORBIDDEN", "CSRF_FAILED"}:
        return status.HTTP_403_FORBIDDEN
    if code == "NOT_FOUND":
        return status.HTTP_404_NOT_FOUND
    if code in {"CONFLICT", "BOOTSTRAP_UNAVAILABLE"}:
        return status.HTTP_409_CONFLICT
    if code == "RATE_LIMITED":
        return status.HTTP_429_TOO_MANY_REQUESTS
    return status.HTTP_400_BAD_REQUEST


def _set_session_cookies(response: Response, tokens: object, settings: Settings) -> None:
    response.set_cookie(
        ACCESS_COOKIE,
        getattr(tokens, "access_token"),
        httponly=True,
        secure=settings.identity_cookie_secure,
        samesite="strict",
        path="/identity",
        max_age=settings.identity_access_ttl_seconds,
    )
    response.set_cookie(
        REFRESH_COOKIE,
        getattr(tokens, "refresh_token"),
        httponly=True,
        secure=settings.identity_cookie_secure,
        samesite="strict",
        path="/identity",
        max_age=settings.identity_refresh_ttl_seconds,
    )
    response.set_cookie(
        CSRF_COOKIE,
        getattr(tokens, "csrf_token"),
        httponly=False,
        secure=settings.identity_cookie_secure,
        samesite="strict",
        path="/identity",
        max_age=settings.identity_refresh_ttl_seconds,
    )
    response.headers["Cache-Control"] = "no-store"


def _clear_session_cookies(response: Response, settings: Settings) -> None:
    for name, httponly in ((ACCESS_COOKIE, True), (REFRESH_COOKIE, True), (CSRF_COOKIE, False)):
        response.delete_cookie(
            name,
            path="/identity",
            secure=settings.identity_cookie_secure,
            httponly=httponly,
            samesite="strict",
        )
    response.headers["Cache-Control"] = "no-store"


def create_identity_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
) -> FastAPI:
    """Build the independently versioned Identity API boundary."""

    service = identity_service or _service(settings)
    limiter = SlidingWindowRateLimiter(
        settings.identity_rate_limit_requests,
        settings.identity_rate_limit_window_seconds,
    )
    app = FastAPI(
        title="Custometry Identity API",
        version=settings.version,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(IdentityFailure)
    async def identity_failure_handler(_: Request, exc: IdentityFailure) -> JSONResponse:
        return JSONResponse(status_code=_status_for(exc.code), content={"code": exc.code})

    def limited(request: Request, endpoint: str) -> None:
        host = request.client.host if request.client else "unknown"
        limiter.check(f"{endpoint}:{host}")

    def browser_origin(request: Request) -> None:
        origin = request.headers.get("origin")
        if origin not in settings.cors_allowed_origins:
            raise IdentityFailure("CSRF_FAILED")

    def authenticated(
        authorization: Annotated[str | None, Header()] = None,
        access_cookie: Annotated[str | None, Cookie(alias=ACCESS_COOKIE)] = None,
    ) -> Actor:
        raw: str | None = None
        if authorization:
            scheme, _, candidate = authorization.partition(" ")
            if scheme.casefold() == "bearer" and candidate:
                raw = candidate
        elif access_cookie:
            raw = access_cookie
        if raw is None:
            raise IdentityFailure("AUTHENTICATION_FAILED")
        return service.authenticate(raw)

    def protect_mutation(request: Request, actor: Actor) -> None:
        if request.headers.get("authorization"):
            return
        browser_origin(request)
        service.verify_csrf(actor, request.headers.get("x-csrf-token"))

    @app.post(
        "/bootstrap",
        response_model=BootstrapResponse,
        operation_id="bootstrap_identity",
        responses={409: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def bootstrap(
        payload: BootstrapRequest,
        request: Request,
        bootstrap_token: Annotated[str | None, Header(alias="X-Bootstrap-Token")] = None,
    ) -> BootstrapResponse:
        limited(request, "bootstrap")
        outcome = service.bootstrap(
            presented_secret=bootstrap_token or "",
            email=payload.email,
            password=payload.password,
            workspace_key=payload.workspace_key,
            workspace_name=payload.workspace_name,
        )
        return BootstrapResponse(
            principal_id=outcome.principal_id,
            workspace_id=outcome.workspace_id,
            workspace_key=outcome.workspace_key,
        )

    @app.post(
        "/login",
        response_model=SessionResponse,
        operation_id="login_identity",
        responses={401: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def login(payload: LoginRequest, request: Request, response: Response) -> SessionResponse:
        limited(request, "login")
        tokens = service.login(
            email=payload.email,
            password=payload.password,
            workspace_id=payload.workspace_id,
            device_label=payload.device_label,
        )
        _set_session_cookies(response, tokens, settings)
        return SessionResponse(
            session_id=tokens.session_id,
            workspace_id=tokens.workspace_id,
            access_expires_at=tokens.access_expires_at.isoformat(),
            absolute_expires_at=tokens.absolute_expires_at.isoformat(),
            csrf_token=tokens.csrf_token,
        )

    @app.post(
        "/refresh",
        response_model=SessionResponse,
        operation_id="refresh_identity_session",
        responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
    )
    def refresh(
        request: Request,
        response: Response,
        refresh_cookie: Annotated[str | None, Cookie(alias=REFRESH_COOKIE)] = None,
        csrf_header: Annotated[str | None, Header(alias="X-CSRF-Token")] = None,
    ) -> SessionResponse:
        browser_origin(request)
        if not refresh_cookie or not csrf_header:
            raise IdentityFailure("AUTHENTICATION_FAILED")
        tokens = service.refresh(refresh_cookie, csrf_header)
        _set_session_cookies(response, tokens, settings)
        return SessionResponse(
            session_id=tokens.session_id,
            workspace_id=tokens.workspace_id,
            access_expires_at=tokens.access_expires_at.isoformat(),
            absolute_expires_at=tokens.absolute_expires_at.isoformat(),
            csrf_token=tokens.csrf_token,
        )

    @app.post(
        "/logout",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        response_model=None,
        operation_id="logout_identity_session",
        responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
    )
    def logout(
        request: Request,
        response: Response,
        refresh_cookie: Annotated[str | None, Cookie(alias=REFRESH_COOKIE)] = None,
        csrf_header: Annotated[str | None, Header(alias="X-CSRF-Token")] = None,
    ) -> None:
        browser_origin(request)
        if not refresh_cookie or not csrf_header:
            raise IdentityFailure("AUTHENTICATION_FAILED")
        service.logout(refresh_cookie, csrf_header)
        _clear_session_cookies(response, settings)

    @app.get("/me", response_model=MeResponse, operation_id="get_identity_actor")
    def me(actor: Actor = Depends(authenticated)) -> MeResponse:
        return MeResponse(
            principal_id=actor.principal_id,
            workspace_id=actor.workspace_id,
            email=actor.email,
            permissions=sorted(actor.permissions),
            installation_admin=actor.installation_admin,
            token_kind=actor.token_kind,
        )

    @app.post(
        "/workspaces",
        response_model=WorkspaceResponse,
        operation_id="create_identity_workspace",
        responses={403: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
    )
    def create_workspace(
        payload: WorkspaceCreateRequest,
        request: Request,
        actor: Actor = Depends(authenticated),
    ) -> WorkspaceResponse:
        protect_mutation(request, actor)
        outcome = service.create_workspace(actor, key=payload.key, name=payload.name)
        return WorkspaceResponse(
            workspace_id=outcome.workspace_id,
            workspace_key=outcome.workspace_key,
            name=outcome.name,
        )

    @app.post(
        "/invitations",
        response_model=InvitationResponse,
        operation_id="create_identity_invitation",
        responses={403: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def create_invitation(
        payload: InvitationCreateRequest,
        request: Request,
        response: Response,
        actor: Actor = Depends(authenticated),
    ) -> InvitationResponse:
        limited(request, "invitation")
        protect_mutation(request, actor)
        outcome = service.invite(
            actor,
            workspace_id=payload.workspace_id,
            email=payload.email,
            roles=payload.roles,
            expires_in_hours=payload.expires_in_hours,
        )
        response.headers["Cache-Control"] = "no-store"
        return InvitationResponse(
            invitation_id=outcome.invitation_id,
            workspace_id=outcome.workspace_id,
            token=outcome.token,
            expires_at=outcome.expires_at.isoformat(),
        )

    @app.post(
        "/invitations/accept",
        response_model=InvitationAcceptResponse,
        operation_id="accept_identity_invitation",
        responses={401: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def accept_invitation(
        payload: InvitationAcceptRequest, request: Request
    ) -> InvitationAcceptResponse:
        limited(request, "invitation_accept")
        return InvitationAcceptResponse(
            principal_id=service.accept_invitation(token=payload.token, password=payload.password)
        )

    @app.delete(
        "/invitations/{invitation_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        response_model=None,
        operation_id="revoke_identity_invitation",
        responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    )
    def revoke_invitation(
        invitation_id: UUID,
        request: Request,
        actor: Actor = Depends(authenticated),
    ) -> None:
        protect_mutation(request, actor)
        service.revoke_invitation(actor, invitation_id)

    @app.get(
        "/workspaces/{workspace_id}/members",
        response_model=MemberListResponse,
        operation_id="list_identity_workspace_members",
        responses={404: {"model": ErrorResponse}},
    )
    def members(workspace_id: UUID, actor: Actor = Depends(authenticated)) -> MemberListResponse:
        rows = service.list_members(actor, workspace_id)
        return MemberListResponse(
            members=[
                MemberView(
                    id=UUID(str(row["id"])),
                    email=str(row["email"]),
                    status=str(row["status"]),
                    roles=[str(role) for role in cast(list[object], row["roles"])],
                )
                for row in rows
            ]
        )

    @app.get(
        "/sessions",
        response_model=SessionListResponse,
        operation_id="list_identity_sessions",
    )
    def sessions(
        principal_id: UUID | None = None,
        actor: Actor = Depends(authenticated),
    ) -> SessionListResponse:
        rows = service.list_sessions(actor, principal_id)
        return SessionListResponse(
            sessions=[
                SessionView(
                    id=UUID(str(row["id"])),
                    device_label=str(row["device_label"]),
                    created_at=cast(datetime, row["created_at"]).isoformat(),
                    last_seen_at=cast(datetime, row["last_seen_at"]).isoformat(),
                    absolute_expires_at=cast(datetime, row["absolute_expires_at"]).isoformat(),
                    revoked=bool(row["revoked"]),
                )
                for row in rows
            ]
        )

    @app.delete(
        "/sessions/{session_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        response_model=None,
        operation_id="revoke_identity_session",
        responses={404: {"model": ErrorResponse}},
    )
    def revoke_session(
        session_id: UUID, request: Request, actor: Actor = Depends(authenticated)
    ) -> None:
        protect_mutation(request, actor)
        service.revoke_session(actor, session_id)

    @app.post(
        "/logout-all",
        response_model=CountResponse,
        operation_id="logout_all_identity_sessions",
    )
    def logout_all(
        request: Request, response: Response, actor: Actor = Depends(authenticated)
    ) -> CountResponse:
        protect_mutation(request, actor)
        count = service.logout_all(actor)
        _clear_session_cookies(response, settings)
        return CountResponse(count=count)

    @app.post(
        "/api-tokens",
        response_model=ApiTokenResponse,
        operation_id="create_identity_api_token",
        responses={403: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def create_api_token(
        payload: ApiTokenCreateRequest,
        request: Request,
        response: Response,
        actor: Actor = Depends(authenticated),
    ) -> ApiTokenResponse:
        limited(request, "api_token")
        protect_mutation(request, actor)
        outcome = service.issue_api_token(
            actor,
            name=payload.name,
            scopes=payload.scopes,
            expires_in_hours=payload.expires_in_hours,
        )
        response.headers["Cache-Control"] = "no-store"
        return ApiTokenResponse(
            token_id=outcome.token_id,
            workspace_id=outcome.workspace_id,
            token=outcome.token,
            scopes=list(outcome.scopes),
            expires_at=outcome.expires_at.isoformat(),
        )

    @app.delete(
        "/api-tokens/{token_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        response_model=None,
        operation_id="revoke_identity_api_token",
        responses={404: {"model": ErrorResponse}},
    )
    def revoke_api_token(
        token_id: UUID, request: Request, actor: Actor = Depends(authenticated)
    ) -> None:
        protect_mutation(request, actor)
        service.revoke_api_token(actor, token_id)

    @app.post(
        "/password/change",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        response_model=None,
        operation_id="change_identity_password",
        responses={401: {"model": ErrorResponse}},
    )
    def change_password(
        payload: PasswordChangeRequest,
        request: Request,
        response: Response,
        actor: Actor = Depends(authenticated),
    ) -> None:
        protect_mutation(request, actor)
        service.change_password(
            actor,
            current=payload.current_password,
            replacement=payload.new_password,
        )
        _clear_session_cookies(response, settings)

    @app.post(
        "/password/resets",
        response_model=PasswordResetResponse,
        operation_id="create_identity_password_reset",
        responses={403: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def create_password_reset(
        payload: PasswordResetCreateRequest,
        request: Request,
        response: Response,
        actor: Actor = Depends(authenticated),
    ) -> PasswordResetResponse:
        limited(request, "password_reset")
        protect_mutation(request, actor)
        outcome = service.create_password_reset(
            actor,
            principal_id=payload.principal_id,
            expires_in_minutes=payload.expires_in_minutes,
        )
        response.headers["Cache-Control"] = "no-store"
        return PasswordResetResponse(
            reset_id=outcome.reset_id,
            token=outcome.token,
            expires_at=outcome.expires_at.isoformat(),
        )

    @app.post(
        "/password/resets/consume",
        response_model=PasswordResetConsumeResponse,
        operation_id="consume_identity_password_reset",
        responses={401: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def consume_password_reset(
        payload: PasswordResetConsumeRequest, request: Request
    ) -> PasswordResetConsumeResponse:
        limited(request, "password_reset_consume")
        return PasswordResetConsumeResponse(
            principal_id=service.consume_password_reset(
                token=payload.token, replacement=payload.new_password
            )
        )

    _ = (
        identity_failure_handler,
        bootstrap,
        login,
        refresh,
        logout,
        me,
        create_workspace,
        create_invitation,
        accept_invitation,
        revoke_invitation,
        members,
        sessions,
        revoke_session,
        logout_all,
        create_api_token,
        revoke_api_token,
        change_password,
        create_password_reset,
        consume_password_reset,
    )
    return app
