from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality.prompt_pack_validation import Pack, contract_digest, digest, document
from tools.custometry_quality.stage_ledger import render

REPOSITORY = Path(__file__).resolve().parents[2]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def marked(marker: str, data: dict[str, Any]) -> str:
    return marker + "\n```json\n" + json.dumps(data) + "\n```\n"


def front(data: dict[str, Any]) -> str:
    return "---\n" + json.dumps(data) + "\n---\n"


def binding(root: Path, path: str) -> dict[str, str]:
    return {"path": path, "sha256": digest(root / path)}


@pytest.fixture
def pack_root(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for filename in ("stage_ledger.py", "prompt_pack_validation.py"):
        destination = tmp_path / "tools/custometry_quality" / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPOSITORY / "tools/custometry_quality" / filename, destination)
    write(tmp_path / "tools/__init__.py", "")
    write(tmp_path / "tools/custometry_quality/__init__.py", "")
    write(tmp_path / "plan.md", front({"version": "1.0.0", "planning_status": "accepted"}))
    plan_binding = {"version": "1.0.0", "sha256": digest(tmp_path / "plan.md")}
    triad = {"plan_doc": "plan.md", "prompt_pack_dir": "prompts", "stage_ledger": "ledger.md"}
    rows: list[dict[str, Any]] = []
    for sid in ("S1", "S2"):
        contract: dict[str, Any] = {
            "id": sid,
            "title": sid,
            "prompt_path": f"prompts/{sid}.md",
            "report_path": f"evidence/{sid}/report.md",
            "receipt_dir": f"evidence/{sid}/receipts",
            "depends_on": [] if sid == "S1" else ["S1"],
            "expected_touches": [],
            "acceptance_criteria": ["A measured result"],
            "proof_boundary": "synthetic CLI test",
            "validation": {
                "profile": "prompt-pack/v1",
                "checks": ["test evidence"],
                "requires_user_acceptance": sid == "S2",
            },
            "entry_inputs": [{"path": "plan.md", "producer_stage": None}],
        }
        write(
            tmp_path / contract["prompt_path"],
            front(
                {
                    "schema_version": "stage-prompt/v1",
                    "prompt_pack_execution": {**triad, "stage_ledger": "../ledger.md"},
                    "stage_contract": contract,
                    "plan_binding": plan_binding,
                }
            ),
        )
        rows.append(
            {
                "contract": contract,
                "status": "pending",
                "execution_allowed": sid == "S1",
                "current_authority": True,
                "executor_claim": None,
                "claimed_at": None,
                "transition_receipt": None,
                "decision_packet": None,
            }
        )
    evidence = {
        "mechanism": "custometry-stage-ledger/v1",
        "result": "pass",
        "implementation": [
            binding(tmp_path, f"tools/custometry_quality/{filename}")
            for filename in ("stage_ledger.py", "prompt_pack_validation.py")
        ],
    }
    write(tmp_path / "capability.md", marked("<!-- stage-ledger-capability:v1 -->", evidence))
    data = {
        "schema_version": "prompt-pack-ledger/v1",
        "prompt_pack_execution": triad,
        "plan_binding": plan_binding,
        "execution_mode": "manual_sequential",
        "ledger_status": "draft",
        "current_stage": None,
        "stages": rows,
        "claim_capability": {
            "mechanism": "custometry-stage-ledger/v1",
            "evidence": binding(tmp_path, "capability.md"),
        },
    }
    write(
        tmp_path / "ledger.md",
        "# Synthetic journal\n"
        + marked("<!-- prompt-pack-ledger:v1 -->", data)
        + "Preserve this history.\n",
    )
    return tmp_path


def command(
    root: Path, action: str, stage: str = "S1", session: str = "test-session", **options: str
) -> list[str]:
    argv = [
        sys.executable,
        "-m",
        "tools.custometry_quality.stage_ledger",
        action,
        "--root",
        str(root),
        "--ledger",
        "ledger.md",
        "--stage",
        stage,
        "--session",
        session,
    ]
    if action != "preflight":
        options.setdefault("expected_sha256", digest(root / "ledger.md"))
    for key, value in options.items():
        argv += ["--" + key.replace("_", "-"), value]
    return argv


