#!/usr/bin/env python3
"""Run canonical Playwright CLI QA for the G4 r5 onboarding board."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
ART = DIR / "artifacts/g4-r5/family-auth-shell-workspace-baseline"
EVID = DIR / "evidence/family.auth.shell-workspace.baseline-r5"
BOARD = ART / "review-board.html"
TARGET = ART / "screens/onboarding.html"
OUTPUT = EVID / "browser-board-qa.json"
SCREENSHOT = EVID / "review-board-1440.png"
SESSION = "g4-auth-workspace-r5-board-qa"


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
    cli("open", "about:blank", "--browser", "chrome")
    try:
        code = r'''async page => {
          const errors=[]; const failures=[];
          page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
          page.on('requestfailed',r=>{if(!r.url().startsWith('file:'))failures.push(r.url())});
          await page.setViewportSize({width:1440,height:1000});
          await page.goto('__BOARD__'); await page.waitForLoadState('load'); await page.waitForTimeout(100);
          const frame=()=>page.frames().find(f=>f!==page.mainFrame());
          const ids=['initial','loading','populated','error','permission_denied','recovery'].map(x=>`UI-AUTH-005.${x}`);
          const selected=[];
          for(const id of ids){await page.locator(`[data-state="${id}"]`).click();await page.waitForTimeout(45);selected.push({id,state:await frame().locator('[data-screen-id]').getAttribute('data-state-id'),url:frame().url()});}
          await page.locator('[data-state="UI-AUTH-005.initial"]').click(); await page.waitForTimeout(40);
          await page.screenshot({path:'__SCREENSHOT__',fullPage:true});
          const f=frame(); const title=await f.locator('h1').innerText(); const steps=await f.locator('[data-ui-element="onboarding-steps"] li').count(); const checks=await f.locator('.checks li').count();
          const action=f.locator('[data-prototype-action="UI-AUTH-005.inspect"]'); await action.focus(); await action.press('Enter'); const result=await f.locator('[data-result]').innerText();
          const responsive=[]; for(const width of [768,1024,1440,1920]){await page.setViewportSize({width,height:width===768?1024:900});await page.waitForTimeout(20);responsive.push({width,overflow:await f.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth)});}
          await page.setViewportSize({width:1440,height:1000}); const target=page.url().replace(/review-board\.html(?:[?#].*)?$/,'screens/onboarding.html'); const probe=await page.context().newPage();
          await probe.goto(`${target}?screen=UI-AUTH-005&state=UI-AUTH-005.initial&lang=en`); await probe.waitForLoadState('load'); const enTitle=await probe.locator('h1').innerText();
          await probe.goto(`${target}?screen=UI-AUTH-005&state=UI-AUTH-005.loading&lang=ru`); await probe.waitForLoadState('load'); const loadingDisabled=await probe.locator('[data-prototype-action]').isDisabled();
          await probe.goto(`${target}?screen=UI-AUTH-005&state=UI-AUTH-005.permission_denied&lang=ru`); await probe.waitForLoadState('load'); const permissionDisabled=await probe.locator('[data-prototype-action]').isDisabled();
          await probe.emulateMedia({reducedMotion:'reduce'}); const reduced=await probe.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches); const duration=await probe.locator('[data-prototype-action]').evaluate(e=>getComputedStyle(e).transitionDuration); await probe.close();
          return {selected,title,steps,checks,result,responsive,enTitle,loadingDisabled,permissionDisabled,reduced,duration,manifest:await page.locator('body').getAttribute('data-review-manifest'),entries:await page.locator('[data-review-entry]').count(),errors,failures};
        }'''.replace("'__BOARD__'", json.dumps(BOARD.resolve().as_uri())).replace("'__SCREENSHOT__'", json.dumps(str(SCREENSHOT)))
        raw = json.loads(cli("run-code", code, json_output=True))
        observed = json.loads(raw["result"])
        checks = {
            "all_states_selectable": len(observed["selected"]) == 6 and all(x["id"] == x["state"] and x["id"] in x["url"] for x in observed["selected"]),
            "five_step_onboarding": observed["steps"] == 5 and observed["checks"] == 4,
            "keyboard_action_feedback": "Следующий шаг" in observed["result"],
            "responsive_web_no_overflow": len(observed["responsive"]) == 4 and all(not x["overflow"] for x in observed["responsive"]),
            "ru_en_equivalence": observed["title"] == "Настройте рабочее пространство" and observed["enTitle"] == "Set up your workspace",
            "bounded_action_states": observed["loadingDisabled"] and observed["permissionDisabled"],
            "reduced_motion": observed["reduced"] and observed["duration"] == "0s",
            "review_closure": observed["entries"] == 12 and bool(observed["manifest"]),
            "console_network_clean": not observed["errors"] and not observed["failures"],
        }
        document={"schema_id":"custometry.ui-g4-browser-board-qa/v1","program_id":"CUSTOMETRY-UI-DESIGN-PROGRAM-V2","stage_instance_id":"G4@family.auth.shell-workspace.baseline-r5","generated_by":{"script":Path(__file__).name,"browser_mechanic":"playwright-cli / Chrome"},"artifacts":{"review_board":{"path":rel(BOARD),"sha256":sha(BOARD)},"target_surface":{"path":rel(TARGET),"sha256":sha(TARGET)},"screenshot":{"path":rel(SCREENSHOT),"sha256":sha(SCREENSHOT)}},"checks":[{"check_id":k,"status":"passed" if v else "failed"} for k,v in checks.items()],"observed":observed,"proof_boundary":"Local isolated browser proof for the finished family board, six states, RU/EN, four responsive Web anchors, keyboard activation and reduced motion; not production runtime, mobile-specific design or full WCAG conformance.","result":"passed" if all(checks.values()) else "failed"}
        OUTPUT.write_text(json.dumps(document,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":document["result"],"output":rel(OUTPUT),"failed":[k for k,v in checks.items() if not v]},ensure_ascii=False,indent=2))
        return 0 if all(checks.values()) else 1
    finally:
        cli("close")


if __name__ == "__main__":
    raise SystemExit(main())
