#!/usr/bin/env python3
"""Build the Custometry G1 atlas manifest from pinned authoritative sources.

This generator is intentionally limited to G1. It does not assign design
families, coverage profiles, waves, representatives, or responsive decisions.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR = Path(__file__).resolve().parent
PROGRAM_PATH = OUTPUT_DIR / "ui-design-program.json"
RECONCILIATION_PATH = OUTPUT_DIR / "g1-source-reconciliation.json"
OWNER_DECISION_JOURNAL_PATH = OUTPUT_DIR / "owner-decision-journal.json"
OWNER_DECISION_POINTER = "/iterations/0/owner_decision"

ROUTES_PATH = "packages/contracts/routes/ui-routes.json"
ROUTE_CONTRACTS_PATH = "packages/contracts/routes/ui-route-contracts.json"
SURFACES_PATH = "packages/contracts/routes/ui-surface-contracts.json"
TECHNICAL_BLUEPRINT_PATH = "custometry-technical-blueprint-ru.md"
HUMAN_BLUEPRINT_PATH = "custometry-technical-blueprint-human-ru.md"
UI_BLUEPRINT_PATH = "custometry-ui-blueprint-ru.md"

APP_PATH = "apps/web/src/App.tsx"
PILOT_TSX_PATH = "apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx"
PILOT_CSS_PATH = "apps/web/src/sales-overview-prototype/sales-overview-prototype.css"
MIGRATION_REGISTRY_PATH = "docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json"
DELIVERY_GRAPH_PATH = ".codex/delivery/graphs/custometry-linear-workspace-ui-transition-v1.json"
W10_EVIDENCE_PATH = ".codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md"
W20_EVIDENCE_PATH = ".codex/delivery/evidence/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md"
W27_EVIDENCE_PATH = ".codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md"
W28_RECEIPT_PATH = ".codex/delivery/evidence/assets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION/browser-reference-receipt.json"
PILOT_MANIFEST_PATH = "packages/contracts/ui-design/ui-an-003.manifest.v1.json"

G2_DEFERRED_REF = (
    "/Users/daniildegtyarev/.codex/skills/ui-design-program/"
    "references/stage-profiles-v1.md#G2-Journeys-And-Families"
)
RESPONSIVE_POLICY_REF = (
    "/Users/daniildegtyarev/.codex/skills/ui-design-program/"
    "references/responsive-policy-v1.md"
)


# G1 journey reconciliation only. These mappings project the normative journey
# order onto stable route/surface identities; they do not assign G2 families,
# coverage profiles, representatives, or waves.
JOURNEY_MAPPING_SPECS: dict[str, dict[str, Any]] = {
    "JOURNEY-001": {
        "entry_screen_ids": ["UI-AUTH-002"],
        "intermediate_screen_ids": ["UI-AUTH-005", "UI-SYS-003"],
        "alternate_screen_ids": [],
        "failure_screen_ids": ["UI-SYS-003"],
        "recovery_screen_ids": ["UI-AUTH-001"],
        "terminal_screen_ids": ["UI-CORE-001"],
        "external_boundary_ids": [],
        "edges": [
            ("UI-AUTH-002", "UI-AUTH-005", "forward", "requirements/0"),
            ("UI-AUTH-005", "UI-CORE-001", "terminal", "completion"),
            ("UI-AUTH-002", "UI-SYS-003", "failure", "requirements/0"),
            ("UI-AUTH-005", "UI-SYS-003", "failure", "requirements/3"),
            ("UI-SYS-003", "UI-AUTH-001", "recovery", "requirements/3"),
            ("UI-AUTH-001", "UI-AUTH-005", "forward", "requirements/3"),
        ],
    },
    "JOURNEY-002": {
        "entry_screen_ids": ["UI-DATA-001"],
        "intermediate_screen_ids": [
            "UI-DATA-002",
            "UI-DATA-004",
            "UI-DATA-005",
            "UI-DATA-008",
            "UI-DATA-009",
            "UI-DATA-010",
            "UI-DATA-013",
            "UI-DATA-014",
            "UI-DATA-006",
            "UI-DATA-020",
            "UI-DATA-012",
            "UI-DQ-004",
        ],
        "alternate_screen_ids": ["UI-DATA-026", "UI-DATA-027"],
        "failure_screen_ids": ["UI-DQ-005"],
        "recovery_screen_ids": ["UI-DQ-004"],
        "terminal_screen_ids": ["UI-DATA-011"],
        "external_boundary_ids": [],
        "edges": [
            ("UI-DATA-001", "UI-DATA-002", "forward", "steps/0"),
            ("UI-DATA-001", "UI-DATA-026", "alternate", "steps/0"),
            ("UI-DATA-026", "UI-DATA-027", "forward", "steps/0"),
            ("UI-DATA-027", "UI-DATA-004", "forward", "steps/1"),
            ("UI-DATA-002", "UI-DATA-004", "forward", "steps/1"),
            ("UI-DATA-004", "UI-DATA-005", "forward", "steps/1"),
            ("UI-DATA-005", "UI-DATA-008", "forward", "steps/2"),
            ("UI-DATA-008", "UI-DATA-009", "forward", "steps/3"),
            ("UI-DATA-009", "UI-DATA-010", "forward", "steps/3"),
            ("UI-DATA-010", "UI-DATA-013", "forward", "steps/3"),
            ("UI-DATA-013", "UI-DATA-014", "forward", "steps/3"),
            ("UI-DATA-014", "UI-DATA-006", "forward", "steps/4"),
            ("UI-DATA-006", "UI-DATA-020", "forward", "steps/5"),
            ("UI-DATA-020", "UI-DATA-012", "forward", "steps/5"),
            ("UI-DATA-012", "UI-DQ-004", "forward", "steps/6"),
            ("UI-DQ-004", "UI-DQ-005", "failure", "completion"),
            ("UI-DQ-005", "UI-DQ-004", "recovery", "completion"),
            ("UI-DQ-004", "UI-DATA-011", "terminal", "completion"),
        ],
    },
    "JOURNEY-003": {
        "entry_screen_ids": ["UI-DQ-005"],
        "intermediate_screen_ids": [
            "UI-DQ-004",
            "UI-OVR-024",
            "UI-OVR-011",
            "UI-OVR-010",
        ],
        "alternate_screen_ids": ["UI-DATA-008", "UI-DQ-003", "UI-OVR-008"],
        "failure_screen_ids": ["UI-DQ-005"],
        "recovery_screen_ids": ["UI-DQ-004"],
        "terminal_screen_ids": ["UI-DQ-001"],
        "external_boundary_ids": [],
        "edges": [
            ("UI-DQ-005", "UI-DQ-004", "recovery", "steps/0"),
            ("UI-DQ-004", "UI-DATA-008", "alternate", "steps/1"),
            ("UI-DQ-004", "UI-DQ-003", "alternate", "steps/1"),
            ("UI-DATA-008", "UI-OVR-024", "forward", "steps/2"),
            ("UI-DQ-003", "UI-OVR-024", "forward", "steps/2"),
            ("UI-DQ-005", "UI-OVR-008", "alternate", "steps/3"),
            ("UI-OVR-024", "UI-OVR-011", "forward", "steps/3"),
            ("UI-OVR-008", "UI-OVR-010", "forward", "steps/3"),
            ("UI-OVR-011", "UI-OVR-010", "forward", "steps/3"),
            ("UI-OVR-010", "UI-DQ-005", "failure", "steps/4"),
            ("UI-OVR-010", "UI-DQ-004", "recovery", "steps/4"),
            ("UI-DQ-004", "UI-DQ-001", "terminal", "completion"),
        ],
    },
    "JOURNEY-004": {
        "entry_screen_ids": ["UI-AN-001"],
        "intermediate_screen_ids": ["UI-AN-002", "UI-OVR-010", "UI-OVR-006"],
        "alternate_screen_ids": [
            "UI-DASH-003",
            "UI-ADMIN-018",
            "UI-PIPE-004",
            "UI-RPT-006",
        ],
        "failure_screen_ids": ["UI-AN-002"],
        "recovery_screen_ids": ["UI-OVR-010"],
        "terminal_screen_ids": ["UI-AN-012"],
        "external_boundary_ids": [],
        "edges": [
            ("UI-AN-001", "UI-AN-002", "forward", "steps/0"),
            ("UI-AN-002", "UI-OVR-010", "forward", "steps/1"),
            ("UI-OVR-010", "UI-AN-002", "failure", "steps/4"),
            ("UI-OVR-010", "UI-OVR-006", "forward", "steps/5"),
            ("UI-OVR-006", "UI-DASH-003", "alternate", "steps/6"),
            ("UI-OVR-006", "UI-ADMIN-018", "alternate", "steps/6"),
            ("UI-OVR-006", "UI-PIPE-004", "alternate", "steps/6"),
            ("UI-OVR-006", "UI-RPT-006", "alternate", "steps/6"),
            ("UI-OVR-006", "UI-AN-012", "terminal", "completion"),
            ("UI-DASH-003", "UI-AN-012", "terminal", "completion"),
            ("UI-ADMIN-018", "UI-AN-012", "terminal", "completion"),
            ("UI-PIPE-004", "UI-AN-012", "terminal", "completion"),
            ("UI-RPT-006", "UI-AN-012", "terminal", "completion"),
        ],
    },
    "JOURNEY-005": {
        "entry_screen_ids": ["UI-FCST-001"],
        "intermediate_screen_ids": [
            "UI-FCST-002",
            "UI-FCST-003",
            "UI-FCST-005",
            "UI-PIPE-004",
            "UI-FCST-006",
        ],
        "alternate_screen_ids": ["UI-FCST-007"],
        "failure_screen_ids": ["UI-FCST-002"],
        "recovery_screen_ids": ["UI-FCST-003"],
        "terminal_screen_ids": ["UI-FCST-004"],
        "external_boundary_ids": [],
        "edges": [
            ("UI-FCST-001", "UI-FCST-002", "forward", "steps/0"),
            ("UI-FCST-002", "UI-FCST-003", "recovery", "steps/1"),
            ("UI-FCST-003", "UI-FCST-002", "failure", "steps/0"),
            ("UI-FCST-003", "UI-FCST-005", "forward", "steps/2"),
            ("UI-FCST-005", "UI-PIPE-004", "forward", "steps/4"),
            ("UI-PIPE-004", "UI-FCST-006", "forward", "steps/4"),
            ("UI-FCST-006", "UI-FCST-007", "alternate", "steps/5"),
            ("UI-FCST-007", "UI-FCST-003", "recovery", "steps/5"),
            ("UI-FCST-006", "UI-FCST-004", "terminal", "completion"),
        ],
    },
    "JOURNEY-006": {
        "entry_screen_ids": ["UI-OPS-001"],
        "intermediate_screen_ids": [
            "UI-OPS-002",
            "UI-OVR-011",
            "UI-OVR-010",
            "UI-NOTIFY-001",
            "UI-OVR-016",
        ],
        "alternate_screen_ids": ["UI-PIPE-004", "UI-OPS-004"],
        "failure_screen_ids": ["UI-OPS-003"],
        "recovery_screen_ids": ["UI-OPS-002", "UI-OVR-010"],
        "terminal_screen_ids": ["UI-ADMIN-010"],
        "external_boundary_ids": [],
        "edges": [
            ("UI-OPS-001", "UI-OPS-002", "forward", "steps/0"),
            ("UI-OPS-001", "UI-PIPE-004", "alternate", "steps/0"),
            ("UI-PIPE-004", "UI-OPS-002", "forward", "steps/0"),
            ("UI-OPS-001", "UI-OPS-004", "alternate", "steps/0"),
            ("UI-OPS-004", "UI-OPS-002", "forward", "steps/0"),
            ("UI-OPS-002", "UI-OPS-003", "failure", "steps/1"),
            ("UI-OPS-003", "UI-OVR-011", "forward", "steps/2"),
            ("UI-OPS-002", "UI-OVR-011", "forward", "steps/2"),
            ("UI-OVR-011", "UI-OVR-010", "recovery", "steps/2"),
            ("UI-OVR-010", "UI-OPS-002", "recovery", "steps/3"),
            ("UI-OPS-002", "UI-NOTIFY-001", "forward", "steps/4"),
            ("UI-NOTIFY-001", "UI-OVR-016", "forward", "steps/4"),
            ("UI-OVR-016", "UI-ADMIN-010", "terminal", "completion"),
        ],
    },
    "JOURNEY-007": {
        "entry_screen_ids": ["UI-AN-013"],
        "intermediate_screen_ids": [
            "UI-DATA-021",
            "UI-DATA-022",
            "UI-DATA-011",
            "UI-DQ-004",
            "UI-AN-014",
            "UI-DATA-028",
            "UI-DATA-029",
            "UI-OVR-006",
            "UI-RPT-002",
            "UI-RPT-003",
            "UI-OVR-024",
        ],
        "alternate_screen_ids": ["UI-DASH-003", "UI-DASH-002", "UI-RPT-006"],
        "failure_screen_ids": ["UI-DQ-005"],
        "recovery_screen_ids": ["UI-DQ-004"],
        "terminal_screen_ids": ["UI-RPT-001"],
        "external_boundary_ids": [],
        "edges": [
            ("UI-AN-013", "UI-DATA-021", "forward", "steps/0"),
            ("UI-DATA-021", "UI-DATA-022", "forward", "steps/1"),
            ("UI-DATA-022", "UI-DATA-011", "forward", "steps/2"),
            ("UI-DATA-011", "UI-DQ-004", "forward", "steps/2"),
            ("UI-DQ-004", "UI-DQ-005", "failure", "steps/2"),
            ("UI-DQ-005", "UI-DQ-004", "recovery", "steps/2"),
            ("UI-DQ-004", "UI-AN-014", "forward", "steps/3"),
            ("UI-AN-014", "UI-DATA-028", "forward", "steps/4"),
            ("UI-DATA-028", "UI-DATA-029", "forward", "steps/4"),
            ("UI-DATA-029", "UI-OVR-006", "forward", "steps/5"),
            ("UI-OVR-006", "UI-RPT-002", "forward", "steps/5"),
            ("UI-RPT-002", "UI-RPT-003", "forward", "steps/5"),
            ("UI-RPT-002", "UI-DASH-003", "alternate", "steps/6"),
            ("UI-DASH-003", "UI-DASH-002", "forward", "steps/6"),
            ("UI-DASH-002", "UI-OVR-024", "forward", "steps/7"),
            ("UI-RPT-003", "UI-RPT-006", "alternate", "steps/6"),
            ("UI-RPT-006", "UI-OVR-024", "forward", "steps/7"),
            ("UI-RPT-003", "UI-OVR-024", "forward", "steps/7"),
            ("UI-OVR-024", "UI-RPT-001", "terminal", "completion"),
        ],
    },
}


def read_json(path: str) -> Any:
    return json.loads((PROJECT_ROOT / path).read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def accepted_program_value() -> dict[str, Any]:
    return {
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V1",
        "revision": 2,
    }


def owner_decision_ref() -> str | None:
    if not OWNER_DECISION_JOURNAL_PATH.is_file():
        return None
    journal = json.loads(OWNER_DECISION_JOURNAL_PATH.read_text(encoding="utf-8"))
    decision = journal["iterations"][0]["owner_decision"]
    accepted_value_hash = sha256_json(accepted_program_value())
    if (
        journal.get("program_id") != accepted_program_value()["program_id"]
        or decision.get("status") != "accepted"
        or decision.get("revision") != accepted_program_value()["revision"]
        or accepted_value_hash not in decision.get("accepted_value_sha256s", [])
    ):
        raise RuntimeError("Owner decision journal does not accept exact G1 revision 2")
    journal_path = str(OWNER_DECISION_JOURNAL_PATH.relative_to(PROJECT_ROOT))
    return (
        f"owner-decision://{sha256_path(OWNER_DECISION_JOURNAL_PATH)}/"
        f"{journal_path}?value_sha256={accepted_value_hash}"
        f"#{OWNER_DECISION_POINTER}"
    )


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def source_hashes(paths: list[str]) -> dict[str, str]:
    return {path: sha256_path(PROJECT_ROOT / path) for path in paths}


def parse_normative_journeys(
    surface_source_refs: dict[str, str],
) -> list[dict[str, Any]]:
    text = (PROJECT_ROOT / TECHNICAL_BLUEPRINT_PATH).read_text(encoding="utf-8")
    match = re.search(r"user_journeys:\n(?P<body>.*?)\n```", text, re.DOTALL)
    if match is None:
        raise RuntimeError("Cannot locate normative user_journeys block")

    journeys: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    collection: str | None = None
    for line in match.group("body").splitlines():
        id_match = re.match(r"  - id: (JOURNEY-\d{3})$", line)
        if id_match:
            if current is not None:
                journeys.append(current)
            current = {
                "journey_id": id_match.group(1),
                "name": None,
                "requirements": [],
                "steps": [],
                "completion": None,
            }
            collection = None
            continue
        if current is None:
            continue
        value_match = re.match(r"    (name|completion): (.+)$", line)
        if value_match:
            current[value_match.group(1)] = value_match.group(2)
            collection = None
            continue
        collection_match = re.match(r"    (requirements|steps):$", line)
        if collection_match:
            collection = collection_match.group(1)
            continue
        item_match = re.match(r"      - (.+)$", line)
        if item_match and collection is not None:
            current[collection].append(item_match.group(1))
    if current is not None:
        journeys.append(current)

    expected_ids = [f"JOURNEY-{index:03d}" for index in range(1, 8)]
    observed_ids = [journey["journey_id"] for journey in journeys]
    if observed_ids != expected_ids:
        raise RuntimeError(
            f"Normative journey identities differ: {observed_ids!r} != {expected_ids!r}"
        )

    for index, journey in enumerate(journeys):
        journey_id = journey["journey_id"]
        spec = JOURNEY_MAPPING_SPECS[journey_id]
        journey_ref = f"{TECHNICAL_BLUEPRINT_PATH}#user_journeys/{index}"
        node_ids = sorted(
            {
                screen_id
                for field in (
                    "entry_screen_ids",
                    "intermediate_screen_ids",
                    "alternate_screen_ids",
                    "failure_screen_ids",
                    "recovery_screen_ids",
                    "terminal_screen_ids",
                )
                for screen_id in spec[field]
            }
        )
        unknown_ids = sorted(set(node_ids) - set(surface_source_refs))
        if unknown_ids:
            raise RuntimeError(
                f"{journey_id} mapping references unknown surface IDs: {unknown_ids!r}"
            )

        transitions = []
        for transition_index, (from_id, to_id, outcome, basis) in enumerate(
            spec["edges"], start=1
        ):
            transition_id = f"{journey_id}-T{transition_index:03d}"
            transitions.append(
                {
                    "transition_id": transition_id,
                    "from_id": from_id,
                    "to_id": to_id,
                    "outcome": outcome,
                    "provenance": {
                        "kind": "derived_formula",
                        "formula": (
                            "Project the cited normative journey step onto the cited "
                            "stable product surfaces in user-observable order; encode "
                            f"the target role as outcome={outcome}."
                        ),
                        "source_refs": [
                            f"{journey_ref}/{basis}",
                            surface_source_refs[from_id],
                            surface_source_refs[to_id],
                        ],
                    },
                }
            )

        journey.update(
            {
                "source_ref": journey_ref,
                "mapping_revision": 1,
                "mapping_status": "source_backed_g1_reconciliation",
                "mapping_provenance": {
                    "kind": "derived_formula",
                    "formula": (
                        "Preserve the normative requirement/step/completion order and "
                        "bind each observable point to a stable route, overlay, or "
                        "system-surface identity. Repeated IDs indicate an explicit "
                        "failure/recovery loop, not a new screen."
                    ),
                    "source_refs": [journey_ref]
                    + [surface_source_refs[screen_id] for screen_id in node_ids],
                },
                "entry_screen_ids": spec["entry_screen_ids"],
                "intermediate_screen_ids": spec["intermediate_screen_ids"],
                "alternate_screen_ids": spec["alternate_screen_ids"],
                "failure_screen_ids": spec["failure_screen_ids"],
                "recovery_screen_ids": spec["recovery_screen_ids"],
                "terminal_screen_ids": spec["terminal_screen_ids"],
                "external_boundary_ids": spec["external_boundary_ids"],
                "external_boundary_provenance": {
                    "kind": "derived_formula",
                    "formula": (
                        "No external boundary is required because every normative "
                        "journey step and completion resolves to a registered Web UI "
                        "route, overlay, or system surface."
                    ),
                    "source_refs": [journey_ref]
                    + [surface_source_refs[screen_id] for screen_id in node_ids],
                },
                "transitions": transitions,
                "unresolved_fields": [],
            }
        )
    return journeys


def build_extension_screens(
    migration_registry: dict[str, Any], w28_receipt: dict[str, Any]
) -> list[dict[str, Any]]:
    shells = [
        {
            "id": shell_id,
            "name": f"Persistent shell profile: {shell_id}",
            "route": None,
            "profile_value": shell_id,
            "source_ref": f"{ROUTE_CONTRACTS_PATH}#/routes/*/shell_profile",
            "required_states": [],
        }
        for shell_id in ("auth", "global", "installation", "workspace")
    ]
    internal_surfaces = [
        {
            "id": "UI-AN-003?view=html-prototype",
            "name": "Sales Overview HTML prototype query surface",
            "route": "/w/northwind-retail/analytics/sales?view=html-prototype",
            "source_ref": f"{APP_PATH}#L196-L197",
            "implementation_refs": [PILOT_TSX_PATH, PILOT_CSS_PATH],
            "required_states": [],
        },
        {
            "id": "UI-AN-003?view=linear-spike",
            "name": "Sales Overview architecture-spike query surface",
            "route": "/w/northwind-retail/analytics/sales?view=linear-spike",
            "source_ref": f"{APP_PATH}#L196-L197",
            "evidence_ref": W20_EVIDENCE_PATH,
            "required_states": [],
        },
    ]
    historical = [
        {
            "id": Path(
                migration_registry["existing_authority"]["accepted_historical_evidence"]
            ).stem,
            "name": "Historical Penpot inventory evidence",
            "route": None,
            "source_ref": f"{MIGRATION_REGISTRY_PATH}#/existing_authority/accepted_historical_evidence",
            "historical_inventory": migration_registry["existing_authority"][
                "accepted_historical_inventory"
            ],
            "required_states": [],
        },
        {
            "id": migration_registry["clusters"][2]["ticket"],
            "name": "Historical contract-compiled Figma pilot",
            "route": None,
            "source_ref": f"{MIGRATION_REGISTRY_PATH}#/clusters/2",
            "state": migration_registry["clusters"][2]["state"],
            "required_states": [],
        },
        {
            "id": w28_receipt["ticket_id"],
            "name": "Superseded W28 Figma synchronization evidence",
            "route": None,
            "source_ref": f"{W28_RECEIPT_PATH}#/ticket_id",
            "required_states": [],
        },
    ]
    return shells + internal_surfaces + historical


def build_reconciliation() -> dict[str, Any]:
    routes_registry = read_json(ROUTES_PATH)
    route_contracts = read_json(ROUTE_CONTRACTS_PATH)
    surfaces = read_json(SURFACES_PATH)
    migration_registry = read_json(MIGRATION_REGISTRY_PATH)
    delivery_graph = read_json(DELIVERY_GRAPH_PATH)
    w28_receipt = read_json(W28_RECEIPT_PATH)

    route_ids = [route["id"] for route in routes_registry["routes"]]
    route_contract_ids = [route["id"] for route in route_contracts["routes"]]
    if len(route_ids) != 117 or len(set(route_ids)) != 117:
        raise RuntimeError("ui-routes.json must contain exactly 117 unique route IDs")
    if route_ids != route_contract_ids:
        raise RuntimeError("Route identity/order mismatch between route registries")

    overlay_ids = [surface["id"] for surface in surfaces["overlays"]]
    system_ids = [surface["id"] for surface in surfaces["system_surfaces"]]
    if overlay_ids != [f"UI-OVR-{index:03d}" for index in range(1, 26)]:
        raise RuntimeError("Overlay identity set is not UI-OVR-001...025")
    if system_ids != [f"UI-SYS-{index:03d}" for index in range(1, 6)]:
        raise RuntimeError("System identity set is not UI-SYS-001...005")

    use_case_bindings = copy.deepcopy(surfaces["use_case_bindings"])
    expected_use_cases = [f"UC-{index:03d}" for index in range(1, 30)]
    use_case_ids = [item["use_case_id"] for item in use_case_bindings]
    if use_case_ids != expected_use_cases:
        raise RuntimeError("Use-case identity set is not UC-001...029")
    for index, binding in enumerate(use_case_bindings):
        binding["source_ref"] = f"{SURFACES_PATH}#/use_case_bindings/{index}"

    known_surface_ids = set(route_ids + overlay_ids + system_ids)
    known_surface_ids.update(
        item["id"] for item in surfaces["cross_surface_capabilities"]
    )
    unknown_bound_ids = sorted(
        {
            surface_id
            for binding in use_case_bindings
            for surface_id in binding["surface_ids"]
            if surface_id not in known_surface_ids
        }
    )
    if unknown_bound_ids:
        raise RuntimeError(f"Use-case bindings contain unknown IDs: {unknown_bound_ids!r}")

    tracked_sources = [
        TECHNICAL_BLUEPRINT_PATH,
        HUMAN_BLUEPRINT_PATH,
        UI_BLUEPRINT_PATH,
        ROUTES_PATH,
        ROUTE_CONTRACTS_PATH,
        SURFACES_PATH,
        APP_PATH,
        PILOT_TSX_PATH,
        PILOT_CSS_PATH,
        MIGRATION_REGISTRY_PATH,
        DELIVERY_GRAPH_PATH,
        W10_EVIDENCE_PATH,
        W20_EVIDENCE_PATH,
        W27_EVIDENCE_PATH,
        W28_RECEIPT_PATH,
        PILOT_MANIFEST_PATH,
    ]
    hashes = source_hashes(tracked_sources)

    route_bindings = []
    for index, route in enumerate(route_contracts["routes"]):
        route_bindings.append(
            {
                "route_id": route["id"],
                "route_registry_ref": f"{ROUTES_PATH}#/routes/{index}",
                "route_contract_ref": f"{ROUTE_CONTRACTS_PATH}#/routes/{index}",
                "shell_profile": route["shell_profile"],
                "role_hints": route["role_hints"],
                "authorization": route["authorization"],
                "guard_profile": route["guard_profile"],
                "state_profile": route["state_profile"],
                "navigation_profile": route["navigation_profile"],
                "query_profile": route["query_profile"],
                "surface_kind": route["surface_kind"],
            }
        )

    surface_source_refs = {
        route_id: f"{ROUTE_CONTRACTS_PATH}#/routes/{index}"
        for index, route_id in enumerate(route_ids)
    }
    surface_source_refs.update(
        {
            overlay_id: f"{SURFACES_PATH}#/overlays/{index}"
            for index, overlay_id in enumerate(overlay_ids)
        }
    )
    surface_source_refs.update(
        {
            system_id: f"{SURFACES_PATH}#/system_surfaces/{index}"
            for index, system_id in enumerate(system_ids)
        }
    )

    return {
        "schema_id": "codex.custometry-ui-g1-source-reconciliation/v1",
        "stage": "G1",
        "authority_snapshot": hashes,
        "route_identity_reconciliation": {
            "ui_routes_count": len(route_ids),
            "ui_route_contracts_count": len(route_contract_ids),
            "ordered_identity_sets_equal": route_ids == route_contract_ids,
            "ordered_identity_set_sha256": sha256_json(route_ids),
            "ids": route_ids,
        },
        "surface_identity_reconciliation": {
            "overlay_count": len(overlay_ids),
            "system_surface_count": len(system_ids),
            "route_backed_overlay_ids": [
                item["id"] for item in surfaces["overlays"] if item["route_backed"]
            ],
            "overlay_ids": overlay_ids,
            "system_surface_ids": system_ids,
        },
        "extension_screens": build_extension_screens(
            migration_registry, w28_receipt
        ),
        "journeys": parse_normative_journeys(surface_source_refs),
        "use_case_binding_reconciliation": {
            "count": len(use_case_bindings),
            "ids": use_case_ids,
            "unknown_surface_ids": unknown_bound_ids,
            "bindings": use_case_bindings,
        },
        "role_permission_state_references": {
            "role_catalog_ref": f"{ROUTE_CONTRACTS_PATH}#/role_catalog",
            "role_catalog": route_contracts["role_catalog"],
            "permission_catalog_ref": f"{ROUTE_CONTRACTS_PATH}#/permission_catalog",
            "permission_catalog": route_contracts["permission_catalog"],
            "guard_profiles_ref": f"{ROUTE_CONTRACTS_PATH}#/profiles/guards",
            "state_profiles_ref": f"{ROUTE_CONTRACTS_PATH}#/profiles/states",
            "navigation_profiles_ref": f"{ROUTE_CONTRACTS_PATH}#/profiles/navigation",
            "query_profiles_ref": f"{ROUTE_CONTRACTS_PATH}#/profiles/queries",
            "route_bindings": route_bindings,
        },
        "pilot_baseline": {
            "screen_id": "UI-AN-003",
            "status": "measured_baseline",
            "accepted_visual": False,
            "accepted_visual_exclusion_reason": (
                "The owner record does not pin the exact current source revision."
            ),
            "route": "/w/northwind-retail/analytics/sales?view=html-prototype",
            "sources": [
                {"path": PILOT_TSX_PATH, "sha256": hashes[PILOT_TSX_PATH]},
                {"path": PILOT_CSS_PATH, "sha256": hashes[PILOT_CSS_PATH]},
            ],
            "desktop_screenshot": {
                "sha256": "be28cd5236ad1c92cf6c63c9fd8e74162e01a628b9b780ca6edac502d8284e0a",
                "evidence_ref": f"{W27_EVIDENCE_PATH}#browser-artifacts",
                "width": 1440,
                "height": 900,
            },
            "family_assignment": None,
            "component_family_assignment": None,
            "template_assignment": None,
        },
        "non_inventory_sources": [
            {
                "ref": PILOT_MANIFEST_PATH,
                "reason": "single-screen pilot manifest, not a product-wide inventory",
            },
            {
                "ref": "packages/contracts/ui-design/** component registry or component map",
                "reason": "component evidence cannot substitute for the all-screen atlas",
            },
            {
                "ref": "W21/W28 Figma artifacts",
                "reason": "historical or superseded visual evidence only",
            },
            {
                "ref": f"{MIGRATION_REGISTRY_PATH}#/existing_authority/accepted_historical_inventory",
                "reason": "historical Penpot 116/25/5 inventory is not current product inventory",
            },
            {
                "ref": next(
                    node["ticket"]
                    for node in delivery_graph["nodes"]
                    if node["ticket_id"] == "W29-HTML-FIRST-UI-FOUNDATION"
                ),
                "reason": "future ui-lab/component catalog is not an atlas source",
            },
            {
                "ref": "pilot screen map",
                "reason": "single-pilot mapping is not product-wide inventory",
            },
        ],
        "mobile_scope": "unauthorized",
        "proof_boundary": "static source reconciliation only",
    }


def null_assignment_origin() -> dict[str, str]:
    return {"kind": "normative_requirement", "ref": G2_DEFERRED_REF}


def screen_entry(
    *,
    path: str,
    pointer: str,
    expected_id: str,
    classification: str,
    classification_origin: dict[str, Any],
    disposition: str,
    disposition_origin: dict[str, Any],
    disposition_reason_ref: str | None = None,
    review_consequence: str | None = None,
    visual_baseline_ref: str | None = None,
) -> dict[str, Any]:
    return {
        "screen_ref": {
            "path": path,
            "json_pointer": pointer,
            "expected_id": expected_id,
        },
        "classification": classification,
        "classification_origin": classification_origin,
        "disposition": disposition,
        "disposition_origin": disposition_origin,
        "disposition_reason_ref": disposition_reason_ref,
        "review_consequence": review_consequence,
        "design_family_id": None,
        "family_assignment_origin": null_assignment_origin(),
        "wave_id": None,
        "wave_assignment_origin": null_assignment_origin(),
        "representative": False,
        "coverage_profile": None,
        "coverage_assignment_origin": null_assignment_origin(),
        "visual_baseline_ref": visual_baseline_ref,
        "unresolved_fields": [],
    }


def source_contract(
    path: str,
    authority: str,
    source_hash: str,
    *,
    screen_collections: list[dict[str, str]] | None = None,
    journey_collections: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return {
        "path": path,
        "authority": authority,
        "required_status": None,
        "sha256": source_hash,
        "screen_collections": screen_collections or [],
        "journey_collections": journey_collections or [],
    }


def build_program(reconciliation: dict[str, Any]) -> dict[str, Any]:
    routes_registry = read_json(ROUTES_PATH)
    route_contracts = read_json(ROUTE_CONTRACTS_PATH)
    surfaces = read_json(SURFACES_PATH)
    hashes = reconciliation["authority_snapshot"]
    reconciliation_path = str(RECONCILIATION_PATH.relative_to(PROJECT_ROOT))
    reconciliation_hash = sha256_path(RECONCILIATION_PATH)
    decision_ref = owner_decision_ref()

    screens: list[dict[str, Any]] = []
    for index, (route, contract) in enumerate(
        zip(routes_registry["routes"], route_contracts["routes"], strict=True)
    ):
        classification = (
            "route_flow" if contract["surface_kind"] == "wizard" else "route_screen"
        )
        screens.append(
            screen_entry(
                path=ROUTES_PATH,
                pointer=f"/routes/{index}",
                expected_id=route["id"],
                classification=classification,
                classification_origin={
                    "kind": "product_contract",
                    "ref": f"{ROUTE_CONTRACTS_PATH}#/routes/{index}/surface_kind",
                },
                disposition="in_scope",
                disposition_origin={
                    "kind": "product_contract",
                    "ref": f"{ROUTES_PATH}#/routes/{index}",
                },
                visual_baseline_ref=(
                    f"{reconciliation_path}#/pilot_baseline"
                    if route["id"] == "UI-AN-003"
                    else None
                ),
            )
        )

    for index, overlay in enumerate(surfaces["overlays"]):
        route_backed = overlay["id"] == "UI-OVR-020"
        screens.append(
            screen_entry(
                path=SURFACES_PATH,
                pointer=f"/overlays/{index}",
                expected_id=overlay["id"],
                classification=(
                    "route_backed_transient" if route_backed else "overlay"
                ),
                classification_origin={
                    "kind": "product_contract",
                    "ref": f"{SURFACES_PATH}#/overlays/{index}",
                },
                disposition="in_scope",
                disposition_origin={
                    "kind": "product_contract",
                    "ref": f"{SURFACES_PATH}#/overlays/{index}",
                },
            )
        )

    for index, system in enumerate(surfaces["system_surfaces"]):
        screens.append(
            screen_entry(
                path=SURFACES_PATH,
                pointer=f"/system_surfaces/{index}",
                expected_id=system["id"],
                classification="system_state_family",
                classification_origin={
                    "kind": "product_contract",
                    "ref": f"{SURFACES_PATH}#/system_surfaces/{index}",
                },
                disposition="in_scope",
                disposition_origin={
                    "kind": "product_contract",
                    "ref": f"{SURFACES_PATH}#/system_surfaces/{index}",
                },
            )
        )

    extension_screens = reconciliation["extension_screens"]
    for index, extension in enumerate(extension_screens):
        if index < 4:
            classification = "persistent_shell"
            disposition = "in_scope"
            origin = {
                "kind": "product_contract",
                "ref": f"{ROUTE_CONTRACTS_PATH}#/routes/*/shell_profile?value={extension['id']}",
            }
            reason = None
            consequence = None
            baseline_ref = None
        elif index < 6:
            classification = "internal_or_non_visual"
            disposition = "internal"
            origin = {
                "kind": "measured_baseline",
                "ref": extension["source_ref"],
                "locator": "selectedView query gate",
                "property": "query-gated internal surface identity",
            }
            reason = extension["source_ref"]
            consequence = "Retain as internal QA coverage; do not count as a product route."
            baseline_ref = (
                f"{reconciliation_path}#/pilot_baseline" if index == 4 else None
            )
        else:
            classification = "historical_exclusion"
            disposition = "excluded"
            origin = {
                "kind": "normative_requirement",
                "ref": extension["source_ref"],
            }
            reason = extension["source_ref"]
            consequence = (
                "Preserve provenance history only; exclude from active atlas source counts."
            )
            baseline_ref = None
        screens.append(
            screen_entry(
                path=reconciliation_path,
                pointer=f"/extension_screens/{index}",
                expected_id=extension["id"],
                classification=classification,
                classification_origin=origin,
                disposition=disposition,
                disposition_origin=origin,
                disposition_reason_ref=reason,
                review_consequence=consequence,
                visual_baseline_ref=baseline_ref,
            )
        )

    journeys = []
    for index, journey in enumerate(reconciliation["journeys"]):
        transitions = [
            {
                "transition_ref": {
                    "path": reconciliation_path,
                    "json_pointer": (
                        f"/journeys/{index}/transitions/{transition_index}"
                    ),
                    "expected_id": transition["transition_id"],
                },
                "from_id": transition["from_id"],
                "to_id": transition["to_id"],
                "outcome": transition["outcome"],
            }
            for transition_index, transition in enumerate(journey["transitions"])
        ]
        journeys.append(
            {
                "journey_ref": {
                    "path": reconciliation_path,
                    "json_pointer": f"/journeys/{index}",
                    "expected_id": journey["journey_id"],
                },
                "entry_screen_ids": journey["entry_screen_ids"],
                "intermediate_screen_ids": journey["intermediate_screen_ids"],
                "alternate_screen_ids": journey["alternate_screen_ids"],
                "failure_screen_ids": journey["failure_screen_ids"],
                "recovery_screen_ids": journey["recovery_screen_ids"],
                "terminal_screen_ids": journey["terminal_screen_ids"],
                "external_boundary_ids": journey["external_boundary_ids"],
                "transitions": transitions,
                "unresolved_fields": journey["unresolved_fields"],
            }
        )

    counts = {
        "route_screens": sum(
            item["classification"] == "route_screen" for item in screens
        ),
        "route_flows": sum(
            item["classification"] == "route_flow" for item in screens
        ),
        "persistent_shells": sum(
            item["classification"] == "persistent_shell" for item in screens
        ),
        "route_backed_transients": sum(
            item["classification"] == "route_backed_transient" for item in screens
        ),
        "overlays": sum(item["classification"] == "overlay" for item in screens),
        "system_state_families": sum(
            item["classification"] == "system_state_family" for item in screens
        ),
        "internal_or_non_visual": sum(
            item["classification"] == "internal_or_non_visual" for item in screens
        ),
        "historical_exclusions": sum(
            item["classification"] == "historical_exclusion" for item in screens
        ),
    }
    counts["total"] = len(screens)
    counts["journeys"] = len(journeys)

    source_contracts = [
        source_contract(
            TECHNICAL_BLUEPRINT_PATH,
            "normative product specification and JOURNEY-001...007",
            hashes[TECHNICAL_BLUEPRINT_PATH],
        ),
        source_contract(
            HUMAN_BLUEPRINT_PATH,
            "required explanatory mirror",
            hashes[HUMAN_BLUEPRINT_PATH],
        ),
        source_contract(
            UI_BLUEPRINT_PATH,
            "normative UI/UX requirements and historical exclusions",
            hashes[UI_BLUEPRINT_PATH],
        ),
        source_contract(
            ROUTES_PATH,
            "current stable product route identities",
            hashes[ROUTES_PATH],
            screen_collections=[{"json_pointer": "/routes", "id_key": "id"}],
        ),
        source_contract(
            ROUTE_CONTRACTS_PATH,
            "route roles permissions state shell and query profiles",
            hashes[ROUTE_CONTRACTS_PATH],
        ),
        source_contract(
            SURFACES_PATH,
            "overlay system-surface capability and use-case bindings",
            hashes[SURFACES_PATH],
            screen_collections=[
                {"json_pointer": "/overlays", "id_key": "id"},
                {"json_pointer": "/system_surfaces", "id_key": "id"},
            ],
        ),
    ]
    extra_authorities = {
        APP_PATH: "observed query-gated internal surface implementation",
        PILOT_TSX_PATH: "UI-AN-003 measured baseline implementation source",
        PILOT_CSS_PATH: "UI-AN-003 measured baseline style source",
        MIGRATION_REGISTRY_PATH: "current HTML-first transition and historical policy",
        DELIVERY_GRAPH_PATH: "current UI transition topology and W29 identity",
        W10_EVIDENCE_PATH: "immutable historical Penpot evidence",
        W20_EVIDENCE_PATH: "observed architecture-spike internal surface evidence",
        W27_EVIDENCE_PATH: "observed HTML pilot evidence without exact source-revision acceptance pin",
        W28_RECEIPT_PATH: "historical/superseded browser-to-Figma evidence identity",
        PILOT_MANIFEST_PATH: "single-screen pilot manifest explicitly excluded from product-wide inventory",
    }
    source_contracts.extend(
        source_contract(path, authority, hashes[path])
        for path, authority in extra_authorities.items()
    )
    source_contracts.append(
        source_contract(
            reconciliation_path,
            "derived G1 normalization; upstream refs remain authoritative",
            reconciliation_hash,
            screen_collections=[
                {"json_pointer": "/extension_screens", "id_key": "id"}
            ],
            journey_collections=[
                {"json_pointer": "/journeys", "id_key": "journey_id"}
            ],
        )
    )

    initialized = json.loads(PROGRAM_PATH.read_text(encoding="utf-8"))
    initialized.update(
        {
            "revision": 2,
            "status": "accepted" if decision_ref else "review",
            "validation_profile": "atlas_gate",
            "source_contracts": source_contracts,
            "scope": {
                "product": "Custometry",
                "platform": "web",
                "included_release_slices": ["FOUNDATION", "MVP", "MVP/V1", "V1"],
                "excluded_release_slices": [
                    "post-v1 product UI absent from the authoritative 117-route registry"
                ],
                "origin": {
                    "kind": "normative_requirement",
                    "ref": ".codex/AGENTS.md#Project-Sources",
                },
            },
            "expected_inventory": counts,
            "screens": screens,
            "journeys": journeys,
            "coverage_profiles": [],
            "families": [],
            "waves": [],
            "responsive_policy": {
                "adaptive_web_required": True,
                "supported_web_width_range": {
                    "min_width": None,
                    "max_width": None,
                    "origin": {
                        "kind": "normative_requirement",
                        "ref": f"{RESPONSIVE_POLICY_REF}#Responsive-Web-Requirement",
                    },
                },
                "anchor_viewports": [],
                "breakpoint_policy": "content_driven",
                "breakpoint_policy_origin": {
                    "kind": "normative_requirement",
                    "ref": f"{RESPONSIVE_POLICY_REF}#Breakpoints-And-Components",
                },
                "component_adaptation": "prefer_container_queries",
                "component_adaptation_origin": {
                    "kind": "normative_requirement",
                    "ref": f"{RESPONSIVE_POLICY_REF}#Breakpoints-And-Components",
                },
                "logical_properties_required": True,
                "logical_properties_origin": {
                    "kind": "normative_requirement",
                    "ref": f"{RESPONSIVE_POLICY_REF}#Breakpoints-And-Components",
                },
                "mobile_scope": "unauthorized",
                "mobile_scope_origin": {
                    "kind": "normative_requirement",
                    "ref": f"{RESPONSIVE_POLICY_REF}#Mobile-Authorization-Boundary",
                },
                "mobile_authorization_ref": None,
                "authorized_mobile_surfaces": [],
                "authorized_mobile_viewports": [],
                "allowed_mobile_changes": [],
            },
            "program_acceptance": {
                "agent_self_acceptance": "prohibited",
                "owner_decision_ref": decision_ref,
                "accepted_revision": 2 if decision_ref else None,
            },
        }
    )
    return initialized


def main() -> int:
    reconciliation = build_reconciliation()
    write_json(RECONCILIATION_PATH, reconciliation)
    program = build_program(reconciliation)
    write_json(PROGRAM_PATH, program)
    print(
        json.dumps(
            {
                "status": "generated",
                "stage": "G1",
                "program": str(PROGRAM_PATH),
                "reconciliation": str(RECONCILIATION_PATH),
                "expected_inventory": program["expected_inventory"],
                "journey_unresolved_count": sum(
                    bool(item["unresolved_fields"]) for item in program["journeys"]
                ),
                "mobile_scope": program["responsive_policy"]["mobile_scope"],
                "families": len(program["families"]),
                "waves": len(program["waves"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
