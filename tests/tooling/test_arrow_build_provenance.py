"""Reject incomplete/stale compiler evidence before source-scope classification."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality.delivery_native import validate_compilation

SPEC = importlib.util.spec_from_file_location(
    "arrow_provenance", Path(__file__).resolve().parents[2] / "deploy/compose/arrow-build-provenance.py")
assert SPEC is not None and SPEC.loader is not None
observer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(observer)


def test_actual_ninja_dependency_format() -> None:
    raw = "a.cc.o: #deps 2, deps mtime 1788863630137610004 (VALID)\n    /src/a.cc\n    /src/a.h\n\nb.o: #deps 1, deps mtime 12 (VALID)\n    /src/b.c\n"
    assert observer.parse_dependencies(raw) == [("a.cc.o", ["/src/a.cc", "/src/a.h"]), ("b.o", ["/src/b.c"])]


@pytest.mark.parametrize("raw", [
    "a.o: #deps 2, deps mtime 1 (VALID)\n    /src/a.c\n",
    "a.o: #deps 1, deps mtime 1 (STALE)\n    /src/a.c\n",
    "    /src/a.c\n", "unsupported dependency output\n",
])
def test_incomplete_or_stale_evidence_fails(raw: str) -> None:
    with pytest.raises(ValueError):
        observer.parse_dependencies(raw)


def test_external_iobuf_is_preserved_and_missing_reference_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, build = tmp_path / "source", tmp_path / "build"
    source.mkdir()
    build.mkdir()
    owned = source / "header.h"
    owned.write_text("owned header\n")
    external = tmp_path / "external/folly/io/IOBuf.h"
    external.parent.mkdir(parents=True)
    external.write_text("external input must remain observable\n")
    (build / "build.ninja").write_text("fixture\n")
    (build / "object.o").write_bytes(b"actual fixture object")
    raw = f"object.o: #deps 2, deps mtime 1 (VALID)\n    {owned}\n    {external}\n"
    def ninja_output(*args: Any, **kwargs: Any) -> str:
        return raw

    monkeypatch.setattr(observer.subprocess, "check_output", ninja_output)
    internal = [{"name": "example", "files": [observer.file_record(owned, "header.h")]}]
    proof: dict[str, Any] = observer.observe(source, build, internal)
    assert proof["objects"][0]["dependency_count"] == 2
    assert len(proof["inputs"]) == 2
    assert any("folly/io/IOBuf.h" in row["path"] for row in proof["inputs"])
    validate_compilation(proof, {"internal_native": internal})
    proof["inputs"] = [row for row in proof["inputs"] if "IOBuf" not in row["path"]]
    with pytest.raises(ValueError):
        validate_compilation(proof, {"internal_native": internal})
