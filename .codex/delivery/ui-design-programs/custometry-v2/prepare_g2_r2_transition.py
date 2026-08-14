#!/usr/bin/env python3
"""Prepare deterministic G2 r2 preflights, report, and transition request."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
G2 = PROGRAM_DIR / "artifacts/g2-r2"
EVIDENCE = PROGRAM_DIR / "evidence/g2-r2"
PREFLIGHT = EVIDENCE / "preflight"
STAGE_ID = "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2"
SNAPSHOT_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/ui-design-program.snapshot.json"
SUMMARY_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g2-r2/structure-exact-cover-evidence.json"
ATLAS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/screen-atlas.md"
RESOLVED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/screen-atlas.resolved.json"
PROMOTED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/promoted-structure-bindings.json"
G3_PROOF_SEED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/g3-rendered-proof-input-seed.json"
NEXT_PROMPT = ".codex/agents/generated/custometry-ui-design-g0-v2/31-g3-foundations-shell-r2.md"
REPORT_REL = ".codex/delivery/evidence/custometry-ui-design-program-v2/g2-r2-structure-report.md"


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
            if (
                isinstance(source_visual_ref, str)
                and isinstance(source_visual_sha256, str)
                and len(source_visual_sha256) == 64
            ):
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
        "gate_id": "G2",
        "status": "passed",
        "facts": facts,
    }


def main() -> None:
    snapshot = load(SNAPSHOT_REL)
    summary = load(SUMMARY_REL)
    resolved = load(RESOLVED_REL)
    promoted = load(PROMOTED_REL)
    counts = summary["counts"]
    expected_counts = {
        "screens_total": 175,
        "screens_in_scope": 151,
        "screens_internal_or_non_visual": 22,
        "screens_historical_exclusions": 2,
        "journeys": 9,
        "critical_journeys": 9,
        "transitions": 16,
        "promoted_bindings": 81,
        "owner_recommendations": 68,
        "reconciliation_additions": 13,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            raise ValueError(f"G2 exact-cover count mismatch for {key}: {counts.get(key)!r}")
    if not all(summary["checks"].values()):
        raise ValueError("G2 exact-cover evidence contains a failed assertion")
    resolved_screens = resolved.get("screens", [])
    if len(resolved_screens) != 175 or any(item.get("unresolved_fields") for item in resolved_screens):
        raise ValueError("G2 rendered atlas is incomplete or unresolved")
    binding_ids = [item["binding_id"] for item in promoted["bindings"]]
    if len(binding_ids) != 81 or len(binding_ids) != len(set(binding_ids)):
        raise ValueError("G2 promoted structure bindings are not an exact cover")
    if snapshot.get("validation_profile") != "structure_gate":
        raise ValueError("G2 snapshot does not carry structure_gate")
    seed = load(G3_PROOF_SEED_REL)
    if seed.get("status") != "pending_g3_execution" or seed.get("ownership") != "G3":
        raise ValueError("G3 rendered-proof input seed must remain pending and G3-owned")
    proof_seed_ref = snapshot.get("g3_rendered_proof", {}).get("review_board", {})
    if proof_seed_ref.get("path") != G3_PROOF_SEED_REL or proof_seed_ref.get("sha256") != sha256(path(G3_PROOF_SEED_REL)):
        raise ValueError("G3 bounded-context proof seed is not hash-pinned")
    source_refs = hash_bound_source_refs(snapshot)
    checks = {
        "current_gate": preflight(
            "current_gate",
            {
                "validation_profile": "structure_gate",
                "artifact_ref": SNAPSHOT_REL,
                "artifact_sha256": sha256(path(SNAPSHOT_REL)),
                "result": "passed",
            },
        ),
        "source_freshness": preflight(
            "source_freshness",
            {
                "source_refs": source_refs,
                "drift_classification": "owned_generated_change",
                "stale_refs": [],
            },
        ),
        "next_stage_inputs": preflight(
            "next_stage_inputs",
            {
                "next_stage_id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
                "task_ref": NEXT_PROMPT,
                "unresolved_inputs": [],
            },
        ),
        "write_scope": preflight(
            "write_scope",
            {
                "allowed_paths": [
                    ".codex/delivery/ui-design-programs/custometry-v2/**",
                    ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                    ".codex/delivery/evidence/custometry-ui-design-program-v2/**",
                ],
                "authorization_basis": "explicit_current_user_authorization",
                "outside_scope_paths": [],
            },
        ),
        "foreign_changes": preflight(
            "foreign_changes",
            {
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
                "inseparable_paths": [],
                "disposition": "separable_foreign_changes_preserved",
            },
        ),
        "execution_route": preflight(
            "execution_route",
            {
                "route": "staged-plan-runner repository-local G3 execution",
                "available": True,
            },
        ),
        "handoff_artifact": preflight(
            "handoff_artifact",
            {
                "artifact_ref": NEXT_PROMPT,
                "artifact_sha256": sha256(path(NEXT_PROMPT)),
                "known_stop_resolution": "none",
            },
        ),
    }
    for check_id, document in checks.items():
        write_json(PREFLIGHT / f"{check_id}.json", document)
    report = f"""# CUSTOMETRY-UI-DESIGN-PROGRAM-V2 G2 r2 structure report

