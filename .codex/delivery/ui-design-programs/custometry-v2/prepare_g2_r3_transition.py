#!/usr/bin/env python3
"""Prepare active-contract G2 r3 proof and transition request."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROGRAM_DIR = Path(__file__).resolve().parent
ROOT = PROGRAM_DIR.parents[3]
sys.path.insert(0, str(PROGRAM_DIR))

import prepare_g2_r2_transition as legacy  # noqa: E402


G2 = PROGRAM_DIR / "artifacts/g2-r3"
EVIDENCE = PROGRAM_DIR / "evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
PREFLIGHT = EVIDENCE / "preflight"
STAGE_ID = "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
SNAPSHOT_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r3/ui-design-program.snapshot.json"
SUMMARY_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3/structure-exact-cover-evidence.json"
ATLAS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r3/screen-atlas.md"
RESOLVED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r3/screen-atlas.resolved.json"
PROMOTED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r3/promoted-structure-bindings.json"
G3_PROOF_SEED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r3/g3-rendered-proof-input-seed.json"
NEXT_PROMPT = ".codex/agents/generated/custometry-ui-design-g0-v2/32-g3-foundations-shell-r3.md"
NEXT_STAGE = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
REPORT_REL = ".codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3-report.md"


def main() -> None:
    legacy.G2 = G2
    legacy.EVIDENCE = EVIDENCE
    legacy.PREFLIGHT = PREFLIGHT
    legacy.STAGE_ID = STAGE_ID
    legacy.SNAPSHOT_REL = SNAPSHOT_REL
    legacy.SUMMARY_REL = SUMMARY_REL
    legacy.ATLAS_REL = ATLAS_REL
    legacy.RESOLVED_REL = RESOLVED_REL
    legacy.PROMOTED_REL = PROMOTED_REL
    legacy.G3_PROOF_SEED_REL = G3_PROOF_SEED_REL
    legacy.NEXT_PROMPT = NEXT_PROMPT
    legacy.REPORT_REL = REPORT_REL
    legacy.main()

    next_inputs = legacy.load((PREFLIGHT / "next_stage_inputs.json").relative_to(ROOT).as_posix())
    next_inputs["facts"].update({"next_stage_id": NEXT_STAGE, "task_ref": NEXT_PROMPT})
    legacy.write_json(PREFLIGHT / "next_stage_inputs.json", next_inputs)
    handoff = legacy.load((PREFLIGHT / "handoff_artifact.json").relative_to(ROOT).as_posix())
    handoff["facts"].update({"artifact_ref": NEXT_PROMPT, "artifact_sha256": legacy.sha256(ROOT / NEXT_PROMPT)})
    legacy.write_json(PREFLIGHT / "handoff_artifact.json", handoff)
    request_path = EVIDENCE / "stage-transition-request.json"
    request = legacy.load(request_path.relative_to(ROOT).as_posix())
    request.update({
        "from_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3",
        "from_revision": 4,
        "to_stage_id": NEXT_STAGE,
        "to_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3",
        "to_task": NEXT_PROMPT,
        "summary": (
            "G2 r3 exact-covers 26 families and four waves under the accepted pilot standard; "
            "one auth family binds UI-AUTH-001 and UI-AUTH-004 as distinct representatives, "
            "and G3 r3 remains unclaimed."
        ),
    })
    legacy.write_json(request_path, request)
    summary = legacy.load(SUMMARY_REL)
    counts = summary["counts"]
    report = f"""# CUSTOMETRY UI Design Program V2 — G2 r3 structure report

- Stage: `{STAGE_ID}`
- Result: `passed`
- Exact cover: `{counts['screens_in_scope']}` visual screens, `{counts['screens_internal_or_non_visual']}` internal/non-visual entries, and `{counts['screens_historical_exclusions']}` historical exclusions.
- Structure: `{counts['families']}` families, `{counts['representatives']}` representatives, `{counts['coverage_profiles']}` coverage profiles, and `{counts['waves']}` bounded waves.
- Auth family: one family exact-covers `UI-AUTH-001 /auth/sign-in` and `UI-AUTH-004 /auth/recovery` as two distinct representatives; shared grammar does not imply identical composition.
- Standard binding: every family binds the accepted revision-4 baseline, standard revision, clause-inventory hash, deterministic applicability policy, and exact exception reference where applicable.
- Determinism: both canonical atlas renders produced identical hashes; zero unresolved screen fields remain.
- Mobile scope: `unauthorized`.
- Proof boundary: static structure, exact-cover, lineage and deterministic artifact proof only; no G3 browser or finished-visual acceptance claim.
"""
    legacy.write_text(ROOT / REPORT_REL, report)
    print(json.dumps({"status": "passed", "families": counts["families"], "waves": counts["waves"], "next_stage": NEXT_STAGE}, indent=2))


if __name__ == "__main__":
    main()
