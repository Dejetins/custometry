#!/usr/bin/env python3
"""Prepare deterministic owner-acceptance evidence and ledger candidates for G4 promo r5."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "accept_g4_fcst_r5.py"
spec = importlib.util.spec_from_file_location("accept_g4_promo_base", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError("forecast acceptance helper cannot be loaded")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.ROOT = Path(__file__).resolve().parents[4]
base.PROGRAM = HERE
base.LEDGER = HERE / "stage-ledger.md"
base.ARTIFACT = HERE / "artifacts/g4-r5/family-promo-shell-workspace-baseline"
base.EVIDENCE = HERE / "evidence/family.promo.shell-workspace.baseline-r5"
base.PREFLIGHT = base.EVIDENCE / "preflight"
base.REPORT = base.ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.promo.shell-workspace.baseline-r5-report.md"
base.STAGE = "G4@family.promo.shell-workspace.baseline-r5"
base.NEXT_STAGE = "G4@family.dash.shell-workspace.baseline-r5"
base.NEXT_PROMPT = base.ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-10-family-dash-shell-workspace-baseline-r5.md"
base.BOARD = base.ARTIFACT / "review-board.html"
base.DECISION = base.EVIDENCE / "family-acceptance-decision-r5.json"
base.RESPONSE = base.EVIDENCE / "owner-input-response-acceptance-r5.json"
base.TRANSITION = base.EVIDENCE / "stage-transition.json"
base.FAMILY = base.EVIDENCE / "family-acceptance.json"
base.OWNER_INPUT = "принимаю promo"


def owner_requests() -> None:
    base.dump(base.EVIDENCE / "family-acceptance-decision-r5-request.json", {
        "$schema": "owner-decision-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "decision_id": f"{base.STAGE}.finished-result",
        "decision_kind": "family_acceptance",
        "status": "accepted",
        "revision": 5,
        "decision_text": (
            "The owner explicitly accepted the complete HTML review board shown for the G4 "
            "Promotions family. Acceptance covers UI-PROMO-001 in all six required states, "
            "the four responsive-Web anchors, both visible isolated actions, Result Trust, "
            "and applicable pilot visual-language inheritance. It does not authorize production "
            "implementation, publication, deployment, mobile-specific design, another G4 family, "
            "G5, G6, or full WCAG conformance."
        ),
        "owner_input": base.OWNER_INPUT,
        "target": {
            "artifact_kind": "review_board",
            "artifact_id": "family.promo.shell-workspace.baseline-r5",
            "revision": 5,
            "validation_profile": "family_review_ready",
            "path": base.rel(base.BOARD),
        },
        "accepted_values": [{
            "stage_instance_id": base.STAGE,
            "screen_ids": ["UI-PROMO-001"],
            "required_states": list(base.STATES),
            "responsive_web_anchors": [768, 1024, 1440, 1920],
            "source_bound_fixture_action_count": 2,
            "result_trust_visible": True,
            "mobile_scope": "unauthorized",
            "production_implementation": "not_accepted_by_this_decision",
        }],
    })
    base.dump(base.EVIDENCE / "owner-input-response-acceptance-r5-request.json", {
        "$schema": "owner-input-response-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": base.STAGE,
        "decision_packet_ref": base.rel(base.EVIDENCE / "owner-review-decision-packet.md"),
        "response_kind": "visual_acceptance",
        "owner_input": base.OWNER_INPUT,
        "canonical_owner_decision_ref": base.rel(base.DECISION),
    })


def acceptance_request() -> None:
    request = json.loads(
        (base.EVIDENCE / "family-acceptance-request-review-ready.json").read_text(encoding="utf-8")
    )
    request["owner_decision_ref"] = base.rel(base.DECISION)
    base.dump(base.EVIDENCE / "family-acceptance-request.json", request)
    base.dump(base.EVIDENCE / "resolved-owner-decisions.json", [{
        "decision_id": f"{base.STAGE}.finished-result",
        "class": "owner_required",
        "status": "resolved",
        "summary": "The owner explicitly accepted the complete Promotions r5 HTML review board.",
        "resolution_ref": base.rel(base.DECISION),
    }])
    base.dump(base.EVIDENCE / "known-blockers.json", [])


def transition_inputs() -> None:
    family = json.loads(base.FAMILY.read_text(encoding="utf-8"))
    if family.get("result") != "passed" or family.get("owner_decision_ref") != base.rel(base.DECISION):
        raise ValueError("strict accepted promotions family aggregate is not current")
    sys.path.insert(0, "/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
    from validate_stage_transition import hash_bound_source_refs  # type: ignore

    checks = {
        "current_gate": {
            "validation_profile": "family_gate",
            "artifact_ref": base.rel(base.FAMILY),
            "artifact_sha256": base.sha(base.FAMILY),
            "result": "passed",
        },
        "source_freshness": {
            "source_refs": hash_bound_source_refs(base.FAMILY, base.ROOT),
            "drift_classification": "owned_generated_change",
            "stale_refs": [],
        },
        "next_stage_inputs": {
            "next_stage_id": base.NEXT_STAGE,
            "task_ref": base.rel(base.NEXT_PROMPT),
            "unresolved_inputs": [],
        },
        "write_scope": {
            "allowed_paths": [
                ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                ".codex/delivery/evidence/custometry-ui-design-program-v2/**",
                ".codex/delivery/ui-design-programs/custometry-v2/**",
            ],
            "authorization_basis": "active_task_and_repository_contract",
            "outside_scope_paths": [],
        },
        "foreign_changes": {
            "observed_paths": [
                ".codex/AGENTS.md",
                "custometry-technical-blueprint-human-ru.md",
                "custometry-technical-blueprint-ru.md",
                "custometry-ui-blueprint-ru.md",
                "docs/generated/requirement-index.json",
                "packages/contracts/routes/ui-surface-contracts.json",
            ],
            "inseparable_paths": [],
            "disposition": "separable_foreign_changes_preserved",
        },
        "execution_route": {
            "route": "delegated staged-plan-runner with ui-design-program CAS ledger updates",
            "available": True,
        },
        "handoff_artifact": {
            "artifact_ref": base.rel(base.NEXT_PROMPT),
            "artifact_sha256": base.sha(base.NEXT_PROMPT),
            "known_stop_resolution": "none",
        },
    }
    for check_id, facts in checks.items():
        base.dump(base.PREFLIGHT / f"{check_id}.json", {
            "$schema": "stage-preflight-evidence.schema.json",
            "schema_id": "codex.ui-stage-preflight-evidence/v1",
            "check_id": check_id,
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
            "stage_instance_id": base.STAGE,
            "gate_id": "G4",
            "status": "passed",
            "facts": facts,
        })
    base.dump(base.EVIDENCE / "stage-transition-request.json", {
        "$schema": "stage-transition-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "from_stage_id": base.STAGE,
        "from_gate": "G4",
        "from_target": "family.promo.shell-workspace.baseline-r5",
        "from_revision": 5,
        "artifact": base.rel(base.FAMILY),
        "to_gate": "G4",
        "to_stage_id": base.NEXT_STAGE,
        "to_target": "family.dash.shell-workspace.baseline-r5",
        "to_task": base.rel(base.NEXT_PROMPT),
        "status": "ready",
        "owner_decision": base.rel(base.DECISION),
        "decision_inventory": base.rel(base.EVIDENCE / "resolved-owner-decisions.json"),
        "blockers": base.rel(base.EVIDENCE / "known-blockers.json"),
        "checks": [
            f"{key}={base.rel(base.PREFLIGHT / f'{key}.json')}"
            for key in (
                "current_gate", "source_freshness", "next_stage_inputs", "write_scope",
                "foreign_changes", "execution_route", "handoff_artifact",
            )
        ],
        "summary": (
            "The owner accepted the complete Promotions HTML review board; "
            "the strict family gate and adjacent-stage preflight pass."
        ),
        "review_artifacts": [
            base.rel(base.BOARD),
            base.rel(base.EVIDENCE / "review-board-1440.png"),
            base.rel(base.EVIDENCE / "browser-board-qa.json"),
        ],
        "questions": [],
    })
    base.REPORT.write_text(f"""---
