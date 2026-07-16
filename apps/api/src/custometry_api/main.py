"""FastAPI composition root for the runnable Foundation slice."""

from collections.abc import Awaitable, Callable
from typing import Literal

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from custometry_api.health import PostgreSQLReadinessProbe, ReadinessProbe


class HealthResponse(BaseModel):
    """Stable, deliberately small public health payload."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "ready", "not_ready"]
    service: Literal["api"]
    version: str = Field(min_length=1)
    code: str | None = None


class VersionResponse(BaseModel):
    """Public application version payload."""

    model_config = ConfigDict(extra="forbid")

    service: Literal["api"]
    version: str = Field(min_length=1)


def create_app(
    *,
    settings: Settings | None = None,
    readiness_probe: ReadinessProbe | None = None,
) -> FastAPI:
    """Build the application from explicit dependencies."""

    runtime_settings = settings or Settings()
    probe = readiness_probe or PostgreSQLReadinessProbe(runtime_settings)
    app = FastAPI(
        title="Custometry Foundation API",
        version=runtime_settings.version,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.middleware("http")
    async def no_store_health_responses(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)
        if request.url.path.startswith(("/health/", "/version")):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/health/live", response_model=HealthResponse, tags=["health"])
    def live() -> HealthResponse:
        return HealthResponse(status="ok", service="api", version=runtime_settings.version)

    @app.get(
        "/health/ready",
        response_model=HealthResponse,
        responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthResponse}},
        tags=["health"],
    )
    def ready() -> HealthResponse | JSONResponse:
        if probe.is_ready():
            return HealthResponse(status="ready", service="api", version=runtime_settings.version)
        payload = HealthResponse(
            status="not_ready",
            service="api",
            version=runtime_settings.version,
            code="DEPENDENCY_UNAVAILABLE",
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=payload.model_dump(exclude_none=True),
        )

    @app.get("/version", response_model=VersionResponse, tags=["version"])
    def version() -> VersionResponse:
        return VersionResponse(service="api", version=runtime_settings.version)

    _ = (no_store_health_responses, live, ready, version)
    return app


app = create_app()
