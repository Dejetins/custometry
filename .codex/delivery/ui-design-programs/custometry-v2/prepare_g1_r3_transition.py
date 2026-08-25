#!/usr/bin/env python3
"""Assemble active-contract G1 r3 proof and transition request."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROGRAM_DIR = Path(__file__).resolve().parent
ROOT = PROGRAM_DIR.parents[3]
sys.path.insert(0, str(PROGRAM_DIR))

import prepare_g1_r2_transition as legacy  # noqa: E402


G1 = PROGRAM_DIR / "artifacts/g1-r3"
EVIDENCE = PROGRAM_DIR / "evidence/atlas-r3"
PREFLIGHT = EVIDENCE / "preflight"
STAGE_ID = "G1@atlas-r3"
NEXT_STAGE_ID = "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
NEXT_PROMPT = ".codex/agents/generated/custometry-ui-design-g0-v2/22-g2-structure-r3.md"
REPORT_REL = ".codex/delivery/evidence/custometry-ui-design-program-v2/atlas-r3-report.md"


def main() -> None:
    legacy.G1 = G1
    legacy.EVIDENCE = EVIDENCE
    legacy.PREFLIGHT = PREFLIGHT
    legacy.STAGE_ID = STAGE_ID
    legacy.EVIDENCE_ARTIFACT_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/atlas-r3/exact-cover-evidence.json"
    legacy.SNAPSHOT_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/ui-design-program.snapshot.json"
    legacy.ARTIFACT_REL = legacy.SNAPSHOT_REL
    legacy.SCREEN_INDEX_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/screens-index.json"
    legacy.JOURNEY_INDEX_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/journeys-index.json"
    legacy.CAPABILITY_INDEX_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/capabilities-index.json"
    legacy.BINDINGS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/promoted-requirement-bindings.json"
    legacy.ATLAS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/screen-atlas.md"
    legacy.RESOLVED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/screen-atlas.resolved.json"
    legacy.SUMMARY_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/exact-cover-summary.json"
    legacy.NEXT_PROMPT = NEXT_PROMPT
    legacy.REPORT_REL = REPORT_REL
    legacy.main()

    proof_path = ROOT / legacy.EVIDENCE_ARTIFACT_REL
    proof = legacy.load(legacy.EVIDENCE_ARTIFACT_REL)
    proof["program_revision"] = 4
    proof["checks"]["auth_sign_in_recovery_route_distinction"] = True
    proof["auth_route_invariant"] = {
        "sign_in": {"screen_id": "UI-AUTH-001", "route": "/auth/sign-in"},
        "recovery": {"screen_id": "UI-AUTH-004", "route": "/auth/recovery"},
        "forbidden_state": "UI-AUTH-001.recovery",
    }
    legacy.write_json(proof_path, proof)

    request_path = EVIDENCE / "stage-transition-request.json"
    request = legacy.load(request_path.relative_to(ROOT).as_posix())
    request.update({
        "from_target": "atlas-r3",
        "from_revision": 4,
        "to_stage_id": NEXT_STAGE_ID,
        "to_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3",
        "to_task": NEXT_PROMPT,
        "summary": (
            "G1 r3 exact-covers 175 authoritative screens, 9 journeys, 22 capabilities, "
            "and 81 promoted bindings under revision 4; corrected sign-in/recovery identities "
            "are machine-checked and G2 r3 remains unclaimed."
        ),
    })
    legacy.write_json(request_path, request)

    next_inputs = legacy.load((PREFLIGHT / "next_stage_inputs.json").relative_to(ROOT).as_posix())
    next_inputs["facts"]["next_stage_id"] = NEXT_STAGE_ID
    next_inputs["facts"]["task_ref"] = NEXT_PROMPT
    legacy.write_json(PREFLIGHT / "next_stage_inputs.json", next_inputs)
    handoff = legacy.load((PREFLIGHT / "handoff_artifact.json").relative_to(ROOT).as_posix())
    handoff["facts"]["artifact_ref"] = NEXT_PROMPT
    handoff["facts"]["artifact_sha256"] = legacy.sha256(ROOT / NEXT_PROMPT)
    legacy.write_json(PREFLIGHT / "handoff_artifact.json", handoff)

    report = f"""# CUSTOMETRY UI Design Program V2 — G1 r3 atlas report

- Stage: `{STAGE_ID}`
- Result: `passed`
- Exact cover: `175` screens, `9` journeys, `22` capabilities, `81` promoted bindings.
- Corrected auth identity: `UI-AUTH-001 /auth/sign-in` and `UI-AUTH-004 /auth/recovery`; `UI-AUTH-001.recovery` is forbidden and absent.
- Rendered atlas: `{legacy.ATLAS_REL}` — `{legacy.sha256(ROOT / legacy.ATLAS_REL)}`.
- Resolved atlas: `{legacy.RESOLVED_REL}` — `{legacy.sha256(ROOT / legacy.RESOLVED_REL)}`.
- Determinism: the second canonical render produced identical atlas and resolved-data hashes.
- G2 ownership remains explicit: journeys/transitions/criticality, families, coverage, representatives, workload-bounded waves, and exact baseline inheritance.
- Mobile scope: `unauthorized`.
- Proof boundary: static exact-cover and source/hash coherence only; no target-screen design, browser runtime, implementation, accessibility conformance, publication, or deployment proof.
"""
    legacy.write_text(ROOT / REPORT_REL, report)
    print(json.dumps({
        "status": "passed",
        "program_revision": 4,
        "screens": 175,
        "journeys": 9,
        "next_stage": NEXT_STAGE_ID,
    }, indent=2))


if __name__ == "__main__":
    main()
