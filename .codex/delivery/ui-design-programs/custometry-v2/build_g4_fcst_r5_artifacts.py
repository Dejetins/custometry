#!/usr/bin/env python3
"""Build the current G4 forecast-family review artifacts from the r5 G4 template."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = PROGRAM_DIR / "artifacts/g4-r5/family-fcst-shell-workspace-baseline"
EVIDENCE_DIR = PROGRAM_DIR / "evidence/family.fcst.shell-workspace.baseline-r5"
INTAKE = PROGRAM_DIR / "artifacts/g0-r5/ui-program-intake.json"
TEMPLATE = PROGRAM_DIR / "build_g4_an_r5_artifacts.py"
SCREEN_ID = "UI-FCST-001"
FAMILY_ID = "family.fcst.shell-workspace.baseline"
FAMILY_REVISION_ID = "family.fcst.shell-workspace.baseline-r5"
STAGE_ID = f"G4@{FAMILY_REVISION_ID}"
STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")
ACTION_STATES = set(STATES)


STATE_CONTENT = {
    "initial": {
        "status": "Прогнозный контур готов",
        "title": "Прогнозы готовы к первому обзору",
        "summary": "Безопасный старт списка прогнозов без production-запросов и внешних изменений.",
        "panel": "Структура списка, Result Trust и recovery controls уже на месте; реальные наборы данных не запрашиваются.",
    },
    "loading": {
        "status": "Загрузка изолированного fixture",
        "title": "Загружаем список прогнозов",
        "summary": "Сохраняем оболочку, действия и доверительную информацию доступными во время ожидания.",
        "panel": "Подготавливаем версии моделей и метаданные доверия. Внешняя сеть отключена.",
    },
    "populated": {
        "status": "7 прогнозов · 2 готовы к продвижению",
        "title": "Прогнозы и версии моделей собраны",
        "summary": "Список связывает обучение, продвижение версии и Result Trust в одной проверяемой поверхности.",
        "panel": "",
    },
    "error": {
        "status": "Ошибка чтения fixture",
        "title": "Список прогнозов временно недоступен",
        "summary": "Контекст сохранён; доступны безопасные повторные действия без внешних side effects.",
        "panel": "Проверьте локальный источник и повторите операцию. Последняя доверенная версия не изменена.",
    },
    "permission_denied": {
        "status": "Требуется разрешение forecast",
        "title": "Доступ к прогнозам ограничен",
        "summary": "Поверхность сохраняет маршрут, Result Trust и точные permission-bound действия.",
        "panel": "Для выполнения действий нужны разрешения forecast.train и forecast.promote.",
    },
    "recovery": {
        "status": "Восстановление доступно",
        "title": "Можно безопасно продолжить работу",
        "summary": "Контекст прогноза сохранён; повторные действия выполняются только в изолированном fixture.",
        "panel": "Выберите обучение или продвижение версии. Производственные данные и модели не изменяются.",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_template() -> Any:
    spec = importlib.util.spec_from_file_location("g4_fcst_template", TEMPLATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("G4 template cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.FAMILY_ID = FAMILY_ID
    module.FAMILY_REVISION_ID = FAMILY_REVISION_ID
    module.STAGE_ID = STAGE_ID
    module.ARTIFACT_DIR = ARTIFACT_DIR
    module.ARTIFACT_REF = ARTIFACT_DIR.relative_to(ROOT).as_posix()
    module.REVIEW_ASSET_DIR = ARTIFACT_DIR / "review-assets"
    module.EVIDENCE_DIR = EVIDENCE_DIR
    module.EVIDENCE_REF = EVIDENCE_DIR.relative_to(ROOT).as_posix()
    module.REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.fcst.shell-workspace.baseline-r5-report.md"
    module.NEXT_PROMPT = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-09-family-promo-shell-workspace-baseline-r5.md"
    return module


def replace_strings(value: Any) -> Any:
    replacements = {
        "UI-AN-013": SCREEN_ID,
        "/screens/55": "/screens/61",
        "/w/:workspaceKey/research": "/w/:workspaceKey/forecasts",
        "research.manage": "forecast.train",
        "finding.manage": "forecast.promote",
        "Research Manage": "Forecast Train",
        "Finding Manage": "Forecast Promote",
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


def visible_actions(screen: dict[str, Any], state: str) -> list[dict[str, Any]]:
    if state not in ACTION_STATES:
        return []
    result = []
    assertions = {
        f"{SCREEN_ID}.forecast.train": "Обучение прогноза запущено в fixture",
        f"{SCREEN_ID}.forecast.promote": "Продвижение версии подготовлено в fixture",
    }
    for action in screen["actions"]:
        action_id = action["action_id"]
        result.append({
            "action_id": action_id,
            "expected_outcome": action["outcome"],
            "side_effect_class": "none",
            "activation_policy": "execute_in_fixture",
            "outcome_assertion": {
                "kind": "dom",
                "selector": "#inspect-result",
                "property": "textContent",
                "expected": assertions[action_id],
            },
        })
    return result


def action_buttons(state: str) -> str:
    if state not in ACTION_STATES:
        return '<div class="hero-actions" aria-hidden="true"></div><p id="inspect-result" role="status" aria-live="polite"></p>'
    return (
        '<div class="hero-actions">'
        f'<button id="train-action" type="button" data-ui-element="train-action" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="{SCREEN_ID}.forecast.train">Обучить модель</button>'
        f'<button id="promote-action" type="button" data-ui-element="promote-action" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="{SCREEN_ID}.forecast.promote">Продвинуть версию</button>'
        '</div><p id="inspect-result" role="status" aria-live="polite"></p>'
    )


def populated_body() -> str:
    return """
          <section class="kpi-module" aria-labelledby="forecast-kpi-title">
            <div class="kpi-module-header"><div class="kpi-module-title"><strong id="forecast-kpi-title">Forecast portfolio</strong><span class="kpi-context">trusted lifecycle</span></div></div>
            <div class="kpi-strip" aria-label="Сводка прогнозов">
              <article class="kpi"><span class="kpi-label">Прогнозы</span><div class="kpi-value-row"><strong class="kpi-value">7</strong><span class="kpi-delta">fixture</span></div><span class="kpi-meta">активный список</span></article>
              <article class="kpi"><span class="kpi-label">Обучаются</span><div class="kpi-value-row"><strong class="kpi-value">2</strong><span class="kpi-delta">локально</span></div><span class="kpi-meta">без внешних side effects</span></article>
              <article class="kpi"><span class="kpi-label">К продвижению</span><div class="kpi-value-row"><strong class="kpi-value">2</strong><span class="kpi-delta tone-warning">review</span></div><span class="kpi-meta">требуют проверки</span></article>
              <article class="kpi"><span class="kpi-label">Горизонт</span><div class="kpi-value-row"><strong class="kpi-value">12 нед.</strong><span class="kpi-delta tone-muted">W+1</span></div><span class="kpi-meta">fixture contract</span></article>
            </div>
          </section>
          <section class="overview-grid">
            <article class="data-card trust-card"><header><div><span class="section-kicker">Result Trust</span><h2>Доверие к прогнозам</h2></div><span class="trust-score">Высокое</span></header><dl><div><dt>Snapshot</dt><dd>forecast-r-42</dd></div><div><dt>Freshness</dt><dd>8 минут</dd></div><div><dt>Backtest</dt><dd>12 недель</dd></div></dl></article>
            <article class="data-card checklist"><header><div><span class="section-kicker">Lifecycle</span><h2>Контроль версии</h2></div><span>2 / 2</span></header><ul><li class="done">forecast.train проверен в изолированном fixture</li><li class="done">forecast.promote сохраняет контекст и не меняет production</li></ul></article>
          </section>
          <section class="data-card run-card"><header><div><span class="section-kicker">Forecast list</span><h2>Версии прогнозов</h2></div><span class="quiet-pill">fixture</span></header><div class="table-wrap"><table><thead><tr><th>Прогноз</th><th>Версия</th><th>Статус</th><th>Result Trust</th></tr></thead><tbody><tr><td>Спрос по регионам</td><td>v42</td><td><span class="result success">Готов</span></td><td>Высокое</td></tr><tr><td>Промо-эластичность</td><td>v17</td><td><span class="result warning">На проверке</span></td><td>Среднее</td></tr><tr><td>Сезонность категории</td><td>v09</td><td><span class="result success">Готов</span></td><td>Высокое</td></tr></tbody></table></div></section>
