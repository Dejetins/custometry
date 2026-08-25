#!/usr/bin/env python3
"""Prepare an atomic ledger candidate for a finished owner-gated review checkpoint."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1: raise SystemExit(f"expected one ledger fragment: {old}")
    return text.replace(old, new, 1)


def update_detail(text: str, stage: str, replacements: list[tuple[str, str]]) -> str:
    heading = f"### `{stage}`\n\n"
    if text.count(heading) != 1: raise SystemExit("stage detail is not unique")
    before, after = text.split(heading, 1)
    if "\n\n### `" in after:
        block, tail = after.split("\n\n### `", 1); suffix = "\n\n### `" + tail
    else: block, suffix = after, ""
    for old, new in replacements: block = replace_once(block, old, new)
    return before + heading + block + suffix


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--ledger",required=True); p.add_argument("--candidate",required=True); p.add_argument("--stage-id",required=True); p.add_argument("--decision-packet",required=True); p.add_argument("--resume-condition",required=True); p.add_argument("--transition-ref",required=True); p.add_argument("--transition-sha256",required=True); a=p.parse_args()
    ledger=Path(a.ledger).resolve(); candidate=Path(a.candidate).resolve(); text=ledger.read_text(encoding="utf-8")
    text=replace_once(text,"ledger_status: active","ledger_status: awaiting_input")
    lines=text.splitlines(); found=0
    for i,line in enumerate(lines):
        if line.startswith(f"| {a.stage_id} |"):
            cols=[x.strip() for x in line.strip().strip("|").split("|")]
            if cols[4] != "in_progress": raise SystemExit("stage row is not in_progress")
            cols[4]="needs_input"; cols[7]=a.transition_ref; lines[i]="| " + " | ".join(cols) + " |"; found+=1
    if found != 1: raise SystemExit("stage row is not unique")
    text="\n".join(lines) + ("\n" if text.endswith("\n") else "")
    text=update_detail(text,a.stage_id,[
        ("- decision_packet: `none`",f"- decision_packet: `{a.decision_packet}`"),
        ("- resume_condition: `none`",f"- resume_condition: `{a.resume_condition}`"),
        ("- transition_receipt: `.codex/delivery/ui-design-programs/custometry-v2/evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3/stage-transition.json`",f"- transition_receipt: `{a.transition_ref}`"),
        ("- transition_receipt_sha256: `none`",f"- transition_receipt_sha256: `{a.transition_sha256}`"),
    ])
    candidate.parent.mkdir(parents=True,exist_ok=True); candidate.write_text(text,encoding="utf-8")
    print(f"source_sha256={sha(ledger)}"); print(f"candidate_sha256={sha(candidate)}")


if __name__ == "__main__": main()
