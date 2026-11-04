"""Create real synthetic sessions outside timed opens; keep credentials ephemeral."""

import argparse
import json
import os
from pathlib import Path
from uuid import UUID
from custometry_api.config import Settings
from custometry_api.identity.router import create_identity_service

root = Path.cwd()
parser = argparse.ArgumentParser()
parser.add_argument("version", choices=["baseline", "candidate"])
parser.add_argument("label")
args = parser.parse_args()
runtime = root / ".runtime/w39" / ("candidate" if args.version == "candidate" else "")
os.environ.update(json.loads((runtime / "connection.json").read_text()))
service = create_identity_service(Settings())
fixtures = json.loads((root / ".runtime/w39/load-fixtures.json").read_text())
values = []
for index, fixture in enumerate(fixtures):
    tokens = service.login(
        workspace_id=UUID(fixture["workspace"]),
        email=fixture["email"],
        password="synthetic-w39-password",
        device_label=f"W39 {args.label} load {index}",
    )
    values.append(
        [
            dict(
                name=name,
                value=value,
                domain="127.0.0.1",
                path=path,
                httpOnly=hidden,
                secure=False,
                sameSite="Strict",
            )
            for name, value, path, hidden in [
                ("custometry_access", tokens.access_token, "/", True),
                ("custometry_refresh", tokens.refresh_token, "/api/identity", True),
                ("custometry_csrf", tokens.csrf_token, "/", False),
            ]
        ]
    )
output = runtime / "sessions.json"
fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w") as handle:
    json.dump(values, handle)
print("Created 50 real sessions; ephemeral credentials are not included in evidence.")
