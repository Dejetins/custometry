#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
ARTIFACT_DIR = PROGRAM / "artifacts/g4-r5/family-seg-shell-workspace-baseline"
EVIDENCE_DIR = PROGRAM / "evidence/family.seg.shell-workspace.baseline-r5"
INTAKE = PROGRAM / "artifacts/g0-r5/ui-program-intake.json"
BASELINE = PROGRAM / "artifacts/g0-r5/platform-ui-baseline.json"
PROGRAM_PATH = PROGRAM / "ui-design-program.json"
ADMISSION = PROGRAM / "evidence/g0-r2/g1-admission-inventory.json"
SCREENS_INDEX = PROGRAM / "artifacts/g2-r4/screens-index.json"
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program")
ASSEMBLE_APPLICABILITY = SKILL / "scripts/assemble_standard_applicability.py"

STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")
ACTION_STATES = set(STATES)
ANCHORS = (
    {"anchor_id": "web-768", "width": 768, "height": 1024},
    {"anchor_id": "web-1440", "width": 1440, "height": 900},
    {"anchor_id": "web-1920", "width": 1920, "height": 1080},
)
SCREEN_ID = "UI-SEG-001"
FAMILY_ID = "family.seg.shell-workspace.baseline"
FONT_HASH = hashlib.sha256(b"Inter,ui-sans-serif,system-ui").hexdigest()
ASSET_HASH = hashlib.sha256(b"inline-css-no-external-assets").hexdigest()
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/platform-ui-baseline.json"
INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json"
ARTIFACT_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-seg-shell-workspace-baseline"
EVIDENCE_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/family.seg.shell-workspace.baseline-r5"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def origin(kind: str, ref: str, **extra):
    return {"kind": kind, "ref": ref, **extra}


def specified(value, ref: str, kind: str = "product_contract"):
    return {
        "value": value,
        "unit": None,
        "origin": origin(kind, ref),
        "tolerance": 0,
        "change_policy": "source_revision_required" if kind == "product_contract" else "fixed",
    }


def baseline_styles(baseline: dict, *, component_id: str, variant: str, size: str, element_type: str, slot: str) -> str:
    values: dict[str, str] = {}
    for clause in baseline["standard_contract"]["clauses"]:
        for target in clause.get("applicability", []):
            if (
                target.get("anchor_id") == "web-1440"
                and target.get("scope") == "component"
                and target.get("component_id") == component_id
                and target.get("variant") == variant
                and target.get("size_class") == size
                and target.get("element_type") == element_type
                and target.get("slot_id") == slot
                and target.get("state_id") == "default"
            ):
                values[clause["property"]] = str(clause["value"])
    return ";".join(f"{key}:{value}" for key, value in sorted(values.items()))


def standard_identity(component_id: str, variant: str, size: str, element_type: str):
    return {
        "component_id": component_id,
        "variant": variant,
        "size_class": size,
        "element_type": element_type,
        "icon_id": None,
        "state_ids": ["default"],
    }


def element(element_id: str, region_id: str, element_type: str, component_id: str, variant: str, size: str,
            content: str, action_ids: list[str], state_id: str, *, standard=None, slot=None, parent=None):
    return {
        "element_id": element_id,
        "parent_element_id": parent,
        "region_id": region_id,
        "locator": f'[data-ui-element="{element_id}"]',
        "visibility": "required",
        "element_type": element_type,
        "standard_slot_id": slot,
        "standard_identity": standard,
        "component_id": component_id,
        "variant": variant,
        "size_class": size,
        "content_contract": content,
        "icon_id": None,
        "action_ids": action_ids,
        "state_ids": [f"{SCREEN_ID}.{state_id}"],
        "component_state_ids": ["default"],
        "responsive_behavior": [specified(
            "preserve meaning and reachability across the supported responsive-Web range",
            "references/responsive-policy-v1.md#responsive-web-requirement",
            "normative_requirement",
        )],
        "accessibility": {
            "name": specified(content, f"{INTAKE_REL}#/screens/58", "product_contract")
        },
        "source_refs": [origin("product_contract", f"{INTAKE_REL}#/screens/58")],
    }


