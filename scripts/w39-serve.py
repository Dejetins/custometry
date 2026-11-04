"""Restartable task-only API process for comparable cold/warm benchmark batches."""

import argparse
import json
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--version", choices=["baseline", "candidate"], required=True)
parser.add_argument("--port", type=int, required=True)
parser.add_argument("--workers", type=int, default=1)
parser.add_argument("--runtime", choices=[".runtime/w39/qa"])
args = parser.parse_args()
if args.port not in (58139, 58140, 58142, 58143, 58145, *range(58160, 58176)) or not 1 <= args.workers <= 16:
    raise SystemExit("OWNED_RUNTIME_ARGUMENT_REQUIRED")
runtime = root / ".runtime/w39" / ("candidate" if args.version == "candidate" else "")
if args.runtime:
    runtime = root / args.runtime
env = dict(os.environ) | json.loads((runtime / "connection.json").read_text())
env["CUSTOMETRY_ANALYTICS_ARTIFACT_ROOT"] = str(
    Path(env["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).parent / "artifacts"
)
env["CUSTOMETRY_CORS_ALLOWED_ORIGINS"] = (
    '["http://127.0.0.1:41739","http://127.0.0.1:41740","http://localhost:41740","http://127.0.0.1:41742","http://127.0.0.1:41743","http://127.0.0.1:41741","http://127.0.0.1:41745","http://127.0.0.1:41746","http://localhost:41746"]'
)
env["CUSTOMETRY_IDENTITY_COOKIE_SECURE"] = "false"
source = root if args.version == "candidate" else root / ".runtime/w39/baseline"
env["PYTHONPATH"] = str(source / "apps/api/src") + os.pathsep + str(source) + os.pathsep + str(root / "scripts")
os.chdir(source)
os.execve(
    root / ".venv/bin/python",
    [
        str(root / ".venv/bin/python"),
        "-m",
        "uvicorn",
        "w39_instrumented:create_app" if os.environ.get("W39_INSTRUMENT") == "1" else "custometry_api.main:create_app",
        "--factory",
        "--host",
        "127.0.0.1",
        "--port",
        str(args.port),
        "--workers",
        str(args.workers),
        "--timeout-graceful-shutdown",
        "5",
        "--log-level",
        "warning",
        "--no-access-log",
    ],
    env,
)
