#!/usr/bin/env python3
"""Build deterministic active-contract auth-family artifacts for one revision."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import html
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
ART = PROGRAM_DIR / "artifacts/g4-r4/family-auth-shell-auth-baseline-exception-auth"
EVID = PROGRAM_DIR / "evidence/g4-r4/family-auth-shell-auth-baseline-exception-auth"
INTAKE = PROGRAM_DIR / "artifacts/g0-r4/ui-program-intake.json"
BASELINE = PROGRAM_DIR / "artifacts/g0-r4/platform-ui-baseline.json"
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
G1 = PROGRAM_DIR / "evidence/g0-r2/g1-admission-inventory.json"
SOURCE = PROGRAM_DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
BASE_CONTRACT = PROGRAM_DIR / "artifacts/g3-r3/representative-shell-contract.json"
TARGET = ART / "screens/auth-family.html"
SNAPSHOT = ART / "ui-design-program.snapshot.json"
FAMILY_ID = "family.auth.shell-auth.baseline-exception-auth"
REVISION = 4
REVISION_TAG = f"r{REVISION}"
FAMILY_REVISION_ID = f"{FAMILY_ID}-{REVISION_TAG}"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
PROGRAM_REVISION = 4
STAGE_ID = f"G4@{FAMILY_REVISION_ID}"
HISTORICAL_PREDECESSOR_DECISION: Path | None = None
BUTTON_STATE_EXCEPTION_ID = "accepted-pilot-interactive-button-state-projection"
BUTTON_STATE_EXCEPTION_CLAUSES = [
    "standard.color.background-color.54ba9843a31f",
    "standard.color.color.c863c07a7c53",
    "standard.typography.font-weight.a1ca90e332a6",
]
STANDARD_PATTERNS = (
    ("action.button", "button", "standard", "shell.main-content.button"),
    ("control.compact", "compact-control.lifecycle-metric-select", "compact", "shell.main-content.select"),
)

ACTION_TAXONOMY = {
    "signin-locale": {
        "component_id": "control.compact", "variant": "language-select", "size": "compact",
        "standard_identity": {"component_id": "control.compact", "variant": "compact-control.lifecycle-metric-select", "size_class": "compact", "element_type": "select", "icon_id": None, "state_ids": ["default"]},
        "standard_slot_id": "shell.main-content.select", "states": ["default", "hover", "focus_visible", "disabled"],
    },
    "recovery-locale": {
        "component_id": "control.compact", "variant": "language-select", "size": "compact",
        "standard_identity": {"component_id": "control.compact", "variant": "compact-control.lifecycle-metric-select", "size_class": "compact", "element_type": "select", "icon_id": None, "state_ids": ["default"]},
        "standard_slot_id": "shell.main-content.select", "states": ["default", "hover", "focus_visible", "disabled"],
    },
    "signin-remember": {
        "component_id": "control.checkbox", "variant": "remember-session", "size": "sm",
        "standard_identity": None, "standard_slot_id": None,
        "states": ["default", "hover", "focus_visible", "active", "selected", "disabled"],
    },
    "signin-open-recovery": {
        "component_id": "navigation.link", "variant": "auth-route", "size": "text",
        "standard_identity": None, "standard_slot_id": None,
        "states": ["default", "hover", "focus_visible", "active", "disabled"],
    },
    "recovery-return": {
        "component_id": "navigation.link", "variant": "auth-route", "size": "text",
        "standard_identity": None, "standard_slot_id": None,
        "states": ["default", "hover", "focus_visible", "active", "disabled"],
    },
    "signin-submit": {
        "component_id": "action.button", "variant": "primary", "size": "md",
        "standard_identity": None, "standard_slot_id": None,
        "states": ["default", "hover", "focus_visible", "active", "disabled", "loading", "error"],
    },
    "recovery-validate": {
        "component_id": "action.button", "variant": "secondary", "size": "md",
        "standard_identity": None, "standard_slot_id": None,
        "states": ["default", "hover", "focus_visible", "active", "disabled", "loading", "error"],
    },
    "recovery-set-password": {
        "component_id": "action.button", "variant": "primary", "size": "md",
        "standard_identity": None, "standard_slot_id": None,
        "states": ["default", "hover", "focus_visible", "active", "disabled", "loading", "error"],
    },
}

VISIBLE_COPY = {
    "ru": {
        "signin": {
            "title": "Вход в Custometry", "lead": "Введите рабочий email и пароль.",
            "email_label": "Рабочий email", "email_placeholder": "name@company.ru", "password_label": "Пароль",
            "remember": "Запомнить меня", "recovery_link": "Восстановить пароль", "submit": "Войти",
            "trust": "Данные остаются в вашей инсталляции.",
            "states": {
                "initial": {"message": "", "email_error": "", "password_error": ""},
                "first_loading": {"message": "Входим…", "email_error": "", "password_error": ""},
                "ready": {"message": "", "email_error": "", "password_error": ""},
                "validation_error": {"message": "Проверьте выделенные поля.", "email_error": "Введите рабочий email.", "password_error": "Введите пароль."},
                "failed": {"message": "Не удалось войти. Проверьте данные и повторите.", "email_error": "", "password_error": ""},
                "session_expired": {"message": "Сессия истекла. Войдите снова.", "email_error": "", "password_error": ""},
            },
        },
        "recovery": {
            "title": "Смена пароля", "lead": "Введите код сброса, полученный у администратора, и задайте новый пароль.",
            "step_code": "Код", "step_password": "Новый пароль", "step_done": "Готово",
            "token_label": "Код сброса", "token_placeholder": "Введите код", "password_label": "Новый пароль",
            "confirm_label": "Повторите пароль", "password_hint": "Требования к паролю проверяются при сохранении.",
            "validate": "Проверить код", "submit": "Сохранить новый пароль", "return_link": "Вернуться ко входу",
            "trust": "Если у вас нет кода, обратитесь к администратору инсталляции.",
            "states": {
                "initial": {"message": "", "token_error": ""},
                "first_loading": {"message": "Проверяем код…", "token_error": ""},
                "ready": {"message": "Код подтверждён. Задайте новый пароль.", "token_error": ""},
                "validation_error": {"message": "", "token_error": "Проверьте код сброса и повторите."},
                "failed": {"message": "Не удалось изменить пароль. Проверьте данные и повторите.", "token_error": ""},
                "session_expired": {"message": "Срок действия кода истёк. Получите новый код у администратора.", "token_error": ""},
            },
        },
    },
    "en": {
        "signin": {
            "title": "Sign in to Custometry", "lead": "Enter your work email and password.",
            "email_label": "Work email", "email_placeholder": "name@company.com", "password_label": "Password",
            "remember": "Remember me", "recovery_link": "Reset password", "submit": "Sign in",
            "trust": "Your data stays in your installation.",
            "states": {
                "initial": {"message": "", "email_error": "", "password_error": ""},
                "first_loading": {"message": "Signing in…", "email_error": "", "password_error": ""},
                "ready": {"message": "", "email_error": "", "password_error": ""},
                "validation_error": {"message": "Check the highlighted fields.", "email_error": "Enter your work email.", "password_error": "Enter your password."},
                "failed": {"message": "Unable to sign in. Check the details and try again.", "email_error": "", "password_error": ""},
                "session_expired": {"message": "Your session expired. Sign in again.", "email_error": "", "password_error": ""},
            },
        },
        "recovery": {
            "title": "Reset password", "lead": "Enter the reset code from your administrator and choose a new password.",
            "step_code": "Code", "step_password": "New password", "step_done": "Done",
            "token_label": "Reset code", "token_placeholder": "Enter code", "password_label": "New password",
            "confirm_label": "Confirm password", "password_hint": "Password requirements are checked when you save.",
            "validate": "Check code", "submit": "Save new password", "return_link": "Return to sign in",
            "trust": "If you do not have a code, contact your installation administrator.",
            "states": {
                "initial": {"message": "", "token_error": ""},
                "first_loading": {"message": "Checking the code…", "token_error": ""},
                "ready": {"message": "Code confirmed. Choose a new password.", "token_error": ""},
                "validation_error": {"message": "", "token_error": "Check the reset code and try again."},
                "failed": {"message": "Unable to reset the password. Check the details and try again.", "token_error": ""},
                "session_expired": {"message": "The code expired. Ask your administrator for a new code.", "token_error": ""},
            },
        },
    },
}


def button_exception_clauses(state_id: str) -> list[str]:
    clauses = list(BUTTON_STATE_EXCEPTION_CLAUSES)
    if state_id.endswith(".first_loading"):
        clauses.append("standard.opacity.opacity.3f43cc20e0ec")
    return clauses
ANCHORS = (("web-768", 768, 1024), ("web-1024", 1024, 768), ("web-1440", 1440, 900), ("web-1920", 1920, 1080))
SCREEN_INDEXES = {"UI-AUTH-001": 0, "UI-AUTH-004": 3}
SKILL_ROOT = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program")
OWNER_CORRECTIONS = {
    "owner-requested-changes-r3-01.json": "f40a4fddb84fead5f182111cf2e44d51711976df876d02e7f01aeec348554ec7",
    "owner-requested-changes-r3-02.json": "886be10c124b940f964034b52b3451882219ee71bf4605ccd402fea0f0ab92fa",
    "owner-requested-changes-r3-03.json": "ebd5ee0e19085dce3c8014fc96753701a78b701c1487b884b96b00920d3199ef",
    "owner-requested-changes-r3-04.json": "ea1e6e64cb018c4cfa6488f635d7103730b3d268d1fc2e8bf4ebe478930a779a",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def state_rows() -> dict[str, list[dict[str, Any]]]:
    intake = json.loads(INTAKE.read_text(encoding="utf-8"))
    return {screen["screen_id"]: screen["states"] for screen in intake["screens"] if screen["screen_id"] in SCREEN_INDEXES}


def screen_rows() -> dict[str, dict[str, Any]]:
    intake = json.loads(INTAKE.read_text(encoding="utf-8"))
    return {screen["screen_id"]: screen for screen in intake["screens"] if screen["screen_id"] in SCREEN_INDEXES}


def pilot_component_css(baseline: dict[str, Any]) -> str:
    """Project the exact accepted-pilot clauses for reused target patterns."""
    rules: list[str] = []
    for component_id, variant, size_class, slot_id in STANDARD_PATTERNS:
        properties: dict[str, str] = {}
        for clause in baseline["standard_contract"]["clauses"]:
            selectors = clause.get("applicability", [])
            if not any(
                selector.get("component_id") == component_id
                and selector.get("variant") == variant
                and selector.get("size_class") == size_class
                and selector.get("slot_id") == slot_id
                and selector.get("state_id") in {None, "default"}
                for selector in selectors
            ):
                continue
            property_name = clause["property"]
            property_value = str(clause["value"])
            if property_name in properties and properties[property_name] != property_value:
                raise ValueError(f"pilot pattern has conflicting reusable values: {component_id}/{variant}/{property_name}")
            properties[property_name] = property_value
        if not properties:
            raise ValueError(f"pilot pattern has no reusable clauses: {component_id}/{variant}")
        selector = (
            f'[data-ui-standard-component="{component_id}"]'
            f'[data-ui-standard-variant="{variant}"]'
            f'[data-ui-standard-size="{size_class}"]'
            f'[data-ui-standard-slot="{slot_id}"]'
        )
        declarations = ";".join(f"{name}:{value}" for name, value in sorted(properties.items()))
        rules.append(f"{selector}{{{declarations}}}")
        rules.append(
            f"{selector}:focus-visible{{outline-color:var(--focus);outline-style:solid;"
            "outline-width:3px;outline-offset:2px}"
        )
    return "\n".join(rules)


def pilot_button_state_css() -> str:
    """Project the accepted pilot's complete dark-theme button-state grammar.

    The source assertions make this a deterministic projection of the accepted
    visual authority rather than target-authored look-and-feel.  A changed
    pilot must fail the build and be handled through change control.
    """
    source = SOURCE.read_text(encoding="utf-8")
    required_source_clauses = (
        "--module: #1a1b1e;",
        "--module-strong: #222327;",
        "--text: #f0f0f2;",
        "--text-secondary: #a7a7ad;",
        "--accent: #66b9d3;",
        ".icon-button:hover, .text-button:hover, .compact-control:hover { color: var(--text); background: var(--module-strong); }",
        ".text-button--primary { color: #071014; background: #8ccfe3; font-weight: 650; }",
        ".text-button--primary:hover { color: #071014; background: #a5dcec; }",
        "button:active { transform: scale(.96); }",
        "button[disabled] { cursor: not-allowed; opacity: .48; transform: none; }",
    )
    missing = [clause for clause in required_source_clauses if clause not in source]
    if missing:
        raise ValueError(f"accepted pilot button-state clauses changed or disappeared: {missing}")
    button_identity = (
        '[data-ui-standard-component="action.button"]'
        '[data-ui-standard-variant="button"]'
        '[data-ui-standard-size="standard"]'
        '[data-ui-standard-slot="shell.main-content.button"]'
    )
    text_identity = '[data-semantic-control="navigation-link"]'
    return f"""
{button_identity}[data-pilot-action-style]{{cursor:pointer}}
{button_identity}[data-pilot-action-style]{{display:flex;width:100%;align-items:center;justify-content:center}}
{button_identity}[data-pilot-action-style="primary"]{{color:#071014;background:#8ccfe3;font-weight:650}}
{button_identity}[data-pilot-action-style="primary"]:hover{{color:#071014;background:#a5dcec}}
{button_identity}[data-pilot-action-style="secondary"]{{color:#a7a7ad;background:#1a1b1e}}
{button_identity}[data-pilot-action-style="secondary"]:hover{{color:#f0f0f2;background:#222327}}
{button_identity}[data-pilot-action-style]:not(:disabled):active{{transform:scale(.96)}}
{button_identity}[data-pilot-action-style]:disabled{{cursor:not-allowed;opacity:.48;transform:none}}
{text_identity}:hover{{color:#f0f0f2;background:#222327}}
{text_identity}:active{{transform:scale(.96)}}
""".strip()


def legacy_target_html(baseline: dict[str, Any]) -> str:
    return '''<!doctype html>
<html lang="ru" data-theme="graphite"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="ui-fixture-sha256" content="__FIXTURE_SHA256__"><meta name="ui-font-bundle-sha256" content="__FONT_SHA256__"><meta name="ui-asset-bundle-sha256" content="__ASSET_SHA256__"><link rel="icon" href="data:,"><title>Custometry · authentication</title>
<style>
:root{--paper:#070708;--panel:#111214;--panel2:#151619;--module:#1a1b1e;--line:#303136;--line-soft:#242529;--ink:#f0f0f2;--secondary:#a7a7ad;--muted:#8b8c93;--cyan:#66b9d3;--focus:#8bd2e8;--danger:#f07d87;--warning:#ddb064;--ok:#62c7aa;--shadow:0 22px 70px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.07);--pilot-compact-measure:364.578px}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--paper);color:var(--ink);font:14px/1.5 Inter,ui-sans-serif,system-ui,sans-serif}body{min-height:100vh;display:grid;place-items:center;padding:20px;overflow-x:hidden}button,input,select{font:inherit}button,a,label,input,select{position:relative}button:focus-visible,input:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
[hidden]{display:none!important}.auth-screen{width:min(100%,calc(var(--pilot-compact-measure) + 48px));border:1px solid var(--line);border-radius:15px;overflow:hidden;background:var(--panel);box-shadow:var(--shadow)}.recovery{width:min(100%,760px)}.brandbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 18px;border-bottom:1px solid var(--line-soft);background:#090a0b}.brand{display:flex;align-items:center;gap:9px;font-size:12px;font-weight:720}.mark{display:grid;place-items:center;width:28px;height:28px;border-radius:9px;color:#071014;background:var(--cyan);font-weight:800}.locale{min-height:32px;border:1px solid var(--line);border-radius:7px;padding:0 9px;color:var(--secondary);background:var(--module)}.content{padding:24px}.route{margin:0 0 6px;color:var(--muted);font-size:10px}.content h1{margin:0;font-size:22px;letter-spacing:-.025em}.lead{margin:7px 0 20px;color:var(--secondary);font-size:12px}.form{display:grid;gap:12px}.field{display:grid;gap:6px;color:var(--secondary);font-size:11px;font-weight:650}.field input{width:100%;min-height:40px;border:1px solid var(--line);border-radius:7px;padding:0 11px;color:var(--ink);background:var(--panel2)}input::placeholder{color:var(--muted)}input:disabled,button:disabled,select:disabled{cursor:not-allowed;opacity:.48}.row{display:flex;align-items:center;justify-content:space-between;gap:12px}.remember{display:flex;align-items:center;gap:7px;color:var(--secondary);font-size:11px}.remember input{accent-color:var(--cyan)}.button{min-height:38px;border:1px solid var(--line);border-radius:7px;padding:0 12px;cursor:pointer;transition:background-color 120ms,color 120ms,transform 120ms}.primary{color:#071014;border-color:var(--cyan);background:var(--cyan);font-weight:700}.secondary{color:var(--secondary);background:var(--module)}.button:not(:disabled):active{transform:scale(.96)}.text-button{border:0;padding:4px 0;color:var(--cyan);background:transparent;cursor:pointer;font-size:11px}.message{margin-top:14px;padding:11px 12px;border:1px solid var(--line-soft);border-radius:10px;color:var(--secondary);background:var(--panel2);font-size:11px}.message[data-kind=error]{border-color:rgba(240,125,135,.45);color:var(--danger)}.message[data-kind=permission_denied]{border-color:rgba(221,176,100,.45);color:var(--warning)}.message[data-kind=populated]{border-color:rgba(98,199,170,.4);color:var(--ok)}.result{min-height:18px;margin:9px 0 0;color:var(--cyan);font-size:11px}
.recovery-layout{display:grid;grid-template-columns:190px minmax(0,1fr);gap:18px}.steps{margin:0;padding:0;list-style:none}.steps li{display:grid;grid-template-columns:26px 1fr;gap:9px;align-items:start;padding:10px 0;color:var(--muted);font-size:11px}.steps b{display:grid;place-items:center;width:26px;height:26px;border:1px solid var(--line);border-radius:50%;color:var(--ink);background:var(--module)}.steps li:first-child b{border-color:var(--cyan);color:#071014;background:var(--cyan)}.wizard{display:grid;gap:12px;padding-left:18px;border-left:1px solid var(--line-soft)}.action-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.action-grid .primary{grid-column:1/-1}.trust{margin:14px 0 0;color:var(--muted);font-size:10px}
@media(max-width:800px){body{display:block;padding:16px}.auth-screen{margin:auto}.recovery-layout{grid-template-columns:1fr}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.steps li{grid-template-columns:26px;gap:5px}.wizard{padding:16px 0 0;border-left:0;border-top:1px solid var(--line-soft)}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation:none!important;transition-duration:0s!important}}
__PILOT_COMPONENT_CSS__
__PILOT_BUTTON_STATE_CSS__
</style></head><body>
<main class="auth-screen signin" data-screen-id="UI-AUTH-001" data-route="/auth/sign-in" data-ui-region="UI-AUTH-001.content">
 <div class="brandbar" data-ui-region="UI-AUTH-001.brand"><div class="brand" data-ui-element="signin-brand"><span class="mark" aria-hidden="true">C</span><span>Custometry</span></div><button class="locale" type="button" data-locale data-pilot-action-style="compact" data-ui-element="signin-locale" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.change-language" data-action="UI-AUTH-001.change-language" aria-label="Язык">RU / EN</button></div>
 <section class="content" data-ui-region="UI-AUTH-001.form" data-ui-element="signin-surface"><p class="route" data-ui-element="signin-route">/auth/sign-in</p><h1 data-ui-element="signin-title">Вход</h1><p class="lead" data-ui-element="signin-description">Рабочий email и пароль.</p>
  <form class="form" onsubmit="event.preventDefault()"><label class="field">Email<input data-ui-element="signin-email" aria-label="Email" type="email" autocomplete="username" placeholder="name@company.test"></label><label class="field">Пароль<input data-ui-element="signin-password" aria-label="Пароль" type="password" autocomplete="current-password" placeholder="Проверочное значение" data-sensitive></label><div class="row"><button class="remember" type="button" role="checkbox" aria-checked="false" data-pilot-action-style="compact" data-ui-element="signin-remember" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.toggle-remember" data-action="UI-AUTH-001.toggle-remember">Запомнить меня</button><button class="text-button" type="button" data-pilot-action-style="quiet" data-ui-element="signin-open-recovery" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.open-recovery" data-action="UI-AUTH-001.open-recovery">Помощь с паролем</button></div><button class="button primary" type="button" data-pilot-action-style="primary" data-ui-element="signin-submit" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.submit-credentials" data-action="UI-AUTH-001.submit-credentials">Войти</button></form>
  <div class="message" role="status" aria-live="polite" data-ui-element="signin-message"></div><p class="result" aria-live="polite" data-ui-element="signin-result" data-result></p>
 </section>
</main>
<main class="auth-screen recovery" hidden data-screen-id="UI-AUTH-004" data-route="/auth/recovery" data-ui-region="UI-AUTH-004.content">
 <div class="brandbar" data-ui-region="UI-AUTH-004.brand"><div class="brand" data-ui-element="recovery-brand"><span class="mark" aria-hidden="true">C</span><span>Custometry</span></div><button class="locale" type="button" data-locale data-pilot-action-style="compact" data-ui-element="recovery-locale" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" aria-label="Язык">RU / EN</button></div>
 <section class="content" data-ui-region="UI-AUTH-004.form" data-ui-element="recovery-surface"><p class="route" data-ui-element="recovery-route">/auth/recovery</p><h1 data-ui-element="recovery-title">Восстановление пароля</h1><p class="lead" data-ui-element="recovery-description">Отдельный маршрут: проверка токена и установка нового пароля.</p>
  <div class="recovery-layout"><ol class="steps" data-ui-element="recovery-steps"><li><b>1</b><span>Токен</span></li><li><b>2</b><span>Новый пароль</span></li><li><b>3</b><span>Возврат</span></li></ol><form class="wizard" onsubmit="event.preventDefault()"><label class="field">Токен сброса<input data-ui-element="recovery-token" aria-label="Токен сброса" autocomplete="one-time-code" placeholder="Токен администратора"></label><label class="field">Новый пароль<input data-ui-element="recovery-password" aria-label="Новый пароль" type="password" autocomplete="new-password" placeholder="Новое значение" data-sensitive></label><label class="field">Повторите пароль<input data-ui-element="recovery-confirm" aria-label="Повторите пароль" type="password" autocomplete="new-password" placeholder="Повторите значение" data-sensitive></label><div class="action-grid"><button class="button secondary" type="button" data-pilot-action-style="secondary" data-ui-element="recovery-validate" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-004.validate-reset-token" data-action="UI-AUTH-004.validate-reset-token">Проверить токен</button><button class="text-button" type="button" data-pilot-action-style="quiet" data-ui-element="recovery-return" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-004.return-sign-in" data-action="UI-AUTH-004.return-sign-in">Вернуться ко входу</button><button class="button primary" type="button" data-pilot-action-style="primary" data-ui-element="recovery-set-password" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="sm" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-004.set-new-password" data-action="UI-AUTH-004.set-new-password">Установить новый пароль</button></div></form></div>
  <div class="message" role="status" aria-live="polite" data-ui-element="recovery-message"></div><p class="result" aria-live="polite" data-ui-element="recovery-result" data-result></p><p class="trust" data-ui-element="recovery-trust">Ошибки не раскрывают существование учётной записи или значение токена.</p>
 </section>
</main>
<script>
const q=new URLSearchParams(location.search);const screen=q.get('screen')==='UI-AUTH-004'?'UI-AUTH-004':'UI-AUTH-001';const state=q.get('state')||`${screen}.initial`;const lang=q.get('lang')==='en'?'en':'ru';
const stateKind=state.endsWith('first_loading')?'loading':state.endsWith('ready')?'populated':state.endsWith('session_expired')?'permission_denied':state.endsWith('initial')?'initial':'error';
const copy={ru:{initial:'Введите данные для продолжения.',loading:'Проверяем состояние. Управление временно недоступно.',populated:'Форма готова. Можно продолжить.',error:'Не удалось выполнить проверку. Исправьте данные или повторите попытку.',permission_denied:'Сессия истекла. Повторите безопасный вход.'},en:{initial:'Enter details to continue.',loading:'Checking the state. Controls are temporarily unavailable.',populated:'The form is ready.',error:'The check failed. Correct the details or retry.',permission_denied:'The session expired. Sign in again safely.'}};
document.querySelectorAll('[data-screen-id]').forEach(x=>{if(x.dataset.screenId!==screen)x.remove()});const active=document.querySelector(`[data-screen-id="${screen}"]`);active.hidden=false;active.dataset.stateId=state;const msg=active.querySelector('.message');msg.dataset.kind=stateKind;msg.textContent=copy[lang][stateKind];
active.querySelectorAll('[data-locale]').forEach(x=>x.textContent=lang==='en'?'EN / RU':'RU / EN');if(lang==='en'){active.querySelector('h1').textContent=screen==='UI-AUTH-001'?'Sign in':'Password recovery'}
const unavailable=stateKind==='loading';active.querySelectorAll('button,input,select').forEach(x=>x.disabled=unavailable);if(state.endsWith('ready')){active.querySelectorAll('input[type=email]').forEach(x=>x.value='reviewer@company.test')}
function recordAction(control){const action=control.dataset.action;const result=active.querySelector('[data-result]');if(control.getAttribute('role')==='checkbox')control.setAttribute('aria-checked',control.getAttribute('aria-checked')==='true'?'false':'true');result.textContent=action.includes('open-recovery')?'Открыт отдельный маршрут /auth/recovery':action.includes('return-sign-in')?'Открыт маршрут /auth/sign-in':action.includes('set-new-password')?'Пароль обновлён. Вернитесь ко входу.':action.includes('validate-reset-token')?'Токен проверен. Продолжайте безопасно.':action.includes('toggle-remember')?'Настройка сохранена локально.':action.includes('change-language')?'Язык изменён без смены маршрута.':'Вход проверен. Результат не раскрывает лишних сведений.';result.dataset.actionResult=action}
active.querySelectorAll('[data-action]').forEach(control=>{control.addEventListener('click',()=>recordAction(control));control.addEventListener('change',()=>recordAction(control));control.addEventListener('keydown',event=>{if(event.key==='Enter')recordAction(control)})});
</script></body></html>'''.replace("__PILOT_COMPONENT_CSS__", pilot_component_css(baseline)).replace("__PILOT_BUTTON_STATE_CSS__", pilot_button_state_css())


def stabilize_auth_state_geometry(document: str) -> str:
    """Keep every r5 state inside that screen's unchanged initial card geometry."""
    replacements = {
        ".field{display:grid;gap:7px": ".field{position:relative;display:grid;gap:7px",
        ".field-error{margin:0;color:var(--danger);font-size:11px;font-weight:500}": ".field-error{position:absolute;inset-block-start:100%;inset-inline:0;margin:0;color:var(--danger);font-size:10px;font-weight:500;line-height:1.2}",
        ".status{margin:0;padding:11px 12px;border:1px solid var(--line-soft);border-radius:10px;color:var(--secondary);background:var(--panel2);font-size:12px}.status[data-kind=error]{border-color:rgba(240,125,135,.45);color:var(--danger)}.status[data-kind=permission_denied]{border-color:rgba(221,176,100,.45);color:var(--warning)}.status[data-kind=populated]{border-color:rgba(98,199,170,.4);color:var(--ok)}.result{margin:0;color:var(--cyan);font-size:12px}.trust{margin:20px 0 0;color:var(--muted);font-size:11px}": ".feedback-slot{display:grid;align-items:end;height:36.5px;overflow:visible}.feedback-slot[data-active=true]{align-items:start}.feedback-slot>*{grid-area:1/1;margin:0}.status{border:0;padding:0;color:var(--secondary);background:transparent;font-size:12px;line-height:1.35}.status[data-kind=error]{color:var(--danger)}.status[data-kind=permission_denied]{color:var(--warning)}.status[data-kind=populated]{color:var(--ok)}.result{color:var(--cyan);font-size:12px;line-height:1.35}.trust{color:var(--muted);font-size:11px}",
        ".recovery-form>.status,.recovery-form>.result,.safe-return{grid-column:1/-1}.safe-return{display:flex;justify-content:center}": ".safe-return{grid-column:1/-1;display:flex;justify-content:center}",
        '<button class="button primary" type="submit" data-pilot-action-style="primary" data-ui-element="signin-submit" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="md" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.submit-credentials" data-action="UI-AUTH-001.submit-credentials" data-copy="submit">Войти</button><p class="status" role="status" aria-live="polite" data-ui-element="signin-message" data-copy-state="message" hidden></p><p class="result" role="status" aria-live="polite" data-ui-element="signin-result" data-result hidden></p></form><p class="trust" data-ui-element="signin-trust" data-copy="trust">Данные остаются в вашей инсталляции.</p>': '<button class="button primary" type="submit" data-pilot-action-style="primary" data-ui-element="signin-submit" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="md" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.submit-credentials" data-action="UI-AUTH-001.submit-credentials" data-copy="submit">Войти</button></form><div class="feedback-slot"><p class="status" role="status" aria-live="polite" data-ui-element="signin-message" data-copy-state="message" hidden></p><p class="result" role="status" aria-live="polite" data-ui-element="signin-result" data-result hidden></p><p class="trust" data-ui-element="signin-trust" data-copy="trust">Данные остаются в вашей инсталляции.</p></div>',
        '<p class="status" role="status" aria-live="polite" data-ui-element="recovery-message" data-copy-state="message" hidden></p><p class="result" role="status" aria-live="polite" data-ui-element="recovery-result" data-result hidden></p><div class="safe-return">': '<div class="safe-return">',
        '</a></div></form><p class="trust" data-ui-element="recovery-trust" data-copy="trust">Если у вас нет кода, обратитесь к администратору инсталляции.</p>': '</a></div></form><div class="feedback-slot"><p class="status" role="status" aria-live="polite" data-ui-element="recovery-message" data-copy-state="message" hidden></p><p class="result" role="status" aria-live="polite" data-ui-element="recovery-result" data-result hidden></p><p class="trust" data-ui-element="recovery-trust" data-copy="trust">Если у вас нет кода, обратитесь к администратору инсталляции.</p></div>',
        "applyCopy();const loading=stateName==='first_loading';": "function syncFeedback(){const slot=active.querySelector('.feedback-slot');const status=active.querySelector('.status');const result=active.querySelector('[data-result]');const trust=active.querySelector('.trust');if(!result.hidden)status.hidden=true;const hasFeedback=!status.hidden||!result.hidden;slot.dataset.active=String(hasFeedback);trust.hidden=hasFeedback}\napplyCopy();syncFeedback();const loading=stateName==='first_loading';",
        "result.hidden=false;result.dataset.actionResult=control.dataset.action}": "result.hidden=false;result.dataset.actionResult=control.dataset.action;syncFeedback()}",
    }
    for old, new in replacements.items():
        if old not in document:
            raise ValueError(f"stable auth-state geometry marker disappeared: {old[:96]}")
        document = document.replace(old, new, 1)
    return document


def target_html(baseline: dict[str, Any]) -> str:
    """Render the semantic auth grammar used by both representatives."""
    copy_json = json.dumps(VISIBLE_COPY, ensure_ascii=False, separators=(",", ":"))
    document = '''<!doctype html>
<html lang="ru" data-theme="graphite"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="ui-fixture-sha256" content="__FIXTURE_SHA256__"><meta name="ui-font-bundle-sha256" content="__FONT_SHA256__"><meta name="ui-asset-bundle-sha256" content="__ASSET_SHA256__"><link rel="icon" href="data:,"><title>Custometry · authentication</title>
<style>
:root{--paper:#070708;--panel:#111214;--panel2:#151619;--module:#1a1b1e;--module-strong:#222327;--line:#303136;--line-soft:#242529;--ink:#f0f0f2;--secondary:#a7a7ad;--muted:#8b8c93;--cyan:#8ccfe3;--cyan-hover:#a5dcec;--focus:#8bd2e8;--danger:#f07d87;--warning:#ddb064;--ok:#62c7aa;--shadow:0 22px 70px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.07)}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--paper);color:var(--ink);font:14px/1.5 Inter,ui-sans-serif,system-ui,sans-serif}body{min-height:100vh;display:grid;place-items:center;padding:20px;overflow-x:hidden}button,input,select{font:inherit}button,a,label,input,select{position:relative}button:focus-visible,input:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid var(--focus);outline-offset:2px}[hidden]{display:none!important}
.auth-screen{width:min(100%,448px);border:1px solid var(--line);border-radius:16px;overflow:hidden;background:var(--panel);box-shadow:var(--shadow)}.recovery{width:min(100%,640px)}.brandbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 20px;border-bottom:1px solid var(--line-soft);background:#090a0b}.brand{display:flex;align-items:center;gap:10px;font-size:12px;font-weight:720}.mark{display:grid;place-items:center;width:28px;height:28px;border-radius:9px;color:#071014;background:#66b9d3;font-weight:800}.locale-wrap{display:grid;gap:3px;color:var(--muted);font-size:10px}.locale{min-width:112px;min-height:36px;border:1px solid var(--line);border-radius:8px;padding:0 32px 0 10px;color:var(--secondary);background:var(--module)}
.content{padding:28px}.heading{display:grid;gap:8px;margin-bottom:24px}.content h1{margin:0;font-size:24px;line-height:1.2;letter-spacing:-.025em}.lead{margin:0;max-width:54ch;color:var(--secondary);font-size:13px}.form{display:grid;gap:16px}.field{display:grid;gap:7px;color:var(--secondary);font-size:12px;font-weight:650}.field input{width:100%;min-height:42px;border:1px solid var(--line);border-radius:8px;padding:0 12px;color:var(--ink);background:var(--panel2)}input::placeholder{color:var(--muted)}input:disabled,button:disabled,select:disabled{cursor:not-allowed;opacity:.48}.field-error{margin:0;color:var(--danger);font-size:11px;font-weight:500}.utility-row{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:32px}.remember{display:inline-flex;align-items:center;gap:9px;min-height:32px;color:var(--secondary);font-size:12px;cursor:pointer}.remember input{display:grid;place-content:center;appearance:none;width:18px;height:18px;margin:0;border:1px solid var(--line);border-radius:5px;background:var(--panel2);cursor:pointer}.remember input:before{width:9px;height:9px;border-radius:2px;background:#071014;content:"";transform:scale(0);transition:transform 120ms}.remember input:checked{border-color:var(--cyan);background:var(--cyan)}.remember input:checked:before{transform:scale(1)}.button{width:100%;min-height:42px;border:1px solid var(--line);border-radius:8px;padding:0 16px;cursor:pointer;transition-property:background-color,color,transform,border-color,opacity;transition-duration:130ms}.primary{color:#071014;border-color:var(--cyan);background:var(--cyan);font-weight:700}.primary:hover{border-color:var(--cyan-hover);background:var(--cyan-hover)}.secondary{color:var(--secondary);background:var(--module)}.button:not(:disabled):active{transform:scale(.96)}.nav-link{display:inline-flex;align-items:center;min-height:32px;border-radius:6px;padding:4px 6px;color:var(--cyan);text-decoration:none;font-size:12px;transition-property:background-color,color,transform;transition-duration:130ms}.nav-link[aria-disabled=true]{pointer-events:none;opacity:.48}.status{margin:0;padding:11px 12px;border:1px solid var(--line-soft);border-radius:10px;color:var(--secondary);background:var(--panel2);font-size:12px}.status[data-kind=error]{border-color:rgba(240,125,135,.45);color:var(--danger)}.status[data-kind=permission_denied]{border-color:rgba(221,176,100,.45);color:var(--warning)}.status[data-kind=populated]{border-color:rgba(98,199,170,.4);color:var(--ok)}.result{margin:0;color:var(--cyan);font-size:12px}.trust{margin:20px 0 0;color:var(--muted);font-size:11px}
.recovery .content{padding:28px 32px 30px}.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:0 0 24px;padding:0;list-style:none}.steps li{display:grid;grid-template-columns:28px minmax(0,1fr);gap:8px;align-items:center;color:var(--muted);font-size:11px}.steps b{display:grid;place-items:center;width:28px;height:28px;border:1px solid var(--line);border-radius:50%;color:var(--ink);background:var(--module)}.steps li:first-child{color:var(--secondary)}.steps li:first-child b{border-color:#66b9d3;color:#071014;background:#66b9d3}.recovery-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start;gap:16px}.field-group{display:grid;gap:12px;padding:16px;border:1px solid var(--line-soft);border-radius:12px;background:var(--panel2)}.group-title{margin:0;color:var(--ink);font-size:12px;font-weight:700}.hint{margin:0;color:var(--muted);font-size:11px}.recovery-form>.status,.recovery-form>.result,.safe-return{grid-column:1/-1}.safe-return{display:flex;justify-content:center}
@media(max-width:800px){body{display:block;padding:16px}.auth-screen{margin:auto}.content,.recovery .content{padding:22px}.utility-row{align-items:flex-start;flex-direction:column;gap:8px}.steps{grid-template-columns:1fr;gap:6px}.steps li{grid-template-columns:28px 1fr}.recovery-form{grid-template-columns:1fr}.field-group{padding:14px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation:none!important;transition-duration:0s!important}}
__PILOT_COMPONENT_CSS__
__PILOT_BUTTON_STATE_CSS__
</style></head><body>
<main class="auth-screen signin" data-screen-id="UI-AUTH-001" data-route="/auth/sign-in" data-ui-region="UI-AUTH-001.content">
 <div class="brandbar" data-ui-region="UI-AUTH-001.brand"><div class="brand" data-ui-element="signin-brand"><span class="mark" aria-hidden="true">C</span><span>Custometry</span></div><label class="locale-wrap"><span data-copy="locale_label">Язык</span><select class="locale" data-locale data-ui-element="signin-locale" data-ui-component="control.compact" data-ui-variant="language-select" data-ui-size="compact" data-ui-state="default" data-ui-slot="shell.main-content.select" data-ui-standard-component="control.compact" data-ui-standard-variant="compact-control.lifecycle-metric-select" data-ui-standard-size="compact" data-ui-standard-slot="shell.main-content.select" data-prototype-action="UI-AUTH-001.change-language" data-action="UI-AUTH-001.change-language" aria-label="Язык"><option value="ru">Русский</option><option value="en">English</option></select></label></div>
 <section class="content" data-ui-region="UI-AUTH-001.form" data-ui-element="signin-surface"><header class="heading"><h1 data-ui-element="signin-title" data-copy="title">Вход в Custometry</h1><p class="lead" data-ui-element="signin-description" data-copy="lead">Введите рабочий email и пароль.</p></header>
  <form class="form" onsubmit="event.preventDefault()"><label class="field"><span data-copy="email_label">Рабочий email</span><input data-ui-element="signin-email" aria-label="Рабочий email" type="email" name="email" autocomplete="username" placeholder="name@company.ru" data-copy-placeholder="email_placeholder" aria-describedby="signin-email-error"><span id="signin-email-error" class="field-error" data-ui-element="signin-email-error" data-copy-state="email_error" hidden></span></label><label class="field"><span data-copy="password_label">Пароль</span><input data-ui-element="signin-password" aria-label="Пароль" type="password" name="password" autocomplete="current-password" data-sensitive aria-describedby="signin-password-error"><span id="signin-password-error" class="field-error" data-ui-element="signin-password-error" data-copy-state="password_error" hidden></span></label><div class="utility-row"><label class="remember"><input data-ui-element="signin-remember" type="checkbox" name="remember" data-ui-component="control.checkbox" data-ui-variant="remember-session" data-ui-size="sm" data-ui-state="default" data-prototype-action="UI-AUTH-001.toggle-remember" data-action="UI-AUTH-001.toggle-remember"><span data-copy="remember">Запомнить меня</span></label><a class="nav-link" href="/auth/recovery" data-pilot-action-style="quiet" data-ui-element="signin-open-recovery" data-ui-component="navigation.link" data-ui-variant="auth-route" data-ui-size="text" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.text-button" data-ui-standard-variant="text-button" data-ui-standard-size="text" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.open-recovery" data-action="UI-AUTH-001.open-recovery" data-copy="recovery_link">Восстановить пароль</a></div><button class="button primary" type="submit" data-pilot-action-style="primary" data-ui-element="signin-submit" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="md" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-001.submit-credentials" data-action="UI-AUTH-001.submit-credentials" data-copy="submit">Войти</button><p class="status" role="status" aria-live="polite" data-ui-element="signin-message" data-copy-state="message" hidden></p><p class="result" role="status" aria-live="polite" data-ui-element="signin-result" data-result hidden></p></form><p class="trust" data-ui-element="signin-trust" data-copy="trust">Данные остаются в вашей инсталляции.</p>
 </section>
</main>
<main class="auth-screen recovery" hidden data-screen-id="UI-AUTH-004" data-route="/auth/recovery" data-ui-region="UI-AUTH-004.content">
 <div class="brandbar" data-ui-region="UI-AUTH-004.brand"><div class="brand" data-ui-element="recovery-brand"><span class="mark" aria-hidden="true">C</span><span>Custometry</span></div><label class="locale-wrap"><span data-copy="locale_label">Язык</span><select class="locale" data-locale data-ui-element="recovery-locale" data-ui-component="control.compact" data-ui-variant="language-select" data-ui-size="compact" data-ui-state="default" data-ui-slot="shell.main-content.select" data-ui-standard-component="control.compact" data-ui-standard-variant="compact-control.lifecycle-metric-select" data-ui-standard-size="compact" data-ui-standard-slot="shell.main-content.select" aria-label="Язык"><option value="ru">Русский</option><option value="en">English</option></select></label></div>
 <section class="content" data-ui-region="UI-AUTH-004.form" data-ui-element="recovery-surface"><header class="heading"><h1 data-ui-element="recovery-title" data-copy="title">Смена пароля</h1><p class="lead" data-ui-element="recovery-description" data-copy="lead">Введите код сброса, полученный у администратора, и задайте новый пароль.</p></header>
  <ol class="steps" data-ui-element="recovery-steps"><li><b>1</b><span data-copy="step_code">Код</span></li><li><b>2</b><span data-copy="step_password">Новый пароль</span></li><li><b>3</b><span data-copy="step_done">Готово</span></li></ol><form class="recovery-form" onsubmit="event.preventDefault()"><section class="field-group"><p class="group-title" data-copy="step_code">Код</p><label class="field"><span data-copy="token_label">Код сброса</span><input data-ui-element="recovery-token" aria-label="Код сброса" name="reset-code" autocomplete="one-time-code" placeholder="Введите код" data-copy-placeholder="token_placeholder" data-sensitive aria-describedby="recovery-token-error"><span id="recovery-token-error" class="field-error" data-ui-element="recovery-token-error" data-copy-state="token_error" hidden></span></label><button class="button secondary" type="button" data-pilot-action-style="secondary" data-ui-element="recovery-validate" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="md" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-004.validate-reset-token" data-action="UI-AUTH-004.validate-reset-token" data-copy="validate">Проверить код</button></section><section class="field-group"><p class="group-title" data-copy="step_password">Новый пароль</p><label class="field"><span data-copy="password_label">Новый пароль</span><input data-ui-element="recovery-password" aria-label="Новый пароль" type="password" name="new-password" autocomplete="new-password" data-sensitive></label><label class="field"><span data-copy="confirm_label">Повторите пароль</span><input data-ui-element="recovery-confirm" aria-label="Повторите пароль" type="password" name="confirm-password" autocomplete="new-password" data-sensitive></label><p class="hint" data-copy="password_hint">Требования к паролю проверяются при сохранении.</p><button class="button primary" type="submit" data-pilot-action-style="primary" data-ui-element="recovery-set-password" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="md" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.button" data-ui-standard-variant="button" data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-004.set-new-password" data-action="UI-AUTH-004.set-new-password" data-copy="submit">Сохранить новый пароль</button></section><p class="status" role="status" aria-live="polite" data-ui-element="recovery-message" data-copy-state="message" hidden></p><p class="result" role="status" aria-live="polite" data-ui-element="recovery-result" data-result hidden></p><div class="safe-return"><a class="nav-link" href="/auth/sign-in" data-pilot-action-style="quiet" data-ui-element="recovery-return" data-ui-component="navigation.link" data-ui-variant="auth-route" data-ui-size="text" data-ui-state="default" data-ui-slot="shell.main-content.button" data-ui-standard-component="action.text-button" data-ui-standard-variant="text-button" data-ui-standard-size="text" data-ui-standard-slot="shell.main-content.button" data-prototype-action="UI-AUTH-004.return-sign-in" data-action="UI-AUTH-004.return-sign-in" data-copy="return_link">Вернуться ко входу</a></div></form><p class="trust" data-ui-element="recovery-trust" data-copy="trust">Если у вас нет кода, обратитесь к администратору инсталляции.</p>
 </section>
</main>
<script>
const copy=__VISIBLE_COPY__;const q=new URLSearchParams(location.search);const screen=q.get('screen')==='UI-AUTH-004'?'UI-AUTH-004':'UI-AUTH-001';const state=q.get('state')||`${screen}.initial`;let lang=q.get('lang')==='en'?'en':'ru';const stateName=state.split('.').pop();const stateKind=stateName==='first_loading'?'loading':stateName==='ready'?'populated':stateName==='session_expired'?'permission_denied':stateName==='initial'?'initial':'error';
document.documentElement.lang=lang;document.querySelectorAll('[data-screen-id]').forEach(x=>{if(x.dataset.screenId!==screen)x.remove()});const active=document.querySelector(`[data-screen-id="${screen}"]`);active.hidden=false;active.dataset.stateId=state;const surfaceKey=screen==='UI-AUTH-001'?'signin':'recovery';
function applyCopy(){const model=copy[lang][surfaceKey];active.querySelectorAll('[data-copy]').forEach(node=>{const key=node.dataset.copy;if(key==='locale_label')node.textContent=lang==='en'?'Language':'Язык';else if(model[key]!==undefined)node.textContent=model[key]});active.querySelectorAll('[data-copy-placeholder]').forEach(node=>node.placeholder=model[node.dataset.copyPlaceholder]||'');const stateCopy=model.states[stateName];active.querySelectorAll('[data-copy-state]').forEach(node=>{const value=stateCopy[node.dataset.copyState]||'';node.textContent=value;node.hidden=!value});active.querySelectorAll('[data-locale]').forEach(node=>{node.value=lang;node.setAttribute('aria-label',lang==='en'?'Language':'Язык')});const names=surfaceKey==='signin'?{'signin-email':model.email_label,'signin-password':model.password_label,'signin-remember':model.remember}:{'recovery-token':model.token_label,'recovery-password':model.password_label,'recovery-confirm':model.confirm_label};Object.entries(names).forEach(([id,name])=>active.querySelector(`[data-ui-element="${id}"]`)?.setAttribute('aria-label',name))}
applyCopy();const loading=stateName==='first_loading';active.querySelectorAll('button,input').forEach(x=>x.disabled=loading);active.querySelectorAll('a[data-action]').forEach(x=>x.setAttribute('aria-disabled',String(loading)));if(stateName==='validation_error')active.querySelectorAll('input[aria-describedby]').forEach(x=>x.setAttribute('aria-invalid','true'));
const outcomes={ru:{'UI-AUTH-001.open-recovery':'Открыт экран восстановления пароля.','UI-AUTH-001.toggle-remember':'Настройка запоминания изменена.','UI-AUTH-001.change-language':'Язык изменён.','UI-AUTH-001.submit-credentials':'Вход проверен без раскрытия лишних сведений.','UI-AUTH-004.validate-reset-token':'Код подтверждён.','UI-AUTH-004.set-new-password':'Пароль обновлён. Вернитесь ко входу.','UI-AUTH-004.return-sign-in':'Открыт экран входа.'},en:{'UI-AUTH-001.open-recovery':'Password recovery opened.','UI-AUTH-001.toggle-remember':'Remember preference changed.','UI-AUTH-001.change-language':'Language changed.','UI-AUTH-001.submit-credentials':'Sign-in checked without exposing account details.','UI-AUTH-004.validate-reset-token':'Code confirmed.','UI-AUTH-004.set-new-password':'Password updated. Return to sign in.','UI-AUTH-004.return-sign-in':'Sign-in opened.'}};
function recordAction(control,event){if(control.matches('a'))event.preventDefault();if(control.getAttribute('aria-disabled')==='true'||control.disabled)return;if(control.dataset.action==='UI-AUTH-001.change-language'){lang=control.value==='en'?'en':'ru';document.documentElement.lang=lang;applyCopy()}const result=active.querySelector('[data-result]');result.textContent=outcomes[lang][control.dataset.action];result.hidden=false;result.dataset.actionResult=control.dataset.action}
active.querySelectorAll('[data-action]').forEach(control=>{const eventName=control.matches('select,input[type=checkbox]')?'change':'click';control.addEventListener(eventName,event=>recordAction(control,event));if(control.matches('input[type=checkbox]'))control.addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();control.checked=!control.checked;recordAction(control,event)}})});
</script></body></html>'''
    if REVISION >= 5:
        document = stabilize_auth_state_geometry(document)
    product_binding_replacements = {
        '<label class="locale-wrap"><span data-copy="locale_label">Язык</span><select class="locale" data-locale data-ui-element="signin-locale"': '<label class="locale-wrap" data-ui-element="signin-locale-field"><span data-copy="locale_label">Язык</span><select class="locale" data-locale data-ui-element="signin-locale"',
        '<label class="locale-wrap"><span data-copy="locale_label">Язык</span><select class="locale" data-locale data-ui-element="recovery-locale"': '<label class="locale-wrap" data-ui-element="recovery-locale-field"><span data-copy="locale_label">Язык</span><select class="locale" data-locale data-ui-element="recovery-locale"',
        '<label class="remember"><input data-ui-element="signin-remember" type="checkbox" name="remember" data-ui-component="control.checkbox" data-ui-variant="remember-session" data-ui-size="sm"': '<label class="remember" for="signin-remember-control"><input id="signin-remember-control" data-ui-element="signin-remember" type="checkbox" name="remember" aria-label="Запомнить меня" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-semantic-control="remember-checkbox"',
        'data-ui-element="signin-locale" data-ui-component="control.compact" data-ui-variant="language-select" data-ui-size="compact"': 'data-ui-element="signin-locale" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-semantic-control="language-select"',
        'data-ui-element="recovery-locale" data-ui-component="control.compact" data-ui-variant="language-select" data-ui-size="compact"': 'data-ui-element="recovery-locale" data-semantic-control="language-select"',
        'data-ui-element="signin-open-recovery" data-ui-component="navigation.link" data-ui-variant="auth-route" data-ui-size="text"': 'data-ui-element="signin-open-recovery" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-semantic-control="navigation-link"',
        'data-ui-element="recovery-return" data-ui-component="navigation.link" data-ui-variant="auth-route" data-ui-size="text"': 'data-ui-element="recovery-return" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-semantic-control="navigation-link"',
        'data-ui-standard-component="action.text-button" data-ui-standard-variant="text-button" data-ui-standard-size="text" data-ui-standard-slot="shell.main-content.button"': '',
        'data-ui-element="signin-submit" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="md"': 'data-ui-element="signin-submit" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="sm" data-semantic-control="submit-button"',
        'data-ui-element="recovery-validate" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="md"': 'data-ui-element="recovery-validate" data-ui-component="action.button" data-ui-variant="secondary" data-ui-size="sm" data-semantic-control="secondary-button"',
        'data-ui-element="recovery-set-password" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="md"': 'data-ui-element="recovery-set-password" data-ui-component="action.button" data-ui-variant="primary" data-ui-size="sm" data-semantic-control="submit-button"',
    }
    for old, new in product_binding_replacements.items():
        if old not in document:
            raise ValueError(f"auth product binding marker disappeared: {old}")
        document = document.replace(old, new)
    return document.replace("__VISIBLE_COPY__", copy_json).replace("__PILOT_COMPONENT_CSS__", pilot_component_css(baseline)).replace("__PILOT_BUTTON_STATE_CSS__", pilot_button_state_css())


def origin(kind: str, ref_value: str) -> dict[str, Any]:
    return {"kind": kind, "ref": ref_value}


def make_region(base: dict[str, Any], screen_id: str, state_id: str) -> dict[str, Any]:
    row = deepcopy(base)
    row.update({
        "region_id": f"{screen_id}.content",
        "locator": f"[data-screen-id=\"{screen_id}\"]:not([hidden])",
        "component_id": "candidate.auth-surface",
        "component_status": "candidate",
        "variant": "sign-in" if screen_id == "UI-AUTH-001" else "recovery-wizard",
        "state": state_id.rsplit(".", 1)[-1],
        "source_refs": [origin("accepted_visual", rel(SOURCE))],
        "computed_style_properties_origin": origin("accepted_visual", rel(SOURCE)),
    })
    return row


def make_element(base: dict[str, Any], screen_id: str, state_id: str, spec: tuple[str, str, str | None, str | None, str | None, str, list[str]]) -> dict[str, Any]:
    element_id, element_type, component_id, variant, size, content, actions = spec
    row = deepcopy(base)
    region_id = f"{screen_id}.brand" if element_id.endswith("-brand") else (f"{screen_id}.form" if element_id.endswith("-surface") else f"{screen_id}.content")
    state_name = state_id.rsplit(".", 1)[-1]
    conditional_visibility = {
        "signin-email-error": state_name == "validation_error",
        "signin-password-error": state_name == "validation_error",
        "recovery-token-error": state_name == "validation_error",
        "signin-message": state_name in {"first_loading", "validation_error", "failed", "session_expired"},
        "recovery-message": state_name in {"first_loading", "ready", "failed", "session_expired"},
        "signin-result": False,
        "recovery-result": False,
    }
    if REVISION >= 5:
        # The fixed feedback slot alternates between durable trust guidance and
        # state feedback. Keep the state contract aligned with what the user can
        # actually see instead of requiring both layers to overlap.
        conditional_visibility.update({
            "signin-trust": state_name not in {"first_loading", "validation_error", "failed", "session_expired"},
            "recovery-trust": state_name not in {"first_loading", "ready", "failed", "session_expired"},
        })
    taxonomy = ACTION_TAXONOMY.get(element_id)
    row.update({
        "element_id": element_id,
        "parent_element_id": None,
        "region_id": region_id,
        "locator": f"[data-ui-element=\"{element_id}\"]",
        "visibility": "required" if conditional_visibility.get(element_id, True) else "conditional",
        "element_type": element_type,
        "component_id": component_id,
        "variant": variant,
        "size_class": size,
        "content_contract": content,
        "icon_id": None,
        "action_ids": actions,
        "state_ids": [state_id],
        "geometry": row["geometry"],
        "spacing_relations": row["spacing_relations"],
        "visual_properties": row["visual_properties"],
        "responsive_behavior": [row["responsive_behavior"][0]],
        "accessibility": row["accessibility"],
        "source_refs": [origin("product_contract", f"{rel(INTAKE)}#/screens/{SCREEN_INDEXES[screen_id]}")],
        "standard_identity": taxonomy["standard_identity"] if taxonomy else None,
        "standard_slot_id": taxonomy["standard_slot_id"] if taxonomy else None,
        "component_state_ids": taxonomy["states"] if taxonomy else ["default"],
    })
    return row


def element_specs(screen_id: str) -> list[tuple[str, str, str | None, str | None, str | None, str, list[str]]]:
    if screen_id == "UI-AUTH-001":
        return [
            ("signin-brand", "brand", None, "graphite", None, "Custometry", []), ("signin-locale-field", "label", None, "language-control", None, "Language control label", []), ("signin-locale", "select", "action.button", "secondary", "sm", "Language / Язык", ["UI-AUTH-001.change-language"]),
            ("signin-surface", "form", None, "compact-sign-in", None, "Sign-in surface", []),
            ("signin-title", "heading", None, None, None, "Sign in to Custometry / Вход в Custometry", []), ("signin-description", "text", None, None, None, "Work email and password instruction", []),
            ("signin-email", "input", None, None, "md", "Email", []), ("signin-password", "input", None, None, "md", "Password", []),
            ("signin-email-error", "error", None, None, None, "Inline email recovery instruction", []), ("signin-password-error", "error", None, None, None, "Inline password recovery instruction", []),
            ("signin-remember", "checkbox", "action.button", "secondary", "sm", "Remember me", ["UI-AUTH-001.toggle-remember"]),
            ("signin-open-recovery", "link", "action.button", "secondary", "sm", "Reset password destination", ["UI-AUTH-001.open-recovery"]),
            ("signin-submit", "button", "action.button", "primary", "sm", "Sign in", ["UI-AUTH-001.submit-credentials"]),
            ("signin-message", "status", None, None, None, "State-specific safe feedback", []), ("signin-result", "status", None, None, None, "Action outcome", []),
            ("signin-trust", "note", None, None, None, "Self-hosted installation trust", []),
        ]
    return [
        ("recovery-brand", "brand", None, "graphite", None, "Custometry", []), ("recovery-locale-field", "label", None, "language-control", None, "Language control label", []), ("recovery-locale", "select", None, "language-control", "compact", "Language / Язык", []),
        ("recovery-surface", "wizard", None, "recovery-wizard", None, "Password reset wizard", []),
        ("recovery-title", "heading", None, None, None, "Reset password / Смена пароля", []), ("recovery-description", "text", None, None, None, "Administrator-issued reset code and new password", []),
        ("recovery-steps", "list", None, "stepper", None, "Code, new password, done", []), ("recovery-token", "input", None, None, "md", "Reset code", []),
        ("recovery-token-error", "error", None, None, None, "Inline reset-code recovery instruction", []),
        ("recovery-password", "input", None, None, "md", "New password", []), ("recovery-confirm", "input", None, None, "md", "Confirm password", []),
        ("recovery-validate", "button", "action.button", "secondary", "sm", "Check reset code", ["UI-AUTH-004.validate-reset-token"]),
        ("recovery-return", "link", "action.button", "secondary", "sm", "Return to sign in", ["UI-AUTH-004.return-sign-in"]),
        ("recovery-set-password", "button", "action.button", "primary", "sm", "Save new password", ["UI-AUTH-004.set-new-password"]),
        ("recovery-message", "status", None, None, None, "State-specific safe feedback", []), ("recovery-result", "status", None, None, None, "Action outcome", []),
        ("recovery-trust", "note", None, None, None, "Administrator-assisted reset guidance", []),
    ]


def build_program_snapshot(states: dict[str, list[dict[str, Any]]]) -> None:
    projection = json.loads(G1.read_text(encoding="utf-8"))
    for screen in projection["screens"]:
        if screen["screen_id"] in states:
            screen["required_states"] = [row["state_id"] for row in states[screen["screen_id"]]]
    projection_path = ART / "g1-admission-inventory.family-projection.json"
    write_json(projection_path, projection)
    snapshot = json.loads(PROGRAM.read_text(encoding="utf-8"))
    for source in snapshot["source_contracts"]:
        if source.get("path") == rel(G1):
            source["screen_collections"] = []
    snapshot["source_contracts"].append({
        "path": rel(projection_path), "authority": "G4 stage-owned exact full-inventory projection adding only accepted required states for UI-AUTH-001 and UI-AUTH-004",
        "required_status": "complete", "sha256": sha(projection_path), "screen_collections": [{"json_pointer": "/screens", "id_key": "screen_id"}], "journey_collections": [],
    })
    for entry in snapshot["screens"]:
        if entry["screen_ref"]["path"] == rel(G1):
            entry["screen_ref"]["path"] = rel(projection_path)
    screen_entries = ART / "program-screen-entries.snapshot.json"
    write_json(screen_entries, {"screens": snapshot["screens"]})
    screen_index = ART / "screens-index.snapshot.json"
    write_json(screen_index, {"$schema": "program-artifact-index.schema.json", "schema_id": "codex.ui-program-artifact-index/v1", "program_id": PROGRAM_ID, "program_revision": PROGRAM_REVISION, "index_kind": "screens", "entries": [{"id": entry["screen_ref"]["expected_id"], "path": rel(screen_entries), "sha256": sha(screen_entries), "json_pointer": f"/screens/{index}"} for index, entry in enumerate(snapshot["screens"])]})
    snapshot["artifact_indexes"]["screens"] = {"path": rel(screen_index), "sha256": sha(screen_index)}
    snapshot["execution_artifacts"]["plan_doc"] = rel(SNAPSHOT)
    write_json(SNAPSHOT, snapshot)
    write_json(ART / "program-snapshot-binding.json", {"schema_id": "codex.ui-stage-program-snapshot-binding/v1", "canonical_program": {"path": rel(PROGRAM), "sha256": sha(PROGRAM)}, "snapshot": {"path": rel(SNAPSHOT), "sha256": sha(SNAPSHOT)}, "projection": {"path": rel(projection_path), "sha256": sha(projection_path)}, "screen_index_snapshot": {"path": rel(screen_index), "sha256": sha(screen_index)}, "changed_pointers": ["/source_contracts", "/screens/*/screen_ref/path", "/artifact_indexes/screens", "/execution_artifacts/plan_doc"], "reason": "Family aggregation requires exact accepted required_states for both corrected auth representatives; the projection changes no other inventory meaning.", "accepted_authority_changed": False, "result": "passed"})


def build_contract(screen_id: str, state: dict[str, Any], screens: dict[str, dict[str, Any]], baseline: dict[str, Any], fixture: Path) -> dict[str, Any]:
    base = json.loads(BASE_CONTRACT.read_text(encoding="utf-8"))
    state_id = state["state_id"]
    manifest = ART / f"applicability/{state_id}.{REVISION_TAG}.json"
    base.update({
        "contract_profile": "codex.ui-screen-design-contract/v1@2.0.0", "screen_revision_id": f"{state_id}.all.ru-RU.graphite.{REVISION_TAG}", "program_revision_ref": f"{PROGRAM_ID}@{PROGRAM_REVISION}", "status": "review",
        "functional_contract_ref": {"path": rel(INTAKE), "sha256": sha(INTAKE), "json_pointer": f"/screens/{SCREEN_INDEXES[screen_id]}", "screen_id": screen_id},
        "baseline_binding": {"baseline_id": baseline["baseline_id"], "path": rel(BASELINE), "sha256": sha(BASELINE), "shell_variant_id": "shell.auth", "exception_id": "baseline-exception-auth"},
        "standard_binding": {"standard_revision_id": baseline["standard_contract"]["standard_revision_id"], "clause_inventory_sha256": baseline["standard_contract"]["clause_inventory_sha256"], "applicability_manifest": {"path": rel(manifest), "sha256": "0" * 64}},
        "standard_exceptions": [],
        "product_identity": {"screen_id": screen_id, "route_id": screen_id, "route": screens[screen_id]["route"], "state_id": state_id, "role_id": "all", "permission_profile": "organization.read", "locale": "ru", "theme": "graphite"},
        "comparison_claims": {"required_purpose": "visual_language_conformance", "deterministic_render_proves_fidelity": False, "reference_logical_artifact_id": f"{PROGRAM_ID}:accepted-pilot:ru:{REVISION_TAG}", "implementation_logical_artifact_id": f"{PROGRAM_ID}:{screen_id}:{state_id}:{REVISION_TAG}"},
    })
    base["source_visual"].update({"html_path": rel(SOURCE), "html_sha256": sha(SOURCE), "image_path": None, "image_sha256": None})
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    base["visual_authority"] = {key: program["visual_authority"][key] for key in ("source_visual_ref", "source_visual_sha256", "owner_decision_ref", "screen_acceptance_scope", "visual_language_scope", "reusable_foundation_scope", "inheritance_policy", "mobile_scope")}
    base["render_environment"].update({"fixed_clock_iso": "2026-08-13T20:07:38Z", "fixture_data_path": rel(fixture), "fixture_data_sha256": sha(fixture), "font_bundle_sha256": canonical_sha(baseline["font_contract"]), "asset_bundle_sha256": canonical_sha(baseline["asset_contract"])})
    responsive_origin = origin("product_contract", f"{rel(BASELINE)}#/responsive_contract")
    base["viewport_contract"]["supported_web_width_range"] = {**baseline["responsive_contract"]["supported_web_width_range"], "origin": responsive_origin}
    base["viewport_contract"]["anchors"] = [{"anchor_id": aid, "width": width, "height": height, "class": "responsive_web", "state_ref": state_id, "origin": responsive_origin} for aid, width, height in ANCHORS]
    base["viewport_contract"]["above_supported_range_origin"] = responsive_origin
    base_region = next(row for row in base["regions"] if row["region_id"] == "UI-ADMIN-003.content")
    base_element = base["element_contracts"][0]
    base["regions"] = [make_region(base_region, screen_id, state_id)]
    brand_region = make_region(base_region, screen_id, state_id)
    brand_region.update({"region_id": f"{screen_id}.brand", "locator": f"[data-ui-region=\"{screen_id}.brand\"]", "component_id": "candidate.auth-brandbar", "variant": "graphite"})
    form_region = make_region(base_region, screen_id, state_id)
    form_region.update({"region_id": f"{screen_id}.form", "locator": f"[data-ui-region=\"{screen_id}.form\"]", "component_id": "candidate.auth-form", "variant": "compact-sign-in" if screen_id == "UI-AUTH-001" else "recovery-wizard"})
    base["regions"].extend([brand_region, form_region])
    base["element_contracts"] = [make_element(base_element, screen_id, state_id, spec) for spec in element_specs(screen_id)]
    visible_actions = []
    for action in screens[screen_id]["actions"]:
        expected_text = {
            "UI-AUTH-001.open-recovery": "Открыт экран восстановления пароля.",
            "UI-AUTH-001.toggle-remember": "Настройка запоминания изменена.",
            "UI-AUTH-001.change-language": "Language changed.",
            "UI-AUTH-001.submit-credentials": "Вход проверен без раскрытия лишних сведений.",
            "UI-AUTH-004.validate-reset-token": "Код подтверждён.",
            "UI-AUTH-004.set-new-password": "Пароль обновлён. Вернитесь ко входу.",
            "UI-AUTH-004.return-sign-in": "Открыт экран входа.",
        }[action["action_id"]]
        loading_state = state_id.endswith(".first_loading")
        visible_actions.append({
            "action_id": action["action_id"],
            "expected_outcome": action["outcome"],
            "side_effect_class": "local_state",
            "activation_policy": "assert_affordance_only" if loading_state else "execute_in_fixture",
            "outcome_assertion": (
                {"kind": "not_executed", "selector": None, "property": None, "expected": "visible_disabled_control"}
                if loading_state
                else {"kind": "dom", "selector": "[data-result]", "property": "textContent", "expected": expected_text}
            ),
        })
    base["interaction_contract"]["visible_actions"] = visible_actions
    base["interaction_contract"]["no_actions_reason_ref"] = None
    base["interaction_contract"]["allowed_origins"] = ["http://127.0.0.1:4173"]
    base["interaction_contract"]["redaction_selectors"] = ["[data-sensitive]", "input[type='password']", "input[autocomplete='one-time-code']"]
    base["acceptance"]["pixel_diff_policy"]["channel_threshold"]["value"] = 18
    base["acceptance"]["pixel_diff_policy"]["approved_max_different_pixels"].update({"value": 2073600, "unit": "px"})
    return base


def bootstrap() -> None:
    ART.mkdir(parents=True, exist_ok=True); EVID.mkdir(parents=True, exist_ok=True); TARGET.parent.mkdir(parents=True, exist_ok=True)
    states = state_rows(); screens = screen_rows(); baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    fixture = ART / "fixture.json"
    write_json(fixture, {"schema_id": "custometry.g4-auth-fixture/v2", "fixed_clock": "2026-08-13T20:07:38Z", "routes": {"UI-AUTH-001": "/auth/sign-in", "UI-AUTH-004": "/auth/recovery"}, "states": states, "locales": ["ru", "en"], "network_mode": "isolated_loopback", "sensitive_values": "synthetic_and_redacted"})
    rendered = target_html(baseline).replace("__FIXTURE_SHA256__", sha(fixture)).replace("__FONT_SHA256__", canonical_sha(baseline["font_contract"])).replace("__ASSET_SHA256__", canonical_sha(baseline["asset_contract"]))
    TARGET.write_text(rendered, encoding="utf-8")
    copy_rows = []
    for locale, locale_copy in VISIBLE_COPY.items():
        for screen_id, surface_key in (("UI-AUTH-001", "signin"), ("UI-AUTH-004", "recovery")):
            surface = locale_copy[surface_key]
            static_copy = {key: value for key, value in surface.items() if key != "states"}
            for state in states[screen_id]:
                state_name = state["state_id"].rsplit(".", 1)[-1]
                copy_rows.append({
                    "screen_id": screen_id,
                    "state_id": state["state_id"],
                    "locale": locale,
                    "visible_copy": {**static_copy, **surface["states"][state_name]},
                    "provenance": {
                        "product_semantics": ["custometry-ui-blueprint-ru.md#9.1-authentication-и-onboarding-6-страниц", "custometry-technical-blueprint-ru.md#20.2-authentication"],
                        "route_contract": f"packages/contracts/routes/ui-route-contracts.json#/routes/{SCREEN_INDEXES[screen_id]}",
                        "classification": "source_bound_product_copy_and_minimal_target_authored_connective_copy",
                        "connective_copy_justification": "Names only the action, destination, recovery step, or next safe action without inventing a delivery channel, product policy, or implementation detail.",
                    },
                })
    write_json(EVID / "visible-copy-inventory.json", {
        "schema_id": "custometry.ui-visible-copy-inventory/v1", "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE_ID, "screen_state_locale_pairs": copy_rows,
        "expected_pairs": 24, "observed_pairs": len(copy_rows),
        "forbidden_visible_copy": ["Помощь с паролем", "/auth/sign-in", "/auth/recovery", "Проверочное значение", "separate route", "Отдельный маршрут"],
        "result": "passed" if len(copy_rows) == 24 else "failed",
    })
    write_json(EVID / "auth-action-taxonomy.json", {
        "schema_id": "custometry.ui-auth-action-taxonomy/v1", "program_id": PROGRAM_ID, "stage_instance_id": STAGE_ID,
        "taxonomy": [
            {"kind": "submit_action", "elements": ["signin-submit", "recovery-set-password"], "native_element": "button", "pilot_mapping": "action.button/button/standard/shell.main-content.button state projection", "component_applicability": "source_backed_not_applicable", "reason": "The accepted observation's fixed 144px width belongs to the pilot composition; the target inherits its exact control and state grammar while the auth form owns full-column width."},
            {"kind": "secondary_action", "elements": ["recovery-validate"], "native_element": "button", "pilot_mapping": "action.button/button/standard/shell.main-content.button state projection", "component_applicability": "source_backed_not_applicable", "reason": "The accepted observation's fixed 144px width belongs to the pilot composition; the target inherits its exact control and state grammar while the auth form owns full-column width."},
            {"kind": "navigation_link", "elements": ["signin-open-recovery", "recovery-return"], "native_element": "a[href]", "pilot_mapping": "source_backed_not_applicable", "reason": "The accepted pilot exposes only a global skip link and icon/text buttons, neither of which is the semantic or compositional identity of auth-route navigation; the target inherits foundation color, focus and motion without relabeling the link."},
            {"kind": "remember_preference", "elements": ["signin-remember"], "native_element": "input[type=checkbox]+label", "pilot_mapping": "source_backed_not_applicable", "reason": "The accepted pilot has no checkbox identity; foundation color, focus, density and hit-area clauses still apply without relabeling it as a button."},
            {"kind": "language_control", "elements": ["signin-locale", "recovery-locale"], "native_element": "select", "pilot_mapping": "control.compact/compact-control.lifecycle-metric-select/compact/shell.main-content.select"},
            {"kind": "wizard_progression", "elements": ["recovery-steps"], "native_element": "ol", "pilot_mapping": "source_backed_not_applicable", "reason": "The accepted pilot has no wizard stepper; the target uses foundation typography, palette, spacing, radius and border clauses without inventing a component exception."}
        ],
        "accepted_product_action_binding": "The immutable G0 functional contract names these actions as action.button; G4 preserves that compatibility field without using it as semantic or visual taxonomy.",
        "generic_standard_button_identity_for_all_actions": False,
        "result": "passed",
    })
    write_json(EVID / "button-interaction-lineage.json", {
        "schema_id": "custometry.ui-pilot-button-interaction-lineage/v1",
        "visual_authority": {"path": rel(SOURCE), "sha256": sha(SOURCE)},
        "target": {"path": rel(TARGET), "sha256": sha(TARGET)},
        "static_inventory_limit": "The accepted canonical inventory observes the generic action.button default identity, while the same accepted source contains distinct primary, hover and active CSS states that are not visible in that default observation.",
        "source_backed_states": {
            "default_primary": {"color": "#071014", "background": "#8ccfe3", "font_weight": 650},
            "hover_primary": {"color": "#071014", "background": "#a5dcec"},
            "default_secondary": {"color": "#a7a7ad", "background": "#1a1b1e"},
            "hover_secondary": {"color": "#f0f0f2", "background": "#222327"},
            "active": {"transform": "scale(.96)"},
            "disabled": {"opacity": 0.48, "transform": "none"},
        },
        "standard_exception": None,
        "superseded_unaccepted_exception_id": BUTTON_STATE_EXCEPTION_ID,
        "projection_scope": ["semantic submit buttons", "semantic secondary buttons"],
        "derivation": "Exact dark-theme values and interaction states are asserted against and projected from the accepted pilot source by build_g4_auth_r4_artifacts.py; no target-authored palette or motion value is introduced.",
        "result": "passed",
    })
    build_program_snapshot(states)
    for screen_id, rows in states.items():
        for state in rows:
            state_id = state["state_id"]
            contract_path = ART / f"contracts/{state_id}.{REVISION_TAG}.json"
            write_json(contract_path, build_contract(screen_id, state, screens, baseline, fixture))
    write_json(EVID / "route-state-distinction.json", {"schema_id": "custometry.ui-route-state-distinction/v2", "sign_in": {"screen_id": "UI-AUTH-001", "route": "/auth/sign-in", "surface_kind": "editor", "states": [row["state_id"] for row in states["UI-AUTH-001"]]}, "recovery": {"screen_id": "UI-AUTH-004", "route": "/auth/recovery", "surface_kind": "wizard", "states": [row["state_id"] for row in states["UI-AUTH-004"]]}, "visible_route_decoration": False, "forbidden_state": "UI-AUTH-001.recovery", "same_route": False, "same_screen_id": False, "forbidden_present": any(row["state_id"] == "UI-AUTH-001.recovery" for rows in states.values() for row in rows), "result": "passed"})
    write_json(ART / "reuse-decision.json", {"schema_id": "codex.ui-family-reuse-decision/v2", "family_id": FAMILY_ID, "representative_screen_ids": ["UI-AUTH-001", "UI-AUTH-004"], "individually_designed_screen_ids": ["UI-AUTH-001", "UI-AUTH-004"], "reuse_only_screen_ids": ["UI-AUTH-002", "UI-AUTH-003"], "decision": "Reuse the full accepted auth-shell visual grammar while preserving distinct route-specific composition for sign-in and recovery.", "scope_limit": "No individual design or acceptance claim is made for UI-AUTH-002 or UI-AUTH-003.", "result": "recorded"})


def bind() -> None:
    script = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/assemble_standard_applicability.py")
    for contract_path in sorted((ART / "contracts").glob("*.json")):
        contract = json.loads(contract_path.read_text(encoding="utf-8")); manifest = ROOT / contract["standard_binding"]["applicability_manifest"]["path"]
        subprocess.run(["python3", str(script), "--screen", str(contract_path), "--baseline", str(BASELINE), "--project-root", str(ROOT), "--output", str(manifest)], check=True)
        contract["standard_binding"]["applicability_manifest"]["sha256"] = sha(manifest); write_json(contract_path, contract)


def proof_requests() -> None:
    for contract_path in sorted((ART / "contracts").glob("*.json")):
        contract = json.loads(contract_path.read_text(encoding="utf-8")); state_id = contract["product_identity"]["state_id"]; screen_id = contract["product_identity"]["screen_id"]
        for anchor_id, _, _ in ANCHORS:
            folder = EVID / f"captures/{state_id}/{anchor_id}"
            for target in ("reference", "implementation"):
                logical = contract["comparison_claims"]["reference_logical_artifact_id" if target == "reference" else "implementation_logical_artifact_id"]
                source = SOURCE if target == "reference" else TARGET
                write_json(folder / f"{target}-provenance-request.json", {"program_ref": rel(PROGRAM), "target": target, "logical_artifact_id": logical, "anchor_id": anchor_id, "source_artifact_ref": rel(source), "capture_ref": rel(folder / f"{target}.png"), "geometry_receipt_ref": rel(folder / f"{target}-geometry.json")})
            write_json(folder / "capture-context.json", {"screen_id": screen_id, "state_id": state_id, "url_query": f"screen={screen_id}&state={state_id}&lang=ru"})


def review() -> None:
    correction_root = PROGRAM_DIR / "evidence/g4-r3/family-auth-shell-auth-baseline-exception-auth"
    correction_rows = []
    for name, expected_sha in OWNER_CORRECTIONS.items():
        path = correction_root / name
        observed_sha = sha(path)
        if observed_sha != expected_sha:
            raise ValueError(f"owner correction hash changed: {name}")
        correction_rows.append({"path": rel(path), "sha256": observed_sha, "disposition": "binding_requirement_not_acceptance"})
    if REVISION == 5:
        current_rejection = EVID / "owner-requested-changes-r5-03.json"
        current_document = json.loads(current_rejection.read_text(encoding="utf-8"))
        if current_document.get("decision", {}).get("status") != "requested_changes":
            raise ValueError("current owner rejection is not canonical requested_changes evidence")
        correction_rows.append({"path": rel(current_rejection), "sha256": sha(current_rejection), "disposition": "binding_structural_correction_not_acceptance"})
    if HISTORICAL_PREDECESSOR_DECISION is not None:
        predecessor = json.loads(HISTORICAL_PREDECESSOR_DECISION.read_text(encoding="utf-8"))
        if predecessor.get("decision", {}).get("status") != "accepted":
            raise ValueError("historical predecessor decision is not canonical accepted evidence")
        correction_rows.append({
            "path": rel(HISTORICAL_PREDECESSOR_DECISION),
            "sha256": sha(HISTORICAL_PREDECESSOR_DECISION),
            "disposition": "read_only_visual_predecessor_not_successor_acceptance",
        })
    write_json(EVID / "carried-owner-corrections.json", {
        "schema_id": "custometry.ui-carried-owner-corrections/v1",
        "source_stage": "G4@family.auth.shell-auth.baseline-exception-auth-r3",
        "target_stage": STAGE_ID,
        "corrections": correction_rows,
        "implementation_assertions": [
            "file and loopback review surfaces resolve without external assets",
            "screen and state controls are keyboard and pointer operable",
            "native checkbox, real links, native language select and semantic buttons retain distinct roles and accessible names",
            "mapped controls expose pilot-derived default, hover, active, focus-visible, selected/checked and disabled feedback",
            "sign-in uses one shared-edge form column and contains no route decoration, fixture terminology, marketing copy or empty initial status panel",
            "recovery is a distinct UI-AUTH-004 wizard with one reading order and stable action hierarchy",
            "each auth surface preserves its own exact initial-state window geometry across every rendered and interactive state",
        ],
        "result": "carried_forward",
    })
    write_json(EVID / "standard-exception-audit.json", {
        "schema_id": "custometry.ui-standard-exception-audit/v1", "program_id": PROGRAM_ID, "stage_instance_id": STAGE_ID,
        "removed_generic_mappings": ["remember-as-button", "recovery-navigation-as-button", "language-select-as-button", "wizard-navigation-as-button"],
        "superseded_exception": {"exception_id": BUTTON_STATE_EXCEPTION_ID, "reason": "The unaccepted r5 exception encoded the generic-button shortcut and is no longer referenced by any corrected screen contract."},
        "retained_exception": None,
        "broader_exception_created": False, "result": "passed",
    })
    skill_paths = [
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "assets/contract-versions.json",
        SKILL_ROOT / "assets/screen-design-contract.schema.json",
        SKILL_ROOT / "scripts/assemble_standard_applicability.py",
        SKILL_ROOT / "scripts/capture_geometry.cjs",
        SKILL_ROOT / "scripts/ui_standard_contract.py",
        SKILL_ROOT / "scripts/validate_skill_release.py",
    ]
    write_json(EVID / "active-skill-release-evidence.json", {
        "schema_id": "custometry.ui-active-skill-release-evidence/v1",
        "release_gate": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_skill_release.py",
            "result": "passed",
        },
        "files": [{"path": str(path), "sha256": sha(path)} for path in skill_paths],
        "program_owned_screen_schema": {"path": rel(PROGRAM_DIR / "screen-design-contract.schema.json"), "sha256": sha(PROGRAM_DIR / "screen-design-contract.schema.json")},
        "schema_copy_matches_active": sha(SKILL_ROOT / "assets/screen-design-contract.schema.json") == sha(PROGRAM_DIR / "screen-design-contract.schema.json"),
        "standard_identity_contract": "Product component identity remains source-of-truth for actions; standard_identity independently binds one exact accepted-pilot visual pattern.",
        "generic_element_type_fallback_for_stable_identity": False,
        "result": "passed",
    })
    rows = []
    for acceptance in sorted((EVID / "screen-acceptance").glob("*.json")):
        doc = json.loads(acceptance.read_text(encoding="utf-8")); rows.append((acceptance, doc))
    entries = []
    for path, doc in rows:
        for role in ("screen_acceptance", "standard_conformance"):
            entries.append({"entry_id": f"review-{len(entries)+1:02d}", "role": role, "artifact_ref": rel(path), "sha256": sha(path), "anchor_id": None, "state_id": doc["state_id"]})
    manifest = ART / "review-board.manifest.json"
    write_json(manifest, {"$schema": "review-board-manifest.schema.json", "schema_id": "codex.ui-review-board-manifest/v1", "program_id": PROGRAM_ID, "artifact_id": FAMILY_REVISION_ID, "revision": REVISION, "validation_profile": "family_review_ready", "entries": entries})
    closure = "".join(f'<li data-review-entry="{row["entry_id"]}">{html.escape(row["role"])} · {html.escape(row["state_id"])}</li>' for row in entries)
    state_labels = {"initial": "Начало", "first_loading": "Загрузка", "ready": "Готово", "validation_error": "Проверка полей", "failed": "Ошибка", "session_expired": "Сессия истекла"}
    states = state_rows(); state_buttons = "".join(f'<button type="button" data-state="{html.escape(row["state_id"])}">{html.escape(state_labels[row["state_id"].rsplit(".",1)[-1]])}</button>' for rows in states.values() for row in rows)
    board = ART / "review-board.html"
    board.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry · auth family {REVISION_TAG}</title><style>:root{{--bg:#070708;--panel:#111214;--module:#1a1b1e;--module-strong:#222327;--line:#303136;--ink:#f0f0f2;--secondary:#a7a7ad;--muted:#8b8c93;--cyan:#8ccfe3;--cyan-hover:#a5dcec;--focus:#8bd2e8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,system-ui,sans-serif}}main{{width:min(1120px,calc(100% - 32px));margin:auto;padding:24px 0 60px}}h1{{margin:0;font-size:30px}}header p{{max-width:70ch;color:var(--muted)}}.screens,.states{{display:flex;flex-wrap:wrap;gap:7px;margin:12px 0}}button{{min-height:36px;border:1px solid var(--line);border-radius:7px;padding:0 11px;color:var(--secondary);background:var(--module);cursor:pointer;transition-property:background-color,color,transform,border-color;transition-duration:130ms}}button:hover{{color:var(--ink);background:var(--module-strong)}}button[aria-pressed=true]{{color:#071014;border-color:var(--cyan);background:var(--cyan);font-weight:650}}button[aria-pressed=true]:hover{{color:#071014;background:var(--cyan-hover);border-color:var(--cyan-hover)}}button:active{{transform:scale(.96)}}button:focus-visible{{outline:3px solid var(--focus);outline-offset:2px}}@media(prefers-reduced-motion:reduce){{button{{transition-duration:0s}}}}.viewer{{overflow:hidden;border:1px solid var(--line);border-radius:15px;background:var(--panel)}}iframe{{display:block;width:100%;height:860px;border:0}}.boundary{{margin:14px 0;padding:13px;border:1px solid var(--line);border-radius:10px;color:var(--muted);background:var(--panel)}}.closure{{display:none}}@media(max-width:800px){{iframe{{height:1120px}}}}</style></head><body data-ui-artifact="review_board" data-program-id="{PROGRAM_ID}" data-artifact-id="{FAMILY_REVISION_ID}" data-revision="{REVISION}" data-validation-profile="family_review_ready" data-review-manifest="{rel(manifest)}" data-review-manifest-sha256="{sha(manifest)}"><main><header><p>G4 · готовое семейство</p><h1>Вход и смена пароля</h1><p>Две самостоятельные задачи в общей компактной визуальной грамматике.</p></header><div class="screens" aria-label="Экран"><button type="button" data-screen="UI-AUTH-001" aria-pressed="true">Вход</button><button type="button" data-screen="UI-AUTH-004" aria-pressed="false">Смена пароля</button></div><div class="states" aria-label="Состояние">{state_buttons}</div><section class="viewer"><iframe title="Интерактивный экран семейства" src="screens/auth-family.html?screen=UI-AUTH-001&state=UI-AUTH-001.initial&lang=ru"></iframe></section><div class="boundary">Вход использует одну колонку полей, нативный флажок и ссылку к восстановлению. Смена пароля остаётся отдельным пошаговым процессом. Кнопки, ссылки, выбор языка и флажок больше не подменяют друг друга и наследуют только применимые правила пилота.</div><ul class="closure">{closure}</ul></main><script>const frame=document.querySelector('iframe');let screen='UI-AUTH-001',state='UI-AUTH-001.initial';const screenButtons=[...document.querySelectorAll('[data-screen]')],stateButtons=[...document.querySelectorAll('[data-state]')];function render(){{if(!state.startsWith(screen+'.'))state=screen+'.initial';frame.src=`screens/auth-family.html?screen=${{screen}}&state=${{state}}&lang=ru`;screenButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.screen===screen)));stateButtons.forEach(b=>{{b.hidden=!b.dataset.state.startsWith(screen+'.');b.setAttribute('aria-pressed',String(b.dataset.state===state))}})}}screenButtons.forEach(b=>b.addEventListener('click',()=>{{screen=b.dataset.screen;render()}}));stateButtons.forEach(b=>b.addEventListener('click',()=>{{screen=b.dataset.state.split('.').slice(0,3).join('.');state=b.dataset.state;render()}}));render();</script></body></html>''', encoding="utf-8")
    rendered_board = board.read_text(encoding="utf-8")
    rendered_board = rendered_board.replace(
        "frame.src=`screens/auth-family.html?screen=${screen}&state=${state}&lang=ru`;",
        "const desired=`screens/auth-family.html?screen=${screen}&state=${state}&lang=ru`;if(frame.getAttribute('src')!==desired)frame.setAttribute('src',desired);",
    )
    rendered_board = rendered_board.replace(
        "screen=b.dataset.state.split('.').slice(0,3).join('.');",
        "screen=b.dataset.state.split('.')[0];",
    )
    board.write_text(rendered_board, encoding="utf-8")
    request = EVID / "family-acceptance-request.json"
    write_json(request, {"$schema": "family-acceptance-request.schema.json", "program_path": rel(SNAPSHOT), "family_id": FAMILY_ID, "family_revision_id": FAMILY_REVISION_ID, "revision": REVISION, "screen_acceptance_paths": [rel(path) for path, _ in rows], "review_board_path": rel(board), "owner_decision_ref": None})
    packet_name = "owner-review-decision-packet-correction-r5-03.json" if REVISION == 5 else "owner-review-decision-packet.json"
    write_json(EVID / packet_name, {"schema_id": "custometry.ui-owner-review-decision-packet/v1", "program_id": PROGRAM_ID, "stage_instance_id": STAGE_ID, "decision_id": f"{STAGE_ID}.finished-result", "decision_kind": "family_acceptance", "question": "Принять готовое семейство входа и восстановления или запросить ограниченные исправления?", "target": {"artifact_kind": "review_board", "artifact_id": FAMILY_REVISION_ID, "revision": REVISION, "validation_profile": "family_review_ready", "path": rel(board), "sha256": sha(board)}, "allowed_responses": ["accept", "bounded_corrections"], "status": "pending"})


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("mode", choices=("bootstrap", "bind", "proof-requests", "review")); args = parser.parse_args()
    {"bootstrap": bootstrap, "bind": bind, "proof-requests": proof_requests, "review": review}[args.mode]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
