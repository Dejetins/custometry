"""Build the pinned local-file Arrow profile and expose exact native provenance.

Executed only inside the owned compiler stage. Final runtime images receive the
wheel, notices and compact provenance. Source delivery is selected separately
from substantiated obligations; optional archives may contain excluded test code.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path("/arrow")


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main() -> None:
    pins_path = Path("/build-inputs/arrow-source-build.json")
    pins = json.loads(pins_path.read_bytes())
    arrow = pins["arrow"]
    ROOT.mkdir()
    archive = ROOT / "arrow-source.tar.gz"
    with urllib.request.urlopen(arrow["url"], timeout=120) as response, archive.open("xb") as target:
        size = 0
        while data := response.read(1048576):
            size += len(data)
            if size > arrow["size_bytes"]:
                raise ValueError("Arrow source size mismatch")
            target.write(data)
    if size != arrow["size_bytes"] or sha(archive) != arrow["sha256"]:
        raise ValueError("Arrow source digest mismatch")
    source_parent = ROOT / "source"
    source_parent.mkdir()
    with tarfile.open(archive) as content:
        content.extractall(source_parent, filter="data")
    source = source_parent / ("arrow-" + arrow["commit"])
    build = ROOT / "build"
    output = ROOT / "out"
    output.mkdir()
    by_name = {row["name"]: row for row in pins["native"]}
    versions = source / "cpp/thirdparty/versions.txt"
    text = versions.read_text()
    modifications = [
        ("ARROW_THRIFT_BUILD_VERSION=0.20.0", "ARROW_THRIFT_BUILD_VERSION=" + by_name["thrift"]["version"]),
        ("ARROW_THRIFT_BUILD_SHA256_CHECKSUM=b5d8311a779470e1502c027f428a1db542f5c051c8e1280ccd2163fa935ff2d6",
         "ARROW_THRIFT_BUILD_SHA256_CHECKSUM=" + by_name["thrift"]["sha256"]),
        ("ARROW_BOOST_BUILD_SHA256_CHECKSUM=9e0ffae35528c35f90468997bc8d99500bf179cbae355415a89a600c38e13574",
         "ARROW_BOOST_BUILD_SHA256_CHECKSUM=" + by_name["boost"]["sha256"]),
    ]
    for original, replacement in modifications:
        if text.count(original) != 1:
            raise ValueError("Arrow source patch context mismatch")
        text = text.replace(original, replacement)
    versions.write_text(text)
    options = {
        "CMAKE_BUILD_TYPE": "Release", "CMAKE_INSTALL_PREFIX": "/opt/arrow", "CMAKE_INSTALL_LIBDIR": "lib",
        "CMAKE_INSTALL_RPATH": "$ORIGIN",
        "ARROW_GIT_ID": arrow["commit"], "ARROW_PACKAGE_KIND": "custometry-source",
        "ARROW_BUILD_STATIC": "OFF", "ARROW_BUILD_SHARED": "ON", "ARROW_DEPENDENCY_SOURCE": "BUNDLED",
        **{f"ARROW_{name}": "ON" for name in ("ACERO", "COMPUTE", "DATASET", "FILESYSTEM", "IPC", "PARQUET", "CSV", "JSON")},
        **{f"ARROW_WITH_{name}": "ON" for name in ("BROTLI", "LZ4", "SNAPPY", "ZLIB", "ZSTD")},
        **{f"ARROW_{name}": "OFF" for name in ("FLIGHT", "S3", "GCS", "AZURE", "GANDIVA", "JEMALLOC", "MIMALLOC", "BUILD_TESTS", "BUILD_EXAMPLES", "BUILD_BENCHMARKS")},
        "PARQUET_REQUIRE_ENCRYPTION": "OFF",
    }
    environment = {**os.environ, "CMAKE_BUILD_PARALLEL_LEVEL": "2", "ARROW_BOOST_URL": by_name["boost"]["url"],
                   "ARROW_THRIFT_URL": by_name["thrift"]["url"]}
    subprocess.run(["cmake", "-S", str(source / "cpp"), "-B", str(build), "-GNinja",
                    *[f"-D{key}={value}" for key, value in options.items()]], env=environment, check=True)
    subprocess.run(["cmake", "--build", str(build), "--parallel", "2"], env=environment, check=True)
    subprocess.run(["cmake", "--install", str(build)], env=environment, check=True)
    environment.update({"ARROW_HOME": "/opt/arrow", "CMAKE_PREFIX_PATH": "/opt/arrow", "LD_LIBRARY_PATH": "/opt/arrow/lib",
                        "PYARROW_BUNDLE_ARROW_CPP": "1", "PYARROW_BUILD_TYPE": "release", "PYARROW_PARALLEL": "2",
                        "SETUPTOOLS_SCM_PRETEND_VERSION": arrow["version"]})
    subprocess.run(["python", "setup.py", "bdist_wheel"], cwd=source / "python", env=environment, check=True)
    wheels = list((source / "python/dist").glob("*.whl"))
    if len(wheels) != 1:
        raise ValueError("Unexpected Arrow wheel count")
    wheel = wheels[0]
    shutil.copyfile(wheel, output / wheel.name)
    native_files: list[dict[str, Any]] = []
    with zipfile.ZipFile(wheel) as content:
        for name in sorted(content.namelist()):
            raw = content.read(name)
            if raw.startswith(b"\x7fELF"):
                if b"OpenSSL 3." in raw:
                    raise ValueError("Unexpected compiled OpenSSL marker")
                native_files.append({"path": name, "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)})
    if not native_files:
        raise ValueError("Missing Arrow native libraries")
    observed: list[dict[str, Any]] = []
    notices: list[dict[str, Any]] = []
    modification_observations: list[dict[str, Any]] = []
    notice_root = output / "notices"
    notice_root.mkdir()
    for row in pins["native"]:
        matches = [path for path in build.rglob(row["filename"]) if path.parent.name == "src" and path.is_file()]
        if len(matches) != 1 or matches[0].stat().st_size != row["size_bytes"] or sha(matches[0]) != row["sha256"]:
            raise ValueError("Native source identity mismatch")
        with tarfile.open(matches[0]) as upstream:
            for member in upstream:
                parts = Path(member.name).parts
                if not member.isfile():
                    continue
                if row["name"] == "utf8proc" and len(parts) == 2 and parts[-1] in {"utf8proc.c", "utf8proc.h", "utf8proc_data.c"}:
                    original = upstream.extractfile(member)
                    assert original is not None
                    raw = original.read()
                    source_file = build / "utf8proc_ep-prefix/src/utf8proc_ep" / parts[-1]
                    original_sha = hashlib.sha256(raw).hexdigest()
                    if not source_file.is_file() or sha(source_file) != original_sha:
                        raise ValueError("Unexpected utf8proc source modification")
                    modification_observations.append({"component": "utf8proc", "source_path": parts[-1],
                                                      "upstream_sha256": original_sha, "compiled_source_sha256": sha(source_file),
                                                      "modified": False})
                root_notice = len(parts) == 2 and ("license" in parts[-1].lower()
                                                 or "copying" in parts[-1].lower() or parts[-1].lower() == "notice")
                library_notice = row["name"] == "lz4" and parts[1:] == ("lib", "LICENSE")
                if not (root_notice or library_notice):
                    continue
                if member.size > 1048576:
                    raise ValueError("Native notice size mismatch")
                original = upstream.extractfile(member)
                assert original is not None
                raw = original.read()
                folder = notice_root / row["name"]
                folder.mkdir(exist_ok=True)
                name = "-".join(parts[1:])
                target = folder / name
                target.write_bytes(raw)
                notices.append({"component": row["name"], "source_path": member.name,
                                "path": row["name"] + "/" + name,
                                "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)})
        observed.append(row)
    if len(modification_observations) != 3:
        raise ValueError("Incomplete utf8proc modification evidence")
    spec = importlib.util.spec_from_file_location("arrow_build_provenance", Path(__file__).with_name("arrow-build-provenance.py"))
    assert spec is not None and spec.loader is not None
    observer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(observer)
    compilation = observer.observe(source, build, pins["internal_native"])
    compiled_path = output / "compilation-inputs.json"
    compiled_path.write_text(json.dumps(compilation, sort_keys=True, separators=(",", ":")) + "\n")
    for filename in ("LICENSE.txt", "NOTICE.txt"):
        raw = (source / filename).read_bytes()
        target = notice_root / ("Arrow-" + filename)
        target.write_bytes(raw)
        notices.append({"component": "arrow-internal", "source_path": filename, "path": target.name,
                        "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)})
    provenance = {"schema_version": 1, "pins_sha256": sha(pins_path), "arrow": arrow,
                  "cmake_options": options, "source_modifications": modifications,
                  "native_sources": observed, "native_files": native_files, "native_notices": notices,
                  "internal_native": pins["internal_native"],
                  "source_modification_observations": modification_observations,
                  "compilation": {"path": "compilation-inputs.json", "sha256": sha(compiled_path),
                                  "size_bytes": compiled_path.stat().st_size},
                  "wheel": {"name": wheel.name, "sha256": sha(wheel), "size_bytes": wheel.stat().st_size}}
    (output / "native-build.json").write_text(json.dumps(provenance, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
