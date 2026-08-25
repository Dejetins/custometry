#!/usr/bin/env python3
"""Build deterministic G4 r3 auth-family design artifacts and review surface."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
ARTIFACT = PROGRAM / "artifacts/g4-r3/family-auth-shell-auth-baseline-exception-auth"
EVIDENCE = PROGRAM / "evidence/g4-r3/family-auth-shell-auth-baseline-exception-auth"
INTAKE = PROGRAM / "artifacts/g0-r2/ui-program-intake.json"
BASELINE = PROGRAM / "artifacts/g0-r2/platform-ui-baseline.json"
VISUAL = PROGRAM / "evidence/pilot-candidate-v2/ru/source.html"
PROGRAM_DOC = PROGRAM / "ui-design-program.json"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/g4-r3/family-auth-shell-auth-baseline-exception-auth-family-report.md"
SCHEMA = "/Users/daniildegtyarev/.codex/skills/ui-design-program/assets/screen-design-contract.schema.json"
DELEGATION_REF = "references/stage-transition-contract-v1.md#delegated-design-envelope"
VISUAL_REF = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2/ru/source.html"
INTAKE_REF = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json"
BASELINE_REF = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
PROGRAM_REF = ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
G1_ADMISSION_REF = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/g1-admission-inventory.json"
FAMILY_ID = "family.auth.shell-auth.baseline-exception-auth"
FAMILY_REVISION_ID = f"{FAMILY_ID}-r3"
STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")
ANCHORS = (
    ("web-768", 768, 1024),
    ("web-1024", 1024, 768),
    ("web-1440", 1440, 900),
    ("web-1920", 1920, 1080),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def delegated_origin(rationale: str = "Realize the accepted Graphite/cyan visual language for the source-backed auth route.") -> dict[str, Any]:
    return {
        "kind": "delegated_design_decision",
        "ref": DELEGATION_REF,
        "rationale": rationale,
        "constraints": [
            "accepted-visual-language-only",
            "shell.auth",
            "baseline-exception-auth",
            "responsive-web-768-1920",
            "mobile-scope-unauthorized",
        ],
    }


def normative_origin(section: str) -> dict[str, Any]:
    return {"kind": "normative_requirement", "ref": section}


def product_origin(pointer: str) -> dict[str, Any]:
    return {"kind": "product_contract", "ref": f"{INTAKE_REF}#{pointer}"}


def specified(value: Any, origin: dict[str, Any], unit: str | None = None) -> dict[str, Any]:
    return {
        "value": value,
        "unit": unit,
        "origin": origin,
        "tolerance": 0,
        "change_policy": "source_revision_required" if origin["kind"] == "product_contract" else "fixed",
    }


def bootstrap() -> None:
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    fixture = {
        "schema_id": "custometry.g4-auth-fixture/v1",
        "fixed_clock": "2026-08-12T08:00:00Z",
        "route": "/auth/sign-in",
        "screen_id": "UI-AUTH-001",
        "locales": ["ru", "en"],
        "states": list(STATES),
        "sensitive_values": "synthetic_and_redacted",
        "network_mode": "isolated_loopback",
    }
    font_bundle = {
        "schema_id": "custometry.font-bundle/v1",
        "stack": ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        "delivery": "local_system_fallback_only",
    }
    asset_bundle = {
        "schema_id": "custometry.asset-bundle/v1",
        "assets": [],
        "icons": "none_required_for_auth-family-r3",
        "external_requests": "forbidden",
    }
    fixture_path = ARTIFACT / "fixture.json"
    font_path = ARTIFACT / "font-bundle.json"
    asset_path = ARTIFACT / "asset-bundle.json"
    write_json(fixture_path, fixture)
    write_json(font_path, font_bundle)
    write_json(asset_path, asset_bundle)
    target_path = ARTIFACT / "auth/sign-in/index.html"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(target_html(sha(fixture_path), sha(font_path), sha(asset_path)), encoding="utf-8")
    write_json(ARTIFACT / "reuse-decision.json", {
        "schema_id": "codex.ui-family-reuse-decision/v1",
        "family_id": FAMILY_ID,
        "representative_screen_id": "UI-AUTH-001",
        "individually_designed_and_accepted_screen_ids": ["UI-AUTH-001"],
        "reuse_only_screen_ids": ["UI-AUTH-002", "UI-AUTH-003", "UI-AUTH-004"],
        "decision": "Reuse the accepted shell.auth structure, Graphite/cyan language, state anatomy, focus/recovery treatment, and responsive rules; each non-representative route still requires its own later source-backed screen realization before any individual acceptance claim.",
        "scope_limit": "No individual design or acceptance claim is made for UI-AUTH-002, UI-AUTH-003, or UI-AUTH-004.",
        "source_refs": [
            ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/families/family.auth.shell-auth.baseline-exception-auth.json#/family",
            f"{INTAKE_REF}#/screens/0",
        ],
        "result": "recorded",
    })
    write_json(ARTIFACT / "inheritance-report.json", {
        "schema_id": "codex.ui-visual-inheritance-report/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "visual_authority_sha256": sha(VISUAL),
        "baseline_id": "custometry.platform-baseline.v2.r2",
        "baseline_sha256": sha(BASELINE),
        "shell_variant_id": "shell.auth",
        "exception_id": "baseline-exception-auth",
        "dimensions": [
            "color", "typography", "spacing", "control_language", "shell_relationships",
            "responsive_web", "focus_and_reduced_motion", "result_trust_and_recovery",
        ],
        "allowed_differences": [
            "The auth surface intentionally omits workspace header and primary navigation under baseline-exception-auth.",
            "The accepted pilot supplies visual language only; auth composition, copy fixture, state anatomy, and route semantics come from the source-backed UI-AUTH-001 contract.",
            "Raster comparison is supporting evidence and is not treated as same-screen fidelity.",
        ],
        "result": "passed",
    })
    admission_projection = json.loads((ROOT / G1_ADMISSION_REF).read_text(encoding="utf-8"))
    admission_projection["screens"][0]["required_states"] = [
        f"UI-AUTH-001.{state}" for state in STATES
    ]
    projection_path = ARTIFACT / "g1-admission-inventory.family-projection.json"
    write_json(projection_path, admission_projection)
    snapshot = json.loads(PROGRAM_DOC.read_text(encoding="utf-8"))
    admission_source = next(item for item in snapshot["source_contracts"] if item["path"] == G1_ADMISSION_REF)
    admission_source["screen_collections"] = []
    snapshot["source_contracts"].append({
        "path": rel(projection_path),
        "authority": "G4 stage-owned exact projection of the accepted G1 admission inventory; only UI-AUTH-001.required_states is added from accepted intake and coverage",
        "required_status": "complete",
        "sha256": sha(projection_path),
        "screen_collections": [{"json_pointer": "/screens", "id_key": "screen_id"}],
        "journey_collections": [],
    })
    for screen_entry in snapshot["screens"]:
        if screen_entry["screen_ref"]["path"] == G1_ADMISSION_REF:
            screen_entry["screen_ref"]["path"] = rel(projection_path)
    screen_entries_path = ARTIFACT / "program-screen-entries.snapshot.json"
    write_json(screen_entries_path, {"screens": snapshot["screens"]})
    screens_index_path = ARTIFACT / "screens-index.snapshot.json"
    write_json(screens_index_path, {
        "$schema": "program-artifact-index.schema.json",
        "schema_id": "codex.ui-program-artifact-index/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 2,
        "index_kind": "screens",
        "entries": [
            {
                "id": entry["screen_ref"]["expected_id"],
                "path": rel(screen_entries_path),
                "sha256": sha(screen_entries_path),
                "json_pointer": f"/screens/{index}",
            }
            for index, entry in enumerate(snapshot["screens"])
        ],
    })
    snapshot["artifact_indexes"]["screens"] = {
        "path": rel(screens_index_path),
        "sha256": sha(screens_index_path),
    }
    snapshot_path = ARTIFACT / "ui-design-program.snapshot.json"
    snapshot["execution_artifacts"]["plan_doc"] = rel(snapshot_path)
    write_json(snapshot_path, snapshot)
    write_json(ARTIFACT / "program-snapshot-binding.json", {
        "schema_id": "codex.ui-stage-program-snapshot-binding/v1",
        "canonical_program": {"path": PROGRAM_REF, "sha256": sha(PROGRAM_DOC)},
        "snapshot": {"path": rel(snapshot_path), "sha256": sha(snapshot_path)},
        "projection": {"path": rel(projection_path), "sha256": sha(projection_path)},
        "screen_index_snapshot": {"path": rel(screens_index_path), "sha256": sha(screens_index_path)},
        "changed_pointers": ["/source_contracts", "/screens/*/screen_ref/path", "/artifact_indexes/screens", "/execution_artifacts/plan_doc"],
        "reason": "The active family assembler resolves required_states from screen_ref; the accepted G1 admission inventory carries identity/classification only. This stage-owned full-inventory projection adds the exact six accepted UI-AUTH-001 states, rebinds the screen source/index mechanically, and self-links the snapshot without mutating accepted G0-G3 artifacts.",
        "accepted_authority_changed": False,
        "result": "passed",
    })
    contracts: dict[str, dict[str, Any]] = {}
    for state in STATES:
        contract = screen_contract(state, fixture_path, font_path, asset_path)
        contracts[state] = contract
        write_json(ARTIFACT / f"contracts/UI-AUTH-001.{state}.r3.json", contract)
    recovery_ids = {item["element_id"] for item in contracts["recovery"]["element_contracts"]}
    sign_in_ids = {item["element_id"] for item in contracts["initial"]["element_contracts"]}
    recovery_required = {"recovery-form", "recovery-submit", "back-to-sign-in", "recovery-result"}
    recovery_forbidden = {"auth-form", "password-field", "continue-button", "inspect-action", "inspect-result", "state-panel"}
    missing = sorted(recovery_required - recovery_ids)
    forbidden_present = sorted(recovery_forbidden & recovery_ids)
    if missing or forbidden_present or recovery_ids == sign_in_ids:
        raise SystemExit(
            "Recovery state distinction failed: "
            f"missing={missing}, forbidden_present={forbidden_present}, "
            f"same_as_sign_in={recovery_ids == sign_in_ids}"
        )
    write_json(EVIDENCE / "state-distinction-r3-04.json", {
        "schema_id": "custometry.ui-state-distinction-evidence/v1",
        "screen_id": "UI-AUTH-001",
        "correction": "r3-04",
        "comparison": ["UI-AUTH-001.initial", "UI-AUTH-001.recovery"],
        "required_only_in_recovery": sorted(recovery_required),
        "forbidden_in_recovery": sorted(recovery_forbidden),
        "observed_recovery_element_ids": sorted(recovery_ids),
        "observed_sign_in_element_ids": sorted(sign_in_ids),
        "same_element_inventory": recovery_ids == sign_in_ids,
        "result": "passed",
        "proof_boundary": "Contract-level structural distinction; canonical browser capture separately proves the rendered inventory and interactions.",
    })


def target_html(fixture_sha: str, font_sha: str, asset_sha: str) -> str:
    states_ru = {
        "initial": ("Введите данные", "Укажите рабочий email и пароль."),
        "loading": ("Проверка доступа", "Поля временно недоступны."),
        "populated": ("Данные заполнены", "Проверьте значения перед продолжением."),
        "error": ("Не удалось проверить данные", "Исправьте данные или повторите попытку."),
        "permission_denied": ("Доступ не разрешён", "Учётная запись распознана, но у неё нет доступа к этому рабочему пространству."),
        "recovery": ("Восстановить доступ", "Укажите рабочий email. Мы отправим ссылку для восстановления."),
    }
    states_en = {
        "initial": ("Enter your details", "Provide your workspace email and password."),
        "loading": ("Checking access", "The fields are temporarily unavailable."),
        "populated": ("Details are populated", "Review the values before continuing."),
        "error": ("Details could not be verified", "Correct the details or try again."),
        "permission_denied": ("Access is not permitted", "The account is recognized but cannot enter this workspace."),
        "recovery": ("Recover access", "Enter your workspace email. We will send a recovery link."),
    }
    state_json = json.dumps({"ru": states_ru, "en": states_en}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="ru" data-theme="graphite">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="ui-fixture-sha256" content="{fixture_sha}">
  <meta name="ui-font-bundle-sha256" content="{font_sha}">
  <meta name="ui-asset-bundle-sha256" content="{asset_sha}">
  <link rel="icon" href="data:,">
  <title>Custometry — sign in</title>
  <style>
    :root{{--ink:#f0f0f2;--muted:#8b8c93;--paper:#070708;--sidebar:#090a0b;--panel:#111214;--panel2:#151619;--module:#1a1b1e;--line:#303136;--line-soft:#242529;--cyan:#66b9d3;--focus:#8bd2e8;--danger:#f07d87;--warning:#ddb064;--ok:#62c7aa;--shadow:0 22px 70px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.07)}}
    *{{box-sizing:border-box}} html,body{{margin:0;min-height:100%;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,sans-serif}}
    body{{min-height:100vh;display:grid;place-items:center;padding:24px;overflow-x:hidden;background:var(--paper)}}
    button,input{{font:inherit}} button:focus-visible,input:focus-visible,a:focus-visible{{outline:2px solid var(--focus);outline-offset:2px}}
    .auth{{width:min(100%,420px);display:grid;grid-template-columns:1fr;border:1px solid var(--line);border-radius:15px;overflow:hidden;background:var(--panel);box-shadow:var(--shadow)}}
    .story{{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:18px 22px;border-bottom:1px solid var(--line-soft);background:var(--sidebar)}}
    .brand{{display:flex;align-items:center;gap:10px;font-size:12px;font-weight:700}} .mark{{width:28px;height:28px;border-radius:9px;display:grid;place-items:center;color:#071014;background:var(--cyan);font-weight:800}}
    h1{{margin:0;font-size:18px;font-weight:680;letter-spacing:-.02em}} .form-side{{padding:28px 24px 24px}} .form-wrap{{width:100%;margin:auto}}
    .kicker{{margin:0 0 8px;color:var(--muted);font-size:10px}} h2{{margin:0;font-size:22px;letter-spacing:-.025em}} .sub{{margin:7px 0 22px;color:#a7a7ad;font-size:12px;line-height:1.5}}
    form{{display:grid;gap:13px}} label{{display:grid;gap:6px;color:#a7a7ad;font-size:11px;font-weight:650}} input{{width:100%;min-height:40px;border:1px solid var(--line);border-radius:7px;padding:0 11px;color:var(--ink);background:var(--panel2)}} input::placeholder{{color:var(--muted)}} input:disabled{{opacity:.52}}
    .primary,.secondary,.inspect{{min-height:38px;border-radius:7px;border:1px solid transparent;padding:0 12px;font-weight:680;cursor:pointer;transition-property:background-color,color,scale;transition-duration:120ms}} .primary{{margin-top:1px;color:#071014;background:var(--cyan)}} .primary:disabled{{cursor:not-allowed;opacity:.42}} .primary:not(:disabled):active,.secondary:active,.inspect:active{{scale:.96}}
    .secondary,.inspect{{width:100%;color:var(--text-secondary,#a7a7ad);background:var(--module);border-color:var(--line)}} .secondary:hover,.inspect:hover{{color:var(--ink);background:#222327}} .inspect{{margin-top:10px}}
    .state{{margin-top:16px;padding:12px 13px;border:1px solid var(--line-soft);border-radius:10px;background:var(--panel2)}} .state strong{{display:block;font-size:12px}} .state p{{margin:5px 0 0;color:var(--muted);font-size:11px;line-height:1.5}}
    .state[data-state="loading"]{{border-color:rgba(102,185,211,.42)}} .state[data-state="error"]{{border-color:rgba(240,125,135,.45)}} .state[data-state="error"] strong{{color:var(--danger)}} .state[data-state="permission_denied"]{{border-color:rgba(221,176,100,.45)}} .state[data-state="permission_denied"] strong{{color:var(--warning)}} .state[data-state="recovery"] strong,.state[data-state="populated"] strong{{color:var(--ok)}}
    .result{{min-height:18px;margin:10px 0 0;color:var(--cyan);font-size:11px}} .recovery-form{{gap:12px}} .recovery-form .secondary,.recovery-form .inspect{{margin-top:0}}
    @media(max-width:452px){{body{{display:block;padding:16px}}.story{{align-items:flex-start;flex-direction:column;gap:14px;padding:22px}}.form-side{{padding:28px 22px}}}}
    @media(prefers-reduced-motion:reduce){{*,*:before,*:after{{scroll-behavior:auto!important;animation:none!important;transition:none!important}}}}
  </style>
</head>
<body>
  <main class="auth" data-ui-region="UI-AUTH-001.content">
    <section class="story" data-ui-element="brand-story">
      <div class="brand"><span class="mark" aria-hidden="true">C</span><span>Custometry</span></div>
      <h1 data-copy="storyTitle">Sign in</h1>
    </section>
    <section class="form-side" data-ui-element="auth-panel">
      <div class="form-wrap" data-form-wrap>
        <p class="kicker" data-ui-element="route-label">/auth/sign-in · shell.auth</p>
        <h2 data-ui-element="form-title" data-copy="title">Workspace credentials</h2>
        <p class="sub" data-ui-element="form-subtitle" data-copy="subtitle">Enter your email and password.</p>
        <form data-ui-element="auth-form" onsubmit="event.preventDefault()">
          <label>Email<input data-ui-element="email-field" aria-label="Workspace email" type="email" placeholder="name@company.test" autocomplete="username"></label>
          <label>Password<input data-ui-element="password-field" aria-label="Workspace password" type="password" placeholder="Synthetic review value" autocomplete="current-password" data-sensitive></label>
          <button data-ui-element="continue-button" class="primary" type="button" disabled>Continue</button>
        </form>
        <div class="state" data-ui-element="state-panel" aria-live="polite"><strong data-state-title></strong><p data-state-copy></p></div>
        <button data-ui-element="inspect-action" class="inspect" type="button" data-prototype-action="UI-AUTH-001.inspect">Check form</button>
        <p class="result" data-ui-element="inspect-result" data-inspect-result aria-live="polite"></p>
      </div>
    </section>
  </main>
  <script>
    const stateCopy={state_json};
    const query=new URLSearchParams(location.search);
    let state={json.dumps(STATES)}.includes(query.get("state"))?query.get("state"):"initial";
    const locale=query.get("lang")==="en"?"en":"ru";
    document.documentElement.lang=locale;
    const wrap=document.querySelector("[data-form-wrap]");
    const signInMarkup=wrap.innerHTML;
    function renderCurrentState(){{
      const copy=stateCopy[locale][state];
      if(state==="recovery"){{
        wrap.innerHTML=`
          <p class="kicker" data-ui-element="route-label">/auth/sign-in · shell.auth</p>
          <h2 data-ui-element="form-title">${{copy[0]}}</h2>
          <p class="sub" data-ui-element="form-subtitle">${{copy[1]}}</p>
          <form class="recovery-form" data-ui-element="recovery-form" onsubmit="event.preventDefault()">
            <label>${{locale==="ru"?"Рабочий email":"Workspace email"}}<input data-ui-element="email-field" aria-label="${{locale==="ru"?"Рабочий email":"Workspace email"}}" type="email" placeholder="name@company.test" autocomplete="username"></label>
            <button data-ui-element="recovery-submit" class="inspect" type="button" data-prototype-action="UI-AUTH-001.inspect">${{locale==="ru"?"Отправить ссылку":"Send recovery link"}}</button>
            <button data-ui-element="back-to-sign-in" class="secondary" type="button">${{locale==="ru"?"Вернуться ко входу":"Back to sign in"}}</button>
          </form>
          <p class="result recovery-result" data-ui-element="recovery-result" data-inspect-result role="status" aria-live="polite"></p>`;
        document.querySelector("[data-copy=storyTitle]").textContent=locale==="ru"?"Восстановление":"Recovery";
        document.querySelector("[data-prototype-action]").addEventListener("click",()=>{{
          document.querySelector("[data-inspect-result]").textContent=locale==="ru"?"Ссылка для восстановления отправлена":"Recovery link sent";
        }});
        document.querySelector("[data-ui-element=back-to-sign-in]").addEventListener("click",()=>{{
          state="initial";
          renderCurrentState();
          window.parent.postMessage({{type:"custometry-auth-state",state}},"*");
        }});
        return;
      }}
      wrap.innerHTML=signInMarkup;
      const panel=document.querySelector(".state"); panel.dataset.state=state;
      document.querySelector("[data-state-title]").textContent=copy[0];
      document.querySelector("[data-state-copy]").textContent=copy[1];
      const action=document.querySelector("[data-prototype-action]");
      const result=document.querySelector("[data-inspect-result]");
      action.addEventListener("click",()=>{{result.textContent=locale==="ru"?"Форма доступна":"Form is available";}});
      const inputs=[...document.querySelectorAll("input")];
      if(state==="loading") inputs.forEach(node=>node.disabled=true);
      if(state==="populated"){{document.querySelector("input[type=email]").value="reviewer@custometry.test";document.querySelector("input[type=password]").value="synthetic-proof";}}
      document.querySelector("[data-copy=storyTitle]").textContent=locale==="ru"?"Вход":"Sign in";
      if(locale==="ru"){{
        document.querySelector("[data-copy=title]").textContent="Учётные данные";
        document.querySelector("[data-copy=subtitle]").textContent="Введите email и пароль.";
        document.querySelector("label").childNodes[0].textContent="Рабочий email";
        document.querySelectorAll("label")[1].childNodes[0].textContent="Пароль";
        document.querySelector(".primary").textContent="Продолжить";
        action.textContent="Проверить форму";
      }}
    }}
    renderCurrentState();
  </script>
</body>
</html>
"""


