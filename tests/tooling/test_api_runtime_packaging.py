from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
API_DOCKERFILE = REPOSITORY_ROOT / "apps/api/Dockerfile"


def test_api_runtime_image_contains_execution_and_notification_import_closure() -> None:
    dockerfile = API_DOCKERFILE.read_text(encoding="utf-8")
    site_packages = "/app/.venv/lib/python3.12/site-packages"
    required_packages = (
        "packages/contracts/data_pipeline",
        "packages/contracts/execution",
        "packages/contracts/notifications",
        "packages/execution",
        "packages/notifications",
    )

    for package in required_packages:
        assert (
            f"COPY --chown=10001:10001 {package} {site_packages}/{package}" in dockerfile
        ), f"API runtime image is missing startup import package: {package}"
