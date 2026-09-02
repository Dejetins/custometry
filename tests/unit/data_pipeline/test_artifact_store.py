from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pyarrow.parquet as pq
import pytest

from packages.artifacts import ArtifactWriteRequest, LocalArtifactStore
from packages.contracts.data_pipeline import DataPipelineFailure


def test_local_artifact_commit_is_atomic_relative_and_idempotent(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path.resolve())
    request = ArtifactWriteRequest(
        artifact_id=uuid4(),
        workspace_id=uuid4(),
        batch_id=uuid4(),
        entity="Receipt",
        pii_class="personal",
    )
    rows = (
        {
            "receipt_id": 1,
            "updated_at": datetime(2026, 1, 1, tzinfo=UTC),
            "net_amount": Decimal("12.34"),
        },
    )

    first = store.write_parquet(request, rows)
    second = store.write_parquet(request, rows)

    assert first == second
    assert not Path(first.relative_uri).is_absolute()
    assert first.content_hash == second.content_hash
    assert first.row_count == 1
    committed = store.resolve(first.relative_uri)
    assert committed.is_file()
    assert pq.read_table(committed).to_pylist()[0]["receipt_id"] == 1
    assert list((tmp_path / ".staging").iterdir()) == []


def test_local_artifact_identity_conflict_and_path_escape_fail_closed(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path.resolve())
    request = ArtifactWriteRequest(uuid4(), uuid4(), uuid4(), "Product")
    store.write_parquet(request, ({"product_id": 1},))

    with pytest.raises(DataPipelineFailure, match="ARTIFACT_IDENTITY_CONFLICT"):
        store.write_parquet(request, ({"product_id": 2},))
    with pytest.raises(DataPipelineFailure, match="ARTIFACT_PATH_ESCAPE"):
        store.resolve("../outside.parquet")
    assert list((tmp_path / ".staging").iterdir()) == []


def test_local_artifact_store_requires_absolute_root(tmp_path: Path) -> None:
    with pytest.raises(DataPipelineFailure, match="ARTIFACT_ROOT_NOT_ABSOLUTE"):
        LocalArtifactStore(Path("relative-artifacts"))
