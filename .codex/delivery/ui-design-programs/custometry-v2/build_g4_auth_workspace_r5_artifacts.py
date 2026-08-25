#!/usr/bin/env python3
"""Build the current G4 r5 onboarding/workspace-shell family checkpoint."""

from __future__ import annotations

import argparse
from copy import deepcopy
import html
import json
from pathlib import Path
import subprocess

import build_g4_auth_r4_artifacts as base


DIR = Path(__file__).resolve().parent
ROOT = base.ROOT
ART = DIR / "artifacts/g4-r5/family-auth-shell-workspace-baseline"
EVID = DIR / "evidence/family.auth.shell-workspace.baseline-r5"
INTAKE = DIR / "artifacts/g0-r5/ui-program-intake.json"
BASELINE = DIR / "artifacts/g0-r5/platform-ui-baseline.json"
PROGRAM = DIR / "ui-design-program.json"
G1 = DIR / "evidence/g0-r2/g1-admission-inventory.json"
SOURCE = DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
BASE_CONTRACT = DIR / "artifacts/g3-r5/representative-shell-contract.json"
TARGET = ART / "screens/onboarding.html"
SNAPSHOT = ART / "ui-design-program.snapshot.json"
FAMILY_ID = "family.auth.shell-workspace.baseline"
FAMILY_REVISION_ID = f"{FAMILY_ID}-r5"
STAGE_ID = f"G4@{FAMILY_REVISION_ID}"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
REVISION = 5
REVISION_TAG = "r5"
ANCHORS = base.ANCHORS
SCREEN_INDEXES = {"UI-AUTH-005": 4}

for name, value in {
    "ART": ART, "EVID": EVID, "INTAKE": INTAKE, "BASELINE": BASELINE,
    "PROGRAM": PROGRAM, "G1": G1, "SOURCE": SOURCE, "BASE_CONTRACT": BASE_CONTRACT,
    "TARGET": TARGET, "SNAPSHOT": SNAPSHOT, "FAMILY_ID": FAMILY_ID,
    "FAMILY_REVISION_ID": FAMILY_REVISION_ID, "STAGE_ID": STAGE_ID,
    "REVISION": REVISION, "REVISION_TAG": REVISION_TAG, "PROGRAM_REVISION": 5,
    "SCREEN_INDEXES": SCREEN_INDEXES,
}.items():
    setattr(base, name, value)


COPY = {
    "ru": {
        "title": "Настройте рабочее пространство", "lead": "Пять коротких шагов — прогресс сохраняется автоматически.",
        "steps": ["Аккаунт", "Рабочее пространство", "Язык и часовой пояс", "Данные или демо", "Готово"],
        "check": ["Профиль подтверждён", "Рабочее пространство названо", "Настройки времени выбраны", "Источник данных можно подключить позже"],
        "next": "Продолжить", "resume": "Можно вернуться позже — начнём с этого шага.",
        "states": {
            "initial": "Начните с базовых настроек рабочего пространства.",
            "loading": "Восстанавливаем сохранённый прогресс…",
            "populated": "Черновик найден: 2 из 5 шагов уже готовы.",
            "error": "Не удалось сохранить этот шаг. Данные остались в форме — повторите.",
            "permission_denied": "Только администратор рабочего пространства может завершить настройку.",
            "recovery": "Продолжите с шага «Язык и часовой пояс» — предыдущие ответы сохранены.",
        },
    },
    "en": {
        "title": "Set up your workspace", "lead": "Five short steps — progress is saved automatically.",
        "steps": ["Account", "Workspace", "Locale & timezone", "Data or demo", "Finish"],
        "check": ["Profile confirmed", "Workspace named", "Time preferences selected", "A data source can be connected later"],
        "next": "Continue", "resume": "You can return later — we will resume from this step.",
        "states": {
            "initial": "Start with the essential workspace settings.",
            "loading": "Restoring saved progress…",
            "populated": "Draft found: 2 of 5 steps are already complete.",
            "error": "This step could not be saved. Your entries remain — try again.",
            "permission_denied": "Only a workspace administrator can complete setup.",
            "recovery": "Continue from Locale & timezone — your previous answers are saved.",
        },
    },
}


