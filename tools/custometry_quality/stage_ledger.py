"""Exclusive local stage-journal transactions for the accepted prompt-pack/v1 profile.

The runner supplies authority and semantic evidence review. This CLI supplies
POSIX mutual exclusion, private session ownership, CAS and atomic replacement.
It never executes a prompt, claims during preflight or publishes artifacts.
"""

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import os
import re
import secrets
import subprocess
import tempfile
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Generator, cast

from .prompt_pack_validation import (
    Invalid,
    Unavailable,
    Pack,
    digest,
    document,
    need,
    field,
    is_array,
)

MARKER = "<!-- prompt-pack-ledger:v1 -->"
CAPABILITY = "custometry-stage-ledger/v1"


def stamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def git_metadata(root: Path) -> Path:
    proc = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--absolute-git-dir"],
        capture_output=True,
        text=True,
        check=False,
    )
    need(proc.returncode == 0, "Updater requires a local Git checkout")
    return Path(proc.stdout.strip()).resolve()


@contextmanager
def exclusive(root: Path, ledger: Path) -> Generator[Path]:
    """Keep the stable lock inode; unlinking it would admit a second owner."""
    directory = git_metadata(root) / "custometry-stage-ledger"
    directory.mkdir(mode=0o700, exist_ok=True)
    need(not directory.is_symlink(), "Updater metadata must not be a symlink")
    key = hashlib.sha256(str(ledger).encode()).hexdigest()
    fd = os.open(directory / f"{key}.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise Invalid(
                "Another journal transaction holds the lock; retry after rereading"
            ) from exc
        yield directory
    finally:
        os.close(fd)


def owner(directory: Path, session: str | None, *, create: bool) -> str:
    need(
        bool(session) and len(session or "") <= 200,
        "Supply the actual runner session via --session or CODEX_THREAD_ID",
    )
    path = directory / (hashlib.sha256(str(session).encode()).hexdigest() + ".owner")
    if create:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            pass
        else:
            with os.fdopen(fd, "wb") as stream:
                stream.write(secrets.token_bytes(32))
                stream.flush()
                os.fsync(stream.fileno())
    need(
        path.is_file() and not path.is_symlink(),
        "Original session ownership unavailable; explicit reconciliation required",
    )
    need(path.stat().st_mode & 0o077 == 0, "Session ownership file must be private")
    raw = path.read_bytes()
    need(len(raw) == 32, "Invalid session ownership file")
    return hashlib.sha256(raw).hexdigest()


def verify_capability(pack: Pack) -> None:
    capability = pack.data.get("claim_capability", {})
    need(capability.get("mechanism") == CAPABILITY, "Unsupported exclusive updater")
    pack.binding(capability.get("evidence"))
    evidence = document(
        pack.path(capability["evidence"]["path"]), "<!-- stage-ledger-capability:v1 -->"
    )
    need(
        evidence.get("mechanism") == CAPABILITY and evidence.get("result") == "pass",
        "Capability evidence is not verified",
    )
    bindings = field(evidence, "implementation")
    need(is_array(bindings) and bool(bindings), "Capability lacks implementation bindings")
    expected = {
        Path(__file__).resolve(),
        Path(__file__).with_name("prompt_pack_validation.py").resolve(),
    }
    observed: set[Path] = set()
    for item in bindings:
        # A completed journal records the implementation used at that time.
        # Draft/active journals still require the exact currently loaded code.
        pack.binding(item, historical=True)
        observed.add(pack.path(item["path"]))
    need(expected <= observed, "Capability does not bind the loaded updater and validator")


def verify_receipt_history(pack: Pack) -> None:
    seen: set[Path] = set()
    for event in pack.data.get("transition_history", []):
        reference = event.get("receipt")
        if reference is None:
            continue
        path = pack.path(reference)
        need(path not in seen, "Receipt path already consumed under another spelling")
        seen.add(path)
        need(
            path.is_file() and digest(path) == event.get("receipt_sha256"),
            "A consumed receipt is missing or changed; preserve immutable history",
        )


def tracked_inputs(pack: Pack) -> dict[Path, str]:
    """Detect evidence/source edits during a cooperative transaction."""
    paths = {pack.triad["plan_doc"], pack.ledger}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            value = cast(dict[str, Any], value)
            if set(value) == {"path", "sha256"}:
                paths.add(pack.path(value["path"]))
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in cast(list[Any], value):
                walk(item)

    walk(pack.data)
    capability = pack.data.get("claim_capability")
    if capability:
        walk(
            document(
                pack.path(capability["evidence"]["path"]), "<!-- stage-ledger-capability:v1 -->"
            )
        )
    for row in pack.rows.values():
        c = row["contract"]
        paths.add(pack.path(c["prompt_path"]))
        for item in c["entry_inputs"]:
            path = pack.path(item["path"])
            if path.is_file():
                paths.add(path)
        receipt = row.get("transition_receipt")
        if receipt:
            path = pack.path(receipt)
            paths.add(path)
            walk(document(path, "<!-- prompt-pack-receipt:v1 -->"))
    return {path: digest(path) for path in paths}


