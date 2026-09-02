import json
from uuid import uuid4

from packages.artifacts.domain.model import ArtifactManifest


def test_artifact_manifest_is_relative_redacted_and_versioned() -> None:
    manifest = ArtifactManifest(
        artifact_id=uuid4(),
        workspace_id=uuid4(),
        batch_id=uuid4(),
        entity="Customer",
        artifact_type="landing_parquet",
        relative_uri=f"objects/{uuid4()}.parquet",
        content_hash="a" * 64,
        row_count=1,
        byte_size=100,
        columns=("customer_id", "email"),
        pii_class="sensitive",
        schema_version=1,
    )
    payload = manifest.as_dict()
    encoded = json.dumps(payload)
    assert not str(payload["relative_uri"]).startswith("/")
    assert "password" not in encoded.casefold()
    assert "dsn" not in encoded.casefold()
    assert "snapshot_token" not in encoded.casefold()
    assert payload["schema_version"] == 1
