#!/usr/bin/env python3
"""Synchronize current-authority G3/G4 prompts with the live visual authority."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
LEDGER = DIR / "stage-ledger.md"
PROGRAM = DIR / "ui-design-program.json"
FIELDS = (
    "source_visual_ref", "source_visual_sha256", "source_evidence_mode",
    "owner_decision_ref", "screen_acceptance_scope", "visual_language_scope",
    "reusable_foundation_scope", "inheritance_policy", "mobile_scope",
)
sys.path.insert(0, "/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
from validate_stage_ledger import parse_ledger  # noqa: E402


def set_line(text: str, key: str, value: str, insert_before: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*.*$")
    matches = pattern.findall(text)
    if len(matches) > 1:
        raise ValueError(f"prompt has duplicate {key}")
    if matches:
        return pattern.sub(f"{key}: {value}", text)
    marker = re.compile(rf"(?m)^{re.escape(insert_before)}:")
    if not marker.search(text):
        raise ValueError(f"prompt lacks unique insertion marker {insert_before}")
    return marker.sub(f"{key}: {value}\n{insert_before}:", text, count=1)


def main() -> int:
    parsed, errors = parse_ledger(LEDGER)
    if errors: raise ValueError("ledger parse failed: " + "; ".join(errors))
    authority = json.loads(PROGRAM.read_text(encoding="utf-8"))["visual_authority"]
    changed = []
    for row in parsed["rows"]:
        stage_id = row["Stage instance"]
        if row["Gate"] not in {"G3", "G4"} or parsed["details"][stage_id].get("current_authority") == "false":
            continue
        path = ROOT / row["Prompt"]
        text = path.read_text(encoding="utf-8")
        text = set_line(text, "owner_review_target", "finished_visuals_only", "plan_doc")
        for key in reversed(FIELDS):
            value = authority.get(key)
            if not isinstance(value, str) or not value:
                raise ValueError(f"live visual authority lacks {key}")
            text = set_line(text, key, value, "plan_doc")
        path.write_text(text, encoding="utf-8")
        changed.append(row["Prompt"])
    print(json.dumps({"status": "passed", "synchronized_prompts": len(changed), "paths": changed}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