def render(original: str, data: dict[str, Any]) -> str:
    need(original.count(MARKER) == 1, "Expected exactly one ledger record")
    head, tail = original.split(MARKER)
    match = re.match(r"(\s*```json\r?\n)(.*?)(\r?\n```(?:\r?\n|$))", tail, re.S)
    need(match is not None, "Missing ledger JSON block")
    assert match is not None
    return (
        head
        + MARKER
        + match[1]
        + json.dumps(data, indent=2, ensure_ascii=False)
        + match[3]
        + tail[match.end() :]
    )


def replace_ledger(path: Path, text: str, expected: dict[Path, str]) -> None:
    for source, before in expected.items():
        need(
            source.is_file() and digest(source) == before,
            "Source/evidence changed during transaction; reread before retry",
        )
    need(not path.is_symlink(), "Ledger cannot be a symlink")
    fd, name = tempfile.mkstemp(prefix=".stage-ledger-", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), path.stat().st_mode & 0o777)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        need(digest(path) == expected[path], "Ledger changed before replacement")
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary.unlink(missing_ok=True)


def transact(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve(strict=True)
    ledger_arg = args.ledger if args.ledger.is_absolute() else root / args.ledger
    need(not ledger_arg.is_symlink(), "Ledger cannot be a symlink")
    ledger = ledger_arg.resolve(strict=True)
    need(ledger.is_relative_to(root), "Ledger escapes checkout")
    with exclusive(root, ledger) as directory:
        pack = Pack(root, ledger)
        verify_capability(pack)
        verify_receipt_history(pack)
        original = ledger.read_text(encoding="utf-8")
        before = digest(ledger)
        need(args.stage in pack.rows, "Unknown stage")
        row = pack.rows[args.stage]
        if args.action == "preflight":
            executor = None
            if row["status"] in {"in_progress", "needs_input"}:
                need(
                    row.get("claim_owner_sha256") == owner(directory, args.session, create=False),
                    "Foreign claim; original session required",
                )
                executor = row["executor_claim"]
            pack.entry(args.stage, executor=executor)
            return {
                "status": "pass",
                "action": "preflight",
                "stage": args.stage,
                "ledger_sha256": before,
                "proof_boundary": "entry-inputs-and-exclusive-updater-availability",
            }
        need(args.expected_sha256 == before, "Stale ledger SHA-256; reread before retry")
        snapshots = tracked_inputs(pack)
        data = copy.deepcopy(pack.data)
        target = next(r for r in data["stages"] if r["contract"]["id"] == args.stage)
        now = stamp()
        if args.action == "advance":
            current = data["current_stage"]
            need(
                data["ledger_status"] == "active"
                and current in pack.rows
                and pack.rows[current]["status"] == "accepted",
                "Advance requires an accepted current stage",
            )
            need(
                row["status"] == "pending" and not row["execution_allowed"],
                "Advance requires a disallowed pending successor",
            )
            need(
                current in pack.ancestors(args.stage),
                "Target is not a successor of the accepted stage",
            )
            need(
                not any(
                    r["status"] == "pending" and r["execution_allowed"] for r in pack.rows.values()
                ),
                "Another pending stage is already allowed",
            )
            need(
                bool(args.reason) and bool(args.evidence),
                "Advance requires current readiness/authority evidence and reason",
            )
            evidence_path = pack.path(args.evidence)
            need(evidence_path.is_file(), "Missing advancement evidence")
            snapshots[evidence_path] = digest(evidence_path)
            if target["decision_packet"] is not None and args.resolution:
                resolution_path = pack.path(args.resolution)
                need(resolution_path.is_file(), "Missing resolution evidence")
                snapshots[resolution_path] = digest(resolution_path)
                target["decision_packet"]["resolution_evidence"] = args.resolution
            Pack(root, ledger, data).entry(args.stage, require_allowed=False)
            target["execution_allowed"] = True
            data["current_stage"] = args.stage
        elif args.action == "claim":
            need(row["status"] == "pending", "Only a pending stage can be claimed")
            pack.entry(args.stage)
            target.update(
                status="in_progress",
                executor_claim=secrets.token_hex(16),
                claimed_at=now,
                claim_owner_sha256=owner(directory, args.session, create=True),
            )
            data.update(ledger_status="active", current_stage=args.stage)
        else:
            need(
                data["current_stage"] == args.stage
                and row["status"] in {"in_progress", "needs_input"},
                "No current resumable claim",
            )
            need(
                row.get("claim_owner_sha256") == owner(directory, args.session, create=False),
                "Foreign claim; original session required",
            )
            if args.action == "resume":
                need(row["status"] == "needs_input", "Resume requires a paused stage")
                need(bool(args.resolution), "Resume requires actual decision-resolution evidence")
                path = pack.path(args.resolution)
                need(path.is_file(), "Missing resolution evidence")
                snapshots[path] = digest(path)
                target["decision_packet"]["resolution_evidence"] = args.resolution
                target["execution_allowed"] = True
                # Recheck resume eligibility before activating the row.
                Pack(root, ledger, data).entry(args.stage, executor=row["executor_claim"])
                target["status"] = "in_progress"
                data["ledger_status"] = "active"
            else:
                need(row["status"] == "in_progress", "Resume the paused stage before proceeding")
                if args.action == "accept":
                    pack.entry(args.stage, executor=row["executor_claim"])
                    need(bool(args.receipt), "Acceptance requires an immutable receipt")
                    path = pack.path(args.receipt)
                    receipt = pack.receipt(path, expected_stage=args.stage)
                    snapshots[path] = digest(path)
                    for key in ("plan", "prompt", "report", "user_acceptance"):
                        binding = receipt.get(key)
                        if binding is not None:
                            snapshots[pack.path(binding["path"])] = binding["sha256"]
                    for binding in receipt["validation"]["evidence"]:
                        snapshots[pack.path(binding["path"])] = binding["sha256"]
                    need(
                        path
                        not in {
                            pack.path(event["receipt"])
                            for event in data.get("transition_history", [])
                            if event.get("receipt")
                        },
                        "Receipt already consumed; create a new immutable receipt",
                    )
                    args.receipt = os.path.relpath(path, pack.base)
                    target["transition_receipt"] = args.receipt
                    target["execution_allowed"] = False
                    if receipt["status"] == "review_ready":
                        target["status"] = "needs_input"
                        target["decision_packet"] = {
                            "question": "Accept the finished stage result?",
                            "resume_condition": "Record unambiguous user acceptance of the reviewed result and rerun required checks",
                            "resolution_evidence": None,
                        }
                        data["ledger_status"] = "awaiting_input"
                    else:
                        target["status"] = "accepted"
                        if receipt["next_stage_allowed"]:
                            nxt = receipt["next_stage"]["id"]
                            next(r for r in data["stages"] if r["contract"]["id"] == nxt)[
                                "execution_allowed"
                            ] = True
                            data["current_stage"] = nxt
                        candidate = Pack(root, ledger, data)
                        if all(candidate.satisfied(sid) for sid in candidate.rows):
                            data["ledger_status"] = "completed"
                elif args.action in {"pause", "block"}:
                    need(
                        bool(args.reason) and bool(args.evidence),
                        "Pause/block requires reason and evidence",
                    )
                    path = pack.path(args.evidence)
                    need(path.is_file(), "Missing stage evidence")
                    snapshots[path] = digest(path)
                    target["execution_allowed"] = False
                    if args.action == "pause":
                        need(
                            bool(args.question) and bool(args.resume_condition),
                            "Pause requires a precise question and resume condition",
                        )
                        target.update(
                            status="needs_input",
                            decision_packet={
                                "question": args.question,
                                "resume_condition": args.resume_condition,
                                "resolution_evidence": None,
                            },
                        )
                        data["ledger_status"] = "awaiting_input"
                    else:
                        target["status"] = "blocked"
                        data["ledger_status"] = "blocked"
                else:
                    raise Invalid("Unsupported action")
        data.setdefault("transition_history", []).append(
            {
                "stage": args.stage,
                "action": args.action,
                "at": now,
                "from": row["status"],
                "to": target["status"],
                "previous_ledger_sha256": before,
                "receipt": args.receipt,
                "receipt_sha256": digest(pack.path(args.receipt)) if args.receipt else None,
                "evidence_sha256": digest(pack.path(args.evidence)) if args.evidence else None,
                "reason": args.reason,
                "evidence": args.evidence,
            }
        )
        validated = Pack(root, ledger, data)
        if args.action == "accept" and target["status"] == "accepted":
            validated.satisfied(args.stage)
            if (
                validated.data["ledger_status"] == "active"
                and validated.data["current_stage"] != args.stage
            ):
                validated.entry(validated.data["current_stage"])
        verify_receipt_history(validated)
        replace_ledger(ledger, render(original, data), snapshots)
        return {
            "status": "pass",
            "action": args.action,
            "stage": args.stage,
            "stage_status": target["status"],
            "ledger_sha256": digest(ledger),
            "proof_boundary": "exclusive-journal-transition-and-artifact-binding",
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action", choices=("preflight", "claim", "advance", "pause", "resume", "accept", "block")
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--session", default=os.environ.get("CODEX_THREAD_ID"))
    parser.add_argument("--receipt")
    parser.add_argument("--resolution")
    parser.add_argument("--question")
    parser.add_argument("--resume-condition")
    parser.add_argument("--reason")
    parser.add_argument("--evidence")
    args = parser.parse_args(argv)
    try:
        result = transact(args)
    except (Invalid, Unavailable, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "fail", "action": args.action, "errors": [str(exc)]}))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