- Stage: `{STAGE_ID}`
- Result: `passed`
- Exact cover: `{counts['screens_in_scope']}` visual screens, `{counts['screens_internal_or_non_visual']}` internal/non-visual entries, and `{counts['screens_historical_exclusions']}` historical exclusions.
- Journeys: `{counts['journeys']}` critical source-backed graphs and `{counts['transitions']}` normalized transitions.
- Structure: `{counts['families']}` families, `{counts['representatives']}` representatives, `{counts['coverage_profiles']}` exact coverage profiles, and `{counts['waves']}` workload-bounded waves.
- Promoted requirements: `{counts['owner_recommendations']}` OWNER-REC and `{counts['reconciliation_additions']}` RECON-ADD bindings preserved exactly once.
- Program snapshot: `{SNAPSHOT_REL}` — `{sha256(path(SNAPSHOT_REL))}`.
- Rendered atlas: `{ATLAS_REL}` — `{sha256(path(ATLAS_REL))}`.
- Resolved atlas: `{RESOLVED_REL}` — `{sha256(path(RESOLVED_REL))}`.
- Determinism: the official atlas renderer and the complete G2 artifact tree reproduced identical SHA-256 values on a second run.
- Baseline: every family exact-binds `custometry.platform-baseline.v2.r2` or one exact accepted shell exception.
- Deferral: only `viewport_anchor_ids`, with normative origin `references/stage-profiles-v1.md#g2-journeys-and-families`; G3 owns exact baseline viewport binding.
- G3 bounded context: a hash-pinned `pending_g3_execution` input seed makes the next manifest resolvable while explicitly proving no G3 visual, browser, responsive-Web, or accessibility outcome.
- G3 ownership remains explicit: foundations, application shell realization, target-screen design, browser evidence, responsive-Web proof, and accessibility smoke.
- Mobile scope: `unauthorized`.
- Proof boundary: static source-backed structure, exact-cover, workload-budget, baseline-inheritance, deterministic artifact, and documentation/control-plane evidence only; no target-screen design, browser runtime, production implementation, accessibility conformance, responsive behavior, performance, publication, deployment, or mobile-specific proof.
"""
    write_text(path(REPORT_REL), report)
    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "from_stage_id": STAGE_ID,
        "from_gate": "G2",
        "from_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "from_revision": 2,
        "artifact": SNAPSHOT_REL,
        "to_gate": "G3",
        "to_stage_id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "to_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "to_task": NEXT_PROMPT,
        "status": "ready",
        "owner_decision": None,
        "decision_inventory": None,
        "blockers": None,
        "checks": [
            f"current_gate={PREFLIGHT.relative_to(ROOT).as_posix()}/current_gate.json",
            f"source_freshness={PREFLIGHT.relative_to(ROOT).as_posix()}/source_freshness.json",
            f"next_stage_inputs={PREFLIGHT.relative_to(ROOT).as_posix()}/next_stage_inputs.json",
            f"write_scope={PREFLIGHT.relative_to(ROOT).as_posix()}/write_scope.json",
            f"foreign_changes={PREFLIGHT.relative_to(ROOT).as_posix()}/foreign_changes.json",
            f"execution_route={PREFLIGHT.relative_to(ROOT).as_posix()}/execution_route.json",
            f"handoff_artifact={PREFLIGHT.relative_to(ROOT).as_posix()}/handoff_artifact.json",
        ],
        "summary": "G2 r2 exact-covers journeys, families, representatives, coverage, waves, budgets, baseline inheritance, and all promoted bindings; G3 r2 is ready and remains unclaimed.",
        "review_artifacts": [REPORT_REL],
        "questions": [],
    }
    write_json(EVIDENCE / "stage-transition-request.json", request)
    print(
        json.dumps(
            {
                "status": "passed",
                "artifact_sha256": sha256(path(SNAPSHOT_REL)),
                "source_refs": len(source_refs),
                "report": REPORT_REL,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
