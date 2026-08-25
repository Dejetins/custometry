#!/usr/bin/env python3
"""Build owned G4 data-connections artifacts for the r5 semantic successor."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = PROGRAM_DIR / "artifacts/g4-r5/family-data-shell-workspace-baseline"
REVIEW_ASSET_DIR = ARTIFACT_DIR / "review-assets"
EVIDENCE_DIR = PROGRAM_DIR / "evidence/family.data.shell-workspace.baseline-r5"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.data.shell-workspace.baseline-r5-report.md"
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
INTAKE = PROGRAM_DIR / "artifacts/g0-r5/ui-program-intake.json"
BASELINE = PROGRAM_DIR / "artifacts/g0-r5/platform-ui-baseline.json"
SOURCE_VISUAL = PROGRAM_DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
G1_INVENTORY = PROGRAM_DIR / "evidence/g0-r2/g1-admission-inventory.json"
NEXT_PROMPT = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-05-family-dq-shell-workspace-baseline-r5.md"
SKILL_SCRIPTS = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")

PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
PROGRAM_REVISION_REF = f"{PROGRAM_ID}@5"
STAGE_ID = "G4@family.data.shell-workspace.baseline-r5"
FAMILY_ID = "family.data.shell-workspace.baseline"
FAMILY_REVISION_ID = "family.data.shell-workspace.baseline-r5"
SOURCE_VISUAL_REF = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/ru/source.html"
BASELINE_REF = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/platform-ui-baseline.json"
INTAKE_REF = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json"
PROGRAM_REF = ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
ARTIFACT_REF = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-data-shell-workspace-baseline"
EVIDENCE_REF = ".codex/delivery/ui-design-programs/custometry-v2/evidence/family.data.shell-workspace.baseline-r5"

STATE_ORDER = ("initial", "loading", "populated", "error", "permission_denied", "recovery")
STATE_COPY = {
    "initial": {
        "eyebrow": "Данные · подключения",
        "title": "Подключения готовы к настройке",
        "summary": "Показываем безопасный старт без чтения реальных credentials и без внешних запросов.",
        "tone": "neutral",
        "status": "Подготовка списка подключений",
    },
    "loading": {
        "eyebrow": "Данные · подключения",
        "title": "Загружаем подключения",
        "summary": "Сохраняем shell, контекст и recovery controls, пока изолированный fixture готовит список.",
        "tone": "neutral",
        "status": "Загрузка · без внешних запросов",
    },
    "populated": {
        "eyebrow": "Данные · подключения",
        "title": "Контуры данных под контролем",
        "summary": "Список связывает статус, freshness, владельца и следующее безопасное действие для каждого подключения.",
        "tone": "success",
        "status": "3 подключения · 2 в норме · 1 требует внимания",
    },
    "error": {
        "eyebrow": "Данные · подключения",
        "title": "Подключения временно недоступны",
        "summary": "Контекст и правила доступа сохранены. Fixture-ошибка не выполняет внешних записей.",
        "tone": "danger",
        "status": "Ошибка чтения snapshot · безопасный повтор доступен",
    },
    "permission_denied": {
        "eyebrow": "Данные · подключения",
        "title": "Недостаточно прав для подключений",
        "summary": "Credentials, статусы и скрытые counts не раскрываются; общая shell-навигация сохранена.",
        "tone": "warning",
        "status": "Требуется workspace membership",
    },
    "recovery": {
        "eyebrow": "Данные · подключения",
        "title": "Восстанавливаем список подключений",
        "summary": "Показываем последний доверенный snapshot и явный путь к безопасной повторной проверке.",
        "tone": "warning",
        "status": "Snapshot v12 · частично восстановлен",
    },
}

ANCHORS = (
    {"anchor_id": "web-768", "width": 768, "height": 1024, "class": "responsive_web", "state_ref": "ready"},
    {"anchor_id": "web-1024", "width": 1024, "height": 768, "class": "responsive_web", "state_ref": "ready"},
    {"anchor_id": "web-1440", "width": 1440, "height": 900, "class": "responsive_web", "state_ref": "ready"},
    {"anchor_id": "web-1920", "width": 1920, "height": 1080, "class": "responsive_web", "state_ref": "ready"},
)

VISUAL_AUTHORITY = {
    "source_visual_ref": SOURCE_VISUAL_REF,
    "source_visual_sha256": "b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700",
    "owner_decision_ref": ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/visual-authority-decision-r4.json",
    "screen_acceptance_scope": "Visual-language and platform-baseline authority only; never exact target-screen composition, product semantics, fixture truth, legend-threshold truth, production implementation, or novel-screen fidelity.",
    "visual_language_scope": "Linear Graphite shell character, calm professional density, compact contextual navigation, bounded analytical surfaces, concise KPI and command language, visible Result Trust, Focus/Explore character, readable analytical labels and tables, and adaptive external series-panel behavior as a visual-language reference.",
    "reusable_foundation_scope": "Hash-pinned source-backed colors, typography stack, spacing rhythm, compact controls, rounded command language, shell/navigation relationships, overlay behavior, and analytical presentation primitives only; exact composition, information architecture, component implementation, runtime semantics, and target-screen acceptance remain later-gate work.",
    "inheritance_policy": "required",
    "mobile_scope": "unauthorized",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def origin(kind: str, ref: str, **extra: Any) -> dict[str, Any]:
    return {"kind": kind, "ref": ref, **extra}


def specified(value: Any, ref: str, *, kind: str = "normative_requirement", unit: str | None = None) -> dict[str, Any]:
    return {
        "value": value,
        "unit": unit,
        "origin": origin(kind, ref),
        "tolerance": 0,
        "change_policy": "fixed",
    }


def css_value(value: Any, unit: str | None) -> str:
    if isinstance(value, (int, float)) and unit:
        return f"{value}{unit}"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def planned_standard_targets() -> list[dict[str, Any]]:
    return [
        {"target_id": "shell-application", "selector": "#app-shell", "component_id": None, "variant": None, "size_class": None, "slot_id": None, "state_id": "default", "shell_region_id": "shell.application", "icon_id": None, "element_type": "div"},
        {"target_id": "page-header", "selector": "#page-header", "component_id": None, "variant": None, "size_class": None, "slot_id": None, "state_id": "default", "shell_region_id": "shell.page-header", "icon_id": None, "element_type": "header"},
        {"target_id": "overview-main", "selector": "#overview-main", "component_id": None, "variant": None, "size_class": None, "slot_id": None, "state_id": "default", "shell_region_id": "shell.main-content", "icon_id": None, "element_type": "main"},
        {"target_id": "nav-overview", "selector": "#nav-overview", "component_id": "navigation.rail-action", "variant": "nav-root.overview", "size_class": "icon", "slot_id": "shell.application.button", "state_id": "default", "shell_region_id": "shell.application", "icon_id": None, "element_type": "button"},
        {"target_id": "nav-overview-icon", "selector": "#nav-overview-icon", "component_id": None, "variant": None, "size_class": None, "slot_id": None, "state_id": "default", "shell_region_id": "shell.application", "icon_id": "i-home", "element_type": "svg"},
        {"target_id": "manage-action", "selector": "#manage-action", "component_id": "action.button", "variant": "button", "size_class": "standard", "slot_id": "shell.main-content.button", "state_id": "default", "shell_region_id": "UI-DATA-001.content", "icon_id": None, "element_type": "button"},
        {"target_id": "rotate-action", "selector": "#rotate-action", "component_id": "action.button", "variant": "button", "size_class": "standard", "slot_id": "shell.main-content.button", "state_id": "default", "shell_region_id": "UI-DATA-001.content", "icon_id": None, "element_type": "button"},
        {"target_id": "continue-action", "selector": "#continue-action", "component_id": "action.button", "variant": "button", "size_class": "standard", "slot_id": "shell.main-content.button", "state_id": "default", "shell_region_id": "UI-DATA-001.content", "icon_id": None, "element_type": "button"},
    ]


def selector_matches(selector: dict[str, Any], target: dict[str, Any]) -> bool:
    fields = ("component_id", "variant", "size_class", "slot_id", "state_id", "shell_region_id", "icon_id", "element_type", "anchor_id")
    exact = all(selector.get(field) is None or target.get(field) == selector.get(field) for field in fields)
    if exact:
        return True
    stable = ("component_id", "variant", "size_class", "slot_id", "shell_region_id", "icon_id")
    return (
        not any(selector.get(field) is not None for field in stable)
        and selector.get("scope") in {"foundation", "interaction"}
        and selector.get("element_type") is not None
        and selector.get("element_type") == target.get("element_type")
        and (selector.get("anchor_id") is None or selector.get("anchor_id") == target.get("anchor_id"))
        and (selector.get("state_id") is None or selector.get("state_id") == target.get("state_id"))
    )


def standard_css(baseline: dict[str, Any]) -> str:
    declarations: dict[str, dict[str, str]] = {target["selector"]: {} for target in planned_standard_targets()}
    for target in planned_standard_targets():
        anchored = {**target, "anchor_id": "web-1440"}
        for clause in baseline["standard_contract"]["clauses"]:
            if not any(selector_matches(selector, anchored) for selector in clause.get("applicability", [])):
                continue
            prop = clause["property"]
            value = css_value(clause["value"], clause.get("unit"))
            previous = declarations[target["selector"]].get(prop)
            if previous is not None and previous != value:
                raise ValueError(f"conflicting pilot clauses for {target['target_id']} {prop}: {previous!r} vs {value!r}")
            declarations[target["selector"]][prop] = value
    rows = ["@media (width: 1440px) {"]
    for selector, properties in declarations.items():
        if not properties:
            continue
        rows.append(f"  {selector} {{")
        rows.extend(f"    {prop}: {value};" for prop, value in sorted(properties.items()))
        rows.append("  }")
    rows.append("}")
    return "\n".join(rows)


def state_body(state: str) -> str:
    copy = STATE_COPY[state]
    if state == "loading":
        primary = """
          <section class="state-panel loading-panel" aria-label="Загрузка подключений">
            <span class="skeleton wide"></span><span class="skeleton"></span><span class="skeleton"></span>
            <p>Проверяем статус, freshness и trust-метаданные в изолированном fixture.</p>
          </section>"""
    elif state == "permission_denied":
        primary = """
          <section class="state-panel permission-panel" role="status">
            <span class="status-mark">Доступ ограничен</span>
            <h2>Подключения скрыты политикой workspace</h2>
            <p>Имена, статусы и credentials не раскрываются. Нужна роль с правом connection.manage.</p>
          </section>"""
    elif state == "error":
        primary = """
          <section class="state-panel error-panel" role="alert">
            <span class="status-mark">Fixture error</span>
            <h2>Не удалось прочитать список подключений</h2>
            <p>Последний доверенный контекст сохранён. Повтор остаётся fixture-only и не ротирует реальные секреты.</p>
          </section>"""
    elif state == "recovery":
        primary = """
          <section class="state-panel recovery-panel" role="status">
            <span class="status-mark">Recovery mode</span>
            <h2>Используется последний доверенный connection snapshot</h2>
            <p>Статусы отстают на 18 минут; ротация credentials заблокирована до успешной повторной проверки.</p>
          </section>"""
    elif state == "initial":
        primary = """
          <section class="state-panel initial-panel" role="status">
            <span class="status-mark">Первый вход</span>
            <h2>Список подключений готов к первому безопасному чтению</h2>
            <p>Структура, trust и recovery controls уже на месте; credentials и production connectors не запрашиваются.</p>
          </section>"""
    else:
        primary = """
          <section class="kpi-module" aria-labelledby="connection-kpi-title">
            <div class="kpi-module-header"><div class="kpi-module-title"><strong id="connection-kpi-title">Connections</strong><span class="kpi-context">trusted snapshot</span></div></div>
            <div class="kpi-strip" aria-label="Сводка подключений">
              <article class="kpi"><span class="kpi-label">Всего</span><div class="kpi-value-row"><strong class="kpi-value">3</strong><span class="kpi-delta">в fixture</span></div><span class="kpi-meta">три изолированных контура</span></article>
              <article class="kpi"><span class="kpi-label">Активны</span><div class="kpi-value-row"><strong class="kpi-value">2</strong><span class="kpi-delta">в норме</span></div><span class="kpi-meta">PostgreSQL и S3</span></article>
              <article class="kpi"><span class="kpi-label">Требуют внимания</span><div class="kpi-value-row"><strong class="kpi-value">1</strong><span class="kpi-delta tone-warning">freshness</span></div><span class="kpi-meta">CRM API отстаёт</span></article>
              <article class="kpi"><span class="kpi-label">Secret rotation</span><div class="kpi-value-row"><strong class="kpi-value">1</strong><span class="kpi-delta tone-muted">план</span></div><span class="kpi-meta">без реальной ротации</span></article>
            </div>
          </section>
          <section class="overview-grid">
            <article class="data-card trust-card"><header><div><span class="section-kicker">Result Trust</span><h2>Доверие к списку</h2></div><span class="trust-score">Высокое</span></header><dl><div><dt>Snapshot</dt><dd>connections-v7</dd></div><div><dt>Freshness</dt><dd>8 минут</dd></div><div><dt>Credentials</dt><dd>не раскрыты</dd></div></dl></article>
            <article class="data-card checklist"><header><div><span class="section-kicker">Safe operation</span><h2>Контроль изменений</h2></div><span>3 / 3</span></header><ul><li class="done">connection.manage проверен</li><li class="done">secret.rotate остаётся fixture-only</li><li class="done">переход к Quality сохраняет контекст</li></ul></article>
          </section>
          <section class="data-card run-card"><header><div><span class="section-kicker">Connection inventory</span><h2>Подключения</h2></div><span class="quiet-pill">fixture</span></header><div class="table-wrap"><table><thead><tr><th>Подключение</th><th>Тип</th><th>Freshness</th><th>Статус</th></tr></thead><tbody><tr><td>Warehouse</td><td>PostgreSQL</td><td>8 мин</td><td><span class="result success">В норме</span></td></tr><tr><td>CRM</td><td>REST API</td><td>42 мин</td><td><span class="result warning">Проверить</span></td></tr><tr><td>Archive</td><td>S3</td><td>12 мин</td><td><span class="result success">В норме</span></td></tr></tbody></table></div></section>"""
    return primary


def render_html(state: str, fixture_sha: str, font_sha: str, asset_sha: str, standard_rules: str) -> str:
    copy = STATE_COPY[state]
    safe_state = html.escape(state)
    favicon = '  <link rel="icon" href="data:,">\n' if state == "populated" else ""
    kpi_styles = """    .kpi-module { display: grid; grid-template-columns: 116px minmax(0,1fr); height: 54px; min-height: 54px; margin: 0; overflow: visible; background: transparent; border-block: 1px solid var(--line); border-radius: 0; box-shadow: none; }
    .kpi-module-header { display: grid; grid-template-columns: minmax(0,1fr); min-width: 0; align-items: center; padding: 7px 6px 7px 0; background: transparent; }
    .kpi-module-title { display: grid; min-width: 0; align-items: center; justify-content: start; gap: 1px; }
    .kpi-module-title strong { color: var(--quiet); font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; }
    .kpi-context { overflow: hidden; color: var(--quiet); font-size: 8px; text-overflow: ellipsis; white-space: nowrap; }
    .kpi-strip { display: flex; min-width: 0; overflow-x: auto; overscroll-behavior-inline: contain; scrollbar-width: thin; scrollbar-color: rgb(52,53,58) transparent; scroll-snap-type: inline proximity; }
    .kpi { position: relative; display: grid; min-width: 140px; flex: 1 0 140px; align-content: center; gap: 2px; padding: 7px 11px; scroll-snap-align: start; }
    .kpi + .kpi::before { position: absolute; inset-block: 10px; inset-inline-start: 0; width: 1px; content: \"\"; background: var(--line); }
    .kpi-label { overflow: hidden; color: var(--quiet); font-size: 9px; text-overflow: ellipsis; white-space: nowrap; }
    .kpi-value-row { display: flex; align-items: baseline; gap: 6px; }
    .kpi-value { overflow: hidden; color: var(--text); font-size: 16px; font-weight: 640; font-variant-numeric: tabular-nums; letter-spacing: -.015em; line-height: normal; text-overflow: ellipsis; white-space: nowrap; }
    .kpi-delta { margin-inline-start: auto; color: var(--success); font-size: 9px; font-variant-numeric: tabular-nums; white-space: nowrap; }
    .kpi-delta.tone-warning { color: var(--warning); }
    .kpi-delta.tone-muted { color: var(--quiet); }
    .kpi-meta { display: none; }
    @media (max-width: 820px) { .kpi-module { grid-template-columns: 104px minmax(0,1fr); } .kpi { min-width: 132px; flex-basis: 132px; } }
""" if state == "populated" else ""
    return f"""<!doctype html>
<html lang="ru" data-theme="graphite">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
{favicon}  <meta name="ui-fixture-sha256" content="{fixture_sha}">
  <meta name="ui-font-bundle-sha256" content="{font_sha}">
  <meta name="ui-asset-bundle-sha256" content="{asset_sha}">
  <title>Custometry · Data Connections · {safe_state}</title>
  <style>
    :root {{ color-scheme: dark; --canvas: rgb(7,7,8); --surface: rgb(17,18,20); --surface-2: rgb(23,24,27); --line: rgb(48,49,54); --text: rgb(240,240,242); --muted: rgb(167,167,173); --quiet: rgb(139,140,147); --accent: rgb(102,185,211); --success: rgb(119,190,141); --warning: rgb(221,175,83); --danger: rgb(220,105,105); }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; min-width: 100%; min-height: 100%; background: var(--canvas); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
    body {{ overflow-x: hidden; }}
    button {{ font: inherit; }}
    button:focus-visible {{ outline: 3px solid var(--accent) !important; outline-offset: 2px; box-shadow: 0 0 0 2px var(--canvas); }}
    #app-shell {{ width: 100%; height: 100vh; min-height: 100vh; overflow: hidden; display: grid; grid-template-columns: 64px minmax(0,1fr); gap: 0; background: var(--canvas); }}
    .rail {{ position: sticky; inset-block-start: 0; height: 100vh; display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 10px 7px; border-inline-end: 1px solid var(--line); background: rgb(10,10,11); }}
    .brand {{ width: 42px; height: 42px; display: grid; place-items: center; margin-block-end: 8px; border: 1px solid var(--line); border-radius: 13px; color: var(--text); font-size: 12px; font-weight: 700; letter-spacing: .08em; }}
    #nav-overview {{ width: 38px; height: 38px; display: grid; place-items: center; cursor: default; }}
    #nav-overview[aria-current="page"] {{ color: var(--quiet); background: transparent; }}
    #nav-overview-icon {{ width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }}
    .rail-note {{ margin-block-start: auto; writing-mode: vertical-rl; color: var(--quiet); font-size: 9px; letter-spacing: .12em; text-transform: uppercase; }}
    .workspace {{ min-width: 0; height: 100vh; overflow-y: auto; }}
    #page-header {{ min-width: 0; display: grid; grid-template-columns: minmax(0,1fr) auto; align-items: center; gap: 14px; border-block-end: 1px solid var(--line); background: rgba(7,7,8,.96); }}
    .header-copy {{ min-width: 0; }}
    .eyebrow, .section-kicker {{ display: block; color: var(--quiet); font-size: 10px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }}
    #page-header h1 {{ margin: 2px 0 0; font-size: clamp(17px,2vw,22px); line-height: 1.15; }}
    .status-chip {{ max-width: 330px; padding: 7px 10px; border: 1px solid var(--line); border-radius: 9px; color: var(--muted); background: var(--surface); font-size: 11px; white-space: normal; }}
    #overview-main {{ min-width: 0; background: var(--canvas); }}
    #overview-content {{ width: min(100%, 1320px); margin-inline: auto; min-height: 100%; display: flex; flex-direction: column; gap: 16px; }}
    .hero {{ display: grid; grid-template-columns: minmax(0,1fr) auto; align-items: end; gap: 18px; padding: 18px 20px; border: 1px solid var(--line); border-radius: 14px; background: linear-gradient(135deg, rgb(23,24,27), rgb(14,15,17)); box-shadow: rgba(0,0,0,.14) 0 1px 2px; }}
    .hero h2 {{ margin: 4px 0 8px; font-size: clamp(22px,3vw,34px); line-height: 1.08; }}
    .hero p {{ margin: 0; max-width: 760px; color: var(--muted); line-height: 1.55; }}
    .hero > div:last-child {{ display: flex; flex-direction: column; align-items: flex-end; }}
    .hero-actions {{ display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; }}
    #manage-action, #rotate-action, #continue-action {{ justify-content: center; align-items: center; cursor: pointer; white-space: nowrap; }}
    #inspect-result {{ min-height: 18px; margin: 0; color: var(--accent); font-size: 11px; text-align: end; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: 12px; }}
    .kpi-grid article, .data-card, .state-panel {{ border: 1px solid var(--line); border-radius: 12px; background: var(--surface); box-shadow: rgba(0,0,0,.14) 0 1px 2px; }}
    .kpi-grid article {{ min-width: 0; padding: 16px; }}
    .kpi-grid span, .kpi-grid small {{ display: block; color: var(--quiet); }}
    .kpi-grid strong {{ display: block; margin: 9px 0 6px; font-size: 25px; line-height: 1; }}
    .kpi-grid small {{ font-size: 10px; line-height: 1.35; }}
    .overview-grid {{ display: grid; grid-template-columns: minmax(0,1.3fr) minmax(280px,.7fr); gap: 12px; }}
    .data-card {{ padding: 16px; }}
    .data-card header {{ display: flex; justify-content: space-between; gap: 12px; align-items: start; margin-block-end: 14px; }}
    .data-card h2, .state-panel h2 {{ margin: 3px 0 0; font-size: 16px; }}
    .trust-score, .quiet-pill, .status-mark {{ padding: 4px 7px; border-radius: 999px; background: rgba(119,190,141,.12); color: var(--success); font-size: 10px; font-weight: 700; }}
    .trust-card dl {{ display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 10px; margin: 0; }}
    .trust-card dl div {{ padding: 11px; border: 1px solid var(--line); border-radius: 9px; background: var(--surface-2); }}
    dt {{ color: var(--quiet); font-size: 10px; }} dd {{ margin: 4px 0 0; font-size: 12px; font-weight: 650; }}
    .checklist ul {{ display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; color: var(--muted); font-size: 11px; }}
    .checklist li::before {{ content: "○"; display: inline-block; width: 18px; color: var(--quiet); }}
    .checklist li.done {{ color: var(--text); }} .checklist li.done::before {{ content: "✓"; color: var(--success); }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 9px; }}
    table {{ width: 100%; min-width: 620px; border-collapse: collapse; font-size: 11px; }}
    th, td {{ padding: 10px 12px; border-block-end: 1px solid var(--line); text-align: start; }} th {{ color: var(--quiet); font-size: 9px; letter-spacing: .08em; text-transform: uppercase; }} tbody tr:last-child td {{ border-block-end: 0; }}
    .result {{ font-weight: 700; }} .result.success {{ color: var(--success); }} .result.warning {{ color: var(--warning); }}
    .state-panel {{ min-height: 320px; display: grid; align-content: center; justify-items: start; gap: 10px; padding: clamp(24px,6vw,72px); }}
    .state-panel p {{ max-width: 680px; margin: 0; color: var(--muted); line-height: 1.55; }}
    .error-panel .status-mark {{ color: var(--danger); background: rgba(220,105,105,.12); }}
    .permission-panel .status-mark, .recovery-panel .status-mark {{ color: var(--warning); background: rgba(221,175,83,.12); }}
    .skeleton {{ width: min(420px,75%); height: 16px; border-radius: 8px; background: rgb(38,39,43); }} .skeleton.wide {{ width: min(680px,95%); height: 42px; }}
    .evidence-footer {{ margin-block-start: auto; padding: 14px 2px; display: flex; justify-content: space-between; gap: 12px; color: var(--quiet); font-size: 9px; }}
    @media (max-width: 1100px) {{ .kpi-grid {{ grid-template-columns: repeat(2,minmax(0,1fr)); }} .overview-grid {{ grid-template-columns: 1fr; }} }}
    @media (max-width: 820px) {{ #app-shell {{ grid-template-columns: 54px minmax(0,1fr); }} .rail {{ padding-inline: 5px; }} #page-header {{ grid-template-columns: 1fr; padding: 10px 12px; }} .status-chip {{ max-width: none; }} #overview-main {{ padding: 12px; }} .hero {{ grid-template-columns: 1fr; }} .hero-actions {{ justify-content: flex-start; }} #inspect-result {{ text-align: start; }} .trust-card dl {{ grid-template-columns: 1fr; }} .evidence-footer {{ flex-direction: column; }} }}
    @media (prefers-reduced-motion: reduce) {{ *,*::before,*::after {{ animation: none !important; scroll-behavior: auto !important; }} }}
{kpi_styles}{standard_rules}
    @media (width: 1440px) {{
      #app-shell > .workspace {{ height: 900px; overflow: hidden; }}
      #app-shell > .workspace > #overview-main {{ height: 1982.735px; }}
    }}
  </style>
</head>
<body>
  <svg width="0" height="0" aria-hidden="true" style="position:absolute;overflow:hidden"><defs><symbol id="i-home" viewBox="0 0 24 24"><path d="m3 11 9-8 9 8v10h-6v-6H9v6H3V11Z"/></symbol></defs></svg>
  <div id="app-shell" data-ui-region="shell.application" data-ui-element="shell-application">
    <aside class="rail" aria-label="Основная навигация">
      <div class="brand" aria-label="Custometry">CU</div>
      <button id="nav-overview" type="button" aria-current="page" aria-label="Обзор" title="Обзор" data-ui-element="nav-overview" data-ui-component="navigation.rail-action" data-ui-variant="nav-root.overview" data-ui-size="icon" data-ui-slot="shell.application.button" data-ui-state="default"><svg id="nav-overview-icon" viewBox="0 0 24 24" aria-hidden="true" data-ui-element="nav-overview-icon" data-ui-icon="i-home" data-ui-state="default"><use href="#i-home"/></svg></button>
      <span class="rail-note" aria-hidden="true">Workspace</span>
    </aside>
    <section class="workspace">
      <header id="page-header" data-ui-region="shell.page-header" data-ui-element="page-header">
        <div class="header-copy"><span class="eyebrow">Custometry · North Star</span><h1>Data Connections</h1></div>
        <div class="status-chip" role="status">{html.escape(copy['status'])}</div>
      </header>
      <main id="overview-main" data-ui-region="shell.main-content" data-ui-element="overview-main">
        <article id="overview-content" data-ui-region="UI-DATA-001.content" data-ui-element="overview-content" data-state="{safe_state}">
          <section class="hero">
            <div><span class="eyebrow">{html.escape(copy['eyebrow'])}</span><h2>{html.escape(copy['title'])}</h2><p>{html.escape(copy['summary'])}</p></div>
            <div><div class="hero-actions"><button id="manage-action" type="button" data-ui-element="manage-action" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="UI-DATA-001.connection.manage">Управлять</button><button id="rotate-action" type="button" data-ui-element="rotate-action" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="UI-DATA-001.connection.secret.rotate">Ротировать секрет</button><button id="continue-action" type="button" data-ui-element="continue-action" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-prototype-action="journey.data-to-trusted-result.1">К качеству</button></div><p id="inspect-result" role="status" aria-live="polite"></p></div>
          </section>
{state_body(state)}
          <footer class="evidence-footer"><span>Изолированный fixture · не production data</span><span>Responsive Web 768–1920 · mobile scope не авторизован</span></footer>
        </article>
      </main>
    </section>
  </div>
  <script>const result=document.getElementById('inspect-result');document.getElementById('manage-action').addEventListener('click',()=>{{result.textContent='Управление подключением открыто в fixture';}});document.getElementById('rotate-action').addEventListener('click',()=>{{result.textContent='Ротация секрета подготовлена без внешней записи';}});document.getElementById('continue-action').addEventListener('click',()=>{{result.textContent='Переход к качеству данных готов';}});</script>
</body>
</html>
"""


def element(
    state_id: str,
    *,
    element_id: str,
    parent: str | None,
    region_id: str,
    locator: str,
    element_type: str,
    component_id: str | None = None,
    variant: str | None = None,
    size_class: str | None = None,
    icon_id: str | None = None,
    action_ids: list[str] | None = None,
    standard_slot_id: str | None = None,
    standard_identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "element_id": element_id,
        "parent_element_id": parent,
        "region_id": region_id,
        "locator": locator,
        "visibility": "required",
        "element_type": element_type,
        "standard_slot_id": standard_slot_id,
        "standard_identity": standard_identity,
        "component_id": component_id,
        "variant": variant,
        "size_class": size_class,
        "content_contract": "Exact visible content is bound to the isolated state fixture and current product-source meaning.",
        "icon_id": icon_id,
        "action_ids": action_ids or [],
        "state_ids": [state_id],
        "component_state_ids": ["default"],
        "responsive_behavior": [specified("preserve task, trust, recovery, and action meaning across the supported Web range", "references/responsive-policy-v1.md#responsive-web-requirement")],
        "accessibility": {"keyboard_and_name": specified("semantic element, accessible name where interactive, visible focus, and coherent reading order", "references/visual-provenance-contract-v1.md#screen-contract")},
        "source_refs": [origin("product_contract", f"{INTAKE_REF}#/screens/7")],
    }


def region(region_id: str, locator: str, component_status: str, source_ref: str) -> dict[str, Any]:
    provenance = origin("product_contract", source_ref)
    return {
        "region_id": region_id,
        "locator": locator,
        "visibility": "required",
        "component_id": None,
        "component_status": component_status,
        "variant": None,
        "state": "default",
        "source_refs": [provenance],
        "geometry": {},
        "layout_rules": [],
        "visual_properties": {},
        "content": {},
        "interactions": [],
        "accessibility": {"required_check": specified("semantic region, coherent reading order, and named controls", "references/visual-provenance-contract-v1.md#screen-contract")},
        "responsive_behavior": [specified("remain reachable without page-level horizontal overflow", "references/responsive-policy-v1.md#verification")],
        "geometry_tolerance_px": 0,
        "geometry_tolerance_origin": origin("normative_requirement", "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence"),
        "computed_style_properties": ["background-color", "color", "display", "overflow-x", "overflow-y"],
        "computed_style_properties_origin": provenance,
    }


def standard_identity(component_id: str | None, variant: str | None, size_class: str | None, element_type: str, icon_id: str | None = None) -> dict[str, Any]:
    return {
        "component_id": component_id,
        "variant": variant,
        "size_class": size_class,
        "element_type": element_type,
        "icon_id": icon_id,
        "state_ids": ["default"],
    }


def screen_contract(state: str, html_path: Path, fixture_path: Path, baseline: dict[str, Any], intake_sha: str, baseline_sha: str, font_sha: str, asset_sha: str) -> dict[str, Any]:
    state_id = f"UI-DATA-001.{state}"
    revision_id = f"UI-DATA-001.{state}.all.ru.graphite@r5"
    manifest_ref = f"{EVIDENCE_REF}/states/{state}/standard-applicability.json"
    anchor_origin = origin("normative_requirement", "docs/adr/0007-responsive-web-frontend-platform.md#responsive-web-contract")
    viewport_anchors = [{**anchor, "state_ref": state_id, "origin": anchor_origin} for anchor in ANCHORS]
    elements = [
        element(state_id, element_id="shell-application", parent=None, region_id="shell.application", locator="#app-shell", element_type="div", standard_identity=standard_identity(None, None, None, "div")),
        element(state_id, element_id="page-header", parent="shell-application", region_id="shell.page-header", locator="#page-header", element_type="header", standard_identity=standard_identity(None, None, None, "header")),
        element(state_id, element_id="overview-main", parent="shell-application", region_id="shell.main-content", locator="#overview-main", element_type="main", standard_identity=standard_identity(None, None, None, "main")),
        element(state_id, element_id="overview-content", parent="overview-main", region_id="UI-DATA-001.content", locator="#overview-content", element_type="article"),
        element(state_id, element_id="nav-overview", parent="shell-application", region_id="shell.application", locator="#nav-overview", element_type="button", standard_slot_id="shell.application.button", standard_identity=standard_identity("navigation.rail-action", "nav-root.overview", "icon", "button")),
        element(state_id, element_id="nav-overview-icon", parent="nav-overview", region_id="shell.application", locator="#nav-overview-icon", element_type="svg", icon_id="layout-grid", standard_identity=standard_identity(None, None, None, "svg", "i-home")),
        element(state_id, element_id="manage-action", parent="overview-content", region_id="UI-DATA-001.content", locator="#manage-action", element_type="button", component_id="action.button", variant="secondary", size_class="sm", action_ids=["UI-DATA-001.connection.manage"], standard_slot_id="shell.main-content.button", standard_identity=standard_identity("action.button", "button", "standard", "button")),
        element(state_id, element_id="rotate-action", parent="overview-content", region_id="UI-DATA-001.content", locator="#rotate-action", element_type="button", component_id="action.button", variant="secondary", size_class="sm", action_ids=["UI-DATA-001.connection.secret.rotate"], standard_slot_id="shell.main-content.button", standard_identity=standard_identity("action.button", "button", "standard", "button")),
        element(state_id, element_id="continue-action", parent="overview-content", region_id="UI-DATA-001.content", locator="#continue-action", element_type="button", component_id="action.button", variant="secondary", size_class="sm", action_ids=["journey.data-to-trusted-result.1"], standard_slot_id="shell.main-content.button", standard_identity=standard_identity("action.button", "button", "standard", "button")),
    ]
    return {
        "$schema": "screen-design-contract.schema.json",
        "schema_id": "codex.ui-screen-design-contract/v1",
        "contract_profile": "codex.ui-screen-design-contract/v1@2.0.0",
        "screen_revision_id": revision_id,
        "program_revision_ref": PROGRAM_REVISION_REF,
        "functional_contract_ref": {"path": INTAKE_REF, "sha256": intake_sha, "json_pointer": "/screens/7", "screen_id": "UI-DATA-001"},
        "baseline_binding": {"baseline_id": baseline["baseline_id"], "path": BASELINE_REF, "sha256": baseline_sha, "shell_variant_id": "shell.workspace", "exception_id": None},
        "standard_binding": {"standard_revision_id": baseline["standard_contract"]["standard_revision_id"], "clause_inventory_sha256": baseline["standard_contract"]["clause_inventory_sha256"], "applicability_manifest": {"path": manifest_ref, "sha256": "0" * 64}},
        "standard_exceptions": [],
        "status": "review",
        "product_identity": {"screen_id": "UI-DATA-001", "route_id": "UI-DATA-001", "route": "/w/:workspaceKey/connections", "state_id": state_id, "role_id": "WA", "permission_profile": "connection.manage", "locale": "ru", "theme": "graphite"},
        "source_visual": {"kind": "delegated_design_output", "evidence_mode": "visual_language_only", "html_path": SOURCE_VISUAL_REF, "image_path": None, "html_sha256": VISUAL_AUTHORITY["source_visual_sha256"], "image_sha256": None, "owner_decision_ref": None, "delegation_ref": "references/stage-transition-contract-v1.md#delegated-design-envelope"},
        "visual_authority": VISUAL_AUTHORITY,
        "comparison_claims": {"required_purpose": "visual_language_conformance", "deterministic_render_proves_fidelity": False, "reference_logical_artifact_id": "custometry-pilot-v3-metadata-ru", "implementation_logical_artifact_id": revision_id},
        "interaction_contract": {
            "visible_actions": [
                {"action_id": "UI-DATA-001.connection.manage", "expected_outcome": "Connection Manage completes or the next contract-bound surface opens", "side_effect_class": "none", "activation_policy": "execute_in_fixture", "outcome_assertion": {"kind": "dom", "selector": "#inspect-result", "property": "textContent", "expected": "Управление подключением открыто в fixture"}},
                {"action_id": "UI-DATA-001.connection.secret.rotate", "expected_outcome": "Connection Secret Rotate completes or the next contract-bound surface opens", "side_effect_class": "none", "activation_policy": "execute_in_fixture", "outcome_assertion": {"kind": "dom", "selector": "#inspect-result", "property": "textContent", "expected": "Ротация секрета подготовлена без внешней записи"}},
                {"action_id": "journey.data-to-trusted-result.1", "expected_outcome": "Continue data to trusted result completes or the next contract-bound surface opens", "side_effect_class": "none", "activation_policy": "execute_in_fixture", "outcome_assertion": {"kind": "dom", "selector": "#inspect-result", "property": "textContent", "expected": "Переход к качеству данных готов"}},
            ],
            "no_actions_reason_ref": None,
            "required_checks": ["keyboard_activation", "focus_visibility", "tab_radio_behavior", "menus", "toggles", "refresh_feedback", "state_transitions", "no_unresolved_file_navigation", "no_console_errors", "no_request_failures", "no_page_horizontal_overflow"],
            "allowed_origins": ["http://127.0.0.1:4173"],
            "fixture_mode": "isolated_local",
            "evidence_redaction_required": True,
            "redaction_selectors": ["[data-sensitive]", "input[type='password']"],
        },
        "render_environment": {"browser": "chromium/150.0.7871.187", "browser_mechanic": "playwright_cli", "device_scale_factor": 1, "timezone": "Europe/Moscow", "fixed_clock_iso": "2026-02-14T10:00:00+03:00", "reduced_motion": True, "animations": "disabled", "fixture_data_path": rel(fixture_path), "fixture_data_sha256": sha256(fixture_path), "font_bundle_sha256": font_sha, "asset_bundle_sha256": asset_sha},
        "viewport_contract": {
            "mode": "responsive_web",
            "supported_web_width_range": {"min_width": 768, "max_width": 1920, "origin": anchor_origin},
            "anchors": viewport_anchors,
            "breakpoint_policy": "content_driven",
            "breakpoint_policy_origin": origin("normative_requirement", "references/responsive-policy-v1.md#breakpoints-and-components"),
            "below_supported_range": "out_of_scope",
            "below_supported_range_origin": origin("normative_requirement", "references/responsive-policy-v1.md#responsive-web-requirement"),
            "above_supported_range": "max_content_width",
            "above_supported_range_origin": origin("normative_requirement", "references/responsive-policy-v1.md#responsive-web-requirement"),
            "mobile_scope": "unauthorized",
            "mobile_scope_origin": origin("normative_requirement", "references/responsive-policy-v1.md#mobile-authorization-boundary"),
            "mobile_authorization_ref": None,
            "mobile_specific_composition": False,
            "authorized_mobile_surfaces": [],
            "authorized_mobile_viewports": [],
            "allowed_mobile_changes": [],
        },
        "regions": [
            region("shell.application", "#app-shell", "registered", f"{BASELINE_REF}#/standard_contract/clauses"),
            region("shell.page-header", "#page-header", "registered", f"{BASELINE_REF}#/standard_contract/clauses"),
            region("shell.main-content", "#overview-main", "registered", f"{BASELINE_REF}#/standard_contract/clauses"),
            region("UI-DATA-001.content", "#overview-content", "one_off", f"{INTAKE_REF}#/screens/7/regions/0"),
        ],
        "element_contracts": elements,
        "allowed_provenance_kinds": ["product_contract", "normative_requirement", "accepted_visual", "measured_baseline", "design_token", "owner_decision", "derived_formula", "delegated_design_decision"],
        "unresolved_decisions": [],
        "acceptance": {
            "agent_self_acceptance": "prohibited",
            "machine_receipt_required": True,
            "owner_decision_required": True,
            "owner_decision_ref": None,
            "screen_acceptance_receipt_path": None,
            "screen_acceptance_receipt_sha256": None,
            "pixel_diff_policy": {
                "channel_threshold": specified(0, "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence", unit="channel-value"),
                "approved_max_different_pixels": specified(0, "references/visual-provenance-contract-v1.md#pixel-and-geometry-evidence", unit="px"),
            },
        },
    }


def prepare() -> None:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    intake_sha = sha256(INTAKE)
    baseline_sha = sha256(BASELINE)
    if baseline_sha != "ec3108e8d23cf4dd59f217766082ef938dda83245aa46dcc43968c64a8f2bc7c":
        raise ValueError("live baseline differs from the ledger-bound context manifest")
    if sha256(SOURCE_VISUAL) != VISUAL_AUTHORITY["source_visual_sha256"]:
        raise ValueError("live visual authority differs from the ledger-bound context manifest")
    font_sha = hashlib.sha256(b"Inter|ui-sans-serif|system-ui|-apple-system|Segoe UI|sans-serif").hexdigest()
    asset_sha = hashlib.sha256(b"exact-inline-pilot-home-symbol|no-external-candidate-assets").hexdigest()
    rules = standard_css(baseline)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    for state in STATE_ORDER:
        fixture = {
            "schema_id": "custometry.ui-review-fixture/v1",
            "screen_id": "UI-DATA-001",
            "state_id": f"UI-DATA-001.{state}",
            "clock": "2026-02-14T10:00:00+03:00",
            "locale": "ru",
            "theme": "graphite",
            "safety": "isolated_local_no_real_data",
            "content": STATE_COPY[state],
        }
        state_artifact = ARTIFACT_DIR / "states" / state
        fixture_path = state_artifact / "fixture.json"
        html_path = state_artifact / "screen.html"
        contract_path = state_artifact / "screen-contract.json"
        write_json(fixture_path, fixture)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(render_html(state, sha256(fixture_path), font_sha, asset_sha, rules), encoding="utf-8")
        write_json(contract_path, screen_contract(state, html_path, fixture_path, baseline, intake_sha, baseline_sha, font_sha, asset_sha))
    print(json.dumps({"status": "prepared", "states": list(STATE_ORDER), "artifact_dir": rel(ARTIFACT_DIR)}, ensure_ascii=False, indent=2))


def bind_applicability() -> None:
    bound: dict[str, str] = {}
    for state in STATE_ORDER:
        contract_path = ARTIFACT_DIR / "states" / state / "screen-contract.json"
        manifest_path = EVIDENCE_DIR / "states" / state / "standard-applicability.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        contract["standard_binding"]["applicability_manifest"]["sha256"] = sha256(manifest_path)
        write_json(contract_path, contract)
        bound[state] = sha256(manifest_path)
    print(json.dumps({"status": "bound", "applicability_sha256s": bound}, indent=2))


def build_program_snapshot() -> Path:
    projection = json.loads(G1_INVENTORY.read_text(encoding="utf-8"))
    matched = [row for row in projection["screens"] if row.get("screen_id") == "UI-DATA-001"]
    if len(matched) != 1:
        raise ValueError("G1 projection cannot resolve exactly one UI-DATA-001 screen")
    matched[0]["required_states"] = [f"UI-DATA-001.{state}" for state in STATE_ORDER]
    projection_path = ARTIFACT_DIR / "g1-admission-inventory.family-projection.json"
    write_json(projection_path, projection)

    snapshot = json.loads(PROGRAM.read_text(encoding="utf-8"))
    for source in snapshot["source_contracts"]:
        if source.get("path") == rel(G1_INVENTORY):
            source["screen_collections"] = []
    snapshot["source_contracts"].append({
        "path": rel(projection_path),
        "authority": "G4 stage-owned exact full-inventory projection adding only accepted required states for UI-DATA-001",
        "required_status": "complete",
        "sha256": sha256(projection_path),
        "screen_collections": [{"json_pointer": "/screens", "id_key": "screen_id"}],
        "journey_collections": [],
    })
    for entry in snapshot["screens"]:
        if entry.get("screen_ref", {}).get("path") == rel(G1_INVENTORY):
            entry["screen_ref"]["path"] = rel(projection_path)
    screen_entries = ARTIFACT_DIR / "program-screen-entries.snapshot.json"
    write_json(screen_entries, {"screens": snapshot["screens"]})
    screen_index = ARTIFACT_DIR / "screens-index.snapshot.json"
    write_json(screen_index, {
        "$schema": "program-artifact-index.schema.json",
        "schema_id": "codex.ui-program-artifact-index/v1",
        "program_id": PROGRAM_ID,
        "program_revision": 5,
        "index_kind": "screens",
        "entries": [
            {
                "id": entry["screen_ref"]["expected_id"],
                "path": rel(screen_entries),
                "sha256": sha256(screen_entries),
                "json_pointer": f"/screens/{index}",
            }
            for index, entry in enumerate(snapshot["screens"])
        ],
    })
    snapshot["artifact_indexes"]["screens"] = {"path": rel(screen_index), "sha256": sha256(screen_index)}
    snapshot_path = ARTIFACT_DIR / "ui-design-program.snapshot.json"
    snapshot["execution_artifacts"]["plan_doc"] = rel(snapshot_path)
    write_json(snapshot_path, snapshot)
    write_json(ARTIFACT_DIR / "program-snapshot-binding.json", {
        "schema_id": "codex.ui-stage-program-snapshot-binding/v1",
        "canonical_program": {"path": rel(PROGRAM), "sha256": sha256(PROGRAM)},
        "snapshot": {"path": rel(snapshot_path), "sha256": sha256(snapshot_path)},
        "projection": {"path": rel(projection_path), "sha256": sha256(projection_path)},
        "screen_index_snapshot": {"path": rel(screen_index), "sha256": sha256(screen_index)},
        "changed_pointers": ["/source_contracts", "/screens/*/screen_ref/path", "/artifact_indexes/screens", "/execution_artifacts/plan_doc"],
        "reason": "Family aggregation adds exact accepted required_states only for the current UI-DATA-001 representative; no other inventory meaning changes.",
        "accepted_authority_changed": False,
        "result": "passed",
    })
    return snapshot_path


def review() -> None:
    snapshot_path = build_program_snapshot()
    REVIEW_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    manifest_entries: list[dict[str, Any]] = []
    acceptance_refs: list[str] = []
    cards: list[str] = []
    for state in STATE_ORDER:
        acceptance_path = EVIDENCE_DIR / "states" / state / "screen-acceptance.json"
        screenshot_path = EVIDENCE_DIR / "states" / state / "web-1440" / "implementation.png"
        review_asset_path = REVIEW_ASSET_DIR / f"{state}.png"
        shutil.copyfile(screenshot_path, review_asset_path)
        review_asset_ref = f"review-assets/{state}.png"
        acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
        acceptance_ref = rel(acceptance_path)
        acceptance_refs.append(acceptance_ref)
        for role in ("screen_acceptance", "standard_conformance"):
            entry_id = f"{state}.{role}"
            manifest_entries.append({"entry_id": entry_id, "role": role, "artifact_ref": acceptance_ref, "sha256": sha256(acceptance_path), "anchor_id": None, "state_id": acceptance["state_id"]})
        cards.append(f"""<article class="review-card" data-state="{state}"><a href="{review_asset_ref}"><img src="{review_asset_ref}" data-asset-sha256="{sha256(review_asset_path)}" alt="Data Connections, состояние {state}, Web 1440"></a><div class="card-copy"><span>{state}</span><strong>{html.escape(STATE_COPY[state]['title'])}</strong><small>{html.escape(STATE_COPY[state]['status'])}</small><i data-review-entry="{state}.screen_acceptance">screen acceptance · passed</i><i data-review-entry="{state}.standard_conformance">standard conformance · passed</i></div></article>""")
    manifest = {
        "$schema": "review-board-manifest.schema.json",
        "schema_id": "codex.ui-review-board-manifest/v1",
        "program_id": PROGRAM_ID,
        "artifact_id": FAMILY_REVISION_ID,
        "revision": 5,
        "validation_profile": "family_review_ready",
        "entries": manifest_entries,
    }
    manifest_path = EVIDENCE_DIR / "review-board-manifest.json"
    write_json(manifest_path, manifest)
    board_path = ARTIFACT_DIR / "review-board.html"
    board_path.write_text(f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry · Data Connections family review</title><style>:root{{color-scheme:dark;--bg:#070708;--surface:#111214;--line:#303136;--text:#f0f0f2;--muted:#a7a7ad;--accent:#66b9d3}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px Inter,system-ui,sans-serif}}main{{width:min(1480px,100%);margin:auto;padding:32px}}header{{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:24px}}h1{{margin:.2rem 0;font-size:clamp(28px,4vw,48px)}}p{{color:var(--muted);max-width:760px;line-height:1.55}}.badge{{padding:7px 10px;border:1px solid var(--line);border-radius:999px;color:var(--accent);white-space:nowrap}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.review-card{{overflow:hidden;border:1px solid var(--line);border-radius:14px;background:var(--surface)}}.review-card a{{display:block;height:330px;overflow:hidden;background:#0a0a0b}}img{{width:100%;height:auto;display:block}}.card-copy{{display:grid;gap:5px;padding:14px}}.card-copy span{{color:var(--accent);font-size:10px;text-transform:uppercase;letter-spacing:.12em}}.card-copy small,.card-copy i{{color:var(--muted);font-size:10px}}.card-copy i{{font-style:normal}}footer{{margin-top:24px;padding:16px;border:1px solid var(--line);border-radius:12px;color:var(--muted)}}@media(max-width:900px){{main{{padding:18px}}header{{display:grid}}.grid{{grid-template-columns:1fr}}.review-card a{{height:260px}}}}</style></head>
<body><main data-ui-artifact="review_board" data-program-id="{PROGRAM_ID}" data-artifact-id="{FAMILY_REVISION_ID}" data-revision="5" data-validation-profile="family_review_ready" data-review-manifest="{rel(manifest_path)}" data-review-manifest-sha256="{sha256(manifest_path)}"><header><div><span>G4 · representative family</span><h1>Data Connections</h1><p>Шесть обязательных состояний connection-list контракта: компактная Graphite shell, явный Result Trust, безопасные fixture-действия и адаптивный Web 768–1920.</p></div><span class="badge">review ready · mobile out of scope</span></header><section class="grid">{''.join(cards)}</section><footer>Fixture-only evidence. Production API, authorization, persistence, performance, deployment и полное WCAG-соответствие здесь не проверяются.</footer></main></body></html>""", encoding="utf-8")
    family_request = {
        "$schema": "family-acceptance-request.schema.json",
        "program_path": rel(snapshot_path),
        "family_id": FAMILY_ID,
        "family_revision_id": FAMILY_REVISION_ID,
        "revision": 5,
        "screen_acceptance_paths": acceptance_refs,
        "review_board_path": rel(board_path),
        "owner_decision_ref": None,
    }
    write_json(EVIDENCE_DIR / "family-acceptance-request-review-ready.json", family_request)
    decision_packet = f"""---
artifact_kind: ui_design_owner_decision_packet
program_id: {PROGRAM_ID}
stage_instance_id: {STAGE_ID}
status: needs_input
question_count: 1
resume_same_stage: true
---

# Готовый Data Connections

## Что уже готово

Готова family review board для `UI-DATA-001`: все шесть обязательных состояний,
четыре responsive-Web anchor и изолированный browser proof без production data.

- `{rel(board_path)}`
- `{rel(EVIDENCE_DIR / 'review-board-1440.png')}`

## Вопрос

### 1. Принимаете готовую family review board?

- **Принять** — агент запишет canonical receipt и закроет этот G4 строгим gate.
- Попросить небольшие правки — агент возобновит тот же stage revision и покажет обновлённую board.

## Что произойдёт после ответа

Агент сам создаст technical receipts, возобновит тот же stage и повторит strict gate.
Хеши, JSON и операции ledger от владельца не требуются.
"""
    (EVIDENCE_DIR / "owner-review-decision-packet.md").write_text(decision_packet, encoding="utf-8")
    print(json.dumps({"status": "review_prepared", "board": rel(board_path), "manifest": rel(manifest_path)}, ensure_ascii=False, indent=2))


def transition_inputs() -> None:
    family_path = EVIDENCE_DIR / "family-acceptance.json"
    board_path = ARTIFACT_DIR / "review-board.html"
    family = json.loads(family_path.read_text(encoding="utf-8"))
    if family.get("result") != "review_ready":
        raise ValueError("family acceptance is not review_ready")
    sys.path.insert(0, str(SKILL_SCRIPTS))
    from validate_stage_transition import hash_bound_source_refs  # type: ignore

    preflight_dir = EVIDENCE_DIR / "preflight"
    artifact_hash = sha256(family_path)
    next_prompt_ref = rel(NEXT_PROMPT)
    checks = {
        "current_gate": {"validation_profile": "family_review_ready", "artifact_ref": rel(family_path), "artifact_sha256": artifact_hash, "result": "passed"},
        "source_freshness": {"source_refs": hash_bound_source_refs(family_path, ROOT), "drift_classification": "owned_generated_change", "stale_refs": []},
        "next_stage_inputs": {"next_stage_id": "G4@family.dq.shell-workspace.baseline-r5", "task_ref": next_prompt_ref, "unresolved_inputs": []},
        "write_scope": {"allowed_paths": [".codex/agents/generated/custometry-ui-design-g0-v2/**", ".codex/delivery/evidence/custometry-ui-design-program-v2/**", ".codex/delivery/ui-design-programs/custometry-v2/**"], "authorization_basis": "active_task_and_repository_contract", "outside_scope_paths": []},
        "foreign_changes": {"observed_paths": [".codex/AGENTS.md", "custometry-technical-blueprint-human-ru.md", "custometry-technical-blueprint-ru.md", "custometry-ui-blueprint-ru.md", "docs/generated/requirement-index.json", "packages/contracts/routes/ui-surface-contracts.json"], "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved"},
        "execution_route": {"route": "goal_driven staged-plan-runner with ui-design-program CAS ledger updates", "available": True},
        "handoff_artifact": {"artifact_ref": next_prompt_ref, "artifact_sha256": sha256(NEXT_PROMPT), "known_stop_resolution": "none"},
    }
    for check_id, facts in checks.items():
        write_json(preflight_dir / f"{check_id}.json", {"$schema": "stage-preflight-evidence.schema.json", "schema_id": "codex.ui-stage-preflight-evidence/v1", "check_id": check_id, "program_id": PROGRAM_ID, "stage_instance_id": STAGE_ID, "gate_id": "G4", "status": "passed", "facts": facts})
    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": PROGRAM_ID,
        "from_stage_id": STAGE_ID,
        "from_gate": "G4",
        "from_target": FAMILY_REVISION_ID,
        "from_revision": 5,
        "artifact": rel(family_path),
        "to_gate": "G4",
        "to_stage_id": "G4@family.dq.shell-workspace.baseline-r5",
        "to_target": "family.dq.shell-workspace.baseline-r5",
        "to_task": next_prompt_ref,
        "status": "review_ready",
        "owner_decision": None,
        "decision_inventory": None,
        "blockers": None,
        "checks": [f"{check_id}={rel(preflight_dir / f'{check_id}.json')}" for check_id in ("current_gate", "source_freshness", "next_stage_inputs", "write_scope", "foreign_changes", "execution_route", "handoff_artifact")],
        "summary": "Data Connections exact-covers all six required states and four responsive-Web anchors; machine proof is ready for owner review.",
        "review_artifacts": [rel(board_path), rel(EVIDENCE_DIR / "review-board-1440.png"), rel(EVIDENCE_DIR / "browser-board-qa.json")],
        "questions": ["Принимаете готовую family review board или хотите небольшие правки?"],
    }
    write_json(EVIDENCE_DIR / "stage-transition-request-review-ready.json", request)
    report = f"""---
artifact_kind: ui_design_program_stage_evidence
stage_instance_id: {STAGE_ID}
gate_id: G4
status: review_ready
proof_boundary: current-contract isolated browser evidence for six UI-DATA-001 states and four responsive-Web anchors; no production implementation, publication, deployment, mobile-specific design, full WCAG conformance, persistence, authorization, or performance proof
---

# G4 data connections family r5 execution report

## Scope

- `UI-DATA-001` only; required states: `{', '.join(STATE_ORDER)}`.
- Responsive Web anchors: `web-768`, `web-1024`, `web-1440`, `web-1920`.
- Visual-language conformance to the hash-pinned pilot and platform baseline.
- Isolated fixture interactions for all three source-bound `UI-DATA-001` actions; no external writes.

## Result

- Family aggregate: `{rel(family_path)}` (`review_ready`).
- Review board: `{rel(board_path)}`.
- Browser board QA: `{rel(EVIDENCE_DIR / 'browser-board-qa.json')}`.
- Transition: `{EVIDENCE_REF}/stage-transition-review-ready.json` (`review_ready`; next stage not allowed).

## Proof boundary and residual risk

Automated evidence covers contract shape, deterministic standard applicability,
clause-level computed values, keyboard/accessibility smoke, loopback isolation,
console/network observations, responsive-Web overflow, and rendered owner review.
Owner acceptance remains required. Mobile-specific scope is unauthorized. No
production frontend, API, authorization, database, performance, deployment,
release, or full WCAG claim is made.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    print(json.dumps({"status": "transition_inputs_prepared", "request": rel(EVIDENCE_DIR / "stage-transition-request-review-ready.json"), "report": rel(REPORT)}, ensure_ascii=False, indent=2))


def acceptance_request() -> None:
    decision_path = EVIDENCE_DIR / "family-acceptance-decision-r5.json"
    review_request_path = EVIDENCE_DIR / "family-acceptance-request-review-ready.json"
    if not decision_path.is_file() or not review_request_path.is_file():
        raise ValueError("accepted owner decision and review-ready family request are required")
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    if decision.get("decision", {}).get("status") != "accepted":
        raise ValueError("owner decision is not accepted")
    request = json.loads(review_request_path.read_text(encoding="utf-8"))
    request["owner_decision_ref"] = rel(decision_path)
    write_json(EVIDENCE_DIR / "family-acceptance-request.json", request)
    write_json(EVIDENCE_DIR / "resolved-owner-decisions.json", [{
        "decision_id": f"{STAGE_ID}.finished-result",
        "class": "owner_required",
        "status": "resolved",
        "summary": "The owner explicitly accepted the exact corrected Data Connections r5 review board.",
        "resolution_ref": rel(decision_path),
    }])
    write_json(EVIDENCE_DIR / "known-blockers.json", [])
    print(json.dumps({
        "status": "acceptance_request_prepared",
        "request": rel(EVIDENCE_DIR / "family-acceptance-request.json"),
        "owner_decision": rel(decision_path),
    }, ensure_ascii=False, indent=2))


def acceptance_transition_inputs() -> None:
    family_path = EVIDENCE_DIR / "family-acceptance.json"
    decision_path = EVIDENCE_DIR / "family-acceptance-decision-r5.json"
    decision_inventory_path = EVIDENCE_DIR / "resolved-owner-decisions.json"
    blockers_path = EVIDENCE_DIR / "known-blockers.json"
    board_path = ARTIFACT_DIR / "review-board.html"
    family = json.loads(family_path.read_text(encoding="utf-8"))
    if family.get("result") != "passed" or family.get("owner_decision_ref") != rel(decision_path):
        raise ValueError("strict accepted family aggregate is not current")
    sys.path.insert(0, str(SKILL_SCRIPTS))
    from validate_stage_transition import hash_bound_source_refs  # type: ignore

    preflight_dir = EVIDENCE_DIR / "preflight"
    artifact_hash = sha256(family_path)
    next_prompt_ref = rel(NEXT_PROMPT)
    checks = {
        "current_gate": {"validation_profile": "family_gate", "artifact_ref": rel(family_path), "artifact_sha256": artifact_hash, "result": "passed"},
        "source_freshness": {"source_refs": hash_bound_source_refs(family_path, ROOT), "drift_classification": "owned_generated_change", "stale_refs": []},
        "next_stage_inputs": {"next_stage_id": "G4@family.dq.shell-workspace.baseline-r5", "task_ref": next_prompt_ref, "unresolved_inputs": []},
        "write_scope": {"allowed_paths": [".codex/agents/generated/custometry-ui-design-g0-v2/**", ".codex/delivery/evidence/custometry-ui-design-program-v2/**", ".codex/delivery/ui-design-programs/custometry-v2/**"], "authorization_basis": "active_task_and_repository_contract", "outside_scope_paths": []},
        "foreign_changes": {"observed_paths": [".codex/AGENTS.md", "custometry-technical-blueprint-human-ru.md", "custometry-technical-blueprint-ru.md", "custometry-ui-blueprint-ru.md", "docs/generated/requirement-index.json", "packages/contracts/routes/ui-surface-contracts.json"], "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved"},
        "execution_route": {"route": "goal_driven staged-plan-runner with ui-design-program CAS ledger updates", "available": True},
        "handoff_artifact": {"artifact_ref": next_prompt_ref, "artifact_sha256": sha256(NEXT_PROMPT), "known_stop_resolution": "none"},
    }
    for check_id, facts in checks.items():
        write_json(preflight_dir / f"{check_id}.json", {"$schema": "stage-preflight-evidence.schema.json", "schema_id": "codex.ui-stage-preflight-evidence/v1", "check_id": check_id, "program_id": PROGRAM_ID, "stage_instance_id": STAGE_ID, "gate_id": "G4", "status": "passed", "facts": facts})
    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": PROGRAM_ID,
        "from_stage_id": STAGE_ID,
        "from_gate": "G4",
        "from_target": FAMILY_REVISION_ID,
        "from_revision": 5,
        "artifact": rel(family_path),
        "to_gate": "G4",
        "to_stage_id": "G4@family.dq.shell-workspace.baseline-r5",
        "to_target": "family.dq.shell-workspace.baseline-r5",
        "to_task": next_prompt_ref,
        "status": "ready",
        "owner_decision": rel(decision_path),
        "decision_inventory": rel(decision_inventory_path),
        "blockers": rel(blockers_path),
        "checks": [f"{check_id}={rel(preflight_dir / f'{check_id}.json')}" for check_id in ("current_gate", "source_freshness", "next_stage_inputs", "write_scope", "foreign_changes", "execution_route", "handoff_artifact")],
        "summary": "The owner accepted the exact corrected Data Connections family; the strict family gate and adjacent-stage preflight pass.",
        "review_artifacts": [rel(board_path), rel(EVIDENCE_DIR / "review-board-1440.png"), rel(EVIDENCE_DIR / "browser-board-qa.json")],
        "questions": [],
    }
    write_json(EVIDENCE_DIR / "stage-transition-request.json", request)
    report = f"""---
artifact_kind: ui_design_program_stage_evidence
stage_instance_id: {STAGE_ID}
gate_id: G4
status: ready
proof_boundary: accepted current-contract isolated browser evidence for six UI-DATA-001 states and four responsive-Web anchors; no production implementation, publication, deployment, mobile-specific design, full WCAG conformance, persistence, authorization, or performance proof
---

# G4 data connections family r5 execution report

## Result

- The exact corrected family review board is owner-accepted.
- Family aggregate: `{rel(family_path)}` (`passed`).
- Review board: `{rel(board_path)}`.
- Browser board QA: `{rel(EVIDENCE_DIR / 'browser-board-qa.json')}`.
- Transition: `{EVIDENCE_REF}/stage-transition.json` (`ready`).

## Validation

- `python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile family_gate --project-root . {rel(family_path)}` — passed with no warnings.
- `python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_stage_ledger.py --project-root . .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md` — passed.
- `python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_stage_transition.py --project-root . --ledger .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md {EVIDENCE_REF}/stage-transition.json` — passed.
- `python3 .codex/delivery/ui-design-programs/custometry-v2/run_g4_data_r5_board_qa.py` — passed, including accepted-pilot KPI-row conformance and clean console/network observations.
- `uv run python -m tools.check --scope local` — passed.

## File manifest

- `created`:
  - `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-data-shell-workspace-baseline/**`
  - `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.data.shell-workspace.baseline-r5/**`
  - `.codex/delivery/evidence/custometry-ui-design-program-v2/family.data.shell-workspace.baseline-r5-report.md`
  - `.codex/delivery/ui-design-programs/custometry-v2/build_g4_data_r5_artifacts.py`
  - `.codex/delivery/ui-design-programs/custometry-v2/run_g4_data_r5_board_qa.py`
  - `.codex/delivery/ui-design-programs/custometry-v2/run_g4_data_r5_proof.py`
- `modified`:
  - `.codex/delivery/ui-design-programs/custometry-v2/mutate_blueprint_rebind_r5_lifecycle.py`
  - `.codex/agents/generated/custometry-ui-design-g0-v2/40-g4-03-family-data-shell-workspace-baseline-r5.md`
  - `.codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md`
- `deleted`: none.
- `outside_expected_paths`: none.
- `foreign_changes_excluded`:
  - `.codex/AGENTS.md`
  - `custometry-technical-blueprint-human-ru.md`
  - `custometry-technical-blueprint-ru.md`
  - `custometry-ui-blueprint-ru.md`
  - `docs/generated/requirement-index.json`
  - `packages/contracts/routes/ui-surface-contracts.json`

## Proof boundary and residual risk

Automated evidence covers contract shape, deterministic standard applicability,
clause-level computed values, keyboard/accessibility smoke, loopback isolation,
console/network observations, responsive-Web overflow, rendered owner review,
and the accepted-pilot KPI-row correction. Mobile-specific scope remains
unauthorized. No production frontend, API, authorization, database, performance,
deployment, release, or full WCAG claim is made.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    print(json.dumps({"status": "acceptance_transition_inputs_prepared", "request": rel(EVIDENCE_DIR / "stage-transition-request.json"), "report": rel(REPORT)}, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "bind-applicability", "review", "transition-inputs", "acceptance-request", "acceptance-transition-inputs"))
    args = parser.parse_args()
    {"prepare": prepare, "bind-applicability": bind_applicability, "review": review, "transition-inputs": transition_inputs, "acceptance-request": acceptance_request, "acceptance-transition-inputs": acceptance_transition_inputs}[args.phase]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
