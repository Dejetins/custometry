"""Verify a locally signed v2 root and retrieve every mandatory source part.

This producer/handoff verifier uses independently installed repository policy and
tools. It never executes payload code. Main artifact retrieval and installation
remain separate boundaries; a local root is not evidence of main publication.
"""
from __future__ import annotations

import argparse
import ctypes
import io
import json
import os
import platform
import shutil
import signal
import stat
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO, Generator

from . import delivery_bundle as bundle
from . import delivery_companions as companions
from . import delivery_obligations as obligations
from . import delivery_supply as supply

API = "https://api.github.com/repos/Dejetins/custometry/"


@contextmanager
def absolute_deadline(seconds: float) -> Generator[None]:
    """Interrupt blocking headers and slow-drip body I/O on supported POSIX CLI."""
    bundle.require(os.name == "posix" and threading.current_thread() is threading.main_thread(),
                   "DELIVERY_PLATFORM_UNSUPPORTED")
    bundle.require(signal.getitimer(signal.ITIMER_REAL) == (0.0, 0.0), "DELIVERY_TIMER_CONFLICT")
    previous = signal.getsignal(signal.SIGALRM)

    def expired(signum: int, frame: Any) -> None:
        raise bundle.BundleError("DELIVERY_TIMEOUT")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def promote_new(source: Path, destination: Path) -> None:
    """Atomic same-filesystem no-replace; even an existing empty target wins."""
    library = ctypes.CDLL(None, use_errno=True)
    if platform.system() == "Darwin":
        function = library.renamex_np
        function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        arguments = (os.fsencode(source), os.fsencode(destination), 4)  # RENAME_EXCL
    elif platform.system() == "Linux" and hasattr(library, "renameat2"):
        function = library.renameat2
        function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        arguments = (-100, os.fsencode(source), -100, os.fsencode(destination), 1)  # AT_FDCWD, RENAME_NOREPLACE
    else:
        raise bundle.BundleError("DELIVERY_PLATFORM_UNSUPPORTED")
    function.restype = ctypes.c_int
    if function(*arguments) != 0:
        raise OSError(ctypes.get_errno(), "DELIVERY_PROMOTION_REJECTED")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: Any, msg: Any,
                         headers: Any, newurl: Any) -> None:
        return None


