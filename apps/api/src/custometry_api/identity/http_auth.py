"""Identity-owned authentication and browser mutation policy for API consumers."""

from typing import Annotated
from fastapi import Request, Header, Cookie

from custometry_api.config import Settings
from packages.identity_access.application.service import IdentityFailure, IdentityService
from packages.identity_access.domain.policy import Actor

ACCESS_COOKIE = "custometry_access"
REFRESH_COOKIE = "custometry_refresh"
CSRF_COOKIE = "custometry_csrf"


class IdentityHTTPAdapter:
    def __init__(self, service: IdentityService, settings: Settings) -> None:
        self.service = service
        self.settings = settings

    def browser_origin(self, request: Request) -> None:
        if request.headers.get("origin") not in self.settings.cors_allowed_origins:
            raise IdentityFailure("CSRF_FAILED")

    def protect_mutation(self, request: Request, actor: Actor) -> None:
        if request.headers.get("authorization"):
            return
        self.browser_origin(request)
        self.service.verify_csrf(actor, request.headers.get("x-csrf-token"))

    def authenticate(
        self,
        request: Request,
        authorization: Annotated[str | None, Header()] = None,
        access_cookie: Annotated[str | None, Cookie(alias=ACCESS_COOKIE)] = None,
    ) -> Actor:
        authorization = request.headers.get("authorization")
        access_cookie = request.cookies.get(ACCESS_COOKIE)
        if authorization is not None:
            scheme, _, token = authorization.partition(" ")
            if scheme.casefold() != "bearer" or not token:
                raise IdentityFailure("AUTHENTICATION_FAILED")
        else:
            token = access_cookie or ""
        if not token:
            raise IdentityFailure("AUTHENTICATION_FAILED")
        actor = self.service.authenticate(token)
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            self.protect_mutation(request, actor)
        return actor
