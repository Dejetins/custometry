"""Safe v2-only failure envelope; legacy response mappings remain separate."""

from fastapi.responses import JSONResponse
from packages.contracts.semantic import Strict


class WorkspaceError(Strict):
    code: str
    retryable: bool


def workspace_error(code: str, cause: BaseException | None = None) -> JSONResponse:
    if code == "ARTIFACT_UNAVAILABLE":
        code = "ARTIFACT_MISSING" if isinstance(cause, FileNotFoundError) else "STORAGE_UNAVAILABLE"
    elif code in {
        "ARTIFACT_INTEGRITY_FAILED",
        "RESULT_ARTIFACT_IDENTITY_CONFLICT",
        "ARTIFACT_BINDING_MISMATCH",
        "RESULT_BINDING_CORRUPT",
    }:
        code = "ARTIFACT_CORRUPT"
    elif code in {"RESULT_STORAGE_UNAVAILABLE"}:
        code = "STORAGE_UNAVAILABLE"
    status = 400
    if code == "AUTHENTICATION_FAILED":
        status = 401
    elif code in {"FORBIDDEN", "CSRF_FAILED"}:
        status = 403
    elif code in {"NOT_FOUND", "SEMANTIC_DATASET_NOT_FOUND", "ARTIFACT_NOT_VISIBLE"}:
        status = 404
    elif code == "WORKSPACE_LIMIT_EXCEEDED":
        status = 413
    elif code.endswith("CONFLICT") or code in {
        "ACCESS_CONTEXT_CHANGED",
        "ARTIFACT_MISSING",
        "ARTIFACT_CORRUPT",
        "REPORT_VERSION_UPGRADE_REQUIRED",
    }:
        status = 409
    elif code == "STORAGE_UNAVAILABLE":
        status = 503
    return JSONResponse(
        status_code=status, content=WorkspaceError(code=code, retryable=status == 503).model_dump()
    )