def invoke(
    root: Path, action: str, stage: str = "S1", session: str = "test-session", **options: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command(root, action, stage, session, **options),
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(root)},
    )


def receipt(root: Path, sid: str, *, review: bool = False, filename: str = "one.md") -> str:
    pack = Pack(root, root / "ledger.md")
    c = pack.rows[sid]["contract"]
    write(root / c["report_path"], "Synthetic successful result\n")
    evidence_path = f"evidence/{sid}/checks.md"
    write(root / evidence_path, "Synthetic passing checks\n")
    nxt: dict[str, Any] | None = None
    if sid == "S1":
        nc = pack.rows["S2"]["contract"]
        nxt = {
            "id": "S2",
            "prompt": binding(root, nc["prompt_path"]),
            "stage_contract_sha256": contract_digest(nc),
        }
    acceptance = None
    if sid == "S2" and not review:
        write(root / "acceptance.md", "User accepted this synthetic result\n")
        acceptance = binding(root, "acceptance.md")
    value = {
        "schema_version": "prompt-pack-receipt/v1",
        "stage_id": sid,
        "stage_contract_sha256": contract_digest(c),
        "created_at": "2026-09-07T12:00:00Z",
        "status": "review_ready" if review else "ready",
        "plan": binding(root, "plan.md"),
        "prompt": binding(root, c["prompt_path"]),
        "report": binding(root, c["report_path"]),
        "validation": {
            "profile": "prompt-pack/v1",
            "result": "pass",
            "evidence": [binding(root, evidence_path)],
        },
        "user_acceptance": acceptance,
        "next_stage": nxt,
        "next_stage_allowed": nxt is not None,
        "handoff_reason": "Synthetic successor or final completion",
    }
    path = c["receipt_dir"] + "/" + filename
    write(root / path, marked("<!-- prompt-pack-receipt:v1 -->", value))
    return path


def assert_pass(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    assert result.returncode == 0, result.stdout + result.stderr
    value = json.loads(result.stdout)
    assert value["status"] == "pass"
    return value


def test_preflight_does_not_claim_or_change_ledger(pack_root: Path) -> None:
    before = (pack_root / "ledger.md").read_bytes()
    assert_pass(invoke(pack_root, "preflight"))
    assert (pack_root / "ledger.md").read_bytes() == before
    assert not list((pack_root / ".git/custometry-stage-ledger").glob("*.owner"))


def test_two_competing_processes_claim_once(pack_root: Path) -> None:
    first = command(pack_root, "claim", session="one")
    second = command(pack_root, "claim", session="two")
    processes = [
        subprocess.Popen(
            argv,
            cwd=pack_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "PYTHONPATH": str(pack_root)},
        )
        for argv in (first, second)
    ]
    for process in processes:
        process.communicate(timeout=10)
    assert sorted(p.returncode for p in processes) == [0, 1]
    value = document(pack_root / "ledger.md", "<!-- prompt-pack-ledger:v1 -->")
    assert value["stages"][0]["status"] == "in_progress"
    assert len(value["transition_history"]) == 1
    assert "Preserve this history." in (pack_root / "ledger.md").read_text()


def test_lock_is_released_after_process_death(pack_root: Path) -> None:
    script = "from pathlib import Path; import time; from tools.custometry_quality.stage_ledger import exclusive\nwith exclusive(Path.cwd(), Path('ledger.md').resolve()):\n print('locked', flush=True)\n time.sleep(30)"
    holder = subprocess.Popen(
        [sys.executable, "-c", script],
        cwd=pack_root,
        stdout=subprocess.PIPE,
        text=True,
        env={**os.environ, "PYTHONPATH": str(pack_root)},
    )
    try:
        assert holder.stdout is not None
        assert holder.stdout.readline().strip() == "locked"
        assert invoke(pack_root, "claim").returncode == 1
    finally:
        holder.kill()
        holder.wait(timeout=5)
    assert_pass(invoke(pack_root, "claim"))