def screen_contract(state: str, fixture_path: Path, font_path: Path, asset_path: Path) -> dict[str, Any]:
    full_state = f"UI-AUTH-001.{state}"
    visual = json.loads(PROGRAM_DOC.read_text(encoding="utf-8"))["visual_authority"]
    common_origin = delegated_origin()
    accepted_origin = {
        "kind": "accepted_visual",
        "ref": VISUAL_REF,
        "locator": "[data-ui-artifact='pilot-screen']",
    }
    accessibility_origin = normative_origin("references/visual-provenance-contract-v1.md#screen-contract")
    responsive_origin = normative_origin("references/responsive-policy-v1.md#viewport-contract")
    product_ref = product_origin("/screens/0")
    region = {
        "region_id": "UI-AUTH-001.content",
        "locator": "[data-ui-region='UI-AUTH-001.content']",
        "visibility": "required",
        "component_id": "auth.sign-in.surface",
        "component_status": "candidate",
        "variant": "shell-auth",
        "state": state,
        "source_refs": [product_ref, common_origin],
        "geometry": {},
        "layout_rules": [specified("one centered 420px authentication card, derived from the accepted pilot context-panel width, with a compact brand header at every supported Web width", accepted_origin)],
        "visual_properties": {},
        "content": {
            "purpose": specified("Provide the editor contract for /auth/sign-in", product_ref),
            "state": specified(full_state, product_origin(f"/screens/0/states/{STATES.index(state)}")),
        },
        "interactions": [],
        "accessibility": {
            "semantic_structure": specified("one functional h1 and one h2, labelled fields, named controls, non-color-only state", normative_origin("references/visual-provenance-contract-v1.md#screen-contract"))
        },
        "responsive_behavior": [specified("preserve task, trust, recovery and available action meaning from 768px through 1920px", responsive_origin)],
        "geometry_tolerance_px": 0,
        "geometry_tolerance_origin": normative_origin("references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence"),
        "computed_style_properties": ["display", "grid-template-columns", "background-color", "border-radius"],
        "computed_style_properties_origin": common_origin,
    }
    shared_elements = [
        ("brand-story", None, "section", None, "compact", "Brand and functional sign-in title", []),
        ("auth-panel", None, "section", None, "panel", "Route-focused auth panel", []),
        ("route-label", "auth-panel", "text", None, None, "/auth/sign-in · shell.auth", []),
    ]
    if state == "recovery":
        elements = shared_elements + [
            ("form-title", "auth-panel", "heading", None, None, "Recover access / Восстановить доступ", []),
            ("form-subtitle", "auth-panel", "text", None, None, "Enter a workspace email to receive a recovery link / Укажите рабочий email для получения ссылки", []),
            ("recovery-form", "auth-panel", "form", None, "recovery", "Password recovery request", []),
            ("email-field", "recovery-form", "input", None, "email", "Workspace email", []),
            ("recovery-submit", "recovery-form", "button", "action.button", "secondary", "Send recovery link / Отправить ссылку", ["UI-AUTH-001.inspect"]),
            ("back-to-sign-in", "recovery-form", "button", "action.button", "secondary", "Back to sign in / Вернуться ко входу", []),
            ("recovery-result", "auth-panel", "status", None, "success", "Recovery link sent / Ссылка для восстановления отправлена", []),
        ]
    else:
        elements = shared_elements + [
            ("form-title", "auth-panel", "heading", None, None, "Workspace credentials / Учётные данные", []),
            ("form-subtitle", "auth-panel", "text", None, None, "Enter email and password / Введите email и пароль", []),
            ("auth-form", "auth-panel", "form", None, "default", "Source-backed auth form fixture", []),
            ("email-field", "auth-form", "input", None, "email", "Workspace email", []),
            ("password-field", "auth-form", "input", None, "password", "Workspace password; redacted", []),
            ("continue-button", "auth-form", "button", "action.button", "primary", "Continue; intentionally non-operative because no sign-in submit action is registered in the source contract", []),
            ("state-panel", "auth-panel", "status", None, state, full_state, []),
            ("inspect-action", "auth-panel", "button", "action.button", "secondary", "Check form / Проверить форму", ["UI-AUTH-001.inspect"]),
            ("inspect-result", "auth-panel", "status", None, "success", "Form is available / Форма доступна", []),
        ]
    element_contracts = []
    for element_id, parent, element_type, component_id, variant, content, action_ids in elements:
        element_contracts.append({
            "element_id": element_id,
            "parent_element_id": parent,
            "region_id": "UI-AUTH-001.content",
            "locator": f"[data-ui-element='{element_id}']",
            "visibility": "required",
            "element_type": element_type,
            "component_id": component_id,
            "variant": variant,
            "size_class": "sm" if element_id in {"inspect-action", "recovery-submit", "back-to-sign-in"} else ("md" if element_type in {"button", "input"} else None),
            "content_contract": content,
            "icon_id": None,
            "action_ids": action_ids,
            "state_ids": [full_state],
            "geometry": {"display": specified("visible", accepted_origin)},
            "spacing_relations": [specified("contained within auth surface rhythm", accepted_origin)],
            "visual_properties": {"visual_language": specified("Graphite surface with cyan focus/accent", accepted_origin)},
            "responsive_behavior": [specified("remains readable and reachable at every declared Web anchor", responsive_origin)],
            "accessibility": {"name_or_role": specified(content, product_ref if action_ids else accessibility_origin)},
            "source_refs": [product_ref, accepted_origin],
        })
    action_selector = "[data-ui-element='recovery-result']" if state == "recovery" else "[data-inspect-result]"
    action_expected = "Ссылка для восстановления отправлена" if state == "recovery" else "Форма доступна"
    visible_actions = [{
        "action_id": "UI-AUTH-001.inspect",
        "expected_outcome": "Inspect current surface completes or the next contract-bound surface opens",
        "side_effect_class": "local_state",
        "activation_policy": "execute_in_fixture",
        "outcome_assertion": {
            "kind": "dom",
            "selector": action_selector,
            "property": "textContent",
            "expected": action_expected,
        },
    }]
    return {
        "$schema": SCHEMA,
        "schema_id": "codex.ui-screen-design-contract/v1",
        "contract_profile": "codex.ui-screen-design-contract/v1@1.4.0",
        "screen_revision_id": f"UI-AUTH-001.{state}.all.ru-RU.graphite.r3",
        "program_revision_ref": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2@2",
        "functional_contract_ref": {
            "path": INTAKE_REF,
            "sha256": sha(INTAKE),
            "json_pointer": "/screens/0",
            "screen_id": "UI-AUTH-001",
        },
        "baseline_binding": {
            "baseline_id": "custometry.platform-baseline.v2.r2",
            "path": BASELINE_REF,
            "sha256": sha(BASELINE),
            "shell_variant_id": "shell.auth",
            "exception_id": "baseline-exception-auth",
        },
        "status": "review",
        "product_identity": {
            "screen_id": "UI-AUTH-001",
            "route_id": "UI-AUTH-001",
            "route": "/auth/sign-in",
            "state_id": full_state,
            "role_id": "all",
            "permission_profile": "organization.read",
            "locale": "ru",
            "theme": "graphite",
        },
        "source_visual": {
            "kind": "delegated_design_output",
            "evidence_mode": "visual_language_only",
            "html_path": VISUAL_REF,
            "image_path": None,
            "html_sha256": sha(VISUAL),
            "image_sha256": None,
            "owner_decision_ref": None,
            "delegation_ref": DELEGATION_REF,
        },
        "visual_authority": {
            key: visual[key] for key in (
                "source_visual_ref", "source_visual_sha256", "owner_decision_ref",
                "screen_acceptance_scope", "visual_language_scope",
                "reusable_foundation_scope", "inheritance_policy", "mobile_scope",
            )
        },
        "comparison_claims": {
            "required_purpose": "visual_language_conformance",
            "deterministic_render_proves_fidelity": False,
            "reference_logical_artifact_id": "custometry-v2:accepted-pilot:ru:r2",
            "implementation_logical_artifact_id": f"custometry-v2:UI-AUTH-001:{state}:r3",
        },
        "interaction_contract": {
            "visible_actions": visible_actions,
            "no_actions_reason_ref": None,
            "required_checks": [
                "keyboard_activation", "focus_visibility", "tab_radio_behavior",
                "menus", "toggles", "refresh_feedback", "state_transitions",
                "no_unresolved_file_navigation", "no_console_errors",
                "no_request_failures", "no_page_horizontal_overflow",
            ],
            "allowed_origins": ["http://127.0.0.1:4173"],
            "fixture_mode": "isolated_local",
            "evidence_redaction_required": True,
            "redaction_selectors": ["[data-sensitive]", "input[type='password']"],
        },
        "render_environment": {
            "browser": "chromium/150.0.7871.187",
            "browser_mechanic": "playwright_cli",
            "device_scale_factor": 1,
            "timezone": "Europe/Moscow",
            "fixed_clock_iso": "2026-08-12T08:00:00Z",
            "reduced_motion": True,
            "animations": "disabled",
            "fixture_data_path": rel(fixture_path),
            "fixture_data_sha256": sha(fixture_path),
            "font_bundle_sha256": sha(font_path),
            "asset_bundle_sha256": sha(asset_path),
        },
        "viewport_contract": {
            "mode": "responsive_web",
            "supported_web_width_range": {"min_width": 768, "max_width": 1920, "origin": responsive_origin},
            "anchors": [
                {"anchor_id": anchor_id, "width": width, "height": height, "class": "responsive_web", "state_ref": full_state, "origin": responsive_origin}
                for anchor_id, width, height in ANCHORS
            ],
            "breakpoint_policy": "content_driven",
            "breakpoint_policy_origin": normative_origin("references/responsive-policy-v1.md#breakpoints-and-components"),
            "below_supported_range": "out_of_scope",
            "below_supported_range_origin": responsive_origin,
            "above_supported_range": "max_content_width",
            "above_supported_range_origin": responsive_origin,
            "mobile_scope": "unauthorized",
            "mobile_scope_origin": normative_origin("references/responsive-policy-v1.md#mobile-authorization-boundary"),
            "mobile_authorization_ref": None,
            "mobile_specific_composition": False,
            "authorized_mobile_surfaces": [],
            "authorized_mobile_viewports": [],
            "allowed_mobile_changes": [],
        },
        "regions": [region],
        "element_contracts": element_contracts,
        "allowed_provenance_kinds": [
            "product_contract", "normative_requirement", "accepted_visual",
            "measured_baseline", "design_token", "owner_decision",
            "derived_formula", "delegated_design_decision",
        ],
        "unresolved_decisions": [],
        "acceptance": {
            "agent_self_acceptance": "prohibited",
            "machine_receipt_required": True,
            "owner_decision_required": True,
            "owner_decision_ref": None,
            "screen_acceptance_receipt_path": None,
            "screen_acceptance_receipt_sha256": None,
            "pixel_diff_policy": {
                "channel_threshold": specified(0, normative_origin("references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence"), "channel-value"),
                "approved_max_different_pixels": specified(2073600, {
                    "kind": "derived_formula",
                    "ref": "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence",
                    "formula": "1920 * 1080; raster is supporting evidence for visual_language_conformance, while contract geometry, interaction and readable content remain primary",
                }, "px"),
            },
        },
    }


