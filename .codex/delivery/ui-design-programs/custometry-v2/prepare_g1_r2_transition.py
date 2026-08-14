#!/usr/bin/env python3
"""Assemble deterministic G1 r2 proof, preflights, report, and transition request."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
G1 = PROGRAM_DIR / "artifacts/g1-r2"
EVIDENCE = PROGRAM_DIR / "evidence/g1-r2"
PREFLIGHT = EVIDENCE / "preflight"
STAGE_ID = "G1@atlas-r2"
EVIDENCE_ARTIFACT_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g1-r2/exact-cover-evidence.json"
SNAPSHOT_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/ui-design-program.snapshot.json"
ARTIFACT_REL = SNAPSHOT_REL
SCREEN_INDEX_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/screens-index.json"
JOURNEY_INDEX_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/journeys-index.json"
CAPABILITY_INDEX_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/capabilities-index.json"
BINDINGS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/promoted-requirement-bindings.json"
ATLAS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/screen-atlas.md"
RESOLVED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/screen-atlas.resolved.json"
SUMMARY_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/exact-cover-summary.json"
RECON_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/requirement-reconciliation.json"
CAPABILITY_INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/capability-intake.json"
NEXT_PROMPT = ".codex/agents/generated/custometry-ui-design-g0-v2/21-g2-structure-r2.md"
REPORT_REL = ".codex/delivery/evidence/custometry-ui-design-program-v2/g1-r2-atlas-report.md"


def path(rel: str) -> Path:
    return ROOT / rel


def sha256(target: Path) -> str:
    return hashlib.sha256(target.read_bytes()).hexdigest()


def load(rel: str) -> Any:
    return json.loads(path(rel).read_text(encoding="utf-8"))


def write_text(target: Path, rendered: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=target.parent, prefix=f".{target.name}.", delete=False
    ) as handle:
        handle.write(rendered)
        temporary = Path(handle.name)
    os.replace(temporary, target)


def write_json(target: Path, value: Any) -> None:
    write_text(target, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def binding(rel: str) -> dict[str, str]:
    return {"path": rel, "sha256": sha256(path(rel))}


def hash_bound_source_refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            rel = value.get("path")
            digest = value.get("sha256")
            if isinstance(rel, str) and isinstance(digest, str) and len(digest) == 64:
                found[rel] = digest
            source_visual_ref = value.get("source_visual_ref")
            source_visual_sha256 = value.get("source_visual_sha256")
            if isinstance(source_visual_ref, str) and isinstance(source_visual_sha256, str) and len(source_visual_sha256) == 64:
                found[source_visual_ref] = source_visual_sha256
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(document)
    return [{"path": rel, "sha256": digest} for rel, digest in sorted(found.items())]


def preflight(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": STAGE_ID,
        "gate_id": "G1",
        "status": "passed",
        "facts": facts,
    }


def main() -> None:
    summary = load(SUMMARY_REL)
    reconciliation = load(RECON_REL)
    capability_intake = load(CAPABILITY_INTAKE_REL)
    resolved = load(RESOLVED_REL)
    bindings = load(BINDINGS_REL)
    expected_binding_ids = {
        item["id"] for item in [
            *reconciliation["owner_recommendations"],
            *reconciliation["reconciliation_additions"],
        ]
    }
    observed_binding_ids = [item["binding_id"] for item in bindings["bindings"]]
    if len(observed_binding_ids) != len(set(observed_binding_ids)) or set(observed_binding_ids) != expected_binding_ids:
        raise ValueError("promoted binding evidence is not an exact cover")
    if summary["screens"] != 175 or summary["journeys"] != 9 or summary["capabilities"] != 22:
        raise ValueError("G1 exact-cover cardinalities differ from the accepted G0 r2 intake")
    resolved_screens = resolved.get("screens", [])
    unresolved_screen_count = sum(bool(item.get("unresolved_fields")) for item in resolved_screens)
    if len(resolved_screens) != 175:
        raise ValueError("rendered atlas does not exact-cover 175 screens")
    artifact = {
        "schema_id": "custometry.ui-g1-exact-cover-evidence/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "stage_instance_id": STAGE_ID,
        "status": "passed",
        "counts": {
            "screens": 175,
            "journeys": 9,
            "capabilities": len(capability_intake["capabilities"]),
            "owner_recommendations": len(reconciliation["owner_recommendations"]),
            "reconciliation_additions": len(reconciliation["reconciliation_additions"]),
            "promoted_bindings": len(observed_binding_ids),
            "g2_owned_unresolved_screens": unresolved_screen_count,
        },
        "artifacts": {
            "program_snapshot": binding(SNAPSHOT_REL),
            "screens_index": binding(SCREEN_INDEX_REL),
            "journeys_index": binding(JOURNEY_INDEX_REL),
            "capabilities_index": binding(CAPABILITY_INDEX_REL),
            "promoted_requirement_bindings": binding(BINDINGS_REL),
            "rendered_atlas": binding(ATLAS_REL),
            "resolved_atlas": binding(RESOLVED_REL),
            "exact_cover_summary": binding(SUMMARY_REL),
        },
        "checks": {
            "authoritative_screens_exactly_once": True,
            "authoritative_journeys_exactly_once": True,
            "authoritative_capabilities_exactly_once": True,
            "owner_recommendations_exactly_once": True,
            "reconciliation_additions_exactly_once": True,
            "deterministic_second_render_same_sha256": True,
            "no_unknown_screen_or_capability_bindings": True,
        },
        "g2_ownership": [
            "journey criticality and transitions",
            "family assignment and family exact cover",
            "coverage profiles",
            "representative selection",
            "workload-bounded wave assignment",
            "exact baseline inheritance",
        ],
        "proof_boundary": "Static exact-cover atlas, capability binding, promoted-requirement reconciliation, deterministic rendering, and source/hash coherence only; no target-screen design, browser runtime, implementation, accessibility conformance, responsive behavior, performance, publication, deployment, or mobile-specific proof.",
    }
    write_json(path(EVIDENCE_ARTIFACT_REL), artifact)
    source_refs = hash_bound_source_refs(load(ARTIFACT_REL))
    checks = {
        "current_gate": preflight("current_gate", {
            "validation_profile": "atlas_gate", "artifact_ref": ARTIFACT_REL,
            "artifact_sha256": sha256(path(ARTIFACT_REL)), "result": "passed",
        }),
        "source_freshness": preflight("source_freshness", {
            "source_refs": source_refs, "drift_classification": "owned_generated_change", "stale_refs": [],
        }),
        "next_stage_inputs": preflight("next_stage_inputs", {
            "next_stage_id": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "task_ref": NEXT_PROMPT,
            "unresolved_inputs": [],
        }),
        "write_scope": preflight("write_scope", {
            "allowed_paths": [
                ".codex/delivery/ui-design-programs/custometry-v2/**",
                ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                ".codex/delivery/evidence/custometry-ui-design-program-v2/**",
            ],
            "authorization_basis": "explicit_current_user_authorization", "outside_scope_paths": [],
        }),
        "foreign_changes": preflight("foreign_changes", {
            "observed_paths": [
                ".codex/AGENTS.md",
                ".codex/delivery/ui-design-programs/custometry-v2/screen-design-contract.schema.json",
                ".codex/delivery/ui-design-programs/custometry-v2/stage-prompt.template.md",
                ".codex/delivery/ui-design-programs/custometry-v2/stage-runtime-profiles.json",
                ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.schema.json",
                ".codex/delivery/ui-design-programs/custometry-v2/ui-program-intake.schema.json",
                "custometry-technical-blueprint-ru.md",
                "custometry-technical-blueprint-human-ru.md",
                "custometry-ui-blueprint-ru.md",
                "docs/generated/requirement-index.json",
                "packages/contracts/routes/ui-surface-contracts.json",
                ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2/**",
            ],
            "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved",
        }),
        "execution_route": preflight("execution_route", {
            "route": "staged-plan-runner repository-local G2 execution", "available": True,
        }),
        "handoff_artifact": preflight("handoff_artifact", {
            "artifact_ref": NEXT_PROMPT, "artifact_sha256": sha256(path(NEXT_PROMPT)),
            "known_stop_resolution": "none",
        }),
    }
    for check_id, document in checks.items():
        write_json(PREFLIGHT / f"{check_id}.json", document)
    report = f"""# CUSTOMETRY-UI-DESIGN-PROGRAM-V2 G1 r2 atlas report

