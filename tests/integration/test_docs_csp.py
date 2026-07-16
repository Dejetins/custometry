from __future__ import annotations

import base64
import hashlib
import subprocess
import sys
from pathlib import Path


def test_docs_csp_hashes_exact_inline_scripts(tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    script = "window.__md_scope=new URL('/',location)"
    (site / "index.html").write_text(
        f'<script src="bundle.js"></script><script>{script}</script>', encoding="utf-8"
    )
    output = tmp_path / "docs-csp.conf"

    completed = subprocess.run(
        [sys.executable, "docs-site/generate_csp.py", str(site), str(output)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
    policy = output.read_text(encoding="utf-8")
    assert f"'sha256-{digest}'" in policy
    assert "script-src 'self' 'unsafe-inline'" not in policy
    assert "style-src 'self' 'unsafe-inline'" in policy
