#!/usr/bin/env python3
"""Build the deterministic G1 r2 exact-cover atlas and capability bindings."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json"
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
ADMISSION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/g1-admission-inventory.json"
CAPABILITY_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/capability-intake.json"
RECONCILIATION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/requirement-reconciliation.json"
G0_SCREENS = PROGRAM_DIR / "artifacts/g0-r2/screens-index.json"
G0_JOURNEYS = PROGRAM_DIR / "artifacts/g0-r2/journeys-index.json"
G1 = PROGRAM_DIR / "artifacts/g1-r2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path | str) -> Any:
    target = ROOT / path if isinstance(path, str) else path
    return json.loads(target.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(rendered)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def resolve_pointer(document: Any, pointer: str) -> Any:
    current = document
    for raw in pointer.removeprefix("/").split("/") if pointer else []:
        token = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def indexed(index_path: Path, identity_key: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for entry in load(index_path)["entries"]:
        target = ROOT / entry["path"]
        if sha256(target) != entry["sha256"]:
            raise ValueError(f"stale indexed shard: {entry['path']}")
        value = resolve_pointer(load(target), entry["json_pointer"])
        if value[identity_key] != entry["id"] or entry["id"] in result:
            raise ValueError(f"invalid or duplicate index identity: {entry['id']}")
        result[entry["id"]] = value
    return result


def declared_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = None
    if isinstance(value, dict) and isinstance(value.get("status"), str):
        return value["status"]
    if text.startswith("---\n"):
        for line in text.splitlines()[1:]:
            if line.strip() == "---":
                break
            if line.strip().startswith("status:"):
                return line.split(":", 1)[1].strip().strip("\"'") or None
    return None


def pending_origin(field: str) -> dict[str, Any]:
    return {
        "kind": "delegated_design_decision",
        "ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
        "rationale": f"{field} is intentionally unresolved until G2 r2 structure work.",
        "constraints": ["Do not assign family, wave, criticality, representative, or coverage structure during G1."],
    }


def screen_entry(
    admitted: dict[str, Any], admission_index: int, functional: dict[str, Any],
    intake_index: int, intake_hash: str, exception_by_screen: dict[str, str],
) -> dict[str, Any]:
    screen_id = admitted["screen_id"]
    classification = admitted["classification"]
    if functional["screen_id"] != screen_id or functional["surface_kind"] != classification:
        raise ValueError(f"screen identity or classification mismatch: {screen_id}")
    if classification == "historical_exclusion":
        disposition = "excluded"
        reason = f"{admitted['source_path']}#{admitted['source_pointer']}"
        consequence = "Historical evidence remains inspectable but is not an active design or execution route."
    elif classification == "internal_or_non_visual":
        disposition, reason, consequence = "internal", None, None
    else:
        disposition, reason, consequence = "in_scope", None, None
    pointer = f"/screens/{admission_index}"
    return {
        "screen_ref": {"path": ADMISSION_REL, "json_pointer": pointer, "expected_id": screen_id},
        "classification": classification,
        "classification_origin": {"kind": "product_contract", "ref": f"{ADMISSION_REL}#{pointer}/classification"},
        "disposition": disposition,
        "disposition_origin": {
            "kind": "derived_formula",
            "ref": f"{ADMISSION_REL}#{pointer}/classification",
            "formula": "historical_exclusion -> excluded; internal_or_non_visual -> internal; every other admitted classification -> in_scope",
        },
        "disposition_reason_ref": reason,
        "review_consequence": consequence,
        "design_family_id": None,
        "family_assignment_origin": pending_origin("design_family_id"),
        "wave_id": None,
        "wave_assignment_origin": pending_origin("wave_id"),
        "representative": False,
        "coverage_profile": None,
        "coverage_assignment_origin": pending_origin("coverage_profile"),
        "visual_baseline_ref": None,
        "functional_contract_ref": {
            "path": INTAKE_REL,
            "sha256": intake_hash,
            "json_pointer": f"/screens/{intake_index}",
            "expected_id": screen_id,
        },
        "shell_variant_id": functional.get("shell_variant_id"),
        "baseline_exception_ref": exception_by_screen.get(screen_id),
        "expected_action_ids": [action["action_id"] for action in functional.get("actions", [])],
        "unresolved_fields": ["design_family_id", "wave_id", "coverage_profile"] if disposition == "in_scope" else [],
    }


def journey_entry(admitted: dict[str, Any], admission_index: int, functional: dict[str, Any]) -> dict[str, Any]:
    journey_id = admitted["journey_id"]
    if functional["journey_id"] != journey_id:
        raise ValueError(f"journey identity mismatch: {journey_id}")
    entry_ids = functional.get("entry_screen_ids", [])
    terminal_ids = functional.get("terminal_screen_ids", [])
    admitted_ids = admitted["screen_ids"]
    if not entry_ids or not terminal_ids or not set(entry_ids + terminal_ids).issubset(admitted_ids):
        raise ValueError(f"journey lacks valid entry/terminal semantics: {journey_id}")
    pointer = f"/journeys/{admission_index}"
    return {
        "journey_ref": {"path": ADMISSION_REL, "json_pointer": pointer, "expected_id": journey_id},
        "entry_screen_ids": entry_ids,
        "intermediate_screen_ids": [item for item in admitted_ids if item not in set(entry_ids + terminal_ids)],
        "alternate_screen_ids": [],
        "failure_screen_ids": [],
        "recovery_screen_ids": [],
        "terminal_screen_ids": terminal_ids,
        "external_boundary_ids": [],
        "transitions": [],
        "unresolved_fields": ["criticality", "criticality_origin", "transitions"],
    }


def write_shards(kind: str, entries: list[dict[str, Any]], ref_key: str, wrapper: str) -> dict[str, str]:
    index_entries: list[dict[str, str]] = []
    for value in entries:
        identity = value[ref_key]["expected_id"]
        shard = G1 / kind / f"{identity}.json"
        write_json(shard, {wrapper: value})
        index_entries.append({
            "id": identity, "path": shard.relative_to(ROOT).as_posix(),
            "sha256": sha256(shard), "json_pointer": f"/{wrapper}",
        })
    index_path = G1 / f"{kind}-index.json"
    write_json(index_path, {
        "$schema": "program-artifact-index.schema.json",
        "schema_id": "codex.ui-program-artifact-index/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "index_kind": kind,
        "entries": index_entries,
    })
    return {"path": index_path.relative_to(ROOT).as_posix(), "sha256": sha256(index_path)}


def build_capabilities(screen_ids: set[str]) -> dict[str, Any]:
    intake = load(CAPABILITY_REL)
    reconciliation = load(RECONCILIATION_REL)
    capabilities = intake["capabilities"]
    capability_ids = [item["id"] for item in capabilities]
    if len(capability_ids) != len(set(capability_ids)):
        raise ValueError("duplicate capability identity")
    capability_set = set(capability_ids)
    bindings = [*reconciliation["owner_recommendations"], *reconciliation["reconciliation_additions"]]
    binding_ids = [item["id"] for item in bindings]
    if len(binding_ids) != len(set(binding_ids)):
        raise ValueError("duplicate promoted requirement binding")
    capability_bindings: dict[str, list[str]] = {item: [] for item in capability_ids}
    normalized: list[dict[str, Any]] = []
    for item in bindings:
        binding = item.get("binding", item)
        bound_screens = binding.get("screen_ids", [])
        bound_capabilities = binding.get("capability_ids", [])
        not_applicable = binding.get("not_applicable_reason")
        if not set(bound_screens).issubset(screen_ids):
            raise ValueError(f"binding references unknown screen: {item['id']}")
        if not set(bound_capabilities).issubset(capability_set):
            raise ValueError(f"binding references unknown capability: {item['id']}")
        if not (bound_screens or bound_capabilities or not_applicable):
            raise ValueError(f"binding has no target or justified not-applicable disposition: {item['id']}")
        for capability_id in bound_capabilities:
            capability_bindings[capability_id].append(item["id"])
        normalized.append({
            "binding_id": item["id"],
            "requirement_id": item.get("requirement_id"),
            "source_ref": item["source_ref"],
            "screen_ids": bound_screens,
            "capability_ids": bound_capabilities,
            "disposition": "not_applicable" if not_applicable else "bound",
            "not_applicable_reason": not_applicable,
        })
    cap_index_entries: list[dict[str, str]] = []
    for capability in capabilities:
        capability_id = capability["id"]
        shard = G1 / "capabilities" / f"{capability_id}.json"
        write_json(shard, {
            "capability": capability,
            "promoted_binding_ids": sorted(capability_bindings[capability_id]),
            "g2_ownership": ["journey criticality", "family assignment", "coverage profile", "representative selection", "workload-bounded wave assignment", "baseline inheritance"],
        })
        cap_index_entries.append({
            "id": capability_id, "path": shard.relative_to(ROOT).as_posix(),
            "sha256": sha256(shard), "json_pointer": "/capability",
        })
    cap_index = G1 / "capabilities-index.json"
    write_json(cap_index, {
        "schema_id": "custometry.ui-capability-index/v1", "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2, "index_kind": "capabilities", "entries": cap_index_entries,
    })
    binding_index = G1 / "promoted-requirement-bindings.json"
    write_json(binding_index, {
        "schema_id": "custometry.ui-promoted-requirement-bindings/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2", "program_revision": 2,
        "expected_owner_recommendations": len(reconciliation["owner_recommendations"]),
        "expected_reconciliation_additions": len(reconciliation["reconciliation_additions"]),
        "bindings": normalized,
    })
    return {
        "capabilities": len(capabilities), "bindings": len(normalized),
        "capabilities_index": {"path": cap_index.relative_to(ROOT).as_posix(), "sha256": sha256(cap_index)},
        "bindings_index": {"path": binding_index.relative_to(ROOT).as_posix(), "sha256": sha256(binding_index)},
    }


def main() -> None:
    program = load(PROGRAM)
    intake = load(INTAKE_REL)
    baseline = load(BASELINE_REL)
    admission = load(ADMISSION_REL)
    g0_screens = indexed(G0_SCREENS, "screen_id")
    g0_journeys = indexed(G0_JOURNEYS, "journey_id")
    intake_by_id = {item["screen_id"]: (index, item) for index, item in enumerate(intake["screens"])}
    admitted_screen_ids = [item["screen_id"] for item in admission["screens"]]
    admitted_journey_ids = [item["journey_id"] for item in admission["journeys"]]
    if len(admitted_screen_ids) != len(set(admitted_screen_ids)) or set(admitted_screen_ids) != set(intake_by_id) or set(admitted_screen_ids) != set(g0_screens):
        raise ValueError("G0 screen sources do not exact-cover the authoritative admission inventory")
    if len(admitted_journey_ids) != len(set(admitted_journey_ids)) or set(admitted_journey_ids) != set(g0_journeys):
        raise ValueError("G0 journey source does not exact-cover the authoritative admission inventory")
    for screen_id in admitted_screen_ids:
        if g0_screens[screen_id] != intake_by_id[screen_id][1]:
            raise ValueError(f"G0 shard differs from intake: {screen_id}")
    exception_by_screen: dict[str, str] = {}
    for exception in baseline["exceptions"]:
        for screen_id in exception["screen_ids"]:
            if screen_id in exception_by_screen:
                raise ValueError(f"duplicate baseline exception: {screen_id}")
            exception_by_screen[screen_id] = exception["exception_id"]
    intake_hash = sha256(ROOT / INTAKE_REL)
    screens = [screen_entry(item, index, intake_by_id[item["screen_id"]][1], intake_by_id[item["screen_id"]][0], intake_hash, exception_by_screen) for index, item in enumerate(admission["screens"])]
    journeys = [journey_entry(item, index, g0_journeys[item["journey_id"]]) for index, item in enumerate(admission["journeys"])]
    screens_index = write_shards("screens", screens, "screen_ref", "screen")
    journeys_index = write_shards("journeys", journeys, "journey_ref", "journey")
    capability_result = build_capabilities(set(admitted_screen_ids))
    for source in program["source_contracts"]:
        source["required_status"] = declared_status(ROOT / source["path"])
    program["validation_profile"] = "atlas_gate"
    program["screens"] = screens
    program["journeys"] = journeys
    program["artifact_indexes"]["screens"] = screens_index
    program["artifact_indexes"]["journeys"] = journeys_index
    write_json(PROGRAM, program)
    write_json(G1 / "ui-design-program.snapshot.json", program)
    result = {
        "status": "passed", "screens": len(screens), "journeys": len(journeys),
        **capability_result, "screens_index": screens_index, "journeys_index": journeys_index,
        "program_sha256": sha256(PROGRAM), "snapshot_sha256": sha256(G1 / "ui-design-program.snapshot.json"),
    }
    write_json(G1 / "exact-cover-summary.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
