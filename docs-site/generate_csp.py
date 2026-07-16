"""Generate a deterministic nginx CSP include for the built MkDocs site.

Material for MkDocs emits small inline bootstrap scripts.  The public docs keep
those scripts without weakening the application-wide policy: every exact script
body is hashed after the pinned documentation build and only those hashes are
allowed inside ``/docs/``.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import re
from pathlib import Path

SCRIPT_PATTERN = re.compile(
    r"<script(?P<attributes>\s[^>]*)?>(?P<body>.*?)</script\s*>",
    flags=re.IGNORECASE | re.DOTALL,
)
SRC_ATTRIBUTE_PATTERN = re.compile(r"(?:^|\s)src\s*=", flags=re.IGNORECASE)


def inline_script_hashes(site_dir: Path) -> list[str]:
    """Return sorted CSP hashes for every inline script in the generated site."""
    hashes: set[str] = set()
    for html_path in sorted(site_dir.rglob("*.html")):
        markup = html_path.read_text(encoding="utf-8")
        for match in SCRIPT_PATTERN.finditer(markup):
            attributes = match.group("attributes") or ""
            if SRC_ATTRIBUTE_PATTERN.search(attributes):
                continue
            body = match.group("body")
            if not body.strip():
                continue
            digest = base64.b64encode(hashlib.sha256(body.encode()).digest()).decode()
            hashes.add(f"'sha256-{digest}'")
    return sorted(hashes)


def render_nginx_include(hashes: list[str]) -> str:
    script_sources = " ".join(["'self'", *hashes])
    policy = (
        "default-src 'self'; "
        f"script-src {script_sources}; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
        "worker-src 'self' blob:; object-src 'none'; base-uri 'self'; "
        "frame-ancestors 'none'; form-action 'self'"
    )
    return (
        f'add_header Content-Security-Policy "{policy}" always;\n'
        'add_header X-Content-Type-Options "nosniff" always;\n'
        'add_header Referrer-Policy "same-origin" always;\n'
        'add_header X-Frame-Options "DENY" always;\n'
        'add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;\n'
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    hashes = inline_script_hashes(args.site_dir)
    if not hashes:
        raise SystemExit("no inline MkDocs scripts found; refusing an empty docs CSP")
    args.output.write_text(render_nginx_include(hashes), encoding="utf-8")


if __name__ == "__main__":
    main()