artifact_kind: ui_design_stage_report
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
stage_instance_id: {base.STAGE}
status: ready
---

# G4 promotions family accepted report

The owner accepted the complete hash-bound HTML review board for `UI-PROMO-001`,
covering all six required states and responsive-Web anchors 768, 1024, 1440,
and 1920.

- Family aggregate: `{base.rel(base.FAMILY)}` (`passed`)
- Owner decision: `{base.rel(base.DECISION)}`
- Owner input response: `{base.rel(base.RESPONSE)}`
- Review board: `{base.rel(base.BOARD)}`
- Browser QA: `{base.rel(base.EVIDENCE / 'browser-board-qa.json')}`
- Transition: `{base.rel(base.TRANSITION)}` (`ready` after assembly)

The proof boundary excludes production implementation, publication, deployment,
mobile-specific design, full WCAG conformance, real-data side effects, and the
execution of the adjacent G4 family.
""", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=(
        "owner-requests", "resume-candidate", "acceptance-request", "transition-inputs",
        "accepted-candidate",
    ))
    phase = parser.parse_args().phase
    {
        "owner-requests": owner_requests,
        "resume-candidate": base.resume_candidate,
        "acceptance-request": acceptance_request,
        "transition-inputs": transition_inputs,
        "accepted-candidate": base.accepted_candidate,
    }[phase]()


if __name__ == "__main__":
    main()