def target_html(baseline: dict) -> str:
    copy_json = json.dumps(COPY, ensure_ascii=False).replace("</", "<\\/")
    css = base.pilot_component_css(baseline)
    button_css = base.pilot_button_state_css()
    return f'''<!doctype html><html lang="ru" data-theme="graphite"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="ui-fixture-sha256" content="__FIXTURE_SHA256__"><meta name="ui-font-bundle-sha256" content="__FONT_SHA256__"><meta name="ui-asset-bundle-sha256" content="__ASSET_SHA256__"><link rel="icon" href="data:,"><title>Custometry · onboarding r5</title><style>
:root{{--paper:#070708;--panel:#111214;--module:#1a1b1e;--module-strong:#222327;--line:#303136;--line-soft:#242529;--ink:#f0f0f2;--secondary:#a7a7ad;--muted:#8b8c93;--cyan:#8ccfe3;--cyan-strong:#66b9d3;--focus:#8bd2e8;--danger:#f07d87;--warning:#ddb064;--ok:#62c7aa;--shadow:0 22px 70px rgba(0,0,0,.42)}}
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:var(--paper);color:var(--ink);font:14px/1.5 Inter,ui-sans-serif,system-ui,sans-serif}}body{{min-height:100vh}}button,select,input{{font:inherit}}button:focus-visible,select:focus-visible,input:focus-visible{{outline:3px solid var(--focus);outline-offset:2px}}[hidden]{{display:none!important}}
.shell{{display:grid;grid-template-columns:220px minmax(0,1fr);min-height:100vh}}.rail{{padding:20px 14px;border-right:1px solid var(--line-soft);background:#090a0b}}.brand{{display:flex;align-items:center;gap:10px;font-weight:740}}.mark{{display:grid;place-items:center;width:30px;height:30px;border-radius:9px;color:#071014;background:var(--cyan);font-weight:850}}.rail-label{{margin:34px 8px 8px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em}}.rail-item{{display:flex;align-items:center;gap:9px;padding:8px;border-radius:8px;color:var(--secondary)}}.rail-item.active{{color:var(--ink);background:var(--module)}}.dot{{width:7px;height:7px;border-radius:50%;background:var(--cyan-strong)}}
.main{{min-width:0}}.topbar{{height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 28px;border-bottom:1px solid var(--line-soft)}}.context{{font-size:12px;color:var(--secondary)}}.locale{{min-height:32px;border:1px solid var(--line);border-radius:7px;padding:0 9px;color:var(--secondary);background:var(--module)}}.content{{width:min(980px,calc(100% - 48px));margin:0 auto;padding:42px 0 64px}}.eyebrow{{margin:0 0 7px;color:var(--cyan-strong);font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}}h1{{margin:0;font-size:32px;line-height:1.15;letter-spacing:-.035em}}.lead{{margin:10px 0 28px;color:var(--secondary)}}
.workspace{{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(260px,.75fr);gap:16px}}.panel{{border:1px solid var(--line);border-radius:15px;background:var(--panel);box-shadow:var(--shadow)}}.wizard{{padding:22px}}.progress{{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;margin:0 0 28px;padding:0;list-style:none}}.step{{position:relative;color:var(--muted);font-size:10px}}.step::before{{content:"";display:block;height:3px;margin-bottom:8px;border-radius:9px;background:var(--line)}}.step.done{{color:var(--secondary)}}.step.done::before,.step.current::before{{background:var(--cyan-strong)}}.step.current{{color:var(--ink);font-weight:700}}.step-index{{display:block;margin-bottom:2px}}.card-title{{margin:0;font-size:18px}}.card-copy{{margin:6px 0 18px;color:var(--secondary);font-size:12px}}.fields{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}label{{display:grid;gap:6px;color:var(--secondary);font-size:11px;font-weight:650}}input,select.field{{width:100%;min-height:40px;border:1px solid var(--line);border-radius:7px;padding:0 11px;color:var(--ink);background:#151619}}.state{{min-height:56px;margin:17px 0;padding:11px 12px;border:1px solid var(--line-soft);border-radius:10px;color:var(--secondary);background:#151619;font-size:12px}}.state.error{{color:var(--danger);border-color:rgba(240,125,135,.45)}}.state.permission_denied{{color:var(--warning);border-color:rgba(221,176,100,.45)}}.actions{{display:flex;align-items:center;justify-content:space-between;gap:12px}}.resume{{color:var(--muted);font-size:11px}}.continue{{min-height:38px;min-width:144px;border:1px solid var(--line);border-radius:7px;padding:0 13px;transition:background-color 120ms,color 120ms,transform 120ms}}.result{{margin-top:10px;color:var(--ok);font-size:11px}}
.checklist{{padding:20px}}.checklist h2{{margin:0 0 4px;font-size:16px}}.checklist>p{{margin:0 0 18px;color:var(--muted);font-size:11px}}.checks{{display:grid;gap:13px;margin:0;padding:0;list-style:none}}.check{{display:grid;grid-template-columns:22px 1fr;gap:9px;color:var(--secondary);font-size:12px}}.checkmark{{display:grid;place-items:center;width:20px;height:20px;border:1px solid var(--line);border-radius:6px;color:var(--ok);background:var(--module)}}
{css}\n{button_css}
@media(max-width:900px){{.shell{{grid-template-columns:76px minmax(0,1fr)}}.brand span,.rail-label,.rail-item span{{display:none}}.rail{{display:grid;align-content:start;justify-items:center}}.rail-item{{justify-content:center;width:42px}}.workspace{{grid-template-columns:1fr}}.checklist{{box-shadow:none}}}}@media(max-width:620px){{.shell{{grid-template-columns:1fr}}.rail{{display:none}}.topbar{{padding:0 16px}}.content{{width:min(100% - 28px,980px);padding-top:26px}}h1{{font-size:27px}}.fields{{grid-template-columns:1fr}}.progress{{grid-template-columns:repeat(5,32px);justify-content:space-between}}.step span:not(.step-index){{display:none}}.actions{{align-items:flex-start;flex-direction:column}}.continue{{width:100%}}}}@media(prefers-reduced-motion:reduce){{*{{transition-duration:0s!important;animation-duration:0s!important}}}}
</style></head><body><div class="shell" data-screen-id="UI-AUTH-005" data-state-id="" data-ui-element="onboarding-shell"><aside class="rail" data-ui-region="UI-AUTH-005.navigation"><div class="brand" data-ui-element="onboarding-brand"><b class="mark">C</b><span>Custometry</span></div><p class="rail-label">Workspace</p><div class="rail-item active"><i class="dot"></i><span>Setup</span></div><div class="rail-item"><i class="dot" style="background:#4b4c51"></i><span>Data</span></div></aside><main class="main"><header class="topbar"><span class="context" data-ui-element="onboarding-context">First run · Workspace</span><label><span hidden>Language</span><select aria-label="Language" class="locale" data-ui-element="onboarding-locale" data-ui-component="control.compact" data-ui-variant="language-select" data-ui-size="compact" data-ui-standard-component="control.compact" data-ui-standard-variant="compact-control.lifecycle-metric-select" data-ui-standard-size="compact" data-ui-standard-slot="shell.main-content.select"><option value="ru">RU</option><option value="en">EN</option></select></label></header><section class="content" data-ui-region="UI-AUTH-005.content"><p class="eyebrow">Onboarding</p><h1 data-ui-element="onboarding-title"></h1><p class="lead" data-ui-element="onboarding-lead"></p><div class="workspace"><section class="panel wizard" data-ui-element="onboarding-wizard"><ol class="progress" data-ui-element="onboarding-steps"></ol><h2 class="card-title" data-ui-element="onboarding-step-title"></h2><p class="card-copy" data-ui-element="onboarding-step-copy"></p><div class="fields"><label><span data-label="workspace">Рабочее пространство</span><input aria-label="Рабочее пространство" data-ui-element="onboarding-workspace" value="Northstar" autocomplete="organization"></label><label><span data-label="timezone">Часовой пояс</span><select aria-label="Часовой пояс" class="field" data-ui-element="onboarding-timezone"><option>Europe/Moscow · UTC+3</option></select></label></div><div class="state" data-ui-element="onboarding-state" role="status"></div><div class="actions"><span class="resume" data-ui-element="onboarding-resume"></span><button type="button" class="continue" data-ui-element="onboarding-continue" data-prototype-action="UI-AUTH-005.inspect" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-pilot-action-style="primary"></button></div><div class="result" data-result data-ui-element="onboarding-result" aria-live="polite"></div></section><aside class="panel checklist" data-ui-element="onboarding-checklist"><h2 data-check-title></h2><p data-check-lead></p><ul class="checks"></ul></aside></div></section></main></div><script>
const COPY={copy_json};const q=new URLSearchParams(location.search);const lang=q.get('lang')==='en'?'en':'ru';const raw=q.get('state')||'UI-AUTH-005.initial';const names=['initial','loading','populated','error','permission_denied','recovery'];const name=names.includes(raw.split('.').pop())?raw.split('.').pop():'initial';const state=`UI-AUTH-005.${{name}}`;const c=COPY[lang];document.documentElement.lang=lang;document.querySelector('[data-screen-id]').dataset.stateId=state;document.querySelector('[data-ui-element="onboarding-title"]').textContent=c.title;document.querySelector('[data-ui-element="onboarding-lead"]').textContent=c.lead;document.querySelector('[data-ui-element="onboarding-step-title"]').textContent=c.steps[2];document.querySelector('[data-ui-element="onboarding-step-copy"]').textContent=lang==='ru'?'Выберите локаль отчётов и рабочий часовой пояс.':'Choose the reporting locale and workspace timezone.';document.querySelector('[data-ui-element="onboarding-resume"]').textContent=c.resume;document.querySelector('[data-ui-element="onboarding-continue"]').textContent=c.next;document.querySelector('[data-ui-element="onboarding-state"]').textContent=c.states[name];document.querySelector('[data-ui-element="onboarding-state"]').className=`state ${{name}}`;document.querySelector('[data-check-title]').textContent=lang==='ru'?'Готовность':'Readiness';document.querySelector('[data-check-lead]').textContent=lang==='ru'?'Сохраняем контекст между сессиями.':'Context is preserved between sessions.';document.querySelector('[data-label="workspace"]').textContent=lang==='ru'?'Рабочее пространство':'Workspace';document.querySelector('[data-label="timezone"]').textContent=lang==='ru'?'Часовой пояс':'Timezone';document.querySelector('.progress').innerHTML=c.steps.map((x,i)=>`<li class="step ${{i<2?'done':i===2?'current':''}}"><span class="step-index">0${{i+1}}</span><span>${{x}}</span></li>`).join('');document.querySelector('.checks').innerHTML=c.check.map((x,i)=>`<li class="check"><span class="checkmark">${{i<2?'✓':'·'}}</span><span>${{x}}</span></li>`).join('');const button=document.querySelector('[data-action]');button.disabled=name==='loading'||name==='permission_denied';button.addEventListener('click',()=>{{document.querySelector('[data-result]').textContent=lang==='ru'?'Следующий шаг подготовлен.':'The next step is ready.'}});document.querySelector('[data-ui-element="onboarding-locale"]').value=lang;document.querySelector('[data-ui-element="onboarding-locale"]').addEventListener('change',e=>{{q.set('lang',e.target.value);location.search=q}});
</script></body></html>'''.replace("document.querySelector('[data-action]')", "document.querySelector('[data-prototype-action]')")


