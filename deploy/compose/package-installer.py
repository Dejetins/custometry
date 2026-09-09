"""Create a new standalone installer toolkit from the selected owned source bytes."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    args.output.mkdir(mode=0o700)
    inventory = []
    for name in (
        "tools/custometry_quality/installation.py",
        "tools/custometry_quality/delivery_consumer.py",
        "deploy/compose/install.sh",
    ):
        target = args.output / name
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        shutil.copyfile(root / name, target)
        target.chmod(0o755 if name.endswith(".sh") else 0o600)
        inventory.append(
            {
                "path": name,
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "size_bytes": target.stat().st_size,
            }
        )
    path = args.output / "installer-files.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "custometry-installer-toolkit/v1",
                "python": "3.12",
                "files": inventory,
            },
            indent=2,
        )
        + "\n"
    )
    path.chmod(0o600)
    print(
        "Standalone installer toolkit created; distribute its inventory through the trusted handoff."
    )


if __name__ == "__main__":
    main()
