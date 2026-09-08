"""Install exact hash-pinned libpq runtime packages into the owned image builder."""

import hashlib
import json
import subprocess
import tempfile
import urllib.request
from pathlib import Path


def main() -> None:
    pins = json.loads(Path("/tmp/libpq-runtime-packages.json").read_text())
    architecture = subprocess.check_output(["dpkg", "--print-architecture"]).decode().strip()
    rows = pins["packages"][architecture]
    with tempfile.TemporaryDirectory(prefix="runtime-debs-") as temporary:
        paths: list[str] = []
        for row in rows:
            if not row["url"].startswith("https://deb.debian.org/") or row["architecture"] != architecture:
                raise ValueError("Invalid pinned runtime package origin/architecture")
            with urllib.request.urlopen(row["url"], timeout=120) as response:
                data = response.read(row["size_bytes"] + 1)
            if len(data) != row["size_bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise ValueError("Runtime package digest mismatch")
            path = Path(temporary) / (row["package"] + ".deb")
            path.write_bytes(data)
            paths.append(str(path))
        subprocess.run(["dpkg", "-i", *paths], check=True)
    for row in rows:
        version = subprocess.check_output(["dpkg-query", "-W", "-f=${Version}", row["package"]]).decode()
        if version != row["version"]:
            raise ValueError("Runtime package installed version mismatch")


if __name__ == "__main__":
    main()