def test_stale_claim_and_foreign_session_fail_without_writes(pack_root: Path) -> None:
    stale = digest(pack_root / "ledger.md")
    assert_pass(invoke(pack_root, "claim"))
    before = (pack_root / "ledger.md").read_bytes()
    assert invoke(pack_root, "claim", expected_sha256=stale).returncode == 1
    assert invoke(pack_root, "preflight", session="foreign").returncode == 1
    assert invoke(pack_root, "claim", stage="S2").returncode == 1
    assert (pack_root / "ledger.md").read_bytes() == before


def test_real_sequence_pause_resume_receipts_and_final_acceptance(pack_root: Path) -> None:
    assert_pass(invoke(pack_root, "claim"))
    write(pack_root / "question.md", "Need the concrete missing input")
    assert_pass(
        invoke(
            pack_root,
            "pause",
            question="Select target",
            resume_condition="Target provided",
            reason="Missing target",
            evidence="question.md",
        )
    )
    assert invoke(pack_root, "claim", stage="S2").returncode == 1
    write(pack_root / "answer.md", "User selected the target")
    assert_pass(invoke(pack_root, "resume", resolution="answer.md"))
    assert_pass(invoke(pack_root, "accept", receipt=receipt(pack_root, "S1")))
    assert_pass(invoke(pack_root, "claim", stage="S2", session="next-session"))
    ref = receipt(pack_root, "S2", review=True)
    assert_pass(invoke(pack_root, "accept", stage="S2", session="next-session", receipt=ref))
    assert Pack(pack_root, pack_root / "ledger.md").data["ledger_status"] == "awaiting_input"
    write(pack_root / "decision.md", "User accepted reviewed final result")
    assert_pass(
        invoke(pack_root, "resume", stage="S2", session="next-session", resolution="decision.md")
    )
    final = receipt(pack_root, "S2", filename="two.md")
    assert_pass(invoke(pack_root, "accept", stage="S2", session="next-session", receipt=final))
    assert Pack(pack_root, pack_root / "ledger.md").data["ledger_status"] == "completed"
    assert (pack_root / ref).is_file()
    assert invoke(pack_root, "claim", stage="S2", session="next-session").returncode == 1


@pytest.mark.parametrize(
    "changed",
    ["plan.md", "capability.md", "prompts/S1.md", "tools/custometry_quality/stage_ledger.py"],
)
def test_changed_bound_input_rejects_claim(pack_root: Path, changed: str) -> None:
    path = pack_root / changed
    text = path.read_text()
    path.write_text(
        text.replace("stage_contract", "changed_contract")
        if changed.startswith("prompts/")
        else text + "\n# Changed\n"
    )
    before = (pack_root / "ledger.md").read_bytes()
    assert invoke(pack_root, "claim").returncode == 1
    assert (pack_root / "ledger.md").read_bytes() == before


def test_changed_receipt_evidence_rejects_acceptance(pack_root: Path) -> None:
    assert_pass(invoke(pack_root, "claim"))
    ref = receipt(pack_root, "S1")
    write(pack_root / "evidence/S1/checks.md", "Changed after receipt")
    before = (pack_root / "ledger.md").read_bytes()
    assert invoke(pack_root, "accept", receipt=ref).returncode == 1
    assert (pack_root / "ledger.md").read_bytes() == before


def test_escaping_and_duplicate_input_fail_closed(pack_root: Path) -> None:
    ledger = pack_root / "ledger.md"
    data = document(ledger, "<!-- prompt-pack-ledger:v1 -->")
    data["stages"][0]["contract"]["report_path"] = "../outside.md"
    ledger.write_text(render(ledger.read_text(), data))
    assert invoke(pack_root, "claim").returncode == 1
    ledger.write_text(
        ledger.read_text().replace(
            '"ledger_status": "draft"', '"ledger_status": "draft", "ledger_status": "active"'
        )
    )
    assert invoke(pack_root, "claim").returncode == 1


