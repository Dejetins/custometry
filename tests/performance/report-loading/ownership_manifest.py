"""Record W39 file identities against HEAD plus the immutable inherited manifest."""

import hashlib
import json
from pathlib import Path
import subprocess
from datetime import UTC, datetime

root = Path.cwd()
evidence = root / ".codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY"
base = json.loads((evidence / "inherited-baseline.json").read_text())
inherited = {f["path"]: f for f in base["files"]}
paths = set(subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines())
paths.update(
    subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], text=True
    ).splitlines()
)
rows = []
for path in sorted(paths):
    if path.startswith(".codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY"):
        continue  # Evidence has its own references and must not hash itself.
    file = root / path
    current = hashlib.sha256(file.read_bytes()).hexdigest() if file.is_file() else None
    if path in inherited:
        prior = inherited[path]["sha256"]
    else:
        original = subprocess.run(
            ["git", "show", base["baseline_commit"] + ":" + path], capture_output=True
        )
        prior = hashlib.sha256(original.stdout).hexdigest() if original.returncode == 0 else None
    if current != prior:
        rows.append(
            dict(
                path=path,
                baseline_sha256=prior,
                current_sha256=current,
                origin="modified inherited input" if path in inherited else "W39 change",
            )
        )
frozen = json.loads((evidence / "frozen-input-check.json").read_text())
checks = [
    dict(
        path=f["path"],
        unchanged=hashlib.sha256((root / f["path"]).read_bytes()).hexdigest()
        == inherited[f["path"]]["sha256"],
    )
    for f in frozen["files"]
]
(evidence / "frozen-input-check.json").write_text(
    json.dumps(
        dict(
            checked_at=datetime.now(UTC).isoformat(),
            checked=len(checks),
            all_unchanged=all(c["unchanged"] for c in checks),
            files=checks,
        ),
        indent=2,
    )
    + "\n"
)
(evidence / "owned-source-manifest.json").write_text(
    json.dumps(
        dict(
            baseline_commit=base["baseline_commit"],
            basis="Git HEAD plus inherited-baseline.json; equal inherited hashes excluded",
            files=rows,
        ),
        indent=2,
    )
    + "\n"
)
assert all(c["unchanged"] for c in checks)
print(f"{len(rows)} W39 changed/new files; {len(checks)} frozen inputs unchanged")
