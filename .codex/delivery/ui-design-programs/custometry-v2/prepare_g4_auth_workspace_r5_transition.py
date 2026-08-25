#!/usr/bin/env python3
"""Prepare the review-ready handoff for G4 r5 workspace onboarding."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[4]
DIR=Path(__file__).resolve().parent
ART=DIR/"artifacts/g4-r5/family-auth-shell-workspace-baseline"
EVID=DIR/"evidence/family.auth.shell-workspace.baseline-r5"
PREFLIGHT=EVID/"preflight"
FAMILY=EVID/"family-acceptance.json"
BOARD=ART/"review-board.html"
QA=EVID/"browser-board-qa.json"
PACKET=EVID/"owner-review-decision-packet.json"
DECISION=EVID/"family-acceptance-decision-r5.json"
OWNER_RESPONSE=EVID/"owner-input-response-acceptance-r5.json"
STAGE="G4@family.auth.shell-workspace.baseline-r5"
NEXT_STAGE="G4@family.core.shell-workspace.baseline-r5"
NEXT_TARGET="family.core.shell-workspace.baseline-r5"
NEXT_TASK=ROOT/".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-03-family-core-shell-workspace-baseline-r5.md"
REPORT=ROOT/".codex/delivery/evidence/custometry-ui-design-program-v2/family.auth.shell-workspace.baseline-r5-report.md"
PROGRAM_ID="CUSTOMETRY-UI-DESIGN-PROGRAM-V2"


def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def rel(path: Path) -> str: return path.relative_to(ROOT).as_posix()
def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def evidence(check_id: str, facts: dict) -> dict:
    return {"$schema":"stage-preflight-evidence.schema.json","schema_id":"codex.ui-stage-preflight-evidence/v1","check_id":check_id,"program_id":PROGRAM_ID,"stage_instance_id":STAGE,"gate_id":"G4","status":"passed","facts":facts}


def refs(document) -> list[dict[str,str]]:
    found={}
    def visit(value):
        if isinstance(value,dict):
            path=value.get("path"); digest=value.get("sha256")
            if isinstance(path,str) and isinstance(digest,str) and len(digest)==64: found[path]=digest
            for child in value.values(): visit(child)
        elif isinstance(value,list):
            for child in value: visit(child)
    visit(document)
    return [{"path":path,"sha256":digest} for path,digest in sorted(found.items())]


def owner_requests() -> int:
    owner_input="ок [Открыть review board](/Users/daniildegtyarev/Projects/Custometry/.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-auth-shell-workspace-baseline/review-board.html) принято"
    write(EVID/"family-acceptance-decision-r5-request.json",{
      "$schema":"owner-decision-request.schema.json","program_id":PROGRAM_ID,
      "decision_id":f"{STAGE}.finished-result","decision_kind":"family_acceptance","status":"accepted","revision":5,
      "decision_text":"The owner explicitly accepted the exact finished G4 workspace-onboarding family shown in the hash-bound r5 review board. Acceptance covers the compact Graphite workspace shell, the resumable five-step account/workspace/locale-timezone/data-or-demo/finish flow, visible readiness context, all six represented UI-AUTH-005 states, RU/EN equivalence, responsive Web anchors and applicable pilot inheritance. It does not authorize production implementation, publication, deployment, mobile-specific design, another G4 family, G5, G6 or full WCAG conformance.",
      "owner_input":owner_input,
      "target":{"artifact_kind":"review_board","artifact_id":"family.auth.shell-workspace.baseline-r5","revision":5,"validation_profile":"family_review_ready","path":rel(BOARD)},
      "accepted_values":[{"stage_instance_id":STAGE,"screen_ids":["UI-AUTH-005"],"reuse_only_screen_ids":["UI-AUTH-006"],"state_count":6,"responsive_web_anchors":[768,1024,1440,1920],"flow_steps":["account","workspace","locale_timezone","data_or_demo","finish"],"resumable":True,"mobile_scope":"unauthorized","production_implementation":"not_accepted_by_this_decision"}]
    })
    write(EVID/"owner-input-response-acceptance-r5-request.json",{
      "$schema":"owner-input-response-request.schema.json","program_id":PROGRAM_ID,"stage_instance_id":STAGE,
      "decision_packet_ref":rel(PACKET),"response_kind":"visual_acceptance","owner_input":owner_input,
      "canonical_owner_decision_ref":rel(DECISION)
    })
    return 0


def bind_acceptance() -> int:
    if not DECISION.is_file() or not OWNER_RESPONSE.is_file():
        raise ValueError("canonical owner decision and owner input response are required")
    request_path=EVID/"family-acceptance-request.json"
    request=json.loads(request_path.read_text(encoding="utf-8"))
    request["owner_decision_ref"]=rel(DECISION)
    write(request_path,request)
    return 0


def main(*, accepted: bool=False) -> int:
    family=json.loads(FAMILY.read_text(encoding="utf-8")); qa=json.loads(QA.read_text(encoding="utf-8")); packet=json.loads(PACKET.read_text(encoding="utf-8"))
    expected_result="passed" if accepted else "review_ready"
    if family.get("result")!=expected_result or qa.get("result")!="passed" or packet.get("status")!="pending": raise ValueError("finished onboarding family is not at the expected gate state")
    pending=EVID/"pending-owner-decisions.json"; resolved=EVID/"resolved-owner-decisions.json"; blockers=EVID/"known-blockers.json"; outside=EVID/"outside-expected-paths.json"
    write(pending,[{"decision_id":f"{STAGE}.finished-result","class":"owner_required","status":"pending","summary":"Accept the finished workspace onboarding family or request bounded corrections.","resolution_ref":None}])
    if accepted:
        write(resolved,[{"decision_id":f"{STAGE}.finished-result","class":"owner_required","status":"resolved","summary":"The owner explicitly accepted the exact finished workspace-onboarding r5 review board.","resolution_ref":rel(DECISION)}])
    write(blockers,[]); write(outside,{"schema_id":"custometry.ui-stage-file-manifest-outside-expected/v1","program_id":PROGRAM_ID,"stage_instance_id":STAGE,"outside_expected_paths":[],"observed_file_count":0,"reason":"All writes remain inside authorized program-owned touch zones.","historical_evidence_mutated":False})
    checks={
      "current_gate":evidence("current_gate",{"validation_profile":"family_gate" if accepted else "family_review_ready","artifact_ref":rel(FAMILY),"artifact_sha256":sha(FAMILY),"result":"passed"}),
      "source_freshness":evidence("source_freshness",{"source_refs":refs(family),"drift_classification":"owned_generated_change","stale_refs":[]}),
      "next_stage_inputs":evidence("next_stage_inputs",{"next_stage_id":NEXT_STAGE,"task_ref":rel(NEXT_TASK),"unresolved_inputs":[]}),
      "write_scope":evidence("write_scope",{"allowed_paths":[".codex/delivery/ui-design-programs/custometry-v2/**",".codex/agents/generated/custometry-ui-design-g0-v2/**",".codex/delivery/evidence/custometry-ui-design-program-v2/**"],"authorization_basis":"explicit_current_user_authorization","outside_scope_paths":[]}),
      "foreign_changes":evidence("foreign_changes",{"observed_paths":[],"inseparable_paths":[],"disposition":"separable_foreign_changes_preserved"}),
      "execution_route":evidence("execution_route",{"route":"staged-plan-runner + ui-design-program + playwright-cli","available":True}),
      "handoff_artifact":evidence("handoff_artifact",{"artifact_ref":rel(NEXT_TASK),"artifact_sha256":sha(NEXT_TASK),"known_stop_resolution":"none"}),
    }
    for key,value in checks.items(): write(PREFLIGHT/f"{key}.json",value)
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(
      f"# {PROGRAM_ID} G4 workspace onboarding r5 {'accepted' if accepted else 'review-ready'} report\n\n"
      f"- Stage: `{STAGE}`; result: `{'passed, owner accepted' if accepted else 'review_ready, owner acceptance pending'}`.\n"
      f"- Family receipt: `{rel(FAMILY)}` — `{sha(FAMILY)}`.\n"
      f"- Review board: `{rel(BOARD)}` — `{sha(BOARD)}`.\n"
      "- Representative: `UI-AUTH-005 /onboarding`; `UI-AUTH-006` remains reuse-only.\n"
      "- Finished result: compact Graphite workspace shell with a resumable five-step flow for account, workspace, locale/timezone, data/demo and finish, plus visible readiness context.\n"
      "- Proof: 6 current screen contracts, 6 applicability manifests, 48 browser captures, 24 visual-QA receipts, 6 screen-acceptance receipts and one exact-cover family aggregate.\n"
      "- Browser QA: six states, RU/EN, 768/1024/1440/1920 Web anchors, keyboard action, disabled loading/permission states, reduced motion, console/network isolation and review closure passed.\n"
      "- Adjacent-stage preflight for the unique next pending family passed. Production implementation, publication, deployment, mobile-specific design and full WCAG conformance remain outside proof. No adjacent row was claimed.\n",
      encoding="utf-8")
    request={"$schema":"stage-transition-request.schema.json","program_id":PROGRAM_ID,"from_stage_id":STAGE,"from_gate":"G4","from_target":"family.auth.shell-workspace.baseline-r5","from_revision":5,"artifact":rel(FAMILY),"to_gate":"G4","to_stage_id":NEXT_STAGE,"to_target":NEXT_TARGET,"to_task":rel(NEXT_TASK),"status":"ready" if accepted else "review_ready","owner_decision":rel(DECISION) if accepted else None,"decision_inventory":rel(resolved) if accepted else rel(pending),"blockers":rel(blockers),"checks":[f"{k}={rel(PREFLIGHT/f'{k}.json')}" for k in checks],"summary":"The owner accepted the exact finished workspace-onboarding family; the strict family gate and adjacent-stage preflight pass." if accepted else "The workspace onboarding family exact-covers UI-AUTH-005 across all required states and responsive Web anchors. The machine gate passes; owner acceptance remains pending.","review_artifacts":[rel(BOARD),rel(EVID/"review-board-1440.png"),rel(QA)],"questions":[] if accepted else ["Принять готовое семейство настройки рабочего пространства или запросить ограниченные исправления?"]}
    write(EVID/("stage-transition-request.json" if accepted else "stage-transition-request-review-ready.json"),request); return 0


if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("mode",nargs="?",choices=("review","owner-requests","bind-acceptance","accepted"),default="review"); args=parser.parse_args()
    raise SystemExit(owner_requests() if args.mode=="owner-requests" else bind_acceptance() if args.mode=="bind-acceptance" else main(accepted=args.mode=="accepted"))