def region(region_id: str, component_id: str, state_id: str):
    return {
        "region_id": region_id,
        "locator": f'[data-ui-region="{region_id}"]',
        "visibility": "required",
        "component_id": component_id,
        "component_status": "candidate",
        "variant": "workspace",
        "state": state_id,
        "source_refs": [origin("product_contract", f"{INTAKE_REL}#/screens/58")],
        "geometry": {},
        "layout_rules": [],
        "visual_properties": {},
        "content": {},
        "interactions": [],
        "accessibility": {"landmark": specified("named landmark", f"{INTAKE_REL}#/screens/58")},
        "responsive_behavior": [specified(
            "responsive Web reflow without mobile-specific composition",
            "references/responsive-policy-v1.md#responsive-web-requirement",
            "normative_requirement",
        )],
        "geometry_tolerance_px": 0,
        "geometry_tolerance_origin": origin("normative_requirement", "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence"),
        "computed_style_properties": ["display", "position", "overflow-x"],
        "computed_style_properties_origin": origin("normative_requirement", "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence"),
    }


def state_copy(state: str):
    return {
        "initial": ("Сегменты", "Подготовка рабочего пространства сегментов", "Проверяем доступные определения и Result Trust."),
        "loading": ("Сегменты", "Загружаем сегменты", "Сохраняем контекст workspace и проверяем актуальность данных."),
        "populated": ("Сегменты", "12 активных сегментов", "Определения готовы к пересчёту, экспорту и повторному использованию."),
        "error": ("Сегменты", "Не удалось обновить список", "Контекст сохранён. Можно безопасно повторить действие или экспортировать последнюю подтверждённую версию."),
        "permission_denied": ("Сегменты", "Доступ ограничен", "Для управления нужен segment.manage; доступный контекст и безопасные действия остаются видимыми."),
        "recovery": ("Сегменты", "Восстановление после сбоя", "Последняя подтверждённая версия доступна; пересчёт можно продолжить без потери контекста."),
    }[state]