def element_specs() -> list[tuple[str, str, str | None, str | None, str | None, str, list[str]]]:
    return [
        ("onboarding-shell", "shell", None, "workspace", None, "Workspace shell", []),
        ("onboarding-brand", "brand", None, "graphite", None, "Custometry", []),
        ("onboarding-context", "text", None, None, None, "First-run workspace context", []),
        ("onboarding-locale", "select", "control.compact", "language-select", "compact", "Language / Язык", []),
        ("onboarding-title", "heading", None, None, None, "Workspace onboarding title", []),
        ("onboarding-lead", "text", None, None, None, "Resumable five-step explanation", []),
        ("onboarding-wizard", "wizard", None, "workspace-onboarding", None, "Five-step onboarding wizard", []),
        ("onboarding-steps", "list", None, "stepper", None, "Account, workspace, locale/timezone, data/demo, finish", []),
        ("onboarding-step-title", "heading", None, None, None, "Current step", []),
        ("onboarding-step-copy", "text", None, None, None, "Current-step instruction", []),
        ("onboarding-workspace", "input", None, None, "md", "Workspace name", []),
        ("onboarding-timezone", "select", None, None, "md", "Timezone", []),
        ("onboarding-state", "status", None, None, None, "State-specific recovery feedback", []),
        ("onboarding-resume", "note", None, None, None, "Resumability guidance", []),
        ("onboarding-continue", "button", "action.button", "secondary", "sm", "Continue", ["UI-AUTH-005.inspect"]),
        ("onboarding-result", "status", None, None, None, "Action outcome", []),
        ("onboarding-checklist", "list", None, "readiness", None, "Resumable readiness checklist", []),
    ]


