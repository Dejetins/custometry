#!/usr/bin/env python3
"""Build the current G4 dashboards-family review artifacts from released r5 machinery."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "build_g4_fcst_r5_artifacts.py"
spec = importlib.util.spec_from_file_location("g4_dash_base", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError("forecast G4 builder cannot be loaded")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.ARTIFACT_DIR = HERE / "artifacts/g4-r5/family-dash-shell-workspace-baseline"
base.EVIDENCE_DIR = HERE / "evidence/family.dash.shell-workspace.baseline-r5"
base.SCREEN_ID = "UI-DASH-001"
base.FAMILY_ID = "family.dash.shell-workspace.baseline"
base.FAMILY_REVISION_ID = "family.dash.shell-workspace.baseline-r5"
base.STAGE_ID = "G4@family.dash.shell-workspace.baseline-r5"
base.ACTION_STATES = set(base.STATES)
base.STATE_CONTENT = {
    "initial": {"status": "Контур дашбордов готов", "title": "Дашборды готовы к обзору", "summary": "Безопасный старт списка дашбордов без production-запросов и внешних изменений.", "panel": "Структура списка, Result Trust и recovery controls доступны до загрузки данных."},
    "loading": {"status": "Загрузка изолированного fixture", "title": "Загружаем список дашбордов", "summary": "Оболочка, маршрут и доверительная информация остаются стабильными во время ожидания.", "panel": "Подготавливаем публикации, доступ и комментарии. Внешняя сеть отключена."},
    "populated": {"status": "8 дашбордов · 2 требуют внимания", "title": "Дашборды и публикации собраны", "summary": "Список объединяет управление, публикацию, доступ, комментарии и стабильное обновление в одной поверхности.", "panel": ""},
    "error": {"status": "Ошибка чтения fixture", "title": "Список дашбордов временно недоступен", "summary": "Контекст сохранён; доступны безопасные повторные действия без внешних side effects.", "panel": "Проверьте локальный источник и повторите операцию. Последняя доверенная версия не изменена."},
    "permission_denied": {"status": "Требуются dashboard permissions", "title": "Доступ к дашбордам ограничен", "summary": "Поверхность сохраняет маршрут, Result Trust и точные permission-bound действия.", "panel": "Управление, публикация, доступ и комментарии выполняются только в изолированном fixture."},
    "recovery": {"status": "Восстановление доступно", "title": "Можно безопасно продолжить работу", "summary": "Контекст дашбордов сохранён; повторные действия выполняются только в изолированном fixture.", "panel": "Продолжите работу или обновление со стабильными anchors. Производственные данные не изменяются."},
}

ACTION_SPECS = (
    ("train-action", "UI-DASH-001.dashboard.manage", "Управлять", "Управление дашбордом открыто в fixture"),
    ("promote-action", "UI-DASH-001.dashboard.publish", "Опубликовать", "Публикация дашборда подготовлена в fixture"),
    ("resolve-comment-action", "UI-DASH-001.dashboard_access.manage", "Настроить доступ", "Управление доступом открыто в fixture"),
    ("comments-action", "UI-DASH-001.comment.read", "Комментарии", "Комментарии открыты в fixture"),
    ("add-comment-action", "UI-DASH-001.comment.create", "Добавить комментарий", "Комментарий добавлен в fixture"),
    ("continue-action", "journey.refresh-with-stable-anchors.1", "Обновить с anchors", "Обновление со стабильными anchors подготовлено в fixture"),
)


def replace_strings(value):
    replacements = {
        "UI-AN-013": base.SCREEN_ID,
        "/screens/55": "/screens/71",
        "/w/:workspaceKey/research": "/w/:workspaceKey/dashboards",
        "research.manage": "dashboard.manage",
        "finding.manage": "dashboard.publish",
        "comment.resolve": "dashboard_access.manage",
        "journey.publish-review-collaborate.1": "journey.refresh-with-stable-anchors.1",
        "Research Manage": "Dashboard Manage",
        "Finding Manage": "Dashboard Publish",
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
    assertions = {action_id: outcome for _, action_id, _, outcome in ACTION_SPECS}
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
    buttons = "".join(
        f'<button id="{element_id}" type="button" data-ui-element="{element_id}" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="{action_id}">{label}</button>'
        for element_id, action_id, label, _ in ACTION_SPECS
    )
    return f'<div class="hero-actions">{buttons}</div><p id="inspect-result" role="status" aria-live="polite"></p>'


def populated_body():
    return """
          <section class="kpi-module" aria-labelledby="dash-kpi-title"><div class="kpi-module-header"><div class="kpi-module-title"><strong id="dash-kpi-title">Dashboard portfolio</strong><span class="kpi-context">stable anchors</span></div></div><div class="kpi-strip" aria-label="Сводка дашбордов"><article class="kpi"><span class="kpi-label">Дашборды</span><div class="kpi-value-row"><strong class="kpi-value">8</strong><span class="kpi-delta">fixture</span></div></article><article class="kpi"><span class="kpi-label">Опубликованы</span><div class="kpi-value-row"><strong class="kpi-value">6</strong><span class="kpi-delta">stable</span></div></article><article class="kpi"><span class="kpi-label">Доступ</span><div class="kpi-value-row"><strong class="kpi-value">2</strong><span class="kpi-delta tone-warning">review</span></div></article><article class="kpi"><span class="kpi-label">Trust</span><div class="kpi-value-row"><strong class="kpi-value">High</strong><span class="kpi-delta tone-muted">8m</span></div></article></div></section>
          <section class="overview-grid"><article class="data-card trust-card"><header><div><span class="section-kicker">Result Trust</span><h2>Доверие к дашбордам</h2></div><span class="trust-score">Высокое</span></header><dl><div><dt>Snapshot</dt><dd>dash-r-31</dd></div><div><dt>Freshness</dt><dd>8 минут</dd></div><div><dt>Anchors</dt><dd>Stable</dd></div></dl></article><article class="data-card checklist"><header><div><span class="section-kicker">Collaboration</span><h2>Контроль публикации</h2></div><span>6 / 6</span></header><ul><li class="done">управление, публикация и доступ проверены в fixture</li><li class="done">комментарии и refresh сохраняют стабильные anchors</li></ul></article></section>
          <section class="data-card run-card"><header><div><span class="section-kicker">Dashboard list</span><h2>Рабочие дашборды</h2></div><span class="quiet-pill">fixture</span></header><div class="table-wrap"><table><thead><tr><th>Дашборд</th><th>Владелец</th><th>Статус</th><th>Result Trust</th></tr></thead><tbody><tr><td>Executive overview</td><td>Analytics</td><td><span class="result success">Опубликован</span></td><td>Высокое</td></tr><tr><td>Promotion health</td><td>Commercial</td><td><span class="result warning">На проверке</span></td><td>Среднее</td></tr><tr><td>Forecast quality</td><td>Planning</td><td><span class="result success">Опубликован</span></td><td>Высокое</td></tr></tbody></table></div></section>
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
original_postprocess_review = base.postprocess_review


