#!/usr/bin/env python3
"""Run canonical Playwright CLI QA for the corrected G4 r5 auth review board."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
ART = DIR / "artifacts/g4-r5/family-auth-shell-auth-baseline-exception-auth"
EVID = DIR / "evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth"
BOARD = ART / "review-board.html"
TARGET = ART / "screens/auth-family.html"
OUTPUT = EVID / "browser-board-qa.json"
WINDOW_BASELINE = EVID / "window-geometry-before-r5-03.json"
SESSION = "g4-auth-r5-board-qa"
SCREENSHOT_DEFAULT = EVID / "review-board-1440.png"
SCREENSHOT_RECOVERY = EVID / "review-board-recovery-validation-error-1440.png"
SCREENSHOT_EN = EVID / "review-board-sign-in-en-1440.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def cli(*args: str, json_output: bool = False) -> str:
    command = ["playwright-cli"]
    if json_output:
        command += ["--json", "--raw"]
    command += [f"-s={SESSION}", *args]
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(result.stdout)
    return result.stdout


def main() -> int:
    generator = (DIR / "build_g4_auth_r4_artifacts.py").read_text(encoding="utf-8")
    active_generator = generator.split("def target_html", 1)[1].split("def origin", 1)[0]
    taxonomy = json.loads((EVID / "auth-action-taxonomy.json").read_text(encoding="utf-8"))
    window_baseline = json.loads(WINDOW_BASELINE.read_text(encoding="utf-8"))
    contracts = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((ART / "contracts").glob("*.json"))]
    focused_regression = {
        "native_checkbox_not_fake_role": 'type="checkbox"' in active_generator and 'role="checkbox"' not in active_generator,
        "generic_help_label_absent": "Помощь с паролем" not in active_generator,
        "raw_route_not_decorative": 'class="route"' not in active_generator,
        "fixture_placeholder_absent": "Проверочное значение" not in active_generator,
        "initial_status_conditional": 'data-copy-state="message" hidden' in active_generator,
        "distinct_action_taxonomy": taxonomy.get("generic_standard_button_identity_for_all_actions") is False,
        "generic_standard_exception_removed": len(contracts) == 12 and all(not row.get("standard_exceptions") for row in contracts),
        "stable_feedback_slot_in_generator": 'class="feedback-slot"' in generator and "height:36.5px" in generator,
        "field_errors_do_not_expand_flow": "position:absolute;inset-block-start:100%" in generator,
        "interactive_feedback_uses_stable_slot": "syncFeedback()" in generator,
    }
    cli("open", "about:blank", "--browser", "chrome")
    try:
        code = r'''async page => {
          const consoleErrors=[]; const failedRequests=[];
          page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text())});
          page.on('requestfailed',r=>{if(!r.url().startsWith('file:'))failedRequests.push(r.url())});
          await page.setViewportSize({width:1440,height:1100});
          await page.goto('__BOARD_URL__'); await page.waitForLoadState('load'); await page.waitForTimeout(120);
          const frame=()=>page.frames().find(f=>f!==page.mainFrame());
          const stateIds=['UI-AUTH-001.initial','UI-AUTH-001.first_loading','UI-AUTH-001.ready','UI-AUTH-001.validation_error','UI-AUTH-001.failed','UI-AUTH-001.session_expired','UI-AUTH-004.initial','UI-AUTH-004.first_loading','UI-AUTH-004.ready','UI-AUTH-004.validation_error','UI-AUTH-004.failed','UI-AUTH-004.session_expired'];
          const selected=[];
          for(const stateId of stateIds){
            const screen=stateId.startsWith('UI-AUTH-001')?'UI-AUTH-001':'UI-AUTH-004';
            await page.locator(`[data-screen="${screen}"]`).click();
            await page.locator(`[data-state="${stateId}"]`).click(); await page.waitForTimeout(35);
            selected.push({stateId,frameState:await frame().locator('[data-screen-id]').getAttribute('data-state-id'),url:frame().url()});
          }
          await page.locator('[data-screen="UI-AUTH-001"]').click();
          await page.locator('[data-state="UI-AUTH-001.initial"]').click(); await page.waitForTimeout(50);
          await page.screenshot({path:'__DEFAULT_SCREENSHOT__',fullPage:true});
          const sign=frame(); const signinSurface=sign.locator('[data-ui-element="signin-surface"]');
          const email=sign.locator('[data-ui-element="signin-email"]'); const password=sign.locator('[data-ui-element="signin-password"]');
          const checkbox=sign.locator('[data-ui-element="signin-remember"]'); const checkboxLabel=sign.locator('label[for="signin-remember-control"]');
          const recoveryLink=sign.locator('[data-ui-element="signin-open-recovery"]'); const submit=sign.locator('[data-ui-element="signin-submit"]');
          const status=sign.locator('[data-ui-element="signin-message"]');
          const visibleText=(await sign.locator('body').innerText()).toLowerCase();
          const forbidden=['помощь с паролем','проверочное значение','separate route','отдельный маршрут','/auth/sign-in','/auth/recovery'];
          const semantics={checkboxTag:await checkbox.evaluate(e=>e.tagName),checkboxType:await checkbox.getAttribute('type'),checkboxRoleObserved:await sign.getByRole('checkbox',{name:'Запомнить меня'}).count()===1,checkboxName:await checkbox.getAttribute('aria-label'),checkboxInitial:await checkbox.isChecked(),labelFor:await checkboxLabel.getAttribute('for'),linkTag:await recoveryLink.evaluate(e=>e.tagName),linkHref:await recoveryLink.getAttribute('href'),submitTag:await submit.evaluate(e=>e.tagName),submitType:await submit.getAttribute('type'),initialStatusHidden:await status.isHidden()};
          await checkboxLabel.click(); const labelChecked=await checkbox.isChecked(); const checkedStyle=await checkbox.evaluate(e=>{const s=getComputedStyle(e);return {background:s.backgroundColor,border:s.borderColor}});
          await checkbox.focus(); await checkbox.press('Enter'); const keyboardChecked=await checkbox.isChecked();
          await recoveryLink.click(); const pointerNavResult=await sign.locator('[data-result]').innerText();
          await recoveryLink.focus(); await recoveryLink.press('Enter'); const keyboardNavResult=await sign.locator('[data-result]').innerText();
          const signinInteractiveRect=await sign.locator('.auth-screen').evaluate(e=>{const r=e.getBoundingClientRect();return {width:r.width,height:r.height,x:r.x,y:r.y}});
          const defaultStyle=await submit.evaluate(e=>{const s=getComputedStyle(e);return {background:s.backgroundColor,color:s.color,transform:s.transform,width:e.getBoundingClientRect().width}});
          await submit.hover(); await page.waitForTimeout(150); const hoverStyle=await submit.evaluate(e=>({background:getComputedStyle(e).backgroundColor,color:getComputedStyle(e).color}));
          await page.mouse.down(); const activeStyle=await submit.evaluate(e=>getComputedStyle(e).transform); await page.mouse.up();
          await recoveryLink.focus(); await page.keyboard.press('Tab'); const focusStyle=await submit.evaluate(e=>getComputedStyle(e).outlineStyle);
          const geometry=await sign.evaluate(()=>{const b=id=>document.querySelector(`[data-ui-element="${id}"]`).getBoundingClientRect();const surface=b('signin-surface'),email=b('signin-email'),password=b('signin-password'),submit=b('signin-submit');return {surface:{x:surface.x,width:surface.width},email:{x:email.x,width:email.width},password:{x:password.x,width:password.width},submit:{x:submit.x,width:submit.width}}});
          const tabOrder=[]; await sign.locator('[data-ui-element="signin-locale"]').focus(); tabOrder.push('signin-locale'); for(let i=1;i<6;i++){await page.keyboard.press('Tab');tabOrder.push(await sign.evaluate(()=>document.activeElement.getAttribute('data-ui-element')||document.activeElement.tagName.toLowerCase()))}
          await sign.locator('[data-locale]').selectOption('en'); await page.waitForTimeout(30); const enHeading=await sign.locator('h1').innerText(); const enCheckboxName=await checkbox.getAttribute('aria-label');
          await page.screenshot({path:'__EN_SCREENSHOT__',fullPage:true});
          const stress=[]; for(const width of [768,1024,1440,1920]){await page.setViewportSize({width,height:width===768?1024:900});await page.waitForTimeout(20);stress.push({width,overflow:await sign.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth)});}
          await sign.evaluate(()=>{document.documentElement.style.zoom='2'}); const zoomOverflow=await sign.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth); await sign.evaluate(()=>{document.documentElement.style.zoom='' });
          await page.emulateMedia({reducedMotion:'reduce'}); const reducedMotion=await sign.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches); const reducedDuration=await submit.evaluate(e=>getComputedStyle(e).transitionDuration);
          await page.setViewportSize({width:1440,height:1100}); await page.locator('[data-screen="UI-AUTH-004"]').click(); await page.locator('[data-state="UI-AUTH-004.validation_error"]').click(); await page.waitForTimeout(50);
          const recovery=frame(); const returnLink=recovery.locator('[data-ui-element="recovery-return"]');
          const recoverySemantics={screen:await recovery.locator('[data-screen-id]').getAttribute('data-screen-id'),state:await recovery.locator('[data-screen-id]').getAttribute('data-state-id'),returnTag:await returnLink.evaluate(e=>e.tagName),returnHref:await returnLink.getAttribute('href'),stepCount:await recovery.locator('[data-ui-element="recovery-steps"] li').count(),statusVisible:await recovery.locator('[data-ui-element="recovery-token-error"]').isVisible()};
          await returnLink.click(); const returnPointer=await recovery.locator('[data-result]').innerText(); await returnLink.focus(); await returnLink.press('Enter'); const returnKeyboard=await recovery.locator('[data-result]').innerText();
          const recoveryInteractiveRect=await recovery.locator('.auth-screen').evaluate(e=>{const r=e.getBoundingClientRect();return {width:r.width,height:r.height,x:r.x,y:r.y}});
          await page.screenshot({path:'__RECOVERY_SCREENSHOT__',fullPage:true});
          const loadingUrl=frame().url().replace('validation_error','first_loading'); await recovery.goto(loadingUrl); await recovery.waitForLoadState('load');
          const loadingDisabled=await recovery.locator('button[data-action]').evaluateAll(nodes=>nodes.every(n=>n.disabled));
          const manifest=await page.locator('body').getAttribute('data-review-manifest'); const entries=await page.locator('[data-review-entry]').count();
          const externalRequests=await page.evaluate(()=>performance.getEntriesByType('resource').map(x=>x.name).filter(x=>!x.startsWith('file:')));
          const targetUrl=page.url().replace(/review-board\.html(?:[?#].*)?$/, 'screens/auth-family.html'); const windowGeometry=[]; const probe=await page.context().newPage();
          for(const [width,height] of [[768,1024],[1024,768],[1440,900],[1920,1080]]){
            await probe.setViewportSize({width,height});
            for(const screen of ['UI-AUTH-001','UI-AUTH-004']) for(const lang of ['ru','en']) for(const stateName of ['initial','first_loading','ready','validation_error','failed','session_expired']){
              const stateId=`${screen}.${stateName}`; await probe.goto(`${targetUrl}?screen=${screen}&state=${stateId}&lang=${lang}`); await probe.waitForLoadState('load');
              const measured=await probe.evaluate(()=>{const card=document.querySelector('.auth-screen');const r=card.getBoundingClientRect();const slot=document.querySelector('.feedback-slot');return {cardWidth:r.width,cardHeight:r.height,x:r.x,y:r.y,cardOverflow:card.scrollHeight>card.clientHeight+0.5,feedbackOverflow:slot.scrollHeight>slot.clientHeight+0.5,pageOverflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth,pageOverflowY:document.documentElement.scrollHeight>document.documentElement.clientHeight}});
              windowGeometry.push({anchorWidth:width,screen,lang,stateName,...measured});
            }
          }
          await probe.close();
          await page.reload(); await page.waitForLoadState('load'); const repeatTitle=await page.title();
          return {selected,semantics,labelChecked,keyboardChecked,checkedStyle,pointerNavResult,keyboardNavResult,signinInteractiveRect,defaultStyle,hoverStyle,activeStyle,focusStyle,geometry,tabOrder,visibleText,forbidden,enHeading,enCheckboxName,stress,zoomOverflow,reducedMotion,reducedDuration,recoverySemantics,returnPointer,returnKeyboard,recoveryInteractiveRect,loadingDisabled,manifest,entries,windowGeometry,consoleErrors,failedRequests,externalRequests,repeatTitle,title:await page.title()};
        }'''
        code = code.replace("'__BOARD_URL__'", json.dumps(BOARD.resolve().as_uri())).replace("'__DEFAULT_SCREENSHOT__'", json.dumps(str(SCREENSHOT_DEFAULT))).replace("'__RECOVERY_SCREENSHOT__'", json.dumps(str(SCREENSHOT_RECOVERY))).replace("'__EN_SCREENSHOT__'", json.dumps(str(SCREENSHOT_EN)))
        raw = json.loads(cli("run-code", code, json_output=True))
        if "result" not in raw:
            raise RuntimeError(json.dumps(raw, ensure_ascii=False, indent=2))
        observed = json.loads(raw["result"])
        s = observed["semantics"]
        g = observed["geometry"]
        initial_geometry = window_baseline["initial_geometry"]
        geometry_matches = all(
            abs(row["cardWidth"] - initial_geometry[row["screen"]][str(row["anchorWidth"])]["width"]) < 0.01
            and abs(row["cardHeight"] - initial_geometry[row["screen"]][str(row["anchorWidth"])]["height"]) < 0.01
            for row in observed["windowGeometry"]
        )
        geometry_groups: dict[tuple[int, str, str], list[dict]] = {}
        for row in observed["windowGeometry"]:
            geometry_groups.setdefault((row["anchorWidth"], row["screen"], row["lang"]), []).append(row)
        position_stable = all(
            all(abs(row["x"] - rows[0]["x"]) < 0.01 and abs(row["y"] - rows[0]["y"]) < 0.01 for row in rows)
            for rows in geometry_groups.values()
        )
        checks = {
            "focused_generator_regression": all(focused_regression.values()),
            "all_12_states_selected": len(observed["selected"]) == 12 and all(row["stateId"] == row["frameState"] and row["stateId"] in row["url"] for row in observed["selected"]),
            "native_checkbox_name_role_state_label": s["checkboxTag"] == "INPUT" and s["checkboxType"] == "checkbox" and s["checkboxRoleObserved"] and bool(s["checkboxName"]) and s["labelFor"] == "signin-remember-control" and not s["checkboxInitial"] and observed["labelChecked"] and not observed["keyboardChecked"],
            "real_route_links": s["linkTag"] == "A" and s["linkHref"] == "/auth/recovery" and observed["recoverySemantics"]["returnTag"] == "A" and observed["recoverySemantics"]["returnHref"] == "/auth/sign-in",
            "semantic_buttons": s["submitTag"] == "BUTTON" and s["submitType"] == "submit" and observed["loadingDisabled"],
            "initial_status_absent": s["initialStatusHidden"],
            "forbidden_visible_copy_absent": all(item not in observed["visibleText"] for item in observed["forbidden"]),
            "pointer_keyboard_navigation": "восстанов" in observed["pointerNavResult"].lower() and "восстанов" in observed["keyboardNavResult"].lower() and "вход" in observed["returnPointer"].lower() and "вход" in observed["returnKeyboard"].lower(),
            "default_hover_focus_active_checked": observed["defaultStyle"]["background"] == "rgb(140, 207, 227)" and observed["hoverStyle"]["background"] == "rgb(165, 220, 236)" and observed["focusStyle"] == "solid" and observed["activeStyle"] not in ("none", observed["defaultStyle"]["transform"]) and observed["checkedStyle"]["background"] == "rgb(140, 207, 227)",
            "shared_edges_and_action_width": abs(g["email"]["x"]-g["password"]["x"]) < 1 and abs(g["email"]["x"]-g["submit"]["x"]) < 1 and abs(g["email"]["width"]-g["password"]["width"]) < 1 and abs(g["email"]["width"]-g["submit"]["width"]) < 1,
            "focus_order": observed["tabOrder"] == ["signin-locale","signin-email","signin-password","signin-remember","signin-open-recovery","signin-submit"],
            "ru_en_equivalence": observed["enHeading"] == "Sign in to Custometry" and observed["enCheckboxName"] == "Remember me",
            "all_web_anchors_no_overflow": len(observed["stress"]) == 4 and all(not row["overflow"] for row in observed["stress"]),
            "all_state_windows_match_initial_geometry": len(observed["windowGeometry"]) == 96 and geometry_matches,
            "window_position_stable_across_states": position_stable,
            "feedback_and_card_content_not_clipped": all(not row["cardOverflow"] and not row["feedbackOverflow"] and not row["pageOverflowX"] for row in observed["windowGeometry"]),
            "interactive_feedback_keeps_initial_geometry": abs(observed["signinInteractiveRect"]["height"] - initial_geometry["UI-AUTH-001"]["1440"]["height"]) < 0.01 and abs(observed["recoveryInteractiveRect"]["height"] - initial_geometry["UI-AUTH-004"]["1440"]["height"]) < 0.01,
            "zoom_200_reflow": not observed["zoomOverflow"],
            "reduced_motion": observed["reducedMotion"] and observed["reducedDuration"] in ("0s", "0.001s"),
            "recovery_reading_state": observed["recoverySemantics"]["screen"] == "UI-AUTH-004" and observed["recoverySemantics"]["state"] == "UI-AUTH-004.validation_error" and observed["recoverySemantics"]["stepCount"] == 3 and observed["recoverySemantics"]["statusVisible"],
            "review_nested_closure": observed["entries"] == 24 and bool(observed["manifest"]),
            "console_network_isolated": not observed["consoleErrors"] and not observed["failedRequests"] and not observed["externalRequests"],
            "deterministic_repeat": observed["repeatTitle"] == observed["title"] == "Custometry · auth family r5",
        }
        document = {
            "schema_id": "custometry.ui-g4-browser-board-qa/v2",
            "generated_by": {"script": Path(__file__).name, "version": "2.0.0", "browser_mechanic": "playwright-cli / Chrome"},
            "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2", "stage_instance_id": "G4@family.auth.shell-auth.baseline-exception-auth-r5",
            "artifacts": {"review_board": {"path": rel(BOARD), "sha256": sha(BOARD)}, "target_surface": {"path": rel(TARGET), "sha256": sha(TARGET)}, "window_geometry_baseline": {"path": rel(WINDOW_BASELINE), "sha256": sha(WINDOW_BASELINE)}, "default_screenshot": {"path": rel(SCREENSHOT_DEFAULT), "sha256": sha(SCREENSHOT_DEFAULT)}, "recovery_screenshot": {"path": rel(SCREENSHOT_RECOVERY), "sha256": sha(SCREENSHOT_RECOVERY)}, "english_screenshot": {"path": rel(SCREENSHOT_EN), "sha256": sha(SCREENSHOT_EN)}},
            "checks": [{"check_id": key, "status": "passed" if value else "failed"} for key, value in checks.items()], "focused_regression": focused_regression, "observed": observed,
            "proof_boundary": "Isolated local file Playwright CLI proof for all 12 states, responsive Web, RU/EN, semantic controls, pointer/keyboard, physical active state, 200% zoom, reduced motion, focus order, console/network and review closure; not production runtime, mobile-specific design or full WCAG conformance.",
            "result": "passed" if all(checks.values()) else "failed",
        }
        OUTPUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": document["result"], "output": rel(OUTPUT), "failed": [key for key, value in checks.items() if not value]}, indent=2))
        return 0 if all(checks.values()) else 1
    finally:
        cli("close")


if __name__ == "__main__":
    raise SystemExit(main())
