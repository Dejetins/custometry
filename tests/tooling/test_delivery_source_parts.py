"""Source upload preparation/reconciliation; fixtures never authorize a release."""
from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import delivery_source_parts as producer

from .test_delivery_companions import fixture


def test_source_partition_has_bounded_deterministic_private_contents(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source"
    source.mkdir()
    for name in ("a", "b", "c"):
        (source / name).write_bytes(name.encode() * 500)
    settings = producer.companions.policy()
    settings["companions"]["archive_bytes"] = 4096
    monkeypatch.setattr(producer.companions, "policy", lambda: settings)
    output = tmp_path / "parts"
    producer.prepare(source, output)
    plan = json.loads((output / "parts.json").read_bytes())
    assert len(plan["parts"]) == 2
    assert [f["path"] for f in plan["parts"][0]["files"]] == ["a", "b"]
    assert (output / "02/c").read_bytes() == b"c" * 500
    with pytest.raises(ValueError):
        producer.prepare(source, output)
    assert not list(tmp_path.glob(".source-parts-*"))


@pytest.mark.parametrize("failure", ["symlink", "unsafe_name", "empty"])
def test_source_preparation_rejects_unpublishable_tree(tmp_path: Path, failure: str) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "a").write_bytes(b"data")
    if failure == "symlink":
        (source / "link").symlink_to(source / "a")
    elif failure == "unsafe_name":
        (source / "a+unknown").write_bytes(b"data")
    else:
        (source / "a").write_bytes(b"")
    with pytest.raises(ValueError):
        producer.prepare(source, tmp_path / "output")
    assert not (tmp_path / "output").exists()


def test_source_plan_rejects_case_collision_before_retrieval() -> None:
    files = [{"path": path, "sha256": "a" * 64, "size_bytes": 1} for path in ("a", "A")]
    with pytest.raises(ValueError):
        producer.validate_plan({"schema_version": 1, "parts": [{"part": 1, "files": files, "expanded_bytes": 2}]})


@pytest.mark.parametrize("failure", [None, "changed", "duplicate_attempt", "future_attempt", "expired", "missing_complete", "missing_published", "new"])
def test_reconcile_never_reassigns_an_existing_part(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str | None,
) -> None:
    record, archive = fixture(tmp_path)
    plan_part = {key: record["companions"][0][key] for key in ("part", "files", "expanded_bytes")}
    plan = {"schema_version": 1, "parts": [plan_part]}
    part = record["companions"][0]
    name = "custometry-delivery-sources-0.1.0-ms001.1-1-1-01"
    metadata = {"id": 1, "name": name, "digest": "sha256:" + part["provider_sha256"],
                "size_in_bytes": part["archive_bytes"], "expires_at": part["expires_at"], "expired": failure == "expired",
                "workflow_run": {"id": 1, "head_sha": record["source"]["commit"], "head_branch": "main"},
                "archive_download_url": producer.delivery.API + "actions/artifacts/1/zip"}
    if failure == "future_attempt":
        metadata["name"] = name.replace("-1-1-01", "-1-3-01")
    values = [metadata]
    if failure in {"new", "missing_complete", "missing_published"}:
        values = []
    if failure == "missing_published":
        values.append({"name": "custometry-delivery-0.1.0-ms001.1-1-1"})
    if failure == "duplicate_attempt":
        extra = copy.deepcopy(metadata)
        extra["id"] = 2
        extra["name"] = name.replace("-1-1-01", "-1-2-01")
        values.append(extra)
    if failure == "changed":
        plan_part["files"][0]["sha256"] = "0" * 64

    class Provider:
        def metadata(self, endpoint: str) -> dict[str, Any]:
            if endpoint.startswith("actions/runs/"):
                return {"id": 1, "head_sha": record["source"]["commit"], "head_branch": "main",
                        "path": ".github/workflows/publish-candidates.yml", "repository": {"full_name": "Dejetins/custometry"},
                        "run_attempt": 2, "status": "in_progress"}
            if "per_page=" in endpoint:
                return {"artifacts": values}
            return metadata

        def download(self, artifact_id: int, target: Path, limit: int) -> None:
            shutil.copyfile(archive, target)

    monkeypatch.setattr(producer.delivery, "GitHub", Provider)
    output = tmp_path / "reconciliation.json"
    if failure in {None, "new"}:
        producer.reconcile(plan, "0.1.0-ms001.1", 1, 2, record["source"]["commit"], output)
        result = json.loads(output.read_bytes())["parts"][0]
        assert result["exists"] is (failure is None)
        assert result["artifact_name"] == (name if failure is None else name.replace("-1-1-01", "-1-2-01"))
        if failure is None:
            assert result["descriptor"]["artifact_id"] == 1
            assert result["descriptor"]["expires_at"] == metadata["expires_at"]
    else:
        with pytest.raises(ValueError):
            producer.reconcile(plan, "0.1.0-ms001.1", 1, 2, record["source"]["commit"], output,
                               require_complete=failure == "missing_complete")
        assert not output.exists()
