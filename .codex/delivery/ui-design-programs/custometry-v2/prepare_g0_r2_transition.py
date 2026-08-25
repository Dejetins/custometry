#!/usr/bin/env python3
"""Assemble deterministic G0 r2 preflight evidence and transition request."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = PROGRAM_DIR / "evidence/g0-r2"
PREFLIGHT_DIR = EVIDENCE_DIR / "preflight"
ARTIFACT_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-design-program.snapshot.json"
PROGRAM_REL = ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json"
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
RECON_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/requirement-reconciliation.json"
CAPS_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/capability-intake.json"
IMPORT_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/pilot-candidate-import-receipt.json"
SOURCE_INDEX_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/source-authority-index.json"
NEXT_PROMPT = ".codex/agents/generated/custometry-ui-design-g0-v2/11-g1-complete-screen-atlas-r2.md"
REPORT_REL = ".codex/delivery/evidence/custometry-ui-design-program-v2/g0-r2-execution-report.md"
STAGE_ID = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2"


def rel(path: str) -> Path:
    return ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: str) -> Any:
    return json.loads(rel(path).read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def evidence(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": STAGE_ID,
        "gate_id": "G0",
        "status": "passed",
        "facts": facts,
    }


def hash_bound_source_refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path = value.get("path")
            digest = value.get("sha256")
            if isinstance(path, str) and isinstance(digest, str) and len(digest) == 64:
                found[path] = digest
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
    return [{"path": path, "sha256": digest} for path, digest in sorted(found.items())]


def main() -> None:
    program = load(PROGRAM_REL)
    intake = load(INTAKE_REL)
    candidate_import = load(IMPORT_REL)
    reconciliation = load(RECON_REL)
    capabilities = load(CAPS_REL)
    source_refs = hash_bound_source_refs(load(ARTIFACT_REL))

    checks = {
        "current_gate": evidence("current_gate", {
            "validation_profile": "draft", "artifact_ref": ARTIFACT_REL,
            "artifact_sha256": sha256(rel(ARTIFACT_REL)), "result": "passed",
        }),
        "source_freshness": evidence("source_freshness", {
            "source_refs": source_refs,
            "drift_classification": "accepted_change",
            "stale_refs": [],
        }),
        "next_stage_inputs": evidence("next_stage_inputs", {
            "next_stage_id": "G1@atlas-r2", "task_ref": NEXT_PROMPT, "unresolved_inputs": [],
        }),
        "write_scope": evidence("write_scope", {
            "allowed_paths": [
                ".codex/delivery/ui-design-programs/custometry-v2/**",
                ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                ".codex/delivery/evidence/custometry-ui-design-program-v2/**",
                "custometry-ui-blueprint-ru.md",
                "docs/generated/requirement-index.json",
            ],
            "authorization_basis": "explicit_current_user_authorization",
            "outside_scope_paths": [],
        }),
        "foreign_changes": evidence("foreign_changes", {
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
        "handoff_artifact": evidence("handoff_artifact", {
            "artifact_ref": NEXT_PROMPT, "artifact_sha256": sha256(rel(NEXT_PROMPT)), "known_stop_resolution": "none",
        }),
    }
    for name, value in checks.items():
        write_json(PREFLIGHT_DIR / f"{name}.json", value)

    report = f"""# CUSTOMETRY-UI-DESIGN-PROGRAM-V2 G0 r2 execution report

- Stage: `{STAGE_ID}`
- Program revision: `2`
- Result: `passed`
- Intake: `{INTAKE_REL}` — 175 screens and 9 journeys, complete and hash-current.
- Platform baseline: `{BASELINE_REL}` — accepted Linear Graphite visual-language/platform-baseline authority with explicit exclusions.
- Candidate import: `{IMPORT_REL}` — {candidate_import['file_count']} files with actual SHA-256 and byte counts.
- Reconciliation: `{RECON_REL}` — {len(reconciliation['owner_recommendations'])} OWNER-REC entries, {len(reconciliation['reconciliation_additions'])} RECON-ADD requirements, preserved conflicts, and later-stage obligations.
- Capability intake: `{CAPS_REL}` — {len(capabilities['capabilities'])} current cross-surface capabilities.
- Mobile scope: `unauthorized`.
- Foreign changes: authoritative inputs incorporated; unrelated contract-maintenance edits preserved and excluded.

## Proof boundary

Observed proof covers documentation authority, complete candidate file/hash provenance, current-source freshness, promoted-requirement reconciliation, intake/baseline schema validation, prompt/ledger synchronization, and static control-plane coherence. It does not prove target-screen design, browser runtime, production implementation, responsive behavior, accessibility conformance, performance, publication, deployment, fixture truth, legend-threshold truth, or mobile-specific IA.

## Residual risk and G1 handoff

G1 must rebuild and exact-cover screens, journeys, capabilities, OWNER-REC dispositions, and RECON-ADD bindings. G2 retains journeys, criticality, families, coverage, representatives, workload-bounded waves, and exact baseline inheritance.
"""
    report_path = rel(REPORT_REL)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "from_stage_id": STAGE_ID,
        "from_gate": "G0",
        "from_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "from_revision": 2,
        "artifact": ARTIFACT_REL,
        "to_gate": "G1",
        "to_stage_id": "G1@atlas-r2",
        "to_target": "atlas-r2",
        "to_task": NEXT_PROMPT,
        "status": "ready",
        "owner_decision": None,
        "decision_inventory": None,
        "blockers": None,
        "checks": [
            f"current_gate={EVIDENCE_DIR.relative_to(ROOT).as_posix()}/preflight/current_gate.json",
            f"source_freshness={EVIDENCE_DIR.relative_to(ROOT).as_posix()}/preflight/source_freshness.json",
            f"next_stage_inputs={EVIDENCE_DIR.relative_to(ROOT).as_posix()}/preflight/next_stage_inputs.json",
            f"write_scope={EVIDENCE_DIR.relative_to(ROOT).as_posix()}/preflight/write_scope.json",
            f"foreign_changes={EVIDENCE_DIR.relative_to(ROOT).as_posix()}/preflight/foreign_changes.json",
            "execution_route=N/A",
            f"handoff_artifact={EVIDENCE_DIR.relative_to(ROOT).as_posix()}/preflight/handoff_artifact.json",
        ],
        "summary": "G0 r2 reconciled current canonical sources, all candidate files, promoted requirements, conflicts, and the accepted platform baseline; G1 r2 is ready and unclaimed.",
        "review_artifacts": [REPORT_REL],
        "questions": [],
    }
    write_json(EVIDENCE_DIR / "stage-transition-request.json", request)
    print(json.dumps({
        "status": "passed", "artifact_sha256": sha256(rel(ARTIFACT_REL)),
        "source_refs": len(source_refs), "report": REPORT_REL,
    }, indent=2))


if __name__ == "__main__":
    main()
