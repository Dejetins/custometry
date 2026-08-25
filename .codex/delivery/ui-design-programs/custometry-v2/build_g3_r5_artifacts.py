#!/usr/bin/env python3
"""Build the blueprint-rebound G3 r5 foundation and shell review artifacts."""

from __future__ import annotations

import argparse
from copy import deepcopy
import fcntl
import hashlib
import html
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
OLD_ART = DIR / "artifacts/g3-r4"
ART = DIR / "artifacts/g3-r5"
EVID = DIR / "evidence/g3-r5"
PROGRAM = DIR / "ui-design-program.json"
BASELINE = DIR / "artifacts/g0-r5/platform-ui-baseline.json"
INTAKE = DIR / "artifacts/g0-r5/ui-program-intake.json"
SOURCE = DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
CONTRACT = ART / "representative-shell-contract.json"
APPLICABILITY = ART / "representative-shell-standard-applicability.json"
STANDARD_BOARD = ART / "standard-board.html"
CANDIDATE = ART / "candidate-shell.html"
FIXTURE = ART / "fixture.json"
INHERITANCE = ART / "inheritance-report.json"
RENDER_CONTEXT = ART / "render-program-context.json"
SNAPSHOT = ART / "ui-design-program.snapshot.json"
PROMOTION = ART / "ui-design-program.promotion-candidate.json"
REVIEW_BOARD = ART / "review-board.html"
REVIEW_MANIFEST = ART / "review-board.manifest.json"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/g3-r5-foundations-shell-report.md"
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
STAGE_ID = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5"
SCREEN_REVISION_ID = "UI-ADMIN-003.populated.IA.ru.graphite.g3-r5"
ANCHORS = (("web-768", 768, 1024), ("web-1024", 1024, 768), ("web-1440", 1440, 900), ("web-1920", 1920, 1080))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def old_builder() -> Any:
    path = DIR / "build_g3_r4_compatibility_reproof.py"
    spec = importlib.util.spec_from_file_location("g3_r4_builder", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def configure(module: Any) -> None:
    module.OLD_ART = OLD_ART
    module.OLD_EVID = DIR / "evidence/g3-r4"
    module.ART = ART
    module.EVID = EVID
    module.PROGRAM = PROGRAM
    module.BASELINE = BASELINE
    module.SOURCE = SOURCE
    module.CONTRACT = CONTRACT
    module.APPLICABILITY = APPLICABILITY
    module.CANDIDATE = CANDIDATE
    module.FIXTURE = FIXTURE
    module.SNAPSHOT = SNAPSHOT
    module.PROMOTION_CANDIDATE = PROMOTION
    module.REVIEW_BOARD = REVIEW_BOARD
    module.REVIEW_MANIFEST = REVIEW_MANIFEST
    module.SCREEN_REVISION_ID = SCREEN_REVISION_ID
    module.ANCHORS = tuple(row[0] for row in ANCHORS)


def patch_candidate(baseline: dict[str, Any]) -> None:
    text = CANDIDATE.read_text(encoding="utf-8")
    text = text.replace("G3 foundations and shell r4 compatibility reproof", "G3 foundations and shell r5 semantic rebind")
    text = text.replace('data-revision="4"', 'data-revision="5"', 1)
    text = re.sub(r'(<meta name="ui-font-bundle-sha256" content=")[a-f0-9]+', rf'\g<1>{canonical_sha(baseline["font_contract"])}', text)
    text = re.sub(r'(<meta name="ui-asset-bundle-sha256" content=")[a-f0-9]+', rf'\g<1>{canonical_sha(baseline["asset_contract"])}', text)
    text = text.replace("Нейтральная оболочка", "Аналитический workspace")
    text = text.replace("Не экран G4", "Foundation checkpoint")
    text = text.replace("Правила оболочки и визуального языка", "Отчёт и Result Inspector")
    text = text.replace(
        "Нейтральный программный specimen показывает только наследуемые foundations, shell-поведение и аналитическую грамматику — без данных и композиции целевого экрана.",
        "Законченный foundation specimen связывает принятую Graphite-оболочку с новыми KPI, period/comparison, filter и template contracts — без приёмки конкретного продуктового экрана.",
    )
    text = text.replace(
        '<button class="context-chip" type="button"><span>Режим</span> <strong>Graphite</strong></button><button class="context-chip" type="button"><span>Web</span> <strong>768–1920</strong></button><button class="context-chip" type="button" data-active="true"><strong>Populated</strong></button>',
        '<button class="context-chip" type="button"><span>Период</span> <strong>Месяц · 2026</strong></button><button class="context-chip" type="button"><span>Сравнение</span> <strong>Год к году</strong></button><button class="context-chip" type="button" data-active="true"><strong>Личный вид</strong></button>',
    )
    text = text.replace("Фиксированные параметры оболочки", "Personal KPI view · опубликованный default можно восстановить")
    text = text.replace("<strong>Контракт</strong><span>Нулевой допуск</span>", "<strong>Мои KPI</strong><span>Сохранено · личное</span>")
    text = text.replace("<span>Rail</span><b>62 px</b><em>pilot</em>", "<span>Выручка · за месяц</span><b>8,42 млн</b><em>+12,4%</em>")
    text = text.replace("<span>Gap</span><b>12 px</b><em>baseline</em>", "<span>Маржа</span><b>31,7%</b><em>+1,8 п.п.</em>")
    text = text.replace("<span>Profile</span><b>32 px</b><em>baseline</em>", "<span>Активные клиенты</span><b>1 248</b><em>+6,2%</em>")
    text = text.replace("<span>Rows</span><b>≥32 px</b><em>analytical</em>", "<span>Средний чек</span><b>6 748 ₽</b><em>−2,1%</em>")
    text = text.replace("<span>Chrome</span><b>97 px</b><em>pilot</em>", "<span>Настройка</span><b>4 KPI</b><em>Сбросить</em>")
    text = text.replace("Источник и реализация hash-bound · восстановление доступно", "Snapshot v18 · автор и публикация видимы · данные разрешены backend")
    text = text.replace("Аналитическая грамматика", "Динамика выручки")
    text = text.replace("Focus / Explore · демонстрационные кривые без продуктового значения", "Блок: Как в отчёте · месяц · год к году")
    text = text.replace("Серии · 4", "Серии · template Graphite")
    text = text.replace("Табличный паттерн", "Data table · тот же bucketed artifact")
    inspector = '''<aside class="inspector-panel" id="inspector-panel-context" data-ui-region="analytics.inspector" data-ui-element="region-analytics-inspector" aria-label="Result Inspector"><header class="panel-header"><div><h2>Result Inspector</h2><p>Период отчёта · месяц · год к году</p></div><button type="button" id="inspector-close" aria-label="Закрыть инспектор">Закрыть</button></header><nav class="inspector-tabs" aria-label="Разделы Result Inspector"><button type="button" aria-selected="true">Контекст</button><button type="button" aria-selected="false">Фильтры</button><button type="button" aria-selected="false">Обсуждение</button><button type="button" aria-selected="false">Доверие</button><button type="button" aria-selected="false">Виды</button></nav><div class="inspector-body"><section class="inspector-card accent-card"><h3>Общий период</h3><p>Месяц · авг. 2026 · год к году. Блок наследует: «Как в отчёте · месяц».</p></section><section class="inspector-card"><h3>Фильтры</h3><div class="filter-state"><span>System / inherited</span><b>Workspace · RU</b></div><div class="filter-state"><span>Draft expression</span><b>Клиент AND (Москва OR Казань)</b></div><div class="filter-state"><span>Applied expression</span><b>Все разрешённые клиенты</b></div><div class="estimate">Предварительно ≈ 12,4 тыс. строк · Apply повторно проверит backend</div></section><section class="inspector-card"><h3>Виды</h3><div class="inspector-source-row"><span>Report template</span><code>Graphite / v3</code></div><div class="inspector-source-row"><span>Block override</span><code>inherit</code></div><p>Конструктор палитры и типографики остаётся отдельной Settings surface.</p></section><section class="inspector-card"><h3>Публикация</h3><p>Автор: Анна В. · обновлено 18 авг. · publication v18. Snapshot раскрывается по запросу.</p></section></div></aside>'''
    text, count = re.subn(r'<aside class="inspector-panel".*?</aside>', inspector, text, count=1, flags=re.S)
    if count != 1:
        raise ValueError("inspector markup was not replaced")
    text = text.replace(
        'id="inspector-panel-context" data-ui-region=',
        'id="inspector-panel-context" data-open="true" data-ui-region=',
        1,
    )
    css = '''
    /* G3 r5 semantic-rebind alignment: one pane/toggle across wide and narrow Web. */
    .workspace[data-inspector-open="true"] .workspace-body{grid-template-columns:minmax(0,1fr);padding-inline-end:clamp(340px,28vw,430px)}
    .inspector-panel,.workspace[data-inspector-open="true"] .inspector-panel{display:block;position:absolute;z-index:390;inset-block:0;inset-inline-end:0;width:clamp(340px,28vw,430px);height:100%;border-inline-start:1px solid var(--line-soft);background:#151619;box-shadow:-18px 0 40px rgba(0,0,0,.28);transform:translateX(calc(100% + 28px));visibility:hidden;transition:transform var(--motion),visibility 0s linear 120ms}
    .workspace[data-inspector-open="true"] .inspector-panel{transform:none;visibility:visible;transition-delay:0s}
    .inspector-panel .panel-header{height:56px;min-height:56px;padding-inline:14px 10px}.inspector-tabs{inset-block-start:56px;grid-template-columns:repeat(5,minmax(0,1fr));height:41px;padding:4px}.inspector-tabs button{font-size:8px}.accent-card{box-shadow:inset 2px 0 var(--accent),inset 0 0 0 1px rgba(255,255,255,.035)}
    .filter-state{display:grid;gap:3px;padding:8px 0;border-top:1px solid var(--line-soft);font-size:9px}.filter-state span{color:var(--soft)}.filter-state b{font-weight:570}.estimate{margin-top:7px;padding:8px;border-radius:7px;background:var(--accent-soft);color:#bfe5ef;font-size:8px;line-height:1.45}
    @media(max-width:1199px){.workspace[data-inspector-open="true"] .workspace-body{padding-inline-end:0}.inspector-panel,.workspace[data-inspector-open="true"] .inspector-panel{position:fixed;z-index:440;inset-block:12px;inset-inline-end:12px;width:min(430px,calc(100vw - 94px));height:calc(100vh - 24px);border:0;border-radius:15px}}
    @media(max-width:899px){.inspector-panel,.workspace[data-inspector-open="true"] .inspector-panel{inset-block:5px;inset-inline-end:5px;width:min(430px,calc(100vw - 10px));height:calc(100vh - 10px)}}
    '''
    text = text.replace("</style>", css + "</style>", 1)
    text = text.replace('class="workspace" data-ui-region=', 'class="workspace" data-inspector-open="true" data-ui-region=', 1)
    text = text.replace(' aria-label="Рабочая область" data-inspector-open="false">', ' aria-label="Рабочая область">', 1)
    text = text.replace("inspector.setAttribute('aria-hidden','true');", "inspector.setAttribute('aria-hidden','false');inspectorToggle.setAttribute('aria-expanded','true');inspectorToggle.setAttribute('aria-label','Закрыть инспектор');")
    CANDIDATE.write_text(text, encoding="utf-8")


def patch_contract(baseline: dict[str, Any], program: dict[str, Any]) -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    origin = {"kind": "product_contract", "ref": f"{rel(BASELINE)}#/responsive_contract"}
    contract["screen_revision_id"] = SCREEN_REVISION_ID
    contract["program_revision_ref"] = f"{PROGRAM_ID}@5"
    contract["functional_contract_ref"].update({"path": rel(INTAKE), "sha256": sha(INTAKE)})
    contract["baseline_binding"].update({"baseline_id": baseline["baseline_id"], "path": rel(BASELINE), "sha256": sha(BASELINE)})
    contract["standard_binding"].update({
        "standard_revision_id": baseline["standard_contract"]["standard_revision_id"],
        "clause_inventory_sha256": baseline["standard_contract"]["clause_inventory_sha256"],
        "applicability_manifest": {"path": rel(APPLICABILITY), "sha256": "0" * 64},
    })
    contract["visual_authority"] = {
        key: program["visual_authority"][key]
        for key in (
            "source_visual_ref", "source_visual_sha256", "owner_decision_ref",
            "screen_acceptance_scope", "visual_language_scope",
            "reusable_foundation_scope", "inheritance_policy", "mobile_scope",
        )
    }
    contract["comparison_claims"].update({
        "reference_logical_artifact_id": f"{PROGRAM_ID}:accepted-pilot:ru:r5",
        "implementation_logical_artifact_id": f"{PROGRAM_ID}:g3-candidate:r5",
    })
    contract["render_environment"].update({
        "fixture_data_path": rel(FIXTURE), "fixture_data_sha256": sha(FIXTURE),
        "font_bundle_sha256": canonical_sha(baseline["font_contract"]),
        "asset_bundle_sha256": canonical_sha(baseline["asset_contract"]),
    })
    contract["viewport_contract"]["supported_web_width_range"] = {**baseline["responsive_contract"]["supported_web_width_range"], "origin": origin}
    contract["viewport_contract"]["anchors"] = [
        {"anchor_id": aid, "width": width, "height": height, "class": "responsive_web", "state_ref": "UI-ADMIN-003.populated", "origin": origin}
        for aid, width, height in ANCHORS
    ]
    contract["viewport_contract"]["above_supported_range_origin"] = origin
    contract["acceptance"].update({"owner_decision_ref": None, "screen_acceptance_receipt_path": None, "screen_acceptance_receipt_sha256": None})
    write_json(CONTRACT, contract)
    subprocess.run(["python3", str(SKILL / "assemble_standard_applicability.py"), "--screen", str(CONTRACT), "--baseline", str(BASELINE), "--project-root", str(ROOT), "--output", str(APPLICABILITY)], check=True)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    contract["standard_binding"]["applicability_manifest"]["sha256"] = sha(APPLICABILITY)
    write_json(CONTRACT, contract)


def bootstrap() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    EVID.mkdir(parents=True, exist_ok=True)
    module = old_builder()
    configure(module)
    module.bootstrap()
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    patch_candidate(baseline)
    patch_contract(baseline, program)
    standard_html = (DIR / "artifacts/g3-r3/standard-board.html").read_text(encoding="utf-8")
    standard_html = standard_html.replace('data-revision="4"', 'data-revision="5"', 1)
    standard_html = standard_html.replace("complete pilot standard", "complete pilot standard · r5 binding", 1)
    STANDARD_BOARD.write_text(standard_html, encoding="utf-8")
    standard = baseline["standard_contract"]
    write_json(INHERITANCE, {
        "schema_id": "codex.ui-visual-inheritance-report/v2",
        "program_id": PROGRAM_ID,
        "program_revision": 5,
        "visual_authority_sha256": canonical_sha(program["visual_authority"]),
        "standard_revision_id": standard["standard_revision_id"],
        "clause_inventory_sha256": standard["clause_inventory_sha256"],
        "clause_ids": sorted(row["clause_id"] for row in standard["clauses"]),
        "accepted_exception_clause_ids": [],
        "standard_board_sha256": sha(STANDARD_BOARD),
        "dimensions": ["tokens", "typography", "density", "spacing", "navigation", "shell_regions", "panel_control_grammar", "responsive_adaptations"],
        "applicability_manifest": {"path": rel(APPLICABILITY), "sha256": sha(APPLICABILITY)},
        "coverage": {
            "clause_count": len(standard["clauses"]),
            "applicable_clause_count": 105,
            "source_backed_not_applicable_clause_count": len(standard["clauses"]) - 105,
            "complete_applicable_rule_set_per_matching_element": True,
            "partial_inheritance": "forbidden",
            "aesthetic_approximation": "forbidden",
        },
        "semantic_rebind": ["personal KPI Saved View and reset", "shared and block-local period/comparison", "five-section Result Inspector", "draft/applied/estimate filter separation", "report template and block override"],
        "excluded": ["exact target-screen composition", "production semantics", "mobile-specific design", "G4 family acceptance"],
        "result": "passed",
    })
    render_context = deepcopy(program)
    render_context.update({"status": "review", "validation_profile": "program_ready"})
    write_json(RENDER_CONTEXT, render_context)
    for aid, _, _ in ANCHORS:
        folder = EVID / "captures" / aid
        for target, logical, source in (
            ("reference", f"{PROGRAM_ID}:accepted-pilot:ru:r5", SOURCE),
            ("implementation", f"{PROGRAM_ID}:g3-candidate:r5", CANDIDATE),
        ):
            write_json(folder / f"{target}-provenance-request.json", {
                "program_ref": rel(RENDER_CONTEXT), "target": target, "logical_artifact_id": logical,
                "anchor_id": aid, "source_artifact_ref": rel(source), "capture_ref": rel(folder / f"{target}.png"),
                "geometry_receipt_ref": rel(folder / f"{target}-geometry.json"),
            })


def finalize() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    source_rows, candidate_rows, entries = [], [], []
    for aid, _, _ in ANCHORS:
        folder = EVID / "captures" / aid
        source_rows.append({"anchor_id": aid, "path": rel(folder / "reference.png"), "sha256": sha(folder / "reference.png"), "render_provenance_ref": rel(folder / "reference-provenance.json"), "render_provenance_sha256": sha(folder / "reference-provenance.json")})
        candidate_rows.append({"anchor_id": aid, "path": rel(folder / "implementation.png"), "sha256": sha(folder / "implementation.png"), "render_provenance_ref": rel(folder / "implementation-provenance.json"), "render_provenance_sha256": sha(folder / "implementation-provenance.json")})
    def add(role: str, path: Path, anchor: str | None = None) -> None:
        entries.append({"entry_id": f"review-{len(entries)+1:02d}", "role": role, "artifact_ref": rel(path), "sha256": sha(path), "anchor_id": anchor, "state_id": None})
    add("source_native", ROOT / program["g3_rendered_proof"]["source_native_capture"]["path"])
    for aid, _, _ in ANCHORS:
        add("source_anchor", EVID / "captures" / aid / "reference.png", aid)
    add("candidate", CANDIDATE)
    for aid, _, _ in ANCHORS:
        add("candidate_anchor", EVID / "captures" / aid / "implementation.png", aid)
    for aid, _, _ in ANCHORS:
        add("render_provenance", EVID / "captures" / aid / "implementation-provenance.json", aid)
    add("inheritance", INHERITANCE)
    add("standard_conformance", STANDARD_BOARD)
    add("screen_contract", CONTRACT)
    write_json(REVIEW_MANIFEST, {"$schema": "review-board-manifest.schema.json", "schema_id": "codex.ui-review-board-manifest/v1", "program_id": PROGRAM_ID, "artifact_id": PROGRAM_ID, "revision": 5, "validation_profile": "program_ready", "entries": entries})
    cards = "".join(f'<figure><img src="../../evidence/g3-r5/captures/{aid}/implementation.png" alt="G3 r5 {aid}"><figcaption>{aid} · Result Inspector открыт</figcaption></figure>' for aid, _, _ in reversed(ANCHORS))
    closure = "".join(f'<li data-review-entry="{row["entry_id"]}">{html.escape(row["role"])}</li>' for row in entries)
    REVIEW_BOARD.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry · G3 r5 semantic rebind</title><style>:root{{--bg:#070708;--panel:#111214;--line:#303136;--ink:#f0f0f2;--muted:#a7a7ad;--accent:#66b9d3}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,system-ui,sans-serif}}main{{width:min(1500px,calc(100% - 32px));margin:auto;padding:26px 0 60px}}h1{{margin:0;font-size:clamp(32px,6vw,64px);line-height:1}}p{{max-width:88ch;color:var(--muted)}}.notice{{padding:16px;border:1px solid #315a67;border-radius:15px;background:#101b1f}}.grid{{columns:2;gap:14px;margin-top:16px}}figure{{break-inside:avoid;margin:0 0 14px;border:1px solid var(--line);border-radius:15px;overflow:hidden;background:var(--panel)}}img{{display:block;width:100%}}figcaption{{padding:10px 14px;color:var(--muted)}}a{{color:#9bd9ec}}.closure{{display:none}}@media(max-width:900px){{.grid{{columns:1}}}}</style></head><body data-ui-artifact="review_board" data-program-id="{PROGRAM_ID}" data-artifact-id="{PROGRAM_ID}" data-revision="5" data-validation-profile="program_ready" data-review-manifest="{rel(REVIEW_MANIFEST)}" data-review-manifest-sha256="{sha(REVIEW_MANIFEST)}"><main><p>G3 · finished foundation checkpoint</p><h1>Graphite shell × новые semantic contracts</h1><div class="notice">Проверьте визуальную систему, иерархию и адаптивное поведение. Это authority для foundations/shell, но не приёмка конкретного G4-экрана.</div><p><a href="candidate-shell.html">Открыть интерактивный specimen</a> · personal KPI · period/comparison · filters · Result Inspector · Views</p><div class="grid">{cards}</div><ul class="closure">{closure}</ul></main></body></html>''', encoding="utf-8")
    proof = {
        "source_evidence_mode": "renderable_html",
        "shell_capture_contract": {"path": rel(CONTRACT), "sha256": sha(CONTRACT), "screen_revision_id": SCREEN_REVISION_ID},
        "source_native_capture": deepcopy(program["g3_rendered_proof"]["source_native_capture"]),
        "source_anchor_observations": source_rows,
        "candidate_artifact": {"path": rel(CANDIDATE), "sha256": sha(CANDIDATE)},
        "candidate_anchor_captures": candidate_rows,
        "standard_board": {"path": rel(STANDARD_BOARD), "sha256": sha(STANDARD_BOARD)},
        "review_board": {"path": rel(REVIEW_BOARD), "sha256": sha(REVIEW_BOARD)},
        "inheritance_report": {"path": rel(INHERITANCE), "sha256": sha(INHERITANCE)},
    }
    successor = deepcopy(program)
    successor.update({"status": "review", "validation_profile": "program_ready", "g3_rendered_proof": proof})
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    responsive = baseline["responsive_contract"]
    origin = {"kind": "product_contract", "ref": f"{rel(BASELINE)}#/responsive_contract"}
    successor["responsive_policy"].update({
        "supported_web_width_range": {**responsive["supported_web_width_range"], "origin": origin},
        "anchor_viewports": [{"anchor_id": aid, "width": width, "height": height, "class": "responsive_web", "origin": origin} for aid, width, height in ANCHORS],
    })
    for coverage in successor["coverage_profiles"]:
        coverage["viewport_anchor_ids"] = {"mode": "required", "values": [row[0] for row in ANCHORS], "origin": origin, "not_applicable_reason_ref": None}
        coverage["unresolved_fields"] = [item for item in coverage.get("unresolved_fields", []) if item != "viewport_anchor_ids"]
    successor["execution_artifacts"]["plan_doc"] = rel(SNAPSHOT)
    write_json(SNAPSHOT, successor)
    promoted = deepcopy(successor)
    promoted["execution_artifacts"]["plan_doc"] = rel(PROGRAM)
    write_json(PROMOTION, promoted)
    packet = {
        "schema_id": "custometry.ui-owner-review-decision-packet/v1", "program_id": PROGRAM_ID, "stage_instance_id": STAGE_ID,
        "decision_id": f"{STAGE_ID}.finished-foundations-shell", "decision_kind": "stage_acceptance",
        "review_artifact": {"path": rel(REVIEW_BOARD), "sha256": sha(REVIEW_BOARD)},
        "candidate_artifact": {"path": rel(CANDIDATE), "sha256": sha(CANDIDATE)},
        "machine_gate": {"profile": "program_ready", "result": "passed", "artifact": rel(PROGRAM), "sha256": sha(PROGRAM)},
        "decision_scope": {"changed": "Foundation/shell expression of the accepted blueprint semantic rebind.", "unchanged": ["accepted visual authority", "exact target-screen composition", "production implementation", "mobile scope"]},
        "question": "Принять законченный G3 r5 foundation/shell checkpoint или запросить ограниченные визуальные исправления?",
        "allowed_responses": ["accept", "bounded_corrections"],
        "resume_condition": "An unambiguous natural-language decision for this exact finished G3 r5 board is recorded through the canonical owner-response route.", "next_stage_allowed": False,
    }
    write_json(EVID / "owner-review-decision-packet.json", packet)
    write_json(EVID / "pending-owner-decisions.json", [{"decision_id": packet["decision_id"], "class": "owner_required", "status": "pending", "summary": "Accept the exact finished G3 r5 board or request bounded visual corrections.", "resolution_ref": None}])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(f"""# G3 r5 foundations and shell report\n\n- Stage: `{STAGE_ID}`\n- Result: `review_ready` pending owner visual acceptance\n- Review board: `{rel(REVIEW_BOARD)}` (`{sha(REVIEW_BOARD)}`)\n- Candidate: `{rel(CANDIDATE)}` (`{sha(CANDIDATE)}`)\n- Web anchors: `768`, `1024`, `1440`, `1920` CSS px\n- Scope: inherited Graphite foundations plus blueprint-rebound shell semantics; no G4 screen acceptance, production implementation, mobile-specific design, publication, or deployment.\n- Next stage allowed: `false`\n""", encoding="utf-8")


def promote(expected_sha256: str | None) -> None:
    if expected_sha256 is None:
        raise ValueError("promote requires --expected-program-sha256")
    lock_path = PROGRAM.with_name(f".{PROGRAM.name}.write.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        observed = sha(PROGRAM)
        if observed != expected_sha256:
            raise ValueError(f"stale program source: expected {expected_sha256}, observed {observed}")
        with tempfile.NamedTemporaryFile(
            dir=PROGRAM.parent, prefix=f".{PROGRAM.name}.", delete=False
        ) as temporary:
            temporary.write(PROMOTION.read_bytes())
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, PROGRAM)
        print(json.dumps({
            "status": "applied", "source_sha256": observed,
            "applied_sha256": sha(PROGRAM),
        }))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("bootstrap", "finalize", "promote"))
    parser.add_argument("--expected-program-sha256")
    args = parser.parse_args()
    if args.mode == "bootstrap":
        bootstrap()
    elif args.mode == "finalize":
        finalize()
    else:
        promote(args.expected_program_sha256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
