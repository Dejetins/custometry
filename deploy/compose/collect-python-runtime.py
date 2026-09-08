"""Retain Python/app closure and actual ELF dependencies, without OS admin tools.

Executed only inside the pinned runtime build image. Keep source package records
for copied libraries so scanners still identify their exact distro versions.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    output = Path("/runtime")
    output.mkdir(exist_ok=False)
    copied: set[str] = set()

    def copy_file(source: Path) -> None:
        if not source.is_file():
            raise ValueError(f"Missing runtime file: {source}")
        destination = output / source.relative_to("/")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.add(str(source.resolve()))

    # The venv owns application dependencies. Base-image pip/install launchers are
    # build tooling, not imports of the venv (include-system-site-packages=false).
    for prefix in (Path("/usr/local"), Path("/app")):
        for source in sorted(prefix.rglob("*")):
            if not source.is_file():
                continue
            if prefix == Path("/usr/local") and (
                "site-packages" in source.parts
                or (source.parent == Path("/usr/local/bin") and source.name.startswith("pip"))
            ):
                continue
            copy_file(source)

    for prefix in (Path("/etc/ssl/certs"), Path("/usr/share/zoneinfo")):
        for source in sorted(prefix.rglob("*")):
            if source.is_file():
                copy_file(source)
    for name in ("/etc/passwd", "/etc/group", "/etc/os-release", "/usr/lib/os-release"):
        copy_file(Path(name))
    (output / "etc/nsswitch.conf").write_text("passwd: files\ngroup: files\nhosts: files dns\n")
    (output / "tmp").mkdir(mode=0o1777)
    (output / "tmp").chmod(0o1777)

    # ldd runs only against trusted, pinned Python/wheel ELF inputs in this builder.
    # Its transitive output includes the dynamic interpreter and all linked libs.
    libraries: set[str] = set()
    elf_files: list[str] = []
    for source in sorted(copied):
        with Path(source).open("rb") as stream:
            if stream.read(4) != b"\x7fELF":
                continue
        elf_files.append(source)
    library_directories = sorted({str(Path(source).parent) for source in elf_files})
    for source in elf_files:
        # Private wheel libraries may inherit their importing extension's search
        # path. Inspect their dependencies with those already retained dirs too.
        environment = {**os.environ, "LD_LIBRARY_PATH": ":".join([str(Path(source).parent), *library_directories])}
        result = subprocess.run(["ldd", source], capture_output=True, text=True, env=environment)
        if "not found" in result.stdout:
            raise ValueError(f"Unresolved runtime library: {source}")
        if result.returncode and "not a dynamic executable" not in result.stderr + result.stdout:
            raise ValueError(f"Cannot inspect runtime library: {source}")
        libraries.update(re.findall(r"(?:=>\s+|^\s*)(/[^\s()]+)", result.stdout, re.M))
    for name in sorted(libraries):
        if not (output / name.lstrip("/")).is_file():
            copy_file(Path(name))

    # Preserve the exact installed package paragraphs and copyright for every
    # copied distro library/resource. No scanner exclusion or version relabeling.
    packages: set[str] = set()
    for listing in Path("/var/lib/dpkg/info").glob("*.list"):
        if any(str(Path(name).resolve()) in copied for name in listing.read_text().splitlines()):
            packages.add(listing.name.removesuffix(".list").split(":")[0])
    status: list[str] = []
    for paragraph in Path("/var/lib/dpkg/status").read_text().split("\n\n"):
        package = re.search(r"^Package: (.+)$", paragraph, re.M)
        if package and package[1] in packages:
            status.append(paragraph)
            copyright_file = Path("/usr/share/doc") / package[1] / "copyright"
            if copyright_file.is_file():
                copy_file(copyright_file)
    target = output / "var/lib/dpkg/status"
    target.parent.mkdir(parents=True)
    target.write_text("\n\n".join(status) + "\n")
    evidence = output / "app/notices/runtime-closure.json"
    evidence.write_text(json.dumps({
        "selection": "complete Python/venv plus linked ELF dependencies and required OS resources",
        "source_packages": sorted(packages),
        "elf_dependency_paths": sorted(libraries),
    }, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