def html_document(state: str, fixture_hash: str, baseline: dict) -> str:
    title, headline, summary = state_copy(state)
    panel_css = baseline_styles(baseline, component_id="surface.panel", variant="panel", size="standard", element_type="article", slot="shell.main-content.article")
    button_css = baseline_styles(baseline, component_id="action.button", variant="button", size="standard", element_type="button", slot="shell.main-content.button")
    actions = ""
    if state in ACTION_STATES:
        rows = [
            ("UI-SEG-001.segment.manage", "Управлять", "Управление сегментом доступно"),
            ("UI-SEG-001.segment.export", "Экспорт", "Экспорт сегмента подготовлен"),
            ("journey.define-recalculate-reuse-segment.1", "Продолжить", "Переход к определению сегмента подготовлен"),
        ]
        actions = "".join(
            f'<button type="button" data-ui-element="action-{index}" data-prototype-action="{html.escape(action_id)}" '
            f'data-ui-component="action.button" data-ui-variant="button" data-ui-size="standard" '
            f'data-ui-slot="shell.main-content.button" data-ui-state="default" style="{html.escape(button_css)}" '
            f'data-outcome="{html.escape(outcome)}">{html.escape(label)}</button>'
            for index, (action_id, label, outcome) in enumerate(rows, start=1)
        )
    state_rows = {
        "populated": "<div class=\"grid\"><b>Лояльные клиенты</b><span>4 правила · 38 420 профилей</span><b>Риск оттока</b><span>6 правил · 7 194 профиля</span><b>Новые покупатели</b><span>3 правила · 12 806 профилей</span></div>",
        "loading": "<div class=\"skeleton\" aria-label=\"Загрузка\"></div>",
    }.get(state, "")
    return f"""<!doctype html>
<html lang="ru" data-theme="graphite"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="ui-fixture-sha256" content="{fixture_hash}"><meta name="ui-font-bundle-sha256" content="{FONT_HASH}"><meta name="ui-asset-bundle-sha256" content="{ASSET_HASH}"><title>{html.escape(title)} · Custometry</title>
<style>
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:#070708;color:#f0f0f2;font-family:Inter,ui-sans-serif,system-ui,sans-serif}}body{{min-width:0}}
.shell{{height:100vh;min-height:0;overflow:hidden;display:grid;grid-template-columns:84px minmax(0,1fr);grid-template-rows:76px minmax(0,1fr);background:#070708}}
[data-ui-region="shell.workspace.header"]{{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border-bottom:1px solid #303136;background:#111214}}
[data-ui-region="shell.workspace.primary-nav"]{{grid-row:2;padding:22px 12px;border-right:1px solid #303136;background:#111214}}
[data-ui-region="shell.workspace.workspace"]{{grid-row:2;min-width:0;padding:32px;overflow:auto;background:radial-gradient(circle at 85% 0,#1c2529 0,transparent 34%),#070708}}
.brand{{font-weight:760;letter-spacing:.02em}}.nav{{display:grid;gap:10px}}.nav span{{display:grid;place-items:center;height:44px;border-radius:12px;color:#a7a7ad;background:#1a1b1e}}.nav .active{{color:#8bd2e8;box-shadow:inset 3px 0 #66b9d3}}
.panel{{max-width:1180px;margin:0 auto}}.eyebrow{{color:#8bd2e8;font-size:12px;text-transform:uppercase;letter-spacing:.14em}}h1{{font-size:clamp(28px,4vw,48px);margin:10px 0 8px}}p{{color:#a7a7ad;max-width:760px;line-height:1.5}}.trust{{display:inline-flex;margin:18px 0;padding:7px 10px;border:1px solid #303136;border-radius:999px;color:#c9cbd0;background:#1a1b1e}}
.actions{{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}}button{{cursor:pointer}}button:focus,button:focus-visible{{outline:3px solid #8bd2e8!important;outline-offset:3px!important}}.outcome{{min-height:22px;margin-top:14px;color:#8bd2e8}}
.grid{{display:grid;grid-template-columns:minmax(180px,1fr) minmax(220px,1.5fr);gap:1px;margin-top:24px;border:1px solid #303136;background:#303136}}.grid>*{{padding:14px;background:#111214}}.skeleton{{height:180px;margin-top:24px;border-radius:12px;background:linear-gradient(90deg,#111214,#242529,#111214);background-size:200% 100%}}
@media(max-width:900px){{.shell{{grid-template-columns:64px minmax(0,1fr)}}[data-ui-region="shell.workspace.workspace"]{{padding:22px 18px}}.grid{{grid-template-columns:1fr}}}}
</style></head><body class="shell">
<header data-ui-region="shell.workspace.header"><div data-ui-element="header-root"><span class="brand">CUSTOMETRY</span> <span>Workspace · Northwind</span></div></header>
<nav aria-label="Основная навигация" data-ui-region="shell.workspace.primary-nav"><div class="nav" data-ui-element="nav-root"><span>⌂</span><span class="active">S</span><span>ƒ</span><span>?</span></div></nav>
<main data-ui-region="shell.workspace.workspace"><article class="panel" data-ui-element="workspace-root" data-ui-state="default">
<div class="eyebrow">Segmentation · {html.escape(state.replace('_',' '))}</div><h1>{html.escape(headline)}</h1><p>{html.escape(summary)}</p><div class="trust">Result Trust · проверено 22 августа, 19:00 UTC</div>{state_rows}
<div class="actions">{actions}</div><div class="outcome" role="status" aria-live="polite" data-action-result="status"></div>
</article></main>
<script>document.querySelectorAll('[data-prototype-action]').forEach(button=>button.addEventListener('click',()=>{{const node=document.querySelector('[data-action-result="status"]');node.textContent=button.dataset.outcome;node.setAttribute('data-last-action',button.dataset.prototypeAction)}}));</script>
</body></html>"""


