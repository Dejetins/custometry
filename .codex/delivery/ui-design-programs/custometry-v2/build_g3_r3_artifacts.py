#!/usr/bin/env python3
"""Build the active-contract G3 foundations/shell candidate without touching r2."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
ART = PROGRAM_DIR / "artifacts/g3-r3"
EVID = PROGRAM_DIR / "evidence/g3-r3"
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
INTAKE = PROGRAM_DIR / "artifacts/g0-r4/ui-program-intake.json"
BASELINE = PROGRAM_DIR / "artifacts/g0-r4/platform-ui-baseline.json"
SOURCE = PROGRAM_DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
CONTRACT = ART / "representative-shell-contract.json"
APPLICABILITY = ART / "representative-shell-standard-applicability.json"
CANDIDATE = ART / "candidate-shell.html"
FIXTURE = ART / "fixture.json"

PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
SCREEN_ID = "UI-ADMIN-003"
SCREEN_INDEX = 94
SCREEN_REVISION_ID = "UI-ADMIN-003.populated.IA.ru.graphite.g3-r3"
ANCHORS = (
    ("web-768", 768, 1024),
    ("web-1024", 1024, 768),
    ("web-1440", 1440, 900),
    ("web-1920", 1920, 1080),
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_legacy_builder():
    path = PROGRAM_DIR / "build_g3_r2_artifacts.py"
    spec = importlib.util.spec_from_file_location("custometry_g3_r2_builder", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def configure_builder(module) -> None:
    module.PROGRAM = PROGRAM
    module.INTAKE = INTAKE
    module.BASELINE = BASELINE
    module.SOURCE = SOURCE
    module.ART = ART
    module.EVID = EVID
    module.FIXTURE = FIXTURE
    module.CANDIDATE = CANDIDATE
    module.CONTRACT = CONTRACT
    module.INHERITANCE = ART / "inheritance-report.json"
    module.DETAILED_INHERITANCE = EVID / "detailed-visual-inheritance-evidence.json"
    module.BEHAVIOR = ART / "shell-behavior-matrix.json"
    module.PROMOTED = PROGRAM_DIR / "artifacts/g2-r3/promoted-structure-bindings.json"
    module.REVIEW_BOARD = ART / "review-board.html"
    module.REVIEW_MANIFEST = ART / "review-board.manifest.json"
    module.SNAPSHOT = ART / "ui-design-program.snapshot.json"
    module.STRESS = EVID / "responsive-language-accessibility-smoke.json"
    module.SCREEN_ID = SCREEN_ID
    module.SCREEN_INDEX = SCREEN_INDEX
    module.SCREEN_REVISION_ID = SCREEN_REVISION_ID
    module.ANCHORS = ANCHORS
    module.BASELINE_ORIGIN = {
        "kind": "product_contract",
        "ref": f"{rel(BASELINE)}#/responsive_contract",
    }
    module.DELEGATED_ORIGIN = {
        "kind": "delegated_design_decision",
        "ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
        "rationale": "Realize the accepted complete pilot standard for the representative shell without changing target product meaning.",
        "constraints": [
            "custometry.platform-baseline.v2.r4",
            "pilot-candidate-v3-metadata:accepted-visual-language",
            "responsive-web:768-1920",
        ],
    }


def patch_candidate() -> None:
    text = CANDIDATE.read_text(encoding="utf-8")
    text = text.replace(
        "<body>",
        f'<body data-ui-artifact="candidate" data-program-id="{PROGRAM_ID}" '
        f'data-artifact-id="{PROGRAM_ID}" data-revision="4" '
        'data-validation-profile="program_ready">',
        1,
    )
    text = text.replace("G3 foundations and shell r2", "G3 foundations and shell r3")
    text = text.replace('data-revision="2"', 'data-revision="4"', 1)
    CANDIDATE.write_text(text, encoding="utf-8")


def patch_contract() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    contract["contract_profile"] = "codex.ui-screen-design-contract/v1@2.0.0"
    contract["program_revision_ref"] = f"{PROGRAM_ID}@{program['revision']}"
    contract["functional_contract_ref"] = {
        "path": rel(INTAKE), "sha256": sha(INTAKE),
        "json_pointer": f"/screens/{SCREEN_INDEX}", "screen_id": SCREEN_ID,
    }
    contract["baseline_binding"] = {
        "baseline_id": baseline["baseline_id"], "path": rel(BASELINE),
        "sha256": sha(BASELINE), "shell_variant_id": "shell.workspace",
        "exception_id": None,
    }
    standard = baseline["standard_contract"]
    contract["standard_binding"] = {
        "standard_revision_id": standard["standard_revision_id"],
        "clause_inventory_sha256": standard["clause_inventory_sha256"],
        "applicability_manifest": {"path": rel(APPLICABILITY), "sha256": "0" * 64},
    }
    contract["standard_exceptions"] = []
    contract["product_identity"].update({
        "screen_id": SCREEN_ID, "route_id": SCREEN_ID,
        "route": "/w/:workspaceKey/settings/access",
        "state_id": f"{SCREEN_ID}.populated", "role_id": "IA",
        "permission_profile": "workspace.manage", "locale": "ru", "theme": "graphite",
    })
    decision_path = Path(program["visual_authority"]["owner_decision_ref"])
    decision = json.loads((ROOT / decision_path).read_text(encoding="utf-8"))
    decision_value_sha = decision["decision"]["accepted_value_sha256s"][0]
    decision_uri = (
        f"owner-decision://{sha(ROOT / decision_path)}/{decision_path.as_posix()}"
        f"?value_sha256={decision_value_sha}#/decision/accepted_values/0"
    )
    contract["source_visual"] = {
        "kind": "delegated_design_output", "evidence_mode": "visual_language_only",
        "html_path": rel(SOURCE), "image_path": None,
        "html_sha256": sha(SOURCE), "image_sha256": None,
        "owner_decision_ref": None,
        "delegation_ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
    }
    contract["visual_authority"] = {
        key: program["visual_authority"][key] for key in (
            "source_visual_ref", "source_visual_sha256", "owner_decision_ref",
            "screen_acceptance_scope", "visual_language_scope",
            "reusable_foundation_scope", "inheritance_policy", "mobile_scope",
        )
    }
    contract["comparison_claims"] = {
        "required_purpose": "visual_language_conformance",
        "deterministic_render_proves_fidelity": False,
        "reference_logical_artifact_id": f"{PROGRAM_ID}:accepted-pilot:ru:r4",
        "implementation_logical_artifact_id": f"{PROGRAM_ID}:g3-candidate:r3",
    }
    contract["render_environment"].update({
        "fixed_clock_iso": "2026-08-13T14:14:04Z",
        "fixture_data_path": rel(FIXTURE), "fixture_data_sha256": sha(FIXTURE),
        "font_bundle_sha256": canonical_sha(baseline["font_contract"]),
        "asset_bundle_sha256": canonical_sha(baseline["asset_contract"]),
    })
    origin = {"kind": "product_contract", "ref": f"{rel(BASELINE)}#/responsive_contract"}
    contract["viewport_contract"]["supported_web_width_range"] = {
        **baseline["responsive_contract"]["supported_web_width_range"], "origin": origin,
    }
    contract["viewport_contract"]["anchors"] = [
        {"anchor_id": aid, "width": width, "height": height,
         "class": "responsive_web", "state_ref": f"{SCREEN_ID}.populated", "origin": origin}
        for aid, width, height in ANCHORS
    ]
    contract["viewport_contract"]["above_supported_range_origin"] = origin
    accepted_visual_origin = {"kind": "accepted_visual", "ref": rel(SOURCE)}
    for region in contract["regions"]:
        region["source_refs"] = [accepted_visual_origin]
        region["computed_style_properties_origin"] = accepted_visual_origin
    required_component_states = {
        row["component_id"]: row["required_states"] for row in baseline["component_contracts"]
    }
    all_screen_states = [
        f"{SCREEN_ID}.initial", f"{SCREEN_ID}.loading", f"{SCREEN_ID}.populated",
        f"{SCREEN_ID}.error", f"{SCREEN_ID}.permission_denied", f"{SCREEN_ID}.recovery",
    ]
    for element in contract["element_contracts"]:
        element["standard_slot_id"] = None
        element["component_state_ids"] = required_component_states.get(
            element.get("component_id"), ["default"]
        )
        if element.get("action_ids"):
            element["state_ids"] = all_screen_states
    write_json(CONTRACT, contract)


def bind_applicability() -> None:
    from subprocess import run
    script = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/assemble_standard_applicability.py")
    run([
        "python3", str(script), "--screen", str(CONTRACT), "--baseline", str(BASELINE),
        "--project-root", str(ROOT), "--output", str(APPLICABILITY),
    ], check=True)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    contract["standard_binding"]["applicability_manifest"]["sha256"] = sha(APPLICABILITY)
    write_json(CONTRACT, contract)


def bind_program() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    responsive = baseline["responsive_contract"]
    origin = {"kind": "product_contract", "ref": f"{rel(BASELINE)}#/responsive_contract"}
    program["status"] = "review"
    program["validation_profile"] = "program_ready"
    program["responsive_policy"] = {
        "adaptive_web_required": True,
        "supported_web_width_range": {**responsive["supported_web_width_range"], "origin": origin},
        "anchor_viewports": [
            {"anchor_id": a, "width": w, "height": h, "class": "responsive_web", "origin": origin}
            for a, w, h in ANCHORS
        ],
        "breakpoint_policy": "content_driven", "breakpoint_policy_origin": origin,
        "component_adaptation": "prefer_container_queries", "component_adaptation_origin": origin,
        "logical_properties_required": True,
        "logical_properties_origin": {"kind": "normative_requirement", "ref": "custometry-ui-blueprint-ru.md#responsive-web"},
        "mobile_scope": "unauthorized",
        "mobile_scope_origin": {"kind": "normative_requirement", "ref": "references/responsive-policy-v1.md#mobile-authorization-boundary"},
        "mobile_authorization_ref": None, "authorized_mobile_surfaces": [],
        "authorized_mobile_viewports": [], "allowed_mobile_changes": [],
    }
    anchor_ids = [row[0] for row in ANCHORS]
    for coverage in program["coverage_profiles"]:
        coverage["viewport_anchor_ids"] = {
            "mode": "required", "values": anchor_ids, "origin": origin,
            "not_applicable_reason_ref": None,
        }
        coverage["unresolved_fields"] = [x for x in coverage.get("unresolved_fields", []) if x != "viewport_anchor_ids"]
    program["g3_rendered_proof"] = {
        "source_evidence_mode": "renderable_html",
        "shell_capture_contract": {"path": rel(CONTRACT), "sha256": sha(CONTRACT), "screen_revision_id": SCREEN_REVISION_ID},
        "source_native_capture": program["g3_rendered_proof"]["source_native_capture"],
        "source_anchor_observations": [],
        "candidate_artifact": {"path": rel(CANDIDATE), "sha256": sha(CANDIDATE)},
        "candidate_anchor_captures": [],
        "standard_board": program["g3_rendered_proof"]["review_board"],
        "review_board": program["g3_rendered_proof"]["review_board"],
        "inheritance_report": program["g3_rendered_proof"]["inheritance_report"],
    }
    write_json(PROGRAM, program)


def main() -> None:
    module = load_legacy_builder()
    configure_builder(module)
    module.prepare()
    patch_candidate()
    patch_contract()
    bind_applicability()
    bind_program()


if __name__ == "__main__":
    main()