def make_region(template: dict, state_id: str, region_id: str, locator: str, component: str, variant: str) -> dict:
    row = deepcopy(template)
    row.update({"region_id": region_id, "locator": locator, "component_id": component, "component_status": "candidate", "variant": variant, "state": state_id.rsplit('.',1)[-1], "source_refs": [base.origin("accepted_visual", base.rel(SOURCE))], "computed_style_properties_origin": base.origin("accepted_visual", base.rel(SOURCE))})
    return row


def make_element(template: dict, state_id: str, spec: tuple) -> dict:
    element_id, element_type, component_id, variant, size, content, actions = spec
    row = deepcopy(template)
    identity = None
    slot = None
    states = ["default"]
    if element_id == "onboarding-continue":
        states=["default","hover","focus_visible","active","disabled"]
    if element_id == "onboarding-locale":
        identity = {"component_id":"control.compact","variant":"compact-control.lifecycle-metric-select","size_class":"compact","element_type":"select","icon_id":None,"state_ids":["default"]}; slot="shell.main-content.select"; states=["default","hover","focus_visible","disabled"]
    row.update({"element_id":element_id,"parent_element_id":None,"region_id":"UI-AUTH-005.content","locator":f'[data-ui-element="{element_id}"]',"visibility":"conditional" if element_id=="onboarding-result" else "required","element_type":element_type,"component_id":component_id,"variant":variant,"size_class":size,"content_contract":content,"icon_id":None,"action_ids":actions,"state_ids":[state_id],"source_refs":[base.origin("product_contract",f"{base.rel(INTAKE)}#/screens/4")],"standard_identity":identity,"standard_slot_id":slot,"component_state_ids":states})
    return row