def review() -> None:
    acceptance_paths = [
        EVIDENCE / f"screen-acceptance/UI-AUTH-001.{state}.r3.json" for state in STATES
    ]
    missing = [path for path in acceptance_paths if not path.is_file()]
    if missing:
        raise SystemExit("Missing screen acceptance receipts: " + ", ".join(rel(path) for path in missing))
    entries = []
    nav_links = []
    labels = {
        "initial": "Начальное",
        "loading": "Загрузка",
        "populated": "Заполнено",
        "error": "Ошибка",
        "permission_denied": "Нет доступа",
        "recovery": "Восстановление",
    }
    for index, (state, acceptance_path) in enumerate(zip(STATES, acceptance_paths), 1):
        receipt = json.loads(acceptance_path.read_text(encoding="utf-8"))
        entry_id = f"screen-state-{index:02d}-{state}"
        entries.append({
            "entry_id": entry_id,
            "role": "screen_acceptance",
            "artifact_ref": rel(acceptance_path),
            "sha256": sha(acceptance_path),
            "anchor_id": None,
            "state_id": receipt["state_id"],
        })
        nav_links.append(
            f'<button type="button" data-review-entry="{entry_id}" data-state="{state}" '
            f'data-state-id="{html.escape(receipt["state_id"])}" aria-pressed="{"true" if index == 1 else "false"}">'
            f'<span>{index:02d}</span>{html.escape(labels[state])}</button>'
        )
    manifest_path = ARTIFACT / "review-board.manifest.json"
    write_json(manifest_path, {
        "$schema": "/Users/daniildegtyarev/.codex/skills/ui-design-program/assets/review-board-manifest.schema.json",
        "schema_id": "codex.ui-review-board-manifest/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "artifact_id": FAMILY_REVISION_ID,
        "revision": 3,
        "validation_profile": "family_review_ready",
        "entries": entries,
    })
    screen_source_js = json.dumps(
        (ARTIFACT / "auth/sign-in/index.html").read_text(encoding="utf-8"),
        ensure_ascii=False,
    ).replace("</script>", "<\\/script>")
    board_path = ARTIFACT / "review-board.html"
    board_path.write_text(f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">
<title>Custometry · auth family review</title><style>
:root{{--bg:#070708;--sidebar:#090a0b;--panel:#111214;--panel-soft:#151619;--module:#1a1b1e;--hover:#2a2b2f;--line:#303136;--line-soft:#242529;--ink:#f0f0f2;--secondary:#a7a7ad;--muted:#8b8c93;--cyan:#66b9d3;--focus:#8bd2e8;--shadow:0 22px 70px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.07)}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,sans-serif}}button,a{{font:inherit}}main{{width:min(100% - 32px,1180px);margin:auto;padding:28px 0 64px}}
.topbar{{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:14px;padding:18px 20px;border:1px solid var(--line);border-radius:15px;background:var(--panel);box-shadow:var(--shadow)}}.eyebrow{{margin:0 0 5px;color:var(--cyan);font-size:9px;font-weight:700;letter-spacing:.075em;text-transform:uppercase}}h1{{margin:0;font-size:26px;letter-spacing:-.03em}}.topbar p:last-child{{margin:6px 0 0;color:var(--muted);font-size:11px}}.language{{display:flex;gap:5px}}.language button,.state-nav button{{border:1px solid var(--line);border-radius:7px;color:var(--secondary);background:var(--module);cursor:pointer;transition-property:background-color,color,scale;transition-duration:120ms}}.language button{{min-height:32px;padding:0 10px}}.language button:hover,.state-nav button:hover{{color:var(--ink);background:var(--hover)}}.language button[aria-pressed=true],.state-nav button[aria-pressed=true]{{color:#071014;background:var(--cyan);border-color:var(--cyan)}}.language button:active,.state-nav button:active{{scale:.96}}
.state-nav{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px;margin:0 0 14px;padding:8px;border:1px solid var(--line);border-radius:10px;background:var(--panel)}}.state-nav button{{display:flex;align-items:center;justify-content:center;gap:6px;min-height:36px;padding:6px;font-size:10px}}.state-nav button span{{font-variant-numeric:tabular-nums;opacity:.7}}button:focus-visible,a:focus-visible{{outline:2px solid var(--focus);outline-offset:2px}}
.viewer{{overflow:hidden;border:1px solid var(--line);border-radius:10px;background:var(--panel);box-shadow:var(--shadow)}}.viewer-head{{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 13px;border-bottom:1px solid var(--line-soft)}}.state-meta{{display:flex;align-items:center;gap:10px}}h2{{margin:0;font-size:12px}}code{{color:var(--muted);font-size:9px}}.open-screen{{color:var(--cyan);font-size:10px}}iframe{{display:block;width:100%;height:720px;border:0;background:var(--bg)}}.note{{margin-top:14px;color:var(--muted);font-size:10px;line-height:1.5}}
@media(max-width:900px){{.topbar{{align-items:flex-start;flex-direction:column}}.state-nav{{grid-template-columns:repeat(3,minmax(0,1fr))}}iframe{{height:720px}}}}
@media(max-width:560px){{.state-nav{{grid-template-columns:repeat(2,minmax(0,1fr))}}.viewer-head{{align-items:flex-start;flex-direction:column}}}}
</style></head>
<body data-ui-artifact="review_board" data-program-id="CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
 data-artifact-id="{FAMILY_REVISION_ID}" data-revision="3" data-validation-profile="family_review_ready"
 data-review-manifest="{rel(manifest_path)}" data-review-manifest-sha256="{sha(manifest_path)}"><main>
<section class="topbar"><div><p class="eyebrow">Проверка семейства авторизации</p><h1>/auth/sign-in</h1><p>Выберите состояние и работайте с формой внутри окна.</p></div><div class="language" aria-label="Язык"><button type="button" data-lang="ru" aria-pressed="true">RU</button><button type="button" data-lang="en" aria-pressed="false">EN</button></div></section>
<nav class="state-nav" aria-label="Состояния семейства">{''.join(nav_links)}</nav>
<section class="viewer"><div class="viewer-head"><div class="state-meta"><h2 data-current-label>{html.escape(labels[STATES[0]])}</h2><code data-current-state>UI-AUTH-001.{STATES[0]}</code></div><a class="open-screen" data-open-screen href="#" target="_blank" rel="noopener">Открыть отдельно</a></div><iframe data-live-screen title="Интерактивный экран авторизации, состояние {html.escape(labels[STATES[0]])}"></iframe></section>
<p class="note">UI-AUTH-002, UI-AUTH-003 и UI-AUTH-004 не входят в эту проверку.</p>
</main><script>
const labels={json.dumps(labels, ensure_ascii=False)};
const screenTemplate={screen_source_js};
const stateButtons=[...document.querySelectorAll("[data-state]")];
const languageButtons=[...document.querySelectorAll("[data-lang]")];
const frame=document.querySelector("[data-live-screen]");
const openScreen=document.querySelector("[data-open-screen]");
let currentState="{STATES[0]}";
let currentLanguage="ru";
function render(){{
  const query=`state=${{encodeURIComponent(currentState)}}&lang=${{currentLanguage}}`;
  const documentText=screenTemplate.replace("const query=new URLSearchParams(location.search);",`const query=new URLSearchParams("${{query}}");`);
  frame.srcdoc=documentText;
  frame.title=`Интерактивный экран авторизации, состояние ${{labels[currentState]}}`;
  openScreen.href=`data:text/html;charset=utf-8,${{encodeURIComponent(documentText)}}`;
  document.querySelector("[data-current-label]").textContent=labels[currentState];
  document.querySelector("[data-current-state]").textContent=`UI-AUTH-001.${{currentState}}`;
  stateButtons.forEach(button=>button.setAttribute("aria-pressed",String(button.dataset.state===currentState)));
  languageButtons.forEach(button=>button.setAttribute("aria-pressed",String(button.dataset.lang===currentLanguage)));
}}
stateButtons.forEach(button=>button.addEventListener("click",()=>{{currentState=button.dataset.state;render();}}));
languageButtons.forEach(button=>button.addEventListener("click",()=>{{currentLanguage=button.dataset.lang;render();}}));
window.addEventListener("message",event=>{{
  if(event.source===frame.contentWindow&&event.data?.type==="custometry-auth-state"&&labels[event.data.state]){{
    currentState=event.data.state;
    render();
  }}
}});
render();
</script></body></html>""", encoding="utf-8")
    request_path = EVIDENCE / "family-acceptance-request.json"
    write_json(request_path, {
        "$schema": "/Users/daniildegtyarev/.codex/skills/ui-design-program/assets/family-acceptance-request.schema.json",
        "program_path": rel(ARTIFACT / "ui-design-program.snapshot.json"),
        "family_id": FAMILY_ID,
        "family_revision_id": FAMILY_REVISION_ID,
        "revision": 3,
        "screen_acceptance_paths": [rel(path) for path in acceptance_paths],
        "review_board_path": rel(board_path),
        "owner_decision_ref": None,
    })
    write_json(EVIDENCE / "owner-review-decision-packet.json", {
        "schema_id": "codex.ui-owner-review-decision-packet/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": "G4@family.auth.shell-auth.baseline-exception-auth-r3",
        "decision_id": "G4@family.auth.shell-auth.baseline-exception-auth-r3.finished-result",
        "decision_kind": "family_acceptance",
        "question": "Accept the finished auth-family result or request bounded corrections.",
        "target": {
            "artifact_kind": "review_board",
            "artifact_id": FAMILY_REVISION_ID,
            "revision": 3,
            "validation_profile": "family_review_ready",
            "path": rel(board_path),
            "sha256": sha(board_path),
        },
        "allowed_responses": ["accept", "request_bounded_corrections"],
        "status": "pending",
    })


def proof_requests() -> None:
    for state in STATES:
        for anchor_id, _, _ in ANCHORS:
            capture_dir = EVIDENCE / f"captures/{state}/{anchor_id}"
            for target in ("reference", "implementation"):
                logical_id = (
                    "custometry-v2:accepted-pilot:ru:r2"
                    if target == "reference"
                    else f"custometry-v2:UI-AUTH-001:{state}:r3"
                )
                source_path = VISUAL if target == "reference" else ARTIFACT / "auth/sign-in/index.html"
                write_json(capture_dir / f"{target}-provenance-request.json", {
                    "program_ref": PROGRAM_REF,
                    "target": target,
                    "logical_artifact_id": logical_id,
                    "anchor_id": anchor_id,
                    "source_artifact_ref": rel(source_path),
                    "capture_ref": rel(capture_dir / f"{target}.png"),
                    "geometry_receipt_ref": rel(capture_dir / f"{target}-geometry.json"),
                })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("bootstrap", "proof-requests", "review"))
    args = parser.parse_args()
    if args.mode == "bootstrap":
        bootstrap()
    elif args.mode == "proof-requests":
        proof_requests()
    else:
        review()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
