from pathlib import Path
import json
import hashlib
from uuid import UUID
import psycopg
from packages.presentation.infrastructure.workspace import PostgresWorkspaceRepository

root = Path.cwd()
fixtures = json.loads((root / ".runtime/w39/load-fixtures.json").read_text())
results = []
for version in ["baseline", "candidate"]:
    runtime = root / ".runtime/w39" / ("candidate" if version == "candidate" else "")
    env = json.loads((runtime / "connection.json").read_text())

    def connect():
        return psycopg.connect(
            host=env["CUSTOMETRY_DATABASE_HOST"],
            port=env["CUSTOMETRY_DATABASE_PORT"],
            dbname=env["CUSTOMETRY_DATABASE_NAME"],
            user=env["CUSTOMETRY_DATABASE_USER"],
            password=Path(env["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).read_text().strip(),
            options="-c default_transaction_read_only=on",
        )

    repo = PostgresWorkspaceRepository(connect)
    rows = []
    for f in fixtures:
        doc = repo.read(UUID(f["workspace"]), UUID(f["report"]))
        worksets = doc["composition"]["definition"]["worksets"]
        rows.append(
            dict(
                report=f["report"],
                sha256=hashlib.sha256(
                    json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest(),
                worksets=len(worksets),
                cards=[len(w["cards"]) for w in worksets],
            )
        )
    results.append(dict(version=version, reports=rows))
value = dict(
    equal=results[0]["reports"] == results[1]["reports"],
    reports=50,
    method="Read-only public PostgresWorkspaceRepository.read; canonical JSON SHA-256",
    results=results,
)
(
    root / ".codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/fixture-equality.json"
).write_text(json.dumps(value, indent=2) + "\n")
print({k: v for k, v in value.items() if k != "results"})
assert value["equal"]