def test_atomic_write_failure_preserves_ledger(
    pack_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tools.custometry_quality import stage_ledger

    path = pack_root / "ledger.md"
    before = path.read_bytes()

    def fail_replace(_source: Any, _target: Any) -> None:
        raise OSError("simulated failure before replacement")

    monkeypatch.setattr(stage_ledger.os, "replace", fail_replace)
    with pytest.raises(OSError):
        stage_ledger.replace_ledger(path, "replacement", {path: hashlib.sha256(before).hexdigest()})
    assert path.read_bytes() == before
    assert not list(pack_root.glob(".stage-ledger-*"))


def test_late_successor_advancement_preserves_accepted_receipt(pack_root: Path) -> None:
    assert_pass(invoke(pack_root, "claim"))
    ref = receipt(pack_root, "S1")
    path = pack_root / ref
    value = document(path, "<!-- prompt-pack-receipt:v1 -->")
    value["next_stage_allowed"] = False
    write(path, marked("<!-- prompt-pack-receipt:v1 -->", value))
    before = path.read_bytes()
    assert_pass(invoke(pack_root, "accept", receipt=ref))
    accepted = Pack(pack_root, pack_root / "ledger.md").rows["S1"]
    assert invoke(pack_root, "claim", stage="S2", session="next").returncode == 1
    write(pack_root / "ready.md", "Actual next-stage inputs and execution authority reviewed")
    assert_pass(
        invoke(
            pack_root,
            "advance",
            stage="S2",
            session="next",
            reason="Inputs now ready",
            evidence="ready.md",
        )
    )
    assert Pack(pack_root, pack_root / "ledger.md").rows["S1"] == accepted
    assert path.read_bytes() == before
    assert_pass(invoke(pack_root, "claim", stage="S2", session="next"))


@pytest.mark.parametrize("action,expected", [("pause", "needs_input"), ("block", "blocked")])
def test_input_loss_can_be_recorded(pack_root: Path, action: str, expected: str) -> None:
    ledger = pack_root / "ledger.md"
    data = document(ledger, "<!-- prompt-pack-ledger:v1 -->")
    contract = data["stages"][0]["contract"]
    contract["entry_inputs"].append({"path": "required.txt", "producer_stage": None})
    prompt = pack_root / contract["prompt_path"]
    prompt_data = document(prompt, frontmatter=True)
    prompt_data["stage_contract"] = contract
    write(prompt, front(prompt_data))
    write(ledger, render(ledger.read_text(), data))
    write(pack_root / "required.txt", "Available at claim")
    assert_pass(invoke(pack_root, "claim"))
    (pack_root / "required.txt").unlink()
    write(pack_root / "lost.md", "Observed required input disappeared")
    assert_pass(
        invoke(
            pack_root,
            action,
            reason="Input lost",
            evidence="lost.md",
            question="Restore input?",
            resume_condition="Input restored",
        )
    )
    assert Pack(pack_root, ledger).rows["S1"]["status"] == expected


@pytest.mark.parametrize("alias", ["relative", "dot", "absolute"])
def test_receipt_alias_cannot_replace_consumed_history(pack_root: Path, alias: str) -> None:
    assert_pass(invoke(pack_root, "claim"))
    assert_pass(invoke(pack_root, "accept", receipt=receipt(pack_root, "S1")))
    assert_pass(invoke(pack_root, "claim", stage="S2"))
    ref = receipt(pack_root, "S2", review=True)
    assert_pass(invoke(pack_root, "accept", stage="S2", receipt=ref))
    write(pack_root / "decision.md", "Accepted reviewed result")
    assert_pass(invoke(pack_root, "resume", stage="S2", resolution="decision.md"))
    receipt(pack_root, "S2")  # Deliberately replace a consumed immutable receipt.
    reference = {"relative": ref, "dot": "./" + ref, "absolute": str(pack_root / ref)}[alias]
    before = (pack_root / "ledger.md").read_bytes()
    assert invoke(pack_root, "accept", stage="S2", receipt=reference).returncode == 1
    assert (pack_root / "ledger.md").read_bytes() == before
