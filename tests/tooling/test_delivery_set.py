"""Trust ordering and all-or-nothing retrieval using explicit test doubles."""
from __future__ import annotations

import io
import shutil
import stat
import threading
import time
import urllib.error
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import delivery_bundle as bundle
from tools.custometry_quality import delivery_set as delivery

from .test_delivery_companions import fixture


@pytest.mark.parametrize("failure", [None, "signature", "provider", "download", "archive", "second_part", "existing", "obligations"])
def test_whole_set_is_private_atomic_and_signature_precedes_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str | None,
) -> None:
    record, archive = fixture(tmp_path)
    tmp_path.chmod(0o700)
    source = tmp_path / "payload"
    source.mkdir()
    (source / "data").write_bytes(b"validated primary test fixture")
    signature = tmp_path / "signature"
    signature.write_bytes(b"test double, not a signature")
    events: list[str] = []
    output = tmp_path / "accepted"
    if failure == "existing":
        output.mkdir()
        (output / "foreign").write_bytes(b"preserve")
    if failure == "second_part":
        import copy
        extra = copy.deepcopy(record["companions"][0])
        extra["part"] = 2
        extra["artifact_id"] = 2
        extra["artifact_name"] = extra["artifact_name"][:-2] + "02"
        extra["files"][0]["path"] = "sources/second.tar.gz"
        record["companions"].append(extra)

    def trusted(*args: Any) -> dict[str, Any]:
        events.append("signature")
        if failure == "signature":
            raise bundle.BundleError("DELIVERY_SIGNATURE_INVALID")
        return record

    class Provider:
        def __init__(self) -> None:
            events.append("credentials")

        def metadata(self, endpoint: str) -> dict[str, Any]:
            if endpoint.startswith("actions/runs/"):
                return {"id": record["producer"]["run_id"], "head_sha": record["source"]["commit"],
                        "head_branch": "main", "path": ".github/workflows/publish-candidates.yml",
                        "repository": {"full_name": "Dejetins/custometry"},
                        "run_attempt": record["producer"]["run_attempt"], "status": "in_progress"}
            part = record["companions"][0]
            if failure == "provider":
                return {}
            if endpoint.endswith("/2"):
                raise OSError("missing second part")
            return {"id": part["artifact_id"], "name": part["artifact_name"],
                    "digest": "sha256:" + part["provider_sha256"], "size_in_bytes": part["archive_bytes"],
                    "expires_at": part["expires_at"], "expired": False,
                    "workflow_run": {"id": record["producer"]["run_id"],
                                     "head_sha": record["source"]["commit"], "head_branch": "main"},
                    "archive_download_url": delivery.API + "actions/artifacts/1/zip"}

        def download(self, artifact_id: int, target: Path, limit: int) -> None:
            events.append("download")
            if failure == "download":
                target.write_bytes(b"partial")
                raise OSError("interrupted")
            shutil.copyfile(archive, target)
            if failure == "archive":
                target.write_bytes(b"tampered")

    monkeypatch.setattr(delivery, "verify_root", trusted)
    monkeypatch.setattr(delivery, "GitHub", Provider)
    def verified_obligations(*args: Any) -> None:
        events.append("obligations")
        if failure == "obligations":
            raise ValueError("missing source obligation")

    monkeypatch.setattr(delivery.obligations, "verify", verified_obligations)
    if failure is None:
        delivery.verify_set(source, signature, signature, record["source"]["commit"], output)
        assert (output / "main/data").read_bytes() == (source / "data").read_bytes()
        assert (output / "companions/01/sources/component.tar.gz").is_file()
        for path in [output, *output.rglob("*")]:
            assert stat.S_IMODE(path.stat().st_mode) == (0o700 if path.is_dir() else 0o600)
        assert events[:3] == ["signature", "signature", "credentials"]
        assert events[-1] == "obligations"
    else:
        with pytest.raises((ValueError, OSError)):
            delivery.verify_set(source, signature, signature, record["source"]["commit"], output)
        assert not output.exists() or failure == "existing"
        if failure in {"signature", "existing"}:
            assert events == ["signature"]
        if failure == "existing":
            assert (output / "foreign").read_bytes() == b"preserve"
    assert not list(tmp_path.glob(".delivery-quarantine-*"))
    assert not (tmp_path / ".accepted.lock").exists()


@pytest.mark.parametrize("redirect", ["https://example.invalid/payload", "http://x.blob.core.windows.net/x",
                                       "https://blob.core.windows.net.evil.invalid/x", "https://user@x.blob.core.windows.net/x",
                                       "https://x.blob.core.windows.net:444/x", "https://x.blob.core.windows.net/x#secret"])