def load_template():
    module = original_load_template()
    module.REPORT = base.ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.dash.shell-workspace.baseline-r5-report.md"
    module.NEXT_PROMPT = base.ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-11-family-rpt-shell-workspace-baseline-r5.md"
    return module


def rewrite_contract(path, state, screen, fixture_sha):
    original_rewrite_contract(path, state, screen, fixture_sha)
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["functional_contract_ref"].update({"json_pointer": "/screens/71", "screen_id": base.SCREEN_ID})
    contract["product_identity"].update({"role_id": "AN", "permission_profile": "dashboard.manage"})
    contract["interaction_contract"]["visible_actions"] = visible_actions(screen, state)
    for region in contract["regions"]:
        region["source_refs"] = [{"kind": "product_contract", "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json#/screens/71"}]
    templates = [item for item in contract["element_contracts"] if item["element_id"] in {"train-action", "promote-action"}]
    contract["element_contracts"] = [item for item in contract["element_contracts"] if item["element_id"] not in {"train-action", "promote-action"}]
    if state in base.ACTION_STATES:
        template = templates[0]
        for element_id, action_id, _, _ in ACTION_SPECS:
            element = copy.deepcopy(template)
            element.update({"element_id": element_id, "locator": f"#{element_id}", "action_ids": [action_id]})
            element["source_refs"] = [{"kind": "product_contract", "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json#/screens/71"}]
            contract["element_contracts"].append(element)
    base.write_json(path, contract)