"""


def article(state: str) -> str:
    content = STATE_CONTENT[state]
    if state == "populated":
        body = populated_body()
    else:
        body = (
            f'<section class="state-panel {state}-panel" role="status">'
            f'<span class="status-mark">{content["status"]}</span>'
            f'<h2>{content["title"]}</h2><p>{content["panel"]}</p></section>'
        )
    return f"""        <article id="overview-content" data-ui-region="{SCREEN_ID}.content" data-ui-element="overview-content" data-state="{state}">
          <section class="hero">
            <div><span class="eyebrow">Прогнозирование · модели</span><h2>{content["title"]}</h2><p>{content["summary"]}</p></div>
            <div>{action_buttons(state)}</div>
          </section>
{body}
          <footer class="evidence-footer"><span>Изолированный fixture · не production data</span><span>Responsive Web 768–1920 · mobile scope не авторизован</span></footer>
        </article>
"""


def rewrite_html(path: Path, state: str, fixture_sha: str) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace("UI-AN-013", SCREEN_ID).replace("Custometry · Research ·", "Custometry · Forecasts ·").replace("#research-action", "#train-action").replace("#finding-action", "#promote-action")
    html = re.sub(r'<meta name="ui-fixture-sha256" content="[0-9a-f]{64}">', f'<meta name="ui-fixture-sha256" content="{fixture_sha}">', html)
    html = re.sub(
        r'<header id="page-header".*?</header>',
        f'<header id="page-header" data-ui-region="shell.page-header" data-ui-element="page-header"><div class="header-copy"><span class="eyebrow">Custometry · North Star</span><h1>Прогнозы</h1></div><div class="status-chip" role="status">{STATE_CONTENT[state]["status"]}</div></header>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    start = html.index('        <article id="overview-content"')
    end = html.index("      </main>", start)
    html = html[:start] + article(state) + html[end:]
    if state in ACTION_STATES:
        script = (
            '<script>const result=document.getElementById("inspect-result");'
            'document.getElementById("train-action").addEventListener("click",()=>{result.textContent="Обучение прогноза запущено в fixture";});'
            'document.getElementById("promote-action").addEventListener("click",()=>{result.textContent="Продвижение версии подготовлено в fixture";});</script>'
        )
    else:
        script = '<script>const result=document.getElementById("inspect-result");</script>'
    html = re.sub(r"<script>.*?</script>", script, html, count=1, flags=re.DOTALL)
    path.write_text(html, encoding="utf-8")


def rewrite_contract(path: Path, state: str, screen: dict[str, Any], fixture_sha: str) -> None:
    contract = replace_strings(json.loads(path.read_text(encoding="utf-8")))
    state_id = f"{SCREEN_ID}.{state}"
    contract["screen_revision_id"] = f"{state_id}.all.ru.graphite@r5"
    contract["functional_contract_ref"].update({"json_pointer": "/screens/61", "screen_id": SCREEN_ID})
    contract["product_identity"].update({
        "screen_id": SCREEN_ID,
        "route_id": SCREEN_ID,
        "route": screen["route"],
        "state_id": state_id,
        "role_id": "ML",
        "permission_profile": "forecast.train",
    })
    contract["comparison_claims"]["implementation_logical_artifact_id"] = contract["screen_revision_id"]
    contract["interaction_contract"]["visible_actions"] = visible_actions(screen, state)
    contract["render_environment"]["fixture_data_sha256"] = fixture_sha
    contract["regions"] = replace_strings(contract["regions"])
    for region in contract["regions"]:
        if region["region_id"].endswith(".content"):
            region["region_id"] = f"{SCREEN_ID}.content"
        region["source_refs"] = [{"kind": "product_contract", "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json#/screens/61"}]
    base_elements = []
    action_templates: dict[str, dict[str, Any]] = {}
    for element in contract["element_contracts"]:
        if element["element_id"] == "research-action":
            action_templates["train-action"] = element
        elif element["element_id"] == "finding-action":
            action_templates["promote-action"] = element
        elif element["element_id"] not in {"comments-action", "add-comment-action", "resolve-comment-action", "continue-action"}:
            base_elements.append(element)
    for element in base_elements:
        element["state_ids"] = [state_id]
        if element["region_id"].endswith(".content"):
            element["region_id"] = f"{SCREEN_ID}.content"
        element["source_refs"] = [{"kind": "product_contract", "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json#/screens/61"}]
    if state in ACTION_STATES:
        action_specs = (
            ("train-action", f"{SCREEN_ID}.forecast.train"),
            ("promote-action", f"{SCREEN_ID}.forecast.promote"),
        )
        for element_id, action_id in action_specs:
            element = copy.deepcopy(action_templates[element_id])
            element["element_id"] = element_id
            element["locator"] = f"#{element_id}"
            element["region_id"] = f"{SCREEN_ID}.content"
            element["action_ids"] = [action_id]
            element["state_ids"] = [state_id]
            element["source_refs"] = [{"kind": "product_contract", "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json#/screens/61"}]
            base_elements.append(element)
    contract["element_contracts"] = base_elements
    write_json(path, contract)


def prepare() -> None:
    module = load_template()
    module.prepare()
    intake = json.loads(INTAKE.read_text(encoding="utf-8"))
    matches = [item for item in intake["screens"] if item["screen_id"] == SCREEN_ID]
    if len(matches) != 1:
        raise RuntimeError("forecast screen binding is not unique")
    screen = matches[0]
    for state in STATES:
        state_dir = ARTIFACT_DIR / "states" / state
        fixture_path = state_dir / "fixture.json"
        fixture = {
            "schema_id": "custometry.ui-review-fixture/v1",
            "screen_id": SCREEN_ID,
            "state_id": f"{SCREEN_ID}.{state}",
            "clock": "2026-02-14T10:00:00+03:00",
            "locale": "ru",
            "theme": "graphite",
            "safety": "isolated_local_no_real_data",
            "content": {"eyebrow": "Прогнозирование · модели", **STATE_CONTENT[state], "tone": "neutral"},
        }
        write_json(fixture_path, fixture)
        fixture_sha = sha256(fixture_path)
        rewrite_html(state_dir / "screen.html", state, fixture_sha)
        rewrite_contract(state_dir / "screen-contract.json", state, screen, fixture_sha)
    write_json(ARTIFACT_DIR / "reuse-decision.json", {
        "schema_id": "codex.ui-family-reuse-decision/v2",
        "family_id": FAMILY_ID,
        "representative_screen_ids": [SCREEN_ID],
        "individually_designed_screen_ids": [SCREEN_ID],
        "reuse_only_screen_ids": [f"UI-FCST-{index:03d}" for index in range(2, 8)],
        "decision": "Use one exact list-family representative while preserving each later route's product-owned semantics.",
        "scope_limit": "No individual design or acceptance claim is made for UI-FCST-002 through UI-FCST-007.",
        "result": "recorded",
    })
    print(json.dumps({"status": "prepared", "stage": STAGE_ID, "screen": SCREEN_ID, "states": list(STATES)}, indent=2))


def build_program_snapshot(module: Any) -> Path:
    projection = json.loads(module.G1_INVENTORY.read_text(encoding="utf-8"))
    matched = [row for row in projection["screens"] if row.get("screen_id") == SCREEN_ID]
    if len(matched) != 1:
        raise RuntimeError("G1 projection cannot resolve exactly one forecast representative")
    matched[0]["required_states"] = [f"{SCREEN_ID}.{state}" for state in STATES]
    projection_path = ARTIFACT_DIR / "g1-admission-inventory.family-projection.json"
    write_json(projection_path, projection)

    snapshot = json.loads(module.PROGRAM.read_text(encoding="utf-8"))
    source_ref = module.rel(module.G1_INVENTORY)
    for source in snapshot["source_contracts"]:
        if source.get("path") == source_ref:
            source["screen_collections"] = []
    snapshot["source_contracts"].append({
        "path": module.rel(projection_path),
        "authority": f"G4 stage-owned full-inventory projection adding only accepted required states for {SCREEN_ID}",
        "required_status": "complete",
        "sha256": sha256(projection_path),
        "screen_collections": [{"json_pointer": "/screens", "id_key": "screen_id"}],
        "journey_collections": [],
    })
    for entry in snapshot["screens"]:
        if entry.get("screen_ref", {}).get("path") == source_ref:
            entry["screen_ref"]["path"] = module.rel(projection_path)
    screen_entries = ARTIFACT_DIR / "program-screen-entries.snapshot.json"
    write_json(screen_entries, {"screens": snapshot["screens"]})
    screen_index = ARTIFACT_DIR / "screens-index.snapshot.json"
    write_json(screen_index, {
        "$schema": "program-artifact-index.schema.json",
        "schema_id": "codex.ui-program-artifact-index/v1",
        "program_id": module.PROGRAM_ID,
        "program_revision": 5,
        "index_kind": "screens",
        "entries": [
            {"id": entry["screen_ref"]["expected_id"], "path": module.rel(screen_entries), "sha256": sha256(screen_entries), "json_pointer": f"/screens/{index}"}
            for index, entry in enumerate(snapshot["screens"])
        ],
    })
    snapshot["artifact_indexes"]["screens"] = {"path": module.rel(screen_index), "sha256": sha256(screen_index)}
    snapshot_path = ARTIFACT_DIR / "ui-design-program.snapshot.json"
    snapshot["execution_artifacts"]["plan_doc"] = module.rel(snapshot_path)
    write_json(snapshot_path, snapshot)
    write_json(ARTIFACT_DIR / "program-snapshot-binding.json", {
        "schema_id": "codex.ui-stage-program-snapshot-binding/v1",
        "canonical_program": {"path": module.rel(module.PROGRAM), "sha256": sha256(module.PROGRAM)},
        "snapshot": {"path": module.rel(snapshot_path), "sha256": sha256(snapshot_path)},
        "projection": {"path": module.rel(projection_path), "sha256": sha256(projection_path)},
        "screen_index_snapshot": {"path": module.rel(screen_index), "sha256": sha256(screen_index)},
        "changed_pointers": ["/source_contracts", "/screens/*/screen_ref/path", "/artifact_indexes/screens", "/execution_artifacts/plan_doc"],
        "reason": f"Family aggregation adds exact accepted required_states only for {SCREEN_ID}; no other inventory meaning changes.",
        "accepted_authority_changed": False,
        "result": "passed",
    })
    return snapshot_path


def postprocess_review(module: Any) -> None:
    board_path = ARTIFACT_DIR / "review-board.html"
    board = board_path.read_text(encoding="utf-8")
    replacements = {
        "Custometry · Research family review": "Custometry · Forecast family review",
        "Research, состояние": "Forecasts, состояние",
        "<h1>Исследования</h1>": "<h1>Прогнозы</h1>",
        "Шесть обязательных состояний research-list контракта: компактная Graphite shell, явный Result Trust, шесть source-bound fixture-действий в применимых состояниях и адаптивный Web 768–1920.": "Шесть обязательных состояний forecast-list контракта: компактная Graphite shell, явный Result Trust, две source-bound fixture-команды и адаптивный Web 768–1920.",
    }
    for before, after in replacements.items():
        board = board.replace(before, after)
    board_path.write_text(board, encoding="utf-8")
    packet_path = EVIDENCE_DIR / "owner-review-decision-packet.md"
    packet = packet_path.read_text(encoding="utf-8")
    packet = packet.replace("Готовые исследования", "Готовые прогнозы").replace("`UI-AN-013`", f"`{SCREEN_ID}`").replace("research-list", "forecast-list")
    packet_path.write_text(packet, encoding="utf-8")


def postprocess_transition() -> None:
    next_stage = "G4@family.promo.shell-workspace.baseline-r5"
    next_target = "family.promo.shell-workspace.baseline-r5"
    next_inputs = EVIDENCE_DIR / "preflight/next_stage_inputs.json"
    value = json.loads(next_inputs.read_text(encoding="utf-8"))
    value["facts"]["next_stage_id"] = next_stage
    write_json(next_inputs, value)
    request_path = EVIDENCE_DIR / "stage-transition-request-review-ready.json"
    request = json.loads(request_path.read_text(encoding="utf-8"))
    request.update({
        "to_stage_id": next_stage,
        "to_target": next_target,
        "summary": "Forecasts exact-cover all six required states, both functional actions, and four responsive-Web anchors; machine proof is ready for owner review.",
        "questions": ["Принимаете готовую family review board прогнозов или хотите небольшие правки?"],
    })
    write_json(request_path, request)
    report = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.fcst.shell-workspace.baseline-r5-report.md"
    text = report.read_text(encoding="utf-8")
    text = text.replace("six UI-AN-013 states", "six UI-FCST-001 states").replace("analytics research", "forecast").replace("`UI-AN-013` only", "`UI-FCST-001` only").replace("all six source-bound `UI-AN-013` actions in the four applicable states", "both source-bound `UI-FCST-001` actions in all six reviewed states")
    report.write_text(text, encoding="utf-8")


def board_qa() -> None:
    path = PROGRAM_DIR / "run_g4_an_r5_board_qa.py"
    spec = importlib.util.spec_from_file_location("g4_fcst_board_qa", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("board QA module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ART = ARTIFACT_DIR
    module.EVID = EVIDENCE_DIR
    module.BOARD = ARTIFACT_DIR / "review-board.html"
    module.POPULATED = ARTIFACT_DIR / "states/populated/screen.html"
    module.OUTPUT = EVIDENCE_DIR / "browser-board-qa.json"
    module.SCREENSHOT = EVIDENCE_DIR / "review-board-1440.png"
    module.SERVER_LOG = EVIDENCE_DIR / "review-board-bundle-server.log"
    module.SESSION = "g4-fcst-r5-board-qa"
    module.PORT = 41738
    result = module.main()
    document = json.loads(module.OUTPUT.read_text(encoding="utf-8"))
    document["stage_instance_id"] = STAGE_ID
    document["generated_by"]["script"] = Path(__file__).name
    write_json(module.OUTPUT, document)
    if result != 0:
        raise RuntimeError("forecast family board QA failed")


def review_ready_candidate(final: bool) -> None:
    import sys

    sys.path.insert(0, str(PROGRAM_DIR))
    from build_blueprint_rebind_r5 import render_ledger

    sys.path.insert(0, "/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
    from validate_stage_ledger import parse_ledger

    ledger = PROGRAM_DIR / "stage-ledger.md"
    parsed, errors = parse_ledger(ledger)
    if errors:
        raise RuntimeError("ledger parse failed: " + "; ".join(errors))
    front = dict(parsed["frontmatter"])
    rows = [dict(row) for row in parsed["rows"]]
    details = {key: dict(value) for key, value in parsed["details"].items()}
    matches = [row for row in rows if row["Stage instance"] == STAGE_ID]
    required_status = "needs_input" if final else "in_progress"
    if len(matches) != 1 or matches[0]["Status"] != required_status:
        raise RuntimeError(f"review-ready candidate requires the exact {required_status} forecast row")
    receipt = EVIDENCE_DIR / "stage-transition-review-ready.json"
    if final and not receipt.is_file():
        raise RuntimeError("final review-ready candidate requires the assembled transition receipt")
    matches[0].update({
        "Status": "needs_input",
        "Evidence": ARTIFACT_DIR.relative_to(ROOT).as_posix() + "/review-board.html",
        "Transition receipt": receipt.relative_to(ROOT).as_posix(),
    })
    details[STAGE_ID].update({
        "decision_packet": (EVIDENCE_DIR / "owner-review-decision-packet.md").relative_to(ROOT).as_posix(),
        "resume_condition": "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_forecast_r5_board",
        "resume_evidence_ref": "none",
        "resume_evidence_sha256": "none",
        "transition_receipt": receipt.relative_to(ROOT).as_posix(),
        "transition_receipt_sha256": sha256(receipt) if final else "none",
        "execution_allowed": "true",
    })
    front.update({"ledger_status": "awaiting_input", "current_stage": STAGE_ID, "Next stage allowed": "false"})
    output = EVIDENCE_DIR / ("review-ready-final-candidate.md" if final else "review-ready-provisional-candidate.md")
    output.write_text(render_ledger(front, rows, details), encoding="utf-8")
    print(json.dumps({"status": "candidate_prepared", "kind": "final" if final else "provisional", "output": output.relative_to(ROOT).as_posix(), "sha256": sha256(output)}, indent=2))


def run_template_phase(name: str) -> None:
    module = load_template()
    if name == "bind_applicability":
        assembler = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/assemble_standard_applicability.py")
        baseline = PROGRAM_DIR / "artifacts/g0-r5/platform-ui-baseline.json"
        for state in STATES:
            contract = ARTIFACT_DIR / "states" / state / "screen-contract.json"
            output = EVIDENCE_DIR / "states" / state / "standard-applicability.json"
            subprocess.run([
                "python3", str(assembler), "--screen", str(contract), "--baseline", str(baseline),
                "--project-root", str(ROOT), "--output", str(output),
            ], check=True)
    if name == "review":
        module.STATE_COPY = {state: {"title": STATE_CONTENT[state]["title"], "status": STATE_CONTENT[state]["status"]} for state in STATES}
        module.build_program_snapshot = lambda: build_program_snapshot(module)
    getattr(module, name)()
    if name == "review":
        postprocess_review(module)
    elif name == "transition_inputs":
        postprocess_transition()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "bind-applicability", "review", "board-qa", "transition-inputs", "review-ready-provisional", "review-ready-final"))
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare()
    elif args.phase == "bind-applicability":
        run_template_phase("bind_applicability")
    elif args.phase == "review":
        run_template_phase("review")
    elif args.phase == "board-qa":
        board_qa()
    elif args.phase == "review-ready-provisional":
        review_ready_candidate(False)
    elif args.phase == "review-ready-final":
        review_ready_candidate(True)
    else:
        run_template_phase("transition_inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