def test_redirect_restrictions(redirect: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GH_TOKEN", "test-secret")
    client = delivery.GitHub()

    class Opener:
        def open(self, request: Any, timeout: float) -> Any:
            from email.message import Message
            headers = Message()
            headers["Location"] = redirect
            raise urllib.error.HTTPError(request.full_url, 302, "redirect", headers, None)

    monkeypatch.setattr(client, "_opener", Opener())
    with pytest.raises(ValueError, match="DELIVERY_COMPANION_ORIGIN"):
        client.transfer("actions/artifacts/1/zip", io.BytesIO(), 100, archive=True)


@pytest.mark.parametrize("failure", [None, "overflow", "truncated", "redirect_loop"])
def test_stream_limits_and_credentials_do_not_follow_redirects(
    failure: str | None, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from email.message import Message
    monkeypatch.setenv("GH_TOKEN", "test-secret")
    client = delivery.GitHub()
    requests: list[Any] = []

    class Response(io.BytesIO):
        status = 200
        headers = {"Content-Length": "9" if failure == "truncated" else "2"}

    class Opener:
        def open(self, request: Any, timeout: float) -> Any:
            requests.append(request)
            if len(requests) == 1 or failure == "redirect_loop":
                headers = Message()
                headers["Location"] = "https://x.blob.core.windows.net/payload?sig=test"
                raise urllib.error.HTTPError(request.full_url, 302, "redirect", headers, None)
            return Response(b"overflow" if failure == "overflow" else b"ok")

    monkeypatch.setattr(client, "_opener", Opener())
    output = io.BytesIO()
    if failure:
        with pytest.raises(ValueError):
            client.transfer("actions/artifacts/1/zip", output, 4, archive=True)
    else:
        assert client.transfer("actions/artifacts/1/zip", output, 4, archive=True) == 2
        assert output.getvalue() == b"ok"
    assert requests[0].get_header("Authorization") == "Bearer test-secret"
    assert all(request.get_header("Authorization") is None for request in requests[1:])


@pytest.mark.parametrize("field,value", [("head_branch", "foreign"), ("head_sha", "f" * 40),
                                         ("path", ".github/workflows/foreign.yml"),
                                         ("status", "queued"), ("run_attempt", True)])
def test_workflow_observation_is_bound(tmp_path: Path, field: str, value: Any) -> None:
    record, _ = fixture(tmp_path)
    run = {"id": record["producer"]["run_id"], "head_sha": record["source"]["commit"],
           "head_branch": "main", "path": ".github/workflows/publish-candidates.yml",
           "repository": {"full_name": "Dejetins/custometry"},
           "run_attempt": record["producer"]["run_attempt"], "status": "in_progress"}
    run[field] = value
    with pytest.raises(ValueError):
        delivery.verify_run(record, run)


def test_atomic_promotion_never_replaces_existing_empty_directory(tmp_path: Path) -> None:
    source = tmp_path / "quarantine"
    source.mkdir()
    (source / "owned").write_bytes(b"verified")
    target = tmp_path / "target"
    target.mkdir()
    identity = target.stat().st_ino
    with pytest.raises(OSError):
        delivery.promote_new(source, target)
    assert target.stat().st_ino == identity and list(target.iterdir()) == []
    assert (source / "owned").read_bytes() == b"verified"
    target.rmdir()
    delivery.promote_new(source, target)
    assert (target / "owned").read_bytes() == b"verified" and not source.exists()


@pytest.mark.parametrize("slow_headers", [False, True])
def test_real_blocking_http_obeys_absolute_deadline(monkeypatch: pytest.MonkeyPatch, slow_headers: bool) -> None:
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if slow_headers:
                time.sleep(0.5)
            self.send_response(200)
            self.send_header("Content-Length", "5")
            self.end_headers()
            try:
                for _ in range(5):
                    self.wfile.write(b"x")
                    self.wfile.flush()
                    time.sleep(0.1)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def log_message(self, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setenv("GH_TOKEN", "local-test-only")
    monkeypatch.setattr(delivery, "API", f"http://127.0.0.1:{server.server_port}/")
    settings = delivery.companions.policy()
    settings["limits"]["timeout_seconds"] = 0.15
    monkeypatch.setattr(delivery.companions, "policy", lambda: settings)
    client = delivery.GitHub()
    started = time.monotonic()
    try:
        with pytest.raises((ValueError, TimeoutError)):
            client.transfer("actions/artifacts/1/zip", io.BytesIO(), 100, archive=True)
        elapsed = time.monotonic() - started
        assert elapsed < 0.30, elapsed
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)