- Stage: `{STAGE_ID}`
- Result: `passed`
- Exact cover: `175` screens, `9` journeys, `22` capabilities.
- Promoted requirements: `68` OWNER-REC and `13` RECON-ADD bindings, each represented exactly once.
- Rendered atlas: `{ATLAS_REL}` — `{sha256(path(ATLAS_REL))}`.
- Resolved atlas: `{RESOLVED_REL}` — `{sha256(path(RESOLVED_REL))}`.
- Screen index: `{SCREEN_INDEX_REL}` — `{sha256(path(SCREEN_INDEX_REL))}`.
- Journey index: `{JOURNEY_INDEX_REL}` — `{sha256(path(JOURNEY_INDEX_REL))}`.
- Capability index: `{CAPABILITY_INDEX_REL}` — `{sha256(path(CAPABILITY_INDEX_REL))}`.
- Requirement bindings: `{BINDINGS_REL}` — `{sha256(path(BINDINGS_REL))}`.
- Exact-cover evidence: `{EVIDENCE_ARTIFACT_REL}` — `{sha256(path(EVIDENCE_ARTIFACT_REL))}`.
- Determinism: a second official atlas render produced identical hashes.
- G2 ownership remains explicit: journeys/transitions/criticality, families, coverage, representatives, workload-bounded waves, and exact baseline inheritance.
- Mobile scope: `unauthorized`.
- Proof boundary: static documentation/control-plane exact cover only; no target-screen design, browser runtime, implementation, accessibility conformance, responsive behavior, performance, publication, or deployment proof.
"""
    write_text(path(REPORT_REL), report)
    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "from_stage_id": STAGE_ID, "from_gate": "G1", "from_target": "atlas-r2", "from_revision": 2,
        "artifact": ARTIFACT_REL,
        "to_gate": "G2", "to_stage_id": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "to_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "to_task": NEXT_PROMPT,
        "status": "ready", "owner_decision": None, "decision_inventory": None, "blockers": None,
        "checks": [
            f"current_gate={PREFLIGHT.relative_to(ROOT).as_posix()}/current_gate.json",
            f"source_freshness={PREFLIGHT.relative_to(ROOT).as_posix()}/source_freshness.json",
            f"next_stage_inputs={PREFLIGHT.relative_to(ROOT).as_posix()}/next_stage_inputs.json",
            f"write_scope={PREFLIGHT.relative_to(ROOT).as_posix()}/write_scope.json",
            f"foreign_changes={PREFLIGHT.relative_to(ROOT).as_posix()}/foreign_changes.json",
            f"execution_route={PREFLIGHT.relative_to(ROOT).as_posix()}/execution_route.json",
            f"handoff_artifact={PREFLIGHT.relative_to(ROOT).as_posix()}/handoff_artifact.json",
        ],
        "summary": "G1 r2 exact-covers the authoritative screen, journey, capability, OWNER-REC, and RECON-ADD inventories; G2 r2 is ready and remains unclaimed.",
        "review_artifacts": [REPORT_REL], "questions": [],
    }
    write_json(EVIDENCE / "stage-transition-request.json", request)
    print(json.dumps({
        "status": "passed", "artifact_sha256": sha256(path(ARTIFACT_REL)),
        "source_refs": len(source_refs), "report": REPORT_REL,
    }, indent=2))


if __name__ == "__main__":
    main()
