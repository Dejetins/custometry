#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LEDGER = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md"
EVIDENCE = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/evidence/family.seg.shell-workspace.baseline-r5"
CANDIDATE = EVIDENCE / "review-ready-final-candidate.md"
TRANSITION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/family.seg.shell-workspace.baseline-r5/stage-transition.json"
DECISION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/family.seg.shell-workspace.baseline-r5/owner-review-decision-packet.md"
STAGE = "G4@family.seg.shell-workspace.baseline-r5"


def replace_once(text: str, before: str, after: str) -> str:
    count = text.count(before)
    if count != 1:
        raise ValueError(f"expected one occurrence, observed {count}: {before[:100]!r}")
    return text.replace(before, after, 1)


def main() -> None:
    transition = ROOT / TRANSITION_REL
    transition_sha = hashlib.sha256(transition.read_bytes()).hexdigest()
    text = LEDGER.read_text(encoding="utf-8")
    text = replace_once(text, "ledger_status: active", "ledger_status: awaiting_input")

    rows = text.splitlines()
    row_index = next(index for index, line in enumerate(rows) if line.startswith(f"| {STAGE} |"))
    cells = [cell.strip() for cell in rows[row_index].strip().strip("|").split("|")]
    if cells[4] != "in_progress":
        raise ValueError(f"unexpected stage row status: {cells[4]}")
    cells[4] = "needs_input"
    cells[7] = TRANSITION_REL
    rows[row_index] = "| " + " | ".join(cells) + " |"
    text = "\n".join(rows) + ("\n" if text.endswith("\n") else "")

    heading = f"### `{STAGE}`\n"
    start = text.index(heading)
    next_heading = text.find("\n### `", start + len(heading))
    end = len(text) if next_heading == -1 else next_heading
    block = text[start:end]
    block = replace_once(block, "- decision_packet: `none`", f"- decision_packet: `{DECISION_REL}`")
    block = replace_once(block, "- resume_condition: `none`", "- resume_condition: `owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_segmentation_family_r5_board`")
    block = replace_once(block, "- transition_receipt_sha256: `none`", f"- transition_receipt_sha256: `{transition_sha}`")
    text = text[:start] + block + text[end:]
    CANDIDATE.write_text(text, encoding="utf-8")
    print(CANDIDATE)


if __name__ == "__main__":
    main()
