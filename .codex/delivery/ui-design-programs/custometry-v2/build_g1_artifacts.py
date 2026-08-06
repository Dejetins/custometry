#!/usr/bin/env python3
"""Assemble the deterministic G1 atlas shards and bind them into the program."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
PROGRAM_PATH = PROGRAM_DIR / "ui-design-program.json"
INTAKE_PATH = PROGRAM_DIR / "ui-program-intake.json"
BASELINE_PATH = PROGRAM_DIR / "platform-ui-baseline.json"
ADMISSION_REL = (
    ".codex/delivery/ui-design-programs/custometry-v2/"
    "evidence/g0/g1-admission-inventory.json"
)
ADMISSION_PATH = PROJECT_ROOT / ADMISSION_REL
G0_SCREENS_INDEX = PROGRAM_DIR / "artifacts/g0/screens-index.json"
G0_JOURNEYS_INDEX = PROGRAM_DIR / "artifacts/g0/journeys-index.json"
G1_DIR = PROGRAM_DIR / "artifacts/g1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = canonical_json(value)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as handle:
        handle.write(rendered)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer!r}")
    current = document
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def load_indexed_values(index_path: Path) -> list[tuple[dict[str, Any], Any]]:
    index = load_json(index_path)
    result: list[tuple[dict[str, Any], Any]] = []
    for entry in index["entries"]:
        target = PROJECT_ROOT / entry["path"]
        actual_hash = sha256(target)
        if actual_hash != entry["sha256"]:
            raise ValueError(
                f"hash mismatch for {entry['id']}: {actual_hash} != {entry['sha256']}"
            )
        value = resolve_pointer(load_json(target), entry["json_pointer"])
        observed_id = value.get("screen_id") or value.get("journey_id")
        if observed_id != entry["id"]:
            raise ValueError(
                f"identity mismatch for {entry['id']}: resolved {observed_id!r}"
            )
        result.append((entry, value))
    return result


def declared_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    try:
        document = json.loads(text)
    except json.JSONDecodeError:
        document = None
    if isinstance(document, dict) and isinstance(document.get("status"), str):
        return document["status"]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if stripped.startswith("status:"):
            return stripped.split(":", 1)[1].strip().strip('"\'') or None
    return None


def pending_g2_origin(field: str) -> dict[str, Any]:
    return {
        "kind": "delegated_design_decision",
        "ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
        "rationale": f"{field} is intentionally unresolved until G2 structure work.",
        "constraints": [
            "Do not assign family, wave, or coverage structure during G1."
        ],
    }


def assemble_screen_entry(
    admission_screen: dict[str, Any],
    admission_index: int,
    functional: dict[str, Any],
    intake_index: int,
    intake_hash: str,
    exception_by_screen: dict[str, str],
) -> dict[str, Any]:
    screen_id = admission_screen["screen_id"]
    classification = admission_screen["classification"]
    if functional["screen_id"] != screen_id:
        raise ValueError(f"functional identity mismatch for {screen_id}")
    if functional["surface_kind"] != classification:
        raise ValueError(f"classification mismatch for {screen_id}")

    if classification == "historical_exclusion":
        disposition = "excluded"
        disposition_reason_ref = (
            f"{admission_screen['source_path']}#{admission_screen['source_pointer']}"
        )
        review_consequence = (
            "Historical evidence remains inspectable but is not an active design or "
            "execution route."
        )
    elif classification == "internal_or_non_visual":
        disposition = "internal"
        disposition_reason_ref = None
        review_consequence = None
    else:
        disposition = "in_scope"
        disposition_reason_ref = None
        review_consequence = None

    admission_pointer = f"/screens/{admission_index}"
    unresolved = (
        ["design_family_id", "wave_id", "coverage_profile"]
        if disposition == "in_scope"
        else []
    )
    return {
        "screen_ref": {
            "path": ADMISSION_REL,
            "json_pointer": admission_pointer,
            "expected_id": screen_id,
        },
        "classification": classification,
        "classification_origin": {
            "kind": "product_contract",
            "ref": f"{ADMISSION_REL}#{admission_pointer}/classification",
        },
        "disposition": disposition,
        "disposition_origin": {
            "kind": "derived_formula",
            "ref": f"{ADMISSION_REL}#{admission_pointer}/classification",
            "formula": (
                "historical_exclusion -> excluded; internal_or_non_visual -> "
                "internal; every other admitted classification -> in_scope"
            ),
        },
        "disposition_reason_ref": disposition_reason_ref,
        "review_consequence": review_consequence,
        "design_family_id": None,
        "family_assignment_origin": pending_g2_origin("design_family_id"),
        "wave_id": None,
        "wave_assignment_origin": pending_g2_origin("wave_id"),
        "representative": False,
        "coverage_profile": None,
        "coverage_assignment_origin": pending_g2_origin("coverage_profile"),
        "visual_baseline_ref": None,
        "functional_contract_ref": {
            "path": ".codex/delivery/ui-design-programs/custometry-v2/ui-program-intake.json",
            "sha256": intake_hash,
            "json_pointer": f"/screens/{intake_index}",
            "expected_id": screen_id,
        },
        "shell_variant_id": functional.get("shell_variant_id"),
        "baseline_exception_ref": exception_by_screen.get(screen_id),
        "expected_action_ids": [
            action["action_id"] for action in functional.get("actions", [])
        ],
        "unresolved_fields": unresolved,
    }


def assemble_journey_entry(
    admission_journey: dict[str, Any],
    admission_index: int,
    functional: dict[str, Any],
) -> dict[str, Any]:
    journey_id = admission_journey["journey_id"]
    if functional["journey_id"] != journey_id:
        raise ValueError(f"journey identity mismatch for {journey_id}")
    admitted_ids = admission_journey["screen_ids"]
    entry_ids = functional.get("entry_screen_ids", [])
    terminal_ids = functional.get("terminal_screen_ids", [])
    if not entry_ids or not terminal_ids:
        raise ValueError(f"journey {journey_id} lacks entry or terminal semantics")
    if set(admitted_ids) != {
        *entry_ids,
        *terminal_ids,
        *[item for item in admitted_ids if item not in entry_ids + terminal_ids],
    }:
        raise ValueError(f"journey membership mismatch for {journey_id}")
    intermediate_ids = [
        item for item in admitted_ids if item not in set(entry_ids + terminal_ids)
    ]
    admission_pointer = f"/journeys/{admission_index}"
    return {
        "journey_ref": {
            "path": ADMISSION_REL,
            "json_pointer": admission_pointer,
            "expected_id": journey_id,
        },
        "entry_screen_ids": entry_ids,
        "intermediate_screen_ids": intermediate_ids,
        "alternate_screen_ids": [],
        "failure_screen_ids": [],
        "recovery_screen_ids": [],
        "terminal_screen_ids": terminal_ids,
        "external_boundary_ids": [],
        "transitions": [],
        "unresolved_fields": [
            "criticality",
            "criticality_origin",
            "transitions",
        ],
    }


def write_shards(
    kind: str, entries: list[dict[str, Any]], identity_key: str, wrapper: str
) -> tuple[Path, str]:
    shard_dir = G1_DIR / kind
    index_entries: list[dict[str, Any]] = []
    for value in entries:
        identity = value[identity_key]["expected_id"]
        shard_path = shard_dir / f"{identity}.json"
        write_json(shard_path, {wrapper: value})
        index_entries.append(
            {
                "id": identity,
                "path": shard_path.relative_to(PROJECT_ROOT).as_posix(),
                "sha256": sha256(shard_path),
                "json_pointer": f"/{wrapper}",
            }
        )
    index_path = G1_DIR / f"{kind}-index.json"
    write_json(
        index_path,
        {
            "$schema": "program-artifact-index.schema.json",
            "schema_id": "codex.ui-program-artifact-index/v1",
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
            "program_revision": 1,
            "index_kind": kind,
            "entries": index_entries,
        },
    )
    return index_path, sha256(index_path)


def main() -> None:
    program = load_json(PROGRAM_PATH)
    intake = load_json(INTAKE_PATH)
    baseline = load_json(BASELINE_PATH)
    admission = load_json(ADMISSION_PATH)
    g0_screen_values = load_indexed_values(G0_SCREENS_INDEX)
    g0_journey_values = load_indexed_values(G0_JOURNEYS_INDEX)

    admission_screens = admission["screens"]
    admission_journeys = admission["journeys"]
    intake_screens = intake["screens"]
    intake_by_id = {item["screen_id"]: (index, item) for index, item in enumerate(intake_screens)}
    g0_screen_by_id = {item["screen_id"]: item for _, item in g0_screen_values}
    g0_journey_by_id = {item["journey_id"]: item for _, item in g0_journey_values}

    screen_ids = [item["screen_id"] for item in admission_screens]
    journey_ids = [item["journey_id"] for item in admission_journeys]
    if set(screen_ids) != set(intake_by_id) or set(screen_ids) != set(g0_screen_by_id):
        raise ValueError("G0 screen indexes do not exact-cover intake and admission inventory")
    if set(journey_ids) != set(g0_journey_by_id):
        raise ValueError("G0 journey index does not exact-cover admission inventory")
    for screen_id in screen_ids:
        if g0_screen_by_id[screen_id] != intake_by_id[screen_id][1]:
            raise ValueError(f"G0 screen shard differs from intake for {screen_id}")

    exception_by_screen: dict[str, str] = {}
    for exception in baseline["exceptions"]:
        for screen_id in exception["screen_ids"]:
            if screen_id in exception_by_screen:
                raise ValueError(f"duplicate baseline exception for {screen_id}")
            exception_by_screen[screen_id] = exception["exception_id"]

    intake_hash = sha256(INTAKE_PATH)
    screen_entries = [
        assemble_screen_entry(
            admission_screen,
            admission_index,
            intake_by_id[admission_screen["screen_id"]][1],
            intake_by_id[admission_screen["screen_id"]][0],
            intake_hash,
            exception_by_screen,
        )
        for admission_index, admission_screen in enumerate(admission_screens)
    ]
    journey_entries = [
        assemble_journey_entry(
            admission_journey,
            admission_index,
            g0_journey_by_id[admission_journey["journey_id"]],
        )
        for admission_index, admission_journey in enumerate(admission_journeys)
    ]

    screens_index, screens_hash = write_shards(
        "screens", screen_entries, "screen_ref", "screen"
    )
    journeys_index, journeys_hash = write_shards(
        "journeys", journey_entries, "journey_ref", "journey"
    )

    for source in program["source_contracts"]:
        source_path = PROJECT_ROOT / source["path"]
        source["required_status"] = declared_status(source_path)

    program["validation_profile"] = "atlas_gate"
    program["scope"]["origin"] = {
        "kind": "product_contract",
        "ref": (
            ".codex/delivery/ui-design-programs/custometry-v2/"
            "evidence/g0/owner-intent.json#/scope"
        ),
    }
    program["screens"] = screen_entries
    program["journeys"] = journey_entries
    program["artifact_indexes"]["screens"] = {
        "path": screens_index.relative_to(PROJECT_ROOT).as_posix(),
        "sha256": screens_hash,
    }
    program["artifact_indexes"]["journeys"] = {
        "path": journeys_index.relative_to(PROJECT_ROOT).as_posix(),
        "sha256": journeys_hash,
    }
    write_json(PROGRAM_PATH, program)
    write_json(G1_DIR / "ui-design-program.snapshot.json", program)

    print(
        json.dumps(
            {
                "status": "passed",
                "screens": len(screen_entries),
                "journeys": len(journey_entries),
                "screens_index_sha256": screens_hash,
                "journeys_index_sha256": journeys_hash,
                "program_sha256": sha256(PROGRAM_PATH),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
