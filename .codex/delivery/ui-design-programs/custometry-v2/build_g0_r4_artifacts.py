#!/usr/bin/env python3
"""Build deterministic G0 r4 baseline, intake, standard, and owner board."""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
from typing import Any


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def selector_key(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


DOMAIN_CATEGORY = {
    "typography": "typography",
    "color": "color",
    "spacing": "spacing",
    "sizing": "sizing",
    "control": "sizing",
    "focus": "sizing",
    "layout": "sizing",
    "shell": "sizing",
    "responsive": "sizing",
    "component": "sizing",
    "icon": "sizing",
    "interaction": "sizing",
    "radius": "radius",
    "border": "border",
    "elevation": "elevation",
    "opacity": "opacity",
    "motion": "motion",
}


def specified(value: Any, unit: Any, source_ref: str) -> dict[str, Any]:
    return {
        "value": value,
        "unit": unit,
        "source_ref": source_ref,
        "tolerance": 0,
        "change_policy": "fixed",
    }


def rebuild_auth_screen(screen: dict[str, Any], *, recovery: bool) -> None:
    screen_id = screen["screen_id"]
    source_ref = screen["source_refs"][0]
    route = "/auth/recovery" if recovery else "/auth/sign-in"
    source_states = (
        "initial", "first_loading", "ready", "validation_error", "failed", "session_expired"
    )
    kind_by_state = {
        "initial": "initial",
        "first_loading": "loading",
        "ready": "populated",
        "validation_error": "error",
        "failed": "error",
        "session_expired": "permission_denied",
    }
    if recovery:
        action_specs = [
            ("validate-reset-token", "Validate reset token", "Validate the host/admin-issued reset token", None,
             "A valid token advances to password entry; invalid or expired tokens get a generic safe error"),
            ("set-new-password", "Set new password", "Set a new password under the source-defined password rules", "/auth/sign-in",
             "The password is reset and the user returns to sign in; failure preserves the step and safe retry"),
            ("return-sign-in", "Return to sign in", "Return without changing credentials", "/auth/sign-in",
             "The sign-in route opens without implying an email reset channel"),
        ]
        screen["purpose"] = "Password recovery/reset wizard for /auth/recovery using a host/admin-issued reset token"
        screen["user_outcomes"] = [
            "Validate an issued reset token, set a compliant password, and return safely to sign in"
        ]
    else:
        action_specs = [
            ("submit-credentials", "Sign in", "Authenticate with email and password", None,
             "A valid session opens the permitted destination; failure stays generic and retryable"),
            ("open-recovery", "Password help", "Open the distinct password recovery flow", "/auth/recovery",
             "The recovery wizard opens as UI-AUTH-004, never as a sign-in state"),
            ("toggle-remember", "Remember me", "Change the session persistence preference", None,
             "The local preference changes without authenticating the user"),
            ("change-language", "Change language", "Switch the authentication locale", None,
             "RU/EN content changes without altering route or product meaning"),
        ]
        screen["purpose"] = "Compact sign-in editor for /auth/sign-in"
        screen["user_outcomes"] = [
            "Authenticate, choose session persistence and language, or open the distinct recovery route"
        ]
    actions = []
    for suffix, label, intent, navigation_target, outcome in action_specs:
        actions.append({
            "action_id": f"{screen_id}.{suffix}",
            "control_type": "button" if suffix not in {"toggle-remember", "change-language"} else ("checkbox" if suffix == "toggle-remember" else "select"),
            "component_id": "action.button",
            "component_variant": "primary" if suffix in {"submit-credentials", "set-new-password"} else "secondary",
            "size_class": "sm",
            "label": label,
            "icon_id": None,
            "region_id": f"{screen_id}.content",
            "intent": intent,
            "visibility": "always",
            "enabled_when": "the current auth step is ready and no conflicting operation is in progress",
            "preconditions": [],
            "trigger": "click, Enter, or Space as appropriate for the native control",
            "outcome": outcome,
            "feedback": "show deterministic pending, success, or safe validation feedback",
            "failure": "show a generic source-backed error without revealing account existence or token details",
            "recovery": "preserve entered context where safe and keep retry or return available",
            "confirmation": "not required",
            "side_effects": [],
            "destructive": False,
            "permission_refs": [],
            "keyboard": "native keyboard operation with visible focus",
            "navigation_target": (
                "UI-AUTH-004" if navigation_target == "/auth/recovery"
                else "UI-AUTH-001" if navigation_target == "/auth/sign-in"
                else None
            ),
            "opens_surface_id": "UI-AUTH-004" if suffix == "open-recovery" else None,
            "source_refs": [source_ref],
        })
    screen["actions"] = actions
    screen["no_actions_reason"] = None
    screen["regions"][0].update({
        "purpose": screen["purpose"],
        "content": "route-specific auth fields, safe status, trust context, and functional controls; no marketing copy",
        "state_ids": [f"{screen_id}.{state}" for state in source_states],
        "action_ids": [action["action_id"] for action in actions],
    })
    state_actions = [action["action_id"] for action in actions]
    screen["states"] = [{
        "state_id": f"{screen_id}.{state}",
        "kind": kind_by_state[state],
        "trigger": (
            "route entry before the first source-profile transition"
            if state == "initial" else f"the source auth_flow state {state} is active"
        ),
        "visible_region_ids": [f"{screen_id}.content"],
        "available_action_ids": state_actions if state in {"ready", "validation_error", "failed", "session_expired"} else [],
        "exit_conditions": ["a declared auth action or source-profile transition occurs"],
        "source_refs": [source_ref],
    } for state in source_states]
    required_kinds = {state["kind"] for state in screen["states"]}
    for item in screen["state_applicability"]:
        item["mode"] = "required" if item["kind"] in required_kinds else "not_applicable"
        item["reason_ref"] = None if item["mode"] == "required" else (
            f"{source_ref}: {item['kind']} is not required by auth_flow for {route}"
        )
    screen["responsive_content_priorities"] = [
        "preserve route identity, task fields, primary action, safe feedback, and return/recovery navigation across the supported Web range"
    ]


def build(root: Path) -> dict[str, Any]:
    program_dir = root / ".codex/delivery/ui-design-programs/custometry-v2"
    old_artifacts = program_dir / "artifacts/g0-r3"
    artifacts = program_dir / "artifacts/g0-r4"
    evidence = program_dir / "evidence/g0-r4"
    artifacts.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    inventory_source = old_artifacts / "ui-standard-source-inventory.json"
    inventory_path = artifacts / "ui-standard-source-inventory.json"
    shutil.copyfile(inventory_source, inventory_path)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    observations = inventory["observations"]

    baseline = json.loads((old_artifacts / "platform-ui-baseline.json").read_text(encoding="utf-8"))
    baseline.update({
        "baseline_id": "custometry.platform-baseline.v3.metadata.r4",
        "revision": 4,
        "status": "draft",
        "unresolved_inputs": [],
    })
    candidate_ref = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/ru/source.html"
    candidate_path = root / candidate_ref
    candidate_hash = file_sha256(candidate_path)
    decision_ref = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/visual-authority-decision-r4.json"
    baseline["source_visual"].update({
        "path": candidate_ref,
        "sha256": candidate_hash,
        "owner_decision_ref": decision_ref,
    })

    groups: dict[str, dict[str, Any]] = {}
    for observation in observations:
        if observation["reuse_expectation"] != "reusable_required":
            continue
        group_material = {
            "domain": observation["domain"],
            "property": observation["property"],
            "value": observation["value"],
            "unit": observation.get("unit"),
        }
        key = canonical_sha256(group_material)
        group = groups.setdefault(key, {**group_material, "source_ids": [], "selectors": {}})
        group["source_ids"].append(observation["observation_id"])
        group["selectors"][selector_key(observation["identity"])] = observation["identity"]

    generated_tokens: dict[str, list[dict[str, Any]]] = {
        key: [] for key in baseline["foundation_tokens"]
    }
    clauses = []
    for key, group in sorted(groups.items(), key=lambda item: (item[1]["domain"], item[1]["property"], item[0])):
        category = DOMAIN_CATEGORY[group["domain"]]
        token_index = len(generated_tokens[category])
        slug = re.sub(r"[^a-z0-9]+", "-", group["property"].lower()).strip("-") or "value"
        clause_id = f"standard.{group['domain']}.{slug}.{key[:12]}"
        source_ids = sorted(group["source_ids"])
        source_ref = next(
            observation["source_ref"] for observation in observations
            if observation["observation_id"] == source_ids[0]
        )
        generated_tokens[category].append({
            "token_id": clause_id,
            "value": specified(group["value"], group["unit"], source_ref),
            "usage": f"Exact pilot-standard representation for {group['domain']} {group['property']}",
        })
        clauses.append({
            "clause_id": clause_id,
            "domain": group["domain"],
            "property": group["property"],
            "value": group["value"],
            "unit": group["unit"],
            "tolerance": 0,
            "source_observation_ids": source_ids,
            "baseline_paths": [f"/foundation_tokens/{pointer_token(category)}/{token_index}/value"],
            "applicability": [group["selectors"][selector] for selector in sorted(group["selectors"])],
            "change_policy": "fixed",
        })
    for category, tokens in generated_tokens.items():
        if tokens:
            baseline["foundation_tokens"][category] = tokens
        else:
            baseline["foundation_tokens"][category] = baseline["foundation_tokens"][category][:1]
    clauses.sort(key=lambda row: row["clause_id"])
    dispositions = [{
        "observation_id": observation["observation_id"],
        "disposition": "source_backed_not_reusable",
        "reason_ref": observation["source_ref"] + "&disposition=explicit-non-reusable-visible-node",
    } for observation in observations if observation["reuse_expectation"] == "disposition_required"]
    dispositions.sort(key=lambda row: row["observation_id"])
    baseline["standard_contract"] = {
        "standard_revision_id": "custometry.pilot-standard.v3.metadata.r4",
        "source_inventory": {
            "inventory_id": inventory["inventory_id"],
            "revision": inventory["revision"],
            "path": str(inventory_path.relative_to(root)),
            "sha256": file_sha256(inventory_path),
        },
        "clause_inventory_sha256": canonical_sha256(clauses),
        "clauses": clauses,
        "source_dispositions": dispositions,
        "applicability_policy": {
            "derivation": "deterministic_exact_identity_match",
            "clause_dispositions": ["conforms", "accepted_exception", "source_backed_not_applicable"],
            "exception_policy": "typed_narrow_source_bound_owner_acceptance",
            "delegated_design_boundary": "screen_specific_composition_only",
        },
    }
    baseline_path = artifacts / "platform-ui-baseline.json"
    write_json(baseline_path, baseline)

    intake = json.loads((old_artifacts / "ui-program-intake.json").read_text(encoding="utf-8"))
    intake.update({"revision": 4, "status": "draft", "unresolved_inputs": []})
    intake["baseline_contract"] = {
        "baseline_id": baseline["baseline_id"],
        "path": str(baseline_path.relative_to(root)),
        "sha256": file_sha256(baseline_path),
    }
    intake["pilot"].update({
        "source_visual_ref": candidate_ref,
        "source_visual_sha256": candidate_hash,
        "owner_decision_ref": decision_ref,
    })
    for screen in intake["screens"]:
        if screen["screen_id"] == "UI-AUTH-001":
            rebuild_auth_screen(screen, recovery=False)
        elif screen["screen_id"] == "UI-AUTH-004":
            rebuild_auth_screen(screen, recovery=True)
    intake_path = artifacts / "ui-program-intake.json"
    write_json(intake_path, intake)

    manifest = {
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4",
        "candidate": {"path": candidate_ref, "sha256": candidate_hash},
        "historical_source": {
            "path": ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2/ru/source.html",
            "sha256": "d5639f0e20a79581972853979cd643ca456b6235c1ce098f5adc98d89636ca15",
        },
        "baseline": {"path": str(baseline_path.relative_to(root)), "sha256": file_sha256(baseline_path)},
        "intake": {"path": str(intake_path.relative_to(root)), "sha256": file_sha256(intake_path)},
        "source_inventory": {"path": str(inventory_path.relative_to(root)), "sha256": file_sha256(inventory_path)},
        "counts": {
            "visible_nodes": len(inventory["visible_nodes"]),
            "observations": len(observations),
            "reusable_observations": sum(o["reuse_expectation"] == "reusable_required" for o in observations),
            "source_dispositions": len(dispositions),
            "standard_clauses": len(clauses),
        },
        "auth_boundary": {
            "sign_in": {"screen_id": "UI-AUTH-001", "route": "/auth/sign-in", "state_ids": [s["state_id"] for s in next(x for x in intake["screens"] if x["screen_id"] == "UI-AUTH-001")["states"]]},
            "recovery": {"screen_id": "UI-AUTH-004", "route": "/auth/recovery", "state_ids": [s["state_id"] for s in next(x for x in intake["screens"] if x["screen_id"] == "UI-AUTH-004")["states"]]},
        },
        "equivalence": "six browser states/anchors exact; zero differing pixels; metadata-only DOM difference",
        "owner_acceptance": "pending",
    }
    manifest_path = evidence / "g0-review-manifest.json"
    write_json(manifest_path, manifest)
    source_image = "../pilot-candidate-v3-metadata/equivalence/source-web-1440-ru-default.png"
    domain_labels = {
        "typography": "Типографика",
        "color": "Палитра",
        "spacing": "Отступы",
        "sizing": "Размеры",
        "radius": "Скругления",
        "border": "Границы",
        "elevation": "Тени",
        "focus": "Фокус",
        "motion": "Движение",
        "responsive": "Переполнение",
        "layout": "Компоновка",
        "opacity": "Прозрачность",
    }
    domain_counts = Counter(clause["domain"] for clause in clauses)
    def rules_label(count: int) -> str:
        if count % 10 == 1 and count % 100 != 11:
            noun = "правило"
        elif count % 10 in {2, 3, 4} and count % 100 not in {12, 13, 14}:
            noun = "правила"
        else:
            noun = "правил"
        return f"{count} {noun}"

    domain_chips = "".join(
        f'<li><strong>{html.escape(domain_labels.get(domain, domain))}</strong><span>{rules_label(count)}</span></li>'
        for domain, count in sorted(domain_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    clause_rows = "".join(
        "<tr>"
        f'<td><code>{html.escape(clause["clause_id"])}</code></td>'
        f'<td>{html.escape(domain_labels.get(clause["domain"], clause["domain"]))}</td>'
        f'<td><code>{html.escape(clause["property"])}</code></td>'
        f'<td><code>{html.escape(str(clause["value"]))}</code></td>'
        f'<td>{len(clause["source_observation_ids"])}</td>'
        f'<td>{len(clause["applicability"])}</td>'
        "</tr>"
        for clause in clauses
    )
    board_path = evidence / "g0-review-board.html"
    board_path.write_text(f"""<!doctype html>
<html lang="ru" data-ui-artifact="review_board" data-program-id="CUSTOMETRY-UI-DESIGN-PROGRAM-V2" data-artifact-id="g0-r4-baseline-board" data-revision="4" data-validation-profile="baseline_review_ready">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry G0 r4 — baseline review</title>
<style>
:root{{--ink:#151719;--muted:#5c6470;--line:#d9dde3;--paper:#fff;--bg:#f4f5f7;--accent:#1663d8;--ok:#087a4b;--info:#eaf2ff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,Arial,sans-serif}}main{{max-width:1180px;margin:auto;padding:28px}}h1{{font-size:30px;line-height:1.2;margin:0 0 8px}}h2{{font-size:20px;line-height:1.3;margin:0 0 10px}}h3{{font-size:16px;margin:0 0 7px}}p{{margin:0 0 12px}}.lede{{font-size:18px;max-width:840px;color:#303640}}.eyebrow{{font-weight:750;color:var(--accent);letter-spacing:.04em;text-transform:uppercase;font-size:12px}}.card{{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:20px;box-shadow:0 2px 10px #0000000a}}.hero{{margin:20px 0;border-left:5px solid var(--accent)}}.decision{{background:var(--info);border-color:#b7cff7}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:18px 0}}.three{{grid-template-columns:repeat(3,1fr)}}.stack{{display:grid;gap:16px}}img{{width:100%;border:1px solid var(--line);border-radius:10px;display:block}}.image-label{{color:var(--muted);margin-bottom:9px}}.zero{{display:inline-flex;gap:8px;align-items:center;color:var(--ok);font-weight:750;background:#eaf8f1;border-radius:999px;padding:6px 10px;margin-top:12px}}.zero::before{{content:'✓';font-size:16px}}ul{{padding-left:20px;margin:8px 0}}li+li{{margin-top:7px}}.rule-groups{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}.rule-groups li{{border:1px solid var(--line);border-radius:10px;padding:10px;margin:0;display:flex;flex-direction:column}}.rule-groups span{{color:var(--muted);font-size:13px}}code{{background:#eef1f4;padding:2px 5px;border-radius:5px;overflow-wrap:anywhere}}.route{{display:grid;grid-template-columns:145px 1fr;gap:8px;margin:10px 0}}.route strong{{font-weight:750}}.route span{{color:var(--muted)}}details{{margin-top:16px}}summary{{cursor:pointer;font-weight:750;color:var(--accent);padding:8px 0}}.table-wrap{{overflow:auto;max-height:560px;border:1px solid var(--line);border-radius:10px}}table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}}th{{position:sticky;top:0;background:#eef1f4;z-index:1}}.choices{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}}.choice{{background:white;border:1px solid #9dbced;border-radius:10px;padding:14px}}.choice strong{{display:block;font-size:16px;margin-bottom:3px}}.choice span{{color:var(--muted)}}.meta{{color:var(--muted);font-size:13px}}@media(max-width:900px){{.three,.rule-groups{{grid-template-columns:1fr 1fr}}}}@media(max-width:700px){{main{{padding:18px}}.grid,.three,.choices,.rule-groups{{grid-template-columns:1fr}}.route{{grid-template-columns:1fr}}h1{{font-size:25px}}}}
</style></head>
<body><main>
<p class="eyebrow">Контрольная точка G0 · правила визуального наследования</p>
<h1>Каждый элемент с соответствующим образцом в пилоте наследует его правила полностью</h1>
<p class="lede">Принятый пилот — обязательный источник визуальных правил. Если в нём есть соответствующий образец элемента, будущий интерфейс получает весь применимый набор его правил, а не выбранные отдельные свойства.</p>

<section class="card hero decision" data-review-entry="decision-scope">
<h2>Какое решение требуется</h2>
<p><strong>Подтвердить обязательное полное наследование визуальных правил из ранее принятого пилота.</strong> Точное семантическое совпадение выбирает набор применимых правил; после этого нельзя взять только удобные цвета, размеры или скругления и проигнорировать остальные правила этого элемента.</p>
<p class="meta">Причина контрольной точки: прежнее решение закрепило визуальное направление v2. Текущая редакция впервые делает полное наследование проверяемым для каждого элемента и исправляет границу auth-маршрутов по действующему контракту 2.0.0.</p>
</section>

<div class="grid three" data-review-entry="decision-boundary">
<section class="card"><h2>Уже было принято</h2><ul><li>Визуальный язык пилота v2.</li><li>Его палитра, типографика, плотность, компоненты, состояния и responsive Web.</li><li>Пилот остаётся визуальным авторитетом программы.</li></ul></section>
<section class="card"><h2>Что фиксируется сейчас</h2><ul><li>Каждый элемент с образцом в пилоте наследует весь применимый набор правил.</li><li>Частичное наследование и эстетическое приближение запрещены.</li><li>Отклонение возможно только как узкое явно принятое исключение.</li></ul></section>
<section class="card"><h2>Что вы сейчас не принимаете</h2><ul><li>Внешний вид будущих экранов входа и восстановления.</li><li>Их конкретную композицию, тексты или данные.</li><li>Production-код, публикацию, deployment или mobile UI.</li></ul></section>
</div>

<section class="card" data-review-entry="inheritance-model">
<h2>Как работает полное наследование</h2>
<div class="grid three"><div><h3>1. Определить элемент</h3><p>Тип компонента, вариант, размер, состояние, slot и роль в shell сопоставляются с пилотом.</p></div><div><h3>2. Получить весь набор</h3><p>Для найденной идентичности собираются все применимые правила: не отдельная категория, а полный визуальный контракт элемента.</p></div><div><h3>3. Проверить результат</h3><p>Будущий элемент должен подтвердить весь набор. Пропущенное правило, подмена или приблизительное значение означают несоответствие.</p></div></div>
<p><strong>Пример:</strong> если будущая кнопка совпала с вариантом кнопки пилота, она наследует одновременно типографику, цвета, размеры, внутренние отступы, границу, скругление, тень, иконку, состояния, focus, motion и responsive-поведение, которые пилот фиксирует для этого варианта.</p>
</section>

<section class="card" style="margin-top:18px" data-review-entry="pilot-authority">
<h2>Принятый пилот — источник правил</h2>
<img src="{html.escape(source_image)}" alt="Ранее принятый пилот Custometry">
<p class="meta" style="margin-top:12px">Отдельная техническая редакция добавляет только невидимые идентификаторы, чтобы правила можно было сопоставлять с элементами однозначно. Она не меняет визуальный язык пилота и не создаёт новый дизайн.</p>
</section>

<section class="card" style="margin-top:18px" data-review-entry="standard-summary">
<h2>Что именно фиксирует стандарт</h2>
<p>Правила извлечены из пилота, а не придуманы для будущих экранов. Точное семантическое совпадение определяет, какой полный набор относится к элементу. Оно не разрешает выбирать внутри этого набора только часть свойств.</p>
<ul class="rule-groups">{domain_chips}</ul>
<p><strong>Полный набор для элемента может включать:</strong> типографику, палитру, размеры, интервалы, скругления, границы, тени, прозрачность, иконки, состояния, focus, motion, shell/layout и responsive-поведение.</p>
<p><strong>Responsive Web:</strong> 768–1920 CSS px с контрольными точками 768, 1024, 1440 и 1920; при 200% zoom сохраняются смысл и управление. Mobile-specific UI не утверждается.</p>
<details><summary>Посмотреть все {manifest['counts']['standard_clauses']} правил</summary><div class="table-wrap"><table><thead><tr><th>ID правила</th><th>Область</th><th>Свойство</th><th>Значение</th><th>Наблюдений</th><th>Точных применений</th></tr></thead><tbody>{clause_rows}</tbody></table></div></details>
</section>

<section class="card" style="margin-top:18px" data-review-entry="auth-boundary">
<h2>Граница auth исправлена по продуктовым источникам</h2>
<div class="route"><strong><code>UI-AUTH-001</code></strong><div><code>/auth/sign-in</code><br><span>Компактный экран входа: credentials, remember me, language и переход в отдельное восстановление.</span></div></div>
<div class="route"><strong><code>UI-AUTH-004</code></strong><div><code>/auth/recovery</code><br><span>Отдельный пошаговый flow: проверка выданного reset token, новый пароль и возврат ко входу.</span></div></div>
<p class="meta">Это исправляет прежнюю ошибку <code>UI-AUTH-001.recovery</code>. Внешний вид этих двух экранов будет показан отдельно на G4; сейчас он не принимается.</p>
</section>

<section class="card hero decision" style="margin-top:18px" data-review-entry="owner-choice">
<h2>Ваш выбор</h2>
<p>Если пилот должен управлять каждым элементом, для которого в нём есть соответствующий образец, именно так — полным набором применимых правил — примите это правило наследования. Если нет, назовите конкретное ограниченное исправление.</p>
<div class="choices"><div class="choice"><strong>Принять полное наследование из пилота</strong><span>Разрешает закрыть G0 и перейти к инвентарю экранов. Это не принимает будущий UI.</span></div><div class="choice"><strong>Запросить ограниченные исправления</strong><span>Укажите, что неверно в полноте наследования, границе применимости или auth-маршрутах.</span></div></div>
</section>
</main></body></html>""", encoding="utf-8")
    packet = {
        "schema_id": "codex.ui-owner-review-packet/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4",
        "decision_kind": "visual_authority",
        "review_board": {"path": str(board_path.relative_to(root)), "sha256": file_sha256(board_path)},
        "manifest": {"path": str(manifest_path.relative_to(root)), "sha256": file_sha256(manifest_path)},
        "question": "Принять обязательное полное наследование из пилота: каждый элемент с соответствующим образцом в пилоте получает весь применимый набор визуальных правил без частичного выбора или эстетического приближения, либо запросить ограниченные исправления? Это решение не принимает будущие экраны или production-код.",
        "owner_acceptance": "pending",
    }
    packet_path = evidence / "g0-owner-decision-packet.json"
    write_json(packet_path, packet)
    return {"baseline": baseline_path, "intake": intake_path, "inventory": inventory_path, "board": board_path, "packet": packet_path, "manifest": manifest_path}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    outputs = build(args.project_root.resolve())
    print(json.dumps({key: str(path) for key, path in outputs.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
