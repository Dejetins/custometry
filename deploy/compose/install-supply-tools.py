"""Install only policy-pinned producer binaries into a new owned CI directory."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
import tarfile
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reader-major", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    policy_name = "delivery-verification-policy.v2.json" if args.reader_major == 2 else "delivery-verification-policy.json"
    policy = json.loads((root / policy_name).read_bytes())
    settings = json.loads((root / "delivery-supply-tools.json").read_bytes())
    if platform.system() != "Linux" or platform.machine() not in {"x86_64", "aarch64"}:
        raise SystemExit("DELIVERY_NATIVE_REQUIRED")
    arm = platform.machine() == "aarch64"
    pins = [
        policy["tools"][1 if arm else 0],
        policy["tools"][4 if arm else 3],
        policy["tools"][6 if arm else 5],
    ]
    if args.reader_major == 2:
        pins.append(policy["tools"][8 if arm else 7])
    args.output.mkdir(mode=0o700, parents=True, exist_ok=False)
    for pin in [*pins, {"name": "trusted_root.json", **settings["trusted_root"]}]:
        with urllib.request.urlopen(pin["url"], timeout=300) as response:
            raw = response.read(268435457)
        if len(raw) > 268435456 or hashlib.sha256(raw).hexdigest() != pin["sha256"]:
            raise SystemExit("DELIVERY_TOOL_DIGEST_MISMATCH")
        if pin["url"].endswith(".tar.gz"):
            with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
                members = [m for m in archive if m.name == pin["name"]]
                if len(members) != 1 or not members[0].isfile() or members[0].size > 268435456:
                    raise SystemExit("DELIVERY_TOOL_ARCHIVE_INVALID")
                stream = archive.extractfile(members[0])
                assert stream is not None
                raw = stream.read()
        target = args.output / pin["name"]
        with target.open("xb") as stream:
            stream.write(raw)
        target.chmod(0o600 if pin["name"].endswith(".json") else 0o700)


if __name__ == "__main__":
    main()