class GitHub:
    """Bounded authenticated API; credentials never cross an artifact redirect."""

    def __init__(self) -> None:
        self._token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not self._token:
            result = subprocess.run(["gh", "auth", "token", "--hostname", "github.com"],
                                    capture_output=True, timeout=30, check=False)
            bundle.require(result.returncode == 0, "DELIVERY_AUTH_REQUIRED")
            self._token = result.stdout.decode("ascii").strip()
        bundle.require(bool(self._token) and "\n" not in self._token and "\r" not in self._token,
                       "DELIVERY_AUTH_REQUIRED")
        self._opener = urllib.request.build_opener(NoRedirect())

    def transfer(self, endpoint: str, destination: BinaryIO, limit: int, *, archive: bool = False) -> int:
        with absolute_deadline(companions.policy()["limits"]["timeout_seconds"]):
            return self._transfer(endpoint, destination, limit, archive=archive)

    def _transfer(self, endpoint: str, destination: BinaryIO, limit: int, *, archive: bool) -> int:
        bundle.require(endpoint.startswith("actions/") and ".." not in endpoint
                       and "#" not in endpoint and ":" not in endpoint, "DELIVERY_COMPANION_ORIGIN")
        settings = companions.policy()["limits"]
        url = API + endpoint
        deadline = time.monotonic() + settings["timeout_seconds"]
        for redirects in range(settings["redirects"] + 1):
            headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
            if redirects == 0:
                headers["Authorization"] = "Bearer " + str(self._token)
            request = urllib.request.Request(url, headers=headers)
            remaining = deadline - time.monotonic()
            bundle.require(remaining > 0, "DELIVERY_TIMEOUT")
            try:
                response = self._opener.open(request, timeout=remaining)
            except urllib.error.HTTPError as exc:
                location = exc.headers.get("Location")
                code = exc.code
                exc.close()
                bundle.require(archive and code in {301, 302, 303, 307, 308} and bool(location)
                               and redirects < settings["redirects"], "DELIVERY_UNAVAILABLE")
                assert location is not None
                parsed = urllib.parse.urlsplit(location)
                bundle.require(parsed.scheme == "https" and parsed.port in {None, 443}
                               and not parsed.username and not parsed.password and not parsed.fragment
                               and bool(parsed.hostname) and any(
                                   str(parsed.hostname).endswith(suffix)
                                   for suffix in companions.policy()["origin"]["redirect_suffixes"]
                               ), "DELIVERY_COMPANION_ORIGIN")
                url = location
                continue
            with response:
                bundle.require(response.status == 200, "DELIVERY_UNAVAILABLE")
                declared = response.headers.get("Content-Length")
                bundle.require(declared is None or declared.isdecimal() and int(declared) <= limit, "DELIVERY_LIMIT")
                total = 0
                while block := response.read(min(1048576, limit + 1 - total)):
                    total += len(block)
                    bundle.require(total <= limit, "DELIVERY_LIMIT")
                    bundle.require(time.monotonic() < deadline, "DELIVERY_TIMEOUT")
                    destination.write(block)
                bundle.require(declared is None or total == int(declared), "DELIVERY_TRUNCATED")
                return total
        raise bundle.BundleError("DELIVERY_UNAVAILABLE")

    def metadata(self, endpoint: str) -> dict[str, Any]:
        output = io.BytesIO()
        self.transfer(endpoint, output, 1048576)
        # Provider descriptions may contain Unicode; only selected identity
        # fields are interpreted. Duplicate keys are still rejected.
        value = json.loads(output.getvalue(), object_pairs_hook=bundle.STRUCTURE._pairs)
        bundle.require(isinstance(value, dict), "DELIVERY_PROVIDER_INVALID")
        return value

    def download(self, artifact_id: int, output: Path, limit: int) -> None:
        with output.open("xb") as stream:
            output.chmod(0o600)
            self.transfer(f"actions/artifacts/{artifact_id}/zip", stream, limit, archive=True)


def verify_run(record: dict[str, Any], observed: dict[str, Any]) -> None:
    producer = record["producer"]
    bundle.require(
        observed.get("id") == producer["run_id"]
        and observed.get("head_sha") == record["source"]["commit"]
        and observed.get("head_branch") == "main"
        and observed.get("path") == companions.policy()["origin"]["workflow"]
        and observed.get("repository", {}).get("full_name") == "Dejetins/custometry"
        and type(observed.get("run_attempt")) is int
        and observed["run_attempt"] >= producer["run_attempt"]
        and (observed.get("status") == "in_progress" or
             observed.get("status") == "completed" and observed.get("conclusion") == "success"),
        "DELIVERY_COMPANION_ORIGIN",
    )


def verify_root(payload: Path, signature: Path, trusted_root: Path, commit: str) -> dict[str, Any]:
    executable = shutil.which("cosign")
    bundle.require(executable is not None, "DELIVERY_TOOL_MISMATCH")
    system = platform.system().lower()
    machine = {"aarch64": "arm64", "arm64": "arm64", "x86_64": "amd64"}.get(platform.machine())
    selected = [entry for entry in companions.policy()["tools"]
                if entry["name"] == "cosign" and entry["url"].endswith(f"cosign-{system}-{machine}")]
    bundle.require(len(selected) == 1 and companions.sha(Path(str(executable))) == selected[0]["sha256"],
                   "DELIVERY_TOOL_MISMATCH")
    for path in (signature, trusted_root):
        bundle.require(path.is_file() and not path.is_symlink() and path.stat().st_size <= 1048576,
                       "DELIVERY_LIMIT")
    record = bundle.STRUCTURE.read_contract(payload / "delivery-manifest.json", reader_major=2)
    companions.validate_descriptors(record)
    # This checks canonical bytes, expected commit, pinned trust root, exact
    # signer/issuer/workflow claims and the complete bounded primary payload.
    supply.verify(payload / "delivery-manifest.json", signature, trusted_root, commit)
    return record