def contract_for(state: str, fixture_path: Path, html_path: Path, baseline: dict, intake_hash: str, baseline_hash: str):
    screen_revision = f"UI-SEG-001.{state}.AN.ru.graphite.r5"
    state_id = f"UI-SEG-001.{state}"
    actions = []
    action_elements = []
    if state in ACTION_STATES:
        action_specs = [
            ("UI-SEG-001.segment.manage", "Segment Manage completes or the next contract-bound surface opens", "Управление сегментом доступно"),
            ("UI-SEG-001.segment.export", "Segment Export completes or the next contract-bound surface opens", "Экспорт сегмента подготовлен"),
            ("journey.define-recalculate-reuse-segment.1", "Continue define recalculate reuse segment completes or the next contract-bound surface opens", "Переход к определению сегмента подготовлен"),
        ]
        for index, (action_id, expected_outcome, asserted_text) in enumerate(action_specs, start=1):
            actions.append({
                "action_id": action_id,
                "expected_outcome": expected_outcome,
                "side_effect_class": "local_state",
                "activation_policy": "execute_in_fixture",
                "outcome_assertion": {"kind": "dom", "selector": "[data-action-result=\"status\"]", "property": "textContent", "expected": asserted_text},
            })
            action_elements.append(element(
                f"action-{index}", "shell.workspace.workspace", "button", "action.button", "secondary", "sm",
                expected_outcome, [action_id], state,
                standard=standard_identity("action.button", "button", "standard", "button"),
                slot="shell.main-content.button", parent="workspace-root",
            ))
    screen = {
        "$schema": "screen-design-contract.schema.json",
        "schema_id": "codex.ui-screen-design-contract/v1",
        "contract_profile": "codex.ui-screen-design-contract/v1@2.0.0",
        "screen_revision_id": screen_revision,
        "program_revision_ref": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2@5",
        "functional_contract_ref": {"path": INTAKE_REL, "sha256": intake_hash, "json_pointer": "/screens/58", "screen_id": SCREEN_ID},
        "baseline_binding": {"baseline_id": baseline["baseline_id"], "path": BASELINE_REL, "sha256": baseline_hash, "shell_variant_id": "shell.workspace", "exception_id": None},
        "standard_binding": {
            "standard_revision_id": baseline["standard_contract"]["standard_revision_id"],
            "clause_inventory_sha256": baseline["standard_contract"]["clause_inventory_sha256"],
            "applicability_manifest": {"path": f"{EVIDENCE_REL}/states/{state}/standard-applicability.json", "sha256": "0" * 64},
        },
        "standard_exceptions": [],
        "status": "review",
        "product_identity": {"screen_id": SCREEN_ID, "route_id": SCREEN_ID, "route": "/w/:workspaceKey/segments", "state_id": state_id, "role_id": "AN", "permission_profile": "segment.manage", "locale": "ru", "theme": "graphite"},
        "source_visual": {"kind": "delegated_design_output", "evidence_mode": "visual_language_only", "html_path": baseline["source_visual"]["path"], "image_path": None, "html_sha256": baseline["source_visual"]["sha256"], "image_sha256": None, "owner_decision_ref": None, "delegation_ref": "references/stage-transition-contract-v1.md#delegated-design-envelope"},
        "visual_authority": {
            "source_visual_ref": baseline["source_visual"]["path"], "source_visual_sha256": baseline["source_visual"]["sha256"], "owner_decision_ref": baseline["source_visual"]["owner_decision_ref"],
            "screen_acceptance_scope": baseline["scope"]["screen_acceptance_scope"], "visual_language_scope": baseline["scope"]["visual_language_scope"], "reusable_foundation_scope": baseline["scope"]["reusable_foundation_scope"],
            "inheritance_policy": "required", "mobile_scope": "unauthorized",
        },
        "comparison_claims": {"required_purpose": "visual_language_conformance", "deterministic_render_proves_fidelity": False, "reference_logical_artifact_id": "custometry-pilot-v3-ru", "implementation_logical_artifact_id": f"{screen_revision}-candidate"},
        "interaction_contract": {
            "visible_actions": actions, "no_actions_reason_ref": None if actions else f"{INTAKE_REL}#/screens/58/states/{STATES.index(state)}/available_action_ids",
            "required_checks": ["keyboard_activation", "focus_visibility", "tab_radio_behavior", "menus", "toggles", "refresh_feedback", "state_transitions", "no_unresolved_file_navigation", "no_console_errors", "no_request_failures", "no_page_horizontal_overflow"],
            "allowed_origins": ["http://127.0.0.1:4173"], "fixture_mode": "isolated_local", "evidence_redaction_required": True, "redaction_selectors": ["[data-sensitive]", "input[type='password']"],
        },
        "render_environment": {"browser": "chromium/150.0.7871.187", "browser_mechanic": "playwright_cli", "device_scale_factor": 1, "timezone": "UTC", "fixed_clock_iso": "2026-08-22T19:00:00Z", "reduced_motion": True, "animations": "disabled", "fixture_data_path": rel(fixture_path), "fixture_data_sha256": sha(fixture_path), "font_bundle_sha256": FONT_HASH, "asset_bundle_sha256": ASSET_HASH},
        "viewport_contract": {
            "mode": "responsive_web", "supported_web_width_range": {"min_width": 768, "max_width": 1920, "origin": origin("normative_requirement", "docs/adr/0007-responsive-web-frontend-platform.md#responsive-web-contract")},
            "anchors": [{**anchor, "class": "responsive_web", "state_ref": state_id, "origin": origin("normative_requirement", "docs/adr/0007-responsive-web-frontend-platform.md#responsive-web-contract")} for anchor in ANCHORS],
            "breakpoint_policy": "content_driven", "breakpoint_policy_origin": origin("normative_requirement", "references/responsive-policy-v1.md#breakpoints-and-components"),
            "below_supported_range": "out_of_scope", "below_supported_range_origin": origin("normative_requirement", "docs/adr/0007-responsive-web-frontend-platform.md#responsive-web-contract"),
            "above_supported_range": "max_content_width", "above_supported_range_origin": origin("normative_requirement", "docs/adr/0007-responsive-web-frontend-platform.md#responsive-web-contract"),
            "mobile_scope": "unauthorized", "mobile_scope_origin": origin("normative_requirement", "references/responsive-policy-v1.md#mobile-authorization-boundary"), "mobile_authorization_ref": None,
            "mobile_specific_composition": False, "authorized_mobile_surfaces": [], "authorized_mobile_viewports": [], "allowed_mobile_changes": [],
        },
        "regions": [region("shell.workspace.header", None, state), region("shell.workspace.primary-nav", None, state), region("shell.workspace.workspace", None, state)],
        "element_contracts": [
            element("header-root", "shell.workspace.header", "div", None, "workspace", "standard", "Custometry workspace identity", [], state),
            element("nav-root", "shell.workspace.primary-nav", "div", None, "workspace", "standard", "Primary workspace navigation", [], state),
            element("workspace-root", "shell.workspace.workspace", "article", None, state, "standard", state_copy(state)[2], [], state),
            *action_elements,
        ],
        "allowed_provenance_kinds": ["product_contract", "normative_requirement", "accepted_visual", "measured_baseline", "design_token", "owner_decision", "derived_formula", "delegated_design_decision"],
        "unresolved_decisions": [],
        "acceptance": {"agent_self_acceptance": "prohibited", "machine_receipt_required": True, "owner_decision_required": True, "owner_decision_ref": None, "screen_acceptance_receipt_path": None, "screen_acceptance_receipt_sha256": None, "pixel_diff_policy": {"channel_threshold": {"value": 0, "unit": "channel-value", "origin": origin("normative_requirement", "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence"), "tolerance": 0, "change_policy": "owner_approval_required"}, "approved_max_different_pixels": {"value": 0, "unit": "px", "origin": origin("normative_requirement", "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence"), "tolerance": 0, "change_policy": "owner_approval_required"}}},
    }
    return screen


