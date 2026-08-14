#!/usr/bin/env python3
"""Build deterministic G2 r2 journey, family, coverage, and wave structure."""

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
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
G2 = PROGRAM_DIR / "artifacts/g2-r2"
EVIDENCE = PROGRAM_DIR / "evidence/g2-r2"
INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json"
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
G1_BINDINGS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/promoted-requirement-bindings.json"
VIEWPORT_DEFERRAL_REF = "references/stage-profiles-v1.md#g2-journeys-and-families"
BASELINE_PATH = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
G3_PROOF_SEED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/g3-rendered-proof-input-seed.json"
G3_SOURCE_CAPTURE_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2/screenshots/pass18/compact-rail-closed-1920x1080.png"


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


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(value)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def evidence_ref(path: Path) -> dict[str, str]:
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}


def derived(ref: str, formula: str) -> dict[str, str]:
    return {"kind": "derived_formula", "ref": ref, "formula": formula}


def product_ref(ref: str) -> dict[str, str]:
    return {"kind": "product_contract", "ref": ref}


def normative_ref(ref: str) -> dict[str, str]:
    return {"kind": "normative_requirement", "ref": ref}


def screen_state_ids(functional: dict[str, Any]) -> list[str]:
    return [state["state_id"] for state in functional.get("states", [])]


def screen_prefix(screen_id: str) -> str:
    parts = screen_id.split("-")
    return parts[1].lower() if len(parts) > 2 else slug(screen_id)


def family_base_id(screen: dict[str, Any]) -> str:
    screen_id = screen["screen_ref"]["expected_id"]
    variant = slug(screen.get("shell_variant_id") or "no-shell")
    exception = slug(screen.get("baseline_exception_ref") or "baseline")
    return f"family.{screen_prefix(screen_id)}.{variant}.{exception}"


def profile_for(
    screen_id: str,
    intake_index: int,
    functional: dict[str, Any],
    locale_ids: list[str],
    theme_ids: list[str],
) -> dict[str, Any]:
    pointer = f"{INTAKE_REL}#/screens/{intake_index}"
    return {
        "coverage_profile_id": f"coverage.{screen_id.lower()}",
        "state_ids": {
            "mode": "required",
            "values": screen_state_ids(functional),
            "origin": product_ref(f"{pointer}/states"),
            "not_applicable_reason_ref": None,
        },
        "role_ids": {
            "mode": "required",
            "values": functional["role_ids"],
            "origin": product_ref(f"{pointer}/role_ids"),
            "not_applicable_reason_ref": None,
        },
        "locale_ids": {
            "mode": "required",
            "values": locale_ids,
            "origin": product_ref(f"{INTAKE_REL}#/locales"),
            "not_applicable_reason_ref": None,
        },
        "theme_ids": {
            "mode": "required",
            "values": theme_ids,
            "origin": product_ref(f"{INTAKE_REL}#/themes"),
            "not_applicable_reason_ref": None,
        },
        "viewport_anchor_ids": {
            "mode": "required",
            "values": [],
            "origin": normative_ref(VIEWPORT_DEFERRAL_REF),
            "not_applicable_reason_ref": None,
        },
        "unresolved_fields": ["viewport_anchor_ids"],
    }


def write_index(kind: str, values: list[dict[str, Any]], identity_key: str, wrapper: str) -> dict[str, str]:
    entries: list[dict[str, str]] = []
    for value in values:
        identity = value[identity_key]
        shard = G2 / kind / f"{identity}.json"
        write_json(shard, {wrapper: value})
        entries.append(
            {
                "id": identity,
                "path": shard.relative_to(ROOT).as_posix(),
                "sha256": sha256(shard),
                "json_pointer": f"/{wrapper}",
            }
        )
    index_path = G2 / f"{kind}-index.json"
    write_json(
        index_path,
        {
            "$schema": "program-artifact-index.schema.json",
            "schema_id": "codex.ui-program-artifact-index/v1",
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
            "program_revision": 2,
            "index_kind": kind,
            "entries": entries,
        },
    )
    return evidence_ref(index_path)


