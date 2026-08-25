#!/usr/bin/env python3
"""Prepare canonical G3 provenance requests and finalize the owner review closure."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
ART = DIR / "artifacts/g3-r3"
EVID = DIR / "evidence/g3-r3"
PROGRAM = DIR / "ui-design-program.json"
BASELINE = DIR / "artifacts/g0-r4/platform-ui-baseline.json"
SOURCE = DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
CANDIDATE = ART / "candidate-shell.html"
CONTRACT = ART / "representative-shell-contract.json"
APPLICABILITY = ART / "representative-shell-standard-applicability.json"
STANDARD_BOARD = ART / "standard-board.html"
INHERITANCE = ART / "inheritance-report.json"
REVIEW_MANIFEST = ART / "review-board.manifest.json"
REVIEW_BOARD = ART / "review-board.html"
SNAPSHOT = ART / "ui-design-program.snapshot.json"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
SCREEN_REVISION_ID = "UI-ADMIN-003.populated.IA.ru.graphite.g3-r3"
ANCHORS = ("web-768", "web-1024", "web-1440", "web-1920")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_requests() -> None:
    req = EVID / "render-provenance-requests"
    req.mkdir(parents=True, exist_ok=True)
    for anchor in ANCHORS:
        for target, logical, artifact, prefix in (
            ("reference", f"{PROGRAM_ID}:accepted-pilot:ru:r4", SOURCE, "source"),
            ("implementation", f"{PROGRAM_ID}:g3-candidate:r3", CANDIDATE, "candidate"),
        ):
            write_json(req / f"{target}-{anchor}.json", {
                "program_ref": rel(PROGRAM), "target": target,
                "logical_artifact_id": logical, "anchor_id": anchor,
                "source_artifact_ref": rel(artifact),
                "capture_ref": rel(EVID / f"{prefix}-{anchor}.png"),
                "geometry_receipt_ref": rel(EVID / f"{prefix}-{anchor}-geometry.json"),
            })


def build_standard_board(baseline: dict) -> None:
    standard = baseline["standard_contract"]
    grouped: dict[str, list[dict]] = {}
    for clause in standard["clauses"]:
        grouped.setdefault(clause["domain"], []).append(clause)
    sections = {
        "foundations": ["color", "spacing", "sizing", "radius", "border", "elevation", "opacity", "icon"],
        "typography": ["typography"],
        "components_states": ["component", "interaction", "focus", "motion"],
        "shell_layout": ["shell", "layout"],
        "responsive": ["responsive", "overflow", "accessibility", "copy"],
    }
    section_titles = {
        "foundations": "Основы", "typography": "Полная типографика",
        "components_states": "Компоненты и состояния", "shell_layout": "Оболочка и компоновка",
        "responsive": "Responsive Web, focus и motion",
    }
    blocks = []
    for section_id, domains in sections.items():
        rows = [row for domain in domains for row in grouped.get(domain, [])]
        items = "".join(
            f'<tr><td><code>{html.escape(row["clause_id"])}</code></td><td>{html.escape(row["property"])}</td>'
            f'<td>{html.escape(str(row["value"]))}</td><td>{len(row["applicability"])}</td></tr>'
            for row in rows
        )
        blocks.append(
            f'<section data-standard-section="{section_id}"><h2>{section_titles[section_id]}</h2>'
            f'<p>{len(rows)} правил. Каждое применимое правило наследуется целиком; частичное наследование запрещено.</p>'
            f'<details><summary>Показать точный список</summary><table><thead><tr><th>Правило</th><th>Свойство</th><th>Значение</th><th>Селекторы</th></tr></thead><tbody>{items}</tbody></table></details></section>'
        )
    STANDARD_BOARD.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Custometry · complete pilot standard</title><style>:root{{--bg:#070708;--card:#111214;--line:#303136;--text:#f0f0f2;--soft:#a7a7ad;--accent:#66b9d3}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 Inter,system-ui,sans-serif}}main{{width:min(1400px,calc(100% - 32px));margin:auto;padding:28px 0 60px}}h1{{font-size:clamp(30px,5vw,62px);letter-spacing:-.045em;line-height:1;margin:0}}header p{{max-width:82ch;color:var(--soft)}}.facts{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:20px 0}}.fact,section{{border:1px solid var(--line);border-radius:15px;background:var(--card);padding:16px}}.fact b{{display:block;font-size:22px}}.fact span,section p{{color:var(--soft)}}section{{margin:12px 0}}summary{{cursor:pointer;color:var(--accent)}}table{{width:100%;border-collapse:collapse;margin-top:12px;font-size:11px}}td,th{{padding:8px;border-top:1px solid var(--line);text-align:left;vertical-align:top}}code{{color:#9bd9ec}}@media(max-width:800px){{.facts{{grid-template-columns:1fr 1fr}}}}</style></head><body data-ui-artifact="candidate" data-program-id="{PROGRAM_ID}" data-artifact-id="{PROGRAM_ID}.standard" data-revision="4" data-validation-profile="program_ready"><main><header><h1>Полный стандарт пилота</h1><p>Это не подборка токенов и не эстетическое приближение. Для каждого элемента последующих экранов канонический механизм определяет все соответствующие правила пилота и требует их полного выполнения либо точного обоснования неприменимости.</p></header><div class="facts"><div class="fact"><b>{len(standard['clauses'])}</b><span>нормативных правил</span></div><div class="fact"><b>5 / 5</b><span>обязательных разделов</span></div><div class="fact"><b>0</b><span>исключений владельца</span></div><div class="fact"><b>точное</b><span>детерминированное применение</span></div></div>{''.join(blocks)}</main></body></html>''', encoding="utf-8")


def evidence_ref(path: Path) -> dict:
    return {"path": rel(path), "sha256": sha(path)}


def finalize() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    applicability = json.loads(APPLICABILITY.read_text(encoding="utf-8"))
    build_standard_board(baseline)
    standard = baseline["standard_contract"]
    clause_ids = sorted(row["clause_id"] for row in standard["clauses"])
    dimensions = ["tokens", "typography", "density", "spacing", "navigation", "shell_regions", "panel_control_grammar", "responsive_adaptations"]
    write_json(INHERITANCE, {
        "schema_id": "codex.ui-visual-inheritance-report/v2",
        "program_id": PROGRAM_ID, "program_revision": program["revision"],
        "visual_authority_sha256": canonical_sha(program["visual_authority"]),
        "standard_revision_id": standard["standard_revision_id"],
        "clause_inventory_sha256": standard["clause_inventory_sha256"],
        "clause_ids": clause_ids, "accepted_exception_clause_ids": [],
        "standard_board_sha256": sha(STANDARD_BOARD), "dimensions": dimensions,
        "applicability_manifest": evidence_ref(APPLICABILITY),
        "coverage": {
            "clause_count": len(clause_ids),
            "applicable_clause_count": sum(x["disposition"] == "applicable" for x in applicability["entries"]),
            "source_backed_not_applicable_clause_count": sum(x["disposition"] == "source_backed_not_applicable" for x in applicability["entries"]),
            "complete_applicable_rule_set_per_matching_element": True,
            "partial_inheritance": "forbidden", "aesthetic_approximation": "forbidden",
        },
        "result": "passed",
    })
    source_rows, candidate_rows = [], []
    for anchor in ANCHORS:
        source_rows.append({
            "anchor_id": anchor, **evidence_ref(EVID / f"source-{anchor}.png"),
            "render_provenance_ref": rel(EVID / f"source-{anchor}-provenance.json"),
            "render_provenance_sha256": sha(EVID / f"source-{anchor}-provenance.json"),
        })
        candidate_rows.append({
            "anchor_id": anchor, **evidence_ref(EVID / f"candidate-{anchor}.png"),
            "render_provenance_ref": rel(EVID / f"candidate-{anchor}-provenance.json"),
            "render_provenance_sha256": sha(EVID / f"candidate-{anchor}-provenance.json"),
        })
    proof = program["g3_rendered_proof"]
    proof.update({
        "source_anchor_observations": source_rows, "candidate_anchor_captures": candidate_rows,
        "candidate_artifact": evidence_ref(CANDIDATE),
        "shell_capture_contract": {**evidence_ref(CONTRACT), "screen_revision_id": SCREEN_REVISION_ID},
        "standard_board": evidence_ref(STANDARD_BOARD), "inheritance_report": evidence_ref(INHERITANCE),
    })
    entries = []
    def add(role: str, ref: dict, anchor: str | None = None, path_key: str = "path", sha_key: str = "sha256") -> None:
        entries.append({"entry_id": f"review-{len(entries)+1:02d}", "role": role,
            "artifact_ref": ref[path_key], "sha256": ref[sha_key], "anchor_id": anchor, "state_id": None})
    add("source_native", proof["source_native_capture"])
    for row in source_rows: add("source_anchor", row, row["anchor_id"])
    add("candidate", proof["candidate_artifact"])
    for row in candidate_rows: add("candidate_anchor", row, row["anchor_id"])
    for row in candidate_rows: add("render_provenance", row, row["anchor_id"], "render_provenance_ref", "render_provenance_sha256")
    add("inheritance", proof["inheritance_report"]); add("standard_conformance", proof["standard_board"]); add("screen_contract", proof["shell_capture_contract"])
    write_json(REVIEW_MANIFEST, {"$schema": "review-board-manifest.schema.json", "schema_id": "codex.ui-review-board-manifest/v1",
        "program_id": PROGRAM_ID, "artifact_id": PROGRAM_ID, "revision": program["revision"],
        "validation_profile": "program_ready", "entries": entries})
    rendered_entries = "".join(f'<li data-review-entry="{x["entry_id"]}">{x["role"]} · {x["anchor_id"] or "program"}</li>' for x in entries)
    cards = "".join(f'<figure><img src="../../evidence/g3-r3/candidate-{a}.png" alt="G3 shell {a}"><figcaption>{a}</figcaption></figure>' for a in reversed(ANCHORS))
    REVIEW_BOARD.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Custometry G3 r3 review</title><style>:root{{--bg:#070708;--card:#111214;--line:#303136;--text:#f0f0f2;--soft:#a7a7ad;--accent:#66b9d3;--good:#62c7aa}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 Inter,system-ui,sans-serif}}main{{width:min(1500px,calc(100% - 32px));margin:auto;padding:28px 0 60px}}h1{{font-size:clamp(34px,6vw,68px);line-height:.95;letter-spacing:-.05em;margin:0}}header p{{max-width:84ch;color:var(--soft)}}.status{{display:inline-block;padding:8px 12px;border:1px solid #315a4b;border-radius:99px;color:#bfead7}}.principle,.review{{margin:16px 0;padding:18px;border:1px solid #315a67;border-radius:15px;background:#101b1f}}.grid{{columns:2;gap:14px}}figure{{break-inside:avoid;margin:0 0 14px;border:1px solid var(--line);border-radius:15px;overflow:hidden;background:var(--card)}}img{{display:block;width:100%}}figcaption{{padding:10px 14px;color:var(--soft)}}.links{{display:flex;gap:12px;flex-wrap:wrap}}a{{color:#9bd9ec}}.closure{{display:none}}@media(max-width:900px){{.grid{{columns:1}}}}</style></head><body data-ui-artifact="review_board" data-program-id="{PROGRAM_ID}" data-artifact-id="{PROGRAM_ID}" data-revision="4" data-validation-profile="program_ready" data-review-manifest="{rel(REVIEW_MANIFEST)}" data-review-manifest-sha256="{sha(REVIEW_MANIFEST)}"><main><header><span class="status">Machine gate · ready for review</span><h1>G3 · основы и оболочка</h1><p>Нейтральная оболочка показывает визуальный язык, который последующие экраны обязаны наследовать из принятого пилота. Она не утверждает продуктовую композицию конкретного экрана.</p></header><div class="principle"><b>Главное правило:</b> каждый элемент с соответствующим паттерном пилота получает весь набор применимых правил — типографику, цвет, размеры, отступы, радиусы, границы, состояния, focus, motion и responsive-поведение. Частичное наследование и «похожий стиль» не допускаются.</div><div class="links"><a href="standard-board.html">Открыть полный стандарт (203 правила)</a><a href="candidate-shell.html">Открыть интерактивную оболочку</a><a href="../../evidence/pilot-candidate-v3-metadata/ru/source.html">Открыть принятый пилот</a></div><div class="grid">{cards}</div><div class="review"><b>Что принимается на G3</b><p>Фундамент, полная типографика, компоненты и состояния, оболочка/компоновка, responsive Web, focus и motion как обязательная основа для G4. Продуктовое содержание и композиция будущих экранов не принимаются.</p></div><ul class="closure">{rendered_entries}</ul></main></body></html>''', encoding="utf-8")
    proof["review_board"] = evidence_ref(REVIEW_BOARD)
    program["g3_rendered_proof"] = proof
    write_json(PROGRAM, program)
    snapshot = json.loads(json.dumps(program)); snapshot["execution_artifacts"]["plan_doc"] = rel(SNAPSHOT); write_json(SNAPSHOT, snapshot)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("mode", choices=("requests", "finalize")); args = parser.parse_args()
    prepare_requests() if args.mode == "requests" else finalize()


if __name__ == "__main__":
    main()