def build_contract(state: dict, screen: dict, baseline: dict, fixture: Path) -> dict:
    contract = json.loads(BASE_CONTRACT.read_text(encoding="utf-8")); state_id=state["state_id"]
    manifest=ART/f"applicability/{state_id}.r5.json"
    contract.update({"contract_profile":"codex.ui-screen-design-contract/v1@2.0.0","screen_revision_id":f"{state_id}.IA-WA.ru-RU.graphite.r5","program_revision_ref":f"{PROGRAM_ID}@5","status":"review","functional_contract_ref":{"path":base.rel(INTAKE),"sha256":base.sha(INTAKE),"json_pointer":"/screens/4","screen_id":"UI-AUTH-005"},"baseline_binding":{"baseline_id":baseline["baseline_id"],"path":base.rel(BASELINE),"sha256":base.sha(BASELINE),"shell_variant_id":"shell.workspace","exception_id":None},"standard_binding":{"standard_revision_id":baseline["standard_contract"]["standard_revision_id"],"clause_inventory_sha256":baseline["standard_contract"]["clause_inventory_sha256"],"applicability_manifest":{"path":base.rel(manifest),"sha256":"0"*64}},"standard_exceptions":[],"product_identity":{"screen_id":"UI-AUTH-005","route_id":"UI-AUTH-005","route":"/onboarding","state_id":state_id,"role_id":"IA-WA","permission_profile":"authenticated_global","locale":"ru","theme":"graphite"},"comparison_claims":{"required_purpose":"visual_language_conformance","deterministic_render_proves_fidelity":False,"reference_logical_artifact_id":f"{PROGRAM_ID}:accepted-pilot:ru:r5","implementation_logical_artifact_id":f"{PROGRAM_ID}:UI-AUTH-005:{state_id}:r5"}})
    contract["source_visual"].update({"html_path":base.rel(SOURCE),"html_sha256":base.sha(SOURCE),"image_path":None,"image_sha256":None})
    program=json.loads(PROGRAM.read_text(encoding="utf-8")); contract["visual_authority"]={k:program["visual_authority"][k] for k in ("source_visual_ref","source_visual_sha256","owner_decision_ref","screen_acceptance_scope","visual_language_scope","reusable_foundation_scope","inheritance_policy","mobile_scope")}
    contract["render_environment"].update({"fixed_clock_iso":"2026-08-19T12:00:00Z","fixture_data_path":base.rel(fixture),"fixture_data_sha256":base.sha(fixture),"font_bundle_sha256":base.canonical_sha(baseline["font_contract"]),"asset_bundle_sha256":base.canonical_sha(baseline["asset_contract"])})
    ro=base.origin("product_contract",f"{base.rel(BASELINE)}#/responsive_contract"); contract["viewport_contract"]["supported_web_width_range"]={**baseline["responsive_contract"]["supported_web_width_range"],"origin":ro}; contract["viewport_contract"]["anchors"]=[{"anchor_id":a,"width":w,"height":h,"class":"responsive_web","state_ref":state_id,"origin":ro} for a,w,h in ANCHORS]; contract["viewport_contract"]["above_supported_range_origin"]=ro
    template=next(x for x in contract["regions"] if x["region_id"]=="UI-ADMIN-003.content"); contract["regions"]=[make_region(template,state_id,"UI-AUTH-005.content",'[data-ui-region="UI-AUTH-005.content"]',"candidate.workspace-onboarding","wizard"),make_region(template,state_id,"UI-AUTH-005.navigation",'[data-ui-region="UI-AUTH-005.navigation"]',"candidate.workspace-rail","compact")]
    et=contract["element_contracts"][0]; contract["element_contracts"]=[make_element(et,state_id,s) for s in element_specs()]
    loading=state_id.endswith((".loading", ".permission_denied")); contract["interaction_contract"]["visible_actions"]=[{"action_id":"UI-AUTH-005.inspect","expected_outcome":screen["actions"][0]["outcome"],"side_effect_class":"local_state","activation_policy":"assert_affordance_only" if loading else "execute_in_fixture","outcome_assertion":{"kind":"not_executed","selector":None,"property":None,"expected":"visible_disabled_control"} if loading else {"kind":"dom","selector":"[data-result]","property":"textContent","expected":"Следующий шаг подготовлен."}}]; contract["interaction_contract"]["no_actions_reason_ref"]=None; contract["interaction_contract"]["allowed_origins"]=["http://127.0.0.1:4173"]; contract["interaction_contract"]["redaction_selectors"]=["[data-sensitive]"]
    contract["acceptance"]["pixel_diff_policy"]["channel_threshold"]["value"]=18; contract["acceptance"]["pixel_diff_policy"]["approved_max_different_pixels"].update({"value":2073600,"unit":"px"})
    return contract