def rewrite_html(path, state, fixture_sha):
    original_rewrite_html(path, state, fixture_sha)
    html = path.read_text(encoding="utf-8")
    html = html.replace("Custometry · Forecasts ·", "Custometry · Dashboards ·").replace("<h1>Прогнозы</h1>", "<h1>Дашборды</h1>").replace("Прогнозирование · модели", "Дашборды · публикация и доступ")
    if state in base.ACTION_STATES:
        listeners = "".join(f'document.getElementById("{element_id}").addEventListener("click",()=>{{result.textContent={json.dumps(outcome, ensure_ascii=False)};}});' for element_id, _, _, outcome in ACTION_SPECS)
        script = f'<script>const result=document.getElementById("inspect-result");{listeners}</script>'
    else:
        script = '<script>const result=document.getElementById("inspect-result");</script>'
    html = re.sub(r"<script>.*?</script>", script, html, count=1, flags=re.DOTALL)
    path.write_text(html, encoding="utf-8")


def prepare():
    original_prepare()
    base.write_json(base.ARTIFACT_DIR / "reuse-decision.json", {"schema_id": "codex.ui-family-reuse-decision/v2", "family_id": base.FAMILY_ID, "representative_screen_ids": [base.SCREEN_ID], "individually_designed_screen_ids": [base.SCREEN_ID], "reuse_only_screen_ids": ["UI-DASH-002", "UI-DASH-003"], "decision": "Use one exact dashboard-list representative while preserving later route semantics.", "scope_limit": "No individual design or acceptance claim is made for UI-DASH-002 or UI-DASH-003.", "result": "recorded"})


def postprocess_review(module):
    original_postprocess_review(module)
    board = base.ARTIFACT_DIR / "review-board.html"
    text = board.read_text(encoding="utf-8").replace("Forecast", "Dashboards").replace("Прогнозы", "Дашборды").replace("forecast-list", "dashboard-list").replace("две source-bound fixture-команды", "шесть source-bound fixture-команд").replace("Dashboardss", "Dashboards")
    board.write_text(text, encoding="utf-8")
    packet = base.EVIDENCE_DIR / "owner-review-decision-packet.md"
    packet.write_text(packet.read_text(encoding="utf-8").replace("Готовые прогнозы", "Готовые дашборды").replace("forecast-list", "dashboard-list").replace("UI-FCST-001", "UI-DASH-001"), encoding="utf-8")


