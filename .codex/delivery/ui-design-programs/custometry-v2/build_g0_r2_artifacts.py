#!/usr/bin/env python3
"""Build the revision-2 G0 reconciliation without mutating revision-1 evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
R1_INTAKE = PROGRAM_DIR / "ui-program-intake.json"
R1_BASELINE = PROGRAM_DIR / "platform-ui-baseline.json"
R1_PROGRAM = PROGRAM_DIR / "artifacts/g0/ui-design-program.snapshot.json"
R2_ARTIFACT_DIR = PROGRAM_DIR / "artifacts/g0-r2"
R2_EVIDENCE_DIR = PROGRAM_DIR / "evidence/g0-r2"
R2_INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json"
R2_BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
R2_OWNER_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/visual-authority-decision-v2.json"
R2_ADMISSION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/g1-admission-inventory.json"
R2_RECONCILIATION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/requirement-reconciliation.json"
R2_CAPABILITY_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/capability-intake.json"
CANDIDATE_DIR_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2"
CANDIDATE_SOURCE_REL = f"{CANDIDATE_DIR_REL}/ru/source.html"
CANDIDATE_MANIFEST_REL = f"{CANDIDATE_DIR_REL}/candidate-manifest.json"
CANDIDATE_IMPORT_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/pilot-candidate-import-receipt.json"
ROUTES_REL = "packages/contracts/routes/ui-route-contracts.json"
SURFACES_REL = "packages/contracts/routes/ui-surface-contracts.json"
TECH_REL = "custometry-technical-blueprint-ru.md"
TECH_MIRROR_REL = "custometry-technical-blueprint-human-ru.md"
UI_REL = "custometry-ui-blueprint-ru.md"
ADR_REL = "docs/adr/0007-responsive-web-frontend-platform.md"
REQUIREMENT_INDEX_REL = "docs/generated/requirement-index.json"

OLD_OWNER = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/owner-intent.json"
OLD_SOURCE = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot/ru/source.html"
OLD_ADMISSION = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/g1-admission-inventory.json"

SCREEN_SCOPE = (
    "Visual-language and platform-baseline authority only; never exact target-screen composition, "
    "product semantics, fixture truth, legend-threshold truth, production implementation, or novel-screen fidelity."
)
VISUAL_SCOPE = (
    "Linear Graphite shell character, calm professional density, compact contextual navigation, bounded analytical "
    "surfaces, concise KPI and command language, visible Result Trust, Focus/Explore character, readable analytical "
    "labels and tables, and adaptive external series-panel behavior as a visual-language reference."
)
FOUNDATION_SCOPE = (
    "Hash-pinned source-backed colors, typography stack, spacing rhythm, compact controls, rounded command language, "
    "shell/navigation relationships, overlay behavior, and analytical presentation primitives only; exact composition, "
    "information architecture, component implementation, runtime semantics, and target-screen acceptance remain later-gate work."
)

PROMOTED_REQUIREMENTS = [
    "METRIC-021", "METRIC-022", "METRIC-023", "METRIC-024",
    "FILTER-011", "FILTER-012",
    "COMPARE-008", "COMPARE-009", "COMPARE-010",
    "SEGMENT-027", "SEGMENT-028",
    "ANALYTICAL-DOC-013", "CHART-020",
]

REQUIREMENT_BINDINGS = {
    "METRIC": {"screen_ids": ["UI-AN-004"], "capability_ids": ["UI-CAP-004"]},
    "FILTER": {"screen_ids": ["UI-OVR-003", "UI-OVR-004"], "capability_ids": ["UI-CAP-002"]},
    "COMPARE": {"screen_ids": ["UI-OVR-005", "UI-AN-004"], "capability_ids": ["UI-CAP-003"]},
    "SEGMENT": {"screen_ids": ["UI-SEG-003", "UI-AN-010"], "capability_ids": ["UI-CAP-019"]},
    "ANALYTICAL-DOC": {"screen_ids": ["UI-RPT-003", "UI-AN-004"], "capability_ids": ["UI-CAP-012"]},
    "CHART": {"screen_ids": ["UI-AN-004", "UI-OVR-007"], "capability_ids": ["UI-CAP-005"]},
}


def rel(path: str) -> Path:
    return ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        handle.write(rendered)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def declared_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    try:
        document = json.loads(text)
    except json.JSONDecodeError:
        document = None
    if isinstance(document, dict) and isinstance(document.get("status"), str):
        return document["status"]
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.strip().startswith("status:"):
                return line.split(":", 1)[1].strip().strip("\"'") or None
    return None


def replace_refs(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [replace_refs(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: replace_refs(item, replacements) for key, item in value.items()}
    return value


def source_contract(path: str, authority: str, covers: list[str]) -> dict[str, Any]:
    return {
        "path": path,
        "sha256": sha256(rel(path)),
        "authority": authority,
        "covers": covers,
    }


def program_source(path: str, authority: str, *, screens: bool = False, journeys: bool = False) -> dict[str, Any]:
    return {
        "path": path,
        "authority": authority,
        "required_status": declared_status(rel(path)),
        "sha256": sha256(rel(path)),
        "screen_collections": ([{"json_pointer": "/screens", "id_key": "screen_id"}] if screens else []),
        "journey_collections": ([{"json_pointer": "/journeys", "id_key": "journey_id"}] if journeys else []),
    }


def build_candidate_import() -> dict[str, Any]:
    candidate_root = rel(CANDIDATE_DIR_REL)
    files = []
    for path in sorted(item for item in candidate_root.rglob("*") if item.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        suffix = path.suffix.lower()
        if suffix == ".html":
            role = "renderable_html_visual_language_source"
        elif suffix == ".png":
            role = "historical_candidate_browser_capture_not_active_gate_proof"
        elif relative.endswith("candidate-manifest.json"):
            role = "candidate_manifest"
        elif suffix in {".js", ".txt"}:
            role = "vendored_candidate_runtime_or_license_not_production_authority"
        else:
            role = "candidate_review_record"
        files.append({"path": relative, "sha256": sha256(path), "byte_count": path.stat().st_size, "role": role})
    return {
        "schema_id": "custometry.ui-pilot-candidate-import/v2",
        "status": "verified",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "revision": 2,
        "candidate_manifest": {"path": CANDIDATE_MANIFEST_REL, "sha256": sha256(rel(CANDIDATE_MANIFEST_REL))},
        "file_count": len(files),
        "files": files,
        "authority": {
            "accepted_for": ["visual_language", "platform_baseline"],
            "excluded": [
                "exact_target_screen_composition", "production_implementation", "product_semantics",
                "fixture_truth", "legend_threshold_truth", "mobile_specific_information_architecture",
                "browser_gate_proof", "deployment",
            ],
        },
    }


def owner_rec_binding(text: str) -> dict[str, Any]:
    lowered = text.lower()
    groups = [
        (("filter", "condition", "and/or"), ["UI-OVR-003", "UI-OVR-004"], ["UI-CAP-002"]),
        (("period", "comparison", "quarter", "year", "yoy"), ["UI-OVR-005", "UI-AN-004"], ["UI-CAP-003"]),
        (("segment", "migration"), ["UI-SEG-003", "UI-AN-010"], ["UI-CAP-019"]),
        (("focus",), ["UI-OVR-020"], ["UI-CAP-007"]),
        (("share", "author", "snapshot", "email"), ["UI-OVR-025", "UI-RPT-003"], ["UI-CAP-012"]),
        (("kpi", "metric"), ["UI-AN-004"], ["UI-CAP-004"]),
        (("chart", "series", "palette", "label", "axis", "echarts"), ["UI-AN-004", "UI-OVR-007"], ["UI-CAP-005"]),
        (("table", "xlsx", "csv", "export"), ["UI-OVR-007", "UI-RPT-003"], ["UI-CAP-006", "UI-CAP-012"]),
        (("sidebar", "navigation", "rail", "shell"), ["UI-SHELL-WORKSPACE"], ["UI-CAP-001"]),
        (("trust", "inspector", "discussion"), ["UI-OVR-006"], ["UI-CAP-008", "UI-CAP-010"]),
    ]
    for terms, screens, capabilities in groups:
        if any(term in lowered for term in terms):
            return {
                "binding_kind": "atlas_and_capability",
                "screen_ids": screens,
                "capability_ids": capabilities,
                "not_applicable_reason": None,
            }
    return {
        "binding_kind": "platform_baseline_only",
        "screen_ids": [],
        "capability_ids": [],
        "not_applicable_reason": (
            "Permitted G1 N/A: this correction constrains the accepted visual-language/platform baseline, "
            "while exact target-screen composition and family realization remain G2-G5 obligations."
        ),
    }


def build_reconciliation(candidate: dict[str, Any]) -> dict[str, Any]:
    machine = rel(TECH_REL).read_text(encoding="utf-8")
    missing = [item for item in PROMOTED_REQUIREMENTS if re.search(rf"\b{re.escape(item)}\b", machine) is None]
    if missing:
        raise ValueError(f"promoted requirements missing from normative blueprint: {missing}")
    owner_recommendations = []
    for index, text in enumerate(candidate["intent"], start=1):
        owner_recommendations.append({
            "id": f"OWNER-REC-{index:03d}",
            "text": text,
            "source_ref": f"{CANDIDATE_MANIFEST_REL}#/intent/{index - 1}",
            "binding": owner_rec_binding(text),
            "authority_limit": "product meaning only where separately promoted into canonical sources; otherwise visual-language/platform-baseline constraint",
        })
    additions = []
    for index, requirement_id in enumerate(PROMOTED_REQUIREMENTS, start=1):
        family = requirement_id.rsplit("-", 1)[0]
        binding = REQUIREMENT_BINDINGS[family]
        additions.append({
            "id": f"RECON-ADD-{index:03d}",
            "requirement_id": requirement_id,
            "source_ref": f"{TECH_REL}#{requirement_id}",
            "screen_ids": binding["screen_ids"],
            "capability_ids": binding["capability_ids"],
            "binding_status": "bound",
        })
    return {
        "schema_id": "custometry.ui-requirement-reconciliation/v2",
        "status": "complete",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "revision": 2,
        "owner_recommendations": owner_recommendations,
        "reconciliation_additions": additions,
        "preserved_conflicts": [
            {"id": "CONFLICT-R2-001", "resolution": "candidate fixed KPI-chart-table order, grid, control placement, and target-screen composition are not authority", "owner": "G2-G5"},
            {"id": "CONFLICT-R2-002", "resolution": "candidate fixtures, sample values, labels, legends, and thresholds are evidence-only and cannot define product truth", "owner": "product contracts and later screen fixtures"},
            {"id": "CONFLICT-R2-003", "resolution": "narrow candidate captures demonstrate adaptive behavior only; mobile-specific IA remains unauthorized", "owner": "responsive Web policy"},
            {"id": "CONFLICT-R2-004", "resolution": "vendored ECharts and candidate HTML are not production implementation or frontend architecture authority", "owner": "implementation handoff"},
            {"id": "CONFLICT-R2-005", "resolution": "UI-CAP-004, UI-CAP-012, and UI-CAP-019 source arrays predate some promoted requirements; r2 evidence binds them without rewriting the foreign source input", "owner": "later canonical contract synchronization"},
        ],
        "later_stage_obligations": [
            {"gate": "G2", "owns": ["journey transitions and criticality", "families", "coverage", "representatives", "workload-bounded waves", "exact baseline inheritance"]},
            {"gate": "G3", "owns": ["platform-baseline realization", "responsive-Web browser evidence", "accessibility smoke", "representative shell contract"]},
            {"gate": "G4-G5", "owns": ["target-screen composition", "family and wave exact-cover acceptance", "functional fixture and legend semantics"]},
            {"gate": "G6", "owns": ["implementation handoff", "cross-program journey proof"]},
        ],
    }


def build_owner_authority() -> dict[str, Any]:
    source_hash = sha256(rel(CANDIDATE_SOURCE_REL))
    return {
        "schema_id": "custometry.ui-program-owner-authority/v2",
        "status": "accepted",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "task_id": "custometry-v2-complete-g0-r2-and-g1-r2",
        "revision": 2,
        "execution_mode": "goal_driven",
        "authorized_stage_sequence": ["G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "G1@atlas-r2"],
        "terminal_target": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2 pending and unclaimed",
        "scope": {
            "platform": "responsive_web",
            "mobile_scope": "unauthorized",
            "publication_authorized": False,
            "owner_acceptance": {"G0": False, "G1": False},
        },
        "source_visual": {"path": CANDIDATE_SOURCE_REL, "sha256": source_hash},
        "visual_authority": {
            "source_visual_ref": CANDIDATE_SOURCE_REL,
            "source_visual_sha256": source_hash,
            "source_evidence_mode": "renderable_html",
            "screen_acceptance_scope": SCREEN_SCOPE,
            "visual_language_scope": VISUAL_SCOPE,
            "reusable_foundation_scope": FOUNDATION_SCOPE,
            "inheritance_policy": "required",
            "mobile_scope": "unauthorized",
        },
        "promoted_requirement_ids": PROMOTED_REQUIREMENTS,
        "decision_policy": "routine technical and reversible choices are agent_decidable; no routine owner input remains for G0 or G1",
    }


def update_baseline(owner: dict[str, Any], candidate_import: dict[str, Any]) -> dict[str, Any]:
    exception_replacements = {}
    for source in sorted((PROGRAM_DIR / "evidence/g0").glob("baseline-exception-*-decision-v1.json")):
        target_name = source.name.replace("-v1.json", "-v2.json")
        target_rel = f".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/{target_name}"
        document = replace_refs(load(source), {OLD_OWNER: R2_OWNER_REL, OLD_SOURCE: CANDIDATE_SOURCE_REL})
        document["revision"] = 2
        document["source"] = {"path": R2_OWNER_REL, "sha256": sha256(rel(R2_OWNER_REL))}
        write_json(rel(target_rel), document)
        exception_replacements[source.relative_to(ROOT).as_posix()] = target_rel

    replacements = {OLD_OWNER: R2_OWNER_REL, OLD_SOURCE: CANDIDATE_SOURCE_REL, **exception_replacements}
    baseline = replace_refs(load(R1_BASELINE), replacements)
    baseline["baseline_id"] = "custometry.platform-baseline.v2.r2"
    baseline["revision"] = 2
    baseline["status"] = "accepted"
    baseline["source_visual"] = {
        "path": CANDIDATE_SOURCE_REL,
        "sha256": sha256(rel(CANDIDATE_SOURCE_REL)),
        "owner_decision_ref": R2_OWNER_REL,
        "native_viewport": {"width": 1920, "height": 1080},
        "state_id": "ready",
        "theme_id": "graphite",
    }
    baseline["scope"] = {
        "screen_acceptance_scope": SCREEN_SCOPE,
        "visual_language_scope": VISUAL_SCOPE,
        "reusable_foundation_scope": FOUNDATION_SCOPE,
        "inheritance_policy": "required",
        "mobile_scope": "unauthorized",
    }
    baseline["supporting_sources"] = [
        {"path": CANDIDATE_MANIFEST_REL, "sha256": sha256(rel(CANDIDATE_MANIFEST_REL)), "authority": "complete candidate manifest; visual-language/platform-baseline input only", "covers": ["product", "tokens", "fonts", "assets", "icons", "responsive", "accessibility", "copy"]},
        {"path": CANDIDATE_IMPORT_REL, "sha256": sha256(rel(CANDIDATE_IMPORT_REL)), "authority": "complete actual file/hash import receipt", "covers": ["assets", "responsive", "copy"]},
        {"path": R2_OWNER_REL, "sha256": sha256(rel(R2_OWNER_REL)), "authority": "current accepted owner scope and authority limits", "covers": ["product", "responsive", "accessibility"]},
        {"path": ADR_REL, "sha256": sha256(rel(ADR_REL)), "authority": "accepted responsive-Web frontend ownership decision", "covers": ["product", "responsive", "accessibility"]},
        {"path": UI_REL, "sha256": sha256(rel(UI_REL)), "authority": "canonical UI requirements and inventory", "covers": ["product", "responsive", "accessibility", "copy"]},
        {"path": ROUTES_REL, "sha256": sha256(rel(ROUTES_REL)), "authority": "current route and navigation contracts", "covers": ["product", "copy"]},
    ]
    for target_rel in exception_replacements.values():
        baseline["supporting_sources"].append({"path": target_rel, "sha256": sha256(rel(target_rel)), "authority": "revision-2 compatibility decision for an exact shell exception", "covers": ["product"]})
    token_updates = {
        "color.surface": "#111214",
        "space.shell": 8,
        "size.control.compact": 32,
        "radius.control": 16,
        "border.default": "1px solid #303136",
        "elevation.overlay": "0 22px 70px rgba(0,0,0,.48)",
        "opacity.disabled": 0.55,
        "motion.shell": "120ms cubic-bezier(.2,0,0,1)",
        "z.overlay": 300,
    }
    for group in baseline["foundation_tokens"].values():
        for token in group:
            token_id = token["token_id"]
            if token_id in token_updates:
                token["value"]["value"] = token_updates[token_id]
    baseline["layout_contract"]["grid"] = "compact icon rail plus overlaying contextual navigation and a fluid rounded analytical workspace"
    baseline["layout_contract"]["content_width"] = "adaptive responsive Web from 768px through 1920px with bounded analytical surfaces and local overflow"
    baseline["layout_contract"]["scroll_policy"] = "preserve stable workspace geometry; contextual navigation overlays rather than resizes the desktop workspace; analytical tables and series panels own overflow"
    baseline["layout_contract"]["layering_rules"] = [
        "contextual navigation flyout overlays the desktop workspace and becomes a viewport-contained modal drawer when required by width",
        "report inspector uses a sibling pane on wide Web and a viewport-contained overlay on narrow Web",
        "high-cardinality series use a right sibling panel or lower panel without redefining chart semantics",
    ]
    baseline["responsive_contract"]["below_supported_range"] = "out_of_scope"
    baseline["icon_contract"]["source_sha256"] = sha256(rel(CANDIDATE_SOURCE_REL))
    baseline["unresolved_inputs"] = []
    return baseline


def write_index(kind: str, values: list[dict[str, Any]], singular: str) -> dict[str, str]:
    entries = []
    for value in values:
        identity = value[f"{singular}_id"]
        target_rel = f".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/{kind}/{identity}.json"
        write_json(rel(target_rel), {singular: value})
        entries.append({"id": identity, "path": target_rel, "sha256": sha256(rel(target_rel)), "json_pointer": f"/{singular}"})
    index_rel = f".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/{kind}-index.json"
    write_json(rel(index_rel), {
        "$schema": "program-artifact-index.schema.json",
        "schema_id": "codex.ui-program-artifact-index/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "index_kind": kind,
        "entries": entries,
    })
    return {"path": index_rel, "sha256": sha256(rel(index_rel))}


def main() -> None:
    candidate_manifest = load(rel(CANDIDATE_MANIFEST_REL))
    owner = build_owner_authority()
    write_json(rel(R2_OWNER_REL), owner)
    candidate_import = build_candidate_import()
    write_json(rel(CANDIDATE_IMPORT_REL), candidate_import)
    reconciliation = build_reconciliation(candidate_manifest)
    write_json(rel(R2_RECONCILIATION_REL), reconciliation)

    r1_admission = load(PROGRAM_DIR / "evidence/g0/g1-admission-inventory.json")
    admission = replace_refs(r1_admission, {OLD_OWNER: R2_OWNER_REL})
    admission["revision"] = 2
    admission["authority_boundary"] = (
        "Exact current route/surface floor plus promoted r2 requirements; pilot-candidate-v2 is visual-language/platform-baseline authority only."
    )
    write_json(rel(R2_ADMISSION_REL), admission)

    surfaces = load(rel(SURFACES_REL))
    capability_intake = {
        "schema_id": "custometry.ui-capability-intake/v2",
        "status": "complete",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "revision": 2,
        "source": {"path": SURFACES_REL, "sha256": sha256(rel(SURFACES_REL)), "json_pointer": "/cross_surface_capabilities"},
        "capabilities": surfaces["cross_surface_capabilities"],
        "promoted_requirement_bindings": reconciliation["reconciliation_additions"],
    }
    write_json(rel(R2_CAPABILITY_REL), capability_intake)

    source_authority = {
        "schema_id": "custometry.ui-source-authority-index/v2",
        "status": "complete",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "revision": 2,
        "sources": [
            {"path": path, "sha256": sha256(rel(path)), "declared_status": declared_status(rel(path))}
            for path in [R2_OWNER_REL, CANDIDATE_MANIFEST_REL, CANDIDATE_SOURCE_REL, CANDIDATE_IMPORT_REL, R2_RECONCILIATION_REL, ROUTES_REL, SURFACES_REL, TECH_REL, TECH_MIRROR_REL, UI_REL, REQUIREMENT_INDEX_REL, ADR_REL]
        ],
    }
    write_json(R2_EVIDENCE_DIR / "source-authority-index.json", source_authority)

    baseline = update_baseline(owner, candidate_import)
    write_json(rel(R2_BASELINE_REL), baseline)

    replacements = {OLD_OWNER: R2_OWNER_REL, OLD_SOURCE: CANDIDATE_SOURCE_REL, OLD_ADMISSION: R2_ADMISSION_REL}
    intake = replace_refs(load(R1_INTAKE), replacements)
    intake["intake_id"] = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2.intake.v2"
    intake["revision"] = 2
    intake["status"] = "complete"
    intake["program_scope"]["source_ref"] = f"{R2_OWNER_REL}#scope"
    intake["accepted_decisions"] = [{"path": R2_OWNER_REL, "sha256": sha256(rel(R2_OWNER_REL))}]
    intake["pilot"] = {
        "source_visual_ref": CANDIDATE_SOURCE_REL,
        "source_visual_sha256": sha256(rel(CANDIDATE_SOURCE_REL)),
        "source_evidence_mode": "renderable_html",
        "owner_decision_ref": R2_OWNER_REL,
        "native_viewport": {"width": 1920, "height": 1080},
        "reviewed_state_ids": ["ready"],
        "reviewed_theme_ids": ["graphite"],
        "represented_screen_ids": ["UI-AN-004"],
        "screen_acceptance_scope": SCREEN_SCOPE,
        "visual_language_scope": VISUAL_SCOPE,
        "reusable_foundation_scope": FOUNDATION_SCOPE,
        "inheritance_policy": "required",
    }
    intake["authoritative_inventory"] = {"path": R2_ADMISSION_REL, "sha256": sha256(rel(R2_ADMISSION_REL)), "screen_collection": {"json_pointer": "/screens", "id_key": "screen_id"}, "journey_collection": {"json_pointer": "/journeys", "id_key": "journey_id"}}
    intake["baseline_contract"] = {"baseline_id": baseline["baseline_id"], "path": R2_BASELINE_REL, "sha256": sha256(rel(R2_BASELINE_REL))}
    intake["themes"] = [{"id": "graphite", "meaning": "accepted Linear Graphite visual-language and analytical-density baseline", "source_refs": [f"{CANDIDATE_SOURCE_REL}#correction-pass-18"]}]
    intake["source_contracts"] = [
        source_contract(R2_OWNER_REL, "accepted current owner scope and r2 reconciliation authority", ["product", "journeys", "screens", "roles", "permissions", "states", "copy", "locales", "themes"]),
        source_contract(ROUTES_REL, "current route, role, permission, guard, state, and navigation contracts", ["routes", "screens", "roles", "permissions", "states", "copy"]),
        source_contract(SURFACES_REL, "current overlay, transient, system-state, and cross-surface capability contracts", ["screens", "states", "copy"]),
        source_contract(TECH_REL, "normative product specification", ["product", "journeys", "roles", "permissions", "states", "data", "copy", "locales"]),
        source_contract(TECH_MIRROR_REL, "required explanatory mirror", ["product", "journeys", "copy"]),
        source_contract(UI_REL, "canonical UI requirements and current inventory", ["screens", "journeys", "states", "copy", "locales", "themes", "assets"]),
        source_contract(R2_ADMISSION_REL, "complete revision-2 G1 admission inventory", ["routes", "screens", "journeys"]),
    ]
    intake["unresolved_inputs"] = []
    write_json(rel(R2_INTAKE_REL), intake)

    indexes = {
        "screens": write_index("screens", intake["screens"], "screen"),
        "journeys": write_index("journeys", intake["journeys"], "journey"),
        "families": write_index("families", [], "family"),
        "waves": write_index("waves", [], "wave"),
    }

    program = replace_refs(load(R1_PROGRAM), replacements)
    program["revision"] = 2
    program["status"] = "draft"
    program["validation_profile"] = "draft"
    program["input_contracts"] = {
        "intake": {"path": R2_INTAKE_REL, "sha256": sha256(rel(R2_INTAKE_REL))},
        "baseline": {"path": R2_BASELINE_REL, "sha256": sha256(rel(R2_BASELINE_REL))},
    }
    program["artifact_indexes"] = indexes
    program["visual_authority"] = {
        "source_visual_ref": CANDIDATE_SOURCE_REL,
        "source_visual_sha256": sha256(rel(CANDIDATE_SOURCE_REL)),
        "source_evidence_mode": "renderable_html",
        "owner_decision_ref": R2_OWNER_REL,
        "screen_acceptance_scope": SCREEN_SCOPE,
        "visual_language_scope": VISUAL_SCOPE,
        "reusable_foundation_scope": FOUNDATION_SCOPE,
        "inheritance_policy": "required",
        "mobile_scope": "unauthorized",
        "product_semantics_scope": "source_registry_only",
    }
    program["scope"]["origin"] = {"kind": "product_contract", "ref": f"{R2_OWNER_REL}#/scope"}
    program["screens"] = []
    program["journeys"] = []
    program["families"] = []
    program["waves"] = []
    program["source_contracts"] = [
        program_source(R2_OWNER_REL, "accepted current owner scope and revision-2 reconciliation authority"),
        program_source(ROUTES_REL, "current route, role, permission, guard, state, and navigation contracts"),
        program_source(SURFACES_REL, "current overlay, transient, system-state, and cross-surface capability contracts"),
        program_source(TECH_REL, "normative product specification"),
        program_source(TECH_MIRROR_REL, "required explanatory mirror"),
        program_source(UI_REL, "canonical UI requirements and current inventory"),
        program_source(R2_ADMISSION_REL, "complete revision-2 G1 admission inventory and exact current-state floor", screens=True, journeys=True),
    ]
    write_json(PROGRAM_DIR / "ui-design-program.json", program)
    write_json(R2_ARTIFACT_DIR / "ui-design-program.snapshot.json", program)
    print(json.dumps({
        "status": "passed",
        "program_revision": 2,
        "screens": len(intake["screens"]),
        "journeys": len(intake["journeys"]),
        "capabilities": len(capability_intake["capabilities"]),
        "owner_recommendations": len(reconciliation["owner_recommendations"]),
        "reconciliation_additions": len(reconciliation["reconciliation_additions"]),
        "candidate_files": candidate_import["file_count"],
        "program_sha256": sha256(PROGRAM_DIR / "ui-design-program.json"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
