from collections.abc import Iterator
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
