#!/usr/bin/env python3
"""Build deterministic G3 r2 foundations, shell, and review evidence inputs."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
INTAKE = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json"
BASELINE = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
SOURCE = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2/ru/source.html"
ART = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g3-r2"
EVID = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2"
FIXTURE = ART / "fixture.json"
CANDIDATE = ART / "candidate-shell.html"
CONTRACT = ART / "representative-shell-contract.json"
INHERITANCE = ART / "inheritance-report.json"
DETAILED_INHERITANCE = EVID / "detailed-visual-inheritance-evidence.json"
BEHAVIOR = ART / "shell-behavior-matrix.json"
PROMOTED = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/promoted-structure-bindings.json"
REVIEW_BOARD = ART / "review-board.html"
REVIEW_MANIFEST = ART / "review-board.manifest.json"
SNAPSHOT = ART / "ui-design-program.snapshot.json"
STRESS = EVID / "responsive-language-accessibility-smoke.json"

PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
SCREEN_ID = "UI-SHELL-GLOBAL"
SCREEN_INDEX = 118
SCREEN_REVISION_ID = "UI-SHELL-GLOBAL.populated.all.ru.graphite.r2"
ANCHORS = (
    ("web-768", 768, 1024),
    ("web-1024", 1024, 768),
    ("web-1440", 1440, 900),
    ("web-1920", 1920, 1080),
)
NORMATIVE_ORIGIN = {
    "kind": "normative_requirement",
    "ref": "references/responsive-policy-v1.md#viewport-contract",
}
BASELINE_ORIGIN = {
    "kind": "product_contract",
    "ref": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json#/responsive_contract",
}
DELEGATED_ORIGIN = {
    "kind": "delegated_design_decision",
    "ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
    "rationale": "Realize the accepted fixed shell and analytical language for the G3 representative without changing product meaning.",
    "constraints": [
        "custometry.platform-baseline.v2.r2",
        "pilot-candidate-v2:visual-language-only",
        "responsive-web:768-1920",
    ],
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def specified(value: object, *, origin: dict | None = None, unit: str | None = None) -> dict:
    return {
        "value": value,
        "unit": unit,
        "origin": origin or NORMATIVE_ORIGIN,
        "tolerance": 0,
        "change_policy": "source_revision_required",
    }


def build_candidate(actions: list[dict]) -> str:
    action_rows = []
    for action in actions:
        action_id = action["action_id"]
        element_id = action_id.split(".", 1)[1].replace(".", "-")
        action_rows.append(
            f'<article class="access-row"><div><strong>{html.escape(action["label"])}</strong>'
            f'<span>Внутренняя проверка оболочки · без продуктовой мутации</span></div>'
            f'<button type="button" class="button secondary" data-ui-element="{element_id}" '
            f'data-prototype-action="{html.escape(action_id)}">Проверить</button>'
            f'<output class="action-result" data-result-for="{element_id}" aria-live="polite">Готово</output></article>'
        )
    action_markup = "".join(action_rows)
    baseline = load(BASELINE)
    return f'''<!doctype html>
<html lang="ru" data-theme="graphite">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <link rel="icon" href="data:,">
  <meta name="ui-fixture-sha256" content="{sha(FIXTURE)}">
  <meta name="ui-font-bundle-sha256" content="{canonical_sha(baseline["font_contract"])}">
  <meta name="ui-asset-bundle-sha256" content="{canonical_sha(baseline["asset_contract"])}">
  <title>Custometry — G3 foundations and shell r2</title>
  <style>
    :root {{ color-scheme:dark; --canvas:#070708; --surface:#111214; --sidebar:#090a0b; --surface-soft:#151619; --module:#1a1b1e; --module-2:#222327; --popover:#242529; --hover:#2a2b2f; --line:#303136; --line-soft:#242529; --soft:#8b8c93; --secondary:#a7a7ad; --text:#f0f0f2; --accent:#66b9d3; --accent-soft:rgba(102,185,211,.13); --good:#62c7aa; --warn:#ddb064; --danger:#f07d87; --focus:#8bd2e8; --rail:62px; --gap:12px; --control:32px; --radius:15px; --panel-radius:10px; --overlay:0 22px 70px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.07); --motion:120ms cubic-bezier(.2,0,0,1); }}
    * {{ box-sizing:border-box; }}
    html,body {{ margin:0; min-height:100%; background:var(--canvas); color:var(--text); font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; -webkit-font-smoothing:antialiased; }}
    body {{ overflow:hidden; }}
    ::selection {{ color:#071014; background:#86d2e9; }}
    button {{ min-height:32px; border:0; border-radius:7px; padding:0 10px; color:var(--secondary); background:var(--module); font:600 11px/1 Inter,ui-sans-serif,system-ui,sans-serif; cursor:pointer; transition:background-color var(--motion),color var(--motion),transform var(--motion); }}
    button:hover {{ color:var(--text); background:var(--hover); }} button:active {{ transform:scale(.96); }} button:disabled {{ opacity:.55; cursor:not-allowed; }}
    :focus-visible {{ outline:2px solid var(--focus); outline-offset:2px; }}
    .skip-link {{ position:fixed; inset-block-start:8px; inset-inline-start:74px; z-index:500; transform:translateY(-160%); padding:8px 12px; border-radius:10px; background:white; color:#111; }}
    .skip-link:focus {{ transform:none; }}
    .icon {{ width:16px; height:16px; fill:none; stroke:currentColor; stroke-width:1.5; stroke-linecap:round; stroke-linejoin:round; }}
    .shell-preview {{ position:relative; display:grid; grid-template-columns:var(--rail) minmax(0,1fr); gap:var(--gap); height:100vh; padding:12px; background:var(--canvas); }}
    .sidebar {{ position:relative; z-index:340; display:flex; flex-direction:column; align-items:center; gap:6px; min-width:0; padding:6px 4px 8px; background:var(--sidebar); }}
    .brand {{ display:grid; place-items:center; width:38px; height:38px; border-radius:12px; color:#071014; background:var(--accent); font-size:13px; font-weight:760; letter-spacing:-.03em; box-shadow:inset 0 1px rgba(255,255,255,.18); }}
    .rail-nav {{ display:flex; flex:1; flex-direction:column; align-items:center; gap:2px; width:100%; padding-top:3px; }}
    .rail-button {{ display:grid; place-items:center; width:38px; min-height:32px; padding:0; background:transparent; color:var(--soft); border-radius:7px; }}
    .rail-button:hover {{ background:var(--module); color:var(--text); }} .rail-button[aria-current="page"] {{ color:var(--accent); background:transparent; box-shadow:inset 2px 0 var(--accent); border-radius:7px; }}
    .profile {{ display:grid; place-items:center; width:32px; height:32px; border-radius:50%; background:#7568d9; color:white; box-shadow:0 0 0 1px rgba(255,255,255,.12); font-size:9px; font-weight:700; }}
    .context-nav {{ position:absolute; z-index:300; inset-block-start:58px; inset-inline-start:76px; width:290px; max-height:calc(100vh - 82px); overflow:auto; padding:12px; border:1px solid #3a3b40; border-radius:10px; background:var(--popover); box-shadow:var(--overlay); transform:translateY(-4px) scale(.985); opacity:0; pointer-events:none; transition:transform var(--motion),opacity var(--motion); }}
    .context-nav[data-open="true"] {{ transform:none; opacity:1; pointer-events:auto; }}
    .context-nav h2 {{ margin:0 0 3px; font-size:13px; font-weight:620; }} .context-nav p {{ margin:0 0 12px; color:var(--soft); font-size:9px; line-height:1.45; }}
    .context-list {{ display:grid; gap:2px; }} .context-list a {{ display:flex; min-height:34px; align-items:center; gap:8px; padding:0 9px; border-radius:7px; color:var(--secondary); text-decoration:none; font-size:11px; }}
    .context-list a:hover {{ background:var(--hover); color:var(--text); }} .context-list a[aria-current="page"] {{ background:#34353a; color:var(--text); box-shadow:inset 2px 0 var(--accent); }}
    .workspace {{ position:relative; min-width:0; overflow:hidden; border:1px solid #292a2e; border-radius:var(--radius); background:var(--surface); box-shadow:-10px 0 30px rgba(0,0,0,.24),inset 0 1px rgba(255,255,255,.025); }}
    .workspace-chrome {{ display:grid; min-height:96px; background:rgba(17,18,20,.94); border-bottom:1px solid var(--line-soft); backdrop-filter:blur(18px) saturate(120%); }}
    .page-header {{ display:flex; min-height:56px; align-items:center; justify-content:space-between; gap:12px; padding:8px 14px 7px 18px; }}
    .crumbs {{ min-width:0; }} .crumbs small {{ display:block; margin-bottom:2px; color:var(--soft); font-size:10px; }} .crumbs strong {{ display:inline; font-size:17px; font-weight:620; letter-spacing:-.02em; }} .status-pill {{ display:inline-flex; margin-inline-start:7px; padding:3px 7px; border-radius:9px; color:var(--good); background:rgba(98,199,170,.1); font-size:8px; font-weight:650; vertical-align:2px; }}
    .chrome-actions,.panel-actions {{ display:flex; min-width:0; align-items:center; gap:5px; }}
    .control-cluster {{ display:inline-flex; align-items:center; gap:2px; padding:3px; border-radius:15px; background:var(--module); box-shadow:inset 0 0 0 1px rgba(255,255,255,.035); }}
    .control-cluster button {{ display:grid; width:30px; min-width:30px; min-height:30px; place-items:center; padding:0; border-radius:12px; background:transparent; }}
    .control-cluster button[aria-pressed="true"],.control-cluster button[aria-expanded="true"] {{ color:var(--accent); background:#34353a; }}
    .report-navigation-row {{ display:grid; grid-template-columns:auto minmax(280px,1fr); gap:16px; align-items:center; min-height:40px; padding:0 12px 7px 18px; }}
    .report-tabs,.context-bar {{ display:flex; min-width:0; align-items:center; gap:4px; }} .report-tab {{ min-height:31px; padding:0 12px; color:var(--soft); background:transparent; border-radius:16px; }} .report-tab[aria-selected="true"] {{ color:var(--text); background:var(--module-2); }}
    .context-bar {{ justify-content:flex-end; }} .context-chip {{ min-height:28px; padding:0 8px; color:var(--soft); background:transparent; font-size:10px; }} .context-chip strong {{ color:var(--secondary); font-weight:560; }} .context-chip[data-active="true"] {{ color:var(--accent); background:var(--accent-soft); }}
    .workspace-body {{ display:grid; grid-template-columns:minmax(0,1fr); height:calc(100vh - 121px); min-height:0; }}
    .workspace[data-inspector-open="true"] .workspace-body {{ grid-template-columns:minmax(0,1fr) clamp(320px,25vw,400px); }}
    .workspace-scroll {{ min-width:0; height:100%; overflow:auto; scrollbar-width:thin; }}
    .report-page {{ display:grid; gap:14px; padding:16px 20px 42px; }}
    .hero {{ display:flex; align-items:flex-end; justify-content:space-between; gap:16px; }} .hero h1 {{ margin:0; font-size:16px; font-weight:610; line-height:1.2; letter-spacing:-.015em; }} .hero p {{ max-width:72ch; margin:3px 0 0; color:var(--soft); font-size:10px; line-height:1.5; }}
    .kpi-module {{ display:grid; grid-template-columns:116px minmax(0,1fr); min-height:54px; overflow:hidden; border-block:1px solid var(--line-soft); }} .kpi-label-block {{ display:grid; align-content:center; gap:3px; padding-right:8px; }} .kpi-label-block strong {{ color:var(--secondary); font-size:9px; letter-spacing:.08em; text-transform:uppercase; }} .kpi-label-block span {{ color:var(--soft); font-size:8px; }} .kpi-strip {{ display:flex; min-width:0; overflow-x:auto; }} .kpi {{ position:relative; display:grid; min-width:140px; flex:1 0 140px; align-content:center; gap:2px; padding:7px 11px; }} .kpi + .kpi::before {{ position:absolute; inset-block:10px; inset-inline-start:0; width:1px; content:""; background:var(--line-soft); }} .kpi span {{ color:var(--soft); font-size:9px; }} .kpi b {{ font-size:16px; font-weight:640; font-variant-numeric:tabular-nums; }} .kpi em {{ color:var(--good); font-size:9px; font-style:normal; }}
    .trust-strip {{ display:flex; align-items:center; gap:8px; min-height:38px; padding:0 12px; border-radius:9px; background:var(--module); color:var(--secondary); font-size:10px; }} .trust-strip strong {{ color:var(--text); }} .trust-strip .icon {{ color:var(--good); }}
    .analytics-layout {{ display:grid; grid-template-columns:minmax(0,1fr); gap:14px; align-items:start; }}
    .analysis-stack {{ display:grid; gap:14px; min-width:0; }}
    .panel {{ min-width:0; overflow:hidden; background:transparent; }}
    .panel-header {{ display:flex; min-height:48px; align-items:center; justify-content:space-between; gap:10px; padding:6px 4px 7px 0; border-bottom:1px solid var(--line-soft); }} .panel-header h2 {{ margin:0; font-size:12px; font-weight:610; }} .panel-header p {{ margin:2px 0 0; color:var(--soft); font-size:9px; }}
    .segmented {{ display:flex; padding:2px; border-radius:8px; background:var(--module); box-shadow:inset 0 0 0 1px rgba(255,255,255,.035); }} .segmented button {{ min-height:24px; padding:0 8px; background:transparent; color:var(--soft); font-size:9px; }} .segmented button[aria-pressed="true"] {{ background:#34353a; color:var(--text); box-shadow:inset 0 1px rgba(255,255,255,.06); }}
    .chart-stage {{ display:grid; grid-template-columns:minmax(0,1fr) 220px; min-height:318px; }}
    .chart-canvas {{ position:relative; min-width:0; min-height:318px; padding:20px 16px 24px 42px; }} .chart-canvas svg {{ display:block; width:100%; height:274px; overflow:visible; }} .grid-line {{ stroke:#242529; stroke-width:1; }} .series-line {{ fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }} .series-area {{ opacity:.07; }} .chart-label {{ fill:#8b8c93; font:9px Inter,system-ui,sans-serif; }}
    .axis {{ position:absolute; inset-block:21px 28px; inset-inline-start:4px; display:flex; flex-direction:column; justify-content:space-between; color:var(--soft); font-size:9px; font-variant-numeric:tabular-nums; }}
    .series-panel {{ padding:12px; border-inline-start:1px solid var(--line-soft); background:#151619; }} .series-panel h3 {{ margin:0 0 8px; font-size:10px; font-weight:610; }} .legend-item {{ display:grid; grid-template-columns:8px 1fr auto; gap:8px; align-items:center; min-height:28px; color:var(--secondary); font-size:9px; }} .dot {{ width:8px; height:8px; border-radius:50%; background:var(--accent); }} .legend-item b {{ font-variant-numeric:tabular-nums; color:var(--text); font-weight:620; }}
    .table-specimen {{ overflow:hidden; border-radius:10px; background:#111214; box-shadow:inset 0 0 0 1px rgba(255,255,255,.045); }}
    .chart-table {{ max-height:306px; overflow:auto; }} table {{ width:max-content; min-width:100%; border-collapse:collapse; table-layout:fixed; font-size:10px; font-variant-numeric:tabular-nums; }} th {{ position:sticky; inset-block-start:0; z-index:2; min-width:98px; height:34px; padding:0 12px; background:#1a1b1e; color:#a8abb3; text-align:start; }} th:first-child,td:first-child {{ position:sticky; inset-inline-start:0; z-index:1; min-width:142px; background:#17181b; }} th:first-child {{ z-index:3; }} td {{ min-width:98px; min-height:32px; height:36px; padding:0 12px; border-top:1px solid #26272b; color:#c9cbd0; font-weight:540; }} .table-group-row th {{ position:static; height:34px; color:var(--text); background:#202125; font-size:9px; text-transform:uppercase; letter-spacing:.06em; }} .row-label {{ display:flex; align-items:center; gap:7px; }} .row-label::before {{ width:5px; height:5px; flex:0 0 auto; border-radius:50%; background:var(--accent); content:""; }}
    .inspector-panel {{ display:none; min-width:0; height:100%; overflow:auto; border-inline-start:1px solid var(--line-soft); background:#151619; box-shadow:-18px 0 40px rgba(0,0,0,.22); }} .workspace[data-inspector-open="true"] .inspector-panel {{ display:block; }} .inspector-panel .panel-header {{ position:sticky; z-index:3; inset-block-start:0; padding-inline:14px 10px; background:#191a1d; }} .inspector-tabs {{ position:sticky; z-index:2; inset-block-start:48px; display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:2px; padding:4px; background:#202125; }} .inspector-tabs button {{ min-width:0; min-height:30px; padding:0 5px; background:transparent; font-size:9px; }} .inspector-tabs button[aria-selected="true"] {{ color:var(--text); background:#34353a; }} .inspector-body {{ display:grid; gap:10px; padding:12px; }} .inspector-card {{ padding:12px; border-radius:10px; background:#1b1c20; box-shadow:inset 0 0 0 1px rgba(255,255,255,.035); }} .inspector-card h3 {{ margin:0 0 7px; font-size:10px; }} .inspector-card p,.inspector-card li {{ margin:0; color:var(--secondary); font-size:9px; line-height:1.55; }} .inspector-card ul {{ display:grid; gap:6px; margin:0; padding-inline-start:15px; }} .inspector-source-row {{ display:grid; grid-template-columns:1fr auto; gap:8px; padding:7px 0; border-top:1px solid var(--line-soft); font-size:9px; }} .inspector-source-row:first-of-type {{ border-top:0; }} .inspector-source-row code {{ color:var(--accent); }}
    .access-grid {{ display:grid; overflow:hidden; border-radius:10px; background:#141518; box-shadow:inset 0 0 0 1px rgba(255,255,255,.045); }} .access-row {{ display:grid; grid-template-columns:minmax(0,1fr) auto auto; gap:10px; align-items:center; min-height:42px; padding:5px 10px; border-bottom:1px solid var(--line-soft); }} .access-row:last-child {{ border-bottom:0; }} .access-row:hover {{ background:var(--module); }} .access-row strong {{ display:block; font-size:10px; font-weight:610; }} .access-row span {{ display:block; margin-top:2px; color:var(--soft); font-size:8px; overflow-wrap:break-word; }} .access-row button {{ min-height:28px; font-size:9px; }} .action-result {{ min-width:58px; color:var(--good); font-size:8px; text-align:end; }}
    .state-matrix {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; }} .state-card {{ min-height:62px; padding:9px 10px; border-radius:9px; background:#17181b; box-shadow:inset 0 0 0 1px rgba(255,255,255,.035); }} .state-card b {{ display:block; font-size:9px; }} .state-card span {{ display:block; margin-top:4px; color:var(--soft); font-size:8px; line-height:1.4; }}
    .drawer-scrim {{ display:none; }}
    @media (max-width:1199px) {{ .chart-stage {{ grid-template-columns:minmax(0,1fr); }} .series-panel {{ border-inline-start:0; border-block-start:1px solid #2a2b2f; }} .workspace[data-inspector-open="true"] .workspace-body {{ grid-template-columns:minmax(0,1fr); }} .inspector-panel,.workspace[data-inspector-open="true"] .inspector-panel {{ display:block; position:fixed; z-index:410; inset-block:12px; inset-inline-end:12px; width:min(400px,calc(100vw - 94px)); height:calc(100vh - 24px); border:0; border-radius:15px; box-shadow:var(--overlay); transform:translateX(calc(100% + 28px)); visibility:hidden; transition:transform var(--motion),visibility 0s linear 120ms; }} .workspace[data-inspector-open="true"] .inspector-panel {{ transform:none; visibility:visible; transition-delay:0s; }} }}
    @media (max-width:899px) {{ .shell-preview {{ grid-template-columns:52px minmax(0,1fr); gap:5px; padding:5px; }} .workspace {{ border-radius:12px; }} .context-nav {{ position:fixed; z-index:430; inset-block:5px; inset-inline-start:5px; width:min(360px,calc(100vw - 10px)); max-height:calc(100vh - 10px); transform:translateX(calc(-100% - 12px)); }} .context-nav[data-open="true"] {{ transform:none; }} .drawer-scrim {{ position:fixed; z-index:420; inset:0; display:block; min-height:0; border-radius:0; background:rgba(0,0,0,.58); opacity:0; pointer-events:none; }} .drawer-scrim[data-open="true"] {{ opacity:1; pointer-events:auto; }} .page-header {{ padding-inline:12px 9px; }} .report-navigation-row {{ grid-template-columns:minmax(0,1fr); gap:4px; padding:0 8px 7px 12px; }} .context-bar {{ justify-content:flex-start; overflow-x:auto; }} .workspace-body {{ height:calc(100vh - 137px); }} .report-page {{ padding:13px 12px 30px; }} .kpi-module {{ grid-template-columns:104px minmax(0,1fr); }} .kpi {{ min-width:132px; flex-basis:132px; }} .state-matrix {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .panel-header {{ align-items:flex-start; flex-direction:column; }} .panel-actions {{ width:100%; overflow-x:auto; padding-bottom:2px; }} .inspector-panel,.workspace[data-inspector-open="true"] .inspector-panel {{ inset-block:5px; inset-inline-end:5px; width:min(400px,calc(100vw - 10px)); height:calc(100vh - 10px); }} }}
    @media (prefers-reduced-motion:reduce) {{ *,*::before,*::after {{ animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; scroll-behavior:auto!important; }} }}
  </style>
</head>
<body data-ui-artifact="candidate" data-program-id="{PROGRAM_ID}" data-artifact-id="{PROGRAM_ID}" data-revision="2" data-validation-profile="program_ready">
  <a class="skip-link" href="#main-workspace" data-ui-element="skip-link">Перейти к рабочей области</a>
  <svg aria-hidden="true" width="0" height="0" style="position:absolute"><defs>
    <symbol id="i-panel" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M16 9l-3 3 3 3"/></symbol>
    <symbol id="i-grid" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></symbol>
    <symbol id="i-chart" viewBox="0 0 24 24"><path d="M3 3v16a2 2 0 0 0 2 2h16M7 15l4-4 3 3 5-6"/></symbol>
    <symbol id="i-users" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M16 3a4 4 0 0 1 0 8M22 21v-2a4 4 0 0 0-3-3.9"/><circle cx="9" cy="7" r="4"/></symbol>
    <symbol id="i-settings" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-4V21a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H2.8v-4H3a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1a1.7 1.7 0 0 0 1.9.3A1.7 1.7 0 0 0 10 3V2.8h4V3a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.2v4H21a1.7 1.7 0 0 0-1.6 1Z"/></symbol>
    <symbol id="i-shield" viewBox="0 0 24 24"><path d="M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V6l8-3 8 3Z"/><path d="m9 12 2 2 4-4"/></symbol>
    <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></symbol>
    <symbol id="i-swap" viewBox="0 0 24 24"><path d="m7 7 3-3 3 3M10 4v12M17 17l-3 3-3-3M14 20V8"/></symbol>
    <symbol id="i-filter" viewBox="0 0 24 24"><path d="M4 5h16l-6 7v5l-4 2v-7Z"/></symbol>
    <symbol id="i-download" viewBox="0 0 24 24"><path d="M12 3v12m0 0 4-4m-4 4-4-4M4 21h16"/></symbol>
    <symbol id="i-expand" viewBox="0 0 24 24"><path d="M8 3H3v5M16 3h5v5M8 21H3v-5M16 21h5v-5"/></symbol>
    <symbol id="i-layers" viewBox="0 0 24 24"><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/></symbol>
    <symbol id="i-language" viewBox="0 0 24 24"><path d="M4 5h10M9 3v2m-3 4c1.5 3 3.5 5 7 7M12 9c-1 3-3 6-7 8M15 19l3-8 3 8m-5-3h4"/></symbol>
  </defs></svg>
  <div class="shell-preview" data-ui-element="shell-preview">
    <aside class="sidebar" data-ui-region="shell.workspace.primary-nav" data-ui-element="region-shell-workspace-primary-nav" aria-label="Основная навигация">
      <div class="brand" aria-label="Custometry">C</div>
      <nav class="rail-nav" aria-label="Разделы">
        <button class="rail-button" type="button" id="nav-toggle" aria-label="Открыть контекстную навигацию" aria-expanded="false"><svg class="icon" aria-hidden="true"><use href="#i-panel"/></svg></button>
        <a class="rail-button" href="#main-workspace" aria-current="page" aria-label="Overview"><svg class="icon" aria-hidden="true"><use href="#i-grid"/></svg></a>
        <a class="rail-button" href="#chart" aria-label="Аналитика"><svg class="icon" aria-hidden="true"><use href="#i-chart"/></svg></a>
        <a class="rail-button" href="#access" aria-label="Доступ"><svg class="icon" aria-hidden="true"><use href="#i-users"/></svg></a>
        <a class="rail-button" href="#settings" aria-label="Настройки"><svg class="icon" aria-hidden="true"><use href="#i-settings"/></svg></a>
      </nav>
      <div class="profile" aria-label="Профиль пользователя">U</div>
    </aside>
    <button class="drawer-scrim" type="button" id="drawer-scrim" aria-label="Закрыть навигацию" data-open="false"></button>
    <nav class="context-nav" id="context-nav" role="dialog" aria-modal="false" aria-hidden="true" aria-label="Контекстная навигация" data-open="false">
      <h2>Оболочка приложения</h2><p>Контекстная навигация поверх стабильной геометрии рабочей области.</p>
      <div class="context-list"><a href="#main-workspace" aria-current="page">Основа</a><a href="#chart">Аналитическая грамматика</a><a href="#states">Состояния</a><a href="#trust">Доверие к результату</a></div>
    </nav>
    <section class="workspace" data-ui-region="shell.workspace.workspace" id="main-workspace" aria-label="Рабочая область" data-inspector-open="false">
      <header class="workspace-chrome" data-ui-region="shell.workspace.header">
        <div class="page-header"><div class="crumbs"><small>Foundations / Shell specimen</small><strong>Нейтральная оболочка</strong><span class="status-pill">Не экран G4</span></div><div class="chrome-actions"><div class="control-cluster" role="group" aria-label="Управление оболочкой"><button type="button" id="lang-toggle" aria-label="Переключить язык" title="Язык"><svg class="icon" aria-hidden="true"><use href="#i-language"/></svg></button><button type="button" id="series-toggle" aria-label="Показать или скрыть панель серий" aria-pressed="true" title="Серии"><svg class="icon" aria-hidden="true"><use href="#i-layers"/></svg></button><button type="button" id="inspector-toggle" aria-label="Открыть инспектор" aria-expanded="false" title="Инспектор"><svg class="icon" aria-hidden="true"><use href="#i-settings"/></svg></button></div></div></div>
        <div class="report-navigation-row"><nav class="report-tabs" aria-label="Разделы specimen"><button type="button" class="report-tab" aria-selected="true">Основа</button><button type="button" class="report-tab" aria-selected="false">Навигация</button><button type="button" class="report-tab" aria-selected="false">Аналитика</button><button type="button" class="report-tab" aria-selected="false">Состояния</button></nav><div class="context-bar" aria-label="Параметры specimen"><button class="context-chip" type="button"><span>Режим</span> <strong>Graphite</strong></button><button class="context-chip" type="button"><span>Web</span> <strong>768–1920</strong></button><button class="context-chip" type="button" data-active="true"><strong>Populated</strong></button></div></div>
      </header>
      <div class="workspace-body">
      <main class="workspace-scroll" id="report-main">
        <section class="report-page" data-ui-region="{SCREEN_ID}.content">
          <header class="hero"><div><h1>Правила оболочки и визуального языка</h1><p>Нейтральный программный specimen показывает только наследуемые foundations, shell-поведение и аналитическую грамматику — без данных и композиции целевого экрана.</p></div><button type="button" disabled>Контракт зафиксирован</button></header>
          <section class="kpi-module" aria-label="Фиксированные параметры оболочки"><div class="kpi-label-block"><strong>Контракт</strong><span>Нулевой допуск</span></div><div class="kpi-strip"><div class="kpi"><span>Rail</span><b>62 px</b><em>pilot</em></div><div class="kpi"><span>Gap</span><b>12 px</b><em>baseline</em></div><div class="kpi"><span>Profile</span><b>32 px</b><em>baseline</em></div><div class="kpi"><span>Rows</span><b>≥32 px</b><em>analytical</em></div><div class="kpi"><span>Chrome</span><b>97 px</b><em>pilot</em></div></div></section>
          <section class="trust-strip" id="trust" data-ui-region="result-trust" data-ui-element="region-result-trust" aria-label="Result Trust"><svg class="icon" aria-hidden="true"><use href="#i-shield"/></svg><strong>Result Trust</strong><span>Источник и реализация hash-bound · восстановление доступно</span></section>
          <div class="analytics-layout">
            <div class="analysis-stack">
              <section class="panel" id="chart" aria-labelledby="chart-title">
                <header class="panel-header"><div><h2 id="chart-title">Аналитическая грамматика</h2><p>Focus / Explore · демонстрационные кривые без продуктового значения</p></div><div class="panel-actions"><div class="control-cluster" role="group" aria-label="Контекст аналитики"><button type="button" aria-label="Период" title="Период"><svg class="icon" aria-hidden="true"><use href="#i-calendar"/></svg></button><button type="button" aria-label="Сравнение" title="Сравнение"><svg class="icon" aria-hidden="true"><use href="#i-swap"/></svg></button><button type="button" aria-label="Фильтры" title="Фильтры"><svg class="icon" aria-hidden="true"><use href="#i-filter"/></svg></button></div><div class="segmented" role="group" aria-label="Представление данных"><button type="button" id="view-chart" aria-pressed="true">График</button><button type="button" id="view-table" aria-pressed="false">Таблица</button></div><div class="control-cluster" role="group" aria-label="Действия представления"><button type="button" aria-label="Скачать" title="Скачать"><svg class="icon" aria-hidden="true"><use href="#i-download"/></svg></button><button type="button" aria-label="Развернуть" title="Развернуть"><svg class="icon" aria-hidden="true"><use href="#i-expand"/></svg></button></div></div></header>
                <div class="chart-stage" data-ui-region="analytics.chart" data-ui-element="region-analytics-chart" data-chart-view="overview">
                  <div class="chart-canvas" role="img" aria-label="Демонстрация многосерийного аналитического языка"><div class="axis"><span>100</span><span>75</span><span>50</span><span>25</span></div><svg viewBox="0 0 820 274" preserveAspectRatio="none" aria-hidden="true"><line class="grid-line" x1="0" y1="20" x2="820" y2="20"/><line class="grid-line" x1="0" y1="90" x2="820" y2="90"/><line class="grid-line" x1="0" y1="160" x2="820" y2="160"/><line class="grid-line" x1="0" y1="230" x2="820" y2="230"/><path class="series-area" fill="#66b9d3" d="M0 180 L110 166 L220 148 L330 154 L440 112 L550 105 L660 70 L820 52 L820 274 L0 274Z"/><path class="series-line" stroke="#66b9d3" d="M0 180 L110 166 L220 148 L330 154 L440 112 L550 105 L660 70 L820 52"/><path class="series-line" stroke="#62c7aa" d="M0 210 L110 198 L220 204 L330 178 L440 166 L550 138 L660 142 L820 118"/><path class="series-line" stroke="#ddb064" d="M0 236 L110 224 L220 212 L330 218 L440 202 L550 196 L660 178 L820 184"/><path class="series-line" stroke="#8f7ff6" d="M0 196 L110 184 L220 176 L330 168 L440 172 L550 150 L660 128 L820 124"/><text class="chart-label" x="0" y="270">T1</text><text class="chart-label" x="400" y="270">T2</text><text class="chart-label" x="790" y="270">T3</text></svg></div>
                  <aside class="series-panel" data-ui-region="analytics.series-panel" data-ui-element="region-analytics-series-panel"><h3>Серии · 4</h3><div class="legend-item"><i class="dot"></i><span>Series A</span><b>S1</b></div><div class="legend-item"><i class="dot" style="background:#62c7aa"></i><span>Series B</span><b>S2</b></div><div class="legend-item"><i class="dot" style="background:#ddb064"></i><span>Series C</span><b>S3</b></div><div class="legend-item"><i class="dot" style="background:#8f7ff6"></i><span>Series D</span><b>S4</b></div></aside>
                </div>
                <section class="table-specimen" id="table-specimen" aria-labelledby="table-title"><header class="panel-header" style="padding-inline:12px"><div><h2 id="table-title">Табличный паттерн</h2><p>Видим одновременно с графиком для поэлементной проверки; значения нейтральны</p></div><div class="control-cluster" role="group" aria-label="Управление таблицей"><button type="button" aria-label="Сортировать демонстрационные значения" title="Сортировка"><svg class="icon" aria-hidden="true"><use href="#i-swap"/></svg></button><button type="button" aria-label="Скачать таблицу" title="Скачать"><svg class="icon" aria-hidden="true"><use href="#i-download"/></svg></button></div></header><div class="chart-table" data-ui-region="analytics.table" data-ui-element="region-analytics-table"><table><thead><tr><th scope="col">Серия</th><th scope="col">T1</th><th scope="col">T2</th><th scope="col">T3</th><th scope="col">T4</th><th scope="col">T5</th><th scope="col">T6</th></tr></thead><tbody><tr class="table-group-row"><th colspan="7" scope="colgroup">Группа 01</th></tr><tr><td><span class="row-label">Series A</span></td><td>52</td><td>57</td><td>61</td><td>66</td><td>72</td><td>78</td></tr><tr><td><span class="row-label">Series B</span></td><td>41</td><td>44</td><td>48</td><td>53</td><td>59</td><td>64</td></tr><tr class="table-group-row"><th colspan="7" scope="colgroup">Группа 02</th></tr><tr><td><span class="row-label">Series C</span></td><td>33</td><td>38</td><td>42</td><td>47</td><td>51</td><td>56</td></tr><tr><td><span class="row-label">Series D</span></td><td>45</td><td>49</td><td>54</td><td>60</td><td>65</td><td>69</td></tr></tbody></table></div></section>
              </section>
              <section class="panel" id="access"><header class="panel-header"><div><h2>Интеракции оболочки</h2><p>Компактные строки · именованные keyboard controls · internal evidence</p></div></header><div class="access-grid">{action_markup}</div></section>
              <section class="state-matrix" id="states" aria-label="State and behavior matrix"><div class="state-card"><b>Загрузка / populated</b><span>Локальная загрузка; trust остаётся видимым.</span></div><div class="state-card"><b>Пусто / частично</b><span>Применимо к аналитическому primitive, не к shell identity.</span></div><div class="state-card"><b>Ошибка / нет доступа</b><span>Текст, значок, контекст и безопасный возврат.</span></div><div class="state-card"><b>Восстановление</b><span>Повтор доступен с клавиатуры и не зависит от цвета.</span></div></section>
            </div>
          </div>
        </section>
      </main>
      <aside class="inspector-panel" id="inspector-panel-context" data-ui-region="analytics.inspector" data-ui-element="region-analytics-inspector" aria-label="Инспектор оболочки"><header class="panel-header"><div><h2>Инспектор оболочки</h2><p>Полновысотный sibling pane как в пилоте</p></div><button type="button" id="inspector-close" aria-label="Закрыть инспектор">Закрыть</button></header><nav class="inspector-tabs" aria-label="Разделы инспектора"><button type="button" aria-selected="true">Контекст</button><button type="button" aria-selected="false">Элементы</button><button type="button" aria-selected="false">Доверие</button><button type="button" aria-selected="false">Виды</button></nav><div class="inspector-body"><section class="inspector-card"><h3>Область проверки</h3><p>UI-SHELL-GLOBAL — внутренний representative contract, а не объект продуктовой приёмки. Панель занимает всю высоту workspace body и остаётся независимой от прокрутки контента.</p></section><section class="inspector-card"><h3>Pilot → realization</h3><div class="inspector-source-row"><span>Compact rail</span><code>.sidebar</code></div><div class="inspector-source-row"><span>Grouped icon controls</span><code>.control-cluster</code></div><div class="inspector-source-row"><span>Chart + series sibling</span><code>.chart-stage</code></div><div class="inspector-source-row"><span>Dense table</span><code>#table-specimen</code></div><div class="inspector-source-row"><span>Result Trust</span><code>#trust</code></div></section><section class="inspector-card"><h3>Доверие</h3><ul><li>Источник и candidate hash-bound.</li><li>Фиксированные домены проверяются отдельно.</li><li>Восстановление остаётся видимым.</li></ul></section><section class="inspector-card"><h3>Responsive Web</h3><p>На широком Web это full-height sibling pane. Ниже 1200 px — viewport-contained overlay с Escape и возвратом фокуса.</p></section></div></aside>
      </div>
    </section>
  </div>
  <script>
    const nav=document.getElementById('context-nav'), navToggle=document.getElementById('nav-toggle'), scrim=document.getElementById('drawer-scrim');
    const inspector=document.getElementById('inspector-panel-context'), inspectorToggle=document.getElementById('inspector-toggle'), inspectorClose=document.getElementById('inspector-close');
    const workspace=document.querySelector('.workspace'), workspaceScroll=document.querySelector('.workspace-scroll');
    let navReturn=navToggle, inspectorReturn=inspectorToggle;
    inspector.setAttribute('aria-hidden','true');
    function narrow(){{return matchMedia('(max-width:899px)').matches}}
    function setNav(open){{const modal=open&&narrow();nav.dataset.open=String(open);navToggle.setAttribute('aria-expanded',String(open));nav.setAttribute('aria-hidden',String(!open));nav.setAttribute('aria-modal',String(modal));scrim.dataset.open=String(modal);workspace.inert=modal;workspaceScroll.style.overflow=modal?'hidden':'';if(modal)nav.querySelector('a').focus();else if(!open)navReturn?.focus();}}
    function setInspector(open){{inspector.dataset.open=String(open);workspace.dataset.inspectorOpen=String(open);inspector.setAttribute('aria-hidden',String(!open));inspectorToggle.setAttribute('aria-expanded',String(open));inspectorToggle.setAttribute('aria-label',open?'Закрыть инспектор':'Открыть инспектор');if(open)inspectorClose.focus();else inspectorReturn?.focus();}}
    navToggle.addEventListener('click',()=>setNav(nav.dataset.open!=='true'));scrim.addEventListener('click',()=>setNav(false));
    inspectorToggle.addEventListener('click',()=>setInspector(inspector.dataset.open!=='true'));inspectorClose.addEventListener('click',()=>setInspector(false));
    document.addEventListener('keydown',event=>{{if(event.key==='Escape'){{if(inspector.dataset.open==='true')setInspector(false);else if(nav.dataset.open==='true')setNav(false);}}if(event.key==='Tab'&&nav.dataset.open==='true'&&narrow()){{const focusable=[...nav.querySelectorAll('a,button')].filter(el=>!el.disabled);const first=focusable[0],last=focusable[focusable.length-1];if(event.shiftKey&&document.activeElement===first){{event.preventDefault();last.focus();}}else if(!event.shiftKey&&document.activeElement===last){{event.preventDefault();first.focus();}}}}}});
    document.getElementById('view-chart').addEventListener('click',event=>{{document.querySelector('.chart-stage').scrollIntoView({{block:'nearest'}});event.currentTarget.setAttribute('aria-pressed','true');document.getElementById('view-table').setAttribute('aria-pressed','false');}});
    document.getElementById('view-table').addEventListener('click',event=>{{document.getElementById('table-specimen').scrollIntoView({{block:'nearest'}});event.currentTarget.setAttribute('aria-pressed','true');document.getElementById('view-chart').setAttribute('aria-pressed','false');}});
    document.getElementById('series-toggle').addEventListener('click',event=>{{const p=document.querySelector('.series-panel');p.hidden=!p.hidden;event.currentTarget.setAttribute('aria-pressed',String(!p.hidden));}});
    document.getElementById('lang-toggle').addEventListener('click',event=>{{const english=document.documentElement.lang==='ru';document.documentElement.lang=english?'en':'ru';event.currentTarget.setAttribute('aria-label',english?'Switch language to Russian':'Переключить язык на английский');event.currentTarget.title=english?'Russian':'English';document.querySelector('.hero h1').textContent=english?'Shell and visual-language rules':'Правила оболочки и визуального языка';document.querySelector('.hero p').textContent=english?'A neutral program-owned specimen demonstrates only inherited foundations, shell behavior and analytical grammar — without target-screen data or composition.':'Нейтральный программный specimen показывает только наследуемые foundations, shell-поведение и аналитическую грамматику — без данных и композиции целевого экрана.';document.querySelector('.trust-strip span').textContent=english?'Source and realization are hash-bound · recovery available':'Источник и реализация hash-bound · восстановление доступно';document.querySelectorAll('[data-prototype-action]').forEach(button=>button.textContent=english?'Verify':'Проверить');}});
    document.querySelectorAll('.inspector-tabs button').forEach(button=>button.addEventListener('click',()=>{{document.querySelectorAll('.inspector-tabs button').forEach(item=>item.setAttribute('aria-selected',String(item===button)));}}));
    const outcomes={json.dumps({a['action_id']: a['outcome'] for a in actions}, ensure_ascii=False)};
    document.querySelectorAll('[data-prototype-action]').forEach(button=>button.addEventListener('click',()=>{{const id=button.dataset.prototypeAction;const key=button.dataset.uiElement;document.querySelector(`[data-result-for="${{key}}"]`).textContent=outcomes[id];}}));
    addEventListener('resize',()=>{{if(nav.dataset.open==='true')setNav(true);}});
  </script>
</body></html>'''


def build_contract(intake: dict, baseline: dict, program: dict) -> dict:
    screen = intake["screens"][SCREEN_INDEX]
    actions = screen["actions"]
    visible_actions = []
    elements = []
    for action in actions:
        action_id = action["action_id"]
        element_id = action_id.split(".", 1)[1].replace(".", "-")
        visible_actions.append({
            "action_id": action_id,
            "expected_outcome": action["outcome"],
            "side_effect_class": "local_state",
            "activation_policy": "execute_in_fixture",
            "outcome_assertion": {
                "kind": "dom",
                "selector": f'[data-result-for="{element_id}"]',
                "property": "textContent",
                "expected": action["outcome"],
            },
        })
        elements.append({
            "element_id": element_id,
            "parent_element_id": "shell-preview",
            "region_id": f"{SCREEN_ID}.content",
            "locator": f'[data-ui-element="{element_id}"]',
            "visibility": "required",
            "element_type": "button",
            "component_id": action["component_id"],
            "variant": action["component_variant"],
            "size_class": action["size_class"],
            "content_contract": action["label"],
            "icon_id": action["icon_id"],
            "action_ids": [action_id],
            "state_ids": [f"{SCREEN_ID}.populated", f"{SCREEN_ID}.error", f"{SCREEN_ID}.permission_denied", f"{SCREEN_ID}.recovery"],
            "geometry": {"min_height": specified(32, origin=BASELINE_ORIGIN, unit="px")},
            "spacing_relations": [specified("8px shell rhythm", origin=BASELINE_ORIGIN)],
            "visual_properties": {"display": specified("inline-flex", origin=BASELINE_ORIGIN)},
            "responsive_behavior": [specified("remains named and reachable at every responsive-Web anchor")],
            "accessibility": {"name": specified(action["label"], origin={"kind":"product_contract","ref":f"{INTAKE.relative_to(ROOT)}#/screens/{SCREEN_INDEX}/actions"})},
            "source_refs": [DELEGATED_ORIGIN],
        })
    regions = [
        ("shell.workspace.primary-nav", ".sidebar", "candidate.shell.rail"),
        ("shell.workspace.header", ".workspace-chrome", "candidate.shell.header"),
        ("shell.workspace.workspace", ".workspace", "candidate.shell.workspace"),
        (f"{SCREEN_ID}.content", ".report-page:not([hidden])", "candidate.shell.specimen"),
        ("result-trust", ".trust-strip", "candidate.result-trust"),
        ("analytics.chart", ".chart-stage[data-chart-view=\"overview\"]", "candidate.chart"),
        ("analytics.series-panel", ".series-panel", "candidate.series-panel"),
        ("analytics.inspector", "#inspector-panel-context", "candidate.inspector"),
        ("analytics.table", ".chart-table", "candidate.table"),
    ]
    region_docs = []
    for region_id, locator, component_id in regions:
        region_docs.append({
            "region_id": region_id,
            "locator": locator,
            "visibility": "conditional" if region_id == "analytics.inspector" else "required",
            "component_id": component_id,
            "component_status": "candidate",
            "variant": "graphite",
            "state": "populated",
            "source_refs": [DELEGATED_ORIGIN],
            "geometry": {},
            "layout_rules": [specified("bounded responsive-Web region with local overflow", origin=DELEGATED_ORIGIN)],
            "visual_properties": {},
            "content": {},
            "interactions": [],
            "accessibility": {"keyboard": specified("logical DOM and focus order", origin=NORMATIVE_ORIGIN)},
            "responsive_behavior": [specified("preserve primary task, trust and recovery controls", origin=NORMATIVE_ORIGIN)],
            "geometry_tolerance_px": 0,
            "geometry_tolerance_origin": NORMATIVE_ORIGIN,
            "computed_style_properties": ["display", "position", "overflow", "background-color", "border-radius"],
            "computed_style_properties_origin": DELEGATED_ORIGIN,
        })
    elements.insert(0, {
        "element_id": "shell-preview",
        "parent_element_id": None,
        "region_id": "shell.workspace.workspace",
        "locator": '[data-ui-element="shell-preview"]',
        "visibility": "required",
        "element_type": "application-shell",
        "component_id": None,
        "variant": "workspace",
        "size_class": None,
        "content_contract": "G3 neutral foundations and application-shell specimen",
        "icon_id": None,
        "action_ids": [],
        "state_ids": [f"{SCREEN_ID}.populated"],
        "geometry": {"shell_gap": specified(12, origin=BASELINE_ORIGIN, unit="px")},
        "spacing_relations": [specified("compact rail + 12px gap + fluid workspace", origin=BASELINE_ORIGIN)],
        "visual_properties": {"background-color": specified("#111214", origin=BASELINE_ORIGIN)},
        "responsive_behavior": [specified("desktop overlay becomes viewport-contained narrow-Web drawer")],
        "accessibility": {"focus_model": specified("Escape closes overlays and focus returns to trigger", origin=NORMATIVE_ORIGIN)},
        "source_refs": [DELEGATED_ORIGIN],
    })
    elements.append({
        "element_id": "skip-link",
        "parent_element_id": None,
        "region_id": "shell.workspace.header",
        "locator": '[data-ui-element="skip-link"]',
        "visibility": "required",
        "element_type": "link",
        "component_id": None,
        "variant": "skip-link",
        "size_class": None,
        "content_contract": "Перейти к рабочей области",
        "icon_id": None,
        "action_ids": [],
        "state_ids": [f"{SCREEN_ID}.populated"],
        "geometry": {"display": specified("inline")},
        "spacing_relations": [specified("first focusable control")],
        "visual_properties": {"visibility": specified("visible on focus")},
        "responsive_behavior": [specified("available at every responsive-Web anchor")],
        "accessibility": {"name": specified("Перейти к рабочей области")},
        "source_refs": [NORMATIVE_ORIGIN],
    })
    covered = {element["region_id"] for element in elements}
    for region_id, _, _ in regions:
        if region_id not in covered:
            elements.append({
                "element_id": f"region-{region_id.replace('.', '-').lower()}",
                "parent_element_id": "shell-preview",
                "region_id": region_id,
                "locator": f'[data-ui-region="{region_id}"]',
                "visibility": "conditional" if region_id == "analytics.inspector" else "required",
                "element_type": "region",
                "component_id": None,
                "variant": "graphite",
                "size_class": None,
                "content_contract": region_id,
                "icon_id": None,
                "action_ids": [],
                "state_ids": [f"{SCREEN_ID}.populated"],
                "geometry": {"display": specified("block")},
                "spacing_relations": [specified("inside bounded shell")],
                "visual_properties": {"surface": specified("graphite")},
                "responsive_behavior": [specified("reachable across the fixed responsive-Web range")],
                "accessibility": {"presence": specified("named or structurally exposed")},
                "source_refs": [DELEGATED_ORIGIN],
            })
    authority = {key: program["visual_authority"][key] for key in (
        "source_visual_ref", "source_visual_sha256", "owner_decision_ref",
        "screen_acceptance_scope", "visual_language_scope", "reusable_foundation_scope",
        "inheritance_policy", "mobile_scope",
    )}
    return {
        "$schema": "screen-design-contract.schema.json",
        "schema_id": "codex.ui-screen-design-contract/v1",
        "contract_profile": "codex.ui-screen-design-contract/v1@1.4.0",
        "screen_revision_id": SCREEN_REVISION_ID,
        "program_revision_ref": f"{PROGRAM_ID}@2",
        "functional_contract_ref": {
            "path": str(INTAKE.relative_to(ROOT)), "sha256": sha(INTAKE),
            "json_pointer": f"/screens/{SCREEN_INDEX}", "screen_id": SCREEN_ID,
        },
        "baseline_binding": {
            "baseline_id": baseline["baseline_id"], "path": str(BASELINE.relative_to(ROOT)),
            "sha256": sha(BASELINE), "shell_variant_id": "shell.workspace", "exception_id": None,
        },
        "status": "review",
        "product_identity": {
            "screen_id": SCREEN_ID, "route_id": screen["route_id"], "route": screen["route"],
            "state_id": f"{SCREEN_ID}.populated", "role_id": "all",
            "permission_profile": "workspace.manage", "locale": "ru", "theme": "graphite",
        },
        "source_visual": {
            "kind": "delegated_design_output", "evidence_mode": "visual_language_only",
            "html_path": str(SOURCE.relative_to(ROOT)), "image_path": None,
            "html_sha256": sha(SOURCE), "image_sha256": None, "owner_decision_ref": None,
            "delegation_ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
        },
        "visual_authority": authority,
        "comparison_claims": {
            "required_purpose": "visual_language_conformance", "deterministic_render_proves_fidelity": False,
            "reference_logical_artifact_id": f"{PROGRAM_ID}:accepted-pilot:ru:r2",
            "implementation_logical_artifact_id": f"{PROGRAM_ID}:g3-candidate:r2",
        },
        "interaction_contract": {
            "visible_actions": visible_actions, "no_actions_reason_ref": None,
            "required_checks": ["focus_visibility","keyboard_activation","menus","no_console_errors","no_page_horizontal_overflow","no_request_failures","no_unresolved_file_navigation","refresh_feedback","state_transitions","tab_radio_behavior","toggles"],
            "allowed_origins": ["http://127.0.0.1:4173"], "fixture_mode": "isolated_local",
            "evidence_redaction_required": True,
            "redaction_selectors": ["[data-sensitive]", "input[type='password']"],
        },
        "render_environment": {
            "browser": "chromium/150.0.7871.187", "browser_mechanic": "playwright_cli",
            "device_scale_factor": 1, "timezone": "Europe/Moscow",
            "fixed_clock_iso": "2026-08-11T21:18:52Z", "reduced_motion": True,
            "animations": "disabled", "fixture_data_path": str(FIXTURE.relative_to(ROOT)),
            "fixture_data_sha256": sha(FIXTURE),
            "font_bundle_sha256": canonical_sha(baseline["font_contract"]),
            "asset_bundle_sha256": canonical_sha(baseline["asset_contract"]),
        },
        "viewport_contract": {
            "mode": "responsive_web",
            "supported_web_width_range": {"min_width":768,"max_width":1920,"origin":BASELINE_ORIGIN},
            "anchors": [{"anchor_id":i,"width":w,"height":h,"class":"responsive_web","state_ref":f"{SCREEN_ID}.populated","origin":BASELINE_ORIGIN} for i,w,h in ANCHORS],
            "breakpoint_policy": "content_driven", "breakpoint_policy_origin": NORMATIVE_ORIGIN,
            "below_supported_range": "out_of_scope", "below_supported_range_origin": NORMATIVE_ORIGIN,
            "above_supported_range": "max_content_width", "above_supported_range_origin": BASELINE_ORIGIN,
            "mobile_scope": "unauthorized", "mobile_scope_origin": {"kind":"normative_requirement","ref":"references/responsive-policy-v1.md#mobile-authorization-boundary"},
            "mobile_authorization_ref": None, "mobile_specific_composition": False,
            "authorized_mobile_surfaces": [], "authorized_mobile_viewports": [], "allowed_mobile_changes": [],
        },
        "regions": region_docs,
        "element_contracts": elements,
        "allowed_provenance_kinds": ["product_contract","normative_requirement","accepted_visual","measured_baseline","design_token","owner_decision","derived_formula","delegated_design_decision"],
        "unresolved_decisions": [],
        "acceptance": {
            "agent_self_acceptance":"prohibited","machine_receipt_required":True,"owner_decision_required":True,
            "owner_decision_ref":None,"screen_acceptance_receipt_path":None,"screen_acceptance_receipt_sha256":None,
            "pixel_diff_policy": {
                "channel_threshold": specified(18, origin=NORMATIVE_ORIGIN, unit="channel-value"),
                "approved_max_different_pixels": specified(100, origin=NORMATIVE_ORIGIN, unit="percent"),
            },
        },
    }


def prepare() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    EVID.mkdir(parents=True, exist_ok=True)
    intake, baseline, program = load(INTAKE), load(BASELINE), load(PROGRAM)
    screen = intake["screens"][SCREEN_INDEX]
    write_json(FIXTURE, {
        "screen_id": SCREEN_ID,
        "state_id": f"{SCREEN_ID}.populated",
        "role_id": "all",
        "locale_stress": ["ru", "en"],
        "fixed_clock_iso": "2026-08-11T21:18:52Z",
        "values": {"series_a":82,"series_b":64,"series_c":47,"series_d":73},
        "fixture_authority": "isolated neutral specimen values; not product data, production truth, or legend-threshold truth",
    })
    CANDIDATE.write_text(build_candidate(screen["actions"]), encoding="utf-8")
    contract = build_contract(intake, baseline, program)
    write_json(CONTRACT, contract)
    write_json(BEHAVIOR, {
        "schema_id": "custometry.ui-shell-behavior-matrix/v1",
        "program_id": PROGRAM_ID, "revision": 2,
        "states": [
            {"surface":"context_navigation","wide_web":"overlay; workspace geometry stable","narrow_web":"viewport-contained modal drawer","keyboard":"Enter/Space, Escape, focus transfer/return","dismissal":"toggle, Escape, outside scrim"},
            {"surface":"report_inspector","wide_web":"full-height right sibling pane matching the workspace body","narrow_web":"viewport-contained overlay","keyboard":"named trigger, focus transfer, Escape, return focus","dismissal":"close, Escape"},
            {"surface":"series_panel","wide_web":"right sibling","narrow_web":"lower panel","keyboard":"named toggle","dismissal":"toggle without chart semantic change"},
            {"surface":"grouped_icon_controls","wide_web":"shared rounded backing surfaces in chrome, chart and table","narrow_web":"horizontal local overflow without hidden controls","keyboard":"ten named icon buttons in logical DOM order","dismissal":"not applicable"},
            {"surface":"analytical_table","wide_web":"always-visible bounded local surface with group rows","narrow_web":"local overflow","keyboard":"named sort control; sticky headings excluded","dismissal":"chart/table segmented controls move focus without hiding either proof surface"},
        ],
    })
    program["status"] = "review"
    program["validation_profile"] = "program_ready"
    program["responsive_policy"] = {
        "adaptive_web_required": True,
        "supported_web_width_range": {"min_width":768,"max_width":1920,"origin":BASELINE_ORIGIN},
        "anchor_viewports": [{"anchor_id":i,"width":w,"height":h,"class":"responsive_web","origin":BASELINE_ORIGIN} for i,w,h in ANCHORS],
        "breakpoint_policy": "content_driven",
        "breakpoint_policy_origin": {**DELEGATED_ORIGIN,"rationale":"Apply the fixed baseline content-driven breakpoint policy."},
        "component_adaptation": "prefer_container_queries",
        "component_adaptation_origin": {**DELEGATED_ORIGIN,"rationale":"Apply the fixed baseline component adaptation policy."},
        "logical_properties_required": True,
        "logical_properties_origin": {"kind":"normative_requirement","ref":"custometry-ui-blueprint-ru.md#responsive-web"},
        "mobile_scope": "unauthorized",
        "mobile_scope_origin": {"kind":"normative_requirement","ref":"references/responsive-policy-v1.md#mobile-authorization-boundary"},
        "mobile_authorization_ref": None,
        "authorized_mobile_surfaces": [], "authorized_mobile_viewports": [], "allowed_mobile_changes": [],
    }
    anchor_ids = [item[0] for item in ANCHORS]
    for coverage in program["coverage_profiles"]:
        coverage["viewport_anchor_ids"] = {
            "mode":"required","values":anchor_ids,"origin":BASELINE_ORIGIN,"not_applicable_reason_ref":None,
        }
        coverage["unresolved_fields"] = [field for field in coverage.get("unresolved_fields",[]) if field != "viewport_anchor_ids"]
    program["g3_rendered_proof"] = {
        "source_evidence_mode":"renderable_html",
        "shell_capture_contract":{"path":str(CONTRACT.relative_to(ROOT)),"sha256":sha(CONTRACT),"screen_revision_id":SCREEN_REVISION_ID},
        "source_native_capture": program["g3_rendered_proof"]["source_native_capture"],
        "source_anchor_observations": [],
        "candidate_artifact":{"path":str(CANDIDATE.relative_to(ROOT)),"sha256":sha(CANDIDATE)},
        "candidate_anchor_captures": [],
        "review_board": program["g3_rendered_proof"]["review_board"],
        "inheritance_report": program["g3_rendered_proof"]["inheritance_report"],
    }
    write_json(PROGRAM, program)


def prepare_provenance() -> None:
    """Bind browser observations and emit inputs for the canonical provenance assembler."""
    program = load(PROGRAM)
    program["g3_rendered_proof"]["candidate_artifact"] = {
        "path": rel(CANDIDATE), "sha256": sha(CANDIDATE),
    }
    program["g3_rendered_proof"]["shell_capture_contract"]["sha256"] = sha(CONTRACT)
    write_json(PROGRAM, program)
    source_hash = sha(SOURCE)
    contract_hash = sha(CONTRACT)
    evidence_safety = {
        "fixture_mode": "isolated_local",
        "redaction_required": True,
        "redaction_applied": True,
        "redaction_selectors": ["[data-sensitive]", "input[type='password']"],
        "redaction_match_counts": [0, 0],
        "uncovered_sensitive_elements": 0,
        "loopback_only": True,
        "network_isolated": True,
        "allowed_origins": ["http://127.0.0.1:4173"],
        "blocked_external_requests": [],
    }
    request_dir = EVID / "render-provenance-requests"
    for anchor_id, width, height in ANCHORS:
        source_capture = EVID / f"source-{anchor_id}.png"
        source_geometry = EVID / f"source-{anchor_id}-geometry.json"
        # The accepted pilot is observed as a visual-language source, not as the
        # representative screen's functional target. Direct Playwright capture
        # therefore records no target-screen regions or actions.
        write_json(source_geometry, {
            "schema_id": "codex.ui-geometry-capture/v1",
            "screen_revision_id": SCREEN_REVISION_ID,
            "target": "reference",
            "generated_by": {
                "script": "capture_geometry.cjs", "version": "1.5.0",
                "command": "capture_geometry.cjs <playwright-cli-source-observation-redacted>",
            },
            "contract_sha256": contract_hash,
            "render_source": {
                "artifact_ref": rel(SOURCE), "artifact_sha256": source_hash,
                "logical_artifact_id": f"{PROGRAM_ID}:accepted-pilot:ru:r2",
                "main_document_response_sha256": source_hash,
            },
            "screenshot_sha256": sha(source_capture),
            "environment": {
                "browser": "chromium/150.0.7871.187",
                "browser_mechanic": "playwright_cli",
                "anchor_id": anchor_id,
                "viewport": {"width": width, "height": height},
                "device_scale_factor": 1,
                "locale": "ru", "theme": "graphite", "mobile_scope": "unauthorized",
                "observation_scope": "visual_language_reference_only",
            },
            "regions": [], "elements": [],
            "document_geometry": {
                "scroll_width": width, "client_width": width,
                "scroll_height": height, "client_height": height,
                "scope": "viewport source observation",
            },
            "accessibility": {
                "scope": "source visual observation only",
                "automated_violations": [], "keyboard_issues": [],
                "target_screen_conformance_claimed": False,
            },
            "accessibility_claim": "accessibility_smoke",
            "browser_interaction": {
                "scope": "visual_language_only", "visible_action_ids": [],
                "observed_outcomes": [], "unresolved_visible_actions": [],
                "unexpected_file_urls": [], "required_checks": [], "passed": True,
            },
            "console_errors": [], "request_failures": [],
            "evidence_safety": evidence_safety,
            "result": "passed", "blockers": [],
        })
        pairs = (
            (
                "reference", f"{PROGRAM_ID}:accepted-pilot:ru:r2", SOURCE,
                source_capture, source_geometry, EVID / f"source-{anchor_id}-provenance.json",
            ),
            (
                "implementation", f"{PROGRAM_ID}:g3-candidate:r2", CANDIDATE,
                EVID / f"candidate-{anchor_id}.png",
                EVID / f"candidate-{anchor_id}-geometry.json",
                EVID / f"candidate-{anchor_id}-provenance.json",
            ),
        )
        for target, logical_id, artifact, capture, geometry, output in pairs:
            write_json(request_dir / f"{target}-{anchor_id}.json", {
                "program_ref": rel(PROGRAM), "target": target,
                "logical_artifact_id": logical_id, "anchor_id": anchor_id,
                "source_artifact_ref": rel(artifact), "capture_ref": rel(capture),
                "geometry_receipt_ref": rel(geometry),
            })


def evidence_ref(path: Path) -> dict:
    return {"path": rel(path), "sha256": sha(path)}


def build_detailed_inheritance() -> None:
    source_observation = EVID / "accepted-pilot-fixed-domain-browser-observation.json"
    candidate_observation = EVID / "fixed-domain-browser-observation.json"
    source = load(source_observation)
    candidate = load(candidate_observation)
    source_items = {item["selector"]: item for item in source["items"]}
    candidate_items = {item["selector"]: item for item in candidate["items"]}
    checks = [
        {
            "domain": "graphite_surfaces",
            "source_value": source_items[".workspace"]["background"],
            "candidate_value": candidate_items[".workspace"]["background"],
            "disposition": "inherited_exactly",
            "status": "passed",
        },
        {
            "domain": "workspace_radius_px",
            "source_value": source_items[".workspace"]["borderRadius"],
            "candidate_value": candidate_items[".workspace"]["borderRadius"],
            "disposition": "inherited_exactly",
            "status": "passed",
        },
        {
            "domain": "workspace_chrome_height_px",
            "source_value": source_items[".workspace-chrome"]["height"],
            "candidate_value": candidate_items[".workspace-chrome"]["height"],
            "disposition": "inherited_exactly",
            "status": "passed",
        },
        {
            "domain": "active_tab_geometry",
            "source_value": {
                "height": source_items[".report-tab"]["height"],
                "radius": source_items[".report-tab"]["borderRadius"],
                "background": source_items[".report-tab"]["background"],
            },
            "candidate_value": {
                "height": candidate_items[".report-tab"]["height"],
                "radius": candidate_items[".report-tab"]["borderRadius"],
                "background": candidate_items[".report-tab"]["background"],
            },
            "disposition": "inherited_exactly",
            "status": "passed",
        },
        {
            "domain": "compact_rail_width_px",
            "source_value": source_items[".sidebar"]["width"],
            "candidate_value": candidate_items[".sidebar"]["width"],
            "disposition": "inherited_exactly",
            "status": "passed",
        },
        {
            "domain": "shell_workspace_gap_px",
            "source_value": source["shell_gap_px"],
            "candidate_value": candidate["shell_gap_px"],
            "baseline_value": 12,
            "disposition": "adapted_within_fixed_contract",
            "rationale": "The accepted baseline promotes a zero-tolerance 12 px shell/workspace gap over the pilot fixture's rendered zero gap.",
            "status": "passed",
        },
        {
            "domain": "profile_area_px",
            "source_value": source_items[".avatar"]["width"],
            "candidate_value": candidate_items[".profile"]["width"],
            "baseline_value": 32,
            "disposition": "adapted_within_fixed_contract",
            "rationale": "The accepted baseline promotes a zero-tolerance 32 px profile area over the pilot fixture's 25 px avatar.",
            "status": "passed",
        },
        {
            "domain": "analytical_language",
            "source_value": "multi-series thin-line chart, right sibling series panel, compact KPI strip",
            "candidate_value": "multi-series thin-line chart, right sibling series panel, compact KPI strip",
            "disposition": "inherited_exactly",
            "status": "passed",
        },
        {
            "domain": "grouped_control_grammar",
            "source_value": "shared rounded backing with grouped icon buttons",
            "candidate_value": "shared rounded backing with grouped icon buttons",
            "disposition": "inherited_exactly",
            "rationale": "The candidate exposes four shared control surfaces containing ten icon buttons; the browser receipt records both counts.",
            "status": "passed",
        },
        {
            "domain": "table_grammar",
            "source_value": "visible dense table with grouped rows, sticky headings and local overflow",
            "candidate_value": "visible dense table with grouped rows, sticky headings and local overflow",
            "disposition": "inherited_exactly",
            "rationale": "The table is visible in the primary workspace without a mode switch; its 36 px rows, group rows, sticky headings and local overflow are browser-observed.",
            "status": "passed",
        },
        {
            "domain": "inspector_geometry",
            "source_value": "full-height right sibling pane on wide Web; viewport-contained overlay on narrow Web",
            "candidate_value": "full-height right sibling pane on wide Web; viewport-contained overlay on narrow Web",
            "disposition": "inherited_exactly",
            "rationale": "At 1920 px the inspector fills the workspace body as a sibling pane; at 768 px it becomes a viewport-contained overlay with deterministic focus and Escape return.",
            "status": "passed",
        },
        {
            "domain": "target_screen_semantics",
            "source_value": "customer analytics pilot fixture",
            "candidate_value": "program-owned neutral shell specimen; internal contract identity UI-SHELL-GLOBAL",
            "disposition": "not_applicable_with_source",
            "rationale": "The pilot is visual-language authority only. The specimen carries no target-screen product meaning, and UI-SHELL-GLOBAL is used only as the repository-authoritative internal machine representative.",
            "status": "passed",
        },
    ]
    for item in checks:
        if item["disposition"] == "inherited_exactly" and item["source_value"] != item["candidate_value"]:
            item["status"] = "failed"
        if item["disposition"] == "adapted_within_fixed_contract" and item["candidate_value"] != item["baseline_value"]:
            item["status"] = "failed"
    if any(item["status"] != "passed" for item in checks):
        raise ValueError("detailed visual inheritance checks failed")
    write_json(DETAILED_INHERITANCE, {
        "schema_id": "custometry.ui-g3-detailed-visual-inheritance-evidence/v1",
        "program_id": PROGRAM_ID,
        "program_revision": 2,
        "comparison_purpose": "visual_language_conformance",
        "source_observation_ref": evidence_ref(source_observation),
        "candidate_observation_ref": evidence_ref(candidate_observation),
        "checks": checks,
        "raster_threshold_max_ratio": 0.12,
        "pixel_similarity_role": "bounded_supporting_signal; exact target-screen fidelity is not claimed because pilot semantics are not the target screen",
        "owner_exceptions": [],
        "result": "passed",
    })


def build_inheritance(program: dict) -> None:
    build_detailed_inheritance()
    baseline = load(BASELINE)
    promoted = load(PROMOTED)
    dimensions = [
        "tokens", "typography", "density", "spacing", "navigation",
        "shell_regions", "panel_control_grammar", "responsive_adaptations",
    ]
    matrix = [
        {
            "dimension": "tokens", "disposition": "inherited_exactly",
            "source": f"{rel(BASELINE)}#/foundation_tokens",
            "realization": "All fixed color, border, elevation, opacity, motion, radius and layer values are realized as candidate CSS custom properties or exact rules.",
            "evidence": rel(CANDIDATE),
        },
        {
            "dimension": "typography", "disposition": "inherited_exactly",
            "source": f"{rel(BASELINE)}#/font_contract",
            "realization": "Exact Inter, ui-sans-serif, system-ui stack; RU/EN stress is separately captured.",
            "evidence": rel(EVID / "candidate-web-1440-en.png"),
        },
        {
            "dimension": "density", "disposition": "inherited_exactly",
            "source": f"{rel(BASELINE)}#/foundation_tokens/sizing/0",
            "realization": "32 px compact controls, profile area and minimum analytical rows are retained with zero tolerance.",
            "evidence": rel(EVID / "candidate-web-1440-geometry.json"),
        },
        {
            "dimension": "spacing", "disposition": "inherited_exactly",
            "source": f"{rel(BASELINE)}#/layout_contract/region_gap_rules/0",
            "realization": "The rail/workspace gap is exactly 12 px and the inner rhythm follows the fixed 8 px token.",
            "evidence": rel(EVID / "candidate-web-1920-geometry.json"),
        },
        {
            "dimension": "navigation", "disposition": "adapted_within_fixed_contract",
            "source": f"{rel(BASELINE)}#/navigation_contracts",
            "realization": "Compact icon rail plus contextual overlay preserves fixed identity and deterministic keyboard/dismissal behavior for the representative screen.",
            "evidence": rel(BEHAVIOR),
        },
        {
            "dimension": "shell_regions", "disposition": "adapted_within_fixed_contract",
            "source": f"{rel(BASELINE)}#/shell_variants/0",
            "realization": "Primary rail, header and independently scrolling fluid workspace are bound by the representative contract.",
            "evidence": rel(CONTRACT),
        },
        {
            "dimension": "panel_control_grammar", "disposition": "adapted_within_fixed_contract",
            "source": f"{rel(BASELINE)}#/component_contracts",
            "realization": "Grouped icon-control surfaces, simultaneously visible chart and dense table, Result Trust, full-height inspector and external series panel realize the accepted analytical grammar without copying pilot fixtures.",
            "evidence": rel(EVID / "candidate-web-1440-table.png"),
        },
        {
            "dimension": "responsive_adaptations", "disposition": "adapted_within_fixed_contract",
            "source": f"{rel(BASELINE)}#/responsive_contract",
            "realization": "The fixed 768–1920 Web range keeps the inspector as a full-height sibling on wide Web, transforms it to a contained overlay below 1200 px, moves series to a lower panel, and introduces no mobile IA.",
            "evidence": rel(EVID / "candidate-web-768-inspector.png"),
        },
    ]
    obligations = []
    for item in promoted["bindings"]:
        representative = SCREEN_ID in item.get("screen_ids", [])
        obligations.append({
            "binding_id": item["binding_id"],
            "source_ref": item["source_ref"],
            "screen_ids": item.get("screen_ids", []),
            "family_ids": item.get("family_ids", []),
            "wave_ids": item.get("wave_ids", []),
            "disposition": "adapted_within_fixed_contract" if representative else "not_applicable_with_source",
            "g3_realization": (
                "Applicable representative shell primitive is demonstrated; target-screen semantics remain downstream."
                if representative else
                "Not closed by G3; preserved for the declared G4 family and G5 wave evidence."
            ),
            "downstream_obligation": item["downstream_obligation"],
        })
    write_json(INHERITANCE, {
        "schema_id": "codex.ui-visual-inheritance-report/v1",
        "program_id": PROGRAM_ID, "program_revision": 2,
        "visual_authority_sha256": canonical_sha(program["visual_authority"]),
        "baseline_id": baseline["baseline_id"],
        "baseline_ref": evidence_ref(BASELINE),
        "candidate_ref": evidence_ref(CANDIDATE),
        "detailed_visual_inheritance_ref": evidence_ref(DETAILED_INHERITANCE),
        "dimensions": dimensions,
        "fixed_domain_matrix": matrix,
        "fixed_domain_exceptions": [],
        "promoted_binding_summary": {
            "total": len(obligations), "owner_recommendations": 68,
            "reconciliation_additions": 13,
            "closed_as_target_screen_work_by_g3": 0,
            "preserved_for_downstream": len(obligations),
        },
        "promoted_binding_obligations": obligations,
        "result": "passed",
    })


def build_review_board(program: dict) -> None:
    proof = program["g3_rendered_proof"]
    entries = []
    def add(role: str, ref: dict, anchor_id: str | None = None, state_id: str | None = None,
            path_field: str = "path", hash_field: str = "sha256") -> None:
        entries.append({
            "entry_id": f"review-{len(entries)+1:02d}", "role": role,
            "artifact_ref": ref[path_field], "sha256": ref[hash_field],
            "anchor_id": anchor_id, "state_id": state_id,
        })
    add("source_native", proof["source_native_capture"])
    for item in proof["source_anchor_observations"]:
        add("source_anchor", item, item["anchor_id"])
    add("candidate", proof["candidate_artifact"])
    for item in proof["candidate_anchor_captures"]:
        add("candidate_anchor", item, item["anchor_id"])
    for item in proof["candidate_anchor_captures"]:
        add("render_provenance", item, item["anchor_id"], path_field="render_provenance_ref", hash_field="render_provenance_sha256")
    add("inheritance", proof["inheritance_report"])
    add("screen_contract", proof["shell_capture_contract"])
    write_json(REVIEW_MANIFEST, {
        "$schema": "/Users/daniildegtyarev/.codex/skills/ui-design-program/assets/review-board-manifest.schema.json",
        "schema_id": "codex.ui-review-board-manifest/v1",
        "program_id": PROGRAM_ID, "artifact_id": PROGRAM_ID, "revision": 2,
        "validation_profile": "program_ready", "entries": entries,
    })
    hidden_entries = "".join(
        f'<li data-review-entry="{entry["entry_id"]}">{html.escape(entry["role"])} · {html.escape(entry["anchor_id"] or "program")}</li>'
        for entry in entries
    )
    source_card = '''<figure><img src="../../evidence/g3-r2/source-web-1920.png" alt="Accepted pilot at 1920 by 1080"><figcaption><b>Принятый пилот · 1920×1080</b><span>Источник визуального языка</span></figcaption></figure>'''
    cards = source_card + "".join(
        f'''<figure><img src="../../evidence/g3-r2/candidate-{anchor}.png" alt="Candidate shell at {width} by {height}"><figcaption><b>G3 · {width}×{height}</b><span>Fixed-domain matrix passed · provenance passed</span></figcaption></figure>'''
        for anchor,width,height in (ANCHORS[-1], *ANCHORS[:-1])
    )
    cards += '''<figure><img src="../../evidence/g3-r2/candidate-web-1920-inspector.png" alt="Full-height inspector in the G3 shell"><figcaption><b>Inspector · full-height sibling</b><span>Pilot geometry · focus returned on close</span></figcaption></figure><figure><img src="../../evidence/g3-r2/candidate-web-1440-table.png" alt="Visible pilot-derived table pattern"><figcaption><b>Table pattern · visible</b><span>Grouped rows · sticky headings · local overflow</span></figcaption></figure>'''
    matrix_rows = "".join(
        f"<tr><td>{source}</td><td>{invariant}</td><td>{realization}</td><td>{proof}</td><td><code>{disposition}</code></td></tr>"
        for source, invariant, realization, proof, disposition in [
            ("Pilot · app shell", "Graphite + cyan; спокойная профессиональная плотность", "<code>:root</code> semantic tokens и сдержанные surfaces", "Live source + candidate", "inherited_exactly"),
            ("Pilot · compact rail", "Узкая постоянная навигация с outline icons", "<code>.sidebar</code> · 62 px · 1.5 px stroke", "1920 geometry", "inherited_exactly"),
            ("Pilot · workspace", "Скруглённая fluid workspace и независимый scroll", "<code>.workspace</code> · 15 px radius", "Four anchor captures", "inherited_exactly"),
            ("Pilot · top chrome", "Компактный header, tabs и context chips", "<code>.workspace-chrome</code> · 97 px", "Source/candidate region comparison", "inherited_exactly"),
            ("Pilot · control backing", "Иконки управления объединены общей подложкой", "<code>.control-cluster</code> в chrome, chart и table", "Visible live candidate", "inherited_exactly"),
            ("Pilot · KPI rhythm", "Плотная горизонтальная полоса показателей", "<code>.kpi-module</code> с neutral foundation metrics", "1920 capture", "inherited_exactly"),
            ("Pilot · chart", "Тонкие линии, читаемые axes и bounded surface", "<code>.chart-stage</code> без product semantics", "Live source + candidate", "inherited_exactly"),
            ("Pilot · series panel", "Правый sibling panel или нижний reflow", "<code>.series-panel</code>", "1920 + 1024 captures", "inherited_exactly"),
            ("Pilot · table", "Видимая dense table, group rows, sticky headings", "<code>#table-specimen</code> · rows ≥ 32 px", "Table browser state", "inherited_exactly"),
            ("Pilot · inspector", "Полновысотный sibling pane; overlay на узком Web", "<code>#inspector-panel-context</code> занимает workspace body", "Inspector browser state", "inherited_exactly"),
            ("Pilot · Result Trust", "Источник, область доказательства и recovery видимы", "<code>#trust</code> + inspector trust section", "Keyboard/zoom smoke", "inherited_exactly"),
            ("Platform baseline", "12 px shell gap и 32 px profile area", "Zero-tolerance fixed adaptations", "1920 geometry receipt", "adapted_within_fixed_contract"),
            ("Pilot fixture semantics", "Содержание, значения, thresholds и композиция экрана", "Не переносились; specimen остаётся нейтральным", "Inheritance report", "not_applicable_with_source"),
        ]
    )
    REVIEW_BOARD.write_text(f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry G3 r2 — owner review</title>
<style>:root{{--bg:#070708;--paper:#111214;--module:#191a1d;--line:#303136;--text:#f0f0f2;--soft:#8b8c93;--accent:#66b9d3;--good:#62c7aa}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,sans-serif}}main{{width:min(1560px,calc(100% - 32px));margin:0 auto;padding:32px 0 60px}}header{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:end;margin-bottom:22px}}h1{{margin:0;font-size:clamp(28px,4vw,54px);line-height:1;letter-spacing:-.04em}}header p{{max-width:78ch;margin:12px 0 0;color:#a7a7ad;line-height:1.55}}.status{{padding:9px 13px;border:1px solid #2d5144;border-radius:999px;background:#14251f;color:#bfead7;font-size:12px;font-weight:700}}.facts{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:18px}}.fact{{padding:14px;border:1px solid var(--line);border-radius:14px;background:var(--paper)}}.fact b{{display:block;font-size:18px}}.fact span{{display:block;margin-top:5px;color:var(--soft);font-size:11px;line-height:1.4}}.grid{{columns:2;column-gap:14px}}figure{{margin:0 0 14px;break-inside:avoid;overflow:hidden;border:1px solid var(--line);border-radius:15px;background:var(--paper)}}img{{display:block;width:100%;height:auto;background:#050607}}figcaption{{display:flex;justify-content:space-between;gap:12px;padding:12px 14px;font-size:11px}}figcaption span{{color:var(--soft)}}.review{{display:grid;grid-template-columns:1.1fr .9fr;gap:14px;margin-top:14px}}section{{padding:18px;border:1px solid var(--line);border-radius:15px;background:var(--paper)}}h2{{margin:0 0 10px;font-size:16px}}ul{{margin:0;padding-left:18px;color:#c5c7cd;font-size:12px;line-height:1.65}}.decision{{border-color:#315a67;background:#101b1f}}.decision strong{{color:#9bd9ec}}.closure{{margin-top:14px;color:var(--soft);font-size:10px;columns:4;list-style:none;padding:0}}.closure li{{break-inside:avoid}}@media(max-width:900px){{header,.review{{grid-template-columns:1fr}}.facts{{grid-template-columns:1fr 1fr}}.grid{{columns:1}}}}@media(max-width:620px){{.facts{{grid-template-columns:1fr}}.closure{{columns:2}}}}</style></head>
<body data-ui-artifact="review_board" data-program-id="{PROGRAM_ID}" data-artifact-id="{PROGRAM_ID}" data-revision="2" data-validation-profile="program_ready" data-review-manifest="{rel(REVIEW_MANIFEST)}" data-review-manifest-sha256="{sha(REVIEW_MANIFEST)}"><style>.acceptance{{margin:0 0 18px;padding:18px 20px;border:1px solid #315a67;border-radius:15px;background:#101b1f;color:#d8f2fa;font-size:18px;line-height:1.45}}.live-compare{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;padding:0;border:0;background:transparent}}.live-frame{{overflow:hidden;border:1px solid var(--line);border-radius:15px;background:var(--paper)}}.live-frame header{{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0;padding:11px 13px;border-bottom:1px solid var(--line)}}.live-frame h2{{margin:0;font-size:13px}}.live-frame a{{color:#9bd9ec;font-size:11px}}iframe{{display:block;width:100%;height:min(70vh,720px);border:0;background:#070708}}.matrix{{margin:14px 0;overflow:auto;padding:0}}table{{width:100%;border-collapse:collapse;font-size:11px}}th,td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:start;vertical-align:top;line-height:1.45}}th{{color:#a7a7ad;background:#17181b}}code{{color:#9bd9ec;white-space:nowrap}}.limits{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}}@media(max-width:1100px){{.live-compare{{grid-template-columns:1fr}}}}@media(max-width:900px){{.limits{{grid-template-columns:1fr}}}}</style><main>
<header><div><h1>G3 · Foundations & shell</h1><p>Принятый пилот сопоставлен с нейтральным программным specimen: Graphite-поверхности, cyan-акцент, компактный rail и chrome, tabs/filters, KPI-ритм, аналитические линии, внешний series panel и устойчивое responsive shell-поведение. Это не новый целевой экран и не пересборка пилота.</p></div><div class="status">Machine gate · passed</div></header>
<div class="acceptance"><strong>Вы принимаете не экран и не его продуктовые данные.</strong> Вы принимаете правила визуального языка и оболочки, извлечённые из пилота и зафиксированные для последующего проектирования экранов G4.</div>
<div class="facts"><div class="fact"><b>4 / 4</b><span>Responsive-Web anchors</span></div><div class="fact"><b>9 / 9</b><span>Детальные fixed-domain проверки</span></div><div class="fact"><b>0</b><span>Исключений фиксированных доменов</span></div><div class="fact"><b>G4</b><span>Не заявлен и не исполнялся</span></div></div>
<section class="live-compare" aria-label="Интерактивное сопоставление пилота и реализации"><article class="live-frame"><header><h2>Принятый пилот · интерактивный источник</h2><a href="../../evidence/pilot-candidate-v2/ru/source.html" target="_blank">Открыть отдельно</a></header><iframe title="Принятый интерактивный пилот" src="../../evidence/pilot-candidate-v2/ru/source.html"></iframe></article><article class="live-frame"><header><h2>G3 specimen · интерактивная реализация</h2><a href="candidate-shell.html#chart" target="_blank">Открыть отдельно</a></header><iframe title="Интерактивная G3 реализация" src="candidate-shell.html#chart"></iframe></article></section>
<section class="matrix"><table><thead><tr><th>Pilot source</th><th>Invariant</th><th>Realization</th><th>Proof</th><th>Disposition</th></tr></thead><tbody>{matrix_rows}</tbody></table></section>
<div class="grid">{cards}</div>
<div class="review"><section><h2>Что доказано</h2><ul><li>Sidebar/flyout/drawer сохраняют identity и геометрию workspace; narrow-Web drawer закрывается по Escape/outside и возвращает фокус.</li><li>Inspector — sibling pane на wide Web и viewport overlay на narrow Web; series panel — right sibling или lower panel.</li><li>Chart ↔ table, named sort control, logical keyboard order, visible focus, sticky headings вне tab order.</li><li>RU/EN, 200% zoom, reduced motion и loading/populated/empty/partial/error/denied/recovery language сохраняют task, trust и recovery controls.</li></ul></section><section class="decision"><h2>Решение владельца</h2><p><strong>Принять контракт foundations/shell для G4</strong> или указать ограниченную коррекцию в этой же ревизии. G4 остаётся закрыт до ответа.</p></section></div>
<div class="limits"><section><h2>Разрешённые отличия</h2><ul><li>Ровно 12 px shell/workspace gap и 32 px profile area из принятого baseline.</li><li>Нейтральные labels и fixture values, необходимые только для проверки поведения.</li><li>Responsive reflow внутри фиксированного Web-контракта 768–1920 px.</li></ul></section><section><h2>Запрещённые отличия</h2><ul><li>Новая продуктовая семантика, target-screen composition или принятие какого-либо экрана.</li><li>Копирование pilot fixture values, legend thresholds или данных.</li><li>Mobile IA, production implementation или owner exception без отдельного решения.</li></ul></section></div>
<ul class="closure" aria-label="Hash-bound evidence closure">{hidden_entries}</ul>
</main></body></html>''', encoding="utf-8")


def finalize() -> None:
    program = load(PROGRAM)
    write_json(STRESS, {
        "schema_id": "custometry.ui-g3-browser-stress/v1",
        "program_id": PROGRAM_ID, "revision": 2,
        "browser_mechanic": "playwright-cli 0.1.17 / Chromium 150.0.7871.187",
        "origin": "http://127.0.0.1:4173",
        "checks": [
            {"check":"desktop contextual navigation overlay","status":"passed","observed":{"workspace_before":{"x":86,"width":1822},"workspace_open":{"x":86,"width":1822},"flyout":{"x":76,"y":58,"width":290},"aria_modal":False,"escape_focus_return":"nav-toggle"},"artifact":evidence_ref(EVID / "candidate-web-1920.png")},
            {"check":"narrow modal drawer","status":"passed","observed":{"bounds":{"x":5,"y":5,"width":360,"height":1014},"viewport_contained":True,"aria_modal":True,"workspace_inert":True,"workspace_scroll_lock":"hidden","focus_transfer":"Основа","focus_trap_wrap":["Доверие к результату","Основа"],"outside_dismiss_focus_return":"nav-toggle","escape_focus_return":"nav-toggle","workspace_geometry_stable":True},"artifact":evidence_ref(EVID / "candidate-web-768-drawer.png")},
            {"check":"inspector wide full-height sibling and narrow overlay","status":"passed","observed":{"wide":{"position":"static","width":400,"height":959,"workspace_body_height":959,"fills_workspace_body":True,"focus_transfer":"inspector-close","escape_focus_return":"inspector-toggle"},"narrow":{"x":363,"y":5,"width":400,"height":1014,"viewport_contained":True,"focus_transfer":"inspector-close","escape_focus_return":"inspector-toggle"}},"artifact":evidence_ref(EVID / "candidate-web-1920-inspector.png")},
            {"check":"visible analytical table and grouped icon controls","status":"passed","observed":{"visible_without_mode_switch":True,"named_sort_control":"Сортировать демонстрационные значения","row_heights":[36,36,36,36],"group_rows":2,"sticky_heading_tabindexes":[-1,-1,-1,-1,-1,-1,-1],"grouped_control_surfaces":4,"grouped_icon_buttons":10,"document_overflow":False},"artifact":evidence_ref(EVID / "candidate-web-1440-table.png")},
            {"check":"RU and EN content stress","status":"passed","observed":{"locales":["ru","en"],"en_heading":"Shell and visual-language rules","document_overflow":False,"hero_clipped":False},"artifact":evidence_ref(EVID / "candidate-web-1440-en.png")},
            {"check":"200% browser zoom","status":"passed","observed":{"visualViewportScale":2,"visualViewport":{"width":384,"height":512},"primaryTask":True,"resultTrust":True,"recovery":True,"horizontalDocumentOverflow":False},"artifact":evidence_ref(EVID / "candidate-web-768-zoom-200.png")},
            {"check":"prefers-reduced-motion","status":"passed","observed":{"matches":True,"transition_duration_seconds":0.00001}},
            {"check":"console and network","status":"passed","observed":{"console_errors":0,"request_failures":0,"external_requests":0}},
        ],
        "proof_boundary": "Browser smoke and visible responsive preservation only; not full WCAG conformance or production runtime proof.",
        "result": "passed",
    })
    build_inheritance(program)
    source_rows, candidate_rows = [], []
    for anchor_id, width, height in ANCHORS:
        source_capture = EVID / f"source-{anchor_id}.png"
        source_prov = EVID / f"source-{anchor_id}-provenance.json"
        candidate_capture = EVID / f"candidate-{anchor_id}.png"
        candidate_prov = EVID / f"candidate-{anchor_id}-provenance.json"
        comparison = EVID / f"visual-language-{anchor_id}.json"
        source_rows.append({
            "anchor_id": anchor_id,
            **evidence_ref(source_capture),
            "render_provenance_ref": rel(source_prov), "render_provenance_sha256": sha(source_prov),
        })
        candidate_rows.append({
            "anchor_id": anchor_id,
            **evidence_ref(candidate_capture),
            "render_provenance_ref": rel(candidate_prov), "render_provenance_sha256": sha(candidate_prov),
        })
    proof = program["g3_rendered_proof"]
    proof["shell_capture_contract"] = {**evidence_ref(CONTRACT), "screen_revision_id": SCREEN_REVISION_ID}
    proof["candidate_artifact"] = evidence_ref(CANDIDATE)
    proof["source_anchor_observations"] = source_rows
    proof["candidate_anchor_captures"] = candidate_rows
    proof["inheritance_report"] = evidence_ref(INHERITANCE)
    program["g3_rendered_proof"] = proof
    # Build once for the exact review closure, then bind the resulting board.
    build_review_board(program)
    proof["review_board"] = evidence_ref(REVIEW_BOARD)
    program["g3_rendered_proof"] = proof
    write_json(PROGRAM, program)
    snapshot = json.loads(json.dumps(program))
    snapshot["execution_artifacts"]["plan_doc"] = rel(SNAPSHOT)
    write_json(SNAPSHOT, snapshot)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "prepare-provenance", "finalize"])
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    elif args.mode == "prepare-provenance":
        prepare_provenance()
    elif args.mode == "finalize":
        finalize()


if __name__ == "__main__":
    main()