def private_copy(source: Path, destination: Path) -> None:
    """Copy a previously validated primary tree into a private owned quarantine."""
    destination.mkdir(mode=0o700)
    total = count = 0
    for path in sorted(source.rglob("*")):
        target = destination / path.relative_to(source)
        mode = path.lstat().st_mode
        bundle.require(not stat.S_ISLNK(mode))
        if stat.S_ISDIR(mode):
            target.mkdir(mode=0o700)
        else:
            bundle.require(stat.S_ISREG(mode))
            count += 1
            bundle.require(count <= 2048, "DELIVERY_LIMIT")
            with path.open("rb") as original, target.open("xb") as copy:
                target.chmod(0o600)
                length = 0
                while block := original.read(1048576):
                    length += len(block)
                    total += len(block)
                    bundle.require(length <= 67108864 and total <= 536870912, "DELIVERY_LIMIT")
                    copy.write(block)


def verify_set(payload: Path, signature: Path, trusted_root: Path, commit: str, output: Path) -> None:
    # No provider credential access or companion download precedes root trust.
    record = verify_root(payload, signature, trusted_root, commit)
    parent = output.parent
    bundle.require(parent.is_dir() and parent.resolve() == parent.absolute()
                   and stat.S_IMODE(parent.stat().st_mode) == 0o700, "DELIVERY_PRIVATE_TARGET")
    bundle.require(not output.exists() and not output.is_symlink(), "DELIVERY_VERSION_CONFLICT")
    lock = parent / ("." + output.name + ".lock")
    # Exclusive reservation serializes cooperating readers of this private target.
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    try:
        with tempfile.TemporaryDirectory(prefix=".delivery-quarantine-", dir=parent) as temporary:
            quarantine = Path(temporary)
            complete = quarantine / "complete"
            complete.mkdir(mode=0o700)
            private_copy(payload, complete / "main")
            signature_copy = complete / "delivery-manifest.sigstore.json"
            with signature.open("rb") as original, signature_copy.open("xb") as copy:
                signature_copy.chmod(0o600)
                raw = original.read(1048577)
                bundle.require(len(raw) <= 1048576, "DELIVERY_LIMIT")
                copy.write(raw)
            # Recheck the copied bytes to close source-change races before use.
            copied = verify_root(complete / "main", signature_copy, trusted_root, commit)
            bundle.require(copied == record, "DELIVERY_SUBJECT_MISMATCH")
            provider = GitHub()
            verify_run(record, provider.metadata(f"actions/runs/{record['producer']['run_id']}"))
            sources = complete / "companions"
            sources.mkdir(mode=0o700)
            for part in record["companions"]:
                now = datetime.now(timezone.utc)
                metadata = provider.metadata(f"actions/artifacts/{part['artifact_id']}")
                companions.verify_provider(part, metadata, record, now=now)
                archive = quarantine / f"part-{part['part']:02d}.zip"
                provider.download(part["artifact_id"], archive, part["archive_bytes"])
                companions.verify_zip(archive, part, sources / f"{part['part']:02d}")
                archive.unlink()
            # No part may expire while the remaining set is being retrieved.
            companions.validate_descriptors(record)
            obligations.verify(record, complete)
            bundle.require(not output.exists() and not output.is_symlink(), "DELIVERY_VERSION_CONFLICT")
            promote_new(complete, output)
    finally:
        lock.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("payload", "signature", "trusted-root", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--expected-commit", required=True)
    args = parser.parse_args()
    try:
        verify_set(args.payload, args.signature, args.trusted_root, args.expected_commit, args.output)
    except (ValueError, OSError, subprocess.SubprocessError):
        # Transport errors can contain signed URLs. Never print external payloads.
        print("DELIVERY_SET_REJECTED")
        return 1
    print("DELIVERY_SET_VERIFIED_LOCAL_ROOT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