def prepare() -> None:
    baseline = load(BASELINE)
    intake = load(INTAKE)
    intake_hash, baseline_hash = sha(INTAKE), sha(BASELINE)
    projection = load(ADMISSION)
    for admitted, source in zip(projection["screens"], intake["screens"], strict=True):
        if admitted["screen_id"] != source["screen_id"]:
            raise ValueError(f"screen projection drift: {admitted['screen_id']} != {source['screen_id']}")
        admitted["required_states"] = [state["state_id"] for state in source["states"]]
    projection["target_family_requirements"] = {
        "family_id": FAMILY_ID,
        "representative_screen_ids": [SCREEN_ID],
        "required_screen_state_ids": [f"{SCREEN_ID}::{SCREEN_ID}.{state}" for state in STATES],
    }
    projection_path = ARTIFACT_DIR / "g1-admission-inventory.family-projection.json"
    dump(projection_path, projection)
    snapshot = load(PROGRAM_PATH)
    for contract in snapshot["source_contracts"]:
        if contract.get("path") == rel(ADMISSION):
            contract["screen_collections"] = []
    snapshot["source_contracts"].append({
        "path": rel(projection_path),
        "authority": "G4 stage-owned exact full-inventory projection adding accepted required states for the family.seg representative",
        "required_status": "complete",
        "sha256": sha(projection_path),
        "screen_collections": [{"json_pointer": "/screens", "id_key": "screen_id"}],
        "journey_collections": [],
    })
    for index, screen in enumerate(snapshot["screens"]):
        screen_id = screen["screen_ref"]["expected_id"]
        screen["screen_ref"] = {
            "path": rel(projection_path),
            "json_pointer": f"/screens/{index}",
            "expected_id": screen_id,
        }
    screen_entries_path = ARTIFACT_DIR / "program-screen-entries.snapshot.json"
    dump(screen_entries_path, {"screens": snapshot["screens"]})
    screens_index = load(SCREENS_INDEX)
    for index, entry in enumerate(screens_index["entries"]):
        entry["path"] = rel(screen_entries_path)
        entry["sha256"] = sha(screen_entries_path)
        entry["json_pointer"] = f"/screens/{index}"
    screens_index_path = ARTIFACT_DIR / "screens-index.snapshot.json"
    dump(screens_index_path, screens_index)
    snapshot_path = ARTIFACT_DIR / "ui-design-program.snapshot.json"
    snapshot["artifact_indexes"]["screens"] = {"path": rel(screens_index_path), "sha256": sha(screens_index_path)}
    snapshot["execution_artifacts"]["plan_doc"] = rel(snapshot_path)
    dump(snapshot_path, snapshot)
    for state in STATES:
        fixture_path = ARTIFACT_DIR / f"states/{state}/fixture.json"
        dump(fixture_path, {"screen_id": SCREEN_ID, "state_id": f"{SCREEN_ID}.{state}", "clock": "2026-08-22T19:00:00Z", "workspace": "Northwind", "records": 12 if state == "populated" else 0})
        html_path = ARTIFACT_DIR / f"states/{state}/screen.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(html_document(state, sha(fixture_path), baseline), encoding="utf-8")
        contract_path = ARTIFACT_DIR / f"states/{state}/screen-contract.json"
        dump(contract_path, contract_for(state, fixture_path, html_path, baseline, intake_hash, baseline_hash))
        applicability = EVIDENCE_DIR / f"states/{state}/standard-applicability.json"
        applicability.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(ASSEMBLE_APPLICABILITY), "--screen", str(contract_path), "--baseline", str(BASELINE), "--project-root", str(ROOT), "--output", str(applicability)], check=True)
        contract = load(contract_path)
        contract["standard_binding"]["applicability_manifest"]["sha256"] = sha(applicability)
        dump(contract_path, contract)
    dump(EVIDENCE_DIR / "family-scope.json", {
        "family_id": FAMILY_ID, "family_revision_id": f"{FAMILY_ID}-r5", "representative_screen_ids": [SCREEN_ID],
        "required_state_ids": [f"{SCREEN_ID}.{state}" for state in STATES], "responsive_anchor_ids": [item["anchor_id"] for item in ANCHORS],
        "mobile_scope": "unauthorized", "proof_boundary": "isolated rendered family review; no production implementation, deployment, mobile-specific design, or full WCAG conformance",
    })


def bind() -> None:
    for state in STATES:
        contract_path = ARTIFACT_DIR / f"states/{state}/screen-contract.json"
        applicability = EVIDENCE_DIR / f"states/{state}/standard-applicability.json"
        contract = load(contract_path)
        contract["standard_binding"]["applicability_manifest"]["sha256"] = sha(applicability)
        dump(contract_path, contract)


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if command == "prepare":
        prepare()
    elif command == "bind-applicability":
        bind()
    else:
        raise SystemExit(f"unknown command: {command}")