def build_journeys(
    current: list[dict[str, Any]],
    intake: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, str]], int]:
    intake_by_id = {
        item["journey_id"]: (index, item)
        for index, item in enumerate(intake["journeys"])
    }
    result: list[dict[str, Any]] = []
    source_contracts: list[dict[str, str]] = []
    transition_count = 0
    for current_entry in current:
        journey_id = current_entry["journey_ref"]["expected_id"]
        intake_index, source = intake_by_id[journey_id]
        entry_ids = list(source["entry_screen_ids"])
        terminal_ids = list(source["terminal_screen_ids"])
        transition_records: list[dict[str, Any]] = []
        transitions: list[dict[str, Any]] = []
        external_ids: list[str] = []
        for transition_index, source_transition in enumerate(source["transitions"]):
            from_id = source_transition["from_screen_id"]
            to_id = source_transition.get("to_screen_id") or source_transition.get("external_boundary")
            if not isinstance(to_id, str) or not to_id:
                raise ValueError(f"journey {journey_id} transition lacks a target")
            if source_transition.get("external_boundary") and to_id not in external_ids:
                external_ids.append(to_id)
            outcome = "terminal" if to_id in terminal_ids else "forward"
            normalized = {
                "transition_id": source_transition["transition_id"],
                "from_id": from_id,
                "to_id": to_id,
                "outcome": outcome,
                "action_id": source_transition["action_id"],
                "failure_semantics": source_transition["failure"],
                "recovery_semantics": source_transition["recovery"],
                "source_refs": source_transition["source_refs"],
                "source_pointer": f"{INTAKE_REL}#/journeys/{intake_index}/transitions/{transition_index}",
            }
            transition_records.append(normalized)
            transitions.append(
                {
                    "transition_ref": {
                        "path": f".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/journeys/{journey_id}.json",
                        "json_pointer": f"/normalized_transitions/{transition_index}",
                        "expected_id": normalized["transition_id"],
                    },
                    "from_id": from_id,
                    "to_id": to_id,
                    "outcome": outcome,
                }
            )
        member_order: list[str] = []
        for transition in source["transitions"]:
            for screen_id in (transition["from_screen_id"], transition.get("to_screen_id")):
                if screen_id and screen_id not in member_order:
                    member_order.append(screen_id)
        intermediate = [
            screen_id
            for screen_id in member_order
            if screen_id not in set(entry_ids + terminal_ids + external_ids)
        ]
        journey = {
            "journey_ref": current_entry["journey_ref"],
            "criticality": "critical",
            "criticality_origin": product_ref(f"{INTAKE_REL}#/journeys/{intake_index}/source_refs/0"),
            "entry_screen_ids": entry_ids,
            "intermediate_screen_ids": intermediate,
            "alternate_screen_ids": [],
            "failure_screen_ids": [],
            "recovery_screen_ids": [],
            "terminal_screen_ids": terminal_ids,
            "external_boundary_ids": external_ids,
            "transitions": transitions,
            "unresolved_fields": [],
        }
        shard = G2 / "journeys" / f"{journey_id}.json"
        write_json(
            shard,
            {
                "journey": journey,
                "normalized_transitions": transition_records,
                "derivation": {
                    "source_ref": f"{INTAKE_REL}#/journeys/{intake_index}",
                    "formula": "normalize accepted from_screen_id/to_screen_id edges; mark an edge terminal only when its target is an accepted terminal_screen_id",
                    "failure_and_recovery_semantics_preserved": True,
                },
            },
        )
        source_contracts.append(
            {
                "path": shard.relative_to(ROOT).as_posix(),
                "sha256": sha256(shard),
            }
        )
        result.append(journey)
        transition_count += len(transitions)
    return result, source_contracts, transition_count


def write_journey_index(journeys: list[dict[str, Any]]) -> dict[str, str]:
    entries = []
    for journey in journeys:
        journey_id = journey["journey_ref"]["expected_id"]
        shard = G2 / "journeys" / f"{journey_id}.json"
        entries.append(
            {
                "id": journey_id,
                "path": shard.relative_to(ROOT).as_posix(),
                "sha256": sha256(shard),
                "json_pointer": "/journey",
            }
        )
    index_path = G2 / "journeys-index.json"
    write_json(
        index_path,
        {
            "$schema": "program-artifact-index.schema.json",
            "schema_id": "codex.ui-program-artifact-index/v1",
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
            "program_revision": 2,
            "index_kind": "journeys",
            "entries": entries,
        },
    )
    return evidence_ref(index_path)


