"""Fault controls confined to the explicitly selected S04 disposable installation."""

import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(os.environ["CUSTOMETRY_PACKAGED_ROOT"]).resolve()
assert root.name.startswith("ms002-s04-")
state = json.loads((root / "installation.json").read_text())
assert state["root"] == str(root) and state["id"].startswith("custometry-")
config = root / "config/compose.json"
base = ["docker", "--context", state["engine"]["context"], "compose", "-p", state["id"], "-f", str(config)]


def cp(*args: str) -> None:
    subprocess.run([*base, *args], check=True, capture_output=True, timeout=90)


mode, action = sys.argv[1:]
assert mode in {"database", "schema", "storage", "api"} and action in {"stop", "start"}
if mode == "schema":
    head = "unsupported" if action == "stop" else "0009_notifications"
    cp("exec", "-T", "control-db", "psql", "-U", "custometry", "-d", "custometry", "-c", f"UPDATE alembic_version SET version_num='{head}'")
elif mode == "storage":
    fault = root / "config/s04-storage-fault.json"
    if action == "stop":
        assert not fault.exists()
        data = json.loads(config.read_text())
        mounts = data["services"]["api"]["volumes"]
        assert len(mounts) == 1 and "/var/lib/custometry/artifacts" in mounts[0]
        data["services"]["api"]["volumes"] = [str(root / "artifacts") + ":/var/lib/custometry/artifacts:ro"]
        fault.write_text(json.dumps(data))
        fault.chmod(0o600)
        base[-1] = str(fault)
        cp("up", "-d", "--no-build", "--no-deps", "api")
    else:
        cp("up", "-d", "--no-build", "--no-deps", "--wait", "api")
        fault.unlink(missing_ok=True)
else:
    service = "control-db" if mode == "database" else "api"
    if action == "stop":
        cp("stop", service)
    else:
        cp("up", "-d", "--no-build", "--no-deps", "--wait", service)
print(json.dumps({"mode": mode, "action": action, "result": "pass"}))