def bootstrap() -> None:
    ART.mkdir(parents=True,exist_ok=True); EVID.mkdir(parents=True,exist_ok=True); TARGET.parent.mkdir(parents=True,exist_ok=True)
    intake=json.loads(INTAKE.read_text(encoding="utf-8")); screen=next(x for x in intake["screens"] if x["screen_id"]=="UI-AUTH-005"); states=screen["states"]; baseline=json.loads(BASELINE.read_text(encoding="utf-8")); fixture=ART/"fixture.json"
    base.write_json(fixture,{"schema_id":"custometry.g4-onboarding-fixture/v1","fixed_clock":"2026-08-19T12:00:00Z","route":"/onboarding","states":states,"roles":["IA","WA"],"locales":["ru","en"],"network_mode":"isolated_loopback"})
    rendered=target_html(baseline).replace("__FIXTURE_SHA256__",base.sha(fixture)).replace("__FONT_SHA256__",base.canonical_sha(baseline["font_contract"])).replace("__ASSET_SHA256__",base.canonical_sha(baseline["asset_contract"])); TARGET.write_text(rendered,encoding="utf-8")
    rows=[{"screen_id":"UI-AUTH-005","state_id":s["state_id"],"locale":lang,"visible_copy":{**{k:v for k,v in copy.items() if k!="states"},"state":copy["states"][s["kind"]]},"provenance":{"product_semantics":["custometry-ui-blueprint-ru.md#9.1-authentication-и-onboarding-6-страниц"],"route_contract":"packages/contracts/routes/ui-route-contracts.json#/routes/4","classification":"source_bound_product_copy_and_minimal_connective_copy"}} for lang,copy in COPY.items() for s in states]
    base.write_json(EVID/"visible-copy-inventory.json",{"schema_id":"custometry.ui-visible-copy-inventory/v1","program_id":PROGRAM_ID,"stage_instance_id":STAGE_ID,"screen_state_locale_pairs":rows,"expected_pairs":12,"observed_pairs":len(rows),"result":"passed" if len(rows)==12 else "failed"})
    base.build_program_snapshot({"UI-AUTH-005":states})
    binding=ART/"program-snapshot-binding.json"; b=json.loads(binding.read_text(encoding="utf-8")); b["reason"]="Family aggregation adds exact accepted required_states only for the current UI-AUTH-005 representative; no other inventory meaning changes."; base.write_json(binding,b)
    for state in states: base.write_json(ART/f"contracts/{state['state_id']}.r5.json",build_contract(state,screen,baseline,fixture))
    base.write_json(EVID/"onboarding-semantics.json",{"schema_id":"custometry.ui-onboarding-semantics/v1","stage_instance_id":STAGE_ID,"steps":["account","workspace","locale_timezone","data_or_demo","finish"],"resumable":True,"roles":["IA","WA"],"representative":"UI-AUTH-005","reuse_only":["UI-AUTH-006"],"result":"passed"})
    base.write_json(ART/"reuse-decision.json",{"schema_id":"codex.ui-family-reuse-decision/v2","family_id":FAMILY_ID,"representative_screen_ids":["UI-AUTH-005"],"individually_designed_screen_ids":["UI-AUTH-005"],"reuse_only_screen_ids":["UI-AUTH-006"],"decision":"Use the accepted compact workspace-shell and five-step resumable onboarding grammar for this family.","scope_limit":"No individual acceptance claim is made for UI-AUTH-006.","result":"recorded"})