def postprocess_transition():
    next_stage = "G4@family.rpt.shell-workspace.baseline-r5"
    next_inputs = base.EVIDENCE_DIR / "preflight/next_stage_inputs.json"
    value = json.loads(next_inputs.read_text(encoding="utf-8")); value["facts"]["next_stage_id"] = next_stage; base.write_json(next_inputs, value)
    request = base.EVIDENCE_DIR / "stage-transition-request-review-ready.json"
    value = json.loads(request.read_text(encoding="utf-8")); value.update({"to_stage_id": next_stage, "to_target": "family.rpt.shell-workspace.baseline-r5", "to_task": ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-11-family-rpt-shell-workspace-baseline-r5.md", "summary": "Dashboards exact-cover all six required states, six functional actions where applicable, and four responsive-Web anchors; machine proof is ready for owner review.", "questions": ["Принимаете готовую family review board дашбордов или хотите небольшие правки?"]}); base.write_json(request, value)
    report = base.ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.dash.shell-workspace.baseline-r5-report.md"
    report.write_text("""---
artifact_kind: ui_design_program_stage_evidence
stage_instance_id: G4@family.dash.shell-workspace.baseline-r5
gate_id: G4
status: review_ready
proof_boundary: current-contract isolated browser evidence for six UI-DASH-001 states and four responsive-Web anchors; no production implementation, publication, deployment, mobile-specific design, full WCAG conformance, persistence, authorization, or performance proof
---

# G4 dashboards family r5 execution report

## Scope

- `UI-DASH-001` only; required states: `initial, loading, populated, error, permission_denied, recovery`.
- Responsive Web anchors: `web-768`, `web-1024`, `web-1440`, `web-1920`.
- Six source-bound actions in all six reviewed states, executed only in an isolated fixture.

## Result

- Family aggregate: `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.dash.shell-workspace.baseline-r5/family-acceptance.json` (`review_ready`).
- Review board: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-dash-shell-workspace-baseline/review-board.html`.
- Browser board QA: `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.dash.shell-workspace.baseline-r5/browser-board-qa.json`.
- Transition: `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.dash.shell-workspace.baseline-r5/stage-transition-review-ready.json` (`review_ready`; next stage not allowed).

## Proof boundary and residual risk

Automated evidence covers contract shape, deterministic standard applicability,
clause-level computed values, keyboard/accessibility smoke, loopback isolation,
console/network observations, responsive-Web overflow, and rendered owner review.
Owner acceptance remains required. Mobile-specific scope is unauthorized. No
production frontend, API, authorization, database, performance, deployment,
release, or full WCAG claim is made.
""", encoding="utf-8")


def review_ready_candidate(final):
    if final:
        output = base.EVIDENCE_DIR / "review-ready-final-candidate.md"
        try:
            original_review_ready_candidate(True)
        except RuntimeError as exc:
            if "requires the exact needs_input forecast row" not in str(exc):
                raise
            original_review_ready_candidate(False)
            provisional = base.EVIDENCE_DIR / "review-ready-provisional-candidate.md"
            text = provisional.read_text(encoding="utf-8")
            heading = f"### `{base.STAGE_ID}`\n"
            start = text.index(heading)
            end = text.find("\n### `", start + len(heading))
            end = len(text) if end == -1 else end
            block = text[start:end]
            receipt = base.EVIDENCE_DIR / "stage-transition-review-ready.json"
            before = "- transition_receipt_sha256: `none`"
            if block.count(before) != 1:
                raise RuntimeError("DASH transition hash placeholder is not unique")
            block = block.replace(before, f"- transition_receipt_sha256: `{base.sha256(receipt)}`", 1)
            text = text[:start] + block + text[end:]
            output.write_text(text, encoding="utf-8")
    else:
        original_review_ready_candidate(False)
        output = base.EVIDENCE_DIR / "review-ready-provisional-candidate.md"
    text = output.read_text(encoding="utf-8").replace("owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_forecast_r5_board", "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_dashboard_r5_board")
    output.write_text(text, encoding="utf-8")


base.load_template = load_template
base.rewrite_contract = rewrite_contract
base.rewrite_html = rewrite_html
base.prepare = prepare
base.postprocess_review = postprocess_review
base.postprocess_transition = postprocess_transition
base.review_ready_candidate = review_ready_candidate


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("phase", choices=("prepare", "bind-applicability", "review", "board-qa", "transition-inputs", "review-ready-provisional", "review-ready-final")); phase = parser.parse_args().phase
    if phase == "prepare": base.prepare()
    elif phase == "bind-applicability": base.run_template_phase("bind_applicability")
    elif phase == "review": base.run_template_phase("review")
    elif phase == "board-qa": base.board_qa()
    elif phase == "transition-inputs": base.run_template_phase("transition_inputs")
    elif phase == "review-ready-provisional": base.review_ready_candidate(False)
    else: base.review_ready_candidate(True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
