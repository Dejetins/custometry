#!/usr/bin/env python3
"""Verify that the G4 core review bundle renders from file and bundle-root HTTP."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import time
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
ART = DIR / "artifacts/g4-r5/family-core-shell-workspace-baseline"
EVID = DIR / "evidence/family.core.shell-workspace.baseline-r5"
BOARD = ART / "review-board.html"
POPULATED = ART / "states/populated/screen.html"
PILOT = DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
OUTPUT = EVID / "browser-board-qa.json"
SCREENSHOT = EVID / "review-board-1440.png"
SERVER_LOG = EVID / "review-board-bundle-server.log"
SESSION = "g4-core-r5-board-qa"
PORT = 41737
STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def cli(*args: str, json_output: bool = False) -> str:
    command = ["playwright-cli"]
    if json_output:
        command += ["--json", "--raw"]
    command += [f"-s={SESSION}", *args]
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        raise RuntimeError(result.stdout)
    return result.stdout


def wait_for_server() -> None:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with urlopen(f"http://127.0.0.1:{PORT}/review-board.html", timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("review bundle server did not become ready")


def main() -> int:
    SERVER_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SERVER_LOG.open("w", encoding="utf-8") as log:
        server = subprocess.Popen(
            ["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
            cwd=ART,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
        try:
            wait_for_server()
            cli("open", "about:blank", "--browser", "chrome")
            try:
                code = (r'''async page => {
                  const consoleErrors=[]; const failedRequests=[]; const badResponses=[];
                  page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text())});
                  page.on('requestfailed',r=>failedRequests.push(r.url()));
                  page.on('response',r=>{if(r.status()>=400)badResponses.push({url:r.url(),status:r.status()})});
                  const inspect=async mode => {
                    await page.waitForLoadState('load');
                    await page.waitForTimeout(100);
                    const responsive=[];
                    for(const width of [768,1440,1920]){
                      await page.setViewportSize({width,height:1000});
                      await page.waitForTimeout(30);
                      responsive.push({width,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth)});
                    }
                    await page.setViewportSize({width:1440,height:1000});
                    const observed=await page.evaluate(() => ({
                      cards:document.querySelectorAll('.review-card').length,
                      entries:document.querySelectorAll('[data-review-entry]').length,
                      manifest:document.querySelector('[data-review-manifest]')?.getAttribute('data-review-manifest'),
                      images:[...document.images].map(img=>({
                        src:img.getAttribute('src'),
                        resolved:img.currentSrc,
                        complete:img.complete,
                        naturalWidth:img.naturalWidth,
                        naturalHeight:img.naturalHeight,
                        assetSha256:img.dataset.assetSha256 || null,
                      })),
                    }));
                    return {mode,url:page.url(),responsive,...observed};
                  };
                  const inspectKpi=async (mode,url) => {
                    const anchors=[];
                    for(const width of [768,1024,1440,1920]){
                      await page.setViewportSize({width,height:1000});
                      await page.goto(url);
                      await page.waitForLoadState('load');
                      await page.waitForTimeout(100);
                      anchors.push(await page.evaluate(width => {
                        const module=document.querySelector('.kpi-module');
                        const header=document.querySelector('.kpi-module-header');
                        const strip=document.querySelector('.kpi-strip');
                        const cells=[...document.querySelectorAll('.kpi')];
                        const first=cells[0];
                        const second=cells[1];
                        const label=first?.querySelector('.kpi-label');
                        const value=first?.querySelector('.kpi-value');
                        const delta=first?.querySelector('.kpi-delta');
                        if(!module || !header || !strip || !first || !second || !label || !value || !delta){
                          return {width,found:false,pageOverflow:document.documentElement.scrollWidth>document.documentElement.clientWidth};
                        }
                        const style=element=>getComputedStyle(element);
                        const rect=element=>{const box=element.getBoundingClientRect();return {x:box.x,y:box.y,width:box.width,height:box.height}};
                        const moduleStyle=style(module);
                        const headerStyle=style(header);
                        const stripStyle=style(strip);
                        const cellStyle=style(first);
                        const separatorStyle=getComputedStyle(second,'::before');
                        return {
                          width,
                          found:true,
                          pageOverflow:document.documentElement.scrollWidth>document.documentElement.clientWidth,
                          cellCount:cells.length,
                          module:{
                            rect:rect(module),
                            display:moduleStyle.display,
                            gridTemplateColumns:moduleStyle.gridTemplateColumns,
                            minHeight:moduleStyle.minHeight,
                            backgroundColor:moduleStyle.backgroundColor,
                            borderTop:`${moduleStyle.borderTopWidth} ${moduleStyle.borderTopStyle}`,
                            borderBottom:`${moduleStyle.borderBottomWidth} ${moduleStyle.borderBottomStyle}`,
                            borderRadius:moduleStyle.borderRadius,
                            boxShadow:moduleStyle.boxShadow,
                            overflow:moduleStyle.overflow,
                          },
                          header:{rect:rect(header),padding:headerStyle.padding,backgroundColor:headerStyle.backgroundColor},
                          strip:{rect:rect(strip),display:stripStyle.display,overflowX:stripStyle.overflowX},
                          cell:{rect:rect(first),padding:cellStyle.padding,minWidth:cellStyle.minWidth,flexBasis:cellStyle.flexBasis,gap:cellStyle.gap},
                          label:{fontSize:style(label).fontSize,color:style(label).color},
                          value:{fontSize:style(value).fontSize,fontWeight:style(value).fontWeight},
                          delta:{fontSize:style(delta).fontSize},
                          separator:{content:separatorStyle.content,width:separatorStyle.width,insetBlockStart:separatorStyle.insetBlockStart,insetBlockEnd:separatorStyle.insetBlockEnd},
                        };
                      },width));
                    }
                    return {mode,url,anchors};
                  };
                  await page.setViewportSize({width:1440,height:1000});
                  await page.goto('__FILE_URL__');
                  const localFile=await inspect('local_file');
                  await page.screenshot({path:'__SCREENSHOT__',fullPage:true});
                  await page.goto('__HTTP_URL__');
                  const bundleHttp=await inspect('bundle_root_http');
                  const pilotKpi=await inspectKpi('accepted_pilot','__PILOT_URL__');
                  const candidateKpi=await inspectKpi('populated_candidate','__POPULATED_URL__');
                  return {localFile,bundleHttp,pilotKpi,candidateKpi,consoleErrors,failedRequests,badResponses};
                }'''.replace("'__FILE_URL__'", json.dumps(BOARD.resolve().as_uri()))
                    .replace("'__HTTP_URL__'", json.dumps(f"http://127.0.0.1:{PORT}/review-board.html"))
                    .replace("'__PILOT_URL__'", json.dumps(PILOT.resolve().as_uri()))
                    .replace("'__POPULATED_URL__'", json.dumps(f"http://127.0.0.1:{PORT}/states/populated/screen.html"))
                    .replace("'__SCREENSHOT__'", json.dumps(str(SCREENSHOT))))
                raw = json.loads(cli("run-code", code, json_output=True))
                observed = json.loads(raw["result"])
            finally:
                cli("close")
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)

    expected_assets = []
    for state in STATES:
        bundled = ART / "review-assets" / f"{state}.png"
        source = EVID / "states" / state / "web-1440" / "implementation.png"
        expected_assets.append({
            "state": state,
            "bundle_ref": rel(bundled),
            "source_ref": rel(source),
            "sha256": sha(bundled),
            "matches_source": sha(bundled) == sha(source),
        })

    def mode_passed(mode: dict) -> bool:
        return (
            mode["cards"] == len(STATES)
            and mode["entries"] == len(STATES) * 2
            and bool(mode["manifest"])
            and len(mode["images"]) == len(STATES)
            and all(
                image["complete"]
                and image["naturalWidth"] > 0
                and image["naturalHeight"] > 0
                and image["src"].startswith("review-assets/")
                for image in mode["images"]
            )
            and all(not anchor["overflow"] for anchor in mode["responsive"])
        )

    def kpi_pilot_conformance_passed() -> bool:
        pilot_by_width = {anchor["width"]: anchor for anchor in observed["pilotKpi"]["anchors"]}
        candidate_by_width = {anchor["width"]: anchor for anchor in observed["candidateKpi"]["anchors"]}
        if set(pilot_by_width) != {768, 1024, 1440, 1920} or set(candidate_by_width) != set(pilot_by_width):
            return False
        for width, pilot in pilot_by_width.items():
            candidate = candidate_by_width[width]
            if not pilot["found"] or not candidate["found"] or candidate["pageOverflow"]:
                return False
            if candidate["cellCount"] != 4:
                return False
            for key in ("display", "minHeight", "backgroundColor", "borderTop", "borderBottom", "borderRadius", "boxShadow", "overflow"):
                if candidate["module"][key] != pilot["module"][key]:
                    return False
            if candidate["module"]["gridTemplateColumns"].split()[0] != pilot["module"]["gridTemplateColumns"].split()[0]:
                return False
            if abs(candidate["module"]["rect"]["height"] - pilot["module"]["rect"]["height"]) > 0.01:
                return False
            if candidate["header"]["padding"] != pilot["header"]["padding"]:
                return False
            if abs(candidate["header"]["rect"]["width"] - pilot["header"]["rect"]["width"]) > 0.01:
                return False
            if candidate["strip"]["display"] != pilot["strip"]["display"] or candidate["strip"]["overflowX"] != pilot["strip"]["overflowX"]:
                return False
            for key in ("padding", "minWidth", "flexBasis", "gap"):
                if candidate["cell"][key] != pilot["cell"][key]:
                    return False
            if candidate["label"]["fontSize"] != pilot["label"]["fontSize"]:
                return False
            if candidate["value"] != pilot["value"] or candidate["delta"]["fontSize"] != pilot["delta"]["fontSize"]:
                return False
            if candidate["separator"] != pilot["separator"]:
                return False
        return True

    checks = {
        "local_file_images_visible": mode_passed(observed["localFile"]),
        "bundle_root_http_images_visible": mode_passed(observed["bundleHttp"]),
        "review_assets_hash_bound": all(item["matches_source"] for item in expected_assets)
        and [image["assetSha256"] for image in observed["localFile"]["images"]]
        == [item["sha256"] for item in expected_assets],
        "populated_kpi_matches_accepted_pilot": kpi_pilot_conformance_passed(),
        "console_network_clean": not observed["consoleErrors"]
        and not observed["failedRequests"]
        and not observed["badResponses"],
    }
    document = {
        "schema_id": "custometry.ui-g4-browser-board-qa/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": "G4@family.core.shell-workspace.baseline-r5",
        "generated_by": {
            "script": Path(__file__).name,
            "browser_mechanic": "playwright-cli / Chrome",
        },
        "artifacts": {
            "review_board": {"path": rel(BOARD), "sha256": sha(BOARD)},
            "populated_screen": {"path": rel(POPULATED), "sha256": sha(POPULATED)},
            "accepted_pilot": {"path": rel(PILOT), "sha256": sha(PILOT)},
            "review_assets": expected_assets,
            "screenshot": {"path": rel(SCREENSHOT), "sha256": sha(SCREENSHOT)},
        },
        "checks": [
            {"check_id": check_id, "status": "passed" if passed else "failed"}
            for check_id, passed in checks.items()
        ],
        "observed": observed,
        "proof_boundary": "Local-file and bundle-root loopback browser proof for the portable finished family review board, six visible PNGs, review closure, responsive-Web board overflow, and direct computed-style/geometry conformance of the populated KPI module to the hash-pinned accepted pilot at all four Web anchors; not production runtime, mobile-specific design, or full WCAG conformance.",
        "result": "passed" if all(checks.values()) else "failed",
    }
    OUTPUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": document["result"],
        "output": rel(OUTPUT),
        "failed": [check_id for check_id, passed in checks.items() if not passed],
    }, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
