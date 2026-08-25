#!/usr/bin/env python3
"""Build the current G4 promotions-family review artifacts from released r5 machinery."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "build_g4_fcst_r5_artifacts.py"
spec = importlib.util.spec_from_file_location("g4_promo_base", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError("forecast G4 builder cannot be loaded")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.ARTIFACT_DIR = HERE / "artifacts/g4-r5/family-promo-shell-workspace-baseline"
base.EVIDENCE_DIR = HERE / "evidence/family.promo.shell-workspace.baseline-r5"
base.SCREEN_ID = "UI-PROMO-001"
base.FAMILY_ID = "family.promo.shell-workspace.baseline"
base.FAMILY_REVISION_ID = "family.promo.shell-workspace.baseline-r5"
base.STAGE_ID = "G4@family.promo.shell-workspace.baseline-r5"
base.ACTION_STATES = set(base.STATES)
base.STATE_CONTENT = {
    "initial": {"status": "Контур промо готов", "title": "Промо готовы к первому обзору", "summary": "Безопасный старт списка промо без production-запросов и внешних изменений.", "panel": "Структура списка, Result Trust и recovery controls уже на месте; реальные данные не запрашиваются."},
    "loading": {"status": "Загрузка изолированного fixture", "title": "Загружаем список промо", "summary": "Сохраняем оболочку, доверительную информацию и маршрут доступными во время ожидания.", "panel": "Подготавливаем промо-объекты и unit economics. Внешняя сеть отключена."},
    "populated": {"status": "6 промо · 2 требуют внимания", "title": "Промо и unit economics собраны", "summary": "Список связывает управление промо, Result Trust и переход к offline unit economics в одной поверхности.", "panel": ""},
    "error": {"status": "Ошибка чтения fixture", "title": "Список промо временно недоступен", "summary": "Контекст сохранён; доступны безопасные повторные действия без внешних side effects.", "panel": "Проверьте локальный источник и повторите операцию. Последняя доверенная версия не изменена."},
    "permission_denied": {"status": "Требуется promotion.manage", "title": "Доступ к управлению промо ограничен", "summary": "Поверхность сохраняет маршрут, Result Trust и точные permission-bound действия.", "panel": "Для управления требуется permission promotion.manage; переход по journey остаётся без production side effects."},
    "recovery": {"status": "Восстановление доступно", "title": "Можно безопасно продолжить работу", "summary": "Контекст промо сохранён; повторные действия выполняются только в изолированном fixture.", "panel": "Управляйте промо или продолжите unit economics. Производственные данные не изменяются."},
}


def replace_strings(value):
    replacements = {
        "UI-AN-013": base.SCREEN_ID,
        "/screens/55": "/screens/68",
        "/w/:workspaceKey/research": "/w/:workspaceKey/promotions",
        "research.manage": "promotion.manage",
        "finding.manage": "journey.digital-to-offline-unit-economics.2",
        "Research Manage": "Promotion Manage",
        "Finding Manage": "Continue digital to offline unit economics",
    }
    if isinstance(value, str):
        for before, after in replacements.items():
            value = value.replace(before, after)
        return value
    if isinstance(value, list):
        return [replace_strings(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item) for key, item in value.items()}
    return value


def visible_actions(screen, state):
    if state not in base.ACTION_STATES:
        return []
    assertions = {
        "UI-PROMO-001.promotion.manage": "Управление промо открыто в fixture",
        "journey.digital-to-offline-unit-economics.2": "Переход к unit economics подготовлен в fixture",
    }
    return [{
        "action_id": action["action_id"],
        "expected_outcome": action["outcome"],
        "side_effect_class": "none",
        "activation_policy": "execute_in_fixture",
        "outcome_assertion": {"kind": "dom", "selector": "#inspect-result", "property": "textContent", "expected": assertions[action["action_id"]]},
    } for action in screen["actions"]]


def action_buttons(state):
    if state not in base.ACTION_STATES:
        return '<div class="hero-actions" aria-hidden="true"></div><p id="inspect-result" role="status" aria-live="polite"></p>'
    return (
        '<div class="hero-actions">'
        '<button id="train-action" type="button" data-ui-element="train-action" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="UI-PROMO-001.promotion.manage">Управлять промо</button>'
        '<button id="promote-action" type="button" data-ui-element="promote-action" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="journey.digital-to-offline-unit-economics.2">Продолжить unit economics</button>'
        '</div><p id="inspect-result" role="status" aria-live="polite"></p>'
    )


def populated_body():
    return """
          <section class="kpi-module" aria-labelledby="promo-kpi-title"><div class="kpi-module-header"><div class="kpi-module-title"><strong id="promo-kpi-title">Promotion portfolio</strong><span class="kpi-context">digital → offline</span></div></div><div class="kpi-strip" aria-label="Сводка промо"><article class="kpi"><span class="kpi-label">Промо</span><div class="kpi-value-row"><strong class="kpi-value">6</strong><span class="kpi-delta">fixture</span></div></article><article class="kpi"><span class="kpi-label">Incremental margin</span><div class="kpi-value-row"><strong class="kpi-value">₽4.8M</strong><span class="kpi-delta">+7.2%</span></div></article><article class="kpi"><span class="kpi-label">Offline uplift</span><div class="kpi-value-row"><strong class="kpi-value">11.4%</strong><span class="kpi-delta tone-warning">review</span></div></article><article class="kpi"><span class="kpi-label">Trust</span><div class="kpi-value-row"><strong class="kpi-value">High</strong><span class="kpi-delta tone-muted">W+1</span></div></article></div></section>
          <section class="overview-grid"><article class="data-card trust-card"><header><div><span class="section-kicker">Result Trust</span><h2>Доверие к unit economics</h2></div><span class="trust-score">Высокое</span></header><dl><div><dt>Snapshot</dt><dd>promo-r-18</dd></div><div><dt>Freshness</dt><dd>8 минут</dd></div><div><dt>Coverage</dt><dd>Digital + offline</dd></div></dl></article><article class="data-card checklist"><header><div><span class="section-kicker">Journey</span><h2>Контроль перехода</h2></div><span>2 / 2</span></header><ul><li class="done">promotion.manage проверен в fixture</li><li class="done">переход к unit economics сохраняет контекст</li></ul></article></section>
          <section class="data-card run-card"><header><div><span class="section-kicker">Promotion list</span><h2>Активные промо</h2></div><span class="quiet-pill">fixture</span></header><div class="table-wrap"><table><thead><tr><th>Промо</th><th>Канал</th><th>Статус</th><th>Incremental margin</th></tr></thead><tbody><tr><td>Weekend bundles</td><td>Digital + store</td><td><span class="result success">Готово</span></td><td>₽2.1M</td></tr><tr><td>Loyalty boost</td><td>Offline</td><td><span class="result warning">На проверке</span></td><td>₽1.4M</td></tr><tr><td>Search acquisition</td><td>Digital</td><td><span class="result success">Готово</span></td><td>₽1.3M</td></tr></tbody></table></div></section>
