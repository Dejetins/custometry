from collections.abc import Iterator
import os
import pytest
from tests.integration.data_pipeline import conftest as pipeline_fixtures
from tests.integration.data_pipeline.conftest import DataPipelineRuntime

base_runtime = pipeline_fixtures.data_pipeline_runtime


@pytest.fixture
def data_pipeline_runtime(base_runtime: DataPipelineRuntime) -> Iterator[DataPipelineRuntime]:
    try:
        yield base_runtime
    finally:
        # This fixture runs only in the fresh stage-owned database from run_tests.py.
        with base_runtime.connect() as c:
            row = c.execute("SELECT to_regclass('presentation_documents')").fetchone()
            if row is not None and row[0] is not None:
                workspace = (base_runtime.workspace_id,)
                c.execute(
                    "UPDATE presentation_documents SET latest_version_id=NULL WHERE workspace_id=%s",
                    workspace,
                )
                c.execute(
                    "DELETE FROM presentation_versions WHERE document_id IN (SELECT id FROM presentation_documents WHERE workspace_id=%s)",
                    workspace,
                )
                c.execute("DELETE FROM presentation_documents WHERE workspace_id=%s", workspace)
                c.execute("DELETE FROM presentation_references WHERE workspace_id=%s", workspace)
            calendar = c.execute(
                "SELECT to_regclass('semantic_business_calendar_versions')"
            ).fetchone()
            if calendar and calendar[0] and os.environ.get("MS004_S03_OWNED_DATABASE") == "1":
                # Only the disposable S03 database: remove this fixture's migration
                # backfill before its base fixture deletes the workspace. Production
                # immutable-version guards remain enabled throughout all assertions.
                c.execute(
                    "DELETE FROM semantic_workspace_calendar_defaults WHERE workspace_id=%s",
                    (base_runtime.workspace_id,),
                )
                c.execute(
                    "ALTER TABLE semantic_business_calendar_versions DISABLE TRIGGER semantic_calendar_version_guard"
                )
                c.execute(
                    "DELETE FROM semantic_business_calendar_versions WHERE workspace_id=%s",
                    (base_runtime.workspace_id,),
                )
                c.execute(
                    "ALTER TABLE semantic_business_calendar_versions ENABLE TRIGGER semantic_calendar_version_guard"
                )