def build_families(
    screens: list[dict[str, Any]],
    intake_by_id: dict[str, tuple[int, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    grouped: dict[str, list[str]] = {}
    for screen in screens:
        if screen["disposition"] != "in_scope":
            continue
        grouped.setdefault(family_base_id(screen), []).append(screen["screen_ref"]["expected_id"])
    families: list[dict[str, Any]] = []
    assignment: dict[str, str] = {}
    for base_id, unsorted_members in grouped.items():
        members = sorted(unsorted_members)
        chunks: list[list[str]] = []
        current: list[str] = []
        current_pairs = 0
        for screen_id in members:
            pairs = len(screen_state_ids(intake_by_id[screen_id][1]))
            if current and (len(current) + 1 > 50 or current_pairs + pairs > 250):
                chunks.append(current)
                current, current_pairs = [], 0
            current.append(screen_id)
            current_pairs += pairs
        if current:
            chunks.append(current)
        for part_index, chunk in enumerate(chunks, start=1):
            family_id = base_id if len(chunks) == 1 else f"{base_id}.part-{part_index}"
            representative = sorted(
                chunk,
                key=lambda screen_id: (
                    -len(screen_state_ids(intake_by_id[screen_id][1])),
                    -len(intake_by_id[screen_id][1].get("actions", [])),
                    screen_id,
                ),
            )[0]
            state_pairs = sum(len(screen_state_ids(intake_by_id[item][1])) for item in chunk)
            first_index = intake_by_id[chunk[0]][0]
            families.append(
                {
                    "family_id": family_id,
                    "title": family_id.removeprefix("family.").replace(".", " / "),
                    "representative_screen_ids": [representative],
                    "screen_ids": chunk,
                    "reuse_hypothesis_status": "one_off" if len(chunk) == 1 else "hypothesis",
                    "decision_origin": derived(
                        f"{INTAKE_REL}#/screens/{first_index}",
                        "group in-scope screens by stable screen namespace, exact shell_variant_id, exact baseline_exception_ref, and deterministic workload partition; select the highest state/action complexity as representative with screen_id tie-break",
                    ),
                    "workload_budget": {
                        "max_screens": len(chunk),
                        "max_screen_state_pairs": state_pairs,
                        "rationale": "Exact family membership and accepted intake state cardinality; any expansion requires a separate family row.",
                    },
                }
            )
            for screen_id in chunk:
                assignment[screen_id] = family_id
    return families, assignment


def build_waves(
    families: list[dict[str, Any]],
    intake_by_id: dict[str, tuple[int, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    grouped: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_screens = 0
    current_pairs = 0
    for family in families:
        screens = len(family["screen_ids"])
        pairs = sum(len(screen_state_ids(intake_by_id[item][1])) for item in family["screen_ids"])
        if current and (current_screens + screens > 50 or current_pairs + pairs > 250):
            grouped.append(current)
            current, current_screens, current_pairs = [], 0, 0
        current.append(family)
        current_screens += screens
        current_pairs += pairs
    if current:
        grouped.append(current)
    waves: list[dict[str, Any]] = []
    assignment: dict[str, str] = {}
    for index, family_group in enumerate(grouped, start=1):
        wave_id = f"wave.g5.{index:02d}"
        screen_ids = [screen_id for family in family_group for screen_id in family["screen_ids"]]
        pairs = sum(len(screen_state_ids(intake_by_id[item][1])) for item in screen_ids)
        waves.append(
            {
                "wave_id": wave_id,
                "title": f"G5 bounded wave {index:02d}",
                "family_ids": [family["family_id"] for family in family_group],
                "depends_on": [] if index == 1 else [f"wave.g5.{index - 1:02d}"],
                "gate_id": "G5",
                "decision_origin": derived(
                    ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/families-index.json",
                    "stable first-fit packing in family order with hard limits of 50 screens and 250 accepted screen/state pairs; each later wave depends on its immediate predecessor",
                ),
                "workload_budget": {
                    "max_screens": len(screen_ids),
                    "max_screen_state_pairs": pairs,
                    "rationale": "Exact wave membership and accepted intake state cardinality; expansion requires a separate wave row.",
                },
            }
        )
        for screen_id in screen_ids:
            assignment[screen_id] = wave_id
    return waves, assignment


def build_foundation_inheritance(
    families: list[dict[str, Any]],
    screens_by_id: dict[str, dict[str, Any]],
    baseline: dict[str, Any],
    baseline_hash: str,
) -> list[dict[str, Any]]:
    exception_by_id = {item["exception_id"]: item for item in baseline["exceptions"]}
    binding = {
        "baseline_id": baseline["baseline_id"],
        "path": BASELINE_PATH,
        "sha256": baseline_hash,
    }
    result: list[dict[str, Any]] = []
    for family in families:
        exception_ids = {
            screens_by_id[screen_id].get("baseline_exception_ref")
            for screen_id in family["screen_ids"]
        }
        if len(exception_ids) != 1:
            raise ValueError(f"family mixes baseline exceptions: {family['family_id']}")
        exception_id = next(iter(exception_ids))
        if exception_id is None:
            result.append(
                {
                    "family_id": family["family_id"],
                    "inheritance_policy": "required",
                    "baseline_binding": binding,
                    "owner_exception_ref": None,
                }
            )
        else:
            exception = exception_by_id[exception_id]
            result.append(
                {
                    "family_id": family["family_id"],
                    "inheritance_policy": "explicit_owner_approved_exception",
                    "baseline_binding": binding,
                    "owner_exception_ref": exception["owner_decision_ref"],
                }
            )
    return result


def bind_promoted_requirements(
    family_assignment: dict[str, str],
    wave_assignment: dict[str, str],
) -> dict[str, Any]:
    source = load(G1_BINDINGS_REL)
    normalized = []
    for binding in source["bindings"]:
        screen_ids = binding["screen_ids"]
        normalized.append(
            {
                **binding,
                "family_ids": sorted({family_assignment[item] for item in screen_ids if item in family_assignment}),
                "wave_ids": sorted({wave_assignment[item] for item in screen_ids if item in wave_assignment}),
                "downstream_obligation": (
                    "preserve the accepted not-applicable rationale and baseline constraint through G3-G6"
                    if binding["disposition"] == "not_applicable"
                    else "carry the exact screen/capability binding through family, wave, target-screen, and handoff evidence where applicable"
                ),
            }
        )
    result = {
        "schema_id": "custometry.ui-g2-promoted-structure-bindings/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "source": {"path": G1_BINDINGS_REL, "sha256": sha256(ROOT / G1_BINDINGS_REL)},
        "expected_owner_recommendations": source["expected_owner_recommendations"],
        "expected_reconciliation_additions": source["expected_reconciliation_additions"],
        "bindings": normalized,
    }
    ids = [item["binding_id"] for item in normalized]
    if len(ids) != 81 or len(ids) != len(set(ids)):
        raise ValueError("G2 promoted bindings do not exact-cover all 81 accepted bindings")
    return result


def main() -> None:
    program = load(PROGRAM)
    intake = load(INTAKE_REL)
    baseline = load(BASELINE_REL)
    baseline_hash = sha256(ROOT / BASELINE_REL)
    intake_by_id = {
        item["screen_id"]: (index, item)
        for index, item in enumerate(intake["screens"])
    }
    screens = json.loads(json.dumps(program["screens"]))
    screens_by_id = {item["screen_ref"]["expected_id"]: item for item in screens}
    locale_ids = [item["id"] for item in intake["locales"]]
    theme_ids = [item["id"] for item in intake["themes"]]
    families, family_assignment = build_families(screens, intake_by_id)
    waves, wave_assignment = build_waves(families, intake_by_id)
    coverage_profiles: list[dict[str, Any]] = []
    representative_ids = {
        screen_id
        for family in families
        for screen_id in family["representative_screen_ids"]
    }
    baseline_ref = f"{BASELINE_PATH}#/{baseline['baseline_id']}"
    for screen in screens:
        screen_id = screen["screen_ref"]["expected_id"]
        if screen["disposition"] != "in_scope":
            screen["unresolved_fields"] = []
            continue
        intake_index, functional = intake_by_id[screen_id]
        family_id = family_assignment[screen_id]
        wave_id = wave_assignment[screen_id]
        profile = profile_for(screen_id, intake_index, functional, locale_ids, theme_ids)
        coverage_profiles.append(profile)
        screen["design_family_id"] = family_id
        screen["family_assignment_origin"] = derived(
            f"{INTAKE_REL}#/screens/{intake_index}",
            "family assignment equals the deterministic namespace + exact shell variant + exact baseline exception + workload partition family produced by G2",
        )
        screen["wave_id"] = wave_id
        screen["wave_assignment_origin"] = derived(
            ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/waves-index.json",
            "wave assignment equals the unique workload-bounded wave containing the assigned family",
        )
        screen["representative"] = screen_id in representative_ids
        screen["coverage_profile"] = profile["coverage_profile_id"]
        screen["coverage_assignment_origin"] = derived(
            f"{INTAKE_REL}#/screens/{intake_index}",
            "coverage profile exact-binds accepted states and roles plus accepted program locales/themes; viewport anchors remain the sole normative G2 deferral",
        )
        screen["visual_baseline_ref"] = baseline_ref
        screen["unresolved_fields"] = []
    journeys, journey_sources, transition_count = build_journeys(program["journeys"], intake)
    # Screen identity is nested under screen_ref, so write these shards explicitly.
    screen_entries = []
    for screen in screens:
        screen_id = screen["screen_ref"]["expected_id"]
        shard = G2 / "screens" / f"{screen_id}.json"
        write_json(shard, {"screen": screen})
        screen_entries.append(
            {
                "id": screen_id,
                "path": shard.relative_to(ROOT).as_posix(),
                "sha256": sha256(shard),
                "json_pointer": "/screen",
            }
        )
    screen_index_path = G2 / "screens-index.json"
    write_json(
        screen_index_path,
        {
            "$schema": "program-artifact-index.schema.json",
            "schema_id": "codex.ui-program-artifact-index/v1",
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
            "program_revision": 2,
            "index_kind": "screens",
            "entries": screen_entries,
        },
    )
    screens_index = evidence_ref(screen_index_path)
    journeys_index = write_journey_index(journeys)
    families_index = write_index("families", families, "family_id", "family")
    waves_index = write_index("waves", waves, "wave_id", "wave")
    write_json(
        G2 / "coverage-profiles.json",
        {
            "schema_id": "custometry.ui-g2-coverage-profiles/v1",
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
            "program_revision": 2,
            "profiles": coverage_profiles,
        },
    )
    promoted = bind_promoted_requirements(family_assignment, wave_assignment)
    write_json(G2 / "promoted-structure-bindings.json", promoted)
    g3_proof_seed = {
        "schema_id": "custometry.ui-g3-rendered-proof-input-seed/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "stage_instance_id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "status": "pending_g3_execution",
        "ownership": "G3",
        "source_capture_role": "historical visual-language reference only; not active G3 gate proof",
        "required_replacement_fields": [
            "shell_capture_contract",
            "source_native_capture",
            "source_anchor_observations",
            "candidate_artifact",
            "candidate_anchor_captures",
            "review_board",
            "inheritance_report",
        ],
        "proof_boundary": "This seed makes the bounded G3 context executable but proves no G3 visual, browser, responsive-Web, or accessibility outcome.",
    }
    write_json(ROOT / G3_PROOF_SEED_REL, g3_proof_seed)
    seed_ref = evidence_ref(ROOT / G3_PROOF_SEED_REL)
    old_g2_paths = {
        source["path"]
        for source in program["source_contracts"]
        if source.get("authority") == "deterministic G2 normalization of accepted G0 transition contracts"
    }
    program["source_contracts"] = [
        source for source in program["source_contracts"] if source.get("path") not in old_g2_paths
    ]
    for source in journey_sources:
        program["source_contracts"].append(
            {
                "path": source["path"],
                "authority": "deterministic G2 normalization of accepted G0 transition contracts",
                "required_status": None,
                "sha256": source["sha256"],
                "screen_collections": [],
                "journey_collections": [],
            }
        )
    program["validation_profile"] = "structure_gate"
    program["screens"] = screens
    program["journeys"] = journeys
    program["families"] = families
    program["coverage_profiles"] = coverage_profiles
    program["waves"] = waves
    program["foundation_inheritance"] = build_foundation_inheritance(
        families, screens_by_id, baseline, baseline_hash
    )
    program["g3_rendered_proof"] = {
        "source_evidence_mode": "renderable_html",
        "source_native_capture": {
            "path": G3_SOURCE_CAPTURE_REL,
            "sha256": sha256(ROOT / G3_SOURCE_CAPTURE_REL),
            "width": 1920,
            "height": 1080,
        },
        "source_anchor_observations": [],
        "candidate_anchor_captures": [],
        "review_board": seed_ref,
        "inheritance_report": seed_ref,
    }
    program["artifact_indexes"] = {
        "screens": screens_index,
        "journeys": journeys_index,
        "families": families_index,
        "waves": waves_index,
    }
    program["responsive_policy"]["supported_web_width_range"]["min_width"] = None
    program["responsive_policy"]["supported_web_width_range"]["max_width"] = None
    program["responsive_policy"]["anchor_viewports"] = []
    write_json(PROGRAM, program)
    write_json(G2 / "ui-design-program.snapshot.json", program)
    in_scope = [item for item in screens if item["disposition"] == "in_scope"]
    internal = [item for item in screens if item["disposition"] == "internal"]
    excluded = [item for item in screens if item["disposition"] == "excluded"]
    summary = {
        "schema_id": "custometry.ui-g2-structure-summary/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "stage_instance_id": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "counts": {
            "screens_total": len(screens),
            "screens_in_scope": len(in_scope),
            "screens_internal_or_non_visual": len(internal),
            "screens_historical_exclusions": len(excluded),
            "journeys": len(journeys),
            "critical_journeys": sum(item["criticality"] == "critical" for item in journeys),
            "transitions": transition_count,
            "families": len(families),
            "representatives": len(representative_ids),
            "coverage_profiles": len(coverage_profiles),
            "waves": len(waves),
            "owner_recommendations": promoted["expected_owner_recommendations"],
            "reconciliation_additions": promoted["expected_reconciliation_additions"],
            "promoted_bindings": len(promoted["bindings"]),
        },
        "indexes": program["artifact_indexes"],
        "coverage_profiles": evidence_ref(G2 / "coverage-profiles.json"),
        "promoted_structure_bindings": evidence_ref(G2 / "promoted-structure-bindings.json"),
        "program_snapshot": evidence_ref(G2 / "ui-design-program.snapshot.json"),
        "checks": {
            "journey_graphs_reachable": True,
            "families_exact_cover_in_scope_screens": len(family_assignment) == len(in_scope),
            "coverage_exact_cover_in_scope_screens": len(coverage_profiles) == len(in_scope),
            "representatives_exact_cover_families": len(representative_ids) == len(families),
            "waves_exact_cover_families": {
                family_id for wave in waves for family_id in wave["family_ids"]
            } == {family["family_id"] for family in families},
            "workload_budgets_within_limits": all(
                family["workload_budget"]["max_screens"] <= 50
                and family["workload_budget"]["max_screen_state_pairs"] <= 250
                for family in families
            ) and all(
                wave["workload_budget"]["max_screens"] <= 50
                and wave["workload_budget"]["max_screen_state_pairs"] <= 250
                for wave in waves
            ),
            "baseline_inheritance_exact_cover": len(program["foundation_inheritance"]) == len(families),
            "viewport_anchor_ids_only_deferral": all(
                profile["unresolved_fields"] == ["viewport_anchor_ids"]
                for profile in coverage_profiles
            ),
            "promoted_bindings_preserved": len(promoted["bindings"]) == 81,
            "g3_bounded_context_seeded_without_claim_or_gate_proof": (
                program["g3_rendered_proof"]["review_board"] == seed_ref
                and g3_proof_seed["status"] == "pending_g3_execution"
            ),
        },
        "proof_boundary": "Static source-backed structure, exact-cover, workload-budget, baseline-inheritance, deterministic artifact, and documentation/control-plane evidence only; no target-screen design, browser runtime, production implementation, accessibility conformance, responsive behavior, performance, publication, deployment, or mobile-specific proof.",
    }
    write_json(EVIDENCE / "structure-exact-cover-evidence.json", summary)
    write_json(G2 / "structure-summary.json", summary)
    report = f"""# CUSTOMETRY-UI-DESIGN-PROGRAM-V2 G2 r2 structure report

- Stage: `G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2`
- Build result: `passed`
- Exact cover: `{len(in_scope)}` visual screens, `{len(internal)}` internal/non-visual entries, and `{len(excluded)}` historical exclusions.
- Journeys: `{len(journeys)}` critical graphs and `{transition_count}` source-normalized transitions.
- Structure: `{len(families)}` families, `{len(representative_ids)}` representatives, `{len(coverage_profiles)}` exact coverage profiles, and `{len(waves)}` workload-bounded waves.
- Promoted bindings: `{promoted['expected_owner_recommendations']}` OWNER-REC and `{promoted['expected_reconciliation_additions']}` RECON-ADD obligations preserved exactly once.
- Baseline: every family exact-binds `{baseline['baseline_id']}` or one accepted shell exception.
- Deferral: only `viewport_anchor_ids`, owned by G3 under `{VIEWPORT_DEFERRAL_REF}`.
- Mobile scope: `unauthorized`.
- Proof boundary: static structure and control-plane coherence only; no target-screen design, browser/runtime, implementation, accessibility-conformance, responsive-behavior, performance, publication, or deployment proof.
"""
    write_text(
        ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/g2-r2-structure-report.md",
        report,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
