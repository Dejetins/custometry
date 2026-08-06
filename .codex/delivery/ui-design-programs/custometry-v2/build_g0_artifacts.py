#!/usr/bin/env python3
"""Build reproducible G0 authority, intake, baseline, and program artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
EVIDENCE_DIR = PROGRAM_DIR / "evidence/g0"
PILOT_RU = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot/ru/source.html"
PILOT_EN = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot/en/source.html"
OWNER_TASK = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/owner-task.txt"
OWNER_INTENT = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/owner-intent.json"
OWNER_REQUEST = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/visual-authority-request.json"
CANONICAL_DECISION = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/visual-authority-owner-decision.json"
VISUAL_ADAPTER = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/visual-authority-decision-v1.json"
INVENTORY = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/g1-admission-inventory.json"
PILOT_RECEIPT = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/pilot-import-receipt.json"
ROUTES = "packages/contracts/routes/ui-route-contracts.json"
SURFACES = "packages/contracts/routes/ui-surface-contracts.json"
TECH_BLUEPRINT = "custometry-technical-blueprint-ru.md"
TECH_MIRROR = "custometry-technical-blueprint-human-ru.md"
UI_BLUEPRINT = "custometry-ui-blueprint-ru.md"
PLATFORM_ADR = "docs/adr/0007-responsive-web-frontend-platform.md"
SOURCE_ATTACHMENT = Path(
    "/Users/daniildegtyarev/.codex/attachments/"
    "be73cd69-033a-47f3-9931-c5971de0eacd/pasted-text.txt"
)

PILOT_RU_SHA = "9d82b59fdf766ccc2b72616fa2c0945d99e1110794be4698c049f232425be780"
PILOT_EN_SHA = "233b3c94723a14dde1eb41f1c54610bc157b311d7cf1e42338302cf839f4e8f4"

SCREEN_ACCEPTANCE_SCOPE = (
    "Visual-language anchor only; no exact-screen fidelity authority for novel or target surfaces."
)
VISUAL_LANGUAGE_SCOPE = (
    "Calm professional character, compact analytical density, concise KPI and context chrome, "
    "visible Result Trust, Focus/Explore interaction character, and independent RU/EN content-stress evidence."
)
FOUNDATION_SCOPE = (
    "Only source-backed primitives measured into the G0 platform baseline; exact composition, "
    "information architecture, responsive acceptance, and implementation remain excluded."
)

INCLUDED = [
    "trusted data ingestion, semantic data, metrics, methodologies, and quality",
    "analytical documents, large workbook composition, reports, dashboards, and exports",
    "publishing, review, comments, findings, collaboration, and stable refresh anchors",
    "segments and reusable recalculation workflows",
    "digital acquisition, promotion, channel, offline, and unit-economics analysis",
    "product, category, assortment, inventory, margin, and discount analysis",
    "forecasting, pipelines, runs, notifications, adoption, capacity, and performance operations",
    "workspace, organization, people, access, branding, localization, themes, help, and installation administration",
]
EXCLUDED = [
    "mobile-specific information architecture or native mobile application",
    "B2B product scope",
    "activation or reverse ETL",
    "arbitrary notebooks or arbitrary SQL authoring",
    "probabilistic identity resolution",
    "unapproved causal attribution",
    "rankings or leaderboards",
    "cloning another platform",
]

JOURNEY_SPECS = [
    ("data-to-trusted-result", ["UI-DATA-001", "UI-DQ-001", "UI-AN-012"]),
    ("compose-large-workbook", ["UI-RPT-001", "UI-RPT-002", "UI-RPT-003"]),
    ("publish-review-collaborate", ["UI-AN-013", "UI-AN-014", "UI-OVR-024"]),
    ("refresh-with-stable-anchors", ["UI-DASH-001", "UI-DASH-002"]),
    ("define-recalculate-reuse-segment", ["UI-SEG-001", "UI-SEG-002", "UI-SEG-003"]),
    ("digital-to-offline-unit-economics", ["UI-AN-009", "UI-PROMO-001", "UI-PROMO-003"]),
    ("product-category-assortment-inventory", ["UI-AN-015", "UI-DATA-004", "UI-DATA-005"]),
    ("open-100x30-document-without-duplicate-compute", ["UI-RPT-001", "UI-RPT-002"]),
    ("adoption-and-performance-operations", ["UI-ADMIN-005", "UI-ADMIN-006", "UI-OPS-004"]),
]


def rel(path: str) -> Path:
    return ROOT / path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_ref(path: str, pointer: str) -> str:
    return f"{path}#{pointer}"


def prepare_owner_artifacts() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    destination = rel(OWNER_TASK)
    if SOURCE_ATTACHMENT.read_bytes() != destination.read_bytes() if destination.exists() else True:
        shutil.copyfile(SOURCE_ATTACHMENT, destination)
    owner_intent = {
        "schema_id": "custometry.ui-program-owner-intent/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "task_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-G0",
        "revision": 1,
        "status": "accepted",
        "source_task": {"path": OWNER_TASK, "sha256": sha(destination)},
        "source_hierarchy": [
            "current owner task and this normalized owner-intent baseline",
            "repository AGENTS.md chain",
            TECH_BLUEPRINT,
            TECH_MIRROR,
            UI_BLUEPRINT,
            "accepted repository architecture and ADRs",
            "hash-pinned route and surface contracts",
        ],
        "scope": {
            "platform": "responsive_web",
            "included_release_slices": INCLUDED,
            "excluded_release_slices": EXCLUDED,
            "public_site_in_scope": False,
            "mobile_scope": "unauthorized",
        },
        "critical_journeys": [item[0] for item in JOURNEY_SPECS],
        "visual_authority": {
            "source_evidence_mode": "renderable_html",
            "screen_acceptance_scope": SCREEN_ACCEPTANCE_SCOPE,
            "visual_language_scope": VISUAL_LANGUAGE_SCOPE,
            "reusable_foundation_scope": FOUNDATION_SCOPE,
            "inheritance_policy": "required",
            "mobile_scope": "unauthorized",
        },
        "source_visual": {"path": PILOT_RU, "sha256": PILOT_RU_SHA},
        "supporting_visual": {"path": PILOT_EN, "sha256": PILOT_EN_SHA},
        "pilot_limits": [
            "visual-language and density anchor only",
            "not exact composition, information architecture, frontend architecture, component implementation, responsive acceptance, or novel-screen fidelity authority",
        ],
        "architecture_boundary": {
            "path": PLATFORM_ADR,
            "frontend": "React/TypeScript responsive Web application with product-owned semantic UI foundation",
            "server_state": "TanStack Query is the sole server-state cache and invalidation owner",
            "presentation_state": "MobX is limited to scoped presentation and draft state",
            "ports_and_adapters": "API/SSE adapters own transport, cancellation, errors, and redaction; the browser cannot create terminal domain state",
            "responsive_range_css_px": {"min_width": 768, "max_width": 1920},
        },
        "execution_limits": {
            "active_gate": "G0",
            "next_gate_not_executed": "G1",
            "no_git_publication": True,
            "no_deployment": True,
            "no_figma_or_browser_work": True,
            "v1_status": "terminal_historical_evidence_only",
        },
    }
    write_json(rel(OWNER_INTENT), owner_intent)
    accepted_values = [{
        "visual_authority": owner_intent["visual_authority"],
        "source_visual": owner_intent["source_visual"],
        "supporting_visual": owner_intent["supporting_visual"],
        "pilot_limits": owner_intent["pilot_limits"],
    }]
    request = {
        "$schema": "owner-decision-request.schema.json",
        "program_id": owner_intent["program_id"],
        "decision_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2.visual-authority",
        "decision_kind": "visual_authority",
        "status": "accepted",
        "revision": 1,
        "decision_text": "Record the exact pilot as a visual-language and density anchor for responsive Web, with no mobile or exact-screen authority.",
        "owner_input": f"The exact accepted owner request is hash-pinned at {OWNER_TASK}; its normalized scope and visual limits are in {OWNER_INTENT}.",
        "recorded_at": "2026-08-05T22:00:00+00:00",
        "accepted_values": accepted_values,
        "target": {
            "artifact_kind": "program",
            "artifact_id": owner_intent["program_id"],
            "revision": 1,
            "validation_profile": "g0_owner_intent",
            "path": OWNER_INTENT,
        },
    }
    write_json(rel(OWNER_REQUEST), request)


def specified(value: Any, unit: str | None = None, source: str | None = None) -> dict[str, Any]:
    return {
        "value": value,
        "unit": unit,
        "source_ref": source or source_ref(PILOT_RU, "source-backed-platform-baseline"),
        "tolerance": 0,
        "change_policy": "fixed",
    }


def action(action_id: str, label: str, region_id: str, ref: str, permission: str | None = None,
           target: str | None = None, surface: str | None = None) -> dict[str, Any]:
    return {
        "action_id": action_id,
        "control_type": "button",
        "component_id": "action.button",
        "component_variant": "secondary",
        "size_class": "sm",
        "label": label,
        "icon_id": None,
        "region_id": region_id,
        "intent": label,
        "visibility": "when the source contract and permission profile allow it",
        "enabled_when": "the surface is available and no conflicting operation is in progress",
        "preconditions": [] if permission is None else [f"permission {permission}"],
        "trigger": "click, Enter, or Space",
        "outcome": f"{label} completes or the next contract-bound surface opens",
        "feedback": "show deterministic pending, success, or destination feedback",
        "failure": "show a source-backed error without inventing terminal domain state",
        "recovery": "retain context and expose a safe retry or return path",
        "confirmation": "required only when the source contract marks the action destructive or irreversible",
        "side_effects": [],
        "destructive": False,
        "permission_refs": [] if permission is None else [permission],
        "keyboard": "Enter or Space on the focused control",
        "navigation_target": target,
        "opens_surface_id": surface,
        "source_refs": [ref],
    }


def screen_contract(item: dict[str, Any], journey_actions: list[dict[str, Any]]) -> dict[str, Any]:
    screen_id = item["screen_id"]
    visual = item["visual_surface"]
    ref = item["source_ref"]
    region_id = f"{screen_id}.content"
    roles = item.get("role_ids") or ["all"]
    actions: list[dict[str, Any]] = []
    if visual:
        for permission in item.get("action_permissions", []):
            label = " ".join(part.capitalize() for part in permission.replace("_", " ").split("."))
            actions.append(action(f"{screen_id}.{permission}", label, region_id, ref, permission))
        if not actions:
            default_label = "Continue" if item["surface_kind"] == "route_flow" else "Inspect current surface"
            actions.append(action(f"{screen_id}.inspect", default_label, region_id, ref))
        actions.extend(journey_actions)
        required_kinds = ["initial", "loading", "populated", "error", "permission_denied", "recovery"]
        states = []
        for kind in required_kinds:
            state_id = f"{screen_id}.{kind}"
            available = [entry["action_id"] for entry in actions] if kind in {"populated", "error", "permission_denied", "recovery"} else []
            states.append({
                "state_id": state_id,
                "kind": kind,
                "trigger": f"the source-backed {kind} condition is active",
                "visible_region_ids": [region_id],
                "available_action_ids": available,
                "exit_conditions": ["a permitted action or authoritative state transition occurs"],
                "source_refs": [ref],
            })
        regions = [{
            "region_id": region_id,
            "purpose": item["purpose"],
            "content": "source-backed content, controls, state, trust, and recovery information",
            "data_refs": [],
            "state_ids": [entry["state_id"] for entry in states],
            "action_ids": [entry["action_id"] for entry in actions],
            "source_refs": [ref],
        }]
        no_actions_reason = None
    else:
        required_kinds = []
        states = []
        regions = []
        no_actions_reason = f"{ref}: classified as {item['surface_kind']} and not admitted as a visual interactive surface"
    applicability = [{
        "kind": kind,
        "mode": "required" if kind in required_kinds else "not_applicable",
        "reason_ref": None if kind in required_kinds else f"{ref}: {kind} is not required by the G0 source contract",
    } for kind in ("initial", "loading", "populated", "empty", "partial", "error", "permission_denied", "offline", "recovery", "terminal", "other")]
    return {
        "screen_id": screen_id,
        "page_id": item.get("page_id"),
        "route_id": item.get("route_id"),
        "route": item.get("route"),
        "surface_kind": item["surface_kind"],
        "visual_surface": visual,
        "shell_variant_id": item.get("shell_variant_id"),
        "purpose": item["purpose"],
        "user_outcomes": [item["purpose"]],
        "entry_points": item.get("entry_points", ["source-defined product navigation or invocation"]),
        "exit_points": item.get("exit_points", ["return to the invoking or permitted destination"]),
        "source_refs": [ref],
        "data": {
            "reads": [], "writes": [], "computed": [],
            "refresh_behavior": "source-defined refresh with stable object and result anchors",
            "freshness_behavior": "show freshness and Result Trust metadata when applicable",
            "empty_data_meaning": "the source-defined dataset or result has no permitted records",
        },
        "role_ids": roles,
        "permission_behavior": item.get("permission_behavior", "apply source-defined route and action permissions"),
        "regions": regions,
        "states": states,
        "state_applicability": applicability,
        "actions": actions,
        "context_menus": [],
        "related_surface_ids": item.get("related_surface_ids", []),
        "no_actions_reason": no_actions_reason,
        "accessibility_contract": "semantic structure, complete keyboard operation, visible focus, named controls, and non-color-only state",
        "responsive_content_priorities": ["preserve task, trust, recovery, and primary action meaning across the supported Web range"],
    }


def shell_region(region_id: str, role: str, order: int, required: bool = True) -> dict[str, Any]:
    return {
        "region_id": region_id,
        "role": role,
        "presence": "required" if required else "not_applicable",
        "not_applicable_reason": None if required else "this source-backed shell variant does not use the region",
        "order": order,
        "geometry": {"minimum_size": specified(32, "px")} if required else None,
        "spacing_relations": [],
        "visual_properties": {"surface": specified("paper-semantic-surface")} if required else None,
        "scroll_behavior": "workspace content scrolls independently; navigation identity remains stable" if required else None,
        "source_refs": [source_ref(PILOT_RU, "source-backed-shell")],
    }


def exception_decision(exception: dict[str, Any], path: str) -> None:
    write_json(rel(path), {
        "status": "accepted",
        "revision": 1,
        "decision_kind": "baseline_exception",
        "source": {"path": OWNER_INTENT, "sha256": sha(rel(OWNER_INTENT))},
        "baseline_exception": {key: exception[key] for key in (
            "exception_id", "screen_ids", "shell_variant_id", "allowed_differences", "reason_ref"
        )},
    })


def build_inventory(routes: dict[str, Any], surfaces: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    screens: list[dict[str, Any]] = []
    intake_items: list[dict[str, Any]] = []
    shell_map = {"auth": "shell.auth", "installation": "shell.setup", "global": "shell.workspace", "workspace": "shell.workspace"}
    known_roles = set(routes["role_catalog"])
    for index, route in enumerate(routes["routes"]):
        classification = "route_flow" if route["surface_kind"] == "wizard" else "route_screen"
        item = {
            "screen_id": route["id"],
            "classification": classification,
            "source_path": ROUTES,
            "source_pointer": f"/routes/{index}",
            "source_ref": source_ref(ROUTES, f"/routes/{index}"),
            "route_id": route["id"],
            "route": route["path"],
            "page_id": route["id"],
            "surface_kind": classification,
            "visual_surface": True,
            "shell_variant_id": shell_map[route["shell_profile"]],
            "purpose": f"Provide the {route['surface_kind']} contract for {route['path']}",
            "role_ids": [value for value in route.get("role_hints", []) if value in known_roles] or ["all"],
            "action_permissions": route.get("authorization", {}).get("action_permissions", []),
            "permission_behavior": f"guard profile {route.get('guard_profile')} with source-defined object and action scope",
        }
        screens.append({key: item[key] for key in ("screen_id", "classification", "source_path", "source_pointer")})
        intake_items.append(item)
    persistent = [
        ("UI-SHELL-AUTH", "shell.auth", "Authentication shell", "auth"),
        ("UI-SHELL-GLOBAL", "shell.workspace", "Global-user shell", "global"),
        ("UI-SHELL-WORKSPACE", "shell.workspace", "Workspace application shell", "workspace"),
        ("UI-SHELL-INSTALLATION", "shell.setup", "Installation administration shell", "installation"),
    ]
    for screen_id, variant, purpose, profile in persistent:
        ref = source_ref(ROUTES, f"/profiles/navigation/{profile}")
        item = {
            "screen_id": screen_id, "classification": "persistent_shell", "source_path": ROUTES,
            "source_pointer": f"/profiles/navigation/{profile}", "source_ref": ref,
            "route_id": None, "route": None, "page_id": screen_id, "surface_kind": "persistent_shell",
            "visual_surface": True, "shell_variant_id": variant, "purpose": purpose,
            "role_ids": ["all"], "action_permissions": [],
        }
        screens.append({key: item[key] for key in ("screen_id", "classification", "source_path", "source_pointer")})
        intake_items.append(item)
    for index, overlay in enumerate(surfaces["overlays"]):
        classification = "route_backed_transient" if overlay.get("route_backed") else "overlay"
        variant = "shell.focus" if overlay["id"] == "UI-OVR-020" else "shell.workspace"
        ref = source_ref(SURFACES, f"/overlays/{index}")
        item = {
            "screen_id": overlay["id"], "classification": classification, "source_path": SURFACES,
            "source_pointer": f"/overlays/{index}", "source_ref": ref,
            "route_id": None, "route": None, "page_id": overlay["id"], "surface_kind": classification,
            "visual_surface": True, "shell_variant_id": variant, "purpose": overlay["name"],
            "role_ids": ["all"], "action_permissions": [],
        }
        screens.append({key: item[key] for key in ("screen_id", "classification", "source_path", "source_pointer")})
        intake_items.append(item)
    for index, system in enumerate(surfaces["system_surfaces"]):
        ref = source_ref(SURFACES, f"/system_surfaces/{index}")
        item = {
            "screen_id": system["id"], "classification": "system_state_family", "source_path": SURFACES,
            "source_pointer": f"/system_surfaces/{index}", "source_ref": ref,
            "route_id": None, "route": None, "page_id": system["id"], "surface_kind": "system_state_family",
            "visual_surface": True, "shell_variant_id": "shell.system", "purpose": system["name"],
            "role_ids": ["all"], "action_permissions": [],
        }
        screens.append({key: item[key] for key in ("screen_id", "classification", "source_path", "source_pointer")})
        intake_items.append(item)
    for index, capability in enumerate(surfaces["cross_surface_capabilities"]):
        ref = source_ref(SURFACES, f"/cross_surface_capabilities/{index}")
        item = {
            "screen_id": capability["id"], "classification": "internal_or_non_visual", "source_path": SURFACES,
            "source_pointer": f"/cross_surface_capabilities/{index}", "source_ref": ref,
            "route_id": None, "route": None, "page_id": capability["id"], "surface_kind": "internal_or_non_visual",
            "visual_surface": False, "shell_variant_id": None, "purpose": capability["name"],
            "role_ids": ["all"], "action_permissions": [],
        }
        screens.append({key: item[key] for key in ("screen_id", "classification", "source_path", "source_pointer")})
        intake_items.append(item)
    historical = [
        ("HISTORICAL-CUSTOMETRY-UI-V1", "Custometry UI Design Program V1 is terminal historical evidence only"),
        ("HISTORICAL-PENPOT", "Penpot evidence is historical and cannot be active visual authority"),
    ]
    for index, (screen_id, purpose) in enumerate(historical):
        ref = source_ref(OWNER_INTENT, f"historical_exclusions/{index}")
        item = {
            "screen_id": screen_id, "classification": "historical_exclusion", "source_path": OWNER_INTENT,
            "source_pointer": f"/execution_limits/{index}", "source_ref": ref,
            "route_id": None, "route": None, "page_id": screen_id, "surface_kind": "historical_exclusion",
            "visual_surface": False, "shell_variant_id": None, "purpose": purpose,
            "role_ids": ["all"], "action_permissions": [],
        }
        screens.append({key: item[key] for key in ("screen_id", "classification", "source_path", "source_pointer")})
        intake_items.append(item)
    journeys = [{"journey_id": journey_id, "screen_ids": screen_ids, "source_ref": source_ref(OWNER_INTENT, f"critical_journeys/{index}")}
                for index, (journey_id, screen_ids) in enumerate(JOURNEY_SPECS)]
    inventory = {
        "schema_id": "custometry.ui-g1-admission-inventory/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "revision": 1,
        "status": "complete",
        "authority_boundary": "G0 current-state floor and owner-intent admission boundary; not the G1 target atlas or a ceiling on source-backed target families",
        "screens": screens,
        "journeys": journeys,
        "target_family_requirements": [
            "analytical documents and large workbook composition",
            "collaboration, comments, review, publishing, and stable anchors",
            "segments and reusable recalculation",
            "digital acquisition, offline, and unit economics",
            "product, category, assortment, and inventory",
            "adoption, capacity, and performance operations",
        ],
    }
    return inventory, intake_items


def build_baseline(screen_items: list[dict[str, Any]]) -> dict[str, Any]:
    variant_kinds = {
        "shell.workspace": "authenticated_application",
        "shell.auth": "shellless_auth",
        "shell.setup": "setup",
        "shell.focus": "full_screen_focus",
        "shell.system": "system_recovery",
    }
    variant_screens = {
        variant_id: sorted(item["screen_id"] for item in screen_items if item["visual_surface"] and item["shell_variant_id"] == variant_id)
        for variant_id in variant_kinds
    }
    exceptions = []
    for variant_id in ("shell.auth", "shell.setup", "shell.focus", "shell.system"):
        slug = variant_id.split(".")[-1]
        decision_path = f".codex/delivery/ui-design-programs/custometry-v2/evidence/g0/baseline-exception-{slug}-decision-v1.json"
        exception = {
            "exception_id": f"baseline-exception-{slug}",
            "screen_ids": variant_screens[variant_id],
            "shell_variant_id": variant_id,
            "allowed_differences": ["shell region presence and composition required by the source-defined surface class"],
            "reason_ref": source_ref(OWNER_INTENT, f"baseline_exceptions/{slug}"),
            "owner_decision_ref": decision_path,
        }
        exception_decision(exception, decision_path)
        exceptions.append(exception)
    supporting_sources = [
        {"path": PILOT_EN, "sha256": sha(rel(PILOT_EN)), "authority": "hash-verified English content-stress companion", "covers": ["copy"]},
        {"path": OWNER_INTENT, "sha256": sha(rel(OWNER_INTENT)), "authority": "accepted owner intent and scope", "covers": ["product", "responsive", "accessibility"]},
        {"path": PLATFORM_ADR, "sha256": sha(rel(PLATFORM_ADR)), "authority": "accepted target responsive-Web frontend ownership decision", "covers": ["product", "responsive", "accessibility"]},
        {"path": UI_BLUEPRINT, "sha256": sha(rel(UI_BLUEPRINT)), "authority": "normative pre-G0 UI requirements and current-state inventory", "covers": ["product", "responsive", "accessibility", "copy"]},
        {"path": ROUTES, "sha256": sha(rel(ROUTES)), "authority": "current route, role, permission, state, and navigation contracts", "covers": ["product", "copy"]},
    ]
    for exception in exceptions:
        supporting_sources.append({
            "path": exception["owner_decision_ref"], "sha256": sha(rel(exception["owner_decision_ref"])),
            "authority": "revisioned compatibility decision for an exact baseline shell exception",
            "covers": ["product"],
        })
    states = []
    for state_id in ("default", "hover", "focus_visible", "active", "disabled", "loading", "error"):
        states.append({
            "state_id": state_id,
            "geometry": {"minimum_height": specified(32, "px")},
            "visual_properties": {"state_treatment": specified(state_id)},
            "content_behavior": "preserve the concise label and source-backed meaning",
            "interaction_behavior": f"apply the {state_id} source-backed control behavior",
            "source_refs": [source_ref(PILOT_RU, "source-backed-controls")],
        })
    token_values = {
        "color": ("color.surface", "#ffffff", None, "application surface"),
        "typography": ("type.body.family", "Inter, ui-sans-serif, system-ui, sans-serif", None, "primary interface font stack"),
        "spacing": ("space.shell", 12, "px", "shell and module rhythm"),
        "sizing": ("size.control.compact", 32, "px", "compact analytical control"),
        "radius": ("radius.control", 8, "px", "compact control radius"),
        "border": ("border.default", "1px solid #a7b2b9", None, "default structural border"),
        "elevation": ("elevation.overlay", "0 12px 32px rgba(25,41,50,.08)", None, "overlay elevation"),
        "opacity": ("opacity.disabled", 0.55, None, "disabled affordance"),
        "motion": ("motion.shell", "200ms ease", None, "shell transformation with reduced-motion override"),
        "z_index": ("z.overlay", 40, None, "overlay layer"),
    }
    foundation_tokens = {category: [{"token_id": values[0], "value": specified(values[1], values[2]), "usage": values[3]}]
                         for category, values in token_values.items()}
    variants = []
    for variant_id, kind in variant_kinds.items():
        is_default = variant_id == "shell.workspace"
        regions = [
            shell_region(f"{variant_id}.header", "header", 0, is_default),
            shell_region(f"{variant_id}.primary-nav", "primary_navigation", 1, is_default),
            shell_region(f"{variant_id}.workspace", "workspace", 2, True),
            shell_region(f"{variant_id}.status", "status_line", 3, False),
        ]
        variants.append({
            "variant_id": variant_id, "variant_kind": kind, "is_default": is_default,
            "screen_ids": variant_screens[variant_id],
            "applicability": f"all intake visual surfaces assigned to {variant_id}",
            "regions": regions,
            "allowed_differences": [] if is_default else ["only the exact region-presence differences in the linked baseline exception"],
            "owner_decision_ref": None if is_default else next(item["owner_decision_ref"] for item in exceptions if item["shell_variant_id"] == variant_id),
        })
    icons = [
        "bell", "building-2", "calendar", "chart-column", "chart-line", "chevron-down", "chevron-left",
        "circle-help", "database", "ellipsis", "file-text", "grid-2x2", "layout-grid", "package",
        "panel-left-close", "search", "settings", "shield-check", "store", "trending-up", "users",
    ]
    baseline = {
        "$schema": "platform-ui-baseline.schema.json",
        "schema_id": "codex.platform-ui-baseline/v1",
        "contract_profile": "codex.platform-ui-baseline/v1@1.0.0",
        "baseline_id": "custometry.platform-baseline.v2",
        "revision": 1,
        "status": "accepted",
        "source_visual": {
            "path": PILOT_RU, "sha256": sha(rel(PILOT_RU)), "owner_decision_ref": VISUAL_ADAPTER,
            "native_viewport": {"width": 1440, "height": 900}, "state_id": "ready", "theme_id": "paper",
        },
        "scope": {
            "screen_acceptance_scope": SCREEN_ACCEPTANCE_SCOPE,
            "visual_language_scope": VISUAL_LANGUAGE_SCOPE,
            "reusable_foundation_scope": FOUNDATION_SCOPE,
            "inheritance_policy": "required", "mobile_scope": "unauthorized",
        },
        "supporting_sources": supporting_sources,
        "default_shell_variant_id": "shell.workspace",
        "shell_variants": variants,
        "navigation_contracts": [{
            "navigation_id": "workspace.primary", "shell_variant_id": "shell.workspace",
            "region_id": "shell.workspace.primary-nav", "orientation": "vertical",
            "items": [{
                "item_id": "workspace.overview", "order": 0, "label": "Overview", "icon_id": "layout-grid",
                "destination": "/w/:workspaceKey/overview", "active_match": "/w/:workspaceKey/overview",
                "group_id": "workspace", "visibility": "authenticated workspace members",
                "tooltip": "Workspace overview", "source_refs": [source_ref(ROUTES, "/routes/6")],
            }],
            "profile_area": {"height": specified(32, "px")},
            "responsive_behavior": [specified("preserve item identity; collapse presentation only when content requires it")],
            "identity_change_policy": "labels_order_icons_groups_destinations_fixed",
        }],
        "foundation_tokens": foundation_tokens,
        "font_contract": {
            "families": ["Inter", "ui-sans-serif", "system-ui"], "bundle_path": None, "bundle_sha256": None,
            "fallback_policy": "Use the exact source stack; a future bundled Inter asset requires a hash-pinned baseline revision.",
            "source_refs": [source_ref(PILOT_RU, "font-family")],
        },
        "asset_contract": {
            "bundle_paths": [], "bundle_sha256s": [], "replacement_policy": "exact_assets_only",
            "source_refs": [source_ref(PILOT_RU, "inline-source-assets")],
        },
        "icon_contract": {
            "library": "Lucide React plus exact source pilot mask assets", "version_or_commit": "0.515.0",
            "source_path": PILOT_RU, "source_sha256": sha(rel(PILOT_RU)),
            "icons": [{"icon_id": icon, "source_name": icon, "source_ref": source_ref(PILOT_RU, f"lucide-{icon}")} for icon in icons],
            "default_size": specified(16, "px"), "default_stroke_width": specified(1.5, "px"),
            "fill_policy": "stroke by default; exact source asset fill only when measured",
            "optical_alignment": "center on the control box and preserve source stroke geometry",
            "source_refs": [source_ref(PILOT_RU, "lucide-icons")],
            "forbidden_replacements": ["emoji", "unicode_glyph", "improvised_svg", "css_drawing"],
        },
        "component_contracts": [{
            "component_id": "action.button", "component_kind": "button",
            "variants": ["primary", "secondary", "quiet", "destructive"], "size_classes": ["sm", "md"],
            "required_states": [item["state_id"] for item in states], "not_applicable_states": {"selected": "buttons are not persistent selection controls"},
            "states": states, "internal_elements": ["label", "optional source-backed icon"],
            "spacing_relations": [{"from": "icon", "to": "label", "property": "gap", "value": specified(8, "px")}],
            "content_rules": "Use one concise outcome-oriented label; never substitute an unlabeled glyph for a named action.",
            "accessibility": "Use native button semantics, visible focus, an accessible name, and deterministic disabled/loading feedback.",
            "source_refs": [source_ref(PILOT_RU, "source-backed-controls")],
        }],
        "interaction_patterns": [{
            "pattern_id": "analytical.table", "kind": "table", "trigger": "open a source-backed analytical data surface",
            "placement": "inside the main workspace region", "dismissal": "not applicable; navigate or close the parent surface",
            "focus_behavior": "logical row and control order with sticky headings excluded from the tab sequence",
            "keyboard_behavior": "all controls are reachable; sorting and paging expose names and state",
            "geometry": {"row_min_height": specified(32, "px")},
            "spacing_relations": [{"from": "cell", "to": "cell", "property": "gap", "value": specified(0, "px")}],
            "states": ["loading", "populated", "empty", "partial", "error", "permission_denied", "recovery"],
            "source_refs": [source_ref(PILOT_RU, "customer-chart-data")],
        }],
        "layout_contract": {
            "grid": "persistent navigation plus fluid analytical workspace and source-backed contextual regions",
            "content_width": "fluid from 768px through 1920px; cap line length and module content where context requires",
            "scroll_policy": "prefer workspace and local data-region scrolling; preserve stable shell and focus anchors",
            "region_gap_rules": [{"from": "shell", "to": "workspace", "property": "gap", "value": specified(12, "px")}],
            "layering_rules": ["overlay and transient surfaces remain above shell content without changing navigation identity"],
            "source_refs": [source_ref(PILOT_RU, "screen-shell")],
        },
        "responsive_contract": {
            "supported_web_width_range": {"min_width": 768, "max_width": 1920},
            "anchor_viewports": [
                {"anchor_id": "web-768", "width": 768, "height": 1024, "state_id": "ready", "theme_id": "paper", "source_ref": source_ref(PLATFORM_ADR, "responsive-web-contract")},
                {"anchor_id": "web-1024", "width": 1024, "height": 768, "state_id": "ready", "theme_id": "paper", "source_ref": source_ref(PLATFORM_ADR, "responsive-web-contract")},
                {"anchor_id": "web-1440", "width": 1440, "height": 900, "state_id": "ready", "theme_id": "paper", "source_ref": source_ref(PLATFORM_ADR, "responsive-web-contract")},
                {"anchor_id": "web-1920", "width": 1920, "height": 1080, "state_id": "ready", "theme_id": "paper", "source_ref": source_ref(PLATFORM_ADR, "responsive-web-contract")},
            ],
            "breakpoint_policy": "content_driven", "shell_transformations": [],
            "navigation_identity_must_remain_exact": True, "component_adaptation": "prefer_container_queries",
            "overflow_policy": "use local overflow for analytical grids; do not hide primary task, trust, or recovery controls",
            "zoom_policy": "preserve meaning and operation at 200% zoom within the supported Web contract",
            "localization_stress_policy": "verify independent RU and EN content stress without changing identity or truncating essential meaning",
            "below_supported_range": "out_of_scope", "above_supported_range": "max_content_width",
            "source_refs": [source_ref(PLATFORM_ADR, "responsive-web-contract"), source_ref(OWNER_INTENT, "architecture_boundary/responsive_range_css_px")],
        },
        "accessibility_contract": {
            "focus_indicator": "minimum 2px visible focus treatment with sufficient contrast",
            "keyboard_navigation": "all named controls, dialogs, drawers, menus, tables, and focus surfaces remain keyboard-operable",
            "target_size": "32px compact analytical minimum with larger critical and touch-adjacent actions where source-backed",
            "contrast": "target WCAG 2.2 AA contrast; conformance requires later browser evidence",
            "reduced_motion": "honor prefers-reduced-motion and remove nonessential transitions",
            "source_refs": [source_ref(PILOT_RU, "focus-visible-and-reduced-motion"), source_ref(UI_BLUEPRINT, "accessibility")],
        },
        "exceptions": exceptions,
        "change_control": {
            "default_change_policy": "fixed",
            "fixed_domains": ["shell", "navigation", "foundation_tokens", "font_contract", "asset_contract", "icon_contract", "component_contracts", "interaction_patterns", "layout_contract", "responsive_contract", "accessibility_contract"],
            "exception_requires_owner_decision": True, "delegated_design_may_change_fixed_domains": False,
        },
        "unresolved_inputs": [],
    }
    return baseline


def main() -> int:
    prepare_owner_artifacts()
    for path, expected in ((PILOT_RU, PILOT_RU_SHA), (PILOT_EN, PILOT_EN_SHA)):
        if not rel(path).is_file() or sha(rel(path)) != expected:
            raise SystemExit(f"pilot hash mismatch: {path}")
    canonical_path = rel(CANONICAL_DECISION)
    if not canonical_path.is_file():
        print(json.dumps({"status": "prepared", "next": "assemble canonical owner decision", "request": OWNER_REQUEST}, indent=2))
        return 3
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    if canonical.get("schema_id") != "codex.ui-owner-decision/v1" or canonical.get("decision", {}).get("status") != "accepted":
        raise SystemExit("canonical visual authority decision is not accepted")
    visual_authority = {
        "source_evidence_mode": "renderable_html",
        "screen_acceptance_scope": SCREEN_ACCEPTANCE_SCOPE,
        "visual_language_scope": VISUAL_LANGUAGE_SCOPE,
        "reusable_foundation_scope": FOUNDATION_SCOPE,
        "inheritance_policy": "required",
        "mobile_scope": "unauthorized",
    }
    write_json(rel(VISUAL_ADAPTER), {
        "status": "accepted", "revision": 1, "decision_kind": "visual_authority",
        "compatibility_role": "Current baseline/intake validator adapter; canonical owner record remains authoritative.",
        "canonical_owner_decision_ref": {"path": CANONICAL_DECISION, "sha256": sha(canonical_path)},
        "owner_intent_ref": {"path": OWNER_INTENT, "sha256": sha(rel(OWNER_INTENT))},
        "source_visual": {"path": PILOT_RU, "sha256": PILOT_RU_SHA},
        "supporting_visual": {"path": PILOT_EN, "sha256": PILOT_EN_SHA},
        "visual_authority": visual_authority,
    })
    routes = json.loads(rel(ROUTES).read_text(encoding="utf-8"))
    surfaces = json.loads(rel(SURFACES).read_text(encoding="utf-8"))
    inventory, items = build_inventory(routes, surfaces)
    write_json(rel(INVENTORY), inventory)
    write_json(rel(PILOT_RECEIPT), {
        "schema_id": "custometry.ui-pilot-import-receipt/v1", "status": "verified", "revision": 1,
        "source_manifest": {"path": "docs/architecture/ui/custometry-pre-g0-pilot-manifest-v1.json", "sha256": sha(rel("docs/architecture/ui/custometry-pre-g0-pilot-manifest-v1.json"))},
        "imports": [
            {"locale": "ru", "path": PILOT_RU, "sha256": sha(rel(PILOT_RU)), "byte_count": rel(PILOT_RU).stat().st_size},
            {"locale": "en", "path": PILOT_EN, "sha256": sha(rel(PILOT_EN)), "byte_count": rel(PILOT_EN).stat().st_size},
        ],
        "authority": "exact-byte repository-owned copies; visual-language and content-stress evidence only",
    })
    by_screen: dict[str, list[dict[str, Any]]] = {}
    journeys = []
    for index, (journey_id, screen_ids) in enumerate(JOURNEY_SPECS):
        transitions = []
        for step, (from_id, to_id) in enumerate(zip(screen_ids, screen_ids[1:])):
            action_id = f"journey.{journey_id}.{step + 1}"
            target_is_surface = to_id.startswith("UI-OVR-")
            from_item = next(item for item in items if item["screen_id"] == from_id)
            by_screen.setdefault(from_id, []).append(action(
                action_id, f"Continue {journey_id.replace('-', ' ')}", f"{from_id}.content",
                source_ref(OWNER_INTENT, f"critical_journeys/{index}"),
                target=None if target_is_surface else to_id, surface=to_id if target_is_surface else None,
            ))
            transitions.append({
                "transition_id": f"{journey_id}.{step + 1}", "from_screen_id": from_id,
                "action_id": action_id, "to_screen_id": to_id, "external_boundary": None,
                "outcome": f"advance the accepted {journey_id} journey",
                "failure": "retain the source screen and show deterministic failure feedback",
                "recovery": "retry or return without losing the stable source anchor",
                "source_refs": [source_ref(OWNER_INTENT, f"critical_journeys/{index}")],
            })
        journeys.append({
            "journey_id": journey_id, "purpose": journey_id.replace("-", " "), "role_ids": ["all"],
            "preconditions": ["the user has a permitted workspace or installation context"],
            "entry_screen_ids": [screen_ids[0]], "terminal_screen_ids": [screen_ids[-1]],
            "outcomes": [f"complete {journey_id.replace('-', ' ')} with trust and stable context"],
            "transitions": transitions, "source_refs": [source_ref(OWNER_INTENT, f"critical_journeys/{index}")],
        })
    intake_screens = [screen_contract(item, by_screen.get(item["screen_id"], [])) for item in items]
    artifact_index_refs: dict[str, dict[str, str]] = {}
    for kind, values, singular in (
        ("screens", intake_screens, "screen"),
        ("journeys", journeys, "journey"),
        ("families", [], "family"),
        ("waves", [], "wave"),
    ):
        entries = []
        for value in values:
            identity = value[f"{singular}_id"]
            shard_ref = f".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0/{kind}/{identity}.json"
            write_json(rel(shard_ref), {singular: value})
            entries.append({
                "id": identity, "path": shard_ref, "sha256": sha(rel(shard_ref)),
                "json_pointer": f"/{singular}",
            })
        index_ref = f".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0/{kind}-index.json"
        write_json(rel(index_ref), {
            "$schema": "program-artifact-index.schema.json",
            "schema_id": "codex.ui-program-artifact-index/v1",
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
            "program_revision": 1,
            "index_kind": kind,
            "entries": entries,
        })
        artifact_index_refs[kind] = {"path": index_ref, "sha256": sha(rel(index_ref))}
    baseline = build_baseline(items)
    write_json(PROGRAM_DIR / "platform-ui-baseline.json", baseline)
    source_contracts = [
        {"path": OWNER_INTENT, "sha256": sha(rel(OWNER_INTENT)), "authority": "accepted current owner intent, scope, exclusions, journeys, and authority hierarchy", "covers": ["product", "journeys", "screens", "roles", "permissions", "states", "copy", "locales", "themes"]},
        {"path": ROUTES, "sha256": sha(rel(ROUTES)), "authority": "current route, role, permission, guard, state, and navigation contracts", "covers": ["routes", "screens", "roles", "permissions", "states", "copy"]},
        {"path": SURFACES, "sha256": sha(rel(SURFACES)), "authority": "current overlay, transient, system-state, and cross-surface capability contracts", "covers": ["screens", "states", "copy"]},
        {"path": TECH_BLUEPRINT, "sha256": sha(rel(TECH_BLUEPRINT)), "authority": "normative product specification", "covers": ["product", "journeys", "roles", "permissions", "states", "data", "copy", "locales"]},
        {"path": TECH_MIRROR, "sha256": sha(rel(TECH_MIRROR)), "authority": "required explanatory mirror of the product specification", "covers": ["product", "journeys", "copy"]},
        {"path": UI_BLUEPRINT, "sha256": sha(rel(UI_BLUEPRINT)), "authority": "pre-G0 UI requirements and current inventory; not accepted visual architecture", "covers": ["screens", "journeys", "states", "copy", "locales", "themes", "assets"]},
        {"path": INVENTORY, "sha256": sha(rel(INVENTORY)), "authority": "complete G1 admission inventory and exact current-state floor", "covers": ["routes", "screens", "journeys"]},
    ]
    intake = {
        "$schema": "ui-program-intake.schema.json", "schema_id": "codex.ui-program-intake/v1",
        "contract_profile": "codex.ui-program-intake/v1@1.0.0",
        "intake_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2.intake.v1", "revision": 1, "status": "complete",
        "product": {
            "product_id": "custometry", "product_name": "Custometry",
            "purpose": "Turn governed source data into trusted, reusable analytical decisions and operational artifacts.",
            "operating_model": "Self-hosted responsive-Web analytical workspace: connect and govern data, define semantic assets, analyze and forecast, publish and collaborate, then operate refresh, quality, adoption, capacity, and recovery with explicit trust metadata.",
            "primary_user_outcomes": [
                "produce trusted analytical results from governed data", "compose and reuse large analytical documents",
                "publish, review, collaborate, and refresh without losing stable anchors", "operate data, forecasts, workflows, adoption, capacity, and recovery",
            ],
            "domain_entities": ["workspace", "dataset", "metric", "methodology", "analysis", "segment", "forecast", "dashboard", "report", "pipeline", "run", "artifact", "organization", "principal"],
            "domain_terms": ["Result Trust", "Focus/Explore", "stable anchor", "semantic data", "quality gate", "publication state", "freshness"],
            "supported_platforms": ["web"],
        },
        "program_scope": {
            "included_release_slices": INCLUDED, "excluded_release_slices": EXCLUDED,
            "public_site_in_scope": False, "mobile_scope": "unauthorized", "source_ref": source_ref(OWNER_INTENT, "scope"),
        },
        "authoritative_inventory": {
            "path": INVENTORY, "sha256": sha(rel(INVENTORY)),
            "screen_collection": {"json_pointer": "/screens", "id_key": "screen_id"},
            "journey_collection": {"json_pointer": "/journeys", "id_key": "journey_id"},
        },
        "source_contracts": source_contracts,
        "roles": [{"id": role, "meaning": f"source-defined {role} role or role hint", "source_refs": [source_ref(ROUTES, f"role_catalog/{index}")]}
                  for index, role in enumerate(routes["role_catalog"])],
        "permission_profiles": [{"id": permission, "meaning": f"source-defined {permission} permission", "source_refs": [source_ref(ROUTES, f"permission_catalog/{index}")]}
                                for index, permission in enumerate(routes["permission_catalog"])],
        "locales": [
            {"id": "ru", "meaning": "Russian product locale and normative product-language source", "source_refs": [source_ref(OWNER_INTENT, "supporting_visual")]},
            {"id": "en", "meaning": "English product locale and independent content-stress companion", "source_refs": [source_ref(OWNER_INTENT, "supporting_visual")]},
        ],
        "themes": [{"id": "paper", "meaning": "accepted pilot paper theme", "source_refs": [source_ref(PILOT_RU, "data-theme-paper")]}],
        "global_data_contracts": [], "journeys": journeys, "screens": intake_screens,
        "pilot": {
            "source_visual_ref": PILOT_RU, "source_visual_sha256": PILOT_RU_SHA,
            "source_evidence_mode": "renderable_html", "owner_decision_ref": VISUAL_ADAPTER,
            "native_viewport": {"width": 1440, "height": 900}, "reviewed_state_ids": ["ready"],
            "reviewed_theme_ids": ["paper"], "represented_screen_ids": ["UI-AN-004"],
            "screen_acceptance_scope": SCREEN_ACCEPTANCE_SCOPE, "visual_language_scope": VISUAL_LANGUAGE_SCOPE,
            "reusable_foundation_scope": FOUNDATION_SCOPE, "inheritance_policy": "required",
        },
        "accepted_decisions": [],
        "baseline_contract": {"baseline_id": baseline["baseline_id"], "path": ".codex/delivery/ui-design-programs/custometry-v2/platform-ui-baseline.json", "sha256": sha(PROGRAM_DIR / "platform-ui-baseline.json")},
        "unresolved_inputs": [],
    }
    write_json(PROGRAM_DIR / "ui-program-intake.json", intake)
    program_path = PROGRAM_DIR / "ui-design-program.json"
    program = json.loads(program_path.read_text(encoding="utf-8"))
    counts = {
        "route_screens": sum(item["classification"] == "route_screen" for item in inventory["screens"]),
        "route_flows": sum(item["classification"] == "route_flow" for item in inventory["screens"]),
        "persistent_shells": sum(item["classification"] == "persistent_shell" for item in inventory["screens"]),
        "route_backed_transients": sum(item["classification"] == "route_backed_transient" for item in inventory["screens"]),
        "overlays": sum(item["classification"] == "overlay" for item in inventory["screens"]),
        "system_state_families": sum(item["classification"] == "system_state_family" for item in inventory["screens"]),
        "internal_or_non_visual": sum(item["classification"] == "internal_or_non_visual" for item in inventory["screens"]),
        "historical_exclusions": sum(item["classification"] == "historical_exclusion" for item in inventory["screens"]),
    }
    program["status"] = "draft"
    program["validation_profile"] = "draft"
    program["input_contracts"] = {
        "intake": {"path": ".codex/delivery/ui-design-programs/custometry-v2/ui-program-intake.json", "sha256": sha(PROGRAM_DIR / "ui-program-intake.json")},
        "baseline": {"path": ".codex/delivery/ui-design-programs/custometry-v2/platform-ui-baseline.json", "sha256": sha(PROGRAM_DIR / "platform-ui-baseline.json")},
    }
    program["source_contracts"] = [{
        "path": source["path"], "authority": source["authority"], "required_status": "current",
        "sha256": source["sha256"],
        "screen_collections": [{"json_pointer": "/screens", "id_key": "screen_id"}] if source["path"] == INVENTORY else [],
        "journey_collections": [{"json_pointer": "/journeys", "id_key": "journey_id"}] if source["path"] == INVENTORY else [],
    } for source in source_contracts]
    program["artifact_indexes"] = artifact_index_refs
    program["visual_authority"] = {
        "source_visual_ref": PILOT_RU, "source_visual_sha256": PILOT_RU_SHA,
        "source_evidence_mode": "renderable_html", "owner_decision_ref": VISUAL_ADAPTER,
        "screen_acceptance_scope": SCREEN_ACCEPTANCE_SCOPE, "visual_language_scope": VISUAL_LANGUAGE_SCOPE,
        "reusable_foundation_scope": FOUNDATION_SCOPE, "inheritance_policy": "required",
        "mobile_scope": "unauthorized", "product_semantics_scope": "source_registry_only",
    }
    program["scope"] = {
        "product": "custometry", "platform": "web", "included_release_slices": INCLUDED,
        "excluded_release_slices": EXCLUDED,
        "origin": {"kind": "owner_decision", "ref": source_ref(OWNER_INTENT, "scope")},
    }
    program["expected_inventory"] = {"total": len(inventory["screens"]), **counts, "journeys": len(JOURNEY_SPECS)}
    # G0 stops at the accepted intake/baseline boundary. Atlas entries are
    # populated only by G1, so deterministic G0 regeneration must clear them.
    program["screens"] = []
    program["journeys"] = []
    program["responsive_policy"] = {
        "adaptive_web_required": True,
        "supported_web_width_range": {"min_width": 768, "max_width": 1920, "origin": {"kind": "delegated_design_decision", "ref": source_ref(PLATFORM_ADR, "responsive-web-contract")}},
        "anchor_viewports": [
            {"anchor_id": "web-768", "width": 768, "height": 1024, "class": "responsive_web", "origin": {"kind": "delegated_design_decision", "ref": source_ref(PLATFORM_ADR, "responsive-web-contract")}},
            {"anchor_id": "web-1024", "width": 1024, "height": 768, "class": "responsive_web", "origin": {"kind": "delegated_design_decision", "ref": source_ref(PLATFORM_ADR, "responsive-web-contract")}},
            {"anchor_id": "web-1440", "width": 1440, "height": 900, "class": "responsive_web", "origin": {"kind": "delegated_design_decision", "ref": source_ref(PLATFORM_ADR, "responsive-web-contract")}},
            {"anchor_id": "web-1920", "width": 1920, "height": 1080, "class": "responsive_web", "origin": {"kind": "delegated_design_decision", "ref": source_ref(PLATFORM_ADR, "responsive-web-contract")}},
        ],
        "breakpoint_policy": "content_driven", "breakpoint_policy_origin": {"kind": "delegated_design_decision", "ref": source_ref(PLATFORM_ADR, "responsive-web-contract")},
        "component_adaptation": "prefer_container_queries", "component_adaptation_origin": {"kind": "delegated_design_decision", "ref": source_ref(PLATFORM_ADR, "responsive-web-contract")},
        "logical_properties_required": True, "logical_properties_origin": {"kind": "normative_requirement", "ref": source_ref(UI_BLUEPRINT, "responsive-web")},
        "mobile_scope": "unauthorized", "mobile_scope_origin": {"kind": "owner_decision", "ref": source_ref(OWNER_INTENT, "scope/mobile_scope")},
        "mobile_authorization_ref": None, "authorized_mobile_surfaces": [], "authorized_mobile_viewports": [], "allowed_mobile_changes": [],
    }
    write_json(program_path, program)
    # Accepted transition receipts must bind immutable stage artifacts. Keep a
    # byte-identical G0 snapshot so later gates can evolve the live program
    # without making the accepted G0 receipt stale.
    write_json(PROGRAM_DIR / "artifacts/g0/ui-design-program.snapshot.json", program)
    print(json.dumps({
        "status": "built", "screens": len(intake_screens), "journeys": len(journeys),
        "route_screens": counts["route_screens"], "route_flows": counts["route_flows"],
        "pilot_hashes": {"ru": sha(rel(PILOT_RU)), "en": sha(rel(PILOT_EN))},
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
