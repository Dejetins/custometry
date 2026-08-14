#!/usr/bin/env python3
"""Build the deterministic pending G0 r4 replacement ledger candidate."""

from __future__ import annotations

import argparse
from pathlib import Path


BLOCKED = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
REPLACEMENT = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4"


def build(source: str) -> str:
    blocked_rows = [line for line in source.splitlines() if line.startswith(f"| {BLOCKED} |")]
    if len(blocked_rows) != 1:
        raise ValueError("source ledger must contain exactly one blocked G0 r3 row")
    row = (
        f"| {REPLACEMENT} | G0 | CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4 | "
        ".codex/agents/generated/custometry-ui-design-g0-v2/03-g0-authoritative-sources-r4.md | "
        "pending | — | .codex/delivery/evidence/custometry-ui-design-program-v2/"
        "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4-report.md | .codex/delivery/ui-design-programs/"
        "custometry-v2/evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4/stage-transition.json | "
        "N/A | — | — |"
    )
    source = source.replace(blocked_rows[0], blocked_rows[0] + "\n" + row, 1)

    heading = f"### `{BLOCKED}`"
    start = source.find(heading)
    if start < 0:
        raise ValueError("blocked G0 r3 detail heading is missing")
    next_heading = source.find("\n### `", start + len(heading))
    if next_heading < 0:
        raise ValueError("blocked G0 r3 detail section has no successor heading")
    detail = """

### `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4`

- title: `Repaired active-contract successor G0: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4`
- report_path: `.codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4-report.md`
- expected_touch_zones: `.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**`
- proof_boundary: `current-contract source authority, exact-cover pilot standard, metadata-only equivalence, owner-reviewed baseline, and adjacent-stage readiness; no production implementation, publication, deployment, mobile-specific design, or full WCAG conformance proof`
- blocker_policy: `needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions`
- decision_packet: `none`
- resume_condition: `none`
- resume_evidence_ref: `none`
- resume_evidence_sha256: `none`
- transition_receipt: `.codex/delivery/ui-design-programs/custometry-v2/evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4/stage-transition.json`
- transition_receipt_sha256: `none`
- execution_allowed: `true`
- replaces_stage: `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3`
- repair_evidence_ref: `.codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/repair-evidence.json`
- historical_outcome: `none`
- current_authority: `false`
- invalidated_by_ref: `none`
- superseded_by_stage: `none`
- supersedes_stage: `none`
- incoming_transition_receipt: `none`
- incoming_transition_receipt_sha256: `none`
"""
    return source[:next_heading] + detail + source[next_heading:]


def claim(source: str, claim_id: str, claimed_at: str) -> str:
    replacements = {
        "ledger_status: blocked": "ledger_status: active",
        f"current_stage: {BLOCKED}": f"current_stage: {REPLACEMENT}",
    }
    for old, new in replacements.items():
        if source.count(old) != 1:
            raise ValueError(f"claim candidate requires exactly one {old!r}")
        source = source.replace(old, new, 1)
    lines = source.splitlines()
    replacement_indexes = [index for index, line in enumerate(lines) if line.startswith(f"| {REPLACEMENT} |")]
    if len(replacement_indexes) != 1:
        raise ValueError("claim candidate must contain exactly one G0 r4 row")
    columns = [part.strip() for part in lines[replacement_indexes[0]].strip("|").split("|")]
    columns[4] = "in_progress"
    columns[9] = claim_id
    columns[10] = claimed_at
    lines[replacement_indexes[0]] = "| " + " | ".join(columns) + " |"
    source = "\n".join(lines) + ("\n" if source.endswith("\n") else "")

    return source


def review_ready(source: str) -> str:
    if source.count("ledger_status: active") != 1:
        raise ValueError("review-ready candidate requires one active ledger")
    source = source.replace("ledger_status: active", "ledger_status: awaiting_input", 1)
    lines = source.splitlines()
    indexes = [index for index, line in enumerate(lines) if line.startswith(f"| {REPLACEMENT} |")]
    if len(indexes) != 1:
        raise ValueError("review-ready candidate requires one G0 r4 row")
    columns = [part.strip() for part in lines[indexes[0]].strip("|").split("|")]
    if columns[4] != "in_progress":
        raise ValueError("review-ready candidate requires in_progress G0 r4")
    columns[4] = "needs_input"
    columns[6] = ".codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4-report.md"
    lines[indexes[0]] = "| " + " | ".join(columns) + " |"
    source = "\n".join(lines) + ("\n" if source.endswith("\n") else "")
    start = source.index(f"### `{REPLACEMENT}`")
    end = source.find("\n### `", start + 5)
    if end < 0:
        end = len(source)
    section = source[start:end]
    replacements = {
        "- decision_packet: `none`": "- decision_packet: `.codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/g0-owner-decision-packet.json`",
        "- resume_condition: `none`": "- resume_condition: `owner accepts the exact metadata candidate, baseline, clause inventory, and rendered standard board, or requests bounded corrections`",
    }
    for old, new in replacements.items():
        if section.count(old) != 1:
            raise ValueError(f"review-ready detail requires exactly one {old!r}")
        section = section.replace(old, new, 1)
    source = source[:start] + section + source[end:]
    return source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--claim-id")
    parser.add_argument("--claimed-at")
    parser.add_argument("--review-ready", action="store_true")
    args = parser.parse_args()
    source = args.ledger.read_text(encoding="utf-8")
    if args.review_ready:
        if args.claim_id or args.claimed_at:
            parser.error("--review-ready cannot be combined with claim fields")
        candidate = review_ready(source)
    elif args.claim_id or args.claimed_at:
        if not args.claim_id or not args.claimed_at:
            parser.error("--claim-id and --claimed-at are required together")
        candidate = claim(source, args.claim_id, args.claimed_at)
    else:
        candidate = build(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(candidate, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