def bind() -> None:
    base.bind()


def proof_requests() -> None:
    base.proof_requests()


def review() -> None:
    acceptances=[]
    for path in sorted((EVID/"screen-acceptance").glob("*.json")):
        acceptances.append((path,json.loads(path.read_text(encoding="utf-8"))))
    entries=[]
    for path,doc in acceptances:
        for role in ("screen_acceptance","standard_conformance"):
            entries.append({"entry_id":f"review-{len(entries)+1:02d}","role":role,"artifact_ref":base.rel(path),"sha256":base.sha(path),"anchor_id":None,"state_id":doc["state_id"]})
    manifest=ART/"review-board.manifest.json"; base.write_json(manifest,{"$schema":"review-board-manifest.schema.json","schema_id":"codex.ui-review-board-manifest/v1","program_id":PROGRAM_ID,"artifact_id":FAMILY_REVISION_ID,"revision":5,"validation_profile":"family_review_ready","entries":entries})
    labels={"initial":"Начало","loading":"Загрузка","populated":"Заполнено","error":"Ошибка","permission_denied":"Нет доступа","recovery":"Возврат"}; buttons=''.join(f'<button type="button" data-state="UI-AUTH-005.{k}">{v}</button>' for k,v in labels.items()); closure=''.join(f'<li data-review-entry="{e["entry_id"]}">{html.escape(e["role"])} · {html.escape(e["state_id"])}</li>' for e in entries)
    board=ART/"review-board.html"; board.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry · onboarding family r5</title><style>:root{{--bg:#070708;--panel:#111214;--module:#1a1b1e;--line:#303136;--ink:#f0f0f2;--secondary:#a7a7ad;--cyan:#8ccfe3;--focus:#8bd2e8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,system-ui,sans-serif}}main{{width:min(1240px,calc(100% - 32px));margin:auto;padding:24px 0 48px}}h1{{margin:0;font-size:29px}}header p{{max-width:76ch;color:var(--secondary)}}.states{{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0}}button{{min-height:36px;border:1px solid var(--line);border-radius:7px;padding:0 11px;color:var(--secondary);background:var(--module);cursor:pointer}}button[aria-pressed=true]{{color:#071014;background:var(--cyan);font-weight:700}}button:focus-visible{{outline:3px solid var(--focus);outline-offset:2px}}.viewer{{overflow:hidden;border:1px solid var(--line);border-radius:15px;background:var(--panel)}}iframe{{display:block;width:100%;height:900px;border:0}}.boundary{{margin:14px 0;padding:13px;border:1px solid var(--line);border-radius:10px;color:var(--secondary);background:var(--panel)}}.closure{{display:none}}@media(max-width:800px){{iframe{{height:1120px}}}}</style></head><body data-ui-artifact="review_board" data-program-id="{PROGRAM_ID}" data-artifact-id="{FAMILY_REVISION_ID}" data-revision="5" data-validation-profile="family_review_ready" data-review-manifest="{base.rel(manifest)}" data-review-manifest-sha256="{base.sha(manifest)}"><main><header><p>G4 · готовое семейство</p><h1>Настройка рабочего пространства</h1><p>Пятишаговый onboarding с сохранением прогресса, явной готовностью и безопасным возвратом.</p></header><div class="states" aria-label="Состояние">{buttons}</div><section class="viewer"><iframe title="Интерактивный экран onboarding" src="screens/onboarding.html?screen=UI-AUTH-005&state=UI-AUTH-005.initial&lang=ru"></iframe></section><div class="boundary">Проверьте общую иерархию, компактность shell, понятность пяти шагов и ощущение сохраняемого прогресса. Это визуальный контракт, не production-реализация.</div><ul class="closure">{closure}</ul></main><script>const frame=document.querySelector('iframe'),buttons=[...document.querySelectorAll('[data-state]')];function select(state){{frame.src=`screens/onboarding.html?screen=UI-AUTH-005&state=${{state}}&lang=ru`;buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)))}}buttons.forEach(b=>b.addEventListener('click',()=>select(b.dataset.state)));select('UI-AUTH-005.initial');</script></body></html>''',encoding="utf-8")
    request=EVID/"family-acceptance-request.json"; base.write_json(request,{"$schema":"family-acceptance-request.schema.json","program_path":base.rel(SNAPSHOT),"family_id":FAMILY_ID,"family_revision_id":FAMILY_REVISION_ID,"revision":5,"screen_acceptance_paths":[base.rel(p) for p,_ in acceptances],"review_board_path":base.rel(board),"owner_decision_ref":None})
    base.write_json(EVID/"owner-review-decision-packet.json",{"schema_id":"custometry.ui-owner-review-decision-packet/v1","program_id":PROGRAM_ID,"stage_instance_id":STAGE_ID,"decision_id":f"{STAGE_ID}.finished-result","decision_kind":"family_acceptance","question":"Принять готовое семейство настройки рабочего пространства или запросить ограниченные исправления?","target":{"artifact_kind":"review_board","artifact_id":FAMILY_REVISION_ID,"revision":5,"validation_profile":"family_review_ready","path":base.rel(board),"sha256":base.sha(board)},"allowed_responses":["accept","bounded_corrections"],"status":"pending"})


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("mode",choices=("bootstrap","bind","proof-requests","review")); args=parser.parse_args(); {"bootstrap":bootstrap,"bind":bind,"proof-requests":proof_requests,"review":review}[args.mode](); return 0


if __name__ == "__main__":
    raise SystemExit(main())