"""


base.replace_strings = replace_strings
base.visible_actions = visible_actions
base.action_buttons = action_buttons
base.populated_body = populated_body

original_rewrite_contract = base.rewrite_contract
original_rewrite_html = base.rewrite_html
original_prepare = base.prepare
original_load_template = base.load_template
original_review_ready_candidate = base.review_ready_candidate


def load_template():
    module = original_load_template()
    module.REPORT = base.ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.promo.shell-workspace.baseline-r5-report.md"
    module.NEXT_PROMPT = base.ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-10-family-dash-shell-workspace-baseline-r5.md"
    return module


base.load_template = load_template


def review_ready_candidate(final):
    original_review_ready_candidate(final)
    output = base.EVIDENCE_DIR / ("review-ready-final-candidate.md" if final else "review-ready-provisional-candidate.md")
    text = output.read_text(encoding="utf-8")
    marker = f"### `{base.STAGE_ID}`"
    before, found, after = text.partition(marker)
    if not found:
        raise RuntimeError("promo stage details are absent from ledger candidate")
    after = after.replace(
        "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_forecast_r5_board",
        "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_promotion_r5_board",
        1,
    )
    output.write_text(before + found + after, encoding="utf-8")


base.review_ready_candidate = review_ready_candidate


def rewrite_contract(path, state, screen, fixture_sha):
    original_rewrite_contract(path, state, screen, fixture_sha)
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["functional_contract_ref"].update({"json_pointer": "/screens/68", "screen_id": base.SCREEN_ID})
    contract["product_identity"].update({"role_id": "AN", "permission_profile": "promotion.manage"})
    contract["interaction_contract"]["visible_actions"] = visible_actions(screen, state)
    for region in contract["regions"]:
        region["source_refs"] = [{"kind": "product_contract", "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json#/screens/68"}]
    action_ids = ["UI-PROMO-001.promotion.manage", "journey.digital-to-offline-unit-economics.2"]
    for element in contract["element_contracts"]:
        element["source_refs"] = [{"kind": "product_contract", "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json#/screens/68"}]
        if element["element_id"] == "train-action":
            element["action_ids"] = [action_ids[0]]
        elif element["element_id"] == "promote-action":
            element["action_ids"] = [action_ids[1]]
    base.write_json(path, contract)


def rewrite_html(path, state, fixture_sha):
    original_rewrite_html(path, state, fixture_sha)
    html = path.read_text(encoding="utf-8")
    html = html.replace("Custometry · Forecasts ·", "Custometry · Promotions ·").replace("<h1>Прогнозы</h1>", "<h1>Промо</h1>").replace("Прогнозирование · модели", "Промо · unit economics")
    html = re.sub(r'<script>.*?</script>', '<script>const result=document.getElementById("inspect-result");const first=document.getElementById("train-action");const second=document.getElementById("promote-action");if(first)first.addEventListener("click",()=>{result.textContent="Управление промо открыто в fixture";});if(second)second.addEventListener("click",()=>{result.textContent="Переход к unit economics подготовлен в fixture";});</script>', html, count=1, flags=re.DOTALL)
    path.write_text(html, encoding="utf-8")


base.rewrite_contract = rewrite_contract
base.rewrite_html = rewrite_html


def prepare():
    original_prepare()
    decision = base.ARTIFACT_DIR / "reuse-decision.json"
    base.write_json(decision, {"schema_id": "codex.ui-family-reuse-decision/v2", "family_id": base.FAMILY_ID, "representative_screen_ids": [base.SCREEN_ID], "individually_designed_screen_ids": [base.SCREEN_ID], "reuse_only_screen_ids": ["UI-PROMO-002", "UI-PROMO-003"], "decision": "Use one exact promotions-list representative while preserving later route semantics.", "scope_limit": "No individual design or acceptance claim is made for UI-PROMO-002 or UI-PROMO-003.", "result": "recorded"})


base.prepare = prepare


def postprocess(phase):
    if phase == "review":
        board = base.ARTIFACT_DIR / "review-board.html"
        text = board.read_text(encoding="utf-8").replace("Forecast", "Promotions").replace("Прогнозы", "Промо").replace("forecast-list", "promotions-list").replace("forecast", "promotion")
        board.write_text(text, encoding="utf-8")
        packet = base.EVIDENCE_DIR / "owner-review-decision-packet.md"
        packet.write_text(packet.read_text(encoding="utf-8").replace("Готовые промоы", "Готовые промо").replace("прогноз", "промо").replace("Forecast", "Promotions").replace("UI-FCST-001", "UI-PROMO-001"), encoding="utf-8")
    elif phase == "transition-inputs":
        next_inputs = base.EVIDENCE_DIR / "preflight/next_stage_inputs.json"
        value = json.loads(next_inputs.read_text(encoding="utf-8")); value["facts"]["next_stage_id"] = "G4@family.dash.shell-workspace.baseline-r5"; base.write_json(next_inputs, value)
        request = base.EVIDENCE_DIR / "stage-transition-request-review-ready.json"
        value = json.loads(request.read_text(encoding="utf-8")); value.update({"to_stage_id": "G4@family.dash.shell-workspace.baseline-r5", "to_target": "family.dash.shell-workspace.baseline-r5", "to_task": ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-10-family-dash-shell-workspace-baseline-r5.md", "summary": "Promotions exact-cover all six required states, both functional actions where applicable, and four responsive-Web anchors; machine proof is ready for owner review.", "questions": ["Принимаете готовую family review board промо или хотите небольшие правки?"]}); base.write_json(request, value)
        report = base.ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.promo.shell-workspace.baseline-r5-report.md"
        report.write_text("""---
artifact_kind: ui_design_program_stage_evidence
stage_instance_id: G4@family.promo.shell-workspace.baseline-r5
gate_id: G4
status: review_ready
proof_boundary: current-contract isolated browser evidence for six UI-PROMO-001 states and four responsive-Web anchors; no production implementation, publication, deployment, mobile-specific design, full WCAG conformance, persistence, authorization, or performance proof
---

# G4 promotions family r5 execution report

## Scope

- `UI-PROMO-001` only; required states: `initial, loading, populated, error, permission_denied, recovery`.
- Responsive Web anchors: `web-768`, `web-1024`, `web-1440`, `web-1920`.
- Visual-language conformance to the hash-pinned pilot and platform baseline.
- Isolated fixture interactions for `UI-PROMO-001.promotion.manage` and `journey.digital-to-offline-unit-economics.2` in all six reviewed states; no external writes.

## Result

- Family aggregate: `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.promo.shell-workspace.baseline-r5/family-acceptance.json` (`review_ready`).
- Review board: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-promo-shell-workspace-baseline/review-board.html`.
- Browser board QA: `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.promo.shell-workspace.baseline-r5/browser-board-qa.json`.
- Transition: `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.promo.shell-workspace.baseline-r5/stage-transition-review-ready.json` (`review_ready`; next stage not allowed).

## Proof boundary and residual risk

Automated evidence covers contract shape, deterministic standard applicability,
clause-level computed values, keyboard/accessibility smoke, loopback isolation,
console/network observations, responsive-Web overflow, and rendered owner review.
Owner acceptance remains required. Mobile-specific scope is unauthorized. No
production frontend, API, authorization, database, performance, deployment,
release, or full WCAG claim is made.
""", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("phase", choices=("prepare", "bind-applicability", "review", "board-qa", "transition-inputs", "review-ready-provisional", "review-ready-final")); phase = parser.parse_args().phase
    if phase == "prepare": base.prepare()
    elif phase == "board-qa": base.board_qa()
    elif phase == "review-ready-provisional": base.review_ready_candidate(False)
    elif phase == "review-ready-final": base.review_ready_candidate(True)
    else:
        base.run_template_phase(phase.replace("-", "_"))
        postprocess(phase)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
